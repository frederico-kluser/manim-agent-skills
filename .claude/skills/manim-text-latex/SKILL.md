---
name: manim-text-latex
description: >-
  Texto e matemática no Manim — as quatro classes (Text, MarkupText, Tex,
  MathTex), quando usar cada uma, e como colorir/animar PARTES de uma
  palavra ou de uma fórmula. Use ao escrever qualquer texto ou equação, ao
  destacar um termo dentro de uma expressão, ao animar a transformação de
  uma equação em outra, ao trocar fonte, ou quando o LaTeX falhar em
  compilar. Cobre t2c/t2g/t2w, isolamento com chaves duplas, ligaduras
  tipográficas, e o setup de TinyTeX desta máquina.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Texto e LaTeX

## Qual classe usar

| Classe | Motor | Use quando |
|---|---|---|
| `Text` | Pango (sem LaTeX) | texto comum, rótulos, títulos. **Rápido.** |
| `MarkupText` | Pango + markup tipo HTML | texto comum com formatação rica por trecho |
| `Tex` | LaTeX, modo texto | prosa com matemática embutida |
| `MathTex` | LaTeX, modo `align*` | fórmulas puras |

`Text` não precisa de LaTeX e compila em milissegundos. `Tex`/`MathTex`
disparam um `latex` + `dvisvgm` por string nova. **Prefira `Text` para
qualquer coisa que não seja matemática.**

## Raw strings são obrigatórias no LaTeX

```python
MathTex(r"\int_0^1 x^2\,dx = \frac{1}{3}")    # certo
MathTex("\int_0^1 x^2")                        # ERRADO: \i, \f viram escapes
```

Sempre `r"..."`. Sem exceção.

## Colorir partes de um `Text`

```python
Text("Olá Mundo", t2c={"Mundo": RED})            # por conteúdo
Text("Derivada", t2c={"[1:4]": RED})             # por fatia de índice
Text("a b c", t2g={"b": (RED, BLUE)})            # gradiente no trecho
Text("negrito", t2w={"negrito": BOLD})           # peso
Text("itálico", t2s={"itálico": ITALIC})         # inclinação
Text("outra fonte", t2f={"outra": "Consolas"})   # fonte por trecho
```

Ambos funcionam na 0.21: chave por **conteúdo** (`"Mundo"`) e por **fatia**
(`"[1:4]"`, semântica de slice do Python — inclui 1, exclui 4).

### O problema das ligaduras

Fontes com ligaduras fundem pares como `fi`, `fl`, `ff` num único glifo.
Colorir por índice então pinta o glifo inteiro, não a letra. Solução:

```python
Text("eficiente", t2c={"[0:2]": RED}, disable_ligatures=True)
```

Custo: perde-se a tipografia bonita da fonte. Use só quando precisar de
controle por caractere.

### `MarkupText` — a saída melhor

Evita o problema de índice por completo, marcando por conteúdo:

```python
MarkupText(
    f'A constante <span fgcolor="{RED}">desaparece</span> na derivada',
    color=WHITE,
)
MarkupText('<b>negrito</b> e <i>itálico</i> e <u>sublinhado</u>')
MarkupText('<span size="x-large">grande</span>')
```

Aceita markup do Pango: `<b> <i> <u> <s> <sub> <sup> <span>` com atributos
`fgcolor`, `bgcolor`, `size`, `font_family`, `weight`, `underline`.

## Colorir partes de uma fórmula — três caminhos

### 1. `tex_to_color_map` — por conteúdo, no construtor

```python
MathTex(r"E = mc^2", tex_to_color_map={"E": BLUE_E, "m": GREEN_C})
```

Simples, mas casa **qualquer ocorrência** da substring — inclusive dentro
de comandos. `{"e": RED}` pinta o `e` de `\frac`. Cuidado com letras soltas.

### 2. Chaves duplas `{{ }}` + `set_color_by_tex` — o mais confiável

As chaves duplas instruem o Manim a **quebrar a fórmula em submobjects
separados** antes de renderizar:

```python
eq = MathTex(r"{{a^2}} + {{b^2}} = c^2")
# verificado: vira 4 submobjects -> ['a^2', ' + ', 'b^2', ' = c^2']
eq.set_color_by_tex("a^2", BLUE_D)
```

Sem as chaves duplas, `MathTex(r"a^2 + b^2 = c^2")` é **1 submobject só** e
não há o que colorir separadamente.

