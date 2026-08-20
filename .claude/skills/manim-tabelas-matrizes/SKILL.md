---
name: manim-tabelas-matrizes
description: >-
  Tabelas e matrizes no Manim — as 9 classes de `mobject/table` e
  `mobject/matrix` (`Table`, `MathTable`, `IntegerTable`, `DecimalTable`,
  `MobjectTable`, `Matrix`, `IntegerMatrix`, `DecimalMatrix`,
  `MobjectMatrix`), mais `matrix_to_tex_string`, `matrix_to_mobject` e
  `get_det_text`. Use quando o pedido soar como "põe uma tabela na cena",
  "monta um comparativo lado a lado", "uma grade com esses números", "desenha
  a matriz", "matriz com colchetes", "destaca essa célula", "pinta essa linha
  da tabela", "circula a coluna do meio", "a tabela entra linha por linha",
  "revela a tabela aos poucos", "troca o valor dessa célula", "a tabela ficou
  gigante", "a tabela sumiu no fundo branco", "as linhas da grade não
  aparecem", "`Table([[1,2]])` deu TypeError", "o realce saiu preto", "o
  destaque caiu na célula errada", "`get_entries((1,1))` devolveu a célula
  errada", "os números da matriz estão colados/sobrepostos", "os colchetes
  ficaram esticados", "1.234,50 saiu como 1,234.50", "2,5 virou 2 na tabela",
  ou envolver `element_to_mobject`, `row_labels`/`col_labels`,
  `add_highlighted_cell`, `get_cell`, `set_row_colors`, `v_buff`/`h_buff`,
  `arrange_in_grid_config`, `line_config`, `stretch_brackets`. Cobre também a
  decisão EDITORIAL que vem antes da API — quando uma tabela não deve ir para
  o vídeo, e o que colocar no lugar. NÃO use para: `BarChart`, `Axes`,
  `NumberPlane` e gráfico de função (`manim-graphs-plots`); `Graph`/`DiGraph`
  de teoria dos grafos e layouts de rede (`manim-grafos-redes`); grade genérica
  de mobjects com `VGroup.arrange_in_grid` sem grade desenhada
  (`manim-mobjects`, `manim-layout-posicionamento`); `Text`/`MathTex`/LaTeX que
  não compila e nitidez de glifo (`manim-text-latex`); escolher paleta,
  contraste e fundo (`manim-color-theming`); `rate_func`/`lag_ratio`/`run_time`
  (`manim-composicao-ritmo`); `ValueTracker`/`always_redraw`/`DecimalNumber`
  vivo (`manim-updaters-valuetracker`); `ApplyMatrix`,
  `LinearTransformationScene` e `VectorScene` (álgebra linear de cena — sem
  skill dona hoje).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Tabelas e matrizes

Duas famílias, nove classes, e a mesma armadilha de origem: `Table` e `Matrix`
usam **os mesmos nomes de parâmetro (`v_buff`, `h_buff`, `element_to_mobject`)
com semânticas diferentes**, e as duas nascem com cores de tema escuro. Quase
todo defeito desta área é silencioso — nada some com erro no terminal.

Antes de tudo, porém, há uma decisão que não é de API e que esta skill trata
primeiro (§1): **na maioria das vezes a resposta certa para "põe uma tabela no
vídeo" é não pôr tabela nenhuma.**

## Como ler esta skill

Três marcadores, válidos para o arquivo inteiro:

- **[FONTE]** — conferido lendo o ManimCE 0.21.0 instalado em
  `.venv/lib/python3.12/site-packages/manim/`, com arquivo e linha, ou o índice
  estático de `api/`. Afirmação forte.
- **[HOJE]** — reproduzido nesta sessão (2026-08-19) com `grep`, `awk` e
  Python **puro** (aritmética e formatação de string, sem importar Manim).
  **Nenhum render, nenhum ffmpeg, nenhuma GPU.**
- **[DECK]** — medição ou decisão editorial vinda do deck consumidor
  `~/Projects/aulas`. Testemunho confiável, não reproduzido aqui.

Onde eu não pude verificar, está dito — §16 lista tudo o que ficou em aberto.

## Cartão de referência — o sintoma manda na seção

| O que aconteceu | Onde ler |
|---|---|
| "põe uma tabela nesse slide" | **§1 primeiro** — a decisão antes da API |
| não sei qual das 9 classes usar | §2 |
| `Table([[1, 2]])` explodiu com `TypeError` | §4 |
| a tabela sumiu / as linhas da grade não aparecem | §12 |
| `1234.5` saiu como `1,234.50` e eu queria `1.234,50` | §4.4 |
| `2.5` virou `2` na `IntegerTable` | §4.5 |
| `get_entries((1,1))` devolveu a célula errada | **§5.3** — é o defeito mais traiçoeiro daqui |
| quero destacar uma célula / linha / coluna | §9 |
| o realce ficou preto depois que mexi nele | §9.2 |
| a tabela é grande demais / encolhi e o realce saiu torto | §10 |
| quero a tabela entrando aos poucos | §11 |
| os números da matriz estão sobrepostos | **§7.1** — `h_buff` na `Matrix` é PASSO, não folga |
| os colchetes saíram esticados/finos | §7.3 |
| `Matrix` falhou e o erro fala de LaTeX | §7.3 e §13 |
| quero mudar a fonte/o tamanho de todas as células | §4 e §12 |
| a tabela está lenta para renderizar | §13 |
| que método existe mesmo? | §14 |

---

## 1. A decisão antes da API: essa tabela deve mesmo ir para o vídeo?

Esta seção é a mais importante do arquivo. Um agente que domina `Table` e a usa
sempre que a palavra "tabela" aparece no pedido produz vídeo pior do que um que
não conhece a classe.

### 1.1 A evidência de produção

O deck consumidor deste projeto (`~/Projects/aulas`, o mesmo que gera os vídeos
das aulas) tem, contado no disco **[HOJE]**:

```
11 arquivos de cena · 8.197 linhas de Python · 77 partes renderizadas
ocorrências de `Table`  : 0
ocorrências de `Matrix` : 0
ocorrências de `arrange_in_grid` : 3
```

Zero. Em oito mil linhas de animação didática de produção, a classe `Table`
nunca foi a resposta certa — e três vezes a resposta foi
`VGroup(...).arrange_in_grid(...)` com caixas de tamanho fixo.

### 1.2 Por que a tabela perde no vídeo

Uma tabela é uma estrutura de **consulta**: ela existe para um leitor que varre
de um lado para o outro, volta, compara duas células distantes, e faz isso no
ritmo dele. O quadro de um vídeo é assistido no ritmo de quem apresenta. As
duas coisas brigam.

E há a conta de densidade. **[DECK]** — Garner & Alley (2013), experimento
randomizado com 110 alunos de engenharia, mesmo roteiro narrado, só o design do
slide mudou: o alvo é **~21 palavras por quadro** e **41 palavras é o modo de
falha medido** (esforço mental percebido 3,01 → 3,61 numa escala de 7,
d = −0,50; compreensão 9,39 → 6,73 de 15, d = 0,81, com efeito ainda maior no
teste 10 dias depois). Uma tabela 4×3 com células de três palavras já são 36
palavras, mais os rótulos: passou do limite antes de você acrescentar o título.

Não reproduzi o experimento; estou repassando a evidência do consumidor. Mas a
aritmética das palavras é conferível na sua própria tabela, em cinco segundos.

### 1.3 As três situações em que a tabela SE PAGA

1. **A grade é o argumento.** Tabela-verdade, tabuada, matriz de confusão,
   produto cartesiano: a estrutura bidimensional *é* o conteúdo, e desenhá-la
   como texto corrido destruiria a ideia.
2. **Cada célula é uma batida falada.** Se a tabela entra célula a célula (ou
   linha a linha) e cada revelação corresponde a uma frase do apresentador, ela
   deixa de ser consulta e vira roteiro. Aí ela é boa — e o formato natural é
   uma linha por parte (skill `manim-presentation-parts`).
3. **É pequena de verdade.** Até ~3 colunas × ~4 linhas, com células de uma ou
   duas palavras.

Fora disso: a tabela grande vai para o **material impresso** da aula, não para
a animação.

### 1.4 O que colocar no lugar

| Em vez de | Use | Skill dona |
|---|---|---|
| coluna de números que se comparam | barras | `manim-graphs-plots` (`BarChart`, ou a barra à mão) |
| grade de rótulos categóricos | `VGroup` de caixas iguais + `arrange_in_grid` | `manim-mobjects`, `manim-layout-posicionamento` |
| duas colunas "antes × depois" | dois blocos lado a lado, com o fio no meio | `manim-layout-posicionamento` |
| a tabela completa de referência | a apostila / o handout | fora do Manim |

