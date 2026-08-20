#!/usr/bin/env python3
"""mede_emenda.py — a métrica DIRECIONAL: quanta tinta SUMIU entre dois quadros.

Serve a duas perguntas que parecem diferentes e são a mesma:

* **emenda entre partes** — o primeiro quadro da parte N+1 tem de ser, pixel a
  pixel, o último da parte N. Se alguma coisa desapareceu na troca, o
  apresentador vê o palco piscar exatamente no quadro em que fica falando.
* **regressão visual** — depois de mexer no código, o que SUMIU do quadro em
  relação ao render anterior?

A métrica é **direcional de propósito**. RMS, `abs(a - b)` e SSIM são
simétricos: acusam como defeito a animação seguinte COMEÇANDO, que é o
comportamento certo. Medição do deck consumidor (2026-08-19, NÃO reproduzida
aqui): uma emenda perfeita dava RMS 4,4 e foi julgada defeituosa por uma métrica
simétrica. O único defeito que importa é tinta que SOME.

Em fundo claro, "sumiu" = o pixel CLAREOU:      (b - a) > delta
Em fundo escuro, "sumiu" = o pixel ESCURECEU:   (a - b) > delta

Uso
---
    python mede_emenda.py fim_p3.png inicio_p4.png
    python mede_emenda.py --dir public/videos/
    python mede_emenda.py --dir saida/ --limiar 400 --escuro
    python mede_emenda.py --dir saida/ --extrair          # tira os quadros do mp4 (PyAV)

Convenção de nomes esperada no modo `--dir` (a mesma do pipeline em partes):

    <base>-p<N>.mp4          o vídeo da parte N
    <base>-p<N>.png          o ÚLTIMO quadro da parte N   (pôster)
    <base>-p<N>-inicio.png   o PRIMEIRO quadro da parte N

Troque com `--sufixo-fim` / `--sufixo-inicio` se o seu pipeline nomeia de outro
jeito.

Limiar
------
**400 px em 1920×1080 (2 073 600 px), fundo claro** — medição do deck, NÃO
reproduzida aqui. Abaixo disso é antialiasing; acima, alguma coisa desapareceu.
Emendas boas ficavam entre 4 e 27 px; a pior aprovada foi 118 px (folga de
3,4×). O limiar escala com a ÁREA, e este script já faz essa conta: o valor de
`--limiar` é sempre expresso em píxeis de 1080p.

Falso positivo que você vai encontrar
-------------------------------------
Se você editou um ato e re-renderizou SÓ a parte dele, a parte vizinha no disco
ainda é a versão velha e a medição estoura. **Investigue antes de "consertar" a
cena** — foi assim que se achou um defeito real (um elemento invisível entrando
na caixa delimitadora e deslocando um grupo em 4 px). A ordem certa é:
re-renderize o alcance inteiro, DEPOIS meça.

Depende de `numpy` e `Pillow`. A opção `--extrair` também usa `av` (PyAV), que
o ManimCE já traz — ela decodifica vídeo, então NÃO é grátis; sem ela o script
só lê PNG que já existe.

ESTE ARQUIVO NÃO FOI EXECUTADO na sessão em que foi escrito.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

AREA_REFERENCIA = 1920 * 1080
DELTA_PADRAO = 24  # degraus de luminância que separam "mudou" de antialiasing


def luminancia_png(caminho: Path) -> np.ndarray:
    return np.asarray(Image.open(caminho).convert("L"), dtype=np.int16)


def luminancia_rgb(rgb: np.ndarray) -> np.ndarray:
    """Mesma conta do `convert('L')` do Pillow (ITU-R 601-2)."""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return (0.299 * r + 0.587 * g + 0.114 * b).astype(np.int16)


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


def sumiu(antes: np.ndarray, depois: np.ndarray, claro: bool, delta: int) -> int:
    """Píxeis que tinham tinta em `antes` e não têm em `depois`."""
    if antes.shape != depois.shape:
        raise SystemExit(
            f"quadros de tamanhos diferentes: {antes.shape} vs {depois.shape} — "
            "renderize os dois na mesma qualidade antes de medir"
        )
    diferenca = (depois - antes) if claro else (antes - depois)
    return int((diferenca > delta).sum())


def extremos_do_video(mp4: Path) -> tuple[np.ndarray, np.ndarray]:
    """(primeiro, último) quadro como luminância. Usa PyAV — decodifica o vídeo."""
    import av  # noqa: PLC0415 — importa só quando `--extrair` é pedido

    primeiro = ultimo = None
    with av.open(str(mp4)) as recipiente:
        fluxo = recipiente.streams.video[0]
        fluxo.thread_type = "AUTO"
        for quadro in recipiente.decode(video=0):
            arranjo = luminancia_rgb(quadro.to_ndarray(format="rgb24"))
            if primeiro is None:
                primeiro = arranjo
            ultimo = arranjo
    if primeiro is None:
        raise SystemExit(f"{mp4}: nenhum quadro decodificado — o vídeo está vazio")
    return primeiro, ultimo


def modo_par(a: Path, b: Path, args) -> int:
    la, lb = luminancia_png(a), luminancia_png(b)
    claro = True if args.claro else (False if args.escuro else fundo_e_claro(la))
    n = sumiu(la, lb, claro, args.delta)
    teto = args.limiar * la.size / AREA_REFERENCIA
    print(f"{a.name} -> {b.name}: {n} px sumiram (teto {teto:.0f}) "
          f"{'REPROVA' if n > teto else 'ok'}")
    return 1 if n > teto else 0


def modo_diretorio(args) -> int:
    diretorio = Path(args.dir)
    padrao = re.compile(args.padrao)
    ultimo_indice: dict[str, int] = {}
    for mp4 in diretorio.glob("*.mp4"):
        m = padrao.match(mp4.stem)
        if m:
            base, n = m.group(1), int(m.group(2))
            ultimo_indice[base] = max(ultimo_indice.get(base, 0), n)

    if not ultimo_indice:
        raise SystemExit(
            f"nenhum arquivo casou com {args.padrao!r} em {diretorio} — "
            "a lista de partes tem de sair do DISCO, nunca de um mapa escrito à mão"
        )

    pior = 0
    reprovou = False
    for base, total in sorted(ultimo_indice.items()):
        for k in range(1, total):
            fim = diretorio / f"{base}-p{k}{args.sufixo_fim}.png"
            ini = diretorio / f"{base}-p{k + 1}{args.sufixo_inicio}.png"

            if fim.exists() and ini.exists():
                la, lb = luminancia_png(fim), luminancia_png(ini)
            elif args.extrair:
                _, la = extremos_do_video(diretorio / f"{base}-p{k}.mp4")
                lb, _ = extremos_do_video(diretorio / f"{base}-p{k + 1}.mp4")
            else:
                print(f"  {base} p{k}->p{k + 1}: PNG faltando "
                      f"({fim.name} / {ini.name}) — use --extrair")
                reprovou = True
                continue

            claro = True if args.claro else (False if args.escuro else fundo_e_claro(la))
            n = sumiu(la, lb, claro, args.delta)
            teto = args.limiar * la.size / AREA_REFERENCIA
            pior = max(pior, n)
            if n > teto:
                reprovou = True
                print(f"  EMENDA COM PERDA: {base} p{k}->p{k + 1}: "
                      f"{n} px sumiram (teto {teto:.0f})")

    print(f"pior emenda: {pior} px  ({'REPROVA' if reprovou else 'ok'})")
    return 1 if reprovou else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("quadros", nargs="*", help="ANTES.png DEPOIS.png (modo par)")
    p.add_argument("--dir", help="diretório com <base>-p<N>.mp4 e os PNG (modo lote)")
    p.add_argument("--padrao", default=r"(.+)-p(\d+)$", help="regex base/índice do nome")
    p.add_argument("--sufixo-fim", default="", dest="sufixo_fim")
    p.add_argument("--sufixo-inicio", default="-inicio", dest="sufixo_inicio")
    p.add_argument("--limiar", type=float, default=400.0,
                   help="px tolerados, expressos em 1080p (padrão 400)")
    p.add_argument("--delta", type=int, default=DELTA_PADRAO,
                   help="degraus de luminância que contam como mudança (padrão 24)")
    p.add_argument("--extrair", action="store_true",
                   help="decodifica os quadros do mp4 com PyAV quando faltar PNG")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--claro", action="store_true")
    g.add_argument("--escuro", action="store_true")
    args = p.parse_args()

    if args.dir:
        return modo_diretorio(args)
    if len(args.quadros) == 2:
        return modo_par(Path(args.quadros[0]), Path(args.quadros[1]), args)
    p.error("passe dois PNG, ou --dir")
    return 2


if __name__ == "__main__":
    sys.exit(main())