Isso também é a base de `TransformMatchingTex` (abaixo).

### 3. Por índice — quando você precisa de um símbolo específico

Descubra os índices **visualmente**, não por tentativa:

```python
class Debug(Scene):
    def construct(self):
        eq = MathTex(r"\frac{d}{dx} f(x) = \lim_{h \to 0} \frac{f(x+h)-f(x)}{h}")
        self.add(eq, index_labels(eq[0]))
```

```bash
bin/mx render cena.py Debug --format png -q l
```

Abra o PNG, leia os números, e só então escreva `eq[0][3:7].set_color(RED)`.

## Transformar uma equação em outra

```python
a = MathTex(r"{{a^2}} + {{b^2}} = {{c^2}}")
b = MathTex(r"{{a^2}} = {{c^2}} - {{b^2}}")
self.play(TransformMatchingTex(a, b))
```

`TransformMatchingTex` casa os submobjects pelo texto LaTeX e move os
termos correspondentes. **Depende das chaves duplas** para saber onde
estão as fronteiras. Sem elas, degrada para um fade cruzado.

Para formas em geral (sem LaTeX): `TransformMatchingShapes`.

## Ambiente LaTeX e templates

`MathTex` usa `align*` por padrão; `Tex` usa modo texto.

```python
MathTex(r"x &= 1 \\ y &= 2")                          # align* multi-linha
MathTex(r"\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}")
Tex(r"Seja $x > 0$ um real.")                          # texto com matemática
MathTex(r"...", tex_environment="gather*")
```

Pacotes extras:

```python
tpl = TexTemplate()
tpl.add_to_preamble(r"\usepackage{physics}\usepackage{siunitx}")
MathTex(r"\dv{f}{x}", tex_template=tpl)
```

## O LaTeX desta máquina

TinyTeX (TeX Live 2026) em `~/.TinyTeX`, **fora do PATH padrão**. Os
wrappers `bin/*` resolvem isso. Se você chamar o Python diretamente, exporte:

```bash
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
```

Pacotes já instalados para o Manim: `standalone` `preview` `amsmath`
`amsfonts` `dvisvgm` `doublestroke` `setspace` `rsfs` `relsize` `ragged2e`
`fundus-calligra` `microtype` `wasysym` `physics` `babel-english`
`gnu-freefont` `mathastext` `cbfonts-fd`.

Faltou algum:

```bash
export PATH="$HOME/.TinyTeX/bin/x86_64-linux:$PATH"
tlmgr install <pacote>
```

Verifique a cadeia inteira:

```bash
bin/mx doctor        # a linha "LaTeX → SVG (MathTex)"
```

## Fontes de `Text`

```python
Text("olá", font="DejaVu Sans", font_size=48, weight=BOLD, slant=ITALIC)
```

```bash
fc-list : family | tr ',' '\n' | sort -u | head -50
```

Fonte inexistente não é erro fatal: o Manim avisa e cai numa substituta.
Desligue o aviso com `warn_missing_font=False`.

## Performance

Cada string LaTeX **nova** dispara `latex` + `dvisvgm` (~1 s). O Manim
cacheia por conteúdo, então repetir a mesma string é barato.

- Reaproveite objetos em vez de recriar.
- Prefira `Text` quando não houver matemática.
- Não desligue o cache (`--no-cache`) sem necessidade — ele guarda o LaTeX
  compilado.
- Muitas fórmulas distintas? Renderize `-q l` enquanto ajusta o conteúdo.

## Armadilhas

- **Faltou `r`** na string → `\f`, `\n`, `\b` viram escapes do Python.
- **`{{ }}` são do Manim, não do LaTeX.** Ele os remove antes de compilar.
  Se você precisa de chaves literais no LaTeX, use `{ {` com espaço.
- **`tex_to_color_map` casa substrings cruas** — inclusive dentro de
  `\frac`, `\text`, nomes de comandos.
- **Índices mudam** quando você edita a fórmula. Reconfira com
  `index_labels`.
- **`Tex` ≠ `MathTex`.** `Tex(r"x^2")` renderiza "x2" em modo texto.
- **Erro de LaTeX aparece como `ValueError`/`CalledProcessError`** com um
  log longo. Procure a linha `! LaTeX Error:` nele. Rode com
  `--no_latex_cleanup` para inspecionar o `.tex`/`.log` gerado.
- **`disable_ligatures=True` muda o espaçamento** — reposicione o que
  estava alinhado.
