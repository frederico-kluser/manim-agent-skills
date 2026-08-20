---
name: manim-text-latex
description: >-
  Texto e matemática na tela do Manim — as nove classes de texto (Text,
  MarkupText, Paragraph, Tex, MathTex, SingleStringMathTex, Title,
  BulletedList, Code), qual usar, como colorir e animar PARTES de uma palavra
  ou de uma fórmula, e a TIPOGRAFIA DE PRECISÃO (o cairo arredonda a posição X
  de cada glifo, e a correção que leva o erro de 5,53% para 0,13%). Use ao
  escrever qualquer texto ou equação numa cena; quando pedirem "põe esse texto
  na tela", "escreve a fórmula", "destaca só o termo x", "pinta o denominador",
  "transforma essa equação na outra", "anima a equação se reorganizando",
  "troca a fonte", "as letras estão soltas / o texto saiu tremido / o
  espaçamento entre letras está errado", "o texto quebrou linha sozinho", "o
  acento sumiu", "mostra esse trecho de código na tela", "escreve o texto letra
  por letra", "o LaTeX não compila", "dvisvgm not found", "instala esse pacote
  do LaTeX", "que fontes tem nesta máquina", "o t2c não pegou a letra certa".
  Cobre `t2c`/`t2f`/`t2s`/`t2w`/`t2g`, markup do Pango, `{{ }}` e as regras
  novas de split da 0.21, `substrings_to_isolate`/`tex_to_color_map`,
  `set_color_by_tex` (que agora casa por IGUALDADE EXATA),
  `TransformMatchingTex`, `TexTemplate`/`TexTemplateLibrary`/`TexFontTemplates`,
  `register_font`, `Code` com Pygments, o TinyTeX desta máquina e os dois
  caches de texto. NÃO use para: escolher a cor em si, tema de projeto, "sumiu
  no fundo branco" como assunto de paleta (skill `manim-color-theming`);
  posicionar, agrupar, medir ou alinhar o mobject depois de criado
  (`manim-mobjects`); o catálogo geral de animações e `rate_func`
  (`manim-animations`); rótulo de eixo e de gráfico (`manim-graphs-plots`);
  contador que conta (`manim-updaters-valuetracker`); descobrir se um nome
  existe (`manim-api-discovery`); render que falhou por ambiente ou codec
  (`manim-troubleshooting`, `manim-gpu-encoding`); CARREGAR o arquivo de fonte,
  o SVG ou o PNG do disco — a ordem de busca, o `.ttf` que o projeto embarca e
  o `SVGMobject` são de `manim-svg-imagens` (aqui `register_font` aparece só
  pelo lado tipográfico, depois que o arquivo já foi achado); e a MECÂNICA dos
  caches — chave, invalidação, `--no-cache`, quanto custa — é de
  `manim-performance-cache` (aqui os dois caches de texto entram só pelo que
  eles fazem com a QUEBRA DE LINHA e o glifo).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Texto e matemática na tela

## Como ler este arquivo

ManimCE **0.21.0**, Python 3.12.3, renderer cairo, nesta máquina, 2026-08-19.
Cada afirmação carrega a sua procedência:

| Marca | O que significa |
|---|---|
| **[FONTE]** | li o código de `.venv/lib/python3.12/site-packages/manim/…` — arquivo e linha citados. Afirmação forte |
| **[ÍNDICE]** | conferido em `api/manim-ce-index.tsv` / `api/manim-ce-methods.tsv` (assinatura, categoria, módulo) |
| **[MÁQUINA]** | comando de leitura rodado aqui (`fc-list`, `manimpango.list_fonts()`, `ls ~/.TinyTeX`) |
| **[DECK]** | medido no projeto consumidor `~/Projects/aulas` em 2026-08-19. Testemunho confiável, **não reproduzido aqui** |
| **[DERIVADO]** | aritmética minha sobre constantes lidas no fonte. Não executado |
| **[NÃO VERIFICADO]** | plausível, com mecanismo explicado, mas nenhum render provou |

Esta rodada foi **inteiramente sem render**: nenhum `mx render`, nenhum
`manim`, nenhum `ffmpeg`. Onde faltou execução, está escrito.

## O resumo, para quem tem trinta segundos

1. **Dois motores, não um.** `Text`/`MarkupText`/`Paragraph`/`Code` passam por
   Pango + cairo. `Tex`/`MathTex`/`Title`/`BulletedList` passam por LaTeX +
   dvisvgm. Quase todas as armadilhas deste arquivo pertencem a **um** dos dois
   lados, e trocar de lado é a correção mais barata que existe.
2. **O cairo arredonda a posição X de cada glifo para inteiro** e isso solta as
   letras das palavras — pior quanto menor o texto (§3). A correção é desenhar
   grande e encolher. Só vale para o lado Pango.
3. **`set_color_by_tex` mudou na 0.21: casa por IGUALDADE EXATA**, não mais por
   substring, e falha **em silêncio** quando não casa (§8.4).
4. **A quebra de linha do `Text` vem de `config.pixel_width`** — a resolução do
   render decide onde a frase quebra — e **o hash do cache de SVG não inclui a
   resolução** (§2.7).
5. **Texto sem cor explícita some em fundo claro**, sem erro nenhum. A conta de
   contraste e o tema são de `manim-color-theming`; aqui ficam só as três
   classes que trazem cor embutida e furam o tema (§13).
6. **`Text` custa milissegundos; `MathTex` custa um `latex` + um `dvisvgm`.**
   Se não é matemática, é `Text`.

---

## 1. As nove classes, e a árvore

[ÍNDICE] Categoria `mobject/text`, só `class` e `function`, tudo em
`manim.mobject.text.*`:

```
VMobject
├── Code                      manim.mobject.text.code_mobject
├── MathTexPart               manim.mobject.text.tex_mobject   (NÃO está no star import)
└── SVGMobject
    ├── MarkupText            manim.mobject.text.text_mobject
    ├── Text                  manim.mobject.text.text_mobject
    ├── Typst                 manim.mobject.text.typst_mobject
    │   └── MathTypst
    └── SingleStringMathTex   manim.mobject.text.tex_mobject
        └── MathTex
            └── Tex
                ├── BulletedList
                └── Title
VGroup
└── Paragraph                 manim.mobject.text.text_mobject
```

Duas coisas que essa árvore já entrega, e que quase todo tutorial erra:

- **`Tex` herda de `MathTex`**, não o contrário. Logo `Tex` tem
  `set_color_by_tex`, `get_part_by_tex`, `substrings_to_isolate`,
  `tex_to_color_map` e o split por `{{ }}` — tudo. A única diferença de fábrica
  é `arg_separator=""` (contra `" "`) e `tex_environment="center"` (contra
  `"align*"`). [ÍNDICE]
- **`Paragraph` é um `VGroup`, não um `SVGMobject`.** Ele monta **um** `Text`
  com `\n` e depois reorganiza os glifos em linhas
  (`text_mobject.py:152-217`). [FONTE] Portanto herda todo o comportamento de
  `Text`, inclusive a quebra de linha por `config.pixel_width`.

Também moram em `mobject/text`, mas **não são desta skill**: `DecimalNumber`,
`Integer`, `Variable` — número que muda na tela é
**`manim-updaters-valuetracker`**. Aparecem na §9.4 **desta** skill só pelo lado
tipográfico.

### 1.1 Qual classe usar

| Quero | Classe | Por quê |
|---|---|---|
| rótulo, título, frase de apoio, legenda | **`Text`** | Pango, milissegundos, sem LaTeX, `t2c` por conteúdo |
| a mesma frase com dois pedaços em estilos diferentes | **`MarkupText`** | marca por conteúdo com tags, sem contar índice |
| bloco de várias linhas com alinhamento por linha | **`Paragraph`** | `alignment="left"/"center"/"right"`, e `par.chars[linha][coluna]` |
| fórmula | **`MathTex`** | modo matemático (`align*`) |
| prosa **com** matemática no meio | **`Tex`** | modo texto; a matemática entra entre `$…$` |
| trecho de código-fonte colorido | **`Code`** | Pygments + `Paragraph`, com número de linha e moldura |
| título sublinhado no topo | `Title` | conveniência; mas leia §9.2 antes |
| lista com marcadores | `BulletedList` | existe; e §9.3 explica por que o deck a proíbe |
| tipografia Typst | `Typst` / `MathTypst` | **indisponível nesta máquina** (§10) |

**A regra que economiza mais tempo:** só use LaTeX quando a saída for
matemática de verdade. `MathTex(r"\text{Custo mensal}")` é um `latex` inteiro
para produzir o que `Text("Custo mensal")` produz em milissegundos, com fonte
pior (Computer Modern) e sem `t2c`.

---

## 2. `Text` — o caminho Pango

[ÍNDICE] Assinatura completa:

```python
Text(text: str,
     fill_opacity: float = 1.0, stroke_width: float = 0,
     color: ParsableManimColor | None = None,
     font_size: float = 48,            # DEFAULT_FONT_SIZE
     line_spacing: float = -1,         # -1 = automático
     font: str = "", slant: str = "NORMAL", weight: str = "NORMAL",
     t2c: dict[str, str] | None = None,        # cor por trecho
     t2f: dict[str, str] | None = None,        # fonte por trecho
     t2g: dict[str, Iterable[ParsableManimColor]] | None = None,   # gradiente
     t2s: dict[str, str] | None = None,        # slant por trecho
     t2w: dict[str, str] | None = None,        # peso por trecho
     gradient: Iterable[ParsableManimColor] | None = None,
     tab_width: int = 4, warn_missing_font: bool = True,
     height: float | None = None, width: float | None = None,
     should_center: bool = True,
     disable_ligatures: bool = False,
     use_svg_cache: bool = False,
     **kwargs)
```

Métodos próprios [ÍNDICE]: `Text.font_list()` (estático) e `init_colors()`. Todo
o resto é herdado de `SVGMobject`/`VMobject`/`Mobject` — posicionar, medir,
agrupar é **`manim-mobjects`** e **`manim-layout-posicionamento`**.

### 2.1 Os pesos e as inclinações são STRINGS constantes

[ÍNDICE] `slant`: `NORMAL` `ITALIC` `OBLIQUE`. `weight`: `THIN` `ULTRALIGHT`
`LIGHT` `SEMILIGHT` `BOOK` `NORMAL` `MEDIUM` `SEMIBOLD` `BOLD` `ULTRABOLD`
`HEAVY` `ULTRAHEAVY`. Todas são constantes cujo valor é a própria string
(`BOLD == "BOLD"`), então `weight="BOLD"` e `weight=BOLD` são a mesma coisa.

