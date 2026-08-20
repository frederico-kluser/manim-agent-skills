---
name: manim-cenas-secoes
description: >-
  A `Scene` POR DENTRO — de qual das 7 classes herdar, o ciclo
  `setup`/`construct`/`tear_down`, a lista de exibição (`add`, `remove`,
  `clear`, `replace`, `bring_to_front`, foreground mobjects), o que sobrevive
  de um `self.play` para o outro, e `next_section` / a Segmented Video API.
  Use quando o pedido for: "de qual Scene eu herdo?", "preciso de fundo/eixos
  iguais em toda cena", "onde ponho o código que roda antes do construct?",
  "dá para passar um parâmetro para a cena?", "esse objeto some quando eu
  animo outro", "o desenho ficou por baixo mesmo depois do bring_to_front",
  "removi o mobject e ele voltou sozinho no play seguinte", "o FadeOut fez o
  objeto APARECER", "o `clear()` não parou o updater", "renderizei e saiu um
  PNG em vez de mp4", "a cena não aparece na lista do `mx scenes`", "o
  `bin/manim` ficou perguntando qual cena eu quero", "minha classe-base
  renderizou sozinha por engano", "como uso `--save_sections`?", "o vídeo da
  seção veio com um número estranho no nome", "chamei `next_section` e não
  saiu arquivo nenhum", "o `super().setup()` é obrigatório?", "por que o
  fundo branco só funciona com duas linhas?". Cobre as assinaturas conferidas
  no ManimCE 0.21.0 instalado, o caminho do código de `render()` até o
  arquivo, as regras de ordem de desenho (z-index vence ordem de `add`), a
  descoberta de cenas (o filtro do CE × o do `mx`, e por que um mixin some) e
  um conferidor estático por AST que roda sem importar manim. NÃO use para: o
  formato em PARTES que o apresentador avança com a seta
  (`manim-presentation-parts` — lá o `next_section` é meio, aqui é o assunto);
  escolher qualidade, formato, `-n a,b` e onde o arquivo foi parar
  (`manim-render-api`); `run_time`, `rate_func`, `lag_ratio`, `LaggedStart`
  (`manim-composicao-ritmo`); qual classe de animação usar e `Transform`
  (`manim-animations`); `ValueTracker` e updaters de mobject
  (`manim-updaters-valuetracker`); mover a câmera em 2D
  (`manim-camera-2d`) ou em 3D, `phi`/`theta` e `add_fixed_in_frame_mobjects`
  (`manim-3d-camera`); posicionar e enquadrar (`manim-layout-posicionamento`);
  paleta, contraste e `set_default` (`manim-color-theming`); o `tema.py` como
  contrato de projeto (`manim-tema-projeto`); `add_sound`/`add_subcaption`
  (`manim-som-legendas`); cache e custo de rasterizar
  (`manim-performance-cache`); traceback e ambiente quebrado
  (`manim-troubleshooting`); achar nome ou assinatura de API
  (`manim-api-discovery`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# A `Scene` por dentro

Quase tudo que se escreve em Manim mora dentro de um `construct`, e quase
ninguém lê o que acontece em volta dele. O resultado é um conjunto de defeitos
que **não levantam exceção nenhuma**: o objeto que volta sozinho para a cena, o
`bring_to_front` que não traz para a frente, a classe-base que renderiza um mp4
de 35 s que ninguém pediu, a cena que sai em PNG quando você pediu mp4, a seção
que você criou e que não virou arquivo.

Esta skill é o mecanismo: **quem chama o quê, em que ordem, e o que sobra na
memória entre uma animação e a seguinte.**

## Procedência

Três marcadores, válidos para o arquivo inteiro:

- **[FONTE]** — lido no ManimCE **0.21.0** instalado em
  `.venv/lib/python3.12/site-packages/manim/`, ou em `manimx/` deste
  repositório, ou no índice estático de `api/`. Vem com arquivo e linha.
  Afirmação forte.
- **[HOJE]** — reproduzido nesta sessão (2026-08-19) com `grep`, `ast` e Python
  puro. **Nenhum render, nenhum `ffmpeg`, nenhuma GPU.**
- **[DECK]** — medido no deck consumidor `~/Projects/aulas`, em outra sessão.
  Testemunho confiável, não reproduzido aqui.

Onde nada está marcado, é dedução minha a partir do fonte, e está escrito como
dedução.

## Cartão de referência — o sintoma manda na seção

| O que aconteceu | Onde ler |
|---|---|
| "de qual `Scene` eu herdo?" | §1.2 |
| quero fundo/eixos/paleta iguais em todas as cenas | §2.2 e §2.6 |
| `super().setup()` — preciso mesmo? | §2.5 |
| "o fundo branco só pega com DUAS linhas, por quê?" | §2.6 |
| quero passar um parâmetro para a cena | §2.4 |
| o objeto ficou por baixo mesmo depois de `bring_to_front` | §3.8 |
| removi o mobject e ele **voltou** no `play` seguinte | §4.2 |
| o `FadeOut` fez o objeto **aparecer** antes de sumir | §4.3 |
| `clear()` não parou o updater / a malha 3D continuou lá | §3.5 |
| `add_foreground_mobject` e `len(self.mobjects)` cresceu 2 | §3.7 |
| a cena **não aparece** no `mx scenes` | §6.1 |
| a minha classe-base **renderizou sozinha** | §6.2 |
| `bin/manim` ficou **perguntando** qual cena | §6.4 |
| pedi mp4 e saiu **PNG** | §7.1 |
| `self.wait(0)` levantou `ValueError` | §4.6 |
| chamei `next_section` e **não saiu arquivo** | §5.3 |
| o nome do vídeo de seção veio com número errado | §5.5 |
| seção × parte: qual eu uso? | §5.8 |
| quero conferir um arquivo de cena **sem renderizar** | §8.4 |

---

## 1. O mapa: são **7** classes de `Scene`, não 13

### 1.1 A árvore

**[FONTE]** `api/manim-ce-inheritance.txt:318-324` — a hierarquia inteira, sem
podas:

```
Scene
  MovingCameraScene
    ZoomedScene
  ThreeDScene
    SpecialThreeDScene
  VectorScene
    LinearTransformationScene
```

**Correção de contagem que já circulou por aí:** a categoria `scene` do índice
tem **13 classes**, e é fácil confundir isso com "13 classes de cena". As outras
seis não são cenas: `SceneFileWriter` (o escritor de arquivo), `Section` e
`DefaultSectionType` (§5), `RerunSceneHandler`, `SceneInteractContinue` e
`SceneInteractRerun` (o modo interativo do OpenGL). **[HOJE]**, conferido com
`awk -F'\t' '$3=="scene" && $1=="class"' api/manim-ce-index.tsv`.

As sete estão todas em `from manim import *` — **[HOJE]**, conferido com
`hasattr(manim, nome)`. **`EndSceneEarlyException` e `RerunSceneException` não
estão**: para capturá-las é `from manim.utils.exceptions import
EndSceneEarlyException` (§2.3).

### 1.2 De qual eu herdo?

| Você precisa de… | Herde de | Quem ensina |
|---|---|---|
| desenhar e animar em 2D — **o caso normal** | `Scene` | esta skill |
| mover, aproximar ou seguir com a câmera em 2D | `MovingCameraScene` | **`manim-camera-2d`** |
| uma lupa: quadro pequeno mostrando um pedaço ampliado | `ZoomedScene` | **`manim-camera-2d`** |
| `phi`/`theta`, superfície, sólido, órbita | `ThreeDScene` | **`manim-3d-camera`** |
| ~~3D com eixos e esfera já configurados num padrão~~ | ~~`SpecialThreeDScene`~~ — **NÃO USE, está quebrada na 0.21**: `SpecialThreeDScene()` levanta `AttributeError: ... has no attribute 'renderer'` antes do `super().__init__()` | **`manim-3d-camera` §2**, que é dona do diagnóstico |
| plano cartesiano + vetores como assunto da aula | `VectorScene` | **buraco declarado** |
| mostrar uma matriz **deformando o plano** | `LinearTransformationScene` | **buraco declarado** |

**Regra de bolso: herde de `Scene`.** As seis subclasses existem para trocar a
`camera_class` ou para pré-montar um cenário; nenhuma delas dá poder novo de
desenho. Se você só quer um fundo e uma paleta próprios, isso é uma classe-base
**sua** (§2.2), não uma das seis.

`VectorScene` e `LinearTransformationScene` são **buracos declarados** neste
projeto: nenhuma skill ensina álgebra linear de cena. Elas existem, as
assinaturas abaixo estão conferidas, e `bin/mx show LinearTransformationScene`
lista os 28 métodos próprios — mas ninguém aqui documentou o fluxo. Não invente
comportamento: confira antes de escrever.

### 1.3 As assinaturas, conferidas

**[FONTE]** `api/manim-ce-index.tsv`, categoria `scene`:

```python
Scene(renderer=None, camera_class=Camera, always_update_mobjects=False,
      random_seed=None, skip_animations=False) -> None

MovingCameraScene(camera_class=MovingCamera, **kwargs) -> None

ZoomedScene(camera_class=MultiCamera, zoomed_display_height=3,
            zoomed_display_width=3, zoomed_display_center=None,
            zoomed_display_corner=UR, zoomed_display_corner_buff=0.5,
            zoomed_camera_config={'default_frame_stroke_width': 2,
                                  'background_opacity': 1},
            zoomed_camera_image_mobject_config={},
            zoomed_camera_frame_starting_position=ORIGIN,
            zoom_factor=0.15, image_frame_stroke_width=3,
            zoom_activated=False, **kwargs) -> None

ThreeDScene(camera_class=ThreeDCamera, ambient_camera_rotation=None,
            default_angled_camera_orientation_kwargs=None, **kwargs)

SpecialThreeDScene(cut_axes_at_radius=True, camera_config={...},
                   three_d_axes_config={...}, sphere_config={...},
                   default_angled_camera_position={...},
                   low_quality_config={...}, **kwargs)

VectorScene(basis_vector_stroke_width=6.0, **kwargs) -> None

LinearTransformationScene(include_background_plane=True,
                          include_foreground_plane=True,
                          background_plane_kwargs=None,
                          foreground_plane_kwargs=None,
                          show_coordinates=False, show_basis_vectors=True,
                          basis_vector_stroke_width=6,
                          i_hat_color=GREEN_C, j_hat_color=RED,
                          leave_ghost_vectors=False, **kwargs) -> None
```

Repare que **todos os parâmetros têm default**. Isso não é coincidência — é
requisito (§2.4).

**Uma ressalva, e é a exceção que prova a regra:** ter todos os defaults é
necessário, não suficiente. `SpecialThreeDScene` os tem e **mesmo assim não
instancia**: `three_d_scene.py:483` lê `self.renderer.camera_config[...]`
**antes** do `super().__init__()`, e `self.renderer` só passa a existir dentro
de `Scene.__init__` (`scene/scene.py:208-214`). Medido nesta máquina:
`AttributeError: 'SpecialThreeDScene' object has no attribute 'renderer'`. É
exatamente o modo de falha que o §2.4 e a armadilha nº 3 do §9 vigiam — e é a
skill `manim-3d-camera` §2 que documenta a alternativa.

### 1.4 Combinar duas? O conflito é de `camera_class`

`ThreeDScene` e `MovingCameraScene` não se combinam, e agora dá para dizer **por
quê** em vez de repetir a proibição: cada uma existe só para trocar o default de
`camera_class` no `__init__` (**[FONTE]** `scene/moving_camera_scene.py:118-121`
e `scene/three_d_scene.py:37-54`). Num `class X(ThreeDScene, MovingCameraScene)`
o MRO resolve `__init__` na primeira base, `ThreeDCamera` ganha, e a
`MovingCamera` — a única que tem `.frame` — nunca é construída. O sintoma é um
`AttributeError` em `self.camera.frame` **em tempo de execução**, no meio do
render, não na definição da classe.

`ZoomedScene(MovingCameraScene)` é a combinação que a biblioteca faz por dentro,
e ela funciona porque a `MultiCamera` **herda** de `MovingCamera`.

---

## 2. O ciclo de vida

### 2.1 `render()`, linha a linha

**[FONTE]** `scene/scene.py:248-300`. Esta é a espinha de tudo:

```python
def render(self, preview=False) -> bool:
    self.setup()                       # 1
    try:
        self.construct()               # 2
    except EndSceneEarlyException:
        pass                           # 3  -> segue para o tear_down
    except RerunSceneException:
        ...; return True               # 4  -> NÃO chama tear_down
    except BaseException:
        self.renderer.file_writer.abort_encode_jobs()
        raise                          # 5  -> NÃO chama tear_down
    self.tear_down()                   # 6
    self.renderer.scene_finished(self) # 7  -> é aqui que o arquivo fecha
```

Quatro leituras que valem dinheiro:

1. **`setup()` roda sempre, antes do `construct`.** É o gancho de projeto.
2. **`tear_down()` NÃO roda quando a cena levanta exceção.** Se você usa
   `tear_down` para gravar um relatório, um CSV ou uma métrica, ele não sai
   justamente no caso em que você mais precisaria dele. Para limpeza garantida,
   use `try/finally` dentro do próprio `construct`.
3. **`tear_down()` roda quando a cena termina cedo por `-n a,b`** (§7.2) —
   `EndSceneEarlyException` é capturada e cai no fluxo normal.
4. **Quem escreve o arquivo é `scene_finished`, depois do `tear_down`.** Um
   `self.add(...)` dentro do `tear_down` ainda influencia o último frame, e
   portanto o PNG (§7.1).

### 2.2 `setup` × `construct` × `tear_down`

**[FONTE]** as três nascem como `pass` (`scene/scene.py:303`, `:311`, `:319`).
Nenhuma delas faz nada por padrão — o valor está em **onde** você as
implementa.

| | Quando roda | Para que serve | Onde ela mora |
|---|---|---|---|
| `setup()` | antes do `construct`, sempre | o que TODA cena do projeto tem em comum: fundo, paleta, eixos, título | na **classe-base do projeto** |
| `construct()` | o corpo da animação | o conteúdo desta cena | na cena concreta |
| `tear_down()` | depois do `construct`, se não houve exceção | raro. Relatório, asserção final | quase sempre em lugar nenhum |

A separação existe porque `setup` é herdável sem que a subclasse precise se
lembrar de nada: a cena concreta implementa só `construct` e ganha o cenário de
graça. É o padrão que o deck consumidor usa — **[DECK]** `CenaAula(Scene)` em
`aulas/002-deepseek-harness/manim/tema.py:369-385`, importada por 81 classes de
cena (§6.2).

### 2.3 As três exceções de controle

| Exceção | Quem levanta | O que acontece |
|---|---|---|
| `EndSceneEarlyException` | `CairoRenderer.update_skipping_status`, quando `num_plays > upto_animation_number` (**[FONTE]** `renderer/cairo_renderer.py:262-267`) | corta o `construct` no meio, roda `tear_down`, fecha o arquivo normalmente |
| `RerunSceneException` | o modo interativo do OpenGL, quando o arquivo muda em disco (`scene/scene.py:1533,1549`) | limpa a tela, zera `num_plays`, aborta os encodes e devolve `True` para o laço de fora re-renderizar |
| qualquer outra | o seu código | aborta os encodes pendentes e **re-levanta** — sem `tear_down`, sem arquivo final |

**Nenhuma das duas primeiras está em `from manim import *`** (**[HOJE]**). O
comentário de `render()` explica por que o `abort_encode_jobs` existe: uma
exceção no meio de um `play` deixa um *encode job* aberto cujo worker **não é
daemon** e travaria o processo na saída.

### 2.4 A cena é instanciada **sem argumentos** — parametrize por atributo de classe

**[FONTE]**, nos dois caminhos de render desta máquina:

- CE: `cli/render/commands.py:123-125` — `with tempconfig({}): scene =
  SceneClass(); scene.render()`;
- `manimx`: `manimx/render.py:419-431` — `with tempconfig(cfg): ... scene =
  scene_class(); scene.render()`.

Consequência dura: **um `__init__` com parâmetro obrigatório torna a cena
irrenderizável pela CLI**, com um `TypeError` que aparece só na hora do render.
Todo parâmetro precisa de default (§1.3 mostra que a própria biblioteca segue
isso).

A saída idiomática é **atributo de classe**:

```python
class Diagrama(Scene):
    COR = AZUL
    N = 5

    def construct(self):
        for i in range(self.N):
            ...

class DiagramaGrande(Diagrama):
    N = 12
```

É exatamente o mecanismo que `manim-presentation-parts` usa com `PARTE = 3`.
A outra saída é `config`/`tempconfig` (**`manim-render-api` §11**) quando o
parâmetro é de render, não de conteúdo.

**O `tempconfig({})` em volta de cada cena é uma garantia útil:** mexer em
`config` dentro de uma cena **não vaza** para a próxima cena do mesmo processo.
Um `bin/manim -a arquivo.py` com uma cena que faz `config.background_color =
BLACK` no `setup` não escurece as outras.

### 2.5 `super().setup()` — obrigatório em duas das seis

`Scene.setup` é `pass`, então esquecer o `super().setup()` numa subclasse direta
de `Scene` não custa nada. **Em duas subclasses custa a cena inteira:**

- **`ZoomedScene.setup()`** (**[FONTE]** `scene/zoomed_scene.py:110-137`) é
  quem constrói `self.zoomed_camera` e `self.zoomed_display`. Sem
  `super().setup()`, `activate_zooming()` estoura em `AttributeError:
  'X' object has no attribute 'zoomed_camera'`.
- **`LinearTransformationScene.setup()`** (**[FONTE]**
  `scene/vector_space_scene.py:701-730`) cria os planos, os vetores de base e
  **cinco listas de rastreio**. Ela ainda se protege com
  `if hasattr(self, "has_already_setup"): return` — quer dizer que chamá-la duas
  vezes é seguro, mas não chamá-la nenhuma deixa a cena sem `self.plane`,
  `self.i_hat`, `self.j_hat`.

Um detalhe dessa mesma função que morde de lado: ela faz
`self.foreground_mobjects = []`, **jogando fora** a lista que `Scene.__init__`
criou. Se você adicionou algo ao foreground no `__init__` da sua subclasse antes
do `setup`, some.

**Regra:** numa classe-base de projeto, chame `super().setup()` sempre. Custa
uma linha e imuniza a base contra a troca da superclasse depois.

### 2.6 O fundo: por que são **duas** linhas, e não uma

O idioma que o deck usa — **[DECK]** `tema.py:382-385`:

```python
class CenaAula(Scene):
    def setup(self) -> None:
        config.background_color = CANVAS
        self.camera.background_color = CANVAS   # <- esta é a que pinta
        super().setup()
```

Parece redundância defensiva. Não é. **[FONTE]**, a ordem real:

1. `Scene.__init__` constrói o renderer: `CairoRenderer(camera_class=...)`
   (`scene/scene.py:208-217`);
2. `CairoRenderer.__init__` constrói a câmera **na hora**: `self.camera =
   camera_cls()` (`renderer/cairo_renderer.py:48`);
3. `Camera.__init__` lê `config["background_color"]` **uma vez** e guarda em
   `self._background_color` (`camera/camera.py:134-139`);
4. só **depois** disso o `render()` chama `setup()`.

Ou seja: quando o seu `setup()` roda, a câmera **já leu** o config. Mexer em
`config.background_color` ali é tarde demais para ela. As duas linhas fazem
coisas diferentes:

| Linha | Alcança |
|---|---|
| `self.camera.background_color = X` | a câmera **desta** cena — é o que aparece no vídeo |
| `config.background_color = X` | qualquer câmera construída **depois** — inclusive a câmera ampliada que `ZoomedScene.setup()` cria — e a resolução de `background_opacity`/`--transparent` |

E o corolário: **se você quer configurar o fundo uma vez só, faça no `manim.cfg`
ou no topo do módulo** (antes de qualquer instanciação), não no `setup`.

Isso também explica a interação com `--theme`: **[FONTE]** `manimx/render.py:
419-431` aplica o tema dentro do `tempconfig` e **antes** de `scene_class()`,
então o tema alcança a câmera. Mas um `setup()` que escreve
`self.camera.background_color` **sobrescreve o tema** — o que é o
comportamento desejado no deck ("o fundo é branco mesmo sem `--theme`") e é uma
armadilha em qualquer projeto que espere que `--theme` mande.

> Escolher **qual** cor, medir contraste e usar `set_default` é de
> **`manim-color-theming`**. O `tema.py` como contrato de projeto (fonte,
> escala, tempos, dados) é de **`manim-tema-projeto`**. Aqui é só o mecanismo
> de *quando* o valor é lido.

### 2.7 O estado inicial que `Scene.__init__` monta

**[FONTE]** `scene/scene.py:170-224`. Vale conhecer os nomes, porque é neles que
se depura:

```python
self.mobjects: list[Mobject] = []           # a lista de exibição (§3)
self.foreground_mobjects: list[Mobject] = []
self.updaters: list[Callable[[float], None]] = []   # updaters DE CENA
self.meshes: list[Object3D] = []            # só OpenGL
self.animations = None                      # reconstruído a cada play
self.moving_mobjects, self.static_mobjects = [], []
self.random_seed = random_seed if ... else config.seed
random.seed(self.random_seed); np.random.seed(self.random_seed)
```

Mais duas propriedades: `self.camera` é `self.renderer.camera`, e `self.time` é
`self.renderer.time` (`scene/scene.py:227-233`).

---

## 3. A lista de exibição

### 3.1 `self.mobjects` é a única coisa que desenha

Não existe "adicionar à cena" em nenhum outro lugar. Um `Mobject` construído e
posicionado, com cor e opacidade certas, **não aparece** enquanto não estiver
em `self.mobjects` — direta ou indiretamente, como submobject de alguém que
está.

Três portas o colocam lá: `self.add(...)`, `self.play(...)` com uma animação
que o toca (§4.2), e `self.replace(...)`.

### 3.2 `add()` — que na verdade é "mover para a frente"

**[FONTE]** `scene/scene.py:491-533`, ramo cairo:

```python
new_and_foreground_mobjects = [*mobjects, *self.foreground_mobjects]
self.restructure_mobjects(to_remove=new_and_foreground_mobjects)
self.mobjects += new_and_foreground_mobjects
```

Três coisas, todas relevantes:

1. **`add` remove antes de acrescentar.** Adicionar de novo um mobject que já
   está na cena não duplica: **move para o fim da lista**, ou seja, para a
   frente do desenho. É por isso que `bring_to_front` é literalmente
   `self.add(...)` (§3.6).
2. **O foreground é re-empilhado a cada `add`.** Todo `add` reanexa a lista de
   foreground no final, e é assim que o "sempre por cima" funciona (§3.7).
3. **A assinatura devolve `Self`**, então `self.add(a).add(b)` encadeia.

### 3.3 `remove()` e a dissolução de grupos

**[FONTE]** `scene/scene.py:547-583` → `restructure_mobjects` (`:691-732`).

`Scene.remove(x)` não é um `list.remove`. Ele varre a lista **e as famílias**:
se `x` é submobject de um `VGroup` que está na cena, o grupo é **dissolvido** e
os irmãos de `x` sobem para o lugar dele em `self.mobjects`. A docstring do
próprio Manim diz isso em `tl:wr` (sic, `scene.py:698`).

Consequência que surpreende: depois de `self.remove(g[1])`, o `g` **não está
mais na cena** — estão `g[0]` e `g[2]`, soltos. Um `self.play(g.animate.shift(
UP))` depois disso reintroduz `g` inteiro (§4.2), e o `g[1]` volta junto.

`remove()` também limpa `foreground_mobjects` (`scene.py:581-582`) — veja §3.6.

### 3.4 `replace()` — trocar preservando a ordem de desenho

**[FONTE]** `scene/scene.py:585-643`.

```python
self.replace(old_mobject, new_mobject) -> None
```

Substitui **no lugar**, inclusive dentro de um grupo: se `old` é submobject de
um `VGroup`, `new` entra na mesma posição do grupo, sem mexer no resto. É a
ferramenta certa para trocar um rótulo sem que ele salte para a frente do
desenho — o que aconteceria com `remove` + `add`.

Dois comportamentos declarados: levanta **`ValueError`** se `old` não estiver na
cena, e emite um **warning** (sem erro) se `old is new`.

### 3.5 `clear()` — e as três coisas que ele **não** limpa

**[FONTE]** `scene/scene.py:883-897`. O corpo inteiro é:

```python
self.mobjects = []
self.foreground_mobjects = []
return self
```

O que **continua vivo** depois de um `clear()`:

| Sobrevive | Por quê | Sintoma |
|---|---|---|
| `self.updaters` (updaters **de cena**) | a lista nem é tocada | uma função de cena continua rodando a cada frame, sobre objetos que não existem mais na tela → `AttributeError` ou trabalho invisível |
| `self.meshes` | só o ramo OpenGL do `remove` mexe nelas, e `clear` não chama `remove` | malha 3D continua desenhada depois de "limpar a cena" |
| os updaters **dos mobjects** removidos | o updater é um atributo do mobject, não da cena | inofensivo enquanto ele estiver fora (§4.4), volta a rodar assim que ele voltar |

Para zerar de verdade, `clear()` mais `self.updaters.clear()` — e, em 3D
OpenGL, `self.meshes.clear()`.

### 3.6 `bring_to_front` e `bring_to_back`

**[FONTE]** `scene/scene.py:844-881`. Os corpos são de uma linha e meia:

```python
def bring_to_front(self, *mobjects):
    self.add(*mobjects); return self

def bring_to_back(self, *mobjects):
    self.remove(*mobjects)
    self.mobjects = list(mobjects) + self.mobjects
    return self
```

Duas leituras:

- **`bring_to_front` é `add`.** Idênticos. Se um estiver funcionando e o outro
  não, o problema é outro (§3.8).
- **`bring_to_back` DESPROMOVE do foreground, em silêncio.** Ele chama
  `self.remove`, que tira o mobject de `foreground_mobjects` também
  (`scene.py:581-582`), e depois prepende só em `self.mobjects`. O objeto passa
  a ser um mobject comum lá atrás, e o próximo `add` de qualquer coisa **não** o
  reanexa. Nenhum aviso.

### 3.7 `foreground_mobjects` — o mecanismo, e onde ele não funciona

```python
Scene.add_foreground_mobjects(*mobjects) -> Scene
Scene.add_foreground_mobject(mobject)    -> Scene
Scene.remove_foreground_mobjects(*to_remove) -> Scene
Scene.remove_foreground_mobject(mobject)     -> Scene
```

**[FONTE]** `scene/scene.py:772-842`. O corpo de `add_foreground_mobjects` é
`self.foreground_mobjects = list_update(self.foreground_mobjects, mobjects)`
seguido de `self.add(*mobjects)`. Como todo `add` reanexa o foreground no fim
(§3.2), o efeito é: **o foreground volta para o topo a cada `add`, para sempre**,
sem você ter que se lembrar.

Três armadilhas, todas conferidas no fonte (nenhuma executada):

**(a) O objeto fica duplicado em `self.mobjects`.** **[FONTE]**, por leitura — em
`add_foreground_mobject(x)`, quando `self.add(x)` roda, `x` já está em
`foreground_mobjects`; então `new_and_foreground_mobjects == [x, x]`, o
`restructure` tira todas as ocorrências e a soma acrescenta **duas**. Isso é
invisível no vídeo — `extract_mobject_family_members` passa por
`remove_list_redundancies`, que mantém a **última** ocorrência
(`utils/iterables.py:257-266`) — mas é bem visível quando você faz
`len(scene.mobjects)` ou itera a lista num teste. Não "conserte": é assim.

**(b) O `Scene` marca a própria API como provisória.** `scene.py:772` traz
`# TODO, remove this, and calls to this`, e `scene.py:220` traz
`# TODO, remove need for foreground mobjects`. Funciona hoje na 0.21.0; não
construa uma abstração de projeto inteira em cima disso — prefira `z_index`
(§3.8), que é a via estável.

**(c) No renderer OpenGL o foreground é ignorado.** **[FONTE]** O ramo OpenGL de
`Scene.add` (`scene.py:507-518`) não consulta `self.foreground_mobjects` em
nenhum momento: ele só faz `remove` + `+=`. Quer dizer que `add_foreground_*`
**alimenta uma lista que ninguém lê** quando `--renderer opengl`. O objeto vai
para a frente no momento da chamada e perde a posição no próximo `add`.

`LinearTransformationScene` tem um **`add_foreground_mobject` próprio, com outra
assinatura e outra semântica** — `(*mobjects) -> None`, contra
`(mobject) -> Scene` da base (**[HOJE]**, `api/manim-ce-methods.tsv`). Se você
herdou dela, não é o método que você leu aqui.

### 3.8 A ordem de desenho de verdade: **z-index vence ordem de `add`**

Este é o item que mais custa tempo, porque a explicação usual ("desenha na ordem
em que foi adicionado") está **incompleta**.

**[FONTE]**, o caminho completo:

1. `Camera.__init__` tem `use_z_index: bool = True` (`camera/camera.py:91,108`);
2. `Camera.get_mobjects_to_display` chama `extract_mobject_family_members(
   mobjects, use_z_index=self.use_z_index, only_those_with_points=True)`
   (`camera/camera.py:448-482`) — e é `Camera.capture_mobjects` que a invoca,
   em `:554`, a cada frame;
3. `extract_mobject_family_members` achata a árvore, tira redundâncias e, se
   `use_z_index`, faz `sorted(extracted, key=lambda m: m.z_index)`
   (`utils/family.py:41-42`).

Então a regra é:

> **A ordem de desenho é `z_index` crescente. Dentro do mesmo `z_index`, a
> ordem de `self.mobjects` decide** — porque `sorted` é estável.

Como todo mobject nasce com `z_index = 0`, quase sempre a ordem de `add` manda,
e é por isso que a explicação simplificada quase sempre funciona. Ela quebra
exatamente no caso em que você está depurando: alguém pôs `z_index=1` em algum
lugar, e agora **`bring_to_front` não faz nada visível**. Nenhum erro.

O diagnóstico é de duas linhas, sem render:

```python
for m in self.mobjects:
    print(f"{m.z_index:>3}  {type(m).__name__}")
```

> Ajustar `z_index` como decisão de layout é de
> **`manim-layout-posicionamento`**. Aqui interessa só o fato de que ele **vem
> antes** da lista da cena.

### 3.9 Consultar a cena

```python
Scene.get_top_level_mobjects()     -> list[Mobject]   # os que não são família de outro
Scene.get_mobject_family_members() -> list[Mobject]   # tudo, achatado (e com z-index no cairo)
Scene.get_attrs(*keys: str)        -> list[Any]       # [getattr(self, k) for k in keys]
```

**[FONTE]** `scene/scene.py:448-489` e `:367-381`.

`get_top_level_mobjects` faz um `O(n²)` sobre as famílias — bom para um
`print` de depuração, ruim dentro de um updater.

`get_mobject_family_members` é o que a cena usa para decidir "este mobject já
está na tela?" em `add_mobjects_from_animations` (§4.2). Se você quer testar
presença você mesmo, é ele — e **não** `x in self.mobjects`, que só enxerga o
topo.

---

## 4. O que sobrevive entre um `play` e o outro

### 4.1 A tabela

**[FONTE]** `scene/scene.py:1292-1340` (`compile_animation_data` /
`begin_animations`) e `:1364-1397` (`play_internal`).

| Estado | Sobrevive ao `play`? |
|---|---|
| `self.mobjects`, `self.foreground_mobjects` | **sim** — é o ponto |
| `self.updaters` (de cena) | **sim** |
| updaters dos mobjects | **sim** |
| `self.meshes` | **sim** |
| `self.time` (= `renderer.time`) | **sim**, monotônico |
| `renderer.num_plays` | **sim**, monotônico — é o índice do `-n a,b` |
| atributos que você pôs em `self` | **sim** |
| `self.animations` | **não** — reescrito a cada `play` |
| `self.moving_mobjects` / `self.static_mobjects` | **não** — zerados e recalculados |
| `self.stop_condition`, `self.duration`, `self.last_t` | **não** |
| `renderer.static_image` | **não** — vira `None` no fim de cada `play` |
| a semente aleatória | **fixada uma vez** no `__init__`, nunca reposta |

A última merece nota: `random.seed(...)` e `np.random.seed(...)` rodam no
`Scene.__init__` (`scene.py:223-224`), com `config.seed`. Duas cenas do mesmo
arquivo começam do mesmo estado aleatório; dois `play` da mesma cena, não.

### 4.2 `play()` **re-adiciona sozinho** o que você removeu

**[FONTE]** `scene/scene.py:535-545`, chamado de dentro de
`compile_animation_data`:

```python
def add_mobjects_from_animations(self, animations):
    curr_mobjects = self.get_mobject_family_members()
    for animation in animations:
        if animation.is_introducer():
            continue
        mob = animation.mobject
        if mob is not None and mob not in curr_mobjects:
            self.add(mob)
```

Leia como uma regra: **animar um mobject o coloca na cena.** Não há exceção
salvo as animações marcadas como *introducer*, que se adicionam sozinhas depois
(`animation/animation.py:244-261`).

Daí o defeito clássico:

```python
self.remove(rotulo)
self.play(rotulo.animate.shift(UP))   # rotulo VOLTA para a tela, cheio
```

Se a intenção era mover algo fora de cena para reintroduzir depois, mexa no
mobject direto (`rotulo.shift(UP)`), sem `play`.

### 4.3 *Introducer* × *remover* — e o `FadeOut` que faz o objeto **aparecer**

**[FONTE]** `animation/animation.py:229-261`, `animation/fading.py:137,185`.

- `FadeIn` é construído com `introducer=True`: `_setup_scene` faz o `add` no
  começo.
- `FadeOut` é construído com `remover=True`: `clean_up_from_scene` faz o
  `remove` no fim.

Junte com §4.2 e sai a armadilha: **`self.play(FadeOut(x))` com `x` fora da
cena faz `x` APARECER opaco e depois desaparecer.** Porque `FadeOut` não é
introducer, `add_mobjects_from_animations` o adiciona; a animação então o
apaga a partir da opacidade cheia. Um piscar de 0,5 s que ninguém consegue
explicar olhando só a linha do `play`.

O mesmo mecanismo, do outro lado, é o que faz `ReplacementTransform` deixar o
alvo na cena e o original fora: `Transform.clean_up_from_scene` troca os dois
quando `replace_mobject_with_target_in_scene=True`
(`animation/transform.py:219-224`).

> Qual animação usar, e `Transform` × `ReplacementTransform`, é de
> **`manim-animations`**. Aqui está só o efeito colateral na **lista da cena**.

### 4.4 Updaters de cena × updaters de mobject

```python
Scene.add_updater(func: Callable[[float], None]) -> None
Scene.remove_updater(func: Callable[[float], None]) -> None
Scene.update_self(dt) -> None      # roda os updaters de cena
Scene.update_mobjects(dt) -> None  # roda os updaters dos mobjects
```

**[FONTE]** `scene/scene.py:645-690`, `:383-394`, `:400-417`. Três fatos:

1. **Os de cena rodam por último.** A docstring de `update_self` é explícita:
   "*scene update functions are called last*".
2. **`update_mobjects` só percorre `self.mobjects`.** Um mobject removido da
   cena para de receber `dt` — o updater não é destruído, só não é chamado.
3. **O aviso oficial contra updater de cena, no cairo** (`scene.py:651-660`):
   *"scene updaters that modify mobjects are not detected in the same way that
   mobject updaters are… TL;DR: Use mobject updaters to update mobjects."* O
   motivo é o particionamento móvel/estático de `begin_animations`
   (`scene.py:1349-1353`): o cairo pinta os estáticos uma vez e reaproveita o
   bitmap. Um objeto mexido só por updater de cena pode ficar classificado como
   estático e **congelar no vídeo**, sem erro nenhum.

`Scene.add_updater` é para o que **não é** mobject: um cronômetro, um contador,
um log. Para mobject, use `Mobject.add_updater` — assunto de
**`manim-updaters-valuetracker`**.

### 4.5 Tempo, e o `wait` congelado que é truncado ao frame

`self.time` é `renderer.time` e avança de três formas (**[FONTE]**
`renderer/cairo_renderer.py:53,78,97,194`): pelo `duration` quando a animação é
pulada, pelo `duration` quando ela vem do cache, e por `num_frames * dt` quando
frames são realmente escritos.

Um `wait` sem updaters vira **frame congelado**: `Scene.should_update_mobjects`
(`scene.py:419-446`) decide isso sozinho, e o renderer chama
`freeze_current_frame(duration)` (`cairo_renderer.py:197-209`), que faz

```python
self.add_frame(self.get_frame(), num_frames=int(duration / dt))
```

O `int()` **trunca**. A 60 fps, `self.wait(0.25)` dá exatamente 15 frames;
`self.wait(0.26)` dá `int(15.6) = 15` — a mesma coisa. Pausas ficam quantizadas
para baixo, em passos de 1/fps. Isso é irrelevante numa pausa de 1,4 s e é
exatamente o tamanho do erro quando alguém tenta afinar uma cauda de 0,25 s.

`Scene.pause(duration)` é açúcar para `wait(duration, frozen_frame=True)`
(`scene.py:1258-1274`), e `Wait` levanta `ValueError` se você combinar
`stop_condition` com `frozen_frame` (`animation/animation.py:615-616`).

### 4.6 `wait(0)` levanta — e o `wait` curto demais é silenciosamente esticado

**[FONTE]** `Scene.validate_run_time` (`scene.py:1113-1139`), um `classmethod`:

- `run_time <= 0` → **`ValueError`**. `self.wait(0)` não é um no-op, é um erro.
- `run_time < 1/fps` → **warning** e o valor é **elevado** para `1/fps`.

E `Scene.get_run_time(animations)` devolve o **máximo**, não a soma
(`scene.py:1141-1158`) — porque quem compõe em sequência é o `AnimationGroup`.

> Quanto tempo, que curva, em que ordem: **`manim-composicao-ritmo`**.

### 4.7 O `play` com zero animações

`compile_animation_data` levanta `ValueError("Called Scene.play with no
animations")` (`scene.py:1318`). Um `self.play(*lista)` com a lista vazia
— caso comum em código gerado por laço — derruba a cena inteira. Guarde com
`if lista:`.

---

## 5. Seções — `next_section` e a Segmented Video API

### 5.1 As assinaturas

**[FONTE]** `api/manim-ce-index.tsv` e `api/manim-ce-methods.tsv`:

```python
Scene.next_section(name: str = 'unnamed',
                   section_type: str = DefaultSectionType.NORMAL,
                   skip_animations: bool = False) -> None

Section(type_: str, video: str | None, name: str, skip_animations: bool)
Section.is_empty() -> bool
Section.get_clean_partial_movie_files() -> list[str]
Section.get_dict(sections_dir: Path) -> dict[str, Any]

DefaultSectionType            # StrEnum com UM membro: NORMAL = "default.normal"

SceneFileWriter.next_section(name: str, type_: str, skip_animations: bool) -> None
SceneFileWriter.finish_last_section() -> None
SceneFileWriter.combine_to_section_videos() -> None
```

**Correção:** uma versão anterior falava numa "inversão" entre os dois — que o
`Scene` teria `name` na primeira posição e o `SceneFileWriter`, `type_`. Não
existe: nos dois, `name` é o primeiro. A divergência real é na **segunda**
posição e nos **defaults**:

```
Scene.next_section          (name='unnamed', section_type=DefaultSectionType.NORMAL, skip_animations=False)
SceneFileWriter.next_section(name,           type_,                                  skip_animations)
```

O segundo parâmetro muda de **nome** (`section_type` → `type_`) e o método
interno **não tem default nenhum** — os três são obrigatórios. Você nunca o
chama direto, mas vai lê-lo num traceback, e é ali que o nome diferente
confunde.

### 5.2 O caminho do código

**[FONTE]**, na ordem:

1. `Scene.next_section(...)` (`scene/scene.py:352-363`) só delega para
   `self.renderer.file_writer.next_section(name, section_type, skip_animations)`;
2. `SceneFileWriter.next_section` (`scene_file_writer.py:332-356`) fecha a
   seção anterior, decide se a nova terá arquivo, e empilha um `Section`;
3. cada `play` seguinte acrescenta o *partial movie* à seção corrente
   (`add_partial_movie_file`, `:359-383`) — inclusive um `None` quando a
   animação foi pulada, para manter o índice alinhado com `num_plays`;
4. no fim, `finish()` chama `combine_to_section_videos()` se
   `config.save_sections` (`:623-624`);
5. `combine_to_section_videos` (`:1040-1054`) concatena os partials de cada
   seção e grava um índice JSON.

### 5.3 Os **quatro** requisitos para uma seção virar arquivo

Este é o ponto que mais gera "chamei `next_section` e não saiu nada". **[FONTE]**
`scene_file_writer.py:337-346` — o `section_video` só recebe um nome se **todas**
estas forem verdade:

```python
not config.dry_run  and  write_to_movie()  and  config.save_sections
and  not skip_animations
```

| Requisito | Como falha na prática |
|---|---|
| `config.save_sections` | **default `False`** (`_config/default.cfg:41-42`). Sem `--save_sections` ou `save_sections=True`, `next_section` não escreve nada — ele só marca o corte |
| `write_to_movie()` | é `False` quando o formato é `png` (`utils/file_ops.py:110-122`). O comentário no fonte é literal: *"images don't support sections"* |
| `not config.dry_run` | `--dry_run` não escreve nada, por definição |
| `not skip_animations` | uma seção pulada não vira arquivo — e isso é o que torna o formato em partes possível (§5.8) |

**Se nenhum dos quatro falhou e ainda assim não saiu arquivo**, veja §5.5: a
seção pode ter sido descartada por estar vazia.

### 5.4 O nome do arquivo e o índice JSON

**[FONTE]** `scene_file_writer.py:346`:

```python
section_video = f"{self.output_name}_{len(self.sections):04}_{name}{config.movie_file_extension}"
```

`MinhaCena` com uma seção chamada `intro` na terceira posição vira
`MinhaCena_0002_intro.mp4`. Tudo isso vai para `sections_dir`, que nesta
máquina é o default `{video_dir}/sections` (**[HOJE]**: `manim.cfg` deste
projeto **não** redefine `sections_dir`; o valor vem de
`_config/default.cfg:90`) — ou seja
`media/videos/<módulo>/1080p60/sections/`.

Ao lado dos mp4 sai `{output_name}.json` (`:1053-1054`), a lista de dicionários
de `Section.get_dict`: `name`, `type`, `video`, mais os metadados do vídeo lidos
por `get_video_metadata`. **É esse JSON que um sistema de apresentação de
terceiros consome** — é para isso que a API existe.

`manimx.render_scene(save_sections=True)` devolve os arquivos em
`RenderResult.sections`, mas com uma ressalva conferida: ele faz
`sorted(Path(sec_dir).glob("*.mp4"))` (`manimx/render.py:447`) — **em `webm` ou
`mov` a lista sai vazia** mesmo com as seções gravadas.

### 5.5 A seção vazia some, e a numeração escorrega

**[FONTE]** `scene_file_writer.py:327-331`:

```python
def finish_last_section(self):
    if len(self.sections) and self.sections[-1].is_empty():
        self.sections.pop()
```

`next_section` chama isso **antes** de empilhar a nova. Consequência: dois
`next_section` seguidos, sem nenhum `play` entre eles, **descartam o primeiro**.
E como o número no nome do arquivo é `len(self.sections)`, todas as seções
seguintes andam uma casa para trás.

Sintoma típico: você conta seis `next_section` no `construct`, e o disco tem
cinco arquivos numerados de `_0000` a `_0004`. Não é bug do Manim; foi uma
seção que não recebeu animação nenhuma.

### 5.6 A seção `autocreated`

**[FONTE]** `scene_file_writer.py:243-248`: o construtor do escritor já cria uma
seção, com o nome literal `"autocreated"`. Ela existe para que o primeiro `play`
tenha onde cair.

Junte com §5.5 e saem os dois casos:

- `construct` **começa** com `self.next_section("intro")` → a `autocreated` está
  vazia, é descartada, e `intro` fica com o índice `0000`;
- `construct` toca alguma coisa **antes** do primeiro `next_section` → a
  `autocreated` sobrevive e vira `MinhaCena_0000_autocreated.mp4`.

O comentário no fonte diz exatamente isso: *"if you need the first section to be
skipped, add a first section by hand, it will replace this one"*.

### 5.7 `skip_animations` — o que garante e o que não

`next_section(..., skip_animations=True)` marca a seção; o renderer lê essa
marca no começo de **cada** `play` e liga o seu próprio `skip_animations`
(**[FONTE]** `renderer/cairo_renderer.py:70-71` e `:253-254`).

Ligado, o `play` **executa a lógica da animação até o estado final** e apenas
não escreve frames (`cairo_renderer.py:74-77`): o hash vira `None`, o partial
movie vira `None`, e `renderer.time` avança pelo `duration`. É por isso que o
estado do palco nunca diverge entre uma renderização parcial e a completa — e
é por isso que pular seções **não é de graça**: custa a passagem inteira pela
lógica da cena, economizando só a rasterização e o encode.

**Não confunda com `Scene(skip_animations=True)`.** O parâmetro do construtor
desliga a escrita da cena **inteira** (`cairo_renderer.py:49-50`,
`_original_skipping_status`) e é restaurado no início de todo `play`. Quem corta
por trecho é o `next_section`.

### 5.8 Seção × parte — a fronteira com `manim-presentation-parts`

Existem dois usos completamente diferentes do mesmo `next_section`, e confundir
os dois é o erro de arquitetura mais caro desta área:

| | **Seções** (esta skill) | **Partes** (`manim-presentation-parts`) |
|---|---|---|
| como se dispara | `--save_sections` num render só | N renders, um por classe `P1..PN`, cada um com `PARTE = n` |
| o que sai | N mp4 + um `.json` de índice, nomes gerados pela biblioteca | N mp4 com o nome que **você** escolheu |
| custo | **uma** passagem pela cena | **N** passagens (a lógica roda inteira em todas) |
| re-renderizar um trecho só | não dá: é tudo ou nada | dá, e é o motivo do formato existir |
| para que serve | exportar um índice para um sistema de apresentação de terceiros | um deck em que o apresentador avança com a seta e fala sobre o frame parado |

**Escolha por aqui:** se você renderiza uma vez e nunca mais mexe,
`--save_sections` é mais barato e mais simples. Se você vai **editar o ato 5
amanhã** e não quer refazer os outros oito, é o formato em partes — e aí a skill
é `manim-presentation-parts`, que é dona do mixin, da ordem das bases, da
granulação por recado falado e da métrica da emenda.

### 5.9 Como disparar seções nesta máquina

**[FONTE]** `manimx/cli.py:453-476` — **o `mx render` não expõe
`--save_sections`.** As duas portas que funcionam:

```bash
bin/manim --save_sections -qh cena.py MinhaCena
```

```python
from manimx import render_scene
r = render_scene("cena.py", "MinhaCena", save_sections=True)
print(r.sections)      # lista de Path, só .mp4 (§5.4)
```

> Escolher qualidade, formato e descobrir o caminho do arquivo é de
> **`manim-render-api`**.

---

## 6. Descoberta: quais classes o Manim considera "cena"

### 6.1 Os dois filtros, lado a lado

**[FONTE]**, e eles **não são iguais**:

```python
# ManimCE — manim/utils/module_ops.py:76-81
inspect.isclass(obj) and issubclass(obj, Scene) and obj != Scene \
    and obj.__module__.startswith(module.__name__)

# manimx (bin/mx) — manimx/render.py:141-145
issubclass(obj, Scene) and obj.__module__ == module_name
```

| Diferença | Efeito |
|---|---|
| `startswith` × `==` | irrelevante em 99% dos casos; o CE aceitaria uma classe de um submódulo cujo nome comece igual |
| `obj != Scene` explícito no CE | no `mx` isso é desnecessário: `Scene` importado de `manim` tem outro `__module__` |
| ordenação | o CE usa `inspect.getmembers`, que devolve **em ordem alfabética**; o `mx` ordena por **linha de definição** (`render.py:147`) |

Essa última tem consequência prática: **`bin/manim -a arquivo.py` renderiza em
ordem alfabética**, `P10` antes de `P2`. O `mx scenes` lista na ordem do
arquivo. Se um script seu depende da ordem, ele depende de qual das duas portas
usou.

### 6.2 As quatro consequências

**1. Uma classe que não herda de `Scene` é invisível.** É o alicerce do padrão
mixin: `class _Atos:` com os métodos e `class P1(_Atos, CenaAula):` como cena.
O mixin não aparece em lista nenhuma e não é renderizado. Se ele herdasse de
`Scene`, seria listado e renderizado por engano.

**[HOJE]**, medido no deck consumidor com o conferidor de §8.4, sem importar
manim: **11 arquivos, 81 classes renderizáveis, 10 mixins invisíveis.** Zero
mixins vazando.

**2. Uma classe importada não conta.** `from tema import CenaAula` no topo do
arquivo de cena: `CenaAula.__module__` é `"tema"`, não bate com o módulo do
arquivo, e ela **não** é renderizada — mesmo herdando de `Scene`. É por isso que
uma classe-base de projeto pode herdar de `Scene` sem virar cena, **desde que
more em outro arquivo**.

**3. A base definida NO MESMO arquivo vira cena.** Este é o erro que produz o
mp4 de 35 s que ninguém pediu:

```python
# aula.py  —  ERRADO
class Base(Scene):          # <- é renderizada junto, e ninguém percebe
    def construct(self): ...
class P1(Base): ...
```

Duas saídas: mover `Base` para outro arquivo, ou não fazê-la herdar de `Scene`
(mixin puro).

**4. O nome com underscore não protege.** Não existe filtro por convenção de
nome; `_Base(Scene)` no mesmo arquivo é cena do mesmo jeito.

### 6.3 `parse_module_attributes` **não** é descoberta de cena — correção

Aparece em listas de "funções de descoberta" e **não serve para isso**.
**[FONTE]** `manim/utils/docbuild/module_parsing.py:62`: a assinatura é
`parse_module_attributes() -> tuple[AliasDocsDict, DataDict, TypeVarDict]` —
**sem argumento nenhum** — e ela varre o código-fonte do próprio Manim atrás de
`TypeAlias` e `TypeVar` para a construção da documentação. Não recebe o seu
arquivo, não devolve cenas.

As funções de verdade, todas em `manim/utils/module_ops.py`:

```python
get_module(file_name: Path) -> types.ModuleType
get_scene_classes_from_module(module) -> list[type[Scene]]
get_scenes_to_render(scene_classes) -> list[type[Scene]]
prompt_user_for_choice(scene_classes) -> list[type[Scene]]
scene_classes_from_file(file_path, require_single_scene=False, full_list=False)
```

### 6.4 O prompt interativo, e como não cair nele

**[FONTE]** `module_ops.py:86-108`. `get_scenes_to_render` decide assim:

1. `--write_all` → todas;
2. os nomes passados na linha de comando que existirem;
3. se sobrou vazio **e o arquivo tem exatamente uma cena** → essa uma;
4. senão → **`prompt_user_for_choice`**, que imprime a lista numerada e **fica
   esperando você digitar no terminal**.

Num agente ou num script de CI, o passo 4 é o processo travado sem sintoma. As
duas defesas: passe sempre o nome da cena, ou use `bin/mx render`, que levanta
`ValueError` listando as cenas em vez de perguntar (é o comportamento
documentado em **`manim-render-api` §1**).

Um efeito colateral do prompt vale registrar: ele faz
`SceneFileWriter.force_output_as_scene_name = True` (`module_ops.py:115`), o que
**ignora um `-o` que você tenha passado**.

---

## 7. Cena que não escreve o que você esperava

### 7.1 Cena sem nenhum `play` sai em **PNG**, não em mp4

**[FONTE]** `renderer/cairo_renderer.py:271-283`:

```python
def scene_finished(self, scene):
    if self.num_plays:
        self.file_writer.finish()
    elif config.write_to_movie:
        config.save_last_frame = True       # <- troca o formato na sua cara
        config.write_to_movie = False
    ...
    if config["save_last_frame"]:
        ...
        self.file_writer.save_image(self.camera.get_image())
```

Uma cena feita só de `self.add(...)`, sem um `self.play` sequer, **não produz
mp4**. O Manim decide sozinho que aquilo é uma imagem, e escreve um PNG. Exit
code 0, nenhum aviso destacado, e `RenderResult.output_file` vem `None` com
`image_file` preenchido.

Se você quer mp4 de uma cena estática, dê a ela um `self.wait(1)` — que é um
`play` de `Wait` (§4.5) e faz `num_plays` valer 1.

### 7.2 `-n a,b` corta por `num_plays`, e o corte é uma exceção

**[FONTE]** `_config/utils.py:811-815` mapeia `-n a,b` para
`from_animation_number = a` e `upto_animation_number = b`. O renderer confere no
começo de cada `play` (`cairo_renderer.py:253-267`):

- abaixo de `a` → pula (executa a lógica, não escreve frame);
- acima de `b` → liga o skip e **levanta `EndSceneEarlyException`**, que corta o
  `construct` no meio (§2.3).

Duas leituras: o índice é o de **`play`**, não o de linha nem o de seção; e o
código que vinha **depois** no `construct` simplesmente não roda — incluindo
qualquer `next_section` que estivesse lá.

### 7.3 `-s` / `save_last_frame` desliga todos os plays

`update_skipping_status` liga `skip_animations` incondicionalmente quando
`config["save_last_frame"]` (`cairo_renderer.py:255-256`). Nenhuma animação é
escrita; a cena roda inteira, e só o frame final é gravado. É por isso que `-s`
é barato **em encode** e não é barato **em CPU**: a lógica da cena roda toda.

---

## 8. Receitas

### 8.1 A classe-base de projeto

O esqueleto, com as decisões de §2.5 e §2.6 embutidas. Baseado no
**[DECK]** `aulas/002-deepseek-harness/manim/tema.py:369-385`, enxuto:

```python
# tema.py  — MORA EM OUTRO ARQUIVO, senão vira cena (§6.2)
from manim import Scene, config

CANVAS = "#FFFFFF"

class CenaBase(Scene):
    def setup(self) -> None:
        config.background_color = CANVAS        # alcança o que vier depois
        self.camera.background_color = CANVAS   # alcança ESTA câmera (§2.6)
        super().setup()                          # nunca custa, um dia salva
```

```python
# cena.py
from tema import CenaBase          # importada => NÃO é listada como cena

class Abertura(CenaBase):
    def construct(self):
        ...
```

### 8.2 Cena parametrizada (sem tocar no `__init__`)

```python
class Grade(Scene):
    COLUNAS = 3          # a CLI instancia com Grade(), sem argumentos (§2.4)

    def construct(self):
        for i in range(self.COLUNAS):
            self.add(Square().shift(RIGHT * i))

class GradeLarga(Grade):
    COLUNAS = 8
```

### 8.3 Seções nomeadas para um índice JSON

```python
class Aula(Scene):
    def construct(self):
        self.next_section("abertura")     # descarta a 'autocreated' (§5.6)
        self.play(...)

        self.next_section("desenvolvimento")
        self.play(...)

        self.next_section("fecho")
        self.play(...)
        self.wait(0.4)                    # o wait pertence à seção que TERMINA
```

```bash
bin/manim --save_sections -qh aula.py Aula
ls media/videos/aula/1080p60/sections/
# Aula_0000_abertura.mp4  Aula_0001_desenvolvimento.mp4
# Aula_0002_fecho.mp4     Aula.json
```

Se algum arquivo faltar, a ordem de investigação é §5.3 (os quatro requisitos) →
§5.5 (seção vazia descartada).

### 8.4 Conferir um arquivo de cena **sem importar manim e sem renderizar**

O script abaixo lê o `.py` com `ast`, resolve as classes-base que vêm de módulos
**irmãos** (o `tema.py` ao lado), e responde às duas perguntas que custam um
render: *quais classes o Manim vai renderizar* e *alguma delas tem `__init__`
com argumento obrigatório* (§2.4). **[HOJE]** — rodado sobre os 11 arquivos de
cena do deck consumidor: 81 cenas, 10 mixins, nenhum falso positivo.

```python
#!/usr/bin/env python3
"""Quais classes deste arquivo o Manim vai renderizar — sem importar manim."""
import ast, sys
from pathlib import Path

def nome_da_base(no):
    if isinstance(no, ast.Name):      return no.id
    if isinstance(no, ast.Attribute): return no.attr
    return ast.unparse(no)

def colhe(caminho: Path, vistos: set) -> dict[str, list[str]]:
    """{classe: [bases]} deste arquivo e dos módulos IRMÃOS que ele importa."""
    caminho = caminho.resolve()
    if caminho in vistos or not caminho.is_file():
        return {}
    vistos.add(caminho)
    arv = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    tabela = {n.name: [nome_da_base(b) for b in n.bases]
              for n in arv.body if isinstance(n, ast.ClassDef)}
    for n in ast.walk(arv):
        if isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
            irmao = caminho.parent / f"{n.module.split('.')[0]}.py"
            for k, v in colhe(irmao, vistos).items():
                tabela.setdefault(k, v)
    return tabela

def main(alvo: str) -> int:
    arquivo = Path(alvo)
    tabela = colhe(arquivo, set())
    locais = {n.name: n for n in ast.parse(arquivo.read_text()).body
              if isinstance(n, ast.ClassDef)}

    def eh_cena(classe: str) -> bool:
        fila, vistas = list(tabela.get(classe, [])), set()
        while fila:
            b = fila.pop()
            if b in vistas:
                continue
            vistas.add(b)
            if b == "Scene" or b.endswith("Scene"):
                return True
            fila += tabela.get(b, [])
        return False

    problemas = 0
    for nome, no in locais.items():
        cena = eh_cena(nome)
        print(f"{'CENA ' if cena else 'mixin'} {nome:32s} "
              f"({', '.join(tabela[nome]) or '—'})")
        if not cena:
            continue
        for corpo in no.body:
            if isinstance(corpo, ast.FunctionDef) and corpo.name == "__init__":
                a = corpo.args
                obrig = len(a.args) - 1 - len(a.defaults)
                if obrig > 0:
                    print(f"      !! __init__ exige {obrig} argumento(s) — "
                          f"o CLI chama {nome}() sem nenhum")
                    problemas += 1
    return 1 if problemas else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
```

**Limite honesto:** é análise sintática. Ele resolve `from tema import CenaBase`
quando `tema.py` está ao lado, e **não** resolve `from pacote.sub import X`,
`import *`, nem base construída dinamicamente. Quando ele discordar do
`bin/mx scenes ARQUIVO.py --json`, **quem tem razão é o `mx`** — ele importa de
verdade. O conferidor serve para o caso em que importar é caro ou impossível
(dependência faltando, cena que lê dado externo no import).

---

## 9. Armadilhas, consolidadas

Todas silenciosas — nenhuma levanta exceção, salvo onde escrito.

| # | Armadilha | Onde | Sintoma |
|---|---|---|---|
| 1 | `config.background_color` no `setup` é tarde para a câmera | §2.6 | fundo continua preto |
| 2 | `tear_down` não roda se a cena levanta exceção | §2.1 | relatório/limpeza some justo quando falha |
| 3 | `__init__` com argumento obrigatório | §2.4 | `TypeError` só na hora do render |
| 4 | esquecer `super().setup()` em `ZoomedScene`/`LinearTransformationScene` | §2.5 | `AttributeError` em `zoomed_camera` / `plane` |
| 5 | `bring_to_front` perde para um `z_index` maior | §3.8 | objeto continua por baixo, sem erro |
| 6 | `bring_to_back` **desfaz** o foreground | §3.6 | o "sempre por cima" para de valer |
| 7 | `clear()` não limpa updaters de cena nem `meshes` | §3.5 | trabalho invisível, malha 3D fantasma |
| 8 | foreground é **ignorado** no renderer OpenGL | §3.7 | funciona em cairo, quebra em `--renderer opengl` |
| 9 | `add_foreground_mobject` duplica o mobject em `self.mobjects` | §3.7 | contagem errada em teste/inspeção (invisível no vídeo) |
| 10 | `play` re-adiciona o mobject que você removeu | §4.2 | ele "volta sozinho" |
| 11 | `FadeOut` de algo fora da cena faz o objeto **aparecer** | §4.3 | um piscar inexplicável |
| 12 | updater de cena mexendo em mobject, no cairo | §4.4 | o objeto congela no vídeo |
| 13 | `self.wait(0)` levanta `ValueError` | §4.6 | **este dá erro** |
| 14 | `self.play(*[])` levanta `ValueError` | §4.7 | **este dá erro** |
| 15 | `next_section` sem `--save_sections` não escreve nada | §5.3 | "chamei e não saiu arquivo" |
| 16 | seção vazia é descartada e a numeração escorrega | §5.5 | 6 chamadas, 5 arquivos, índices "errados" |
| 17 | classe-base que herda de `Scene` **no mesmo arquivo** | §6.2 | mp4 longo que ninguém pediu |
| 18 | `bin/manim` sem nome de cena **pergunta no terminal** | §6.4 | agente/CI travado sem sintoma |
| 19 | cena sem nenhum `play` sai em PNG | §7.1 | "cadê o mp4?" com exit 0 |
| 20 | `-n a,b` mata o resto do `construct` via exceção | §7.2 | seções e `wait` finais somem |
| 21 | `interactive_embed()` no cairo levanta `AssertionError`; com `--format` ou `-w` ele **desiste com um warning** | `scene.py:1399-1428` | o embed "não abre" e ninguém lê o log |

---

## 10. Onde esta skill para

| A pergunta é… | Vá para |
|---|---|
| cena de PALESTRA cortada em partes que o apresentador avança; o mixin `_Atos`, a ordem das bases, a emenda | **`manim-presentation-parts`** |
| qualidade, formato, `-n a,b`, `-s`, onde o arquivo foi parar, `--json` | **`manim-render-api`** |
| `run_time`, `rate_func`, `lag_ratio`, `AnimationGroup`, `LaggedStart`, `ChangeSpeed`, `path_func` | **`manim-composicao-ritmo`** |
| qual classe de animação usar, `.animate`, `Transform` × `ReplacementTransform` | **`manim-animations`** |
| `ValueTracker`, `always_redraw`, updaters **de mobject**, contador | **`manim-updaters-valuetracker`** |
| `self.camera.frame`, zoom e pan em 2D, `activate_zooming` | **`manim-camera-2d`** |
| `phi`/`theta`/`gamma`, `move_camera`, `add_fixed_in_frame_mobjects`, superfícies | **`manim-3d-camera`** |
| `z_index` como decisão de camada, margem, "cabe na tela?", `arrange` | **`manim-layout-posicionamento`** |
| `VGroup` × `Group`, árvore de submobjects, qual classe desenha o quê | **`manim-mobjects`** |
| paleta, contraste, `set_default`, "o texto sumiu no fundo branco" | **`manim-color-theming`** |
| o `tema.py` como contrato do projeto (fonte, escala, tempos, dados) | **`manim-tema-projeto`** |
| `add_sound`, `add_subcaption`, `.srt` | **`manim-som-legendas`** |
| o hash do cache, `--no-cache`, custo de rasterizar, `max_files_cached` | **`manim-performance-cache`** |
| codec, NVENC, peso do arquivo, "está lento" no encode | **`manim-gpu-encoding`** |
| renderizar muitas cenas em paralelo, CI | **`manim-batch-pipeline`** |
| olhar o frame e julgar se ficou bom | **`manim-verificacao-visual`** |
| traceback, ambiente quebrado, LaTeX, bissecção | **`manim-troubleshooting`** |
| achar nome, assinatura ou kwarg de qualquer API | **`manim-api-discovery`** |
| ambiente, wrappers `bin/`, ficha da máquina, roteamento geral | **`manim-project`** |

### Buracos declarados que tocam esta skill

Diga que a área não tem guia em vez de improvisar:

| Assunto | Símbolos | Estado |
|---|---|---|
| álgebra linear de cena | `LinearTransformationScene` (28 métodos próprios) `VectorScene` (17) `ApplyMatrix` `ApplyComplexFunction` | **órfão.** Esta skill mapeia as classes e as assinaturas; ninguém ensina o fluxo |
| câmeras exóticas | `MultiCamera` `SplitScreenCamera` `MappingCamera` `OldMultiCamera` | órfão salvo o uso via `ZoomedScene` (`manim-camera-2d`) |
| modo interativo | `Scene.embed` `interactive_embed` `RerunSceneHandler` `SceneInteract*` `--enable_gui` `--force_window` | órfão. Só OpenGL, e desiste em silêncio quando se está escrevendo arquivo (§9, linha 21). Para interativo de verdade, `bin/manimgl` (`manimgl-3b1b`) |
| `SceneFileWriter` por dentro | 28 métodos próprios | repartido: seções aqui (§5), caminhos e nomes em `manim-render-api`, cache em `manim-performance-cache`, áudio em `manim-som-legendas` |
