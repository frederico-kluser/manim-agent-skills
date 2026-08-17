"""Cenas de exemplo — servem de teste do ambiente e de modelo para agentes.

Renderize todas:

    python tools/batch_render.py scenes/exemplos.py -q m --codec nvenc -j 2

Ou uma só:

    bin/mx render scenes/exemplos.py Pitagoras -q h --codec nvenc --json
"""

from __future__ import annotations

import numpy as np
from manim import *


class OlaManim(Scene):
    """Menor cena útil: texto, fórmula e uma forma."""

    def construct(self):
        titulo = Text("Manim está funcionando", font_size=44)
        eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=64, color=YELLOW)
        c = Circle(radius=1.2).set_stroke(BLUE_D, 6).set_fill(BLUE_E, 0.35)

        self.play(Write(titulo))
        self.play(titulo.animate.to_edge(UP))
        self.play(Create(c))
        self.play(FadeIn(eq.next_to(c, DOWN, buff=0.8)))
        self.wait(0.6)


class Pitagoras(Scene):
    """Isolamento de submobjects com `{{ }}` e TransformMatchingTex."""

    def construct(self):
        a = MathTex(r"{{a^2}} + {{b^2}} = {{c^2}}", font_size=72)
        b = MathTex(r"{{a^2}} = {{c^2}} - {{b^2}}", font_size=72)

        a.set_color_by_tex("a^2", BLUE_D)
        a.set_color_by_tex("b^2", GREEN_C)
        a.set_color_by_tex("c^2", RED_C)

        self.play(Write(a))
        self.wait(0.4)
        self.play(TransformMatchingTex(a, b), run_time=1.6)
        self.wait(0.6)


class TangenteViva(Scene):
    """ValueTracker + always_redraw: a reta tangente corre pela parábola."""

    def construct(self):
        ax = Axes(
            x_range=[-3, 3, 1], y_range=[-1, 9, 2],
            x_length=10, y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 22},
        )
        f = ax.plot(lambda x: x**2, color=BLUE)
        rotulo = ax.get_graph_label(f, MathTex("x^2"), x_val=2.4, direction=UR)

        self.play(Create(ax), Create(f), Write(rotulo))

        x = ValueTracker(-2.4)
        ponto = always_redraw(lambda: Dot(ax.i2gp(x.get_value(), f), color=YELLOW))
        tang = always_redraw(
            lambda: ax.get_secant_slope_group(
                x=x.get_value(), graph=f, dx=0.001,
                secant_line_color=YELLOW, secant_line_length=4,
            )
        )
        leitura = always_redraw(
            lambda: MathTex(
                rf"f'({x.get_value():.2f}) = {2 * x.get_value():.2f}",
                font_size=36,
            ).to_corner(UL)
        )

        self.add(ponto, tang, leitura)
        self.play(x.animate.set_value(2.4), run_time=4, rate_func=linear)
        self.wait(0.5)


class LousaBranca(Scene):
    """Tema claro. Note os `set_default` ANTES de qualquer Mobject."""

    def construct(self):
        self.camera.background_color = "#FFFFFF"
        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        VMobject.set_default(color=BLACK)

        t = Text("Lousa branca", font_size=48)
        eq = MathTex(r"\int_0^1 x^2\,dx = \frac{1}{3}", font_size=56)
        eq.set_color_by_tex("frac", BLUE_E)

        self.play(Write(t))
        self.play(t.animate.to_edge(UP))
        self.play(Write(eq))
        self.wait(0.6)


class Superficie3D(ThreeDScene):
    """Cena 3D com câmera orbitando e texto fixo na tela."""

    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-2, 2])
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=0.85)

        sup = Surface(
            lambda u, v: axes.c2p(u, v, 0.8 * np.sin(u) * np.cos(v)),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=(22, 22),
            fill_opacity=0.75,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        titulo = Text("z = sin(u)·cos(v)", font_size=32)
        self.add_fixed_in_frame_mobjects(titulo)
        titulo.to_corner(UL)

        self.add(axes)
        self.play(Create(sup), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.3, about="theta")
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(0.3)


class Cascata(Scene):
    """LaggedStart e rate functions — controle de ritmo."""

    def construct(self):
        formas = VGroup(
            *[
                RegularPolygon(n, radius=0.55)
                .set_stroke(width=4)
                .set_fill(opacity=0.4)
                .set_color_by_gradient(BLUE_D, TEAL_C)
                for n in range(3, 10)
            ]
        ).arrange(RIGHT, buff=0.45)

        self.play(LaggedStart(*[GrowFromCenter(m) for m in formas], lag_ratio=0.15))
        self.play(
            LaggedStart(
                *[m.animate.rotate(PI / 3).set_color(YELLOW) for m in formas],
                lag_ratio=0.08,
            ),
            run_time=2,
        )
        self.play(
            formas.animate.arrange(RIGHT, buff=0.1).scale(0.8),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait(0.4)
