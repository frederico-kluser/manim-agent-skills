---
name: manim-graphs-plots
description: >-
  Eixos, planos e gráfico de função no Manim — `Axes`, `NumberPlane`,
  `NumberLine`, `PolarPlane`, `ComplexPlane`, `ThreeDAxes`, `plot` e as curvas
  (`ParametricFunction`, `FunctionGraph`, `ImplicitFunction`), a máquina de
  cálculo (área, retângulos de Riemann, secante, tangente, derivada,
  antiderivada), escala logarítmica (`LogBase`), série de dados medidos
  (`plot_line_graph`) e `BarChart`. Use quando o pedido soar como "plota essa
  função", "desenha um plano cartesiano", "põe eixos", "anima a curva sendo
  traçada", "gráfico de barras", "quero as barras crescendo", "mostra a área
  sob a curva", "a reta tangente correndo", "escala log", "o eixo não mostra o
  último número", "sumiu o zero do eixo", "o rótulo do eixo ficou para trás
  quando eu movi o gráfico", "o ponto caiu fora do quadro", "a curva ficou
  poligonal / serrilhada", "o gráfico estourou a tela", "esse plano deixou o
  render lento", "a linha guia não aparece no fundo branco". Cobre a conversão
  entre coordenadas do gráfico e da cena (`c2p`/`p2c`/`i2gp`, e o operador
  `@`), a regra de amostragem que decide se a curva sai lisa ou quebrada, e
  quando desenhar a barra à mão em vez de usar `BarChart`. NÃO use para:
  `Table`/`Matrix` e dados tabulares (skill `manim-tabelas-matrizes`);
  `Graph`/`DiGraph` de teoria dos grafos, layouts e redes
  (`manim-grafos-redes`); posicionar/agrupar/medir mobject e caber na tela
  (`manim-mobjects`, `manim-layout-posicionamento`); escolher a classe de
  animação, `rate_func` ou `lag_ratio` (`manim-animations`,
  `manim-composicao-ritmo`); `ValueTracker`/`always_redraw`/updaters
  (`manim-updaters-valuetracker`); cor, contraste e tema
  (`manim-color-theming`); `Text`/`MathTex`/LaTeX (`manim-text-latex`);
  câmera 3D, `Surface` e `phi/theta` (`manim-3d-camera`); campos vetoriais
  `VectorField`/`StreamLines` (sem skill dona hoje).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Eixos, planos e gráficos

Tudo aqui sai de **15 classes** e de **um mixin**. Confira a lista quando
duvidar de um nome:

```bash
awk -F'\t' '$3=="mobject/graphing" && ($1=="class"||$1=="function")' \
  api/manim-ce-index.tsv | cut -f1,2,5
```

| classe | herda de | para quê |
|---|---|---|
| `CoordinateSystem` | — (**mixin puro, não é Mobject**) | onde moram `c2p`, `plot`, `get_area`, `get_riemann_rectangles`… |
| `Axes` | `VGroup` + `CoordinateSystem` | o par de eixos cartesianos |
| `NumberPlane` | `Axes` | eixos + grade de fundo |
| `ComplexPlane` | `NumberPlane` | o mesmo, indexado por número complexo |
| `PolarPlane` | `Axes` | grade radial + azimutal |
| `ThreeDAxes` | `Axes` | três eixos (skill `manim-3d-camera` para a câmera) |
| `NumberLine` | `Line` | **um** eixo, sozinho — é a peça de que `Axes` é feito |
| `UnitInterval` | `NumberLine` | `x_range=(0, 1, 0.1)`, `unit_size=10` |
| `BarChart` | `Axes` | barras verticais |
| `SampleSpace` | `Rectangle` | quadrado de probabilidade dividido |
| `ParametricFunction` | `VMobject` | a curva que `plot` devolve |
| `FunctionGraph` | `ParametricFunction` | curva em coordenadas **da cena** |
| `ImplicitFunction` | `VMobject` | `f(x,y) = 0` |
| `LinearBase` / `LogBase` | `_ScaleBase` | a escala de um eixo |

A herança inteira, sem chutar:

```bash
grep -nE "^\s*(CoordinateSystem|Axes|NumberLine|ParametricFunction)\b" \
  api/manim-ce-inheritance.txt
```

---

## 1. Correções à versão anterior desta skill

Registro do que estava errado aqui, porque quem leu a versão antiga precisa
desaprender. Cada item foi conferido no fonte de
`.venv/lib/python3.12/site-packages/manim/` — leitura, não render.

| Dizia | O certo |
|---|---|
| "`NumberPlane` com passo 0,25 já gera **milhares de linhas**, é o item mais caro de uma cena típica" | **88 linhas**, no quadro padrão. A conta está em §14 com a fórmula do fonte. O item caro de uma cena típica é a **amostragem das curvas**, não a grade: uma `ax.plot` default já são ~140 segmentos, seis vezes a grade inteira |
| "`Table` recebe strings, não números. `Table([[1,2]])` falha" | A assinatura declara `Iterable[Iterable[float \| str \| VMobject]]`. O que espera `str` é o `element_to_mobject` padrão (`Paragraph`). E `Table` **não é mais desta skill** — é de `manim-tabelas-matrizes` |
| `x_axis_config={"numbers_to_include": [-2, 0, 2]}` mostrado como receita | O `0` some assim mesmo — e `numbers_to_exclude: []` sozinho **também não** o traz de volta: são duas barreiras em série (§7) |
| "o último tick nunca aparece; use `b + 0.001`" | Só com `tips=True`. Quem manda é `include_tip`, e §4 recomenda `tips=False` — aí o último tick já sai (§5) |
| Grafos (`Graph`, `DiGraph`, layouts) como assunto desta skill | Passou para `manim-grafos-redes` |
| `ax.plot(..., discontinuities=[0])` apresentado como a correção da singularidade | Ele evita o traço **atravessando** o polo, mas não limita o `y`: a caixa delimitadora da curva continua explodindo (§8) |

Também some daqui, por decisão de fronteira: `Matrix`/`IntegerMatrix`/
`MobjectMatrix` (→ `manim-tabelas-matrizes`).

---

## 2. Quatro espaços de coordenadas, não dois

A regra "converta com `c2p`" está certa, mas incompleta — na prática existem
quatro sistemas na tela ao mesmo tempo, e o erro nasce ao misturar dois.

| espaço | unidade | quem vive nele |
|---|---|---|
| **cena** | 14,222 × 8, origem no centro | todo Mobject; `move_to`, `next_to`, `to_edge` |
| **gráfico** | `x_range` × `y_range` | o que você pensa: "custo = 9,51" |
| **do plano bruto** | 1 unidade de gráfico = 1 unidade de cena | só `NumberPlane()` sem `x_length` (§14) |
| **pixel** | 1920 × 1080 | ninguém, dentro da cena — é do render |

```python
ax = Axes(x_range=[0, 10], y_range=[0, 100, 20])

Dot(ax.c2p(3, 45))              # certo
Dot(np.array([3, 45, 0]))       # ERRADO: y=45 fica 41 unidades acima do quadro
```

As quatro conversões, com a assinatura do índice:

```python
ax.coords_to_point(*coords)   # c2p  — gráfico  -> cena
ax.point_to_coords(point)     # p2c  — cena     -> gráfico
ax.i2gp(x, curva)             # input_to_graph_point:  x -> ponto da cena SOBRE a curva
ax.i2gc(x, curva)             # input_to_graph_coords: x -> (x, f(x)) em coords do gráfico
```

E existe açúcar de operador, documentado no fonte e quase desconhecido
(`coordinate_systems.py:1864-1870`, `number_line.py:678-683`):

```python
ax @ (3, 45)        # == ax.c2p(3, 45)      — aceita Mobject: usa get_center()
ponto @ ax          # == ax.p2c(ponto)
linha @ 7           # NumberLine: == linha.n2p(7)
```

**`c2p` e `p2c` são vetorizados.** Isso importa: converter 500 pontos num laço
Python é 500 chamadas; em bloco é uma. Do docstring do fonte
(`coordinate_systems.py:2103-2126`):

```python
ax.c2p([[0, 1], [1, 1], [1, 0]])      # lista de pontos -> array (3, 3)
ax.c2p([0, 1, 1], [1, 1, 0])          # um array por eixo -> a transposta
ax.c2p(np.array([1, 0]))              # um ponto como array plano
```

### `get_origin()` mente quando o intervalo não contém o zero

