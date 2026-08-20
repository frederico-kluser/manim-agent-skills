---
name: manim-grafos-redes
description: >-
  Grafo no sentido de TEORIA DOS GRAFOS — `Graph`, `DiGraph`, vértices, arestas,
  os 10 layouts automáticos, layout manual por dicionário, `LayoutFunction`
  própria, `from_networkx`, inserir e remover vértice/aresta com animação, e
  destacar um caminho. Use quando o pedido soar como "desenha uma rede",
  "monta um grafo", "uma árvore com raiz", "um grafo dirigido", "põe setas nas
  arestas", "liga esses nós", "anima o caminho mais curto", "destaca essa
  aresta", "adiciona um nó no meio da animação", "expande a árvore", "uma rede
  neural em camadas", "grafo bipartido", "importa do networkx", "o grafo mudou
  de lugar a cada render", "as arestas não seguem os vértices", "o grafo sumiu
  no fundo branco", "o `buff` da aresta não fez nada", "o `edge_config` de uma
  aresta foi ignorado", "o grafo voltou para o centro quando troquei o layout",
  "`ValueError: Could not find (1, 2) in vertices or edges`", "o grafo se
  desmontou depois que eu pisquei uma aresta". Cobre a assinatura completa
  conferida no fonte, o updater `update_edges` (o que ele garante, o que ele
  quebra e quanto custa), a não-determinação de `spring`/`random` e as três
  correções, e a decisão que mais custa em aula — **um diagrama de 5 caixas e
  setas NÃO é um `Graph`**. NÃO use para: gráfico de FUNÇÃO, eixos, plano
  cartesiano, `BarChart` e curvas (skill `manim-graphs-plots` — "graph" ali é
  plot, aqui é rede); grade de células e `Matrix` (`manim-tabelas-matrizes`);
  desenhar caixas, setas e chaves à mão (`manim-mobjects`) e posicioná-las
  (`manim-layout-posicionamento`); escolher classe de animação, `rate_func` ou
  `lag_ratio` (`manim-animations`, `manim-composicao-ritmo`); `ValueTracker` e
  `always_redraw` (`manim-updaters-valuetracker`); cor, contraste e tema
  (`manim-color-theming`); cortar a cena em partes para slide
  (`manim-presentation-parts`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Grafos e redes — `Graph`, `DiGraph`

**"Graph" no Manim é ambíguo e a ambiguidade custa tempo.** `manim.mobject.graph`
é teoria dos grafos: vértices e arestas. `manim.mobject.graphing` é plotagem:
eixos e curvas. A primeira linha do módulo diz isso literalmente
(`mobject/graph.py:1`): *"Mobjects used to represent mathematical graphs (think
graph theory, not plotting)"*. Se o pedido é "plota o seno", você está na skill
errada — vá para **`manim-graphs-plots`**.

## Procedência de cada afirmação

Quatro marcadores, válidos para o arquivo inteiro:

- **[FONTE]** — lido no ManimCE **0.21.0** instalado em
  `.venv/lib/python3.12/site-packages/manim/`, ou no networkx **3.6.1** do mesmo
  venv, com arquivo e linha. Afirmação forte.
- **[ÍNDICE]** — assinatura copiada de `api/manim-ce-index.tsv` /
  `api/manim-ce-methods.tsv`.
- **[HOJE]** — contado nesta sessão, 2026-08-19, com `grep`/`awk`/`sed`.
  **Nenhum render, nenhum ffmpeg, nenhuma GPU.**
- **[NÃO VERIFICADO]** — dedução de leitura do código que ninguém executou.
  Está marcado onde aparece, e §17 lista tudo junto.

**Nada neste arquivo foi renderizado.** Os exemplos são referência de API, não
receitas testadas. Antes de commitar qualquer cena que saia daqui, rode o ciclo
de `manim-verificacao-visual`: renderizar rápido → **OLHAR o PNG** → corrigir.

## Cartão de referência — o sintoma manda na seção

| O que você quer / o que aconteceu | Onde ler |
|---|---|
| "isso é grafo mesmo, ou eu quero 5 caixas e setas?" | **§1 — leia antes de tudo** |
| a assinatura, o que existe na categoria | §2 |
| `g[…]`, `g.vertices`, `g.edges`, o que o objeto guarda | §3 |
| vértice: tamanho, cor, rótulo, mobject próprio | §4 |
| aresta: cor, espessura, curva, ponta de seta | §5 |
| escolher layout / posicionar à mão / layout próprio | §6 |
| **o grafo saiu diferente a cada render** | **§7** — e é fatal em cena em partes |
| troquei o layout e o grafo voltou para o centro / perdeu o `scale` | §8 |
| inserir/remover vértice ou aresta com animação | §9 |
| destacar caminho, piscar aresta, correr um ponto pela rede | §10 |
| **o grafo se desmontou e as arestas pararam de seguir** | §10.4 |
| o render ficou lento depois que entrou o grafo | §11 |
| `from_networkx`, caminho mínimo, o resto do networkx | §12 |
| o grafo sumiu no fundo branco / os rótulos se sobrepõem | §4.5 e §13 |
| uma cena de referência inteira, comentada | §14 |
| conferir sem renderizar | §15 |
| `ValueError: Could not find … in vertices or edges` | §3.2 |
| `ValueError: The layout '…' is neither a recognized layout…` | §6.6 |
| `nx.NetworkXException: G is not planar` | §6.2 |
| `ValueError: The tree layout requires the root_vertex parameter` | §6.4 |

---

## 1. A pergunta que vem antes de qualquer código

**Um diagrama de arquitetura com 5 caixas rotuladas não é um `Graph`.** Esta é
a decisão que mais custa retrabalho nesta área, e o argumento tem número.

**[HOJE]** No deck consumidor `~/Projects/aulas` — 11 arquivos de cena, ~77
classes de parte em produção — a contagem de ocorrências de `Graph(`, `DiGraph`
ou `networkx` é **zero**. Todos os diagramas (worktrees, orquestrador, MCP,
skills, harness) são `VGroup` + `Rectangle` + `Arrow`/`Line` posicionados à mão:
**33 `Line(`** e **9 `Arrow(`** espalhados nos 11 arquivos. Não é ignorância da
API: é que layout automático briga com legibilidade.

### Por que `Graph` perde num diagrama de explicação

| O que `Graph` te dá | Por que atrapalha num diagrama de 5 caixas |
|---|---|
| posição calculada por algoritmo | você já sabe onde cada caixa deve ficar; o algoritmo não sabe |
| aresta que segue o vértice | as caixas não se mexem |
| vértice = `Dot`/`LabeledDot` circular | um serviço, um repositório e um processo querem formas **diferentes** |
| aresta = `Line`/`Arrow` reta | você quer cotovelo, curva, tracejado, rótulo no meio |
| `spring`/`random` mudam a cada render (§7) | um diagrama que muda de lugar entre a parte 3 e a parte 4 do vídeo é defeito puro |

### A regra prática

| Situação | Use |
|---|---|
| ≤ ~8 nós, você sabe onde cada um vai, cada um tem forma/rótulo próprio | `VGroup` + `Rectangle`/`RoundedRectangle` + `Arrow`, à mão — **`manim-mobjects`** e **`manim-layout-posicionamento`** |
| a **topologia** é o assunto (grau, caminho, ciclo, árvore, bipartido, corte) | `Graph`/`DiGraph` — esta skill |
| ≥ ~12 nós, ou os dados vêm de fora (CSV, API, `networkx`) | `Graph`/`DiGraph`, com layout **determinístico** (§7) |
| o grafo **muda durante a cena** (nó entra, aresta some, árvore expande) | `Graph` — §9 é toda sobre isso |
| você quer o algoritmo de layout mas não quer os `Dot` | `Graph` só para calcular, e leia `g._layout` — ou use `nx.spring_layout` direto (§12.3) |

Escolher errado tem conserto barato num sentido só: sair do `Graph` para o
desenho à mão é reescrever; começar à mão e depois precisar de topologia é
raro. Na dúvida em aula, comece à mão.

---

## 2. O inventário completo da categoria

**[HOJE]** `awk -F'\t' '$3=="mobject/graph"' api/manim-ce-index.tsv` devolve
**5 linhas**: 4 classes/protocolos e 2 constantes re-exportadas (`BLACK`,
`TYPE_CHECKING`). É a menor categoria acionável do índice — e a mais densa em
parâmetros por classe.

| Símbolo | O que é | No `from manim import *`? |
|---|---|---|
| `Graph` | grafo **não** dirigido | **sim** [FONTE] `__all__` do módulo, e `api/manim-ce-toplevel.md:103` |
| `DiGraph` | grafo dirigido (arestas com ponta) | **sim** — `manim-ce-toplevel.md:82` |
| `GenericGraph` | base abstrata dos dois; é dela que vêm **todos** os métodos públicos | **não** — `from manim.mobject.graph import GenericGraph` |
| `LayoutFunction` | `Protocol` para escrever um layout próprio | **não** — mesmo import |

**[ÍNDICE]** Herança (`api/manim-ce-inheritance.txt:153-155`):

```
VMobject
  GenericGraph
    DiGraph
    Graph
```

Ou seja: um grafo **é um `VMobject`**. Ele aceita `scale`, `shift`, `move_to`,
`set_stroke`, `copy`, `become`, `save_state` — todo o vocabulário de
`manim-mobjects`. **[HOJE]** `awk -F'\t' '$1=="Graph"' api/manim-ce-methods.tsv`
dá **250 métodos**, dos quais **8 são próprios do assunto grafo**
(`add_vertices`, `remove_vertices`, `add_edges`, `remove_edges`,
`change_layout`, `from_networkx`, `update_edges`, `__getitem__`) — os outros 242
são de `Mobject`/`VMobject` e pertencem às skills irmãs.

