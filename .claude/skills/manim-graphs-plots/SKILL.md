---
name: manim-graphs-plots
description: >-
  Eixos, gráficos e visualização de dados no Manim — Axes, NumberPlane,
  NumberLine, PolarPlane, ComplexPlane, plot de funções, curvas
  paramétricas, área sob a curva, retas tangentes, riemann, BarChart,
  Table, Matrix e grafos (Graph/DiGraph). Use ao plotar função, desenhar
  plano cartesiano, animar uma curva sendo traçada, marcar pontos,
  rotular eixos, mostrar dados tabulares ou matrizes. Cobre a conversão
  entre coordenadas do gráfico e coordenadas da cena, que é a origem da
  maioria dos erros de posicionamento.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Eixos, gráficos e dados

## A regra que evita a maioria dos bugs

Coordenadas do **gráfico** e coordenadas da **cena** são espaços diferentes.
Nunca posicione um objeto num gráfico com `move_to(np.array([x, y, 0]))`.
Converta:

```python
ax.c2p(x, y)      # coords do gráfico -> ponto da cena  (coords_to_point)
ax.p2c(ponto)     # ponto da cena -> coords do gráfico
```

```python
ax = Axes(x_range=[0, 10], y_range=[0, 100, 20])
dot = Dot(ax.c2p(3, 45))          # certo
dot = Dot(np.array([3, 45, 0]))   # ERRADO: cai muito fora do quadro
```

## `Axes`

```python
ax = Axes(
    x_range=[-3, 3, 0.5],          # [início, fim, passo]
    y_range=[-1.5, 1.5, 0.5],
    x_length=10,                    # tamanho NA CENA, em unidades Manim
    y_length=6,
    axis_config={"color": GREY_B, "include_numbers": True,
                 "font_size": 24, "stroke_width": 2},
    x_axis_config={"numbers_to_include": [-2, 0, 2]},
    tips=True,
)
labels = ax.get_axis_labels(x_label="t", y_label=r"f(t)")
self.add(ax, labels)
```

`x_range` é o domínio **matemático**; `x_length` é o tamanho **visual**. São
independentes — é assim que se controla a escala.

## Plotar funções

```python
g = ax.plot(lambda x: np.sin(x), color=BLUE, x_range=[-3, 3])
g2 = ax.plot(lambda x: x**2, color=RED, use_vectorized=False)
self.play(Create(g), run_time=2)

# rótulo grudado na curva
lbl = ax.get_graph_label(g, MathTex(r"\sin x"), x_val=2, direction=UR)

# descontinuidades: quebre o domínio
h = ax.plot(lambda x: 1 / x, x_range=[0.1, 5], discontinuities=[0])
```

Curvas paramétricas e implícitas:

```python
c = ax.plot_parametric_curve(
    lambda t: np.array([np.cos(t), np.sin(t), 0]), t_range=[0, TAU]
)
i = ax.plot_implicit_curve(lambda x, y: x**2 + y**2 - 4)
p = ax.plot_polar_graph(lambda th: 1 + np.cos(th), theta_range=[0, TAU])
```

## Anotações sobre o gráfico

```python
area  = ax.get_area(g, x_range=[0, 2], color=BLUE, opacity=0.3)
area2 = ax.get_area(g, x_range=[0, 2], bounded_graph=g2)   # entre curvas
riemann = ax.get_riemann_rectangles(g, x_range=[0, 3], dx=0.25,
                                    input_sample_type="left")
tangent = ax.get_secant_slope_group(x=1.5, graph=g, dx=0.01,
                                    secant_line_color=YELLOW)
vline = ax.get_vertical_line(ax.i2gp(2, g), color=YELLOW)
hline = ax.get_horizontal_line(ax.c2p(2, 4))
lines = ax.get_lines_to_point(ax.c2p(2, 4))
```

`ax.i2gp(x, graph)` (*input to graph point*) devolve o ponto da cena sobre a
curva no `x` dado — é o jeito certo de colocar um `Dot` em cima do gráfico.

Animar a integral crescendo, ou a tangente correndo: use `ValueTracker` +
`always_redraw` (skill `manim-updaters-valuetracker`).

## Outros planos