`get_origin()` é literalmente `coords_to_point(0, 0)`. Com
`x_range=[2, 8]`, `c2p(0, ...)` **extrapola** a reta numérica: o ponto sai à
esquerda do eixo desenhado, fora da região do gráfico. Não há erro, e
`ax.get_origin()` vira uma âncora inválida.

O canto inferior esquerdo real é sempre:

```python
canto = ax.c2p(ax.x_range[0], ax.y_range[0])
```

---

## 3. `Axes` — a assinatura, e os defaults que dependem do `config`

```
Axes(x_range=None, y_range=None, x_length=12, y_length=6,
     axis_config=None, x_axis_config=None, y_axis_config=None,
     tips=True, **kwargs)
```

Os dois `12`/`6` que o índice imprime não são literais no fonte. São
(`coordinate_systems.py:1934-1935`):

```python
x_length = round(config.frame_width) - 2     # round(14,222) - 2 = 12
y_length = round(config.frame_height) - 2    # round(8)      - 2 = 6
```

Avaliados **na importação do módulo**. Se o projeto mexer em `frame_width`
(vídeo 9:16, por exemplo), os defaults mudam junto — e um `Axes()` sem
argumentos passa a ter outro tamanho sem que nenhuma linha de cena mude.

`x_range`/`y_range` default vêm de `CoordinateSystem.__init__`
(`:132-149`): `[round(-frame_x_radius), round(frame_x_radius), 1]`, ou seja
`[-7, 7, 1]` e `[-4, 4, 1]`. **Com dois elementos, o passo 1 é acrescentado
em silêncio** — o próprio comentário do fonte reclama disso: *"a user can't
know default without peeking at source code"*.

Daí a aritmética que resolve metade dos problemas de enquadramento:

```
unidade x = x_length / (x_max - x_min)     # default: 12/14 = 0,857
unidade y = y_length / (y_max - y_min)     # default:  6/8  = 0,750
```

`x_range` é o domínio **matemático**; `x_length` é o tamanho **visual**. São
independentes — é exatamente assim que se controla a escala, e é por isso que
`Axes(x_range=[0, 1e6])` cabe na tela sem drama.

### O `Axes` se centraliza no MEIO do intervalo, não no zero

Última linha do `__init__` (`:2027-2033`):

```python
lines_center_point = [ (axis.x_range[1] + axis.x_range[0]) / 2  for axis in self.axes ]
self.shift(-self.coords_to_point(*lines_center_point))
```

O ponto médio dos intervalos vai para a origem da cena. Consequência prática:
`Axes(x_range=[0, 10], y_range=[0, 100])` fica centralizado, e o canto
inferior esquerdo dele fica em baixo-à-esquerda — não no centro. Não tente
"consertar" com `.center()`: já está centralizado.

### `tips=True` faz o desenho ser MAIOR que `x_length`

A ponta de flecha é acrescentada depois do `set_length`
(`number_line.py:229-245`). Ou seja: `ax.width > x_length`, e mais ainda
depois de `add_coordinates()`. Se o cálculo de espaço foi feito com
`x_length`, mede errado. Meça o objeto:

```python
ax.width, ax.height          # o que realmente ocupa
```

### Precedência dos três dicts de configuração

`axis_config` é a base; `x_axis_config` e `y_axis_config` são mesclados
**por cima**, recursivamente (`_update_default_configs` →
`merge_dicts_recursively`, `:1955-1972`). E o `Axes` já chega com defaults
próprios que você está sobrescrevendo sem saber:

```python
axis_config   = {"include_tip": tips, "numbers_to_exclude": [0]}
y_axis_config = {"rotation": 90 * DEGREES, "label_direction": LEFT}
```

Passar `y_axis_config={"label_direction": DOWN}` mantém a rotação. Mas
`axis_config={"numbers_to_exclude": []}` **não basta** para recuperar o zero: o
`Axes` ainda força `exclude_origin_tick = True` depois do merge, e são duas
barreiras (§7).

---

## 4. Receita mínima que funciona

```python
ax = Axes(
    x_range=[-3, 3, 0.5],
    y_range=[-1.5, 1.5, 0.5],
    x_length=10,
    y_length=5,
    axis_config={"color": GREY_B, "stroke_width": 2,
                 "include_numbers": True, "font_size": 24},
    tips=False,
)
rotulos = ax.get_axis_labels(x_label="t", y_label=r"f(t)")
curva = ax.plot(np.sin, color=BLUE)
self.add(ax, rotulos, curva)
```

`tips=False` é o default certo para gráfico de aula: a flecha só ajuda quando
o eixo representa uma reta infinita, e atrapalha o cálculo de espaço sempre.

---

## 5. Os ticks: `get_tick_range`, e quem de fato decide o último

**Esta seção é uma correção.** A versão anterior citava
`number_line.py:340-357` mas começava o bloco na linha 345 — apagando
justamente as duas linhas que decidem o resultado. O fonte **inteiro**,
`number_line.py:340-357`:

```python
x_min, x_max, x_step = self.x_range
if not self.include_tip:            # ← as duas linhas que faltavam
    x_max += 1e-6                   # ← e que mudam TUDO

if x_min < x_max < 0 or x_max > x_min > 0:
    tick_range = np.arange(x_min, x_max, x_step)
else:
    start_point = x_step if self.exclude_origin_tick else 0
    x_min_segment = np.arange(start_point, np.abs(x_min) + 1e-6, x_step) * -1
    x_max_segment = np.arange(start_point, x_max, x_step)
    tick_range = np.unique(np.concatenate((x_min_segment, x_max_segment)))
```

Quem some não é "o último tick": é o último tick **quando há ponta de seta**.
O `+ 1e-6` que o lado negativo sempre leva, o lado positivo só ganha se
`include_tip` for falso — e `include_tip` sai de `tips=` do `Axes`.

Reprodução aritmética da função (numpy puro, sem cena):

| `x_range` | `tips=True` (default do `Axes`) | **`tips=False`** |
|---|---|---|
| `[-4, 4, 1]` | −4 −3 −2 −1 · 1 2 3 — **falta o 4** | −4 −3 −2 −1 · 1 2 3 **4** |
| `[0, 10, 2]` | 2 4 6 8 — **faltam 0 e 10** | 2 4 6 8 **10** (o 0 continua fora, §7) |
| `[2, 8, 2]` | 2 4 6 — **falta o 8** | 2 4 6 **8** |

Consequência prática, e é a que interessa aqui: **§4 recomenda `tips=False`
como o default certo para gráfico de aula — e nesse caminho o último tick já
aparece.** A gambiarra do milésimo é para quem mantém `tips=True`; num eixo sem
ponta ela é ruído que ainda desloca a escala e a centralização.

Se você mantém `tips=True`, três saídas, em ordem de preferência:

```python
Axes(x_range=[0, 10.001, 2])                                  # estica 1 milésimo
Axes(x_axis_config={"numbers_to_include": [0, 2, 4, 6, 8, 10]})  # lista explícita
ax.x_axis.add_labels({10: "10"})                              # a marca que faltou
```

`exclude_origin_tick` é ligado automaticamente por `Axes` quando a escala é
`LinearBase`, e desligado quando é `LogBase` — porque em log o "ponto 0" é
`10^0`, que é um valor legítimo do eixo, não a origem (`:1996-2011`).

---

## 6. Os números do eixo exigem LaTeX — e como fugir disso

`NumberLine(label_constructor=MathTex)` é o default, e o número é montado por
`DecimalNumber(x, mob_class=label_constructor)`
(`number_line.py:164, 493-496`). Isto é: **`include_numbers=True` compila
LaTeX**, em cada rótulo, em todo eixo. Numa máquina sem `dvisvgm` no PATH o
gráfico inteiro falha por causa dos números (`manim-troubleshooting` e
`manim-project §3` para o caso do symlink ausente).

A fuga, quando o projeto usa fonte de texto e não quer LaTeX:

```python
Axes(axis_config={"label_constructor": Text})
```

`DecimalNumber` chama `mob_class(string)` — `Text` aceita essa forma, então o
caminho não passa por LaTeX. *(Deduzido do fonte; não executado nesta
rodada.)*

### `_decimal_places_from_step`: o passo decide as casas decimais

`number_line.py:672-677`:

```python
step_str = str(step)
return 0 if "." not in step_str else len(step_str.split(".")[-1])
```

É `str()` do float, contando dígitos depois do ponto.