### A assinatura, idêntica nas três classes

**[ÍNDICE]** `Graph`, `DiGraph` e `GenericGraph` têm exatamente a mesma:

```python
Graph(vertices: Sequence[Hashable],
      edges: Sequence[tuple[Hashable, Hashable]],
      labels: bool | dict = False,
      label_fill_color: str = BLACK,
      layout: LayoutName | dict[Hashable, Point3DLike] | LayoutFunction = "spring",
      layout_scale: float | tuple[float, float, float] = 2,
      layout_config: dict | None = None,
      vertex_type: type[Mobject] = Dot,
      vertex_config: dict | None = None,
      vertex_mobjects: dict | None = None,
      edge_type: type[Mobject] = Line,
      partitions: Sequence[Sequence[Hashable]] | None = None,
      root_vertex: Hashable | None = None,
      edge_config: dict | None = None) -> None
```

Repare: **não existe `**kwargs`**. `Graph(..., color=BLUE)` levanta
`TypeError`. Cor de vértice vai em `vertex_config`, cor de aresta em
`edge_config` (§4, §5) — ou depois, com `g.set_stroke(...)`.

### Os 8 métodos próprios

**[ÍNDICE]** `api/manim-ce-methods.tsv`, todos definidos em `GenericGraph`
exceto `update_edges`:

```python
GenericGraph.add_vertices(self, *vertices: Hashable, positions: dict | None = None,
    labels: bool = False, label_fill_color: str = BLACK,
    vertex_type: type[Mobject] = Dot, vertex_config: dict | None = None,
    vertex_mobjects: dict | None = None)
GenericGraph.remove_vertices(self, *vertices)
GenericGraph.add_edges(self, *edges: tuple[Hashable, Hashable],
    edge_type: type[Mobject] = Line, edge_config: dict | None = None, **kwargs)
GenericGraph.remove_edges(self, *edges: tuple[Hashable]) -> VGroup
GenericGraph.change_layout(self, layout=..., layout_scale=2, layout_config=None,
    partitions=None, root_vertex=None) -> Graph
GenericGraph.from_networkx(nxgraph, **kwargs)          # classmethod
Graph.update_edges(self, graph) -> Self                # e DiGraph.update_edges
GenericGraph.__getitem__(self, k) -> Mobject
```

Os privados `_add_vertex`, `_add_edge`, `_remove_vertex`, `_remove_edge`,
`_create_vertex(es)`, `_add_created_vertex`, `_populate_edge_dict`,
`_empty_networkx_graph` existem e são estáveis, mas o público faz o mesmo com
plural e com `.animate` (§9). Não os chame.

---

## 3. O objeto por dentro

### 3.1 Os atributos que você pode ler

**[FONTE]** `mobject/graph.py:563-659` (o `__init__`):

| Atributo | O que guarda |
|---|---|
| `g.vertices` | `dict[Hashable, Mobject]` — vértice → o `Dot`/`LabeledDot` |
| `g.edges` | `dict[tuple, Mobject]` — a tupla **exatamente como você escreveu** → a `Line` |
| `g._graph` | o `nx.Graph`/`nx.DiGraph` de verdade. É por aqui que se chama `nx.shortest_path` (§12.2) |
| `g._layout` | `dict[vértice, Point3D]` — as posições que o layout calculou. **Não** acompanha `shift`/`scale` (§8) |
| `g._labels` | `dict[vértice, Mobject]` dos rótulos |
| `g._vertex_config`, `g._edge_config`, `g._tip_config` | os kwargs por vértice / por aresta / da ponta de seta |
| `g.default_vertex_config`, `g.default_edge_config` | os kwargs que valem para todo mundo |

Só `vertices` e `edges` são API documentada; os `_` são internos e o código
deste módulo os usa o tempo todo. Ler é seguro; escrever direto é como o
próprio Manim se enrola (§5.2).

### 3.2 `g[…]` — vértice **ou** aresta, e o erro que mente

**[FONTE]** `graph.py:672-696`:

```python
g[1]          # o Dot do vértice 1
g[(1, 2)]     # a Line da aresta (1, 2)
```

A docstring do método promete `KeyError`; o corpo levanta **`ValueError`**:

```python
raise ValueError(f"Could not find {k} in vertices or edges")   # graph.py:695
```

**Consequência prática:** um `try: ... except KeyError:` em volta de `g[e]`
**não pega nada** e a cena morre. Se você precisa de acesso tolerante, use
`g.edges.get(e)` sobre o dicionário, que é um `dict` de verdade.

E a causa nº 1 desse `ValueError` numa aresta é a §5.3: você escreveu `(2, 1)`
e a aresta está registrada como `(1, 2)`.

### 3.3 A ordem dos submobjects e o `z_index=-1`

**[FONTE]** `graph.py:656-659`:

```python
self.add(*self.vertices.values())
self.add(*self.edges.values())
self.add_updater(self.update_edges)
```

Vértices primeiro, arestas depois — mas as arestas nascem com **`z_index=-1`**
(`graph.py:1573` no `Graph`, `1781` no `DiGraph`, `1057` no `_add_edge`), então desenham **atrás**
dos vértices. É isso que faz a linha sumir sob o `Dot` em vez de cruzá-lo.

**A armadilha:** `Mobject.set_z_index(valor, family=True)` — e `family=True` é
o **default** [ÍNDICE]. Um `g.set_z_index(2)` para pôr o grafo na frente de um
retângulo de fundo achata o `-1` das arestas e elas passam a cruzar os
vértices. Use `g.set_z_index(2, family=False)`.

Consequência secundária de "vértices primeiro": **`Create(g)`** desenha
**todos os pontos e só depois as linhas** — `Create` tem `lag_ratio=1.0` por
default [ÍNDICE], então é sequencial. Para desenhar "nó, aresta, nó, aresta",
não use `Create(g)`: componha a mão com `LaggedStart` sobre `g.vertices` e
`g.edges` na ordem que você quer (`manim-composicao-ritmo`).

### 3.4 O updater: o que ele garante

O grafo carrega **um updater permanente**, registrado no `__init__`. Ele é o
motivo de a aresta seguir o vértice quando você anima `g[1].animate.move_to(…)`.

**[FONTE]** `Graph.update_edges` (`graph.py:1579-1588`):

```python
def update_edges(self, graph) -> Self:
    for (u, v), edge in graph.edges.items():
        edge.set_points_by_ends(
            graph[u].get_center(),
            graph[v].get_center(),
            buff=self._edge_config.get("buff", 0),
            path_arc=self._edge_config.get("path_arc", 0),
        )
    return self
```

`DiGraph.update_edges` (`graph.py:1790-1806`) é igual, com três diferenças:
passa **os Mobjects** (`graph[u]`, não `.get_center()`), e faz
`tip = edge.pop_tips()[0]` antes / `edge.add_tip(tip)` depois — porque uma
ponta de seta deforma se você reescrever os pontos da linha por baixo dela.

Três consequências que valem dinheiro:

1. **`Graph` liga CENTRO a CENTRO; `DiGraph` liga BORDA a BORDA.**
   **[FONTE]** `Line._set_start_and_end_attrs` (`line.py:163-172`) chama
   `_pointify(start, vect)`, que para um Mobject devolve
   `get_boundary_point(direction)`. Passando um ponto, devolve o ponto. Por
   isso a seta do `DiGraph` para na circunferência do vértice, e a linha do
   `Graph` entra por baixo dele.
2. **O updater só roda enquanto o grafo estiver na lista de mobjects da cena.**
   Se ele sair de lá, as arestas congelam (§10.4).
3. **O updater derruba o cache de frame estático** — e não só o do grafo (§11).

### 3.5 O bug do `buff` e do `path_arc` no updater

Olhe de novo: `self._edge_config.get("buff", 0)`. Mas `self._edge_config` é
**indexado por tupla de aresta**, não por nome de opção (§3.1). A chave
`"buff"` nunca existe ali.

**[FONTE]** Resultado, lendo os dois caminhos:

- na **construção** (`graph.py:1569-1577`) a aresta nasce com
  `Line(start, end, z_index=-1, **self._edge_config[(u,v)])` — ou seja, o seu
  `buff`/`path_arc` **é** aplicado;
- no **primeiro frame** em que o updater roda, `set_points_by_ends` é chamado
  com `buff=0, path_arc=0` e **desfaz** os dois.

Ou seja: `edge_config={"buff": 0.2}` funciona no frame estático e some assim que
a cena anda. Idem `path_arc` — arestas curvas endireitam.

**[NÃO VERIFICADO]** — o mecanismo está lido linha a linha, o efeito visual não
foi renderizado.

**As saídas, em ordem de preferência:**

```python
# 1. Não precise de buff no Graph: use DiGraph com ponta de tamanho zero,
#    que já para na borda do vértice (é o idioma da própria doc, graph.py:1733-1762)
g = DiGraph(V, E, labels=True,
            edge_config={"stroke_width": 2, "tip_config": {"tip_length": 0, "tip_width": 0}})

# 2. Se você precisa MESMO de arestas curvas e o grafo NÃO se move:
g.clear_updaters()          # depois de posicionar tudo — ver §11
```

Não tente `g._edge_config["buff"] = 0.2`: isso injetaria uma chave que o
`_populate_edge_dict` e o `_remove_edge` tratam como se fosse uma aresta.

---

## 4. Vértices

### 4.1 Os quatro parâmetros, e qual vence

**[FONTE]** `graph.py:589-617`, na ordem em que o código resolve:

