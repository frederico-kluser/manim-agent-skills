---
name: manim-camera-2d
description: >-
  Câmera 2D no ManimCE — a moldura que TAMBÉM é um Mobject: `MovingCameraScene`
  e `self.camera.frame` (pan, zoom, `save_state`/`Restore`, `auto_zoom`, updater
  que segue um objeto), `ZoomedScene` e a lupa (`activate_zooming`,
  `zoomed_camera`, `zoomed_display`, `zoom_factor`, `MultiCamera`), a `Camera`
  crua (`frame_center`, `frame_width`, `is_in_frame`, `background_image`) e as
  câmeras vestigiais (`MappingCamera`, `SplitScreenCamera`, `OldMultiCamera`).
  Use quando o pedido for "dá um zoom nisso", "aproxima a câmera", "afasta para
  mostrar tudo", "faz um pan para a direita", "a câmera segue o ponto", "volta o
  enquadramento de antes", "mostra o mapa inteiro e depois foca no detalhe",
  "põe uma lupa aqui", "quero um inset ampliado no canto", "enquadra esses três
  objetos juntos", "o texto ficou pequeno, chega mais perto" — e também quando o
  sintoma for "a cena esticou/achatou depois que mexi na câmera", "a lupa não
  aparece", "a lupa saiu com fundo preto no slide branco", "não vejo a borda da
  lupa", "o updater da câmera não roda", "a câmera restaura e pula de volta para
  o objeto", "a cena ficou lenta depois que a câmera passou a se mexer",
  `AttributeError: 'OpenGLCamera' object has no attribute 'frame'`,
  `Exception: Could not determine bounding box of the mobjects given to
  'auto_zoom'` ou `Exception: Trying to restore without having saved`. NÃO use
  para 3D, `phi`/`theta`/`gamma`, `move_camera`, `add_fixed_in_frame_mobjects`
  ou `ThreeDCamera` (skill `manim-3d-camera`); para escolher de qual `Scene`
  herdar em geral, ciclo de vida e `next_section` (`manim-cenas-secoes`); para
  `rate_func`, `run_time` e composição do movimento (`manim-composicao-ritmo`);
  para `Transform` × `ReplacementTransform` e o catálogo de animações
  (`manim-animations`); para escrever updater em geral (
  `manim-updaters-valuetracker`); para posicionar mobjects, buffers e "cabe na
  tela?" (`manim-layout-posicionamento`); para `background_color`,
  `background_opacity` e contraste (`manim-color-theming`); para o corte de
  vídeo em partes do slide (`manim-presentation-parts`); nem para codec, NVENC e
  tempo de render medido (`manim-gpu-encoding`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Câmera 2D — a moldura que também é um Mobject

Em 3D a câmera é um ponto de vista, e você a comanda por ângulos. **Em 2D no
ManimCE a câmera é um retângulo desenhado no mesmo plano da cena** — um
`ScreenRectangle` de verdade, com `.animate`, `.scale`, `.move_to`,
`.save_state` e updaters. Não existe "comando de zoom": existe um retângulo que
você move e redimensiona, e a imagem é o que couber dentro dele.

Essa é a boa notícia, e é também a origem de todas as armadilhas desta skill:
como o frame é um Mobject, ele aceita métodos que **deformam** tanto quanto os
que enquadram, e ninguém avisa qual é qual.

## Procedência do que está escrito aqui

- **[FONTE]** — lido no ManimCE **0.21.0** instalado em
  `.venv/lib/python3.12/site-packages/manim/`, com arquivo e linha. Afirmação
  forte.
- **[ÍNDICE]** — assinatura conferida em `api/manim-ce-index.tsv` /
  `api/manim-ce-methods.tsv` / `api/manim-ce-api.json.gz`.
- **[CALCULADO]** — aritmética minha sobre uma fórmula que está no fonte. O
  mecanismo é certo; o efeito visual não foi visto.
- **[NÃO VERIFICADO]** — não foi executado. **Nesta revisão nada foi
  renderizado** (proibição de CPU/GPU vigente): não há um único número de tempo,
  de memória ou de pixel medido neste arquivo. §18 lista o que ficou de fora.

Os exemplos marcados **[EXEMPLO OFICIAL]** foram copiados dos docstrings do
próprio módulo (`scene/moving_camera_scene.py`, `scene/zoomed_scene.py`) — são
o que a biblioteca publica como uso correto, e não foram rodados aqui.

---

## Cartão de referência — o sintoma manda na seção

| O que você quer, ou o que quebrou | Seção |
|---|---|
| "dá um zoom", "aproxima", "afasta" | §2.3, §3 |
| "a câmera segue o ponto" | §6 |
| "volta o enquadramento" | §5 |
| "enquadra esses três de uma vez" | §4 |
| "põe uma lupa / um inset ampliado" | §8 |
| a cena **esticou ou achatou** | §3 — você usou `frame_width =` no lugar de `set(width=)` |
| o updater da câmera **não roda** | §6.1 — falta `self.add(self.camera.frame)` |
| a câmera **restaura e pula de volta** | §6.3 — falta `clear_updaters()` |
| `Exception: Could not determine bounding box…` | §4.3 |
| `Exception: Trying to restore without having saved` | §5.2 |
| a **lupa não aparece** | §8.2 — falta `activate_zooming()` |
| a lupa saiu **preta** num slide de fundo claro | §8.6 |
| **não se vê a borda** da lupa (fundo claro) | §8.5 |
| passei `zoom_activated=True` e não ativou nada | §8.4 |
| `image_frame_stroke_width` não muda nada | §8.4 |
| a cena **ficou lenta** depois que a câmera se mexeu | §7 |
| `AttributeError: 'OpenGLCamera' object has no attribute 'frame'` | §12 |
| `AttributeError: … 'ThreeDCamera' … 'frame'` | §11 |
| `TypeError: __init__() missing 2 required positional arguments` numa câmera | §9.1 |
| a câmera se move e o fundo fica **congelado** | §10.1 |
| "isso cabe na tela agora?" sem renderizar | §15 |
| vídeo de slide em partes com pan/zoom | §13 |

---

## 1. O modelo mental, e a conta que a câmera faz

### 1.1 A cadeia de herança real — **[ÍNDICE]** (`bases` do `api-dump`)

```
Camera                       ← props: background_color, background_opacity
├── MovingCamera             ← + frame_center, frame_height, frame_width  (e o atributo .frame)
│   └── MultiCamera          ← + a lista image_mobjects_from_cameras
├── ThreeDCamera             ← + frame_center  (NÃO tem .frame — §11)
├── MappingCamera            ← distorce o espaço (§9.2)
└── OldMultiCamera           ← vestigial
    └── SplitScreenCamera    ← inalcançável na prática (§9.1)

Scene
└── MovingCameraScene        camera_class=MovingCamera
    └── ZoomedScene          camera_class=MultiCamera   ← herda de MovingCameraScene!
```

Duas coisas dessa árvore que quase todo mundo erra:

1. **`ZoomedScene` É uma `MovingCameraScene`.** Você não escolhe entre "mover a
   câmera" e "ter uma lupa" — numa `ZoomedScene` você tem `self.camera.frame`
   (câmera principal) **e** `self.zoomed_camera.frame` (a lupa). §8.9.
2. **`.frame` não é da `Camera`.** É atributo de `MovingCamera`
   (`camera/moving_camera.py:57`). Numa `Scene` comum, `self.camera.frame` não
   existe. Numa `ThreeDScene` também não — §11.

### 1.2 A conta, em uma linha — **[FONTE]** `camera/camera.py:1227-1237`

```python
shifted_points = points - self.frame_center
width_mult  = self.pixel_width  / self.frame_width      # px por unidade em x
height_mult = self.pixel_height / self.frame_height     # px por unidade em y
```

É só isso. A câmera 2D é **uma translação e duas escalas independentes**. Três
consequências que valem por metade desta skill:

- **não há rotação.** O fonte de `MovingCamera` traz, literalmente,
  `# TODO, make these work for a rotated frame` (`moving_camera.py:60`). Girar
  o frame não gira a imagem — muda a *caixa delimitadora* dele, e portanto a
  largura/altura, e o resultado é um zoom-out torto. **[FONTE + CALCULADO]**
- **as duas escalas são independentes**, logo é perfeitamente possível deformar
  a cena sem erro nenhum. É §3.
- no estado de partida elas são **iguais**: com o palco padrão 14,222 × 8 e
  1920 × 1080 px, `width_mult = 1920/14,222 = 135,0` e
  `height_mult = 1080/8 = 135,0`. **[CALCULADO]** Enquanto o frame guardar a
  proporção do quadro, a imagem não distorce.

### 1.3 De onde vem o frame inicial — **[FONTE]** `moving_camera.py:52-57`

```python
if frame is None:
    frame = ScreenRectangle(height=config["frame_height"])
    frame.set_stroke(self.default_frame_stroke_color,   # WHITE
                     self.default_frame_stroke_width)   # 0
self.frame = frame
```

`ScreenRectangle(aspect_ratio=16/9, height=4)` **[ÍNDICE]** — aqui com
`height=config["frame_height"]`, e em seguida `Camera.__init__` o estica para
`config["frame_width"]`/`["frame_height"]` e chama `resize_frame_shape()`
(`camera.py:122-128, 158`), que força a proporção do frame a bater com a dos
pixels: `frame_height = frame_width / (pixel_width/pixel_height)`.

Isto responde uma pergunta prática: **`config.frame_width` é quem manda**; o
`frame_height` é recalculado a partir dele e da resolução. Em vídeo vertical
9:16 o palco não é 14,222 × 8 e sim ~4,5 × 8 — o `config` já faz
`frame_width = frame_height * aspect_ratio` ao ler o arquivo
(`_config/utils.py:673-678`). **[FONTE]** O que isso significa para *posicionar
coisas* é assunto de `manim-layout-posicionamento`.

### 1.4 Por que o frame nasce com traço 0 — e por que na lupa nasce com 2

O frame da câmera principal é, **por definição**, a borda da tela: a vista é
exatamente o retângulo. Desenhá-lo produziria uma moldura colada na margem, o
tempo todo, sem informação nenhuma. Por isso `default_frame_stroke_width=0`.

Na lupa é o contrário: `ZoomedScene` passa
`zoomed_camera_config={"default_frame_stroke_width": 2, "background_opacity": 1}`
**[FONTE]** `zoomed_scene.py:84-87`, porque ali o frame é um retângulo pequeno
*dentro* da vista principal — é ele que mostra ao espectador de onde vem o
detalhe ampliado. Guarde: **traço 0 é decisão de projeto, não descuido.**

---

## 2. `MovingCameraScene` — o básico completo

### 2.1 Assinaturas — **[ÍNDICE]**

```python
class MovingCameraScene(Scene):
    def __init__(self, camera_class: type[Camera] = MovingCamera, **kwargs: Any) -> None

class MovingCamera(Camera):
    def __init__(self, frame: Mobject | None = None,
                 fixed_dimension: int = 0,
                 default_frame_stroke_color: ManimColor = WHITE,
                 default_frame_stroke_width: int = 0,
                 **kwargs: Any)
```

`MovingCameraScene` tem **um único método próprio** além do `__init__`:
`get_moving_mobjects(*animations) -> list[Mobject]` **[ÍNDICE]** — que você
nunca chama, mas que explica o custo de §7.

`MovingCamera` tem cinco métodos próprios **[ÍNDICE]**, e só um interessa
(`auto_zoom`, §4). `capture_mobjects`, `cache_cairo_context`,
`get_cached_cairo_context` e `get_mobjects_indicating_movement` são maquinaria
interna — mas `get_cached_cairo_context` reaparece em §7, porque é ela que
desliga um cache.

### 2.2 O que é `self.camera.frame`

Um `ScreenRectangle`, isto é, um `Rectangle`, isto é, um `VMobject`. **Tudo o
que vale para um mobject vale para ele**: `.animate`, `.shift`, `.move_to`,
`.scale`, `.set(width=…)`, `.save_state()`, `.add_updater()`,
`.set_stroke()`, `.get_center()`, `.width`. Não há uma API de câmera para
aprender — há a API de Mobject, que você já conhece, aplicada a um retângulo
especial. O catálogo de métodos de posicionamento é de
`manim-layout-posicionamento`.

`self.camera`, por sua vez, é uma **property só-de-leitura** de `Scene`
(`scene/scene.py:226-228`: `return self.renderer.camera`) **[FONTE]**. Atribuir
`self.camera = outra_coisa` levanta `AttributeError`; a câmera é escolhida uma
vez, por `camera_class`, no `__init__` — §9.3.

### 2.3 Os quatro verbos

```python
class Passeio(MovingCameraScene):
    def construct(self):
        alvo = Dot(2 * RIGHT + UP)
        self.add(alvo, Square(), Text("legenda", font_size=24).to_edge(DOWN))

        f = self.camera.frame
        self.add(f)                                           # 0. põe o frame na cena — §6.1, §7 item 1
        f.save_state()                                        # 1. guardar o enquadramento

        self.play(f.animate.move_to(alvo))                    # 2. PAN
        self.play(f.animate.set(width=4))                     # 3. ZOOM (uniforme — §3)
        self.play(f.animate.scale(2).shift(3 * LEFT))         #    zoom + pan no mesmo play
        self.play(Restore(f))                                 # 4. voltar
```

- **pan** = `move_to` / `shift` no frame.
- **zoom** = `set(width=…)`, `set(height=…)` ou `scale(k)` no frame.
  `scale(0,5)` **aproxima** (o retângulo encolhe, cabe menos coisa, tudo parece
  maior). `scale(2)` afasta. É invertido em relação à intuição de "zoom", e é a
  troca de sinal mais comum aqui.
- **voltar** = `save_state()` + `Restore(f)` — §5.
- **seguir** = updater — §6.

`Restore` é `manim-animations`; `run_time` e `rate_func` do movimento são
`manim-composicao-ritmo`. Um pan feito com `rate_func=linear` parece uma
câmera de vigilância; o default `smooth` é quase sempre o certo.

### 2.4 Os exemplos oficiais — **[EXEMPLO OFICIAL]** `moving_camera_scene.py:11-85`

Vale conhecê-los porque são a referência que a biblioteca publica, e porque o
último mostra `auto_zoom` num laço:

```python
class ChangingCameraWidthAndRestore(MovingCameraScene):
    def construct(self):
        text = Text("Hello World").set_color(BLUE)
        self.add(text)
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=text.width * 1.2))
        self.wait(0.3)
        self.play(Restore(self.camera.frame))

class MovingCameraOnGraph(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        ax = Axes(x_range=[-1, 10], y_range=[-1, 10])
        graph = ax.plot(lambda x: np.sin(x), color=WHITE, x_range=[0, 3 * PI])
        dot_1 = Dot(ax.i2gp(graph.t_min, graph))
        dot_2 = Dot(ax.i2gp(graph.t_max, graph))
        self.add(ax, graph, dot_1, dot_2)
        self.play(self.camera.frame.animate.scale(0.5).move_to(dot_1))
        self.play(self.camera.frame.animate.move_to(dot_2))
        self.play(Restore(self.camera.frame))
        self.wait()

class SlidingMultipleFrames(MovingCameraScene):
    def construct(self):
        def create_frame(number):
            frame = Rectangle(width=16, height=9)
            circ = Circle().shift(LEFT)
            text = Tex(f"This is Frame {str(number)}").next_to(circ, RIGHT)
            frame.add(circ, text)
            return frame

        group = VGroup(*(create_frame(i) for i in range(4))).arrange_in_grid(buff=4)
        self.add(group)
        self.camera.auto_zoom(group[0], animate=False)
        for frame in group:
            self.play(self.camera.auto_zoom(frame))
            self.wait()
        self.play(self.camera.auto_zoom(group, margin=2))
```

Repare no `set(width=text.width * 1.2)` do primeiro: **o enquadramento é
derivado da medida do conteúdo**, não um número mágico. É o idioma que sobrevive
a mudança de texto, de fonte e de resolução.

---

## 3. `set(width=…)` × `frame_width = …` — a armadilha-mor

As duas linhas abaixo parecem sinônimos. Uma enquadra; a outra **deforma a cena
inteira**, sem erro, sem warning e sem nada no terminal.

```python
self.camera.frame.set(width=7)     # ✅ escala UNIFORME: zoom de verdade
self.camera.frame_width = 7        # ❌ estica SÓ a largura: a cena achata
```

### 3.1 Por que — as duas escadas de código, **[FONTE]**

| Você escreve | Chega em | Efeito |
|---|---|---|
| `frame.set(width=7)` / `frame.width = 7` | `Mobject.width` setter → `scale_to_fit_width` (`mobject/mobject.py:809-810`) | **uniforme** — largura e altura mudam juntas |
| `camera.frame_width = 7` | `MovingCamera.frame_width` setter → `frame.stretch_to_fit_width` (`moving_camera.py:83-104`) | **não uniforme** — só a largura muda |
| `camera.frame_height = 4` | `MovingCamera.frame_height` setter → `frame.stretch_to_fit_height` (`moving_camera.py:61-82`) | **não uniforme** |
| `frame.scale(k)` | `Mobject.scale` | uniforme |
| `frame.stretch_to_fit_width(7)` | direto | não uniforme (é a mesma coisa que a linha 2) |

### 3.2 O tamanho do estrago — **[CALCULADO]** sobre §1.2

Palco 14,222 × 8 em 1920 × 1080. Depois de `camera.frame_width = 7` o frame vira
**7 × 8** (a altura não foi tocada):

```
width_mult  = 1920 / 7 = 274,3      (era 135,0)
height_mult = 1080 / 8 = 135,0      (inalterado)
```

Tudo aparece **2,03× mais largo do que alto**. Um `Circle` vira elipse; um
`Square`, retângulo; o texto engorda. E como todo o quadro deforma junto, a
imagem parece "esquisita" sem que nenhum elemento pareça errado — é o pior tipo
de defeito visual, porque não tem culpado local. Só aparece **olhando o PNG**
(`manim-verificacao-visual`).

### 3.3 Então para que servem os setters?

Para **pan sem animação**, onde eles são convenientes e corretos:

```python
self.camera.frame_center = 3 * RIGHT      # frame.move_to(3*RIGHT)   [FONTE moving_camera.py:105-127]
self.camera.frame_center = alvo            # move_to aceita Mobject: centraliza no alvo
```

`frame_center` é o único dos três que **não deforma nada** — o setter é
`move_to`. Use-o à vontade para posicionar a câmera antes do primeiro `play`;
para movimento animado, `self.play(frame.animate.move_to(...))`.

### 3.4 A regra de bolso

> **Fale com o `frame`, não com a `camera`.** `self.camera.frame.<qualquer
> coisa de Mobject>` é sempre seguro em proporção. `self.camera.frame_width` e
> `self.camera.frame_height` são *leituras* úteis (`f"{self.camera.frame_width:.2f}"`)
> e *escritas* perigosas.

Corolário: `ScreenRectangle.aspect_ratio` também tem setter por
`stretch_to_fit_width` (`mobject/frame.py:33-35`) **[FONTE]** — mesma família,
mesmo cuidado.

---

## 4. `auto_zoom` — enquadrar um conjunto sem fazer conta

O único método de `MovingCamera` que você vai chamar de verdade.

### 4.1 Assinatura — **[ÍNDICE]**

```python
MovingCamera.auto_zoom(
    mobjects: Iterable[Mobject],
    margin: float = 0,
    only_mobjects_in_frame: bool = False,
    animate: bool = True,
) -> _AnimationBuilder | Mobject
```

```python
self.play(self.camera.auto_zoom(VGroup(a, b, c), margin=0.6))   # animado
self.camera.auto_zoom([a, b, c], animate=False)                  # aplica na hora
```

### 4.2 O que ele faz — **[FONTE]** `moving_camera.py:187-243`

Calcula a caixa delimitadora dos mobjects (via `get_critical_point`), centra o
frame nela com `set_x`/`set_y`, e ajusta **a dimensão limitante** com
`.set(width=…)` ou `.set(height=…)` — portanto **escala uniforme**, sem o
problema de §3. O `margin` é somado **só à dimensão escolhida**, em unidades de
palco: a folga real no outro eixo sai proporcional, não igual.

Detalhe útil: o laço **pula o próprio frame da câmera**
(`if (m == self.frame) … continue`), então `self.camera.auto_zoom(self.mobjects)`
funciona mesmo com o frame adicionado à cena (§6.1).

### 4.3 Os três jeitos de errar

**a) Esquecer o `self.play`.** Com `animate=True` (o default) a função devolve
um `_AnimationBuilder` e **não faz nada sozinha**. `self.camera.auto_zoom(g)`
numa linha solta é um no-op silencioso — o objeto é criado e descartado.

