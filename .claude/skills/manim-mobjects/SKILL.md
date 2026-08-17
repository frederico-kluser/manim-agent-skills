---
name: manim-mobjects
description: >-
  Criar e manipular objetos visuais (Mobjects) no Manim — formas
  geométricas, setas, chaves, grupos, posicionamento relativo e absoluto,
  alinhamento, escala, rotação, cópia, e a árvore de submobjects. Use ao
  montar a composição visual de uma cena, posicionar elementos uns em
  relação aos outros, agrupar, ou quando algo aparecer fora do quadro, na
  posição errada, ou sobreposto. Cobre o sistema de coordenadas do Manim e
  a diferença entre VGroup e Group.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Mobjects — o que aparece na tela

## O sistema de coordenadas

O quadro tem **8 unidades de altura** e ~14,22 de largura (16:9), com a
origem `(0,0,0)` no centro. Isso é fixo, independente da resolução — 480p e
4K têm as mesmas coordenadas.

```python
ORIGIN                       # (0, 0, 0)
UP DOWN LEFT RIGHT           # vetores unitários
IN OUT                       # eixo Z
UL UR DL DR                  # diagonais
config.frame_width           # 14.222…
config.frame_height          # 8.0
```

Buffers padronizados: `SMALL_BUFF` 0.1 · `MED_SMALL_BUFF` 0.25 ·
`MED_LARGE_BUFF` 0.5 · `LARGE_BUFF` 1.0.

## Nada aparece até você adicionar

```python
c = Circle()          # existe em memória, invisível
self.add(c)           # aparece instantaneamente
self.play(Create(c))  # aparece animado
self.remove(c)
```

## Posicionamento

```python
mob.move_to(ORIGIN)             # centro do mobject vai para o ponto
mob.move_to(outro)              # sobrepõe no centro de outro
mob.shift(UP * 2 + RIGHT)       # desloca relativo à posição atual
mob.to_edge(UP, buff=0.5)       # encosta na borda do quadro
mob.to_corner(UR)
mob.next_to(outro, RIGHT, buff=0.3)   # ao lado de outro
mob.align_to(outro, LEFT)             # alinha uma borda
mob.center()
```

`move_to` é absoluto, `shift` é relativo. Confundir os dois é a causa mais
comum de "o objeto foi para o lugar errado".

`next_to` posiciona pela **caixa delimitadora**, não pelo centro visual.
Objetos com muito espaço em branco (texto com descendentes, `MathTex` com
integrais) parecem desalinhados — ajuste com `buff` ou `align_to`.

## Tamanho e orientação

```python
mob.scale(2)                          # em torno do próprio centro
mob.scale(2, about_point=ORIGIN)      # em torno de um ponto
mob.rotate(PI / 4)                    # radianos, sempre
mob.rotate(45 * DEGREES)              # mais legível
mob.flip(UP)
mob.stretch(2, dim=0)                 # só no eixo X
mob.set_width(4)                      # mantém proporção
mob.set_height(2)
mob.scale_to_fit_width(6)
mob.match_width(outro)
mob.match_style(outro)
```

## Consultar geometria

```python
mob.get_center()      mob.get_top()       mob.get_bottom()
mob.get_left()        mob.get_right()
mob.get_corner(UR)    mob.get_boundary_point(RIGHT)
mob.width             mob.height          mob.depth
mob.get_start()       mob.get_end()          # curvas
mob.point_from_proportion(0.5)               # ponto ao longo do caminho
mob.get_all_points()
```

## Grupos: `VGroup` vs `Group`

```python
g = VGroup(a, b, c)      # SÓ VMobject (formas vetoriais, texto, LaTeX)
g = Group(a, img, c)     # qualquer Mobject, inclusive ImageMobject
```

Usar `VGroup` com um `ImageMobject` dá `TypeError`. Essa é a distinção que
mais pega.

```python
g.arrange(RIGHT, buff=0.5)                  # enfileira
g.arrange_in_grid(rows=2, buff=0.3)
g.set_color(BLUE)                           # propaga para todos
g[0], g[1:3]                                # indexável e fatiável
g.add(novo);  g.remove(a)
self.play(Create(g))                        # anima todos juntos
```

## Catálogo — descubra o que existe

Não confie na memória. Liste:

```bash
awk -F'\t' '$1=="class" && $3=="mobject/geometry" {print $2"\t"$4}' \
  api/manim-ce-index.tsv | sort

bin/mx show Arrow          # assinatura completa + todos os métodos
bin/mx find "brace"
```

Os grupos principais (`api/manim-ce-by-category.md`):

| Categoria | Exemplos |
|---|---|
| `mobject/geometry` | `Circle` `Square` `Rectangle` `RoundedRectangle` `Triangle` `Polygon` `RegularPolygon` `Ellipse` `Annulus` `Arc` `ArcBetweenPoints` `Sector` `Line` `DashedLine` `Arrow` `DoubleArrow` `Vector` `Dot` `LabeledDot` `Angle` `RightAngle` `Brace` `BraceLabel` `Cutout` `Star` |
| `mobject/text` | `Text` `MarkupText` `Tex` `MathTex` `Title` `BulletedList` `Code` `DecimalNumber` `Integer` `Paragraph` |
| `mobject/graphing` | `Axes` `NumberPlane` `NumberLine` `ThreeDAxes` `PolarPlane` `ComplexPlane` `BarChart` `FunctionGraph` `ParametricFunction` |
| `mobject/3d` | `Sphere` `Cube` `Cylinder` `Cone` `Torus` `Prism` `Arrow3D` `Surface` `Dodecahedron` |
| `mobject/matrix` | `Matrix` `IntegerMatrix` `DecimalMatrix` `MobjectMatrix` |
| `mobject/table` | `Table` `MathTable` `MobjectTable` `IntegerTable` |
| `mobject/graph` | `Graph` `DiGraph` (teoria dos grafos) |
| `mobject/svg` | `SVGMobject` `ImageMobject` |
| `mobject/value_tracker` | `ValueTracker` `ComplexValueTracker` |
| `mobject/vector_field` | `ArrowVectorField` `StreamLines` |

## Cópia — quase sempre você quer `.copy()`

```python
b = a.copy().shift(RIGHT * 2)      # independente
b = a                              # MESMO objeto; mexer em b mexe em a
```

Transformar sem destruir o original:

```python
self.play(TransformFromCopy(a, b))    # preserva a
self.play(Transform(a, b))            # `a` vira `b`; `b` nunca foi adicionado
self.play(ReplacementTransform(a, b)) # `a` sai da cena, `b` entra
```

`Transform` versus `ReplacementTransform` é uma pegadinha clássica: depois
de `Transform(a, b)`, a variável que continua na cena é **`a`** (com a
aparência de `b`). Se você depois animar `b`, nada acontece. Use
`ReplacementTransform` quando quiser continuar manipulando `b`.

## Encadeamento

Quase todo método devolve `Self`, então dá para encadear:

```python
sq = (Square(side_length=2)
      .set_fill(BLUE, 0.5)
      .set_stroke(WHITE, 3)
      .rotate(PI / 6)
      .to_edge(LEFT))
```

Para descobrir o que é encadeável numa classe:

```bash
awk -F'\t' '$1=="Square" && $6 ~ /Self/ {print $2$6}' api/manim-ce-methods.tsv
```

## Submobjects

Texto, fórmulas e grupos são árvores. Colorir ou animar partes exige
navegar nela.

```python
eq = MathTex(r"a^2 + b^2 = c^2")
len(eq.submobjects)          # partes de nível 1
eq[0][2]                     # caractere dentro da primeira parte
eq.get_family()              # tudo, recursivamente
self.add(index_labels(eq[0]))   # DESENHA os índices na tela — essencial
```

`index_labels` é a ferramenta certa para descobrir qual índice corresponde
a qual símbolo. Renderize um PNG com ela, olhe, e só então escreva os
índices no código:

```bash
bin/mx render cena.py Debug --format png -q l
```

## Armadilhas

- **Ângulos em radianos.** `rotate(90)` gira ~14 voltas. Use `90 * DEGREES`.
- **`set_fill` sem `opacity` não mostra nada.**
- **`VGroup` recusa `ImageMobject`.** Use `Group`.
- **`arrange` sobrescreve posições** que você tinha definido antes.
- **Coordenadas são 3D.** `np.array([x, y, 0])`, não `[x, y]`.
- **Objeto fora do quadro** = coordenada além de ±7,1 (X) ou ±4 (Y).
  Confirme com `mob.get_center()` ou renderize um PNG.