O idioma que o deck usa, e que resolve o caso "grade de rótulos" melhor que
`Table` **[HOJE, lido em `aulas/002-deepseek-harness/manim/aula_002_run_code.py:282-296`]**:

```python
# Caixas de tamanho FIXO: a grade fica regular mesmo com textos de larguras
# diferentes — o que uma Table não faz (lá a coluna tem a largura da célula
# mais larga, e a grade "respira" de forma irregular).
pilulas = VGroup(*[_caixa(nome, LARGURA, ALTURA, tamanho=T_MIUDO) for nome in FERRAMENTAS])
pilulas.arrange_in_grid(rows=2, cols=4, buff=(0.16, 0.16))
```

Esse padrão dá o que `Table` não dá: célula de tamanho constante, cor por
célula com significado, e cada caixa é um mobject próprio que você anima
sozinho.

**Se depois de tudo isso a tabela continua sendo a resposta certa, o resto
deste arquivo é sobre fazê-la direito.**

---

## 2. As nove classes, e a árvore

```bash
awk -F'\t' '($3=="mobject/table" || $3=="mobject/matrix") && ($1=="class"||$1=="function")' \
  api/manim-ce-index.tsv | cut -f1,2,3
```

**[FONTE]** — `api/manim-ce-inheritance.txt:158-161` e `:241-245`:

```
VMobject
├─ Matrix                    ← NÃO é VGroup
│   ├─ DecimalMatrix
│   ├─ IntegerMatrix
│   └─ MobjectMatrix
└─ VGroup
    └─ Table                 ← é VGroup
        ├─ DecimalTable
        ├─ IntegerTable
        ├─ MathTable
        └─ MobjectTable
```

| classe | `element_to_mobject` padrão | precisa de LaTeX? | serve para |
|---|---|---|---|
| `Table` | `Paragraph` (→ `Text`, Pango) | **não** | texto; a única da família que roda sem LaTeX |
| `MathTable` | `MathTex` | sim | fórmulas, símbolos, tabuada |
| `IntegerTable` | `Integer` | sim (via `MathTex`) | inteiros, com arredondamento (§4.5) |
| `DecimalTable` | `DecimalNumber` (`num_decimal_places=1`) | sim | decimais |
| `MobjectTable` | `lambda m: m` (identidade) | não | células que já são mobjects |
| `Matrix` | `MathTex` | **sim, sempre** (§7.3) | matriz com colchetes |
| `IntegerMatrix` | `Integer` | sim | idem, inteiros |
| `DecimalMatrix` | `DecimalNumber` (`num_decimal_places=1`) | sim | idem, decimais |
| `MobjectMatrix` | `lambda m: m` | **sim** — os colchetes são `MathTex` | matriz de figuras |

As quatro subclasses de `Table` e as três de `Matrix` **não acrescentam método
nenhum**: cada uma tem exatamente 1 método próprio, o `__init__`, e ele só
troca o `element_to_mobject` padrão **[FONTE, `api/manim-ce-methods.tsv`]**.
Escolher entre elas é escolher o conversor de célula — e você pode passá-lo à
mão na `Table` crua, o que dá o mesmo resultado com mais controle (§4).

Contagem de métodos **[FONTE]**: `Table` tem **259** métodos, **18 próprios**
(17 + `__init__`) e 241 herdados de `VGroup`/`VMobject`/`Mobject`. `Matrix` tem
**251**, **9 próprios**. Tudo o que não estiver nas seções abaixo é método
genérico de `Mobject` e pertence a `manim-mobjects` /
`manim-layout-posicionamento`.

### 2.1 A consequência de `Table` ser `VGroup` e `Matrix` não ser

- `Table` recusa filho que não seja `VMobject` (é a checagem do `VGroup`) —
  então **`MobjectTable` não aceita `ImageMobject`**. Uma tabela com prints de
  tela não se faz assim; monte um `Group` à mão (skill `manim-mobjects`, e as
  imagens são de `manim-svg-imagens`).
- A estrutura interna difere, e é por isso que indexar na mão é frágil:
  `tabela[0]` é `self.elements` (todas as células) e `tabela[1:]` são as `Line`
  da grade, uma a uma **[FONTE, `table.py:261-265`]**; `matriz[0]` é
  `self.elements` e `matriz[1]`/`matriz[2]` são o colchete esquerdo e o direito
  **[FONTE, `matrix.py:199-200`]**. Acrescentar `include_outer_lines` muda essa
  contagem. **Use os getters de §8**, nunca o índice.

---

## 3. `Table` — a assinatura inteira

**[FONTE]** `api/manim-ce-index.tsv`, idêntica ao fonte em `table.py:194-222`:

```python
Table(
    table: Iterable[Iterable[float | str | VMobject]],
    row_labels: Iterable[VMobject] | None = None,
    col_labels: Iterable[VMobject] | None = None,
    top_left_entry: VMobject | None = None,
    v_buff: float = 0.8,
    h_buff: float = 1.3,
    include_outer_lines: bool = False,
    include_inner_lines: bool = True,
    add_background_rectangles_to_entries: bool = False,
    entries_background_color: ParsableManimColor = BLACK,
    include_background_rectangle: bool = False,
    background_rectangle_color: ParsableManimColor = BLACK,
    element_to_mobject: Callable[...] | type[VMobject] = Paragraph,
    element_to_mobject_config: dict = {},
    arrange_in_grid_config: dict = {},
    line_config: dict = {},
    **kwargs,
)
```

### 3.1 A ordem de construção, e o que ela decide

**[FONTE, `table.py:224-267`]** — vale decorar porque explica três armadilhas:

```
230-231  row_dim / col_dim  ← contados ANTES dos rótulos: são as dimensões dos DADOS
244-249  valida que toda linha tem o mesmo comprimento
         → ValueError("Not all rows in table have the same length.")
251      super().__init__(**kwargs)      ← a família ainda está VAZIA aqui
252      _table_to_mob_table()           ← element_to_mobject roda em cada célula
253      elements_without_labels = VGroup(*todas as células de dado)
254      _add_labels()                   ← rótulos entram no mob_table
255      _organize_mob_table()           ← arrange_in_grid
256      elements = VGroup(*tudo, com rótulos)
258-259  se elements[0] não tem ponto nenhum, ele é REMOVIDO   ← §5.2
261-262  add(elements); center()
264-265  _add_horizontal_lines(); _add_vertical_lines()
```

**Consequência imediata:** `Table(dados, color=BLACK)` **não pinta nada**. O
`color=` cai em `**kwargs` → `VMobject.__init__` → `init_colors()`, que percorre
`family_members_with_points()` — e na linha 251 a família ainda está vazia; as
células e as linhas nascem depois, cada uma com a cor default dela. Pintar
tabela tem três rotas legítimas, todas em §12.

### 3.2 Os pares de kwargs que ninguém lê até dar errado

| kwarg | default | o que faz de verdade |
|---|---|---|
| `include_inner_lines` | `True` | a grade interna. Desligue para uma "tabela" só de alinhamento |
| `include_outer_lines` | `False` | a moldura externa. O default é **sem** moldura |
| `add_background_rectangles_to_entries` | `False` | um `BackgroundRectangle` por célula, na cor `entries_background_color` (default **`BLACK`**) |
| `include_background_rectangle` | `False` | um retângulo atrás da tabela inteira, cor `background_rectangle_color` (default **`BLACK`**) |
| `line_config` | `{}` | vai direto para cada `Line(...)` da grade — é **o único** jeito de dar cor e espessura à grade na construção |
| `arrange_in_grid_config` | `{}` | vai para `Mobject.arrange_in_grid` — com três chaves proibidas (§6.3) |
| `element_to_mobject_config` | `{}` | vai para cada chamada do conversor de célula |

Os dois defaults `BLACK` são de tema escuro e são a causa nº 1 de "a tabela
ficou com blocos pretos" em projeto de fundo claro (§12).

---

## 4. `element_to_mobject` — o parâmetro que decide tudo

Cada célula é construída assim, e só assim **[FONTE, `table.py:292`]**:

```python
self.element_to_mobject(item, **self.element_to_mobject_config)
```

Uma chamada, um argumento posicional, um dicionário de kwargs. Todo o resto
segue disso.

### 4.1 `Table` com números explode — e o erro não fala de Manim

O default é `Paragraph`, e `Paragraph.__init__` faz
`lines_str = "\n".join(list(text))` **[FONTE, `text_mobject.py:164`]**. Logo
**[HOJE]**:

```
Table([[1, 2]])  →  TypeError: sequence item 0: expected str instance, int found
```

A correção **não** é "converter para string e seguir": é escolher a classe
certa.

