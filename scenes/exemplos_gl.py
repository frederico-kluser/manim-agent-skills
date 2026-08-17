"""Cenas de exemplo do **ManimGL** (3b1b) — sintaxe `manimlib`, não `manim`.

Este arquivo NÃO roda no ManimCE, e as cenas de `exemplos.py` não rodam
aqui. São bibliotecas diferentes, em venvs diferentes.

    bin/manimgl -w -l scenes/exemplos_gl.py GLOla        # arquivo
    bin/manimgl scenes/exemplos_gl.py GLOla              # janela interativa
    bin/manimgl -w --hd --vcodec hevc_nvenc scenes/exemplos_gl.py GLSuperficie

A saída vai para `media-gl/videos/` (definido em `custom_config.yml`).
"""

from manimlib import *


class GLOla(Scene):
    """Equivalente ao OlaManim do ManimCE — note as diferenças de API."""

    def construct(self):
        titulo = Text("ManimGL funcionando", font_size=44)
        # No GL é `Tex` para matemática; o CE usaria `MathTex`.
        eq = Tex(R"e^{i\pi} + 1 = 0", font_size=64).set_color(YELLOW)
        c = Circle(radius=1.2).set_stroke(BLUE_D, 6).set_fill(BLUE_E, 0.35)

        # `ShowCreation` no GL; `Create` no CE.
        self.play(Write(titulo))
        self.play(titulo.animate.to_edge(UP))
        self.play(ShowCreation(c))
        self.play(FadeIn(eq.next_to(c, DOWN, buff=0.8)))
        self.wait(0.6)


class GLSuperficie(ThreeDScene):
    """3D com a câmera do ManimGL — arraste com o mouse na janela."""

    def construct(self):
        axes = ThreeDAxes()
        surface = ParametricSurface(
            lambda u, v: np.array([u, v, 0.8 * np.sin(u) * np.cos(v)]),
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(32, 32),
        )
        surface.set_color(BLUE_E).set_opacity(0.8)

        frame = self.camera.frame
        frame.set_euler_angles(theta=-30 * DEGREES, phi=70 * DEGREES)

        self.add(axes)
        self.play(ShowCreation(surface), run_time=2)
        self.play(frame.animate.set_euler_angles(theta=60 * DEGREES), run_time=4)
        self.wait(0.3)


class GLInterativa(Scene):
    """Fluxo do 3b1b: descomente `self.embed()` e rode SEM `-w`.

    Isso abre um IPython com a cena viva; `self.play(...)` renderiza na
    janela imediatamente. É o principal motivo para usar ManimGL em vez
    do ManimCE.
    """

    def construct(self):
        grid = NumberPlane()
        dot = Dot(color=YELLOW).scale(2)

        self.play(ShowCreation(grid, lag_ratio=0.02, run_time=2))
        self.play(FadeIn(dot))
        self.play(dot.animate.shift(RIGHT * 3 + UP * 2))

        # self.embed()   # <- descomente para o REPL interativo
        self.wait(0.4)
