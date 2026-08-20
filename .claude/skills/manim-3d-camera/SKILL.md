---
name: manim-3d-camera
description: >-
  Cena TRIDIMENSIONAL no ManimCE — `ThreeDScene`, a `ThreeDCamera` (phi, theta,
  gamma, zoom, focal_distance, frame_center), `ThreeDAxes`, `Surface` e os
  sólidos (`Sphere` `Cube` `Prism` `Cone` `Cylinder` `Torus` `Line3D` `Arrow3D`
  `Dot3D` `Polyhedron` e os 5 poliedros regulares), órbita e ilusão de rotação,
  texto legível em 3D (`add_fixed_in_frame_mobjects` /
  `add_fixed_orientation_mobjects`), sombreamento e a ordem de desenho por
  profundidade. Use quando o pedido for "faz em 3D", "gira em torno do objeto",
  "plota uma superfície / z = f(x,y)", "põe eixos 3D", "monta um cubo/esfera/
  toro", "a câmera não se move", "o texto entortou / sumiu atrás da superfície",
  "os sólidos aparecem na ordem errada / um atravessa o outro", "phi e theta",
  "a cena 3D está lentíssima", "o mesmo código muda de cara com --renderer
  opengl", ou quando aparecer `AttributeError: 'OpenGLCamera' object has no
  attribute 'set_zoom'` / `'...' object has no attribute 'renderer'`. NÃO use
  para câmera 2D — pan, zoom, seguir um objeto, `MovingCameraScene`,
  `ZoomedScene`, `MultiCamera`, `SplitScreenCamera`, `self.camera.frame` (skill
  `manim-camera-2d`); para escolher de qual `Scene` herdar em geral e para
  `next_section` (skill `manim-cenas-secoes`); para codec, NVENC e a escolha
  cairo × opengl por TEMPO medido (skill `manim-gpu-encoding`); para eixos e
  gráficos 2D (skill `manim-graphs-plots`); para o formato de vídeo em partes
  do slide (skill `manim-presentation-parts`); nem para a API do ManimGL em si
  (skill `manimgl-3b1b`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# 3D no ManimCE — a câmera, a profundidade e o custo

Tudo aqui foi conferido contra o índice estático (`api/manim-ce-index.tsv`,
`api/manim-ce-methods.tsv`, `api/manim-ce-api.json.gz`) e contra o fonte
instalado em `.venv/lib/python3.12/site-packages/manim/` — **ManimCE 0.21.0**.
Onde a afirmação vem de leitura de código e **não** de execução, está escrito
`[LIDO, NÃO EXECUTADO]`. Nenhum render foi feito nesta rodada; a seção 18 lista
o que ficou por medir.

---

## 1. O modelo mental: no cairo não existe z-buffer

Esta é a única coisa que, entendida, resolve dois terços dos defeitos de cena
3D no ManimCE. **O renderer cairo não tem buffer de profundidade.** Ele desenha
uma lista de mobjects em ordem, um por cima do outro — algoritmo do pintor. A
`ThreeDCamera` só decide a ORDEM, e decide usando **um ponto por submobject**:

```python
# manim/camera/three_d_camera.py, get_mobjects_to_display
def z_key(mob):
    if not (hasattr(mob, "shade_in_3d") and mob.shade_in_3d):
        return np.inf
    return np.dot(mob.get_z_index_reference_point(), rot_matrix.T)[2]

return sorted(mobjects, key=z_key)
```

e `get_z_index_reference_point()` é, por padrão, **`mob.get_center()`**
(`manim/mobject/mobject.py:2417-2420`). Ou seja: a profundidade de uma peça é a
profundidade do CENTRO dela. Cinco consequências, todas verificadas no fonte:

1. **Duas superfícies que se interpenetram não podem sair certas.** Cada uma é
   desenhada inteira, antes ou depois da outra. A saída é: fatie a que atravessa
   em pedaços menores (mais `resolution`), ou não faça interpenetração.
2. **`shade_in_3d=False` ⇒ `z_key = inf` ⇒ desenhado por ÚLTIMO, sempre em
   cima.** É o caso de todo `Text`, `MathTex`, `Line`, `Dot` comum — o default
   de `VMobject.__init__` é `shade_in_3d: bool = False`
   (`vectorized_mobject.py:126`). Por isso um rótulo nunca some atrás de uma
   esfera: ele flutua na frente de tudo, ainda que geometricamente esteja atrás.
3. **`z_index` não some — ele fica subordinado.** `Camera(use_z_index=True)` é o
   default e a lista chega ao `sorted` já ordenada por `z_index`; como o
   `sorted` do Python é **estável**, o `z_index` só decide empates de `z_key`.
   Na prática: **`z_index` ordena os planos entre si dentro do grupo `inf`** (o
   seu HUD, os rótulos, as linhas 2D) e é sobrescrito por qualquer diferença de
   profundidade real. Ele não "não funciona"; ele funciona no segundo nível.
4. **`set_shade_in_3d(value=True, z_index_as_group=False)`** (`VMobject`,
   `vectorized_mobject.py:787-793`) liga a participação na ordenação para a
   família inteira. Com `z_index_as_group=True` ele grava `submob.z_index_group
   = self`, e aí **todos os submobjects passam a usar o centro do GRUPO** como
   profundidade — o objeto composto vira uma peça só e nunca é fatiado por
   outro. É a correção certa quando uma curva 3D fica "costurada" no meio de uma
   superfície.
5. **Cor sofre a mesma ordenação.** `fill_opacity < 1` num sólido significa que
   você vê as faces de trás; combinado com ordenação por centroide, o resultado
   é instável durante uma órbita. Sólido que precisa parecer sólido usa
   `fill_opacity=1`.

O renderer **opengl** tem `depth_test=True` de verdade (`OpenGLSurface`,
`OpenGLMobject.__init__` guarda `self.depth_test`) e ordena por triângulo — mas
troca de renderer troca meia dúzia de outras coisas por baixo. Seção 11.

---

## 2. Qual classe de cena

| Classe | Câmera | Use para | Skill dona |
|---|---|---|---|
| `Scene` | `Camera`, fixa | 2D | `manim-mobjects` |
| **`ThreeDScene`** | **`ThreeDCamera`** | **3D orbital** | **esta** |
| `MovingCameraScene` | `MovingCamera` | pan/zoom 2D (`self.camera.frame`) | `manim-camera-2d` |
| `ZoomedScene` | `MultiCamera` | lupa num inset 2D | `manim-camera-2d` |
| `LinearTransformationScene`, `VectorScene` | `Camera` | álgebra linear 2D | **órfã** (§17) |
| `SpecialThreeDScene` | — | **não use: está quebrada** | — |

```python
class ThreeDScene(Scene):
    def __init__(self, camera_class=ThreeDCamera, ambient_camera_rotation=None,
                 default_angled_camera_orientation_kwargs=None, **kwargs)
