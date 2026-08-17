---
name: manim-color-theming
description: >-
  Cor no Manim — cor de fundo da cena, cor de traço e preenchimento de
  Mobjects, gradientes, opacidade, transparência com canal alfa, paleta
  nativa (BLUE_D, RED_A, XKCD…), temas claro/escuro e defaults globais.
  Use ao mudar fundo, deixar o vídeo com lousa branca, colorir formas,
  aplicar gradiente, exportar com alfa para editor de vídeo, ou quando a
  cor sair errada/invisível. Contém as mudanças da ManimCE 0.21 que
  invalidam tutoriais antigos (o flag `--background_color` foi REMOVIDO).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Cor, fundo e temas

## Correções à documentação que circula por aí

Verificado nesta instalação (ManimCE 0.21.0):

| Afirmação comum | Realidade na 0.21 |
|---|---|
| `manim -c WHITE arq.py Cena` muda o fundo | **Falso.** `-c` agora é `--config_file`. Passar uma cor dá `FileNotFoundError`. |
| Existe `--background_color` na CLI | **Falso.** O flag foi removido. `manim render --help` não o lista. |
| Hex de 3 dígitos (`#F00`) quebra o parser | **Falso.** `ManimColor("#F00")` resolve para `#FF0000`. |
| O fundo padrão do ManimGL é preto | **Falso.** O master usa `#333333`. |

O que **de fato** quebra: hex **sem** o `#` (`"F00"` → `ValueError`) e hex
com número ímpar/errado de dígitos (`"#12345"`).

## Mudar a cor de fundo — os três caminhos que funcionam

Todos verificados lendo o pixel do canto da imagem renderizada.

### 1. `manim.cfg` — vale para o projeto inteiro

```ini
[CLI]
background_color = #FF0000
```

### 2. `config` no topo do script — vale para o arquivo

```python
from manim import *
config.background_color = "#00FF00"

class Demo(Scene):
    def construct(self): ...
```

### 3. `self.camera` — vale só para aquela cena

```python
class Demo(Scene):
    def construct(self):
        self.camera.background_color = "#0000FF"
```

### 4. Pela camada `manimx` (recomendado para agentes)

```bash
bin/mx render cena.py Demo --background "#FFFFFF"
bin/mx render cena.py Demo --theme whiteboard
```

```python
from manimx.render import render_file
render_file("cena.py", "Demo", background_color="#FFFFFF")
```

## Temas prontos

```bash
bin/mx presets     # lista todos com o hex
```

| Tema | Fundo | Uso |
|---|---|---|
| `3b1b` | `#000000` | padrão do canal |
| `whiteboard` | `#FFFFFF` | corporativo, artigo, slide claro |
| `paper` | `#F4F1EA` | papel creme, bom para impressão |
| `slate` | `#1E1E2E` | escuro suave (Catppuccin) |
| `solarized-dark` / `solarized-light` | | |
| `nord` | `#2E3440` | |
| `transparent` | alfa 0 | composição em NLE |

```python
from manimx import apply_theme
apply_theme("whiteboard")   # ANTES de instanciar qualquer Mobject
```

`apply_theme` faz duas coisas: muda `config.background_color` **e** roda
`set_default(color=...)` em `Text`, `Tex`, `MathTex` e `VMobject`. Sem a
segunda parte, fundo branco + traço branco = tela em branco.

## Fundo claro: a armadilha do traço branco

Mobjects nascem com traço claro. Em fundo branco eles somem. Corrija com
defaults globais, no topo do arquivo:

```python
from manim import *
config.background_color = WHITE

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK)
MathTex.set_default(color=BLACK)
VMobject.set_default(color=BLACK)

class Demo(Scene):
    def construct(self):
        self.add(Circle(), Text("agora aparece"))
```

`set_default` é `classmethod` e afeta **todas as instâncias criadas depois**.
Chame antes de qualquer construtor.

## Colorir um Mobject

| Método | Efeito | Assinatura |
|---|---|---|
| `.set_color(c)` | traço **e** preenchimento | `(color, family=True)` |
| `.set_stroke(color=, width=, opacity=)` | só a borda | também `background=False` |
| `.set_fill(color=, opacity=)` | só o interior | `opacity` é obrigatória para aparecer |
| `.set_color_by_gradient(*cores)` | gradiente ao longo do mobject | |
| `.set_opacity(x)` | traço + preenchimento juntos | |

```python
c = (Circle(radius=1.5)
     .set_stroke(BLUE_D, width=6)
     .set_fill(BLUE_E, opacity=0.4))
```