**b) Passar um conjunto vazio.** Se nenhum mobject entrar na conta, o fonte
levanta um `Exception` **cru** (`moving_camera.py:283-285`) **[FONTE]**:

```
Exception: Could not determine bounding box of the mobjects given to 'auto_zoom'.
```

Acontece com `VGroup()` vazio, com um `Mobject()` sem pontos e sem
submobjects, e — o caso que morde — com `only_mobjects_in_frame=True` quando
tudo já saiu do enquadramento. Sendo `Exception` puro, não dá para capturar de
forma estreita: teste antes (`if len(grupo) == 0`).

**c) Achar que funciona com a cena girada.** O docstring é explícito
**[FONTE]**: *"This method only works when 2D-objects in the XY-plane are
considered, it will not work correctly when the camera has been rotated."*

### 4.4 Como a iteração enxerga o argumento — **[FONTE]** `mobject.py:2520-2521`

`Mobject.__iter__` devolve `chain([self] if self.has_points() else [],
self.submobjects)`. Ou seja: um `Circle` (tem pontos) itera como ele mesmo; um
`VGroup` ou um `Text` (não têm pontos próprios) iteram como seus filhos. É por
isso que `auto_zoom(circulo)` e `auto_zoom(grupo)` funcionam igual — e por que
`auto_zoom(VGroup())` estoura.