```

`default_angled_camera_orientation_kwargs` cai em `{"phi": 70*DEGREES, "theta":
-135*DEGREES}` e só é usado por `set_to_default_angled_camera_orientation()`.
`ambient_camera_rotation` é guardado como atributo e **nunca lido** — não
adianta passá-lo.

### `ThreeDScene` + `MovingCameraScene` não combinam — e agora com o motivo

O motivo não é gosto: as duas fixam `camera_class` em `__init__`, e o MRO
resolve **uma** delas. Se `ThreeDScene` vier primeiro, a câmera é
`ThreeDCamera`, que **não tem `.frame`** — a propriedade `frame` existe em
`MovingCamera` (`camera/moving_camera.py`), e o índice confirma que as
propriedades de `ThreeDCamera` são só `background_color`, `background_opacity`
e `frame_center`. Todo o vocabulário de `MovingCameraScene`
(`self.camera.frame.animate.scale(...)`) morre com `AttributeError`. Para
enquadrar em 3D use `zoom=` e `frame_center=`; §3.

### `SpecialThreeDScene` está morta na 0.21 — **[MEDIDO]**

`scene/three_d_scene.py:483` faz, **antes** de chamar `super().__init__()`:

```python
if self.renderer.camera_config["pixel_width"] == config["pixel_width"]:
```

`self.renderer` só é criado dentro de `Scene.__init__` (`scene/scene.py:208-216`)
e `Scene` não tem `__getattr__` nem atributo de classe `renderer` — logo,
instanciar levanta `AttributeError: ... object has no attribute 'renderer'`. E,
mesmo que passasse, `renderer.camera_config` não existe em lugar nenhum: o
`CairoRenderer` cria a câmera com `self.camera = camera_cls()`, **sem argumento
nenhum** (`renderer/cairo_renderer.py:47-48`), e `camera_config` só aparece em
`three_d_scene.py` e `zoomed_scene.py`. O caminho de baixa qualidade ainda
repassaria `camera_config=` a `Scene.__init__`, que não aceita esse kwarg.

Confira em 2 s, sem render:

```bash
grep -n "self.renderer.camera_config" .venv/lib/python3.12/site-packages/manim/scene/three_d_scene.py
grep -n "self.camera = camera_cls()"   .venv/lib/python3.12/site-packages/manim/renderer/cairo_renderer.py
```

O que `SpecialThreeDScene` oferecia (eixos com hastes cortadas, esfera com
resolução maior, sombreamento configurado) se reproduz em 6 linhas com
`ThreeDAxes(...)`, `Sphere(resolution=(24, 48))` e mutação da câmera no
`setup()`.

---

## 3. A `ThreeDCamera`: cinco números e um ponto

```python
class ThreeDCamera(Camera):
    def __init__(self, focal_distance=20.0, shading_factor=0.2, default_distance=5.0,
                 light_source_start_point=array([-7., -9., 10.]),
                 should_apply_shading=True, exponential_projection=False,
                 phi=0, theta=-1.5707963267948966, gamma=0, zoom=1, **kwargs)
```

Os cinco números vivem em **`ValueTracker`s** (`phi_tracker`, `theta_tracker`,
`focal_distance_tracker`, `gamma_tracker`, `zoom_tracker`) — é por isso que a
câmera pode ser animada, encadeada em updater e lida no meio da cena. O ponto é
`_frame_center`, um `Point` mobject; a propriedade pública `frame_center` lê e
escreve nele.

| Parâmetro | Significado | Default | Faixa útil |
|---|---|---:|---|
| `phi` | ângulo polar: 0 = olhando de cima, para baixo no eixo Z; π/2 = de lado | **0** | 55°–80° |
| `theta` | azimute: gira em torno de Z | **−90°** | qualquer |
| `gamma` | rolagem (gira a imagem no próprio plano) | 0 | quase sempre 0 |
| `zoom` | multiplica x e y na projeção; >1 aproxima, <1 afasta | 1 | 0,6–1,4 |
| `focal_distance` | distância focal da projeção perspectiva | 20,0 | ver abaixo |
| `frame_center` | ponto que a projeção usa como origem | ORIGIN | ver a ressalva |

**A primeira armadilha é o default.** `phi=0` significa **olhando de cima para
baixo, direto no eixo Z**: uma `ThreeDScene` sem `set_camera_orientation` é
visualmente indistinguível de uma `Scene` 2D. Quem escreve "fiz em 3D e ficou
igual" quase sempre esqueceu essa linha.

**Tudo em radianos.** `DEGREES = 0.017453292519943295` (= π/180). `phi=70` são
~11 voltas; escreva `70 * DEGREES`.

### A matemática que decide o que você vê

`project_points` (`camera/three_d_camera.py:305-340`), depois de rotacionar os
pontos para o espaço da câmera:

```python
factor = focal_distance / (focal_distance - zs)
factor[(focal_distance - zs) < 0] = 10**6
points[:, i] *= factor * zoom      # i em 0, 1
```

Três leituras práticas:

- **Perspectiva quase ortográfica de graça:** `focal_distance=100` faz `factor`
  ficar entre 0,96 e 1,04 para geometria dentro do quadro — as arestas paralelas
  param de convergir. É o visual de diagrama técnico, sem trocar de renderer.
  `focal_distance=6` faz o oposto: perspectiva forte, quase lente grande-angular.
- **`focal_distance` é um teto rígido.** Qualquer ponto cuja profundidade em
  espaço de câmera chegue a `focal_distance` recebe `factor = 10**6` e é atirado
  para fora do universo. Com o default 20 e um quadro de ±4 isso não acontece —
  mas uma `Sphere(radius=25)` acontece. **Correção:** uma versão anterior citava
  também `ThreeDAxes(z_range=[-30, 30])`. Não vale: `z_range` é o domínio de
  DADOS, e o eixo z mede `z_length` unidades de PALCO — default
  `config.frame_height - 1.5` = **6,5** (`coordinate_systems.py:2453`), repassado
  como `axis_config["length"]` (`:2067`) qualquer que seja o `z_range`. |z| ≤
  3,25, longe dos 20. Quem estoura o teto é geometria grande em unidades de
  palco, não intervalo de dados grande.
  Sintoma: um risco atravessando a tela inteira, ou o mobject some.
- **`exponential_projection=True`** troca `factor` por `exp(z/d)` do lado
  positivo, suavizando exatamente esse artefato. Default `False`; ligue mutando
  a câmera (abaixo), não por construtor.

### A câmera não se configura por construtor — **[LIDO, NÃO EXECUTADO]**

`CairoRenderer.__init__` faz `self.camera = camera_cls()`. **Nenhum kwarg
chega à câmera.** Não existe `camera_config` em `Scene` na 0.21. Para mexer em
`focal_distance`, `should_apply_shading`, `light_source_start_point` ou
`exponential_projection`, mute a instância — o lugar certo é `setup()`, que roda
antes de `construct()`:

```python
class Diagrama(ThreeDScene):
    def setup(self):
        super().setup()
        self.camera.exponential_projection = True
        self.camera.should_apply_shading = False   # visual chapado, sem gradiente
        self.camera.light_source.move_to([0, -6, 8])
        self.set_camera_orientation(phi=68 * DEGREES, theta=-40 * DEGREES,
                                    focal_distance=60, zoom=0.95)
```

`focal_distance` e `zoom` também entram por `set_camera_orientation`, que é a
via documentada; os outros três não têm parâmetro lá.

### `frame_center`: use com desconfiança — **[LIDO, NÃO EXECUTADO]**

`project_points` começa com `points = points - frame_center`; depois,
`Camera.points_to_subpixel_coords` (`camera/camera.py:1226-1227`) faz
`shifted_points = points - self.frame_center` **de novo**, agora já em espaço de
câmera. Com o default `ORIGIN` as duas subtrações são zero e nada disso aparece. Com
`frame_center=[3, 0, 0]` o deslocamento entra duas vezes e o ponto que você
mandou centralizar **não** vai para o centro da tela. Não reproduzi por render
— mas a leitura é direta e o efeito é grande. Prefira mover a geometria (`VGroup
.move_to(ORIGIN)`) a mover o `frame_center`; se usar, **confira um PNG** antes
de confiar no valor.

E há um detalhe de custo escondido: `move_camera` remove `self.camera
._frame_center` da cena logo depois da animação, com um comentário explicando
que, se o Manim achar que o `frame_center` está se movendo, ele redesenha tudo
(`three_d_scene.py:304-310`). Ver §12.

### Ler a câmera no meio da cena

```python
self.camera.get_phi()             # -> float, radianos
self.camera.get_theta()
self.camera.get_gamma()
self.camera.get_zoom()
self.camera.get_focal_distance()
self.camera.get_rotation_matrix() # 3x3, a matriz em vigor
self.camera.project_point(p)      # Point3D -> Point3D já projetado
```

Todos existem como métodos próprios de `ThreeDCamera` (conferido em
`api/manim-ce-methods.tsv`). E a posição implícita da câmera, quando você
precisa apontar um rótulo ou uma luz para ela, sai de
`manim.utils.space_ops.spherical_to_cartesian((r, theta, phi))` — a convenção do
módulo (`theta` = azimute, `phi` = polar) é **exatamente** a da câmera:

```python
from manim.utils.space_ops import spherical_to_cartesian
olho = spherical_to_cartesian((10, self.camera.get_theta(), self.camera.get_phi()))
```

---

## 4. Mover a câmera

### Salto instantâneo

```python
def set_camera_orientation(self, phi=None, theta=None, gamma=None, zoom=None,
                           focal_distance=None, frame_center=None, **kwargs)