**`set_fill` sem `opacity` não mostra nada** — o padrão de preenchimento é
0. Este é o erro de cor mais comum.

`family=True` (padrão) propaga para os submobjects. Use `family=False` para
colorir só o objeto pai — importante em `VGroup`, `Axes` e `MathTex`.

## A paleta

`from manim import *` traz centenas de constantes. Famílias com sufixo de
luminosidade `_A` (mais claro) → `_E` (mais escuro), com `_C` no meio:

```
BLUE_A BLUE_B BLUE_C BLUE_D BLUE_E    (idem TEAL, GREEN, YELLOW, GOLD,
                                       RED, MAROON, PURPLE, GREY)
PURE_RED PURE_GREEN PURE_BLUE          saturação total
WHITE BLACK GREY_BROWN DARK_BROWN LIGHT_BROWN PINK LIGHT_PINK ORANGE
```

O 3b1b usa `BLUE_D`/`BLUE_E` como azul de assinatura e `RED_A`…`RED_E` para
destaque.

Além dessas há paletas completas em submódulos: `XKCD`, `X11`, `AS2700`,
`BS381`, `DVIPSNAMES`, `SVGNAMES`.

```python
from manim.utils.color import XKCD
dot = Dot(color=XKCD.BLOODRED)
```

Ache qualquer cor:

```bash
bin/mx find BLOODRED --kind constant
awk -F'\t' '$1=="constant" && $2 ~ /^TEAL/ {print $2"\t"$4}' api/manim-ce-index.tsv | sort -u
```

## Formatos de cor aceitos

```python
Circle(color=BLUE_D)              # constante
Circle(color="#3B82F6")           # hex 6 dígitos  (preferido)
Circle(color="#38F")              # hex 3 dígitos  (funciona na 0.21)
Circle(color=ManimColor("#3B82F6"))
Circle(color=ManimColor.from_rgb((59, 130, 246)))
```

Sempre inclua o `#`. `"3B82F6"` sem prefixo é interpretado como *nome* de
cor e levanta `ValueError`.

## Gradientes

```python
# ao longo de um mobject
Text("gradiente").set_color_by_gradient(BLUE, GREEN, YELLOW)

# no construtor de Text, por palavra
Text("Olá Mundo", t2g={"Mundo": (RED, BLUE)})

# preenchimento com dois pontos
sq = Square().set_fill(color=[RED, BLUE], opacity=1)
```

## Transparência (canal alfa) para editor de vídeo

```bash
bin/mx render cena.py Demo -t -q h          # gera .mov com qtrle RGBA
```

Pontos que importam:

- **NVENC não codifica alfa.** A camada `manimx` detecta `-t` e mantém
  `qtrle` de propósito, avisando no log. Não é falha.
- O container vira `.mov`, não `.mp4`.
- `qtrle` é sem perdas → arquivos grandes. Espere centenas de MiB por minuto.
- Para alfa parcial em vez de total: `config.background_opacity = 0.5`.

Fundo transparente com objetos visíveis exige que os objetos **não** sejam
brancos-em-branco; aplique um tema explícito antes.

## Imagem de fundo em vez de cor chapada

```python
class Demo(Scene):
    def construct(self):
        bg = ImageMobject("assets/fundo.jpg")
        bg.scale_to_fit_height(config.frame_height)
        self.add(bg)                 # adicionar primeiro já o põe atrás
        # ou, se já houver outros objetos:
        self.bring_to_back(bg)
        self.play(Create(Circle()))
```

`ImageMobject` não é `VMobject`: não aceita `set_stroke`/`set_fill` e não
entra em `VGroup` (use `Group`).

## Ordem de desenho (eixo Z)

```python
self.bring_to_front(mob)
self.bring_to_back(mob)
mob.set_z_index(5)          # maior = mais na frente
```

## Diagnóstico rápido

| Sintoma | Causa provável |
|---|---|
| Forma invisível | `set_fill` sem `opacity`, ou cor igual ao fundo |
| Tudo branco em fundo branco | faltou `set_default(color=...)` |
| `ValueError: Color X not found` | faltou o `#` no hex |
| `FileNotFoundError` ao usar `-c` | `-c` é `--config_file` na 0.21 |
| Cor só no contorno de uma fórmula | use `set_color_by_tex` (ver `manim-text-latex`) |
| Alfa não aparece no editor | o arquivo virou `.mp4`; confirme que saiu `.mov` |