### 4.5 Quando NÃO usar `auto_zoom`

Quando o enquadramento precisa ser **estável entre partes de um vídeo**
(§13) ou entre renders: `auto_zoom` depende do conteúdo, e conteúdo muda.
Numa aula, um enquadramento explícito e escrito como constante
(`self.camera.frame.set(width=LARGURA_FOCO).move_to(CENTRO_FOCO)`) é revisável e
não desliza quando alguém acrescenta uma etiqueta na cena.

---

## 5. Salvar e restaurar o enquadramento

### 5.1 O idioma

```python
f = self.camera.frame
f.save_state()                 # no começo do construct, ANTES de qualquer mexida
...
self.play(Restore(f))          # volta posição, tamanho e estilo de uma vez
```

`Mobject.save_state()` guarda `self.saved_state = self.copy()`
(`mobject.py:2152-2159`) **[FONTE]** — para um retângulo é uma cópia barata.
`Restore(mobject, **kwargs)` **[ÍNDICE]** herda de `ApplyMethod` e chama
`mobject.restore` (`animation/transform.py:598-620`).

### 5.2 As duas maneiras de quebrar

**Restaurar sem ter salvo** — `mobject.py:2161-2166` **[FONTE]**:

```
Exception: Trying to restore without having saved
```

**Salvar tarde.** `save_state()` sobrescreve o estado anterior; se você o chama
depois de já ter dado zoom, o `Restore` volta para o zoom, não para o
enquadramento original. A disciplina é: **um `save_state()` na primeira linha do
`construct`**, e mais nenhum, a não ser que você queira mesmo mudar a âncora.

Se precisar de duas âncoras, não use `save_state` duas vezes — guarde os números:

```python
CASA = (self.camera.frame.width, self.camera.frame.get_center().copy())
...
self.play(self.camera.frame.animate.set(width=CASA[0]).move_to(CASA[1]))
```

`.copy()` no `get_center()` importa: ele devolve um `ndarray` que pode ser
reaproveitado por outra chamada. **[INFERIDO — não reproduzido]**

### 5.3 Restaurar × recalcular

`Restore` interpola do estado atual para o salvo — em `run_time` padrão, 1 s.
Para "volta e mostra tudo de novo", `Restore` é o certo. Para "afasta até caber
o que está na tela AGORA" (que pode ser mais do que havia no começo), o certo é
`auto_zoom` sobre `self.mobjects` — §4.

---

## 6. Seguir um mobject — a câmera com updater

### 6.1 A linha sem a qual nada acontece

```python
self.camera.frame.add_updater(lambda m: m.move_to(dot))
self.add(self.camera.frame)        # ← SEM ISTO O UPDATER NUNCA RODA
```

**[FONTE]** `Scene.update_mobjects` (`scene/scene.py:383-393`) é literalmente
`for mobj in self.mobjects: mobj.update(dt)`. O frame da câmera **não está** em
`self.mobjects` — ele mora dentro da câmera. Um updater nele é registrado com
sucesso, nunca é chamado, e não há erro nenhum. É o defeito nº 1 desta seção.

Adicionar o frame à cena é seguro porque ele nasce com traço 0 (§1.4): entra no
grafo, não pinta pixel. Duas consequências a lembrar mesmo assim:

- ele passa a contar em `self.mobjects` — um `Group(*self.mobjects)` para medir
  layout vai incluir um retângulo do tamanho da tela;
- `auto_zoom` já o ignora de propósito (§4.2), então essa combinação está ok.

Para tirá-lo depois: `self.remove(self.camera.frame)` — mas pense duas vezes:
**esta linha tem uma segunda função**, e ela vale mesmo sem updater nenhum. É
por estar em `self.mobjects` que o frame entra na contabilidade de
móvel × estático do renderer cairo, que é o que garante o redesenho completo
durante um pan. §7, item 1.

### 6.2 Perseguição dura × amortecida

```python
# dura: cola no alvo. Todo tremor do alvo vira tremor de câmera.
self.camera.frame.add_updater(lambda m: m.move_to(dot))

# amortecida: a câmera "alcança" o alvo. dt no nome do 2º parâmetro é obrigatório.
def segue(m, dt):
    m.move_to(interpolate(m.get_center(), dot.get_center(), min(1.0, 6 * dt)))
self.camera.frame.add_updater(segue)
```

`interpolate(start, end, alpha)` é de `manim.utils.bezier` **[ÍNDICE]**. A regra
"o segundo parâmetro **precisa se chamar `dt`**" e o porquê (o Manim inspeciona
a assinatura) são de `manim-updaters-valuetracker` — não repita a explicação,
consulte lá.

O `min(1.0, 6*dt)` limita o passo: com 60 fps, `6*dt = 0,1` por frame, e a
câmera cobre ~99,9 % da distância em ~1,1 s. **[CALCULADO]** Ajuste o 6 para
mudar a "inércia".