```

Escreve direto nos trackers. Sem animação, sem `run_time`. É a primeira linha
de quase toda cena 3D.

### Movimento animado

```python
def move_camera(self, phi=None, theta=None, gamma=None, zoom=None,
                focal_distance=None, frame_center=None,
                added_anims=[], **kwargs)
```

Monta um `tracker.animate.set_value(v)` para cada valor não-`None` e chama
`self.play(*anims + added_anims, **kwargs)`. Duas consequências que economizam
tempo:

- **`**kwargs` vai inteiro para o `play`.** `run_time`, `rate_func` e
  `lag_ratio` funcionam aqui: `self.move_camera(theta=..., run_time=2.5,
  rate_func=rate_functions.ease_in_out_sine)`. O vocabulário de ritmo é da skill
  `manim-composicao-ritmo`.
- **`added_anims` é o jeito de fazer a cena andar enquanto a câmera anda.** Sem
  ele você gasta dois `play` e o espectador vê duas ações onde havia uma:
  ```python
  self.move_camera(phi=55 * DEGREES, theta=25 * DEGREES, run_time=2,
                   added_anims=[FadeIn(rotulo), sup.animate.set_fill(opacity=0.6)])
  ```

### Órbita automática

```python
def begin_ambient_camera_rotation(self, rate=0.02, about="theta")
def stop_ambient_camera_rotation(self, about="theta")
```

`rate` é em **radianos por segundo** (`x.increment_value(rate * dt)`), então o
default 0,02 rad/s dá uma volta em ~5 min — quase sempre lento demais. Para uma
volta completa em `T` segundos, `rate = TAU / T`. `about` aceita `"theta"`,
`"phi"` ou `"gamma"`.

Quatro armadilhas, todas do fonte:

1. **A órbita só acontece durante tempo que passa.** `begin_...()` seguido de
   `self.play(...)` de 3 s gira 3 s. Sem `wait`/`play` depois, não gira nada.
2. **`stop_ambient_camera_rotation()` tem `about="theta"` como default e NÃO
   lembra o que você começou.** Se ligou com `about="phi"` e parou sem
   argumento, o `stop` limpa os updaters do tracker de theta (que não tem
   nenhum) e **o phi continua girando** pelo resto da cena, sem erro. Pare com o
   mesmo `about` com que começou.
3. **A mensagem de erro mente.** Todo o corpo está dentro de um `try/except
   Exception` que re-levanta como `ValueError("Invalid ambient rotation
   angle.")`. Qualquer falha ali dentro — não só um `about` inválido — sai com
   esse texto.
4. **A órbita mata o cache de frame estático.** `begin_...` adiciona o
   `ValueTracker` à cena; ele tem updater, logo está "se movendo"; e
   `ThreeDScene.get_moving_mobjects` devolve `self.mobjects` inteiro quando um
   mobject de câmera se move. §12.

### Ilusão de rotação (a "respiração" do 3blue1brown)

```python
def begin_3dillusion_camera_rotation(self, rate=1, origin_phi=None, origin_theta=None)
def stop_3dillusion_camera_rotation(self)
```

Não é uma órbita: são duas oscilações em torno da posição atual, com amplitude
fixa no código — `theta` oscila `±0.2 rad` (≈ ±11,5°) por `0.2*sin(t*rate)` e
`phi` oscila `0.1*cos(t*rate) − 0.1` (≈ 0 a −11,5°, sempre para baixo). Serve
para dar volume a um objeto parado sem tirá-lo do lugar. `rate` aqui é a
frequência angular da oscilação, não velocidade de giro. O `stop` não tem
parâmetro e limpa os dois trackers.

### O caminho cru: updater no tracker

Quando você quer a câmera amarrada a outra coisa (seguir um ponto, acelerar com
o gráfico), mexa no tracker direto:

```python
self.camera.theta_tracker.add_updater(lambda m, dt: m.increment_value(0.6 * dt))
self.add(self.camera.theta_tracker)     # sem isto o updater não roda
...
self.camera.theta_tracker.clear_updaters()
self.remove(self.camera.theta_tracker)
```

O `self.add` é obrigatório pelo mesmo motivo que em 2D: updater só roda em
mobject que está na cena. A mecânica de `ValueTracker` e updaters é da skill
`manim-updaters-valuetracker`.

---

## 5. Texto e HUD em 3D

Um `Text` comum numa cena 3D é um mobject plano deitado no plano XY: ele é
projetado junto com o resto, então **entorta** com a câmera. Como
`shade_in_3d=False`, ele nunca fica escondido — fica na frente, torto. Há três
respostas, e elas resolvem problemas diferentes.

### (a) Fixo na tela — o HUD

```python
def add_fixed_in_frame_mobjects(self, *mobjects: Mobject)
def remove_fixed_in_frame_mobjects(self, *mobjects: Mobject)
```

O mobject deixa de ser projetado: `transform_points_pre_display` devolve os
pontos crus (`three_d_camera.py:367-368`). É título, legenda, rodapé, contador.

```python
titulo = Text("Superfície de sela", color=BLACK).to_corner(UL)   # cor SEMPRE explícita — §13
self.add_fixed_in_frame_mobjects(titulo)     # ele JÁ adiciona à cena
```

**`ThreeDScene.add_fixed_in_frame_mobjects` faz `self.add(*mobjects)` por
dentro** (`three_d_scene.py:361-372`, linha 370). Um `self.add(titulo)` antes é
redundante; depois, inofensivo.

### (b) Fixo na orientação — o rótulo que gruda num ponto 3D

```python
# na Scene:
def add_fixed_orientation_mobjects(self, *mobjects, **kwargs)
# na câmera, a assinatura completa:
def add_fixed_orientation_mobjects(self, *mobjects, use_static_center_func=False,
                                   center_func=None)
```

Aqui o mobject **mantém a posição 3D** mas nunca gira: a câmera projeta só o
centro e translada a peça inteira para lá (`three_d_camera.py:369-374`). É
exatamente o que se quer num rótulo de vértice, de eixo ou de ponto notável — e
ele não encolhe com a distância, então o corpo do texto fica constante.

- `center_func` — uma função sem argumentos que devolve o ponto de ancoragem.
  Use para grudar o rótulo num alvo que se move: `center_func=lambda:
  ponta.get_center()`.
- `use_static_center_func=True` — congela o ponto de ancoragem na criação e
  evita recalcular `get_center()` a cada frame. Otimização real quando há muitos
  rótulos e nada se move.

### (c) Girar o texto para dentro de um plano

Quando o rótulo faz parte do desenho (um "z" ao lado do eixo, um nome numa
face), o certo é levá-lo ao plano da coisa:

```python
lbl = MathTex("z", color=BLACK).rotate(PI / 2, axis=RIGHT)   # deita no plano XZ
```

`ThreeDAxes` já faz isso por você — §6.

### As três armadilhas de mobject fixo, todas mecânicas

**1. A família é fotografada NO MOMENTO da chamada.** Tanto
`add_fixed_in_frame_mobjects` (via `extract_mobject_family_members`) quanto
`add_fixed_orientation_mobjects` (via `mobject.get_family()`) percorrem a
família e guardam as **identidades** num `set`/`dict`. Submobject acrescentado
DEPOIS não está lá:

```python
hud = VGroup(titulo)
self.add_fixed_in_frame_mobjects(hud)
hud.add(subtitulo)          # ERRADO: o subtitulo voa para dentro do 3D
```
Correção: monte o grupo inteiro antes, ou chame de novo depois de mexer.

**2. `become()` e `Transform` podem criar submobjects novos.** `Mobject.become`
alinha as famílias, e `add_n_more_submobjects` (`mobject.py:3079-3099`) **cria
cópias** para igualar as contagens. Essas cópias são objetos novos, fora do set.
Trocar um `Text("3")` fixo por um `Text("12")` com mais glifos vaza os glifos
extras para o 3D. **[LIDO, NÃO EXECUTADO]** — o mecanismo é direto, mas não
renderizei.
Correção: `self.add_fixed_in_frame_mobjects(hud)` de novo depois da troca; ou
use um `DecimalNumber`/`Integer` com contagem de glifos estável; ou desenhe o
número num `VGroup` de tamanho fixo.

**3. `ReplacementTransform` sempre vaza.** Ele põe o mobject-alvo na cena, e o
alvo nunca passou por `add_fixed_in_frame_mobjects`. Use `Transform` (que muta o
original e preserva a identidade) para HUD, ou fixe o alvo antes.

### E a assimetria de `remove_fixed_*`

No cairo, `remove_fixed_in_frame_mobjects` **só desfixa** — o mobject continua
na cena e volta a ser projetado em 3D, o que quase nunca é o que se queria. No
opengl, a mesma chamada faz `self.remove(mob)` (`three_d_scene.py:410-416`).
Se a intenção é "sumir com o título", escreva `self.play(FadeOut(titulo))` ou
`self.remove(titulo)` explicitamente — não conte com o `remove_fixed_*`.

---

## 6. `ThreeDAxes`

```python
class ThreeDAxes(Axes):
    def __init__(self, x_range=(-6, 6, 1), y_range=(-5, 5, 1), z_range=(-4, 4, 1),
                 x_length=10.5, y_length=10.5, z_length=6.5,
                 z_axis_config=None, z_normal=array([0., -1., 0.]),
                 num_axis_pieces=20, light_source=array([-7., -9., 10.]),
                 depth=None, gloss=0.5, **kwargs)
```

Métodos próprios (o resto vem de `Axes`/`CoordinateSystem`):

```python
get_axis_labels(x_label="x", y_label="y", z_label="z") -> VGroup
get_y_axis_label(label, edge=UR, direction=UR, buff=0.1,
                 rotation=PI/2, rotation_axis=OUT) -> Mobject
get_z_axis_label(label, edge=OUT, direction=RIGHT, buff=0.1,
                 rotation=PI/2, rotation_axis=RIGHT) -> Mobject
```

Repare que os defaults de `get_z_axis_label` já **giram o rótulo em torno de
RIGHT**, ou seja, deitam o texto no plano XZ. É a razão de usar o método em vez
de posicionar um `MathTex` na mão.

**`num_axis_pieces=20` existe por causa do §1.** Sob cairo, `_add_3d_pieces`
(`coordinate_systems.py:2518-2522`) corta cada eixo em 20 pedaços, zera o
stroke do eixo inteiro e liga `set_shade_in_3d(True)` nos pedaços — assim uma
superfície pode passar entre dois pedaços do mesmo eixo. Um eixo inteiriço teria
um centroide só e ficaria todo na frente ou todo atrás. Consequência de custo:
um `ThreeDAxes` traz **60 pedaços de eixo** antes de qualquer tick ou rótulo.
Diminuir `num_axis_pieces` acelera e piora a oclusão; sob opengl a divisão nem
acontece.

`_set_axis_shading` usa `light_source` para dar um `set_sheen(0.2)` degradê em
cada eixo — é isso que faz o eixo parecer cilíndrico. Trocar `light_source` muda
de que lado o eixo é claro.

### Coordenadas e plotagem

```python
axes.c2p(x, y, z)                  # coords_to_point, aceita 3 coordenadas
axes.p2c(ponto)                    # volta
axes.plot_parametric_curve(lambda t: np.array([...]), t_range=[0, TAU])
axes.plot_surface(f, u_range=(-3, 3), v_range=(-3, 3),
                  resolution=(24, 24),
                  colorscale=[BLUE, GREEN, YELLOW, ORANGE, RED],
                  colorscale_axis=2)   # 0=x, 1=y, 2=z
```

**`plot_surface` é o caminho certo para `z = f(x, y)`** e quase ninguém o usa —
a internet ensina a montar `Surface(lambda u, v: axes.c2p(u, v, f(u, v)))`, que
é literalmente o que ele faz por dentro (`coordinate_systems.py:997-1009`), só
que sem o `colorscale`. A função recebe `(u, v)` e devolve **só o z**.

Curva 3D solta (fora de eixos) é `ParametricFunction`, e ela nasce
`shade_in_3d=False`. Se a curva precisa passar por dentro/atrás de uma
superfície:

```python
mola = ParametricFunction(lambda u: (1.2*np.cos(u), 1.2*np.sin(u), 0.05*u),
                          t_range=(-3*TAU, 5*TAU, 0.01),
                          color=BLUE_D).set_shade_in_3d(True)
```

Eixos e gráficos **2D** (`Axes`, `NumberPlane`, `plot`, `get_area`, rótulos,
`BarChart`) são da skill `manim-graphs-plots`; aqui fica só o que muda por
existir um eixo Z.

---

## 7. `Surface` — a superfície paramétrica

```python
class Surface(VGroup, metaclass=ConvertToOpenGL):
    def __init__(self, func, u_range=(0, 1), v_range=(0, 1), resolution=32,
                 surface_piece_config={}, fill_color=BLUE_D, fill_opacity=1.0,
                 checkerboard_colors=[BLUE_D, BLUE_E], stroke_color=LIGHT_GREY,
                 stroke_width=0.5, should_make_jagged=False,
                 pre_function_handle_to_anchor_scale_factor=1e-05, **kwargs)
```

Métodos próprios: `func(u, v)`, `set_fill_by_checkerboard(*colors,
opacity=None)`, `set_fill_by_value(axes, colorscale=None, axis=2, **kwargs)`.

### O que ela é, por dentro (e por que isso é a conta de custo)

`_setup_in_uv_space` monta uma grade de `u_res × v_res` quadriláteros, cada um
um `ThreeDVMobject` de 4 curvas de Bézier, e depois aplica `func` a todos os
pontos. **`resolution=(u, v)` produz exatamente `u × v` submobjects.** Um `int`
vale para os dois eixos.

| `resolution` | quads | curvas de Bézier | comentário |
|---|---:|---:|---|
| `(12, 12)` | 144 | 576 | rascunho, `-q l` |
| `(24, 24)` | 576 | 2 304 | **o ponto doce para aula** |
| `32` (default) | 1 024 | 4 096 | já pesa |
| `(64, 64)` | 4 096 | 16 384 | 4K ou detalhe real |

O custo é quadrático e a leitura é linear: dobrar a resolução multiplica o
trabalho por 4, e o ganho visual, numa superfície suave, é quase nulo depois de
~32. **Itere em `(12, 12)`; suba só na entrega.**

### As duas maneiras de colorir

```python
sup.set_fill_by_checkerboard(BLUE_D, BLUE_E, opacity=0.9)  # xadrez, o default
sup.set_fill_by_value(axes=eixos, axis=2,                  # degradê por z
                      colorscale=[(BLUE_E, -2), (WHITE, 0), (RED_E, 2)])
```

`colorscale` aceita lista de cores (pivôs distribuídos) ou lista de
`(cor, pivô)` com os cortes que você escolher. `axis` é 0/1/2 para x/y/z. É o
que `plot_surface(colorscale=...)` chama por baixo.

`checkerboard_colors=False` desliga o xadrez e deixa `fill_color` uniforme — o
que quase sempre é o certo em tema claro, onde duas variações de azul viram uma
mancha suja.

### `Create` numa `Surface` é uma armadilha de ritmo

```python
class Create(mobject, lag_ratio: float = 1.0, introducer: bool = True, **kwargs)
```

`lag_ratio=1.0` com N submobjects faz `get_sub_alpha` distribuir o tempo em N
fatias sequenciais (`animation/animation.py:384-388`): `full_length = (N-1)*1 +
1 = N`. Com 576 quads, `Create(sup)` desenha **576 quadradinhos em fila**. Num
`run_time=2` cada quad ganha 3,5 ms — o resultado é uma varredura estranha, e
o cálculo custa caro. Para superfície, prefira:

```python
self.play(FadeIn(sup, run_time=1.2))              # o mais barato e o mais legível
self.play(Create(sup, lag_ratio=0.002, run_time=2))  # varredura suave, se quiser
self.play(GrowFromCenter(sup))
```

---

## 8. Sólidos e primitivas — o catálogo com as assinaturas reais

Tudo abaixo é `mobject/3d` e está conferido em `api/manim-ce-index.tsv`.

```python
Sphere(center=ORIGIN, radius=1, resolution=None,
       u_range=(0, TAU), v_range=(0, PI), **kwargs)          # Surface
Dot3D(point=ORIGIN, radius=0.08, color=WHITE, resolution=(8, 8))   # Sphere
Cube(side_length=2, fill_opacity=0.75, fill_color=BLUE, stroke_width=0)  # VGroup de 6 Squares
Prism(dimensions=[3, 2, 1], **kwargs)                        # Cube reescalado
Cone(base_radius=1, height=1, direction=OUT, show_base=False,
     v_range=(0, TAU), u_min=0, checkerboard_colors=False)   # Surface
Cylinder(radius=1, height=2, direction=OUT, v_range=(0, TAU),
         show_ends=True, resolution=(24, 24))                # Surface
Line3D(start=LEFT, end=RIGHT, thickness=0.02, color=None, resolution=24)   # Cylinder!
Arrow3D(start=LEFT, end=RIGHT, thickness=0.02, height=0.3,
        base_radius=0.08, color=WHITE, resolution=24)        # Line3D
Torus(major_radius=3, minor_radius=1, u_range=(0, TAU),
      v_range=(0, TAU), resolution=None)                     # Surface
ThreeDVMobject(shade_in_3d=True, **kwargs)                   # VMobject que participa da ordenação
Polyhedron(vertex_coords, faces_list, faces_config={}, graph_config={})
Tetrahedron(edge_length=1)   Octahedron(edge_length=1)
Icosahedron(edge_length=1)   Dodecahedron(edge_length=1)
ConvexHull3D(*points, tolerance=1e-05, **kwargs)
```

Detalhes que custam tempo quando se descobre por render:

- **`Line3D` e `Arrow3D` são cilindros, não linhas.** `Line3D(Cylinder)`,
  `Arrow3D(Line3D)`, e `Arrow3D` ainda acrescenta um `Cone` de ponta. Um
  `resolution` inteiro vira `(2, resolution)` aqui (`three_dimensions.py:
  1010-1011`), isto é 48 quads por linha — barato perto de uma superfície, caro
  perto de um `Line` 2D. E o `thickness` é **raio em unidades de palco** (0,02),
  não `stroke_width`: dobrar `stroke_width` não faz nada.
- **`Line3D` tem dois construtores de classe** que quase ninguém acha:
  `Line3D.parallel_to(line, point=ORIGIN, length=5)` e
  `Line3D.perpendicular_to(line, point=ORIGIN, length=5)` — ambos
  `classmethod`.
- **`Cylinder.show_ends=True` chama `add_bases()`**, que acrescenta dois
  `Circle` com `shade_in_3d=True`. Em cilindro semitransparente as tampas
  aparecem "por dentro" — é a ordenação por centroide de novo.
- **`Cone` tem `show_base=False` por default** e `checkerboard_colors=False`
  (ao contrário da `Surface`, que vem xadrez).
- **`Cube` é um `VGroup` de 6 `Square`** com `shade_in_3d=True` e
  `LineJointType.BEVEL` (`three_dimensions.py:577-589`). Seis centroides bem
  separados: a ordenação acerta. Mas o default `fill_opacity=0.75` deixa ver o
  fundo — para um cubo opaco, passe `fill_opacity=1`.
- **`Polyhedron` instala um updater permanente**: o `__init__` termina em
  `self.add_updater(self.update_faces)` (`polyhedra.py:129`), porque as faces
  seguem o `Graph` de vértices. Consequência: **um poliedro na cena nunca é
  estático**, e o cache de frame estático do cairo é invalidado a partir dele
  (§12). Ele também constrói um `Graph` com um `Dot3D` em cada vértice, e cada
  `Dot3D` é uma `Sphere` de resolução (8, 8) = 64 quads: um `Icosahedron` são 12
  dessas esferas (768 quads) mais 20 faces, tudo com updater. É o mobject mais
  caro deste catálogo por unidade de tela.
- `Polyhedron.graph` e `.faces` são públicos e documentados:
  `octahedron.faces[2].set_color(YELLOW)`.

Utilidades de baixo nível, quando você escreve um mobject 3D próprio
(a construção de `Mobject` customizado é da skill `manim-mobjects-customizados`):

```python
from manim.mobject.three_d.three_d_utils import (
    get_3d_vmob_unit_normal, get_3d_vmob_start_corner, get_3d_vmob_end_corner,
    get_3d_vmob_start_corner_unit_normal, get_3d_vmob_end_corner_unit_normal,
    get_3d_vmob_gradient_start_and_end_points,
)
from manim.utils.space_ops import (
    z_to_vector, rotation_matrix, rotate_vector, cross, get_unit_normal,
    cartesian_to_spherical, spherical_to_cartesian,
)
```

`z_to_vector(v)` devolve a matriz que leva `OUT` a `v` — é como `Cube` orienta
cada face e como se aponta um `Cylinder` numa direção arbitrária.

---

## 9. Luz e sombreamento

O sombreamento do cairo é uma linha só (`utils/color/core.py:1631-1636`):

```python
to_sun = normalize(light_source - point)
light = 0.5 * np.dot(unit_normal_vect, to_sun) ** 3
if light < 0: light *= 0.5
shaded_rgb = rgb + light
```

Quatro coisas caem daí:

1. **É aditivo, não multiplicativo.** Uma face virada para a luz recebe até
   `+0,5` em cada canal RGB. Em **tema claro**, uma superfície já clara é
   empurrada para o branco e some contra o canvas. É o irmão 3D do defeito nº 1
   deste projeto ("texto sem cor explícita em fundo branco"). A correção é
   escolher cores de superfície com folga para cima (ver `manim-color-theming`
   para a conta de contraste) ou desligar o sombreamento.
2. **`should_apply_shading=False` desliga tudo** e devolve cor chapada — o
   visual de diagrama. `self.camera.should_apply_shading = False` no `setup()`.
3. **`shading_factor` NÃO FAZ NADA.** Ele é atribuído em
   `three_d_camera.py:68` e **nunca lido em lugar nenhum do pacote**:
   `grep -rn "shading_factor" .venv/.../manim/` devolve só a assinatura e a
   atribuição. A intensidade está fixa no `0.5 * dot³`. Não perca tempo
   ajustando esse número.
4. **A luz é um mobject.** `self.camera.light_source` é um `Point` em
   `light_source_start_point` (default `array([-7., -9., 10.])`, isto é
   `9*DOWN + 7*LEFT + 10*OUT`). Dá para movê-lo — inclusive com updater — e o
   sombreamento acompanha. E só as **duas primeiras** linhas de rgba de cada
   VMobject são sombreadas (canto inicial e canto final), o que é o que produz o
   degradê dentro de cada quad.

O ManimGL tem `shading: (gloss, shadow, ...)` por mobject e é outro modelo;
`OpenGLMobject` da CE tem `gloss=0.0`/`shadow=0.0` e `OpenGLSurface` usa
`gloss=0.3, shadow=0.4`.

---

## 10. Animar em 3D

Nada de especial: as animações são as mesmas, e o catálogo é da skill
`manim-animations`. O que muda:

```python
Rotate(mob, angle=PI, axis=OUT, about_point=None, about_edge=None, **kwargs)
Rotating(mob, angle=TAU, axis=OUT, about_point=None, about_edge=None,
         run_time=5, rate_func=linear, **kwargs)
```

- **`axis` é o parâmetro que existe em 3D e ninguém usa em 2D.**
  `Rotate(cubo, PI/2, axis=RIGHT)` gira em torno do eixo X. `Rotating` é a
  versão contínua, já com `rate_func=linear` e `run_time=5` de fábrica.
- **Girar o objeto ≠ girar a câmera.** Girar o objeto muda as normais e portanto
  o sombreamento; girar a câmera não muda a geometria. Para "mostrar o outro
  lado", quase sempre o certo é a câmera — o espectador entende que é o ponto de
  vista que anda.
- `ApplyMatrix(matriz, mob, about_point=ORIGIN)` aceita matriz 3×3 e é o jeito
  de aplicar uma transformação linear a um sólido.
- Para superfície: `FadeIn`/`GrowFromCenter` em vez de `Create` (§7).
- `Transform` entre dois sólidos de contagem de faces diferente funciona, mas o
  alinhamento cria submobjects — releia §5 se algum deles for fixo em frame.

---

## 11. `cairo` × `opengl` numa cena 3D — o que quebra

O renderer não é uma opção de velocidade: **ele troca a semântica**. Esta tabela
é a contribuição mais cara desta skill; tudo nela saiu do fonte.

| O que | cairo | opengl | Como falha |
|---|---|---|---|
| `set_camera_orientation(zoom=...)` | ok | **`AttributeError`** | `OpenGLCamera` não tem `set_zoom`; conferido: `awk -F'\t' '$2=="set_zoom"' api/manim-ce-methods.tsv` devolve **só `ThreeDCamera`** |
| `set_camera_orientation(focal_distance=...)` | ok | **`AttributeError`** | idem, `set_focal_distance` só existe em `ThreeDCamera` |
| `set_camera_orientation(frame_center=...)` | ok (com a ressalva do §3) | **`AttributeError`** | o método toca `camera._frame_center`, que `OpenGLCamera` não tem |
| `move_camera(focal_distance=...)` | ok | **warning e ignora** | `warnings.warn("focal distance of OpenGLCamera can not be adjusted.")` |
| `Sphere(...)` é subclasse de `Surface`? | sim | **não** | a metaclasse `ConvertToOpenGL` reescreve a base `Surface` → `OpenGLSurface` (`opengl_compatibility.py:31-43`) |
| `checkerboard_colors=`, `set_fill_by_value`, `set_fill_by_checkerboard` | ok | **somem calado** | `OpenGLSurface` não tem esses métodos; o kwarg cai no `**kwargs` de `OpenGLMobject.__init__`, que **nunca o lê** |
| `Sphere()` sem `resolution` | `(24, 12)` = 288 quads | `(101, 51)` = **5 151** quads | `three_dimensions.py:453-460` |
| `Torus()` sem `resolution` | `(24, 24)` = 576 | `(101, 101)` = **10 201** | `three_dimensions.py:1324-1329` |
| `ThreeDAxes` fatiado em `num_axis_pieces` | sim | **não** | `coordinate_systems.py:2514-2515` |
| oclusão | painter's por centroide | z-buffer por triângulo (`depth_test=True`) | opengl acerta interpenetração |
| `--format png` | rápido | **~100× mais lento** | medido em `manim-gpu-encoding §9` |

Ou seja, para o mesmo código: **~18× mais geometria** (linhas de `Sphere` e
`Torus`) e **nenhum** dos kwargs de cor. A primeira linha da tabela é a que mais
morde, porque `self.set_camera_orientation(phi=..., theta=..., zoom=0.9)` é a
abertura padrão de toda cena 3D — e ela quebra no opengl **na primeira linha do
`construct`**, antes de qualquer desenho.

Se você precisa mesmo do opengl (interpenetração correta, malha muito densa),
ramifique — `RendererType` é top-level (`manim.constants.RendererType`):

```python
from manim import config, RendererType

ZOOM = 0.9
if config.renderer == RendererType.OPENGL:
    self.camera.set_euler_angles(theta=-40 * DEGREES, phi=68 * DEGREES)
    # a mesma conta que move_camera faz por dentro (three_d_scene.py:281-283):
    self.camera.scale(config.frame_height / (ZOOM * self.camera.height))
else:
    self.set_camera_orientation(phi=68 * DEGREES, theta=-40 * DEGREES, zoom=ZOOM)
```

**Não escolha renderer por fé de desempenho.** A afirmação "o opengl economiza
~19% em cena pesada de geometria" circulava NESTA skill e **foi derrubada por
medição**: `manim-gpu-encoding §9` registra 6,12/6,48 s (cairo) contra
7,14/6,55 s (opengl) na mesma cena, isto é, "custa 17%" e "custa 1%" em duas
rodadas do mesmo dia. Aquela skill é a dona do assunto e tem a tabela datada;
esta aqui só registra o que muda **de comportamento**.

---

## 12. Custo: o orçamento de geometria de uma cena 3D

O cairo tem uma otimização única e é dela que tudo depende: a cada `play`, os
mobjects **estáticos** são rasterizados uma vez e guardados como imagem
(`CairoRenderer.save_static_frame_data` → `self.static_image`), e só os
**móveis** são redesenhados por frame. `Scene.get_moving_mobjects` devolve a
lista **do primeiro mobject móvel em diante** — um updater no primeiro mobject
da cena já derruba o cache de todos os seguintes.

Em `ThreeDScene` há um degrau a mais:

```python
# scene/three_d_scene.py:308-322
def get_moving_mobjects(self, *animations):
    moving_mobjects = super().get_moving_mobjects(*animations)
    camera_mobjects = self.renderer.camera.get_value_trackers() + [self.renderer.camera._frame_center]
    if any(cm in moving_mobjects for cm in camera_mobjects):
        return self.mobjects        # TUDO
    return moving_mobjects
```

**Qualquer movimento de câmera torna a cena inteira móvel.** `move_camera`,
`begin_ambient_camera_rotation`, updater num tracker — todos. Não é bug: se a
câmera anda, a projeção de todo mundo muda mesmo. Mas é a razão pela qual uma
órbita de 8 s custa muito mais do que 8 s de animação local.

A ordem de grandeza para orçar uma cena:

| Item | Submobjects |
|---|---:|
| `Surface(resolution=(24, 24))` | 576 |
| `Sphere()` cairo | 288 |
| `Torus()` cairo | 576 |
| `Cube()` | 6 |
| `ThreeDAxes()` | ~60 só de pedaços de eixo |
| `Icosahedron()` | 20 faces + 12 `Dot3D` (cada um 8×8 = 64 quads) |
| `Line3D` | 2 × 24 = 48 (é um cilindro) |

Receita que funciona:

1. Escreva com `resolution=(12, 12)` e `-q l`.
2. Confira o PNG (§15). Enquadramento, cor e oclusão não dependem de resolução.
3. Só então suba para `(24, 24)` — e para `(32, 32)`+ apenas se a superfície
   tiver dobra fina de verdade.
4. Ambiente/órbita: prefira **um** `move_camera` longo a `begin_ambient` +
   `wait` longo. O primeiro tem `rate_func` (entra e sai suave); a órbita é
   linear e, em vídeo de aula, lê como "está travado girando".
5. Se a cena tem `Polyhedron`, saiba que ela nunca é estática.

Cache de render, `--no-cache`, `max_files_cached` e o hash do partial movie são
da skill `manim-performance-cache`. Codec, NVENC, peso do arquivo e VRAM são da
`manim-gpu-encoding` — dela vale repetir só o limite operacional: **4K com
superfície densa estoura os 8 GiB desta placa; renderize 4K no cairo.**

---

## 13. 3D dentro de uma apresentação

O formato de cena em PARTES (mixin + `next_section(skip_animations=...)`, uma
parte por recado falado) é da skill **`manim-presentation-parts`** — não
reescrevo aqui. O que é específico de 3D:

- **A órbita não pode atravessar um corte.** Cada parte termina num **frame
  parado** que o apresentador olha enquanto fala. Se a última coisa da parte é
  uma órbita em curso, o frame congelado é um meio-giro arbitrário e a plateia
  lê "travou". Regra: `begin_ambient_camera_rotation()` … `wait()` …
  `stop_ambient_camera_rotation()` **dentro da mesma parte**, e o corte vem
  depois de a câmera parar numa orientação escolhida.
- **Prefira `move_camera` com `rate_func` a órbita** justamente por isso: ele
  começa e termina em ângulos que você escreveu.
- **Nenhuma parte pode terminar em `FadeOut`.** O pôster do slide é o **último
  frame** do mp4; uma cena 3D que fecha esvaziando a tela vira página branca no
  PDF de backup. (Regra geral do pipeline, registrada em
  `manim-presentation-parts` e em `~/Projects/aulas/CLAUDE.md`.)
- **Sem título dentro do vídeo.** O slide já tem o `h2`. Em 3D isso é ainda mais
  caro: o título ia de `add_fixed_in_frame_mobjects` e roubaria a faixa de cima
  justo onde a projeção da superfície é mais alta.
- **Fundo claro é o caso normal deste projeto.** Releia o §9: em canvas branco o
  sombreamento aditivo apaga a superfície. Ou `should_apply_shading = False`, ou
  cores com folga. E todo `Text`/`Mobject` com cor explícita, sempre — o Manim
  escreve branco por padrão e some sem erro nenhum.

---

## 14. 3D interativo — quando o ManimGL vale a pena

Para **desenvolver** um enquadramento 3D, arrastar com o mouse até achar o
ângulo e só então escrever o número é incomparavelmente mais rápido:

```bash
bin/manimgl scenes/demo3d.py Demo3D        # abre janela; arraste para orbitar
```

Teclas da janela, conferidas em `.venv-gl/.../manimlib/default_config.yml:129-143`:
`d` pan 3D · `f` pan · `r` reset · `s` select · `u` unselect · `g` grab ·
`h`/`v`/`z` grab em x/y/z · `t` resize · `c` color · `i` information ·
`k` cursor · `q` (com command) quit.

A tradução de câmera CE ↔ GL, que é onde se erra:

| ManimCE | ManimGL | Cuidado |
|---|---|---|
| `self.set_camera_orientation(phi=..., theta=...)` | `self.frame.reorient(theta_degrees, phi_degrees, gamma_degrees, center, height)` | **GL é em GRAUS e theta vem PRIMEIRO** |
| `self.camera.set_phi(x)` | `self.frame.set_phi(x)` / `self.frame.set_euler_angles(theta, phi, gamma)` | no GL, `self.frame` **é** a `CameraFrame` (`manimlib/scene/scene.py:114`) e é um Mobject |
| `begin_ambient_camera_rotation(rate)` | `self.frame.add_ambient_rotation(angular_speed=1*DEGREES)` | |
| `zoom=` | `self.frame.set_height(h)` / `scale` | GL não tem "zoom" |
| `focal_distance=` | `self.frame.set_field_of_view(...)` / `set_focal_distance` | modelos diferentes |
| `ThreeDScene` | qualquer `Scene` | **no GL toda cena é 3D**; o `ThreeDScene` de lá tem **um** método próprio (`add(..., set_depth_test=True)`) |
| `Sphere(resolution=(24,12))` | `Sphere(resolution=(101,51))` | defaults diferentes |
| — | `TexturedSurface`, `SurfaceMesh`, `depth_test` por mobject | no caminho **cairo** da CE não existem; sob `--renderer opengl` há os espelhos `OpenGLTexturedSurface`/`OpenGLSurfaceMesh` |

A API do ManimGL inteira, as flags do binário e o `custom_config.yml` são da
skill **`manimgl-3b1b`**. Aqui fica só: **use o GL para ACHAR o ângulo, escreva
o número na cena CE.** Os dois projetos não compartilham código.

---

## 15. Conferir uma cena 3D sem renderizar o filme

Metade dos defeitos de 3D é de enquadramento, e enquadramento se confere num
frame:

```bash
bin/mx render cena.py Demo3D --format png -q l          # último frame, cairo
bin/manim -ql -s -n 12,13 cena.py Demo3D                # um instante específico
```

**Correção:** `mx render` **não tem `-n`** — `manimx/cli.py:457-476` define o
subparser sem ele, e o parse é estrito, então a linha sai em
`error: unrecognized arguments`. O recorte `-n a,b` só existe no `bin/manim`
cru, como a tabela de `manim-render-api` §6.1 já dizia. Uma versão anterior
desta skill escrevia `mx render … -n 12,13`.
O caminho do arquivo vem em **`image_file`** no JSON (`output_file` é `null`
em png) — detalhe da skill `manim-render-api`. **Olhe a imagem.** Sobreposição,
superfície saindo do quadro, texto entortado, contraste ruim e ordem de
desenho errada **não dão erro no terminal**. O ciclo canônico
(escrever → render rápido → OLHAR → corrigir → render final) e os medidores são
da skill `manim-verificacao-visual`.

Conferências que não custam render nenhum:

```bash
# a classe existe e a assinatura é essa mesmo?
awk -F'\t' '$1=="class" && $3=="mobject/3d"' api/manim-ce-index.tsv | cut -f2,4

# os 13 métodos próprios da ThreeDScene, sem os 56 herdados de Scene
bin/mx show ThreeDScene --own-only

# esse método é da câmera 3D ou só da 2D?
awk -F'\t' '$2=="set_zoom" || $2=="frame"' api/manim-ce-methods.tsv | cut -f1,2,4
```

E dentro da cena, antes de gastar frame:

```python
print(sup.get_center(), sup.width, sup.height)      # cabe em x∈[-7.11,7.11], y∈[-4,4]?
print(self.camera.get_phi() / DEGREES)              # em graus, para ler
```

O palco é de 14,222 × 8 unidades; posicionamento, margens e "cabe na tela?" são
da skill `manim-layout-posicionamento`.

---

## 16. Armadilhas — sintoma, causa, correção

| Sintoma | Causa | Correção |
|---|---|---|
| A cena 3D parece 2D | `phi=0` é o default: você olha de cima | `self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)` |
| Objeto some ou vira um risco atravessando a tela | profundidade de câmera ≥ `focal_distance` (20) → `factor = 1e6` | encolha a geometria, ou `focal_distance=60` |
| Uma superfície atravessa a outra por inteiro | painter's algorithm por centroide (§1) | mais `resolution`, ou `set_shade_in_3d(True, z_index_as_group=True)`, ou opengl |
| O rótulo flutua na frente de tudo | `shade_in_3d=False` ⇒ `z_key = inf` | `set_shade_in_3d(True)` se ele é geometria; se é HUD, era isso mesmo |
| `z_index` "não funciona" em 3D | ele só desempata dentro do mesmo `z_key` | ordene por profundidade real, ou fixe em frame |
| Texto ilegível, deitado, girando com a cena | `Text` é plano e é projetado | `add_fixed_in_frame_mobjects` (HUD) ou `add_fixed_orientation_mobjects` (rótulo) |
| Parte do HUD "voou" para dentro do 3D | a família é fotografada na chamada; `become`/`ReplacementTransform` cria submobject novo | refixe depois de mexer; use `Transform`, não `ReplacementTransform` |
| Tirei o título com `remove_fixed_in_frame_mobjects` e ele continua na tela, agora torto | no cairo esse método só **desfixa** | `self.remove(...)` ou `FadeOut(...)` |
| `begin_ambient_camera_rotation` não girou nada | rotação acontece durante tempo que passa | `self.wait(...)` ou um `play` depois |
| A câmera continua girando depois do `stop` | parou com `about` diferente do que começou | `stop_ambient_camera_rotation(about="phi")` |
| `ValueError: Invalid ambient rotation angle.` com `about` válido | o `try/except Exception` reescreve **qualquer** erro interno | leia o traceback completo com `-v DEBUG`; ver `manim-troubleshooting` |
| Rotação lentíssima | `rate` é rad/s e o default é **0,02** | `rate = TAU / segundos_por_volta` |
| `AttributeError: 'OpenGLCamera' object has no attribute 'set_zoom'` | `zoom=`/`focal_distance=`/`frame_center=` não existem no opengl | tire-os, ou ramifique por `config.renderer` (§11) |
| `AttributeError: ... has no attribute 'renderer'` numa cena 3D | você herdou de `SpecialThreeDScene` | herde de `ThreeDScene` (§2) |
| A esfera ficou ~18× mais pesada só de trocar o renderer | `Sphere` default é `(24,12)` no cairo e `(101,51)` no opengl | passe `resolution=` explicitamente, sempre |
| `checkerboard_colors` sumiu no opengl | kwarg engolido por `OpenGLMobject.__init__` | `colorscale=` do `OpenGLSurface`, ou fique no cairo |
| Superfície some no fundo branco | sombreamento é **aditivo** (+0,5 no RGB) | `should_apply_shading = False` ou cor com folga |
| Ajustei `shading_factor` e nada mudou | ele nunca é lido | não existe esse controle; §9 |
| `Create(superficie)` demora e sai varrendo | `Create(lag_ratio=1.0)` × 576 submobjects | `FadeIn`, ou `Create(..., lag_ratio=0.002)` |
| Cena 3D lentíssima e o cache não ajuda | qualquer movimento de câmera marca **todos** os mobjects como móveis | menos `resolution`, menos órbita, §12 |
| `frame_center` não centralizou o que eu pedi | o deslocamento entra duas vezes | mova a geometria; §3 |
| `self.camera.frame` dá `AttributeError` numa `ThreeDScene` | `.frame` é de `MovingCamera`, não de `ThreeDCamera` | use `zoom`/`frame_center`; para câmera 2D, `manim-camera-2d` |

---

## 17. Fronteiras — o que NÃO é desta skill

| Assunto | Skill dona |
|---|---|
| `MovingCameraScene`, `ZoomedScene`, `self.camera.frame`, pan/zoom 2D, seguir um objeto, `MultiCamera`, `SplitScreenCamera`, `MappingCamera` | **`manim-camera-2d`** |
| de qual `Scene` herdar em geral, ciclo `setup`/`construct`/`tear_down`, `next_section`, `add`/`remove`/`bring_to_front` | `manim-cenas-secoes` |
| catálogo de animações, `Transform` × `ReplacementTransform`, `.animate` | `manim-animations` |
| `rate_func`, `lag_ratio`, `run_time`, `path_func`, orçamento de segundos | `manim-composicao-ritmo` |
| `Axes`, `NumberPlane`, `plot`, `BarChart`, rótulos e áreas em 2D | `manim-graphs-plots` |
| formas 2D, `VGroup` × `Group`, `Brace`, submobjects | `manim-mobjects` |
| posicionar, `to_edge`, `arrange`, margens, "cabe na tela?" | `manim-layout-posicionamento` |
| escrever um `Mobject`/`Animation` próprio, caminhos de Bézier, booleanos, `ConvexHull` | `manim-mobjects-customizados` |
| `ValueTracker`, updaters, `always_redraw`, `DecimalNumber` | `manim-updaters-valuetracker` |
| cor, contraste, tema claro, `tema.py`, `apply_theme` | `manim-color-theming` (paleta) e `manim-tema-projeto` (contrato) |
| codec, NVENC, tempo de render medido, cairo × opengl por DESEMPENHO, VRAM | `manim-gpu-encoding` |
| cache de partial movie, `--no-cache`, `max_files_cached` | `manim-performance-cache` |
| qualidade, formato, `-n a,b`, caminho da saída, `image_file` | `manim-render-api` |
| olhar o PNG, medir frame, "renderizou e não olhou = não terminou" | `manim-verificacao-visual` |
| cena cortada em partes para slide, emenda, pôster | `manim-presentation-parts` |
| API do ManimGL, flags do `manimgl`, `custom_config.yml` | `manimgl-3b1b` |
| descobrir assinatura/kwarg/nome de qualquer símbolo | `manim-api-discovery` |
| ambiente, wrappers `bin/`, roteamento entre skills | `manim-project` |

### Buracos declarados — não invente skill que não existe

- **`LinearTransformationScene` e `VectorScene`** (álgebra linear de cena,
  `ApplyMatrix`, `ApplyComplexFunction`): **sem skill dona**. As assinaturas
  estão no índice; `mx show LinearTransformationScene`.
- **`VectorField`, `ArrowVectorField`, `StreamLines`, `PhaseFlow`,
  `Homotopy`**: **sem skill dona**. E note: as três primeiras são de campo
  **2D** — não existe campo vetorial 3D pronto na CE. Para um campo em 3D,
  monte um `VGroup` de `Arrow3D` a partir de uma malha, e conte o custo (§8).
- **Os 48 mobjects `OpenGL*`** (`OpenGLSurface`, `OpenGLSurfaceMesh`,
  `OpenGLTexturedSurface`, `Shader`, `Mesh`, `Object3D`, `Window`): órfãos **de
  propósito**. No fluxo de aula deste projeto o renderer é cairo; documentar 48
  espelhos custa caro e rende pouco. Para listá-los,
`bin/mx find surface --category mobject/opengl` — o `query` do `mx find` é
posicional e **obrigatório** (`manimx/cli.py:493`), então `mx find --category …`
sozinho sai em `error: the following arguments are required: query`.
Para varrer a categoria inteira, passe uma string vazia:
`bin/mx find "" --category mobject/opengl --kind class -n 60`.
- **`Broadcast`, `ManimBanner`, `SampleSpace`**: órfãos triviais.

---

## 18. O que ficou NÃO VERIFICADO nesta redação

Esta rodada foi **só leitura** — nenhum `mx render`, `manim`, `ffmpeg` ou
benchmark rodou. Todas as assinaturas, defaults, categorias e caminhos de código
foram conferidos no índice e no fonte instalado; o que não pôde ser conferido
por execução:

1. ~~**A quebra de `SpecialThreeDScene`**~~ (§2) — **FECHADA**: `SpecialThreeDScene()` foi instanciada nesta máquina e levanta
   `AttributeError: 'SpecialThreeDScene' object has no attribute 'renderer'`.
   O que segue era a leitura que previu isso, e ela estava certa. A leitura é direta e dupla
   (`self.renderer` antes de `super().__init__`; `camera_config` inexistente),
   mas ninguém instanciou a classe para ver o traceback.
2. **A dupla subtração de `frame_center`** (§3). O caminho de código está
   citado linha a linha; o deslocamento resultante na tela não foi medido.
   Trate como "confira o PNG antes de confiar no valor".
3. **O vazamento de `become`/`Transform` em mobject fixo em frame** (§5). O
   mecanismo (`add_n_more_submobjects` cria cópias; o set guarda identidades) é
   inequívoco no fonte; o sintoma visual não foi reproduzido.
4. **Os `AttributeError` do renderer opengl** (§11). Deduzidos de o índice não
   listar `set_zoom`/`set_focal_distance`/`_frame_center` em `OpenGLCamera` e de
   `set_camera_orientation` não ramificar por renderer. Nenhum render opengl
   foi feito.
5. **`checkerboard_colors` engolido no opengl** (§11). `OpenGLMobject.__init__`
   recebe `**kwargs` e nunca os lê — lido, não executado.
6. **Todos os números de tempo, peso e VRAM** citados vêm de
   `manim-gpu-encoding`, medidos em 2026-08-19 nesta máquina, e não foram
   remedidos aqui. Onde divergirem, **vale o daquela skill** — ela tem o comando
   ao lado da tabela.

Se você for executar qualquer um destes, o mais barato é o item 1: uma linha de
Python que só instancia a classe, sem render.