**Armadilha:** pedir um peso que a fonte não tem não dá erro. O Pango
sintetiza (embolden) ou cai no peso mais próximo. Confira com
`fc-list "Fira Sans" family style` quais faces REAIS existem —
[MÁQUINA] Fira Sans tem 15 faces aqui, Ubuntu tem 1, Noto Sans tem 1.
[DECK] uma pilha de fontes que põe `"Inter"` (só-Regular) antes de
`"Inter Variable"` faz o Pango resolver `SEMIBOLD` e `BOLD` para a Regular —
**instalar a fonte "certa" pode piorar**, se ela vier com uma face só.

### 2.2 `font_size` não é um atributo, é uma escala disfarçada

[FONTE] `text_mobject.py:622-639`. O getter devolve
`height/initial_height / TEXT_MOB_SCALE_FACTOR * 2.4 * _font_size / DEFAULT_FONT_SIZE`.
Com `TEXT_MOB_SCALE_FACTOR = 0.05` e `DEFAULT_FONT_SIZE = 48` [ÍNDICE], isso
simplifica para **`font_size == (altura atual / altura inicial) × font_size pedido`**
[DERIVADO]. O setter faz `self.scale(font_val / self.font_size)`.

Consequências práticas:

- `t.font_size = 30` **escala o mobject**; não re-rasteriza nada. A grade de
  glifos continua a do tamanho original — é exatamente isso que a §3 explora.
- `t.scale(0.5)` faz `t.font_size` passar a relatar metade. Os dois caminhos são
  o mesmo caminho.
- `font_size <= 0` levanta `ValueError`. [FONTE]

### 2.3 A fonte: como o nome é resolvido, e o que mente

[FONTE] `text_mobject.py:476-491` (idêntico em `MarkupText`, `:1203-1218`):

```python
if font and warn_missing_font:            # ← só entra aqui se o aviso estiver LIGADO
    fonts_list = Text.font_list()         # manimpango.list_fonts(), com @functools.cache
    if font.lower() == "sans-serif": font = "sans"
    if font not in fonts_list:
        if   font.capitalize() in fonts_list: font = font.capitalize()
        elif font.lower()      in fonts_list: font = font.lower()
        elif font.title()      in fonts_list: font = font.title()
        else: logger.warning(f"Font {font} not in {fonts_list}.")
self.font = font
```

Três coisas aqui que ninguém espera:

1. **A recuperação de caixa mora DENTRO do `if warn_missing_font`.** Passar
   `warn_missing_font=False` não silencia só o aviso: **desliga também a
   correção de maiúsculas/minúsculas**. `Text("x", font="fira sans")` funciona
   (vira `"Fira Sans"` por `.title()`); `Text("x", font="fira sans", warn_missing_font=False)`
   entrega `"fira sans"` cru ao Pango. [FONTE]
2. **O objeto mente.** `self.font = font` guarda o que você pediu. Se a família
   não existe, o Pango substitui **sem avisar o objeto** e `t.font` continua
   devolvendo o nome errado. Isto é `manim-project` §10.4 — não reescrevo a
   medição dele, só a repito na forma acionável: *a única prova de que a fonte
   é a que você quer é o nome estar em `manimpango.list_fonts()`.*
3. O aviso despeja **a lista inteira de famílias no log** — 411 nomes
   [MÁQUINA]. É por isso que um WARNING de fonte parece um travamento.

**Nesta máquina** [MÁQUINA], `manimpango.list_fonts()` devolve **411 famílias**:

| Nome | Existe? |
|---|---|
| `Inter`, `Source Code Pro` | **não** |
| `Fira Sans`, `Fira Code`, `Fira Mono`, `DejaVu Sans`, `DejaVu Sans Mono`, `Cantarell`, `Ubuntu`, `Noto Sans`, `JetBrains Mono`, `Hack`, `Liberation Sans`, `Monospace`, `Sans` | sim |
| `sans` (minúsculo), `monospace` (minúsculo) | **não** — mas a recuperação de caixa os salva |

`fc-list : family | sort -u | wc -l` devolve **612** [MÁQUINA] — número maior e
**errado para este fim**, porque conta aliases e nomes localizados que o
manimpango não expõe. A lista que vale é a do `manimpango`:

```bash
.venv/bin/python -c "import manimpango; print(len(manimpango.list_fonts()))"
.venv/bin/python -c "import manimpango; print([f for f in manimpango.list_fonts() if 'Fira' in f])"
```

Custa uma fração do que custa importar o `manim` inteiro, porque o
`manimpango` é um módulo compilado sozinho.

### 2.4 `register_font` — usar um `.ttf` que não está instalado

[ÍNDICE] `register_font(font_file: str | Path) -> Iterator[None]`, decorado com
`@contextmanager` [FONTE] `text_mobject.py:1522`.

```python
from manim import register_font, Text

with register_font("assets/MinhaFonte.ttf"):
    titulo = Text("olá", font="Minha Fonte")   # o nome é o da FAMÍLIA, não o do arquivo
```

Duas armadilhas: o registro vale **só dentro do `with`** (fora dele o Manim
volta a não conhecer a família), e o `font=` continua sendo o **nome da
família** declarado dentro do arquivo, que raramente é o nome do arquivo.
Descubra com `fc-query -f '%{family}\n' assets/MinhaFonte.ttf`.

### 2.5 Fatiar um `Text`: as duas convenções que discordam

[FONTE] `text_mobject.py:308-329` — o próprio Manim documenta isto num
`.. warning::`, e é a armadilha nº 1 do `t2c`:

- **`meu_texto[3:7]`** indexa os **glifos renderizados**, isto é, o texto **sem
  espaço nem quebra de linha** (eles não viram submobject porque não há o que
  desenhar).
- **`t2c={"[3:7]": RED}`** indexa o **argumento `text` original**, com espaços.

Para `Text("Hello World")`: `t2c={"[3:7]": RED}` pinta `l`, `o`, `W` (o espaço
no índice 5 cai na faixa e não tem o que colorir), enquanto `meu_texto[3:7]`
seleciona **quatro** glifos, `l o W o`.

**A saída é não usar índice.** Quando você já sabe qual é a substring, use a
substring como chave — `t2c={"World": RED}` — que casa por busca de texto e é
imune a isso. [FONTE] `_find_indexes` (`:671-687`) só interpreta a chave como
fatia quando ela casa o regex `\[([0-9\-]{0,}):([0-9\-]{0,})\]`; qualquer outra
coisa é `str.find` em laço, e **todas** as ocorrências são pintadas. Índices
negativos e extremos vazios funcionam: `"[:3]"`, `"[-4:]"`.

### 2.6 `disable_ligatures` muda o significado de `texto[i]`

[FONTE] `text_mobject.py:553-555`:

```python
if self.disable_ligatures:
    self.submobjects = [*self._gen_chars()]
self.chars = self.get_group_class()(*self.submobjects)
```

`_gen_chars()` (`:641-668`) percorre a string e, **para cada caractere de
espaço**, insere um `Dot(radius=0, fill_opacity=0, stroke_opacity=0)` no lugar.
Isto é: com `disable_ligatures=True`, os espaços **passam a ser submobjects
invisíveis** e `texto[i]` passa a indexar caracteres, não glifos. Com o padrão
`False`, não passam.

Ou seja, `disable_ligatures` faz **três** coisas, e todo mundo só conhece a
primeira:

1. impede que `fi`/`fl`/`ff` virem um glifo só;
2. **realinha a indexação** com a string original (espaços contam);
3. muda o espaçamento visual — reposicione o que estava alinhado.

Para desfazer (2) quando ele atrapalha, existe
`remove_invisible_chars(mobject: VMobject) -> VMobject` [ÍNDICE], que devolve um
**`VGroup` novo** sem os `Dot`s — não mexe no original. **Ela não está no
`from manim import *`** [ÍNDICE]:

```python
from manim.mobject.text.text_mobject import remove_invisible_chars
```

Ainda em `_gen_chars`, um erro que vale conhecer pelo texto [FONTE] `:655-666`:
se a fonte renderizar **menos** glifos que os caracteres não-espaço mesmo com
`disable_ligatures=True`, o Manim levanta `ValueError` explicando que a fonte
implementa ligaduras por *feature* OpenType (`calt`, o caso das ligaduras de
programação da Fira Code) que a flag não desliga. **Tradução operacional: não
use Fira Code em `Text` se for fatiar por índice.**

### 2.7 A quebra de linha vem da RESOLUÇÃO — e o cache não sabe disso

[FONTE] `text_mobject.py:834-865`. `Text._text2svg` faz:

```python
size /= TEXT2SVG_ADJUSTMENT_FACTOR          # 4.8   [ÍNDICE]
...
if file_name.exists():                      # ← devolve o cache ANTES de olhar a resolução
    svg_file = str(file_name.resolve())
else:
    width  = config["pixel_width"]
    height = config["pixel_height"]
    svg_file = manimpango.text2svg(settings, size, line_spacing,
                                   self.disable_ligatures, file_name,
                                   START_X, START_Y, width, height, self.text)
```

[FONTE] `manimpango/cmanimpango.pyx:56,89-92`: `width`/`height` viram
`cairo_svg_surface_create(...)` **e**, como o `pango_width` fica `None`,
`pango_layout_set_width(layout, pango_units_from_double(width))`. Isto é:
**`config.pixel_width` é a largura de quebra de linha do Pango.**

E o hash que nomeia o arquivo [FONTE] `text_mobject.py:689-701` é:

```
"PANGO" + font + slant + weight + str(color)
        + str(t2f) + str(t2s) + str(t2w) + str(t2c)
        + str(line_spacing) + str(_font_size)
        + str(disable_ligatures) + str(gradient)
        + text                                       → sha256[:16]
```

**Duas ausências, as duas com consequência real:**

| Falta no hash | O que acontece |
|---|---|
| `pixel_width` / `pixel_height` | um render `-ql` (854 px) e um `-qh` (1920 px) podem quebrar a mesma frase em lugares diferentes, e o segundo **reaproveita o SVG do primeiro**. É `manim-project` §10.6 ("brinde"), agora com a linha exata |
| **`t2g`** | `t2g` **afeta** o SVG (vira `TextSetting` por caractere, `:748-765`) mas **não entra no hash**. Dois `Text` iguais em tudo menos no `t2g` colidem: o segundo herda o gradiente do primeiro. `gradient` (global) está no hash; `t2g` (por trecho) não |