```python
NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1],
            background_line_style={"stroke_width": 1, "stroke_opacity": 0.4})
NumberLine(x_range=[0, 10, 1], length=12, include_numbers=True)
PolarPlane(radius_max=3, azimuth_units="PI radians")
ComplexPlane().add_coordinates()
ThreeDAxes(x_range=[-3, 3], y_range=[-3, 3], z_range=[-2, 2])
```

`NumberPlane` com passo muito fino é o item mais caro de uma cena típica.
`0.25` já gera milhares de linhas. Se estiver lento, aumente o passo.

## Dados tabulares

```python
BarChart(values=[3, 7, 1, 9], bar_names=["a", "b", "c", "d"],
         y_range=[0, 10, 2], bar_colors=[BLUE, GREEN, RED, YELLOW])

t = Table([["1", "2"], ["3", "4"]],
          row_labels=[Text("L1"), Text("L2")],
          col_labels=[Text("C1"), Text("C2")],
          include_outer_lines=True)
t.add_highlighted_cell((2, 2), color=YELLOW)
t.get_cell((1, 1));  t.get_rows();  t.get_columns()

Matrix([[1, 2], [3, 4]])
IntegerMatrix([[1, 2], [3, 4]])
MobjectMatrix([[Circle(), Square()], [Triangle(), Dot()]])
```

## Grafos

```python
v = [1, 2, 3, 4]
e = [(1, 2), (2, 3), (3, 4), (4, 1)]
g = Graph(v, e, layout="circular", labels=True,
          vertex_config={"radius": 0.2, "color": BLUE},
          edge_config={"stroke_width": 3})
self.play(Create(g))
self.play(g.animate.change_layout("spring"))

DiGraph(v, e)   # dirigido
```

Layouts: `spring` `circular` `kamada_kawai` `planar` `random` `shell`
`spectral` `spiral` `tree` `partite`, ou um dict `{vértice: posição}`.

## Descobrir o resto

`Axes` tem dezenas de métodos além dos citados:

```bash
bin/mx show Axes --own-only
awk -F'\t' '$1=="Axes" {print $2$6}' api/manim-ce-methods.tsv | sort
awk -F'\t' '$1=="class" && $3=="mobject/graphing" {print $2}' api/manim-ce-index.tsv
```

## Cena completa de exemplo

```python
from manim import *
import numpy as np

class Derivada(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2],
                  x_length=10, y_length=5.5,
                  axis_config={"include_numbers": True})
        lbl = ax.get_axis_labels("x", "y")
        f = ax.plot(lambda x: x**2, color=BLUE)
        f_lbl = ax.get_graph_label(f, MathTex("x^2"), x_val=2.2, direction=UR)

        self.play(Create(ax), Write(lbl))
        self.play(Create(f), Write(f_lbl))

        x = ValueTracker(-2.5)
        tangente = always_redraw(
            lambda: ax.get_secant_slope_group(
                x=x.get_value(), graph=f, dx=0.001,
                secant_line_color=YELLOW, secant_line_length=4,
            )
        )
        ponto = always_redraw(lambda: Dot(ax.i2gp(x.get_value(), f), color=YELLOW))

        self.add(tangente, ponto)
        self.play(x.animate.set_value(2.5), run_time=4, rate_func=linear)
        self.wait()
```

```bash
bin/mx render scenes/derivada.py Derivada -q h --codec nvenc
```

## Armadilhas

- **`move_to` com coordenadas do gráfico** — sempre `ax.c2p(...)`.
- **`x_range` tem 3 elementos**; omitir o passo usa 1, que pode ser
  grosseiro demais ou fino demais.
- **`plot` com singularidade** (`1/x`, `tan`) desenha uma reta vertical
  gigante. Quebre o `x_range` ou passe `discontinuities=`.
- **`use_vectorized=True`** exige que a função aceite arrays NumPy. Com
  `lambda x: np.sin(x)` funciona; com `if x > 0` quebra.
- **Eixos grandes demais** saem do quadro: `x_length` + `y_length` devem
  caber em 14,2 × 8.
- **`NumberPlane` de passo fino é caro.** É o gargalo típico de geometria.
- **`Table` recebe strings**, não números. `Table([[1,2]])` falha; use
  `[["1","2"]]` ou `IntegerTable`.