| Parâmetro | Escopo | Vence quem |
|---|---|---|
| `vertex_type` | a classe de todo vértice | default `Dot` |
| `vertex_config` | kwargs do construtor | ver 4.2 |
| `labels` | rótulo | promove `Dot` → `LabeledDot` (4.3) |
| `vertex_mobjects` | um mobject pronto por vértice | **sobrepõe tudo** — `self.vertices.update(vertex_mobjects)` (`graph.py:617`) |

`vertex_mobjects={"api": Rectangle(...)}` é a válvula de escape quando um nó
precisa de outra forma. Mas repare: se você chegou nesse ponto para 3 nós de 5,
§1 já respondeu — desenhe à mão.

### 4.2 `vertex_config` é um dicionário de duas caras

**[FONTE]** `graph.py:604-612`:

```python
default_vertex_config = {k: v for k, v in vertex_config.items() if k not in vertices}
self._vertex_config = {v: vertex_config.get(v, copy(default_vertex_config)) for v in vertices}
```

A regra: **chave que é um vértice** → configuração daquele vértice;
**chave que não é** → default para todos.

```python
Graph(V, E, vertex_config={"radius": 0.18, "color": BLUE,      # vale para todos
                           7: {"fill_color": RED}})            # só para o 7
```

Duas armadilhas nascem daí:

1. **Config por vértice SUBSTITUI, não mescla.** `7: {"fill_color": RED}` é o
   dicionário inteiro do vértice 7 — ele **não** herda `radius: 0.18`. Repita o
   que precisar: `7: {"radius": 0.18, "fill_color": RED}`.
   (No `add_vertices` é diferente: `_create_vertex` faz
   `base_vertex_config.update(vertex_config)` — `graph.py:726-729` — e ali
   **mescla**. A assimetria é real.)
2. **Vértice com nome de kwarg quebra em silêncio.** Se um vértice se chama
   `"color"` e você passa `vertex_config={"color": BLUE}`, `"color" in vertices`
   é verdadeiro → `BLUE` vira "a config do vértice color" → `Dot(**BLUE)` →
   `TypeError`. Vértices com nomes de string em português (`"cor"`, `"raio"`)
   escapam por acaso; em inglês, não. **[NÃO VERIFICADO]** — leitura do código.

### 4.3 `labels=True` passa pelo LaTeX, e troca a classe do vértice

**[FONTE]** `graph.py:589-596` (o bloco de `labels`):

```python
if labels:
    self._labels = {v: MathTex(v, color=label_fill_color) for v in vertices}
...
if self._labels and vertex_type is Dot:
    vertex_type = LabeledDot
```

Três coisas embutidas aí:

- **`MathTex`** — precisa de LaTeX funcionando, e o nome do vértice é
  interpretado como **matemática**: `Child_0` vira "Child" com subscrito 0,
  `AB` vira dois itálicos multiplicados. Para rótulo em prosa passe um dict:
  `labels={1: Text("API"), 2: Text("Banco")}`. LaTeX quebrado é assunto de
  `manim-text-latex` e `manim-troubleshooting`.
- **A troca `Dot` → `LabeledDot` só acontece se `vertex_type` ainda for `Dot`.**
  Passou `vertex_type=Square` com `labels=True`? O rótulo entra em
  `vertex_config["label"]` e o `Square` recebe um kwarg `label` que ele não
  conhece → `TypeError`. **[NÃO VERIFICADO]**
- **`label_fill_color` default é `BLACK`** — em fundo escuro, sobre o `Dot`
  branco, funciona. Em canvas branco (§4.5) você fica com rótulo preto sobre
  disco branco: legível, mas o disco some.

### 4.4 O raio do vértice rotulado é calculado, e varia por rótulo

**[FONTE]** `LabeledDot.__init__` (`mobject/geometry/arc.py:895-898`):

```python
if radius is None:
    radius = buff + float(np.linalg.norm([rendered_label.width, rendered_label.height]) / 2)
```

Meia diagonal do rótulo, mais `buff` (default `SMALL_BUFF` = 0,1).
Consequência: **`"1"` e `"Greatgrandchild_0"` viram círculos de tamanhos
muito diferentes**, e o layout não sabe disso — ele posiciona **centros**, não
caixas. Rótulo longo em layout apertado se sobrepõe sem erro nenhum.

As duas saídas: encurte o rótulo (é o certo — o nome comprido vai numa legenda
ao lado), ou fixe `vertex_config={"radius": 0.28}` e aceite que o texto
transborda o disco.

**Números de enquadramento**, para decidir sem renderizar. Quadro do Manim:
14,222 × 8 unidades; a 1920×1080 isso é **135 px por unidade** (1080/8).

| Coisa | Unidades | Pixels a 1080p |
|---|---|---|
| `Dot` default (`radius=0.08`) [ÍNDICE] | 0,16 de diâmetro | **21,6 px** — pequeno demais para projetor |
| um `Dot` legível de longe | 0,18–0,28 de raio | 49–76 px de diâmetro |
| caixa do grafo com `layout_scale=2` (default) | 4 × 4 | 540 × 540 px |
| quadro inteiro | 14,222 × 8 | 1920 × 1080 |

Com o default, o grafo ocupa **um quarto da altura e um sétimo da largura**.
`layout_scale=3` (≈ 810 px) é o valor que a própria doc usa nos exemplos
grandes.

### 4.5 Fundo branco: o grafo inteiro desaparece

**[ÍNDICE]** `Dot(..., color=WHITE)`; `Line` herda o `color` default de
`Mobject`, que também é branco. Num tema de canvas claro
(`--theme whiteboard`, `background_color = #FFFFFF`, ou o `CANVAS` de um
`tema.py`), **um `Graph(V, E)` cru sai invisível — sem erro, sem aviso**.

Este é o defeito nº 1 de vídeo gerado por agente em tema claro, e a defesa é a
mesma do resto do projeto: **cor explícita, vinda do tema**.

```python
from tema import TINTA, ACENTO          # nunca hex solto na cena

g = Graph(
    V, E,
    labels={v: Text(v, color=TINTA, font_size=22) for v in V},
    vertex_config={"radius": 0.22, "color": ACENTO},
    edge_config={"stroke_color": TINTA, "stroke_width": 3},
)
```

Quem manda em paleta, contraste e `set_default` é **`manim-color-theming`**;
quem manda no `tema.py` como contrato é **`manim-tema-projeto`**. Esta skill só
registra que `Graph` é um dos objetos que **não** têm cor própria e por isso
some.

---

## 5. Arestas

### 5.1 `edge_config` também tem duas caras — e mais uma terceira

**[FONTE]** `graph.py:628-651`. A regra de separação aqui **não** é "é um
vértice?", é **"é uma tupla?"**:

```python
default_tip_config  = edge_config.pop("tip_config", {})
default_edge_config = {k: v for k, v in edge_config.items() if not isinstance(k, tuple)}
```

| Chave | Vira |
|---|---|
| `"tip_config"` | config da ponta de seta, para **todas** as arestas (só `DiGraph` usa) |
| qualquer nome que **não** seja tupla (`"stroke_width"`, `"color"`) | default de todas as arestas |
| uma **tupla** `(u, v)` | config só daquela aresta — e ela pode ter o seu próprio `"tip_config"` dentro |

Exemplo completo, copiado da doc do módulo (`graph.py:1695-1725`) e conferido
contra a assinatura:

```python
edge_config = {
    "stroke_width": 2,
    "tip_config": {"tip_shape": ArrowSquareTip, "tip_length": 0.15},
    (3, 4): {"color": RED, "tip_config": {"tip_length": 0.25, "tip_width": 0.25}},
}
g = DiGraph(vertices, edges, labels=True, layout="circular", edge_config=edge_config)
```

**Efeito colateral real:** o código faz `edge_config[e].pop("tip_config", …)` —
`pop`, não `get`. Ele **modifica o dicionário que você passou**. Reusar a mesma
constante `EDGE_CONFIG` em dois grafos dá dois resultados diferentes: no
segundo, o `tip_config` interno já foi removido. **[NÃO VERIFICADO]** — leitura
de `graph.py:633-651`. Passe uma cópia: `edge_config=copy.deepcopy(EDGE_CONFIG)`.

### 5.2 O `(u,v)` × `(v,u)` que a documentação promete e o código não faz

A doc do `Graph` diz, textualmente (**[FONTE]** `graph.py:1412-1416`):

> *In `edge_config`, edges can be passed in both directions: if `(u, v)` is an
> edge in the graph, both `(u, v)` as well as `(v, u)` can be used as keys.*

O código não implementa isso. **[FONTE]** `graph.py:643-651` itera sobre a lista
`edges` **que você passou** e testa `if e in edge_config` — comparação de tupla
crua. **[HOJE]** `grep -n "v, u\|reversed\|sorted(\|frozenset" graph.py` não
encontra normalização nenhuma no módulo inteiro (o único `sorted(` é de um
exemplo de docstring, linha 64).

A chave invertida cai no `else` e o seu estilo é **descartado em silêncio** —
ela nem entra em `default_edge_config`, porque tuplas são filtradas de lá.

**O exemplo da própria documentação do ManimCE cai nessa armadilha.**
`LabeledModifiedGraph` (`graph.py:1418-1432`) pinta três arestas de vermelho:

```python
edges = [(1, 7), (1, 8), ..., (7, 2), (7, 4)]          # graph.py:1424-1426
edge_config={(1, 7): {...}, (2, 7): {...}, (4, 7): {...}}   # graph.py:1429-1431
```

