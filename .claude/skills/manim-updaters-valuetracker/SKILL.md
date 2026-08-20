---
name: manim-updaters-valuetracker
description: >-
  Animação REATIVA no Manim — o valor que mexe em tudo: `ValueTracker`,
  `add_updater`, `always_redraw`, a família `always`/`f_always`/`always_rotate`,
  `DecimalNumber`/`Integer`/`Variable` para número que conta na tela,
  `UpdateFromFunc`/`UpdateFromAlphaFunc`/`MaintainPositionRelativeTo`, e
  `TracedPath`/`AnimatedBoundary` (que são MOBJECTS, não animações). Use quando
  o pedido for "a etiqueta tem que seguir o ponto", "o número tem que contar",
  "a tangente corre pela curva", "a barra reflete o valor", "o gráfico se
  redesenha enquanto x muda", "deixa isso girando", "põe um rastro atrás",
  "a câmera segue o objeto", "quero animar um parâmetro e não uma posição" — e
  também quando o sintoma for "o updater não roda", "a etiqueta grudou e não
  para", "o objeto voltou para o lugar quando a animação acabou", "o `wait` não
  anima nada", "a cena com `always_redraw` demora 10× mais", "a parte pulada do
  vídeo saiu diferente", ou "`TypeError: <lambda>() missing 1 required
  positional argument: 'dt'`". Cobre o laço de frame real (lido no fonte), a
  ordem animação→updater de mobject→updater de cena, a regra do parâmetro
  chamado `dt`, o `suspend_mobject_updating=True` que faz a animação VENCER o
  updater, o frame estático do `wait`, e o `dt` gigante das seções puladas. NÃO
  use para escolher a classe de animação ou `Transform` × `ReplacementTransform`
  (`manim-animations`), para `rate_func`/`path_func`/`lag_ratio`
  (`manim-composicao-ritmo`), para o corte em partes de um vídeo de slide
  (`manim-presentation-parts`), para mover a CÂMERA (`manim-camera-2d`,
  `manim-3d-camera`), nem para eixos, `plot` e `get_secant_slope_group`
  (`manim-graphs-plots`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Updaters e ValueTracker — a animação que depende de um valor

Animação normal interpola de A para B, os dois conhecidos antes de começar.
Updater é para quando **B não existe até o frame acontecer**: a etiqueta que
segue um ponto que outra animação está movendo, a reta tangente cujo ângulo é
função de x, o número que precisa mostrar o valor que o `ValueTracker` carrega
neste instante.

O preço é alto e quase todo mundo descobre tarde: updater desliga o cache de
frame estático, roda `inspect.signature` a cada frame, e **perde silenciosamente
para qualquer animação que toque o mesmo mobject**. Esta skill existe para você
pagar esse preço de propósito, e só quando compensa.

Tudo aqui foi conferido contra o ManimCE **0.21.0** instalado nesta máquina —
`api/manim-ce-index.tsv` para assinatura, e o fonte em
`.venv/lib/python3.12/site-packages/manim/` para mecanismo. Onde uma afirmação
veio de medição de outra skill, ela está citada com a fonte e a data. Onde não
foi verificada, está dito.

---

## 1. Antes de escrever um updater: pergunte se você precisa

### 1.1 A evidência que mais deveria te frear

O deck em produção que consome este projeto (`~/Projects/aulas`) tem **13
arquivos Python de cena e 59 partes de vídeo renderizadas**. Contagem feita no
disco em 2026-08-19:

```bash
grep -rc "add_updater\|always_redraw\|ValueTracker\|DecimalNumber" \
     ~/Projects/aulas/aulas/*/manim/*.py
# 13 arquivos, TODOS com 0 ocorrências
```

**Zero updaters. Zero ValueTracker.** Barra que cresce, número que aparece,
diagrama que se monta — tudo com `save_state()` + `stretch` + `Restore`,
`Transform`, `LaggedStart`. Isso não é ignorância do recurso: é a escolha certa
para vídeo de aula, onde cada parte termina num frame parado e o professor fala
por cima. Updater é ferramenta de vídeo **contínuo e paramétrico**, não de
slide.

### 1.2 A evidência de custo

Medido em `manim-gpu-encoding` (2026-08-19, `-q h`, cairo + NVENC, mesma
máquina), quatro cenas de `scenes/exemplos.py`:

| Cena | Tempo | O que faz |
|---|---:|---|
| `Pitagoras` | 2,69 s | `MathTex` + `TransformMatchingTex` |
| `Cascata` | 3,44 s | formas + `LaggedStart` |
| `OlaManim` | 3,65 s | texto + `Write` + `Create` |
| **`TangenteViva`** | **38,22 s** | `ValueTracker` + 3 × `always_redraw`, 4 s de play |

**~11× as outras no mesmo preset**, para 4,5 s de vídeo. Nenhum flag de GPU
conserta: o gargalo é rasterização por frame, não encode. Ver §13 para o que
fazer com isso.

### 1.3 A tabela de decisão

| Você quer | Use | Não use |
|---|---|---|
| um objeto vai de um lugar a outro | `self.play(mob.animate.shift(...))` | updater |
| uma barra cresce até um valor fixo | `save_state()` + `stretch` + `Restore` | `always_redraw` |
| um número aparece já no valor final | `Write(Text(f"{v}"))` | `DecimalNumber` + tracker |
| **um número CONTA na frente da plateia** | `DecimalNumber` + `add_updater` | `always_redraw(lambda: MathTex(...))` |
| **B é função de A, e A está animando** | `add_updater` em B | duas `.animate` em paralelo |
| **um parâmetro varre um intervalo** | `ValueTracker` + `always_redraw` | `Transform` de N estados |
| **movimento contínuo, sem alvo** (girar, deslizar) | `always_rotate` / `always_shift` | `Rotate` com `run_time` chutado |
| um rastro atrás de um ponto | `TracedPath` | `always_redraw` reconstruindo `VMobject` |
| a etiqueta acompanha durante UMA animação | `UpdateFromFunc` no mesmo `play` | updater permanente |

A pergunta que resolve 80% dos casos: **o valor final é conhecido agora?** Se
sim, é animação normal. Se ele depende do que outro objeto vai fazer, é updater.

---

## 2. O motor: como um updater roda de verdade

Sem isto, metade das armadilhas parece magia. Tudo abaixo foi lido no fonte.

### 2.1 A regra de alcance

`Scene.update_mobjects` (`scene/scene.py:383-393`):

```python
def update_mobjects(self, dt: float) -> None:
    for mobj in self.mobjects:
        mobj.update(dt)
```

e `Mobject.update(dt=0, recursive=True)` (`mobject/mobject.py:920-956`) desce
por `self.submobjects`. Logo:

> **Um updater roda se, e somente se, o mobject for alcançável a partir de
> `scene.mobjects` — diretamente ou como submobject de algo que está lá.**

Consequências imediatas:

- `always_redraw(...)` sem `self.add(...)` não roda. **É o erro nº 1.**
- `self.add(grupo)` já basta: o updater de um filho do grupo roda. Você **não**
  precisa adicionar o filho separadamente — e se adicionar, `Scene.add` chama
  `restructure_mobjects`, que **dissolve o grupo** dentro de `scene.mobjects`
  (`scene/scene.py:691-732`). Detalhe de estrutura: skill `manim-mobjects`.
- `FadeOut(mob)` é `remover=True` → `scene.remove(mob)`. Os updaters continuam
  **anexados** mas param de rodar. Ao readicionar, o primeiro `update` salta
  para onde o updater mandar, sem transição.
- `ValueTracker` só precisa estar na cena se **ele mesmo** tiver updater
  (§3.6). Quem lê o valor por closure lê de qualquer lugar.

### 2.2 A ordem dentro de um frame

`Scene.update_to_time` (`scene/scene.py:1700-1710`):

```python
def update_to_time(self, t):
    dt = t - self.last_t
    self.last_t = t
    for animation in self.animations:
        animation.update_mobjects(dt)      # 1. mobjects auxiliares da animação
        animation.interpolate(t / animation.run_time)   # 2. a animação escreve
    self.update_mobjects(dt)               # 3. updaters de MOBJECT
    self.update_meshes(dt)                 # 4. meshes (OpenGL)
    self.update_self(dt)                   # 5. updaters de CENA
```

Essa ordem é o contrato inteiro:

- **A animação escreve ANTES dos updaters.** Por isso
  `etiqueta.add_updater(lambda m: m.next_to(alvo, UP))` funciona enquanto
  `alvo` está sendo animado: quando o updater roda, `alvo` já está na posição
  deste frame.
- **Updater de cena roda por último**, depois de todos os de mobject. É onde
  cabe medição, log, ou uma decisão que dependa do estado já resolvido.
- Se dois updaters de mobjects diferentes dependem um do outro, quem ganha é a
  ordem de `scene.mobjects` — ou seja, a **ordem em que você chamou `add`**. Um
  ciclo A↔B fica sempre um frame atrasado de um dos lados.

### 2.3 A regra do `dt` — o nome do parâmetro é load-bearing

`Mobject.update` (`mobject/mobject.py:944-955`):

```python
if self.updating_suspended:
    return self
for updater in self.updaters:
    if "dt" in inspect.signature(updater).parameters:
        updater(self, dt)
    else:
        updater(self)
```

Três fatos que saem daí, e nenhum está na documentação:

1. **O parâmetro tem que se chamar literalmente `dt`.** Posição não conta.
   `lambda m, delta: ...` não é reconhecido como time-based, é chamado com **um**
   argumento, e você recebe
   `TypeError: <lambda>() missing 1 required positional argument: 'delta'`.
   `lambda m, dt=0: ...` funciona (o nome está lá).
2. **`inspect.signature` roda a cada updater, a cada frame.** No renderer cairo
   não há cache. Com muitos updaters isso entra na conta de §13. (O renderer
   OpenGL resolve isso de outro jeito — §14.)
3. `updating_suspended` faz o `update` inteiro virar no-op — é a chave de §10.

### 2.4 O que decide o que precisa ser redesenhado

`Scene.get_moving_mobjects` (`scene/scene.py:899-946`), só no renderer cairo:

```python
for i, mob in enumerate(mobjects):
    update_possibilities = [
        mob in animation_mobjects,
        len(mob.get_family_updaters()) > 0,
        mob in self.foreground_mobjects,
    ]
    if any(update_possibilities):
        return mobjects[i:]        # deste ponto em DIANTE, tudo é "movendo"
return []
```

Tudo que vem **antes** do primeiro mobject "movendo" é pintado uma vez num
frame estático (`save_static_frame_data`) e reaproveitado. Tudo que vem depois
é rasterizado a cada frame.

> **A ordem de `self.add` é performance.** Adicione o cenário parado PRIMEIRO e
> os mobjects com updater POR ÚLTIMO. Invertido, um único `always_redraw` no
> começo da lista faz um `NumberPlane` de 400 linhas ser rasterizado 60×/s.

---

## 3. `ValueTracker` — o número que a animação sabe interpolar

```python
class ValueTracker(Mobject, metaclass=ConvertToOpenGL)
ValueTracker(value: float = 0, **kwargs) -> None
```

Módulo `manim.mobject.value_tracker`; está no `from manim import *`.

### 3.1 O que ele é por dentro

```python
def __init__(self, value=0, **kwargs):
    super().__init__(**kwargs)
    self.set(points=np.zeros((1, 3)))
    self.set_value(value)

def get_value(self):      return self.points[0, 0]
def set_value(self, v):   self.points[0, 0] = v; return self
```

Um `Mobject` com **um ponto**, e o valor mora em `points[0, 0]`. É por isso que
ele é animável: `Transform` já sabe interpolar arrays de pontos. E é por isso
que ele não aparece na tela — o despachante do camera cairo tem
`Mobject: lambda batch, pa: batch,  # Do nothing` (`camera/camera.py:217-224`).
Um `Mobject` puro não é desenhado por nenhum caminho.

### 3.2 A API própria (5 métodos, conferidos no índice)

| Método | Assinatura | Nota |
|---|---|---|
| `get_value` | `(self) -> float` | lê |
| `set_value` | `(self, value: float) -> Self` | escreve, **instantâneo** |
| `increment_value` | `(self, d_value: float) -> Self` | soma, instantâneo |
| `interpolate` | `(self, mobject1, mobject2, alpha, path_func=straight_path()) -> Self` | sobrescrito: é o que faz `.animate` funcionar |
| `__init__` | `(self, value: float = 0, **kwargs) -> None` | |

Uso:

```python
t = ValueTracker(0)

t.get_value()                                   # lê
t.set_value(5)                                  # escreve AGORA, sem animar
t.increment_value(1)                            # soma AGORA
self.play(t.animate.set_value(10), run_time=3)  # 3 s indo de 5 para 10
```

### 3.3 `.animate` no tracker segue o `rate_func` — e o default não é linear

`Animation.__init__` tem `rate_func=smooth` (`animation/animation.py:133`). Um
`t.animate.set_value(10)` acelera e desacelera. Para um parâmetro varrendo um
intervalo — tangente correndo, ângulo abrindo — isso quase sempre está errado:

```python
self.play(t.animate.set_value(2.5), run_time=5, rate_func=linear)
```

O catálogo das 49 curvas e quando usar cada uma é da skill
**`manim-composicao-ritmo`**.

### 3.4 Os operadores — açúcar instantâneo, com uma cilada

O `ValueTracker` define `+ - * / // % **` e as versões `+=` etc.
(`mobject/value_tracker.py:104-190`). As duas famílias **não são equivalentes**:

```python
t += 1.5        # __iadd__  → muta o MESMO objeto e devolve self
t = t + 1.5     # __add__   → devolve um ValueTracker NOVO
```

Um `t = t + 1.5` troca o objeto por baixo: o novo tracker **não está na cena** e
**não carrega os updaters** que o antigo tinha. Se o antigo tinha
`t.add_updater(lambda m, dt: m.increment_value(dt))`, o relógio simplesmente
para, sem erro. Use sempre a forma composta (`+=`, `-=`, …) ou `set_value`.

Detalhe honesto: `t + Mobject` levanta `ValueError` com mensagem clara — esse
caso a biblioteca já protege.

### 3.5 `ComplexValueTracker`

```python
ComplexValueTracker(value: float = 0, **kwargs) -> None
get_value(self) -> complex
set_value(self, value: complex | float) -> Self
```

Guarda `(real, imag)` em `points[0, :2]`, o que permite o idioma do próprio
docstring da classe — ler os pontos como posição, sem conversão:

```python
tracker = ComplexValueTracker(-2 + 1j)
dot = Dot().add_updater(lambda m: m.move_to(tracker.points))
self.add(NumberPlane(), dot)
self.play(tracker.animate.set_value(3 + 2j))
```

`.animate` interpola em **linha reta** no plano complexo (é `straight_path`).
Para girar em arco, anime o ângulo num `ValueTracker` real e calcule o complexo
no updater.

### 3.6 Quando o tracker PRECISA entrar na cena

Se o tracker só é **lido** por closure, não precisa de `self.add`. Precisa em
dois casos:

```python
# (a) o tracker tem updater PRÓPRIO — um relógio
t.add_updater(lambda m, dt: m.increment_value(dt))
self.add(t)          # sem isto o updater dele nunca roda

# (b) você quer que ele conte como "time-based" para manter o `wait` vivo (§11)
```

`self.play(t.animate...)` adiciona o tracker à cena sozinho
(`Scene.add_mobjects_from_animations`, `scene/scene.py:535-545`) — ele fica lá
depois, e a partir daí updaters próprios dele passam a rodar.

---

## 4. `add_updater` e a gestão dos updaters

### 4.1 A assinatura completa

```python
Mobject.add_updater(update_function: _Updater,
                    index: int | None = None,
                    call_updater: bool = False) -> Self
```

- `index` — posição na lista. Os updaters rodam **na ordem da lista**;
  `index=0` põe o seu antes de todos os outros já anexados. Serve para o caso
  "primeiro reposiciono, depois recoloro".
- `call_updater` — chama uma vez **imediatamente**. Sem isso, o mobject fica no
  lugar em que nasceu até o primeiro frame renderizar. Se você posiciona por
  updater e adiciona o mobject num `play` que não é o primeiro, o frame de
  entrada mostra o objeto no lugar errado por 1/60 s — o suficiente para
  aparecer num pôster (§12).

```python
etiqueta = Text("aqui", color=TINTA)
etiqueta.add_updater(lambda m: m.next_to(alvo, UP, buff=0.2), call_updater=True)
self.add(etiqueta)
```

### 4.2 Os oito métodos de gestão (todos conferidos no índice)

| Método | Assinatura (cairo) | O que faz |
|---|---|---|
| `add_updater` | `(update_function, index=None, call_updater=False) -> Self` | anexa |
| `remove_updater` | `(update_function) -> Self` | remove **todas** as ocorrências daquela função |
| `clear_updaters` | `(recursive=True) -> Self` | esvazia — **e desce nos submobjects** |
| `get_updaters` | `() -> list[_Updater]` | a lista deste mobject |
| `get_family_updaters` | `() -> list[_Updater]` | os deste e de toda a descendência |
| `get_time_based_updaters` | `() -> list[_TimeBasedUpdater]` | só os que têm `dt` |
| `has_time_based_updater` | `() -> bool` | usado pelo `wait` (§11) |
| `match_updaters` | `(mobject) -> Self` | limpa os seus e copia os do outro |
| `suspend_updating` | `(recursive=True) -> Self` | liga `updating_suspended` |
| `resume_updating` | `(recursive=True) -> Self` | desliga **e chama `update(dt=0)`** |
| `update` | `(dt=0, recursive=True) -> Self` | dispara na mão |

Três leituras de fonte que mudam o uso:

- **`remove_updater` compara por igualdade de objeto** (`while f in self.updaters`).
  Uma `lambda` anônima não pode ser removida: guarde a referência, ou use
  `clear_updaters`.
- **`clear_updaters()` é recursivo por padrão.** Num `VGroup`, ele apaga também
  o updater que você pôs num filho. Quando quiser cirurgia, `recursive=False`.
- **`resume_updating` chama `self.update(dt=0)` no fim**
  (`mobject/mobject.py:1230-1233`). Isso é a causa do "o objeto voltou sozinho"
  de §10.

### 4.3 Com `dt`: movimento contínuo

```python
girando = Square(color=TINTA)
girando.add_updater(lambda m, dt: m.rotate(dt * PI))   # meia volta por segundo
self.add(girando)
self.wait(4)
girando.clear_updaters()
```

`dt` é o tempo desde o frame anterior. Sem ele, `lambda m: m.rotate(0.1)` gira
0,1 rad **por frame** — em `-q l` (15 fps) o quadrado dá 1/4 das voltas que dá
em `-q h` (60 fps). A animação muda de velocidade conforme a qualidade, e o
defeito só aparece no render final.

### 4.4 A cilada da variável de laço

```python
for i, ponto in enumerate(pontos):
    ponto.add_updater(lambda m: m.move_to(alvos[i]))      # ERRADO
    ponto.add_updater(lambda m, i=i: m.move_to(alvos[i])) # certo
```

O lambda captura a **variável**, não o valor: no primeiro frame todos os N
updaters leem o `i` final. Vale para qualquer closure, não só updater; aqui dói
mais porque o efeito só aparece em movimento.

---

## 5. `always_redraw` — reconstruir em vez de ajustar

### 5.1 O corpo real (`animation/updaters/mobject_update_utils.py:66-105`)

```python
def always_redraw(func: Callable[[], M]) -> M:
    mob = func()
    mob.add_updater(lambda _: mob.become(func()))
    return mob
```

Três coisas que a paráfrase comum (`f().add_updater(lambda m: m.become(f()))`)
erra, e que importam:

1. O updater captura `mob` **por closure**, não pelo parâmetro.
2. O parâmetro se chama `_`, não `dt` — portanto `always_redraw` **nunca** é
   time-based. É exatamente por isso que ele não segura um `wait` vivo (§11).
3. É `become`, então a **identidade do objeto é preservada**: referências
   antigas, `z_index`, pertencimento a grupos e outros updaters continuam
   valendo. É o que torna o padrão utilizável.

### 5.2 Uso

```python
x = ValueTracker(-2.5)

ponto = always_redraw(lambda: Dot(ax.i2gp(x.get_value(), f), color=ACENTO))
linha = always_redraw(lambda: ax.get_vertical_line(ponto.get_center()))

self.add(ax, f, ponto, linha)          # cenário primeiro, redraw por último (§2.4)
self.play(x.animate.set_value(2.5), run_time=5, rate_func=linear)
```

### 5.3 A armadilha estrutural: a família só CRESCE

`become` chama `align_data(mobject, skip_point_alignment=True)`
(`mobject/mobject.py:3308-3311`), que chama `align_submobjects`
(`:3047-3054`), que chama `add_n_more_submobjects` (`:3079-3099`) — e este
duplica submobjects existentes com `.fade(1)` até os dois lados terem a mesma
contagem.

O alinhamento é **simétrico e destrutivo só de um lado**: o mobject persistente
nunca encolhe. Se a sua função devolve um objeto com número **variável** de
submobjects — um `MathTex` cujo texto muda de comprimento, um `VGroup` cuja
lista varia —, a contagem de submobjects do objeto na cena vira o **máximo já
visto**, para sempre, e o excedente são cópias transparentes.

Duas consequências, ambas silenciosas:

- **custo por frame cresce** e não volta;
- **a caixa delimitadora inclui os invisíveis.** Um submobject transparente
  continua contando em `.width`, `.get_center()` e `VGroup.move_to()`. É o
  mesmo defeito de 4 px que o deck rastreou em `~/Projects/aulas` (elemento
  invisível deslocando o grupo). Posicione pelo corpo visível.

Defesa: faça a função devolver **sempre a mesma estrutura**. Para número que
muda de largura, `DecimalNumber` + `set_value` (§7) em vez de
`always_redraw(lambda: MathTex(...))`.

### 5.4 Quando NÃO usar `always_redraw`

- **Só a posição muda** → `add_updater(lambda m: m.move_to(...))`. Reconstruir
  um `Dot` 300 vezes para mudar 3 floats é desperdício puro.
- **Só o número muda** → `DecimalNumber` + `set_value`.
- **Nada além de você mexe naquilo** → então o valor final é conhecido: use
  animação normal.
- **A função constrói `Text`/`MathTex`/`Tex`** → o item mais caro que existe
  dentro de um `always_redraw`. **Mas o custo depende de a STRING mudar, e esta
  é uma correção:** a versão anterior desta linha dizia que "a compilação
  acontece uma vez e o parse do SVG acontece em todo frame". Os dois lados
  estão errados.

  | O que a lambda devolve | O que custa por frame |
  |---|---|
  | **string que MUDA** (`f"{t.get_value():.2f}"`) | **compilação de LaTeX inteira**: o `.tex` é nomeado pelo hash da EXPRESSÃO (`tex_file_writing.py:107`), string nova = arquivo novo = **miss** (`:61-63`) → `latex` + `dvisvgm`, **dois subprocessos por frame** |
  | **string CONSTANTE** | quase nada: `SVG_HASH_TO_MOB_MAP` (`svg_mobject.py:29, 171-179`) devolve um `.copy()` do mobject já montado. Nem parse de SVG, nem montagem de curvas |

  É por isso que a cena de referência de §13 custa 38,22 s: `MathTex` com
  `rf"f'({x.get_value():.2f}) = …"` a 60 fps por 4 s são **~240 strings
  distintas**, ou seja ~240 execuções de `latex`. A correção da §13.2
  (`DecimalNumber` + `set_value`) elimina exatamente isso.

  Ver `manim-text-latex` para os dois caches de texto e
  `manim-performance-cache` para medir.

---

## 6. A família `always` — açúcar, com um aviso do próprio fonte

Sete funções de `animation/updaters/mobject_update_utils.py`, todas no
`from manim import *`.

| Símbolo | Assinatura (índice) |
|---|---|
| `always` | `(method: Callable, *args, **kwargs) -> Mobject` |
| `f_always` | `(method: Callable[[M], None], *arg_generators, **kwargs) -> M` |
| `always_redraw` | `(func: Callable[[], M]) -> M` |
| `always_shift` | `(mobject: M, direction=RIGHT, rate: float = 0.1) -> M` |
| `always_rotate` | `(mobject: M, rate: float = 0.3490658503988659, **kwargs) -> M` |
| `turn_animation_into_updater` | `(animation, cycle: bool = False, delay: float = 0, **kwargs) -> Mobject` |
| `cycle_animation` | `(animation, **kwargs) -> Mobject` |
| `assert_is_mobject_method` | `(method: Callable) -> None` |

### 6.1 `always` e `Mobject.always` congelam os argumentos — este é o erro

Existem **duas** coisas chamadas `always`:

```python
always(t.next_to, sq, UP)     # a FUNÇÃO do módulo
t.always.next_to(sq, UP)      # a PROPRIEDADE de Mobject
```

As duas fazem o mesmo (`mobject/mobject.py:3477-3492`):
`add_updater(lambda m: getattr(m, name)(*args, **kwargs), call_updater=True)`.
Os argumentos são avaliados **uma vez**, na hora da chamada.

O aviso está no docstring da propriedade (`mobject/mobject.py:425-427`), com
todas as letras:

> `always` is not compatible with `ValueTracker.get_value()`, because the value
> will be computed once and then never updated again.

Ou seja:

```python
dot.always.set_x(t.get_value())      # ERRADO — congela o valor de agora
dot.add_updater(lambda m: m.set_x(t.get_value()))   # certo
```

`always` serve para argumento que é **objeto vivo** (`next_to(sq, UP)` — `sq` é
lido a cada frame porque o objeto é o mesmo), e falha para argumento que é
**valor** (um float lido agora). Essa distinção não aparece em lugar nenhum
além daquele parágrafo.

### 6.2 `f_always` — a versão que resolve isso

```python
def f_always(method, *arg_generators, **kwargs):
    def updater(mob):
        args = [g() for g in arg_generators]
        func(mob, *args, **kwargs)
```

Cada argumento é uma **função sem parâmetros**, chamada a cada frame:

```python
f_always(dot.set_x, t.get_value)     # certo: passa a função, não o valor
```

Repare que é `t.get_value` (sem parênteses). `f_always(dot.set_x, t.get_value())`
volta a congelar.

`assert_is_mobject_method` é o guarda dos dois: `always`/`f_always` exigem um
**método ligado a um mobject** (`inspect.ismethod` + `isinstance(Mobject)`).
Passar uma função solta levanta `AssertionError` sem mensagem.

### 6.3 `always_shift` e `always_rotate` — movimento perpétuo

```python
always_shift(sq, RIGHT, rate=5)        # 5 unidades de palco por segundo
always_rotate(tri, rate=2*PI, about_point=ORIGIN)   # uma volta por segundo
```

Corpos reais:

```python
mobject.add_updater(lambda m, dt: m.shift(dt * rate * normalize(direction)))
mobject.add_updater(lambda m, dt: m.rotate(dt * rate, **kwargs))
```

Os dois são time-based, os dois **normalizam a direção** (a magnitude do vetor
não conta, só `rate`), e o `**kwargs` do `always_rotate` vai direto para
`Mobject.rotate` — é assim que se passa `about_point` / `axis`.

Default de `always_rotate`: `rate=20*DEGREES` ≈ 0,349 rad/s — quase parado.
Quase sempre você quer explicitar.

Como são lineares em `dt`, eles **sobrevivem** a uma seção pulada (§12): uma
chamada com `dt` grande produz o mesmo deslocamento total.

### 6.4 `turn_animation_into_updater` e `cycle_animation`

Transformam uma `Animation` num updater que roda **em paralelo** ao resto,
sem ocupar um `self.play`:

```python
turn_animation_into_updater(Write(palavras, run_time=0.9))
self.add(palavras)
self.wait(0.5)
self.play(banner.expand(), run_time=0.5)   # o Write continua por baixo
```

Mecânica lida no fonte: ele força `animation.suspend_mobject_updating = False`,
chama `begin()`, e anexa um updater que acumula `total_time` e chama
`interpolate(alpha)`. Sem `cycle`, o updater **se auto-remove** ao chegar em
alpha 1 (`m.remove_updater(update)`); com `cycle=True` (que é o que
`cycle_animation` faz) ele repete para sempre. `delay` adia o começo em
segundos.

Quando isso é a resposta certa: um `Write` de fundo que não pode segurar a
linha do tempo, um loop de "carregando". Quando não é: qualquer coisa cujo fim
você precise sincronizar — o `play` seguinte não espera por ele.

---

## 7. Número que conta na tela

### 7.1 `DecimalNumber` — a assinatura inteira

```python
DecimalNumber(number: float = 0,
              num_decimal_places: int = 2,
              mob_class: type[SingleStringMathTex] = MathTex,
              include_sign: bool = False,
              group_with_commas: bool = True,
              digit_buff_per_font_unit: float = 0.001,
              show_ellipsis: bool = False,
              unit: str | None = None,
              unit_buff_per_font_unit: float = 0,
              include_background_rectangle: bool = False,
              edge_to_fix: Vector3DLike = LEFT,
              font_size: float = 48,
              stroke_width: float = 0,
              fill_opacity: float = 1.0,
              **kwargs)
```

Métodos próprios: `set_value(number) -> Self`, `get_value() -> float`,
`increment_value(delta_t: float = 1) -> Self`.

`Integer(number=0, num_decimal_places=0, **kwargs)` é só isso — a mesma classe
com zero casas.

### 7.2 O padrão

```python
n = DecimalNumber(0, num_decimal_places=2, color=TINTA, font_size=48)
t = ValueTracker(0)
n.add_updater(lambda m: m.set_value(t.get_value()))
self.add(t, n)
self.play(t.animate.set_value(99.9), run_time=3, rate_func=linear)
n.clear_updaters()
```

Sem o tracker, quando o alvo é fixo, use a animação pronta — mais barata e sem
updater para limpar depois:

```python
self.play(ChangeDecimalToValue(n, 100), run_time=2)
```

### 7.3 As duas animações de `animation/numbers`

```python
ChangingDecimal(decimal_mob: DecimalNumber,
                number_update_func: Callable[[float], float],
                suspend_mobject_updating: bool = False, **kwargs)

ChangeDecimalToValue(decimal_mob: DecimalNumber, target_number: int, **kwargs)
```

- `ChangingDecimal` recebe **uma função de alpha** e chama
  `set_value(func(rate_func(alpha)))`. Serve para contagem não linear:
  `ChangingDecimal(n, lambda a: 100 * a**2, run_time=3)`.
- `ChangeDecimalToValue` é ela com `lambda a: interpolate(inicio, alvo, a)`.
- Repare no default `suspend_mobject_updating=False` das duas: ao contrário de
  quase toda animação do Manim, elas **não** desligam os updaters do mobject
  (§10). É deliberado — o `DecimalNumber` costuma ter um updater de posição.
- `ChangingDecimal` levanta `TypeError` se o mobject não for `DecimalNumber`.

### 7.4 `edge_to_fix` — a razão de o número "pular"

`set_value` reconstrói os glifos e chama
`self.move_to(move_to_point, self.edge_to_fix)`, onde `move_to_point` foi lido
com `get_edge_center(self.edge_to_fix)` antes da troca
(`mobject/text/numbers.py:288-296`).

Default `LEFT`: a borda **esquerda** fica parada. De `9` para `10`, o número
cresce para a direita. Isso é certo para um rótulo que começa numa margem, e
errado para quase todo o resto:

| Situação | `edge_to_fix` |
|---|---|
| rótulo alinhado à esquerda | `LEFT` (default) |
| número centralizado num card | `ORIGIN` |
| coluna numérica alinhada à direita | `RIGHT` |
| número em cima de uma barra de gráfico | `DOWN` (a base não sobe) |

### 7.5 Custo real — e o mito que vale corrigir

`_string_to_mob` (`mobject/text/numbers.py:216-229`) usa um dicionário
**de módulo**:

```python
string_to_mob_map: dict[str, SingleStringMathTex] = {}
...
if string not in string_to_mob_map:
    string_to_mob_map[string] = mob_class(string, **kwargs)
mob = string_to_mob_map[string].copy()
```

Ou seja: **o LaTeX de cada caractere compila uma vez por processo**, não uma vez
por frame. `set_value` a 60 fps não roda `latex` 60×. O que ele faz por frame é:
formatar a string, **copiar** um mobject por caractere, `arrange`, `match_style`
por submobject, `move_to`, e — no cairo — zerar os pontos da família antiga.
Isso é O(nº de caracteres) por frame.

Portanto a receita "reduza `num_decimal_places` se estiver lento" continua
válida, mas pelo motivo certo: **menos caracteres, menos cópias e menos
`arrange`**. `group_with_commas=False` também tira caracteres.

Dois detalhes lidos no fonte que valem registrar:

- O cache é indexado **só pela string**, ignorando `mob_class` e os kwargs. Um
  `DecimalNumber(mob_class=Tex)` depois de um `DecimalNumber(mob_class=MathTex)`
  reaproveita a versão `MathTex` do caractere. *(Consequência lida no código,
  não reproduzida.)*
- No cairo, `set_value` faz `mob.points[:] = 0` em toda a família antiga — um
  hack explicitamente comentado como necessário "para compatibilidade com
  updaters". Se você guardou uma referência a um submobject antigo do
  `DecimalNumber`, ela vira um objeto degenerado na origem.

### 7.6 `Variable` — rótulo + tracker + número, já montado

```python
Variable(var: float,
         label: str | Tex | MathTex | Text | SingleStringMathTex,
         var_type: type[DecimalNumber | Integer] = DecimalNumber,
         num_decimal_places: int = 2, **kwargs)
```

É um `VMobject` que contém `self.label` (rótulo + `=`) e `self.value`, com
`self.tracker: ValueTracker` **como atributo** e o updater já anexado ao
`value`:

```python
x_var  = Variable(2.0, "x",   num_decimal_places=3)
sqr    = Variable(4.0, "x^2", num_decimal_places=3)
VGroup(x_var, sqr).arrange(DOWN)
sqr.add_updater(lambda v: v.tracker.set_value(x_var.tracker.get_value() ** 2))

self.add(x_var, sqr)
self.play(x_var.tracker.animate.set_value(5), run_time=2, rate_func=linear)
```

Atenção: `tracker` **não é submobject**, é atributo. Adicionar a `Variable` à
cena não coloca o tracker lá. Enquanto você anima com
`self.play(v.tracker.animate...)` isso não importa (o `play` adiciona sozinho);
se o tracker tiver updater próprio, adicione-o na mão.

E `Variable` **não tem nenhum updater time-based**, então mudar o tracker por
`set_value` seguido de `self.wait()` não mostra nada — §11.

`Variable` mora em `mobject/text` e é território disputado; para o resto de
`Text`/`MathTex`, a skill é `manim-text-latex`.

---

## 8. Updater embrulhado em animação — quando ele deve morrer no fim do `play`

Três classes de `animation/updaters/update.py`, no `from manim import *`:

```python
UpdateFromFunc(mobject, update_function: Callable[[Mobject], Any],
               suspend_mobject_updating: bool = False, **kwargs)

UpdateFromAlphaFunc(mobject, update_function: Callable[[Mobject], Any],
                    suspend_mobject_updating: bool = False, **kwargs)

MaintainPositionRelativeTo(mobject, tracked_mobject, **kwargs)
```

Corpos (leitura direta):

```python
class UpdateFromFunc(Animation):
    def interpolate_mobject(self, alpha): self.update_function(self.mobject)

class UpdateFromAlphaFunc(UpdateFromFunc):
    def interpolate_mobject(self, alpha):
        self.update_function(self.mobject, self.rate_func(alpha))

class MaintainPositionRelativeTo(Animation):
    def __init__(self, mobject, tracked_mobject, **kwargs):
        self.diff = mobject.get_center() - tracked_mobject.get_center()
    def interpolate_mobject(self, alpha):
        self.mobject.shift(self.tracked_mobject.get_center()
                           - self.mobject.get_center() + self.diff)
```

### 8.1 Por que preferir isso a `add_updater`

**Ele acaba sozinho.** Um `add_updater` continua vivo nas animações seguintes e
é a causa do "a etiqueta grudou". Um `UpdateFromFunc` existe só durante aquele
`self.play` — não há nada para limpar, e não há como esquecer.

```python
self.play(
    alvo.animate.shift(RIGHT * 4),
    UpdateFromFunc(etiqueta, lambda m: m.next_to(alvo, UP)),
)
```

> **Regra prática:** se o acompanhamento vale só durante **uma** animação, use
> `UpdateFromFunc`. `add_updater` é para o que precisa atravessar vários `play`
> e `wait`.

### 8.2 As diferenças que importam

- `UpdateFromAlphaFunc` recebe **`rate_func(alpha)`, não `alpha` cru**. A curva
  já está aplicada: não aplique de novo.
- Os dois nascem com `suspend_mobject_updating=False` — de propósito, porque o
  alvo tipicamente tem outros updaters que devem continuar (§10).
- `MaintainPositionRelativeTo` **não** passa esse default: ele herda `True` de
  `Animation`, e portanto **suspende** os updaters do mobject acompanhado
  durante a animação. Ele congela o deslocamento no `__init__` — se o mobject
  se move por outro motivo entre a construção da animação e o `begin()`, o
  offset é o antigo.
- Os três interpolam pelo `alpha` do `play`. Num `AnimationGroup` com
  `lag_ratio`, eles começam junto com o grupo, não com o vizinho.

---

## 9. `TracedPath` e `AnimatedBoundary` são MOBJECTS, não animações

Eles moram em `manim/animation/changing.py` — e é por isso que várias listas os
classificam errado, inclusive a de `manim-animations` (§"Outras", linha 92).
As bases são inequívocas:

```python
class TracedPath(VMobject, metaclass=ConvertToOpenGL)
class AnimatedBoundary(VGroup)
```

> Entram com **`self.add(...)`**. `self.play(TracedPath(...))` não é uma coisa
> que exista.

### 9.1 `TracedPath`

```python
TracedPath(traced_point_func: Callable,
           stroke_width: float = 2,
           stroke_color: ParsableManimColor | None = WHITE,
           dissipating_time: float | None = None,
           **kwargs)
```

```python
rastro = TracedPath(ponto.get_center, stroke_color=ACENTO, stroke_width=3)
self.add(rastro)                       # ANTES do objeto, para ficar atrás
self.play(ponto.animate.shift(RIGHT * 6), run_time=4, rate_func=linear)
```

O updater dele (anexado no `__init__`, e **time-based**):

```python
def update_path(self, mob, dt):
    new_point = self.traced_point_func()
    if not self.has_points(): self.start_new_path(new_point)
    self.add_line_to(new_point)
    if self.dissipating_time:
        self.time += dt
        if self.time - 1 > self.dissipating_time:
            self.set_points(self.points[self.n_points_per_curve:])
```

Quatro coisas:

1. **`stroke_color` default é `WHITE`.** Em tema claro, o rastro não aparece e
   não dá erro nenhum. É o defeito nº 1 de fundo branco (`manim-color-theming`,
   e `manim-project` §10). Sempre passe a cor do seu tema.
2. **Uma curva por FRAME.** 4 s a 60 fps = 240 segmentos ≈ 960 pontos. Um rastro
   de 20 s é um `VMobject` de 1200 curvas, redesenhado a cada frame. Use
   `dissipating_time` para dar um teto.
3. Ele recebe uma **função**, não um ponto: `ponto.get_center` (sem parênteses).
   Com parênteses você passa um array e o rastro fica parado.
4. `dissipating_time` combina com `stroke_opacity=[0, 1]` (gradiente ao longo do
   traço) — é o idioma do docstring da classe.

**Em cena cortada em partes, `TracedPath` é o caso perigoso** — §12.2.

### 9.2 `AnimatedBoundary`

```python
AnimatedBoundary(vmobject: VMobject,
                 colors=[BLUE_D, BLUE_B, BLUE_E, GREY_BROWN],
                 max_stroke_width: float = 3,
                 cycle_rate: float = 0.5,
                 back_and_forth: bool = True,
                 draw_rate_func: RateFunction = smooth,
                 fade_rate_func: RateFunction = smooth,
                 **kwargs)
```

```python
self.add(texto, AnimatedBoundary(texto, colors=[ACENTO, VERDE], cycle_rate=3))
self.wait(2)
```

É um `VGroup` com **duas cópias** do contorno do alvo (uma crescendo, outra
sumindo) e um updater time-based que acumula `total_time`. A paleta default é
azul do Manim — em projeto com tema, passe `colors`. Como o updater é
time-based, ele **mantém o `wait` vivo** (§11), o que é útil e às vezes
indesejado: um `AnimatedBoundary` esquecido na cena impede qualquer frame
estático até o fim.

---

## 10. A briga: animação × updater — e a animação VENCE

Esta é a correção mais importante desta revisão. Muita gente (e a versão
anterior desta skill) afirma que o updater sobrescreve a interpolação. **É o
contrário.**

`Animation.__init__` (`animation/animation.py:137`) tem
`suspend_mobject_updating: bool = True`, e:

```python
def begin(self):
    self.starting_mobject = self.create_starting_mobject()
    if self.suspend_mobject_updating:
        self.mobject.suspend_updating()      # <- os updaters PARAM
    self.interpolate(0)

def finish(self):
    self.interpolate(1)
    if self.suspend_mobject_updating and self.mobject is not None:
        self.mobject.resume_updating()       # <- e voltam
```

E `resume_updating` termina com `self.update(dt=0, recursive=recursive)`
(`mobject/mobject.py:1230-1233`).

### 10.1 A sequência completa do defeito

```python
etiqueta.add_updater(lambda m: m.next_to(alvo, UP))
self.add(etiqueta)
self.play(etiqueta.animate.shift(DOWN * 2))     # parece funcionar...
```

1. `begin()` → `etiqueta.suspend_updating()`. O updater está desligado.
2. Durante o `play`, a etiqueta desce lindamente. **Nenhum conflito visível.**
3. `finish()` → `interpolate(1)` (ela chega embaixo) → `resume_updating()` →
   `update(dt=0)` → o updater roda → `next_to(alvo, UP)` → **a etiqueta salta de
   volta para cima do alvo**, num frame.

O sintoma relatado é "o objeto voltou sozinho quando a animação acabou" ou "a
animação não teve efeito". A causa não é briga: é que a animação foi desfeita
pela primeira execução do updater ao ser reativado.

Vale para `.animate` também: `_AnimationBuilder` produz um
`_MethodAnimation(MoveToTarget)`, que é um `Transform`, que é uma `Animation`
com o mesmo default.

### 10.2 As quatro saídas

```python
# (a) anime o PARÂMETRO, não o objeto — a saída canônica
self.play(t.animate.set_value(10))          # o updater lê t e reposiciona

# (b) tire o updater durante o play
etiqueta.clear_updaters()
self.play(etiqueta.animate.shift(DOWN * 2))
etiqueta.add_updater(...)                   # se ainda fizer sentido

# (c) troque por uma animação com updater embutido (§8)
self.play(UpdateFromFunc(etiqueta, lambda m: m.next_to(alvo, UP)),
          alvo.animate.shift(RIGHT * 4))

# (d) desligue a suspensão, se você QUER os dois rodando
self.play(Transform(a, b, suspend_mobject_updating=False))
```

A (d) é a única que produz a briga verdadeira: a animação escreve e o updater
sobrescreve no mesmo frame (§2.2 — updater roda depois). Só use quando o
updater mexe numa propriedade que a animação não toca.

### 10.3 O corolário do grupo

`suspend_updating(recursive=True)` desce por toda a família. Portanto
`self.play(grupo.animate.shift(RIGHT))` **congela o updater de todo filho do
grupo** durante a animação — inclusive o `always_redraw` que você pôs lá
dentro. Ele volta no fim e salta.

### 10.4 O outro corolário: `.animate` fotografa o alvo cedo demais

`_AnimationBuilder.__init__` chama `self.mobject.generate_target()`
(`mobject/mobject.py:3415-3418`) — ou seja, **no instante em que você escreve
`mob.animate`**, não quando o `play` começa. Se um updater vai mexer no mobject
entre uma coisa e outra, o alvo foi calculado a partir de um estado velho.
Com updaters na cena, prefira construir a animação na mesma linha do `play`.

---

## 11. O `wait` estático — por que "o updater não roda no wait"

`Scene.should_update_mobjects` (`scene/scene.py:419-445`):

```python
should_update = (
    self.always_update_mobjects
    or self.updaters                                  # updaters de CENA
    or wait_animation.stop_condition is not None
    or any(mob.has_time_based_updater()
           for mob in self.get_mobject_family_members())
)
wait_animation.is_static_wait = not should_update
```

Se nenhuma dessas quatro condições vale, o renderer chama
`freeze_current_frame(scene.duration)` (`renderer/cairo_renderer.py:112-117`):
**um frame é desenhado e repetido**. Nenhum updater roda durante o `wait`.

E `has_time_based_updater()` só olha quem tem **`dt` na assinatura**. Portanto:

> Um `always_redraw` sozinho na cena **não** segura o `wait` vivo — o updater
> dele tem o parâmetro chamado `_` (§5.1). O mesmo vale para
> `add_updater(lambda m: ...)`.

Isso quase sempre está certo (se nada muda no tempo, o frame é mesmo estático).
Ele morde em três casos:

```python
# (1) o tracker é o relógio, mas você esqueceu de adicioná-lo à cena
t.add_updater(lambda m, dt: m.increment_value(dt))
self.add(t)                     # SEM isto o wait congela

# (2) o updater lê algo externo (self.time, um contador, um arquivo)
self.wait(3, frozen_frame=False)          # força o laço de frames

# (3) você quer parar quando uma condição acontecer
self.wait_until(lambda: t.get_value() > 5, max_time=10)
```

Assinaturas conferidas:

```python
Scene.wait(duration: float = 1.0,
           stop_condition: Callable[[], bool] | None = None,
           frozen_frame: bool | None = None) -> None
Scene.wait_until(stop_condition: Callable[[], bool], max_time: float = 60) -> None
Scene.pause(duration: float = 1.0) -> None      # alias de wait(frozen_frame=True)
```

`Wait(stop_condition=..., frozen_frame=True)` levanta `ValueError` — as duas
coisas são incompatíveis por construção.

Lado bom, e é grande: **`self.pause()` / `wait(frozen_frame=True)` é o
mecanismo que faz um frame parado custar quase nada** — exatamente o que o
formato em partes de `manim-presentation-parts` explora.

---

## 12. Seção pulada, `-s` e `-n`: o `dt` gigante

Este é o achado que mais afeta quem faz vídeo de aula, e ele não está em
documentação nenhuma.

### 12.1 O mecanismo

`Scene.get_time_progression` (`scene/scene.py:1097-1101`):

```python
if self.renderer.skip_animations and not override_skip_animations:
    times = [run_time]                              # UMA iteração
else:
    times = np.arange(0, run_time, 1 / config["frame_rate"])
```

E `skip_animations` liga em quatro situações
(`renderer/cairo_renderer.py:245-267` e `:91-97`):

| Situação | Origem |
|---|---|
| `next_section(..., skip_animations=True)` | `file_writer.sections[-1].skip_animations` |
| `-s` / `--save_last_frame` | `config["save_last_frame"]` |
| `-n a,b` fora da faixa | `from_animation_number` / `upto_animation_number` |
| **animação encontrada no cache** | `is_already_cached(...)` → `self.skip_animations = True` |

Nessas quatro, `update_to_time` é chamado **uma vez** com `dt = run_time`
inteiro, em vez de N vezes com `dt = 1/fps`.

### 12.2 O que sobrevive e o que quebra

| Updater | Sobrevive? | Por quê |
|---|---|---|
| `always_redraw` / `lambda m:` | **sim** | idempotente: uma chamada no estado final basta |
| `always_rotate`, `always_shift` | **sim** | linear em `dt`: um passo grande = N passos pequenos |
| `AnimatedBoundary` | **sim** | acumula `total_time += dt`, também linear |
| `lambda m, dt: m.scale(1 + dt)` | **não** | multiplicativo: `1+3` ≠ `(1+0.05)**60` |
| **`TracedPath`** | **não** | acrescenta **um** segmento por chamada |
| `turn_animation_into_updater` | parcial | chega ao alpha final, mas sem os frames do meio |

O caso `TracedPath` é o que dói de verdade no formato em partes: no ato pulado
o rastro ganha 1 segmento em vez de 240, então **o estado do palco no começo da
parte N+1 não é o do fim da parte N**. A métrica direcional de emenda de
`manim-presentation-parts` acusa isso como "tinta que sumiu", e o instinto é
procurar o defeito na animação — quando ele está no updater.

**Regra para cena em partes:** só use updater **idempotente ou linear em `dt`**.
Rastro, acumulador e qualquer coisa multiplicativa não podem atravessar um
`next_section(skip_animations=True)`.

### 12.3 O mesmo mecanismo no pôster e no cache

- **`-s` / `--format png`**: todos os `play` anteriores são pulados. Um pôster
  gerado assim tem o rastro vazio e o relógio errado. Se o seu pipeline extrai
  o pôster do mp4 com `ffmpeg -sseof -1 -update 1` (é o que
  `manim-batch-pipeline` recomenda), o problema não existe — o frame vem do
  vídeo de verdade.
- **Cache**: uma animação servida do cache também roda com o `dt` gigante, o que
  significa que o **estado que ela deixa para a animação seguinte** pode diferir
  de um render frio. Cena com updater acumulador merece `--no-cache`.
  *(Consequência derivada do fonte, não reproduzida nesta sessão.)* O cache em
  si é de `manim-performance-cache`; o dado externo que o hash não enxerga está
  em `manim-project` §10.7.

---

## 13. Custo, e o que fazer com ele

### 13.1 De onde vem a lentidão

Em ordem de peso, com a evidência de cada uma:

1. **O frame estático morre.** `get_moving_mobjects` (§2.4) devolve tudo a
   partir do primeiro mobject com updater. Um `always_redraw` adicionado cedo
   faz o cenário inteiro ser rasterizado 60×/s.
2. **Recompilar LaTeX por frame.** `always_redraw(lambda: MathTex(f"…{v:.2f}…"))`
   muda a STRING a cada frame, e o cache de `media/Tex` é indexado pela
   expressão — logo cada frame é um **miss**: `latex` + `dvisvgm`, dois
   subprocessos. É o item mais caro de `TangenteViva` (~240 compilações em 4 s).
   Com string **constante** o custo cai a um `.copy()` de cache em memória
   (§5.4).
3. **A família que só cresce** (§5.3): submobjects transparentes acumulados que
   continuam sendo percorridos.
4. **`inspect.signature` por updater, por frame** (§2.3), no cairo.
5. **`TracedPath` longo**: uma curva por frame, sem teto, redesenhado inteiro
   sempre.

### 13.2 A refatoração de `TangenteViva`, passo a passo

A cena medida em 38,22 s (`scenes/exemplos.py:50-81`) tem três `always_redraw`,
um deles com `MathTex`. A versão barata do mesmo efeito:

```python
x = ValueTracker(-2.4)

# 1. o ponto MOVE, não renasce
ponto = Dot(ax.i2gp(x.get_value(), f), color=ACENTO)
ponto.add_updater(lambda m: m.move_to(ax.i2gp(x.get_value(), f)))

# 2. o número é DecimalNumber, não MathTex reconstruído
leitura = DecimalNumber(0, num_decimal_places=2, color=TINTA,
                        edge_to_fix=LEFT).to_corner(UL)
leitura.add_updater(lambda m: m.set_value(2 * x.get_value()))

# 3. o cenário parado ENTRA PRIMEIRO (§2.4)
self.add(ax, f, rotulo)
self.add(ponto, leitura)

self.play(x.animate.set_value(2.4), run_time=4, rate_func=linear)
```

Sobra um `always_redraw` legítimo: a reta secante, que muda de geometria e não
só de posição.

**Não medi o ganho** — render é proibido nesta sessão. O que está medido é o
custo do original (38,22 s contra 2,69–3,65 s das cenas vizinhas,
`manim-gpu-encoding`, 2026-08-19). A estimativa de melhora fica em aberto;
quem for medir, use `bin/mx bench` e a skill `manim-gpu-encoding`.

### 13.3 Checklist de barateamento

- [ ] cenário parado adicionado **antes** de qualquer coisa com updater
- [ ] `always_redraw` só onde a **estrutura** muda; posição vira `add_updater`
- [ ] nenhum `Text`/`Tex`/`MathTex` construído dentro de um `always_redraw`
- [ ] `DecimalNumber` com o menor `num_decimal_places` que serve
- [ ] `TracedPath` com `dissipating_time` quando o rastro passa de ~5 s
- [ ] `clear_updaters()` no fim de cada trecho, para o frame estático voltar
- [ ] o `wait` final não tem nenhum updater time-based vivo (§11) — senão ele
      renderiza N frames em vez de congelar um

O último item é o mais fácil de esquecer e o mais visível na conta: um
`AnimatedBoundary` esquecido faz cada `self.wait(2)` custar 120 frames.

---

## 14. cairo × OpenGL: a mesma ideia, outra implementação

O renderer OpenGL não usa `Mobject`, usa `OpenGLMobject` — e o sistema de
updaters é reescrito.

| | cairo (`Mobject`) | OpenGL (`OpenGLMobject`) |
|---|---|---|
| lista de updaters | uma só (`self.updaters`) | **duas**: `time_based_updaters` e `non_time_updaters` |
| como decide se é time-based | `inspect.signature` **a cada frame** | uma vez, no `add_updater` |
| atalho de família | — | flag `has_updaters` + `refresh_has_updater_status()` |
| `update` | `(dt=0, **recursive**=True)` | `(dt=0, **recurse**=True)` |
| `clear_updaters` | `(recursive=True)` | `(recurse=True)` |
| `suspend_updating` | `(recursive=True)` | `(recurse=True)` |
| `resume_updating` | `(recursive=True)` | `(recurse=True, call_updater=True)` |
| exclusivos | — | `init_updaters()`, `refresh_has_updater_status()` |

> **`recursive` × `recurse`.** O mesmo código com `mob.clear_updaters(recursive=False)`
> quebra com `TypeError` ao trocar para `--renderer opengl`, e vice-versa.
> Escrever posicionalmente (`mob.clear_updaters(False)`) atravessa os dois.

`ValueTracker`, `DecimalNumber`, `TracedPath` e `Variable` usam
`metaclass=ConvertToOpenGL`, então trocam de base sozinhos conforme o renderer.
As **funções** (`always_redraw`, `always_rotate`, …) funcionam nos dois.

Escolha de renderer, e por que quase sempre é cairo aqui: `manim-gpu-encoding`.

---

## 15. Cache, dado externo e updater

O hash que nomeia o partial movie serializa funções pelo **texto do código
fonte** e pelas **variáveis de closure** (`utils/hashing.py:265-283`:
`inspect.getsource(obj)` + `inspect.getclosurevars`). Duas consequências:

- Editar o corpo de um updater **invalida** o cache. Bom.
- Um updater que lê algo de **fora** do processo (um CSV, uma API, `random` sem
  semente, `datetime.now()`) não muda nada no hash: o Manim reaproveita o vídeo
  velho com o dado novo. É o mesmo defeito de `manim-project` §10.7 — cena com
  dado externo pede `--no-cache`.
- `inspect.getsource` de uma `lambda` devolve a **linha inteira** em que ela
  está. Dois updaters diferentes escritos na mesma linha produzem o mesmo texto.

O resto do assunto cache é de **`manim-performance-cache`**.

---

## 16. Catálogo — a categoria inteira, sem buraco

Gerado do índice; confira com
`awk -F'\t' '$3=="animation/updaters"' api/manim-ce-index.tsv`.

### `animation/updaters` (11 símbolos acionáveis)

| Símbolo | Tipo | Seção |
|---|---|---|
| `always` | função | §6.1 |
| `f_always` | função | §6.2 |
| `always_redraw` | função | §5 |
| `always_shift` | função | §6.3 |
| `always_rotate` | função | §6.3 |
| `turn_animation_into_updater` | função | §6.4 |
| `cycle_animation` | função | §6.4 |
| `assert_is_mobject_method` | função | §6.2 |
| `UpdateFromFunc` | classe | §8 |
| `UpdateFromAlphaFunc` | classe | §8 |
| `MaintainPositionRelativeTo` | classe | §8 |

### `mobject/value_tracker` (2)

`ValueTracker` §3 · `ComplexValueTracker` §3.5

### `animation/numbers` (2)

`ChangingDecimal` §7.3 · `ChangeDecimalToValue` §7.3

### `animation/changing` (2)

`TracedPath` §9.1 · `AnimatedBoundary` §9.2

### Métodos de `Mobject` (11) — §4.2

`add_updater` `remove_updater` `clear_updaters` `get_updaters`
`get_family_updaters` `get_time_based_updaters` `has_time_based_updater`
`match_updaters` `suspend_updating` `resume_updating` `update`

### Métodos de `Scene` (7) — §11 e abaixo

`add_updater` `remove_updater` `update_self` `update_mobjects`
`should_update_mobjects` `wait` `wait_until`

```python
Scene.add_updater(func: Callable[[float], None]) -> None      # recebe SÓ dt
Scene.remove_updater(func: Callable[[float], None]) -> None
Scene.update_self(dt: float) -> None
```

Updater de cena recebe **um** argumento (`dt`), não o mobject. Roda **por
último** no frame (§2.2), e a remoção é por identidade
(`[f for f in self.updaters if f is not func]`, `scene/scene.py:689`) — guarde
a referência. Use `self.time` (propriedade → `self.renderer.time`), não
`self.renderer.time` na mão.

```python
def registra(dt):
    print(self.time, dot.get_center())
self.add_updater(registra)
...
self.remove_updater(registra)
```

### Do índice, e uma nota para quem confere assinatura

`Mobject.always` e `Mobject.animate` são **propriedades**, e o
`api/manim-ce-methods.tsv` **não indexa propriedades** (as únicas `kind` para
`Mobject` são `method`, `classmethod`, `staticmethod`). Não conclua que não
existem por não achar no TSV — confirme no fonte. Metodologia:
`manim-api-discovery`.

---

## 17. Armadilhas, com a causa e o conserto

| Sintoma | Causa real | Conserto |
|---|---|---|
| updater não roda | o mobject não está alcançável de `scene.mobjects` | `self.add(...)` — §2.1 |
| `TypeError: <lambda>() missing 1 required positional argument` | o 2º parâmetro não se chama `dt` | renomeie para `dt` — §2.3 |
| velocidade muda entre `-q l` e `-q h` | updater sem `dt` gira por frame | use `dt` — §4.3 |
| **objeto volta ao lugar quando a animação acaba** | `resume_updating()` chama `update(dt=0)` | anime o tracker, não o objeto — §10 |
| a animação "não teve efeito" | o updater reposiciona no fim | idem §10 |
| "a etiqueta grudou e não para" | updater não removido | `clear_updaters()` ou use `UpdateFromFunc` — §8.1 |
| `self.wait()` não anima nada | nenhum updater **time-based** na cena | `self.add(tracker)` ou `wait(frozen_frame=False)` — §11 |
| `dot.always.set_x(t.get_value())` não muda | `always` congela os argumentos | `f_always(dot.set_x, t.get_value)` — §6.1 |
| o rastro não aparece em fundo branco | `TracedPath` nasce `stroke_color=WHITE` | passe a cor do tema — §9.1 |
| `self.play(TracedPath(...))` dá erro | é Mobject, não Animation | `self.add(...)` — §9 |
| todos os N updaters usam o último índice | closure captura a variável do laço | `lambda m, i=i:` — §4.4 |
| o objeto desloca alguns px sem motivo | submobjects invisíveis acumulados por `become` | estrutura fixa na função — §5.3 |
| a parte pulada do vídeo saiu diferente | `dt` gigante em updater não linear | só updater idempotente/linear — §12.2 |
| o relógio do tracker parou | `t = t + 1` trocou o objeto | use `t += 1` — §3.4 |
| a cena leva 10× mais tempo | frame estático desligado + redraw de texto | §13 |
| `mob.clear_updaters(recursive=False)` quebra no opengl | lá o kwarg é `recurse` | posicional — §14 |
| updater de cena não sai com `remove_updater` | comparação por identidade | guarde a referência — §16 |
| `ValueTracker` dentro de `VGroup` dá `TypeError` | `VGroup` só aceita `VMobject` | use `Group`, ou não agrupe — `manim-mobjects` |

---

## 18. Conferir sem renderizar

Nenhum destes precisa de GPU; todos pegam defeito que não dá erro.

```bash
# 1. updater com segundo parâmetro que não se chama dt  -> TypeError garantido
grep -rnP 'add_updater\(\s*lambda\s+\w+\s*,\s*(?!dt\b)\w+' cenas/

# 2. always_redraw cujo retorno nunca é adicionado à cena
grep -rn "always_redraw" cenas/ | grep -v "self.add"    # inspecione cada linha

# 3. .always com get_value dentro — congelamento silencioso (§6.1)
grep -rnE '\.always\.[a-z_]+\([^)]*get_value\(\)' cenas/

# 4. updater anexado e nunca limpo
grep -c "add_updater" cena.py ; grep -c "clear_updaters\|remove_updater" cena.py

# 5. TracedPath sem cor explícita — invisível em fundo claro
grep -rn "TracedPath(" cenas/ | grep -v "stroke_color"

# 6. em cena EM PARTES: acumulador atravessando um corte
grep -n "_corte\|TracedPath\|+= dt\|scale(1 +" cena_em_partes.py
```

E o conferidor estático de cena de `manim-api-discovery` §5 valida os **nomes**
de tudo isso sem importar o Manim.

Depois de renderizar, o que fecha o ciclo é **olhar o PNG** — updater errado
quase nunca dá erro no terminal. Procedimento em **`manim-verificacao-visual`**.

---

## 19. Onde esta skill para

| Assunto | Skill dona |
|---|---|
| escolher a classe de animação, `Transform` × `ReplacementTransform`, `.animate` | `manim-animations` |
| `rate_func`, as 49 curvas, `path_func`, `lag_ratio`, `AnimationGroup`, orçamento de tempo | `manim-composicao-ritmo` |
| corte em partes, `next_section`, emenda, métrica direcional | `manim-presentation-parts` |
| `Scene.next_section` e o mapa das classes de `Scene` | `manim-cenas-secoes` |
| `Axes`, `plot`, `i2gp`, `c2p`, `get_secant_slope_group`, `get_riemann_rectangles` | `manim-graphs-plots` |
| `self.camera.frame` com updater, zoom e pan 2D | `manim-camera-2d` |
| `phi`/`theta`, `move_camera`, 3D | `manim-3d-camera` |
| posicionar, `next_to`, buffers, "cabe na tela?" | `manim-layout-posicionamento` |
| `VGroup` × `Group`, submobjects, `restructure_mobjects` | `manim-mobjects` |
| cor, contraste, o `tema.py` como paleta, texto sumindo no fundo | `manim-color-theming` |
| `Text`/`MathTex`, cache de LaTeX, nitidez de glifo | `manim-text-latex` |
| cache de partial movie, `--no-cache`, `max_files_cached` | `manim-performance-cache` |
| codec, NVENC, medir tempo de render, `mx bench` | `manim-gpu-encoding` |
| olhar o PNG, comparar frames, conferir o pôster | `manim-verificacao-visual` |
| achar assinatura, kwarg, "esse método existe?" | `manim-api-discovery` |
| render falhou por ambiente, traceback, bissecção | `manim-troubleshooting` |
| escrever `Animation` ou `Mobject` próprio, `override_animate` | `manim-mobjects-customizados` |

**Sem skill dona hoje** (declare o buraco, não improvise): `VectorField`,
`ArrowVectorField`, `StreamLines`, `PhaseFlow`, `Homotopy`, `ComplexHomotopy`,
`SmoothedVectorizedHomotopy` — campos e fluxo. Eles fazem fronteira com esta
skill (`TracedPath` costuma aparecer junto), mas o assunto é outro.

---

## 20. O que aqui NÃO foi verificado

Nada foi renderizado nesta revisão (proibição de CPU/GPU). Todo mecanismo veio
de leitura de fonte e do índice estático. Ficam explicitamente **não
verificados**:

1. **O ganho da refatoração de §13.2.** O custo do original (38,22 s) é medição
   de `manim-gpu-encoding` de 2026-08-19; a versão barata não foi medida.
2. **O custo por frame de `inspect.signature`** (§2.3). O código está lido; o
   microbenchmark não foi feito.
3. **A divergência de estado por cache com updater acumulador** (§12.3). É
   dedução direta de `get_time_progression` + `skip_animations`, não um
   experimento.
4. **O reaproveitamento indevido de `string_to_mob_map` entre `mob_class`
   diferentes** (§7.5). Lido no código, não reproduzido.
5. **A diferença visual do `dt` gigante em `TracedPath` dentro de uma seção
   pulada** (§12.2). O mecanismo está provado no fonte; a comparação de frames
   não foi rodada. Quem for conferir: a métrica direcional de
   `manim-presentation-parts`.