O `t2g` é [FONTE] pelas duas metades (afeta o SVG; ausente do hash) e
**[NÃO VERIFICADO]** como sintoma — nenhum render foi feito para vê-lo. Se um
gradiente por trecho sair "errado e teimoso", apague `media/texts/` antes de
procurar em qualquer outro lugar.

`use_svg_cache` é **outra** coisa: é o cache **em memória** do `SVGMobject`
(`SVG_HASH_TO_MOB_MAP`), e o `Text` da 0.21 nasce com ele **desligado**
(`use_svg_cache: bool = False` [ÍNDICE], contra `True` no `SVGMobject`).
`MarkupText`, `Tex` e `MathTex` não expõem o parâmetro e portanto ficam com o
padrão `True` [FONTE] `svg_mobject.py:112,161-180`. Desligar o cache em memória
**não** desliga o cache em disco — o `if file_name.exists()` acima é
incondicional.

### 2.8 Outros detalhes de `Text` que já custaram tempo

- **`t.text` não é o que você passou.** [FONTE] `:556` — depois do `__init__`,
  `self.text` é o texto **sem espaços e sem `\n`**. O original está em
  `t.original_text`, que é o que o `__repr__` mostra.
- **Tabulação vira espaço** antes de qualquer coisa: `tab_width=4` por padrão,
  e `\t` é substituído por 4 espaços [FONTE] `:528-531`.
- **`line_spacing=-1` significa automático**, e o valor efetivo é
  `font_size * 1.3` (`DEFAULT_LINE_SPACING_SCALE = 0.3` [ÍNDICE]). Um número
  positivo é **multiplicador adicional**, não o espaçamento absoluto:
  `line_spacing=0.5` vira `font_size * 1.5` [FONTE] `:532-537`.
- **Os aliases longos existem**: `text2color`, `text2font`, `text2gradient`,
  `text2slant`, `text2weight` são aceitos por `**kwargs` e **têm precedência**
  sobre `t2c`/`t2f`/`t2g`/`t2s`/`t2w` [FONTE] `:512-518`. Se `t2c` "não pegou",
  cheque se alguém passou `text2color` no mesmo lugar.
- **`t2c` é normalizado para hex na hora**: `{k: ManimColor(v).to_hex()}`
  [FONTE] `:520`. Aceita tudo que `ManimColor` aceita (ver
  `manim-color-theming` §2).
- **Ordem de precedência dos `t2*`**, quando as faixas se sobrepõem: quem
  resolve é `_merge_settings` (`:703-728`), com a faixa mais interna vencendo.
  Faixas parcialmente sobrepostas produzem um terceiro trecho — não presuma
  "o último ganha".

---

## 3. Tipografia de precisão: o cairo arredonda a posição X de cada glifo

Esta seção é o motivo de esta skill existir na forma atual. `manim-project`
§10.5 registra o fenômeno e **aponta para cá** para a receita.

### 3.1 O sintoma

Nos vídeos, as letras se soltam das palavras — "o a r q u i v o q u e" — e
**quanto menor o texto, pior**. Não há erro, não há aviso, o exit code é 0.

### 3.2 A causa, com a aritmética

[FONTE] `text_mobject.py:838`: o ManimCE entrega a string ao Pango em
`font_size / TEXT2SVG_ADJUSTMENT_FACTOR` pontos, e
`TEXT2SVG_ADJUSTMENT_FACTOR = 4.8` [ÍNDICE]. O cairo grava o SVG com a posição
X de **cada glifo arredondada para inteiro**. Dá para ver cru no cache, em
`media/texts/*.svg`:

```
font_size=22    <use x="30"/> <use x="34"/> <use x="36"/> <use x="39"/>   y="26.532227"
font_size=720   <use x="30"/> <use x="145"/> <use x="197"/> <use x="310"/> y="233.799805"
```

**X inteiro, Y fracionário.** [DECK, e reproduzido em `manim-project` §10.5]

Medindo esses avanços contra a largura conhecida das letras, o em vale
**`font_size / 3,6`** unidades do SVG [DECK]. (A razão entre 3,6 e o 4,8 do
código é o fator 4/3 de ponto para pixel a 96 dpi, que o cairo aplica no meio
do caminho.) Então:

| `font_size` | em, em unidades do SVG | meia unidade de arredondamento vale |
|---:|---:|---:|
| 18 | 5,0 | **10,0% do em** |
| 22 | 6,1 | **8,2% do em** |
| 44 | 12,2 | 4,1% |
| 96 | 26,7 | 1,9% |
| **720** | **200,0** | **0,25%** |

O erro é **proporcional a 1/tamanho**, e é por letra. Numa frase de 47 glifos
ele acumula deriva de mais de um em [DECK].

### 3.3 Três hipóteses DERRUBADAS com medição

Registre-as: são exatamente as que dá vontade de tentar de novo. [DECK]

| Hipótese | O que a medição disse |
|---|---|
| "é a fonte" | seis fontes, todas ~8% de erro rms: Fira Sans 8,02 · Cantarell 8,10 · DejaVu Sans 8,02 · Liberation 6,55 · Ubuntu 8,02 · Inter 7,36. Trocar de fonte não conserta nada |
| "é peso sintético" | o mesmo erro em `NORMAL`, `SEMIBOLD` e `BOLD`; e `fc-match "Fira Sans:weight=180"` devolve uma face **real** |
| "é hinting do fontconfig" | um `FONTCONFIG_FILE` com `hinting=false` produz SVG **idêntico byte a byte**. Quem arredonda é o `hint_metrics` do cairo, que o `manimpango` nunca configura — **não dá para desligar de fora** |

### 3.4 A correção: mexer na GRADE

Desenhe todo texto num tamanho único e grande e **encolha o mobject depois**. O
arredondamento continua sendo de 1 unidade, mas passa a valer 1/200 do em em
vez de 1/6.

```python
_TAMANHO_RENDER = 720.0            # 720 / 3,6 = 200 unidades por em
_PALCO_TEXTO = (65536, 36864)      # ver por que, abaixo

def texto_nitido(conteudo: str, tamanho: float, **kw) -> Text:
    largura, altura = config.pixel_width, config.pixel_height
    try:
        config.pixel_width, config.pixel_height = _PALCO_TEXTO
        mob = Text(conteudo, font_size=_TAMANHO_RENDER, **kw)
    finally:
        config.pixel_width, config.pixel_height = largura, altura
    return mob.scale(tamanho / _TAMANHO_RENDER)
```

Implementação de referência **real**, em produção:
`~/Projects/aulas/aulas/002-deepseek-harness/manim/tema.py` (constantes em
`:232` e `:240`, função em `:266-287`; bloco explicativo em `:182-240`). Um
gêmeo idêntico existe em `aulas/001-multi-work/manim/tema.py`.

**O `try/finally` não é decoração e o palco gigante não é exagero.** [FONTE]
`config.pixel_width` é a largura de quebra do Pango (§2.7); com o texto 30×
maior, uma linha longa quebraria sozinha — e quebraria **diferente** conforme
a qualidade do render. Fixar `(65536, 36864)` dá 65536/200 ≈ **327 em** de
linha antes da quebra, uns 650 caracteres: nenhuma frase de slide chega lá.
Devolver os valores no `finally` é obrigatório porque `config` é global.

**Efeito colateral bom:** como `_font_size` entra no hash do SVG (§2.7) e agora
é sempre 720, a **mesma string em dois tamanhos passa a compartilhar um SVG
só** [DERIVADO, do hash lido].

### 3.5 O ganho medido

[DECK] Erro de avanço entre glifos contra um render de referência 200× maior,
em % do em, frase de 47 glifos, peso NORMAL (`SEMIBOLD` e `BOLD` dão o mesmo
dentro de 0,03 pp):

| tamanho | antes (rms) | depois (rms) | ganho |
|---|---:|---:|---:|
| 18 | 5,46% | 0,13% | 41× |
| 22 | 5,53% | 0,13% | 43× |
| 28 | 4,05% | 0,14% | 29× |
| 34 | 4,16% | 0,13% | 32× |
| 44 | 2,33% | 0,13% | 18× |
| 60 | 1,61% | 0,13% | 12× |
| 96 | 1,26% | 0,13% | 10× |

A coluna "depois" é **constante de propósito**: todo tamanho passa pelo mesmo
render de 720, então todo tamanho ganha a mesma grade.

### 3.6 A métrica que enxerga o defeito — e a que é CEGA

Contraintuitivo, e custa uma tarde descobrir sozinho: **o desvio-padrão do
avanço de um par de letras REPETIDO ("nnnn…") dá 0,0000% e é completamente
cego** a este defeito — letras iguais arredondam iguais. O que a vista percebe
é cada par **diferente** errando para um lado diferente.

A medida que funciona é o **erro de avanço glifo a glifo, numa frase real,
contra um render de referência muito maior**, em % do em. O procedimento
(**lê o SVG que o Manim já deixou no cache; não renderiza vídeo, não usa GPU**):

```python
# .venv/bin/python  — constrói mobjects de Text, custa segundos
import glob, os, re, shutil
import numpy as np
from manim import config
config.media_dir = "/tmp/nitidez/media"
from manim import Text

FRASE = "o arquivo que o plugin escreve fica fora do repositorio"
CACHE = "/tmp/nitidez/media/texts"

def xs(em_unidades):
    svg = max(glob.glob(CACHE + "/*.svg"), key=os.path.getmtime)
    v = re.findall(r'<use [^>]*x="([-0-9.]+)"', open(svg).read())
    return np.array([float(m) for m in v]) / em_unidades

def limpa(): shutil.rmtree(CACHE, ignore_errors=True)

# REFERÊNCIA: font_size 7200 = 2000 unidades por em (grade de 0,05% do em).
limpa()
larg, alt = config.pixel_width, config.pixel_height
config.pixel_width, config.pixel_height = 65536, 36864     # senão o Pango quebra a cada glifo
Text(FRASE, font_size=7200, font="Fira Sans")
ref = xs(2000.0)
config.pixel_width, config.pixel_height = larg, alt

limpa(); Text(FRASE, font_size=22, font="Fira Sans")
erro = np.diff(xs(22 / 3.6)) - np.diff(ref)
print("erro rms: %.2f%% do em" % (np.sqrt((erro**2).mean()) * 100))

limpa(); Text("n" * 20, font_size=22, font="Fira Sans")
print("CEGA: %.4f%%" % (np.diff(xs(22 / 3.6)).std() * 100))   # sai 0.0000%
```

[DECK] Rodado em 2026-08-19 no projeto consumidor, reproduz a tabela da §3.5
dentro de ~0,15 pp e a linha `CEGA` sai `0.0000%`. **Não reexecutado aqui.**