`(1,7)` está na lista como `(1,7)` → funciona. `(2,7)` e `(4,7)` estão na lista
como `(7,2)` e `(7,4)` → **ignoradas**. **[NÃO VERIFICADO]** por render, mas o
caminho de código não deixa alternativa.

**A regra que resolve, e serve para `g.edges` também:** guarde as arestas numa
lista só, e indexe **por ela**.

```python
ARESTAS = [(1, 7), (1, 8), (7, 2), (7, 4)]
CAMINHO = [(1, 7), (7, 4)]                 # escrito na mesma direção da lista

def aresta(g, u, v):
    """A Line de {u,v}, na direção em que ela foi registrada."""
    return g.edges.get((u, v)) or g.edges[(v, u)]     # KeyError claro se não existe
```

### 5.3 Ponta de seta: só `DiGraph`, e o truque do tamanho zero

**[FONTE]** `graph.py:1787-1788` — só o `DiGraph` chama `add_tip`:

```python
for (u, v), edge in self.edges.items():
    edge.add_tip(**self._tip_config[(u, v)])
```

`tip_config` aceita o que `Mobject.add_tip` aceita: `tip_shape` (as 8 classes
`Arrow*Tip` de `mobject/geometry`, catálogo em `manim-mobjects`), `tip_length`,
`tip_width`.

**O idioma que a doc do módulo ensina e vale ouro** (`graph.py:1733-1762`):
para um grafo **não dirigido** cujas arestas devem parar na **borda** do
vértice (e não sumir sob ele), use um `DiGraph` com ponta de tamanho zero:

```python
g = DiGraph(V, E, labels=True,
            edge_config={"tip_config": {"tip_length": 0, "tip_width": 0}})
```

Isso resolve o caso "o rótulo é grande e a linha atravessa o texto", porque o
`DiGraph` mede a **caixa delimitadora** do vértice (§3.4, item 1), que com
`LabeledDot` inclui o rótulo.

### 5.4 Rótulo de aresta (peso): `LabeledLine` **não** serve aqui

A tentação é `edge_type=LabeledLine`, com `edge_config={(1,2): {"label": "7"}}`.
**[ÍNDICE]** a assinatura aceita:
`LabeledLine(label, label_position=0.5, label_config=None, box_config=None, frame_config=None, *args, **kwargs)`.

Mas **[FONTE]** `mobject/geometry/labeled.py:172-185`: o rótulo é posicionado
**uma vez, no `__init__`**, com `self.label.move_to(label_coords)` e
`self.add(self.label)`. Não há updater. Quando `update_edges` reescreve os
pontos da linha (§3.4), o rótulo **fica onde estava**. Num grafo cujos vértices
se movem, os pesos descolam das arestas. **[NÃO VERIFICADO]** — leitura.

O que fazer, e é mais barato do que parece: rótulo é um mobject **fora** do
grafo, preso ao meio da aresta por `always_redraw`.

```python
peso = always_redraw(
    lambda: Text("7", color=TINTA, font_size=20)
        .move_to(aresta(g, 1, 2).get_center() + 0.22 * UP)
)
self.add(peso)
```

`always_redraw` e updaters em geral são de **`manim-updaters-valuetracker`** —
é lá que estão o custo e as armadilhas dele. Aqui fica só a razão de precisar
dele.

---

## 6. Layout

### 6.1 Os três jeitos de posicionar

**[FONTE]** `_determine_graph_layout` (`graph.py:444-477`) resolve nesta ordem:

```python
if isinstance(layout, dict):        return layout          # 1. manual
elif layout in _layouts:            ...                    # 2. nome de layout
else:                               layout(nx_graph, ...)  # 3. LayoutFunction
```

### 6.2 Os 10 nomes, com o que cada um exige e quando explode

**[FONTE]** `_layouts` (`graph.py:430-441`) — 8 vêm do networkx 3.6.1, 2 são do
próprio Manim. A coluna "determinístico" é a que decide se você pode usar num
vídeo (§7).

| `layout=` | Implementação | Determinístico? | Exige | Explode quando |
|---|---|---|---|---|
| `"spring"` **(default)** | `nx.layout.spring_layout` | **NÃO** [FONTE] `@np_random_state("seed")`, `layout.py:451` | — | — |
| `"random"` | `_random_layout` do Manim (`graph.py:310`), que embrulha `nx.layout.random_layout` | **NÃO** [FONTE] `@np_random_state(3)`, `layout.py:63` | — | `dim=3` no `layout_config` — o código só trata 2D (`graph.py:315`) |
| `"circular"` | `nx.layout.circular_layout` | sim | — | — |
| `"shell"` | `nx.layout.shell_layout` | sim | — | — |
| `"spectral"` | `nx.layout.spectral_layout` | sim | — | — |
| `"spiral"` | `nx.layout.spiral_layout` | sim | — | — |
| `"kamada_kawai"` | `nx.layout.kamada_kawai_layout` | sim | scipy (já é dependência do Manim) | grafo desconexo — resultado degenerado |
| `"planar"` | `nx.layout.planar_layout` | sim | **grafo planar** | `nx.NetworkXException: G is not planar.` [FONTE] `layout.py` |
| `"tree"` | `_tree_layout` (`graph.py:319`) | sim | `root_vertex` **e** que o grafo seja uma árvore | `ValueError: The tree layout requires the root_vertex parameter`; ou `ValueError: The tree layout must be used with trees` (`nx.is_tree` falso) |
| `"partite"` | `_partite_layout` (`graph.py:284`) | sim | `partitions` não vazio | `ValueError: The partite layout requires partitions parameter…`; e `KeyError` se um vértice da partição não existe no grafo |

**[ÍNDICE/FONTE]** As assinaturas do networkx 3.6.1 que recebem os
`layout_config` (extraídas de `networkx/drawing/layout.py`):

```
spring_layout(G, k=None, pos=None, fixed=None, iterations=50, threshold=1e-4,
              weight="weight", scale=1, center=None, dim=2, seed=None, ...)
circular_layout(G, scale=1, center=None, dim=2, ...)
shell_layout(G, nlist=None, rotate=None, scale=1, center=None, dim=2, ...)
spectral_layout(G, weight="weight", scale=1, center=None, dim=2, ...)
spiral_layout(G, scale=1, center=None, dim=2, resolution=0.35, equidistant=False, ...)
kamada_kawai_layout(G, dist=None, pos=None, weight="weight", scale=1, center=None, dim=2, ...)
planar_layout(G, scale=1, center=None, dim=2, ...)
multipartite_layout(G, subset_key="subset", align="vertical", scale=1, center=None, ...)
```

Tudo o que estiver nessas assinaturas pode ir em `layout_config`. Exemplos
úteis: `layout_config={"seed": 42}` (§7), `{"iterations": 200}` para o spring
relaxar mais, `{"nlist": [[1,2],[3,4,5]]}` para escolher os anéis do shell,
`{"rotate": 0}` para o shell não girar.

### 6.3 `layout_scale` — o que ele faz e o que ele **não** faz

**[FONTE]** os layouts do networkx terminam em `rescale_layout`
(`layout.py:1888-1894`):

```python
pos -= pos.mean(axis=0)
lim = np.abs(pos).max()          # o MAIOR valor de TODOS os eixos
if lim > 0: pos *= scale / lim
```

Três leituras diretas disso:

1. **O escalonamento preserva a proporção.** `layout_scale=2` garante que a
   maior coordenada, em qualquer eixo, vale 2 — não que o grafo tenha 4×4. Uma
   rede larga e baixa continua larga e baixa, só que menor.
2. **`layout_scale` como tupla só funciona no `tree`.** A assinatura anuncia
   `float | tuple[float, float, float]` [ÍNDICE], e `_tree_layout`
   (`graph.py:395-404`) de fato trata tupla. Mas nos layouts do networkx o
   valor cai em `pos *= scale / lim` → `tuple / float` → `TypeError`.
   **[NÃO VERIFICADO]**, mas o caminho é aritmética de Python.
3. **`layout_scale` é ignorado no layout manual** — o dicionário volta cru
   (`graph.py:454`). É por isso que o §6.5 existe.

### 6.4 `tree` e `partite`: os dois que precisam de um segundo parâmetro

```python
Graph(V, E, layout="tree", root_vertex="ROOT",
      layout_config={"vertex_spacing": (0.6, 1.1)})
```

**`vertex_spacing=(dx, dy)`** é especialidade do `_tree_layout`
(`graph.py:395-404`): irmãos ficam a pelo menos `dx` de distância horizontal e
camadas vizinhas a `dy` na vertical — e **ele sobrepõe o `layout_scale`**, ou
seja, o tamanho final passa a depender de quantos nós a árvore tem. Árvore
grande + `vertex_spacing` = grafo maior que o quadro; a doc do Manim resolve
isso com `MovingCameraScene` e `self.camera.auto_zoom(g, margin=1)`
(**[ÍNDICE]** `MovingCamera.auto_zoom(mobjects, margin=0, only_mobjects_in_frame=False, animate=True)`),
que é assunto de **`manim-camera-2d`**.

`_tree_layout` também aceita `orientation` (`"down"` default, qualquer outra
coisa inverte o sinal — `graph.py:341`).

```python
Graph(V, E, layout="partite", partitions=[[1, 2], [3, 4, 5], [6]])
```

**[FONTE]** `_partite_layout` (`graph.py:284-307`) marca
`nx_graph.nodes[v]["subset"] = i` e chama `nx.multipartite_layout`, cujo default
é `align="vertical"` → **colunas**. Dois detalhes que a doc registra e o código
confirma:

- vértices que você **não** listou em partição nenhuma entram numa partição
  extra, à direita (`graph.py:302-306`);
