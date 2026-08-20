---
name: manim-api-discovery
description: >-
  Descobrir QUALQUER classe, método, propriedade, kwarg, constante, cor, alias
  de tipo ou membro de Enum do Manim sem chutar — e PROVAR que existe antes de
  escrever a linha. Use quando a pergunta for "que classe faz X?", "qual a
  assinatura disso?", "esse método existe?", "que parâmetros esse construtor
  aceita?", "posso passar esse kwarg aqui?", "de onde vem esse método?", "quem
  herda de X?", "quem tem esse método?", "qual o valor dessa cor?", "o que
  `Point3DLike` quer dizer?", "isso é CE ou GL?", "isso está depreciado?",
  "esse nome mudou de versão?", "confere se essa cena não inventou nada", "o
  índice está velho?", "como eu regenero o índice?", "que cenas tem nesse
  arquivo?" — e sempre que um `AttributeError`, um `TypeError: unexpected
  keyword argument` ou um `ImportError: cannot import name` sugerir que o nome,
  o parâmetro ou o caminho de import está errado. Cobre `mx find` / `mx show` /
  `mx scenes`, os seis arquivos de `api/` (5523 símbolos, 588 nomes no topo,
  50945 métodos com origem), o FONTE instalado como sétima fonte (6,4 MiB
  grepáveis em 20 ms), as receitas de `grep`/`awk`, três formas de listar os
  kwargs de um construtor (uma delas sem importar o Manim, em 0,09 s), como
  LER uma assinatura do índice sem se enganar, a introspecção ao vivo, o
  conferidor estático de cena e o mapa CE×GL. NÃO use para depurar um render
  que já falhou por ambiente, LaTeX, codec ou saída (`manim-troubleshooting`),
  para escolher qualidade/formato e achar o caminho do arquivo
  (`manim-render-api`), nem para APRENDER A USAR uma classe que você já
  identificou — aí a skill é a do assunto (`manim-mobjects`,
  `manim-layout-posicionamento`, `manim-animations`, `manim-composicao-ritmo`,
  `manim-graphs-plots`, `manim-tabelas-matrizes`, `manim-grafos-redes`,
  `manim-text-latex`, `manim-svg-imagens`, `manim-color-theming`,
  `manim-camera-2d`, `manim-3d-camera`, `manim-cenas-secoes`,
  `manim-updaters-valuetracker`, `manim-mobjects-customizados`,
  `manimgl-3b1b`).
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Descoberta de API — nunca chute um nome, uma assinatura ou um kwarg

O erro mais caro do Manim não é o algoritmo errado: é o **nome inventado**. Ele
não aparece no editor, não aparece na revisão, e cobra o preço no fim de um
render. Metade dos tutoriais na internet descreve a API do ManimGL
(`ShowCreation`, `TexMobject`, `CONFIG = {...}`) e a outra metade descreve
versões da CE que já mudaram. Um modelo de linguagem interpola as duas com
confiança total.

Este projeto carrega um índice **gerado por reflexão do pacote instalado**
(`bin/mx api-dump`), então ele bate exatamente com a versão em uso — hoje
ManimCE **0.21.0** e ManimGL **1.7.2**, Python 3.12.3. O índice não é uma cópia
da documentação: é o pacote se descrevendo.

> **Procedência deste arquivo.** Toda contagem, assinatura, caminho e número de
> linha abaixo foi conferido contra `api/*.tsv`, `api/*.json.gz` ou o fonte em
> `.venv/lib/python3.12/site-packages/manim/`. As poucas afirmações que
> dependem de executar algo estão marcadas **[não reverificado]** com a data da
> medição original. Nenhum render foi feito para escrever isto — e nenhum é
> necessário para responder a nada desta skill.

---

## 0. O custo de perguntar, medido

| Ação | Tempo | Comando |
|---|---:|---|
| `grep` no `manim-ce-index.tsv` (528 KiB) | **< 10 ms** | `grep -P '^class\tCircle\t' api/manim-ce-index.tsv` |
| `awk` no `manim-ce-methods.tsv` (6,8 MiB) | **~20 ms** | `awk -F'\t' '$1=="Circle"' api/manim-ce-methods.tsv` |
| `grep -rn` no **fonte instalado** (6,4 MiB, 168 `.py`) | **~20 ms** | `grep -rIn riemann .venv/lib/python3.12/site-packages/manim/` |
| varredura do MRO **pelo índice** (§10, receita A) | **~90 ms** | `awk` duplo sobre `methods.tsv` |
| carregar `manim-ce-api.json.gz` em Python | **~130 ms** | `json.load(gzip.open(...))` — 338 classes com propriedades |
| `bin/mx find` / `bin/mx show` | **~0,19 s** | lê o `.json.gz`, **não importa o manim** |
| `.venv/bin/python -c "import manim"` | **1,6–1,7 s** | 8× mais caro que o `mx` |
| render de 1 frame (`--format png`, cache quente) | ~0,6–2 s | assunto de `manim-render-api` |

**Não existe desculpa de custo para chutar.** A consulta mais cara desta skill
custa menos que o tempo de digitar o nome errado — e muito menos que descobrir
o erro no fim de um render.

---

## 1. O funil: a pergunta manda na ferramenta

| A sua pergunta | A ferramenta | Custo |
|---|---|---|
| "existe uma classe chamada X?" | `grep -P '^class\tX\t' api/manim-ce-index.tsv` | 10 ms |
| "qual a assinatura de X?" | `bin/mx show X` | 0,19 s |
| "que métodos X tem, e de onde vêm?" | `bin/mx show X` (ou `--own-only`) | 0,19 s |
| "que classe faz \<coisa que não sei nomear\>?" | `bin/mx find "<coisa>"` | 0,19 s |
| "tudo que existe nessa categoria" | `bin/mx find "" --category mobject/table --kind class -n 999` (§4) | 0,19 s |
| "quem tem o método `plot`?" | `awk '$2=="plot"' methods.tsv` | 20 ms |
| "quem herda de `Animation`?" | `awk '$4=="Animation" && $5=="1"' methods.tsv` (§9 — melhor que a árvore) | 20 ms |
| **"que kwargs esse construtor aceita?"** | **varredura do MRO (§10)** — a assinatura sozinha NÃO responde | 90 ms |
| "quem aceita este kwarg?" | §10, pergunta inversa | 90 ms / 1,7 s |
| "qual o valor dessa cor?" | `bin/mx find NOME --kind constant` (nunca `mx show`) | 0,19 s |
| "que propriedades X tem?" | `bin/mx show X` ou o `.json.gz` — **os TSV não guardam propriedade** (§5) | 0,19 s |
| "o que `Point3DLike` quer dizer?" | o fonte: `manim/typing.py` — **não está no índice** (§11) | 20 ms |
| "quais são os membros desse Enum?" | o fonte, ou `list(Enum)` ao vivo — **não está no índice** (§3) | 20 ms |
| "isso está depreciado?" | **nenhuma fonte responde** — a 0.21 não marca nada (§12) | — |
| "o docstring INTEIRO / o corpo do método" | `grep` no fonte (§12) ou `inspect.getsource` (§22) | 20 ms / 1,7 s |
| "isso é da CE ou do GL?" | `api/ce-vs-gl.md`, `--package manimgl` | 10 ms |
| "essa cena inventou algum nome ou kwarg?" | o conferidor de §16 | 1,7 s |
| "quais cenas tem neste arquivo?" | `bin/mx scenes arquivo.py` | 0,2 s |

### A regra de ouro, em uma frase

**Se a resposta não saiu de uma consulta, ela é um chute — mesmo que pareça
óbvia.** `set_width` "obviamente" existe. Não existe (§13).

---

## 2. As OITO fontes, e o que cada uma NÃO responde

O erro de método mais comum aqui não é consultar errado: é consultar a fonte
que **não tem** aquela informação e concluir "não existe".

| # | Fonte | Responde | **NÃO responde** |
|---|---|---|---|
| 1 | `api/manim-ce-index.tsv` (528 KiB) | existe? kind, categoria, assinatura, módulo, 1ª linha do doc | propriedade, membro de Enum, atributo de classe, alias de tipo, kwarg herdado |
| 2 | `api/manim-ce-methods.tsv` (6,84 MiB) | quem tem esse método, de onde ele vem, assinatura dele | propriedade, o corpo do método, classe privada |
| 3 | `api/manim-ce-toplevel.md` (35,6 KiB) | o que `from manim import *` traz de fato, e o que é `[só no topo]` | qualquer coisa fora do namespace raiz |
| 4 | `api/manim-ce-by-category.md` (585 KiB) | navegação por assunto, métodos próprios em `<details>` | métodos herdados; e a **contagem do sumário engana** (§8) |
| 5 | `api/manim-ce-inheritance.txt` (5,9 KiB) | a família inteira de uma classe, de relance | quem desce por uma base **privada** (§9) |
| 6 | `api/manim-ce-api.json.gz` (1,39 MiB) | tudo dos itens 1–5 **mais as propriedades**, estruturado | corpo, Enum, atributo de classe |
| 7 | **o fonte instalado** `.venv/lib/python3.12/site-packages/manim/` (6,4 MiB) | docstring inteiro, corpo, classe privada, membro de Enum, atributo de classe, decorador, alias de tipo | nada — é a verdade (§12) |
| 8 | **introspecção ao vivo** (`import manim`, 1,7 s) | comportamento em vez de forma: MRO real, valor computado, Enum materializado | custa 8× o `mx` (§22) |

Os `.tsv`/`.md` ficam em texto puro **de propósito**: existem para serem
grepados. O `.json.gz` é o único comprimido, porque é lido por programa
(`mx find`/`mx show`) e o JSON cru passa de 14 MiB. **Não leia os grandes
inteiros** — `manim-ce-methods.tsv` tem 50 945 linhas.

E o item 7 é o que falta na cabeça da maioria: **o pacote instalado é um índice
grepável de 20 ms.** Ele responde tudo que os seis arquivos não respondem, e
nunca mente.

---

## 3. `mx show` — quando você já sabe o nome

```bash
bin/mx show Circle                 # tudo: assinatura, bases, propriedades, 4 próprios + 260 herdados
bin/mx show Circle --own-only      # só o que Circle define (+ a contagem dos herdados)
bin/mx show Transform --json       # o SymbolInfo inteiro, para parsear
bin/mx show ShowCreation --package manimgl
```

Saída real, anotada:

```
class Circle(radius: 'float | None' = None, color: 'ParsableManimColor' = ManimColor('#FC6255'), **kwargs: 'Any') -> 'None'
módulo   : manim.mobject.geometry.arc      ← de onde importar quando não está no topo
categoria: mobject/geometry                 ← serve de filtro no `mx find --category`
herda de : Arc                              ← só as bases DIRETAS; a família está no inheritance.txt
doc      : A circle.                        ← só a PRIMEIRA linha do docstring

propriedades (9): always, animate, color, depth, fill_color, height, n_points_per_curve, stroke_color, width
métodos próprios (4):  ...
métodos herdados (260): [Mobject] add(...), [VMobject] add_line_to(...), ...
```

O prefixo `[Classe]` de cada método herdado é **de onde ele vem** — é assim que
se descobre que `next_to` é do `Mobject` e vale para tudo, enquanto
`get_riemann_rectangles` é do `CoordinateSystem` e só existe em quem herda dele.

O `--json` devolve o `SymbolInfo` completo, com estas 11 chaves (idêntico ao que
`mx find --json` devolve por item):

```
bases  category  doc  kind  methods  module  name  properties  qualname  signature  value_repr
```

`methods` é uma lista de `{name, kind, signature, doc, defined_in, inherited}`.
`properties` é uma lista de strings — **e ela só existe aqui e no `.json.gz`**
(§5).

### Armadilha: estar no índice prova que o NOME existe, não que ele funciona

`Mobject` tem **5 métodos-tampão** que levantam `NotImplementedError` em vez de
fazer alguma coisa. Conferidos um a um em
`.venv/lib/python3.12/site-packages/manim/mobject/mobject.py`:

| método | linha do `raise` | mensagem |
|---|---:|---|
| `point_from_proportion` | 2401 | `"Please override in a child class."` |
| `proportion_from_point` | 2404 | `"Please override in a child class."` |
| `align_points_with_larger` | 3045 | `"Please override in a child class."` |
| `interpolate_color` | 3180 | `"Please override in a child class."` |
| **`get_point_mobject`** | **3033** | **`f"get_point_mobject not implemented for {self.__class__.__name__}"`** |

> **Correção de uma versão anterior desta skill.** Ela dizia que os cinco têm
> "o corpo inteiro igual a `raise NotImplementedError("Please override in a
> child class.")`". São cinco tampões, mas **só quatro** usam essa mensagem —
> `get_point_mobject` monta a sua com f-string (`msg = f"get_point_mobject not
> implemented for {...}"`, linhas 3032-3033). Quem procurar os cinco grepando a
> string literal acha quatro e conclui, errado, que o quinto está implementado.

Eles aparecem no `mx show` de **toda** subclasse, inclusive das que não os
implementam:

```python
ImageMobject("x.png").point_from_proportion(0.5)
# NotImplementedError: Please override in a child class.          [não reverificado — 2026-08-19]
```

E o índice não avisa: `awk '$1=="ImageMobject" && $2=="point_from_proportion"'`
devolve a linha com `defined_in=Mobject`, `inherited=1`. **Sinal de alerta: um
método geométrico com `defined_in` igual a `Mobject`.** Confirme no fonte (§12)
antes de contar com ele. Nada disso é exclusividade do `Mobject` — a busca geral
é uma linha:

```bash
grep -rn "raise NotImplementedError" .venv/lib/python3.12/site-packages/manim/
```

### Armadilha: homônimo, e o `mx show` escolhe em silêncio

`cmd_show` faz `matches[0]` (`manimx/cli.py:345`). Se dois símbolos diferentes
têm o mesmo nome, você vê um e nunca fica sabendo do outro. Na CE 0.21 há
**exatamente um** caso entre classes (conferido varrendo o índice inteiro):

```bash
$ awk -F'\t' '$1=="class" && $2=="Polygon" {print $2"\t"$5}' api/manim-ce-index.tsv
Polygon	manim.mobject.geometry.polygram     ← o Mobject que você quer
Polygon	manim.utils.polylabel               ← estrutura interna do polylabel, NÃO é Mobject
```

Verificado ao vivo: `manim.Polygon is manim.utils.polylabel.Polygon` → `False`.
**O desempate é sorte, não projeto:** o dicionário do `.json.gz` é gravado
`sorted()` por `qualname`, então `matches[0]` é o primeiro em ordem alfabética
de módulo — e `manim.mobject...` vem antes de `manim.utils...` por acaso. Numa
colisão futura o `mx show` pode passar a mostrar o símbolo errado sem que nada
mude na sua consulta.

Antes de confiar no `mx show`, confirme que o nome é único:

```bash
awk -F'\t' -v n=Polygon '$2==n {print $1"\t"$3"\t"$5}' api/manim-ce-index.tsv | sort -u
```

(Entre kinds diferentes não há nenhuma colisão: nenhum nome é ao mesmo tempo
classe e função, ou função e constante. Conferido no índice inteiro.)

### Armadilha: para uma CONSTANTE, o modo texto esconde o valor

```
$ bin/mx show BLUE_D
constant BLUE_D
módulo   : manim
categoria: other          ← e nenhum valor
```

O `cmd_show` não imprime `value_repr`. Use uma das duas formas:

```bash
bin/mx find BLUE_D --kind constant -n 4     # constant BLUE_D  ...  ManimColor('#29ABCA')
bin/mx show BLUE_D --json                   # "value_repr": "ManimColor('#29ABCA')"
```

### Armadilha: o cabeçalho de `Animation` não é o `__init__`

`inspect.signature(cls)` pode vir do `__new__`. Varredura das 258 classes do
topo: **8 divergem** de `signature(cls.__init__)` [não reverificado — 2026-08-19] — 6 são Enums/dtype/namespace,
e a única que importa é `Animation`:

```
$ bin/mx show Animation
class Animation(mobject=None, *args, use_override=True, **kwargs) -> 'Self'   ← isto é o __new__
...
métodos próprios (22):
  __init__(self, mobject, lag_ratio=0.0, run_time=1.0, rate_func=<smooth>,
           reverse_rate_function=False, name=None, remover=False,
           suspend_mobject_updating=True, introducer=False, ...)             ← isto é o que você passa
```

Regra: **para animação, leia a linha `__init__` da seção "métodos próprios",
não o cabeçalho.** É lá que moram `run_time`, `rate_func` e `lag_ratio`. As
subclasses (`Create`, `FadeIn`, `Transform`) não têm `__new__` próprio e o
cabeçalho delas está certo — mas aí entra o problema de §10, que é o
`**kwargs`.

### Armadilha: atributo de classe e membro de Enum são INVISÍVEIS

A varredura indexa métodos, propriedades e constantes **de módulo**. Atributo
de classe, não (`_class_members` em `manimx/introspect.py` só coleta `property`,
`staticmethod`, `classmethod` e rotinas). Dois casos que doem:

```
$ bin/mx show TexTemplateLibrary
class TexTemplateLibrary()
doc      : A collection of basic TeX template objects
métodos herdados (1): [object] __init__(...)          ← e nada mais

$ .venv/bin/python -c "from manim import TexTemplateLibrary as T; print([a for a in dir(T) if not a.startswith('_')])"
['ctex', 'default', 'simple', 'threeb1b']              ← o conteúdo real

$ bin/mx show LineJointType
herda de : Enum                                        ← e nenhum membro

$ .venv/bin/python -c "from manim import LineJointType as L; print(list(L))"
[<LineJointType.AUTO: 0>, <LineJointType.ROUND: 1>, <LineJointType.BEVEL: 2>, <LineJointType.MITER: 3>]
```

Isso é estrutural, e dá para provar sem executar nada: **três classes do índice
não têm método nenhum indexado**, e são justamente Enums — `CapStyleType`,
`LineJointType`, `RendererType` (conferido no `.json.gz`). Elas são, por isso, as
únicas 3 classes de 337 que não aparecem no `methods.tsv` (334 nomes lá).

Regra: **viu `herda de : Enum`, ou uma classe sem métodos próprios? a resposta
está no fonte (§12) ou no interpretador (§22).** Vale para `CapStyleType`,
`LineJointType`, `RendererType`, `DefaultSectionType`, `TexTemplateLibrary`,
`TexFontTemplates`.

Sem executar nada:

```bash
grep -n "class LineJointType" -A 8 .venv/lib/python3.12/site-packages/manim/constants.py
```

### Armadilha: `herda de` pode apontar para uma classe que você não consegue abrir

```
$ bin/mx show FadeIn
class FadeIn(*mobjects: 'Mobject', **kwargs: 'Any') -> 'None'
herda de : _Fade                       ← e `mx show _Fade` não acha nada
propriedades (3): path_arc, path_func, run_time
```

`_Fade` começa com `_`, então **a varredura nunca o indexa**. São **27 classes**
com pelo menos uma base ausente do índice; **8 delas por base privada**
(conferido no `.json.gz`):

| base privada | classes afetadas |
|---|---|
| `_Fade` | `FadeIn`, `FadeOut` |
| `_BooleanOps` | `Union`, `Difference`, `Intersection`, `Exclusion` |
| `_ScaleBase` | `LinearBase`, `LogBase` |

As outras 19 têm base fora do pacote (`Protocol`, `Enum`, `Exception`, `dict`,
`Formatter`, `Namespace`…). As consequências estão em §9 (a árvore quebra) e
§10 (a varredura de kwargs pelo índice para ali). O antídoto é sempre o mesmo:
o fonte.

```bash
grep -n "class _Fade" -A 20 .venv/lib/python3.12/site-packages/manim/animation/fading.py
```

---

## 4. `mx find` — quando você não sabe o nome

```bash
bin/mx find "transform"                        # qualquer coisa com "transform"
bin/mx find "fade" --kind class                # kind ∈ {class, function, constant} — e SÓ esses três
bin/mx find "rotate" --category animation/     # o filtro é startswith: "mobject" pega mobject/*
bin/mx find "color" --kind function -n 50
bin/mx find "shift" --package manimgl          # o default de --package aqui é `manim-ce`
```

A busca é por **cinco níveis de proximidade**, nesta ordem
(`manimx/cli.py:311-323`):

| score | casa em | exemplo conferido |
|---:|---|---|
| 0 | nome exato | `mx find Cutout` |
| 1 | nome começa com | `mx find Show` |
| 2 | substring do nome | `mx find transform` |
| 3 | **substring da PRIMEIRA LINHA do docstring** | `mx find polar` também devolve `angle_of_vector` ("Returns polar coordinate theta…") |
| 4 | **substring de um nome de MÉTODO** | `mx find riemann` → devolve as 7 CLASSES que têm `get_riemann_rectangles` |

Os níveis 3 e 4 são o motivo de esta ferramenta valer mais que `grep`: você
descreve o que quer ("riemann", "next_to", "polar") e ela devolve o portador.

> **Correção de uma versão anterior desta skill.** Ela dizia "substring do
> docstring" e usava `mx find riemann` → `Axes` como exemplo de **score 3**. As
> duas coisas estão erradas, e pelo mesmo motivo: o índice guarda só a
> **primeira linha** do docstring (`_first_doc_line` em
> `manimx/introspect.py`). Conferido: `awk -F'\t' 'tolower($6) ~ /riemann/'
> api/manim-ce-index.tsv` devolve **zero** linhas — nenhum símbolo tem
> "riemann" na primeira linha do doc. Aquele `Axes` veio de **score 4**, pelo
> método `get_riemann_rectangles`.
>
> A consequência prática é maior que a errata: **`mx find` NÃO procura dentro
> do corpo do docstring.** Um conceito explicado no terceiro parágrafo da
> documentação de uma classe é invisível para ele. Para isso, `grep` no fonte
> (§12).

### O truque da consulta vazia: listar uma categoria inteira

A string vazia é substring de todo nome (score 2), então:

```bash
bin/mx find "" --category mobject/table --kind class -n 999
```

```
class    DecimalTable   mobject/table   (table: 'Iterable[Iterable[float | str]]', element_to_mobject: …)
class    IntegerTable   mobject/table   …
class    MathTable      mobject/table   …
class    MobjectTable   mobject/table   …
class    Table          mobject/table   (table: 'Iterable[Iterable[float | str | VMobject]]', row_labels: …)
```

É a forma mais rápida de "me mostre tudo que existe nesse assunto, com
assinatura". **Sem `--kind class` vêm junto as constantes reexportadas**
(`BLACK`, `PURE_YELLOW` aparecem em `mobject/table` porque o módulo as importa)
— ver §8.

### Armadilha: `-n` tem default 30 e trunca em SILÊNCIO

```
$ bin/mx find color --kind class --json | jq length        # com o default
30
$ bin/mx find color --kind class -n 999 --json | jq length # de verdade
209
```

Não há linha de "mostrando 30 de 209" [medição de 2026-08-19]. Quando estiver fazendo **inventário** (e
não caçando um nome), passe `-n 999` **sempre**.

### Armadilha: o resultado tem mais linhas que o nome procurado

`mx find` é substring, e não deduplica. Medido:

```
$ bin/mx find RIGHT --kind constant -n 999 --json | jq -r '.[].name' | sort | uniq -c | sort -rn
     42 RIGHT              ← as 42 reexportações da MESMA constante (§7)
      1 LIGHTBRIGHTGREEN   ← "bright" contém "right"
      1 BRIGHTYELLOW
      …                    ← 25 cores da paleta XKCD ao todo, total 67 acertos
```

Os 42 `RIGHT` são score 0 e vêm primeiro, então **para achar está tudo bem; para
contar, nunca use a saída do `find`** — conte no `index.tsv` com `awk`, onde
você controla `$2==` (igualdade) em vez de substring.

Outros dois detalhes verificados: `-n 0` devolve vazio com exit 1 (parece "não
existe", e não é); e `--kind` **não aceita `method`** nem `module` — os choices
do argparse são exatamente `class`, `function`, `constant` (`manimx/cli.py:493`).
Para procurar método, use o `methods.tsv` (§17) ou o score 4.

### Armadilha: `| head` num comando `mx` polui a saída

`bin/mx show Circle | head -3` termina com `erro: BrokenPipeError` grudado no
resultado. Use `--own-only`, `-n`, ou `| sed -n '1,20p'` (o `sed` sem `q`
consome o fluxo inteiro e não quebra o cano). [não reverificado — 2026-08-19]

---

## 5. As colunas dos TSV, e o que NÃO está neles

```
manim-ce-index.tsv     $1 kind   $2 name    $3 category  $4 signature   $5 module   $6 doc
manim-ce-methods.tsv   $1 class  $2 method  $3 kind      $4 defined_in  $5 inherited(0|1)  $6 signature  $7 doc
```

- Em `index.tsv`, `$4` é a **assinatura** para classe/função e o **valor** para
  constante — os dois ocupam a mesma coluna (`sym.signature or sym.value_repr`).
- Em `index.tsv`, `$6` é a **primeira linha** do docstring, nunca ele inteiro.
- Em `methods.tsv`, `$5` é `0` para método próprio e `1` para herdado; `$4` diz
  em que classe do MRO ele foi definido; `$3` ∈ `method` (50 041) ·
  `classmethod` (597) · `staticmethod` (307).

### O que há dentro, em números conferidos hoje

```
index.tsv     5523 linhas  =  338 class + 285 function + 4900 constant
              2662 nomes únicos (337 classes, 281 funções, 2044 constantes)
methods.tsv   50945 linhas =  1901 próprias + 49044 herdadas, em 334 classes
              1900 pares (classe, método) próprios distintos
```

`class` tem 338 linhas para 337 nomes por causa do homônimo `Polygon`; e
`methods.tsv` tem 334 classes porque as 3 Enums sem método nenhum não geram
linha (§3). As 4900 linhas de constante para 2044 nomes são reexportação:
`RIGHT` aparece 42 vezes, `UP` 40, `PI` 37 — uma por módulo que as importa
(§7).

### **Propriedade não está em TSV nenhum.** Este é o buraco que mais engana

Conferido, e vale gravar:

```bash
$ awk -F'\t' '$2=="width"'   api/manim-ce-methods.tsv | wc -l     # 0
$ awk -F'\t' '$2=="animate"' api/manim-ce-methods.tsv | wc -l     # 0
$ awk -F'\t' '$2=="width"'   api/manim-ce-index.tsv   | wc -l     # 0
$ grep -c "propriedades" api/manim-ce-by-category.md               # 0
```

`dump_api` escreve `sym.methods` nos TSV e no `by-category.md`, e
`sym.properties` **só** no `.json.gz`. Como `width`, `height`, `animate`,
`color`, `fill_color` e `stroke_color` são **propriedades**, o `grep` mais
natural do mundo — "esse atributo existe?" — devolve zero e induz à conclusão
oposta da verdade.

As duas formas que funcionam:

```bash
bin/mx show Circle | sed -n '/^propriedades/p'
```

```bash
# quem tem a propriedade X, e quantas propriedades distintas existem
python3 - <<'PY'
import gzip, json, collections
S = json.load(gzip.open("api/manim-ce-api.json.gz", "rt"))["symbols"]
c = collections.Counter(p for v in S.values() if v["kind"] == "class" for p in v["properties"])
print(len(c), "propriedades distintas")
print(c.most_common(10))
PY
```

Saída real (0,13 s): **161 propriedades distintas**, em 287 das 338 classes.
As mais espalhadas:

| propriedade | classes | propriedade | classes |
|---|---:|---|---:|
| `height` / `width` | 193 | `always` | 147 |
| `animate` / `depth` | 192 | `n_points_per_curve` | 134 |
| `color` / `fill_color` / `stroke_color` | 166 | `run_time` | 75 |
| `submobjects` | 45 | `path_arc` / `path_func` | 31 |

`Mobject` define exatamente cinco: `always`, `animate`, `depth`, `height`,
`width`. Todo `get_X`/`set_X` sobre elas é açúcar depreciado — §13.

---

## 6. O mapa das 41 categorias — onde procurar, e quem é o dono

A `category` sai de `_CATEGORY_BY_MODULE` em `manimx/introspect.py`: prefixo de
módulo → rótulo, **prefixo mais longo vence**. Ela não é semântica, é
geográfica: diz em que pasta do pacote o símbolo mora.

`total` = linhas do índice nessa categoria (inclui constante reexportada).
`c` = classes, `f` = funções — **esses dois são o número acionável**.

| categoria | total | c | f | quem ensina a usar |
|---|---:|---:|---:|---|
| `utils/color` | 2335 | 4 | 15 | `manim-color-theming` |
| `mobject/opengl` | 546 | 45 | 3 | — (buraco declarado de propósito) |
| `mobject/geometry` | 384 | 57 | 0 | `manim-mobjects`; booleanos e casco em `manim-mobjects-customizados` |
| `mobject/core` | 281 | 19 | 4 | `manim-mobjects`, `manim-layout-posicionamento` |
| `mobject/text` | 272 | 15 | 2 | `manim-text-latex` (`Code`/`Typst`/`Paragraph`: órfãos) |
| `mobject/graphing` | 216 | 15 | 0 | `manim-graphs-plots` |
| `scene` | 213 | 13 | 2 | `manim-cenas-secoes` |
| `other` | 189 | 7 | 15 | infra de CLI — `manim-project` |
| `camera` | 138 | 8 | 0 | `manim-camera-2d` (2D) · `manim-3d-camera` (`ThreeDCamera`) |
| `utils/other` | 137 | 15 | 89 | repartida (é a maior massa órfã do índice) |
| `mobject/3d` | 96 | 17 | 8 | `manim-3d-camera` |
| `renderer` | 89 | 9 | 12 | `manim-gpu-encoding` (parcial); shaders sem dono |
| `mobject/svg` | 72 | 7 | 0 | `manim-svg-imagens` (`Brace*` mora aqui, mas é de `manim-mobjects`) |
| `animation/indication` | 72 | 9 | 0 | órfã — e muito usada em aula |
| `mobject/matrix` | 68 | 4 | 3 | `manim-tabelas-matrizes` |
| `constants` | 65 | 4 | 0 | `manim-layout-posicionamento` |
| `animation/specialized` | 62 | 1 | 0 | órfã (só `Broadcast`) |
| `utils/rate_functions` | 50 | 1 | 49 | `manim-composicao-ritmo` |
| `utils/space_ops` | 43 | 0 | 36 | `manim-mobjects-customizados` |
| `animation/transform` | 30 | 24 | 0 | `manim-animations` |
| `utils/bezier` | 22 | 0 | 17 | `manim-mobjects-customizados` |
| `animation/creation` | 17 | 14 | 0 | `manim-animations` |
| `animation/updaters` | 16 | 3 | 8 | `manim-updaters-valuetracker` |
| `utils/tex` | 16 | 3 | 11 | `manim-text-latex` |
| `config` | 14 | 3 | 7 | `manim-project`, `manim-performance-cache` |
| `mobject/vector_field` | 12 | 3 | 0 | órfã |
| `animation/core` | 8 | 3 | 2 | `manim-animations` · `manim-composicao-ritmo` |
| `animation/changing` | 7 | 2 | 0 | `manim-updaters-valuetracker` |
| `animation/growing` | 7 | 5 | 0 | `manim-animations` |
| `mobject/table` | 7 | 5 | 0 | `manim-tabelas-matrizes` |
| `animation/composition` | 6 | 4 | 0 | `manim-composicao-ritmo` |
| `animation/movement` | 6 | 5 | 0 | `manim-animations` (`MoveAlongPath`); `Homotopy`/`PhaseFlow` órfãos |
| `animation/rotation` | 6 | 2 | 0 | `manim-animations` |
| `mobject/graph` | 6 | 4 | 0 | `manim-grafos-redes` |
| `animation/fading` | 3 | 2 | 0 | `manim-animations` |
| `mobject/value_tracker` | 3 | 2 | 0 | `manim-updaters-valuetracker` |
| `animation/numbers` | 2 | 2 | 0 | `manim-updaters-valuetracker` |
| `animation/speed` | 2 | 1 | 0 | `manim-composicao-ritmo` (`ChangeSpeed`) |
| `mobject/logo` | 2 | 1 | 0 | órfã trivial (`ManimBanner`) |
| `plugins` | 2 | 0 | 2 | `manim-project` (**nenhum plugin instalado nesta máquina**) |
| `typing` | 1 | 0 | 0 | **só `TYPE_CHECKING`** — os aliases NÃO estão aqui (§11) |

Regenerável em 10 ms, sempre atual:

```bash
awk -F'\t' 'NR>1{t[$3]++; if($1=="class")c[$3]++; if($1=="function")f[$3]++}
     END{for(k in t) printf "%6d %4d %4d  %s\n", t[k], c[k]+0, f[k]+0, k}' \
  api/manim-ce-index.tsv | sort -rn
```

**Armadilha da categoria `other` (189 linhas, 7 classes, 15 funções):** ela é o
saco de gatos do `categorize()` — tudo que não casou com prefixo nenhum. Não
conclua nada dela; olhe a coluna `module`.

---

## 7. `toplevel.md` — e a marca `[só no topo]`

O arquivo lista tudo que `dir(manim)` expõe, agrupado: **classe (258) ·
constante/instância (69) · cor (89) · função (148) · submódulo/paleta (24) =
588 nomes**. (No ManimGL: 272 + 176 + 205 + 51 = **704**.)

E marca com `[só no topo]` o que existe no namespace mas **não** está no índice
— porque a varredura só indexa classes/funções cujo `__module__` começa com
`manim`, e valores não-chamáveis só se o nome for MAIÚSCULO ou o objeto for
cor. São **36 nomes na CE** (94 no GL), e vários deles são os que você mais usa:

```
config  logger  console  error_console  frame  version  np  unit  rate_functions
XKCD  X11  SVGNAMES  DVIPSNAMES  AS2700  BS381  manim_colors  ParsableManimColor
animation camera cli color constants core data_structures mobject opengl plugins
renderer scene typing utils  annotations  choose  cli_ctx_settings
ManimColorDType  PackageNotFoundError
```

Das 258 classes do topo, **256 estão no índice**. As duas de fora são
`ManimColorDType` (alias de dtype do numpy) e `PackageNotFoundError` (vem do
`importlib.metadata`) — as duas reprovam no teste de `__module__`.

Consequência prática, verificada: `bin/mx show config` responde *"'config' não
encontrado"*. Não é que não exista — é uma **instância**, e o índice guarda o
**tipo**:

```bash
bin/mx show ManimConfig      # 74 propriedades: pixel_width, frame_height, quality, tex_dir…
```

Regra: **`mx show` falhou num nome que você tem certeza de que existe? procure
o TIPO dele**, ou abra o `toplevel.md`.

---

## 8. `by-category.md` — a contagem do sumário ENGANA

O sumário diz "`animation/specialized` — 62 símbolos". São **1 classe
(`Broadcast`) e 61 constantes reexportadas**. Idem `animation/indication`: "72"
= 9 classes + 63 constantes; `utils/color`: "2335" = 4 classes + 15 funções +
2316 cores; `camera`: "138" = 8 classes + 130 constantes.

A causa é a mesma do §7: todo módulo que faz `from manim.constants import *`
carrega `UP`, `DOWN`, `PI`, `BLACK`… para dentro do próprio namespace, e a
varredura indexa o público de **cada** módulo. Use sempre a coluna `kind`
(§6) antes de tirar conclusão de tamanho.

O corpo do arquivo, esse, é bom: por classe ele traz assinatura, bases, a
primeira linha do doc e um `<details>` com os **métodos próprios** — que é
exatamente o recorte que interessa para "o que essa classe acrescenta". Os
herdados ficam de fora de propósito (seriam 49 044 linhas).

---

## 9. `inheritance.txt` — árvore de COBERTURA, e ela PERDE gente

Ela é gerada com um `seen` global e corte em profundidade 12
(`emit()` em `manimx/introspect.py`). São 337 linhas para 337 classes: **cada
classe aparece exatamente uma vez**, sob o primeiro pai que a alcança. Duas
consequências conhecidas:

- numa herança múltipla você não vê o segundo caminho — use o `herda de` do
  `mx show`, que lista todas as bases diretas;
- há **61 raízes**, e uma classe cujas bases estão todas fora do índice cai na
  raiz como se não herdasse de ninguém.

### O caso que quebra de verdade: base privada

`FadeIn` e `FadeOut` herdam de `_Fade`, que é privado e por isso nunca entra no
índice (§3). Resultado: os dois aparecem **como raiz** da árvore, e a família
`Animation` fica menor do que é. Medido:

```bash
$ awk 'f && /^[A-Za-z]/{exit} /^Animation$/{f=1} f' api/manim-ce-inheritance.txt | wc -l
73        # = a linha "Animation" + 72 descendentes

$ awk -F'\t' '$4=="Animation" && $5=="1"{print $1}' api/manim-ce-methods.tsv | sort -u | wc -l
74        # 74 descendentes
```

A diferença é exatamente `FadeIn` e `FadeOut` (conferido com `comm`). Ou seja:
**a árvore esconde duas das animações mais usadas do Manim.**

### A rota melhor: `defined_in` como reconstrutor de MRO

O truque vale para qualquer pergunta de herança, custa 20 ms e não depende da
árvore:

```bash
# quem DESCENDE de X (herdou algum método público dele)
awk -F'\t' '$4=="Animation" && $5=="1" {print $1}' api/manim-ce-methods.tsv | sort -u   # 74
awk -F'\t' '$4=="VMobject"  && $5=="1" {print $1}' api/manim-ce-methods.tsv | sort -u   # 133
awk -F'\t' '$4=="Mobject"   && $5=="1" {print $1}' api/manim-ce-methods.tsv | sort -u   # 146

# o MRO de uma classe, reconstruído
$ awk -F'\t' '$1=="Circle"{print $4}' api/manim-ce-methods.tsv | sort -u
Arc  Circle  Mobject  TipableVMobject  VMobject

$ awk -F'\t' '$1=="FadeIn"{print $4}' api/manim-ce-methods.tsv | sort -u
Animation  FadeIn  Transform          ← recupera Transform e Animation; só `_Fade` continua invisível
```

**A ordem sai alfabética, não a do MRO** — para saber quem ganha numa colisão de
default, é `inspect.getmro` ao vivo (§22). E o método só aparece se for público:
um ancestral que só define coisa privada não deixa rastro nenhum.

Ainda assim a árvore é a forma mais rápida de ver a família de relance:

```bash
awk 'f && /^[A-Za-z]/{exit} /^Animation$/{f=1} f' api/manim-ce-inheritance.txt
```

---

## 10. A pergunta que o índice quase não responde: "que kwargs isso aceita?"

Esta é a maior lacuna, e é a que mais gera código inventado.

Contado no índice (10 ms, reproduzível): **282 das 338 classes (83,4%)
terminam a assinatura em `**kwargs`**. Entre as 258 do topo, são **231 de 257
(89,9%)** pela assinatura, e **238 de 258 (92,2%)** olhando o `__init__` ao
vivo — a diferença é o caso `__new__` de §3. Para todas elas a assinatura do
índice é verdadeira e **incompleta**: o parâmetro que você quer mora no
`__init__` de um ancestral, e `methods.tsv` guarda **um único `__init__` por
classe**, o mais derivado.

```
$ bin/mx show Circle | sed -n 1p
class Circle(radius=None, color=ManimColor('#FC6255'), **kwargs) -> 'None'
```

Nada ali diz que `fill_opacity`, `stroke_width` e `z_index` são aceitos. São.

### Receita A — pelo ÍNDICE, sem importar o Manim (~90 ms)

A melhor relação custo/benefício. Usa o truque de §9: o conjunto de
`defined_in` dá o MRO indexado; para cada ancestral, pega o `__init__` **próprio**
(`$5=="0"`).

```bash
#!/usr/bin/env bash
# bin-local: kwargs-do-indice.sh <Classe>
set -euo pipefail
API=${API:-api/manim-ce-methods.tsv}
cls=$1
mro=$(awk -F'\t' -v c="$cls" '$1==c{print $4}' "$API" | sort -u)
[ -z "$mro" ] && { echo "classe $cls não está no índice de métodos"; exit 1; }
for anc in $mro; do
  awk -F'\t' -v a="$anc" '$1==a && $2=="__init__" && $5=="0" {print "["a"] "$6}' "$API"
done
```

Saída real para `Circle` (recortada; ordem alfabética, não a do MRO):

```
[Arc]              (self, radius=1.0, start_angle=0, angle=1.5707963267948966, num_components=9, arc_center=array([0., 0., 0.]))
[Circle]           (self, radius=None, color=ManimColor('#FC6255'), **kwargs)
[Mobject]          (self, color=ManimColor('#FFFFFF'), name=None, dim=3, target=None, z_index=0)
[TipableVMobject]  (self, tip_length=0.35, normal_vector=array([0., 0., 1.]), tip_style=None)
[VMobject]         (self, fill_color=None, fill_opacity=0.0, stroke_color=None, stroke_opacity=1.0,
                    stroke_width=4, background_stroke_color=ManimColor('#000000'), …19 no total)
```

E para `Circumscribe`, o caso que resolve a dúvida "posso passar `run_time`
aqui?":

```
[Circumscribe]     (self, mobject, shape=<class '…Rectangle'>, fade_in=False, fade_out=False, time_width=0.3, …)
[Succession]       (self, lag_ratio=1)
[AnimationGroup]   (self, group=None, run_time=None, rate_func=<function linear …>, lag_ratio=0, …)
[Animation]        (self, mobject, lag_ratio=0.0, run_time=1.0, rate_func=<function smooth …>, …)
```

**Onde a receita A falha, e é honesto saber:** quando o MRO passa por uma classe
**privada** (§3, §9). `FadeIn`:

```
$ kwargs-do-indice.sh FadeIn
[Animation]  (self, mobject, lag_ratio=0.0, run_time=1.0, rate_func=<smooth>, …)
[FadeIn]     (self, *mobjects: 'Mobject', **kwargs: 'Any')
[Transform]  (self, mobject, target_mobject=None, path_func=None, path_arc=0, …)
```

Nenhum dos três traz `shift`, `scale` ou `target_position` — que são os kwargs
que a gente de fato usa em `FadeIn(texto, shift=UP*0.3)`. Eles moram em `_Fade`,
e conferi ao vivo:

```python
_Fade.__init__(self, *mobjects, shift=None, target_position=None, scale=1, **kwargs)
```

**Nenhuma consulta ao índice consegue chegar nesse `shift`.** As duas saídas são
o fonte (20 ms) —

```bash
grep -n "class _Fade" -A 20 .venv/lib/python3.12/site-packages/manim/animation/fading.py
```

— ou a receita B.

### Receita B — MRO ao vivo (1,7 s, nunca erra)

```python
# kwargs_de.py — .venv/bin/python kwargs_de.py Circle
import inspect, sys, warnings
warnings.filterwarnings("ignore")
import manim

cls = getattr(manim, sys.argv[1])
for klass in cls.__mro__:
    init = vars(klass).get("__init__")          # só o __init__ que a classe DEFINE
    if init is None:
        continue
    params = [p for p in inspect.signature(init).parameters.values()
              if p.name != "self" and p.kind not in (p.VAR_KEYWORD, p.VAR_POSITIONAL)]
    if params:
        print(f"[{klass.__name__}]  " + ", ".join(str(p) for p in params))
```

É a única que enxerga classe privada, e a única que dá a **ordem real do MRO**
(`FadeIn → _Fade → Transform → Animation → object`, conferido). Use quando a
receita A vier vazia ou incompleta, e sempre que a classe estiver na lista das
27 com base ausente do índice.

**Quando nenhuma das duas se aplica:** função não tem MRO. Para função,
`bin/mx show nome` já dá a assinatura completa, porque função não herda nada.

### A pergunta inversa: "quem aceita este kwarg?"

```python
# quem_aceita.py — .venv/bin/python quem_aceita.py time_width
import inspect, sys, warnings
warnings.filterwarnings("ignore")
import manim

alvo, achou = sys.argv[1], []
for n in sorted(dir(manim)):
    o = getattr(manim, n)
    if not inspect.isclass(o):
        continue
    for k in o.__mro__:
        init = vars(k).get("__init__")
        if init and alvo in inspect.signature(init).parameters:
            achou.append(f"{n} (de {k.__name__})")
            break
print(f"{alvo!r}: {len(achou)} classes do topo\n  " + ", ".join(achou[:14]))
```

Medido [não reverificado — 2026-08-19]: `sheen_factor` → 132 classes (todas via
`VMobject`); `tip_length` → 27 (via `TipableVMobject`); `time_width` → **5**
(`ApplyWave`, `Circumscribe`, `Flash`, `ShowPassingFlash`,
`ShowPassingFlashWithThinningStrokeWidth`, cada uma definindo o próprio). Esse
"5" é a resposta certa para "posso passar `time_width` aqui?".

A versão barata, só pelo índice, responde a metade da pergunta (quem define,
não quem herda) em 20 ms:

```bash
awk -F'\t' '$2=="__init__" && $5=="0" && $6 ~ /time_width/ {print $1}' api/manim-ce-methods.tsv
```

### A boa notícia: kwarg errado falha ALTO

```python
Circle(raio=2)
# TypeError: Mobject.__init__() got an unexpected keyword argument 'raio'
```

O Manim **não** engole kwarg desconhecido. Mas repare na mensagem: ela acusa
`Mobject.__init__()` mesmo quando você chamou `Circle(...)` — porque o
`**kwargs` desceu o MRO inteiro e quem estourou foi o último elo. Não procure
`raio` no `Mobject`; o erro só diz "ninguém no MRO aceitou isso".

Isso vale para **construtor**. Para atributo, a história é o oposto — §13.

---

## 11. Ler uma assinatura do índice sem se enganar

As assinaturas vêm de `str(inspect.signature(obj))` com caminhos saneados. Cinco
coisas nelas confundem quem grepa:

**1. As anotações são strings entre aspas.** O Manim usa `from __future__ import
annotations`, então a anotação chega ao `repr` como texto:
`radius: 'float | None' = None`. Quem procurar `radius: float` não acha nada —
procure `radius:` e leia.

**2. Os defaults são `repr()`, não literais que você possa colar.** Conferido no
índice:

| forma | onde aparece | exemplo |
|---|---:|---|
| `array([0., 0., 0.])` | 557 linhas do `index.tsv` | `arc_center: 'Point3DLike' = array([0., 0., 0.])` |
| `<function smooth at 0x713b…>` | 21 no `index.tsv`, 561 no `methods.tsv` | `rate_func = <function smooth at 0x…>` |
| `<CapStyleType.AUTO: 0>` | membro de Enum | `cap_style: 'CapStyleType' = <CapStyleType.AUTO: 0>` |
| `<class 'manim.…Rectangle'>` | 22 no `index.tsv` | `shape: 'type[Rectangle] \| type[Circle]' = <class '…'>` |
| `PosixPath('<site-packages>/…')` | 2 no `index.tsv` | `SHADER_FOLDER`, `MANIM_ROOT` |

O endereço `at 0x…` **muda a cada varredura** — é o ruído de §21, não uma
mudança de API. E `<site-packages>` é substituição deliberada
(`_scrub_paths`), para o índice não vazar o nome de usuário da máquina.

**3. `-> 'Self'` significa encadeável.** É a convenção do Manim para "devolvo eu
mesmo". `Circle` tem **148** métodos assim (`awk '$1=="Circle" && $6 ~ /Self/'`)
— todos aceitam `.animate` e todos podem ser postos em cadeia (§14).

**4. Os ALIASES DE TIPO não estão no índice.** Este é o buraco silencioso.
Contado nas assinaturas do `index.tsv`:

| alias | ocorrências | está no índice? | onde está de verdade |
|---|---:|:-:|---|
| `Point3DLike` | 51 | **não** | `manim/typing.py:386` — `Point3D \| tuple[float, float, float]` |
| `ParsableManimColor` | 43 | **não** (só `[só no topo]`) | `manim/utils/color/core.py:1214` — `ManimColor \| int \| str \| IntRGBLike \| FloatRGBLike \| IntRGBALike \| FloatRGBALike` |
| `Vector3DLike` | 30 | **não** | `manim/typing.py:503` — `NDArray[PointDType] \| tuple[float, float, float]` |
| `Point3DLike_Array` | 9 | **não** | `manim/typing.py:402` |
| `RateFunction` | 9 | **sim** (é `class`, um `Protocol` com `__call__`) | `utils/rate_functions` |
| `PixelArray` | — | **não** | `manim/typing.py:958` |

A categoria `typing` tem **uma linha só**, e é `TYPE_CHECKING`. Ou seja: quando
a assinatura diz `arc_center: 'Point3DLike'`, o índice não sabe o que isso é.
A resposta está a 20 ms:

```bash
grep -n "^Point3DLike\|^Vector3DLike\|^Point2DLike" .venv/lib/python3.12/site-packages/manim/typing.py
```

Na prática, os três primeiros querem dizer a mesma coisa: **você pode passar uma
tupla de três floats onde a assinatura pede um "Point3DLike"** — `LEFT`,
`[1, 0, 0]` e `np.array([1., 0., 0.])` são todos aceitos.

**5. `*args` / `**kwargs` na assinatura não são decoração.** `Cutout(main_shape,
*mobjects, **kwargs)` aceita N formas posicionais; `AnimationGroup(*animations,
…)` idem. Se a assinatura abre com `*`, os posicionais são o conteúdo, não os
parâmetros.

---

## 12. O fonte instalado é a sétima fonte — e responde o que as outras seis não respondem

```bash
MANIM_SRC=.venv/lib/python3.12/site-packages/manim        #  6,4 MiB · 168 arquivos .py
MANIMGL_SRC=.venv-gl/lib/python3.12/site-packages/manimlib #  2,7 MiB · 100 arquivos .py
```

Um `grep -rIn` no primeiro custa **20 ms medidos** — mais barato que o `mx`, e é
a única fonte que nunca omite. Ele responde:

| pergunta | por que só ele responde |
|---|---|
| o docstring INTEIRO | o índice guarda só a 1ª linha (§4, §5) |
| o CORPO de um método | nenhum índice guarda corpo |
| classe/função **privada** (`_Fade`, `_BooleanOps`, `_ScaleBase`) | a varredura pula tudo que começa com `_` (§3) |
| membro de Enum, atributo de classe | `_class_members` não os coleta (§3) |
| alias de tipo (`Point3DLike`) | não é classe nem função nem constante MAIÚSCULA (§11) |
| decorador (`@override_animate`, `@deprecated`, `@property`) | não é indexado |
| o valor real de uma constante calculada | o índice guarda o `repr` no momento do dump |

Receitas:

```bash
# o docstring inteiro de um método, sem importar nada
grep -n "def get_riemann_rectangles" -A 60 $MANIM_SRC/mobject/graphing/coordinate_systems.py

# em que arquivo mora um conceito (20 ms para o pacote inteiro)
grep -rIln "riemann" $MANIM_SRC/

# a definição de uma classe privada que apareceu num `herda de`
grep -rn "^class _Fade" -A 25 $MANIM_SRC/

# quem usa um decorador
grep -rn "@override_animate" $MANIM_SRC/

# todos os tampões da biblioteca
grep -rn "raise NotImplementedError" $MANIM_SRC/
```

### Achado: **a CE 0.21 não marca NADA como depreciado**

O Manim tem os decoradores `deprecated` e `deprecated_params`
(`manim/utils/deprecation.py`, os dois indexados em `utils/other`). Varredura do
pacote inteiro atrás de **usos**:

```bash
$ grep -rn "^\s*@deprecated" $MANIM_SRC/ | grep -v utils/deprecation.py
.venv/…/manim/cli/default_group.py:159:    @deprecated
```

Uma única aplicação, num utilitário de CLI que nem entra no índice. E o índice
confirma o outro lado: `awk -F'\t' 'tolower($6) ~ /deprecat/'` no `index.tsv`
devolve só as duas funções decoradoras, e o mesmo teste na coluna de doc do
`methods.tsv` devolve **zero linhas**.

Duas conclusões, e as duas importam:

1. **Nenhuma fonte deste projeto sabe dizer o que está depreciado.** Se uma
   skill afirma "X está depreciada", ou ela cita o fonte, ou é opinião de
   idiomatismo. Conferido no fonte: `ApplyMethod` (`animation/transform.py:454`)
   **não tem decorador nenhum** — ela é desaconselhada por estilo (use
   `.animate`), não pela biblioteca.
2. O único `DeprecationWarning` que você vai encontrar de verdade na CE 0.21 é
   emitido **em tempo de execução**, pelo `__getattr__` do `Mobject` — §13.

---

## 13. Métodos que não existem — mas respondem

Esta é a armadilha mais perigosa da descoberta, porque ela **derrota o
`hasattr`**. `Mobject.__getattr__` (`$MANIM_SRC/mobject/mobject.py:729`)
sintetiza um método para **qualquer** atributo que comece com `get_` ou `set_`:

```python
def __getattr__(self, attr):
    if attr.startswith("get_"):
        to_get = attr[4:]
        def getter(self):
            warnings.warn("This method is not guaranteed to stay around. Please prefer "
                          "getting the attribute normally.", DeprecationWarning, stacklevel=2)
            return getattr(self, to_get)
        return types.MethodType(getter, self)
    if attr.startswith("set_"):
        to_set = attr[4:]
        def setter(self, value):
            warnings.warn(..., DeprecationWarning, stacklevel=2)
            setattr(self, to_set, value)
            return self
        return types.MethodType(setter, self)
    raise AttributeError(f"{type(self).__name__} object has no attribute '{attr}'")
```

Comportamento medido:

```python
>>> c = Circle()
>>> hasattr(c, "set_banana")      # True  (!)
>>> hasattr(c, "get_banana")      # True  (!)
>>> c.set_banana(3) is c          # True — e grava c.banana = 3
>>> c.set_banana(1, 2)            # TypeError: setter() takes 2 positional arguments but 3 were given
>>> c.get_inexistente()           # AttributeError: Mobject object has no attribute 'inexistente'
>>> c.metodo_inventado()          # AttributeError — nome sem prefixo falha na hora
```

Quatro coisas que caem daí, e nenhuma é óbvia:

1. **`hasattr(mob, "set_qualquer_coisa")` é sempre `True`**, e a chamada sempre
   "funciona": grava um atributo que ninguém lê e não desenha nada. Não há erro,
   o render sai limpo e o quadro sai errado.
2. **O setter sintetizado tem aridade 1.** `set_color(RED, family=False)` só
   funciona porque `set_color` é um método REAL do `VMobject`; num nome
   inventado o segundo argumento vira `TypeError` — o que, ironicamente, é a
   melhor rede de segurança que existe aqui.
3. **A mensagem do `AttributeError` nomeia o atributo DESPIDO do prefixo.**
   Você chamou `get_inexistente()` e o Python fala de `'inexistente'`. Quem
   procurar `get_inexistente` no fonte não acha, e conclui coisa errada.
4. A camada **não interfere** em `get_*`/`set_*` de verdade — `__getattr__` só
   dispara quando a busca normal falha. Por isso ela é invisível até o dia em
   que não é.

**Corolário: `hasattr` não é verificação para nomes `get_*`/`set_*`.** A
verificação é o índice:

```bash
awk -F'\t' '$2=="set_width" {print $1"\t"$4}' api/manim-ce-methods.tsv | sort -u
#   OpenGLMobject   OpenGLMobject        ← e mais ninguém
```

`set_width` é método REAL **só** no `OpenGLMobject`. No caminho cairo ele é
sintético e emite `DeprecationWarning: This method is not guaranteed to stay
around. Please prefer setting the attribute normally or with Mobject.set().`
O idiomático, tudo conferido no `mx show Mobject`:

```python
mob.width = 3                  # `width` é PROPRIEDADE — e propriedade não está em TSV nenhum (§5)
mob.set(width=3)               # Mobject.set(**kwargs) -> Self
mob.scale_to_fit_width(3)      # Mobject.scale_to_fit_width(width, **kwargs) -> Self
mob.match_width(outro)         # Mobject.match_width(mobject, **kwargs) -> Self
```

Propriedades de `Mobject`, as cinco: `always`, `animate`, `depth`, `height`,
`width`. Todo `get_X`/`set_X` sobre elas é açúcar depreciado.

> Isto é matéria de descoberta, não de uso. **Como** dimensionar e posicionar é
> `manim-layout-posicionamento`; o catálogo de formas é `manim-mobjects`.

---

## 14. Encadeamento, `.animate`, overrides e `set_default`

Quase todo método de `Mobject` que devolve `Self` encadeia e aceita `.animate`:

```python
circle.set_color(RED).shift(UP).scale(2)            # estático
self.play(circle.animate.set_color(RED).shift(UP))  # animado
```

`animate` e `always` **não são métodos** — são propriedades (aparecem na linha
"propriedades" do `mx show`, nunca na lista de métodos, e não estão em TSV
nenhum). `c.animate` devolve um `_AnimationBuilder`; `c.always` devolve um
`_UpdaterBuilder`.

### Overrides: são DOIS decoradores parecidos, e trocá-los custa caro

**Correção.** Uma versão anterior desta skill tratava os dois como um só. Eles
não são intercambiáveis, e a diferença muda o resultado do `grep`:

| Decorador | Onde mora | O que substitui | Atributo gravado |
|---|---|---|---|
| `@override_animate(metodo)` | `mobject/mobject.py:3540-3553` | o método sob **`.animate`** (`mob.animate.metodo()`) | `_override_animate` |
| `@override_animation(Classe)` | `animation/animation.py:725-765` | uma **classe de `Animation`** inteira (`Create(mob)`) | `_override_animation` |

Os dois sítios de uso, **[FONTE]** `grep -rn` no pacote instalado:

```bash
grep -rn "@override_animate\b"   $MANIM_SRC/   # 4 reais + 2 em docstring
grep -rn "@override_animation\b" $MANIM_SRC/   # 1 real + 1 em docstring
```

- `@override_animate` — **`GenericGraph.add_vertices` / `remove_vertices` /
  `add_edges` / `remove_edges`** (`mobject/graph.py:922, 1003, 1127, 1182`). Os
  hits de `mobject.py:3531` e `opengl/opengl_mobject.py:3177` estão **dentro de
  docstring**, não são registros.
- `@override_animation` — **`ManimBanner.create`** (`mobject/logo.py:206`,
  substituindo `Create`). O hit de `animation/animation.py:754` é docstring.

Ou seja: `ManimBanner` **não** aparece no `grep` por `@override_animate`. Uma
versão anterior o listava ali; procurar o `.animate` de `ManimBanner` com esse
grep devolve o vazio e induz a conclusão errada.

E há um detalhe que só o fonte conta
(`$MANIM_SRC/mobject/mobject.py:3441-3446`): o `__getattr__` do
`_AnimationBuilder` testa `hasattr(method, "_override_animate")` e levanta

```
NotImplementedError: Method chaining is currently not supported for overridden animations
```

Repare em **qual** atributo ele testa: é o do `@override_animate`. Logo a
exceção vale para `g.animate.add_vertices(...).shift(UP)` (um `GenericGraph`),
**não** para `banner.animate.create()` — `ManimBanner.create` carrega
`_override_animation`, que esse teste não enxerga. A limitação é do encadeamento
sob `.animate`, e a única família que a sofre hoje é a de grafos (§15).

### `set_default` — três definições em toda a biblioteca

```bash
$ awk -F'\t' '$2=="set_default" && $5=="0"{print $1"\t"$3"\t"$6}' api/manim-ce-methods.tsv
Animation        classmethod  (**kwargs) -> 'None'
Mobject          classmethod  (**kwargs: 'Any') -> 'None'
OpenGLMobject    classmethod  (**kwargs: 'Any') -> 'None'
```

Descoberta é isso: em uma linha você sabe que o mecanismo existe, que é
`classmethod`, e que vale para toda animação e todo mobject. **Para que serve e
o que ele NÃO alcança é `manim-color-theming` §10** — não repita a conta aqui.

### Só três classes são chamáveis

```bash
$ awk -F'\t' '$2=="__call__" && $5=="0"{print $1}' api/manim-ce-methods.tsv | sort -u
HealthCheckFunction   LayoutFunction   RateFunction
```

As duas últimas são `Protocol` — é por isso que `utils/rate_functions` tem "50
símbolos" sendo 49 funções + 1 classe, e por que `LayoutFunction` é o tipo que
você implementa para dar um layout próprio a um `Graph`
(`manim-grafos-redes`).

---

## 15. O índice cobre mais que o namespace — e isso confunde

A varredura importa **167 submódulos** do pacote e indexa o público de cada um.
`from manim import *` traz menos. Contado:

- **337 classes no índice**, das quais **256 estão no topo** e **81 NÃO estão**.

Exemplos que doem: `GenericGraph`, `LayoutFunction`, `ManimConfig`,
`MarkupUtils`, `AbstractImageMobject`, `ConvertToOpenGL`, `Mesh`, `Object3D`,
`DefaultGroup`, `Cell`, `Facet` — e **41 das 44 classes `OpenGL*`** (só
`OpenGLPMobject`, `OpenGLPGroup` e `OpenGLPMPoint` chegam ao topo;
`OpenGLCircle` e companhia, não).

```python
from manim import GenericGraph
# ImportError: cannot import name 'GenericGraph' from 'manim'
```

**A coluna 5 (`module`) do `index.tsv` é a resposta**: ela diz o caminho de
import correto (`manim.mobject.graph`). Regra: `mx find` achou → antes de
escrever `from manim import X`, cheque se `X` está no `toplevel.md`; se não
estiver, importe pelo módulo.

### E o que a varredura NÃO vê

`collect_api` (`manimx/introspect.py:229` — a versão anterior desta skill dizia
228) indexa, por módulo:

- nomes **públicos** (sem `_` inicial) — classe/função privada não entra (§3);
- classe e função **cujo `__module__` começa com o pacote** — reexport de numpy,
  PIL, `importlib.metadata` fica de fora (é por isso que `PackageNotFoundError`
  e `ManimColorDType` aparecem no `toplevel.md` mas não no índice);
- valor não-chamável **só se o nome for MAIÚSCULO ou o objeto for cor** — não há
  nenhuma constante minúscula no índice, conferido;
- de cada classe: métodos, `classmethod`, `staticmethod` e propriedades, pulando
  todo `_privado` e todo dunder **exceto `__init__` e `__call__`**;
- **atributo de classe, não** (§3).

E, no arquivo gravado, a **propriedade só sobrevive no `.json.gz`** (§5).

Caminhos locais nos valores padrão são saneados para `<site-packages>` /
`<repo>` / `<home>` — por isso `SHADER_FOLDER` aparece como
`PosixPath('<site-packages>/manim/renderer/shaders')` e não com o seu usuário.

**4 dos 167 submódulos falham ao importar** e somem do índice em silêncio
[não reverificado — 2026-08-19]
(`logger.debug`). Conferido, e nenhum deles serve para fazer vídeo:
`utils.docbuild.autoaliasattr_directive`, `utils.docbuild.autocolor_directive`
(faltam `docutils`), `utils.docbuild.manim_directive` (falta `jinja2`) e
`utils.testing.frames_comparison` (falta `pytest`).

---

## 16. Conferir uma cena INTEIRA sem renderizar

Junta as duas verificações — nome e kwarg — num passe estático. É o que
transforma "eu conferi o que lembrei de conferir" em "não sobrou nada por
conferir".

```python
#!/usr/bin/env python
"""conferir_cena.py — .venv/bin/python conferir_cena.py cena.py

Pega dois erros que só apareceriam depois de esperar o render:
  1. nome que não existe em `from manim import *`;
  2. kwarg que a classe (nem nenhum ancestral dela) aceita.
"""
from __future__ import annotations
import ast, builtins, inspect, sys, warnings
warnings.filterwarnings("ignore")
import manim

TOPO = {n for n in dir(manim) if not n.startswith("_")}
BUILTINS = set(dir(builtins)) | {"__file__", "__name__", "__doc__", "__package__"}


def kwargs_aceitos(cls: type) -> set[str] | None:
    nomes: set[str] = set()
    for klass in cls.__mro__:
        init = vars(klass).get("__init__")
        if init is None:
            continue
        try:
            sig = inspect.signature(init)
        except (TypeError, ValueError):
            return None
        for p in sig.parameters.values():
            if p.name == "self" or p.kind in (p.VAR_KEYWORD, p.VAR_POSITIONAL):
                continue
            nomes.add(p.name)
    return nomes


def conferir(caminho: str) -> int:
    arvore = ast.parse(open(caminho, encoding="utf-8").read(), caminho)
    definidos: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definidos.add(no.name)
        elif isinstance(no, ast.arg):
            definidos.add(no.arg)
        elif isinstance(no, ast.Name) and isinstance(no.ctx, (ast.Store, ast.Del)):
            definidos.add(no.id)
        elif isinstance(no, (ast.Import, ast.ImportFrom)):
            for a in no.names:
                definidos.add(a.asname or a.name.split(".")[0])
        elif isinstance(no, ast.ExceptHandler) and no.name:
            definidos.add(no.name)

    problemas = 0
    for no in ast.walk(arvore):
        if isinstance(no, ast.Name) and isinstance(no.ctx, ast.Load):
            if no.id in definidos or no.id in BUILTINS or no.id in TOPO:
                continue
            print(f"{caminho}:{no.lineno}: nome desconhecido: {no.id!r}")
            problemas += 1
        elif isinstance(no, ast.Call) and isinstance(no.func, ast.Name):
            obj = getattr(manim, no.func.id, None)
            if not inspect.isclass(obj) or no.func.id in definidos:
                continue
            aceitos = kwargs_aceitos(obj)
            if aceitos is None:
                continue
            for kw in no.keywords:
                if kw.arg and kw.arg not in aceitos:
                    print(f"{caminho}:{no.lineno}: {no.func.id}(...) não aceita "
                          f"o kwarg {kw.arg!r}")
                    problemas += 1
    print(f"{caminho}: {problemas} problema(s)")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(max(conferir(a) for a in sys.argv[1:]))
```

Numa cena com três erros plantados, ele acha os três:

```
cena_com_erro.py:6: Text(...) não aceita o kwarg 'tamanho'
cena_com_erro.py:7: Rectangle(...) não aceita o kwarg 'cor'
cena_com_erro.py:8: nome desconhecido: 'ShowCreation'
```

**Calibração** [não reverificada — 2026-08-19]: rodado nos 11 arquivos de cena
de produção do deck `~/Projects/aulas` mais o `scenes/exemplos.py` deste repo →
**0 falso positivo** nos 12. (O único que existia era `__file__`, um dunder de
módulo; está na lista de builtins acima.)

### Os quatro limites dele, e como cobrir cada um

| limite | por quê | o que fazer |
|---|---|---|
| não confere **nome de método** (`c.set_widht(3)`) | `hasattr` mente para `get_*`/`set_*` (§13), e um AST não sabe o tipo de `c` | `awk '$2=="set_widht"' methods.tsv` no que for suspeito |
| **`Scene`/`CenaBase` importada de outro módulo** vira "nome desconhecido"? não | os `import` entram em `definidos` | — |
| kwarg de classe **não indexada** que você importou pelo módulo | `getattr(manim, nome)` devolve `None` e ele pula | conferir à mão com a receita B (§10) |
| valor errado dentro de kwarg certo, objeto fora do quadro, branco no branco, sobreposição, ordem de desenho | isso é pixel, não sintaxe | o ciclo **escrever → renderizar rápido → OLHAR o PNG → corrigir** — `manim-verificacao-visual` é o dono, `manim-render-api` dá o comando |

Este conferidor é o **passo 0**, não o passo final.

---

## 17. Receitas de `grep`/`awk`

```bash
# ---------- existência e assinatura ----------
# Existe? — o teste mais barato que existe, < 10 ms
grep -qP '^class\tCircumscribe\t' api/manim-ce-index.tsv && echo existe || echo NÃO EXISTE

# Um nome é único? (antes de confiar no `mx show`)
awk -F'\t' -v n=Polygon '$2==n {print $1"\t"$3"\t"$5}' api/manim-ce-index.tsv | sort -u

# Todas as animações que existem  →  77 nomes
awk -F'\t' '$1=="class" && $3 ~ /^animation/ {print $2}' api/manim-ce-index.tsv | sort -u

# Geometrias com a assinatura inteira
awk -F'\t' '$1=="class" && $3=="mobject/geometry" {print $2"\t"$4}' api/manim-ce-index.tsv

# As 49 rate functions (a 50ª entrada da categoria é o protocolo `RateFunction`)
awk -F'\t' '$1=="function" && $3=="utils/rate_functions" {print $2}' api/manim-ce-index.tsv | sort -u

# Contagem ACIONÁVEL por categoria (sem as constantes reexportadas)
awk -F'\t' 'NR>1 && $1!="constant" {c[$3]++} END{for(k in c) printf "%5d  %s\n", c[k], k}' \
  api/manim-ce-index.tsv | sort -rn

# ---------- métodos ----------
# Quem tem o método `plot`, e quem o DEFINE
awk -F'\t' '$2=="plot" {print $1" <- "$4}' api/manim-ce-methods.tsv | sort -u
#   Axes, BarChart, ComplexPlane, NumberPlane, PolarPlane, ThreeDAxes <- CoordinateSystem
awk -F'\t' '$2=="plot" && $5=="0" {print $1"\t"$6}' api/manim-ce-methods.tsv
#   CoordinateSystem  (self, function, x_range=None, use_vectorized=False, colorscale=None, …)

# Só os métodos que a classe DEFINE (coluna 5 == 0)
awk -F'\t' '$1=="Axes" && $5=="0" {print $2}' api/manim-ce-methods.tsv
#   __init__ coords_to_point get_axes get_axis_labels plot_line_graph point_to_coords

# Tudo que é encadeável numa classe (devolve `Self`)  →  148 em Circle
awk -F'\t' '$1=="Circle" && $6 ~ /Self/ {print $2$6}' api/manim-ce-methods.tsv

# Só classmethod / staticmethod (a coluna 3 do methods.tsv)
awk -F'\t' '$3=="classmethod" && $5=="0" {print $1"."$2}' api/manim-ce-methods.tsv | sort -u

# ---------- herança (§9) ----------
awk -F'\t' '$1=="FadeIn"{print $4}' api/manim-ce-methods.tsv | sort -u          # o MRO indexado
awk -F'\t' '$4=="Animation" && $5=="1"{print $1}' api/manim-ce-methods.tsv | sort -u   # descendentes
awk 'f && /^[A-Za-z]/{exit} /^Animation$/{f=1} f' api/manim-ce-inheritance.txt         # a família de relance

# ---------- kwargs (§10) ----------
for a in $(awk -F'\t' '$1=="Circle"{print $4}' api/manim-ce-methods.tsv | sort -u); do
  awk -F'\t' -v a="$a" '$1==a && $2=="__init__" && $5=="0"{print "["a"] "$6}' api/manim-ce-methods.tsv
done
# quem DEFINE um kwarg (não pega quem herda)
awk -F'\t' '$2=="__init__" && $5=="0" && $6 ~ /time_width/ {print $1}' api/manim-ce-methods.tsv

# ---------- constantes e cor (§18) ----------
grep -P '^constant\tBLUE_D\t' api/manim-ce-index.tsv                # leia sempre a coluna 5
awk -F'\t' '$1=="constant" && $2=="MAROON"{print $4"\t"$5}' api/manim-ce-index.tsv | sort -u
# nomes de constante com MAIS DE UM valor  →  165
awk -F'\t' '$1=="constant"{print $2"\t"$4}' api/manim-ce-index.tsv | sort -u \
  | awk -F'\t' '{c[$1]++} END{n=0; for(k in c) if(c[k]>1) n++; print n}'

# ---------- o fonte (§12) ----------
grep -rIln "riemann" .venv/lib/python3.12/site-packages/manim/
grep -rn "^class _Fade" -A 25 .venv/lib/python3.12/site-packages/manim/
```

---

## 18. Cor: o NOME não identifica a cor

Uma versão antiga desta skill dizia que as constantes duplicadas têm sempre o
mesmo valor. **Está errado.** Contado no índice: **165 nomes de constante têm
mais de um valor distinto**, e os 165 são cores (nenhuma constante não-cor
diverge — conferido).

O pior caso é `MAROON`, com **seis** valores:

```
$ awk -F'\t' '$1=="constant" && $2=="MAROON"{print $4"\t"$5}' api/manim-ce-index.tsv | sort -u
ManimColor('#471B21')   manim.utils.color.BS381
ManimColor('#650021')   manim.utils.color.XKCD
ManimColor('#7F0000')   manim.utils.color.SVGNAMES
ManimColor('#AF3235')   manim.utils.color.DVIPSNAMES
ManimColor('#B03060')   manim.utils.color.X11
ManimColor('#C55F73')   manim                      ← o que `from manim import *` dá
```

`SALMON` e `PURPLE` têm 5; `RED`, `GREEN`, `BLUE`, `YELLOW`, `TURQUOISE` e mais
uma dúzia têm 4; `TEAL` tem 3 (`#5CD0B3` no manim, `#007F7F` no SVGNAMES,
`#029386` no XKCD).

Duas regras que caem daí:

1. **Ao ler uma cor do índice, leia a coluna 5.** Só a linha com módulo `manim`
   (ou `manim.utils.color.manim_colors`) é a que o `import *` entrega.
2. **Nome de paleta precisa de prefixo.** `from manim import BLOODRED` levanta
   `ImportError`; o índice diz `manim.utils.color.XKCD`, então o certo é
   `from manim.utils.color import XKCD` e `XKCD.BLOODRED` (`#980002`).

Tamanho de cada paleta no índice: XKCD 922 · X11 504 · BS381 287 · AS2700 206 ·
SVGNAMES 151 · manim_colors 89 · DVIPSNAMES 68.

Para **usar** cor (paleta do tema, gradiente, contraste, `set_default`,
transparência), a skill é `manim-color-theming` — ela tem os 25 métodos de
`ManimColor` e a auditoria WCAG. Aqui só se resolve "qual é o valor e de onde
importar".

---

## 19. CE × GL — a mesma palavra, duas APIs

`api/ce-vs-gl.md` é gerado por reflexão dos **dois pacotes instalados**
(`mx api-diff`), não copiado de blog. Números conferidos:

| | ManimCE 0.21.0 | ManimGL 1.7.2 |
|---|---:|---:|
| import / CLI | `from manim import *` · `manim` | `from manimlib import *` · `manimgl` |
| classes públicas | 337 | 270 |
| funções públicas | 281 | 216 |
| só nesta edição | 184 | 117 |
| nome em comum | 153 | 153 |
| **desses 153, com assinatura diferente** | **153** | **153** |

**100% das classes homônimas têm assinatura diferente.** Nome igual nunca é
prova de API igual — e o modo de falha é silencioso, porque o import funciona e
o construtor aceita. O exemplo canônico, direto do arquivo:

```
AnnularSector   CE: (inner_radius=1, outer_radius=2, angle=π/2, start_angle=0, …)
                GL: (angle=π/2, start_angle=0.0, inner_radius=…, …)
```

Copiar `AnnularSector(1, 2, PI)` de um tutorial do 3b1b não dá erro nenhum: dá
outra figura.

Seções do arquivo: `## Resumo`, `## Renomeações e mudanças de fluxo` (tabela
`ShowCreation`→`Create`, `TexMobject`→`MathTex`, `GraphScene`→`Axes`,
`get_graph`→`Axes.plot`, `CONFIG`→kwargs, com coluna "existe?" gerada por
reflexão), `## Classes só no ManimCE (184)`, `## Classes só no ManimGL (117)`,
`## Nome igual, assinatura diferente (153 de 153)`.

Na prática:

```bash
bin/mx find ShowCreation                    # exit 1 — não existe na CE
bin/mx find ShowCreation --package manimgl  # existe: manimlib.animation.creation
bin/mx show ShowCreation --package manimgl --own-only
grep -n '`AnnularSector`' api/ce-vs-gl.md   # a linha das duas assinaturas
```

Para trabalhar **dentro** do ManimGL (flags, `custom_config.yml`, teclas da
janela, fluxo do 3b1b), a skill é `manimgl-3b1b`.

---

## 20. Descobrir as cenas de um ARQUIVO (`mx scenes`)

```bash
bin/mx scenes scenes/exemplos.py           # nome, bases, primeira linha do docstring
bin/mx scenes scenes/exemplos.py --json    # [{"name":…, "bases":[…], "doc":…}]
```

O filtro é `issubclass(obj, Scene) and obj.__module__ == module_name`
(`manimx/render.py:144`) e a ordem é a de **definição no arquivo**
(`__firstlineno__`), não alfabética. São **duas** condições independentes, e as
duas foram testadas ao vivo com um arquivo de laboratório
[não reverificado — 2026-08-19]:

```python
from base import CenaBase        # subclasse de Scene, mas de OUTRO módulo
class _AtosDemo:  ...            # mixin: não herda de Scene
class DemoP1(_AtosDemo, CenaBase): ...
class Solta(Scene): ...
```

```
$ bin/mx scenes demo.py
DemoP1   (_AtosDemo, CenaBase)  — Parte 1.
Solta    (Scene)                — Cena normal.
```

`CenaBase` sumiu por **`__module__`** (veio de `base.py`); `_AtosDemo` sumiu por
**herança**. Cada filtro protege um padrão diferente: a base de tema importada
some sozinha; o mixin de cena-em-partes some porque não herda de `Scene`. Quem
usa esse formato é a skill `manim-presentation-parts` — o "por quê" está lá, e
inverter isso (fazer o mixin herdar de `Scene`) faz o pipeline renderizar a cena
inteira por engano.

`load_scene_classes` importa o arquivo de verdade, com o diretório dele em
`sys.path` — então **o módulo é executado**. Código de topo com efeito colateral
roda aqui.

`mx` só enxerga o venv da CE: `bin/mx scenes scenes/exemplos_gl.py` →
`ModuleNotFoundError: No module named 'manimlib'`. Cena GL só pelo `bin/manimgl`.

---

## 21. Regenerar o índice — e o `--label` que falta na receita óbvia

Obrigatório depois de atualizar o Manim, senão o índice mente com cara de
verdade.

### A armadilha: `bin/mx api-dump` sozinho NÃO regenera o índice em uso

O nome dos arquivos é `label or package`, e o default de `--package` no
`api-dump` é **`manim`** (`manimx/cli.py:479`) — enquanto o default de
`--package` no `find`/`show` é **`manim-ce`** (`cli.py:492`). Os dois nomes não
são o mesmo, e quem lê é `_load_index("manim-ce")`, que procura
`api/manim-ce-api.json.gz`:

```
$ bin/mx api-dump --out /tmp/x
manim-api.json.gz  manim-index.tsv  manim-methods.tsv  …    ← nomes ERRADOS
```

O resultado é o pior possível: seis arquivos órfãos em `api/`, o índice velho
intacto, e `mx find` continuando a responder pela versão antiga. **A forma
certa:**

```bash
bin/mx api-dump --label manim-ce        # CE  (~10 s, 167 submódulos)
bin/mx api-diff                         # regenera api/ce-vs-gl.md
```

### Armadilha irmã: um `.json` cru tem PRECEDÊNCIA sobre o `.json.gz`

`_load_index` (`manimx/cli.py:275-292`) lê `api/<pkg>-api.json` **antes** de
`api/<pkg>-api.json.gz`. O `dump_api` apaga o cru quando regenera, mas um dump
feito à mão em `/tmp` e copiado para `api/` passa a mandar em tudo, para sempre,
sem nenhum aviso. Se `mx show` estiver respondendo coisa impossível, o primeiro
teste é `ls api/*.json` — se existir, é ele.

### ManimGL: o `import manimlib` parseia `sys.argv` no import

`bin/mx api-dump --package manimlib` **falha** (`ModuleNotFoundError`), porque o
`bin/mx` sempre entra no venv da CE (`bin/mx` faz `manimx_use_ce` e executa
`.venv/bin/python -m manimx.cli`). E chamar o venv do GL direto também falha,
por um motivo que não está documentado em lugar nenhum: **importar `manimlib`
dispara o `argparse` dele**, e qualquer flag estranha na linha mata o processo:

```
$ .venv-gl/bin/python -c "import manimlib" --package manimlib
-c: error: unrecognized arguments: --package
```

A receita que funciona — **testada, e reproduz o índice comitado byte a byte**
(1242 linhas de index, 51 194 de methods, 718 de toplevel)
[não reverificada — 2026-08-19]:

```python
# /tmp/dump_gl.py — rode com .venv-gl/bin/python
import sys, warnings
warnings.filterwarnings("ignore")
sys.argv = [sys.argv[0]]                       # manimlib parseia sys.argv NO IMPORT
sys.path.insert(0, "/home/ondokai/Projects/manim")
from manimx.introspect import dump_api
for nome, caminho in dump_api("api", "manimlib", label="manimgl").items():
    print(f"{nome:12s} {caminho}")
```

```bash
.venv-gl/bin/python /tmp/dump_gl.py
```

### O índice é byte-instável — não confunda ruído com mudança de API

Regerando o índice da CE **sem trocar nada**, o `diff` contra o comitado não sai
vazio. Medido [não reverificado — 2026-08-19]:

| Arquivo | Linhas que mudam | Total | Por quê |
|---|---:|---:|---|
| `manim-ce-index.tsv` | **24** | 5523 | `repr()` de default `<function smooth at 0x713b…>` + um `set` cuja ordem depende do `PYTHONHASHSEED` (`KEYS_TO_FILTER_OUT`) |
| `manim-ce-methods.tsv` | **564** | 50945 | mesma causa |

O número bate com a contagem estática: hoje há **21** linhas com `<function … at
0x…>` no `index.tsv` e **561** no `methods.tsv` — o resto são as chaves do
`set`. Normalizando os endereços, o diff é **zero**. Portanto:

```bash
diff <(sed -E 's/at 0x[0-9a-f]+/at 0xADDR/g' velho.tsv) \
     <(sed -E 's/at 0x[0-9a-f]+/at 0xADDR/g' novo.tsv)
```

### O índice está velho? (uma linha, exit 1 quando estiver)

```bash
.venv/bin/python - <<'PY'
import gzip, json, importlib.metadata as md
ind = json.load(gzip.open("api/manim-ce-api.json.gz", "rt"))["version"]
ins = md.version("manim")
print(f"OK  índice = pacote = {ins}" if ind == ins
      else f"VELHO  índice={ind} pacote={ins} -> bin/mx api-dump --label manim-ce")
raise SystemExit(ind != ins)
PY
```

O `.json.gz` carrega o cabeçalho todo:
`{"package": "manim", "version": "0.21.0", "python": "3.12.3", "symbol_count": 5523, "method_count": 50945}`.
No GL: `manimlib 1.7.2`, 1241 símbolos, 51 193 métodos.

---

## 22. Introspecção ao vivo — quando nem o índice nem o fonte bastam

Custa 1,6–1,7 s (o `import manim`). Vale quando você precisa de **comportamento
em vez de forma**: o MRO real na ordem certa, um Enum materializado, um valor
computado, o `getsource` de um método que você não sabe em que arquivo mora.

```bash
bin/mx render --help                     # as flags reais da CLI (não decore, consulte)

.venv/bin/python -c "
from manim import *
help(Axes.plot)"                          # o docstring completo, com os Parameters

.venv/bin/python -c "
from manim import *
import inspect
print([c.__name__ for c in FadeIn.__mro__])          # a ORDEM real do MRO
print(inspect.signature(TransformMatchingTex.__init__))
print(inspect.getsource(Circle))"

.venv/bin/python -c "
from manim import *
print([m for m in dir(Circle()) if not m.startswith('_')])"   # a superfície da INSTÂNCIA
```

Três cautelas medidas nesta máquina [não reverificadas — 2026-08-19]:

- **`dir()` e `hasattr()` discordam, e nenhum dos dois é prova.** Medido em
  `Circle`: `'set_width' in dir(Circle)` → `False`; `'set_width' in dir(c)` →
  **também `False`**; `hasattr(c, 'set_width')` → **`True`**. `dir()` não
  dispara `__getattr__`, e o `__getattr__` do `Mobject` inventa o método na
  hora (§13). Quem prova é o `methods.tsv`.
- `dir()` de **instância** tem 358 nomes contra 320 da classe em `Circle`, e a
  diferença são **atributos de estado** (`angle`, `arc_center`, `cap_style`,
  `background_stroke_width`…), não métodos. Serve para inspecionar um objeto
  vivo, não para descobrir API.
- `warnings.filterwarnings("ignore")` antes do `import manim` evita que
  `DeprecationWarning` de método sintetizado polua a saída que você vai ler.

---

## 23. Um exemplo completo do método

Toda linha abaixo saiu de uma consulta, nenhuma da memória.

```bash
bin/mx show Cutout          # class Cutout(main_shape: 'VMobject', *mobjects: 'VMobject', **kwargs)
bin/mx show Circumscribe    # (mobject, shape=<class Rectangle>, fade_in=False, fade_out=False,
                            #  time_width=0.3, buff=0.1, color=#FFFF00, run_time=1, stroke_width=4, **kwargs)
kwargs-do-indice.sh Cutout  # [VMobject] fill_opacity, stroke_width…  → confirmado herdado (§10)
```

```python
from manim import *

class Conferido(Scene):
    def construct(self):
        alvo = Cutout(
            Square(side_length=3, color=BLUE),
            Circle(radius=0.9),
            fill_opacity=1,        # de VMobject, herdado — confirmado, não chutado
            fill_color=BLUE_E,
            stroke_width=0,
        )
        self.add(alvo)
        self.play(Circumscribe(alvo, color=YELLOW, time_width=0.4, buff=0.15))
        self.wait(0.2)
```

```
$ bin/mx render conferido.py Conferido --format png --media-dir /tmp/saida --json
"success": true, "elapsed_s": 0.107, "num_animations": 2      [não reverificado — 2026-08-19]
```

(Repare no JSON: em `--format png` o caminho vem em **`image_file`** e
`output_file` é `null`. Isso é assunto de `manim-render-api`.)

Note também o que este exemplo **não** prova: que o desenho está certo. Ele
prova que o código é legal. O quadro só o PNG mostra — `manim-verificacao-visual`.

---

## Armadilhas, em uma tela

| Armadilha | Sintoma | O antídoto |
|---|---|---|
| Nome homônimo | `mx show` mostra o símbolo errado, sem avisar (desempate = ordem alfabética de módulo) | `awk '$2==nome' index.tsv \| sort -u` antes |
| Constante no `mx show` | mostra `categoria: other` e nenhum valor | `mx find NOME --kind constant` ou `--json` |
| Cabeçalho de `Animation` | é o `__new__`, some `run_time`/`rate_func` | leia a linha `__init__` de "métodos próprios" |
| Enum / atributo de classe | classe "vazia" no `mx show` (3 classes não têm método nenhum) | o fonte, ou `list(Enum)` no interpretador |
| Método-tampão | está no `mx show` e levanta `NotImplementedError` | 5 deles; `defined_in=Mobject` num método geométrico → veja o fonte |
| Base **privada** (`_Fade`, `_BooleanOps`, `_ScaleBase`) | `herda de : _Fade` e `mx show _Fade` não acha | 8 classes; caia no fonte — a árvore e a varredura de kwargs param ali |
| `inheritance.txt` perde descendente | `Animation` "tem 72 filhos", tem 74 | `awk '$4=="Animation" && $5=="1"' methods.tsv` |
| **Propriedade não está em TSV nenhum** | `awk '$2=="width"' methods.tsv` → 0 linhas | `mx show`, ou o `.json.gz` (161 propriedades, 287 classes) |
| `mx find` procura só a 1ª linha do doc | conceito documentado no 3º parágrafo é invisível | `grep -rIn` no fonte (20 ms) |
| `mx show` não acha `config`/`XKCD` | são os 36 nomes `[só no topo]` | procure o TIPO (`ManimConfig`) ou abra `toplevel.md` |
| `-n` default 30 | inventário sai truncado sem aviso (209 → 30) | `-n 999` sempre que for listar |
| `-n 0` | vazio + exit 1, parece "não existe" | não use 0 |
| `mx find` é substring e não deduplica | `find RIGHT --kind constant` → 67 acertos para 42 linhas de `RIGHT` | para CONTAR, `awk '$2==nome'`; o `find` é para ACHAR |
| `\| head` num `mx` | `erro: BrokenPipeError` colado na saída | `--own-only`, `-n`, ou `\| sed -n '1,20p'` |
| Contagem do `by-category.md` | "62 símbolos" = 1 classe + 61 constantes | conte com `$1!="constant"` |
| Categoria `other` | 189 linhas de coisa sem parentesco | não conclua nada; olhe a coluna `module` |
| `**kwargs` (83% do índice, 92% do topo) | a assinatura não lista o parâmetro que existe | varredura do MRO (§10) |
| Alias de tipo (`Point3DLike`, 51 usos) | não está em índice nenhum | `manim/typing.py` |
| `hasattr(mob, "set_X")` | **sempre True**; a chamada grava lixo e não desenha | `awk '$2=="set_X"' methods.tsv` |
| `AttributeError` de `get_X` | a mensagem fala de `'X'`, não de `'get_X'` | saiba que o prefixo foi tirado antes do erro |
| Encadear em cima de override de `.animate` | `NotImplementedError: Method chaining is currently not supported…` | não encadeie depois de `.create()` etc. |
| Cor com nome repetido | 165 nomes com >1 valor; `MAROON` tem 6 | leia a coluna 5 (módulo) |
| Cor de paleta | `from manim import BLOODRED` → `ImportError` | `from manim.utils.color import XKCD` |
| 81 classes fora do topo | `ImportError: cannot import name` | coluna 5 dá o módulo certo |
| "está depreciado?" | **nada** na 0.21 é marcado; o índice não sabe | só o fonte, e o único uso é num helper de CLI |
| `mx api-dump` sem `--label` | gera `manim-*.tsv`; o índice lido continua velho | `--label manim-ce` |
| `api/*.json` cru na pasta | tem precedência sobre o `.gz` e nunca é atualizado | `ls api/*.json` antes de duvidar do `mx` |
| `import manimlib` | mata o script com `argparse error` | `sys.argv = [sys.argv[0]]` antes do import |
| Diff do índice nunca vazio | 24 linhas mudam por `repr` de endereço | normalize `at 0x…` antes de comparar |
| Índice velho depois de upgrade | tudo mente com cara de verdade | o checador de versão da §21 |
| CE × GL homônimo | import e construtor aceitam; a figura sai outra | 153 de 153 divergem — `api/ce-vs-gl.md` |

---

## O que NENHUMA fonte deste projeto responde

Saber o limite é parte do método. Nada aqui responde a:

1. **"isso está depreciado?"** — a 0.21 não marca (§12). É o fonte + julgamento.
2. **"esse valor é razoável?"** — o índice diz que `stroke_width` existe e que o
   default é 4. Se 4 é grosso demais no seu palco, é render e olho
   (`manim-verificacao-visual`).
3. **"isso vai caber na tela?"** — `manim-layout-posicionamento`.
4. **"isso vai ficar bonito / legível?"** — `manim-color-theming` (contraste),
   `aula-slides` no repo `~/Projects/aulas` (densidade).
5. **"por que o render falhou?"** — `manim-troubleshooting`.
6. **"quanto tempo/quanto disco isso custa?"** — `manim-gpu-encoding`,
   `manim-performance-cache`.
7. **o corpo de um método privado do ManimGL** — o índice do GL tem a mesma
   limitação de `_privado`; o fonte dele está em
   `.venv-gl/lib/python3.12/site-packages/manimlib/`.

---

## Onde esta skill para

- **Como usar** a classe que você acabou de identificar → a skill do assunto:
  `manim-mobjects` (formas, grupos, submobjects), `manim-layout-posicionamento`
  (posicionar, enquadrar, z-index), `manim-animations` (o catálogo do quê),
  `manim-composicao-ritmo` (o tempo: `rate_func`, `lag_ratio`, `path_func`,
  composição), `manim-graphs-plots` (eixos e funções), `manim-tabelas-matrizes`,
  `manim-grafos-redes`, `manim-text-latex` (texto e fórmula), `manim-svg-imagens`
  (SVG, PNG, fonte), `manim-color-theming` (paleta, tema, transparência,
  `set_default`), `manim-camera-2d` (pan e zoom), `manim-3d-camera`,
  `manim-cenas-secoes` (de qual `Scene` herdar, `next_section`),
  `manim-updaters-valuetracker`, `manim-mobjects-customizados` (escrever
  `Mobject`/`Animation` próprios, bezier, `space_ops`).
- **Renderizar**, escolher qualidade/formato/codec, achar o caminho de saída →
  `manim-render-api`. Em lote → `manim-batch-pipeline`. Na GPU →
  `manim-gpu-encoding`. Cache e custo → `manim-performance-cache`.
- **Olhar o resultado** (renderizou e não olhou = não terminou) →
  `manim-verificacao-visual`.
- **Um render que falhou** por ambiente, LaTeX, codec ou arquivo →
  `manim-troubleshooting`. A fronteira: erro de **nome/assinatura/kwarg** é
  aqui; erro de **ambiente/saída** é lá.
- **Cena que para dentro de um slide** (mixin, `next_section`, partes) →
  `manim-presentation-parts`. O `tema.py` como contrato de projeto →
  `manim-tema-projeto`.
- **ManimGL de verdade** (flags, YAML, janela, fluxo 3b1b) → `manimgl-3b1b`.
- **O projeto como um todo** e o roteamento entre skills → `manim-project`.