| a célula é | use | por quê |
|---|---|---|
| texto | `Table` (`Paragraph`) | sem LaTeX, e `"a\nb"` vira duas linhas na célula |
| inteiro | `IntegerTable` | formata e alinha como número |
| decimal | `DecimalTable` | `num_decimal_places` controlado |
| fórmula | `MathTable` | cada célula num `align*` |
| mobject pronto | `MobjectTable` | identidade |
| **o texto do seu tema** | `Table(..., element_to_mobject=seu_helper)` | §4.3 |

### 4.2 Cabeçalho não vai na grade de dados

`IntegerTable([["modelo", "US$"], [15, 3]])` falha: `Integer("modelo")` não
formata. É por isso que o exemplo oficial da própria classe põe os cabeçalhos em
`col_labels` **[FONTE, `table.py:1118-1131`]** — `row_labels` e `col_labels`
recebem **`VMobject` já construídos**, não passam pelo `element_to_mobject`, e
por isso podem ser de outro tipo que a grade.

```python
IntegerTable(
    [[0, 30, 45], [90, 60, 45]],
    row_labels=[MathTex(r"\sin"), MathTex(r"\cos")],   # VMobjects, não strings
    col_labels=[Tex("a"), Tex("b"), Tex("c")],
)
```

### 4.3 O gancho de tema: é aqui que o projeto entra

`element_to_mobject` aceita qualquer callable de um argumento. Num projeto com
`tema.py` (skill `manim-tema-projeto`), é o ponto único onde a tabela inteira
herda fonte, tamanho e cor:

```python
def celula(s: str) -> Text:
    return txt(s, T_CORPO, TINTA)          # o helper do tema, com cor explícita

tabela = Table(
    [["Opus", "15,00"], ["Sonnet", "3,00"], ["Haiku", "0,80"]],
    col_labels=[celula("modelo"), celula("US$/Mtok")],
    element_to_mobject=celula,
    line_config={"color": DIVISORIA, "stroke_width": 1.2},
    v_buff=0.35,
    h_buff=0.9,
)
```

Duas coisas a notar. **(a)** Os rótulos usam o mesmo helper de propósito — eles
*não* passam pelo `element_to_mobject`, então se você esquecer, eles saem
brancos enquanto o corpo sai na cor certa; é exatamente o tipo de defeito que
não dá erro. **(b)** Esse gancho é também por onde entra o helper de **texto
nítido** do projeto (o que desenha em `font_size=720` e encolhe, por causa do
arredondamento de posição de glifo do cairo). O assunto é de
**`manim-text-latex §3`** — aqui só fica registrado que a tabela não tem via
própria: ou o conversor de célula devolve texto nítido, ou nenhuma célula é.

### 4.4 O separador de milhar é americano, e não há opção de locale

`Integer` e `DecimalNumber` montam a string com o format spec
`"{:" + ("," se group_with_commas) + "." + str(num_decimal_places) + "f}"`
**[FONTE, `numbers.py:251-262`]**. Resultado **[HOJE]**:

```
group_with_commas=True   num_decimal_places=2  →  1,234.50
group_with_commas=False  num_decimal_places=2  →  1234.50
group_with_commas=True   num_decimal_places=0  →  1,234,567
group_with_commas=False  num_decimal_places=0  →  1234567
```

Não existe `1.234,50` em lugar nenhum da API. Para português:

```python
DecimalTable(dados, element_to_mobject_config={"group_with_commas": False})
```
…e, se você precisa de fato do ponto de milhar brasileiro, a única saída é a
`Table` crua com as strings já formatadas pelo seu helper de tema
(`usd()`/`vezes()` e afins — `manim-tema-projeto`).

### 4.5 `IntegerTable` arredonda para o par mais próximo, calado

`Integer` é `DecimalNumber(num_decimal_places=0)` → format `"{:,.0f}"` → a
regra do Python é **half-to-even**, não "meio para cima". Medido **[HOJE]**:

```
0.5 → 0     1.5 → 2     2.5 → 2     3.5 → 4     3.7 → 4     -2.5 → -2
```

Uma coluna de médias medidas passa por `IntegerTable` e sai com dois valores
`2,5` virando `2` e `3` sem nenhum aviso. Se o número na parede importa, use
`DecimalTable` com casas explícitas, ou `Table` com a string que você mesmo
formatou. (E todo número na parede carrega procedência — a regra é do deck,
registrada em `manim-graphs-plots §23`.)

### 4.6 `MobjectTable` **move** os mobjects, não copia

O conversor é a identidade **[FONTE, `table.py:1088-1089`]**, e
`_organize_mob_table` chama `arrange_in_grid` **nos objetos que você passou**.
Duas consequências:

- o mesmo mobject em duas células aparece **uma vez só** (a segunda posição
  vence); o exemplo oficial usa `a.copy()`, `b.copy()` **[FONTE, `table.py:1075`]**;
- os mobjects que você tinha posicionado na cena **se mudam** para dentro da
  tabela.

---

## 5. Rótulos, o mobject fantasma, e as duas numerações

### 5.1 Como os rótulos entram

**[FONTE, `table.py:324-353`]**: `row_labels` vira a primeira coluna,
`col_labels` vira a primeira linha, e quando os dois existem o canto superior
esquerdo precisa de alguém. Se você deu `top_left_entry`, é ele. Se não deu, o
Manim insere um **mobject vazio de placeholder** só para o `arrange_in_grid`
fechar a conta.

### 5.2 O placeholder é removido depois — e ele não é o único candidato

```python
if len(self.elements[0].get_all_points()) == 0:
    self.elements.remove(self.elements[0])          # table.py:258-259
```

A remoção é incondicional quanto à origem: ela derruba **o primeiro elemento
que não tiver ponto nenhum**, seja o placeholder, seja um `top_left_entry` que
você passou e que renderizou vazio. Quando isso acontece com um `top_left_entry`
real, todos os índices de `get_entries(pos)` deslizam uma posição e você
descobre pelo destaque na célula errada.

### 5.3 A armadilha: `get_entries((1,1))` devolve a última célula

A aritmética **[FONTE, `table.py:630-639`]**:

```python
if row_labels and col_labels and top_left_entry is None:
    index = len(self.mob_table[0]) * (pos[0] - 1) + pos[1] - 2      # ← o -2
else:
    index = len(self.mob_table[0]) * (pos[0] - 1) + pos[1] - 1
```

O `-2` compensa o placeholder removido. Mas em `pos=(1,1)` — o canto vazio, que
não existe como célula — a conta dá **−1**, e `Mobject.__getitem__` normaliza
índice negativo com `range(len(self))[value]` **[FONTE, `mobject.py:2515`]**.
Não há erro: você recebe a **última célula da tabela**.

Simulado **[HOJE]** com a aritmética exata do fonte, para uma tabela 2×2 com
os dois conjuntos de rótulos e sem `top_left_entry`:

```
grade   : [[DUMMY, C1, C2], [R1, d11, d12], [R2, d21, d22]]
elements: [C1, C2, R1, d11, d12, R2, d21, d22]

get_entries((1,1)) → d22   ← ERRADO, e silencioso
get_entries((1,2)) → C1    ✓ (rótulo de coluna)
get_entries((2,1)) → R1    ✓ (rótulo de linha)
get_entries((2,2)) → d11   ✓ (primeira célula de dado)
get_entries((3,3)) → d22   ✓
```

### 5.4 As duas numerações, lado a lado

Existem **duas** origens de coordenadas, e trocar uma pela outra é o erro de
destaque mais comum:

| método | conta a partir de | fórmula **[FONTE]** |
|---|---|---|
| `get_entries(pos)` | a grade **com** rótulos: `(1,1)` é o canto superior esquerdo da grade inteira | `table.py:634/637` |
| `get_entries_without_labels(pos)` | só os **dados**: `(1,1)` é a primeira célula de dado | `col_dim * (row-1) + col - 1`, `table.py:682` |
| `get_cell(pos)` / `get_highlighted_cell(pos)` / `add_highlighted_cell(pos)` | a grade **com** rótulos, via `get_rows()[pos[0]-1]` e `get_columns()[pos[1]-1]` | `table.py:820-821` |

Note que `col_dim` foi fixado **antes** dos rótulos (`table.py:231`) — é por
isso que `get_entries_without_labels` tem uma fórmula mais simples e nunca sofre
do problema de §5.3.

**Regra prática:** para mexer em dado, use sempre
`get_entries_without_labels((i, j))`. Para desenhar realce, use `get_cell`, e
lembre que ali o `(1,1)` inclui a faixa de rótulos.

---

## 6. A grade: buffers, linhas e `arrange_in_grid_config`

### 6.1 `h_buff` / `v_buff` na `Table` são FOLGA

**[FONTE, `table.py:316-320`]** os dois viram o `buff` de
`Mobject.arrange_in_grid`:

```python
help_table.arrange_in_grid(rows=..., cols=..., buff=(self.h_buff, self.v_buff),
                           **self.arrange_in_grid_config)
```

E `arrange_in_grid` mede **[FONTE, `mobject.py:2837-2842`]**:

```python
measured_heigths = [max(grid[r][c].height for c in range(cols)) for r in range(rows)]
measured_widths  = [max(grid[r][c].width  for r in range(rows)) for c in range(cols)]
```

Ou seja: **a largura de uma coluna é a da célula mais larga dela**, e o buffer é
o vão entre colunas. Numa `Table`, células não se sobrepõem — a única forma de
provocar isso é forçar `col_widths`/`row_heights` menores que o conteúdo pelo
`arrange_in_grid_config` (§6.3). Os defaults (1,3 horizontal, 0,8 vertical) são
folgados para texto grande; para uma tabela compacta de aula, algo entre 0,3 e
0,9 costuma ser o alvo.

O outro lado da mesma moeda: **a grade de uma `Table` é irregular de propósito**
— cada coluna tem a largura do seu conteúdo. Se você quer células do mesmo
tamanho (que é o que faz uma grade parecer desenhada, e não composta), `Table`
é a ferramenta errada; volte para §1.4.

### 6.2 A grade nasce branca

As linhas são `Line(..., **self.line_config)` **[FONTE, `table.py:355-421`]**, e
`Line` sem cor é branca. Em fundo claro a grade some **sem erro**. `line_config`
é o único caminho na construção:

```python
line_config={"color": DIVISORIA, "stroke_width": 1.2}
```

### 6.3 As três chaves que fazem `arrange_in_grid_config` explodir

`rows`, `cols` e `buff` já são passados pelo próprio `Table`. Repeti-los no
dicionário é `TypeError` **[HOJE, reproduzido com a assinatura real]**:

```
{'buff': 0.5}             → TypeError: arrange_in_grid() got multiple values for keyword argument 'buff'
{'rows': 3}               → TypeError: ... 'rows'
{'cols': 2}               → TypeError: ... 'cols'
{'col_alignments': 'lrr'} → ok
```

O que **sobra** e é útil **[FONTE, assinatura de `Mobject.arrange_in_grid`]**:
`cell_alignment`, `row_alignments`, `col_alignments`, `row_heights`,
`col_widths`, `flow_order`.

```python
# alinhar a coluna de rótulos à esquerda e as duas de números à direita
Table(dados, row_labels=[...],
      arrange_in_grid_config={"col_alignments": "lrr"})
```

Duas ressalvas, ambas do fonte:

- o comprimento de `col_alignments` tem de bater com o número de colunas
  **incluindo a coluna de rótulos**, senão
  `ValueError: col_alignments has a mismatching size.` **[FONTE, `mobject.py:2783`]**;
- **não mexa em `flow_order`**. O default `"rd"` é o que faz `mob_table` (que já
  está em ordem de leitura) cair nas posições certas; qualquer outro valor
  embaralha a tabela sem erro.

`col_alignments` alinha a **caixa** da célula na coluna, não a vírgula decimal.
Para números de larguras diferentes alinharem pelo dígito, use `DecimalTable`
com o mesmo `num_decimal_places` em todas.

---

## 7. `Matrix` — mesmos nomes, outra semântica

**[FONTE]** a assinatura completa (`matrix.py:165-188`):

```python
Matrix(
    matrix: Iterable[Iterable[Any] | Vector2DLike],
    v_buff: float = 0.8,
    h_buff: float = 1.3,
    bracket_h_buff: float = MED_SMALL_BUFF,      # 0.25
    bracket_v_buff: float = MED_SMALL_BUFF,      # 0.25
    add_background_rectangles_to_entries: bool = False,
    include_background_rectangle: bool = False,
    element_to_mobject: type[VMobject] | Callable[..., VMobject] = MathTex,
    element_to_mobject_config: dict[str, Any] = {},
    element_alignment_corner: Vector3DLike = DR,
    left_bracket: str = "[",
    right_bracket: str = "]",
    stretch_brackets: bool = True,
    bracket_config: dict = {},
    **kwargs,
)
```

### 7.1 `h_buff` e `v_buff` aqui são PASSO, não folga — e por isso há sobreposição

A `Matrix` **não usa `arrange_in_grid`**. Ela posiciona cada entrada num
reticulado fixo **[FONTE, `matrix.py:220-229`]**:

```python
mob.move_to(i * self.v_buff * DOWN + j * self.h_buff * RIGHT,
            self.element_alignment_corner)          # element_alignment_corner = DR
```

Cada entrada tem o **canto inferior-direito** ancorado no ponto do reticulado.
Logo:

- o passo entre colunas é `h_buff = 1,3`, **independente do conteúdo**;
- uma entrada mais larga que 1,3 **invade a coluna anterior** (ela cresce para a
  esquerda, porque está ancorada pela direita);
- uma entrada mais alta que `v_buff = 0,8` — uma fração de duas linhas, por
  exemplo — encosta na de cima.

Nada disso emite aviso. É a diferença estrutural nº 1 entre as duas famílias, e
explica por que todo exemplo de `Matrix` na documentação usa entradas curtas:

| | `Table` | `Matrix` |
|---|---|---|
| motor de posicionamento | `arrange_in_grid` | reticulado fixo `i·v_buff·DOWN + j·h_buff·RIGHT` |
| `h_buff` significa | folga entre colunas | **passo** entre colunas |
| largura da coluna | a da célula mais larga | fixa |
| sobreposição possível? | não | **sim, calada** |
| alinhamento da entrada | `cell_alignment` (default centrado) | `element_alignment_corner` (default `DR`) |

Entrada larga demais? Aumente `h_buff` até caber, ou encolha as entradas com
`element_to_mobject_config={"font_size": ...}`.

O `element_alignment_corner=DR` é também o motivo de os números de uma matriz
saírem visualmente alinhados à direita — o que é o que se quer para números, e
o oposto do que se quer para palavras. Para palavras: `element_alignment_corner=ORIGIN`
(centrado) ou `DL` (à esquerda).

### 7.2 Os getters da `Matrix` são um subconjunto dos da `Table`

**[FONTE]** os 9 métodos próprios: `__init__`, `add_background_to_entries`,
`get_brackets`, `get_columns`, `get_entries`, `get_mob_matrix`, `get_rows`,
`set_column_colors`, `set_row_colors`.

**Não existem** em `Matrix`: `get_cell`, `get_highlighted_cell`,
`add_highlighted_cell`, `get_labels`, `get_horizontal_lines`,
`get_vertical_lines`, `create`, e a sobrescrita de `scale`. Destacar uma
entrada de matriz é `SurroundingRectangle` sobre `get_entries()[k]` ou sobre
`get_rows()[i]` (§9.4). E `Matrix.get_entries()` **não aceita `pos`** — ela
devolve o `VGroup` inteiro, em ordem de leitura; o elemento `(i, j)` é
`get_mob_matrix()[i][j]` ou `get_rows()[i][j]`.

### 7.3 Os colchetes são LaTeX — sempre, inclusive na `MobjectMatrix`

**[FONTE, `matrix.py:230-282`]** `_add_brackets` é chamado incondicionalmente no
`__init__` (`matrix.py:200`) e monta os dois colchetes com `MathTex`. Ou seja:

- **qualquer** `Matrix` precisa de LaTeX funcionando, mesmo
  `MobjectMatrix([[Circle(), Square()]])`;
- `left_bracket` / `right_bracket` são **strings LaTeX**: `"("`, `r"\{"`,
  `r"\langle"`, `r"\|"`. Um `"("` simples funciona; um `"{"` sem escape não;
- `bracket_config` vai para os dois `MathTex` (é onde entra `color=`).

A altura vem de uma constante interna: `BRACKET_HEIGHT = 0.5977` e
`n = int(self.height / BRACKET_HEIGHT) + 1` linhas de `\quad` num array vazio
**[FONTE, `matrix.py:248-250`]** — o LaTeX só sabe produzir colchetes em passos
discretos. Por isso existe `stretch_brackets=True` (default), que faz

```python
bracket_pair.stretch_to_fit_height(self.height + 2 * self.bracket_v_buff)   # matrix.py:277
```

`stretch_to_fit_height` **deforma**: numa matriz alta o traço do colchete estica
junto e fica visivelmente fino ou grosso. Se o colchete parece errado, é isso —
`stretch_brackets=False` devolve o desenho nativo do LaTeX, quantizado nos
passos de 0,5977, com a folga que sobrar.

`bracket_v_buff` está documentado como "altura dos colchetes", mas no código ele
é a **folga extra** acima e abaixo do conteúdo. `bracket_h_buff` é a distância
lateral entre a matriz e cada colchete (`next_to(..., buff=bracket_h_buff)`).