- `_partite_layout` **escreve no grafo** (`nodes[v]["subset"]`), violando o
  contrato do próprio `LayoutFunction`, que exige função pura (`graph.py:41`).
  Depois de um layout partite, `g._graph` carrega atributos `subset`.
  **[NÃO VERIFICADO]** quanto a efeito colateral observável.
- a checagem `if nx_graph.nodes[v] is None` (`graph.py:297-300`) **nunca** é
  verdadeira: para um vértice ausente, `nodes[v]` já levanta `KeyError`. Ou
  seja, partição com nome errado dá `KeyError` cru, não a mensagem amigável.

Uma rede neural em camadas é exatamente isto — é o exemplo `LinearNN` da doc
(`graph.py:1461-1486`): uma partição por camada, `layout_scale=3`,
`vertex_config={'radius': 0.20}`.

### 6.5 Layout manual: **pontos 3D, obrigatoriamente**

```python
POSICOES = {1: [-2, 0, 0], 2: [-1, 1, 0], 3: [0, 0, 0], 4: [1, 1, 0]}
g = Graph(V, E, layout=POSICOES)
```

**[FONTE]** `graph.py:453-454`: quando `layout` é dict, o código faz
`return layout` — **sem passar pelo `np.append(v, [0])`** que os layouts
automáticos recebem (`graph.py:466`). Depois, `change_layout` faz
`self[v].move_to(self._layout[v])`.

Consequência: um dicionário com pontos **2D** (`{1: [0, 0]}`) chega em
`Mobject.move_to` com shape (2,) e estoura no `shift`, com um
`ValueError: operands could not be broadcast together with shapes (2,) (3,)` —
um erro que não menciona grafo nenhum. **[NÃO VERIFICADO]** quanto ao texto
exato; o mecanismo (subtração numpy de shapes incompatíveis) é certo.

E `layout_scale` não faz nada aqui: as coordenadas do dicionário são
**coordenadas de cena**, diretas.

### 6.6 `LayoutFunction` própria

**[ÍNDICE]** o protocolo (`manim.mobject.graph.LayoutFunction`, fora do star
import):

```python
def __call__(self, graph: NxGraph, scale: float | tuple = 2,
             *args, **kwargs) -> dict[Hashable, Point3D]: ...
```

Contrato, do docstring (`graph.py:39-41`): **função pura — não modifique o grafo
recebido.** Ela recebe `scale=layout_scale` e o `**layout_config` inteiro.

```python
def grade(graph, scale=2, colunas=4, **kwargs):
    """Arruma os vértices em grade, em ordem estável de nome."""
    nos = sorted(graph)
    linhas = (len(nos) + colunas - 1) // colunas
    return {
        no: scale * np.array([(i % colunas) - (colunas - 1) / 2,
                              -(i // colunas) + (linhas - 1) / 2,
                              0])
        for i, no in enumerate(nos)
    }

g = Graph(V, E, layout=grade, layout_config={"colunas": 4})
```

Devolva **pontos 3D** (o `np.append` só roda no ramo dos layouts nomeados,
`graph.py:461-466`; uma função própria entra pelo ramo do `else`, linha 469, e
o retorno vai cru para o `move_to`).

Se o objeto que você passou não for chamável, o `except TypeError` transforma
tudo em uma mensagem só (`graph.py:471-476`):

```
ValueError: The layout 'sprng' is neither a recognized layout, a layout function,
nor a vertex placement dictionary.
```

Ou seja: **nome de layout digitado errado vira "não é função"**, não "nome
inválido". Se você viu essa mensagem, confira primeiro a grafia contra a
tabela do §6.2.

---

## 7. A armadilha-mor: `spring` e `random` mudam a cada render

**Esta é a seção que salva um dia de trabalho.** O layout default é `"spring"`,
e ele é aleatório.

### 7.1 O mecanismo, em três saltos

1. **[FONTE]** `networkx/drawing/layout.py:451` — `@np_random_state("seed")`
   decora `spring_layout`. Com `seed=None`, ele usa o **estado global do numpy**.
   (`random_layout` idem, `layout.py:63`.)
2. **[FONTE]** `manim/scene/scene.py:180, 223-224` — o `Scene.__init__` faz:
   ```python
   self.random_seed = random_seed if random_seed is not None else config.seed
   random.seed(self.random_seed)
   np.random.seed(self.random_seed)
   ```
3. **[FONTE]** `config.seed` não tem valor no `default.cfg` do ManimCE e
   **[HOJE]** não aparece no `manim.cfg` deste projeto (`grep -n seed manim.cfg`
   → nada). Logo `config.seed is None` → `np.random.seed(None)` → o numpy
   **reembaralha a partir da entropia do sistema** a cada processo.

**Resultado:** dois renders da mesma cena produzem grafos com vértices em
lugares diferentes. Sem erro. Sem aviso.

### 7.2 Por que isso é FATAL numa cena em partes

O formato de **`manim-presentation-parts`** garante que o primeiro frame da
parte N+1 é, pixel a pixel, o último da parte N — porque é o mesmo código
rodando de novo, com `skip_animations`. Um layout aleatório **quebra essa
garantia**: cada parte é um processo diferente, cada processo sorteia outro
layout, e a emenda vira um salto do grafo inteiro.

E a métrica direcional de emenda (tinta que some) vai acusar centenas ou
milhares de pixels — muito acima do limiar de 400 px em 1920×1080. Se você
mediu uma emenda estourada numa cena com `Graph`, **suspeite disto antes de
qualquer outra coisa**.

O mesmo vale, em menor grau, para o cache de partial movies: o hash da chamada
de `play` muda a cada execução, então **nada** é reaproveitado
(`manim-performance-cache`).

### 7.3 As correções, em ordem de preferência

```python
# 1. LOCAL e explícita — a melhor. Vai direto para o nx.spring_layout.
g = Graph(V, E, layout="spring", layout_config={"seed": 42})

# 2. Determinismo por construção: escolha um layout que não sorteia.
g = Graph(V, E, layout="circular")     # ou kamada_kawai, shell, tree, partite…

# 3. Congele o resultado UMA vez e escreva o dicionário na cena.
#    (rode uma vez com print(g._layout), cole o dict, use layout=POSICOES)
g = Graph(V, E, layout=POSICOES)
```

A opção 3 é a que o §1 recomenda para diagrama de aula: layout automático é
ótimo para **explorar**, e ruim para **entregar**.

**O que NÃO resolve:** `mx render` **não expõe `--seed`**. **[HOJE]**
`manimx/cli.py:457-476` lista as flags do subcomando `render` e `--seed` não
está lá; ela existe só no `bin/manim` (`manim/cli/render/global_options.py:147-152`).
Um `config.seed = 42` no topo do módulo de cena funciona — mas é estado global,
e não protege quem importar a cena de outro jeito. Prefira `layout_config`.

---

## 8. `change_layout` — o que ele desfaz

**[ÍNDICE]**

```python
GenericGraph.change_layout(self, layout="spring", layout_scale=2,
                           layout_config=None, partitions=None,
                           root_vertex=None) -> Graph
```

**[FONTE]** o corpo inteiro (`graph.py:1256-1271`) faz três coisas:

```python
if partitions is not None and "partitions" not in layout_config:
    layout_config["partitions"] = partitions
if root_vertex is not None and "root_vertex" not in layout_config:
    layout_config["root_vertex"] = root_vertex
self._layout = _determine_graph_layout(self._graph, layout, layout_scale, layout_config)
for v in self.vertices:
    self[v].move_to(self._layout[v])
```

Daí saem três armadilhas, todas de leitura direta:

### 8.1 Ele recentraliza na ORIGEM e joga fora `shift`/`move_to`/`scale`

Os layouts do networkx centram em `center=None` → origem, e `_tree_layout`
subtrai o próprio centro. `self._layout` nunca soube que você mexeu no grafo:
**[HOJE]** `grep -n "_layout\b" graph.py` mostra que ele só é escrito em
**4 lugares** — `change_layout` (1262), `_add_created_vertex` (755),
`_remove_vertex` (964, um `pop`) e o `__init__` via `change_layout` (619).
`shift`, `scale` e `move_to` não tocam nele.

Então:

```python
g = Graph(V, E, layout="circular").scale(1.4).to_edge(LEFT)
self.play(g.animate.change_layout("kamada_kawai"))
#  → o grafo PULA para o centro do quadro, com as posições em escala 2.
#    (os Dots continuam 1,4× maiores — só as POSIÇÕES voltaram)
```

**A correção:** reposicione depois, na mesma animação.

```python
alvo = g.copy().change_layout("kamada_kawai").scale(1.4).to_edge(LEFT)
self.play(Transform(g, alvo))
```

…ou passe `center` pelo `layout_config`, que os layouts do networkx aceitam
(`layout.py`, coluna `center=None` em todas as assinaturas do §6.2) — lembrando
que ele é 2D ali, porque o `np.append(v,[0])` vem depois. **[NÃO VERIFICADO]**
para `tree`/`partite`, que não têm `center` na assinatura.

### 8.2 Ele MUTA o `layout_config` que você passou

`layout_config` não é copiado; `layout_config["partitions"] = …` escreve no seu
dicionário. Reusar uma constante de classe entre duas chamadas contamina a
segunda:

```python
LAYOUT_CONFIG = {"vertex_spacing": (0.5, 1)}
g.change_layout("tree", root_vertex="ROOT", layout_config=LAYOUT_CONFIG)
#   LAYOUT_CONFIG agora é {"vertex_spacing": (0.5,1), "root_vertex": "ROOT"}
g.change_layout("circular", layout_config=LAYOUT_CONFIG)
#   → nx.circular_layout(G, scale=2, vertex_spacing=…, root_vertex=…) → TypeError
```