| passo | rótulos |
|---|---|
| `1` | `0`, `1`, `2` |
| `0.5` | `0.5`, `1.0` |
| `1/3` | `str(0.3333333333333333)` → **16 casas** em cada rótulo |
| `0.1 * 3` | `str(0.30000000000000004)` → **17 casas** |

Passo que veio de conta de ponto flutuante entope o eixo. Corrija na fonte
(`round(passo, 3)`) ou force:

```python
Axes(axis_config={"decimal_number_config": {"num_decimal_places": 2}})
```

Cuidado: passar `decimal_number_config` **substitui** o dict inteiro que
seria derivado do passo (`number_line.py:188-191`).

---

## 7. O zero que some, e os dois caminhos de rótulo

**Esta seção é uma correção.** São **duas** barreiras em série, e a versão
anterior só conhecia a segunda — por isso a receita que ela dava não funcionava.

**Barreira 1, o tick.** `Axes.__init__` força, **depois** de mesclar a sua
config e para toda escala `LinearBase`:

```python
# coordinate_systems.py:1980-1990
self.x_axis_config["exclude_origin_tick"] = True     # e o mesmo para y
```

Não é um default sobrescrevível: é uma atribuição posterior ao merge. Logo
`get_tick_range()` **nunca** contém o 0 (§5), e nenhum valor de
`numbers_to_exclude` traz o 0 de volta pelo caminho automático.

**Barreira 2, o rótulo.** `Axes` também injeta `numbers_to_exclude: [0]` no
`axis_config` (`coordinate_systems.py:1944-1947`), e `add_numbers` usa isso como
`excluding` (`number_line.py:544-556`).

Resultado: `axis_config={"numbers_to_exclude": []}` **sozinho não devolve o
zero** — derruba a barreira 2 e esbarra na 1. O que funciona é dizer o valor
explicitamente, porque `add_numbers(x_values=...)` ignora o `tick_range`
(`number_line.py:541-542`) e as **duas** chaves precisam ceder juntas:

```python
Axes(x_axis_config={"numbers_to_include": [-2, 0, 2],   # pula o tick_range
                    "numbers_to_exclude": []},          # e o filtro do 0
     tips=False)
```

Isso devolve o **número** 0 no eixo. A **marca** de tick em 0 continua não
existindo em escala linear — se você precisa dela, desenhe-a
(`ax.x_axis.add_labels(...)` ou um `Line` seu). Em `LogBase`
`exclude_origin_tick` vira `False`, porque ali o "0" é `10^0`, um valor
legítimo do eixo, não a origem.

Existem dois caminhos distintos de rotulagem, e eles não se misturam:

```python
ax.add_coordinates()                       # números em todos os ticks
ax.add_coordinates([1, 2, 3], None)        # x explícito, y default
ax.add_coordinates({1: "seg", 2: "ter"})   # dict: posição -> texto
ax.coordinate_labels                       # onde eles ficam guardados
```

No caminho de **dict**, uma `str` vira `Tex` (modo texto), não `MathTex`
(`number_line.py:613-618`) — mesmo com `label_constructor=MathTex`. Um label
mobject sem atributo `font_size` levanta `AttributeError` explícito
(`:625`).

### `add_coordinates` gruda; `get_axis_labels` NÃO

Esta é a causa nº 1 de "o rótulo ficou para trás quando eu movi o gráfico".

| chamada | vira filho dos eixos? |
|---|---|
| `ax.add_coordinates(...)` | **sim** — `axis.add_numbers` faz `self.add(numbers)` |
| `ax.get_axis_labels(...)` | **não** — monta `self.axis_labels` e só devolve |
| `ax.get_graph_label(...)` | **não** |
| `ax.get_area / get_riemann_rectangles / get_secant_slope_group / get_vertical_line` | **não** |

```python
rotulos = ax.get_axis_labels("t", "f(t)")
self.play(ax.animate.shift(LEFT))          # ERRADO: os rótulos ficam parados
grupo = VGroup(ax, rotulos, curva)
self.play(grupo.animate.shift(LEFT))       # certo
```

E há um efeito colateral escondido: `_get_axis_label` e `get_graph_label`
terminam com `shift_onto_screen()` (`:382, 1178`). O rótulo é puxado para
dentro do quadro **no momento em que é criado**. Se você criar os rótulos com
os eixos ainda fora da tela (para animar a entrada), eles nascem deslocados em
relação ao eixo, e ninguém avisa. **Posicione primeiro, rotule depois.**

---

## 8. `plot` — a regra de amostragem que decide se a curva sai lisa

Assinatura real (`CoordinateSystem`):

```
plot(function, x_range=None, use_vectorized=False,
     colorscale=None, colorscale_axis=1, **kwargs)  -> ParametricFunction
```

O trecho que manda (`coordinate_systems.py:729-739`):

```python
t_range = np.array(self.x_range, dtype=float)
if x_range is not None:
    t_range[: len(x_range)] = x_range
if x_range is None or len(x_range) < 3:
    t_range[2] /= self.num_sampled_graph_points_per_tick   # = 10
```

Leia com atenção, porque o terceiro elemento **troca de significado**:

| como você chama | passo de amostragem |
|---|---|
| `ax.plot(f)` | `x_step / 10` — no `Axes` default, `1/10 = 0,1` → ~141 pontos |
| `ax.plot(f, x_range=[0, 5])` | `x_step / 10` (o passo vem dos eixos) |
| `ax.plot(f, x_range=[0, 5, 1])` | **1** — 5 pontos, curva poligonal |
| `ax.plot(f, x_range=[0, 5, 0.01])` | 0,01 — 500 pontos |

**No `Axes` o terceiro número de `x_range` é a frequência de TICK; no `plot`
é a frequência de AMOSTRA.** Copiar o `x_range` dos eixos para dentro do
`plot` é o jeito clássico de produzir uma curva quebrada. O próprio docstring
do upstream monta três painéis lado a lado só para mostrar isso
(`:686-725`).

`use_smoothing=True` (default de `ParametricFunction`) roda `make_smooth()` no
fim — o que arredonda cantos que deveriam ser bicudos:

```python
ax.plot(lambda x: abs(x), use_smoothing=False)   # o "V" continua bicudo
ax.plot(np.floor, use_smoothing=False, x_range=[-3, 3, 0.005])
```

`use_vectorized=True` passa o array inteiro de `t` para a função de uma vez
(`functions.py:167-172`). Vale para curva com muitas amostras, e exige que a
função aceite arrays: `np.sin` sim, `lambda x: x if x > 0 else 0` não
(`ValueError: truth value of an array...`).

### `colorscale` quebra sem `x_range` explícito

Linha 780 de `coordinate_systems.py`, dentro do bloco `if colorscale:`:

```python
resolution = 0.01 if len(x_range) == 2 else x_range[2]
```

`x_range` é o parâmetro, que continua `None` se você não passou. `len(None)`
→ `TypeError: object of type 'NoneType' has no len()`. Portanto:

```python
ax.plot(f, colorscale=[BLUE, GREEN, YELLOW])                  # TypeError
ax.plot(f, x_range=[-3, 3, 0.02], colorscale=[BLUE, YELLOW])  # ok
ax.plot(f, x_range=[-3, 3, 0.02],
        colorscale=[(BLUE, -3), (YELLOW, 0), (RED, 3)])       # pivôs explícitos
```

`colorscale_axis` é `1` (colore por `y`) ou `0` (por `x`). O laço que monta as
cores é Python puro sobre `arange(x0, x1 + res, res)` (`:782-810`): com
`x_range=(0, 6, 0.001)` são 6.000 iterações com `interpolate_color` em cada
uma, só para pintar. Prefira poucos pivôs e passo grosso para a cor.

### Singularidade: `discontinuities` corta o traço, não o `y`

```python
h = ax.plot(lambda x: 1 / x, x_range=[-4, 4, 0.01],
            discontinuities=[0], dt=0.1)
```

`ParametricFunction.generate_points` (`functions.py:141-160`) parte o domínio
em `[t_min, d-dt] ∪ [d+dt, t_max]` e inicia um **subcaminho novo** em cada
trecho — some a reta vertical que atravessava o polo. Mas os valores perto do
polo continuam sendo amostrados: com `dt=1e-8` (o **default**!) o ponto mais
próximo vale 10⁸, e a caixa delimitadora da curva vai junto. Efeitos:
`curva.height` fica astronômico, `next_to(curva, UP)` manda o rótulo para o
infinito, e o traço sai da tela em vez de parar na borda.