### 7.4 As três funções soltas do módulo

**[FONTE, `api/manim-ce-index.tsv`]** — as três estão no topo (`from manim import ...`):

```python
matrix_to_tex_string(matrix: np.ndarray) -> str
matrix_to_mobject(matrix: np.ndarray) -> MathTex
get_det_text(matrix: Matrix, determinant: int | str | None = None,
             background_rect: bool = False, initial_scale_factor: float = 2) -> VGroup
```

- `matrix_to_tex_string` monta `\left[ \begin{array}{cc} … \end{array} \right]`
  e trata `ndim == 1` reformatando como coluna **[FONTE, `matrix.py:60-68`].
- `matrix_to_mobject` é `MathTex(matrix_to_tex_string(m))`: uma matriz que é **um
  único mobject de LaTeX**. Você perde `get_rows`, `get_entries`, o realce por
  célula — tudo. Serve quando a matriz é só um símbolo dentro de uma equação
  maior; nunca quando você vai animar partes dela.
  Aviso do próprio fonte: o comentário em `matrix.py:56-57` diz que as duas
  funções **não são usadas em lugar nenhum do arquivo** e que a manutenção não
  sabia se as manteria.
- `get_det_text` devolve um `VGroup` com `det`, os parênteses e opcionalmente
  `= valor`. **Ele não é adicionado à matriz** — o exemplo oficial diz
  literalmente "must add the matrix" e faz `self.add(matrix)` e `self.add(det)`
  separados **[FONTE, `matrix.py:578` e `:623-624`]**. Consequência prática: mover a
  matriz depois **não** leva o `det` junto. Se for mover, embrulhe os dois num
  `VGroup` você mesmo.

---

## 8. Ler pedaços: o mapa dos getters, e quais devolvem embrulho descartável

Isto resolve metade dos bugs de animação de tabela, e não está em documentação
nenhuma.

| chamada | devolve | é o objeto real ou um embrulho novo? |
|---|---|---|
| `Table.get_entries()` | `self.elements` | **real** — é submobject da tabela |
| `Table.get_entries_without_labels()` | `self.elements_without_labels` | embrulho **persistente**, criado no `__init__`, **não** é submobject |
| `Table.get_horizontal_lines()` / `get_vertical_lines()` | `self.horizontal_lines` / `self.vertical_lines` | embrulho **persistente**; as `Line` em si são submobjects da tabela |
| `Table.get_rows()` / `get_columns()` / `get_labels()` / `get_row_labels()` / `get_col_labels()` | `VGroup` novo | **embrulho descartável** — outro objeto a cada chamada |
| `Table.get_cell(pos)` | `Polygon` novo | **não faz parte da tabela** até você `add` |
| `Table.get_highlighted_cell(pos)` | `BackgroundRectangle` novo | idem |
| `Matrix.get_entries()` | `self.elements` | **real** |
| `Matrix.get_brackets()` | `self.brackets` | embrulho persistente (os dois colchetes são submobjects) |
| `Matrix.get_rows()` / `get_columns()` | `VGroup` novo | **descartável** |
| `Matrix.get_mob_matrix()` | `list[list[VMobject]]` | as células reais, em lista de listas |

**[FONTE]** para as linhas "descartável": `table.py:499` e `:530`,
`matrix.py:304-310` e `:361`.

O que decorre disso:

1. **Identidade não vale.** `tabela.get_rows()[1] is tabela.get_rows()[1]` é
   `False`. Guarde a referência numa variável se você vai usá-la duas vezes.
2. **Animar pelo embrulho funciona** — ele contém as células reais, então
   `self.play(tabela.get_rows()[1].animate.set_color(ACENTO))` pinta as células
   de verdade.
3. **Mover pelo embrulho quebra a tabela.** `tabela.get_rows()[1].shift(UP)`
   move as células e deixa as linhas da grade para trás. Para mover, mova a
   tabela.
4. **Introduzir pelo embrulho suja a cena.** É exatamente o que acontece com
   `create()` — §11.1.

---

## 9. Destacar célula, linha e coluna — quatro caminhos

### 9.1 `add_highlighted_cell` — o pronto, e o que ele realmente faz

```python
Table.add_highlighted_cell(pos=(1, 1), color=PURE_YELLOW, **kwargs) -> Self
Table.get_highlighted_cell(pos=(1, 1), color=PURE_YELLOW, **kwargs) -> BackgroundRectangle
Table.get_cell(pos=(1, 1), **kwargs) -> Polygon
```

**[FONTE, `table.py:884-922`]** `add_highlighted_cell` chama `get_highlighted_cell`,
faz `self.add_to_back(bg_cell)` (fica atrás de tudo dentro da tabela) e ainda
grava `entry.background_rectangle = bg_cell` na célula — é esse atributo que
`create()` procura depois (§11.1).

Três defaults que quase sempre precisam mudar num projeto com tema: a cor é
`PURE_YELLOW` (`#FFFF00`), o preenchimento é `fill_opacity=0.75` e o traço é
zero **[FONTE, `shape_matchers.py:108-129`]**. Amarelo puro a 75% sobre canvas
branco lava o texto por baixo.

### 9.2 A armadilha: `BackgroundRectangle` recusa restilização

**[FONTE, `shape_matchers.py:136-144`]**:

```python
def set_style(self, fill_opacity: float, **kwargs) -> Self:
    # Unchangeable style, except for fill_opacity
    super().set_style(stroke_color=BLACK, stroke_width=0,
                      fill_color=BLACK, fill_opacity=fill_opacity, ...)
```

Duas consequências, e as duas são silenciosas:

- `realce.match_style(outra_coisa)` chama `set_style` **[FONTE, `vectorized_mobject.py:459`]**
  → **o realce vira preto**;
- `realce.set_style(fill_color=RED)` é `TypeError: set_style() missing 1
  required positional argument: 'fill_opacity'` — a assinatura desta subclasse
  não é a de `VMobject`.

O que **funciona** é `realce.set_color(...)`, porque `VMobject.set_color` chama
`set_fill`/`set_stroke` direto, sem passar por `set_style`
**[FONTE, `vectorized_mobject.py:473-476`]**. E `Create(realce)` também é
peculiar: `BackgroundRectangle.pointwise_become_partial` foi sobrescrito para
mexer só na opacidade **[FONTE, `shape_matchers.py:132-134`]**, então `Create`
nele se comporta como um fade, não como um traço sendo desenhado.

### 9.3 O caminho recomendado em projeto com tema: `get_cell` + `Polygon`

`get_cell(pos, **kwargs)` devolve um `Polygon` cru, com os quatro cantos da
célula (borda + meio buffer de cada lado) **[FONTE, `table.py:788-843`]**, e os
`kwargs` vão direto para o `Polygon`. Sem `set_style` travado, sem cor forçada,
sem opacidade de 0,75:

```python
realce = tabela.get_cell((3, 2), fill_color=ACENTO, fill_opacity=0.12, stroke_width=0)
tabela.add_to_back(realce)          # atrás das células, dentro da tabela
```

Cuidado com um default, **e é o oposto do que se supõe num canvas claro:**
`Polygon` sem cor **não** nasce branco — nasce **azul `#58C4DD`** (o `BLUE` do
Manim), com `stroke_width=4`. `Polygon` é `Polygram` puro
(`geometry/polygram.py:341`), e `Polygram.__init__` tem
`color: ParsableManimColor = BLUE` (`:83-89`;
`utils/color/manim_colors.py:162`).

Consequência prática: um `get_cell` sem `color=` **não some** no fundo branco —
vira um retângulo azul-Manim gritante com 4 px de traço. É mais fácil de
perceber que o caso do texto (§12), e por isso mais fácil de deixar passar num
preview rápido. Se você quer só o preenchimento, zere o traço explicitamente,
como acima.

O idioma oficial de "moldura na célula" usa o mesmo método com traço:

```python
tabela.add(tabela.get_cell((2, 2), color=ACENTO, stroke_width=2))   # table.py:24
```

### 9.4 Linha, coluna e entrada de matriz: `SurroundingRectangle`

```python
SurroundingRectangle(*mobjects, color=PURE_YELLOW, buff=SMALL_BUFF, corner_radius=0.0, **kwargs)
#                            └ #FFFF00, não o YELLOW #F7D96F   └ = 0.1
```

```python
faixa = SurroundingRectangle(tabela.get_rows()[2], color=ACENTO, buff=0.14, corner_radius=0.06)
coluna = SurroundingRectangle(tabela.get_columns()[1], color=ACENTO, buff=0.14)
entrada = SurroundingRectangle(matriz.get_entries()[3], color=ACENTO, buff=0.08)
```