### 6.3 O updater que vence o `Restore` — e por que a câmera "pula de volta"

Sintoma: você toca `Restore(self.camera.frame)`, a animação roda bonitinha, e
**no último frame a câmera salta de volta para cima do alvo**.

Causa **[FONTE]** `animation/animation.py:137,150,206,226`: `Animation` nasce com
`suspend_mobject_updating=True` e, em `begin()`, suspende os updaters do
mobject animado — por isso a animação *parece* funcionar. Em `finish()` ela
chama `resume_updating()`, o updater volta a rodar no frame seguinte e devolve a
câmera para o alvo, num salto de um frame.

Correção: **desligue antes de restaurar.**

```python
self.camera.frame.clear_updaters()
self.play(Restore(self.camera.frame))
```

`clear_updaters(recursive=True)` **[ÍNDICE]**. A anatomia completa da disputa
animação × updater é de `manim-updaters-valuetracker`.

### 6.4 Seguir e enquadrar ao mesmo tempo

```python
grupo = VGroup(carro, placa)
self.camera.frame.add_updater(
    lambda m: m.move_to(grupo).set(width=max(6.0, grupo.width * 1.4))
)
```

Funciona, e é **caro**: reconstrói a caixa delimitadora do grupo a cada frame
(§7). O `max(6.0, …)` é o que evita o zoom respirar sem parar quando o grupo
muda de tamanho — sem um piso, a câmera "bombeia" e dá enjoo em quem assiste.

Chamar `auto_zoom` dentro de um updater é possível e quase sempre errado: ele
devolve `_AnimationBuilder` quando `animate=True`, então seria
`auto_zoom(..., animate=False)`, e aí você paga a caixa delimitadora de toda a
lista, a cada frame.

---

## 7. O preço: mover a câmera desliga DUAS otimizações

Esta seção é mecanismo lido, **sem um único número medido** — a proibição de
CPU/GPU desta revisão vale aqui inteira. Meça com `manim-gpu-encoding` antes de
citar custo para alguém.

**1. O frame estático morre — e o gatilho depende de uma linha sua.** O
renderer cairo pinta uma vez os mobjects que não se mexem e reusa esse bitmap
como fundo (`renderer/cairo_renderer.py:110,153-154,218-243`) **[FONTE]**. Quem
separa móvel de estático é `Scene.get_moving_and_static_mobjects`, chamada só
sob `RendererType.CAIRO` (`scene/scene.py:1347-1353`), e o critério de
`Scene.get_moving_mobjects` (`scene/scene.py:899-946`) **[FONTE]** varre
`self.mobjects`: conta como móvel quem está numa animação, quem tem updater na
família, ou quem é foreground.

`MovingCameraScene` acrescenta uma regra por cima
(`moving_camera_scene.py:123-142`) **[FONTE]**:

```python
movement_indicators = self.renderer.camera.get_mobjects_indicating_movement()  # = [self.frame]
for movement_indicator in movement_indicators:
    if movement_indicator in all_moving_mobjects:
        return list_update(self.mobjects, moving_mobjects)   # então TUDO é "móvel"
```

Lendo palavra por palavra: ela só dispara **se o frame estiver entre os
móveis** — e o frame só chega lá se estiver em `self.mobjects`, porque
`Scene.get_mobject_family_members` (`scene/scene.py:467-488`) lê `self.mobjects`
e mais nada. Daí a recomendação de §6.1 valer **sempre**, não só com updater:

> **`self.add(self.camera.frame)` na abertura do `construct`.** Com o frame na
> cena, todo `play` que o anime o marca como móvel, a regra acima dispara, a
> lista de estáticos fica vazia, `save_static_frame_data` grava
> `static_image = None` (`cairo_renderer.py:238-242`) e o quadro é redesenhado
> inteiro — que é exatamente o que um pan precisa. Custa caro, e é o preço
> certo.

**RESOLVIDO por leitura — e a leitura provisória anterior estava errada.** A
versão anterior desta caixa dizia que um pan **sem** `self.add(self.camera.frame)`
"deveria deixar rastro do enquadramento antigo", e registrava isso como a
pergunta em aberto mais importante da skill, resolvível só renderizando. Não é:
existe um caminho, e ele está **26 linhas acima** do trecho citado.

```python
# scene/scene.py:535-545
def add_mobjects_from_animations(self, animations):
    curr_mobjects = self.get_mobject_family_members()
    for animation in animations:
        if animation.is_introducer():
            continue
        # Anything animated that's not already in the scene gets added to the scene
        mob = animation.mobject
        if mob is not None and mob not in curr_mobjects:
            self.add(mob)
```

A cadeia, toda no fonte:

1. `self.camera.frame.animate.shift(...)` produz um `_MethodAnimation`
   (`animation/transform.py:443-446`), cujo `self.mobject` **é o frame**;
2. `Animation.__init__` tem `introducer: bool = False` (`animation/animation.py:138`),
   logo `is_introducer()` é `False` e o `continue` não dispara;
3. `compile_animation_data` chama `add_mobjects_from_animations` na
   `scene.py:1321`, **antes** de `begin_animations` (1340) — então o frame entra
   em `self.mobjects` no **primeiro** `play` que o anima;
4. só então `scene.py:1347-1353` calcula móveis × estáticos, e
   `MovingCameraScene.get_moving_mobjects` (`moving_camera_scene.py:136-140`)
   encontra o frame entre os móveis.

**Conclusão: não há rastro, e os exemplos oficiais estão certos.** O
`self.add(self.camera.frame)` explícito continua valendo — mas como
**garantia**, não como conserto de um defeito: ele cobre o caso do frame movido
por *updater* (que não passa por `play` nenhum, §6.1) e o do primeiro frame de
um `play` em que a câmera ainda não foi animada. Não precisa dele para um pan
comum feito com `.animate`.

**2. O contexto do cairo deixa de ser cacheado.** `MovingCamera` sobrescreve
`get_cached_cairo_context` para devolver `None` e `cache_cairo_context` para não
fazer nada (`moving_camera.py:134-148`) **[FONTE]**, com o comentário
*"Since the frame can be moving around, the cairo context … should be
regenerated at each frame. So no caching."* Isso vale para a cena inteira, o
tempo todo — **inclusive nos `play` em que a câmera está parada**, porque quem
sobrescreve é a classe, não o instante.

Consequência prática, e é a que interessa: **herdar de `MovingCameraScene` já
custa, mesmo sem mover a câmera.** Se o vídeo não precisa de pan nem de zoom,
herde de `Scene`. E se apenas 1 de 9 partes precisa (§13), pense duas vezes
antes de transformar a cena inteira.

O que fazer quando pesar: reduzir o número de curvas na tela e evitar
`always_redraw` junto do pan (`manim-performance-cache`), e medir de verdade
(`manim-gpu-encoding`), nunca chutar.

---

## 8. `ZoomedScene` — a lupa num inset

### 8.1 A assinatura inteira — **[ÍNDICE]**

```python
class ZoomedScene(MovingCameraScene):
    def __init__(self,
        camera_class: type[Camera] = MultiCamera,
        zoomed_display_height: float = 3,
        zoomed_display_width: float = 3,
        zoomed_display_center: Point3DLike | None = None,
        zoomed_display_corner: Vector3D = UP + RIGHT,          # array([1., 1., 0.]) = UR
        zoomed_display_corner_buff: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,   # 0.5
        zoomed_camera_config: dict = {"default_frame_stroke_width": 2,
                                      "background_opacity": 1},
        zoomed_camera_image_mobject_config: dict = {},
        zoomed_camera_frame_starting_position: Point3DLike = ORIGIN,
        zoom_factor: float = 0.15,
        image_frame_stroke_width: float = 3,                   # MORTO — §8.4
        zoom_activated: bool = False,                          # MORTO — §8.4
        **kwargs) -> None
```

Métodos próprios **[ÍNDICE]**: `setup()`, `activate_zooming(animate=False)`,
`get_zoom_in_animation(run_time=2, **kwargs) -> ApplyMethod`,
`get_zoomed_display_pop_out_animation(**kwargs) -> ApplyMethod`,
`get_zoom_factor() -> float`.

Como `ZoomedScene.__init__` **não** aceita esses parâmetros por cena de fora, a
forma canônica de configurá-la é sobrescrever o `__init__` — é o que o exemplo
oficial faz:

```python
# [EXEMPLO OFICIAL] zoomed_scene.py:18-45
class ChangingZoomScale(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(self, zoom_factor=0.3, zoomed_display_height=1,
                             zoomed_display_width=3, image_frame_stroke_width=20,
                             zoomed_camera_config={"default_frame_stroke_width": 3},
                             **kwargs)

    def construct(self):
        dot = Dot().set_color(GREEN)
        sq = Circle(fill_opacity=1, radius=0.2).next_to(dot, RIGHT)
        self.add(dot, sq)
        self.wait(1)
        self.activate_zooming(animate=False)
        self.wait(1)
        self.play(dot.animate.shift(LEFT * 0.3))
        self.play(self.zoomed_camera.frame.animate.scale(4))
        self.play(self.zoomed_camera.frame.animate.shift(0.5 * DOWN))
```