### 3.7 Os quatro limites da correção — leia antes de copiar

1. **Só vale para o lado Pango.** `Tex`/`MathTex` não passam pelo cairo: o
   caminho é `latex` → `.dvi` → `dvisvgm --no-fonts` → SVG de **contornos
   vetoriais**, sem `config.pixel_width` em lugar nenhum [FONTE]
   `utils/tex_file_writing.py` inteiro. Aplicar o truque a `MathTex` não faz
   nada de bom e ainda mexe no `font_size` que a §8 usa. [DERIVADO]
2. **NÃO funciona em `MarkupText`.** [FONTE] `text_mobject.py:1380-1417`: o
   `_text2svg` do `MarkupText` **ignora `config`** e passa constantes
   literais — superfície `600, 400` e `pango_width=500`. Como a quebra é fixa
   em 500 unidades e o em cresce com o `font_size`, o orçamento de linha é
   ≈ `500 / (font_size/3,6)` = **`1800 / font_size` em** [DERIVADO]: ~37 em a
   `font_size=48`, e **~2,5 em a 720** — uma ou duas letras por linha. Se
   precisa de nitidez E de markup, use `Text` com `t2c`/`t2w`/`t2s`, ou aceite
   o `MarkupText` no tamanho final.
3. **Não baixe o 720.** Ele *é* a grade; o erro cresce na proporção inversa.
4. **As larguras de linha mudam.** [DECK] até ±6% em relação ao render antigo
   (amostra de frases: de −6,2% a +4,8%). A direção é a certa — a largura
   antiga é que estava errada, com deriva acumulada. Layout por `next_to` /
   `arrange` / `to_edge` se acomoda sozinho; **posição calculada a partir da
   largura de um texto merece uma conferida no PNG**.

E a regra de disciplina que faz isso valer: **todo texto do projeto passa por
um helper só**. Se uma cena chamar `Text(...)` direto, o defeito volta sem erro
nenhum. O teste é um `grep`:

```bash
grep -rn '\bText(' cenas/*.py        # esperado: nada fora do tema
```

O tema como contrato é **`manim-tema-projeto`**; a paleta é
**`manim-color-theming`**.

---

## 4. `MarkupText` — marcar por conteúdo, sem contar índice

[ÍNDICE] Mesma assinatura de `Text` **menos** `t2c/t2f/t2g/t2s/t2w` e
`use_svg_cache`, **mais** `justify: bool = False`.

```python
MarkupText(f'A constante <span fgcolor="{RED}">desaparece</span> na derivada')
MarkupText('<b>negrito</b>, <i>itálico</i>, <u>sublinhado</u>, <s>riscado</s>')
MarkupText('<tt>monoespaçado</tt> e <big>maior</big> e <small>menor</small>')
MarkupText('x<sup>2</sup> e H<sub>2</sub>O')
MarkupText('<span font_family="Fira Mono" foreground="#0071E3">trecho</span>')
MarkupText('<gradient from="YELLOW" to="RED">degradê</gradient>')
```

[FONTE] `text_mobject.py:925-937` lista as tags suportadas; além das acima,
`<span underline="double|error" underline_color=…>`, `<span overline="single"
overline_color=…>`, `<span strikethrough="true" strikethrough_color=…>`.

### 4.1 O que só o `MarkupText` tem

- **`<gradient from=… to=…>`** é uma tag **do Manim**, não do Pango [FONTE]
  `:1439-1471`. Aceita hex e constantes do Manim (`RED`, `RED_A`). Tem um
  atributo `offset` para compensar ligaduras e sublinhados, que entram como
  *paths* extras no SVG: `offset="1"` começa uma letra antes, `offset=",1"`
  termina uma antes, `offset="2,1"` faz as duas coisas.
- **`justify=True`** — justificação de verdade, que o `Text` não tem.
- **`<color>` está DEPRECIADA** e emite `logger.warning` [FONTE] `:1233-1236`.
  Use `<span foreground="…">`.

### 4.2 Escape: `&` e `<` **quebram** o render

[FONTE] `:1238-1240` — o construtor chama `MarkupUtils.validate(self.text)` e,
se houver erro, **levanta `ValueError`**. Regras [FONTE] `:975-977`:

| Caractere | Regra |
|---|---|
| `&` | **obrigatório** `&amp;` |
| `<` | **obrigatório** `&lt;` |
| `>` | *deveria* ser `&gt;` |

`MarkupText("Fulano & Cia")` é `ValueError`, não um render feio. Se o texto vem
de dado externo, passe por `html.escape` antes — ou use `Text`, que não
interpreta nada.

### 4.3 As duas constantes escondidas

[FONTE] `:1413-1416`, já citado na §3.7: superfície **600×400** e
**`pango_width=500`**, literais, sem passar por `config`. Consequências:

- **imune** ao descasamento de resolução da §2.7 (a quebra não depende do
  `-q`);
- **incompatível** com o truque de nitidez;
- `font_size` alto começa a quebrar linha cedo, e isso parece bug de layout.

O hash do `MarkupText` [FONTE] `:1363-1377` é `"MARKUPPANGO" + font + slant +
weight + cor + line_spacing + _font_size + disable_ligatures + justify + text`
— **não** tem `gradient` nem `t2*` (que não existem aqui), e o markup inteiro
está dentro de `text`, então mudar uma tag muda o hash. Sem o buraco do `t2g`.

### 4.4 Quando NÃO usar

Quando você for **animar partes separadamente**. `MarkupText` produz um
`SVGMobject` plano de glifos; ele não cria grupos por tag. Para "esta palavra
entra depois", monte dois `Text` e um `VGroup` — ou use `t2c` para a cor e
`Indicate`/`Circumscribe` para o destaque (as duas são de `manim-animations`).

---

## 5. `Paragraph` — várias linhas com alinhamento por linha

[ÍNDICE] `Paragraph(*text: str, line_spacing: float = -1, alignment: str | None = None, **kwargs)`

`**kwargs` vai inteiro para o `Text` interno [FONTE] `:165` — então `font`,
`color`, `font_size`, `t2c`, `disable_ligatures` funcionam.

```python
par = Paragraph(
    "primeira linha",
    "segunda linha",
    "terceira",
    alignment="left",          # "left" | "center" | "right" | None
    line_spacing=0.6,
    font="Fira Sans", color=BLACK, font_size=28,
)
par.chars[1][0:6].set_color(BLUE)      # linha 1, primeiros 6 caracteres
```

Estrutura [FONTE] `:166-177`: `par.chars` é um `VGroup` de linhas, cada linha um
`VGroup` de caracteres; `par` **é** esse mesmo conjunto de linhas
(`self.add(*self.lines_chars)`). Também guarda `lines_text` (o `Text` inteiro),
`lines_alignments` e `lines_initial_positions`.

**Armadilhas:**

- `consider_spaces_as_chars` é lido de `kwargs["disable_ligatures"]` [FONTE]
  `:161` — ou seja, **a contagem de caracteres por linha depende do
  `disable_ligatures`**, exatamente como na §2.6. Ligue-o se for fatiar
  `par.chars[i][a:b]` contando espaços.
- Uma string com `\n` dentro **também** quebra em linhas (ele junta tudo com
  `\n` e re-divide) — `Paragraph("a\nb", "c")` tem 3 linhas.
- Herda a quebra automática por `config.pixel_width` do `Text`. Se a linha é
  longa, ela pode quebrar de novo por conta própria, dentro da "linha".

---

## 6. `Code` — código-fonte na tela

[ÍNDICE] **Não aceita `**kwargs`.** A assinatura é fechada:

```python
Code(code_file: StrPath | None = None,
     code_string: str | None = None,
     language: str | None = None,
     formatter_style: str | type[Style] = "vim",
     tab_width: int = 4,
     add_line_numbers: bool = True,
     line_numbers_from: int = 1,
     background: Literal["rectangle", "window"] = "rectangle",
     background_config: dict | None = None,
     paragraph_config: dict | None = None)
```

**`Code(..., font_size=30)` é `TypeError`.** Tamanho, fonte e espaçamento vão em
`paragraph_config`; cor e forma da moldura vão em `background_config`.

Padrões [FONTE] `code_mobject.py:156-169`:

```python
default_paragraph_config  = {"font": "Monospace", "font_size": 24,
                             "line_spacing": 0.5, "disable_ligatures": True}
default_background_config = {"buff": 0.3, "fill_color": None, "stroke_color": WHITE,
                             "corner_radius": 0.2, "stroke_width": 1, "fill_opacity": 1}
```

Uso:

```python
listagem = Code(
    code_string=fonte,
    language="python",
    formatter_style="friendly",                 # ← claro; o padrão "vim" é ESCURO
    background="window",
    add_line_numbers=True, line_numbers_from=12,
    paragraph_config={"font": "Fira Mono", "font_size": 20},
    background_config={"stroke_color": "#D2D2D7", "corner_radius": 0.12},
)
listagem.code_lines[3].set_opacity(0.35)        # apaga a linha 4
```

Atributos públicos [FONTE]: `code_lines` (um `Paragraph`), `line_numbers` (um
`Paragraph`, **só existe se `add_line_numbers=True`**) e `background` (um
`SurroundingRectangle`; em `background="window"` ele carrega também os três
pontinhos de janela).

**Armadilhas, todas [FONTE]:**

1. **O `formatter_style` decide o FUNDO.** `background_config["fill_color"]`
   nasce `None` e é preenchido com `selected_style.background_color`
   (`:321-322`). O padrão `"vim"` é um tema escuro — numa cena de fundo branco,
   `Code(...)` sozinho põe um retângulo preto na tela. [MÁQUINA] São **50**
   estilos aqui (`pygments.styles.get_all_styles()`); classificando cada um
   pela luminância do `background_color`, **30 são claros e 20 são escuros** —
   e `vim`, o padrão, está entre os escuros, junto de `monokai` `dracula`
   `nord` `native` `zenburn` `solarized-dark` `github-dark` `one-dark`.
   Os 30 claros: `friendly` `friendly_grayscale` `bw` `default` `emacs`
   `tango` `trac` `vs` `xcode` `pastie` `perldoc` `colorful` `autumn` `borland`
   `manni` `murphy` `sas` `arduino` `igor` `lovelace` `paraiso-light`
   `solarized-light` `stata-light` `gruvbox-light` `lilypond` `abap` `algol`
   `algol_nu` `rainbow_dash` `staroffice`. Liste no código com
   `Code.get_styles_list()` e resolva uma com `Code.get_pygments_style(nome)`
   (ambos `classmethod` [ÍNDICE]).