É também o único caminho para `Matrix`, que não tem `get_cell` (§7.2). O default
`color=YELLOW` é de tema escuro — passe a sua cor sempre.

**Fronteira:** `SurroundingRectangle`, `Brace`, `Indicate`, `Circumscribe` e
`Flash` — o pacote de **apontar para a coisa** — **não têm skill dona hoje**
neste projeto. Use as assinaturas, não invente semântica; e ver §17.

### 9.5 `set_row_colors` / `set_column_colors` e o off-by-one dos rótulos

```python
Table.set_row_colors(*colors) -> Self          # table.py:561-587
Table.set_column_colors(*colors) -> Self
Matrix.set_row_colors(*colors) -> Self         # matrix.py:363-391
```

O corpo é `for color, row in zip(colors, self.get_rows(), strict=False)`
**[FONTE]**. Duas coisas:

- **`get_rows()` inclui a linha de rótulos** quando há `col_labels` (e
  `get_columns()` inclui a coluna de rótulos quando há `row_labels`). Então, numa
  tabela com cabeçalho, `set_row_colors(VERMELHO, AZUL)` pinta **o cabeçalho e a
  primeira linha de dados** — não as duas primeiras linhas de dados. Ou você
  passa a cor do cabeçalho como primeiro argumento, ou abandona o método e pinta
  o índice que quer: `tabela.get_rows()[1].set_color(ACENTO)`.
- `strict=False` significa que **sobra sem reclamar**: menos cores que linhas
  pinta só as primeiras; mais cores que linhas ignora o excesso. Nunca dá erro,
  e um off-by-one aqui é invisível no terminal.
- passar uma **lista** onde se espera uma cor (`set_row_colors([RED, BLUE], GREEN)`,
  como no exemplo oficial do próprio módulo) não distribui as cores pelas
  células: `set_fill` repassa a lista inteira a cada submobject
  **[FONTE, `vectorized_mobject.py:322-325`]**, e uma lista de cores vira
  **gradiente dentro de cada célula**. É comportamento de `set_color`, não de
  `Table`.

### 9.6 z-index: quem fica na frente

Realce, linhas de grade e células podem se cobrir. O exemplo do próprio módulo
resolve com `set_z_index` **[FONTE, `table.py:31-33`]**, e o `create()` empurra
as células para `z_index=2` **[FONTE, `table.py:976`]**. Se o seu realce
esconde a linha de grade (ou vice-versa), é aí que se mexe — a mecânica de
`z_index` é de `manim-mobjects`.

---

## 10. Escala: o único método que `Table` sobrescreve

```python
Table.scale(scale_factor: float, scale_stroke: bool = False, **kwargs) -> Self
```

**[FONTE, `table.py:998-1006`]**:

```python
self.h_buff *= scale_factor
self.v_buff *= scale_factor
super().scale(scale_factor, scale_stroke=scale_stroke, **kwargs)
```

O comentário no próprio fonte diz por quê: `get_cell` reconstrói o polígono a
partir de `h_buff`/`v_buff` **em tempo de chamada**. Se os buffers não
acompanharem a escala, todo realce criado depois sai com a folga do tamanho
antigo.

### 10.1 O que passa por essa sobrescrita — e o que escapa

**Passa (seguro):**

```python
tabela.scale(0.6)
tabela.width = 8.0                 # width.setter → scale_to_fit_width → rescale_to_fit → self.scale
tabela.scale_to_fit_width(8.0)     # mobject.py:1757-1767
tabela.scale_to_fit_height(3.0)
```

**Escapa (silencioso):**

```python
VGroup(tabela, legenda).scale(0.6)     # ← Mobject.scale transforma PONTOS da família;
                                       #   não chama Table.scale de ninguém
Group(t0, t1).scale(0.5).arrange(...)  # ← e este é o exemplo oficial do módulo!
tabela.stretch_to_fit_width(8.0)       # stretch, não scale — e ainda deforma os glifos
```

**[FONTE, `mobject.py:1335-1337`]** `Mobject.scale` chama
`apply_points_function_about_point` sobre a família inteira; ele **não** invoca
o `.scale()` de cada submobject. Então escalar a tabela por um grupo-pai a
desenha certinho e deixa `h_buff`/`v_buff` com o valor antigo. `get_cell`,
`get_highlighted_cell` e `add_highlighted_cell` passam a devolver um retângulo
grande demais (fator 1/escala), invadindo as células vizinhas.

**Regra:** escale a `Table` **pelo próprio objeto**, antes de agrupá-la; e crie
os realces **depois** de escalar. Se você precisa mesmo escalar o grupo, crie os
realces antes e escale tudo junto — o polígono já existente escala com o resto.

`Matrix` **não** sobrescreve `scale`, e não precisa: os buffers dela só são
usados na construção.

---

## 11. Animar a entrada

### 11.1 `create()` — o pronto, e as três coisas que ele faz que você não espera

```python
Table.create(lag_ratio: float = 1,
             line_animation: Callable = Create,
             label_animation: Callable = Write,
             element_animation: Callable = Create,
             entry_animation: Callable = FadeIn,
             **kwargs) -> AnimationGroup
```

**[FONTE, `table.py:924-996`]**. Ele monta, nesta ordem:

1. `line_animation(VGroup(vertical_lines, horizontal_lines), **kwargs)`
2. `element_animation(elements_without_labels.set_z_index(2), **kwargs)`
3. se há rótulos: `label_animation(get_labels(), **kwargs)`
4. um `entry_animation` por célula que tenha `background_rectangle` (ou seja:
   por célula que você destacou com `add_highlighted_cell` antes)

E devolve `AnimationGroup(*animations, lag_ratio=lag_ratio)`.

**(a) `lag_ratio=1` é sequencial, e a conta dá mais que você espera.** Com
`lag_ratio=1` cada animação começa quando a anterior acaba, e `init_run_time`
toma o máximo dos tempos de fim **[FONTE, `composition.py:146-160`]**. Os
`run_time` das filhas: `Create` usa o default 1,0 s
**[FONTE, `animation.py:26`]**, mas **`Write` usa 1 s se o alvo tiver menos de
15 membros de família com pontos, e 2 s a partir daí**
**[FONTE, `creation.py:344-354`]** — uma linha de rótulos com quatro palavras
passa desse limite fácil. Então uma tabela **com** rótulos custa 1 + 1 + 2 =
**4 s** de default. Para aula, isso é uma eternidade:

```python
self.play(tabela.create(lag_ratio=0.35), run_time=1.4)
```

**(b) Os `**kwargs` vão para as animações-filhas, não para o grupo.**
`tabela.create(run_time=0.6)` dá 0,6 s **a cada** filha — total 1,8 s, não 0,6.
Para controlar o total, passe `run_time` no `self.play`, como acima. Só o
`lag_ratio` é do grupo (é parâmetro nomeado de `create`, não vai nos kwargs).

**(c) Ele adiciona *embrulhos* à cena, não a tabela.** Os alvos das animações
são `VGroup(vertical_lines, horizontal_lines)`, `elements_without_labels` e
`get_labels()` — todos embrulhos (§8). Como são introducers, é isso que entra em
`scene.mobjects`; a `tabela` em si **nunca é adicionada**. Depois, um
`FadeOut(tabela)` não remove nada da lista da cena, e `self.remove(tabela)` é
no-op.

A correção é uma linha, e vale sempre:

```python
self.play(tabela.create(lag_ratio=0.35), run_time=1.4)
self.add(tabela)        # a cena passa a ser dona da TABELA; os embrulhos saem da lista
```

`Scene.add` chama `restructure_mobjects(to_remove=[tabela])`, que remove da lista
todo mobject cuja família esteja contida na de `tabela` — os embrulhos
desaparecem, e sobra a tabela **[FONTE, `scene.py:521-526`, `724-731`, `755-769`]**.

### 11.2 Linha por linha, com o embrulho na mão

Quando cada linha é uma frase falada, o `create()` não serve — você quer
controlar o ritmo:

```python
tabela = Table(...)
grade = VGroup(tabela.get_horizontal_lines(), tabela.get_vertical_lines())
linhas = list(tabela.get_rows())      # UMA chamada: cada uma devolve embrulhos novos (§8)

self.play(Create(grade), run_time=0.5)
self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.18) for l in linhas], lag_ratio=0.25))
self.add(tabela)
```

`lag_ratio` e `run_time` como decisão de ritmo são de **`manim-composicao-ritmo`**;
aqui só interessa que os alvos certos existem e como pegá-los.

### 11.3 Uma linha por PARTE — o formato de palestra

