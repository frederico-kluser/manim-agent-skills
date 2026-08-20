---
name: manim-mobjects-customizados
description: >-
  ESTENDER a biblioteca em vez de usá-la: quando vale escrever uma classe
  própria e quando uma função-fábrica que devolve `VGroup` é a resposta certa;
  herdar de `VMobject`/`VGroup`/`Mobject`/`PMobject`; o modelo de `points`
  (âncoras e alças, 4 pontos por curva cúbica); construir caminho à mão
  (`start_new_path`, `add_line_to`, `add_cubic_bezier_curve_to`,
  `set_points_as_corners`, `set_points_smoothly`, `close_path`, `make_smooth`);
  `copy()` × `deepcopy` × `become` × `match_points` × `save_state` e o que cada
  um MUTA; o alinhamento (`align_data`, `align_points`, `add_n_more_submobjects`)
  que explica por que duas formas não casam num `Transform`; combinar formas
  (grupo × subpath × booleano); os booleanos `Union`/`Intersection`/`Difference`/
  `Exclusion`/`Cutout` e `ConvexHull`/`QuickHull` POR DENTRO; escrever uma
  `Animation` própria (`interpolate_mobject`, `interpolate_submobject`,
  `begin`/`finish`, `remover`/`introducer`); `override_animate` e
  `override_animation`; e a matemática de `utils/bezier` (17 funções) e
  `utils/space_ops` (36). Use quando o pedido for "cria uma classe própria para
  isso", "faço um Mobject novo ou um VGroup?", "quero uma forma que não existe no
  catálogo", "desenhar um caminho ponto a ponto", "uma seta/balão/engrenagem
  personalizada", "combinar duas formas numa só", "furar essa forma", "recortar",
  "por que o Create não anima a minha classe", "por que o Transform deforma",
  "por que a cópia mexeu no original", "escrever uma animação nova", "quero que
  `.animate.meu_metodo()` funcione", "o FadeIn dessa classe tem que ser outra
  coisa", "por que apply_function ignorou o about_point". NÃO use para: escolher
  entre as formas que JÁ existem, `VGroup` × `Group`, estilo e caixa
  delimitadora (`manim-mobjects`); posicionar e alinhar (`manim-layout-posicionamento`);
  o catálogo de animações prontas e `Transform` × `ReplacementTransform`
  (`manim-animations`); `rate_func`, `path_func`, `lag_ratio` e composição
  (`manim-composicao-ritmo`); updaters e `always_redraw`
  (`manim-updaters-valuetracker`); cor, contraste e tema (`manim-color-theming`);
  `SVGMobject`/`ImageMobject` (`manim-svg-imagens`); `Surface`, `Polyhedron`,
  `ConvexHull3D` (`manim-3d-camera`); só descobrir se um nome existe
  (`manim-api-discovery`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Mobjects customizados — estender a biblioteca

Esta skill começa com uma pergunta desconfortável: **na maior parte das vezes
você não deveria escrever uma classe.** O Manim convida à herança — a
biblioteca inteira é uma árvore de subclasses de `VMobject` — mas o código de
produção que consome este projeto não tem nenhuma. Aqui está o número, e depois
está o resto: como se herda direito quando herdar é mesmo a resposta.

## Procedência do que está escrito aqui

Quatro marcadores, e valem para o arquivo inteiro:

- **[FONTE]** — lido no ManimCE **0.21.0** instalado em
  `.venv/lib/python3.12/site-packages/manim/`, com arquivo e linha, ou no índice
  estático de `api/`. Afirmação forte.
- **[HOJE]** — apurado nesta sessão (2026-08-19) com `grep`/`awk`/`sed` sobre o
  fonte e sobre o deck consumidor. **Nenhum render, nenhum `ffmpeg`, nenhuma
  GPU, nenhum Python executado.**
- **[DECK]** — contado ou medido no deck consumidor `~/Projects/aulas`
  (13 arquivos de cena, ~76 classes de cena, 59+ partes em produção).
- **[PYTHON]** — semântica de CPython 3.12 lida em `/usr/lib/python3.12/`.

**Nenhum exemplo desta skill foi executado.** As assinaturas foram todas
conferidas no índice ou no fonte; a composição delas em código que roda, não.
Onde um comportamento é inferência minha e não leitura direta, está marcado
**[NÃO VERIFICADO]**.

## Cartão de referência — o sintoma manda na seção

| O que você quer / o que aconteceu | Onde ler |
|---|---|
| "faço uma classe ou uma função?" | **§1** — a decisão, com o número do deck |
| vou herdar: de quem? | §2.1, a tabela de bases |
| escrevi `__init__`, os atributos não chegaram no desenho | §2.2 — `generate_points` roda DENTRO de `Mobject.__init__` |
| `init_points` ou `generate_points`? | §2.3 |
| classe que agrupa peças com nome | §3 |
| desenhar uma forma que não existe: caminho ponto a ponto | §4 |
| `IndexError: index -1 is out of bounds for axis 0 with size 0` (num `add_line_to`) | §4.2 |
| `Exception: Cannot call Mobject.add_cubic_bezier_curve_to for a Mobject with no points` | §4.2 |
| a forma saiu **invisível** e sem erro | §4.5 |
| quantas curvas isso tem? o ponto a 30% do caminho? | §5 |
| `Create` não anima a minha classe / `TypeError: … only works for VMobjects` | §6 |
| a cópia mexeu no original / o updater da cópia mexe no original | §7.2 |
| `become` mudou o objeto que eu passei como ARGUMENTO | §7.3 |
| `Transform` deforma, torce ou "explode" a forma | §8 |
| `NotImplementedError: Please override in a child class.` | §8.3 |
| combinar duas formas numa só | §9 — as quatro rotas |
| `Union`/`Difference` saiu vazio, ou perdeu o texto | §10.2 |
| `ConvexHull` saiu errado | §10.4 |
| escrever uma `Animation` nova | §11 |
| `.animate.meu_metodo()` tem que virar outra animação | §12.1 |
| `FadeIn` dessa classe tem que ser `Create` | §12.2 |
| `MultiAnimationOverrideException` | §12.3 |
| `apply_function(f, about_point=X)` ignorou o `about_point` | §13.1 |
| preciso de `rotate_vector`, `line_intersection`, `shoelace`, `split_bezier` | §14 |
| conferir a classe nova sem renderizar | §15 |

---

## 1. A decisão que vem antes de tudo: função-fábrica ou subclasse

### 1.1 O número

[DECK, contado hoje] O deck consumidor tem **13 arquivos de cena**, **104
funções de módulo** e **zero** subclasses de `Mobject`, `VMobject`, `VGroup`,
`Group`, `VDict` ou de qualquer forma pronta. Das 104 funções, **25 devolvem
`VGroup`** e uma devolve `tuple[VGroup, list[RoundedRectangle], list]`. Todo
componente visual reutilizável da produção — a pasta com aba, a caixa de
plugin, a gaveta, a pilha de blocos, o cartão, o recado de rodapé, o contador —
é **uma função que monta primitivas e devolve o grupo**.

Isso não é preguiça: é a escolha que sobreviveu a 59 partes de vídeo em
produção. As razões estão em §1.3.

### 1.2 As duas formas, lado a lado

```python
# ROTA A — função-fábrica (o padrão do deck)
def _caixa(rotulo: str, cor: str, largura: float = 2.4) -> VGroup:
    corpo = RoundedRectangle(corner_radius=0.08, width=largura, height=0.62,
                             fill_color=CANVAS, fill_opacity=1.0,
                             stroke_color=cor, stroke_width=1.6)
    texto = txt(rotulo, T_MIUDO, cor)
    texto.move_to(corpo.get_center())
    return VGroup(corpo, texto)

# ROTA B — subclasse
class Caixa(VGroup):
    def __init__(self, rotulo: str, cor: str, largura: float = 2.4, **kwargs):
        super().__init__(**kwargs)
        self.corpo = RoundedRectangle(...)
        self.texto = txt(rotulo, T_MIUDO, cor).move_to(self.corpo.get_center())
        self.add(self.corpo, self.texto)
```

*(Nenhum dos dois foi executado nesta sessão. `VGroup(*vmobjects, **kwargs)` e
`VGroup.add(*vmobjects)` conferidos no índice [FONTE].)*

### 1.3 Quando cada uma ganha

| Escolha | Quando ela é a resposta |
|---|---|
| **Função-fábrica → `VGroup`** | o caso comum. Você quer um arranjo de primitivas com um nome. Não precisa de método próprio, não precisa que `isinstance` diga nada, e **as peças internas precisam ser animadas separadamente** (§1.4) |
| **Função-fábrica → tupla** | quando outro ato vai animar UMA peça: `return grupo, moldura, selo`. [DECK] é o padrão de produção, e a docstring de lá diz por quê: *"as três referências extras não são luxo: a parte 1 monta a pasta em tempos e o ato 2 troca linhas e selo sem tocar no resto"* |
| **Subclasse de `VGroup`** | há **método próprio com estado** (`caixa.acender()`, `medidor.set_valor(0.4)`), ou você quer `@override_animate` (§12.1), ou `isinstance` decide alguma coisa no código |
| **Subclasse de `VMobject`** | a forma **não é** composição de formas prontas: é um caminho que você calcula (§4). Zigue-zague, balão com bico, contorno paramétrico, engrenagem |
| **Subclasse de `Mobject`** puro | quase nunca. Você perde `set_fill`, `set_stroke`, `point_from_proportion`, `pointwise_become_partial` — e ganha os `NotImplementedError` de §8.3 |
| **Subclasse de `PMobject`** | nuvem de pontos (`Point`, `PointCloudDot`, `Mobject1D`, `Mobject2D`). Nicho real, mas raro em aula |

### 1.4 As três razões concretas para NÃO subclassar

1. **A herança não te dá nomes; o `__init__` sim — e o `__init__` é o mesmo
   trabalho da função.** A vantagem real da rota B é `self.corpo` /
   `self.texto`. A rota A alcança o mesmo devolvendo a tupla, sem herdar nada.
   Alcançar por índice (`grupo[0][2]`) é que é frágil: quebra em silêncio no dia
   em que alguém acrescenta um submobject.
2. **Uma subclasse de `VGroup` herda um contrato que você não escreveu.**
   [FONTE] `VGroup._assert_valid_submobjects` recusa qualquer coisa que não seja
   `VMobject` — sua classe passa a recusar `ImageMobject` sem que você tenha
   decidido isso. Herda também `__add__`/`__sub__`/`__setitem__` (§3.3), cujo
   comportamento surpreende.
3. **A subclasse entra na maquinaria de `Animation`.** [FONTE]
   `Mobject.__init_subclass__` (`mobject.py:100-105`) roda em TODA subclasse e
   faz três coisas: zera `cls.animation_overrides = {}`, chama
   `cls._add_intrinsic_animation_overrides()` (que varre `dir(cls)` atrás de
   métodos decorados) e guarda `cls._original__init__`. É de graça enquanto você
   não usa overrides — mas é a superfície onde §12.3 explode.

### 1.5 O teste de uma linha

> Se a resposta para *"que método próprio esta classe tem?"* for "nenhum",
> escreva uma função.

---

## 2. Herdar: de quem, e o que roda quando

### 2.1 A tabela de bases

[FONTE] declarações conferidas em `mobject/mobject.py:72`,
`mobject/types/vectorized_mobject.py:81,2181,2410`,
`mobject/types/point_cloud_mobject.py:47,287`.

| Base | Declaração real | O que você ganha | O que você tem de escrever |
|---|---|---|---|
| `Mobject` | `class Mobject:` | árvore de submobjects, posicionamento, caixa delimitadora, updaters | tudo o que desenha; e os tampões de §8.3 |
| `VMobject` | `class VMobject(Mobject):` | `points` como spline cúbica, `set_fill`/`set_stroke`, `point_from_proportion`, `pointwise_become_partial` | `generate_points()` (ou monte o caminho no `__init__`) |
| `VGroup` | `class VGroup(VMobject, metaclass=ConvertToOpenGL):` | contêiner que só aceita `VMobject`, operadores, `add` variádico | só o `__init__` que monta as peças |
| `VDict` | `class VDict(VMobject, metaclass=ConvertToOpenGL):` | acesso por chave (`d["sq"]`), `add`/`remove` por chave | idem |
| `PMobject` | `class PMobject(Mobject, metaclass=ConvertToOpenGL):` | nuvem de pontos com `rgbas` por ponto | `generate_points()` chamando `add_points(...)` |

**A base que quase ninguém precisa é `Mobject` puro.** [FONTE] Cinco métodos do
`Mobject` são tampões que levantam `NotImplementedError`
(`mobject.py:2400, 2403, 3028, 3044, 3177`) — quatro com a mensagem *"Please
override in a child class."* e `get_point_mobject` com uma mensagem própria. Se
a sua classe não herda de `VMobject`/`PMobject`, ela cai neles no primeiro
`Transform`. O inventário desses cinco é de **`manim-api-discovery §1`**.

### 2.2 A ordem de construção — e a regra que economiza uma tarde

[FONTE] `mobject.py:107-127`, o `__init__` inteiro:

```python
self.name = ...; self.dim = dim; self.target = target; self.z_index = z_index
self.point_hash = None
self.submobjects = []
self.updaters = []
self.updating_suspended = False
self.color = ManimColor.parse(color)

self.reset_points()      # points = np.zeros((0, dim))
self.generate_points()   # <— o SEU desenho, ainda dentro do super().__init__()
self.init_colors()       # VMobject aplica fill/stroke aqui
```

> **`generate_points()` é chamado DE DENTRO de `super().__init__()`.**
> Qualquer atributo que o seu `generate_points` leia precisa existir **antes**
> da chamada a `super().__init__()`.

É exatamente o que a biblioteca faz. [FONTE] `geometry/arc.py:330-343`:

```python
class Arc(TipableVMobject):
    def __init__(self, radius=1.0, start_angle=0, angle=TAU/4, num_components=9, ...):
        self.radius = radius
        self.num_components = num_components
        self.arc_center = arc_center
        self.start_angle = start_angle
        self.angle = angle
        self._failed_to_get_center = False
        super().__init__(**kwargs)      # <— só agora; generate_points já vê tudo

    def generate_points(self):
        self._set_pre_positioned_points()
        self.scale(self.radius, about_point=ORIGIN)
        self.shift(self.arc_center)
        return self
```

O modo de falha, se você inverter: `AttributeError: 'MinhaForma' object has no
attribute 'raio'` **vindo de dentro do `super().__init__()`** — um traceback que
não menciona a sua linha e manda a maioria das pessoas procurar no lugar errado.

**A alternativa legítima:** não implemente `generate_points` e monte o caminho
*depois* do `super().__init__()`, no corpo do seu `__init__`. É o que
`Polygram` faz. [FONTE] `geometry/polygram.py:36-53`:

```python
def __init__(self, *vertex_groups, color=BLUE, **kwargs):
    super().__init__(color=color, **kwargs)
    for vertices in vertex_groups:
        first_vertex, *vertices = vertices
        first_vertex = np.array(first_vertex)
        self.start_new_path(first_vertex)
        self.add_points_as_corners([*(np.array(v) for v in vertices), first_vertex])
```

As duas rotas funcionam. A diferença prática: quem implementa `generate_points`
pode chamá-lo de novo depois para **redesenhar** (é o que `Arc.init_points`
faz); quem monta no `__init__` não tem esse botão.

### 2.3 `generate_points` × `init_points` — não são sinônimos

[HOJE, `api/manim-ce-methods.tsv`] **`Mobject` não tem `init_points`.** O gancho
do renderer cairo é `generate_points`. `init_points` é o nome do lado
**OpenGL** (`OpenGLMobject.init_points`), e algumas classes do cairo definem os
dois: `Arc` tem `generate_points` (posicionado) **e** `init_points`
(pré-posicionado, com o comentário no fonte *"Points are set a bit differently
when rendering via OpenGL"*), enquanto `Line` e `PointCloudDot` fazem
`init_points(self): self.generate_points()` — alias puro.

> Para uma classe sua no fluxo normal (renderer cairo): **implemente
> `generate_points`**. Implementar só `init_points` produz uma forma vazia, sem
> erro nenhum.

### 2.4 `set_default` numa classe sua

[FONTE] `mobject.py:296-306` — `Mobject.set_default(**kwargs)` é `classmethod` e
faz `cls.__init__ = partialmethod(cls.__init__, **kwargs)`; sem kwargs, restaura
`cls._original__init__` (guardado por `__init_subclass__`). Funciona na sua
classe porque `__init_subclass__` roda para ela também. **[PYTHON]** chamadas
sucessivas empilham `partialmethod`s (a última vence, porque `partial` faz
`{**self.keywords, **call_kwargs}`), e só `set_default()` sem argumentos desfaz
a pilha. Quem é dono do assunto — o que ele alcança e o que ele **não** alcança
— é **`manim-color-theming §10`**.

---

## 3. Herdar de `VGroup` — o caso mais comum de subclasse legítima

### 3.1 O modelo, com o exemplo da própria biblioteca

[FONTE] `mobject/mobject.py:3519-3529`, na docstring de `override_animate`:

```python
class CircleWithContent(VGroup):
    def __init__(self, content):
        super().__init__()
        self.circle = Circle()
        self.content = content
        self.add(self.circle, content)
        content.move_to(self.circle.get_center())

    def clear_content(self):
        self.remove(self.content)
        self.content = None
```

Três coisas para copiar daí: (a) `super().__init__()` **primeiro** — num `VGroup`
não há `generate_points` seu, então a ordem de §2.2 não morde; (b) as peças
ganham **nome de atributo**, que é a razão inteira de a classe existir; (c)
`self.add(...)` é o que as põe na árvore — atribuir a um atributo **não** as
adiciona.

> `self.corpo = Rectangle()` sem `self.add(self.corpo)` produz um grupo vazio
> que se posiciona no ORIGIN e não desenha nada. Sem erro.

### 3.2 O contrato herdado: só `VMobject` entra

[FONTE] `vectorized_mobject.py:174-175` — `VGroup._assert_valid_submobjects`
delega para `_assert_valid_submobjects_internal(submobjects, VMobject)`. Sua
subclasse herda a restrição: `ImageMobject` levanta `TypeError`. Se o seu
componente precisa misturar bitmap com vetor, herde de **`Group`**
(`Group(*mobjects, **kwargs)` [FONTE]), não de `VGroup`. O par `VGroup` × `Group`
é matéria de **`manim-mobjects §6`**.

### 3.3 Os operadores que você herda sem pedir

[FONTE] `vectorized_mobject.py:2368-2389`:

```python
def __add__(self, vmobject):  return VGroup(*self.submobjects, vmobject)
def __iadd__(self, vmobject): return self.add(vmobject)
def __sub__(self, vmobject):
    copy = VGroup(*self.submobjects); copy.remove(vmobject); return copy
def __isub__(self, vmobject): return self.remove(vmobject)
def __setitem__(self, key, value):
    self._assert_valid_submobjects(tuplify(value))
    self.submobjects[key] = value
```

Três armadilhas, todas silenciosas:

- **`g + x` devolve um `VGroup` NOVO** (e da classe `VGroup`, **não** da sua
  subclasse) que **não está na cena**. `g += x` muta. Quem escreve `g + x`
  esperando o segundo comportamento perde o objeto.
- **`g - x` compartilha os membros.** `VGroup(*self.submobjects)` guarda as
  MESMAS referências: mover o resultado move os membros do original. Não é cópia.
- **`g[0] = novo` troca a lista e mais nada.** O submobject antigo continua na
  cena se tiver sido adicionado por fora, e o novo não é adicionado a lugar
  nenhum além da lista de filhos.

### 3.4 `VDict` — quando as peças têm nome mas são variáveis

[FONTE] `VDict(mapping_or_iterable={}, show_keys=False, **kwargs)`, métodos
próprios `add(mapping_or_iterable)`, `add_key_value_pair(key, value)`,
`remove(key)`, `get_all_submobjects()`, mais `__getitem__`/`__setitem__`/
`__delitem__`/`__contains__` por chave.

```python
d = VDict({"caixa": Square(), "rotulo": Text("x", color=TINTA)})
d["seta"] = Arrow(LEFT, RIGHT, color=ACENTO)   # substitui se a chave já existir
del d["rotulo"]
```

**Duas diferenças que quebram o hábito de `VGroup`:** `VDict.add` recebe um
**mapeamento**, não `*vmobjects`; e `VDict.remove` recebe uma **chave**, não um
mobject. [FONTE] `__setitem__` (`vectorized_mobject.py:2607-2630`) faz
`if key in self.submob_dict: self.remove(key)` antes de adicionar — reatribuir é
seguro. `show_keys=True` desenha as chaves na tela: é ferramenta de depuração,
não de produção.

Use `VDict` quando o conjunto de peças **varia em tempo de execução** e você
precisa alcançá-las por nome. Para um componente com peças fixas, atributo
nomeado num `VGroup` é mais simples e tipável.

---

## 4. Herdar de `VMobject` — desenhar um caminho

### 4.1 O modelo de `points`

Um `VMobject` guarda **uma única matriz** `points` de forma `(N, 3)`. Ela não é
uma lista de vértices: é uma sequência de curvas de Bézier **cúbicas**, quatro
pontos por curva. [FONTE] `VMobject.__init__(..., n_points_per_cubic_curve=4)` e
`set_anchors_and_handles` (`vectorized_mobject.py:821-853`):

```
points = [ a0, h0, h1, a1,  a1, h2, h3, a2,  a2, ... ]
           ^   ^   ^   ^
           |   |   |   +-- âncora final da curva 0 (= âncora inicial da curva 1)
           |   +---+------ as duas alças de controle
           +-------------- âncora inicial
```

Portanto: **`len(points)` é sempre múltiplo de 4 num caminho fechado e
consistente**, e `get_num_curves() == len(points) // 4`. Um resto 1 significa
"um caminho recém-começado, com só a âncora inicial" — [FONTE]
`has_new_path_started(): return len(self.points) % nppcc == 1`
(`vectorized_mobject.py:1052-1055`).

Um **subcaminho** (subpath) é um trecho contíguo dessas curvas separado dos
outros por um `start_new_path`. É assim que uma letra com furo, um `Polygram` de
vários laços ou o resultado de um booleano moram num único `VMobject` sem
submobject nenhum.

### 4.2 As primitivas de construção — a ordem importa

Assinaturas [FONTE], todas devolvendo `Self` (encadeáveis):

```python
VMobject.start_new_path(point: Point3DLike) -> Self
VMobject.add_line_to(point: Point3DLike) -> Self
VMobject.add_cubic_bezier_curve_to(handle1, handle2, anchor) -> Self
VMobject.add_cubic_bezier_curve(anchor1, handle1, handle2, anchor2) -> Self
VMobject.add_quadratic_bezier_curve_to(handle, anchor) -> Self
VMobject.add_smooth_curve_to(*points) -> Self          # 1 ou 2 pontos, senão ValueError
VMobject.add_points_as_corners(points: Point3DLike_Array) -> Self
VMobject.add_subpath(points: CubicBezierPathLike) -> Self
VMobject.append_points(new_points: Point3DLike_Array) -> Self
VMobject.close_path() -> Self
VMobject.set_points_as_corners(points: Point3DLike_Array) -> Self
VMobject.set_points_smoothly(points: Point3DLike_Array) -> Self
VMobject.set_points(points: Point3DLike_Array) -> Self
VMobject.set_anchors_and_handles(anchors1, handles1, handles2, anchors2) -> Self
VMobject.clear_points() -> Self
```

**A regra que produz o erro mais comum:** tudo que começa com `add_…_to` exige
que o caminho já tenha começado. A correção é sempre a mesma —
**`start_new_path(primeiro_ponto)` antes** — mas o **erro que aparece na tela
depende de por onde você entrou**, e vale saber os dois para não grepar a string
errada.

**Correção.** Uma versão anterior desta seção imprimia, marcada `[FONTE]`,
`Exception: Cannot call Mobject.add_line_to for a Mobject with no points`. Essa
string **não pode existir**, por duas razões independentes.

**(a) `add_line_to` nunca chega à guarda.** Ele avalia `get_last_point()`
dentro da própria lista de argumentos (`vectorized_mobject.py:1001-1004`):

```python
self.add_cubic_bezier_curve_to(
    *(interpolate(self.get_last_point(), point, t) for t in self._bezier_t_values[1:])
)
```

`get_last_point()` é `self.points[-1]`, e num `VMobject()` novo `points` tem
forma `(0, 3)`. Medido:

```console
$ .venv/bin/python -c "from manim import VMobject; VMobject().add_line_to([1,0,0])"
IndexError: index -1 is out of bounds for axis 0 with size 0
```

`add_quadratic_bezier_curve_to` (`:983-985`) faz o mesmo — a alegação de que
"passam pela guarda" também era falsa.

**(b) O nome na mensagem sai do chamador DIRETO.** `mobject.py:3336-3341` usa
`sys._getframe(1).f_code.co_name`, e os **cinco** sítios que chamam
`throw_error_if_no_points` (`vectorized_mobject.py:953, 1041, 1087, 1664, 1711`)
são `add_cubic_bezier_curve_to`, `add_smooth_curve_to`,
`add_points_as_corners` e `point_from_proportion`. `add_line_to` não está entre
eles e nunca estará.

| Você chamou | O que estoura |
|---|---|
| `add_line_to`, `add_quadratic_bezier_curve_to` | `IndexError: index -1 is out of bounds for axis 0 with size 0` |
| `add_cubic_bezier_curve_to` | `Exception: Cannot call Mobject.add_cubic_bezier_curve_to for a Mobject with no points` |
| `add_smooth_curve_to` | idem, com `add_smooth_curve_to` no lugar do nome |
| `add_points_as_corners`, `point_from_proportion` | idem, com o nome respectivo |

`set_points_as_corners`, ao contrário, **substitui** tudo e não precisa de nada
antes — é o atalho para uma polilinha inteira de uma vez.

### 4.3 `set_…` × `add_…` — a distinção que decide o resultado

| | `set_points_as_corners(pts)` | `add_points_as_corners(pts)` |
|---|---|---|
| pontos anteriores | **descartados** | preservados; a polilinha continua do último ponto |
| precisa de caminho aberto | não | **sim** (`throw_error_if_no_points`) |
| N pontos produzem | N−1 curvas | N curvas (a primeira sai do ponto atual) |

[FONTE] `set_points_as_corners` (`vectorized_mobject.py:1113-1157`) chama
`set_anchors_and_handles(*(interpolate(points[:-1], points[1:], t) for t in ...))`
— com **um** ponto só, `points[:-1]` é vazio e o resultado é um mobject com
**zero curvas**: invisível, sem erro. Com dois pontos, uma curva reta.

[FONTE] `add_points_as_corners` (`:1069-1111`) tem um detalhe que surpreende:
se `has_new_path_started()`, ele **remove o último ponto** (`self.points =
self.points[:-1]`) antes de anexar, porque aquela âncora solta vira o começo da
primeira curva nova. É por isso que o idioma `start_new_path(p0)` seguido de
`add_points_as_corners([p1, p2, p0])` produz exatamente 3 curvas, e não 4.

### 4.4 As três formas de fechar

```python
v.close_path()                       # acrescenta uma reta até o início do ÚLTIMO subpath
v.add_points_as_corners([..., p0])   # repetir o primeiro ponto no fim (o que Polygram faz)
v.is_closed()                        # -> bool: o primeiro e o último ponto coincidem?
```

[FONTE] `close_path` (`:1064-1067`) é `if not self.is_closed(): self.add_line_to(self.get_subpaths()[-1][0])`
e `is_closed` compara `points[0]` com `points[-1]` — **os do mobject inteiro**,
não os do último subcaminho. Num caminho de vários subcaminhos, `is_closed()`
pode devolver `False` mesmo com todos os laços fechados. Não use `is_closed`
como teste de "esta forma preenche".

O preenchimento (`fill_opacity`) segue a regra de par-ímpar do cairo: dois laços
sobrepostos no mesmo `VMobject` produzem um **furo**, não uma mancha dupla.
[NÃO VERIFICADO por render] — é o mecanismo em que `Cutout` se apoia, e o
motivo de a docstring dele avisar que se comporta como diferença simétrica.

### 4.5 A armadilha que apaga o seu trabalho: o `VMobject` nasce branco

Um `VMobject()` recém-construído tem `stroke_color` branco e `fill_opacity=0`
[FONTE] `VMobject.__init__(fill_opacity=0.0, stroke_width=4, ...)`. Em tema
claro isso é **invisível, sem erro nenhum**.

O exemplo real de produção, com a docstring original [DECK]
(`aulas/002-deepseek-harness/manim/aula_002_monolito.py:272-289`) — a única
construção de caminho à mão em 13 arquivos de cena:

```python
def _fissura(y, x0, x1, dentes=9, amp=0.05) -> VMobject:
    """
    A rachadura: um zigue-zague curto atravessando o bloco na costura entre
    duas bandas.

    Cor explícita e escura (`TINTA_2`): um `VMobject` novo nasce BRANCO, e
    branco sobre o cinza do bloco — sobre o branco do fundo, então — some sem
    erro nenhum. É a armadilha nº 1 do Manim neste deck.
    """
    pontos = []
    for i in range(dentes + 1):
        x = x0 + (x1 - x0) * i / dentes
        pontos.append([x, y + (amp if i % 2 else -amp), 0])
    traco = VMobject().set_points_as_corners(pontos)
    return traco.set_stroke(TINTA_2, width=3.0)
```

Repare que ele nem subclassa: `VMobject()` cru + `set_points_as_corners` +
`set_stroke`. Para uma forma sem método próprio, isso é o suficiente — §1 de
novo. A disciplina de cor (um `tema.py`, um helper obrigatório) é de
**`manim-color-theming §11`** e **`manim-tema-projeto`**.

### 4.6 Suavizar e endurecer

```python
VMobject.make_smooth() -> Self       # = change_anchor_mode("smooth")
VMobject.make_jagged() -> Self       # = change_anchor_mode("jagged")
VMobject.change_anchor_mode(mode: Literal["jagged","smooth"]) -> Self
VMobject.set_points_smoothly(points) -> Self   # = set_points_as_corners + make_smooth
```

[FONTE] `change_anchor_mode` (`:1163-1196`) percorre
`self.family_members_with_points()`, extrai as âncoras de cada subcaminho,
recalcula as alças (`get_smooth_cubic_bezier_handle_points` no modo smooth;
interpolação a 1/3 e 2/3 no jagged) e reescreve os pontos. Duas consequências:

- ele **propaga por família** — chamar em um grupo suaviza todos os filhos;
- ele **descarta** as alças que você tinha posto à mão. `add_cubic_bezier_curve_to`
  com alças cuidadosamente escolhidas seguido de `make_smooth()` joga o trabalho
  fora.

### 4.7 Sentido do caminho

```python
VMobject.get_direction() -> Literal["CW","CCW"]
VMobject.force_direction(target_direction: Literal["CW","CCW"]) -> Self
VMobject.reverse_direction() -> Self
```

Importa em duas situações: no preenchimento com furo (o furo tem de ter o
sentido oposto ao do contorno — é o que `Cutout` explora, e por isso ele **muta**
os argumentos com `force_direction`, [FONTE] `polygram.py:790-799`, detalhado em
**`manim-mobjects §8.2`**) e na direção em que `Create` desenha.

---

## 5. Consultar e reamostrar curvas

Tudo [FONTE], métodos próprios de `VMobject`:

```python
get_num_curves() -> int
get_anchors() -> list[Point3D]                     # só as âncoras, na ordem
get_start_anchors() -> Point3D_Array               # a âncora inicial de cada curva
get_end_anchors() -> Point3D_Array
get_anchors_and_handles() -> list[Point3D_Array]   # 4 arrays: a1, h1, h2, a2
get_cubic_bezier_tuples() -> CubicBezierPoints_Array
get_subpaths() -> list[CubicSpline]
get_nth_curve_points(n) -> CubicBezierPoints
get_nth_curve_function(n) -> Callable[[float], Point3D]
get_nth_curve_length(n, sample_points=None) -> float
get_curve_functions() -> Iterable[Callable[[float], Point3D]]
get_arc_length(sample_points_per_curve=None) -> float
point_from_proportion(alpha: float) -> Point3D
proportion_from_point(point: Point3DLike) -> float
get_subcurve(a: float, b: float) -> Self
insert_n_curves(n: int) -> Self
insert_n_curves_to_point_list(n, points) -> BezierPath
resize_points(new_length, resize_func=resize_array) -> Self
split() -> list[VMobject]
nonempty_submobjects() -> Sequence[VMobject]
```

Notas que valem um render cada:

- **`get_vertices()` é do `Polygram`, não do `VMobject`.** [FONTE]
  `Polygram.get_vertices()` é literalmente `return self.get_start_anchors()`. Na
  sua classe, use `get_start_anchors()`.
- **`point_from_proportion` levanta.** [FONTE] `vectorized_mobject.py:1661-1664`:
  `ValueError` se `alpha` sai de [0, 1], e `throw_error_if_no_points()` logo em
  seguida. Num `VMobject` vazio, exceção — não `ORIGIN`.
- **`insert_n_curves(n)` acrescenta `n` curvas**, não redimensiona para `n`.
  É a peça que faz duas formas diferentes casarem antes de um `Transform` (§8), e
  é também o custo: dobrar as curvas dobra o trabalho de rasterização por frame.
  O assunto "quanto custa" é de **`manim-performance-cache`**.
- **`get_subcurve(a, b)` devolve um mobject novo** com o pedaço do caminho;
  `DashedVMobject` é construído com ele. [FONTE] `DashedVMobject` termina em
  `self.match_style(base_vmobject, family=False)`, que **descarta o `color=` do
  construtor** — armadilha documentada em **`manim-mobjects §8.4`**; estilize o
  original antes de embrulhar.
- **`CurvesAsSubmobjects(vmobject)`** [FONTE] `vectorized_mobject.py:2787-2810`
  quebra uma curva em N `VMobject`s de uma curva cada, cada um com
  `match_style` do original. É como se faz gradiente ao longo de um traço
  (`set_color_by_gradient` depois). Custo: N submobjects onde havia 1.

---

## 6. `pointwise_become_partial` — a razão de `Create` não funcionar na sua classe

```python
VMobject.pointwise_become_partial(vmobject: VMobject, a: float, b: float) -> Self
```

É o método que **desenha o caminho parcialmente**, de `t = a` a `t = b`. Quem o
chama, um por frame, é `ShowPartial` — a base de `Create`, `Uncreate`,
`DrawBorderThenFill`, `Write` e `ShowPassingFlash`. [FONTE]
`animation/creation.py:126-134`:

```python
def interpolate_submobject(self, submobject, starting_submobject, alpha):
    submobject.pointwise_become_partial(starting_submobject, *self._get_bounds(alpha))
```

E a guarda, no construtor [FONTE] `creation.py:116-124`:

```python
pointwise = getattr(mobject, "pointwise_become_partial", None)
if not callable(pointwise):
    raise TypeError(f"{self.__class__.__name__} only works for VMobjects.")
```

Consequências diretas para quem escreve classe:

1. **Herdou de `VMobject`?** Você já tem `pointwise_become_partial` de graça e
   `Create` funciona sem escrever uma linha.
2. **Herdou de `Mobject` puro?** `Create(minha)` levanta
   `TypeError: Create only works for VMobjects.` — o erro é claro, ao menos.
   As saídas: herdar de `VMobject`, ou implementar
   `pointwise_become_partial(self, mob, a, b)` você mesmo, ou usar `FadeIn`
   (que só mexe em opacidade e posição e não exige nada disso).
3. **Herdou de `VGroup`?** Funciona, e `Create` percorre a família: cada peça é
   desenhada com o mesmo `alpha`, a não ser que você passe `lag_ratio`.
   [FONTE] `Animation.get_sub_alpha` distribui o alpha por índice de família.
   O ritmo é de **`manim-composicao-ritmo`**.
4. **`BackgroundRectangle` reinterpreta o método** como opacidade em vez de
   traçado — [FONTE], e é a prova de que dá para subvertê-lo de propósito.

---

## 7. Cópia, identidade e o que cada operação MUTA

Esta é a seção onde mais gente se queima, porque o Manim tem cinco operações
parecidas com semânticas diferentes — e três delas mutam algo que você não
passou como alvo.

### 7.1 O quadro

| Operação | Assinatura [FONTE] | Devolve | Muta |
|---|---|---|---|
| `mob.copy()` | `() -> Self` | objeto novo, fora da cena | nada |
| `mob.become(outro, match_height=False, match_width=False, match_depth=False, match_center=False, stretch=False)` | `-> Self` | `self` | **`self` e `outro`** (§7.3) |
| `mob.match_points(outro, copy_submobjects=True)` | `-> Self` | `self` | só `self.points` (estilo intacto) |
| `mob.save_state()` / `mob.restore()` | `() -> Self` | `self` | `restore` usa `become` (§7.3) |
| `mob.generate_target(use_deepcopy=False)` | `-> Self` | `self.target` | grava `self.target` |
| `mob.align_data(outro, skip_point_alignment=False)` | `-> Self` | `self` | **os dois** (§8) |

### 7.2 `copy()` é `deepcopy` — e o `deepcopy` copia coisas que você esqueceu

[FONTE] `mobject.py:895-908`: `copy()` é `copy.deepcopy(self)`.
[FONTE] `mobject.py:444-451`, o `__deepcopy__` próprio:

```python
def __deepcopy__(self, clone_from_id):
    cls = self.__class__
    result = cls.__new__(cls)
    clone_from_id[id(self)] = result
    for k, v in self.__dict__.items():
        setattr(result, k, copy.deepcopy(v, clone_from_id))
    result.original_id = str(id(self))
    return result
```

Ele copia **o `__dict__` inteiro**. Isso inclui `submobjects` (bom),
`saved_state` se existir (memória), `target` se existir (memória) — e
**`updaters`**.

> **[PYTHON] + [FONTE] A armadilha do updater copiado.**
> `/usr/lib/python3.12/copy.py:187` registra
> `d[types.FunctionType] = _deepcopy_atomic`: **função e lambda não são
> copiadas**, o `deepcopy` devolve o mesmo objeto. Logo, a lista `updaters` da
> cópia contém as MESMAS funções, cujas closures continuam apontando para o
> mobject **original**.
>
> Um mobject vindo de `always_redraw` (cujo updater é
> `lambda _: mob.become(func())`, com `mob` capturado por closure) copiado com
> `.copy()` produz um objeto cujo updater **redesenha o original**. A cópia fica
> parada; o original pisca duas vezes por frame. Nada disso levanta erro.
>
> A saída: `c = mob.copy(); c.clear_updaters()` — e reinstale o updater com a
> closure certa se precisar. `clear_updaters(recursive=True)` [FONTE]. O assunto
> updater é de **`manim-updaters-valuetracker`**; o que é desta skill é a
> interação com `copy`.
>
> **[PYTHON]** Um *método vinculado* (`self.meu_updater`) é caso diferente:
> `copy.py:225-227` registra `_deepcopy_method`, que **copia o `__self__`**.
> Um updater escrito como método da sua classe, portanto, acompanha a cópia
> corretamente. É um argumento real a favor da subclasse quando há updaters.
> [NÃO VERIFICADO por execução.]

### 7.3 `become` muta o ARGUMENTO

[FONTE] `mobject.py:3291-3312`, o corpo de `become` depois da docstring:

```python
if stretch or match_height or match_width or match_depth or match_center:
    mobject = mobject.copy()        # <— só NESTE caminho o argumento é protegido
    ...
self.align_data(mobject, skip_point_alignment=True)
for sm1, sm2 in zip(self.get_family(), mobject.get_family(), strict=True):
    sm1.points = np.array(sm2.points)
    sm1.interpolate_color(sm1, sm2, 1)
```

Sem nenhum dos cinco kwargs, **`mobject` é o objeto que você passou** e
`align_data` mexe nele (§8.1). Se `self` tinha mais submobjects que `outro`,
`outro` sai da chamada com submobjects nulos acrescentados. Se `outro` estava na
cena, você acabou de mudar a caixa delimitadora dele.

Corolário desagradável: **`restore()` é `become(self.saved_state)`** [FONTE]
`mobject.py:2161-2166` — restaurar pode alterar estruturalmente o estado salvo.
E, na direção contrária, o `Restore` apaga submobjects acrescentados depois do
`save_state` (registrado em **`manim-animations`**).

Quando você quer o efeito sem o dano: `self.become(outro.copy())`.

### 7.4 `match_points` é o bisturi

[FONTE] `mobject.py:3314-3333`:

```python
for sm1, sm2 in zip(self.get_family(), mobject.get_family(), strict=False):
    sm1.points = np.array(sm2.points)
```

Copia **só a geometria**, mantém o estilo, e usa `strict=False` — famílias de
tamanhos diferentes não levantam: o excedente é **ignorado em silêncio**. É a
ferramenta certa para "assuma a forma daquilo, mantendo a minha cor"; é a
ferramenta errada quando as estruturas não batem, porque o defeito não aparece.

---

## 8. Alinhamento — por que duas formas não casam

Quando `Transform` ou `become` precisam interpolar A → B, os dois têm de ter a
mesma **estrutura de família** e a mesma **contagem de pontos**. Quem faz isso
é `align_data`, e o que ele faz explica quase todo "o Transform deformou".

### 8.1 A cascata

[FONTE] `mobject.py:3018-3025`:

```python
def align_data(self, mobject, skip_point_alignment=False):
    self.null_point_align(mobject)
    self.align_submobjects(mobject)
    if not skip_point_alignment:
        self.align_points(mobject)
    for m1, m2 in zip(self.submobjects, mobject.submobjects, strict=True):
        m1.align_data(m2)
    return self
```

Os três passos, todos [FONTE] no mesmo arquivo:

1. **`null_point_align`** (`:3055-3070`) — se um tem pontos próprios e o outro
   não, o que tem pontos é **empurrado para dentro dos próprios submobjects**
   (`push_self_into_submobjects`: copia a si mesmo, zera os próprios pontos e
   adiciona a cópia como filho). Uma `Circle` transformada num `VGroup` deixa de
   ser uma `Circle` com pontos e vira um contêiner com uma `Circle` dentro.
2. **`align_submobjects`** (`:3045-3053`) — chama
   `mob1.add_n_more_submobjects(max(0, n2-n1))` **e**
   `mob2.add_n_more_submobjects(max(0, n1-n2))`. **Os dois lados são mutados.**
3. **`align_points`** (`:3034-3041`) — quem tiver menos pontos chama
   `align_points_with_larger`. No `VMobject` (`:1820+`) isso subdivide as curvas
   e, quando a contagem de subcaminhos difere, **cria subcaminhos novos feitos de
   um ponto repetido**.

### 8.2 O que `add_n_more_submobjects` acrescenta

[FONTE] `mobject.py:3079-3099`:

```python
if curr == 0:
    self.submobjects = [self.get_point_mobject() for k in range(n)]
    return None
...
new_submobs.extend(submob.copy().fade(1) for _ in range(1, sf))
```

Ou seja: **cópias desbotadas** (`fade(1)`, opacidade zero) dos submobjects que já
existem, ou — se não havia nenhum — `VectorizedPoint`s.

E aqui a ponta se encontra com uma lição cara do deck: **elemento invisível
continua na caixa delimitadora**. [FONTE] `VectorizedPoint` sobrescreve os
*getters* de `width` e `height` para devolver `artificial_width` e
`artificial_height`, ambos **0.01** (`vectorized_mobject.py:2748-2782`). [DECK]
um detalhe transparente deslocou um `VGroup.move_to()` em **4 px medidos, em
silêncio**. Um `Transform` entre grupos de tamanhos diferentes deixa o menor com
membros invisíveis — e é por isso que a regra do deck é **posicionar pelo corpo
visível, nunca pelo grupo**.

### 8.3 Os tampões que a sua classe herda se não for `VMobject`

[FONTE] `mobject.py:3028-3033` e `:3043`:

```python
def get_point_mobject(self, center=None):
    raise NotImplementedError(f"get_point_mobject not implemented for {self.__class__.__name__}")
def align_points_with_larger(self, larger_mobject):
    raise NotImplementedError("Please override in a child class.")
```

**Correção, e ela piora o aviso em vez de aliviá-lo.** Uma versão anterior
dizia que "`VMobject` implementa os dois". Não implementa — só um
[FONTE] `api/manim-ce-methods.tsv`, coluna `inherited`:

| Classe | `get_point_mobject` | `align_points_with_larger` |
|---|---|---|
| `VMobject` | **próprio** (devolve `VectorizedPoint` com `match_style(self)`) | **herdado de `Mobject`** — ou seja, ainda é o tampão |
| `PMobject` | próprio (devolve `Point`) | **próprio** |

Consequência: **herdar de `VMobject` não te protege dos dois.** Uma subclasse de
`VMobject` ainda pode estourar
`NotImplementedError: Please override in a child class.` — e a mensagem não diz
qual método era, porque o texto é genérico. Se o traceback trouxer essa frase
exata, o método é `align_points_with_larger`; se trouxer
`get_point_mobject not implemented for <SuaClasse>`, é o outro, e aí você
herdou de `Mobject` puro.

Em qualquer dos casos o estouro acontece **na primeira vez que alguém
transformar** o objeto — não na construção.

### 8.4 `Transform` muta a FONTE; `become` muta os dois

[FONTE] `animation/transform.py:200-212`, com o comentário do próprio upstream:

```python
def begin(self):
    self.target_mobject = self.create_target()
    self.target_copy = self.target_mobject.copy()
    # Note, this potentially changes the structure
    # of both mobject and target_mobject
    self.mobject.align_data(self.target_copy)
    super().begin()
```

O alvo é protegido por uma **cópia**; a fonte, não. Depois de
`self.play(Transform(a, b))`, `a` pode ter submobjects nulos a mais — e `b`
está intacto. Em `a.become(b)` sem kwargs, os dois mudam. Esta assimetria é a
resposta para "por que o mesmo objeto se comporta diferente na segunda vez que
eu transformo".

### 8.5 O que a interpolação NÃO leva

[FONTE] `mobject.py:3104-3113`, `Mobject.interpolate` interpola **pontos e cor**,
e nada mais. Se a sua classe guarda estado próprio (um valor, um rótulo, um
índice), esse estado **não** viaja num `Transform`: a forma vira a outra e o
atributo continua o antigo. As saídas são `become` (que copia a família inteira,
mas também não copia atributos seus), um `UpdateFromAlphaFunc`
(**`manim-updaters-valuetracker`**) ou uma `Animation` própria (§11).

---

## 9. Combinar formas — as quatro rotas, e quando cada uma

| Rota | O que produz | Escolha quando |
|---|---|---|
| **`VGroup(a, b)`** | dois mobjects que se movem juntos | quase sempre. As peças continuam alcançáveis e animáveis separadamente |
| **Subcaminhos no mesmo `VMobject`** (`start_new_path`) | **um** mobject, um `points` só, vários laços | você precisa de UM preenchimento contínuo, ou de um furo par-ímpar (§4.4), ou quer que `Create` desenhe tudo como um traço só |
| **Booleano** (`Union`, `Intersection`, `Difference`, `Exclusion`) | um `VMobject` novo com a geometria REAL do resultado | a forma resultante é o objetivo (uma placa furada, uma lente, um recorte), e ela não vai mudar depois |
| **`Cutout(main, *furos)`** | um `VMobject` que **parece** recortado | atalho barato; leia as três armadilhas em **`manim-mobjects §8.2`** antes — ele muta os argumentos e usa só `.points` do nó |

**A pergunta que decide entre a 1ª e as outras:** *alguma peça precisa se mexer
sozinha depois?* Se sim, é grupo. Booleano e subcaminho fundem a geometria e não
há volta.

---

## 10. Os booleanos por dentro

`manim-mobjects §8.6` é dona do uso (as assinaturas, o `ValueError` de um
argumento só, "o resultado é novo e os operandos continuam na cena"). Esta seção
é o mecanismo — e ele explica falhas que o uso não prevê.

### 10.1 Quem faz a conta

[FONTE] `mobject/geometry/boolean_ops.py:1-20`: `from pathops import Path as
SkiaPath, PathVerb, difference, intersection, union, xor`. É o **skia-pathops**,
a mesma engine de caminho do Skia. [HOJE] `skia_pathops-0.9.2.dist-info` está
presente no `.venv` — não é dependência opcional aqui.

Assinaturas [FONTE]:

```python
Union(*vmobjects: VMobject, **kwargs)          # < 2 -> ValueError("At least 2 mobjects needed for Union.")
Intersection(*vmobjects: VMobject, **kwargs)   # < 2 -> ValueError(... for Intersection.)
Difference(subject: VMobject, clip: VMobject, **kwargs)
Exclusion(subject: VMobject, clip: VMobject, **kwargs)   # XOR
```

Todos herdam de `_BooleanOps(VMobject, metaclass=ConvertToOpenGL)` e, no
`__init__`, convertem cada operando com `_convert_vmobject_to_skia_path`,
chamam a função do pathops e reconstroem o resultado dentro de `self` com
`_convert_skia_path_to_vmobject`.

### 10.2 A armadilha que apaga metade dos seus operandos

[FONTE] `boolean_ops.py:62-107`, `_convert_vmobject_to_skia_path(vmobject)` lê
**`vmobject.points`** — os pontos PRÓPRIOS do nó — e nada mais. Ele **não
percorre submobjects**.

> Todo mobject cuja geometria mora em filhos contribui com um caminho **vazio**:
> `Text` (os glifos são submobjects), `Tex`/`MathTex`, `VGroup`, `Brace` com
> rótulo, `Rectangle(grid_xstep=…)` (a grade é filho), qualquer coisa que a sua
> fábrica de §1 devolveu.

`Union(texto, circulo)` devolve, na prática, o círculo — sem erro, sem aviso. É
a mesma raiz da armadilha já documentada em `Cutout`, mas ela vale para os
**quatro** booleanos e quase ninguém a testa antes.

A saída: opere sobre nós com pontos próprios. Para um `VGroup` de formas, faça
`reduce(Union, grupo.submobjects)` — [NÃO VERIFICADO por execução; a assinatura
`Union(*vmobjects)` suporta a chamada]. Para texto, não há saída simples: os
glifos são submobjects e cada um teria de ser tratado individualmente.

### 10.3 Mais cinco fatos do fonte

- **É 2D, sempre.** `_convert_2d_to_3d_array(points, z_dim=0.0)` na volta: tudo
  achata em `z=0`. Uma forma deslocada em z volta ao plano.
- **A conta é feita uma vez, na construção.** Não é vínculo: mover um operando
  depois não atualiza o resultado. Para união viva, `always_redraw`
  (**`manim-updaters-valuetracker`**) reconstruindo o booleano — caro, por
  frame.
- **O resultado tem mais curvas que os operandos.** `PathVerb.CLOSE` vira
  `add_line_to(current_path_start)` [FONTE] `:141-142`, e o pathops fatia os
  contornos nos cruzamentos. Um `Transform` de/para um booleano interpola contra
  essa contagem, então a forma "explode" mais que o esperado (§8).
- **A conversão depende do renderer no momento da construção.** [FONTE] `:84-107`
  ramifica em `config.renderer`: cúbicas no cairo, quadráticas no OpenGL.
  Trocar de renderer troca o caminho gerado.
- **A docstring do `Union` está errada no upstream.** [FONTE] `:150-151`:
  *"Union of two or more VMobject s. This returns the common region of the
  VMobject s"* — "common region" descreve a **interseção**. `mx show Union`
  mostra esse texto. Confie na função do pathops (`union`), não na frase.

### 10.4 `ConvexHull` e `QuickHull`

```python
ConvexHull(*points: Point3DLike, tolerance: float = 1e-5, **kwargs)   # mobject/geometry
QuickHull(tolerance: float = 1e-5)                                    # utils/other
QuickHull.build(points) · initialize(points) · classify(facet) · compute_horizon(eye, start_facet)
```

[FONTE] `polygram.py`, o `__init__` de `ConvexHull` abre com
`array = np.array(points)[:, :2]`, roda `QuickHull(tolerance).build(array)`,
caminha pelos `subfacets` para pôr os vértices em ordem e monta um `Polygram`.

Duas armadilhas:

- **`ConvexHull` recebe pontos SOLTOS, não uma lista.** `ConvexHull(*pontos)`
  está certo; `ConvexHull(pontos)` produz `np.array` de forma `(1, N, 3)`, o
  `[:, :2]` fatia o eixo errado e o resultado é lixo — **[NÃO VERIFICADO por
  execução]**, mas é o que a expressão faz.
- **Ele é 2D** (`[:, :2]`). Para 3D existe `ConvexHull3D(*points, tolerance=1e-5)`,
  que é de **`manim-3d-camera`**.

`QuickHull` é utilizável direto quando você quer só os vértices do casco, sem
mobject nenhum: `h = QuickHull(); h.build(array_Nx2)` e depois `h.facets` /
`h.removed` / `h.neighbors`. É o que o `ConvexHull` faz. [NÃO VERIFICADO por
execução.]

---

## 11. Escrever uma `Animation` própria

O ciclo de vida completo (os sete ganchos, quem chama quem, quando o
`starting_mobject` nasce) é de **`manim-animations §2`** — não repito aqui. Esta
seção é a outra metade: **o que você implementa**.

### 11.1 O contrato mínimo

```python
class Preencher(Animation):
    """Anima o fill_opacity de 0 até o valor final. [NÃO EXECUTADO]"""

    def __init__(self, mobject, opacidade_final: float = 1.0, **kwargs):
        self.opacidade_final = opacidade_final
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        t = self.rate_func(alpha)
        self.mobject.set_fill(opacity=t * self.opacidade_final)
```

[FONTE] `animation/animation.py:339-352` — o `interpolate_mobject` padrão faz o
laço por família e delega a `interpolate_submobject`; sobrescrevendo-o você fica
com o mobject inteiro na mão e **o `rate_func` passa a ser sua
responsabilidade** (o padrão o aplica dentro de `get_sub_alpha`, `:364-391`).

### 11.2 A rota por submobject

```python
def interpolate_submobject(self, submobject, starting_submobject, alpha) -> None:
    ...
```

[FONTE] `:349-352` — o `interpolate_mobject` padrão monta
`list(self.get_all_families_zipped())`, e para cada tupla chama
`interpolate_submobject(*mobs, sub_alpha)` com o `sub_alpha` já passado pelo
`rate_func` e deslocado pelo `lag_ratio`. **Esta é a rota que ganha de graça
`lag_ratio` e `rate_func`.**

Dois detalhes do zip [FONTE] `:279-287`:

- no cairo ele usa **`family_members_with_points()`** — contêineres sem pontos
  próprios **não** aparecem em `interpolate_submobject`;
- o zip é `strict=False`: famílias de tamanhos diferentes **não** levantam, o
  excedente é ignorado. Sua animação silenciosamente deixa de animar parte do
  objeto.

### 11.3 Trazer mais mobjects para a conta

[FONTE] `:267-287`. `get_all_mobjects()` devolve, por padrão,
`(self.mobject, self.starting_mobject)`, e **a ordem tem de bater com a
assinatura de `interpolate_submobject`** — a docstring diz isso literalmente
(*"Ordering must match the ordering of arguments to interpolate_submobject"*).
`Transform` é o exemplo canônico: sobrescreve `get_all_mobjects` para quatro
elementos, `get_all_families_zipped` para três, e
`interpolate_submobject(self, submobject, starting_submobject, target_copy, alpha)`
com um argumento a mais [FONTE] `transform.py:224-250`.

### 11.4 Os outros ganchos que você pode querer

| Gancho | Assinatura [FONTE] | Escreva quando |
|---|---|---|
| `begin()` | `() -> None` | precisa preparar/copiar. O padrão faz `starting_mobject = create_starting_mobject()`, suspende updaters e chama `interpolate(0)` — **chame `super().begin()`** |
| `create_starting_mobject()` | `() -> Mobject` | o "estado inicial" não é `self.mobject.copy()` |
| `finish()` | `() -> None` | precisa de estado final exato. O padrão é `interpolate(1)` + `resume_updating()` |
| `clean_up_from_scene(scene)` | `(Scene) -> None` | precisa mexer na cena no fim (é onde `ReplacementTransform` faz `scene.replace`) |
| `is_remover()` / `is_introducer()` | `() -> bool` | normalmente basta `remover=True` / `introducer=True` no `__init__` |
| `update_mobjects(dt)` | `(float) -> None` | raro |

Os dois flags do construtor decidem a cena: [FONTE] `_setup_scene` faz
`scene.add(mobject)` se `is_introducer()`, e `clean_up_from_scene` faz
`scene.remove(mobject)` se `is_remover()`. Uma animação que "aparece do nada"
sem `introducer=True` obriga o autor da cena a lembrar do `self.add`.

### 11.5 Quando NÃO escrever uma `Animation`

Quase sempre. As alternativas mais baratas, em ordem:

1. **`.animate`** — para aplicar métodos. `manim-animations §6`.
2. **`UpdateFromAlphaFunc(mob, func)`** — uma função `(mob, alpha)` por frame,
   sem classe nenhuma. **`manim-updaters-valuetracker`**.
3. **`AnimationGroup`/`Succession`/`LaggedStart`** — se o que você quer é
   coreografia, não movimento novo. **`manim-composicao-ritmo`**.
4. **`rate_func` próprio** — se o que muda é o *tempo*, não o *quê*. Uma
   `rate_func` é `Callable[[float], float]`, cinco linhas, e não herda nada.

Escrever uma `Animation` só se paga quando o movimento é **novo** (nenhuma
interpolação de pontos/cor produz aquilo) **e** vai ser reusado.

---

## 12. Fazer a sua classe conversar com as animações prontas

### 12.1 `override_animate` — trocar o que `.animate.metodo()` faz

[FONTE] `mobject.py:3495-3555`. O decorador guarda a função de animação no
atributo `_override_animate` do método original; `_AnimationBuilder.__getattr__`
(`:3439-3446`) verifica `hasattr(method, "_override_animate")`.

```python
class CircleWithContent(VGroup):
    ...
    def clear_content(self):
        self.remove(self.content)
        self.content = None

    @override_animate(clear_content)
    def _clear_content_animation(self, anim_args=None):
        if anim_args is None:
            anim_args = {}
        anim = Uncreate(self.content, **anim_args)
        self.clear_content()
        return anim
```

*(Exemplo copiado da docstring do fonte [FONTE] `mobject.py:3519-3537`; não
executado aqui.)* Três regras:

- o decorador recebe **a função original**, não uma string;
- a função de animação **executa o efeito** (`self.clear_content()`) e devolve a
  `Animation`. Ela não é um envelope: é o dono do efeito;
- **encadeamento passa a ser proibido.** [FONTE] `:3443-3446` levanta
  `NotImplementedError: Method chaining is currently not supported for
  overridden animations`. Na biblioteca isso existe em `Graph.add_vertices`,
  `remove_vertices`, `add_edges`, `remove_edges`.

### 12.2 `override_animation` — trocar uma classe de animação inteira

```python
override_animation(animation_class: type[Animation]) -> Callable[[Callable], Callable]
```

[FONTE] `animation/animation.py:725-766`:

```python
class MinhaCaixa(VGroup):
    @override_animation(FadeIn)
    def _fade_in_override(self, **kwargs):
        return Create(self, **kwargs)
```

O mecanismo é o `__new__`, não o `__init__`. [FONTE] `animation.py:109-126`:

```python
def __new__(cls, mobject=None, *args, use_override=True, **kwargs):
    if isinstance(mobject, Mobject) and use_override:
        func = mobject.animation_override_for(cls)
        if func is not None:
            anim = func(mobject, *args, **kwargs)
            return anim
    return super().__new__(cls)
```

Quatro consequências que ninguém adivinha:

1. **`FadeIn(minha)` pode não ser um `FadeIn`.** O construtor devolve outro
   objeto. `isinstance(anim, FadeIn)` é `False`.
2. **A correspondência é por classe EXATA.** [FONTE] `animation_override_for`
   (`mobject.py:187-207`) é `if animation_class in cls.animation_overrides`.
   Sobrescrever `Transform` não pega `ReplacementTransform`; sobrescrever
   `Create` não pega `Uncreate`. A docstring diz: *"They don't override
   subclasses of the Animation they override."*
3. **`use_override=False` desliga**, e serve para chamar o comportamento
   original de dentro do seu override sem recursão infinita.
4. **[PYTHON]** se o seu override devolver uma instância **da mesma classe** que
   está sendo sobrescrita, o `type.__call__` chama `__init__` de novo sobre ela.
   Devolva sempre uma classe diferente. [NÃO VERIFICADO por execução.]

### 12.3 O registro por subclasse, e o `MultiAnimationOverrideException`

[FONTE] `mobject.py:99-105` e `:209-255`. Em **toda** subclasse de `Mobject`,
`__init_subclass__` faz `cls.animation_overrides = {}` e depois
`_add_intrinsic_animation_overrides()`, que varre `dir(cls)` inteiro (pulando
dunders) atrás de `method._override_animation` e chama `add_animation_override`.

Como `dir(cls)` **inclui os métodos herdados**, um override definido na classe
mãe é re-registrado na filha — é assim que ele "se herda". E é também como se
produz a exceção:

```
MultiAnimationOverrideException: The animation FadeIn for MinhaFilha is
overridden by more than one method: Mae._fade_in_override and Filha._outro.
```

[FONTE] `:249-255`. Se você sobrescrever a mesma `Animation` na mãe e na filha
com **nomes de método diferentes**, os dois aparecem em `dir(cls)` e a classe
**falha na definição** — o erro acontece no `import`, não no uso. A correção é
usar o **mesmo nome de método** na filha (aí ele substitui, não duplica).

---

## 13. Detalhes do fonte que mordem quem escreve classe

### 13.1 `VMobject.apply_function` DESCARTA `about_point` e `about_edge`

[FONTE] `vectorized_mobject.py:1218-1231`:

```python
def apply_function(self, function, *, about_point=None, about_edge=None) -> Self:
    factor = self.pre_function_handle_to_anchor_scale_factor
    self.scale_handle_to_anchor_distances(factor)
    super().apply_function(function)          # <— about_point/about_edge NÃO são repassados
    self.scale_handle_to_anchor_distances(1.0 / factor)
    if self.make_smooth_after_applying_functions:
        self.make_smooth()
    return self
```

Os dois parâmetros são aceitos e **jogados fora**; a base
(`mobject.py:1458-1468`) então assume `about_point = ORIGIN`. Ou seja:
`forma.apply_function(f, about_point=forma.get_center())` mapeia **em torno da
origem do palco**, e a forma sai de lugar. Sem erro, sem aviso.

A saída é mover, aplicar e voltar:

```python
c = forma.get_center()
forma.shift(-c).apply_function(f).shift(c)
```

O `factor = pre_function_handle_to_anchor_scale_factor` (default **0.01**,
[FONTE] `VMobject.__init__`) é o truque que mantém a curva parecida com ela mesma
sob uma função não linear: as alças são puxadas para 1% da distância antes de
mapear e devolvidas depois. `make_smooth_after_applying_functions` nasce
`False`.

### 13.2 O metaclass `ConvertToOpenGL`

[FONTE] `mobject/opengl/opengl_compatibility.py` inteiro. O metaclass troca as
**bases** na criação da classe quando `config.renderer == OPENGL`, e a troca é
por **nome literal da base**: só `Mobject`, `VMobject`, `PMobject`, `Mobject1D`,
`Mobject2D` e `Surface` estão no mapa.

Fatos que decorrem disso, todos [HOJE] conferidos nas declarações:

- **`class Mobject:` e `class VMobject(Mobject):` NÃO declaram o metaclass.** Quem
  declara é `VGroup`, `VDict`, `VectorizedPoint`, `DashedVMobject`, `PMobject`,
  `Mobject1D`, `Mobject2D`, `_BooleanOps`, `TipableVMobject` e companhia.
- Logo, `class Minha(VMobject):` — sem mais nada — **não** é convertida sob
  `--renderer opengl`. Para paridade, espelhe a biblioteca:
  `class Minha(VMobject, metaclass=ConvertToOpenGL):`.
- `class Minha(VGroup):` herda o metaclass automaticamente [PYTHON], mas a
  substituição de base não acontece (a base se chama `VGroup`, que não está no
  mapa) — e não precisa: o próprio `VGroup` já foi convertido no import.
- No fluxo de aula deste projeto o renderer é o **cairo**, e os 45 mobjects
  `OpenGL*` são um **buraco declarado de propósito** (§16). Se você não vai rodar
  em OpenGL, ignore o metaclass — mas saiba por que ele está lá quando o ler.

### 13.3 Homônimos que o `mx show` escolhe em silêncio

[HOJE, índice] Três nomes desta matéria existem em mais de um lugar:

| Nome | Onde |
|---|---|
| `interpolate` | função `utils/bezier` · método `Mobject.interpolate` · método `Animation.interpolate` |
| `is_closed` | função `utils/bezier.is_closed(points)` · método `VMobject.is_closed()` |
| `Polygon` | classe `mobject/geometry.polygram` · classe em `utils/other` (o `polylabel`) |

`mx show interpolate` resolve por pontuação e mostra **um**. A armadilha é
documentada em **`manim-api-discovery §3`**; a defesa é filtrar o índice por
categoria:

```bash
awk -F'\t' '$2=="interpolate" {print $1"\t"$3"\t"$4}' api/manim-ce-index.tsv
```

---

## 14. A matemática: `utils/bezier` e `utils/space_ops`

Nenhuma das duas tem skill dona além desta. As assinaturas abaixo saíram
integralmente do índice [HOJE].

### 14.1 `utils/bezier` — 17 funções

```python
bezier(points) -> Callable[[float | ColVector], Point3D_Array]
interpolate(start, end, alpha)                     # o interpolador linear de tudo
inverse_interpolate(start, end, value)             # o inverso: "que alpha dá esse valor?"
match_interpolate(new_start, new_end, old_start, old_end, old_value)   # remapear faixa
mid(start, end)
integer_interpolate(start, end, alpha) -> tuple[int, float]
split_bezier(points, t) -> Spline                  # corta UMA curva em duas
subdivide_bezier(points, n_divisions) -> Spline    # corta em n
partial_bezier_points(points, a, b) -> BezierPoints # o pedaço [a,b] de uma curva
bezier_remap(bezier_tuples, new_number_of_curves) -> BezierPoints_Array
point_lies_on_bezier(point, control_points, round_to=1e-6) -> bool
proportions_along_bezier_curve_for_point(point, control_points, round_to=1e-6) -> MatrixMN
is_closed(points) -> bool
get_smooth_cubic_bezier_handle_points(anchors) -> tuple[Point3D_Array, Point3D_Array]
get_smooth_open_cubic_bezier_handle_points(anchors) -> tuple[...]
get_smooth_closed_cubic_bezier_handle_points(anchors) -> tuple[...]
get_quadratic_approximation_of_cubic(a0, h0, h1, a1) -> QuadraticSpline | QuadraticBezierPath
```

As três que você realmente vai usar:

- **`interpolate(a, b, alpha)`** — funciona com escalares e com arrays de pontos.
  É o que `set_points_as_corners` usa para pôr as alças em cima da reta.
- **`get_smooth_cubic_bezier_handle_points(anchors)`** — dá as duas listas de
  alças que fazem uma curva suave passar pelas âncoras. É o miolo do
  `make_smooth`. Use quando quiser as alças **sem** deixar o `change_anchor_mode`
  destruir o resto (§4.6).
- **`partial_bezier_points(points, a, b)`** — o pedaço de uma curva. É a peça de
  `pointwise_become_partial` e de `get_subcurve`.

### 14.2 `utils/space_ops` — 36 funções

Agrupadas pelo que resolvem:

```python
# vetores no plano
normalize(vect, fall_back=None)          normalize_along_axis(array, axis)
angle_of_vector(vector)                  angle_between_vectors(v1, v2)
rotate_vector(vector, angle, axis=OUT)   rotation_about_z(angle)
cross(v1, v2)                            cross2d(a, b)
get_unit_normal(v1, v2, tol=1e-6)        norm_squared(v)
midpoint(point1, point2)                 center_of_mass(points)

# geometria de interseção — o que economiza trigonometria à mão
line_intersection(line1, line2)          # duas retas dadas por 2 pontos cada
find_intersection(p0s, v0s, p1s, v1s, threshold=1e-5) -> list[Point3D]
perpendicular_bisector(line, norm_vector=OUT)

# polígonos
regular_vertices(n, *, radius=1, start_angle=None) -> tuple[np.ndarray, float]
compass_directions(n=4, start_vect=RIGHT)
shoelace(x_y) -> float                   # área com sinal
shoelace_direction(x_y) -> str           # "CW" ou "CCW"
get_winding_number(points) -> float
earclip_triangulation(verts, ring_ends) -> list
thick_diagonal(dim, thickness=2)

# 3D e rotação
rotation_matrix(angle, axis, homogeneous=False)
rotation_matrix_transpose(angle, axis)
z_to_vector(vector)
cartesian_to_spherical(vec)              spherical_to_cartesian(spherical)
quaternion_from_angle_axis(angle, axis, axis_normalized=False)
quaternion_mult(*quats)                  quaternion_conjugate(quaternion)
angle_axis_from_quaternion(quaternion)
rotation_matrix_from_quaternion(quat)    rotation_matrix_transpose_from_quaternion(quat)

# complexos
complex_to_R3(complex_num)               R3_to_complex(point)
complex_func_to_R3_func(complex_func)
```

As quatro que aparecem em código de aula de verdade:

- **`rotate_vector(v, angle)`** — girar um deslocamento sem girar o mobject.
  É como se posiciona coisa em torno de um centro sem `Rotate`.
- **`line_intersection(l1, l2)`** — onde dois fios se cruzam, para pôr um ponto
  ali. Sem isso vira trigonometria à mão dentro do `construct`.
- **`regular_vertices(n, radius=…, start_angle=…)`** — os vértices de um polígono
  regular, prontos para `set_points_as_corners`. Devolve `(vértices, ângulo)`.
- **`shoelace_direction(x_y)`** — descobrir o sentido de um contorno antes de
  usá-lo como furo (§4.7).

**Cuidado com o alcance de `normalize`:** `fall_back` existe justamente porque
normalizar o vetor nulo é indefinido; sem ele o resultado é `nan` que se propaga
silenciosamente pela geometria inteira. [NÃO VERIFICADO por execução.]

---

## 15. Conferir uma classe nova sem renderizar

Renderizar custa; boa parte do que quebra numa classe nova é visível antes.

```python
# 1. desenha alguma coisa?
m.has_points()               # -> bool  (o nó ele mesmo)
len(m.submobjects)
len(m.family_members_with_points())

# 2. a geometria fechou?
m.get_num_curves()           # 0 = você construiu um mobject vazio
len(m.points) % 4            # 1 = caminho aberto pendente (has_new_path_started)
m.is_closed()                # ressalva de §4.4
len(m.get_subpaths())

# 3. cabe na tela?
m.is_off_screen()
m.get_corner(UR), m.get_corner(DL)      # x ∈ [-7,11; 7,11] · y ∈ [-4; 4]
m.width, m.height

# 4. o índice de um submobject
self.add(index_labels(m))    # DESENHA os índices por cima
```

[FONTE] `index_labels(mobject, label_height=0.15, background_stroke_width=5,
background_stroke_color=BLACK, **kwargs) -> VGroup`, em `manim.utils.debug`.

Duas conferências específicas de classe própria:

```bash
# a sua classe está sendo listada como CENA por engano?
bin/mx scenes arquivo.py --json

# um método que você acha que existe: existe mesmo, e em qual classe?
awk -F'\t' '$2=="set_points_as_corners" {print $1"\t"$4}' api/manim-ce-methods.tsv | sort -u
```

O segundo comando é a defesa contra a armadilha nº 1 de `manim-api-discovery`:
`Mobject.__getattr__` **sintetiza** qualquer `set_<coisa>` e emite só um
`DeprecationWarning` — `mob.set_pontos(...)` "funciona", grava um atributo e não
desenha nada. A metodologia inteira é de **`manim-api-discovery §13`**.

O ciclo com render (escrever → render rápido → **OLHAR o PNG** → corrigir →
render final) é de **`manim-verificacao-visual`**. Nada nesta seção substitui
olhar a imagem: [DECK] três defeitos reais de uma investigação só apareceram no
PNG, e **nenhum** deu erro no terminal.

---

## 16. Armadilhas, em uma lista

| Armadilha | Sintoma | Correção |
|---|---|---|
| atributo definido **depois** de `super().__init__()` | `AttributeError` vindo de dentro do `super()` | defina antes; `generate_points` roda lá (§2.2) |
| implementou só `init_points` | forma vazia, sem erro | o gancho do cairo é `generate_points` (§2.3) |
| `self.peca = …` sem `self.add(self.peca)` | grupo vazio no ORIGIN | `add` é o que põe na árvore (§3.1) |
| `add_line_to` num mobject novo | `IndexError: index -1 is out of bounds…` (não é `Exception`, §4.2) | `start_new_path(p0)` antes (§4.2) |
| `set_points_as_corners` com 1 ponto | zero curvas, invisível | precisa de ≥ 2 (§4.3) |
| `VMobject()` sem cor | some no fundo claro, sem erro | `set_stroke`/`set_fill` explícitos (§4.5) |
| `make_smooth()` depois de alças à mão | as alças somem | `change_anchor_mode` reescreve tudo (§4.6) |
| `.copy()` de mobject com updater | a cópia mexe no ORIGINAL | `clear_updaters()` na cópia (§7.2) |
| `a.become(b)` | `b` ganha submobjects nulos | `a.become(b.copy())` (§7.3) |
| `match_points` com famílias diferentes | metade não copia, sem erro | `strict=False` no zip (§7.4) |
| `Transform` entre grupos de tamanhos diferentes | o menor ganha membros invisíveis; `move_to` desloca | posicione pelo corpo visível (§8.2) [DECK: 4 px] |
| subclasse de `Mobject` puro no `Transform` | `NotImplementedError: Please override in a child class.` | herde de `VMobject` (§8.3) |
| `Create(minha_classe)` | `TypeError: Create only works for VMobjects.` | herde de `VMobject` ou implemente `pointwise_become_partial` (§6) |
| `Union`/`Difference` com `Text`/`VGroup` | resultado sem o operando, sem erro | só `.points` do nó entra (§10.2) |
| `ConvexHull(lista)` | forma errada, sem erro | `ConvexHull(*lista)` (§10.4) |
| booleano que "não acompanha" | a união fica parada | é calculada uma vez (§10.3) |
| `apply_function(f, about_point=…)` | a forma sai de lugar | os kwargs são descartados; `shift(-c)…shift(c)` (§13.1) |
| override da mesma `Animation` na mãe e na filha | `MultiAnimationOverrideException` **no import** | use o mesmo nome de método (§12.3) |
| `.animate.metodo().shift(...)` com override | `NotImplementedError: Method chaining…` | um builder por vez (§12.1) |
| `g + x` esperando mutação | o objeto some | `g += x` (§3.3) |

**A armadilha estrutural:** quinze dessas vinte não levantam exceção nenhuma.
Uma classe nova que "compila" não está pronta — ela está **não conferida**.

---

## 17. Onde esta skill para

| O assunto | A skill |
|---|---|
| escolher entre as formas que **já existem**, `VGroup` × `Group`, estilo, caixa delimitadora, `Brace`, `SurroundingRectangle`, `DashedVMobject`, o **uso** dos booleanos | **`manim-mobjects`** |
| posicionar, alinhar, `next_to`/`to_edge`, margem, "cabe na tela?", `z_index` | **`manim-layout-posicionamento`** |
| o catálogo de `Animation` pronta, `.animate`, `Transform` × `ReplacementTransform`, o ciclo de vida dos 7 ganchos | **`manim-animations`** |
| `rate_func`, `path_func`, `lag_ratio`, `AnimationGroup`, orçamento de tempo | **`manim-composicao-ritmo`** |
| `ValueTracker`, `add_updater`, `always_redraw`, `TracedPath` | **`manim-updaters-valuetracker`** |
| cor, contraste, "sumiu no fundo branco", `set_default` de cor, o `tema.py` | **`manim-color-theming`** / **`manim-tema-projeto`** |
| `Text`, `Tex`, `MathTex`, glifos, nitidez | **`manim-text-latex`** |
| `Axes`, `plot`, `BarChart` | **`manim-graphs-plots`** |
| `SVGMobject`, `ImageMobject`, `VMobjectFromSVGPath`, fonte | **`manim-svg-imagens`** |
| `Surface`, `Polyhedron`, `ConvexHull3D`, câmera 3D | **`manim-3d-camera`** |
| custo de rasterizar, número de curvas, cache | **`manim-performance-cache`** |
| olhar o PNG, pôster vazio, conferência visual | **`manim-verificacao-visual`** |
| descobrir se um nome/kwarg existe, homônimos, `__getattr__` sintetizado | **`manim-api-discovery`** |
| renderizar, qualidade, caminho da saída | **`manim-render-api`** |
| traceback, ambiente, LaTeX, codec | **`manim-troubleshooting`** |
| cena cortada em partes para slide | **`manim-presentation-parts`** |

**Buracos declarados — não invente skill que não existe.** Os 45 mobjects
`OpenGL*` de `mobject/opengl`, mais `Shader`, `ShaderWrapper`, `Mesh`,
`Object3D`, `Window` e `FullScreenQuad`, ficam **órfãos de propósito**: no fluxo
de aula o renderer é o cairo. `LinearTransformationScene`, `VectorScene` e
`ApplyMatrix` como assunto de álgebra linear não têm dona. `VectorField`,
`ArrowVectorField`, `StreamLines`, `Homotopy` e `PhaseFlow` não têm dona.
`Flash`, `Indicate`, `Circumscribe` e o resto da ênfase animada não têm dona —
o catálogo cru está em `manim-animations`.