Por isso: `dt` generoso (o exemplo do próprio upstream usa `0.1`) **e**
domínio partido quando o polo estiver no meio do que interessa:

```python
esq = ax.plot(lambda x: 1/x, x_range=[-4, -0.25, 0.01], color=BLUE)
dir = ax.plot(lambda x: 1/x, x_range=[0.25, 4, 0.01], color=BLUE)
```

`use_vectorized` + `discontinuities` juntos: não verificado nesta rodada.

---

## 9. As três curvas que NÃO conhecem os eixos

`ax.plot` embrulha a sua função em `lambda t: ax.coords_to_point(t, f(t))` —
por isso a curva cai em cima dos eixos. As classes soltas **não fazem isso**:

```
FunctionGraph(function, x_range=None, color=PURE_YELLOW, **kwargs)
ParametricFunction(function, t_range=(0,1), scaling=LinearBase(), dt=1e-8,
                   discontinuities=None, use_smoothing=True,
                   use_vectorized=False, **kwargs)
ImplicitFunction(func, x_range=None, y_range=None, min_depth=5,
                 max_quads=1500, use_smoothing=True, **kwargs)
```

`FunctionGraph` default `x_range = (-frame_x_radius, frame_x_radius)` e
desenha em **coordenadas da cena** (`functions.py:216-230`). Ele casa com
`NumberPlane()` sem argumentos (que também é 1:1 com a cena) e **não** casa com
`Axes(x_length=10)`. O sintoma é uma curva do tamanho errado ao lado dos
eixos, sem erro nenhum.

```python
FunctionGraph(np.sin)                 # cena;  combina com NumberPlane()
ax.plot(np.sin)                       # eixos; é o que você quer em 99% dos casos
```

Os equivalentes que respeitam os eixos:

```python
ax.plot_parametric_curve(lambda t: np.array([np.cos(t), np.sin(t), 0]),
                         t_range=[0, TAU])
ax.plot_implicit_curve(lambda x, y: x**2 + y**2 - 4)   # estica e desloca p/ os eixos
ax.plot_polar_graph(lambda th: 1 + np.cos(th), theta_range=[0, TAU])
ax.plot_surface(f, u_range=..., v_range=...)           # exige ThreeDAxes + cena 3D
```

`ImplicitFunction` não amostra: ele varre quadtree (`plot_isoline`) com
`min_depth=5` (4⁵ = 1.024 quads iniciais) até `max_quads=1500`. Detalhe fino
some com `min_depth` baixo; `max_quads` alto custa tempo de construção. É a
única classe deste conjunto cujo custo **não** é linear no `x_range`.

---

## 10. Dado medido: `plot_line_graph` (e o que ele não sabe fazer)

```
Axes.plot_line_graph(x_values, y_values, z_values=None,
                     line_color=PURE_YELLOW, add_vertex_dots=True,
                     vertex_dot_radius=0.08, vertex_dot_style=None,
                     **kwargs) -> VDict
```

É a ferramenta certa quando os pontos vêm de um arquivo, não de uma fórmula —
o caso de toda aula que mostra número real.

```python
g = ax.plot_line_graph(
    x_values=[0, 1, 2, 3, 4],
    y_values=[9.51, 12.3, 11.8, 15.2, 14.0],
    line_color=ACENTO, vertex_dot_style={"fill_color": ACENTO},
    stroke_width=4,
)
g["line_graph"]     # a poligonal
g["vertex_dots"]    # os pontos
```

Três coisas que ele **não** é (`coordinate_systems.py:2368-2392`):

1. Devolve `VDict`, não `ParametricFunction`. Chaves: `"line_graph"` e
   `"vertex_dots"` (esta última só existe com `add_vertex_dots=True`).
2. **Não tem `underlying_function`.** Logo `i2gc`, `get_area`,
   `slope_of_tangent`, `angle_of_tangent`, `plot_derivative_graph` e
   `plot_antiderivative_graph` levantam `AttributeError` sobre ele. O
   `i2gp` até funciona, mas cai numa busca binária sobre a curva
   (`:1069-1080`), que é mais lenta e levanta `ValueError` fora do domínio.
3. `zip(x_values, y_values, z_values, strict=True)`: listas de tamanhos
   diferentes levantam `ValueError` na construção — o que é bom, é o único
   lugar deste módulo que reclama alto.

Número que aparece na parede tem origem: leia de `dados/*.json` (a disciplina
está em `manim-tema-projeto`) e carimbe a data de coleta no rodapé do slide.

---

## 11. Cálculo: área, Riemann, secante, derivada

```
get_area(graph, x_range=None, color=(BLUE, GREEN), opacity=0.3,
         bounded_graph=None, **kwargs) -> Polygon
get_riemann_rectangles(graph, x_range=None, dx=0.1, input_sample_type="left",
                       stroke_width=1, stroke_color=BLACK, fill_opacity=1,
                       color=(BLUE, GREEN), show_signed_area=True,
                       bounded_graph=None, blend=False,
                       width_scale_factor=1.001) -> VGroup
get_secant_slope_group(x, graph, dx=None, dx_line_color=PURE_YELLOW,
                       dy_line_color=None, dx_label=None, dy_label=None,
                       include_secant_line=True, secant_line_color=GREEN,
                       secant_line_length=10) -> VGroup
get_vertical_lines_to_graph(graph, x_range=None, num_lines=20, **kwargs) -> VGroup
get_T_label(x_val, graph, label=None, label_color=None, triangle_size=0.25,
            triangle_color=WHITE, line_func=Line, line_color=PURE_YELLOW) -> VGroup
angle_of_tangent(x, graph, dx=1e-8) -> float
slope_of_tangent(x, graph, **kwargs) -> float
plot_derivative_graph(graph, color=GREEN, **kwargs) -> ParametricFunction
plot_antiderivative_graph(graph, y_intercept=0, samples=50,
                          use_vectorized=False, **kwargs) -> ParametricFunction
```

```python
area   = ax.get_area(curva, x_range=[0, 2], color=BLUE, opacity=0.3)
entre  = ax.get_area(curva, x_range=[0, 2], bounded_graph=outra)
riem   = ax.get_riemann_rectangles(curva, x_range=[0, 3], dx=0.25,
                                   input_sample_type="left")
tang   = ax.get_secant_slope_group(x=1.5, graph=curva, dx=0.01,
                                   secant_line_color=YELLOW)
```

**`get_area` reaproveita os pontos da curva**, não reamostra
(`:1418-1430`): ele monta um `Polygon` com `[p for p in graph.points if a <= p2c(p)[0] <= b]`.
Se a curva foi plotada com passo grosso, a borda de cima da área é a mesma
poligonal grosseira — e como área preenchida isso salta mais aos olhos que
na linha. Amostre a curva bem antes de pedir a área.

`get_area` retorna `Polygon` e termina com `.set_opacity(opacity)`, que em
`VMobject` mexe em **fill e stroke**. Área com `opacity=0.3` tem contorno
translúcido também; para uma área sem borda, `stroke_width=0` vai em
`**kwargs` (chegam ao `Polygon`).

`get_secant_slope_group` devolve um `VGroup` com atributos nomeados — é assim
que se estiliza cada peça:

```python
g = ax.get_secant_slope_group(x=1.5, graph=curva, dx=0.5,
                              dx_label="dx", dy_label="dy")
g.dx_line, g.df_line, g.secant_line, g.dx_label, g.df_label
```

`dx=None` vira `(x_max - x_min) / 10` (`:1682`). E `secant_line_length=10`
é comprimento **na cena**: numa `Axes` pequena a secante atravessa a tela
inteira. Reduza-a junto com o gráfico.

### O docstring de `slope_of_tangent` está desatualizado no 0.21

O fonte diz (`:1499-1501`) que `ax.slope_of_tangent(x=-2, graph=x²)` devolve
`-3.5000000259052038`. A derivada verdadeira é **−4**.

O `-3,5` é `-4 × (0,75 / 0,857)` — a razão entre as unidades y e x do `Axes`
default. Isto é: o número do docstring vem de uma implementação **antiga**,
que media o ângulo em coordenadas da **cena**. A implementação atual mede em
coordenadas do **gráfico** (`p0 = input_to_graph_coords(x)`, `:1470-1472`), e
o docstring irmão de `angle_of_tangent` confirma: para `x²` em `x=3` ele
promete `1.4056476493802699`, que é exatamente `atan(6)` — a derivada certa.