**[NÃO VERIFICADO]** por execução; a mutação está em `graph.py:1258-1261`, sem
cópia. Passe `layout_config=dict(LAYOUT_CONFIG)`.

### 8.3 `.animate.change_layout(...)` funciona, e por quê

`change_layout` **não** tem `override_animate`, então `.animate` cai no
caminho genérico: `_AnimationBuilder` faz `generate_target()` (uma cópia
profunda do grafo), aplica o método no alvo e monta um `_MethodAnimation`
(família `Transform`). Como só as posições mudaram e a contagem de submobjects
é a mesma, a interpolação é bem-comportada — é o exemplo oficial
(`graph.py:1241-1255`).

Durante essa animação o updater do grafo fica **suspenso**
(**[ÍNDICE]** `Animation.__init__(..., suspend_mobject_updating: bool = True)`,
`animation/animation.py:137`), e as arestas interpolam como pontos. Isso é
correto para troca de layout — e é a razão de a aresta não "chicotear".

---

## 9. Mutação animada: vértices e arestas entrando e saindo

### 9.1 As quatro operações, com e sem animação

**[FONTE]** `add_vertices`, `remove_vertices`, `add_edges` e `remove_edges`
têm cada uma um par decorado com `@override_animate` (`graph.py:923, 1004,
1128, 1183`). Ou seja, `g.animate.add_vertices(...)` **não** é um `Transform` —
é um `AnimationGroup` construído à mão.

```python
# imediato
g.add_vertices(5, 6, positions={5: [2, 1, 0], 6: [2, -1, 0]},
               vertex_config={"radius": 0.2, "color": ACENTO})
g.add_edges((1, 5), (5, 6))
g.remove_edges((1, 2))
g.remove_vertices(3)

# animado
self.play(g.animate.add_vertices(5, positions={5: [2, 1, 0]}))
self.play(g.animate.add_edges((1, 5)))
self.play(g.animate.remove_vertices(3))
```

**A animação usada em cada caso** (`graph.py:927, 1008, 1131, 1187`):

| Operação | Animação default | Como trocar |
|---|---|---|
| `add_vertices` | `Create` | `anim_args={"animation": FadeIn}` |
| `add_edges` | `Create` | idem |
| `remove_vertices` | `Uncreate` | `anim_args={"animation": FadeOut}` |
| `remove_edges` | `Uncreate` | idem |

`anim_args` também carrega `run_time`, `rate_func`, `lag_ratio` — tudo que
`manim-composicao-ritmo` cobre:

```python
self.play(g.animate.add_edges((1, 5), (5, 6),
                              anim_args={"animation": FadeIn, "run_time": 0.8}))
```

### 9.2 Encadeamento com `.animate` é **proibido** aqui

**[FONTE]** `mobject/mobject.py:3443-3446`:

```python
if (self.is_chaining and has_overridden_animation) or self.overridden_animation:
    raise NotImplementedError(
        "Method chaining is currently not supported for overridden animations")
```

Então **as duas** formas abaixo levantam `NotImplementedError`:

```python
g.animate.add_vertices(5).shift(UP)      # ✗
g.animate.shift(UP).add_vertices(5)      # ✗
```

Separe em dois `play`, ou em duas animações dentro do mesmo `play`
(`self.play(g.animate.add_vertices(5), outra_coisa.animate.shift(UP))`).

### 9.3 `add_edges` cria vértices faltantes — **no centro do grafo**

**[FONTE]** `graph.py:1044` (`_add_edge`) e `graph.py:707-708` (`_create_vertex`):

```python
added_mobjects = [self._add_vertex(v) for v in edge if v not in self.vertices]
...
np_position = self.get_center() if position is None else np.asarray(position)
```

`g.add_edges((1, 99))` com o vértice 99 inexistente **cria** o 99 — empilhado no
centro geométrico do grafo, com config default. Numa árvore que cresce, todos
os filhos novos nascem no mesmo ponto e ficam sobrepostos até o próximo
`change_layout`.

É exatamente o que o exemplo `LargeTreeGeneration` da doc faz de propósito
(`graph.py:1522-1560`): cria com `positions={k: g.vertices[pai].get_center() + 0.1*DOWN}`
e só depois anima `g.animate.change_layout("tree", root_vertex="ROOT", …)`.
**Nascer no pai e depois abrir a árvore** é o idioma; nascer no centro é o
default e quase nunca é o que você quer.

### 9.4 `remove_vertices` leva as arestas incidentes junto

**[FONTE]** `graph.py:969-976` — o `_remove_vertex` recolhe
`[e for e in self.edges if vertex in e]` e devolve tudo num `VGroup`. O
docstring traz o retorno literal:

```
>>> G = Graph([1, 2, 3], [(1, 2), (2, 3)])
>>> removed = G.remove_vertices(2, 3); removed
VGroup(Line, Line, Dot, Dot)
```

Ou seja: as duas linhas saem junto com os dois pontos, e o `Uncreate` do
`.animate` cai sobre os quatro. É o comportamento certo — só não conte com
"remover um vértice remove um mobject".

### 9.5 Uma assimetria observada, sem consequência conhecida

**[FONTE]** três dos quatro `AnimationGroup` gerados passam `group=self`
(`graph.py:938, 1012, 1135`); o de `_remove_edges_animation` (`graph.py:1190`)
**não** passa. **[NÃO VERIFICADO]** que efeito isso tem — provavelmente nenhum
visível, já que as arestas já foram destacadas do grafo antes da animação
começar. Registrado para quem for depurar um `remove_edges` que se comporta
diferente dos outros três.

---

## 10. Destacar um caminho

Esta é a coisa que mais se pede a um grafo em aula: "mostra o caminho de A
até B". São quatro peças.

### 10.1 Achar o caminho — o networkx já está instalado

**[HOJE]** `networkx>=2.6` é **dependência declarada** do ManimCE
(`manim-*.dist-info/METADATA`), e a versão instalada aqui é **3.6.1**. Não
precisa instalar nada, e `g._graph` já é o objeto que o networkx entende.

```python
import networkx as nx

caminho = nx.shortest_path(g._graph, 1, 6)          # [1, 3, 5, 6]
pares   = list(zip(caminho, caminho[1:]))           # [(1,3), (3,5), (5,6)]
arestas = [aresta(g, u, v) for u, v in pares]       # o helper do §5.2 — indispensável
```

**O helper do §5.2 não é opcional.** `nx.shortest_path` devolve os vértices na
ordem do percurso; `g.edges` está indexado pela tupla **como você escreveu na
lista de arestas**. Num `Graph` não dirigido, metade dos pares vem invertida e
`g[(u, v)]` levanta `ValueError` (§3.2).

### 10.2 Recolorir — o mais legível, e o que fica na tela

```python
self.play(*[a.animate.set_stroke(ACENTO, width=6) for a in arestas],
          *[g[v].animate.set_color(ACENTO) for v in caminho],
          lag_ratio=0.15)
```

`lag_ratio` num `play` com várias animações é de **`manim-composicao-ritmo`**.
Para um frame de repouso num slide, este é o resultado que você quer: o
caminho **permanece** destacado enquanto o professor fala.

### 10.3 Um ponto correndo pela rede

```python
bolinha = Dot(color=ACENTO, radius=0.12).move_to(g[caminho[0]])
self.add(bolinha)
self.play(Succession(*[MoveAlongPath(bolinha, a) for a in arestas]))
```

`MoveAlongPath` percorre a `Line` na direção em que ela foi **construída**, e o
helper do §5.2 devolve metade das arestas invertidas — nessas, o ponto anda
para trás. Não tente corrigir girando a aresta: construa a trajetória na ordem
do caminho, com uma `Line` descartável.

```python
trilhos = [Line(g[u].get_center(), g[v].get_center()) for u, v in pares]
self.play(Succession(*[MoveAlongPath(bolinha, t) for t in trilhos]))
```

`Succession` e `MoveAlongPath` são de **`manim-composicao-ritmo`** e
**`manim-animations`**.

### 10.4 `ShowPassingFlash` numa aresta **desmonta o grafo**

Este é o defeito silencioso mais caro desta skill, e ele só aparece **depois**.

**[FONTE]** `animation/indication.py:308-312`:

```python
super().__init__(mobject, remover=True, introducer=True, **kwargs)
```

`remover=True` → ao terminar, a animação chama `scene.remove(a_aresta)`.
E **[FONTE]** `Scene.remove` → `restructure_mobjects`, cujo próprio docstring
(`scene/scene.py:698-706`) diz o que faz:

> *If your scene has a Group(), and you removed a mobject from the Group, this
> dissolves the group and puts the rest of the mobjects directly in
> self.mobjects.*

O grafo é um `VMobject` com submobjects. Remover **uma aresta** da cena
**dissolve o grafo**: ele deixa de estar em `self.mobjects` e no lugar dele
entram os seus filhos, soltos.

O estrago aparece na animação **seguinte**: **[FONTE]** `Scene.update_mobjects`
(`scene/scene.py:392-393`) é `for mobj in self.mobjects: mobj.update(dt)` — só
os mobjects **de topo**. Com o grafo fora dessa lista, `update_edges` nunca mais
roda, e **as arestas param de seguir os vértices**. Nada dá erro; o vídeo sai
com as linhas presas no ar.

**A correção é uma palavra: `copy()`.**

```python
self.play(*[ShowPassingFlash(a.copy().set_stroke(ACENTO, width=8), time_width=0.5)
            for a in arestas])
```

