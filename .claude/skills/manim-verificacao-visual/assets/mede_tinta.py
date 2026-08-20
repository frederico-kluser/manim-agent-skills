#!/usr/bin/env python3
"""mede_tinta.py — quanta TINTA existe num quadro.

Responde a UMA pergunta: este PNG está vazio?

Um quadro vazio não é um erro. É um `FadeOut` que fechou a cena, um texto na
cor do fundo, um `fill_opacity=0`, um mobject que ficou fora do quadro. Nenhum
desses casos levanta exceção, nenhum aparece no exit code, e o pôster que vai
para o PDF de backup sai em página branca.

Uso
---
    python mede_tinta.py public/videos/*.png
    python mede_tinta.py saida/*.png --minimo 1.0          # % de tinta exigida
    python mede_tinta.py cena.png --escuro                 # força fundo escuro
    python mede_tinta.py cena.png --limiar 200             # o corte de luminância

Saída: uma linha por arquivo, e código de saída 1 se alguma ficar abaixo de
`--minimo`. Serve em pre-commit e em CI.

Referência de calibragem (medida no deck consumidor `~/Projects/aulas`,
2026-08-19, NÃO reproduzida aqui): a cobertura de tinta das cenas em produção
vai de **2,9 %** a **21 %**. Abaixo de **1 %** é fade-out disfarçado.

Depende só de `numpy` e `Pillow` — os dois já estão no `.venv` deste projeto.
Não renderiza nada, não chama ffmpeg, não abre GPU.

ESTE ARQUIVO NÃO FOI EXECUTADO na sessão em que foi escrito (proibição de
CPU/GPU). Ele é referência de API e de método; confira a primeira saída.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Luminância ITU-R 601-2 — é a mesma conta que o `convert("L")` do Pillow faz.
CLARO_PADRAO = 235  # em fundo claro, tinta é pixel MAIS ESCURO que isto
ESCURO_PADRAO = 20  # em fundo escuro, tinta é pixel MAIS CLARO que isto


def luminancia(caminho: Path) -> np.ndarray:
    """Devolve o quadro como luminância 0..255, int16 (para subtrair sem estourar)."""
    return np.asarray(Image.open(caminho).convert("L"), dtype=np.int16)


def fundo_e_claro(lum: np.ndarray, canto: int = 8) -> bool:
    """Decide claro × escuro pela MEDIANA dos quatro cantos.

    Canto é a região que quase nunca tem conteúdo. A mediana (e não a média)
    sobrevive a um logo no canto superior direito.
    """
    c = canto
    amostra = np.concatenate(
        [
            lum[:c, :c].ravel(),
            lum[:c, -c:].ravel(),
            lum[-c:, :c].ravel(),
            lum[-c:, -c:].ravel(),
        ]
    )
    return float(np.median(amostra)) > 128.0


def mascara_tinta(lum: np.ndarray, claro: bool, limiar: int) -> np.ndarray:
    """Máscara booleana do que é TINTA — o sinal inverte com o fundo."""
    return (lum < limiar) if claro else (lum > limiar)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("imagens", nargs="+", help="PNG/JPG a medir")
    p.add_argument(
        "--minimo",
        type=float,
        default=1.0,
        help="%% mínimo de tinta para o quadro ser considerado não-vazio (padrão 1.0)",
    )
    p.add_argument("--limiar", type=int, default=None, help="corte de luminância 0..255")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--claro", action="store_true", help="força fundo claro")
    g.add_argument("--escuro", action="store_true", help="força fundo escuro")
    args = p.parse_args()

    reprovou = False
    print(f"{'arquivo':<44} {'fundo':<7} {'tinta':>7}  {'min':>4} {'max':>4}  veredito")
    for bruto in args.imagens:
        caminho = Path(bruto)
        if not caminho.exists():
            print(f"{caminho.name:<44} {'-':<7} {'-':>7}  {'-':>4} {'-':>4}  NÃO EXISTE")
            reprovou = True
            continue

        lum = luminancia(caminho)
        if args.claro:
            claro = True
        elif args.escuro:
            claro = False
        else:
            claro = fundo_e_claro(lum)

        limiar = args.limiar if args.limiar is not None else (
            CLARO_PADRAO if claro else ESCURO_PADRAO
        )
        pct = float(mascara_tinta(lum, claro, limiar).mean()) * 100.0
        ok = pct >= args.minimo
        reprovou |= not ok
        print(
            f"{caminho.name:<44} {'claro' if claro else 'escuro':<7} "
            f"{pct:6.2f}% {int(lum.min()):>4} {int(lum.max()):>4}  "
            f"{'ok' if ok else 'QUADRO QUASE VAZIO'}"
        )

    return 1 if reprovou else 0


if __name__ == "__main__":
    sys.exit(main())