(O `image_frame_stroke_width=20` desse exemplo oficial **não faz nada** — §8.4.)

### 8.2 As duas peças, e a linha que liga a lupa

`setup()` **[FONTE]** `zoomed_scene.py:110-136` cria dois objetos e os pendura
na cena:

| Atributo | O que é | Papel |
|---|---|---|
| `self.zoomed_camera` | uma `MovingCamera` independente | **o que** é ampliado — o `.frame` dela é o retângulo pequeno na cena |
| `self.zoomed_display` | um `ImageMobjectFromCamera` | **onde** aparece — o inset no canto, com moldura |

`setup()` estica os dois para `zoomed_display_height`/`_width`, encolhe o frame
por `zoom_factor`, e posiciona o display em `zoomed_display_corner` (UR) com
buff 0,5 — ou em `zoomed_display_center`, se você tiver passado um.

**Mas nada disso aparece.** Quem liga a lupa é:

```python
self.activate_zooming(animate=False)   # ou animate=True para a entrada animada
```

**[FONTE]** `zoomed_scene.py:139-157`: ela registra o display na `MultiCamera`
(`add_image_mobject_from_camera`) e adiciona frame e display como
`add_foreground_mobjects`. Sem essa chamada, `self.zoomed_camera` existe,
`self.zoomed_display` existe, nenhum erro acontece e **a lupa simplesmente não
está no vídeo**. É o sintoma nº 1 de `ZoomedScene`.

Com `animate=True` ela toca duas animações prontas: `get_zoom_in_animation()`
(o frame nasce do tamanho da tela e encolhe até o alvo) e
`get_zoomed_display_pop_out_animation()` (o inset "salta" da posição do frame
para o canto). Ambas devolvem `ApplyMethod` — que `manim-animations` classifica
como não idiomático, mas aqui é o que a biblioteca entrega pronto.

### 8.3 `zoom_factor` é o INVERSO da ampliação

`zoom_factor=0.15` (default) **não** é "ampliar 0,15×". **[FONTE]**
`setup()` estica o frame para o tamanho do display e depois faz
`zoomed_camera.frame.scale(self.zoom_factor)` — o frame fica 0,15 do tamanho do
display. E `get_zoom_factor()` devolve `frame.height / display.height`.

Logo, **ampliação = 1 / zoom_factor**:

| `zoom_factor` | frame na cena (com display 3×3) | ampliação |
|---|---|---|
| 0,50 | 1,5 × 1,5 | 2× |
| **0,15** (default) | **0,45 × 0,45** | **≈ 6,7×** |
| 0,05 | 0,15 × 0,15 | 20× |

**[CALCULADO]** Menor `zoom_factor` = mais perto. Quem quer "dar mais zoom"
diminui o número, e essa é a inversão que faz todo mundo mexer para o lado
errado na primeira vez.

### 8.4 Três parâmetros que não fazem nada — **[FONTE]** (grep no pacote inteiro)

| Parâmetro | Onde aparece | Verdade |
|---|---|---|
| `ZoomedScene(image_frame_stroke_width=…)` | atribuído em `zoomed_scene.py:106` | **nunca lido**. `add_display_frame()` é chamado sem kwargs (`:120`) — a espessura da moldura do inset é sempre a do default (3) |
| `ZoomedScene(zoom_activated=True)` | atribuído em `:107`, escrito em `:148` | **nunca lido**. Passar `True` **não** ativa a lupa; só `activate_zooming()` ativa |
| `MovingCamera(fixed_dimension=…)` | atribuído em `moving_camera.py:48` | **nunca lido**. O único uso está em `realign_frame_shape`, que está **comentado** (`:151-157`) |

O `grep` que sustenta isto (leitura pura, sem render):

```bash
grep -rn "image_frame_stroke_width\|zoom_activated\|fixed_dimension" \
  /home/ondokai/Projects/manim/.venv/lib/python3.12/site-packages/manim/
```

É a mesma família de defeito que `manim-3d-camera` documenta em
`ThreeDScene(ambient_camera_rotation=…)` — parâmetro guardado e nunca
consultado. Quando um kwarg de câmera "não faz nada", **grep antes de duvidar de
você**.

Para mudar a espessura da moldura do inset, mexa no mobject depois do `setup`:

```python
self.zoomed_display.display_frame.set_stroke(width=1.5)
```

### 8.5 As duas bordas são BRANCAS — e somem em fundo claro

**[FONTE]** dois defaults, dois lugares:

- o frame da lupa: `MovingCamera(default_frame_stroke_color=WHITE)`
  (`moving_camera.py:41`) — `manim-color-theming` já lista `MovingCamera
  default_frame_stroke_color=#FFFFFF` na tabela "branco: some em fundo claro";
- a moldura do inset: `ImageMobjectFromCamera.add_display_frame` monta um
  `SurroundingRectangle(self, stroke_width=3, stroke_color=WHITE, buff=0)`
  (`mobject/types/image_mobject.py:325-343`).

Num tema claro (o `CANVAS` branco do deck de aulas) as duas desaparecem sem
erro, e o resultado é um retângulo de imagem flutuando sem borda e um alvo
invisível na cena. A correção mora no `construct`, depois do `setup`:

```python
self.zoomed_camera.frame.set_stroke(ACENTO, 2)          # o alvo, na cena
self.zoomed_display.display_frame.set_stroke(TINTA, 2)  # a moldura do inset
```

A disciplina de nunca deixar cor implícita é de `manim-color-theming`; aqui só
fica o registro de que a lupa tem **duas** peças brancas por default, e as duas
passam pelo `--theme whiteboard` sem serem alcançadas (é estilo de instância,
não default de classe).

### 8.6 O fundo do inset é da SUB-câmera, e ele nasce preto

A `zoomed_camera` é uma `Camera` separada. **[FONTE]** `camera.py:134-137`: ela
lê `config["background_color"]` **no momento em que é construída** — e ela é
construída dentro de `ZoomedScene.setup()`. Portanto:

```python
class CenaClara(ZoomedScene):
    def setup(self):
        config.background_color = CANVAS          # ANTES
        self.camera.background_color = CANVAS
        super().setup()                            # ← aqui a zoomed_camera nasce
        self.zoomed_camera.background_color = CANVAS   # cinto e suspensório
```

Se você trocar o fundo **depois** do `super().setup()` e não tocar na
sub-câmera, o inset sai com o fundo antigo — em tema claro, **um retângulo preto
no canto do slide**, e o mesmo retângulo preto no PNG que vira pôster do PDF.

Note também `zoomed_camera_config={"background_opacity": 1}`: sem opacidade
cheia o inset seria transparente e mostraria o que está atrás dele. A catraca
de mão única do `background_opacity` (mexer nele troca a extensão do arquivo
para `.mov`) é assunto de `manim-color-theming §12.2` — **não** mexa em
`config.background_opacity` para resolver a lupa.

### 8.7 A resolução do inset é derivada — e pode explodir

**[FONTE]** `multi_camera.py:62-73`, chamado a cada captura de frame:

```python
imfc.camera.reset_pixel_shape(
    int(pixel_height * imfc.height / self.frame_height),
    int(pixel_width  * imfc.width  / self.frame_width),
)
```

Com os defaults (1080 × 1920 px, display 3 × 3, palco 8 × 14,222):
`1080·3/8 = 405` e `1920·3/14,222 = 405`. A sub-câmera renderiza em **405 × 405**
— exatamente o tamanho que o inset ocupa na tela. **[CALCULADO]** Duas leituras
disso:

- **a lupa não perde nitidez com o zoom.** Ela não amplia pixels: re-renderiza o
  vetor no recorte novo. Ampliar 20× continua nítido.
- **a resolução do inset é proporcional ao tamanho do inset na tela e
  INVERSAMENTE proporcional ao enquadramento da câmera principal.** Se você der
  zoom na câmera principal até `frame_height = 0,8` (10×), o denominador cai e a
  sub-câmera passa a 1080·3/0,8 = **4050** de altura e ~4050 de largura —
  4050² × 4 bytes ≈ **65 MB por frame**, realocados a cada frame
  (`reset_pixel_shape` → `init_background` → `np.zeros`, `camera.py:233-247,
  291-299`). **[CALCULADO — NÃO MEDIDO]**

Regra que sai daí: **lupa e zoom da câmera principal ao mesmo tempo é caro por
construção.** Se precisar dos dois, faça em momentos separados.

### 8.8 O frame da lupa é comandado pela LARGURA; a altura é recalculada

Continuação do mesmo trecho: `reset_pixel_shape` termina em
`resize_frame_shape()`, que numa `MovingCamera` **escreve** `frame_height` —
isto é, `stretch_to_fit_height` no retângulo (§3.1). Como isso acontece a cada
frame, o frame da lupa é forçado à proporção do display **continuamente**.