**Conclusão: `slope_of_tangent` devolve a derivada verdadeira; é o exemplo do
docstring que está velho.** Se você leu a documentação e esperava −3,5,
esqueça. *(Aritmética conferida com `math.atan`; a chamada em si NÃO foi
executada nesta rodada.)*

### As duas derivadas numéricas são caras

`plot_derivative_graph` chama `slope_of_tangent` **em cada amostra**, e cada
uma faz duas avaliações da função com `dx=1e-8` — diferença finita no limite
do double, sujeita a cancelamento catastrófico numa função mal condicionada.
`plot_antiderivative_graph` faz uma integral por trapézios de `samples=50`
pontos **em cada amostra**: com o passo default (141 amostras) são ~7.000
avaliações da sua função. Se ela lê arquivo, chama API ou tem `sleep`, isso
aparece no relógio.

Quando a derivada analítica existe, plote a derivada:

```python
ax.plot(lambda x: 2 * x, color=GREEN)          # barato e exato
ax.plot_derivative_graph(curva, color=GREEN)   # numérico, ~2× o custo da curva
```

---

## 12. Linhas guia — e a que some no fundo branco

```python
ax.get_vertical_line(ax.i2gp(2, curva), color=YELLOW)
ax.get_horizontal_line(ax.c2p(2, 4))
ax.get_lines_to_point(ax.c2p(2, 4))            # as duas de uma vez
ax.get_vertical_lines_to_graph(curva, x_range=[0, 3], num_lines=12)
```

As três primeiras passam por `get_line_from_axis_to_point`
(`:485-532`), cujos defaults são:

```python
line_func = DashedLine          # tracejada, não sólida
color     = VMobject().color    # -> WHITE
```

**Num projeto de fundo claro elas nascem brancas e invisíveis, sem erro
nenhum.** É a mesma família de defeito que `manim-color-theming §10` descreve
para `set_default`. Sempre explicite, e de preferência a partir do tema:

```python
ax.get_vertical_line(ax.i2gp(2, curva), color=TINTA_3, stroke_width=2)
ax.get_lines_to_point(ax.c2p(2, 4), color=DIVISORIA,
                      line_func=Line)          # sólida, se preferir
```

`get_vertical_lines_to_graph` é a exceção: repassa `**kwargs` para
`get_vertical_line`, então o `color=` vale igual.

---

## 13. `NumberLine` sozinha

```
NumberLine(x_range=None, length=None, unit_size=1, include_ticks=True,
           tick_size=0.1, numbers_with_elongated_ticks=None,
           longer_tick_multiple=2, exclude_origin_tick=False, rotation=0,
           stroke_width=2.0, include_tip=False, tip_width=0.35,
           tip_height=0.35, tip_shape=None, include_numbers=False,
           font_size=36, label_direction=DOWN, label_constructor=MathTex,
           scaling=LinearBase(), line_to_number_buff=0.25,
           decimal_number_config=None, numbers_to_exclude=None,
           numbers_to_include=None, **kwargs)
```

`length` **ou** `unit_size`, nunca os dois: `if self.length: set_length(...)
else: self.scale(self.unit_size)` (`number_line.py:229-236`). Passar `length`
faz o `unit_size` ser recalculado e o seu valor é descartado em silêncio.

Uma linha do tempo, uma barra de progresso e um eixo de "quanto de X" são
todos `NumberLine` — e ela é bem mais leve que um `Axes` inteiro:

```python
linha = NumberLine(
    x_range=[0, 12, 1], length=10, include_numbers=True, font_size=24,
    color=DIVISORIA, label_constructor=Text,
)
linha.add_labels({0: "jan", 6: "jul", 12: "dez"})
Dot(linha.n2p(7), color=ACENTO)
```

Métodos próprios úteis: `n2p`/`p2n`, `get_tick_range()`, `get_unit_size()`,
`get_unit_vector()`, `get_tick(x)`, `get_tick_marks()`, `add_ticks()`,
`add_numbers()`, `add_labels()`, `rotate_about_number(n, angle)`,
`rotate_about_zero(angle)`.

`rotation=90*DEGREES` (em radianos, apesar do nome) é como o `Axes` faz o eixo
y. `UnitInterval` é só `NumberLine(x_range=(0,1,0.1), unit_size=10)` com
ticks longos em 0 e 1 e uma casa decimal.

---

## 14. `NumberPlane` — e a conta de custo, corrigida

```
NumberPlane(x_range=(-7.111…, 7.111…, 1), y_range=(-4.0, 4.0, 1),
            x_length=None, y_length=None, background_line_style=None,
            faded_line_style=None, faded_line_ratio=1,
            make_smooth_after_applying_functions=True, **kwargs)
```

`x_length=None` → `NumberLine` cai em `scale(unit_size=1)`: **1 unidade de
gráfico = 1 unidade de cena**, e o plano default cobre exatamente o quadro.
É por isso que `NumberPlane()` combina com `Dot((2, 2, 0))` e com
`FunctionGraph`, e é o único objeto deste módulo em que ignorar `c2p` não
produz erro visível. Assim que você passar `x_length=`, a coincidência acaba —
e todo mundo que estava usando coordenadas de cena quebra.

Estilo (`:2791-2795`):

```python
NumberPlane(
    background_line_style={"stroke_color": DIVISORIA, "stroke_width": 1,
                           "stroke_opacity": 0.4},
    axis_config={"stroke_color": TINTA_3},
    faded_line_ratio=0,      # sem linhas intermediárias
)
```

`faded_line_style=None` gera automaticamente uma cópia do
`background_line_style` com **todo valor numérico dividido por 2**
(`:2826-2833`) — largura e opacidade, junto. Se você deixou
`stroke_width: 1`, as linhas fracas ficam com 0,5 e somem no projetor.

### O custo real da grade

`_get_lines_parallel_to_axis` (`:2909-2942`) com `step = freq /
faded_line_ratio`; para cada direção sai `1 + len(arange(step, min(span,
max), step)) * 2` linhas. Aplicando a fórmula ao quadro padrão
(x ∈ [−7,11, 7,11], y ∈ [−4, 4]):

| passo x,y | `faded_line_ratio` | horizontais | verticais | **total** |
|---:|---:|---:|---:|---:|
| 1 | 1 | 7 | 15 | **22** |
| 0,5 | 1 | 15 | 29 | **44** |
| 0,25 | 1 | 31 | 57 | **88** |
| 1 | 4 | 31 | 57 | **88** |
| 0,25 | 4 | 127 | 227 | **354** |
| 0,1 | 1 | 79 | 143 | **222** |

*(Aritmética reproduzida a partir da fórmula do fonte, com `numpy.arange`
puro — nenhuma cena foi construída.)*

Cada linha dessas é **1** curva cúbica. Compare com uma curva plotada:
`ax.plot(f)` no `Axes` default já são ~140 curvas, e o cenário `BenchGeometry`
do `mx bench` (`manimx/bench.py:45-63`) empilha 11 `FunctionGraph` com
`x_range=[-7, 7, 0.02]` — 700 amostras cada, **7.700 curvas** — ao lado de um
plano de passo 0,25 que contribui com ~100. A grade é ~1% da geometria
daquele cenário.

**Portanto: se o render está lento por causa de geometria, olhe primeiro o
passo de amostragem das curvas e a quantidade de `Dot`, não a grade.** Números
de tempo: `manim-gpu-encoding` e `manim-performance-cache` são os donos; esta
skill não mede.

`prepare_for_nonlinear_transform(num_inserted_curves=50)` insere curvas
sobrando em cada peça do plano para que `ApplyPointwiseFunction`/`Homotopy`
dobrem o desenho em vez de quebrá-lo. Multiplica o número de curvas por ~50 —
use no plano que vai deformar, nunca no de fundo.

`plane.get_vector([2, 1])` devolve um `Arrow` da origem até `c2p(2, 1)`, com
`buff=0` forçado.

---

## 15. `PolarPlane` e `ComplexPlane`

```
PolarPlane(radius_max=4.0, size=None, radius_step=1, azimuth_step=None,
           azimuth_units="PI radians", azimuth_compact_fraction=True,
           azimuth_offset=0, azimuth_direction="CCW", azimuth_label_buff=0.1,
           azimuth_label_font_size=24, radius_config=None,
           background_line_style=None, faded_line_style=None,
           faded_line_ratio=1, make_smooth_after_applying_functions=True,
           **kwargs)
```

