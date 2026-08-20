#!/usr/bin/env python3
"""confere_borda.py — a tinta encosta na borda do quadro?

Corte na borda é o defeito de layout mais comum do Manim e **não levanta
exceção nenhuma**: o cairo simplesmente não desenha o que caiu fora do buffer
de pixels. Pior, o teste que a biblioteca oferece (`Mobject.is_off_screen()`)
só é `True` quando o objeto está INTEIRAMENTE fora — um título cortado ao meio
devolve `False`. Ver `manim-verificacao-visual` §5.1.

Este script mede o que sobrou no PIXEL, que é a única evidência que não mente:

1. a caixa de toda a tinta do quadro (`bbox`), e a distância dela para cada
   uma das quatro bordas, em px e em % da dimensão;
2. quanta tinta existe DENTRO da faixa de `--margem` px de cada borda.

Uso
---
    python confere_borda.py quadro.png
    python confere_borda.py saida/*.png --margem 32          # margem exigida
    python confere_borda.py quadro.png --tolerancia 200      # px de tinta tolerados
    python confere_borda.py quadro.png --escuro

Código de saída 1 se qualquer faixa tiver mais que `--tolerancia` pixels de
tinta. `--tolerancia 0` é estrito demais para cena com fundo de grade que vai
até a borda de propósito — nesse caso use `--margem 0` e leia só o bbox.

Régua de tradução, para converter px em unidades de palco: o palco padrão do
ManimCE é 14,222 × 8,0 unidades. Em 1920×1080, **1 unidade = 135 px**; em
854×480, 1 unidade = 60 px. Uma margem de 0,5 unidade (o `buff` padrão de
`to_edge`) são 67,5 px em 1080p.

Depende só de `numpy` e `Pillow`. Não renderiza, não chama ffmpeg.

ESTE ARQUIVO NÃO FOI EXECUTADO na sessão em que foi escrito.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

CLARO_PADRAO = 235
ESCURO_PADRAO = 20


def luminancia(caminho: Path) -> np.ndarray:
    return np.asarray(Image.open(caminho).convert("L"), dtype=np.int16)


def fundo_e_claro(lum: np.ndarray, canto: int = 8) -> bool:
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
    return (lum < limiar) if claro else (lum > limiar)


def analisa(mascara: np.ndarray, margem: int) -> dict:
    """Caixa da tinta + contagem por faixa de borda.

    A imagem é indexada [linha, coluna] = [y de cima para baixo, x].
    """
    altura, largura = mascara.shape
    linhas = np.flatnonzero(mascara.any(axis=1))
    colunas = np.flatnonzero(mascara.any(axis=0))
    if linhas.size == 0:
        return {"vazio": True, "altura": altura, "largura": largura}

    topo, base = int(linhas[0]), int(linhas[-1])
    esq, dir_ = int(colunas[0]), int(colunas[-1])

    faixas = {"topo": 0, "base": 0, "esquerda": 0, "direita": 0}
    if margem > 0:
        m = min(margem, altura // 2, largura // 2)
        faixas["topo"] = int(mascara[:m, :].sum())
        faixas["base"] = int(mascara[-m:, :].sum())
        faixas["esquerda"] = int(mascara[:, :m].sum())
        faixas["direita"] = int(mascara[:, -m:].sum())

    return {
        "vazio": False,
        "altura": altura,
        "largura": largura,
        "folga_topo": topo,
        "folga_base": altura - 1 - base,
        "folga_esquerda": esq,
        "folga_direita": largura - 1 - dir_,
        "faixas": faixas,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("imagens", nargs="+")
    p.add_argument("--margem", type=int, default=24, help="faixa de borda em px (padrão 24)")
    p.add_argument(
        "--tolerancia",
        type=int,
        default=0,
        help="px de tinta tolerados dentro da faixa (padrão 0)",
    )
    p.add_argument("--limiar", type=int, default=None)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--claro", action="store_true")
    g.add_argument("--escuro", action="store_true")
    args = p.parse_args()

    reprovou = False
    for bruto in args.imagens:
        caminho = Path(bruto)
        if not caminho.exists():
            print(f"{caminho}: NÃO EXISTE")
            reprovou = True
            continue

        lum = luminancia(caminho)
        claro = True if args.claro else (False if args.escuro else fundo_e_claro(lum))
        limiar = args.limiar if args.limiar is not None else (
            CLARO_PADRAO if claro else ESCURO_PADRAO
        )
        r = analisa(mascara_tinta(lum, claro, limiar), args.margem)

        print(f"\n{caminho}  ({r['largura']}x{r['altura']}, fundo {'claro' if claro else 'escuro'})")
        if r["vazio"]:
            print("  QUADRO SEM TINTA NENHUMA — ver mede_tinta.py")
            reprovou = True
            continue

        for lado, chave, total in (
            ("topo    ", "folga_topo", r["altura"]),
            ("base    ", "folga_base", r["altura"]),
            ("esquerda", "folga_esquerda", r["largura"]),
            ("direita ", "folga_direita", r["largura"]),
        ):
            folga = r[chave]
            estourou = r["faixas"][lado.strip()] > args.tolerancia
            reprovou |= estourou
            print(
                f"  folga {lado}: {folga:>4} px ({folga / total * 100:5.2f}%)"
                f"   tinta na faixa de {args.margem}px: {r['faixas'][lado.strip()]:>6}"
                f"   {'ENCOSTA NA BORDA' if estourou else 'ok'}"
            )

    return 1 if reprovou else 0


if __name__ == "__main__":
    sys.exit(main())