Consequência **[CALCULADO]**: `self.zoomed_camera.frame.stretch_to_fit_height(x)`
não sobrevive ao próximo frame. Para mudar o tamanho da lupa use **escala
uniforme** — que é o que o exemplo oficial faz:
`self.play(self.zoomed_camera.frame.animate.scale(4))`. Para mudar a *proporção*
da lupa, mude a proporção do **display** (`zoomed_display_width`/`_height` no
`__init__`); o frame acompanha sozinho.

E é essa mesma correspondência que mantém o inset sem distorção: o frame e o
display têm sempre a mesma proporção, então as duas anamorfoses (mundo → pixels
da sub-câmera, pixels → inset na tela) se cancelam. Esticar **um** dos dois
sozinho quebra o cancelamento.

### 8.9 `ZoomedScene` tem DUAS câmeras móveis

Como `ZoomedScene(MovingCameraScene)` **[ÍNDICE]**:

| Você escreve | Move o quê |
|---|---|
| `self.camera.frame` | a câmera **principal** — o enquadramento do vídeo inteiro |
| `self.zoomed_camera.frame` | **a lupa** — o retângulo que diz o que vai para o inset |
| `self.zoomed_display` | **o inset** — onde ele aparece na tela (é um `ImageMobject`; use `Group`, não `VGroup`) |

Confundir os dois é o segundo erro mais comum: `self.camera.frame.animate.scale(0.5)`
numa `ZoomedScene` dá zoom no vídeo todo, e a lupa vem junto, ampliada.

Bônus: como `activate_zooming` faz `add_foreground_mobjects(self.zoomed_camera.frame,
self.zoomed_display)` e `add_foreground_mobjects` chama `self.add(...)`
(`scene/scene.py:773-790`) **[FONTE]**, o frame **da lupa** já está em
`self.mobjects` — então updaters nele funcionam sem a linha extra de §6.1. O
frame da **principal** continua precisando dela.

### 8.10 Se você sobrescrever `setup()`

`ZoomedScene.setup()` é onde `self.zoomed_camera` e `self.zoomed_display`
nascem. Um `setup()` seu que esqueça `super().setup()` faz
`activate_zooming()` estourar com `AttributeError: 'X' object has no attribute
'zoomed_camera'`. **[FONTE — dedução direta de `zoomed_scene.py:110-136`]**

Numa base de projeto (o `CenaAula(Scene)` do deck de aulas é o caso real),
trocar a base para `ZoomedScene` exige revisar o `setup()` da base — a ordem
correta é a de §8.6.

---

## 9. As outras câmeras — o que dá para usar e o que é vestígio

### 9.1 `camera_class` é instanciado SEM ARGUMENTOS — e isso mata a `SplitScreenCamera`

**[FONTE]** `renderer/cairo_renderer.py:47-48`:

```python
camera_cls = camera_class if camera_class is not None else Camera
self.camera = camera_cls()
```

Nenhum kwarg. Portanto:

| Classe | `camera_cls()` | Situação |
|---|---|---|
| `Camera`, `MovingCamera`, `MultiCamera`, `ThreeDCamera`, `MappingCamera`, `OldMultiCamera` | ok (tudo tem default) | usáveis como `camera_class` |
| **`SplitScreenCamera(left_camera, right_camera)`** | `TypeError: … missing 2 required positional arguments` | **inalcançável** por `camera_class` **[FONTE + INFERIDO]** |

`OldMultiCamera()` instancia, mas sem `cameras_with_start_positions` não faz
nada: `capture_mobjects` itera uma lista vazia e o quadro sai só com o fundo.
**[FONTE]** `mapping_camera.py:108-118`. O próprio arquivo carrega o comentário
`# TODO, the classes below should likely be deleted`. Trate `OldMultiCamera` e
`SplitScreenCamera` como **vestígio**: não construa nada em cima.

Para tela dividida de verdade em 2D, o caminho que funciona não é câmera: são
dois `VGroup` posicionados lado a lado e uma `Line` no meio
(`manim-layout-posicionamento`), ou dois vídeos montados fora do Manim.

### 9.2 `MappingCamera` — distorcer o espaço inteiro

```python
class MappingCamera(Camera):
    def __init__(self, mapping_func=lambda p: p, min_num_curves=50,
                 allow_object_intrusion=False, **kwargs)
```
**[ÍNDICE]**

Ela aplica `mapping_func` a cada ponto antes de virar pixel
(`points_to_pixel_coords`), e **copia todos os mobjects** a cada captura
(`allow_object_intrusion=False`) e roda `insert_n_curves(min_num_curves)` em
todo `VMobject` com poucas curvas — para o traço não virar polígono ao entortar.
**[FONTE]** `mapping_camera.py:44-73`.

Funciona como `camera_class`, mas o custo é copiar e subdividir a cena inteira
por frame, e não há `Scene` pronta para ela. É uma curiosidade: use-a quando o
efeito de distorção *for* o assunto (mapa conforme, lente), não como ferramenta
de enquadramento.

### 9.3 Como configurar uma câmera apesar do `camera_cls()`

Duas saídas, ambas por classe:

```python
# a) subclasse com os defaults que você quer
class CameraDoDeck(MovingCamera):
    def __init__(self, **kw):
        super().__init__(default_frame_stroke_color=ACENTO,
                         default_frame_stroke_width=0, **kw)

class Cena(MovingCameraScene):
    def __init__(self, **kw):
        super().__init__(camera_class=CameraDoDeck, **kw)

# b) functools.partial — é chamável, então camera_cls() funciona
from functools import partial
class Cena(MovingCameraScene):
    def __init__(self, **kw):
        super().__init__(camera_class=partial(MovingCamera,
                                              default_frame_stroke_width=0), **kw)
```

(b) contraria a anotação `type[Camera]`, mas satisfaz o que o código realmente
faz (`camera_cls()`). **[INFERIDO — não executado]**. Em cena de produção
prefira (a): é o que um checador de tipo aceita e o que o próximo leitor
entende.

Terceira saída, mais simples quando é só um ajuste: **mexer na instância depois**,
no `setup()` da cena — `self.camera.frame.set_stroke(...)`,
`self.camera.background_image = "fundo.png"; self.camera.init_background()`
(não há chave de `config` para `background_image` **[FONTE — grep em
`_config/`]**; imagem de fundo é assunto de `manim-svg-imagens`).

---

## 10. A `Camera` crua de uma `Scene` comum

### 10.1 `frame_center` existe — e mesmo assim não faça pan numa `Scene`

Na `Camera` base, `frame_center`, `frame_width` e `frame_height` são **atributos
simples**, não properties (`camera.py:103,124,128`; as únicas properties de
`Camera` são `background_color` e `background_opacity` **[ÍNDICE]**). Você pode
escrever:

```python
class NaoFacaIsso(Scene):
    def construct(self):
        self.add(Square(), Circle().shift(3 * RIGHT))
        self.camera.frame_center = 3 * RIGHT      # "pan" instantâneo
```

E funciona — antes do primeiro `play`. **Dentro** de um `play` ele quebra em
silêncio, e a razão é §7 ao contrário: a `Camera` base **não tem**
`get_mobjects_indicating_movement`, então nada avisa a cena de que o
enquadramento mudou; os mobjects parados foram pintados no `static_image` com a
câmera antiga e esse bitmap é reutilizado (`cairo_renderer.py:153-154`)
**[FONTE]**. Resultado: o que se move acompanha a câmera nova, o resto fica
congelado na posição velha. Nenhum erro.

**Se a câmera precisa se mexer, herde de `MovingCameraScene`.** É a única
resposta.

### 10.2 O resto da `Camera` que às vezes é útil

`Camera` tem 45 métodos próprios além do `__init__` **[ÍNDICE]** e quase todos são rasterização
interna (`display_multiple_vectorized_mobjects`, `apply_stroke`,
`points_to_pixel_coords`…). Os quatro que aparecem em código de usuário:

| Método / atributo | Para quê |
|---|---|
| `is_in_frame(mobject) -> bool` | §15 — "isto está visível agora?" |
| `get_image(pixel_array=None) -> PIL.Image` | pegar o frame atual como imagem (`manim-verificacao-visual`) |
| `background_image` + `init_background()` | pôr uma imagem de fundo (`manim-svg-imagens`) |
| `background_color` / `background_opacity` | cor de fundo (`manim-color-theming` — inclusive a catraca do `.mov`) |

`BackgroundColoredVMobjectDisplayer(camera)` **[ÍNDICE]** é a maquinaria por
trás de `VMobject.set_background_image` / `color_using_background_image` —
pintar um mobject com a textura de uma imagem. É de `manim-svg-imagens`.

---

## 11. Fronteira com 3D — `ThreeDCamera` não tem `.frame`

**[ÍNDICE]** as properties de `ThreeDCamera` são `background_color`,
`background_opacity` e `frame_center`. **Não existe `.frame`.** Em
`ThreeDScene`, `self.camera.frame` levanta `AttributeError`, e todo o vocabulário
desta skill morre junto.