```python
pp = PolarPlane(radius_max=3, azimuth_units="PI radians", azimuth_step=8)
pp.add_coordinates()                    # r_values, a_values opcionais
pp.pr2pt(2, PI/3)                       # polar_to_point -> ponto da cena
pp.pt2pr(algum_ponto)                   # point_to_polar
r = pp.plot_polar_graph(lambda th: 1 + np.cos(th), theta_range=[0, TAU])
```

`azimuth_units` aceita `"PI radians"`, `"TAU radians"`, `"degrees"`,
`"gradians"` e `None` (sem rótulo azimutal). `polar_to_point`/`point_to_polar`
existem em `CoordinateSystem`, então funcionam em `Axes` também — leem o
raio/ângulo no espaço do gráfico.

```
ComplexPlane(**kwargs)          # é um NumberPlane com métodos de complexo
```

```python
cp = ComplexPlane().add_coordinates()
cp.n2p(2 + 3j)          # number_to_point  -> ponto da cena
cp.p2n(algum_ponto)     # point_to_number  -> complex
cp.add_coordinates([1, 2j, 1 + 1j])
```

`ComplexPlane` herda tudo de `NumberPlane` — inclusive o 1:1 com a cena
quando não recebe `x_length`.

---

## 16. Escala logarítmica

```
LogBase(base=10, custom_labels=True)      # function(v) = base ** v
LinearBase(scale_factor=1.0)              # function(v) = scale_factor * v
```

O ponto que sempre pega: **com `LogBase`, o `y_range` é escrito em
EXPOENTES.**

```python
ax = Axes(
    x_range=[0, 10, 1],
    y_range=[-2, 4, 1],                       # de 10^-2 a 10^4
    y_axis_config={"scaling": LogBase(base=10)},
    tips=False,
)
ax.plot(lambda x: 10 ** (x / 2), x_range=[0, 8, 0.05])
```

Três consequências, todas do fonte:

1. `Axes` liga `exclude_origin_tick=False` para eixo não-linear
   (`:1996-2011`): o "0" do eixo é `10^0 = 1`, um valor legítimo, e some se
   for excluído.
2. `custom_labels=True` faz o eixo desenhar `10^n` com mobjects `Integer` —
   **LaTeX obrigatório**, sem a fuga por `Text` da §6.
3. `LogBase.inverse_function` levanta `ValueError("log(0) is undefined")` para
   valor ≤ 0. Um `y_range` cujo mínimo real seja 0 quebra a construção do eixo.

Escala log é a resposta certa quando a maior barra é 100× a menor (o caso de
custo por modelo). Mas para **plateia**, o gráfico log mente sobre a razão:
uma barra que parece o dobro é 100×. Prefira dizer o fator em número
(`116×`) e deixar a barra em escala linear estourando a tela — o exagero
visual é o argumento (é o que a `CustoMensal` do deck faz; §19).

---

## 17. `ThreeDAxes`

```
ThreeDAxes(x_range=(-6,6,1), y_range=(-5,5,1), z_range=(-4,4,1),
           x_length=10.5, y_length=10.5, z_length=6.5, z_axis_config=None,
           z_normal=(0,-1,0), num_axis_pieces=20,
           light_source=(-7,-9,10), depth=None, gloss=0.5, **kwargs)
```

O que é desta skill: `c2p(x, y, z)` com três coordenadas, `get_z_axis()`,
`get_axis_labels(x_label, y_label, z_label)`, `get_z_axis_label(...)`, e
`plot_surface(f, u_range, v_range, colorscale=None, colorscale_axis=2)`.
`ThreeDAxes.get_y_axis_label` e `get_z_axis_label` acrescentam `rotation` e
`rotation_axis` (default: girar o rótulo para o plano do eixo).

Tudo o mais — `ThreeDScene`, `set_camera_orientation`, `phi`/`theta`,
`add_fixed_in_frame_mobjects`, `Surface`, iluminação — é da skill
**`manim-3d-camera`**. Um aviso que atravessa as duas: rótulo de eixo 3D sem
`add_fixed_orientation_mobjects` gira com a cena e fica ilegível.

---

## 18. `BarChart` — completo, e as quatro armadilhas

```
BarChart(values, bar_names=None, y_range=None, x_length=None, y_length=None,
         bar_colors=['#003f5c','#58508d','#bc5090','#ff6361','#ffa600'],
         bar_width=0.6, bar_fill_opacity=0.7, bar_stroke_width=3, **kwargs)
```

Métodos próprios: `change_bar_values(values, update_colors=True)` e
`get_bar_labels(color=None, font_size=24, buff=MED_SMALL_BUFF,
label_constructor=Tex)`. Atributos: `.bars`, `.x_labels`, `.bar_labels`,
`.values`.

```python
c = BarChart(values=[3, 7, 1, 9], bar_names=["a", "b", "c", "d"],
             y_range=[0, 10, 2], bar_colors=[BLUE, GREEN, RED, YELLOW],
             y_axis_config={"font_size": 24})
self.add(c, c.get_bar_labels(font_size=24))
self.play(c.animate.change_bar_values([9, 1, 7, 3]))
```

**(a) `bar_colors` é uma lista de PARADAS de gradiente, não uma cor por
barra.** `_update_colors` chama `self.bars.set_color_by_gradient(*bar_colors)`
(`probability.py:349-357`), que vai a `color_gradient(colors, len(bars))`
(`mobject.py:2082-2092`). Com 5 paradas e 4 barras você recebe 4 cores
**interpoladas** — nenhuma delas necessariamente igual às que você passou.
`color_gradient` usa `np.linspace(0, n-1, saída)`, então **uma cor por barra
devolve as suas cores exatas** e qualquer outra contagem interpola.

**(b) `y_range` default produz passo feio.** Sem `y_range`
(`probability.py:299-315`):

```python
y_length = config.frame_height - 4            # 4.0
y_range  = [min(0, min(values)), max(0, max(values)), round(max(values)/y_length, 2)]
```

Para `max(values) = 9` o passo é `round(2.25, 2) = 2.25`, e o eixo sai com
2,25 / 4,5 / 6,75. **Sempre passe `y_range` explícito.** (E `max(values)` muito
pequeno arredonda o passo para `0.0` — passo zero.)

**(c) `values` precisa ser mutável.** A assinatura pede
`MutableSequence[float]` porque `change_bar_values` termina em
`self.values[: len(list(values))] = values` (`:555`). `BarChart(values=(3, 7, 1))`
constrói sem reclamar e só quebra depois, com
`TypeError: 'tuple' object does not support item assignment`. Use lista.

**(d) `BarChart` compila LaTeX, sempre.** O `__init__` termina com
`self.y_axis.add_numbers()` (`:347`) e usa `label_constructor: Tex` no eixo x
(`:323`). Não há flag para desligar; o jeito de ter um gráfico de barras sem
LaTeX é `axis_config={"label_constructor": Text}` — ou desenhar a barra à
mão (§19).

Detalhes menores, todos verificados: `tips` é forçado a `False` se você não
passar; `x_range` é sempre `[0, len(values), 1]` e não é seu; `x_length`
default é `min(len(values), frame_width - 2)`; os rótulos de `bar_names` vão
para **baixo** da barra positiva e para **cima** da negativa; e
`change_bar_values` usa `zip(..., strict=False)`, então uma lista de tamanho
diferente é aceita em silêncio, mexendo só no prefixo comum.

---

## 19. Quando NÃO usar `BarChart` — a barra à mão

Nas 12 cenas de produção do deck de aulas
(`~/Projects/aulas/aulas/*/manim/`), `BarChart` e `Axes` aparecem **zero
vezes**. Todo gráfico de barras é `Rectangle` posicionado à mão. Isso não é
preguiça — é a consequência de quatro requisitos que `BarChart` não atende:

- o eixo y não deve existir (o valor vai **ao lado da barra**, em texto);
- a cor de cada barra é semântica (vermelho = caro, verde = a resposta), não
  um gradiente;
- os rótulos são `Text` do tema, com a fonte do slide, sem LaTeX;
- as barras crescem **uma a uma**, cada uma no seu clique (skill
  `manim-presentation-parts`).

O idioma de crescimento, de `aulas/001-multi-work/manim/aula_001_custo.py:124-143`:

```python
def _prepara_horizontal(barra: Rectangle) -> None:
    """`GrowFromEdge` escala nos DOIS eixos: a barra engorda enquanto avança e,
    numa barra fina, isso lê como bug de render."""
    borda = barra.get_left()
    barra.save_state()                    # guarda o estado FINAL
    barra.stretch_to_fit_width(0.02)      # encolhe só no eixo do crescimento
    barra.next_to(borda, RIGHT, buff=0)   # reancora na borda

# depois:
self.play(Restore(barra, rate_func=SAIDA))
```