**A mesma regra vale para qualquer animação `remover=True` aplicada a uma peça
do grafo:** `FadeOut(g[3])`, `Uncreate(g[(1,2)])`, `ShowPassingFlash`. Se você
quer **tirar** a peça, use a API do grafo — `g.animate.remove_vertices(3)`,
`g.animate.remove_edges((1,2))` — que destaca o mobject **antes** de animar
(`graph.py:1010, 1189`) e por isso não dissolve nada. Se você quer só
**destacar**, anime uma cópia.

Animações que **não** removem e são seguras direto na peça: `Indicate`,
`Wiggle`, `Circumscribe`, `Flash`, `.animate.set_color(...)`, `.animate.scale(...)`.
O exemplo `MovingVertices` da própria doc usa `Wiggle(g[(1, 2)])`
(`graph.py:1367`).

---

## 11. O custo: o updater derruba o cache de frame estático

**[FONTE]** `Scene.get_moving_mobjects` (`scene/scene.py:899-946`):

```python
mobjects = self.get_mobject_family_members()
for i, mob in enumerate(mobjects):
    update_possibilities = [
        mob in animation_mobjects,
        len(mob.get_family_updaters()) > 0,
        mob in self.foreground_mobjects,
    ]
    if any(update_possibilities):
        return mobjects[i:]        # <-- daqui para a FRENTE, tudo é "moving"
```

Leia a linha do `return`. Assim que a varredura encontra **um** mobject com
updater, **tudo o que vem depois dele** na ordem da cena é declarado móvel e sai
do cache de frame estático — precisa ser rasterizado de novo a cada frame.

Um `Graph` **sempre** tem updater (§3.4). Logo:

| Decisão | Efeito |
|---|---|
| `self.add(grafo)` **antes** do plano de fundo, do título e do rodapé | o fundo inteiro é re-rasterizado 60×/s pelo resto da cena |
| `self.add(fundo, titulo, rodape)` e **depois** `self.add(grafo)` | só o grafo é móvel |
| `grafo.clear_updaters()` quando ele parar de se mexer | o grafo volta a ser estático |

**A regra:** **o grafo entra por último**, e quando ele parar de andar,
`g.clear_updaters()`. Depois disso, mover um vértice deixa a aresta para trás —
que é exatamente o que você quer num diagrama parado.

O tamanho também conta: um `Graph` com V vértices e A arestas tem
**V + A submobjects diretos** (mais os rótulos, que são filhos dos
`LabeledDot`). Um grafo de 30 nós e 60 arestas é um `VMobject` de ~90 filhos
sendo rasterizado a cada frame. Escolher `Dot` em vez de `LabeledDot` corta os
rótulos, que são `MathTex` — os mais caros da lista.

Cache de partial movies, `max_files_cached` e o que o hash enxerga são de
**`manim-performance-cache`**; codec e GPU são de **`manim-gpu-encoding`**.

---

## 12. `from_networkx` e o resto do networkx

### 12.1 A ponte

**[ÍNDICE]** `GenericGraph.from_networkx(nxgraph, **kwargs)` — `classmethod`.
**[FONTE]** o corpo é uma linha (`graph.py:1226`):

```python
return cls(list(nxgraph.nodes), list(nxgraph.edges), **kwargs)
```

Ou seja: `from_networkx` **não** herda nada além de nós e arestas. Pesos,
atributos de nó, cores guardadas no grafo do networkx — tudo se perde. Se você
tem atributos, leia-os você mesmo e converta em `vertex_config`/`edge_config`:

```python
import networkx as nx
nxg = nx.erdos_renyi_graph(14, 0.5, seed=7)          # seed! §7

g = Graph.from_networkx(nxg, layout="spring", layout_scale=3.5,
                        layout_config={"seed": 7},
                        vertex_config={"radius": 0.16, "color": ACENTO},
                        edge_config={"stroke_color": TINTA, "stroke_width": 2})
```

`Graph.from_networkx` devolve `Graph`; `DiGraph.from_networkx` devolve
`DiGraph` (é `cls(...)`). Passar um `nx.DiGraph` para `Graph.from_networkx`
funciona e **perde a direção** — as arestas viram um `nx.Graph` interno.

### 12.2 O que o networkx resolve e você não deveria reimplementar

Com `g._graph` na mão (ou o `nxg` original):

```python
nx.shortest_path(G, a, b)              # caminho mínimo → lista de vértices
nx.shortest_path_length(G, a, b)
nx.dijkstra_path(G, a, b, weight="peso")
nx.bfs_edges(G, raiz)   /  nx.dfs_edges(G, raiz)     # a ORDEM da travessia
nx.topological_sort(G)                 # só DiGraph acíclico
nx.minimum_spanning_edges(G)
nx.connected_components(G)
nx.degree(G)  /  nx.is_tree(G)  /  nx.check_planarity(G)
```

`nx.bfs_edges`/`dfs_edges` são particularmente úteis em aula: eles dão a
sequência de arestas na ordem em que o algoritmo as descobre, que é exatamente
a ordem de um `Succession` (`manim-composicao-ritmo`) — a animação vira uma
tradução direta do algoritmo.

### 12.3 Quando usar só o layout do networkx, sem `Graph`

Se você quer os `Rectangle` rotulados do §1 mas não quer decidir posição na
mão, chame o layout direto e posicione os seus próprios mobjects:

```python
import networkx as nx
pos = nx.spring_layout(nxg, scale=3, seed=42)       # {no: array([x, y])}
for nome, caixa in caixas.items():
    x, y = pos[nome]
    caixa.move_to([x, y, 0])                        # o 3º eixo é seu
```

Você fica com layout automático, formas próprias e nenhum updater — o melhor
dos dois lados quando o grafo não muda.

---

## 13. Legibilidade: o que decidir antes de renderizar

Um grafo bonito na documentação do Manim (fundo escuro, 8 nós, tela cheia) vira
ilegível num slide (canvas claro, com título e rodapé, projetado a 6 m). A
tabela abaixo é o mínimo para não descobrir isso depois do render.

| Decisão | Valor de partida | Por quê |
|---|---|---|
| `layout_scale` | **3** com o grafo sozinho; **2** se dividir o palco | 3 → caixa de 6 unidades ≈ 810 px; ainda cabe em 8 de altura com folga para título |
| raio do vértice | `vertex_config={"radius": 0.20}` | o default 0,08 dá **21,6 px** de diâmetro (§4.4) |
| `stroke_width` da aresta | 2–3 | o default do `VMobject` é 4 [ÍNDICE]; num grafo denso vira mancha |
| rótulo | `labels={v: Text(str(v), font_size=20, color=TINTA)}` | `labels=True` passa pelo `MathTex` (§4.3) e italiza tudo |
| cor | **sempre explícita** | branco no branco (§4.5) |
| número de nós | ≤ 12 numa tela cheia | acima disso os rótulos se tocam, e o layout não sabe do tamanho deles (§4.4) |
| direção | `DiGraph` só se a direção **for o assunto** | a ponta de seta come ~0,3 unidade de cada aresta e polui grafo denso |

Caber ou não caber na tela, margem, `is_off_screen()` e as réguas
(`FullScreenRectangle`) são de **`manim-layout-posicionamento`**. Contraste e
paleta são de **`manim-color-theming`**.

---

## 14. Uma cena de referência, comentada

Não foi renderizada. Toda assinatura usada está conferida no índice ou no
fonte, com a seção que a justifica ao lado.

```python
"""Rede de serviços: quem chama quem, e o caminho de uma requisição."""
import networkx as nx
from manim import *

from tema import CANVAS, TINTA, ACENTO, T_LEGENDA      # manim-tema-projeto


NOS = ["cliente", "api", "fila", "worker", "banco"]
ARESTAS = [("cliente", "api"), ("api", "fila"), ("fila", "worker"),
           ("worker", "banco"), ("api", "banco")]      # a ORDEM é o índice (§5.2)

POSICOES = {                                            # §7.3 opção 2/3: determinístico
    "cliente": [-5.0,  0.0, 0],
    "api":     [-2.2,  0.0, 0],
    "fila":    [ 0.6,  1.4, 0],
    "worker":  [ 3.4,  1.4, 0],
    "banco":   [ 3.4, -1.4, 0],
}


def aresta(g, u, v):
    """A Line de (u,v) na direção em que ela foi registrada — §5.2."""
    return g.edges.get((u, v)) or g.edges[(v, u)]


class RedeDeServicos(Scene):
    def construct(self):
        self.camera.background_color = CANVAS

        g = DiGraph(                                    # §5.3: direção É o assunto
            NOS, ARESTAS,
            layout=POSICOES,                            # §6.5: pontos 3D
            labels={v: Text(v, color=TINTA, font_size=20) for v in NOS},   # §4.3
            vertex_config={"radius": 0.42, "color": ACENTO,
                           "fill_opacity": 1.0},        # §4.5: cor explícita
            edge_config={"stroke_color": TINTA, "stroke_width": 3,
                         "tip_config": {"tip_length": 0.22}},
        )

        # §11: o grafo entra DEPOIS do cenário fixo, e é o único móvel.
        # OBRIGATÓRIO, e é o defeito mais caro desta skill (§10.4): sem esta
        # linha o que entra em scene.mobjects são os Dot e as Line SOLTOS —
        # `Animation._setup_scene` (animation.py:257-261) adiciona o mobject da
        # ANIMAÇÃO, não o pai. E `Scene.update_mobjects` (scene.py:392-393) só
        # percorre o topo, então `update_edges` NUNCA roda e as arestas
        # congelam, sem erro.
        self.add(g)
        for v in NOS:                     # invisíveis até o LaggedStart abaixo
            g.vertices[v].set_opacity(0)
        self.play(LaggedStart(*[FadeIn(g.vertices[v]) for v in NOS], lag_ratio=0.12))
        self.play(LaggedStart(*[Create(aresta(g, u, v)) for u, v in ARESTAS],
                              lag_ratio=0.10))
        self.wait(0.4)

        # o caminho da requisição — §10.1
        caminho = nx.shortest_path(g._graph, "cliente", "banco")
        pares = list(zip(caminho, caminho[1:]))

        # §10.4: pisca uma CÓPIA, nunca a aresta do grafo
        self.play(*[ShowPassingFlash(aresta(g, u, v).copy().set_stroke(ACENTO, width=9),
                                     time_width=0.6, run_time=1.2)
                    for u, v in pares])

        # §10.2: o destaque que FICA, para o frame de repouso
        # §10.2: `set_color` desce na FAMÍLIA (vectorized_mobject.py:473-476), e
        # com `labels` o vértice virou LabeledDot (graph.py:594-595) — o Text é
        # submobject dele. `g[v].animate.set_color(...)` repintaria o RÓTULO da
        # mesma cor do disco e ele sumiria. Pinte só o disco: submobject 0.
        self.play(*[aresta(g, u, v).animate.set_stroke(ACENTO, width=5) for u, v in pares],
                  *[g[v][0].animate.set_color(ACENTO) for v in caminho],
                  run_time=0.6)

        # §11: acabou o movimento — o grafo volta a ser estático.
        # Só faz sentido porque o `self.add(g)` lá em cima pôs o updater
        # `update_edges` para rodar de verdade; sem ele isto seria no-op.
        g.clear_updaters()
        self.wait(0.4)
```

