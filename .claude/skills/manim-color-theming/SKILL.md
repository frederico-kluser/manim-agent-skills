---
name: manim-color-theming
description: >-
  Cor no Manim, de ponta a ponta: fundo da cena, tinta de traço e
  preenchimento, gradiente, sheen, as sete opacidades independentes, canal
  alfa, a paleta nativa e as 2.138 cores das paletas extras, aritmética de cor
  (interpolar, clarear, escurecer, misturar, os 20 operadores de `ManimColor`),
  contraste WCAG medido, temas claro e escuro, e a DISCIPLINA de paleta única
  do projeto. Use quando o pedido soar como "muda o fundo", "deixa fundo
  branco", "põe lousa branca", "quero tema claro/escuro", "essa forma sumiu",
  "o texto não aparece", "ficou branco no branco", "o traço saiu invisível",
  "que azul eu uso?", "esse cinza dá para ler?", "põe um gradiente", "deixa
  translúcido", "por que o preenchimento não aparece?", "exporta com fundo
  transparente para o Premiere/DaVinci", "as cores estão inconsistentes entre
  as cenas", "monta a paleta do projeto", "o tracejado sumiu", "o `-c WHITE`
  deu erro", "meu tema não pegou nessa cena", "a segunda cena do lote saiu
  preta". Cobre `ManimColor` inteiro (25 métodos + os operadores), o parser
  `ParsableManimColor`, `interpolate_color`/`color_gradient`/`average_color`/
  `contrasting`, as 52 classes do ManimCE que hard-codam cor na assinatura, os
  8 temas do `mx`, `apply_theme`, `set_default` e tudo que ele NÃO alcança, os
  três vazamentos silenciosos de tema entre renders no mesmo processo, e alfa
  premultiplicado em `.mov`. NÃO use para: escolher a CLASSE de texto ou
  colorir trechos com t2c/t2g/set_color_by_tex (skill `manim-text-latex`);
  posicionar, agrupar, medir mobject ou ordenar z-index (`manim-mobjects`,
  `manim-layout-posicionamento`); animar a troca de cor (`manim-animations`);
  o `tema.py` do projeto como CONTRATO — fonte, escala tipográfica, tempos,
  classe-base, dado externo (`manim-tema-projeto`, que defere a cor a esta);
  codec, NVENC e tamanho de arquivo (`manim-gpu-encoding`); ler
  `image_file`/`output_file` do render (`manim-render-api`); olhar o PNG e
  medir o quadro (`manim-verificacao-visual`); carregar SVG, PNG e fonte
  (`manim-svg-imagens`); luz e sombreamento 3D (`manim-3d-camera`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cor, fundo e tema

## Como ler esta skill

Cada afirmação carrega a origem. **Nada aqui é opinião sem marca.**

| Marca | Significa |
|---|---|
| **[medido]** | executado nesta máquina em 2026-08-19 — render, pixel de PNG, ou REPL. ManimCE **0.21.0**, Python 3.12.3, renderer cairo |
| **[fonte]** | lido no código do ManimCE 0.21 instalado em `.venv/lib/python3.12/site-packages/manim/`, com arquivo e linha. **Não executado** |
| **[conta]** | aritmética pura feita aqui (WCAG, truncamento), sem importar o Manim |
| **não verificado** | nem uma coisa nem outra. Está escrito assim, de propósito |

O resumo em seis frases, para quem só tem trinta segundos:

1. **Fundo é `config`/`camera`; tinta é `set_default` por classe** — dois
   mecanismos independentes, e cada um falha em silêncio sem o outro.
2. **`set_default` não alcança quem hard-coda cor na própria assinatura.**
   São **52 classes** no ManimCE 0.21 [fonte]; `VMobject.set_default(color=BLACK)`
   chega a 11 de 28 classes comuns [medido]. `Square`, `Rectangle`, `Dot`,
   `Annulus` continuam brancos — invisíveis em fundo branco, sem erro nenhum.
3. **A paleta nativa foi desenhada para fundo PRETO.** Das 89 constantes de
   `manim_colors`, **21 passam** AA 4,5:1 sobre branco, 68 sobre preto, e
   **nenhuma passa nos dois** [conta].
4. **`fill_opacity` nasce 0,0.** `set_fill(AZUL)` sem `opacity` não pinta nada,
   e não avisa [fonte: `vectorized_mobject.py`, assinatura de `VMobject`].
5. **Cor sem cor explícita é o defeito nº 1 de vídeo gerado por agente**, e ele
   nunca aparece no exit code. Renderize um PNG e **olhe** (§20).
6. **`mob.color` é um valor DERIVADO, não um registro.** Num `VMobject` ele
   devolve o traço quando o preenchimento é transparente, e pode devolver
   `None` [fonte: `vectorized_mobject.py:640-644`]. Ver §9.4.

---

## 0. Mapa rápido: onde mora cada decisão

| A pergunta | A seção | A resposta em uma linha |
|---|---|---|
| que cor eu escrevo? | §2, §6 | hex com `#`. Nome de constante só resolve nas 89 nativas |
| como o fundo muda? | §7 | `config` **e** `self.camera`, no `setup()` |
| por que a forma sumiu? | §10, §9.2 | classe hard-coda `color=WHITE`, ou `fill_opacity=0` |
| dá para ler? | §5 | WCAG ≥ 4,5 para texto, ≥ 3,0 para barra e traço |
| a paleta do projeto | §11 | uma constante nomeada por papel, e nenhum hex fora do tema |
| o tema vazou entre cenas | §12 | `set_default` sobrevive ao `tempconfig` |
| gradiente | §14 | `set_fill(color=[a, b])` é espacial; `set_color_by_gradient` é por filho |
| translúcido, alfa, `.mov` | §15, §16 | são sete opacidades diferentes; `-t` é uma catraca |
| não sei o nome da função | §19 | `bin/mx find` / `bin/mx show`, 0,05-0,23 s |

---

## 1. Correções ao que circula por aí

| Afirmação comum | Realidade na 0.21, com a prova |
|---|---|
| `manim -c WHITE arq.py Cena` muda o fundo | **Falso.** `-c` é `--config_file` [fonte: `cli/render/global_options.py:59-60`]. Passar `WHITE` dá `FileNotFoundError: --config_file could not find a valid config file.: 'WHITE'` [medido] |
| Existe `--background_color` na CLI | **Falso.** Removido. `manim render --help \| grep background` não devolve nada [medido] |
| Hex de 3 dígitos quebra o parser | **Falso.** `ManimColor("#F00").to_hex()` → `#FF0000`. `#F00F` (4 dígitos, com alfa) também [medido; fonte: `utils/color/core.py:315-316`, `if len(hex_) in (3, 4): hex_ = "".join([x * 2 for x in hex_])`] |
| Hex precisa de 6 dígitos | **Falso.** O que importa é o **prefixo**: `#` ou `0x`. `ManimColor("0xFF0000")` → `#FF0000`; `ManimColor("F00")` → `ValueError: Color F00 not found` |
| Fundo padrão do ManimGL é preto | **Falso** na biblioteca (`default_config.yml:61` = `#333333`), **verdadeiro** neste projeto: `custom_config.yml` força `#000000` de propósito |
| `RGBA` é uma classe de cor separada | **Falso.** `RGBA = ManimColor` [fonte: `core.py:1087`, a linha literal `RGBA = ManimColor`]. É um alias; `BLUE_D.into(RGBA)` devolve um `ManimColor` comum |
| Todo Mobject nasce branco | **Falso.** `Circle()` nasce **`#FC6255` (RED)**, `Polygon`/`Triangle`/`Star` nascem **`#58C4DD` (BLUE)**, `Cube` nasce azul. `Square`/`Rectangle`/`Line`/`Dot`/`Arrow`/`Axes` é que nascem brancos. A lista completa das 52 está em §10.2 |
| `mob.color` diz a cor que aparece | **Falso para container, e derivado sempre.** `Text("xyz").color` → `#000000`, mas os glifos desenhados são `#FFFFFF` [medido]. O mecanismo está em §9.4 |
| `ManimColor("red")` dá o vermelho do CSS | **Falso.** Dá o vermelho do **Manim**, `#FC6255`. O CSS red é `#FF0000` |
| `ManimColor("BLOODRED")` acha a cor da XKCD | **Falso.** Nome só resolve no dicionário montado no `__init__` do pacote, que contém **as 89 nativas e nada mais** [fonte: `utils/color/__init__.py:60-62` — `_all_color_dict` é feito de `globals()`, e as outras paletas entram como **módulo**, não como nome solto] |

**De onde vem o mito do `-c`.** Da documentação do próprio ManimCE: o docstring
de `ManimConfig` ainda ensina `manim scene.py -c BLUE` [fonte:
`_config/utils.py:236-241`]. O texto ficou; a flag mudou de significado. Quando
alguém insistir, é esse parágrafo que a pessoa leu.

O que **de fato** quebra: hex sem `#`/`0x`, e hex com contagem inválida
(`ManimColor("#12345")` → `ValueError: Hex colors must be specified with either
0x or # as prefix and contain 6 or 8 hexadecimal numbers`) [fonte: `core.py:318-322`].

---

## 2. Como o Manim entende uma cor

O tipo aceito em toda API de cor chama-se `ParsableManimColor` [fonte:
`core.py:1214` — `ManimColor | int | str | IntRGBLike | FloatRGBLike |
IntRGBALike | FloatRGBALike`]. Estas oito formas foram testadas uma a uma
[medido]:

```python
from manim import *

Circle(color=BLUE_D)                        # constante da paleta
Circle(color="#3B82F6")                     # hex 6 dígitos   ← prefira esta
Circle(color="#38F")                        # hex 3 dígitos   → expande
Circle(color="#3B82F6FF")                   # hex 8 = com alfa
Circle(color="0x3B82F6")                    # prefixo 0x também vale
Circle(color="BLUE_D")                      # NOME da constante, como string
Circle(color=ManimColor.from_rgb((59, 130, 246)))
Circle(color=ManimColor.from_hsv((0.6, 0.8, 0.9)))
```

### 2.1 O construtor, ramo a ramo

`ManimColor.__init__(value, alpha=1.0)` decide por `isinstance`, nesta ordem
[fonte: `core.py:163-224`]:

| `value` é | O que acontece | Pegadinha |
|---|---|---|
| `None` | preto com o `alpha` pedido | `ManimColor(None)` = `#000000`, **não** é erro. É assim que `Text` acaba com `.color` preto (§9.4) |
| outro `ManimColor` | **compartilha o array interno**, não copia | dois nomes apontando para o mesmo `_internal_value` |
| `int` | `0xRRGGBB` | `ManimColor(0)` = preto — e `0` é **falsy** (§9.5) |
| `str` com `#`/`0x` | caminho do hex, rápido | |
| `str` sem prefixo | busca no dicionário de nomes, **lento**, e o próprio código avisa: *"It can be horribly slow"* [fonte: `core.py:184-186`] | e **muta a constante global** se `alpha != 1.0` (§2.3) |
| `list`/`tuple`/`ndarray` de 3 ou 4 | float → escala 0-1; senão → escala 0-255 | ver 2.2 |
| qualquer outra coisa | `TypeError` | |

### 2.2 A armadilha do inteiro — e a da tupla MISTA

`from_rgb` (e o construtor) decidem sozinhos se a tupla é 0–255 ou 0.0–1.0
**pelo tipo de TODOS os elementos**: o teste é
`all(isinstance(x, float) for x in value)` [fonte: `core.py:191`].

```
ManimColor.from_rgb((255, 255, 255))    → #FFFFFF     int  → escala 0-255
ManimColor.from_rgb((1.0, 1.0, 1.0))    → #FFFFFF     float→ escala 0-1
ManimColor.from_rgb((1, 1, 1))          → #010101     ← int! quase preto   [medido]
ManimColor((1.0, 0.5, 0))               → ~#000000    ← UM int derruba a tupla inteira para
                                                        a escala 0-255 [fonte: core.py:191]
```

`(1, 1, 1)` é branco na cabeça de quem escreve e quase-preto na do Manim. E o
caso misto é pior, porque a maioria dos elementos "parece certa". **Escreva
sempre com ponto decimal** quando a escala for 0–1 — inclusive o zero: `0.0`.

### 2.3 Nome de cor: resolve na paleta do MANIM, e MUTA a constante global

```
ManimColor('red')    → #FC6255      CSS red    = #FF0000
ManimColor('green')  → #83C167      CSS green  = #008000
ManimColor('blue')   → #58C4DD      CSS blue   = #0000FF
ManimColor('teal')   → #5CD0B3      SVG teal   = #007F7F
```

Se você copiou um hex de um design system, **cole o hex**. Traduzir para nome
troca a cor sem avisar.

E há um efeito colateral que ninguém espera, **[fonte: `core.py:451-455`]**:

```python
def _internal_from_string(name: str, alpha: float) -> ManimColorInternal:
    from . import _all_color_dict
    if tmp := _all_color_dict.get(name.upper()):
        tmp._internal_value[3] = alpha       # ← escreve NA CONSTANTE GLOBAL
        return tmp._internal_value.copy()
```

`_all_color_dict` guarda **os próprios objetos** exportados por
`manim_colors` [fonte: `utils/color/__init__.py:60-62`]. Logo:

```python
ManimColor("BLUE_D", 0.3)     # devolve azul a 30%
BLUE_D.to_hex(True)           # → #29ABCA4C   ← a CONSTANTE global ficou a 30%
```

Como o caminho normal (`Circle(color="BLUE_D")`) usa `alpha=1.0`, o estrago só
aparece quando alguém pede opacidade **por nome** — em `ManimColor(nome, a)`,
`ManimColor.parse(nomes, alpha=a)` ou `color_to_rgba(nome, a)`. O sintoma é
distante da causa: uma cena depois, todo mundo que usa `BLUE_D` sai
translúcido. **Peça alfa pelo objeto, nunca pelo nome:**
`BLUE_D.opacity(0.3)` — esse copia antes de escrever [fonte: `core.py:761-763`].
**não verificado por execução** (leitura de fonte); a mutação está explícita
nas três linhas acima.

---

## 3. `ManimColor` — 25 métodos e 20 operadores

`bin/mx show ManimColor` lista todos [medido: 25 métodos próprios].
Assinatura da classe [fonte: `core.py:163`]:

```
ManimColor(value: ParsableManimColor | None, alpha: float = 1.0)
```

### 3.1 Construir

| Método | Assinatura (do índice) | Nota |
|---|---|---|
| `from_hex` | `(hex_str, alpha=1.0)` | aceita 3, 4, 6 e 8 dígitos |
| `from_rgb` | `(rgb, alpha=1.0)` | int → 0-255, float → 0-1 (§2.2) |
| `from_rgba` | `(rgba)` | mesma heurística; **não** tem parâmetro `alpha` |
| `from_hsv` | `(hsv, alpha=1.0)` | `(0.6, 0.8, 0.9)` → `#2D77E5` [medido] |
| `from_hsl` | `(hsl, alpha=1.0)` | atenção: internamente reordena para `hls_to_rgb(h, l, s)` [fonte: `core.py:903`] |
| `parse` | `(color \| Sequence[color], alpha=1.0)` | aceita **lista** e devolve lista. `parse(None)` → `ManimColor('#000000')` |

`parse` só considera sequência quando o argumento é `list` ou `tuple`
[fonte: `core.py:945-947`] — um `ndarray` de 4 floats vira **uma** cor, não
quatro. É a diferença entre `parse([RED, BLUE])` (duas cores) e
`parse(np.array([1., 0., 0., 1.]))` (uma).

### 3.2 Converter

`to_hex(with_alpha=False)` · `to_rgb()` · `to_rgba()` · `to_rgba_with_alpha(alpha)` ·
`to_int_rgb()` · `to_int_rgba()` · `to_int_rgba_with_alpha(alpha)` · `to_hsv()` ·
`to_hsl()` · `to_integer()` · `into(class_type)`

```
c = ManimColor("#3B82F6")
c.to_rgb()      → [0.23137255 0.50980392 0.96470588]
c.to_int_rgb()  → [ 59 130 246]
c.to_hsv()      → [0.60338681 0.7601626  0.96470588]
c.to_integer()  → 3900150
c.to_hex(True)  → #3B82F6FF
```

**`to_rgb()` e `to_rgba()` devolvem uma VISTA do array interno, não uma cópia**
[fonte: `core.py:478` — `return self._internal_value[:3]`; `:502` —
`return self._internal_value`]. Escrever no que voltou reescreve a cor:

```python
arr = BLUE_D.to_rgba()
arr *= 0.5              # ← o BLUE_D global acabou de escurecer, para sempre
```

Some com o problema fazendo `np.array(c.to_rgb())` ou `c.to_rgb().copy()`
sempre que o valor for entrar numa conta que escreve no lugar.

### 3.3 A deriva de 1/255, e de onde ela vem

O `to_hex` faz `int(canal * 255)` — **truncamento, não arredondamento**
[fonte: `core.py:561-568`]. Consequências, calculadas aqui **[conta]**:

- ida e volta direta pelo hex: **0 perdas em 256 valores**. Hex → interno → hex
  é exato;
- ida e volta pelo HSV (que é o que `into(HSV)` e `to_hsv()` fazem):
  numa amostra de 20.000 cores aleatórias, **10.084 (50%) perdem 1 unidade em
  pelo menos um canal**, sempre **para baixo**, nunca mais que 1;
- trocando `int()` por `round()` na mesma conta: **0 perdas**.

É por isso que `#3B82F6 → into(HSV) → #3A82F6` [medido]. Não é o espaço de cor
que perde precisão — é a truncagem na saída. Regra prática: **guarde a cor de
origem e derive dela toda vez**; nunca encadeie conversões dentro de um laço de
animação, ou a deriva vira degrau visível ao longo do vídeo.

### 3.4 Derivar

| Método | Assinatura | O que faz [medido] |
|---|---|---|
| `lighter` | `(blend=0.2)` | interpola com WHITE. `BLUE_D.lighter()` → `#53BBD4`; `.lighter(0.5)` → `#94D4E4` |
| `darker` | `(blend=0.2)` | interpola com BLACK. `BLUE_D.darker()` → `#2088A1` |
| `invert` | `(with_alpha=False)` | inversão linear. `BLUE_D.invert()` → `#D65435` |
| `opacity` | `(opacity)` | cópia com alfa novo. `BLUE_D.opacity(0.3).to_hex(True)` → `#29ABCA4C` |
| `interpolate` | `(other, alpha)` | `RED.interpolate(BLUE, 0.5)` → `#AA9399` |
| `contrasting` | `(threshold=0.5, light=None, dark=None)` | ver §5.1 |
| `gradient` | `(colors, length)` | **`raise NotImplementedError`** — o próprio docstring manda usar `color_gradient` [fonte: `core.py:957-965`] |

`lighter`/`darker` **preservam a opacidade**: eles leem `_internal_space[3]` e
reaplicam com `.opacity(alpha)` no fim [fonte: `core.py:672-677`, `:699-704`].
Encadear `.opacity(0.3).darker()` mantém 0,3.

**Os três interpolam no espaço do OBJETO.** Num `ManimColor` isso é RGBA; num
`HSV` é HSV [fonte: `core.py:631-651` usa `_internal_space`, que a `HSV`
sobrescreve em `:1169-1171`]. `HSV(...).darker()` interpola o **matiz** em
direção ao matiz do preto (que é 0, vermelho) — o resultado não é a cor mais
escura, é outra cor. **não verificado por execução.** Para escurecer, use
sempre um `ManimColor` comum.

### 3.5 Os operadores — cor como aritmética

`ManimColor` implementa `+ - * / // % **`, os refletidos, `~`, `& | ^`, `int()`
e `[]` [fonte: `core.py:981-1085`]. Todos operam sobre `_internal_space`, que
inclui **o canal alfa**, e **nenhum faz clamp**:

```python
BLUE * 0.5      # escurece… e deixa a opacidade em 0,5 junto
RED + GREEN     # soma canal a canal, pode passar de 1.0 sem reclamar
~BLUE           # == BLUE.invert()
BLUE[0]         # 0.34509804 — o canal R do espaço interno
int(BLUE)       # to_integer()
```

Quatro armadilhas, todas **[fonte]**:

1. **Os operadores refletidos estão trocados.** `__rsub__` faz
   `return self - other`; `__rtruediv__` faz `return self / other`; idem
   `__rfloordiv__`, `__rmod__`, `__rpow__` [fonte: `core.py:1000-1001`,
   `1022-1023`, `1033-1034`, `1044-1045`, `1055-1056`]. Ou seja
   `1.0 - cor` **não** é `1.0 - cor`, é `cor - 1.0`. Para inverter, use
   `cor.invert()` ou `~cor`. **não verificado por execução** — a leitura é
   inequívoca.
2. **A multiplicação come a opacidade.** `cor * 0.5` multiplica os quatro
   canais. Se a cor era opaca, ela sai a 50% de opacidade e alguém vai passar a
   tarde procurando o `set_opacity` culpado. Multiplique e devolva o alfa:
   `(cor * 0.5).opacity(1.0)`.
3. **Sem clamp, o excesso só aparece no `to_hex`**, onde `int(x*255)` de um
   valor acima de 1,0 estoura o `%02X` e produz hex de 3 dígitos por canal
   (`#1FF...`). Se um hex "cresceu", procure uma soma de cores.
4. **`==` levanta exceção contra outro tipo.** `__eq__` faz
   `raise TypeError(f"Cannot compare {…} with {…}")` para não-`ManimColor`
   [fonte: `core.py:973-980`]. Então `cor in (None, WHITE)` e
   `cor == "#FFFFFF"` **estouram**, não devolvem `False`. Use `is`/`is not`, ou
   compare `to_hex()`. `__hash__` existe e usa `to_hex(with_alpha=True)`, então
   cor funciona como chave de dicionário e dentro de `set` [fonte: `core.py:1083-1084`].

### 3.6 `into()` e o espaço de cor

`into(class_type)` reembala o mesmo valor interno noutra classe de espaço
[fonte: `core.py:765-782`]. Serve para uma coisa só que vale muito: **fazer
aritmética no espaço certo**.

```python
from manim import HSV
girado = BLUE.into(HSV) + 0.1      # +0,1 de MATIZ (não de vermelho)
```

Duas ressalvas, ambas **[fonte]** e **não verificadas por execução**:

- `HSV.__init__` guarda o alfa em `__hsv[3]`, mas o getter `_internal_value`
  monta o RGBA com `self.__alpha`, que veio do `super().__init__(None)` e vale
  sempre **1.0** [fonte: `core.py:1094-1105` × `:1170-1183`]. Resultado: o
  `alpha=` de um `HSV` não chega ao render. Precisa de opacidade? converta de
  volta (`HSV(...).into(ManimColor).opacity(a)`) antes de usar;
- `.opacity()` num `HSV` escreve em `__hsv[-1]`, que é o mesmo campo ignorado
  acima. Mesmo desfecho.

---

## 4. Cor como cálculo — as funções de módulo

Nenhuma delas exige uma cena; todas rodam no interpretador. São as **19**
entradas não-constantes da categoria `utils/color` no índice
(`awk -F'\t' '$3=="utils/color" && $1!="constant"' api/manim-ce-index.tsv`):
4 classes (`ManimColor`, `HSV`, `RGBA`, `RandomColorGenerator`) e 15 funções.

```python
from manim import (interpolate_color, color_gradient, average_color,
                   invert_color, random_color, random_bright_color,
                   RandomColorGenerator, hex_to_rgb, rgb_to_hex,
                   color_to_rgb, color_to_rgba, color_to_int_rgb,
                   color_to_int_rgba, rgb_to_color, rgba_to_color,
                   get_shaded_rgb, HSV, RGBA)
```

| Função | Assinatura (índice) | Medido / lido |
|---|---|---|
| `interpolate_color` | `(color1, color2, alpha)` | `(RED, BLUE, 0.5)` → `#AA9399`. **Interpola o alfa junto** [fonte: `core.py:645-650`] |
| `color_gradient` | `(reference_colors, length_of_output)` | `([RED, BLUE], 5)` → `['#FC6255','#D37A77','#AA9399','#81ABBB','#58C4DD']`. **Descarta o alfa** — trabalha em `to_rgb()` e devolve `rgb_to_color` [fonte: `core.py:1411-1423`] |
| `average_color` | `(*colors)` | `(RED, BLUE)` → `#AA9399` (idêntico a interpolar em 0,5). **Descarta o alfa**, e o docstring diz isso [fonte: `core.py:1448-1462`] |
| `invert_color` | `(color)` | `BLUE_D` → `#D65435`. Preserva o alfa |
| `hex_to_rgb` / `rgb_to_hex` | `(hex_code)` / `(rgb)` | ida e volta perde ~1: `rgb_to_hex((0.23,0.51,0.96))` → `#3A82F4` [medido] — é a truncagem de §3.3 |
| `color_to_rgb` / `color_to_rgba` | `(color)` / `(color, alpha=1.0)` | atalhos; `color_to_rgba` aceita **nome**, e aí vale o aviso de §2.3 |
| `get_shaded_rgb` | `(rgb, point, unit_normal_vect, light_source)` | sombreamento 3D; devolve RGB **sem clamp** — `[0.47, 0.87, 1.17]` num teste [medido]. Ver §17 |

### 4.1 Quatro armadilhas de `color_gradient`, todas medidas

```
color_gradient([RED, BLUE], 5)  → 5 cores          ok
color_gradient([RED, BLUE], 1)  → [ManimColor('#58C4DD')]   ← a ÚLTIMA, não a primeira
color_gradient([RED, BLUE], 0)  → []               lista vazia, sem erro
color_gradient([RED], 5)        → 5 vezes #FC6255  degrada em constante
color_gradient([], 5)           → ValueError: Expected 1 or more reference colors. Got 0 colors.
```

O caso `length_of_output=1` é o que morde, e o mecanismo explica por quê: a
função força `alphas_mod1[-1] = 1` e `floors[-1] = num_colors - 2`, o que para
uma saída de um elemento só significa "pegue o fim do último trecho"
[fonte: `core.py:1417-1419`]. Uma legenda de série única fica com a cor errada
e ninguém repara até alguém comparar com o gráfico de duas séries. **Trate
`len == 1` na mão.**

### 4.2 Aleatório: só com semente, e nunca sobre branco

```python
g = RandomColorGenerator(seed=42)
[g.next().to_hex() for _ in range(3)]   # ['#8B4513', '#BBBBBB', '#BBBBBB']   [medido]
```

Assinatura: `RandomColorGenerator(seed: int | None = None, sample_colors: list[ManimColor] | None = None)`.
Com a mesma semente a sequência se repete byte a byte [medido]. **Sem
semente, o render não é reproduzível** — e cena em partes com cor sorteada
quebra a emenda entre partes (ver `manim-presentation-parts`).

Três notas, e a terceira é uma prova:

- a sequência com `seed=42` repetiu `#BBBBBB` em posições consecutivas: a
  amostragem é `random.choice` sobre a paleta inteira, **com repetição**
  [fonte: `core.py:1565-1567`];
- `next()` devolve **o próprio objeto** da lista `_all_manim_colors`, não uma
  cópia [fonte: `core.py:1567`]. Somado a §3.2, mexer no que voltou mexe na
  constante global;
- **`random_bright_color()` NUNCA passa AA 4,5 sobre branco.** Ele é
  `0.5 * (rgb_aleatório + 1)` [fonte: `core.py:1465-1478`], então o canal mais
  escuro possível é 0,5 nos três — luminância relativa 0,2140, razão contra
  branco **3,98** [conta]. O melhor caso já reprova. Se precisar de cor
  aleatória sobre fundo claro, passe `sample_colors` com uma lista sua já
  auditada por contraste (§5).

`random_color()` usa um singleton sem semente [fonte: `core.py:1585-1600`], que
cai no `random` global do Python — então `random.seed(0)` no topo do módulo
torna a sequência reproduzível. **não verificado por execução.**

---

## 5. Contraste: a conta que decide se dá para ler

### 5.1 `contrasting()` — o que a biblioteca oferece

```python
ManimColor("#F4F1EA").contrasting()                        # → #000000
ManimColor("#1E1E2E").contrasting()                        # → #FFFFFF
BLUE_D.contrasting(light=YELLOW, dark=MAROON_E)            # → #94424F
GREY.contrasting(0.5) , GREY.contrasting(0.8)              # → #000000 , #FFFFFF
```

Assinatura: `contrasting(threshold: float = 0.5, light: Self | None = None, dark: Self | None = None)`.
Ele calcula `colorsys.rgb_to_yiq(*self.to_rgb())[0]` e devolve `light` se a
luminância for **menor** que `threshold`, senão `dark` [fonte: `core.py:706-741`].

Isso é **YIQ sobre sRGB gama-codificado**, não a luminância relativa da WCAG.
Testado contra WCAG em 14 cores da paleta: discordam em **1** (`PINK` `#D147BD`
— o `contrasting()` manda branco, a WCAG prefere preto, 5,35 contra 3,93)
[medido/conta]. Para rótulo dentro de uma barra colorida, `contrasting()`
resolve e é uma linha. Para decidir se a paleta do projeto é legível, use a
conta abaixo.

### 5.2 O medidor WCAG (rode antes de fechar a paleta)

Este arquivo foi escrito, executado e conferido [medido]:

```python
"""contraste.py — auditoria WCAG 2.1 de uma paleta contra o fundo do tema."""
from manim import ManimColor


def _luminancia(cor: ManimColor) -> float:
    def lin(u: float) -> float:
        return u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4
    r, g, b = cor.to_rgb()
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def razao(a, b) -> float:
    """1.0 = cores iguais · 21.0 = preto contra branco."""
    la, lb = _luminancia(ManimColor(a)), _luminancia(ManimColor(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def audita(fundo, paleta: dict, minimo: float = 4.5) -> list[str]:
    ruins = []
    for nome, cor in paleta.items():
        r = razao(fundo, cor)
        if r < minimo:
            ruins.append(nome)
        print(f"  {nome:12} {ManimColor(cor).to_hex():9} {r:6.2f}  "
              f"{'ok' if r >= minimo else 'REPROVA'}")
    return ruins
```

Patamares: **4,5** é AA para texto corrido, **3,0** para texto grande (≥ 18 pt,
ou 14 pt em negrito) e para **elementos gráficos** — uma barra, um traço, uma
seta —, **7,0** é AAA. Num vídeo projetado, com sala clara e compressão em
cima, trate 4,5 como piso e não como meta. E lembre que uma barra de gráfico
compete com o **fundo**, não com o texto: a barra pode viver em 3,0, mas o
número escrito em cima dela precisa de 4,5 contra a barra.

### 5.3 O que a medição diz da paleta nativa

`razao()` de todas as 89 constantes de `manim.utils.color.manim_colors`
[conta, recalculado nesta rodada e idêntico à medição de 19/08]:

| Fundo | Passam AA 4,5 | Passam 3,0 |
|---|---|---|
| **preto** `#000000` | **68 de 89** | **76 de 89** |
| **branco** `#FFFFFF` | **21 de 89** | **35 de 89** |
| **nos dois** | **0 de 89** | — |

As 21 que passam sobre branco, na íntegra — repare que são **cinzas escuros,
roxos, marrons e um azul**, e que os aliases `GRAY_*`/`GREY_*` dobram a lista:

```
BLACK       21,00   GRAY_E/GREY_E/DARKER_GRAY/DARKER_GREY  15,91
LOGO_BLACK  12,45   GRAY_D/GREY_D/DARK_GRAY/DARK_GREY       9,74
PURE_BLUE    8,59   PURPLE_E   8,26   DARK_BROWN  7,10
MAROON_E     6,66   LOGO_BLUE  6,61   PURPLE_D    6,32
BLUE_E/DARK_BLUE 5,89   GRAY_BROWN/GREY_BROWN 5,75   MAROON_D 5,57
```

A faixa **3,0–4,5** — reprova para texto, **serve para barra, traço e seta**
sobre branco:

```
RED_E 4,30 · PURE_RED 4,00 · MAROON_C/MAROON 3,99 · PINK 3,93 ·
PURPLE_C/PURPLE 3,91 · GRAY_C/GREY_C/GRAY/GREY 3,54 · RED_D 3,54 ·
GREEN_E 3,24 · PURE_MAGENTA 3,14
```

E os campeões de tutorial, os dois lados:

| Constante | hex | sobre branco | sobre preto |
|---|---|---|---|
| `BLUE_D` | `#29ABCA` | **2,70** | 7,77 |
| `BLUE` | `#58C4DD` | **2,03** | 10,36 |
| `RED` | `#FC6255` | **2,99** | 7,02 |
| `GREEN` | `#83C167` | **2,15** | 9,79 |
| `YELLOW` | `#F7D96F` | **1,39** | 15,11 |
| `TEAL` | `#5CD0B3` | **1,89** | 11,13 |
| `ORANGE` | `#FF862F` | **2,41** | 8,70 |
| `GOLD` | `#F0AC5F` | **1,95** | 10,77 |

`YELLOW` sobre branco é praticamente invisível. E a cor que
`SurroundingRectangle`, `Flash`, `Indicate` e `Circumscribe` hard-codam (§10.2)
é **pior ainda**: não é `YELLOW`, é **`PURE_YELLOW` = `#FFFF00`**, que mede
**1,07:1** sobre branco (19,56:1 sobre preto) — a um passo do piso teórico de
1,00.

```
shape_matchers.py:53      color: ParsableManimColor = PURE_YELLOW   # SurroundingRectangle
animation/indication.py:156, 229, 621                              # Flash, Indicate, Circumscribe
```

**Correção.** Uma versão anterior deste parágrafo dizia `YELLOW`, contradizendo
a tabela de §10.2 e a de §22 deste mesmo arquivo, que sempre disseram `#FFFF00`.
Num tema claro, o destaque some antes do conteúdo — e some mais do que a tabela
acima faz supor.

**Conclusão operacional: um projeto de fundo claro precisa de paleta própria.**
A do exemplo de §11 (`#1D1D1F` tinta, `#0071E3` acento, `#B3261E` alerta,
`#6E6E73` apagado) mede **16,83 · 4,70 · 6,54 · 5,07** sobre branco [conta] —
passa AA em tudo, e o acento passa por pouco (4,70 contra o piso de 4,50;
**reprova AAA**).

### 5.4 Os 8 temas do `mx`, medidos

```
tema             fundo     texto     razão   AA 4,5
3b1b             #000000   #FFFFFF   21,00   ok
whiteboard       #FFFFFF   #000000   21,00   ok
paper            #F4F1EA   #1C1B19   15,26   ok
slate            #1E1E2E   #CDD6F4   11,34   ok
nord             #2E3440   #ECEFF4   10,84   ok
solarized-dark   #002B36   #93A1A1    5,61   ok
solarized-light  #FDF6E3   #586E75    4,99   ok   ← o mais apertado
transparent      #000000   #FFFFFF   21,00   ok
```

`solarized-light` a 4,99 é o piso do conjunto: legível, mas sem folga para um
segundo tom de cinza. Se precisar de texto secundário nesse tema, escureça —
`ManimColor("#586E75").darker(0.3)` — e re-audite.

**Uma cor de acento não sobrevive à troca de tema.** O mesmo `#0071E3`, contra
o fundo de cada tema [conta]:

```
whiteboard 4,70  ok   ·  3b1b 4,47  quase  ·  solarized-light 4,35  reprova
paper      4,16  reprova  ·  slate 3,49  ·  solarized-dark 3,20  ·  nord 2,66
```

Ou seja: trocar de tema **não é trocar o fundo**, é refazer a paleta inteira.
Quem mantém dois temas mantém dois conjuntos de acento, auditados
separadamente.

---

## 6. As paletas: 89 nativas + 2.138 nomeadas

`from manim import *` traz **89** constantes de `manim_colors` [conta:
89 linhas `NOME = ManimColor("#…")` no módulo]. Famílias com sufixo de
luminosidade `_A` (mais claro) → `_E` (mais escuro):

```
BLUE_A BLUE_B BLUE_C BLUE_D BLUE_E      (idem TEAL, GREEN, YELLOW, GOLD,
                                         RED, MAROON, PURPLE, GREY/GRAY)
PURE_RED PURE_GREEN PURE_BLUE PURE_CYAN PURE_MAGENTA PURE_YELLOW
WHITE BLACK GREY_BROWN DARK_BROWN LIGHT_BROWN PINK LIGHT_PINK ORANGE
LOGO_BLACK LOGO_BLUE LOGO_GREEN LOGO_RED LOGO_WHITE
```

`BLUE` sem sufixo é `BLUE_C`; o azul de assinatura do 3b1b é `BLUE_D`/`BLUE_E`.
Cada família tem grafia dupla `GREY_*`/`GRAY_*` (mesmo hex), mais os aliases
`DARK_GREY`/`DARKER_GREY`/`LIGHT_GREY` — daí 89 constantes para bem menos cores
distintas.

Paletas extras [conta, contadas no fonte de cada módulo]:

| Módulo | Cores | Para quê |
|---|---|---|
| `XKCD` | 922 | nomes coloquiais de uma pesquisa com humanos (`BLOODRED` `#980002`) |
| `X11` | 504 | X11/Xorg, com as variantes numeradas (`DODGERBLUE1`…`4`) |
| `BS381` | 287 | norma britânica |
| `AS2700` | 206 | norma australiana |
| `SVGNAMES` | 151 | nomes CSS/SVG oficiais |
| `DVIPSNAMES` | 68 | as do `xcolor` do LaTeX |

Total: **2.138** extras + 89 nativas = 2.227 constantes de cor.

```python
from manim.utils.color import XKCD, SVGNAMES
Dot(color=XKCD.BLOODRED)
```

### 6.1 NUNCA faça star-import de uma paleta

[medido]

```python
from manim import *
TEAL.to_hex()                                  # '#5CD0B3'
from manim.utils.color.SVGNAMES import *
TEAL.to_hex()                                  # '#007F7F'   ← sobrescreveu
```

Colisões de nome com `manim_colors`, e quantas têm **hex diferente**
[conta, recontado nesta rodada]:

| Módulo | nomes que colidem | com hex diferente | exemplos |
|---|---|---|---|
| SVGNAMES | 14 | **12** | `BLUE` `GREEN` `GOLD` `GRAY` `GREY` `MAROON` |
| XKCD | 13 | **11** | `BLUE` `GOLD` `GREEN` `GREY` `MAROON` `ORANGE` |
| DVIPSNAMES | 10 | **9** | `BLACK` `BLUE` `GRAY` `GREEN` `MAROON` `ORANGE` |
| X11 | 6 | **4** | `GRAY` `MAROON` `PINK` `PURPLE` |
| BS381 | 4 | **4** | `DARK_BROWN` `LIGHT_BROWN` `LIGHT_GREY` `MAROON` |
| AS2700 | 0 | 0 | — |

Sempre `from manim.utils.color import SVGNAMES` e depois `SVGNAMES.TEAL`. E ao
buscar no índice, lembre que `mx find TEAL` devolve **três** linhas com três
hex — `#5CD0B3` (nativa), `#007F7F` (SVGNAMES) e `#029386` (XKCD) — porque o
índice cobre todas as paletas.

### 6.2 Nome como string só funciona para as 89

`ManimColor("BLOODRED")` **levanta `ValueError`**, apesar de `XKCD.BLOODRED`
existir. O dicionário de nomes é montado a partir dos `globals()` do pacote
`manim.utils.color`, onde as outras seis paletas entram como **módulo**, não
como nome solto [fonte: `utils/color/__init__.py:57-62`]. Consequência prática:
`--background "AVOCADO"` e `Circle(color="AVOCADO")` falham, mas
`Circle(color=XKCD.AVOCADO)` funciona. **não verificado por execução.**

---

## 7. O fundo da cena: cinco caminhos e a ORDEM que decide

Todos verificados lendo o pixel `(5,5)` do PNG renderizado [medido].

### 7.1 `manim.cfg` — o projeto inteiro

```ini
[CLI]
background_color = #FF0000
```

Aceita hex **e nome**: o `manim.cfg` deste projeto tem `background_color = BLACK`
na linha 57 (confirme com `bin/manim cfg show`, que imprime
`background_color : BLACK`). **Use `bin/manim`, não `.venv/bin/manim`** — o
wrapper resolve LaTeX e GPU antes de chamar o binário, e é passthrough puro
para o resto [fonte: `bin/manim:14`].

### 7.2 `config` no topo do módulo — o arquivo

```python
from manim import *
config.background_color = "#00FF00"        # aqui FUNCIONA
```

O setter converte para `ManimColor` na hora [fonte: `_config/utils.py:1205-1207`],
então valor inválido explode aqui e não no meio do render.

### 7.3 `self.camera.background_color` — aquela cena, a qualquer momento

```python
class Demo(Scene):
    def construct(self):
        self.camera.background_color = "#0000FF"    # canto medido: (0, 0, 255) ✓
```

O setter da câmera chama `init_background()` **imediatamente**
[fonte: `camera/camera.py:172-175`], que repinta o array de fundo inteiro. Por
isso ele funciona dentro do `construct` — e por isso dá para **trocar o fundo
no meio da cena**, sem animação: a troca é instantânea, no frame seguinte. Para
transição suave, anime um `Rectangle` de tela cheia por cima.

### 7.4 A armadilha: `config.background_color` DENTRO do `construct` não faz nada

```python
class Demo(Scene):
    def construct(self):
        config.background_color = "#00FF00"     # canto medido: (0, 0, 0) ✗
        self.add(Dot())
```

A câmera lê o `config` **uma vez**, quando é construída
[fonte: `camera/camera.py:134-142` — `if background_color is None: … config["background_color"]`];
mexer no `config` depois disso não a alcança. E não sai erro, nem aviso: o
vídeo simplesmente fica com o fundo antigo. Foi medido lado a lado: as três
cenas acima, mesmo comando, cantos `(0,0,0)` / `(0,0,255)` / `(255,0,255)`.

**A defesa é escrever nos dois lugares, no `setup()`:**

```python
class CenaBase(Scene):
    FUNDO = "#FFFFFF"

    def setup(self) -> None:
        config.background_color = self.FUNDO        # para quem LÊ o config
        self.camera.background_color = self.FUNDO   # para quem DESENHA
        super().setup()
```

`setup()` roda antes de `construct()` e depois de a câmera existir — canto
medido `(255,0,255)` com `#FF00FF`. É esse par que garante o fundo em todos os
caminhos de render (vídeo, `--format png`, `-s`, `--save_sections`).

**E o `config` não é redundante.** Quem mais lê `config.background_color`
durante a cena:

- `BackgroundRectangle(...)` sem `color=`, que assume o fundo do config
  [fonte: `geometry/shape_matchers.py:118-119`] — com o config errado, a placa
  que deveria sumir vira um retângulo visível;
- `Mobject.add_background_rectangle()`, que constrói o mesmo objeto;
- qualquer código seu que consulte o tema.

### 7.5 CLI, pela camada `manimx`

```bash
bin/mx render cena.py Demo --background "#FFFFFF"
bin/mx render cena.py Demo --background "#F00"      # 3 dígitos: OK
bin/mx render cena.py Demo --background "BLUE_E"    # nome: OK, canto (35,107,142)
bin/mx render cena.py Demo --background "F00"       # FALHA com ValueError: Color F00 not found
```

O `--help` do flag diz "cor hex de 6 dígitos"; medido, ele aceita 3, 6, 8, `0x`
e nome de constante nativa. O que ele recusa é a falta de prefixo — e recusa
**alto**, com a exceção do Manim no stderr, que é o comportamento certo.

**`--theme` vence `--background`.** O `--background` entra no dicionário do
`tempconfig`; o `apply_theme` roda **depois**, já dentro do `with`, e
sobrescreve `config.background_color` [fonte: `manimx/render.py:218-219` ×
`:422-425`]. Passar os dois é silenciosamente o tema. **não verificado por
execução.**

### 7.6 `render_file` / `render_scene` em Python

```python
from manimx.render import render_file
render_file("cena.py", "Demo", background_color="#FFFFFF")
```

### 7.7 A precedência, resumida

```
defaults da biblioteca
  → ~/.config/manim/manim.cfg
    → manim.cfg do projeto            (background_color = BLACK, aqui)
      → flags da CLI                  (--background)
        → --theme                     (vence a flag acima)
          → config.<chave> no topo do módulo / tempconfig
            → self.camera.background_color   (o último a falar, e o que pinta)
```

Para o resto da precedência de config (o `cwd` como parte da configuração, as
chaves que só existem no `.cfg`), veja `manim-project` §5 — este é o único
recorte de cor.

---

## 8. Temas prontos

```bash
bin/mx presets                 # imprime tudo, 0,06 s
bin/mx presets --json          # chaves: quality, codec, nvenc_profiles, themes
```

| Tema | Fundo | Texto | Uso |
|---|---|---|---|
| `3b1b` | `#000000` | `#FFFFFF` | padrão do canal |
| `whiteboard` | `#FFFFFF` | `#000000` | corporativo, artigo, slide claro |
| `paper` | `#F4F1EA` | `#1C1B19` | papel creme, bom para impressão |
| `slate` | `#1E1E2E` | `#CDD6F4` | escuro suave (Catppuccin Mocha) |
| `solarized-dark` | `#002B36` | `#93A1A1` | |
| `solarized-light` | `#FDF6E3` | `#586E75` | |
| `nord` | `#2E3440` | `#ECEFF4` | |
| `transparent` | `#000000` + opacidade 0 | `#FFFFFF` | composição em NLE (§16) |

```bash
bin/mx render cena.py Demo --theme whiteboard
```

```python
from manimx import apply_theme
apply_theme("whiteboard")     # ANTES de instanciar qualquer Mobject
```

Assinatura real: `apply_theme(name: str, *, set_defaults: bool = True) -> dict`.
Ele faz **duas** coisas e devolve o dicionário do tema [fonte: `manimx/presets.py:207-222`]:

1. `config.background_color = <fundo>` (e `background_opacity`, **só se o tema
   trouxer a chave** — e só o `transparent` traz);
2. com `set_defaults=True`: `set_default(color=<texto>)` em exatamente quatro
   classes — `Text`, `Tex`, `MathTex` e `VMobject`.

**A parte 2 cobre metade do problema — e só metade.** Ver §10.

No caminho do `mx render`, `apply_theme` é chamado dentro do `tempconfig` e
**antes** de `scene_class()` [fonte: `manimx/render.py:419-431`]. Consequência
medida em §13: mobject criado no import do módulo não recebe o tema.

**O que `--theme` NÃO faz:** ele não toca em `self.camera.background_color`.
Se a sua cena-base escreve o fundo no `setup()` (§7.4), **ela vence o tema** —
a cena sai com o fundo da classe e a tinta do tema. É a combinação que produz
"pedi whiteboard e o fundo continuou preto".

---

## 9. Pintar: `Mobject` e `VMobject` são duas APIs, não uma

A confusão mais cara desta área: quase tudo que se ensina como "método de
Mobject" só existe em `VMobject`. A tabela abaixo saiu do índice
(`awk -F'\t' '$2=="set_stroke" {print $4}' api/manim-ce-methods.tsv`), coluna
`defined_in`.

### 9.1 Quem define o quê

| Método | Definido em | Assinatura |
|---|---|---|
| `set_color` | **`Mobject`** e `VMobject` (redefinido) | `Mobject:(color=PURE_YELLOW, alpha=None, family=True)` · `VMobject:(color, family=True)` |
| `set_color_by_gradient` | **`Mobject`** | `(*colors)` |
| `set_colors_by_radial_gradient` | **`Mobject`** | `(center=None, radius=1, inner_color=WHITE, outer_color=BLACK)` |
| `set_submobject_colors_by_gradient` | **`Mobject`** | `(*colors)` |
| `match_color` | **`Mobject`** | `(mobject)` |
| `to_original_color` | **`Mobject`** | `()` — reaplica `self.color` |
| `fade` | **`Mobject`** (no-op) e `VMobject` | `(darkness=0.5, family=True)` |
| `fade_to` | **`Mobject`** | `(color, alpha, family=True)` |
| `add_background_rectangle` | **`Mobject`** | `(color=None, opacity=0.75, **kwargs)` |
| `set_z_index` | **`Mobject`** | `(z_index_value, family=True)` |
| `set_stroke` | **só `VMobject`** | `(color=None, width=None, opacity=None, background=False, family=True)` |
| `set_fill` | **só `VMobject`** | `(color=None, opacity=None, family=True)` |
| `set_opacity` | **só `VMobject`** (e `ImageMobject`) | `(opacity, family=True)` |
| `set_style` / `get_style` | **só `VMobject`** | ver a assinatura completa abaixo |
| `match_style` | **só `VMobject`** | `(vmobject, family=True)` |
| `set_sheen` / `set_sheen_direction` / `rotate_sheen_direction` | **só `VMobject`** | `(factor, direction=None, family=True)` |
| `set_background_stroke` | **só `VMobject`** | `(**kwargs)` → `set_stroke(**kwargs, background=True)` |
| `set_cap_style` | **só `VMobject`** | `(cap_style: CapStyleType)` — `AUTO`, `ROUND`, `BUTT`, `SQUARE` |
| `color_using_background_image` | **só `VMobject`** | `(background_image)` |
| `get_fill_color` / `get_stroke_color` / `get_fill_opacity` / `get_stroke_opacity` | **só `VMobject`** | ver 9.4 |

```
VMobject.set_style(fill_color, fill_opacity, stroke_color, stroke_width,
                   stroke_opacity, background_stroke_color, background_stroke_width,
                   background_stroke_opacity, sheen_factor, sheen_direction,
                   background_image, family=True)
```

Duas consequências imediatas:

- **`ImageMobject` e `PMobject` não têm `set_fill`/`set_stroke`.** Numa cena com
  imagem, `set_opacity` existe (`ImageMobject` tem o seu), mas `set_fill` dá
  `AttributeError`. Ver `manim-svg-imagens`;
- **`Mobject.set_color(cor, alpha=0.5)` ignora o `alpha` em silêncio** — o
  parâmetro nunca é usado no corpo [fonte: `mobject.py:2036-2052`] — e
  `VMobject.set_color` nem aceita o argumento, então o mesmo código dá
  `TypeError` num `Circle` e passa batido num `PMobject`. Para opacidade,
  `set_fill(opacity=…)` / `set_stroke(opacity=…)` / `set_opacity(…)`.

```python
c = (Circle(radius=1.5)
     .set_stroke("#0071E3", width=6)
     .set_fill("#0071E3", opacity=0.15))
```

### 9.2 `set_fill` sem `opacity` não mostra nada — e o motivo está na assinatura

`VMobject.__init__` nasce com `fill_opacity: float = 0.0` e
`stroke_opacity: float = 1.0`, `stroke_width: float = 4` [fonte: assinatura de
`VMobject` no índice]. O preenchimento padrão da maioria das formas é **0**
[medido: `Circle` 0.0, `Square` 0.0, `Rectangle` 0.0, `Line` 0.0, `Arrow` 0.0;
as exceções são `Dot` 1.0 e `Annulus` 1.0, que declaram `fill_opacity=1` na
própria assinatura].

Este é o erro de cor mais comum e **não dá erro nenhum**:

```python
Square().set_fill(AZUL)                # nada aparece
Square().set_fill(AZUL, opacity=1)     # certo
Square(fill_color=AZUL, fill_opacity=1)  # certo, e num construtor só
```

`VMobject.set_color(cor)` chama `set_fill(cor)` **e** `set_stroke(cor)`
[fonte: `vectorized_mobject.py:473-476`] — mas nenhum dos dois toca em
opacidade. Ou seja: `set_color` numa forma de `fill_opacity=0` continua sem
preenchimento. É por isso que "mudei a cor e não mudou nada" costuma ser, na
verdade, "só o traço de 4 px mudou".

### 9.3 `family=True` propaga; `family=False` não

Padrão é `True`, e é o que você quer 95% das vezes. Use `False` para colorir só
o objeto pai — em `VGroup`, `Axes` e `MathTex`, onde os filhos têm cor própria.
`set_opacity` é o caso mais agressivo: ele escreve em fill, stroke **e**
background stroke de toda a família [fonte: `vectorized_mobject.py:478-482`].

### 9.4 `mob.color` é DERIVADO — e pode ser `None`

Em `VMobject`, `color` não é um atributo: é uma **propriedade**
`property(get_color, set_color)` [fonte: `vectorized_mobject.py:644`]. E
`get_color` decide a fonte na hora:

```python
def get_color(self) -> ManimColor:
    if np.all(self.get_fill_opacities() == 0):
        return self.get_stroke_color()      # ← forma sem preenchimento: devolve o TRAÇO
    return self.get_fill_color()
```

[fonte: `vectorized_mobject.py:640-643`]. Três desdobramentos:

1. **a mesma linha de código devolve coisas diferentes** conforme a
   `fill_opacity` do momento — pintar o preenchimento muda o que `.color`
   responde;
2. **pode devolver `None`.** `get_fill_colors`/`get_stroke_colors` devolvem
   `None` quando o RGBA é todo zero [fonte: `vectorized_mobject.py:593-596`,
   `:632-636`]. Um mobject completamente invisível (fill 0 e stroke 0) faz
   `mob.color.to_hex()` estourar com
   `AttributeError: 'NoneType' object has no attribute 'to_hex'`;
3. **atribuir `mob.color = RED` chama `set_color`** — pinta traço e
   preenchimento, propagando para a família. Não é só marcar um campo.

E em **container**, `.color` mente com todas as letras [medido]:

```
Text("xyz").color               → #000000
Text("xyz")[0].get_fill_color() → #FFFFFF      ← o que é desenhado
```

O mecanismo, que ninguém documenta: `SVGMobject.__init__` executa
`self.color = ManimColor(color)` com `color=None`, e `ManimColor(None)` é
**preto** [fonte: `svg/svg_mobject.py:123` × `core.py:167-168`]. Isso acontece
**antes** de os glifos existirem, então pinta o container vazio de preto; os
glifos entram depois, com a cor que o Pango escreveu no SVG. `Text`, `Tex`,
`MathTex`, `VGroup`, `Axes`, `Brace`, `NumberPlane` — todos containers, todos
mentem. Para saber a cor **desenhada**:

```python
def cor_desenhada(m):
    folhas = m.family_members_with_points()
    if not folhas:
        return None
    x = folhas[0]
    return x.get_stroke_color(), x.get_fill_color(), x.get_fill_opacity()
```

Ou, melhor ainda, renderize um PNG e olhe (`manim-verificacao-visual`).

### 9.5 Como `Text` resolve a própria cor

```python
parsed_color = ManimColor(color) if color else VMobject().color
```

[fonte: `text/text_mobject.py:539`]. Três coisas saem daí:

- **`Text` obedece a `VMobject.set_default(color=…)`** mesmo sem
  `Text.set_default` — porque ele instancia um `VMobject()` descartável só para
  ler a cor corrente. É por isso que `apply_theme` mexe em `VMobject`;
- **a cor entra no hash do SVG em cache** [fonte: `text_mobject.py:689-701`]:
  cada cor de texto gera um arquivo próprio em `media/texts`. Trocar a paleta
  invalida esse cache inteiro (assunto de `manim-performance-cache`);
- **`Text("x", color=0)` ignora a cor**, porque `0` é o preto na forma inteira
  e é falsy — cai no `else`. Curiosidade barata, mas é exatamente o tipo de
  coisa que some sem erro.

`SVGMobject` importado de arquivo é o oposto: ele passa
`super().__init__(color=None, stroke_color=None, fill_color=None)`
explicitamente [fonte: `svg_mobject.py:115`], e argumento explícito **vence** o
`set_default` (semântica de `functools.partial`). Um logo em SVG **não é
recolorido pelo tema** — mantém as cores do arquivo. Isso é o certo para uma
marca e é armadilha para um ícone monocromático: pinte-o à mão com
`.set_color(TINTA)` depois de carregar.

### 9.6 `fade` compõe, e `Mobject.fade` é um no-op

```python
VMobject.fade(darkness=0.5)   # multiplica as três opacidades por (1 - darkness)
```

[fonte: `vectorized_mobject.py:557-566`]. Duas notas: ele **compõe** — chamar
duas vezes com 0,5 deixa em 0,25, e não existe "desfazer" —; e em
`Mobject` (não vetorizado) o método só recorre nos filhos, **sem fazer nada**
[fonte: `mobject.py:2130-2134`]. Num `Group` com `ImageMobject`, `fade` parece
funcionar (a imagem tem o seu) e num `PMobject` não faz nada.

`Mobject.fade_to(color, alpha)` é outra coisa: interpola a **cor** em direção a
`color`, sem mexer em opacidade [fonte: `mobject.py:2119-2128`]. O nome engana
os dois lados.

### 9.7 `DashedVMobject` DESCARTA o `color=` que você passou

Este custou uma tarde num deck em produção. `DashedVMobject(vmobject,
num_dashes=15, dashed_ratio=0.5, dash_offset=0, color=WHITE, equal_lengths=True)`
aceita `color=` — e a **última linha do `__init__`** é

```python
self.match_style(base_vmobject, family=False)
```

[fonte: `vectorized_mobject.py:3043-3046`]. O estilo do mobject de origem
sobrescreve tudo; além disso os tracinhos são subcurvas de uma **cópia** do
original, e já nascem com o estilo dele. Em fundo branco, tracejar uma `Line`
sem cor explícita produz tracinhos brancos — invisíveis, sem erro.

```python
base = Line(A, B, color=TINTA, stroke_width=2)     # ESTILIZE ANTES
tracejado = DashedVMobject(base, num_dashes=24)    # e ignore o color= daqui
```

O mesmo padrão vale para qualquer wrapper que chame `match_style` no fim.

---

## 10. `set_default` e as 52 classes que hard-codam cor

### 10.1 O mecanismo

`Mobject.set_default(**kwargs)` é `classmethod` e faz literalmente isto
[fonte: `mobject.py:300-306`]:

```python
if kwargs:
    cls.__init__ = partialmethod(cls.__init__, **kwargs)
else:
    cls.__init__ = cls._original__init__
```

Quatro consequências que ninguém documenta:

1. **Uma subclasse que declara a cor com default na PRÓPRIA assinatura passa
   esse valor adiante explicitamente, e o default do pai nunca é consultado.**
   É a armadilha inteira desta seção;
2. **as chamadas acumulam.** `partialmethod` de `partialmethod` é achatado pelo
   CPython, com as chaves novas ganhando das velhas — então
   `X.set_default(color=A)` seguido de `X.set_default(fill_opacity=1)` mantém
   as duas, e um segundo `color=B` substitui o A;
3. **`set_default()` sem argumento restaura TUDO daquela classe**, não só a
   cor. Se você também tinha ajustado `stroke_width` por lá, ele volta junto;
4. **`Mobject.set_default()` (sem args) quebra.** `_original__init__` só é
   gravado em `__init_subclass__` [fonte: `mobject.py:99-105`], e `Mobject` não
   é subclasse de si mesmo — o atributo existe só como anotação
   [fonte: `mobject.py:93`]. Restaure a partir de `VMobject` para baixo.
   **não verificado por execução.**

### 10.2 As 39 classes do caminho cairo que hard-codam cor

Levantadas do índice — toda classe cuja assinatura própria traz um
`ManimColor(...)` como default [conta/fonte]:

```bash
awk -F'\t' '$1=="class" && $4 ~ /ManimColor\(/ {print $2"\t"$3}' \
  api/manim-ce-index.tsv | sort -u | grep -v '^OpenGL'
```

São **52 no total**: **12** com o prefixo `OpenGL*` e **40** no caminho normal.

**Correção, e a armadilha vale mais que o número.** Uma versão anterior dizia
"13 `OpenGL*` e 39 no caminho normal" — o próprio `awk` acima devolve 12 e 40.
A 40ª, ausente da tabela abaixo, é **`DotCloud`**
(`color: ParsableManimColor = ManimColor('#FFFF00')`), e ela é justamente o
motivo de o filtro por nome enganar: `DotCloud` **é OpenGL-only sem o prefixo
no nome**.

```
api/manim-ce-inheritance.txt:264  OpenGLPMobject
api/manim-ce-inheritance.txt:265    DotCloud
```

Ou seja: `grep -v '^OpenGL'` não separa "cairo" de "opengl", separa por
convenção de nomenclatura. Para a decisão real use a árvore de herança, não o
nome. Agrupadas pelo que a cor significa:

| Grupo | Classes e o valor hard-codado |
|---|---|
| **branco — some em fundo claro** | `Mobject` `color=#FFFFFF` · `Rectangle` (e por herança `Square`, `RoundedRectangle`) `#FFFFFF` · `Dot` `#FFFFFF` · `Dot3D` `#FFFFFF` · `Arrow3D` `#FFFFFF` · `Annulus` `#FFFFFF` · `AnnularSector` `#FFFFFF` · `Angle` **`dot_color`**`=#FFFFFF` · `AnnotationDot` **`stroke_color`**`=#FFFFFF` · `DashedVMobject` `#FFFFFF` (mas ver §9.7) · `TracedPath` **`stroke_color`**`=#FFFFFF` · `MovingCamera` `default_frame_stroke_color=#FFFFFF` |
| **preto — some em fundo escuro** | `VMobject` **`background_stroke_color`**`=#000000` · `Brace` idem · `MathTexPart` idem · `Point` / `VectorizedPoint` `#000000` · `Graph`/`DiGraph`/`GenericGraph` **`label_fill_color`**`=#000000` · `Table` **`entries_background_color`** e **`background_rectangle_color`**`=#000000` |
| **amarelo semântico — NÃO pinte** | `SurroundingRectangle` `#FFFF00` · `Flash` `#FFFF00` · `Indicate` `#FFFF00` · `Circumscribe` `#FFFF00` · `FunctionGraph` `#FFFF00` · `PointCloudDot` `#FFFF00` · `FocusOn` `#888888` |
| **cor de identidade** | `Circle` `#FC6255` · `Cross` **`stroke_color`**`=#FC6255` · `Polygram` (e `Polygon`, `Triangle`, `RegularPolygon`, `Star`) `#58C4DD` · `Cube` **`fill_color`**`=#58C4DD` · `Surface` `fill_color=#29ABCA`, `checkerboard_colors=[#29ABCA,#236B8E]`, `stroke_color=#BBBBBB` · `SampleSpace` `fill_color=#444444`, `stroke_color=#BBBBBB` · `LinearTransformationScene` `i_hat_color=#83C167`, `j_hat_color=#FC6255` |
| **listas de cor** | `VectorField`, `ArrowVectorField`, `StreamLines` `colors=[#236B8E,#83C167,#F7D96F,#FC6255]` · `AnimatedBoundary` `colors=[#29ABCA,#9CDCEB,#236B8E,#736357]` |

**A lição que a tabela ensina e a versão anterior desta skill não dizia: o
parâmetro nem sempre se chama `color`.** `stroke_color`, `fill_color`,
`dot_color`, `label_fill_color`, `background_stroke_color`,
`entries_background_color`, `checkerboard_colors`, `colors`, `i_hat_color` —
qualquer predicado que procure só por `color=` deixa passar 15 dessas classes.

### 10.3 A medição, e a prova em pixel

`VMobject.set_default(color=BLACK)` num processo limpo, e a cor de 28 classes
antes e depois [medido]:

| Alcança (vira preto) | Ignora (mantém o próprio default) |
|---|---|
| `Line`, `DashedLine`, `Arrow`, `Vector`, `Arc`, `Angle`, `Axes`, `NumberLine`, `NumberPlane`, `Brace`, `Underline` | `Circle` `#FC6255` · `Square` `#FFFFFF` · `Rectangle` `#FFFFFF` · `RoundedRectangle` `#FFFFFF` · `Dot` `#FFFFFF` · `Polygon`/`RegularPolygon`/`Triangle`/`Star` `#58C4DD` · `Annulus` `#FFFFFF` · `Sector` `#FFFFFF` · `Ellipse` `#FC6255` · `SurroundingRectangle` `#FFFF00` · `Cross` `#FC6255` · `Sphere` `#29ABCA` · `Cube` `#58C4DD` · `Surface` `#29ABCA` |

**11 de 28.** E entre os 17 ignorados, **seis nascem brancos** — `Square`,
`Rectangle`, `RoundedRectangle`, `Dot`, `Annulus`, `Sector`. Num tema
`whiteboard`, esses seis somem sem erro nenhum.

Repare que `Square`, `Sector` e `Ellipse` **não aparecem** na tabela de §10.2:
elas não hard-codam nada, mas herdam de quem hard-coda (`Square(Rectangle)`,
`Sector(AnnularSector)`, `Ellipse(Circle)`). Pintar a ANCESTRAL resolve a
descendente, porque o `partialmethod` é encontrado pelo `super().__init__()` —
foi assim que a varredura de §11 consertou as sete formas do teste pintando
16 classes.

Prova em pixel. Cena com `Circle(radius=3)` e `Text("some?")`, `-q l` [medido]:

| Comando | pixels com luminância < 128 | menor luminância |
|---|---|---|
| `--background "#FFFFFF"` | **0** de 409.920 | 143 (só franja de antialias) |
| `--theme whiteboard` | 3.815 | 0 |

Zero pixels escuros num quadro inteiro: o texto sumiu, o exit code foi `OK`, e
o círculo que sobrou apareceu **vermelho** porque `Circle` hard-coda `RED`.

### 10.4 Diagnóstico: esta classe obedece ou não?

```python
import inspect
from manim import *

def hard_coda_cor(cls) -> bool:
    """True se o __init__ PRÓPRIO da classe traz um `color=` com default."""
    try:
        sig = inspect.signature(getattr(cls, "_original__init__", cls.__init__))
    except (TypeError, ValueError):
        return False
    p = sig.parameters.get("color")
    return (p is not None
            and p.default is not inspect.Parameter.empty
            and p.default is not None)

hard_coda_cor(Circle)   # True  → precisa de Circle.set_default(...)
hard_coda_cor(Line)     # False → VMobject.set_default(...) já resolve
```

A versão completa, que enxerga os outros nomes de parâmetro de §10.2
(**escrita a partir do índice, não executada nesta rodada**):

```python
def parametros_de_cor(cls) -> dict[str, object]:
    """Todo parâmetro do __init__ próprio cujo default É uma cor."""
    from manim import ManimColor
    try:
        sig = inspect.signature(getattr(cls, "_original__init__", cls.__init__))
    except (TypeError, ValueError):
        return {}
    achados = {}
    for nome, p in sig.parameters.items():
        d = p.default
        if d is inspect.Parameter.empty or d is None:
            continue
        if isinstance(d, ManimColor):
            achados[nome] = d
        elif isinstance(d, (list, tuple)) and d and all(isinstance(x, ManimColor) for x in d):
            achados[nome] = list(d)
    return achados

parametros_de_cor(Surface)
# {'fill_color': …#29ABCA, 'checkerboard_colors': [#29ABCA, #236B8E], 'stroke_color': …#BBBBBB}
```

**Cuidado ao escrever qualquer uma das duas:** comparar o default com
`in (empty, None)` levanta `TypeError: Cannot compare ManimColor with type` —
o `__eq__` do `ManimColor` recusa outros tipos (§3.5). Use `is not`. Foi
exatamente esse o erro que derrubou a primeira versão do `tema.py` desta skill.

---

## 11. A disciplina: uma paleta, um lugar

> **Fronteira.** Esta seção é sobre **cor**: a paleta, a varredura que a aplica
> e a auditoria que a aprova. O `tema.py` como **contrato de projeto** —
> escala tipográfica, pilha de fontes com fallback, tempos e curvas,
> classe-base, número vindo de arquivo — é da skill **`manim-tema-projeto`**.
> As duas convivem no mesmo arquivo; só não escreva a mesma coisa duas vezes.

O padrão vem de um deck em produção (`~/Projects/aulas`), e existe por três
motivos: **deriva visual** (cada cena virando um design diferente), **texto
invisível** (§10) e **retrabalho** (mudar o acento do projeto vira 300 edições).

A regra que vale a pena copiar: **nenhuma cena digita um hex.** Tudo vem de um
nome importado. Confere com uma linha:

```bash
grep -rnE '#[0-9A-Fa-f]{3,8}\b' cenas/*.py | grep -v tema.py   # esperado: nada
```

E o segundo grep, que pega o caso mais comum de todos — a constante nativa
usada direto numa cena de fundo claro:

```bash
grep -rnE '\b(WHITE|YELLOW|BLUE|RED|GREEN|TEAL|GOLD|ORANGE)\b' cenas/*.py | grep -v tema.py
```

### 11.1 A paleta: um nome por PAPEL, não por cor

O que generaliza não são os hex, são os **papéis**. Uma paleta de projeto
precisa exatamente disto, e cada linha tem uma pergunta que ela responde:

| Papel | Pergunta que ele responde | Exemplo auditado (fundo claro) |
|---|---|---|
| `CANVAS` | o fundo | `#FFFFFF` |
| `CANVAS_SUAVE` | a faixa/placa que não é o fundo, mas quase | `#F5F5F7` |
| `TINTA` | texto e traço principais | `#1D1D1F` — 16,83 |
| `TINTA_2` | texto secundário | `#6E6E73` — 5,07 |
| `DIVISORIA` | fio, grade, borda | um cinza claro; **não precisa de 4,5, precisa de 3,0** |
| `ACENTO` | a única cor de destaque | `#0071E3` — 4,70 |
| `VERDE`/`VERMELHO`/`LARANJA` | sinal em gráfico (bom/ruim/atenção) | só para **elemento gráfico**: piso 3,0 |

Três regras que evitam retrabalho:

1. **um acento só.** Dois acentos é o começo de uma paleta de seis, e aí nada
   destaca nada;
2. **cor de sinal não é cor de texto.** Verde e vermelho de gráfico costumam
   viver na faixa 3,0–4,5 (§5.2). Rótulo por cima da barra usa `TINTA`, ou
   `contrasting()`;
3. **a paleta é auditada antes de a primeira cena existir.** `audita()` de §5.2,
   uma vez, e o resultado vai comentado ao lado das constantes — assim ninguém
   troca um hex "só um tiquinho" sem ver a conta.

### 11.2 A varredura que alcança as classes rebeldes

Este módulo foi escrito, renderizado e conferido no PNG [medido]:

```python
"""cores.py — uma cor, um lugar. Importado por TODA cena do projeto."""
from __future__ import annotations

import inspect

from manim import *

# ── paleta (auditada em §5: 16,83 · 4,70 · 6,54 · 5,07 sobre branco) ─────
CANVAS = ManimColor("#FFFFFF")
TINTA = ManimColor("#1D1D1F")
ACENTO = ManimColor("#0071E3")
ALERTA = ManimColor("#B3261E")
APAGADO = ManimColor("#6E6E73")

#: cor SEMÂNTICA, que não pode virar tinta (destaque, marca, sombra)
_POUPADAS: set[type] = {SurroundingRectangle, BackgroundRectangle, Cross}

#: as classes que este módulo alterou — para `limpa_tema()` desfazer
_TOCADAS: set[type] = set()


def _hard_coda_cor(cls: type) -> bool:
    try:
        sig = inspect.signature(getattr(cls, "_original__init__", cls.__init__))
    except (TypeError, ValueError):
        return False
    par = sig.parameters.get("color")
    return (par is not None
            and par.default is not inspect.Parameter.empty
            and par.default is not None)


def aplica_tema(fundo: ManimColor = CANVAS, tinta: ManimColor = TINTA) -> int:
    """Fundo + tinta em TUDO. Devolve quantas classes precisaram de tratamento."""
    config.background_color = fundo

    # 1) alcança quem NÃO hard-coda `color=`: Line, Arrow, Axes, Brace, Angle…
    for cls in (VMobject, Text, MarkupText, Tex, MathTex):
        cls.set_default(color=tinta)
        _TOCADAS.add(cls)

    # 2) quem hard-coda precisa de set_default PRÓPRIO: Circle, Rectangle, Dot…
    vistos: set[type] = set()
    pilha: list[type] = [VMobject]
    while pilha:
        cls = pilha.pop()
        if cls in vistos:
            continue
        vistos.add(cls)
        pilha.extend(cls.__subclasses__())
        if cls in _POUPADAS or not _hard_coda_cor(cls):
            continue
        cls.set_default(color=tinta)
        _TOCADAS.add(cls)
    return len(_TOCADAS)


def limpa_tema() -> None:
    """Desfaz o tema. OBRIGATÓRIO entre temas diferentes no MESMO processo."""
    for cls in _TOCADAS:
        cls.set_default()
    _TOCADAS.clear()
```

Uso, e o resultado medido (`CenaBase` é a de §7.4, que fixa o fundo nos dois
lugares — o `aplica_tema` só cuida da tinta e do `config`):

```python
print("[tema] classes pintadas:", aplica_tema())   # → 16

class Prova(CenaBase):
    def construct(self):
        formas = VGroup(Square(1.2), Circle(0.6), Dot(),
                        Rectangle(width=1.2, height=0.8), Triangle().scale(0.6),
                        Line(LEFT * 0.6, RIGHT * 0.6),
                        Annulus(inner_radius=0.25, outer_radius=0.55)
                        ).arrange(RIGHT, buff=0.45)
        marca = SurroundingRectangle(formas[1])       # segue AMARELO
        self.add(VGroup(formas, marca).arrange(DOWN, buff=0.9))
```

```bash
bin/mx render cena.py Prova --format png --media-dir /tmp/t -q m
```

PNG conferido [medido]: as sete formas em tinta `#1D1D1F`, o
`SurroundingRectangle` preservado em amarelo. Ida e volta também conferida:

```
antes : #FC6255 #FFFFFF #FFFFFF      (Circle, Square, Line)
tema  : #1D1D1F #1D1D1F #1D1D1F      16 classes
limpo : #FC6255 #FFFFFF #FFFFFF      após limpa_tema()
```

### 11.3 O que `_POUPADAS` de fato poupa — e o que ela NÃO alcança

Correção de uma versão anterior desta skill, que dizia que sem `_POUPADAS` a
varredura pintaria as três classes. **Pelo predicado acima, só uma das três
seria pintada** [fonte, assinaturas do índice]:

| Classe | Assinatura | O predicado a pega? |
|---|---|---|
| `SurroundingRectangle` | `color: ParsableManimColor = ManimColor('#FFFF00')` | **sim** — é a que a lista realmente protege |
| `BackgroundRectangle` | `color: ParsableManimColor \| None = None` | **não** — o `is not None` reprova |
| `Cross` | não tem `color`; tem `stroke_color = ManimColor('#FC6255')` | **não** — o predicado procura `color` |

As duas últimas continuam na lista de propósito, e por dois motivos honestos:
`BackgroundRectangle` **deve** seguir `config.background_color`
(§7.4) e pintá-la de tinta transformaria a placa invisível num retângulo
opaco no meio da cena; e assim que alguém trocar o predicado pelo
`parametros_de_cor` de §10.4 — que enxerga `stroke_color` — o `Cross` passa a
ser alcançado, e continuaria precisando ficar de fora.

**O que nenhuma das duas versões alcança**, e por isso vai na sua lista
explícita: `Flash`, `Indicate`, `Circumscribe`, `FocusOn` (são `Animation`, não
`Mobject`, e não estão na árvore de `VMobject.__subclasses__()`), e
`Table`/`Graph`, cujas cores hard-codadas moram em parâmetros com outro nome.
Para animação de ênfase, passe a cor no ponto de uso:
`Indicate(mob, color=ACENTO)`.

### 11.4 Quando NÃO varrer

A varredura é um instrumento cego. Em projeto pequeno, a lista explícita é
melhor:

```python
for cls in (Circle, Square, Rectangle, Dot, Polygon, Arc, Line, Text, MathTex):
    cls.set_default(color=TINTA)
```

**Explícito ganha de varredura sempre que você consegue enumerar.** A varredura
existe para o caso em que a cena importa formas que você não escolheu — e mesmo
aí, o número que ela devolve (16, no teste) merece uma olhada: se subir de
repente, alguém importou uma família nova.

---

## 12. Três vazamentos de tema, todos silenciosos

### 12.1 `set_default` sobrevive ao `tempconfig`

[medido]

```
antes :                       Line() = #FFFFFF
dentro do tempconfig + apply_theme("whiteboard"):
                              Line() = #000000 , config.background_color = #FFFFFF
depois (fora do with):        Line() = #000000 , config.background_color = #000000
```

O `config` volta; **o default de classe não** — ele foi gravado no `__init__`
da classe, que não é config nenhum. Como `render_many` renderiza
sequencialmente no **mesmo processo** (ver `manim-render-api`), uma cena com
`--theme whiteboard` deixa a próxima cena do lote com traço preto — sobre fundo
preto. Vídeo em branco, exit code `OK`.

Defesa: `limpa_tema()` entre cenas de temas diferentes, ou **um processo por
tema** (que é o que `manim-batch-pipeline` faz de qualquer jeito). Lembre de
§10.1: `set_default()` sem argumento zera **todos** os defaults daquela classe,
não só a cor.

### 12.2 `background_opacity` é uma catraca de mão única

[medido]

```
apply_theme("transparent")  → bg #000000, opacity 0.0, extensão .mov
apply_theme("paper")        → bg #F4F1EA, opacity 0.0, extensão .mov   ← VAZOU
```

O tema `transparent` traz `background_opacity: 0.0`; os outros sete **não
trazem a chave**, então `apply_theme` não a toca [fonte: `manimx/presets.py:210-212`].
Pior: o setter de `background_opacity` só chama
`resolve_movie_file_extension(is_transparent=True)` quando o valor é `< 1`
[fonte: `_config/utils.py:1317-1320`] — voltar para `1.0` **não restaura o
`.mp4`**:

```
config.background_opacity = 0.5   → .mov  (+ WARNING "Output format changed to '.mov'")
config.background_opacity = 1.0   → .mov  ← continua
config.transparent = False        → .mp4  ← esta é a que desfaz
```

`config.transparent` é a propriedade que chama `resolve_movie_file_extension`
nos dois sentidos [fonte: `_config/utils.py:1360-1363`]. **Para sair do modo
transparente, escreva `config.transparent = False`, nunca
`background_opacity = 1.0`.**

No caminho do `mx render` isso está contido: o `apply_theme` roda dentro de
`tempconfig`, e o `tempconfig` restaura `background_opacity` e
`movie_file_extension` [medido]. O vazamento morde quem chama `apply_theme`
à mão num script.

### 12.3 Pedir alfa por NOME de cor muta a constante global

Já detalhado em §2.3: `ManimColor("BLUE_D", 0.3)` escreve o alfa **dentro** do
objeto `BLUE_D` exportado pelo módulo [fonte: `core.py:451-455`]. O sintoma
aparece longe da causa e sobrevive a qualquer `tempconfig`, porque não é
config: é o array de uma constante do módulo, no mesmo processo. Peça alfa pelo
objeto (`BLUE_D.opacity(0.3)`), nunca pelo nome.

---

## 13. Timing: mobject de módulo nasce SEM tema

Cena de teste, dois `Line` idênticos, um criado no import e outro no
`construct`, renderizada com `--theme whiteboard` [medido]:

```python
from manim import *
CEDO = Line(LEFT * 3, RIGHT * 3).shift(UP)      # criado NO IMPORT

class Timing(Scene):
    def construct(self):
        TARDE = Line(LEFT * 3, RIGHT * 3).shift(DOWN)
        print("[cor] import:", CEDO.color.to_hex(), " construct:", TARDE.color.to_hex())
```

```
[cor] import: #FFFFFF  construct: #000000
```

O `import` do módulo acontece antes de `apply_theme`; o `construct`, depois
[fonte: `manimx/render.py:419-431`]. Um módulo de tema que exporta **mobjects
prontos** (uma marca d'água, um rodapé, uma moldura) exporta objetos sem tema.
Exporte **fábricas**, não instâncias:

```python
def rodape() -> Text:                    # certo
    return Text("...", color=TINTA)

RODAPE = Text("...", color=TINTA)        # errado: nasce no import
```

A mesma regra pega `BackgroundRectangle` criado no nível do módulo: ele lê
`config.background_color` no construtor (§7.4) e congela o fundo **de antes**
do tema.

---

## 14. Gradientes, sheen e legibilidade sobre fundo ocupado

As seis formas abaixo foram renderizadas juntas num PNG e conferidas a olho
[medido].

```python
Square(2).set_color_by_gradient(BLUE, YELLOW)          # (a)
Square(2).set_fill(color=[BLUE, YELLOW], opacity=1)    # (b)
Square(2).set_fill(BLUE, 1).set_sheen(0.6, UR)         # (c)
Circle(1).set_fill(WHITE, 1).set_colors_by_radial_gradient(ORIGIN, 1, YELLOW, RED)  # (d)
Text("gradiente").set_color_by_gradient(BLUE, YELLOW)  # (e)
VGroup(*quadrados).set_submobject_colors_by_gradient(BLUE, YELLOW)  # (f)
```

Assinaturas conferidas no índice:
`set_color_by_gradient(*colors)` ·
`set_submobject_colors_by_gradient(*colors)` ·
`set_sheen(factor, direction=None, family=True)` ·
`set_colors_by_radial_gradient(center=None, radius=1, inner_color=WHITE, outer_color=BLACK)` ·
`set_submobject_colors_by_radial_gradient(...)` mesma assinatura ·
`set_sheen_direction(direction, family=True)` · `rotate_sheen_direction(angle, axis=OUT, family=True)`.

### 14.1 Existem DOIS gradientes, e eles não são a mesma coisa

**Correção de uma versão anterior desta skill**, que dizia que
`set_color_by_gradient` interpola ao longo dos pontos. No renderer cairo ele
**não** interpola: o corpo inteiro do método é
`self.set_submobject_colors_by_gradient(*colors)` [fonte: `mobject.py:2054-2065`],
e esse distribui **uma cor chapada por family member com pontos**
[fonte: `mobject.py:2082-2093`]. Num `Text`, isso é uma cor por **glifo** —
nunca dentro de uma letra. `set_color_by_gradient` e
`set_submobject_colors_by_gradient` são, no cairo, o mesmo método.

O gradiente **espacial** é outro caminho: passar uma **lista** de cores a
`set_fill`/`set_stroke`. Aí o cairo monta um `cairo.LinearGradient` entre os
dois pontos devolvidos por `get_gradient_start_and_end_points()`
[fonte: `camera/camera.py:788-799`], que são o centro do mobject deslocado pela
**direção do sheen** [fonte: `vectorized_mobject.py:761-771`] — e a direção
padrão do sheen é `[-1, 1, 0]`, ou seja **UL → DR**.

| Você quer | Use | Eixo |
|---|---|---|
| cada item de uma lista/barra com sua cor | `set_submobject_colors_by_gradient(A, B)` | por filho |
| a forma inteira degradê de A para B | `set_fill(color=[A, B], opacity=1)` | espacial, na direção do sheen |
| girar o eixo do degradê | `set_sheen_direction(RIGHT)` antes | |
| volume/brilho, não dado | `set_sheen(fator, direção)` | |

O que a imagem mostrou [medido]:

- **(a) num mobject sem preenchimento, o resultado só aparece no TRAÇO** — e num
  quadrado de 4 px de traço a variação quase não se lê. Para gradiente que
  apareça, combine com `set_fill(..., opacity=1)` ou use (b);
- **(b)** é o caminho direto: `set_fill` aceita **lista** de cores;
- **(c) `set_sheen`** tem sinal, e o sinal importa em tema claro: **fator
  positivo degrada a partir do BRANCO, negativo a partir do PRETO**
  [fonte: `vectorized_mobject.py:725-727`]. Num canvas branco, `set_sheen(0.6)`
  faz o objeto desbotar contra o fundo; o que você quer é `set_sheen(-0.3, DR)`;
- **(f)** é o que você quer numa `VGroup` de barras ou de itens de lista.

`Text(gradient=[A, B])` e `t2g` são ainda um terceiro caminho: eles pedem ao
Pango uma cor **por caractere**, via `color_gradient(self.gradient, len(self.text))`
[fonte: `text_mobject.py:748-756`] — decidido antes de o SVG existir, e por isso
entra no hash do cache. Assunto de `manim-text-latex`.

### 14.2 O halo que não funciona, e o prato que funciona

`set_background_stroke(**kwargs)` (que é `set_stroke(**kwargs, background=True)`)
existe e o cairo o desenha. Mas foi testado sobre uma grade de linhas cinza,
com texto de `font_size=40` [medido]:

- `width=8`: **invisível**, a grade continuou atravessando as letras;
- `width=20`: aparece, mas o traço é aplicado ao contorno de **cada glifo** —
  as letras engordam, o miolo do `o` e do `e` fecha, e a grade ainda passa nos
  vãos entre as palavras. O texto sai deformado.

E há um detalhe que garante o fracasso em tema claro: `background_stroke_color`
nasce **`#000000`** [fonte: assinatura de `VMobject`]. Um halo preto atrás de
texto preto não faz nada; num tema escuro ele é invisível por ser da cor do
fundo. Se for usar, passe a cor explícita.

A técnica que funciona é a **placa opaca da cor do fundo, atrás do bloco
inteiro**:

```python
texto = Text("tokens", color=TINTA)
prato = Rectangle(
    width=texto.width + 0.30,
    height=texto.height + 0.25,
    fill_color=CANVAS,          # a MESMA cor do fundo: o prato não aparece,
    fill_opacity=1.0,           # ele só apaga o que está atrás das letras
    stroke_width=0.0,
).move_to(texto)

grupo = VGroup(prato, texto)    # prato ANTES: a ordem do VGroup é a de desenho
```

Folga de ~0,2 a 0,3 em volta, e o prato **antes** do texto no `VGroup`. No PNG
conferido, a grade fica cortada limpa atrás da frase inteira [medido].

**O Manim já traz esse prato pronto**, e ele é ciente do tema:

```python
texto.add_background_rectangle(color=CANVAS, opacity=1.0, buff=0.12)
```

`Mobject.add_background_rectangle(color=None, opacity=0.75, **kwargs)` constrói
um `BackgroundRectangle`, e com `color=None` ele assume `config.background_color`
[fonte: `geometry/shape_matchers.py:118-119`]. Duas ressalvas antes de trocar o
prato manual por ele:

1. o default de opacidade é **0,75**, não 1,0 — a grade continua aparecendo,
   fantasma, atrás das letras;
2. `BackgroundRectangle.set_style` **ignora tudo menos `fill_opacity` e força
   preto** [fonte: `shape_matchers.py:136-144`]. Qualquer `match_style` ou
   `set_style` posterior (inclusive dentro de um `Transform` que copie estilo)
   transforma a placa num retângulo **preto** opaco. Em tema claro, isso é uma
   tarja no meio do slide. Onde houver `Transform` por perto, prefira o
   `Rectangle` manual.

---

## 15. As sete opacidades independentes

"Deixa translúcido" pode significar sete coisas diferentes, e elas se
multiplicam entre si:

| # | Onde | Como se escreve | Alcance |
|---|---|---|---|
| 1 | alfa **da cor** | `ACENTO.opacity(0.3)` | viaja junto com a cor; `interpolate_color` preserva, `color_gradient`/`average_color` descartam (§4) |
| 2 | preenchimento | `set_fill(opacity=0.3)` / `fill_opacity=` | só o interior |
| 3 | traço | `set_stroke(opacity=0.3)` | só a borda |
| 4 | traço de fundo | `set_background_stroke(opacity=…)` | o halo de §14.2 |
| 5 | tudo do mobject | `set_opacity(0.3)` | escreve 2, 3 e 4 de uma vez [fonte: `vectorized_mobject.py:478-482`] |
| 6 | esmaecer composto | `fade(0.5)` | **multiplica** as três; compõe a cada chamada (§9.6) |
| 7 | o **fundo da cena** | `config.background_opacity` / `-t` | é a catraca de §12.2 |

Três notas de projeto:

- **`fill_opacity` e `stroke_opacity` não são o mesmo botão.** Uma forma com
  `set_opacity(0.3)` fica com borda fraca *e* miolo fraco; para um destaque
  legível o que se quer quase sempre é borda cheia e miolo a 15%:
  `.set_stroke(ACENTO, 6).set_fill(ACENTO, 0.15)`;
- **sobreposição de translúcidos compõe.** Com `fill_opacity=0.5` nos dois, a
  interseção de um azul e um vermelho mediu `(152,110,135)` [medido] — útil para
  diagrama de Venn, e **péssimo para dado quantitativo**, porque a cor da
  interseção não pertence a nenhuma das duas séries e ninguém consegue
  associá-la a uma legenda. Para região composta de verdade, use os booleanos
  de forma (`Union`, `Intersection`, `Difference`, `Exclusion`) —
  `manim-mobjects-customizados`;
- **quem tapa quem é ordem e `z_index`, não opacidade.** Sem `z_index`, vale a
  ordem de adição; um `Circle` com `set_z_index(-1)` foi corretamente desenhado
  atrás de um `Square` adicionado antes dele [medido]. O assunto de camada e
  ordenação é de `manim-layout-posicionamento`; aqui só interessa que
  **translúcido não substitui camada**.

---

## 16. Transparência (canal alfa) para editor de vídeo

```bash
bin/mx render cena.py Demo -t -q h              # = --codec transparent
```

`-t` é `--transparent` e é uma flag booleana [fonte: `cli/render/render_options.py:214-218`].

Medições nesta máquina [medido]:

| Fato | Como foi visto |
|---|---|
| container vira `.mov`, codec `qtrle`, `pix_fmt=argb` | `ffprobe -show_entries stream=codec_name,pix_fmt` |
| o alfa é **premultiplicado** | frame com alfa 216: RGB gravado `(74,166,187)`; dividido por 216/255 dá `(88,196,221)` = o BLUE original. Em opacidade cheia (alfa 255) o RGB sai exato |
| `-t` e `--codec transparent` são o mesmo caminho | ambos saem `qtrle` em `.mov` |
| **NVENC não codifica alfa** | a camada `manimx` detecta e mantém `qtrle`, com aviso no log. Não é falha |
| **`--codec webm` não tem alfa**, nem com `-t` | `ffprobe` devolveu `vp9,yuv420p` nas duas tentativas |
| custo de tamanho | cena de 30 discos coloridos, 1 s a 1080p60: `.mov` qtrle **2.799.765 B (2,7 MiB/s)** contra `.mp4` h264_nvenc **491.096 B (0,47 MiB/s)** — 5,7× |

**Se o NLE mostrar franja escura nas bordas, importe como alfa
PREMULTIPLICADO**, não "straight". É a causa nº 1 de "o Manim exportou errado".

Duas consequências de projeto, herdadas de deck em produção:

- **o primeiro frame de uma cena costuma ser vazio** (alfa 0 em 100% do quadro,
  medido) — se você extrair pôster, extraia o **último** frame
  (`ffmpeg -sseof -1 -i x.mov -update 1 x.png`, **sem** `-frames:v 1`);
- **fundo transparente não conserta cor invisível.** Alfa 0 no fundo continua
  deixando texto branco em cima de um NLE de timeline branca. Aplique o tema
  explícito antes.

Para alfa **parcial** no fundo: `config.background_opacity = 0.5` — e leia
§12.2 antes, porque isso é uma catraca. O valor é grampeado em [0, 1]
[fonte: `_config/utils.py:1319` — `_set_between`], então `2.0` vira `1.0` sem
reclamar.

---

## 17. Fundo em imagem, e cor em 3D

```python
class Demo(Scene):
    def construct(self):
        bg = ImageMobject("assets/fundo.jpg")
        bg.scale_to_fit_height(config.frame_height)
        self.add(bg)                    # adicionar primeiro já o põe atrás
        self.play(Create(Circle()))
```

`ImageMobject(filename_or_array, scale_to_resolution=1080, invert=False, image_mode='RGBA')`.
Não é `VMobject`: não aceita `set_stroke`/`set_fill`, e **não entra em `VGroup`** —
a mensagem exata é `TypeError: Only values of type VMobject can be added as
submobjects of VGroup, but the value ImageMobject (at index 0 of parameter 0) is
of type ImageMobject.` [medido]. Use `Group`.

Há um segundo caminho, pela **câmera**: `Camera(background_image=…)`, ou
`self.camera.background_image = "x.png"` seguido de
`self.camera.init_background()` — aí a imagem substitui a cor de fundo no array
que a câmera pinta [fonte: `camera/camera.py:283-292`]. **não verificado por
execução.** Caminho de asset, cache de SVG e `register_font` são de
`manim-svg-imagens`.

Também existe `VMobject.color_using_background_image(background_image)`, que usa
uma imagem como *preenchimento* de uma forma vetorial. O corpo é curto e revela
o efeito colateral: ele faz `self.set_color(WHITE)` e propaga para os
submobjects [fonte: `vectorized_mobject.py:773-778`] — ou seja, **descarta a cor
que o objeto tinha**. Aplique-o antes de qualquer estilo, nunca depois.
**não verificado por execução.**

Em 3D, a cor entra por parâmetro próprio, e nenhum deles se chama `color`:

```
Surface(..., fill_color=#29ABCA, fill_opacity=1.0,
        checkerboard_colors=[#29ABCA, #236B8E],
        stroke_color=#BBBBBB, stroke_width=0.5)
```

`checkerboard_colors=False` desliga o xadrez e usa `fill_color` chapado.
`set_shade_in_3d(value=True, z_index_as_group=False)` liga o sombreamento por
normal, que internamente usa `get_shaded_rgb` — cuidado: essa função devolve
RGB **sem clamp** (medido `[0.47, 0.87, 1.17]`, com o canal azul acima de 1,0)
[fonte: `core.py:1628-1631` — `shaded_rgb = rgb + light`, sem `np.clip`]. Luz,
câmera e material: `manim-3d-camera`.

---

## 18. Diagnóstico

| Sintoma | Causa provável | Comando que decide |
|---|---|---|
| forma invisível em fundo claro | classe que hard-coda `color=WHITE` e ignora `set_default` (§10.2) | `python -c "from manim import *; print(Square().color.to_hex())"` |
| forma invisível, qualquer fundo | `set_fill` sem `opacity` (padrão 0) | `print(mob.get_fill_opacity())` |
| tracejado invisível | `DashedVMobject` descartou o seu `color=` (§9.7) | estilize o mobject **antes** de embrulhar |
| halo/contorno não aparece | `background_stroke_color` nasce preto (§14.2) | passe a cor explícita, ou use o prato |
| tudo branco em fundo branco | usou `--background` em vez de `--theme`; ou faltou `set_default` | renderize PNG e conte tinta: `(np.array(Image.open(p).convert('L')) < 128).sum()` |
| o fundo não mudou | `config.background_color` escrito **dentro** do `construct` (§7.4) | leia o pixel `(5,5)` do PNG |
| pedi `--theme` e o fundo continuou o antigo | a cena-base escreve o fundo no `setup()`, que roda **depois** do tema (§8) | `grep -n "background_color" cena.py tema.py` |
| passei `--background` e `--theme` e o fundo é do tema | é o esperado: o tema roda depois (§7.5) | tire um dos dois |
| `ValueError: Color X not found` | hex sem `#`/`0x`, ou nome que não está nas 89 nativas (§6.2) | `ManimColor("#" + x)` ou `XKCD.X` |
| `FileNotFoundError ... --config_file` | usou `-c COR`; `-c` é `--config_file` | `bin/manim render --help \| grep config_file` |
| `TypeError: Cannot compare ManimColor with type` | comparou cor com `in (...)`/`==` contra outro tipo (§3.5) | troque por `is`/`is not`, ou compare `to_hex()` |
| `AttributeError: 'NoneType' object has no attribute 'to_hex'` | `mob.color` devolveu `None`: fill e stroke ambos a opacidade 0 (§9.4) | `print(mob.get_fill_opacity(), mob.get_stroke_opacity())` |
| `TypeError: set_color() got an unexpected keyword argument 'alpha'` | `alpha=` só existe no `Mobject.set_color`, e lá é ignorado (§9.1) | use `set_fill(opacity=…)` |
| o vídeo saiu `.mov` sem eu pedir | alguém mexeu em `background_opacity` (§12.2) | `print(config.transparent, config.movie_file_extension)` |
| a 2ª cena do lote saiu preta no preto | `set_default` vazou do render anterior (§12.1) | `limpa_tema()` ou um processo por tema |
| uma cor da paleta ficou translúcida sozinha | alguém pediu alfa por NOME e mutou a constante (§2.3, §12.3) | `grep -nE 'ManimColor\("[A-Z_]+", *[0-9.]' .` |
| o tema não pegou naquele mobject | ele foi criado no **import** do módulo (§13) | mova para dentro de `construct`, ou exporte fábrica |
| a cor do gradiente saiu errada com 1 série | `color_gradient(..., 1)` devolve a **última** cor (§4.1) | trate `length == 1` na mão |
| o degradê não aparece dentro da forma | `set_color_by_gradient` é por filho; o espacial é `set_fill(color=[a,b])` (§14.1) | |
| o objeto desbotou ao aplicar sheen | `set_sheen` positivo degrada a partir do BRANCO (§14.1) | use fator negativo em tema claro |
| franja escura no NLE | alfa premultiplicado importado como straight (§16) | troque o modo de interpretação no NLE |
| `mob.color` não bate com a tela | `mob` é container, e `.color` é derivado (§9.4) | `mob.family_members_with_points()[0].get_fill_color()` |
| a cor mudou depois de um `from ... import *` | colisão de nome entre paletas (§6.1) | `grep -n "import \*" cena.py` |
| um hex saiu com 7+ dígitos | soma/multiplicação de cor estourou 1,0, sem clamp (§3.5) | | 
| o logo SVG não pegou o tema | `SVGMobject` passa `color=None` explícito (§9.5) | `.set_color(TINTA)` depois de carregar |

---

## 19. Descoberta: ache a cor sem chutar

Custo medido: `mx find` 0,23 s, `mx show` 0,05 s, `mx presets` 0,06 s. Não há
desculpa de tempo para inventar um nome.

```bash
bin/mx show ManimColor                       # os 25 métodos
bin/mx find BLOODRED --kind constant         # constant BLOODRED  utils/color  ManimColor('#980002')
bin/mx find contrasting                      # acha a CLASSE que tem o método
bin/mx presets                               # os 8 temas com o hex
bin/mx presets --json | jq .themes.paper     # {"background_color":"#F4F1EA", ...}
```

Índice bruto — 4.900 linhas de constante em `api/manim-ce-index.tsv` (colunas:
`kind name category signature module doc`):

```bash
cd ~/Projects/manim

# toda a família TEAL, com o hex — repare nos TRÊS TEAL de paletas diferentes
awk -F'\t' '$1=="constant" && $2 ~ /^TEAL/ {print $2"\t"$4}' api/manim-ce-index.tsv | sort -u

# só as 89 nativas (as outras vivem em XKCD/X11/…)
grep -cE '^[A-Z_0-9]+ = ManimColor' .venv/lib/python3.12/site-packages/manim/utils/color/manim_colors.py

# toda função/classe de cor que não seja constante — as 19 de utils/color
awk -F'\t' '$3=="utils/color" && $1!="constant" {print $1"\t"$2"\t"$4}' api/manim-ce-index.tsv | sort -u

# TODA classe que hard-coda uma cor na assinatura (as 52 de §10.2)
awk -F'\t' '$1=="class" && $4 ~ /ManimColor\(/ {print $2"\t"$3}' api/manim-ce-index.tsv | sort -u

# todo método de VMobject que mexe em cor, com a assinatura
awk -F'\t' '$1=="VMobject" && $5==0 && $2 ~ /color|fill|stroke|opacity|sheen|style/ {print $2"\t"$6}' \
  api/manim-ce-methods.tsv | sort -u

# quem DEFINE um método (Mobject ou VMobject?) — a coluna 4 é `defined_in`
awk -F'\t' '$2=="set_opacity" {print $4}' api/manim-ce-methods.tsv | sort -u
```

---

## 20. O ciclo que pega defeito de cor

Renderizar e conferir o exit code **não pega nada** aqui: texto branco no
branco, forma com `fill_opacity=0`, contraste ruim e sobreposição saem todos
com `OK`. Três defeitos desta auditoria só apareceram ao **olhar o PNG**.

```bash
# 1. um frame, rápido, no cairo (opengl é ~100x mais lento em --format png)
bin/mx render cena.py Cena --format png --media-dir /tmp/t -q m

# 2. OLHE. Obrigatório.
#    (o caminho vem em `image_file`, NÃO em `output_file`, que é null em png —
#     ver manim-render-api)

# 3. e meça, quando o olho não basta:
python - <<'EOF'
from PIL import Image; import numpy as np
a = np.array(Image.open("/tmp/t/images/cena/Cena_ManimCE_v0.21.0.png").convert("L"))
print("tinta escura (<128):", int((a < 128).sum()), "de", a.size, "  min:", a.min())
EOF
```

Um quadro com **zero** pixels abaixo de 128 num tema claro é um quadro vazio,
por mais que a cena tenha 40 mobjects. Foi assim que a medição de §10.3 foi
feita.

Três conferências de cor que rodam **sem render**, e por isso cabem num
pre-commit:

```python
# 1. a paleta ainda passa no contraste?
assert razao(CANVAS, TINTA)  >= 4.5
assert razao(CANVAS, ACENTO) >= 4.5
assert razao(CANVAS, DIVISORIA) >= 3.0

# 2. nenhuma classe da cena ficou com a cor de fábrica
for cls in (Circle, Square, Dot, Rectangle):
    assert cls().color.to_hex().upper() == TINTA.to_hex().upper(), cls.__name__

# 3. nenhum hex literal fora do módulo de cor
#    grep -rnE '#[0-9A-Fa-f]{3,8}\b' cenas/*.py | grep -v cores.py
```

O ciclo completo de verificação visual — quando olhar, o que medir, como
comparar dois frames — é de **`manim-verificacao-visual`**. O recorte acima é
só a parte que decide se a COR está errada.

---

## 21. Receita: tema claro do zero, na ordem

Para quando o pedido é "põe lousa branca" e você quer acabar em um render, não
em cinco:

1. **escolha a paleta por papel** (§11.1) e **audite** com `razao()` (§5.2).
   Nenhuma constante nativa sobrevive a fundo branco (§5.3): você vai escrever
   hex novo;
2. **fixe o fundo nos dois lugares**, no `setup()` da cena-base (§7.4);
3. **pinte as classes**: `VMobject`, `Text`, `MarkupText`, `Tex`, `MathTex`,
   mais a varredura ou a lista explícita (§11.2, §11.4);
4. **passe a cor à mão** nas quatro que a varredura não alcança —
   `Indicate`, `Flash`, `Circumscribe`, `FocusOn` (§11.3) — e revise
   `Table`/`Graph` se a cena os usar;
5. **estilize antes de embrulhar** qualquer `DashedVMobject` (§9.7) e antes de
   `color_using_background_image` (§17);
6. **renderize um PNG e olhe** (§20). Conte a tinta escura: zero é quadro
   vazio;
7. se o projeto tiver dois temas, **limpe entre eles** (`limpa_tema()`) ou use
   um processo por tema (§12.1).

---

## 22. Fronteiras — o que NÃO está aqui

| Você quer | Skill |
|---|---|
| escolher entre `Text`/`Tex`/`MathTex`/`Typst`; colorir **trechos** com `t2c`, `t2g`, `set_color_by_tex`, `{{ }}`; nitidez de glifo | `manim-text-latex` |
| posicionar, agrupar, medir, `VGroup` × `Group`, árvore de submobjects | `manim-mobjects` |
| enquadrar, margem, `z_index`, ordem de camada, "cabe na tela?" | `manim-layout-posicionamento` |
| animar a troca de cor (`FadeToColor`, `mob.animate.set_color`, `Indicate`, `Flash`, `Circumscribe`) | `manim-animations` (o catálogo). **Ênfase e anotação em profundidade não têm skill dona** — buraco declarado |
| o `tema.py` como CONTRATO: fonte com fallback, escala tipográfica, tempos e curvas, classe-base, número vindo de JSON | `manim-tema-projeto` (ela defere a cor a esta) |
| `rate_func`, `run_time`, `lag_ratio`, ritmo | `manim-composicao-ritmo` |
| codec, NVENC, `.mov` × `.mp4`, tamanho de arquivo, tempo de encode | `manim-gpu-encoding` |
| `output_file` × `image_file`, `tempconfig`, `render_scene`, iterar rápido | `manim-render-api` |
| olhar o PNG, comparar frames, a métrica direcional | `manim-verificacao-visual` |
| lote de cenas em paralelo e o vazamento de `set_default` entre elas | `manim-batch-pipeline` |
| cache de LaTeX/SVG/partial movie, e o custo de recompilar texto colorido | `manim-performance-cache` |
| luz, normal, material, `set_shade_in_3d`, câmera 3D | `manim-3d-camera` |
| `SVGMobject`, `ImageMobject`, `register_font`, caminho de asset | `manim-svg-imagens` |
| cor de eixo, de barra, de série num gráfico | `manim-graphs-plots` |
| `Table`/`Matrix` e as cores hard-codadas delas | `manim-tabelas-matrizes` |
| `Graph`/`DiGraph` e o `label_fill_color` | `manim-grafos-redes` |
| booleanos de forma para região composta em vez de opacidade; Mobject próprio | `manim-mobjects-customizados` |
| cena em partes, e por que cor aleatória quebra a emenda | `manim-presentation-parts` |
| de qual `Scene` herdar, seções | `manim-cenas-secoes` |
| o erro não é de cor, é de render/ambiente | `manim-troubleshooting` |
| achar nome, assinatura ou kwarg de qualquer símbolo | `manim-api-discovery` |

### Onde esta skill para, e ninguém assume

- **os 12 mobjects `OpenGL*` que hard-codam cor — mais o `DotCloud`, que é
  OpenGL sem o prefixo no nome** (§10.2) — só importam com `--renderer opengl`,
  que não é o caminho de produção aqui. Buraco declarado;
- **ênfase e anotação** (`Flash`, `Indicate`, `Circumscribe`, `FocusOn`,
  `Brace*`, `SurroundingRectangle`, `Underline`, `Cross`) não têm skill dona. As
  cores hard-codadas delas estão em §10.2; o resto é `manim-animations`;
- **`VectorField`/`StreamLines`** e a paleta de quatro cores que elas trazem:
  sem skill. A lista está em §10.2;
- **`ManimConfig` inteiro** (precedência, `config_file_paths`, `parse_theme` —
  que é o tema do **logger rich**, não da cena) não tem skill dona;
  `manim-project` §5 cobre o essencial.
