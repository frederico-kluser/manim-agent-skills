#!/usr/bin/env python3
"""guarda_enquadramento.py — o enquadramento conferido SEM olhar pixel nenhum.

Por que este arquivo existe: o teste que a biblioteca oferece não é o teste que
você quer.

    # manim/mobject/mobject.py:1744-1752  [FONTE, ManimCE 0.21.0]
    def is_off_screen(self) -> bool:
        if self.get_left()[0]  >  config["frame_x_radius"]: return True
        if self.get_right()[0] < -config["frame_x_radius"]: return True
        if self.get_bottom()[1] >  config["frame_y_radius"]: return True
        return self.get_top()[1] < -config["frame_y_radius"]

`is_off_screen()` só é `True` quando o mobject está **inteiramente** fora do
quadro. Um título cortado ao meio devolve `False`. `Camera.is_in_frame`
(`camera/camera.py:485-510`) é a negação literal dos mesmos quatro testes — com
a diferença de que ele respeita `self.frame_center`, e o `is_off_screen` do
Mobject **não**: sob `MovingCameraScene` com a câmera deslocada, `is_off_screen`
mede contra o quadro da ORIGEM e mente.

O que este módulo oferece é o teste de CONTENÇÃO — "cabe inteiro, com margem?" —
e o relatório de quanto estourou, em unidades de palco e em píxeis.

Uso como biblioteca
-------------------
    from guarda_enquadramento import cabe, estouro, relatorio

    assert cabe(titulo, margem=0.3), estouro(titulo, margem=0.3)
    relatorio(self.mobjects)                 # tabela do palco inteiro

Uso como guarda de cena (falha no primeiro `play` que estoura)
--------------------------------------------------------------
    class MinhaCena(GuardaEnquadramento, Scene):
        MARGEM = 0.25
        def construct(self):
            ...

O guarda roda DEPOIS de cada `play`/`wait`/`add`. Ele não custa render: são
comparações de bounding box, na mesma passagem que já ia acontecer. Deixe-o
ligado enquanto escreve a cena e desligue (`MARGEM = None`) na entrega, se a
cena tiver algo que sai do quadro de propósito.

Limitações honestas
-------------------
1. A caixa vem dos PONTOS da curva. A **espessura do traço** é desenhada para
   FORA deles: um `Line(stroke_width=8)` colado no limite perde metade do traço
   e este módulo aprova. Use uma margem maior que `stroke_width / 2` convertida
   em unidades (§ regra abaixo).
2. Ponto de controle de Bézier pode ficar fora do desenho visível — a caixa
   pode ser levemente PESSIMISTA em curvas fechadas.
3. Ele não enxerga sobreposição, cor, nem legibilidade. Isso é pixel, e mora em
   `mede_tinta.py` / `confere_borda.py` e na skill `manim-color-theming`.

Régua de conversão
------------------
Palco padrão do ManimCE: 14,222 × 8,0 unidades (`frame_x_radius = 7,111`,
`frame_y_radius = 4,0`). Em 1920×1080, **1 unidade = 135 px**. Logo
`stroke_width=8` ocupa 8 px ⇒ 0,03 unidade para cada lado. O `buff` padrão de
`to_edge` é 0,5 unidade = 67,5 px em 1080p.

ESTE ARQUIVO NÃO FOI EXECUTADO na sessão em que foi escrito (proibição de
CPU/GPU). As assinaturas foram conferidas no índice estático de `api/`.
"""

from __future__ import annotations

from typing import Any, Iterable

import numpy as np
from manim import Mobject, config


# ─────────────────────────────────────────────────────────────────────────────
# Limites do quadro
# ─────────────────────────────────────────────────────────────────────────────
def limites() -> tuple[float, float, float, float]:
    """(x_min, x_max, y_min, y_max) do quadro ATUAL, lidos da config.

    `config.frame_x_radius` / `frame_y_radius` são propriedades reais de
    `ManimConfig` (`_config/utils.py:1149-1166`) e acompanham `frame_width` /
    `frame_height`. `config.left_side`, `right_side`, `top` e `bottom` devolvem
    os mesmos números como vetores.
    """
    rx = float(config.frame_x_radius)
    ry = float(config.frame_y_radius)
    return -rx, rx, -ry, ry


def unidades_por_pixel() -> float:
    """Quantas unidades de palco vale UM pixel, na resolução configurada."""
    return float(config.frame_width) / float(config.pixel_width)


# ─────────────────────────────────────────────────────────────────────────────
# A caixa que interessa: só o que é VISÍVEL
# ─────────────────────────────────────────────────────────────────────────────
def _visivel(m: Mobject) -> bool:
    """Um mobject transparente continua na caixa delimitadora do `VGroup`.

    Esse é um defeito real e medido: um espaçador com opacidade zero deslocou
    um grupo inteiro em 4 px num `VGroup.move_to()`. Posicione e confira pelo
    CORPO visível, não pelo grupo.
    """
    if not m.has_points():
        return False
    preenchimento = getattr(m, "get_fill_opacity", None)
    traco = getattr(m, "get_stroke_opacity", None)
    largura = getattr(m, "get_stroke_width", None)
    if preenchimento is None or traco is None or largura is None:
        return True  # não é VMobject: não dá para julgar, então conta
    return float(preenchimento()) > 0.0 or (
        float(traco()) > 0.0 and float(largura()) > 0.0
    )


