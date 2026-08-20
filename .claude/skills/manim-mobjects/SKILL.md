---
name: manim-mobjects
description: >-
  O CATÁLOGO de objetos visuais do Manim e o modelo por trás deles: as 57
  classes de `mobject/geometry` (círculo, retângulo arredondado, polígono,
  estrela, linha, seta, ponta de seta, chave/`Brace`, retângulo de destaque,
  booleanos, casco convexo), o par `Mobject`/`VMobject`, pontos × submobjects ×
  família, `VGroup` × `Group` × `VDict`, estilo mecânico (`set_fill`,
  `set_stroke`, `family=`), tamanho (`scale_to_fit_*`, `stretch_to_fit_*`,
  `match_*`), cópia, `become`, `save_state` e a caixa delimitadora que decide
  tudo. Use quando a pergunta for "que forma eu uso para isso?", "como faço uma
  caixa arredondada / uma seta / uma chave / um destaque / um risco tracejado?",
  "como eu agrupo isso", "por que o VGroup deu TypeError", "por que meu objeto
  ficou maior do que eu pedi", "por que a seta ficou curta / fina", "por que o
  traço vazou da caixa", "sumiu o grupo inteiro quando removi uma peça", "como
  descubro o índice desse submobject", "isso é `Mobject` ou `VMobject`?". NÃO
  use para: posicionar, alinhar, medir margem, enquadrar e z-index
  (`manim-layout-posicionamento`); animar (`manim-animations`) e ritmo
  (`manim-composicao-ritmo`); escolher cor, contraste e tema
  (`manim-color-theming`); texto e LaTeX (`manim-text-latex`); eixos e gráficos
  (`manim-graphs-plots`); tabela e matriz (`manim-tabelas-matrizes`); grafo
  (`manim-grafos-redes`); 3D (`manim-3d-camera`); SVG, PNG e fonte
  (`manim-svg-imagens`); escrever Mobject, Animation ou caminho de Bézier
  próprio (`manim-mobjects-customizados`); apenas descobrir se um nome existe
  (`manim-api-discovery`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Mobjects — o catálogo e o modelo

Tudo que aparece num frame do Manim é um **Mobject**. Esta skill é o catálogo
(que classe existe, com que assinatura, para que serve, quando NÃO serve) e o
modelo por trás dele (pontos, submobjects, família, caixa delimitadora) — que é
o que explica quase todo comportamento "estranho" da biblioteca.

**Como cada afirmação foi apurada.** Marcadores usados aqui:

- **[FONTE]** — conferido no código de `.venv/lib/python3.12/site-packages/manim/`
  (ManimCE 0.21.0) ou no índice `api/manim-ce-index.tsv` / `api/manim-ce-methods.tsv`,
  gerados por reflexão do pacote instalado. É afirmação forte.
- **[DECK]** — medido no deck consumidor `~/Projects/aulas` (12 arquivos de cena,
  ~76 classes, 59 partes em produção). Eles mediram; não foi reproduzido aqui.
- **[NÃO VERIFICADO]** — derivado da leitura do fonte, sem execução. Nesta
  redação **nenhum render, nenhum `ffmpeg`, nenhum benchmark foi executado**.

---

## 1. O modelo: pontos, submobjects, família

Um `Mobject` é um **nó de árvore** com duas coisas dentro:

| | O que é | Quem tem |
|---|---|---|
| `mob.points` | as coordenadas do desenho DESTE nó | quem desenha algo por si |
| `mob.submobjects` | a lista ordenada de filhos | quem é composto |

Um `Circle` tem pontos e nenhum filho. Um `VGroup` tem filhos e nenhum ponto.
Um `Text` tem filhos (os glifos) e nenhum ponto próprio. Um
`Rectangle(grid_xstep=1)` tem **os dois** — a moldura em `points` e as linhas da
grade num submobject ([FONTE] `polygram.py`, `Rectangle.__init__` termina em
`self.add(self.grid_lines)`).

Três consultas resolvem qualquer dúvida sobre um mobject desconhecido:

```python
mob.has_points()         # este nó desenha algo por si?
len(mob.submobjects)     # quantos filhos diretos
mob.get_family()         # este nó + todos os descendentes, recursivo
```

### 1.1 O nó entra no próprio índice — e isso surpreende

[FONTE] `mobject.py:2497-2524`. `__getitem__`, `__iter__` e `__len__` do
`Mobject` incluem **o próprio nó** na sequência quando ele tem pontos:

```python
def __iter__(self):
    return it.chain([self] if self.has_points() else [], self.submobjects)

def __len__(self):
    return len(self.submobjects) + (1 if self.has_points() else 0)
```

Consequências práticas:

```python
g = VGroup(a, b, c)
len(g)      # 3   — VGroup não tem pontos próprios
g[0] is a   # True

c = Circle()
len(c)      # 1   — o círculo tem pontos e nenhum filho
c[0] is c   # True
for x in c: ...   # roda UMA vez, com x == c

r = Rectangle(grid_xstep=1.0)
len(r)      # 2   — o retângulo (pontos) + o VGroup da grade
r[0] is r   # True
```

O erro que isto produz é do tipo que não dá exceção: um
`for peça in mob: peça.set_opacity(0.3)` num mobject com pontos próprios aplica
a operação **no pai também** — e como `set_opacity` propaga por família
(§4), o efeito é aplicado duas vezes. Quando você quer só os filhos, escreva
`mob.submobjects`, que é explícito e não muda de comportamento conforme a
classe.

### 1.2 `get_family()` × `family_members_with_points()`

`get_family()` devolve todo mundo, inclusive contêineres vazios;
`family_members_with_points()` filtra quem desenha. [FONTE] `mobject.py:2572`.
A câmera desenha a família achatada do que está na cena — é por isso que um
`VGroup` não é "uma coisa" na hora de pintar: ele some e sobram os filhos.

---

## 2. Nada aparece até você adicionar — e a ordem é a ordem de adição

```python
c = Circle()             # existe em memória, invisível
self.add(c)              # aparece instantaneamente
self.play(Create(c))     # aparece animado (a animação também adiciona)
self.remove(c)
```

[FONTE] `scene.py:491` — *"Mobjects will be displayed, from background to
foreground in the order with which they are added."* O primeiro adicionado fica
por baixo.

**Adicionar de novo traz para a frente.** [FONTE] `Scene.add` faz
`restructure_mobjects(to_remove=...)` e só então `self.mobjects += ...`: um
mobject já presente é removido da lista e recolocado no fim. `self.add(mob)` é o
"bring to front" mais barato que existe. (`bring_to_front`,
`add_foreground_mobject` e a gestão de cena em geral são de
**`manim-cenas-secoes`**; z-index é de **`manim-layout-posicionamento`** — o
mecanismo está no §7 aqui só porque depende da família.)

### 2.1 A armadilha que dissolve o grupo

[FONTE] `scene.py`, docstring de `restructure_mobjects`:

> *"If your scene has a Group(), and you removed a mobject from the Group, this
> dissolves the group and puts the rest of the mobjects directly in
> self.mobjects."*

Ou seja: `self.remove(peça)` — ou qualquer animação com `remover=True`, como
`FadeOut(peça)` — quando `peça` é filha de um `VGroup` que está na cena,
**substitui o grupo pelos irmãos restantes** na lista da cena. O objeto Python
`grupo` não é tocado: ele continua com `peça` entre os `submobjects`.

[NÃO VERIFICADO — derivado do fonte, sem execução] A consequência mais cara é a
volta: como `grupo` não está mais em `self.mobjects`, o próximo
`self.play(grupo.animate.shift(...))` re-adiciona o grupo inteiro pela via de
`add_mobjects_from_animations` — e a peça "removida" reaparece.

A forma segura é remover dos **dois** lados, e nessa ordem:

```python
grupo.remove(peça)      # da árvore
self.remove(peça)       # da cena
```

---

## 3. `Mobject` × `VMobject` — a divisão que decide metade dos erros

`VMobject` é o Mobject **vetorial**: caminhos de Bézier com preenchimento e
contorno. Praticamente todo o catálogo (geometria, texto, LaTeX, eixos, chaves)
é `VMobject`. Fora dele ficam só dois ramos: `ImageMobject` (bitmap) e
`PMobject`/`PGroup`/`DotCloud` (nuvem de pontos).

**Correção.** Uma versão anterior desta linha também punha "os mobjects 3D de
malha" fora do `VMobject`. **Está errado**: na CE 0.21 com renderer cairo, todo
sólido é vetorial. `Surface(VGroup)`, `Sphere(Surface)`, `Cone`/`Cylinder`/
`Torus(Surface)`, `Cube(VGroup)`, `Polyhedron(VGroup)` e os 5 poliedros
regulares — `VGroup` é `VMobject`, logo todos são
(`mobject/three_d/three_dimensions.py:49,61,356,531,636,805,1285`;
`three_d/polyhedra.py:30,163,198,244,309,375`). `Sphere().set_fill(...)` e
`VGroup(esfera, cubo)` funcionam. A única "malha" de verdade é `Mesh`, que mora
em `manim.renderer.shader` e **não é mobject** — só existe no caminho OpenGL
(3D é assunto de `manim-3d-camera`).

Métodos que **existem só no `VMobject`** e que a gente costuma atribuir ao
`Mobject` por engano [FONTE] `api/manim-ce-methods.tsv`, coluna `defined_in`:

| Método | Onde vive |
|---|---|
| `set_fill` `set_stroke` `set_opacity` `set_style` `get_style` `match_style` | `VMobject` |
| `set_cap_style` `set_sheen` `set_sheen_direction` | `VMobject` |
| `point_from_proportion` `proportion_from_point` | `VMobject` (tampão no `Mobject`) |
| `get_subcurve` `insert_n_curves` `get_num_curves` `get_arc_length` | `VMobject` |
| `make_smooth` `make_jagged` `close_path` `is_closed` | `VMobject` |

[FONTE] `mobject.py:2400-2404` — em `Mobject`, `point_from_proportion` e
`proportion_from_point` são **tampões** cujo corpo é
`raise NotImplementedError("Please override in a child class.")`. Chamar num
`ImageMobject` estoura; num `VMobject` funciona. (A lista completa dos cinco
tampões está em `manim-api-discovery` §1.)

E `set_width`/`set_height` **não existem em nenhum dos dois** — ver §5.1.

---

## 4. Estilo: o mecanismo (a decisão de cor é de outra skill)

```python
mob.set_fill(color=BLUE, opacity=0.5, family=True)
mob.set_stroke(color=WHITE, width=3, opacity=1, background=False, family=True)
mob.set_color(BLUE)              # preenchimento E contorno
mob.set_opacity(0.3)             # os dois canais
mob.match_style(outro, family=True)
```

Assinaturas [FONTE]:

```
VMobject.set_fill(color=None, opacity=None, family=True) -> Self
VMobject.set_stroke(color=None, width=None, opacity=None, background=False, family=True) -> Self
VMobject.set_color(color, family=True) -> Self
VMobject.set_opacity(opacity, family=True) -> Self
```

Quatro fatos mecânicos que valem mais que qualquer tabela de cor:

1. **`fill_opacity` nasce em 0.** [FONTE] `VMobject.__init__(fill_opacity=0.0,
   stroke_width=4)`. Toda forma do catálogo é **oca** por padrão, com exceções
   que vêm com preenchimento embutido: `Dot` (`fill_opacity=1.0,
   stroke_width=0`), `AnnularSector`, `Annulus`, `Sector` (`fill_opacity=1,
   stroke_width=0`) e as pontas `*FilledTip`. Por isso `set_fill(BLUE)` sem
   `opacity=` **não mostra nada**: [FONTE] o corpo só escreve
   `self.fill_opacity = opacity` quando `opacity is not None`.
2. **`family=True` é o padrão em tudo.** Pintar um grupo pinta os filhos. É o
   que você quer 90% das vezes e é exatamente o que estraga os outros 10% — um
   `Rectangle(grid_xstep=1).set_fill(BLUE, 1)` preenche também as `Line` da
   grade.
3. **Escalar não engrossa o traço.** [FONTE]
   `VMobject.scale(scale_factor, scale_stroke=False, ...)`. Encolher uma forma
   para 0,3 mantém `stroke_width=4`, e ela lê como "borda gorda demais". Passe
   `scale_stroke=True` ou recalcule o traço.
4. **Junta e ponta de traço são enums, não strings.** [FONTE] `constants.py`:
   `LineJointType` = `AUTO=0 ROUND=1 BEVEL=2 MITER=3`; `CapStyleType` =
   `AUTO=0 ROUND=1 BUTT=2 SQUARE=3`. Uso: `VMobject(joint_type=LineJointType.ROUND)`
   ou `mob.set_cap_style(CapStyleType.ROUND)`. Em traço grosso a junta MITER
   produz bicos que estouram a caixa delimitadora sem aparecer em `mob.width`
   (§5.3).

**Que cor usar, contraste, paleta, tema, `set_default`, e o mobject que some em
fundo branco: `manim-color-theming` é dona.** Não duplique a matéria dela aqui.

---

## 5. Tamanho e forma

### 5.1 `set_width`/`set_height` não existem — e o motivo importa mais que o erro

Versões anteriores desta skill mandavam usar `mob.set_width(4)`. **Está errado.**
[FONTE] `awk -F'\t' '$2=="set_width"' api/manim-ce-methods.tsv` devolve 45
linhas, **todas** com `defined_in = OpenGLMobject`. No caminho cairo o nome não
é um método: é sintetizado por `Mobject.__getattr__` (`mobject.py:754-774`):

```python
if attr.startswith("set_"):
    to_set = attr[4:]
    def setter(self, value):
        warnings.warn("... Please prefer setting the attribute normally or with Mobject.set().",
                      DeprecationWarning, stacklevel=2)
        setattr(self, to_set, value)
        return self
    return types.MethodType(setter, self)
raise AttributeError(...)
```

Para `set_width` o resultado por acaso está certo: `setattr(self, "width", 4)`
cai na property `width`, cujo setter é `self.scale_to_fit_width(value)`
([FONTE] `mobject.py:809-810`). **O perigo não é `set_width` — é o mesmo
fallback engolir qualquer `set_<erro de digitação>`:** ele cria um atributo
morto, devolve `self` (a cadeia continua funcionando) e nada muda na tela.
`mob.set_witdh(4)` não levanta nada.

E o aviso é praticamente mudo. [FONTE] A CLI da CE instala
`warnings.filterwarnings("default", category=DeprecationWarning, module=<seu módulo>)`
em `manim/utils/module_ops.py:53`, então `bin/manim` mostra o `DeprecationWarning`.
O `mx render` carrega a cena por outro caminho (`manimx/render.py:120-140`) e
**não instala esse filtro** — sob o filtro padrão do Python, `DeprecationWarning`
fora de `__main__` é silencioso. [NÃO VERIFICADO em execução; o mecanismo é
[FONTE] nos dois arquivos.]

**Use os métodos reais** — são os únicos que levantam `AttributeError` quando
você digita errado, porque `__getattr__` só socorre os prefixos `get_` e `set_`:

```python
mob.scale_to_fit_width(4)      # mantém proporção   ← typo aqui LEVANTA
mob.stretch_to_fit_width(4)    # deforma            ← typo aqui LEVANTA
mob.match_width(outro)         #                    ← typo aqui LEVANTA
mob.width = 4                  # a property; equivale ao scale_to_fit
mob.set(width=4)               # `set` é só um setattr em laço [FONTE]
```

As duas últimas formas funcionam, mas **não são à prova de digitação**:
`mob.widht = 4` e `mob.set(widht=4)` criam um atributo morto sem reclamar —
[FONTE] `Mobject.set` é literalmente
`for attr, value in kwargs.items(): setattr(self, attr, value)`.

### 5.2 O quadro completo de redimensionar

| Você quer | Método [FONTE] |
|---|---|
| multiplicar por um fator | `scale(factor, *, about_point=None, about_edge=None)` |
| idem, engrossando o traço junto | `VMobject.scale(factor, scale_stroke=True)` |
| esticar em UM eixo | `stretch(factor, dim, *, about_point=None, about_edge=None)` — `dim` 0=x 1=y 2=z |
| chegar a uma largura, mantendo proporção | `scale_to_fit_width(w)` · idem `_height` `_depth` |
| chegar a uma largura, deformando | `stretch_to_fit_width(w)` · idem `_height` `_depth` |
| copiar a medida de outro | `match_width(m)` `match_height(m)` `match_depth(m)` `match_dim_size(m, dim)` |
| caber DENTRO de outro | `replace(m, dim_to_match=0, stretch=False)` |
| envolver outro com folga | `surround(m, dim_to_match=0, stretch=False, buff=0.25)` |
| espelhar | `flip(axis=UP, *, about_point=None, about_edge=None)` |
| girar | `rotate(angle, axis=OUT, *, about_point=None, about_edge=None)` |
| aplicar uma matriz / uma função | `apply_matrix(M, ...)` · `apply_function(f, ...)` · `apply_complex_function(f, ...)` |
| esticar entre dois pontos | `put_start_and_end_on(start, end)` |

Duas pegadinhas de assinatura, ambas [FONTE]:

- **`Circle.surround` tem outro parâmetro.** `Mobject.surround(..., buff=0.25)`,
  mas `Circle.surround(mobject, dim_to_match=0, stretch=False, buffer_factor=1.2)`.
  `circulo.surround(x, buff=0.3)` dá `TypeError: unexpected keyword argument`.
- **`put_start_and_end_on` num objeto fechado só translada.** [FONTE]
  `mobject.py` — se `current_start == current_end`, ele emite
  `warnings.warn("...has been called on a closed loop or zero-length mobject...")`
  e apenas desloca. Num `Circle` isso significa que a chamada não faz o que você
  espera, e o aviso passa batido no log.

### 5.3 A caixa delimitadora: âncoras, nada além disso

Todo `next_to`, `align_to`, `surround`, `SurroundingRectangle`, `arrange`,
`width` e `height` sai da mesma conta. [FONTE]
`VMobject.get_points_defining_boundary` (`vectorized_mobject.py:1793`):

```python
return np.array(tuple(it.chain(*(sm.get_anchors() for sm in self.get_family()))))
```

Leia com cuidado — três consequências, todas silenciosas:

1. **Traço não conta.** A caixa usa pontos do caminho. Um `stroke_width=20`
   transborda `mob.width` por metade da espessura em cada lado. Um retângulo de
   destaque colado (`buff=0`) corta o traço do que ele destaca.
2. **Alça de Bézier não conta.** `get_anchors()` devolve só as âncoras, não os
   handles. Uma curva que estufa entre duas âncoras é desenhada **fora** da
   caixa que o Manim declara. Em `Arc` o erro é pequeno (`num_components=9`);
   num `CubicBezier` com alças longas, é grande.
3. **Objeto invisível conta.** Opacidade 0 e `stroke_width=0` não removem
   âncoras. Uma lingueta transparente, um espaçador, um `VectorizedPoint` de
   ancoragem — todos entram na caixa e deslocam o grupo.

O item 3 tem preço medido. [DECK] Um detalhe transparente dentro de um `VGroup`
fez `VGroup.move_to()` deslocar o grupo inteiro em **4 px** — silenciosos,
descobertos só pela métrica de emenda entre partes de vídeo. **A regra que saiu
disso: posicione pelo CORPO visível, não pelo grupo.**

```python
grupo = VGroup(corpo, lingueta_invisivel)
grupo.shift(alvo - corpo.get_center())      # certo: mede o corpo
# grupo.move_to(alvo)                       # errado: mede a lingueta junto
```

Réguas prontas para conferir enquadramento (`FullScreenRectangle`,
`ScreenRectangle`, `mob.is_off_screen()`, `shift_onto_screen()`) são de
**`manim-layout-posicionamento`**.

---

## 6. Grupos

```python
g = VGroup(a, b, c)        # SÓ VMobject
g = Group(a, img, c)       # qualquer Mobject, inclusive ImageMobject
d = VDict({"topo": a, "base": b})   # filhos com NOME em vez de índice
```

Assinaturas [FONTE]:

```
VGroup(*vmobjects: VMobject | Iterable[VMobject], **kwargs)
Group(*mobjects: Any, **kwargs)
VDict(mapping_or_iterable={}, show_keys=False, **kwargs)
```

### 6.1 Por que `VGroup` recusa — e a mensagem que ele dá

[FONTE] `vectorized_mobject.py:2340-2372`. `VGroup.add` valida item a item e
levanta `TypeError` com um texto que já diz a saída:

> `Only values of type VMobject can be added as submobjects of VGroup, but the
> value <ImageMobject ...> (at index 0 of parameter 0) is of type ImageMobject.
> You can try adding this value into a Group instead.`

Detalhe útil no meio dessa validação: **`VGroup` aceita um iterável** —
`VGroup([a, b, c])` e `VGroup(*lista)` fazem a mesma coisa. Mas um `Mobject`
que não seja `VMobject` cai na cláusula que sugere o `Group`, porque
[FONTE] `Mobject` define `__iter__` e portanto passa em `isinstance(x, Iterable)`.

### 6.2 Operadores e fatias

[FONTE] `vectorized_mobject.py`, logo abaixo de `add`:

```python
g2 = g + novo      # NOVO VGroup; g não muda
g += novo          # equivale a g.add(novo)  → muta g
g3 = g - a         # NOVO VGroup sem `a`
g -= a             # equivale a g.remove(a)  → muta g
g[0] = outro       # __setitem__ existe: troca um filho no lugar
g[1:3]             # devolve um VGroup (get_group_class)
```

`g + novo` **não** modifica `g` — é a confusão mais comum com esses operadores.

### 6.3 `arrange` e `arrange_in_grid`

```
Mobject.arrange(direction=RIGHT, buff=0.25, center=True, **kwargs) -> Self
Mobject.arrange_in_grid(rows=None, cols=None, buff=0.25, cell_alignment=ORIGIN,
                        row_alignments=None, col_alignments=None,
                        row_heights=None, col_widths=None,
                        flow_order="rd", **kwargs) -> Self
```

[FONTE] O corpo de `arrange` é literalmente um `next_to` encadeado seguido de
`self.center()`:

```python
for m1, m2 in zip(self.submobjects[:-1], self.submobjects[1:], strict=True):
    m2.next_to(m1, direction, buff, **kwargs)
if center:
    self.center()
```

Daí as duas armadilhas: **`arrange` joga fora a posição que você já tinha**
(`center()` leva o grupo para a ORIGEM — use `center=False` para preservar a
posição do primeiro filho), e **os `**kwargs` vão para o `next_to`**, então
`arrange(DOWN, aligned_edge=LEFT)` é válido e é o idioma para alinhar uma
coluna pela esquerda.

`flow_order` aceita exatamente `"rd" "dr" "ld" "dl" "ru" "ur" "lu" "ul"`
([FONTE] `mobject.py:2811-2816`, com `ValueError` nomeando os oito); `"rd"` é
preencher para a direita e depois para baixo.

### 6.4 Quando NÃO agrupar

Um `VGroup` é a resposta para "estes elementos se movem juntos". Não é a
resposta para "estes elementos são um assunto". Três contraindicações concretas:

- **A peça de que outro ato precisa animar sozinha.** Se a parte 6 do vídeo vai
  trocar só o selo, o selo tem que ter nome. [DECK] O padrão em produção é a
  função de desenho devolver o grupo **e** as referências internas:
  `def _pasta(...) -> tuple[VGroup, VGroup, VGroup, VGroup]` devolvendo
  `(grupo, moldura, linhas, selo)`. O motivo está na própria docstring de lá:
  *"as três referências extras não são luxo: a parte 1 monta a pasta em tempos e
  o ato 2 troca linhas e selo sem tocar no resto"*. A alternativa —
  `grupo[0][2]` no meio de um `self.play` — quebra em silêncio no dia em que
  alguém acrescentar um submobject.
- **O grupo com um membro invisível.** Ver §5.3.
- **O grupo que só existe para pintar.** `set_color` aceita `family=True`; para
  pintar N objetos não é preciso agrupá-los, e agrupar cria uma caixa
  delimitadora nova que vai atrapalhar o posicionamento depois.

`VDict`, `PGroup`, `CurvesAsSubmobjects` e o resto do ferramental de contêiner
para quem escreve classe própria são de **`manim-mobjects-customizados`**.

---

## 7. Cópia, estado e identidade

```python
b = a.copy().shift(RIGHT * 2)     # independente
b = a                             # MESMO objeto; mexer em b mexe em a
```

[FONTE] `mobject.py:895-908` — `copy()` é `copy.deepcopy(self)`, e a docstring
avisa: *"The clone is initially not visible in the Scene, even if the original
was."* A cópia é profunda: os submobjects também são novos.

| Operação | Assinatura [FONTE] | Serve para |
|---|---|---|
| `mob.copy()` | `() -> Self` | duplicar |
| `mob.become(outro, match_height=False, match_width=False, match_depth=False, match_center=False, stretch=False)` | | trocar o conteúdo **mantendo a identidade** — a variável continua sendo a mesma, updaters e referências sobrevivem |
| `mob.save_state()` / `mob.restore()` | `() -> Self` | guardar e voltar (a animação `Restore` usa isso) |
| `mob.generate_target(use_deepcopy=False)` | | preparar `mob.target` para `MoveToTarget` |
| `mob.match_points(outro, copy_submobjects=True)` | | copiar só a geometria, preservando o estilo |

`become` é a ferramenta certa quando algo **na cena** precisa virar outra coisa
sem sair e voltar — inclusive dentro de um updater, que é o uso de
`always_redraw` ([FONTE] o updater dele é `lambda _: mob.become(func())`; a
matéria é de **`manim-updaters-valuetracker`**).

`Transform` × `ReplacementTransform` × `TransformFromCopy` é matéria de
**`manim-animations`** — ela é a dona. O que interessa aqui é só a parte de
identidade: depois de `Transform(a, b)` quem está na cena é `a`; `b` nunca
entrou.

---

## 8. O catálogo de `mobject/geometry` — as 57 classes

O índice tem **384 linhas** com `category == mobject/geometry`, mas
**327 delas são constantes re-exportadas**: as classes são **57**. (É a
armadilha de contagem que `manim-api-discovery` documenta; filtre sempre por
`$1=="class"`.)

```bash
awk -F'\t' '$1=="class" && $3=="mobject/geometry" {print $2"\t"$4}' \
  api/manim-ce-index.tsv | sort
```

A herança, que explica muito comportamento herdado [FONTE]:

```
VMobject
├── TipableVMobject
│   ├── Arc
│   │   ├── ArcBetweenPoints ── CurvedArrow ── CurvedDoubleArrow
│   │   │                   └── TangentialArc
│   │   ├── Circle ── Dot ── AnnotationDot · LabeledDot
│   │   │       ├── Ellipse
│   │   │       └── Annulus
│   │   └── AnnularSector ── Sector
│   └── Line ── DashedLine · TangentLine · Underline · LabeledLine
│           └── Arrow ── Vector · DoubleArrow
├── Polygram
│   ├── Polygon ── Star
│   │          └── Rectangle ── Square
│   │                       └── RoundedRectangle ── SurroundingRectangle ── BackgroundRectangle
│   ├── RegularPolygram ── RegularPolygon ── Triangle
│   ├── ConvexHull
│   └── LabeledPolygram
├── CubicBezier · ArcPolygon · ArcPolygonFromArcs · Elbow · Angle ── RightAngle
├── Cutout · Union · Intersection · Difference · Exclusion
└── ArrowTip ── ArrowTriangleTip ── ArrowTriangleFilledTip
            ├── ArrowCircleTip ── ArrowCircleFilledTip
            ├── ArrowSquareTip ── ArrowSquareFilledTip
            └── StealthTip
VGroup
├── Cross
└── Label
```

Duas heranças múltiplas, que o desenho acima não comporta [FONTE]:
`LabeledArrow(LabeledLine, Arrow)` e as pontas geométricas
(`ArrowTriangleTip(ArrowTip, Triangle)`, `ArrowCircleTip(ArrowTip, Circle)`,
`ArrowSquareTip(ArrowTip, Square)`).

### 8.1 Arcos e círculos

```
Arc(radius=1.0, start_angle=0, angle=PI/2, num_components=9, arc_center=ORIGIN)
ArcBetweenPoints(start, end, angle=PI/2, radius=None)
Circle(radius=None, color=RED)                    # radius=None vira 1.0
Dot(point=ORIGIN, radius=0.08, stroke_width=0, fill_opacity=1.0, color=WHITE)
AnnotationDot(radius=0.104, stroke_width=5, stroke_color=WHITE, fill_color=BLUE)
LabeledDot(label, radius=None, buff=0.1)
Ellipse(width=2, height=1)
AnnularSector(inner_radius=1, outer_radius=2, angle=PI/2, start_angle=0, fill_opacity=1, stroke_width=0)
Sector(radius=1, **kwargs)                        # AnnularSector com inner_radius=0
Annulus(inner_radius=1, outer_radius=2, fill_opacity=1, stroke_width=0)
CubicBezier(start_anchor, start_handle, end_handle, end_anchor)
TangentialArc(line1, line2, radius, corner=(1, 1))
```

Métodos próprios que valem lembrar [FONTE]:
`Circle.point_at_angle(angle)`, `Circle.from_three_points(p1, p2, p3)`,
`Arc.get_arc_center()`, `Arc.move_arc_center_to(point)`, `Arc.stop_angle()`.

Exemplo mínimo — um medidor circular, com todas as assinaturas conferidas
([NÃO VERIFICADO por render]:

```python
fundo = Annulus(inner_radius=0.8, outer_radius=1.0, color=GREY_D)
fatia = AnnularSector(inner_radius=0.8, outer_radius=1.0,
                      start_angle=PI / 2, angle=-0.72 * TAU, color=BLUE)
self.add(fundo, fatia)
```

**Quando NÃO usar.** `Circle` para marcar um ponto é desperdício — `Dot` já vem
preenchido e com `stroke_width=0`. `Arc` para ligar duas coisas é quase sempre
pior que `Line(..., path_arc=0.4)` ou `CurvedArrow`, porque estes conhecem os
extremos.

### 8.2 Polígonos

```
Polygram(*vertex_groups: Point3DLike_Array, color=BLUE)   # vários laços fechados
Polygon(*vertices: Point3DLike)                           # UM laço
RegularPolygram(num_vertices, *, density=2, radius=1, start_angle=None)
RegularPolygon(n=6, **kwargs)
Triangle(**kwargs)                                        # = RegularPolygon(n=3)
Rectangle(color=WHITE, height=2.0, width=4.0, grid_xstep=None, grid_ystep=None,
          mark_paths_closed=True, close_new_points=True)
Square(side_length=2.0)
RoundedRectangle(corner_radius=0.5, **kwargs)
Star(n=5, *, outer_radius=1, inner_radius=None, density=2, start_angle=PI/2)
ConvexHull(*points, tolerance=1e-05)
Cutout(main_shape: VMobject, *mobjects: VMobject)   # NÃO é Polygram — ver abaixo
```

Métodos próprios do `Polygram` — herdados por todos acima **exceto `Cutout`**
[FONTE] `api/manim-ce-methods.tsv`:

```
get_vertices() -> Point3D_Array
get_vertex_groups() -> list[Point3D_Array]
round_corners(radius=0.5, evenly_distribute_anchors=False, components_per_rounded_corner=2) -> Self
```

**A exceção que quebra calado:** `Cutout` está na lista de "polígonos" por
parentesco visual, não por herança. `polygram.py:755` diz
`class Cutout(VMobject, metaclass=ConvertToOpenGL)` — irmão de `Polygram`, não
filho. `awk -F'\t' '$1=="Cutout" && $2=="round_corners"' api/manim-ce-methods.tsv`
devolve vazio. Chamar `.get_vertices()` ou `.round_corners()` num `Cutout` é
`AttributeError`. `ConvexHull(Polygram)` (`polygram.py:802`) herda normalmente.

`round_corners` é a peça mais subestimada do módulo:

- [FONTE] `radius == 0` faz `return self` — é por isso que
  `SurroundingRectangle(corner_radius=0.0)` não paga nada;
- **raio negativo produz canto CÔNCAVO** (`angle *= np.sign(current_radius)`);
- o corte é **limitado a metade da aresta mais curta**
  (`max_cut_off = min(|v1|, |v2|) / 2`), então um raio absurdo não explode:
  ele satura. Corrigido por causa do issue #3052 do upstream;
- `radius` aceita **lista**, repetida ciclicamente por vértice —
  `poligono.round_corners([0.3, 0, 0, 0.3])`.

Duas armadilhas verificadas:

- **`Rectangle(grid_xstep=…)` cria submobjects.** [FONTE] O retângulo passa a ter
  pontos próprios **e** um `VGroup` de `Line` chamado `grid_lines`. Isso muda
  `len(rect)` para 2, faz `rect[0] is rect`, e faz `rect.set_stroke(...)`
  repintar a grade junto (§4, `family=True`).
- **`Cutout` MUTA os argumentos e só olha para os pontos PRÓPRIOS.** [FONTE]
  `polygram.py:790-799`:

  ```python
  self.append_points(main_shape.points)
  sub_direction = "CCW" if main_shape.get_direction() == "CW" else "CW"
  for mobject in mobjects:
      self.append_points(mobject.force_direction(sub_direction).points)
  ```

  Ou seja: (a) `force_direction` inverte o sentido do caminho **do mobject que
  você passou**, in place; (b) se `main_shape` for um `VGroup`, um `Text` ou
  qualquer coisa cuja geometria mora em submobjects, `main_shape.points` está
  vazio e o `Cutout` sai **vazio, sem erro**; (c) o resultado depende da regra de
  preenchimento, e a própria docstring avisa que a operação se comporta como
  diferença simétrica — pedaço do furo que caia fora da forma principal
  **aparece**. Para recorte de verdade, use `Difference`.

### 8.3 Linhas, setas e pontas

```
Line(start=LEFT, end=RIGHT, buff=0, path_arc=0)
DashedLine(*args, dash_length=0.05, dashed_ratio=0.5)
TangentLine(vmob, alpha, length=1, d_alpha=1e-06)
Elbow(width=0.2, angle=0)
Arrow(*args, stroke_width=6, buff=0.25,
      max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=5)
DoubleArrow(*args, **kwargs)
Vector(direction=RIGHT, buff=0)
CurvedArrow(start_point, end_point)  ·  CurvedDoubleArrow(start_point, end_point)
Angle(line1, line2, radius=None, quadrant=(1,1), other_angle=False,
      dot=False, dot_radius=None, dot_distance=0.55, dot_color=WHITE, elbow=False)
RightAngle(line1, line2, length=None)
```

`Line` e `Arrow` aceitam **Mobject** como extremo:
`Line(start: Point3DLike | Mobject, end: Point3DLike | Mobject)` — a linha nasce
ligando os centros e o `buff` recua de cada lado.

Métodos próprios [FONTE]:

```
Line: get_vector() get_unit_vector() get_angle() get_slope() get_projection(point)
      set_angle(angle, about_point=None) set_length(length) set_path_arc(v)
      set_points_by_ends(start, end, buff=0, path_arc=0)
TipableVMobject (Arc e Line herdam): add_tip(tip=None, tip_shape=None, tip_length=None,
      tip_width=None, at_start=False) · get_tip() · get_tips() · pop_tips() ·
      has_tip() · has_start_tip() · get_length() · get_start() · get_end()
Arrow: get_normal_vector() · scale(factor, scale_tips=False)
Angle: get_value(degrees=False) · get_lines() · Angle.from_three_points(A, B, C)
Vector: coordinate_label(integer_labels=True, n_dim=2, color=None) -> Matrix
```

**As três armadilhas da `Arrow`, todas [FONTE] `geometry/line.py`:**

1. **`buff=0.25` por padrão.** `Arrow(A, B)` não encosta em A nem em B: encolhe
   0,25 de cada lado. Uma seta curta some. `Line` tem `buff=0`.
2. **O traço afina sozinho.** `_set_stroke_width_from_length` faz
   `width = min(initial_stroke_width, max_stroke_width_to_length_ratio * length)`
   — com o padrão 5, qualquer seta menor que 1,2 unidade fica mais fina que os
   6 que você pediu. E `initial_stroke_width` é capturado **na construção**;
   um `set_stroke(width=…)` posterior é reescrito no próximo `scale`.
3. **A ponta é limitada por `max_tip_length_to_length_ratio=0.25`.** Numa seta de
   0,4 de comprimento a ponta cabe em 0,1 — não nos 0,35 de
   `DEFAULT_ARROW_TIP_LENGTH`. Setas curtas parecem "sem cabeça", e a correção
   é subir esse ratio, não engrossar o traço.

`Arrow.scale(factor)` preserva ponta e traço de propósito ([FONTE] docstring:
*"Scale an arrow, but keep stroke width and arrow tip size fixed"*). Se você
QUER escalar a ponta junto, `scale_tips=True`; se quer o comportamento genérico,
chame `VMobject.scale(arrow, factor)` explicitamente.

As oito pontas prontas, para `Arrow(..., tip_shape=…)` ou `add_tip(tip_shape=…)`
[FONTE]:

| Classe | Preenchida | Padrões próprios |
|---|---|---|
| `ArrowTriangleTip` | não | `stroke_width=3, length=0.35, width=0.35, start_angle=PI` |
| `ArrowTriangleFilledTip` | **sim** | `fill_opacity=1, stroke_width=0` — é o default da `Arrow` |
| `ArrowCircleTip` / `ArrowCircleFilledTip` | não / sim | `length=0.35, start_angle=PI` |
| `ArrowSquareTip` / `ArrowSquareFilledTip` | não / sim | idem |
| `StealthTip` | **sim** | `fill_opacity=1, stroke_width=3, length=0.175` |
| `ArrowTip` | — | base abstrata |

**`DashedLine` não tem pontos próprios — e isso quebra tudo que anda sobre
curva.** [FONTE] `line.py:316-332`: o construtor monta os tracinhos e faz
`self.clear_points(); self.add(*dashes)`. Consequências:

- `dashed.point_from_proportion(0.5)` levanta exceção ([FONTE]
  `VMobject.point_from_proportion` documenta *"Exception: if the VMobject has no
  points"*);
- `MoveAlongPath(mob, dashed)` não tem por onde andar;
- a classe reimplementa `get_start`/`get_end`/`get_first_handle`/`get_last_handle`
  só por causa disso.

[DECK] A solução em produção é um trilho invisível com os mesmos extremos —
`aulas/001-multi-work/manim/aula_001_worktrees.py:328-334`:

```python
def _trilho(inicio):
    """Um `DashedLine` é um grupo de tracinhos — os pontos moram nos submobjects
    e `MoveAlongPath` precisa de uma curva com pontos próprios. Daí este trilho
    invisível, com o mesmo começo e o mesmo fim do fio."""
    return Line(inicio, ANCORA)
```

### 8.4 `DashedVMobject` descarta o `color=` que você passou

Vale para qualquer curva, e é a causa nº 1 de "o tracejado sumiu no fundo
branco". [FONTE] `vectorized_mobject.py:2931-3050`. O construtor é
`DashedVMobject(vmobject, num_dashes=15, dashed_ratio=0.5, dash_offset=0,
color=WHITE, equal_lengths=True)`, mas a **última coisa** que ele faz antes de
recolocar as pontas é:

```python
self.match_style(base_vmobject, family=False)
```

E os tracinhos em si são `vmobject.get_subcurve(...)` — cópias da curva
original, já com o estilo dela. O `color=` do construtor não é "o que resta": é
o que é **descartado**. Em fundo branco, uma curva sem cor explícita vira
tracinhos brancos, invisíveis, sem erro nenhum.

**A correção é estilizar o original ANTES de embrulhar** — [DECK]
`aulas/002-deepseek-harness/manim/aula_002_monolito.py:563-570`:

```python
caixa = RoundedRectangle(corner_radius=0.18, width=CORDIS_W, height=CORDIS_H)
caixa.set_stroke(TINTA_3, width=2.0).set_fill(opacity=0.0)     # o estilo entra AQUI
moldura = DashedVMobject(caixa, num_dashes=96, dashed_ratio=0.55, color=TINTA_3)
```

Dois brindes do mesmo fonte, ambos [FONTE]: ele trabalha numa **cópia**
(*"Work on a copy to avoid mutating the caller's mobject"*), e ele **retira e
recoloca as pontas** de um `TipableVMobject` — sem isso, tracejar uma `Arrow`
produziria uma cabeça de flecha por tracinho.

### 8.5 Anotação: destaque, sublinhado, cruz, chave

```
SurroundingRectangle(*mobjects, color=PURE_YELLOW, buff=0.1, corner_radius=0.0)
BackgroundRectangle(*mobjects, color=None, stroke_width=0, stroke_opacity=0,
                    fill_opacity=0.75, buff=0)
Underline(mobject, buff=0.1)
Cross(mobject=None, stroke_color=RED, stroke_width=6.0, scale_factor=1.0)
Brace(mobject, direction=DOWN, buff=0.2, sharpness=2, stroke_width=0, fill_opacity=1.0)
BraceLabel(obj, text, brace_direction=DOWN, label_constructor=MathTex, font_size=48, buff=0.2)
BraceText(obj, text, label_constructor=Text)
BraceBetweenPoints(point_1, point_2, direction=ORIGIN)
ArcBrace(arc=None, direction=RIGHT)
```

`Brace` e família moram em `mobject/svg` ([FONTE] módulo
`manim.mobject.svg.brace`) — **não** em `mobject/geometry`, ao contrário do que
esta skill afirmava. Elas continuam sendo matéria daqui porque são anotação de
forma, não asset externo.

Fatos [FONTE] que economizam um render cada:

- **`SurroundingRectangle` é um retrato, não um vínculo.** Ele é um
  `RoundedRectangle` cujas medidas saem de `Group(*mobjects).width/height` no
  momento da construção. Se o alvo se mexer depois, o retângulo fica. Para
  seguir, `always_redraw` (**`manim-updaters-valuetracker`**).
- `buff` aceita **tupla** `(buff_x, buff_y)` — folga diferente em cada eixo.
- **`BackgroundRectangle` lê `config.background_color`**, não
  `self.camera.background_color`, quando `color=None`. Num projeto que só ajusta
  a câmera no `setup()`, o retângulo de fundo sai da cor errada. [DECK] É
  exatamente por isso que a cena-base do deck fixa o fundo **nos dois lugares**.
- **`BackgroundRectangle` recusa ser reestilizado.** [FONTE]
  `set_style(self, fill_opacity, **kwargs)` ignora tudo menos `fill_opacity`,
  e `pointwise_become_partial` reinterpreta o progresso de `Create` como
  opacidade.
- **`Cross` ignora `color=`.** É um `VGroup` de duas `Line` e o construtor
  termina em `set_stroke(color=stroke_color, width=stroke_width)`, que propaga
  por família. Use `stroke_color=`.
- **`Brace` roda o seu mobject e desroda.** [FONTE] `brace.py`:
  `mobject.rotate(-angle, about_point=ORIGIN)` … `for mob in mobject, self:
  mob.rotate(angle, about_point=ORIGIN)`. O argumento é **mutado** e volta com
  ida-e-volta de ponto flutuante. Não é destrutivo na prática, mas não conte com
  coordenadas idênticas depois.
- **A chave não precisa de LaTeX; o rótulo dela, sim.** O `Brace` é um caminho
  SVG embutido no fonte. Mas `Brace.get_text(*text) -> Tex` e
  `Brace.get_tex(*tex) -> MathTex` — **os dois** passam por LaTeX. Para rótulo
  sem LaTeX, `BraceText` (cujo `label_constructor` já é `Text`) ou
  `BraceLabel(..., label_constructor=Text)`. Detalhe cruel: o método chamado
  `get_text` devolve `Tex`, não `Text`.
- `Brace.put_at_tip(mob, use_next_to=True)` e `Brace.get_tip() -> Point3D`
  posicionam qualquer mobject na ponta da chave.

A família `Labeled*` ([FONTE] `manim.mobject.geometry.labeled`) resolve
"rótulo dentro de uma caixinha sobre a linha":

```
Label(label, label_config=None, box_config=None, frame_config=None)
LabeledLine(label, label_position=0.5, label_config=None, box_config=None, frame_config=None, *args, **kwargs)
LabeledArrow(*args, **kwargs)                     # LabeledLine + Arrow
LabeledPolygram(*vertex_groups, label, precision=0.01, ...)
```

`LabeledPolygram` põe o rótulo no **polo de inacessibilidade** do polígono (o
ponto interior mais distante da borda), calculado por `polylabel` — o lugar
certo para rotular uma região côncava.

`Flash`, `Indicate`, `Circumscribe`, `Wiggle`, `FocusOn` e o resto de **ênfase
animada** não têm skill dona neste repositório hoje. É um buraco declarado
(§11); enquanto isso, `manim-animations` tem o catálogo cru.

### 8.6 Booleanos e casco convexo

```
Union(*vmobjects)            # ≥ 2, senão ValueError
Intersection(*vmobjects)
Difference(subject, clip)
Exclusion(subject, clip)     # XOR
ConvexHull(*points, tolerance=1e-05)
```

[FONTE] `boolean_ops.py` usa `skia-pathops` (`from pathops import ...`), que
**está instalado nesta máquina** (`skia_pathops-0.9.2`). Quatro coisas que o
fonte deixa claro:

- o resultado é um **VMobject NOVO**; os operandos continuam intactos e, se
  estavam na cena, continuam desenhados — quase sempre você quer
  `self.remove(a, b)` ou `ReplacementTransform`;
- a conta é feita **na construção**, uma vez. Não é uma relação viva: mover `a`
  depois não atualiza a união;
- é **2D**: os pontos são achatados em z=0 na ida e voltam com `z_dim=0.0`;
- `Union` com um argumento só levanta
  `ValueError("At least 2 mobjects needed for Union.")`.

Exemplo mínimo, assinaturas conferidas ([NÃO VERIFICADO por render]):

```python
placa = RoundedRectangle(corner_radius=0.2, width=4, height=2)
furo = Circle(radius=0.4).move_to(placa.get_corner(UR) + DL * 0.6)
janela = Difference(placa, furo, color=BLUE, fill_opacity=1)
self.add(janela)          # e NÃO adicione placa/furo
```

A matemática por trás (`utils/bezier`, `utils/space_ops`, `QuickHull`,
`Polygram` como base para classe própria) é de
**`manim-mobjects-customizados`**.

---

## 9. Descobrir o que existe — sem chutar

O índice custa **menos de 10 ms** por consulta e bate exatamente com o pacote
instalado. Não existe desculpa de custo para inventar um nome.

```bash
# todas as classes de uma categoria (SEMPRE filtre por $1=="class")
awk -F'\t' '$1=="class" && $3=="mobject/geometry" {print $2"\t"$4}' \
  api/manim-ce-index.tsv | sort

# a assinatura exata de uma classe
grep -P '^class\tRoundedRectangle\t' api/manim-ce-index.tsv | cut -f4

# os métodos PRÓPRIOS de uma classe (coluna 5 = inherited)
awk -F'\t' '$1=="Polygram" && $5=="0" {print $2$6}' api/manim-ce-methods.tsv

# onde um método foi DEFINIDO (a pergunta que derrubou set_width)
awk -F'\t' '$2=="set_width" {print $4}' api/manim-ce-methods.tsv | sort -u

# o que é encadeável numa classe (devolve Self)
awk -F'\t' '$1=="Square" && $6 ~ /Self/ {print $2$6}' api/manim-ce-methods.tsv

bin/mx show Arrow          # assinatura + todos os métodos, ~0,19 s
bin/mx find "brace"        # busca por assunto
```

**Achar o índice de um submobject sem adivinhar:**

```python
self.add(index_labels(eq[0]))     # DESENHA os índices por cima
```

[FONTE] `index_labels(mobject, label_height=0.15, background_stroke_width=5,
background_stroke_color=BLACK, **kwargs) -> VGroup`, em `manim.utils.debug`.
Renderize um frame com ela, **olhe a imagem**, e só então escreva os índices no
código. O ciclo completo de conferência visual é de
**`manim-verificacao-visual`**; o comando cru, de `manim-render-api`.

A metodologia de descoberta em profundidade (varredura de kwargs pelo MRO,
conferidor estático de cena, CE × GL, regeneração do índice) é de
**`manim-api-discovery`** — ela é a dona.

---

## 10. Armadilhas, em uma lista

Cada linha custou pelo menos um render perdido.

| Armadilha | Sintoma | Correção |
|---|---|---|
| **Ângulo em graus** | `rotate(90)` gira ~14 voltas | `rotate(90 * DEGREES)` |
| **`set_fill` sem `opacity`** | a forma continua oca | `set_fill(BLUE, opacity=1)` |
| **`set_width` / `set_<typo>`** | nada muda, sem erro | `scale_to_fit_width(4)` (§5.1) |
| **`VGroup` com `ImageMobject`** | `TypeError` na construção | `Group` (§6.1) |
| **`arrange` depois de posicionar** | o grupo pula para a origem | `arrange(..., center=False)` |
| **Coordenada 2D** | erro de broadcast do numpy | `np.array([x, y, 0])` — sempre 3D |
| **Objeto fora do quadro** | some sem aviso | `mob.is_off_screen()`; x ∈ [−7,11; 7,11], y ∈ [−4; 4] |
| **Membro invisível no grupo** | grupo desloca ~4 px [DECK] | posicione pelo corpo visível (§5.3) |
| **Traço grosso vazando** | o destaque corta o alvo | a caixa é só de âncoras (§5.3); aumente `buff` |
| **`Arrow` curta e magra** | seta sem cabeça, traço fino | `buff=0`, suba os dois `max_*_ratio` (§8.3) |
| **`DashedVMobject(color=…)`** | tracinhos invisíveis | estilize o original antes (§8.4) |
| **`DashedLine` em `MoveAlongPath`** | exceção "no points" | trilho `Line` invisível (§8.3) |
| **`Cross(color=…)`** | a cor é ignorada | `stroke_color=` (§8.5) |
| **`Circle.surround(buff=…)`** | `TypeError` | `buffer_factor=` (§5.2) |
| **`Cutout` de um `VGroup`/`Text`** | resultado vazio, sem erro | `Cutout` usa só `.points` do nó (§8.2) |
| **`self.remove(peça)` de um grupo** | o grupo inteiro se desfaz / reaparece | remova dos dois lados (§2.1) |
| **`for x in forma`** | itera o próprio mobject | use `mob.submobjects` (§1.1) |
| **`Brace.get_text`** | erro de LaTeX num projeto sem LaTeX | `BraceLabel(..., label_constructor=Text)` (§8.5) |
| **Booleano vivo** | a união não acompanha o movimento | é calculada uma vez (§8.6) |

**A armadilha estrutural, que vale por todas:** nenhuma delas levanta exceção
no terminal. Renderizar e não olhar a imagem é não ter terminado. Um agente que
confia no exit code entrega texto branco no branco, elemento cortado pela borda
e sobreposição — três defeitos que [DECK] só apareceram ao OLHAR o PNG, nenhum
com erro no terminal.

---

## 11. Onde esta skill para

Não improvise a matéria de ninguém: vá na skill dona.

| O assunto | A skill |
|---|---|
| posicionar, alinhar, medir margem, `next_to`/`to_edge`/`align_to`, enquadramento, z-index, formato vertical | **`manim-layout-posicionamento`** |
| animar (o catálogo de `Animation`, `.animate`, `Transform` × `ReplacementTransform`) | **`manim-animations`** |
| ritmo, `rate_func`, `lag_ratio`, `run_time`, `path_func`, composição | **`manim-composicao-ritmo`** |
| cor, contraste, paleta, `set_default`, tema, "sumiu no fundo branco" | **`manim-color-theming`** |
| `Text` `MarkupText` `Tex` `MathTex`, `t2c`, glifos, nitidez do texto | **`manim-text-latex`** |
| `Axes` `NumberPlane` `NumberLine` `BarChart` `FunctionGraph`, plotar | **`manim-graphs-plots`** |
| `Table` `Matrix` e suas variantes | **`manim-tabelas-matrizes`** |
| `Graph` `DiGraph` `LayoutFunction`, layout automático de rede | **`manim-grafos-redes`** |
| `Sphere` `Cube` `Surface` `Polyhedron` `ConvexHull3D`, câmera 3D | **`manim-3d-camera`** |
| `SVGMobject` `ImageMobject` `register_font`, asset externo | **`manim-svg-imagens`** |
| herdar de `VMobject`, construir caminho de Bézier, `VDict`/`PGroup`, `Union` por dentro, `utils/bezier`, `utils/space_ops`, `override_animate` | **`manim-mobjects-customizados`** |
| `ValueTracker`, updater, `always_redraw`, número que conta | **`manim-updaters-valuetracker`** |
| `Scene.add`/`remove`/`bring_to_front`/`add_foreground_mobject`, seções, de qual `Scene` herdar | **`manim-cenas-secoes`** |
| zoom e pan 2D, `self.camera.frame` | **`manim-camera-2d`** |
| descobrir se um nome/kwarg existe, regenerar o índice | **`manim-api-discovery`** |
| renderizar, qualidade, formato, onde o arquivo saiu | **`manim-render-api`** |
| olhar o PNG, conferir sem render, pôster vazio | **`manim-verificacao-visual`** |
| cena cortada em partes para slide | **`manim-presentation-parts`** |
| erro de ambiente, codec, LaTeX, traceback | **`manim-troubleshooting`** |

**Buracos declarados — não invente skill que não existe.** Ênfase e anotação
animada (`Flash` `Indicate` `Circumscribe` `FocusOn` `Wiggle` `ApplyWave`
`ShowPassingFlash`) não têm dona. `Code` `Typst` `Paragraph` `Variable`
`BulletedList` `Title` não têm dona. `VectorField` `ArrowVectorField`
`StreamLines` não têm dona. Os **45** mobjects `OpenGL*` de `mobject/opengl`
ficam órfãos **de propósito**: no fluxo de aula o renderer é o cairo, e espelhar
45 classes custa caro e rende pouco. `Broadcast`, `ManimBanner` e `SampleSpace`
são órfãos triviais.

---

## 12. O que mudou nesta revisão, e por quê

Registro para quem vier depois — cinco afirmações da versão anterior estavam
erradas e foram corrigidas contra o índice e o fonte:

1. **`mob.set_width(4)` / `mob.set_height(2)` apresentados como API.** `set_width`
   só existe em `OpenGLMobject` (45/45 linhas do `methods.tsv`); no cairo é
   síntese de `__getattr__`. Substituído por `scale_to_fit_width` e explicado o
   mecanismo, que é o que protege contra o `set_<typo>` silencioso (§5.1).
2. **`Brace` e `BraceLabel` listados em `mobject/geometry`.** São
   `mobject/svg` — `manim.mobject.svg.brace` (§8.5).
3. **`ImageMobject` listado em `mobject/svg`.** É `mobject/core`,
   `manim.mobject.types.image_mobject`. E a matéria é de `manim-svg-imagens`.
4. **`point_from_proportion` na lista de consultas genéricas.** Em `Mobject` é
   tampão `NotImplementedError` (§3).
5. **`Transform` × `ReplacementTransform` explicados aqui.** Duplicavam
   `manim-animations`, que é a dona. Viraram ponteiro (§7).