| Você quer | 2D (esta skill) | 3D (`manim-3d-camera`) |
|---|---|---|
| aproximar | `frame.animate.set(width=…)` / `.scale(k)` | `set_camera_orientation(zoom=…)` / `move_camera(zoom=…)` |
| deslocar | `frame.animate.move_to(…)` | `frame_center=` em `move_camera` |
| girar | **não existe** (§1.2) | `phi` / `theta` / `gamma` |
| seguir um objeto | updater no `frame` (§6) | `move_camera` a cada trecho |

E as duas classes **não combinam**: `ThreeDScene` e `MovingCameraScene` fixam
`camera_class` no `__init__`, o MRO resolve uma só, e a que perder deixa de
existir. `manim-3d-camera §2` é dona dessa explicação — não a duplique.

`manim-3d-camera` também é dona de `SpecialThreeDScene` (que está quebrada na
0.21) e de tudo que envolva `add_fixed_in_frame_mobjects`.

---

## 12. Fronteira com o renderer `opengl` — outra câmera inteira

Com `--renderer opengl`, `OpenGLRenderer.__init__` faz `self.camera =
OpenGLCamera()` **incondicionalmente** (`renderer/opengl_renderer.py:513`)
**[FONTE]** — o seu `camera_class` é ignorado. E `OpenGLCamera` **é** um
`OpenGLMobject` (`bases: ['OpenGLMobject']` **[ÍNDICE]**), sem atributo `frame`
e sem `__getattr__` que o sintetize.

```
AttributeError: 'OpenGLCamera' object has no attribute 'frame'
```

Sob opengl, **a câmera é o próprio frame**:

```python
self.play(self.camera.animate.scale(0.5).move_to(dot))   # em vez de self.camera.frame
self.camera.to_default_state()                            # volta ao enquadramento inicial
largura, altura = self.camera.get_shape()                 # frame_shape
```

**[ÍNDICE]** `OpenGLCamera(frame_shape=None, center_point=None, euler_angles=None,
focal_distance=2.0, light_source_position=None, orthographic=False,
minimum_polar_angle=-π/2, maximum_polar_angle=π/2, model_matrix=None)`, com
`set_euler_angles`, `set_phi/theta/gamma`, `increment_phi/theta/gamma`,
`get_center`, `get_shape`, `to_default_state`, `rotate`.

Duas notas de fronteira:

- **`ZoomedScene` é cairo-only, na prática.** `activate_zooming` chama
  `self.renderer.camera.add_image_mobject_from_camera(...)`
  (`zoomed_scene.py:149`) **[FONTE]**, método que só existe em `MultiCamera`.
  Sob opengl a câmera é `OpenGLCamera` → `AttributeError`. **[INFERIDO — não
  executado]**
- **o custo de §7 não se aplica.** `get_moving_and_static_mobjects` só roda sob
  `RendererType.CAIRO` (`scene/scene.py:1347`) **[FONTE]**; sob opengl não há
  frame estático a perder.

A escolha entre cairo e opengl por **tempo medido** é de `manim-gpu-encoding`
(que derrubou o "opengl economiza 19%"). A API do ManimGL do 3b1b — onde
`self.frame`/`self.camera.frame` é o idioma normal em qualquer cena — é de
`manimgl-3b1b §10.6`.

---

## 13. Câmera dentro de uma cena EM PARTES (o formato do deck de aulas)

O formato — mixin com os atos, `_corte(n)`, subclasses `P1..PN`, o mixin que
**não** herda de `Scene` — é de `manim-presentation-parts`. Aqui ficam só as
quatro coisas que mudam quando a câmera entra nele.

**1. A base muda para todas as partes.** As classes `PN` herdam
`(Mixin, CenaBase)`; trocar `CenaBase` para `MovingCameraScene` afeta a cena
inteira, inclusive as partes que não mexem na câmera — e §7 diz que isso já
custa. Se só um ato precisa de zoom, considere fazer o "zoom" com os mobjects
(`VGroup.animate.scale(2).move_to(ORIGIN)`) em vez de com a câmera.

**2. O estado do frame atravessa o corte, e isso é bom.** `next_section(
skip_animations=True)` executa a animação até o estado final e só não grava
frames — então, ao renderizar a parte 6, o frame da câmera chega nela exatamente
onde a parte 5 o deixou. É o mesmo mecanismo que faz o primeiro frame da parte
N+1 ser, pixel a pixel, o último da N. **Não reconstrua o enquadramento na mão
no começo de cada parte** — além de redundante, é a maneira mais fácil de
quebrar a emenda.

**3. Nunca corte no meio de um movimento de câmera.** O corte deve cair num
ponto de repouso (é a regra 5.7 de `manim-presentation-parts`), e com câmera isso
é mais forte: um `_corte` no meio de um pan deixa a parte N terminando com a
tela deslizando e a parte N+1 começando com ela ainda deslizando — e entre as
duas há o **frame parado** em que o professor fala. Pan é um ato inteiro:
começa parado, termina parado.

**4. O pôster é o último frame** — e portanto o **enquadramento** do último
frame. Uma parte que termina com a câmera fechada num detalhe produz um pôster
(e uma página de PDF) que mostra só aquele detalhe, sem contexto. Se o pôster
precisa mostrar o todo, a última coisa do ato é o `Restore` da câmera.

Um alerta de manutenção que vale a pena: a tabela de alcance de re-render de
`manim-presentation-parts` ("o que **sobrevive** ao ato decide o alcance") tem
uma consequência dura aqui — **enquadramento sempre sobrevive**. Mexeu na câmera
no ato 5? Re-renderize da P5 até a última. Não existe "mexi só no zoom, é local".

Registro honesto: **nenhuma das 12 cenas do deck consumidor
(`~/Projects/aulas/aulas/*/manim/`) usa `MovingCameraScene` ou `ZoomedScene`
hoje** — conferido por `grep` em 2026-08-19. Esta seção é receita derivada do
formato, **não** prática observada.

---

## 14. Quando NÃO mover a câmera

A pergunta antes de qualquer coisa nesta skill: *dá para resolver mexendo nos
mobjects?* Quase sempre dá, e quase sempre é melhor.

| Situação | Câmera | Alternativa melhor |
|---|---|---|
| "esse detalhe é pequeno demais" | zoom | desenhe-o maior desde o começo; o palco é 14,222 × 8 e cabe |
| "quero mostrar A e depois B" | pan | `FadeOut(A)` + `FadeIn(B)` no mesmo lugar — o olho não precisa viajar |
| "a lista é longa demais para a tela" | pan vertical | corte em partes (`manim-presentation-parts`) — o professor controla o ritmo |
| "quero ampliar um pedaço do gráfico" | `ZoomedScene` | um segundo `Axes` menor com o recorte, ao lado (`manim-graphs-plots`) |
| "quero enfatizar este elemento" | zoom | `Indicate`, `Circumscribe`, `SurroundingRectangle` — **órfãos de skill hoje**, confira com `bin/mx show` |

Movimento de câmera é caro em atenção: enquanto a câmera anda, ninguém lê nada
na tela. Em vídeo de aula, onde cada parte tem um recado falado, um pan de 1,5 s
é 1,5 s em que o professor não pode dizer nada novo. Use quando o **espaço
percorrido for a informação** (um mapa, uma linha do tempo, um diagrama grande
demais para caber legível) — não para dar dinamismo.

E o caso em que a câmera é claramente certa: **manter a escala do desenho e
mudar só o recorte**. Ampliar mobjects muda a espessura de traço e o tamanho do
texto relativo ao resto; mover a câmera preserva as duas coisas.

---

## 15. Conferir sem renderizar

Antes de gastar GPU, dá para responder "isso está enquadrado?" com aritmética.

**a) `is_in_frame` respeita a câmera móvel.** **[FONTE]** `camera.py:485-510`:

```python
fc, fh, fw = self.frame_center, self.frame_height, self.frame_width
return not (mob.get_right()[0] < fc[0] - fw/2 or mob.get_bottom()[1] > fc[1] + fh/2
            or mob.get_left()[0] > fc[0] + fw/2 or mob.get_top()[1] < fc[1] - fh/2)
```

Numa `MovingCameraScene`, `fc/fh/fw` são lidos do frame **atual**, então
`self.camera.is_in_frame(mob)` responde pela câmera de agora. Duas ressalvas:

- é teste de **interseção**, não de contenção: um mobject metade fora devolve
  `True`;
- é caixa delimitadora, não pixel.

**b) Contenção de verdade**, que é o que costuma interessar:

```python
def cabe(cam, mob, folga=0.0):
    fc, fw, fh = cam.frame_center, cam.frame_width, cam.frame_height
    return (mob.get_left()[0]   >= fc[0] - fw/2 + folga and
            mob.get_right()[0]  <= fc[0] + fw/2 - folga and
            mob.get_bottom()[1] >= fc[1] - fh/2 + folga and
            mob.get_top()[1]    <= fc[1] + fh/2 - folga)
```