2. **A cor de cada token vem do Pygments, não do seu tema.** `:262-278` aplica
   `set_color` glifo a glifo a partir do HTML colorido. `set_default`,
   `apply_theme` e a paleta do projeto **não alcançam** o interior de um `Code`
   — escolha o `formatter_style` que combina com o tema.
3. **Sem `language`, ele adivinha** (`guess_lexer`), e a própria docstring diz
   que a adivinhação é instável. Sempre passe `language=`.
4. **`code_file` ou `code_string`, nunca os dois nem nenhum**: sem um dos dois
   é `ValueError("Either a code file or a code string must be specified.")`.
   Com os dois, o arquivo vence (`:191-200`).
5. **`disable_ligatures=True` é o padrão** do `paragraph_config` — e é
   deliberado, porque é o que mantém caractere e glifo em correspondência 1:1
   para o colorido por token funcionar. Se você sobrescrever
   `paragraph_config` inteiro sem repor a chave, o alinhamento das cores pode
   deslizar. **Atualize o dicionário, não o substitua** — o Manim já faz
   `default.copy(); update(seu)` (`:218-219`), então basta passar as chaves que
   você quer mudar.
6. **Uma fonte com ligaduras de programação (Fira Code) é a pior escolha aqui**
   — é o `ValueError` da §2.6. Fira **Mono** e JetBrains Mono estão instaladas
   [MÁQUINA] e não têm o problema no mesmo grau.

**Quando não usar `Code`:** para 3 ou 4 linhas destacando uma ideia, um `Text`
monoespaçado com `t2c` é mais leve, combina com o tema e não traz moldura
nenhuma. `Code` ganha quando há **muitas** linhas e o realce por token importa.

---

## 7. `Typst` e `MathTypst` — indisponíveis nesta máquina

[MÁQUINA] O pacote `typst` **não está instalado** no `.venv`. [FONTE]
`utils/typst_file_writing.py:71-73` faz o `import typst` **dentro** da função e
levanta `ImportError` com instrução de instalação — por isso `from manim import
*` funciona e o erro só aparece quando você constrói um `Typst`.

Não instale nada por conta própria (é o mesmo princípio de
`manim-project` §13.7 para plugins). Se um dia entrar, o que muda em relação a
`MathTex`, pela docstring [FONTE] `typst_mobject.py:1-120`: a seleção é por
**rótulo** (`text.select("headline")`), o `{{ … }}` só vale em `MathTypst` e
aceita a forma `{{ a^2 + b^2 : lhs }}`, e há `track_baselines=True` com
`get_baseline_frame`. Métodos próprios [ÍNDICE]: `select`,
`get_baseline_frame`, `get_mob_from_shape_element`, `modify_xml_tree`,
`init_colors`, `scale`.

---

## 8. `Tex` e `MathTex` — o caminho LaTeX

### 8.1 O pipeline inteiro, e onde ele guarda coisas

[FONTE] `utils/tex_file_writing.py`:

```
TexTemplate.body                              → documentclass + preâmbulo + \begin{document} …
  ↓ get_texcode_for_expression_in_env(expr, env)
tex_hash(código completo) → media/Tex/<16 hex>.tex     (não reescreve se já existe)
  ↓ compile_tex: latex -interaction=batchmode -halt-on-error -output-format=dvi
media/Tex/<hash>.dvi                                   (não recompila se já existe)
  ↓ convert_to_svg: dvisvgm --page=1 --no-fonts --verbosity=0
media/Tex/<hash>.svg                                   (não reconverte se já existe)
  ↓ delete_nonsvg_files()   ← a menos que config.no_latex_cleanup
SVGMobject(file_name=…)
```

Quatro leituras que valem dinheiro:

- **O hash é do código-fonte LaTeX INTEIRO**, não da expressão. Mudou o
  preâmbulo, mudou o `documentclass`, mudou o `tex_environment` — recompila
  tudo. Duas expressões idênticas com templates diferentes convivem sem
  colidir.
- **`--no-fonts`** é o que faz cada letra virar **contorno vetorial**. É por
  isso que `eq[0][3]` é um glifo fatiável e por isso que não existe o problema
  de arredondamento da §3 aqui: quem posiciona é o dvisvgm, não o cairo.
- **`delete_nonsvg_files()`** apaga **todo** arquivo de `media/Tex` que não seja
  `.svg` ou `.tex` [FONTE] `:279-284`. Não guarde nada seu nessa pasta —
  `manim-batch-pipeline` documenta o mesmo estrago no modo lote.
- **A resolução não aparece em canto nenhum** do caminho. `grep -n "pixel_width"
  utils/tex_file_writing.py` → vazio [MÁQUINA]. LaTeX é imune ao problema da
  §2.7.

### 8.2 `Tex` × `MathTex`, com precisão

[ÍNDICE]

```python
MathTex(*tex_strings, arg_separator=" ",  substrings_to_isolate=None,
        tex_to_color_map=None, tex_environment="align*", **kwargs)
Tex    (*tex_strings, arg_separator="",   tex_environment="center", **kwargs)
```

`Tex` é `MathTex` com dois defaults trocados. **Modo texto**: a matemática
precisa de `$…$`.

```python
MathTex(r"\int_0^1 x^2\,dx = \tfrac13")
Tex(r"Seja $x > 0$ um número real.")
MathTex(r"x &= 1 \\ y &= 2")                       # align* aceita & e \\
MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
MathTex(r"\sum_{k}", tex_environment="gather*")
```

**`Tex(r"x^2")` não produz x².** Em modo texto o `^` é caractere de modo
matemático; o `latex` responde `! Missing $ inserted.` e, com `-halt-on-error`,
isso vira o `ValueError` da §11. [DERIVADO — o mecanismo é a catcode 7 do TeX;
**não executado nesta rodada**.] Escreva `Tex(r"$x^2$")` ou `MathTex(r"x^2")`.

**Raw string sempre.** `MathTex("\int_0^1")` interpreta `\i` como escape do
Python antes de o LaTeX ver qualquer coisa. `r"..."` sem exceção — e note que
isso vale também para `\\` de quebra de linha, que em raw string continua sendo
dois caracteres.

`tex_environment` aceita formas soltas [FONTE] `utils/tex.py:167-201`:
`"align*"`, `"{align*}"`, `r"\begin{align*}"`, e até
`"{tabular}[t]{cccl}"` — o `\end` fecha no primeiro `}`.
`tex_environment=None` significa **sem ambiente**, a expressão entra direta no
documento.

### 8.3 Os consertos SILENCIOSOS que o Manim faz na sua fórmula

[FONTE] `tex_mobject.py:129-204`. Antes de compilar, o Manim **reescreve** a
sua string, e nada disso avisa:

| Situação | O que ele faz |
|---|---|
| chaves desbalanceadas | `_remove_stray_braces` acrescenta `{` no começo ou `}` no fim até equilibrar |
| `\left` e `\right` em número diferente | troca **os dois** por `\big` |
| a string termina em `_`, `^`, `dot`, ou é só `\over`/`\overline`/`\sqrt` | acrescenta `{\quad}` |
| string vazia, ou `\substack` sozinho | vira `\quad` |
| começa com `\\` | vira `\quad\\` |
| tem `\begin{array}` sem `\end{array}` (ou vice-versa) | **vira string vazia** |

O `_remove_stray_braces` existe para o caso legítimo de
`MathTex(r"e^{i", r"\tau} = 1")`, em que a chave abre num argumento e fecha no
outro. O preço é que **um erro de digitação de chave não dá erro: dá uma
fórmula diferente**. Se a fórmula saiu "quase certa" e você não entende por
quê, conte as chaves.

### 8.4 Colorir e endereçar PARTES — o que mudou na 0.21

Este é o ponto onde a documentação de terceiros está mais desatualizada. Na
0.21, `MathTex` **não** renderiza cada pedaço em SVG separado. Ele injeta
marcadores no LaTeX e lê os grupos de volta do SVG [FONTE] `:429-541`:

```python
\special{dvisvgm:raw <g id='unique000'>}  a^2  \special{dvisvgm:raw </g>}
```

e depois monta `self.id_to_vgroup_dict[id] → VGroup`. Daí saem **duas** coisas
diferentes, e confundi-las é a origem de metade dos problemas:

| Mecanismo | O que cria | Onde aparece |
|---|---|---|
| **vários argumentos** ou **`{{ … }}`** | um `MathTexPart` por parte, e **`self.submobjects` é reescrito** com eles [FONTE] `:522-541` | `eq[0]`, `eq[1]`, … e `TransformMatchingTex` |
| **`substrings_to_isolate=` / `tex_to_color_map=`** | só um `<g id>` no SVG, **acessível apenas por `get_part_by_tex`/`set_color_by_tex`** | *não* vira submobject, *não* muda `len(eq)` |

Ou seja: **para colorir, você não precisa mais de `{{ }}`.** Precisa dele para
`TransformMatchingTex` e para endereçar por índice.

#### As regras do `{{ … }}` (novas, e estritas)

[FONTE] `:351-427`, docstring em `:243-256`:

1. `{{` só abre grupo **no início da string ou logo depois de um espaço em
   branco**. Isso é o que impede `\frac{{{n}}}{k}` e `a^{{2}}` de serem
   fatiados por engano.
2. Dentro do grupo, a profundidade de chaves **reais** é contada; `}}` só fecha
   com profundidade zero. `{{ a^{b^{c}} }}` funciona.
3. `\\`, `\{` e `\}` são consumidos como unidades atômicas.
4. Para impedir um split não intencional: escreva `{ { … } }` com espaço.
5. Se a compilação falhar e tiver havido split, o Manim **loga um erro
   explicando isso** antes de relançar (`:352-365`).

Contagem, para calibrar: `MathTex(r"{{a^2}} + {{b^2}} = c^2")` → **4** partes,
`["a^2", " + ", "b^2", " = c^2"]`. `MathTex("{{ a }} + {{ b }} = {{ c }}")` →
**5** (é o exemplo do próprio docstring).

**Repare nos espaços.** As partes **não são strippadas** [FONTE] `:344-349`. Em
`{{a^2}} + {{b^2}}` a parte do meio é `" + "`, com os dois espaços. Isso importa
por causa do item seguinte.

#### `set_color_by_tex` casa por IGUALDADE EXATA e falha em SILÊNCIO

[FONTE] `:549-556`:

```python
def set_color_by_tex(self, tex, color, **kwargs):
    for tex_str, match_id in self.matched_strings_and_ids:
        if tex_str == tex:                     # ← igualdade, não substring
            self.id_to_vgroup_dict[match_id].set_color(color)
    return self
```

Não há `get_parts_by_tex` na 0.21 [ÍNDICE — o nome não existe no índice]. E
`get_part_by_tex` devolve **`None`** quando não casa (`:543-547`), o que vira
`AttributeError: 'NoneType' object has no attribute …` uma linha depois.

| Você escreveu | O que acontece |
|---|---|
| `eq.set_color_by_tex("+", RED)` numa `{{ }}` cuja parte é `" + "` | **nada**, sem erro, sem aviso |
| `eq.get_part_by_tex("a")` sem `"a"` isolado | `None` → `AttributeError` na linha seguinte |

**A saída limpa: passe as partes como argumentos separados**, aí o nome da
parte é exatamente a string que você escreveu:

```python
eq = MathTex("a^2", "+", "b^2", "=", "c^2")     # 5 partes, nomes exatos
eq.set_color_by_tex("a^2", BLUE_D)
eq.set_color_by_tex("+", GREY)                   # agora casa
eq[0].set_opacity(0.4)                           # e o índice também funciona
```

O `arg_separator` (`" "` em `MathTex`, `""` em `Tex`) é inserido **entre** as
partes, dentro do grupo da parte anterior [FONTE] `:459-462` — ele não vira
parte nem entra no nome.

#### Os outros métodos de parte

[ÍNDICE] Todos em `MathTex`, herdados por `Tex`, `Title`, `BulletedList`:

| Método | Assinatura | Nota |
|---|---|---|
| `get_part_by_tex` | `(tex: str, **kwargs) -> VGroup \| None` | igualdade exata; `None` se não achar |
| `set_color_by_tex` | `(tex: str, color, **kwargs) -> Self` | pinta **todas** as partes com aquele nome |
| `set_color_by_tex_to_color_map` | `(texs_to_color_map: dict, **kwargs) -> Self` | é o que o `tex_to_color_map=` chama no fim do `__init__` |
| `set_opacity_by_tex` | `(tex, opacity=0.5, remaining_opacity=None, **kwargs) -> Self` | com `remaining_opacity`, apaga o resto primeiro — é o idioma de "destaca um termo" |
| `index_of_part` | `(part: VMobject) -> int` | levanta `ValueError` se a parte não estiver na fórmula |
| `sort_alphabetically` | `() -> Self` | reordena `submobjects` por `get_tex_string()` |

E `SingleStringMathTex.get_tex_string() -> str` devolve a string da parte;
`MathTexPart.__repr__` mostra `MathTexPart('a^2')`, o que torna
`print(eq.submobjects)` um bom depurador.

#### `tex_to_color_map` casa SUBSTRING crua, e isso pode quebrar o LaTeX

[FONTE] `:346-347` (as chaves entram em `substrings_to_isolate`) e `:465-501`
(o casamento é `re.match(f"(.*?)({re.escape(sub)})(.*)")`, o mais à esquerda,
desempate pelo mais longo). O marcador `\special{…}` é **injetado no meio da
string LaTeX, na posição do casamento**.

Então `tex_to_color_map={"a": RED}` sobre `MathTex(r"\alpha + a")` casa o `a`
de **`\alpha`** primeiro e produz `\` + `\special{…}` + `lpha` — LaTeX
quebrado. O sintoma esperado é um `ValueError` de compilação, não uma cor
errada. [DERIVADO do mecanismo; **não executado**.]

**Regra:** chave de `tex_to_color_map` e de `substrings_to_isolate` nunca deve
ser uma letra solta que apareça dentro de um comando. Prefira `{{ }}`, ou
argumentos separados, ou isole com um trecho maior (`r"a^2"`, não `"a"`).

#### Por índice de glifo, quando não há outro jeito

Descubra os índices **olhando**, nunca por tentativa:

```python
class Depurar(Scene):
    def construct(self):
        eq = MathTex(r"\frac{d}{dx}f(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}",
                     color=BLACK)
        self.add(eq, index_labels(eq[0]))
```

```bash
bin/mx render cena.py Depurar --format png -q l
```

[ÍNDICE] `index_labels(mobject, label_height=0.15, background_stroke_width=5,
background_stroke_color=ManimColor('#000000'), **kwargs) -> VGroup`. Repare no
`eq[0]`: em uma `MathTex` de parte única, `eq` tem **um** submobject (o
`MathTexPart`) e os glifos estão um nível abaixo.

**O caminho do PNG vem em `image_file`, não em `output_file`** — é
`manim-render-api` e `manim-color-theming` §20 que são donos disso; a
verificação visual em geral é **`manim-verificacao-visual`**.

E a armadilha permanente: **índice muda quando a fórmula muda**. Um `eq[0][3:7]`
sobrevive mal a uma edição. Prefira nome.

### 8.5 `\color` do LaTeX sobrevive; o resto não

[FONTE] `tex_mobject.py:213-225`:

```python
def init_colors(self, propagate_colors=True):
    for submobject in self.submobjects:
        if submobject.color != BLACK:      # ← quem já tem cor do LaTeX é poupado
            continue
        submobject.color = self.color
```

Os glifos saem do dvisvgm em preto; `init_colors` os repinta com a cor do
mobject. Um `\textcolor{red}{…}` dentro do LaTeX produz glifos **não-pretos**,
que ficam como estão. É assim que se mistura cor de LaTeX com cor de Manim na
mesma fórmula — e é também por que uma cor de LaTeX que **seja** preta será
sobrescrita.

---

## 9. As três subclasses de conveniência

### 9.1 `SingleStringMathTex`

[ÍNDICE] É o bloco elementar; `MathTex` herda dele. Você raramente o instancia,
mas ele carrega parâmetros que **chegam por `**kwargs` nas outras**:
`tex_template`, `organize_left_to_right`, `stroke_width`, `should_center`,
`height`, `font_size`, `color`. Métodos próprios: `get_tex_string`,
`init_colors`. `organize_left_to_right=True` reordena os submobjects pela
coordenada x [FONTE] `:206-208` — útil quando o LaTeX emite glifos fora de
ordem e uma animação letra a letra sai bagunçada.

### 9.2 `Title`

[ÍNDICE] `Title(*text_parts, include_underline=True,
match_underline_width_to_text=False, underline_buff=0.25, **kwargs)`

[FONTE] `:740-762`. Faz três coisas que surpreendem:

1. **Chama `self.to_edge(UP)` no construtor.** O mobject já nasce posicionado;
   qualquer layout seu precisa vir depois.
2. **O sublinhado é um `Line(LEFT, RIGHT)` sem cor** → nasce **branco**. Em
   fundo claro ele **desaparece sem erro**. Pinte: `titulo.underline.set_color(TINTA)`
   — o objeto fica em `self.underline`.
3. A largura padrão é `config["frame_width"] - 2`, isto é **12,22** no palco
   padrão, não a largura do texto. Para acompanhar o texto:
   `match_underline_width_to_text=True`.

E é um `Tex`: um `latex` inteiro para um título. Num deck com tema próprio,
`Text(...)` + um `Line` seu costuma ser melhor.

### 9.3 `BulletedList`

[ÍNDICE] `BulletedList(*items, buff=0.5, dot_scale_factor=2,
tex_environment=None, dot_buff=0.1, **kwargs)`, com
`fade_all_but(index_or_string: int | str, opacity: float = 0.5) -> Self`.

[FONTE] `:677-717`: cada item vira `item + "\\\\"`, o marcador é um
`MathTex("\\cdot")` escalado, e o conjunto é arranjado com
`arrange(DOWN, aligned_edge=LEFT, buff=buff)`. `fade_all_but("Item 2")` usa
`get_part_by_tex` e **levanta `Exception`** se não achar (não devolve `None`
como o método base).

**Aviso de projeto, não de API:** no repositório consumidor `~/Projects/aulas`
a lista de tópicos é **proibida** em slide (skill `aula-slides`: título é
frase-tese, corpo é gráfico). `BulletedList` existe e funciona; só não é o que
aquele deck quer. Se a sua saída é um deck, confira a regra antes.

### 9.4 Onde `DecimalNumber`/`Integer`/`Variable` tocam esta skill

[ÍNDICE] Moram em `mobject/text`, mas o assunto deles é estado que muda —
**`manim-updaters-valuetracker`** é o dono. O que é tipográfico e vale saber
aqui: `DecimalNumber` desenha cada dígito com `mob_class=MathTex`, ou seja,
**cada atualização de valor pode disparar LaTeX**. Num contador que roda 60
vezes por segundo isso é caro; `Text` como `mob_class` não é opção suportada
pela assinatura. `Variable(var, label, var_type=DecimalNumber,
num_decimal_places=2)` aceita `label` como `str | Tex | MathTex | Text |
SingleStringMathTex`.

---

## 10. Transformar uma fórmula em outra

[ÍNDICE] `manim/animation/transform_matching_parts.py`, categoria
`animation/transform`. As três classes têm **a mesma assinatura**:

```python
TransformMatchingTex   (mobject, target_mobject, transform_mismatches=False,
                        fade_transform_mismatches=False, key_map=None, **kwargs)