E a escala é uma linha, não um objeto:

```python
escala = LARGURA_MAX / max(valores)
Rectangle(width=valor * escala, height=0.38, color=cor,
          fill_opacity=1, stroke_width=0)
```

**A regra de decisão:**

| use `BarChart` | desenhe à mão |
|---|---|
| eixo y numerado importa | o número vai ao lado da barra |
| muitas barras (>8) | 3 a 8 barras, cada uma com nome |
| protótipo, exploração | vídeo que vai para um slide |
| valores mudam na cena (`change_bar_values`) | cada barra entra num clique |
| LaTeX disponível e desejado | tipografia do tema, sem LaTeX |

O mesmo raciocínio vale para eixos: um gráfico de aula com **duas** séries e
seis pontos costuma ficar melhor como texto grande + duas linhas desenhadas do
que como `Axes` completo. `Axes` ganha quando o eixo é o argumento (a forma da
curva, a assíntota, a área).

### O prato opaco, quando o rótulo cruza a grade

Quando um número precisa ficar sobre a grade ou sobre a área preenchida, o
tracejado atravessando as letras lê como texto quebrado num frame parado. A
correção não é mover o número:

```python
prato = Rectangle(width=texto.width + 0.22, height=texto.height + 0.16,
                  fill_color=CANVAS, fill_opacity=1.0, stroke_width=0.0
                  ).move_to(texto.get_center())
rotulo = VGroup(prato, texto)      # prato ANTES do texto
```

(Origem: `aulas/001-multi-work/manim/aula_001_skills.py:339-366`; também em
`manim-presentation-parts`.)

---

## 20. `SampleSpace`

Herda de `Rectangle`, não de `Axes` — é o quadrado de probabilidade dividido
em faixas com chaves e rótulos.

```
SampleSpace(height=3, width=3, fill_color=DARK_GREY, fill_opacity=1,
            stroke_width=0.5, stroke_color=LIGHT_GREY, default_label_scale_val=1)
```

```python
s = SampleSpace()
s.divide_horizontally([0.3, 0.7])
s.add_title("Espaço amostral")
s.get_side_braces_and_labels([r"p", r"1-p"])
```

Métodos: `divide_horizontally`, `divide_vertically`,
`get_horizontal_division(p_list, colors, vect)`, `get_vertical_division`,
`get_division_along_dimension`, `add_braces_and_labels`, `add_label`,
`add_title`, `get_top/bottom/side_braces_and_labels`,
`get_subdivision_braces_and_labels`, `complete_p_list`.

Cores default são cinzas e verdes escuros — em fundo branco, revise
(`manim-color-theming`).

---

## 21. Animar um gráfico

A ordem que funciona quase sempre — eixos, depois curva, depois anotação:

```python
self.play(Create(ax), Write(rotulos))
self.play(Create(curva), run_time=2)
self.play(FadeIn(area))
```

`Create` numa curva desenha ponta a ponta e é a animação natural aqui;
`Write` é para texto. Numa `Axes` inteira, `Create` percorre os dois eixos e
os números — se ficar bagunçado, anime as partes:

```python
self.play(Create(ax.x_axis), Create(ax.y_axis), lag_ratio=0.2)
```

Escolha da classe e do ritmo: `manim-animations` e `manim-composicao-ritmo`.

Trocar uma curva por outra tem uma sutileza: `Transform(c1, c2)` interpola
ponto a ponto, e duas curvas com contagens de amostra diferentes ficam
estranhas no meio do caminho. Plote as duas com o **mesmo** `x_range` de
amostragem, ou use `ReplacementTransform` e aceite o cruzamento.

Para curva/valor/ponto que **acompanham** um número, o mecanismo é
`ValueTracker` + `always_redraw`, e o dono é
**`manim-updaters-valuetracker`**. O gancho desta skill é só o par de linhas
que liga um ao outro:

```python
x = ValueTracker(-2.5)
ponto = always_redraw(lambda: Dot(ax.i2gp(x.get_value(), curva), color=ACENTO))
tang  = always_redraw(lambda: ax.get_secant_slope_group(
            x=x.get_value(), graph=curva, dx=0.001, secant_line_length=4))
self.add(ponto, tang)
self.play(x.animate.set_value(2.5), run_time=4, rate_func=linear)
```

**Custo:** `always_redraw` reconstrói o mobject **a cada frame**. Um
`get_secant_slope_group` redesenhado a 60 fps por 4 s são 240 reconstruções,
cada uma com duas chamadas a `input_to_graph_point`. Aceitável; um
`get_riemann_rectangles(dx=0.05)` em `always_redraw` já não é — ali prefira
`UpdateFromAlphaFunc` ou reconstruir em poucos passos.

---

## 22. Caber na tela

O quadro é 14,222 × 8. Um `Axes(x_length=10, y_length=5)` ocupa 10 × 5 **antes**
de tips, números e rótulos. O jeito de não descobrir isso no projetor:

```python
tudo = VGroup(ax, rotulos, curva, area)
tudo.scale_to_fit_height(6.2).move_to(ORIGIN)        # ou .to_edge(DOWN, buff=0.6)
print(tudo.width, tudo.height)                        # antes de renderizar
```

Consultas baratas, sem render: `mob.width`, `mob.height`,
`mob.get_corner(UR)`, `mob.get_corner(DL)`, `mob.is_off_screen()`. Um gráfico
cortado **não dá erro nenhum** — só some no `overflow` do quadro. O
procedimento completo de verificação é de **`manim-verificacao-visual`**; o
enquadramento e a régua, de **`manim-layout-posicionamento`**.

Uma armadilha específica de gráfico: escalar o `VGroup` depois de pronto
encolhe **o texto dos números junto**. `font_size: 24` num `Axes` que depois
leva `.scale(0.7)` vira 16,8 efetivos — ilegível a 3 metros. Prefira acertar
`x_length`/`y_length` e `font_size` do que escalar no fim.

---

## 23. Procedência: gráfico com número na parede

Regra do repositório de aulas, que atravessa para cá: **todo número mostrado
carrega fonte e data de coleta**, e o gráfico entra num passo *depois* de um
passo que diz o que está fixo e o que varia. Com as barras já na tela, a
plateia chega à conclusão antes do argumento.

Concretamente, para uma cena Manim:

- os valores vêm de um JSON lido pelo tema (`manim-tema-projeto`), nunca
  redigitados dentro da cena;
- o rodapé com a fonte e a data é um `Text` pequeno, fora da área do gráfico,
  acima de uma divisória — não um `axis_config`;
- séries de origens diferentes ganham marca no **rótulo da própria barra**,
  não só no rodapé;
- cena que lê dado externo precisa de `--no-cache`: o hash do cache do Manim
  **não enxerga** o conteúdo do JSON (`manim-project` §10.7,
  `manim-performance-cache`). Sem isso o vídeo antigo é reaproveitado com o
  número novo no slide, e a divergência aparece no palco.

---

## 24. Descobrir o resto sem chutar

```bash
# tudo que existe na categoria
awk -F'\t' '$3=="mobject/graphing" && ($1=="class"||$1=="function")' \
  api/manim-ce-index.tsv | cut -f1,2,5

# a assinatura de uma classe
awk -F'\t' '$1=="class" && $2=="BarChart" {print $4}' api/manim-ce-index.tsv

# métodos PRÓPRIOS (coluna 5 = inherited)
awk -F'\t' '$1=="CoordinateSystem" && $5=="0" {print $2"\t"$6}' \
  api/manim-ce-methods.tsv

# de onde veio um método que você achou num exemplo
awk -F'\t' '$1=="Axes" && $2=="plot" {print $4}' api/manim-ce-methods.tsv

bin/mx show Axes --own-only
bin/mx find riemann
```

`Axes` tem 6 métodos próprios e 39 vindos de `CoordinateSystem` (que tem 44 no total; `Axes` sobrescreve 5) — se você
procurar `plot` em `Axes` no fonte e não achar, é por isso. A metodologia
completa de descoberta é de **`manim-api-discovery`**.

---

## 25. Cena completa

