---
name: manim-3d-camera
description: >-
  Cenas 3D e controle de câmera no Manim — ThreeDScene, MovingCameraScene,
  ZoomedScene, orientação por phi/theta/gamma, rotação ambiente, zoom,
  pan, superfícies paramétricas, sólidos, e como manter texto legível em
  3D. Use ao criar animação tridimensional, girar a câmera em torno de um
  objeto, dar zoom, seguir um elemento, plotar superfície ou campo vetorial
  3D, ou quando a câmera não se mover / o texto aparecer deformado.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# 3D e câmera

## Escolha a classe de cena certa

| Classe | Para quê |
|---|---|
| `Scene` | 2D. A câmera é fixa. |
| `MovingCameraScene` | 2D com câmera que anda/dá zoom (`self.camera.frame`) |
| `ThreeDScene` | 3D com câmera orbital (phi/theta/gamma) |
| `ZoomedScene` | 2D com uma "lupa" num inset |
| `ThreeDScene` + `MovingCameraScene` | não combine; escolha uma |

Em `Scene` comum, `self.camera.frame` **não existe** — é o erro mais comum
de câmera.

## `ThreeDScene`

```python
from manim import *

class Demo3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-2, 2])
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.9)
        self.add(axes)

        sup = Surface(
            lambda u, v: axes.c2p(u, v, np.sin(u) * np.cos(v)),
            u_range=[-3, 3], v_range=[-3, 3],
            resolution=(24, 24),
            fill_opacity=0.7, checkerboard_colors=[BLUE_D, BLUE_E],
        )
        self.play(Create(sup), run_time=2)

        # órbita automática
        self.begin_ambient_camera_rotation(rate=0.25, about="theta")
        self.wait(5)
        self.stop_ambient_camera_rotation()

        # movimento explícito
        self.move_camera(phi=40 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()
```

Os ângulos:

- **`phi`** — inclinação a partir do eixo Z. `0` = de cima; `90°` = de lado.
  Comece em `60–75°`.
- **`theta`** — rotação em torno de Z (a órbita horizontal).
- **`gamma`** — rolagem da câmera.
- **`zoom`** — `<1` afasta, `>1` aproxima.
- **`frame_center`** — para onde a câmera olha.

Sempre em **radianos**; use `* DEGREES`.

```bash
bin/mx show ThreeDScene --own-only     # todos os métodos de câmera
```

## Texto legível em 3D

Texto plano em cena 3D fica deitado no plano XY e ilegível. Duas soluções:

```python
# 1. fixar na tela (HUD) — não gira com a câmera
titulo = Text("Superfície")
self.add_fixed_in_frame_mobjects(titulo)
titulo.to_corner(UL)

# 2. orientar o texto para a câmera
lbl = Text("z").rotate(PI / 2, axis=RIGHT)
```

Também existe `self.add_fixed_orientation_mobjects(mob)`, que mantém o
objeto na posição 3D mas sempre virado para a câmera.

## Sólidos e superfícies

```python
Sphere(radius=1, resolution=(24, 24))
Cube(side_length=2, fill_opacity=0.7)
Cylinder(radius=1, height=2)
Cone(base_radius=1, height=2)
Torus(major_radius=2, minor_radius=0.5)
Prism(dimensions=[2, 1, 3])
Dodecahedron()
Arrow3D(start=ORIGIN, end=[1, 1, 1])
Line3D(start=ORIGIN, end=[2, 0, 0])
Surface(func, u_range=..., v_range=..., resolution=(n, m))
```

```bash
awk -F'\t' '$1=="class" && $3=="mobject/3d" {print $2"\t"$4}' api/manim-ce-index.tsv
```

**`resolution` domina o custo.** `(24, 24)` = 576 quads; `(64, 64)` = 4096.
Ajuste em `-q l` antes de subir a qualidade.

## `MovingCameraScene` — câmera 2D

```python
class Zoom(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        grupo = VGroup(*[Dot(RIGHT * i) for i in range(-5, 6)])
        self.add(grupo)

        self.play(self.camera.frame.animate.scale(0.4).move_to(grupo[8]))
        self.wait()
        self.play(self.camera.frame.animate.set(width=20))
        self.play(Restore(self.camera.frame))
```

`self.camera.frame` é um Mobject: aceita `.animate`, `.move_to`, `.scale`,
`.set(width=)`, `.shift`, `.rotate`.

Seguir um objeto continuamente:

```python
self.camera.frame.add_updater(lambda f: f.move_to(alvo.get_center()))
self.add(self.camera.frame)     # necessário para os updaters rodarem
...
self.camera.frame.clear_updaters()
```

## `ZoomedScene` — lupa

```python
class Lupa(ZoomedScene):
    def __init__(self, **kwargs):
        super().__init__(zoom_factor=0.3, zoomed_display_height=3,
                         zoomed_display_width=4, **kwargs)

    def construct(self):
        self.add(Text("detalhe fino", font_size=12))
        self.activate_zooming(animate=True)
        self.play(self.zoomed_camera.frame.animate.shift(RIGHT))
```

## 3D interativo — use o ManimGL

Para girar a cena com o mouse enquanto desenvolve, o ManimGL (wgpu/Vulkan)
é muito melhor:

```bash
bin/manimgl scenes/demo3d.py Demo3D        # abre janela; arraste para orbitar
```

Teclas: `d` pan 3D · `f` pan · `r` reset · `z` grab no eixo Z · `s` select.
Sintaxe diferente — ver skill `manimgl-3b1b`.

## Performance em 3D

Cena 3D é pesada em geometria, então quem ajuda é o **renderer**, não o
codec:

```bash
bin/mx render cena.py Demo3D --renderer opengl --codec nvenc -q h
```

Medido nesta máquina: `opengl` economiza ~19% vs `cairo` em cena pesada de
geometria. Detalhes na skill `manim-gpu-encoding`.

Cuidado com os 8 GiB de VRAM: 4K + superfícies de alta resolução estouram.
Renderize 4K no `cairo`.

## Armadilhas

- **`self.camera.frame` só existe em `MovingCameraScene`/`ThreeDScene`.**
  Em `Scene` dá `AttributeError`.
- **Graus vs radianos.** `phi=70` são ~11 voltas; escreva `70 * DEGREES`.
- **`begin_ambient_camera_rotation` sem `self.wait()` depois** não produz
  movimento — a rotação acontece durante o tempo que passa.
- **Esqueceu `stop_ambient_camera_rotation`** e a câmera continua girando
  nas animações seguintes.
- **Texto 3D ilegível** — use `add_fixed_in_frame_mobjects`.
- **`Surface` com `resolution` alta** trava a renderização. Comece baixo.
- **Updater na câmera não roda** se o frame não estiver adicionado à cena
  (`self.add(self.camera.frame)`).
- **`z_index` não ordena em 3D** — a profundidade vem da geometria.