TransformMatchingShapes(mobject, target_mobject, …)     # idem
TransformMatchingAbstractBase(…)                        # a base, para subclassear
```

### 10.1 O mecanismo, em quatro linhas

[FONTE] `:89-140`. Ele constrói um `dict {chave → VGroup}` para a origem e
outro para o destino, e então:

- chaves **em comum** → um `Transform` só, com todas as partes;
- pares declarados em **`key_map={"x": "a"}`** → `FadeTransformPieces` (e
  saem dos dois mapas);
- o que sobra: por padrão `FadeOut` da origem + `FadeIn` do destino; com
  `transform_mismatches=True` vira `Transform`; com
  `fade_transform_mismatches=True` vira `FadeTransformPieces`.

A chave é diferente em cada subclasse [FONTE] `:227-235, 296-300`:

| Classe | Peças | Chave |
|---|---|---|
| `TransformMatchingTex` | `mobject.submobjects` (recursivo dentro de `Group`/`VGroup`) | `part.tex_string` — **exige `MathTexPart`**, com `assert` |
| `TransformMatchingShapes` | `family_members_with_points()` | hash dos pontos normalizados (centrado, altura 1) |

### 10.2 As três formas de falhar

1. **Sem `{{ }}` e sem vários argumentos, não há o que casar.** Uma `MathTex`
   de string única tem **um** submobject, cuja chave é a fórmula inteira;
   origem e destino nunca coincidem e a animação degrada para um fade cruzado.
   Funciona, mas não é o efeito que você pediu.
2. **`assert isinstance(mobject, MathTexPart)`** [FONTE] `:299`. Passar um
   `Text` para `TransformMatchingTex` é `AssertionError` (e antes disso já
   falharia o `assert hasattr(mobject, "tex_string")` de `:293`). Para texto
   comum use `TransformMatchingShapes`.
3. **Partes com espaço no nome não casam com partes sem.** `" + "` de um lado e
   `"+"` do outro são chaves diferentes. É a §8.4 de novo, e é a razão nº 1 de
   "ele transformou tudo em fade".

```python
a = MathTex("a^2", "+", "b^2", "=", "c^2")
b = MathTex("a^2", "=", "c^2", "-", "b^2")
self.play(TransformMatchingTex(a, b))                      # casa a^2, =, b^2, c^2
self.play(TransformMatchingTex(a, b, key_map={"+": "-"}))  # e ainda liga + → −
```

`run_time`, `rate_func`, `lag_ratio` e o resto do vocabulário temporal são de
**`manim-composicao-ritmo`**; o catálogo de animações é de
**`manim-animations`**.

---

## 11. Animar o texto aparecendo

Estas quatro existem e são específicas de texto; o catálogo completo é de
**`manim-animations`**. [ÍNDICE], categoria `animation/creation`:

```python
Write(vmobject, rate_func=linear, reverse=False, **kwargs)
Unwrite(vmobject, rate_func=linear, reverse=True, **kwargs)
AddTextLetterByLetter(text: Text, suspend_mobject_updating=False, int_func=np.ceil,
                      rate_func=linear, time_per_char=0.1, run_time=None, …)
AddTextWordByWord(text_mobject: Text, run_time=None, time_per_char=0.06, **kwargs)
RemoveTextLetterByLetter(text: Text, …, time_per_char=0.1, reverse_rate_function=True,
                         introducer=False, remover=True, **kwargs)
```

Três notas operacionais:

- `AddTextLetterByLetter` e `AddTextWordByWord` estão **tipados para `Text`**.
  Numa `MathTex` o que se usa é `Write`.
- **`run_time` e `time_per_char` brigam**: se você passar `run_time`, ele manda;
  senão o tempo é `time_per_char × nº de glifos`, o que faz uma frase longa
  demorar muito mais do que você imaginava.
- `Write` num texto grande é bonito e **caro de ler**: cada glifo é um caminho
  vetorial sendo desenhado. Para vídeo de aula, `FadeIn(shift=UP*0.28)` costuma
  ser mais legível — mas isso é gosto de projeto, e o dono do assunto é
  `manim-composicao-ritmo`.

---

## 12. `TexTemplate` — mudar o preâmbulo, a fonte e o compilador

[ÍNDICE] É uma `@dataclass`:

```python
TexTemplate(tex_compiler: str | list[str] = "latex",
            description: str = "",
            output_format: str = ".dvi",
            documentclass: str = r"\documentclass[preview]{standalone}",
            preamble: str = "\\usepackage[english]{babel}\n\\usepackage{amsmath}\n\\usepackage{amssymb}",
            placeholder_text: str = "YourTextHere",
            post_doc_commands: str = "")
```

Métodos próprios [ÍNDICE]: `add_to_preamble(txt, prepend=False)`,
`add_to_document(txt)`, `get_texcode_for_expression(expression)`,
`get_texcode_for_expression_in_env(expression, environment)`, `copy()`, e o
classmethod `from_file(file="tex_template.tex", **kwargs)`.

**O preâmbulo padrão tem exatamente três pacotes**: `babel[english]`,
`amsmath`, `amssymb`. Nada mais. Se a fórmula usa `\dv`, `\qty`, `\SI`,
`\mathscr`, `\mathds` — não vai compilar sem pacote.

```python
from manim import MathTex, TexTemplate