Se a tabela é o conteúdo de uma cena de slide, cada linha revelada é um recado
falado, e recado falado é clique novo. O formato (mixin `_Atos`, `_corte(n)`,
subclasses `P1..PN`) é inteiro de **`manim-presentation-parts`**. O que esta
skill acrescenta: a tabela deve ser **construída inteira uma vez**, no ato 1, e
os atos seguintes só revelam pedaços dela — nunca reconstruir a tabela por
parte, senão o primeiro frame da parte N+1 deixa de ser o último da N e a emenda
quebra.

### 11.4 Trocar um valor no lugar

Duas rotas, e a escolha depende de a célula ser ou não um `DecimalNumber`.

```python
# Qualquer tabela: transforma o mobject velho no novo, ancorado onde o velho estava.
antigo = tabela.get_entries_without_labels((2, 3))
novo = celula("9,51").move_to(antigo)
self.play(Transform(antigo, novo))
```

```python
# DecimalTable / IntegerTable: a célula JÁ é um DecimalNumber
tabela.get_entries_without_labels((2, 3)).set_value(9.51)
```

Armadilha do segundo caminho: `DecimalNumber.set_value` re-ancora o número em
`edge_to_fix`, que por padrão é `LEFT` **[FONTE, `numbers.py:291-296`]** — o
número **cresce para a direita** e sai do centro da célula. Numa tabela, ou você
passa `element_to_mobject_config={"edge_to_fix": ORIGIN}` para ele crescer
centrado, ou aceita o deslocamento. E `set_value` reconstrói os submobjects, um
`SingleStringMathTex` por caractere **[FONTE, `numbers.py:155-160`]** — número
vivo dentro de tabela é caro e é assunto de
**`manim-updaters-valuetracker`**.

### 11.5 O realce que anda

```python
faixa = SurroundingRectangle(tabela.get_rows()[1], color=ACENTO, buff=0.12)
self.play(Create(faixa))
for i in (2, 3):
    self.play(Transform(faixa, SurroundingRectangle(tabela.get_rows()[i],
                                                    color=ACENTO, buff=0.12)))
```

`Transform` (e não `.animate.move_to`) porque as linhas têm larguras diferentes
— o retângulo precisa mudar de tamanho, não só de lugar. A distinção
`Transform` × `ReplacementTransform` é de **`manim-animations §8`**.

---

## 12. Fundo claro: tudo o que some sem erro

Esta é a seção que mais economiza render. O Manim escreve branco por padrão;
em canvas claro, cada item abaixo desaparece **sem uma linha no terminal**.

| o que | por que some | a correção |
|---|---|---|
| o texto das células | `Paragraph`→`Text` nasce branco | `element_to_mobject_config={"color": TINTA}`, ou um `element_to_mobject` do tema (§4.3) |
| os **rótulos** | você os construiu à mão e esqueceu a cor | passe a cor ao criar cada `Text`/`MathTex` do `row_labels`/`col_labels` |
| as linhas da grade | `Line` sem cor é branca | `line_config={"color": DIVISORIA, "stroke_width": 1.2}` |
| os colchetes da `Matrix` | `MathTex` sem cor é branco | `bracket_config={"color": TINTA}` |
| — | — | — |
| **blocos pretos** onde deveria haver nada | `entries_background_color` e `background_rectangle_color` têm default **`BLACK`** | passe a cor do seu canvas, ou não ligue esses flags |
| `Table.add_background_to_entries()` sem argumento | assinatura `(color=BLACK)` **[FONTE, `table.py:782`]** | `tabela.add_background_to_entries(color=CANVAS)` |
| `Matrix.add_background_to_entries()` | assinatura **sem parâmetro nenhum**; usa `config.background_color` **[FONTE, `matrix.py:393-403`]** | funciona sozinha se `config.background_color` já é o seu canvas |

Repare na **assimetria da API**: o método tem o mesmo nome nas duas famílias e
assinatura diferente. Na `Table` ele exige que você passe a cor; na `Matrix` ele
acerta sozinho, porque `BackgroundRectangle` com `color=None` cai em
`config.background_color` **[FONTE, `shape_matchers.py:118-119`]**.

E o que **não** funciona, por mais natural que pareça:

```python
Table(dados, color=TINTA)      # ← não pinta NADA (§3.1: a família está vazia no super().__init__)
```

As três rotas que funcionam:

1. na construção, pelos `*_config` (é a preferida — o mobject nasce certo);
2. depois, com `tabela.set_color(TINTA)` — percorre a família inteira, inclusive
   as linhas da grade, e por isso apaga a distinção entre grade e texto;
3. peça a peça: `tabela.get_entries().set_color(TINTA)`,
   `tabela.get_horizontal_lines().set_color(DIVISORIA)`.

A decisão de **qual** cor, o contraste WCAG e o `tema.py` são de
**`manim-color-theming`** (§5 para contraste, §11 para a disciplina de paleta) e
**`manim-tema-projeto`**. Esta skill só diz onde o valor entra.

---

## 13. Custo: quanto LaTeX uma tabela compila

- `Table` com `Paragraph`/`Text`: **zero LaTeX**. É a única das nove cujo
  conversor padrão não passa por LaTeX. (`MobjectTable` também pode ser zero —
  mas aí quem decide é o mobject que você entregou.)
- `MathTable`: um `MathTex` por célula — 20 células, até 20 compilações na
  primeira vez.
- `IntegerTable` / `DecimalTable` / `IntegerMatrix` / `DecimalMatrix`: um
  `SingleStringMathTex` **por caractere** do número
  **[FONTE, `numbers.py:155-160`]**. Parece pior do que é: o cache de LaTeX é
  indexado pela string, e há só dez dígitos, o ponto, a vírgula e o sinal — a
  segunda tabela de números é praticamente de graça.
- `Matrix` de qualquer tipo: **+2 compilações** só para os colchetes, e são
  strings longas (um `array` de `\quad` proporcional à altura), o que significa
  que **mudar a altura da matriz gera uma string de colchete nova** e um miss de
  cache.

Onde esse cache mora, como invalidá-lo e por que ele **não enxerga dado externo**
(um CSV que mudou não muda o hash) é de **`manim-performance-cache`**; por que o
LaTeX às vezes falha só fora do `bin/mx` é de **`manim-troubleshooting`** e
**`manim-text-latex §15-16`**.

---

## 14. Descobrir o resto sem chutar

```bash
# tudo que existe nas duas categorias
awk -F'\t' '($3=="mobject/table" || $3=="mobject/matrix") && ($1=="class"||$1=="function")' \
  api/manim-ce-index.tsv | cut -f1,2,5

# a assinatura de uma classe
awk -F'\t' '$1=="class" && $2=="Table" {print $4}' api/manim-ce-index.tsv

# métodos PRÓPRIOS (coluna 5 = inherited)
awk -F'\t' '$1=="Table" && $5=="0" {print $2"\t"$6}' api/manim-ce-methods.tsv
awk -F'\t' '$1=="Matrix" && $5=="0" {print $2"\t"$6}' api/manim-ce-methods.tsv

bin/mx show Table --own-only
bin/mx find highlighted
```

Um homônimo para não cair: **`Cell` não é célula de tabela.** O índice tem
`class Cell (c: Point2DLike, h: float, polygon: Polygon)` em `utils/other`, do
módulo `manim.utils.polylabel` — é a célula de um algoritmo de rótulo de
polígono, sem nenhuma relação com `Table.get_cell`
**[FONTE, `api/manim-ce-index.tsv`]**. A metodologia completa de descoberta (e o
catálogo de homônimos) é de **`manim-api-discovery`**.

---

## 15. Armadilhas, em uma tela

