---
name: manim-api-discovery
description: >-
  Descobrir QUALQUER classe, método, função, propriedade ou constante do
  Manim sem chutar e sem depender de memória. Use sempre que precisar do
  nome exato de uma animação, da assinatura de um construtor, da lista
  completa de métodos de um Mobject, do valor de uma cor, ou quando um
  `AttributeError`/`TypeError` sugerir que o nome ou o parâmetro está
  errado. Cobre o índice offline em `api/` (5523 símbolos da CE, 2662 no
  topo, todos os métodos herdados), os comandos `mx find` / `mx show`,
  e a introspecção ao vivo. Use ANTES de escrever código que chame um
  método que você não confirmou.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Descoberta de API — acesso a TODOS os métodos e funções

A API do Manim é grande demais para memorizar e muda entre versões. Este
projeto carrega um índice **gerado por reflexão do pacote instalado**, então
ele bate exatamente com a versão em uso (ManimCE 0.21.0 / ManimGL 1.7.2).

## Nunca chute um nome

Antes de escrever `mob.algum_metodo(...)`, confirme. Custa um comando.

```bash
bin/mx show Circle                 # tudo: 4 métodos próprios + 260 herdados
bin/mx show Circle --own-only      # só o que Circle define
bin/mx show Transform --json       # para parsear
```

## Buscar quando você não sabe o nome

```bash
bin/mx find "transform"                        # qualquer coisa com "transform"
bin/mx find "fade" --kind class                # só classes
bin/mx find "rotate" --category animation/     # dentro de uma categoria
bin/mx find "color" --kind function -n 50
bin/mx find "shift" --package manimgl          # no ManimGL
```

A busca cobre nome, docstring **e nomes de métodos** — então
`bin/mx find "next_to"` encontra as classes que têm esse método.

## Os arquivos do índice

Todos em `api/`, regeneráveis com `bin/mx api-dump`.

| Arquivo | Para quê | Tamanho |
|---|---|---|
| `manim-ce-index.tsv` | 1 símbolo por linha. **Use `grep` aqui.** | 528 KiB |
| `manim-ce-methods.tsv` | 1 método por linha, com classe e assinatura | 6,8 MiB |
| `manim-ce-toplevel.md` | tudo que `from manim import *` traz | 33 KiB |
| `manim-ce-by-category.md` | navegação por categoria | 570 KiB |
| `manim-ce-inheritance.txt` | árvore de herança | 6 KiB |
| `manim-ce-api.json.gz` | tudo, estruturado — **comprimido** | 1,4 MiB |
| `manimgl-*.{tsv,md,json.gz}` | o mesmo para o ManimGL | |
| `ce-vs-gl.md` | mapa de compatibilidade entre os dois | |

O `.json.gz` é lido por programa (`mx find` / `mx show`), nunca por
`grep` — por isso ele é o único comprimido. Os `.tsv` e `.md`, que existem
justamente para serem grepados, ficam em texto puro.

**Não leia os arquivos grandes inteiros.** Use `grep`.

### Receitas de grep

```bash
# Todas as animações disponíveis
awk -F'\t' '$1=="class" && $3 ~ /^animation/ {print $2}' api/manim-ce-index.tsv | sort

# Todos os Mobjects de geometria com a assinatura
awk -F'\t' '$1=="class" && $3=="mobject/geometry" {print $2"\t"$4}' api/manim-ce-index.tsv

# Todos os métodos de qualquer classe cujo nome contenha "set_"
awk -F'\t' '$2 ~ /^set_/ {print $1"."$2$6}' api/manim-ce-methods.tsv | sort -u | head -60

# Só os métodos que a classe define (não herdados)
awk -F'\t' '$1=="Axes" && $5=="0" {print $2$6}' api/manim-ce-methods.tsv

# Qual classe define este método?
awk -F'\t' '$2=="point_from_proportion" {print $1" <- definido em "$4}' api/manim-ce-methods.tsv | sort -u

# Todas as rate functions
awk -F'\t' '$3=="utils/rate_functions" {print $2$4}' api/manim-ce-index.tsv

# Uma cor específica e seu valor
grep -P '^constant\tBLUE_D\t' api/manim-ce-index.tsv

# Todas as cores de uma família
awk -F'\t' '$1=="constant" && $2 ~ /^TEAL/ {print $2"\t"$4}' api/manim-ce-index.tsv | sort -u
```

## Introspecção ao vivo

Quando o índice não basta (ex.: você quer o docstring inteiro):

```bash
bin/mx render --help                    # flags reais da CLI

.venv/bin/python -c "
from manim import *
help(Axes.plot)
"

.venv/bin/python -c "
from manim import *
import inspect
print(inspect.signature(TransformMatchingTex.__init__))
print(inspect.getsource(Circle))
"

# Todos os métodos públicos de uma instância, ao vivo
.venv/bin/python -c "
from manim import *
c = Circle()
print([m for m in dir(c) if not m.startswith('_')])
"
```

## Encadeamento e `.animate` — o que é chamável

Quase todo método de `Mobject` que devolve `Self` pode ser encadeado e usado
com `.animate`:

```python
circle.set_color(RED).shift(UP).scale(2)           # estático, imediato
self.play(circle.animate.set_color(RED).shift(UP)) # animado
```

Para descobrir o que é encadeável numa classe:

```bash
awk -F'\t' '$1=="Circle" && $6 ~ /Self/ {print $2$6}' api/manim-ce-methods.tsv | head -40
```

## Regenerar o índice

Obrigatório depois de atualizar o Manim, senão o índice mente.

```bash
bin/mx api-dump                                    # ManimCE
bin/mx api-dump --package manimlib --label manimgl # ManimGL (rode no .venv-gl)
bin/mx api-diff                                    # atualiza ce-vs-gl.md
```

## Armadilhas

- **Nome igual ≠ API igual.** As 153 classes com nome comum entre CE e GL
  têm assinatura diferente em 100% dos casos. Confira o pacote certo com
  `--package`.
- **A maior parte da API é herdada.** `Circle` define 4 métodos e herda 260.
  Se você olhar só os próprios, vai concluir errado que algo não existe.
- **Depreciados ainda aparecem no índice.** `ApplyMethod` existe, mas o
  caminho atual é `.animate`. O índice diz o que existe, não o que é idiomático.
- **Constantes de cor têm entradas duplicadas** (reexportadas de vários
  módulos). Isso é esperado; o valor é o mesmo.