tpl = TexTemplate()
tpl.add_to_preamble(r"\usepackage{physics}")     # instalado aqui  [MÁQUINA]
MathTex(r"\dv{f}{x}", tex_template=tpl)
```

**Armadilhas [FONTE] `utils/tex.py`:**

- `from_file(...)` fixa o `body` inteiro; depois disso `add_to_preamble` e
  `add_to_document` **não fazem nada** e emitem `UserWarning` (`:100-106`).
- `add_to_preamble` **muta o template**. Se você reusa um template compartilhado
  em cenas diferentes, chame `.copy()` antes — ou vai acumular `\usepackage`
  repetidos entre cenas do mesmo processo.
- Trocar o template **invalida o cache inteiro** de LaTeX (o hash é do código
  completo, §8.1). O primeiro render depois disso é lento; isso é esperado.
- **Trocar `output_format` para `".pdf"` (pdflatex) provavelmente quebra o
  split em partes**, porque os `\special{dvisvgm:raw <g id=…>}` da §8.4 não
  sobrevivem ao caminho PDF. O sintoma é o `logger.error("MathTex: Could not
  find SVG group for tex part …")` e o *fallback* para o grupo `root`, isto é,
  **uma parte só** [FONTE] `tex_mobject.py:534-540`. [NÃO VERIFICADO — o
  mecanismo está lido, o render não foi feito.]

### 12.1 As duas bibliotecas prontas

[ÍNDICE] `TexTemplateLibrary` e `TexFontTemplates`, ambas no star import.

`TexTemplateLibrary` [FONTE] `utils/tex_templates.py:52-80`:

| Atributo | O que é |
|---|---|
| `default`, `threeb1b` | o preâmbulo do 3b1b: `lmodern` `dsfont` `setspace` `tipa` `relsize` `textcomp` `mathrsfs` `calligra` `wasysym` `ragged2e` `physics` `xcolor` `microtype` + `\DisableLigatures` |
| `ctex` | o mesmo, com `ctex` no lugar do `DisableLigatures`, **compilador `xelatex`**, `output_format=".xdv"` — é o caminho para CJK |
| `simple` | só `babel` + `amsmath` + `amssymb` (igual ao padrão) |

**Cuidado:** `TexTemplateLibrary.default` **não** é o template padrão do Manim.
O padrão é um `TexTemplate()` cru [FONTE] `_config/utils.py:1812-1820`. Os
nomes enganam.

`TexFontTemplates` é uma coleção de templates baseados em `mathastext` para
tipografar matemática em outras fontes (`american_typewriter`, `biolinum`,
`baskervald_adf_fourier`, …). [FONTE] a própria docstring avisa que **muitos
exigem fontes instaladas no sistema** e não compilam sem elas.

### 12.2 Trocar o template para o projeto inteiro

[FONTE] `_config/utils.py:307-308, 681-683, 851-853, 1812-1842`:

```python
from manim import config, TexTemplate
config.tex_template = TexTemplate(preamble=meu_preambulo)   # em Python
```

```ini
# manim.cfg
tex_template_file = ./meu_template.tex
```

```bash
bin/manim --tex_template ./meu_template.tex arquivo.py Cena
```

A precedência entre CLI, `manim.cfg`, `config` e `tempconfig` é de
**`manim-project`** §5; o tema como contrato é **`manim-tema-projeto`**.

---

## 13. Fundo claro: o que some, e o que é de outra skill

A conta de contraste, a paleta, `set_default`, `apply_theme` e os oito temas do
`mx` são **`manim-color-theming`** — não reescrevo nada disso. O que é
específico de texto:

| Objeto | Por que some | Correção |
|---|---|---|
| `Title.underline` | é um `Line` sem cor → branco [FONTE] `:752-762` | `t.underline.set_color(...)` |
| `Code` | fundo e cores vêm do `formatter_style` do Pygments, não do seu tema (§6) | escolher um estilo claro |
| glifos de `MathTex` | `init_colors` só repinta quem está preto (§8.5) | passar `color=` no construtor |
| `Text` container | `Text("xyz").color` devolve `#000000` mesmo com glifos brancos — o container mente | é `manim-color-theming` §9; confie no PNG |

E a regra que vale para as quatro linhas: **cor explícita em todo texto**. Um
helper obrigatório no tema do projeto é a única defesa que escala.

---

## 14. Desempenho e os DOIS caches de texto

Existem dois, com donos diferentes, e confundi-los é a origem de conselhos
errados que circulam:

| Cache | Onde | Chave | Como limpar |
|---|---|---|---|
| **LaTeX** | `media/Tex/*.tex,.dvi,.svg` | `tex_hash(código LaTeX completo)` [FONTE] | **`rm -rf media/Tex`, e só** — ver a nota abaixo |
| **Pango** | `media/texts/*.svg` | o sha256 da §2.7 | apagar a pasta |
| *(nenhum dos dois)* | `media/videos/…/partial_movie_files` | hash da chamada de `play` | `--no-cache` / `--disable_caching` |

**Correção, e ela importa porque a tabela acima existe para ser a última
palavra.** Uma versão anterior oferecia `--flush_cache` e `delete_nonsvg_files`
como formas de limpar o cache de LaTeX. **Nenhuma das duas limpa.**

```
scene_file_writer.py:1078-1090   def flush_cache_directory(self):
                                     # docstring: Delete all the cached partial movie files
                                     ... self.partial_movie_directory.iterdir()
cli/render/global_options.py:77  "--flush_cache"  help="Remove cached partial movie files."
utils/tex_file_writing.py:277    file_suffix_whitelist = {".svg", ".tex", *additional_endings}
                                 for f in tex_dir.iterdir():
                                     if f.suffix not in file_suffix_whitelist: f.unlink()
```

- `--flush_cache` apaga **partial movies** — o mesmo diretório do `--no-cache`
  que esta skill acabou de desqualificar. Não toca em `media/Tex`.
- `delete_nonsvg_files()` apaga `.dvi`, `.log`, `.aux` — e **preserva** `.svg` e
  `.tex`, os dois arquivos que fazem o cache de LaTeX acertar. Ele limpa lixo,
  não cache.
- Agravante: `--flush_cache` **não existe no `mx render`** (`manimx/cli.py:457-476`
  não o declara), só como parâmetro Python em `manimx/render.py`.

O único caminho real é `rm -rf media/Tex`.

**`--no-cache` NÃO desliga nem preserva o cache de LaTeX.** Ele é
`disable_caching`, e trata de *partial movies*. O cache de LaTeX está sempre
ligado e não tem chave para desligar. (Esta é uma correção ao que esta própria
skill dizia; ver §17.) Cache em profundidade: **`manim-performance-cache`** e
**`manim-render-api`**.

Regras de custo:

- Cada string LaTeX **nova** dispara `latex` + `dvisvgm`. Repetir uma string
  idêntica é leitura de disco.
- **Reaproveite objetos** em vez de reconstruir dentro de um laço.
- **`Text` quando não houver matemática** — é a economia mais barata do
  arquivo.
- Muitas fórmulas em edição? Renderize `-q l` enquanto ajusta o conteúdo, e
  volte para o final só no fim (a armadilha de esquecer é de
  `manim-batch-pipeline`).
- Num lote em paralelo, **isole `tex_dir` por worker**: `delete_nonsvg_files()`
  varre a pasta inteira e um worker apaga o `.dvi` do outro no meio da
  compilação. `tools/batch_render.py` já faz isso; o assunto é
  **`manim-batch-pipeline`**.

---

## 15. O LaTeX desta máquina

[MÁQUINA] TinyTeX (TeX Live **2026**) em `~/.TinyTeX`, **203** pacotes em
`~/.TinyTeX/tlpkg/tlpobj/`.

**Compiladores disponíveis** em `~/.TinyTeX/bin/x86_64-linux/`: `latex`,
`pdflatex`, `xelatex`, `lualatex`, `luahbtex`, `dvips`, `dvipdfmx`, **`dvisvgm`**,
`tlmgr`.

**Pacotes conferidos por `.sty`/`.cls` presente** [MÁQUINA]:

| Presentes | Ausentes |
|---|---|
| `standalone` `preview` `amsmath` `amssymb` `physics` `xcolor` `microtype` `mathastext` `relsize` `ragged2e` `setspace` `wasysym` `tipa` `dsfont` `lmodern` `textcomp` `mathrsfs` `calligra` `babel` `inputenc` `fontenc` `ctex` | **`siunitx`** |

`rsfs` está como pacote TeX Live (fontes) mas não expõe um `.sty` — o acesso é
via `\usepackage{mathrsfs}`.

### 15.1 A armadilha do PATH — e por que `tlmgr install dvisvgm` não resolve

[MÁQUINA] `~/.local/bin` tem symlinks para `latex`, `pdflatex`, `xelatex`,
`lualatex`, `tlmgr` — **mas não para `dvisvgm`**:

```
$ which latex     → /home/ondokai/.local/bin/latex
$ which dvisvgm   → dvisvgm not found
```

E `~/.TinyTeX/bin/x86_64-linux/dvisvgm` **existe**. Ou seja: chamando o Python
direto, o `latex` compila e o `dvisvgm` estoura `FileNotFoundError` no
`subprocess.run` de `convert_to_svg` [FONTE] `:238-246`. **Instalar o pacote
não conserta nada — o binário já está lá.**

A correção é usar os wrappers, que põem o diretório do TinyTeX no PATH
[FONTE] `bin/manim-env.sh:13-23`:

```bash
bin/mx render cena.py Cena          # certo
bin/manim -ql cena.py Cena          # certo
.venv/bin/python -m manim …         # ERRADO: sem dvisvgm
```

Se precisar chamar o Python cru:

```bash
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
```

Confira a cadeia inteira com `bin/mx doctor` — a linha "LaTeX → SVG (MathTex)".
Diagnóstico de ambiente em geral: **`manim-troubleshooting`** e
**`manim-project`**.

### 15.2 Instalar um pacote que falta

```bash
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
tlmgr install siunitx
```

---

## 16. Quando o LaTeX falha: ler o erro certo

[FONTE] `utils/tex_file_writing.py:200-225`. O compilador roda com
`-interaction=batchmode -halt-on-error` e a saída vai para `DEVNULL`. Se o
código de retorno não for zero, o Manim chama `print_all_tex_errors` e levanta:

```
ValueError: latex error converting to dvi. See log output above or the log file: media/Tex/<hash>.log
```

**É `ValueError`, sempre.** Não é `CalledProcessError` — o `subprocess.run` é
chamado sem `check=True`.

Antes de levantar, ele já imprimiu no logger [FONTE] `:288-364`:

- **cada** linha do `.log` que começa com `!`;
- **o contexto do `.tex`**, três linhas antes e depois, com a linha culpada
  marcada por `-> `;
- e, quando o erro casa um dos dois padrões conhecidos (`LATEX_ERROR_INSIGHTS`),
  uma dica em português técnico:

| Padrão no log | Dica emitida |
|---|---|
| `inputenc Error: Unicode character … (U+XXXX)` | nomeia o caractere pelo `unicodedata` e manda usar um `TexTemplate` próprio |
| `LaTeX Error: File '…sty' not found` | "You do not have package X installed" |

**O `.tex` e o `.log` são apagados** por `delete_nonsvg_files()` logo depois de
um render bem-sucedido. Para inspecioná-los:

```bash
bin/manim -ql --no_latex_cleanup cena.py Cena     # a flag existe só no `manim`
```

[MÁQUINA] `mx render` **não expõe** essa flag (`manimx/cli.py:457-476`). Mas ela
é uma chave de `config` [FONTE] `_config/utils.py:1025-1031`, então dá para
ligá-la de dentro da cena, o que funciona nos dois caminhos:

```python
from manim import config
config.no_latex_cleanup = True
```

Roteiro de bissecção de erro, traceback e "renderizou e não é o que eu queria":
**`manim-troubleshooting`** e **`manim-verificacao-visual`**.

---

## 17. Correções ao que circula por aí (e ao que esta skill dizia antes)

| Afirmação | Realidade na 0.21, com a prova |
|---|---|
| `Tex` é a classe base e `MathTex` a especializada | **invertido.** `Tex(MathTex)`, `MathTex(SingleStringMathTex)` [ÍNDICE, `api/manim-ce-inheritance.txt:182-187`] |
| `set_color_by_tex` casa substring | **não mais.** `if tex_str == tex` [FONTE] `tex_mobject.py:553`. Falha em silêncio |
| existe `get_parts_by_tex` | **não existe** na 0.21 [ÍNDICE] |
| `{{ }}` funciona em qualquer posição | só no **início da string ou depois de espaço** [FONTE] `:392-395` |
| `{{ }}` é obrigatório para colorir uma parte | **não é.** `tex_to_color_map`/`substrings_to_isolate` criam grupos endereçáveis sem virar submobject [FONTE] `:522-541` |
| **(estava aqui)** o exemplo `add_to_preamble(r"\usepackage{physics}\usepackage{siunitx}")` | **`siunitx` NÃO está instalado** nesta máquina [MÁQUINA] — o exemplo não compila. `physics` está |
| **(estava aqui)** "rode com `--no_latex_cleanup`" logo depois de exemplos com `bin/mx render` | a flag é do **`bin/manim`**; `mx render` não a tem [MÁQUINA, `manimx/cli.py`]. Alternativa: `config.no_latex_cleanup = True` (§16) |
| **(estava aqui)** "não desligue `--no-cache`, ele guarda o LaTeX compilado" | **errado.** `--no-cache` é `disable_caching`, o cache de *partial movies*. O LaTeX vive em `media/Tex` e sai **apagando a pasta** (§14) |
| **(estava aqui)** "o LaTeX sai com `--flush_cache`/`delete_nonsvg_files`" | **errado também, e da mesma família.** `--flush_cache` varre o MESMO diretório de partial movies que o `--no-cache` acima; `delete_nonsvg_files` **preserva** `.svg` e `.tex`, que são exatamente os arquivos que fazem o cache acertar (§14) |
| **(estava aqui)** erro de LaTeX vem como `ValueError`/`CalledProcessError` | só **`ValueError`** [FONTE] `tex_file_writing.py:220-225` |
| **(estava aqui)** a fatia de `t2c` é "semântica de slice do Python", sem dizer sobre o quê | ela indexa o **texto original com espaços**; `mob[a:b]` indexa **glifos** (§2.5) [FONTE] `text_mobject.py:308-329` |
| `dvisvgm not found` significa pacote TeX faltando | o **binário existe**; falta o symlink em `~/.local/bin`. Use `bin/mx`/`bin/manim` (§15.1). `manim-troubleshooting` tem essa linha para corrigir |
| `Text(font="X", warn_missing_font=False)` só silencia o aviso | **também desliga a recuperação de caixa** (§2.3) [FONTE] `:476-491` |
| `use_svg_cache=False` desliga o cache de texto | desliga só o cache **em memória**; o de **disco** é incondicional (§2.7) |

---

## 18. Onde esta skill para

| Assunto | Skill |
|---|---|
| escolher a cor, contraste, paleta, tema, "sumiu no fundo branco" | **`manim-color-theming`** |
| o `tema.py` como contrato (fonte, escala, helper obrigatório, dado externo) | **`manim-tema-projeto`** |
| posicionar, alinhar, medir, agrupar o texto depois de criado | **`manim-mobjects`**, **`manim-layout-posicionamento`** |
| o catálogo de animações; `Transform` × `ReplacementTransform` | **`manim-animations`** |
| `run_time`, `rate_func`, `lag_ratio`, orçamento de segundos | **`manim-composicao-ritmo`** |
| rótulo de eixo, `get_graph_label`, texto dentro de `Table`/`Matrix` | **`manim-graphs-plots`**, **`manim-tabelas-matrizes`** |
| número que conta na tela, `DecimalNumber`, `ValueTracker` | **`manim-updaters-valuetracker`** |
| descobrir se um nome/kwarg existe, conferir uma cena estaticamente | **`manim-api-discovery`** |
| qualidade, formato, onde o arquivo saiu | **`manim-render-api`** |
| olhar o PNG e provar que ficou certo | **`manim-verificacao-visual`** |
| cache, custo de rasterizar, `media/` | **`manim-performance-cache`** |
| lote, paralelismo, isolar `tex_dir` por worker | **`manim-batch-pipeline`** |
| erro de ambiente, traceback, bissecção | **`manim-troubleshooting`** |
| cortar a cena em partes para o slide avançar | **`manim-presentation-parts`** |
| SVG externo, imagem, logo, `register_font` de um `.ttf` do projeto | **`manim-svg-imagens`** (o `register_font` em si está na §2.4 daqui) |
| `Text` do **ManimGL** (outra API, `Text` do `manimlib`) | **`manimgl-3b1b`** |

**Buracos declarados, que nenhuma skill cobre hoje** — se o pedido cair aqui,
diga que não há skill em vez de improvisar: ênfase e anotação (`Flash`,
`Indicate`, `Circumscribe`, `Brace`, `BraceLabel`, `SurroundingRectangle`,
`Underline`, `Cross`); `LinearTransformationScene`/`VectorScene`; os 48
mobjects `OpenGL*`.