def caixa(mob: Mobject, so_visivel: bool = True) -> tuple[float, float, float, float]:
    """(x_min, x_max, y_min, y_max) do mobject, em unidades de palco."""
    membros = [m for m in mob.family_members_with_points() if not so_visivel or _visivel(m)]
    if not membros:
        raise ValueError(f"{mob} não tem nenhum submobject visível com pontos")
    pontos = np.vstack([m.points for m in membros])
    return (
        float(pontos[:, 0].min()),
        float(pontos[:, 0].max()),
        float(pontos[:, 1].min()),
        float(pontos[:, 1].max()),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Os testes
# ─────────────────────────────────────────────────────────────────────────────
def estouro(mob: Mobject, margem: float = 0.0, so_visivel: bool = True) -> dict[str, float]:
    """Quanto o mobject passa de cada borda, em unidades. 0 = não passa.

    Devolve sempre as quatro chaves; some os valores para um veredito único.
    """
    x0, x1, y0, y1 = caixa(mob, so_visivel)
    lx0, lx1, ly0, ly1 = limites()
    return {
        "esquerda": max(0.0, (lx0 + margem) - x0),
        "direita": max(0.0, x1 - (lx1 - margem)),
        "base": max(0.0, (ly0 + margem) - y0),
        "topo": max(0.0, y1 - (ly1 - margem)),
    }


def cabe(mob: Mobject, margem: float = 0.0, so_visivel: bool = True) -> bool:
    """True se o mobject inteiro cabe no quadro respeitando a margem."""
    return not any(estouro(mob, margem, so_visivel).values())


def relatorio(
    mobjects: Iterable[Mobject],
    margem: float = 0.0,
    so_visivel: bool = True,
) -> int:
    """Imprime uma linha por mobject e devolve quantos estouraram."""
    upp = unidades_por_pixel()
    print(
        f"quadro {config.frame_width:.3f}x{config.frame_height:.3f} u "
        f"({config.pixel_width}x{config.pixel_height} px, 1 u = {1 / upp:.1f} px), "
        f"margem exigida {margem} u"
    )
    ruins = 0
    for m in mobjects:
        try:
            e = estouro(m, margem, so_visivel)
        except ValueError:
            print(f"  {type(m).__name__:<22} (sem pontos visíveis)")
            continue
        pior = max(e.values())
        if pior > 0:
            ruins += 1
            lados = ", ".join(f"{k} {v:.3f} u ({v / upp:.0f} px)" for k, v in e.items() if v > 0)
            print(f"  {type(m).__name__:<22} ESTOURA — {lados}")
        else:
            x0, x1, y0, y1 = caixa(m, so_visivel)
            print(
                f"  {type(m).__name__:<22} ok  x[{x0:6.2f},{x1:6.2f}] y[{y0:6.2f},{y1:6.2f}]"
            )
    return ruins


# ─────────────────────────────────────────────────────────────────────────────
# O guarda de cena
# ─────────────────────────────────────────────────────────────────────────────
class GuardaEnquadramento:
    """Mixin: confere o palco depois de cada `add`, `play` e `wait`.

    NÃO herda de `Scene` — de propósito. Uma classe-base que herda de `Scene`
    aparece em `mx scenes` e no descobridor do ManimCE (`issubclass(obj, Scene)`)
    e vira uma cena renderizada por engano. A ordem das bases também importa:
    `class MinhaCena(GuardaEnquadramento, Scene)`, mixin PRIMEIRO — invertida, o
    MRO resolve os métodos em `Scene` e o guarda nunca roda.

    Ver `manim-presentation-parts` §3.2 e §3.3 para o mesmo mecanismo aplicado
    a cenas em partes.
    """

    MARGEM: float | None = 0.0  # None desliga o guarda
    ESTRITO: bool = True  # False só avisa, True levanta AssertionError

    def _confere_palco(self, onde: str) -> None:
        if self.MARGEM is None:
            return
        culpados = []
        for m in self.mobjects:  # type: ignore[attr-defined]
            try:
                e = estouro(m, self.MARGEM)
            except ValueError:
                continue
            if any(e.values()):
                culpados.append((m, e))
        if not culpados:
            return
        linhas = [
            f"  {type(m).__name__}: "
            + ", ".join(f"{k} +{v:.3f} u" for k, v in e.items() if v > 0)
            for m, e in culpados
        ]
        recado = f"[{onde}] {len(culpados)} mobject(s) fora do quadro:\n" + "\n".join(linhas)
        if self.ESTRITO:
            raise AssertionError(recado)
        print(recado)

    def add(self, *mobjects: Any) -> Any:
        r = super().add(*mobjects)  # type: ignore[misc]
        self._confere_palco("add")
        return r

    def play(self, *args: Any, **kwargs: Any) -> Any:
        r = super().play(*args, **kwargs)  # type: ignore[misc]
        self._confere_palco("play")
        return r

    def wait(self, *args: Any, **kwargs: Any) -> Any:
        r = super().wait(*args, **kwargs)  # type: ignore[misc]
        self._confere_palco("wait")
        return r


__all__ = [
    "GuardaEnquadramento",
    "caixa",
    "cabe",
    "estouro",
    "limites",
    "relatorio",
    "unidades_por_pixel",
]