| Sintoma | Causa | Correção |
|---|---|---|
| `TypeError: sequence item 0: expected str instance, int found` | `Table` usa `Paragraph`, que só junta strings | `IntegerTable`/`DecimalTable`/`MathTable`, ou strings (§4.1) |
| `ValueError: Not all rows in table have the same length.` | linhas de comprimentos diferentes | preencha com `""` (§3.1) |
| destaque na célula errada, uma posição adiantada | `get_entries` conta **com** rótulos | `get_entries_without_labels` (§5.4) |
| `get_entries((1,1))` devolveu a célula do canto oposto | índice −1 no canto vazio, normalizado por `__getitem__` | não peça `(1,1)` numa tabela com os dois rótulos e sem `top_left_entry` (§5.3) |
| `TypeError: ... got multiple values for keyword argument 'buff'` | `buff`/`rows`/`cols` repetidos no `arrange_in_grid_config` | tire-os do dicionário (§6.3) |
| tabela embaralhada | `flow_order` mexido no `arrange_in_grid_config` | não mexa (§6.3) |
| `ValueError: col_alignments has a mismatching size.` | esqueceu a coluna de rótulos na contagem | conte com os rótulos (§6.3) |
| entradas da matriz coladas ou sobrepostas | `h_buff`/`v_buff` na `Matrix` são **passo**, não folga | aumente `h_buff`, ou encolha as entradas (§7.1) |
| colchete fino/grosso, deformado | `stretch_brackets=True` estica com `stretch_to_fit_height` | `stretch_brackets=False` (§7.3) |
| `MobjectMatrix` falhou pedindo LaTeX | os colchetes são `MathTex`, sempre | instale/ative o LaTeX, ou use `MobjectTable` (§7.3) |
| a mesma figura aparece uma vez só na `MobjectTable` | a identidade **move**, não copia | `.copy()` em cada célula (§4.6) |
| tabela invisível no fundo branco | `Text` e `Line` nascem brancos | `element_to_mobject_config` + `line_config` (§12) |
| blocos pretos atrás das células | `entries_background_color=BLACK` por default | passe a cor do canvas (§12) |
| `Table(dados, color=X)` não pintou nada | a família está vazia no `super().__init__` | §3.1, §12 |
| o realce ficou preto depois de eu "só copiar o estilo" | `BackgroundRectangle.set_style` força `BLACK` | `set_color`, ou use `get_cell` + `Polygon` (§9.2, §9.3) |
| `set_style() missing 1 required positional argument: 'fill_opacity'` | a subclasse mudou a assinatura | §9.2 |
| `set_row_colors` pintou o cabeçalho | `get_rows()` inclui a linha de rótulos | §9.5 |
| encolhi a tabela num grupo e o realce saiu grande demais | `Mobject.scale` do pai não passa por `Table.scale` | escale a tabela pelo próprio objeto (§10.1) |
| `2.5` virou `2` | `"{:,.0f}"` arredonda meio-para-par | `DecimalTable`, ou string formatada (§4.5) |
| `1234.5` saiu `1,234.50` | separador americano, sem locale | `group_with_commas=False` (§4.4) |
| `create()` levou 3 s | `lag_ratio=1` é sequencial | `lag_ratio` menor + `run_time` no `play` (§11.1) |
| `FadeOut(tabela)` não removeu nada | `create()` pôs embrulhos na cena, não a tabela | `self.add(tabela)` depois do play (§11.1) |
| movi uma linha e a grade ficou para trás | embrulho descartável move as células, não a tabela | mova a tabela (§8) |
| o `det` não acompanhou a matriz | `get_det_text` devolve um `VGroup` solto | embrulhe os dois (§7.4) |

---

## 16. O que ficou NÃO VERIFICADO

Nada foi renderizado nesta sessão — proibição de CPU/GPU. Tudo acima saiu de
leitura de `.venv/lib/python3.12/site-packages/manim/mobject/table.py` (1.210
linhas), `matrix.py` (645), `numbers.py`, `shape_matchers.py`, `mobject.py`,
`composition.py`, `scene.py` e do índice estático de `api/`. Em aberto:

- **Nenhum exemplo de código deste arquivo foi executado.** As assinaturas e os
  defaults estão conferidos um a um contra `api/manim-ce-index.tsv` e o fonte;
  a composição das chamadas não passou por interpretador.
- **§5.3** (o `get_entries((1,1))` errado) foi provado pela **aritmética** do
  fonte reproduzida em Python puro, não construindo a tabela. A conclusão
  depende de `Mobject.__getitem__` normalizar índice negativo — eu li o código
  (`mobject.py:2515`), mas não executei.
- **§7.1** (entradas de `Matrix` se sobrepõem acima de `h_buff`) é dedução
  geométrica direta de `matrix.py:220-229`. Não medi um caso real; o limiar
  exato depende da largura renderizada da entrada.
- **§10.1** (escala por grupo-pai não atualiza `h_buff`) segue de
  `Mobject.scale` usar `apply_points_function_about_point` e não recursão por
  `.scale()`. Não comparei dois PNGs.
- **§11.1(c)** (o `create()` deixa embrulhos na cena) segue de
  `AnimationGroup._setup_scene` delegar aos filhos e de
  `Scene.restructure_mobjects`. A limpeza pelo `self.add(tabela)` é leitura de
  `scene.py:755-769`, não observação.
- **§13** — não medi tempo de render de tabela nenhuma. Contagem de compilações
  é raciocínio sobre o código; o custo real é de `manim-performance-cache`.
- **§1.2** — o experimento de Garner & Alley é **[DECK]**: repassado do
  `CLAUDE.md` do consumidor, não lido no original.
- **`Vector2DLike` como entrada de `Matrix`** — a anotação aceita
  `Iterable[Iterable[Any] | Vector2DLike]`, mas `_matrix_to_mob_matrix` itera as
  linhas; não testei que forma exata de vetor-coluna funciona.
- **O renderer OpenGL.** `Table` usa `get_vectorized_mobject_class()` para criar
  o placeholder, o que sugere que o caminho OpenGL foi pensado, mas nada aqui
  foi conferido fora do cairo.

---

## 17. Onde esta skill para

| Assunto | Skill dona |
|---|---|
| `BarChart`, `Axes`, `NumberPlane`, curva de função, área, Riemann | `manim-graphs-plots` |
| `Graph`, `DiGraph`, layouts, `from_networkx`, rede | `manim-grafos-redes` |
| `VGroup` × `Group`, submobjects, `arrange_in_grid` genérico, `z_index` | `manim-mobjects` |
| caber na tela, margem, `to_edge`, medir, enquadrar | `manim-layout-posicionamento` |
| `Text` × `MathTex` × `Paragraph`, `t2c`, LaTeX que não compila, **nitidez de glifo** | `manim-text-latex` |
| paleta, contraste WCAG, fundo da cena, "sumiu no branco" como decisão | `manim-color-theming` |
| `tema.py` como contrato, dado externo em JSON, classe-base de cena | `manim-tema-projeto` |
| escolher a classe de animação, `Transform` × `ReplacementTransform` | `manim-animations` |
| `rate_func`, `lag_ratio`, `run_time`, orçamento de tempo, `path_func` | `manim-composicao-ritmo` |
| `ValueTracker`, `always_redraw`, `DecimalNumber` vivo, updaters | `manim-updaters-valuetracker` |
| cortar a cena em partes para o slide, a emenda, `next_section` | `manim-presentation-parts` |
| `Scene`, ciclo de vida, `add`/`remove`/`bring_to_front`, seções | `manim-cenas-secoes` |
| cache de LaTeX, custo de rasterizar, `--no-cache` | `manim-performance-cache` |
| olhar o PNG, conferir sem render, pôster vazio | `manim-verificacao-visual` |
| imagem, SVG, fonte instalada | `manim-svg-imagens` |
| qualidade, formato, caminho da saída | `manim-render-api` |
| codec, NVENC, peso do arquivo | `manim-gpu-encoding` |
| achar nome, assinatura, kwarg, homônimo | `manim-api-discovery` |
| traceback, bissecção, ambiente quebrado | `manim-troubleshooting` |

**Sem skill dona hoje — declare o buraco, não improvise:**

- **Ênfase e anotação**: `Brace`, `BraceLabel`, `BraceText`, `BraceBetweenPoints`,
  `ArcBrace`, `Indicate`, `Circumscribe`, `Flash`, `FocusOn`, `Wiggle`,
  `Underline`, `Cross`. Esta skill usa `SurroundingRectangle` (§9.4) porque não
  há alternativa, mas quem manda em "apontar para a coisa" não existe. O mais
  próximo é `manim-mobjects`.
- **Álgebra linear de cena**: `LinearTransformationScene`, `VectorScene`,
  `ApplyMatrix`, `ApplyComplexFunction`. `ApplyMatrix(matrix, mobject,
  about_point=ORIGIN)` é uma animação de `animation/transform` e **não** tem
  nada a ver com o mobject `Matrix` desta skill — a confusão de nome é a
  armadilha, e o catálogo de animações é de `manim-animations`.
- **`Code`, `Typst`, `Variable`, `BulletedList`, `Title`** — código e texto
  estruturado na tela.

---

## 18. Correções que esta skill traz ao que circulava antes

Duas afirmações que estavam em `manim-graphs-plots` e vieram para cá corrigidas:

1. **"`Table` recebe strings, não números. `Table([[1,2]])` falha."** — a
   conclusão está certa, a explicação não. A assinatura declara
   `Iterable[Iterable[float | str | VMobject]]`; quem recusa o número é o
   `element_to_mobject` **padrão** (`Paragraph`), e o erro é um `TypeError` de
   `str.join`, não do Manim (§4.1). Trocar a classe resolve; trocar o
   `element_to_mobject` também.
2. **`Table`/`Matrix` dentro de uma skill de gráficos.** Eram ~26 linhas para 9
   classes com 27 métodos próprios. A fronteira agora é: **eixo é
   `manim-graphs-plots`, grade desenhada é aqui**. `BarChart` fica lá porque
   herda de `Axes`.