**c) O que o zoom faz com a legibilidade.** Ampliação = `config.frame_width /
self.camera.frame.width`. Um `Text(font_size=24)` numa câmera com `width=4`
aparece com o mesmo tamanho aparente de um `font_size` ~85 no enquadramento
cheio (`24 · 14,222/4`). **[CALCULADO]** É a conta que evita a legenda gigante
que ninguém previu — e o inverso: texto que fica ilegível quando a câmera se
afasta.

**d) Nada disso substitui olhar o PNG.** Câmera deformada (§3), lupa preta
(§8.6) e borda invisível (§8.5) **não têm assinatura numérica** — aparecem na
imagem e em nenhum outro lugar. O ciclo escrever → renderizar rápido → **olhar
o PNG** → corrigir é de `manim-verificacao-visual`.

---

## 16. Sintoma → causa → correção

| Sintoma | Causa | Correção |
|---|---|---|
| a cena inteira achatou/esticou | `camera.frame_width =` ou `frame_height =` (stretch) | `frame.set(width=…)` ou `frame.scale(k)` — §3 |
| `AttributeError: … no attribute 'frame'` numa cena 2D | herdou de `Scene`, não de `MovingCameraScene` | trocar a base — §2.1 |
| idem, mas em 3D | `ThreeDCamera` não tem `.frame` | `zoom=` / `frame_center=` — §11, `manim-3d-camera` |
| idem, com `OpenGLCamera` | `--renderer opengl` ignora `camera_class` | use `self.camera` direto — §12 |
| o updater da câmera não roda | o frame não está em `self.mobjects` | `self.add(self.camera.frame)` — §6.1 |
| a câmera restaura e **pula** de volta | updater retomado no `finish()` da animação | `clear_updaters()` antes — §6.3 |
| `auto_zoom` não fez nada | faltou `self.play(...)` (devolve builder) | `self.play(self.camera.auto_zoom(g))` — §4.3a |
| `Exception: Could not determine bounding box…` | conjunto vazio, ou `only_mobjects_in_frame` sem nada em quadro | teste `len()` antes — §4.3b |
| `Exception: Trying to restore without having saved` | `Restore` sem `save_state()` | §5.2 |
| a lupa não aparece | faltou `activate_zooming()` | §8.2 |
| passei `zoom_activated=True` e nada | parâmetro morto | `activate_zooming()` — §8.4 |
| `image_frame_stroke_width` não muda a moldura | parâmetro morto | `self.zoomed_display.display_frame.set_stroke(width=…)` — §8.4 |
| o zoom da lupa foi para o lado errado | `zoom_factor` é o inverso da ampliação | diminua o número — §8.3 |
| inset com fundo preto em slide branco | a sub-câmera nasceu com o fundo antigo | `config.background_color` antes de `super().setup()` — §8.6 |
| não se vê a borda da lupa nem do inset | dois defaults `WHITE` | `set_stroke` nos dois — §8.5 |
| `AttributeError: … 'zoomed_camera'` | `setup()` sobrescrito sem `super().setup()` | §8.10 |
| `TypeError: __init__() missing 2 required positional arguments` | `SplitScreenCamera` como `camera_class` | não use — §9.1 |
| a cena ficou lenta ao mover a câmera | dois caches desligados | §7; meça com `manim-gpu-encoding` |
| a lupa engasgou quando dei zoom na câmera principal | pixel array da sub-câmera explodiu | não combine os dois — §8.7 |
| fundo congelado enquanto a câmera anda | pan numa `Scene` comum via `frame_center` | herde de `MovingCameraScene` — §10.1 |
| girei o frame e a imagem não girou | não há rotação de câmera em 2D | §1.2 |
| rastro do enquadramento antigo durante um pan | **não acontece** com `.animate`: o frame entra sozinho na cena (§7, item 1). Se acontecer, o pan veio de **updater** | §6.1 — `self.add(self.camera.frame)` na abertura |

---

## 17. Onde esta skill para

| Assunto | Skill dona |
|---|---|
| 3D, `phi`/`theta`/`gamma`, `move_camera`, `ThreeDCamera`, `add_fixed_in_frame_mobjects`, `SpecialThreeDScene` | `manim-3d-camera` |
| de qual `Scene` herdar em geral, ciclo `setup`/`construct`/`tear_down`, `next_section`, `Section` | `manim-cenas-secoes` |
| `run_time`, `rate_func`, `lag_ratio`, `AnimationGroup`, `path_func`, orçamento de tempo do movimento | `manim-composicao-ritmo` |
| catálogo de animações, `Transform` × `ReplacementTransform`, `Restore`/`ApplyMethod` como classes | `manim-animations` |
| escrever updater, `dt`, `always_redraw`, `ValueTracker`, animação × updater | `manim-updaters-valuetracker` |
| `move_to`, `next_to`, buffers, `arrange`, "cabe na tela?", 9:16 | `manim-layout-posicionamento` |
| `VGroup` × `Group` (o inset é `ImageMobject`!), submobjects, formas | `manim-mobjects` |
| `background_color`, `background_opacity` e a catraca do `.mov`, contraste, o branco que some | `manim-color-theming` |
| imagem de fundo, `ImageMobject`, SVG, `background_image` | `manim-svg-imagens` |
| corte em partes, mixin, `_corte`, emenda, métrica direcional, pôster | `manim-presentation-parts` |
| olhar o PNG, comparar frames, conferir o pôster, `--format png` | `manim-verificacao-visual` |
| `Axes`, `plot`, `c2p`, gráfico ao qual você quer dar zoom | `manim-graphs-plots` |
| cache de partial movie, custo de rasterizar, `--no-cache` | `manim-performance-cache` |
| codec, NVENC, cairo × opengl **por tempo medido**, `mx bench` | `manim-gpu-encoding` |
| a API do ManimGL do 3b1b (`self.frame`, `CameraFrame`) | `manimgl-3b1b` |
| achar assinatura, kwarg, "esse método existe mesmo?" | `manim-api-discovery` |
| render falhou por ambiente, traceback, bissecção | `manim-troubleshooting` |
| escrever `Mobject`/`Animation` própria | `manim-mobjects-customizados` |

**Sem skill dona hoje** — declare o buraco, não improvise:

- **ênfase e anotação** (`Indicate`, `Circumscribe`, `FocusOn`, `Flash`,
  `SurroundingRectangle`, `Brace*`) — é a alternativa nº 1 ao zoom (§14) e não
  tem guia. Confira cada um com `bin/mx show <Nome>` antes de escrever.
- **`LinearTransformationScene` / `VectorScene`** — outras duas subclasses de
  `Scene` com câmera própria; `manim-cenas-secoes` lista, ninguém ensina.
- **renderer OpenGL do CE** (`OpenGLCamera` inclusive) — órfão de propósito;
  §12 dá só o mínimo para não travar.

---

## 18. O que aqui NÃO foi verificado

Nada foi renderizado, medido ou executado nesta revisão. Todo mecanismo veio de
leitura do fonte instalado e do índice estático. Ficam explicitamente **não
verificados**:

1. **Todo custo de §7.** Que os dois caches são desligados está provado no
   fonte; **quanto** isso custa não foi medido, e esta skill não cita nenhum
   número. Quem for medir: `manim-gpu-encoding`, nunca a olho.
2. **Os 65 MB por frame de §8.7.** É aritmética sobre a fórmula de
   `multi_camera.py:62-73`, não uma leitura de memória.
3. **A deformação de §3.2 (2,03×).** Sai da conta de `points_to_pixel_coords`;
   nenhum PNG foi olhado para confirmar o aspecto visual.
4. **`ZoomedScene` sob `--renderer opengl` (§12).** A ausência de
   `add_image_mobject_from_camera` em `OpenGLCamera` está no índice; o
   `AttributeError` não foi provocado.
5. **`SplitScreenCamera` como `camera_class` (§9.1).** O `TypeError` é
   consequência direta de `camera_cls()` sem argumentos; não foi reproduzido.
6. **`functools.partial` como `camera_class` (§9.3b).** Funciona pelo que o
   código faz; contraria a anotação de tipo e não foi executado.
7. **A ordem de `setup()` de §8.6/§8.10.** Deduzida de onde a sub-câmera é
   construída; nenhum inset foi visto preto nem branco aqui.
8. **Os exemplos oficiais de §2.4 e §8.1.** São cópia dos docstrings do
   ManimCE 0.21 — a biblioteca os publica como corretos, mas não foram rodados
   nesta máquina nesta revisão.
9. **§13 inteira.** É receita derivada do formato de `manim-presentation-parts`;
   o deck consumidor **não** tem hoje nenhuma cena com câmera móvel
   (`grep` em `~/Projects/aulas/aulas/`, 2026-08-19).
10. ~~**A pergunta em aberto de §7**~~ — **FECHADA nesta rodada, por leitura.**
    `Scene.add_mobjects_from_animations` (`scene.py:535-545`, chamado em
    `:1321`) adiciona à cena o mobject de qualquer animação não-introducer — o
    frame incluído. Não há rastro; os exemplos oficiais estão certos. A §7 (item 1) foi
    reescrita com o resultado. Fica de pé só a parte de *updater*, que não passa
    por `play` e por isso ainda pede o `self.add` explícito (§6.1).