O que este exemplo **não** faz de propósito: não usa `labels=True` (§4.3), não
usa `layout="spring"` (§7), não pisca a aresta original (§10.4), não põe título
dentro do vídeo (isso é do slide — `manim-presentation-parts`).

---

## 15. Conferir sem renderizar

Três coisas dão para checar em milissegundos, e cobrem os erros mais caros
desta skill. **[NÃO VERIFICADO]** — os comandos abaixo foram escritos, não
executados nesta sessão.

**1. Layout não determinístico numa cena que vai virar vídeo:**

```bash
grep -nE 'layout\s*=\s*"(spring|random)"' cena.py \
  | grep -v 'seed' \
  && echo "^^ layout aleatório sem seed — leia a §7"
```

Um `Graph(V, E)` **sem `layout=`** também cai aqui (o default é `"spring"`):

```bash
grep -nE '\b(Di)?Graph\(' cena.py | grep -v 'layout'
```

**2. Aresta destacada sem `.copy()`** — o §10.4:

```bash
grep -nE '(ShowPassingFlash|FadeOut|Uncreate)\([^)]*(g\.edges|g\[\()' cena.py \
  | grep -v '\.copy()' \
  && echo "^^ animação remover=True sobre peça do grafo — dissolve o grafo"
```

**3. Chave de `edge_config` que não existe na lista de arestas** — o §5.2.
Um script de 12 linhas com `ast`, sem importar o Manim:

```python
import ast, sys

fonte = ast.parse(open(sys.argv[1]).read())
tuplas = {
    tuple(ast.literal_eval(e) for e in no.elts)
    for no in ast.walk(fonte)
    if isinstance(no, ast.Tuple) and len(no.elts) == 2
    and all(isinstance(e, ast.Constant) for e in no.elts)
}
# arestas e chaves de edge_config saem do MESMO conjunto de tuplas;
# o que interessa é achar par simétrico: (a,b) e (b,a) no mesmo arquivo.
invertidas = {(a, b) for (a, b) in tuplas if (b, a) in tuplas and a != b}
if invertidas:
    print("tuplas presentes nos DOIS sentidos (§5.2):", sorted(invertidas))
```

O ciclo completo de verificação — renderizar rápido, **olhar o PNG**, corrigir —
é de **`manim-verificacao-visual`**. Os três defeitos que esta skill produz e que
**não dão erro nenhum** são: grafo branco no fundo branco (§4.5), layout que
muda entre partes (§7.2) e arestas congeladas depois de um flash (§10.4). Os
três só aparecem na imagem.

---

## 16. Onde esta skill para

| Você quer | Vá para |
|---|---|
| plotar uma **função**, eixos, `BarChart`, curva | **`manim-graphs-plots`** — "graph" ali é plot |
| grade de células com texto, `Matrix`, determinante | **`manim-tabelas-matrizes`** |
| 5 caixas e setas de um diagrama de arquitetura | **`manim-mobjects`** (as formas) + **`manim-layout-posicionamento`** (onde) — e §1 aqui |
| `Arrow`, `CurvedArrow`, `Brace`, `SurroundingRectangle`, as 8 pontas de seta | **`manim-mobjects`** |
| posicionar, medir, caber na tela, `z_index`, margem | **`manim-layout-posicionamento`** |
| `Transform` × `ReplacementTransform`, catálogo de animações, `.animate` genérico | **`manim-animations`** |
| `rate_func`, `lag_ratio`, `LaggedStart`, `Succession`, orçamento de tempo | **`manim-composicao-ritmo`** |
| `always_redraw`, `ValueTracker`, updater próprio, `TracedPath` | **`manim-updaters-valuetracker`** |
| paleta, contraste, `set_default`, o grafo que sumiu no branco **como decisão de tema** | **`manim-color-theming`** (a §4.5 **desta** skill só registra o sintoma) |
| o `tema.py` como contrato do projeto | **`manim-tema-projeto`** |
| `Text` vs `MathTex`, LaTeX quebrado, fonte ausente | **`manim-text-latex`** |
| zoom/pan/`auto_zoom` para caber uma árvore grande | **`manim-camera-2d`** |
| cortar a cena em partes que o apresentador avança | **`manim-presentation-parts`** — e leia a §7.2 antes |
| cache, `--no-cache`, o que custa rasterizar | **`manim-performance-cache`** |
| renderizar, qualidade, formato, caminho da saída | **`manim-render-api`** |
| olhar o PNG, conferir o resultado | **`manim-verificacao-visual`** |
| escrever um `Mobject`/`Animation` próprio, Bézier | **`manim-mobjects-customizados`** |
| descobrir se um nome existe, assinatura, kwarg | **`manim-api-discovery`** |

**Buracos declarados** (nesta rodada ninguém cobre; não invente skill):

- `VectorField`, `ArrowVectorField`, `StreamLines` — rede ≠ campo vetorial;
- `LinearTransformationScene`, `VectorScene`, `ApplyMatrix` — álgebra linear de
  cena;
- os 48 espelhos `OpenGL*` de `mobject/opengl` — no fluxo de aula o renderer é
  cairo;
- animação de **algoritmo** sobre grafo (Dijkstra passo a passo, coloração)
  não tem API no Manim: é `Succession` sobre `nx.bfs_edges`/`dfs_edges`
  escrito à mão (§12.2).

---

## 17. O que ficou marcado como NÃO VERIFICADO

Nenhum render, nenhum `ffmpeg`, nenhuma GPU foi usada para escrever este
arquivo. Tudo o que é assinatura, default, categoria ou linha de fonte foi
conferido; o que segue é **dedução de leitura** e merece um render de
confirmação antes de virar dogma:

| § | Afirmação | O que confirmaria |
|---|---|---|
| 3.5 | `buff`/`path_arc` de `edge_config` são desfeitos no primeiro frame pelo `.get("buff", 0)` sobre dict de tuplas | um PNG com `edge_config={"buff": 0.3}` depois de um `wait` |
| 4.2 | vértice com nome de kwarg (`"color"`) vira `Dot(**valor)` → `TypeError` | um `Graph(["color"], [], vertex_config={"color": BLUE})` |
| 4.3 | `vertex_type` ≠ `Dot` com `labels=True` passa `label=` para uma classe que não aceita | `Graph(V, E, labels=True, vertex_type=Square)` |
| 5.1 | `edge_config[e].pop("tip_config")` muta o dicionário do chamador | dois `DiGraph` com a mesma constante |
| 5.2 | chave `(v,u)` invertida é descartada em silêncio (inclusive no exemplo `LabeledModifiedGraph` da própria doc) | render do exemplo: 1 de 3 arestas vermelhas |
| 5.4 | rótulo de `LabeledLine` não acompanha a aresta quando o vértice se move | um `Graph(edge_type=LabeledLine)` com `.animate.move_to` |
| 6.3 | `layout_scale` como tupla quebra em todo layout do networkx (só `tree` trata) | `Graph(V, E, layout="circular", layout_scale=(3,2))` |
| 6.4 | `_partite_layout` escreve `subset` no `_graph` (viola o contrato do `LayoutFunction`) | inspecionar `g._graph.nodes(data=True)` |
| 6.5 | dicionário de layout 2D estoura no `move_to` com erro de broadcast do numpy | `Graph([1], [], layout={1: [0, 0]})` |
| 8.1 | `change_layout` recentraliza na origem e descarta `shift`/`to_edge` | dois PNGs, antes e depois |
| 8.2 | `change_layout` muta o `layout_config` recebido | duas chamadas com a mesma constante |
| 9.5 | `_remove_edges_animation` é o único sem `group=self` | comportamento comparado das quatro |
| 15 | os três conferidores (`grep` e o script `ast`) | rodá-los sobre uma cena real |

Onde o mecanismo está lido linha a linha, o texto diz **[FONTE]** com arquivo e
linha — isso vale como afirmação forte. A tabela acima é só sobre o **efeito
observável**, que ninguém olhou.