```python
from manim import *
import numpy as np


class Derivada(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-3, 3, 1],               # com tips=False o 3 já sai (§5)
            y_range=[-1, 9, 2],
            x_length=10, y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 24},
            # o rótulo "0" exige as DUAS chaves, e só no eixo que precisa (§7):
            x_axis_config={"numbers_to_include": [-3, -2, -1, 0, 1, 2, 3],
                           "numbers_to_exclude": []},
            tips=False,
        )
        rotulos = ax.get_axis_labels("x", "y")
        f = ax.plot(lambda x: x**2, color=BLUE)               # ~60 amostras
        f_lbl = ax.get_graph_label(f, MathTex("x^2"), x_val=2.2, direction=UR)

        tudo = VGroup(ax, rotulos, f, f_lbl)
        tudo.scale_to_fit_height(6.2).move_to(ORIGIN)          # antes de animar

        self.play(Create(ax), Write(rotulos))
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
        self.wait(0.4)
```

```bash
bin/mx render scenes/derivada.py Derivada -q l --format png   # OLHE a imagem
bin/mx render scenes/derivada.py Derivada -q h --codec nvenc  # só depois
```

O ciclo é **escrever → renderizar rápido → OLHAR o PNG → corrigir → render
final**. Nada nesta skill dá erro no terminal quando sai errado: a curva
poligonal, a linha guia branca no branco, o rótulo que ficou para trás e o
gráfico cortado só aparecem na imagem. Detalhes em
**`manim-verificacao-visual`** e `manim-render-api`.

---

## 26. Armadilhas, em uma tela

| Sintoma | Causa | Correção |
|---|---|---|
| ponto/objeto voa para fora do quadro | `move_to` com coords do gráfico | `ax.c2p(x, y)` (§2) |
| `ax.get_origin()` aponta fora dos eixos | o intervalo não contém 0 → `c2p(0,0)` extrapola | `ax.c2p(ax.x_range[0], ax.y_range[0])` (§2) |
| falta o último número do eixo | com `tips=True`, `get_tick_range` exclui `x_max` (o `+1e-6` só entra se `include_tip` for falso) | `tips=False` — ou `x_range=[a, b+0.001, p]` se a ponta é obrigatória (§5) |
| o `0` não aparece | **duas** barreiras: `exclude_origin_tick=True` forçado depois do merge tira o tick, e `numbers_to_exclude: [0]` tira o rótulo | `x_axis_config={"numbers_to_include": [...0...], "numbers_to_exclude": []}` — as duas juntas (§7) |
| rótulos com 16 casas decimais | `_decimal_places_from_step(str(passo))` | passo redondo, ou `decimal_number_config` (§6) |
| rótulo do eixo fica para trás ao mover | `get_axis_labels` não vira filho dos eixos | `VGroup(ax, rotulos, ...)` (§7) |
| rótulo nasce deslocado do eixo | `shift_onto_screen()` no fim de `_get_axis_label` | posicione os eixos ANTES de rotular (§7) |
| curva poligonal/serrilhada | `x_range` de 3 elementos no `plot` = passo de AMOSTRA | passo pequeno, ou 2 elementos (§8) |
| canto que deveria ser bicudo saiu redondo | `use_smoothing=True` | `use_smoothing=False` (§8) |
| `TypeError: NoneType has no len()` no `plot` | `colorscale` sem `x_range` explícito | passe `x_range=` junto (§8) |
| `ValueError: truth value of an array...` | `use_vectorized=True` com função escalar | `use_vectorized=False` ou vetorize (§8) |
| reta vertical gigante em `1/x`, `tan` | polo amostrado | `discontinuities=[...]` **com `dt` grande**, e/ou domínio partido (§8) |
| curva do tamanho errado ao lado dos eixos | `FunctionGraph` desenha em coords da CENA | `ax.plot(...)` (§9) |
| `AttributeError: underlying_function` | o "gráfico" veio de `plot_line_graph` | só `i2gp` funciona nele (§10) |
| borda da área preenchida em degraus | `get_area` reusa `graph.points` | amostre melhor a curva antes (§11) |
| linha guia não aparece | `get_vertical_line` é `DashedLine` **branca** | `color=` explícito (§12) |
| eixo/gráfico falha por LaTeX | `label_constructor=MathTex`; `BarChart` chama `add_numbers()` | `label_constructor=Text` (§6, §18) |
| `y_range` de `BarChart` com passo 2,25 | passo default = `round(max/4, 2)` | passe `y_range` (§18) |
| cores das barras não são as que passei | `bar_colors` é gradiente, não lista 1:1 | uma cor por barra (§18) |
| `TypeError: 'tuple' object does not support item assignment` | `values` precisa ser `MutableSequence` | use lista (§18) |
| `ValueError: log(0) is undefined` | `LogBase` com valor ≤ 0 no intervalo | intervalo em expoentes, mínimo > 0 (§16) |
| render lento com plano de fundo | quase sempre **não** é a grade | conte as amostras das curvas (§14) |
| gráfico cortado na borda | `x_length` + tips + números > quadro | meça `mob.width/height` (§22) |

---

## 27. O que ficou NÃO VERIFICADO

Honestidade sobre o método: nada foi renderizado nesta rodada (proibição de
CPU/GPU). Tudo acima saiu de leitura do fonte em
`.venv/lib/python3.12/site-packages/manim/mobject/graphing/` e do índice
estático de `api/`. O que continua em aberto:

- **`slope_of_tangent`**: a leitura do fonte e a aritmética (`atan(6) =
  1,40564…`) dizem que ele devolve a derivada verdadeira e que o `-3,5` do
  docstring é resíduo de uma versão antiga. **A chamada não foi executada.**
- **`label_constructor=Text`** como fuga do LaTeX: deduzido de
  `DecimalNumber(mob_class=...)` chamando `mob_class(string)`. Não executado.
- **`use_vectorized=True` combinado com `discontinuities`**: o código percorre
  os trechos separadamente e chama `self.function(t_range)` em cada um; não
  testei se um trecho de um único ponto quebra o desempacotamento `x, y, z`.
- **Tempo de render** de qualquer configuração: não medido, e não é desta
  skill — `manim-gpu-encoding` e `manim-performance-cache` são os donos.
- **A contagem de linhas do `NumberPlane`** (§14) veio de reproduzir a fórmula
  do fonte com `numpy.arange`, sem construir a cena.

---

## 28. Onde esta skill para

| Assunto | Skill dona |
|---|---|
| `Table`, `MathTable`, `Matrix`, `IntegerMatrix`, `MobjectMatrix` | `manim-tabelas-matrizes` |
| `Graph`, `DiGraph`, layouts, `from_networkx` | `manim-grafos-redes` |
| posicionar, agrupar, medir, caber na tela, `z_index` | `manim-mobjects`, `manim-layout-posicionamento` |
| escolher a classe de animação, `Transform` × `ReplacementTransform` | `manim-animations` |
| `rate_func`, `lag_ratio`, `run_time`, `path_func`, orçamento de tempo | `manim-composicao-ritmo` |
| `ValueTracker`, `always_redraw`, `add_updater`, `DecimalNumber` vivo | `manim-updaters-valuetracker` |
| cor, contraste, fundo, tema, "sumiu no branco" | `manim-color-theming` |
| `Text` × `MathTex`, `t2c`, LaTeX que não compila, nitidez do texto | `manim-text-latex` |
| `tema.py` como contrato, dado externo, classe-base de cena | `manim-tema-projeto` |
| `ThreeDScene`, câmera, `Surface`, `phi/theta` | `manim-3d-camera` |
| cortar a cena em partes para o slide | `manim-presentation-parts` |
| qualidade, formato, caminho da saída, seções | `manim-render-api` |
| codec, NVENC, peso do arquivo | `manim-gpu-encoding` |
| cache, custo de rasterização, `--no-cache` | `manim-performance-cache` |
| olhar o PNG, conferir sem render, pôster vazio | `manim-verificacao-visual` |
| achar nome/assinatura/kwarg de qualquer símbolo | `manim-api-discovery` |
| traceback, bissecção, ambiente quebrado | `manim-troubleshooting` |

**Sem skill dona hoje** (declare o buraco, não improvise): `VectorField`,
`ArrowVectorField`, `StreamLines`, `PhaseFlow`, `Homotopy`,
`LinearTransformationScene`, `VectorScene`, `ApplyMatrix` — o pacote de
campos vetoriais e álgebra linear de cena. `Brace`, `Indicate`, `Circumscribe`
e `SurroundingRectangle` (anotar/apontar para o gráfico) também estão órfãos;
o mais próximo é `manim-mobjects`.
