---
name: manim-composicao-ritmo
description: >-
  O TEMPO de uma cena Manim: `run_time`, `rate_func` (as 49 curvas com o efeito
  percebido de cada uma), `lag_ratio`, `AnimationGroup` × `Succession` ×
  `LaggedStart` × `LaggedStartMap`, `ChangeSpeed`, `path_func` (os 6), `wait` /
  `pause` / `wait_until`, e o orçamento de segundos que separa um vídeo com
  ritmo de um vídeo que corre. Use quando o pedido for sobre QUANTO tempo, QUE
  CURVA ou EM QUE ORDEM: "o vídeo está muito rápido", "ninguém consegue ler",
  "isso passou voando", "deixa mais devagar", "acelera essa parte", "as coisas
  aparecem todas de uma vez", "quero que apareçam uma depois da outra", "em
  cascata", "escalonado", "um por um", "essa animação começa antes da outra",
  "as duas animações não terminam juntas", "a curva está dura/robótica", "quero
  que desacelere no fim", "com efeito de mola", "quica no fim", "passa do ponto
  e volta", "faz uma pausa no meio", "quanto tempo essa cena tem?", "põe um
  respiro entre os passos", "o `LaggedStart` ficou longo demais", "o
  `lag_ratio` não fez nada", "o quadrado voltou pro começo no meio da
  animação", "o objeto saiu voando da tela", "meu `rate_func` não existe /
  NameError", "`ease_out_expo` não está definido", "a animação termina antes do
  fim", "o `Succession` e o `AnimationGroup` dão resultados diferentes",
  "`ChangeSpeed` deu AssertionError", "quantos frames tem um `run_time` de
  0,45?". Cobre a cadeia `t → alpha → rate_func → path_func` conferida no
  fonte, por que o último frame de um `play` NUNCA é o estado final, os dois
  decoradores que fazem uma curva clampar (e o que acontece com a sua lambda
  que não clampa), o catálogo das 49 curvas com valores calculados, e o que o
  `from manim import *` NÃO traz. NÃO use para: escolher QUAL classe de
  animação usar, `.animate`, a família `Transform`, `introducer`/`remover`
  (`manim-animations`); `ValueTracker`, updaters, `always_redraw`, `dt`
  (`manim-updaters-valuetracker`); cortar a cena em partes que o apresentador
  avança, cauda de parte, emenda (`manim-presentation-parts`); `next_section`
  como recurso da biblioteca e o mapa das classes de `Scene`
  (`manim-cenas-secoes`); `-q`/`-r`/`--fps`, caminho de saída e cache
  (`manim-render-api`); codec, NVENC e peso do arquivo (`manim-gpu-encoding`);
  descobrir se um nome existe (`manim-api-discovery`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Ritmo — quanto tempo, que curva, em que ordem

`manim-animations` responde **o quê** (qual classe faz o objeto aparecer). Esta
skill responde **quando**: quantos segundos, com que curva, em que ordem, e com
quanto respiro entre um beat e o outro. É a diferença entre um vídeo que a
plateia acompanha e um vídeo que passa voando — e é, no deck consumidor real
(`~/Projects/aulas`), o parâmetro mais editado depois de nascer a cena.

## Procedência do que está escrito aqui

Quatro marcadores, e eles valem para o arquivo inteiro:

- **[FONTE]** — conferido lendo o ManimCE **0.21.0** instalado em
  `.venv/lib/python3.12/site-packages/manim/`, ou os índices de `api/`. Vem com
  arquivo e linha.
- **[MEDIDO]** — calculado nesta máquina em 2026-08-19 com
  `.venv/bin/python`, **construindo objetos e chamando `interpolate()` na mão**.
  Nada foi renderizado: nenhum `mx render`, nenhum frame, nenhum ffmpeg, nenhuma
  GPU. É aritmética e construção de Mobject, custa milissegundos.
- **[DECK]** — contado ou medido no deck consumidor `~/Projects/aulas`
  (11 arquivos de cena, 2 aulas em produção). Testemunho, não reprodução.
- **[INFERIDO]** — encadeamento meu a partir do fonte, sem execução. Sempre
  marcado; nunca apresentado como fato medido.

O resumo em seis frases, para quem tem trinta segundos:

1. **`rate_func` é QUANDO, `path_func` é POR ONDE, `lag_ratio` é EM QUE ORDEM.**
   Os três atuam em pontos diferentes da mesma cadeia, e confundi-los é a
   origem de metade dos pedidos de "não ficou como eu queria".
2. **O último frame renderizado de um `play` nunca é o estado final.** O laço
   é `np.arange(0, run_time, 1/fps)`, que **exclui** o fim. Quem mostra o estado
   final é o `wait` seguinte **[FONTE]**.
3. **`self.play(a, b)` com durações diferentes dura `max(run_time)`**, e a
   animação curta recebe `alpha > 1`. Ela só não explode porque quase toda
   `rate_func` da biblioteca é decorada com `@unit_interval`. Uma lambda sua
   não é: medi `x = +36.00` onde o esperado era `+4.00` **[MEDIDO]**.
4. **`Succession(a, b)` e `AnimationGroup(a, b, lag_ratio=1)` têm a MESMA linha
   do tempo e resultados DIFERENTES.** O grupo começa todas as animações no
   instante 0; a `Succession` começa uma de cada vez. Dois `Rotate(PI/2)` no
   mesmo quadrado: `Succession` termina em 225°, `AnimationGroup` em 135°, com
   um salto para trás visível no meio **[MEDIDO]**.
5. **`lag_ratio` ALONGA o `LaggedStart`.** 10 animações de 1 s com
   `lag_ratio=0.25` duram **3,25 s**, não 1 s — apesar de a docstring da classe
   dizer que não influencia **[MEDIDO]**.
6. **Só 17 das 49 `rate_function` chegam pelo `from manim import *`.** As 30
   `ease_*`, mais `unit_interval` e `zero`, ficam de fora do `__all__`
   **[FONTE: `utils/rate_functions.py:88-106`]**.

---

## 1. O relógio: como um `play` vira frames

### 1.1 A cadeia inteira, do segundo ao pixel

```
t (segundos do play)
  └─ alpha  = t / animation.run_time            Scene.update_to_time      [FONTE scene.py:1706]
      └─ sub_alpha = rate_func(alpha*L - i*lag)  Animation.get_sub_alpha   [FONTE animation.py:384-391]
          └─ interpolate_submobject(..., sub_alpha)
              └─ path_func(pontos_ini, pontos_fim, sub_alpha)   (só na família Transform)
```

Quatro consequências que valem lembrar antes de mexer em qualquer número:

- **`rate_func` é aplicada DEPOIS do `lag_ratio`**, dentro do `get_sub_alpha`.
  Por isso `lag_ratio` numa animação isolada escalona submobject a submobject
  *dentro* da curva, e não a curva inteira. O `lag_ratio` de uma animação
  sozinha é assunto de `manim-animations` §3; aqui o `lag_ratio` que interessa é
  o de **composição** (§6).
- **`path_func` recebe o alpha JÁ suavizado.** Ele decide a trajetória, nunca a
  velocidade.
- **`alpha` não é clampado pelo `Scene`.** Ver §3.
- **Nada disso roda quando `skip_animations` está ligado**: aí
  `get_time_progression` devolve `[run_time]`, uma iteração só
  **[FONTE `scene.py:1096-1100`]**. As quatro situações que ligam o skip e o que
  elas quebram estão em `manim-updaters-valuetracker` §12 — não repito aqui.

### 1.2 O orçamento de frames: quanto um `run_time` compra

`Scene.get_time_progression` **[FONTE `scene.py:1099-1100`]**:

```python
step  = 1 / config["frame_rate"]
times = np.arange(0, run_time, step)          # início inclusivo, fim EXCLUSIVO
```

Frames de um `play`, contados com esse `np.arange` **[MEDIDO]**:

| `run_time` | 15 fps (`-q l`) | 30 fps (`-q m`) | 60 fps (`-q h`/`p`/`k`) |
|---:|---:|---:|---:|
| 0,10 s | **2** | 3 | 6 |
| 0,20 s | 3 | 6 | 12 |
| 0,30 s | 5 | 9 | 18 |
| **0,45 s** | **7** | 14 | **27** |
| 0,50 s | 8 | 15 | 30 |
| **0,80 s** | **12** | 24 | **48** |
| 1,00 s | 15 | 30 | 60 |
| 1,40 s | 21 | 42 | 84 |
| 3,00 s | 45 | 90 | 180 |

O FPS vem da qualidade **[FONTE `constants.py:206-241`]**: `-q l` **15**,
`-q m` **30**, `-q h`/`-q p`/`-q k` **60**. É por isso que "avalie ritmo em
`-q m` no mínimo": um movimento de 0,45 s tem **7 frames** em `-q l` e lê como
engasgo, não como ritmo. E `manim-project` mediu que `-r` sobrescreve a
resolução mas **não** o FPS (`-q l -r 1280x720` grava em `720p15`) — para mudar
só o FPS existe `--fps` (`mx render --fps`, `manimx/cli.py:466`; `bin/manim
--fps/--frame_rate`).

### 1.3 O último frame de um `play` NUNCA é o estado final

Este é o achado que mais gente conserta pelo lado errado.

```python
for t in self.time_progression:      # np.arange(0, run_time, 1/fps): NÃO inclui run_time
    self.update_to_time(t)
    self.renderer.render(self, t, self.moving_mobjects)
for animation in self.animations:
    animation.finish()               # <- interpolate(1) acontece AQUI, DEPOIS do laço
```
**[FONTE `scene.py:1381-1390`]** e `Animation.finish` → `self.interpolate(1)`
**[FONTE `animation.py:216-227`]**.

Com `run_time=1` a 60 fps, o último `t` do laço é **0,9833** — logo o último
frame escrito tem `alpha = 0,9833`, não 1,0 **[MEDIDO]**. A 15 fps, `alpha =
0,9333`. O `interpolate(1)` acontece **depois** do último `render`, e **nenhum
frame é escrito para ele**.

| FPS | frames do `play` (`run_time=1`) | alpha do ÚLTIMO frame |
|---:|---:|---:|
| 15 | 15 | 0,9333 |
| 30 | 30 | 0,9667 |
| 60 | 60 | 0,9833 |

**O que isso causa na prática:**

- O primeiro frame de todo `play` é `alpha = 0` — o estado **antes** do
  movimento. Encadeando `play`s isso não duplica nada, porque o `play` seguinte
  parte do estado que o `finish()` do anterior deixou.
- **Se a cena termina num `play`, o último frame do mp4 está a 1/60 s do fim.**
  Num `FadeIn` com `ease_out_expo`, 1/60 s antes do fim já é indistinguível.
  Num `Rotate` linear de 1 s, são **6 graus** faltando. E como o pôster do vídeo
  é o último frame (`ffmpeg -sseof -1 -update 1`), o defeito vai direto para o
  PDF de backup.
- **A correção é um `wait` no fim**, não mexer no `run_time`: o `wait` renderiza
  o estado atual (pós-`finish`, `alpha = 1`) e o congela (§1.4). É o mecanismo
  por trás da regra empírica de `manim-presentation-parts` ("toda parte fecha
  numa cauda") — lá está a política; aqui está o motivo.

### 1.4 `wait` é outro caminho no renderer

Um `play` com **uma única** `Wait` e nenhum mobject com updater vira frame
congelado: `compile_animation_data` marca `is_static_wait = True` e o renderer
desvia **[FONTE `scene.py:1329-1335`, `cairo_renderer.py:111-117`]**:

```python
if scene.is_current_animation_frozen_frame():
    self.update_frame(scene, mobjects=scene.moving_mobjects)   # renderiza UMA vez
    self.freeze_current_frame(scene.duration)                  # e duplica N vezes
```

E `freeze_current_frame` **[FONTE `cairo_renderer.py:197-209`]**:

```python
dt = 1 / self.camera.frame_rate
self.add_frame(self.get_frame(), num_frames=int(duration / dt))     # int() TRUNCA
```

Frames congelados por `wait`, com a fórmula exata do fonte **[MEDIDO]**:

| `wait(d)` | 15 fps | 30 fps | 60 fps |
|---:|---:|---:|---:|
| 0,01 s | **1** ⚠ | **1** ⚠ | **1** ⚠ |
| 0,05 s | **1** ⚠ | 1 | 3 |
| 0,10 s | 1 | 3 | 6 |
| 0,25 s | 3 | **7** | 15 |
| 0,35 s | 5 | 10 | 21 |
| 0,40 s | 6 | 12 | 24 |
| 0,80 s | 12 | 24 | 48 |

Três leituras:

1. **Um `wait` menor que `1/fps` é ELEVADO a `1/fps`, com warning alto** — as
   células marcadas ⚠ acima. **Correção:** uma versão anterior desta tabela
   aplicava `int(duration/dt)` à duração CRUA e concluía "zero frames". Não é o
   que acontece: `Scene.wait` valida **antes** de construir a `Wait`
   (`scene.py:1249`), e `validate_run_time` corrige o valor
   (`scene.py:1128-1137`), então `int((1/fps)/(1/fps)) == 1`. `self.wait(0.01)`
   grava **1** frame e grita no log — e, pela leitura nº 3 abaixo, esse único
   frame é justamente o que mostra `alpha = 1`.
2. **A truncagem não é neutra.** `wait(0.25)` a 30 fps são 7 frames = 0,2333 s:
   a cauda encolhe **7%** só por mudar a qualidade. A 60 fps são 15 frames
   exatos.
3. **O frame congelado é o estado pós-`finish`** — é literalmente o único jeito
   de o `alpha = 1` aparecer no vídeo (§1.3).

Se **qualquer** mobject na cena tiver updater time-based, o wait deixa de ser
congelado e passa pelo laço normal, renderizando frame a frame. Quem decide é
`should_update_mobjects` — assunto de `manim-updaters-valuetracker`.

### 1.5 `validate_run_time`: os dois portões

```python
Scene.validate_run_time(run_time, method, parameter_name='run_time') -> float
```
**[FONTE `scene.py:1113-1137`]**, aplicado em `play` (via `get_run_time`),
`wait`, `pause` e `wait_until`:

| Situação | O que acontece |
|---|---|
| `run_time <= 0` | **`ValueError`** — "which Manim cannot render". Falha alto. `self.wait(0)` morre aqui |
| `0 < run_time < 1/fps` | **warning** e o valor é elevado a `1/fps`. Não falha |
| `run_time < 0` no construtor | **`ValueError`** antes, no setter da property `run_time` **[FONTE `animation.py:174-181`]**: *"The run_time of Create cannot be negative"* **[MEDIDO]** |

E `Scene.get_run_time(animations)` é literalmente `max(anim.run_time for anim in
animations)` **[FONTE `scene.py:1141-1157`]** — a base do §3.

---

## 2. Os parâmetros do tempo, e quem manda em quem

### 2.1 No construtor da animação

```python
Animation.__init__(mobject, lag_ratio=0.0, run_time=1.0, rate_func=smooth,
                   reverse_rate_function=False, name=None, remover=False,
                   suspend_mobject_updating=True, introducer=False, *,
                   _on_finish=…, use_override=True)
```
**[FONTE, índice `api/manim-ce-methods.tsv`]**. Os que são desta skill:
`run_time`, `rate_func`, `lag_ratio`. `remover`, `introducer`,
`suspend_mobject_updating` e `reverse_rate_function` são de `manim-animations`
§3.

Constantes do módulo **[FONTE `api/manim-ce-index.tsv`, categoria
`animation/core`]**:

| Constante | Valor |
|---|---|
| `DEFAULT_ANIMATION_RUN_TIME` | `1.0` |
| `DEFAULT_ANIMATION_LAG_RATIO` | `0.0` |
| `DEFAULT_LAGGED_START_LAG_RATIO` | `0.05` (`animation/composition`) |
| `DEFAULT_WAIT_TIME` | `1.0` (`constants.py:178`) |

### 2.2 Os getters e setters

`set_run_time(run_time) -> Animation` · `get_run_time() -> float` ·
`set_rate_func(rate_func) -> Animation` · `get_rate_func() -> Callable`
**[FONTE `animation.py:394-452`]**. Todos devolvem `self`, então encadeiam.
A docstring do `set_run_time` avisa: **não mude o `run_time` de uma animação já
em execução**.

```python
anim = Create(c).set_run_time(2).set_rate_func(rate_functions.ease_out_expo)
```

### 2.3 O kwarg do `play` é um `setattr` cego — e é uma armadilha

```python
for animation in animations:
    for k, v in kwargs.items():
        setattr(animation, k, v)
```
**[FONTE `scene.py:1006-1008`]**. Três consequências, todas silenciosas:

1. **`self.play(a, b, run_time=2)` sobrescreve o `run_time` das DUAS.** Passe os
   tempos por animação e não repita o kwarg no `play` (`manim-animations` §4).
2. **Erro de digitação no kwarg não dá erro nenhum.**
   `self.play(Create(c), runtime=2)` cria um atributo `runtime` que ninguém lê;
   `run_time` continua 1,0 **[MEDIDO]**. Vale para `rate_fun=`, `lag_ration=`,
   `runtime=`. Se o ritmo "não mudou", confira a grafia antes de qualquer outra
   coisa.
3. **`lag_ratio` no `play` NÃO reescalona um `AnimationGroup` já construído.**
   A linha do tempo é calculada dentro do `__init__` (`init_run_time` →
   `build_animations_with_timings`); um `setattr` posterior não a reconstrói.
   Medido: `LaggedStart(...)` com `lag_ratio=0.25` tem starts
   `[0, 0.25, 0.5, 0.75]`; depois de `g.lag_ratio = 0.9` os starts continuam
   `[0, 0.25, 0.5, 0.75]` **[MEDIDO]**. O `lag_ratio` vai no **construtor**.

---

## 3. Sincronizar animações de duração diferente

### 3.1 A regra

`self.play(a, b, c)` dura `max(run_time)` **[FONTE `scene.py:1156`]**, e cada
animação recebe o seu próprio `alpha = t / self.run_time`, **sem clamp**
**[FONTE `scene.py:1706`]**.

Então numa `play(curta_1s, longa_3s)`, a curta recebe `alpha` indo até ~2,98.
Ela não explode porque **quase toda `rate_func` da biblioteca é decorada**:

```python
@unit_interval          # t<0 → 0 ; t>1 → 1
def smooth(t, inflection=10.0): ...
```
**[FONTE `utils/rate_functions.py:120-145`]**.

Medido chamando `interpolate()` na mão num `Dot` que anda 4 unidades para a
direita **[MEDIDO]**:

| `rate_func` | alpha=1 | alpha=2 | alpha=3 |
|---|---:|---:|---:|
| `smooth` (`@unit_interval`) | +4,00 | +4,00 | +4,00 |
| `lambda t: t*t` (sem decorador) | +4,00 | **+16,00** | **+36,00** |

O quadro tem **±7,11** de largura. Um `alpha = 3` com uma lambda quadrática põe
o objeto a 36 unidades da origem: ele some da tela, o vídeo não dá erro, e o
sintoma ("o objeto saiu voando") aparece só na animação **curta** da `play` —
o último lugar onde alguém procura.

**Regra dura: toda `rate_func` escrita à mão leva `@unit_interval`** (ou clampa
sozinha). Ver §4.6.

### 3.2 Os quatro jeitos de sincronizar, e quando cada um serve

| Você quer | Faça | Por quê |
|---|---|---|
| todas terminam **juntas** | um `run_time` igual em todas — **só isso** | `AnimationGroup(run_time=X)` NÃO serve: ele reescala a linha inteira e **preserva** as proporções, então a curta continua terminando antes (§6.2). Com `run_times=[1, 3]` e `run_time=2`, a curta acaba em 0,667 s e a longa em 2 s |
| a curta **chega e espera** | não faça nada: `self.play(curta, longa)` | a `rate_func` decorada clampa em 1 e o mobject fica parado no destino |
| a curta **começa depois** | `rate_func=squish_rate_func(smooth, 0.6, 1.0)` | §7 — escalona dentro do mesmo `play`, sem grupo |
| ordem estrita, uma **depois** da outra | `Succession(...)` | e **não** `AnimationGroup(lag_ratio=1)` — §6.5 |

Diferença que importa: dentro de um `AnimationGroup` o clamp é **explícito no
código do grupo** (`sub_alphas[sub_alphas > 1] = 1`, **[FONTE
`composition.py:186`]**), não depende do decorador da curva. Ou seja, a mesma
lambda que explode em `self.play(a, b)` se comporta dentro de
`AnimationGroup(a, b)`. Não é motivo para escrever curva sem decorador — é
motivo para desconfiar quando "o mesmo código funciona aqui e não ali".

---

## 4. `rate_func` — a curva do tempo

### 4.1 O contrato e os dois decoradores

```python
class RateFunction(Protocol):
    def __call__(self, t: float, *args, **kwargs) -> float: ...
```
**[FONTE `utils/rate_functions.py:118-119`]** — a 50ª entrada da categoria
`utils/rate_functions`, que tem **49 funções + 1 protocolo**.

Dois decoradores, ambos exportados só de dentro do módulo:

| Decorador | Fora de `[0,1]` | Assinatura |
|---|---|---|
| `unit_interval(function)` | `t<0 → 0`, `t>1 → 1` | `(function: RateFunction) -> RateFunction` |
| `zero(function)` | `t<0` **ou** `t>1` → **0** | idem |

**[FONTE `rate_functions.py:120-145`]**. `@zero` está em `there_and_back`,
`there_and_back_with_pause` e `wiggle` — as três que **voltam ao ponto de
partida**. Todo o resto é `@unit_interval`, exceto as quatro fábricas
(`not_quite_there`, `squish_rate_func`, e os dois decoradores em si).

### 4.2 O que o `from manim import *` NÃO traz — 32 das 49

`utils/rate_functions.__all__` tem **17 nomes** **[FONTE `rate_functions.py:88-106`]**:

```
linear  smooth  smoothstep  smootherstep  smoothererstep  rush_into  rush_from
slow_into  double_smooth  there_and_back  there_and_back_with_pause
running_start  not_quite_there  wiggle  squish_rate_func  lingering
exponential_decay
```

As **30 `ease_*`**, mais `unit_interval` e `zero`, **não chegam pelo star
import** — confirmado contra `api/manim-ce-toplevel.md`, que lista os 17 e
nenhum `ease_*`. O sintoma é `NameError: name 'ease_out_expo' is not defined`,
e é o pedido "meu rate_func não existe".

O módulo `rate_functions` **está** no topo (`api/manim-ce-toplevel.md:599`,
marcado `[só no topo]`). Então as duas formas certas são:

```python
from manim import *
self.play(FadeIn(t), rate_func=rate_functions.ease_out_expo)      # via módulo

from manim.utils.rate_functions import ease_out_expo               # import direto
```

O idioma do deck é o segundo, num alias com nome de intenção (§10.5).

### 4.3 O catálogo — as 49, com valores calculados

Todos os números abaixo foram **calculados** chamando cada função em `t = 0,25`,
`0,5`, `0,75` e varrendo `t` em 2001 pontos para achar mínimo e máximo
**[MEDIDO]**. `min`/`max` fora de `[0,1]` significam **ultrapassagem** — o
mobject passa do destino ou recua antes de partir.

#### O padrão e as sigmoides

| Curva | min | max | t=,25 | t=,5 | t=,75 | Efeito percebido |
|---|---:|---:|---:|---:|---:|---|
| `linear` | 0 | 1 | ,250 | ,500 | ,750 | mecânico. Certo para rotação contínua, régua, cronômetro; **errado** para qualquer coisa que "chega" |
| **`smooth`** ★ | 0 | 1 | **,070** | ,500 | ,930 | o default de `Animation`. Sigmoide com `inflection=10`, **bem mais agressiva nas pontas que um smoothstep** |
| `smoothstep` | 0 | 1 | ,156 | ,500 | ,844 | 3t²−2t³. Suave e discreta; a mais "neutra" das simétricas |
| `smootherstep` | 0 | 1 | ,104 | ,500 | ,896 | 2ª ordem: aceleração zero nas pontas |
| `smoothererstep` | 0 | 1 | ,071 | ,500 | ,929 | 3ª ordem: jerk zero. Praticamente igual a `smooth` na leitura |
| `double_smooth` | 0 | 1 | ,250 | ,500 | ,750 | duas suavizadas emendadas: acelera, **desacelera no meio**, acelera de novo. Lê como duas etapas |
| `slow_into` | 0 | 1 | ,661 | ,866 | ,968 | quarto de círculo. Idêntica a `ease_out_circ` |
| `rush_into` | 0 | 1 | ,033 | ,140 | ,438 | meia sigmoide: parte devagar e **termina a toda** |
| `rush_from` | 0 | 1 | ,562 | ,860 | ,967 | o espelho: **larga rápido** e desacelera |

★ `smooth` é o default de `Animation.__init__`. **Não** é o default de todas as
classes: `Write`, `Unwrite`, `Wait`, `Rotating`, `AddTextLetterByLetter` e
**`AnimationGroup`** nascem com `linear` (§6.6, e `manim-animations` §3).

#### As 30 `ease_*` — três direções × dez formas

A direção diz **onde está a suavidade**: `in` = começo macio / fim seco;
`out` = começo seco / fim macio; `in_out` = os dois.

| Forma | `in` (t=,5) | `out` (t=,5) | `in_out` (t=,5) | Leitura |
|---|---:|---:|---:|---|
| `sine` | ,293 | ,707 | ,500 | a mais discreta de todas. Quando você quer só "tirar o robótico" |
| `quad` | ,250 | ,750 | ,500 | discreta |
| `cubic` | ,125 | ,875 | ,500 | o meio-termo confortável |
| `quart` | ,062 | ,938 | ,500 | já é dramática |
| `quint` | ,031 | ,969 | ,500 | muito dramática |
| `expo` | ,031 | **,969** | ,500 | **a desaceleração longa** — chega quase tudo no primeiro terço e "assenta". É a curva de UI da Apple |
| `circ` | ,134 | ,866 | ,500 | arco de círculo: fim/começo abrupto e depois constante |
| `back` | −,088 | **1,088** | ,500 | **ultrapassa** (min −0,100 / max 1,100): recua antes de sair, ou passa do ponto e volta |
| `elastic` | −,016 | **1,016** | ,500 | mola: **min −0,373 / max 1,373** no `out`. Várias oscilações |
| `bounce` | ,234 | ,766 | ,500 | quica. Três quiques decrescentes |

Ancoragem útil no `out` (`t = 0,25`, ou seja **um quarto do tempo**):
`sine ,383` · `quad ,438` · `cubic ,578` · `quart ,684` · `quint ,763` ·
`expo ,823` · `circ ,661` · `back ,817` · `elastic ,912` · `bounce ,473`
**[MEDIDO]**. `ease_out_expo` já entregou **82%** do movimento no primeiro
quarto do tempo — é isso que faz a plateia sentir que a coisa "chegou" antes de
o `run_time` acabar.

Ultrapassagens exatas **[MEDIDO]**: `ease_out_back` **1,100** ·
`ease_in_back` **−0,100** · `ease_in_out_back` **−0,100 / 1,100** ·
`ease_out_elastic` **1,373** · `ease_in_elastic` **−0,373** ·
`ease_in_out_elastic` **−0,118 / 1,118**.

> **Ultrapassagem é orçamento de espaço, não só de tempo.** Um `ease_out_back`
> num texto que já encosta na margem estoura o quadro em 10% da distância
> percorrida — e `.slides`/o `overflow` do palco não avisam. "Cabe na tela?" é
> de `manim-layout-posicionamento`; a causa aqui é a curva.

#### As três que voltam ao começo (`@zero`)

| Curva | min | max | t=,25 | t=,5 | t=,75 | Termina em |
|---|---:|---:|---:|---:|---:|---:|
| `there_and_back` | 0 | 1 | ,500 | **1,000** | ,500 | **0** |
| `there_and_back_with_pause` | 0 | 1 | ,930 | 1,000 | ,930 | **0** |
| `wiggle` | **−,733** | **,733** | ,500 | ,000 | −,500 | **0** |

- `there_and_back(t, inflection=10.0)` — vai e volta suave. É o `rate_func` de
  fábrica do `Indicate` **[FONTE]**, e é por isso que `Indicate` devolve o
  mobject ao estado original.
- `there_and_back_with_pause(t, pause_ratio=1/3)` — vai, **fica parado no topo
  um terço do tempo**, volta. Medido: platô exato de `t = 0,333` a `t = 0,667`
  **[MEDIDO]**. É a curva do "destaca, segura, solta" — a única do catálogo com
  um repouso embutido, e portanto a única que dá tempo de **falar** sobre o que
  foi destacado sem gastar um `play` extra.
- `wiggle(t, wiggles=2)` — **nunca chega a 1** (máximo 0,733, em `t ≈ 0,33`) e
  **fica negativa**: medido, num `Dot` que deveria andar +4, `alpha = 0,75` dá
  **x = −2,00** **[MEDIDO]**. Ela passa *atrás* do ponto de partida. Isso é
  desejado num chacoalhão e é um defeito em qualquer outro uso.

**Consequência comum às três:** a animação **termina onde começou**. Usar
`there_and_back` num `FadeIn` faz o objeto aparecer e sumir — e como
`FadeIn` é `introducer`, ele fica na cena, invisível. Sintoma: "o objeto não
apareceu, mas está lá".

#### As que não terminam em 1

| Curva | Fim | Para quê |
|---|---:|---|
| `not_quite_there(func=smooth, proportion=0.7)` | **0,7** | "chega quase lá". Medido: um `Dot` que deveria andar +4 para em **+2,80** depois do `finish()` **[MEDIDO]** |
| `lingering` | 1,0 em **t = 0,8** | chega ao destino a 80% do `run_time` e **segura** os 20% finais. Medido: `t=0,79 → 0,9875`, `t=0,80 → 1,0`, `t=0,90 → 1,0` **[MEDIDO]** |
| `exponential_decay(t, half_life=0.1)` | ~1 já em `t = 0,3` | `1 − e^(−t/h)`. Com o default, **95% do movimento em 30% do tempo** (`t=0,1 → 0,632`; `t=0,3 → 0,950`). O resto do `run_time` é cauda visual |
| `running_start(t, pull_factor=-0.5)` | 1,0 | **recua** antes de partir: mínimo **−0,185** em `t ≈ 0,29` **[MEDIDO]**. É o "toma impulso" |

> `lingering` é a curva mais subestimada do catálogo para vídeo de aula: ela
> **fabrica um respiro dentro do próprio `play`**, sem `wait` separado e sem
> partial movie a mais. O comentário `# TODO: Isn't this just 0.8 * t?` no fonte
> **está errado** — a conta é `squish_rate_func(identity, 0, 0.8)(t)`, que dá
> `min(t/0,8, 1)`, e não `0,8·t` **[FONTE `rate_functions.py:300-306` + MEDIDO]**.

#### As quatro fábricas (devolvem uma curva, não um valor)

| Nome | Assinatura | Devolve |
|---|---|---|
| `squish_rate_func` | `(func, a=0.4, b=0.6) -> RateFunction` | `func` comprimida na janela `[a,b]`; 0 antes de `a`, 1 depois de `b` |
| `not_quite_there` | `(func=smooth, proportion=0.7) -> RateFunction` | `proportion * func(t)` |
| `unit_interval` | `(function) -> RateFunction` | decorador de clamp |
| `zero` | `(function) -> RateFunction` | decorador de anulação |

**Chame a fábrica.** `rate_func=squish_rate_func` (sem parênteses) passa a
fábrica no lugar da curva; o resultado é lixo silencioso, porque ela aceita um
`float` como `func` e devolve um closure.

### 4.4 Escolher: da intenção para a curva

| O que a pessoa pede | Curva | Por quê |
|---|---|---|
| "não deixa robótico" | `ease_in_out_sine` ou `smoothstep` | a menor alteração possível sobre `linear` |
| "que desacelere no fim", "que assente" | **`ease_out_expo`** | 82% do movimento no primeiro quarto **[MEDIDO]**; é a assinatura do deck |
| "entra e para bonito" | `ease_out_cubic` | meio-termo; menos dramática que `expo` |
| "com efeito de mola" | `ease_out_back` | ultrapassa 10% e volta |
| "quica" | `ease_out_bounce` | três quiques |
| "toma impulso antes" | `running_start` | recua 18,5% |
| "vai e volta", "pisca" | `there_and_back` | termina no início |
| "destaca e SEGURA" | `there_and_back_with_pause` | platô de 1/3 no topo |
| "chega antes e espera" | `lingering` | chega em 80% do tempo |
| "chacoalha" | `wiggle` | oscila e passa atrás |
| "rotação contínua", "régua", "contador" | `linear` | qualquer easing num valor numérico mente sobre a taxa |
| "acelera no fim" | `rush_into` ou `ease_in_*` | |
| "essa parte da animação começa mais tarde" | `squish_rate_func(smooth, a, b)` | §7 |

### 4.5 Curvas que já vêm trocadas de fábrica

Não sobrescreva sem saber o que estava lá **[FONTE, assinaturas do índice]**:

| Classe | `rate_func` de fábrica | Consequência |
|---|---|---|
| `Animation` (base) | `smooth` | |
| `AnimationGroup` e filhas | **`linear`** | §6.6 |
| `Write` / `Unwrite` | `linear` | e o `run_time` é calculado sozinho |
| `Wait` | `linear` | e `Wait.interpolate` é `pass` — a curva é **inerte** (§9.2) |
| `Rotating` | `linear` | |
| `AddTextLetterByLetter` / `RemoveTextLetterByLetter` | `linear` | |
| `DrawBorderThenFill` | `double_smooth` | as duas fases |
| `Indicate` / `ApplyWave` / `Wiggle` / `Circumscribe` | `there_and_back` e parentes | voltam ao estado original |
| `PhaseFlow` | `linear` | |

### 4.6 Escrever a sua

```python
from manim.utils.rate_functions import unit_interval

@unit_interval                      # OBRIGATÓRIO: sem isso, veja §3.1
def freio_de_mao(t: float) -> float:
    """Anda 90% em metade do tempo, depois arrasta."""
    return 1.8 * t if t < 0.5 else 0.9 + 0.2 * (t - 0.5)
```

Três regras:

1. **Decore.** `@unit_interval` para curva normal, `@zero` para curva que volta
   ao começo. Sem decorador, `alpha > 1` vira o defeito do §3.1.
2. **Termine em 1,0** — a menos que a intenção seja a do `not_quite_there`.
   `finish()` chama `interpolate(1)` e o estado final da cena é literalmente
   `rate_func(1)` aplicado.
3. **`f(0)` deve ser 0.** O primeiro frame de todo `play` é `alpha = 0` (§1.3):
   se `f(0) != 0`, o objeto **salta** no primeiro frame.

---

## 5. `path_func` — por onde, não quando

### 5.1 O contrato

```python
path(start_points: Point3D_Array, end_points: Point3D_Array, alpha: float) -> Point3D_Array
```

Aplica-se à família `Transform` (e a tudo que herda dela: `ReplacementTransform`,
`MoveToTarget`, `ApplyMethod`, `Restore`, `_MethodAnimation` do `.animate`…).
Recebe o alpha **já passado pela `rate_func`** — nunca decide velocidade.

### 5.2 Os seis, com assinatura do índice

| Função | Assinatura | O que faz |
|---|---|---|
| `straight_path()` | `() -> PathFuncType` | linha reta. Devolve o próprio `interpolate` de `utils.bezier` **[FONTE `paths.py:76`]** |
| `path_along_arc(arc_angle, axis=OUT)` | `(float, Vector3DLike) -> PathFuncType` | arco de `arc_angle` radianos |
| `clockwise_path()` | `() -> PathFuncType` | **é** `path_along_arc(-π)` **[FONTE `paths.py:268`]** |
| `counterclockwise_path()` | `() -> PathFuncType` | **é** `path_along_arc(+π)` **[FONTE `paths.py:314`]** |
| `spiral_path(angle, axis=OUT)` | `(float, Vector3DLike) -> PathFuncType` | espiral: gira enquanto encolhe a distância |
| `path_along_circles(arc_angle, circles_centers, axis=OUT)` | `(float, Point3DLike_Array, Vector3DLike) -> PathFuncType` | um centro de arco por ponto — para trajetórias que não compartilham centro |

```python
self.play(Transform(a, b, path_func=path_along_arc(PI / 2), rate_func=smooth))
```

### 5.3 As três armadilhas

1. **São FÁBRICAS. Chame.** `path_func=path_along_arc` (sem argumento) é a
   função-fábrica, não um caminho. Até `straight_path` precisa de `()`. O
   `TypeError` aparece só no primeiro frame, dentro do `interpolate`.
2. **`spiral_path` e `path_along_circles` NÃO estão no star import.**
   `paths.__all__` tem só quatro nomes: `straight_path`, `path_along_arc`,
   `clockwise_path`, `counterclockwise_path` **[FONTE `paths.py:5-10`]** — e
   `api/manim-ce-toplevel.md` confirma que os outros dois não chegam. Os
   próprios exemplos da docstring escrevem `utils.paths.spiral_path(...)`.
   Use `from manim.utils.paths import spiral_path`.
3. **Ângulo pequeno vira linha reta em silêncio.** `path_along_arc` e
   `spiral_path` fazem `if abs(angle) < STRAIGHT_PATH_THRESHOLD: return
   straight_path()`, com `STRAIGHT_PATH_THRESHOLD = 0.01`
   **[FONTE `paths.py:30, 208, 367`]**. Um arco de 0,5° (0,0087 rad) some
   sem aviso.

A **precedência** entre `path_func`, `path_arc_centers` e `path_arc` no
construtor do `Transform` (`path_func` > `path_arc_centers` > `path_arc`) é de
`manim-animations` §8.4 — é decisão de qual `Transform` usar, não de ritmo.

---

## 6. Composição: `AnimationGroup`, `Succession`, `LaggedStart`, `LaggedStartMap`

### 6.1 As quatro assinaturas, do índice

```python
AnimationGroup(*animations: Animation | Iterable[Animation],
               group: Group | VGroup | OpenGLGroup | OpenGLVGroup | None = None,
               run_time: float | None = None,
               rate_func: Callable[[float], float] = linear,
               lag_ratio: float = 0, **kwargs)

Succession(*animations: Animation, lag_ratio: float = 1, **kwargs)

LaggedStart(*animations: Animation, lag_ratio: float = 0.05, **kwargs)

LaggedStartMap(animation_class: type[Animation], mobject: Mobject,
               arg_creator: Callable[[Mobject], Iterable[Any]] | None = None,
               run_time: float = 2, lag_ratio: float = 0.05, **kwargs)
```

`Succession`, `LaggedStart` e `LaggedStartMap` **herdam de `AnimationGroup`** e
só trocam o `lag_ratio` default — exceto a `Succession`, que reescreve
`begin`/`interpolate` (§6.5).

Métodos próprios de `AnimationGroup` **[FONTE `api/manim-ce-methods.tsv`]**:
`init_run_time(run_time)` · `build_animations_with_timings()` · `begin` ·
`interpolate` · `finish` · `clean_up_from_scene` · `update_mobjects` ·
`get_all_mobjects`. Da `Succession`, mais duas:
`next_animation()` e `update_active_animation(index)`.

### 6.2 A linha do tempo, exatamente

```python
lags   = run_times[:-1] * self.lag_ratio
start  = [0, *accumulate(lags)]
end    = start + run_times
max_end_time = max(end)                     # <- o run_time do grupo, se você não passar um
```
**[FONTE `composition.py:146-160`, `123-144`]**

Duas coisas que só se veem lendo isso:

- **O atraso da animação `i` é uma fração do `run_time` da animação `i−1`**, não
  do total nem do próprio. Com durações desiguais, os atrasos ficam desiguais.
- **`init_run_time` devolve `max(end)`**, não `sum` nem `max(run_times)`. Com
  `run_time=None` (o default), o grupo **dura o que a linha do tempo pedir**.

E `interpolate` **[FONTE `composition.py:162-195`]**:

```python
anim_group_time = self.rate_func(alpha) * self.max_end_time
...
sub_alphas[sub_alphas > 1] = 1              # clamp EXPLÍCITO (cf. §3.1)
```

Passar `run_time=X` ao grupo **não** muda a linha interna: ela continua indo de
0 a `max_end_time`, só que percorrida em `X` segundos. É um reescalonamento
proporcional — as proporções entre as animações se preservam.

### 6.3 `lag_ratio` alonga o grupo — e a docstring diz o contrário

`n` animações de 1 s cada **[MEDIDO]**:

| `lag_ratio` | n=3 | n=5 | n=10 | Leitura |
|---:|---:|---:|---:|---|
| 0 | 1,00 s | 1,00 s | 1,00 s | tudo junto (= `AnimationGroup` puro) |
| **0,05** | 1,10 s | 1,20 s | 1,45 s | o default do `LaggedStart` |
| 0,25 | 1,50 s | 2,00 s | 3,25 s | |
| 0,30 | 1,60 s | 2,20 s | 3,70 s | a **mediana do deck** |
| 0,50 | 2,00 s | 3,00 s | 5,50 s | |
| 1,00 | 3,00 s | 5,00 s | 10,00 s | estritamente em fila |

A docstring do parâmetro afirma *"This does not influence the total runtime of
the animation"* **[FONTE `composition.py:49-51`]**. **Ela só vale quando você
passa `run_time` explicitamente.** Sem `run_time`, o total é `max(end)` e cresce
com `lag_ratio × (n−1)`. Um `LaggedStart` de 10 itens com `lag_ratio=0.5` que
você imaginava de 1 s ocupa **5,5 s** de vídeo.

**O default `lag_ratio=0.05` quase nunca é o que se quer numa aula.** Com itens
de 1 s a 60 fps, 0,05 é **3 frames** de defasagem entre um item e o seguinte —
abaixo do que a plateia lê como "um depois do outro". No deck consumidor, os 54
`LaggedStart` usam `lag_ratio` de **0,030 a 0,55, mediana 0,30** **[DECK]** —
seis vezes o default.

### 6.4 `run_time` desiguais invertem a ordem de término

O próprio fonte avisa, num comentário de 5 linhas **[FONTE `composition.py:137-142`]**.
Medido com `run_times = [2, 0.5, 0.5]` e `lag_ratio = 0.5` **[MEDIDO]**:

| Animação | start | end |
|---|---:|---:|
| 1 (2,0 s) | 0,00 | **2,00** |
| 2 (0,5 s) | 1,00 | 1,50 |
| 3 (0,5 s) | 1,25 | 1,75 |

A primeira **termina por último**. Numa cascata isso lê como bagunça — o item de
cima ainda está entrando quando os de baixo já pararam. **Cascata quer
`run_time` uniforme**; se algum item precisa de mais tempo, tire-o do grupo.

### 6.5 `Succession(a, b)` ≠ `AnimationGroup(a, b, lag_ratio=1)`

Mesma linha do tempo, resultados diferentes, nenhum erro. É o achado desta skill.

**O mecanismo** **[FONTE]**:

| | `AnimationGroup.begin()` (`composition.py:86-96`) | `Succession.begin()` (`composition.py:238-244`) |
|---|---|---|
| o que faz | `for anim in self.animations: anim.begin()` — **todas**, no instante 0 | `self.update_active_animation(0)` — só a **primeira** |
| quando as outras começam | nunca mais: já começaram | em `next_animation()`, quando a anterior termina (`:277-284`) |

`begin()` é onde cada animação **tira a fotografia do estado inicial**
(`create_starting_mobject` → `mobject.copy()`). No grupo, todas fotografam o
mesmo instante; na `Succession`, cada uma fotografa o estado que a anterior
deixou.

**A medição.** Dois `Rotate(quadrado, PI/2)` sobre o **mesmo** quadrado, lendo o
ângulo de um vértice a cada passo **[MEDIDO]**:

```
Succession       a=0,00  45° | a=0,25  90° | a=0,50 135° | a=0,75 180° | a=1,00 225°   FIM 225°
AnimationGroup   a=0,00  45° | a=0,25  90° | a=0,50  45° | a=0,75  90° | a=1,00 135°   FIM 135°
   (lag_ratio=1)                              ^^^^^^^^^ o salto para trás, no meio
```

O grupo gira 90° no total (não 180°) **e dá um salto visível de −90° na
metade** — o frame em que a segunda animação assume, partindo da fotografia
antiga. Em vídeo contínuo é um piscar; como **primeiro frame de uma parte de
apresentação**, é o quadro em que o vídeo fica parado enquanto o professor fala.

**A regra:**

| Situação | Use |
|---|---|
| animações **independentes**, escalonadas | `LaggedStart` / `AnimationGroup(lag_ratio=…)` |
| animações que **dependem do estado** deixada pela anterior | **`Succession`** |
| duas ou mais animações sobre o **mesmo mobject** | **`Succession`**, sempre |
| `Wait` no meio de uma coreografia | `Succession` (§6.7) |

Detalhe operacional: `Succession._setup_scene` guarda `self.scene`, e
`Succession.begin()` precisa dele. Fora de um `self.play` (dirigindo a animação
na mão, como fiz para medir), é preciso `anim.scene = None` antes do `begin()`
**[MEDIDO]** — `_setup_scene(None)` retorna cedo e nunca atribui o campo
**[FONTE `composition.py:254-262`]**.

### 6.6 A `rate_func` do grupo é uma SEGUNDA suavização

`AnimationGroup` nasce com `rate_func=linear` **de propósito**: a curva do grupo
se aplica à **linha do tempo inteira**, por cima da curva de cada sub-animação.

```python
anim_group_time = self.rate_func(alpha) * self.max_end_time     # [FONTE composition.py:168]
```

Passar `rate_func=smooth` a um `LaggedStart` **não** suaviza os itens (eles já
têm as próprias curvas) — **deforma o escalonamento**: os itens do meio passam a
disparar quase juntos e os das pontas ficam espaçados, porque o tempo do grupo
corre devagar-rápido-devagar. O sintoma é "a cascata ficou irregular e eu não
mudei o `lag_ratio`".

Quando isso **é** o que você quer, é um recurso: `Succession(*[Add(c,
run_time=0.2) for c in circulos], rate_func=smooth)` — o exemplo da própria
docstring do `Add` **[FONTE `animation.py:685-700`]** — revela uma grade com
cadência que acelera e desacelera.

### 6.7 `Wait` e `Add` dentro de composição

Ambos são animações de pleno direito (`animation/core`):

```python
Wait(run_time=1, stop_condition=None, frozen_frame=None, rate_func=linear)
Add(*mobjects: Mobject, run_time: float = 0.0)
```

- **`Wait` dentro de `AnimationGroup` não faz nada de útil**: com o `lag_ratio=0`
  default, ele roda em paralelo. Medido: `AnimationGroup(FadeIn(d), Wait(1),
  FadeOut(d))` tem `run_time = 1.0` e as três acontecem juntas **[MEDIDO]**.
  Dentro de `Succession(...)` o mesmo trio dá `run_time = 3.0` **[MEDIDO]** —
  que é o comportamento pretendido.
- **`Wait` numa composição custa frames de verdade.** A otimização de frame
  congelado exige uma `Wait` **sozinha** no `play`
  (`len(animations) == 1 and isinstance(animations[0], Wait)`,
  **[FONTE `scene.py:1355-1362`]**). Dentro de uma `Succession`, aquele segundo
  é renderizado quadro a quadro. Prefira `self.wait()` **entre** `play`s quando
  a pausa não precisa estar dentro da coreografia.
- **`Add` sozinho no `play` levanta `ValueError`.** `Add` tem `run_time=0.0` de
  fábrica; `get_run_time` devolve 0 e `validate_run_time` recusa `<= 0`
  **[INFERIDO, encadeando `animation.py:703-707` com `scene.py:1120-1125`]**.
  `Add` foi feita para viver **dentro** de uma `Succession`, e `Add(m,
  run_time=0.2)` é o idioma de "adiciona e espera um pouco" sem gastar um `Wait`
  separado **[FONTE, docstring de `Add`]**.
- `Wait(stop_condition=…, frozen_frame=True)` levanta `ValueError` no construtor
  **[FONTE `animation.py:615-617`]**.
- **`Wait` não aparece no `group`** do `AnimationGroup`: o grupo é montado só com
  `anim.mobject` das não-introdutoras, e `Wait.mobject` é `None`. Medido: o
  `AnimationGroup` do trio acima tem `len(group) == 2` **[MEDIDO]**. Não quebra.

### 6.8 `LaggedStartMap` — a cascata sobre os submobjects

```python
LaggedStartMap(animation_class, mobject, arg_creator=None, run_time=2, lag_ratio=0.05, **kwargs)
```

Constrói uma animação da classe dada **para cada submobject** de `mobject`
**[FONTE `composition.py:400-421`]**:

```python
args_list  = [arg_creator(submob) for submob in mobject]
animations = [animation_class(*args, **kwargs_sem_lag_ratio) for args in args_list]
```

```python
self.play(LaggedStartMap(FadeIn, VGroup(*linhas), lag_ratio=0.25, run_time=1.6))
```

Três notas:

- `arg_creator` devolve uma **tupla de argumentos**, não um mobject. O default é
  a identidade (o submobject vira o primeiro argumento).
- `run_time=2` é default **da classe**, não da `Animation` — 2 s, não 1.
- O `lag_ratio` é **removido** dos kwargs repassados às sub-animações
  (`anim_kwargs.pop("lag_ratio")`). Ele é do grupo, sempre.
- É `LaggedStart(*[Anim(sub) for sub in mob])` escrito curto. Quando você
  precisa de argumentos diferentes por item, escreva o `LaggedStart` na mão.

### 6.9 Detalhes que mordem

- **`remover` propaga.** `AnimationGroup.clean_up_from_scene` faz
  `if self.remover: anim.remover = self.remover` **[FONTE `composition.py:110-115`]**.
  `AnimationGroup(..., remover=True)` remove **tudo** da cena no fim.
- **Grupo vazio levanta `ValueError`** em `begin()`, não no construtor
  **[FONTE `composition.py:87-91`]** — um `LaggedStart(*[])` de uma
  list-comprehension que filtrou tudo só falha no `play`.
- **`AnimationGroup` aceita iteráveis aninhados** (`flatten_iterable_parameters`)
  — `AnimationGroup([FadeIn(a), FadeIn(b)], FadeIn(c))` funciona.
- `prepare_animation(anim)` converte um `_AnimationBuilder` (o `.animate`) em
  `Animation`; é o que permite `LaggedStart(a.animate.shift(UP), ...)`. **Não
  está no star import** — `from manim.animation.animation import
  prepare_animation` **[FONTE, ausente de `api/manim-ce-toplevel.md`]**.

---

## 7. `squish_rate_func` — escalonar sem grupo

A alternativa mais barata ao `LaggedStart` quando são **duas ou três** coisas: um
`play` só, cada animação com a curva comprimida na sua janela.

```python
squish_rate_func(func: RateFunction, a: float = 0.4, b: float = 0.6) -> RateFunction
```

Medido, com `smooth` e a janela default `[0,4 ; 0,6]` **[MEDIDO]**:

| t | 0 | 0,3 | 0,4 | 0,5 | 0,6 | 0,7 | 1,0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| valor | 0 | 0 | 0 | **0,5** | **1,0** | 1,0 | 1,0 |

Ou seja: **parada até `a`, a curva inteira entre `a` e `b`, parada depois**.

```python
self.play(
    FadeIn(cabecalho, rate_func=squish_rate_func(smooth, 0.0, 0.4)),
    FadeIn(corpo,     rate_func=squish_rate_func(smooth, 0.3, 0.8)),
    FadeIn(rodape,    rate_func=squish_rate_func(smooth, 0.6, 1.0)),
    run_time=1.6,
)
```

Quando preferir isto ao `LaggedStart`:

| | `squish_rate_func` | `LaggedStart` |
|---|---|---|
| duração total | **exatamente o `run_time` do `play`** | cresce com `lag_ratio × (n−1)` |
| janelas | **independentes e sobrepostas à vontade** | uniformes, derivadas do `lag_ratio` |
| n de itens | 2 a 4 (fica ilegível acima disso) | qualquer |
| gerado por laço | ruim | **é para isso que serve** |

Cuidado: quem aparece com `squish_rate_func` **fica na tela desde o frame 0**, com
`alpha = 0`. Para `FadeIn` isso é opacidade 0 (invisível) e está certo. Para uma
animação cujo `alpha = 0` já é visível (um `Transform` entre dois mobjects
diferentes, por exemplo), o objeto aparece parado antes de a janela abrir — aí o
certo é `LaggedStart`.

---

## 8. `ChangeSpeed` — acelerar ou frear no meio de uma animação

```python
ChangeSpeed(anim: Animation | _AnimationBuilder,
            speedinfo: dict[float, float],
            rate_func: Callable[[float], float] | None = None,
            affects_speed_updaters: bool = True, **kwargs)
```

`speedinfo` é `{fração_do_run_time: fator_de_velocidade}`. Entre dois nós, o
fator interpola por uma parábola escolhida para que a **velocidade** (a derivada)
seja contínua nos nós **[FONTE `speedmodifier.py:126-133`]**.

```python
self.play(ChangeSpeed(
    AnimationGroup(a.animate(run_time=1).shift(RIGHT * 8),
                   b.animate(run_time=1).shift(LEFT * 8)),
    speedinfo={0.3: 1, 0.4: 0.1, 0.6: 0.1, 1: 1},     # freia a 10% entre 40% e 60%
    rate_func=linear,
))
```

### 8.1 As quatro armadilhas, todas medidas

**1. O `run_time` NÃO se conserva — e a conta é surpreendente.** O `run_time` da
`ChangeSpeed` é `get_scaled_total_time() * anim.run_time`
**[FONTE `speedmodifier.py:212`]**. Medido no exemplo da própria docstring
(animação interna de 1 s): **3,209 s** **[MEDIDO]**. Freiar 20% do percurso a
10% da velocidade triplicou a duração. Um `speedinfo={1: 2}` (dobrar a
velocidade ao longo de tudo) dá **0,667 s** **[MEDIDO]**.

**2. `ChangeSpeed` MUTA o dicionário que você passa.** O construtor faz
`speedinfo[0] = 1` e `speedinfo[1] = …` quando as chaves faltam
**[FONTE `speedmodifier.py:137-140`]**. Medido: `{0.3:1, 0.4:0.1, 0.6:0.1, 1:1}`
volta como `{0.3:1, 0.4:0.1, 0.6:0.1, 1:1, 0:1}` **[MEDIDO]**. Um dicionário
constante no topo do módulo, reusado por três cenas, chega poluído na segunda.
**Passe sempre um literal ou um `dict(...)` novo.**

**3. `is_changing_dt` é estado de CLASSE, e a segunda construção falha.** Com o
default `affects_speed_updaters=True`, o construtor executa
`assert ChangeSpeed.is_changing_dt is False` e depois liga a flag
**[FONTE `speedmodifier.py:116-122`]**. A flag só é desligada quando a rate_func
interna é chamada com `t == 1` (`:194-196`), ou seja **durante o render**.
Medido: construir duas `ChangeSpeed` antes de tocar a primeira levanta
`AssertionError: Only one animation at a time can play that changes speed (dt)
for ChangeSpeed updaters` **[MEDIDO]**. Construir as animações todas no topo do
`construct` — que é um estilo comum — quebra. **Se você não usa
`ChangeSpeed.add_updater`, passe `affects_speed_updaters=False`**: medido, aí duas
instâncias coexistem sem problema **[MEDIDO]**.

**4. Updater normal ignora a mudança de velocidade.** Só updaters registrados por
`ChangeSpeed.add_updater(mobject, update_function, index=None,
call_updater=False)` (classmethod) seguem o `dt` alterado
**[FONTE `speedmodifier.py:235-249`]**. Os de `Mobject.add_updater` continuam no
`dt` do relógio. O assunto updater é de `manim-updaters-valuetracker`; a parte de
velocidade é esta.

### 8.2 Quando NÃO usar `ChangeSpeed`

Praticamente sempre, num vídeo de aula. Se o que você quer é "devagar aqui,
rápido ali", **duas `play` com `run_time` diferentes** dizem a mesma coisa, são
legíveis, cacheiam melhor e não trazem nenhuma das quatro armadilhas acima. Uma
`rate_func` composta (`squish_rate_func`, `double_smooth`) cobre a maior parte do
resto. `ChangeSpeed` ganha quando a animação é **uma só e indivisível** — um
`MoveAlongPath` longo, uma câmera atravessando um diagrama — e você precisa de um
freio no meio dela.

Contagem no deck consumidor: **0 usos de `ChangeSpeed`** em 11 arquivos de cena
**[DECK]**.

---

## 9. `wait`, `pause`, `wait_until` — o respiro

### 9.1 As três assinaturas

```python
Scene.wait(duration: float = 1.0,
           stop_condition: Callable[[], bool] | None = None,
           frozen_frame: bool | None = None) -> None
Scene.pause(duration: float = 1.0) -> None                    # = wait(frozen_frame=True)
Scene.wait_until(stop_condition: Callable[[], bool], max_time: float = 60) -> None
```
**[FONTE `scene.py:1223-1291`]**. `pause` é literalmente `wait(duration,
frozen_frame=True)`; `wait_until` é `wait(max_time, stop_condition=…)`.

### 9.2 O que um `wait` é, mecanicamente

- **É um `play`.** `Scene.wait` monta uma `Wait` e chama `self.play(...)`
  **[FONTE `scene.py:1250-1256`]**. Ele conta no `Scene.time`, gera partial movie
  próprio e entra no hash do cache.
- **`Wait.interpolate` é `pass`** **[FONTE `animation.py:637-638`]** — a
  `rate_func` de uma `Wait` é **inerte**. A única exceção é dentro de
  `ChangeSpeed`, que substitui o método por monkey-patch para poder acionar
  updaters **[FONTE `speedmodifier.py:216-221`]**.
- **Frame congelado × frames de verdade**: §1.4.
- **`self.wait(0)` levanta `ValueError`; `self.wait(0.01)` é elevado a `1/fps`
  e grava 1 frame, com warning.** §1.5 e §1.4.

### 9.3 O respiro é o parâmetro que mais falta

Um vídeo "correndo" quase nunca é `run_time` curto demais: é **falta de repouso
entre os beats**. A plateia precisa de um momento com a tela parada para ler o
que acabou de entrar — e o professor precisa dele para falar.

Números observados no deck consumidor **[DECK]**, contados estaticamente nos 11
arquivos de cena:

| `wait` | ocorrências |
|---|---:|
| `self.wait(0.4)` | **48** |
| `self.wait(0.5)` | 13 |
| `self.wait(0.8)` | 10 |
| `self.wait(0.35)` | 10 |
| `self.wait(PAUSA)` (= 0,7) | 9 |
| `self.wait(0.6)` / `self.wait(0.3)` | 6 / 6 |

A cauda modal é **0,4 s** — 24 frames a 60 fps. Isso é o suficiente para o olho
assentar e curto o bastante para não parecer travado.

**Onde esta skill para, aqui:** a *cauda de uma parte de apresentação* (o
`wait` imediatamente antes do `next_section`, o teto de 0,4 s, o `wait(0.8)` do
fecho, e por que o `wait` mora **antes** do corte) é política de
`manim-presentation-parts` §3.4 e §5.5. Eu dou o mecanismo; ela dá a regra.

---

## 10. Como um vídeo ganha ritmo em vez de correr

### 10.1 Um vocabulário nomeado, não números soltos

`run_time=0.8` espalhado por 900 linhas é irrevisável. `run_time=BASE` diz *por
que* aquele tempo, e "o vídeo está rápido demais" vira **uma** edição.

```python
# tema.py — o vocabulário de movimento do projeto
from manim.utils import rate_functions

SAIDA     = rate_functions.ease_out_expo      # a curva-assinatura: desaceleração longa
ENTRA_SAI = rate_functions.ease_in_out_sine   # para o que vai e volta

RAPIDO, BASE, LENTO   = 0.45, 0.8, 1.4        # três durações, e só três
PAUSA, PAUSA_LONGA    = 0.7, 1.4              # respiro depois de cada beat
```

Estrutura real do deck consumidor
(`aulas/002-deepseek-harness/manim/tema.py:243-258`) **[DECK]**. Os **valores**
são daquele palco; o que transfere é a forma: **duas curvas, três durações, duas
pausas**. Onde esse arquivo mora e o que mais ele carrega é assunto de
`manim-tema-projeto`.

### 10.2 A estatística de um projeto que já rodou

Contado nos 11 arquivos de cena do deck consumidor **[DECK]**:

| | ocorrências |
|---|---:|
| `rate_func=SAIDA` (`ease_out_expo`) | **208** |
| `rate_func=ENTRA_SAI` (`ease_in_out_sine`) | 7 |
| `rate_func=rate_functions.ease_in_quad` | 1 |
| `run_time=BASE` (0,8 s) | **108** |
| `run_time=RAPIDO` (0,45 s) | **104** |
| `run_time=LENTO` (1,4 s) | 12 |
| `LaggedStart(` | **54** |
| `AnimationGroup(` | 2 |
| `Succession(` / `ChangeSpeed(` | **0** / **0** |
| `lag_ratio` explícito | 54 valores, de 0,030 a 0,55, **mediana 0,30** |

Quatro leituras, e as quatro são conselho:

1. **Uma curva responde por 96% do movimento.** Um projeto com identidade usa
   *uma* curva-assinatura e abre exceção por motivo, não por variedade.
2. **Duas durações respondem por 90% dos `run_time`.** Três degraus bastam. Uma
   escala com sete valores vira ruído.
3. **A composição usada é uma só: `LaggedStart`.** `AnimationGroup` puro e
   `Succession` aparecem quando são necessários — não como default.
4. **O `lag_ratio` mediano é 6× o default da biblioteca.** Ver §6.3.

### 10.3 O orçamento: um beat, uma frase

A conta que funciona para vídeo de aula, do deck **[DECK]** e coerente com o
formato em partes:

```
1 beat = 1 play (0,45–1,4 s)  +  1 wait (0,3–0,8 s)  ≈  1,0 a 2,0 s
```

E um beat carrega **uma** frase falada. Daí sai a granulação: se o ato tem dois
recados, são dois beats — e, num vídeo de slide, duas partes
(`manim-presentation-parts`). A duração total de uma cena é
`Σ run_time + Σ wait`, e dá para conferir sem renderizar (§10.5).

### 10.4 Ritmo é contraste, não velocidade média

Um vídeo com tudo em 0,8 s e pausa de 0,5 s é monótono, não ritmado. O contraste
vem de três lugares, nesta ordem de eficácia:

1. **A duração**: o beat que importa dura `LENTO`, os de serviço duram `RAPIDO`.
2. **A pausa**: `PAUSA_LONGA` depois da frase que a plateia precisa digerir.
3. **A curva**: reserve a ultrapassagem (`ease_out_back`) e o platô
   (`there_and_back_with_pause`) para **um** momento por cena. Duas molas numa
   cena viram circo — o mesmo princípio de "um efeito marcante por slide".

### 10.5 `Animation.set_default` — mudar o ritmo do projeto inteiro

```python
Animation.set_default(**kwargs) -> None            # classmethod
```
**[FONTE `api/manim-ce-methods.tsv`]**. Chamado numa subclasse, muda o default
**daquela classe**:

```python
# no tema.py, uma vez
FadeIn.set_default(run_time=BASE, rate_func=SAIDA)
Create.set_default(run_time=BASE, rate_func=SAIDA)
Rotate.set_default(run_time=LENTO, rate_func=rate_functions.linear)
```

É estado global do processo — vale para todas as cenas do módulo, e é
exatamente por isso que ele mora no `tema.py` e não numa cena. O que
`set_default` **não** alcança (e a disciplina de tema em geral) é de
`manim-color-theming` §10-§11 e `manim-tema-projeto`.

### 10.6 Medir o ritmo sem renderizar

Três medições baratas, todas sem GPU:

```bash
# 1. o histograma de tempo do projeto: o vocabulário está sendo respeitado?
grep -rhoE "run_time=[A-Za-z0-9_.]+" manim/*.py | sort | uniq -c | sort -rn
grep -rhoE "self\.wait\([A-Za-z0-9_.]*\)" manim/*.py | sort | uniq -c | sort -rn
grep -rhoE "lag_ratio=[0-9.]+" manim/*.py | cut -d= -f2 | sort -n | \
  awk '{a[NR]=$1} END{print "n="NR, "min="a[1], "mediana="a[int(NR/2)], "max="a[NR]}'

# 2. quem escapou da curva-assinatura
grep -rn "rate_func=" manim/*.py | grep -v "SAIDA\|ENTRA_SAI"
```

```python
# 3. dentro do construct: o cronômetro da cena (Scene.time = renderer.time)
def construct(self):
    ...
    self.play(...)
    print(f"[ritmo] apos o ato 3: {self.time:.2f}s")
```

`Scene.time` é uma property que devolve `self.renderer.time`
**[FONTE `scene.py:231-233`]** e acumula `run_time` de `play` e `wait`. Não custa
frame nenhum.

O que **não** dá para medir sem renderizar: se o resultado ficou bonito. O ciclo
escrever → render rápido → **olhar o PNG** → corrigir é de
`manim-verificacao-visual`.

---

## 11. Receitas curtas

```python
# cascata de itens, cadência que a plateia lê como "um depois do outro"
self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.25) for l in linhas],
                      lag_ratio=0.30, run_time=1.6, rate_func=SAIDA))
# 5 itens, lag 0.30, run_time explícito: dura 1,6 s (sem o run_time, duraria 2,2 s)
```

```python
# coreografia dependente: cada passo parte de onde o anterior parou
self.play(Succession(
    Create(caixa, run_time=0.5),
    Write(rotulo, run_time=0.6),
    caixa.animate(run_time=0.4).set_stroke(ACENTO, 3),
))
```

```python
# duas entradas escalonadas, duração total fixa, sem grupo
self.play(
    FadeIn(titulo, rate_func=squish_rate_func(smooth, 0.0, 0.5)),
    FadeIn(corpo,  rate_func=squish_rate_func(smooth, 0.4, 1.0)),
    run_time=1.2,
)
```

```python
# destaca e SEGURA, para dar tempo de falar, sem gastar um play a mais
self.play(Indicate(numero, color=ACENTO, scale_factor=1.15,
                   rate_func=rate_functions.there_and_back_with_pause,
                   run_time=1.6))          # ~0,53 s de platô no topo
```

```python
# transição por arco: o objeto contorna em vez de atravessar o que está no meio
from manim.utils.paths import path_along_arc
self.play(Transform(a, b, path_func=path_along_arc(PI / 2),
                    rate_func=SAIDA, run_time=BASE))
```

```python
# beat completo: movimento + respiro
self.play(FadeIn(bloco, shift=UP * 0.3), run_time=BASE, rate_func=SAIDA)
self.wait(0.4)          # 24 frames a 60 fps; e é ele que mostra o alpha=1 (§1.3)
```

```python
# rotação contínua: linear, sempre — qualquer easing mente sobre a taxa
self.play(Rotate(engrenagem, TAU, run_time=4, rate_func=rate_functions.linear))
```

---

## 12. Armadilhas — a lista consolidada

**1. O último frame de um `play` não é o estado final** (§1.3). `np.arange` exclui
o fim; `interpolate(1)` roda depois do laço e não é renderizado. Feche com um
`wait`.

**2. `alpha` não é clampado pelo `Scene`** (§3.1). Numa `play` com durações
diferentes, a curta recebe `alpha > 1`. Uma `rate_func` sua sem `@unit_interval`
manda o objeto para fora do quadro: medi **+36,00** onde o esperado era +4,00.

**3. `lag_ratio` alonga o `LaggedStart`** (§6.3) — 10 itens a 0,5 duram 5,5 s. A
docstring diz que não influencia; ela só vale com `run_time` explícito.

**4. O default `lag_ratio=0.05` lê como simultâneo** (§6.3) — 3 frames a 60 fps.
Mediana observada em produção: **0,30**.

**5. `Succession` ≠ `AnimationGroup(lag_ratio=1)`** (§6.5). Mesma linha do tempo,
resultados diferentes, e um salto para trás visível no meio. Duas animações sobre
o mesmo mobject **sempre** pedem `Succession`.

**6. `lag_ratio` no `play` não reescalona um grupo já construído** (§2.3). As
timings são baked no `__init__`.

**7. Kwarg com erro de digitação no `play` não dá erro** (§2.3). `runtime=2` cria
um atributo que ninguém lê. Se "não mudou nada", confira a grafia primeiro.

**8. `run_time` no `play` sobrescreve o das animações** (§2.3). Passe por
animação e não repita no `play`.

**9. Só 17 das 49 `rate_function` estão no star import** (§4.2). `ease_out_expo`
dá `NameError`. Use `rate_functions.ease_out_expo` ou importe do módulo.

**10. `spiral_path` e `path_along_circles` também não estão** (§5.3) — só quatro
dos seis `path_func` chegam pelo `from manim import *`.

**11. `path_func` são fábricas: chame-as** (§5.3). Até `straight_path()`.

**12. Arco menor que 0,01 rad vira reta em silêncio** (§5.3).

**13. `there_and_back`, `there_and_back_with_pause` e `wiggle` terminam em ZERO**
(§4.3). Num `FadeIn`, o objeto aparece, some, e continua na cena — invisível.

**14. `wiggle` nunca chega a 1 e fica negativa** (§4.3). Máximo 0,733; medido
x = −2,00 num deslocamento de +4.

**15. `not_quite_there()` termina em 70%** (§4.3), permanentemente — `finish()`
chama `interpolate(1)` e `rate_func(1)` vale 0,7.

**16. `rate_func` numa `Wait` é inerte** (§9.2) — `Wait.interpolate` é `pass`.

**17. `self.wait(0)` levanta `ValueError`; `wait` menor que `1/fps` é elevado a
`1/fps`** (§1.4, §1.5). O segundo grava **1** frame e emite warning — não é
silencioso, e não é zero.

**18. A `rate_func` de um `AnimationGroup` é uma SEGUNDA suavização** (§6.6), por
cima da de cada item — deforma o escalonamento, não suaviza os itens.

**19. `AnimationGroup` vazio só falha no `begin()`** (§6.9), não no construtor.

**20. `ChangeSpeed` muta o `speedinfo` que você passou** (§8.1). Dicionário
constante reusado chega poluído.

**21. `ChangeSpeed.is_changing_dt` é estado de classe** (§8.1). Construir duas
antes de tocar a primeira levanta `AssertionError`. Use
`affects_speed_updaters=False` quando não houver `ChangeSpeed.add_updater`.

**22. `ChangeSpeed` não conserva duração** (§8.1) — medi 1 s virando **3,21 s** no
exemplo da própria documentação.

**23. `Add` sozinho no `play` levanta `ValueError`** (§6.7): `run_time=0.0` de
fábrica e `validate_run_time` recusa `<= 0`. Ele vive dentro de uma `Succession`.

**24. `Wait` dentro de `Succession` custa frames de verdade** (§6.7) — a
otimização de frame congelado exige a `Wait` sozinha no `play`.

**25. `run_time` desiguais dentro de um `LaggedStart` invertem a ordem de
término** (§6.4). Cascata quer durações uniformes.

**26. `run_time` curto demais para o FPS engasga** (§1.2). 0,45 s são **7
frames** em `-q l`. Avalie ritmo em `-q m` no mínimo — e lembre que `-r` não muda
o FPS (`manim-project`).

**27. Ultrapassagem é orçamento de ESPAÇO** (§4.3). `ease_out_back` estoura o
destino em 10%, `ease_out_elastic` em 37%. Perto da margem, isso corta.

**28. `f(0) != 0` numa curva sua faz o objeto saltar no primeiro frame** (§4.6),
porque o primeiro frame de todo `play` é `alpha = 0`.

---

## 13. Onde esta skill para

| Assunto | Skill dona | Fronteira |
|---|---|---|
| **qual** classe de animação usar, `.animate`, família `Transform`, `introducer`/`remover`, ciclo de vida da `Animation` | **`manim-animations`** | ela diz **o quê**, eu digo **quando**. `lag_ratio` de uma animação **isolada** (escalonar submobjects) é dela; `lag_ratio` de **composição** é meu |
| `path_arc` × `path_arc_centers` × `path_func` — a **precedência** no construtor do `Transform` | **`manim-animations`** §8.4 | eu documento os 6 `path_func` e o que cada um desenha |
| `ValueTracker`, updaters, `always_redraw`, `dt`, o que `skip_animations` quebra | **`manim-updaters-valuetracker`** | `ChangeSpeed.add_updater` é citado aqui só como exceção de velocidade |
| cortar a cena em **partes que o apresentador avança**, cauda de parte, emenda, o `wait` antes do `next_section` | **`manim-presentation-parts`** | eu dou o **mecanismo** do frame congelado e do último frame; ela dá a **política** (teto de 0,4 s, um recado por parte) |
| `next_section` como recurso da biblioteca, `Section`, o mapa das classes de `Scene`, ciclo de vida | **`manim-cenas-secoes`** | |
| `-q`, `-r`, `--fps`, formato, caminho de saída, cache de partial movie | **`manim-render-api`** | eu uso o FPS como orçamento de frames; escolher a qualidade é lá |
| custo de render, cache, o que é caro rasterizar | **`manim-performance-cache`** | |
| codec, NVENC, peso do arquivo | **`manim-gpu-encoding`** | |
| "cabe na tela?", margem, `is_off_screen`, buffers | **`manim-layout-posicionamento`** | a ultrapassagem de `ease_out_back` é ritmo virando layout; a régua é dela |
| cor, contraste, `set_default` **de cor** | **`manim-color-theming`** | `Animation.set_default` de **tempo** é meu (§10.5) |
| o `tema.py` como contrato (onde `SAIDA`/`BASE`/`PAUSA` moram) | **`manim-tema-projeto`** | eu digo **quais** constantes existem e por quê; ela diz como o arquivo se organiza |
| escrever uma `Animation` própria, `interpolate_mobject`, `override_animation` | **`manim-mobjects-customizados`** | escrever uma **`rate_func`** própria é meu (§4.6) |
| olhar o PNG, conferir que nada sumiu ou saiu do quadro | **`manim-verificacao-visual`** | |
| descobrir se um nome existe / assinatura / kwarg | **`manim-api-discovery`** | |
| ritmo no **ManimGL** (`3b1b`) | **`manimgl-3b1b`** | as `rate_func` do GL têm outros nomes e outra base |
| `Homotopy`, `PhaseFlow`, `ComplexHomotopy` (o `virtual_time` deles é ritmo, mas o assunto é campo vetorial) | **órfão** — não existe skill | aqui está só a assinatura, via `manim-animations` |
| `ShowPassingFlash` / `time_width` como recurso de ênfase | **órfão** — ênfase e anotação não têm skill | `time_width` é um parâmetro de tempo, mas quem o usa é `animation/indication`, cujo catálogo está em `manim-animations` §7.3 |

---

## 14. O que NÃO foi verificado nesta rodada

Escrito para a próxima pessoa não confundir leitura com medição:

- **Nada foi renderizado.** Nenhum `mx render`, nenhum frame escrito, nenhum
  `ffmpeg`, nenhuma GPU. Toda contagem de frames desta skill vem de **reproduzir
  em Python puro a fórmula do fonte** (`np.arange(0, run_time, 1/fps)` e
  `int(duration/dt)`), não de contar frames num mp4.
- **O "efeito percebido" de cada curva** (§4.3, §4.4) é interpretação minha dos
  valores calculados. Os **números** são medição; a coluna "leitura" é opinião
  informada, e é onde vale discordar.
- **O salto de −90° do `AnimationGroup(lag_ratio=1)`** (§6.5) foi medido lendo o
  ângulo do mobject a cada `interpolate()`, não olhando um vídeo. Que ele seja
  *visível* na tela é inferência — sólida, porque é um frame inteiro com o
  objeto a 90° do lugar, mas inferência.
- **`Add` sozinho no `play` levantando `ValueError`** (§6.7) está marcado
  **[INFERIDO]**: encadeei `Add.run_time = 0.0` com `get_run_time` → `max` →
  `validate_run_time(<= 0)`. Não executei o `play`. Se alguém confirmar (ou
  derrubar), corrija aqui.
- **Os números do deck** (§9.3, §10.2) foram contados por `grep` nos arquivos
  `.py` do consumidor em 2026-08-19. São contagem de código, não medição de
  vídeo — um `run_time=BASE` dentro de um bloco morto conta igual.
- **Nada sobre custo de render** de `lag_ratio`, `Wait` em `Succession` ou
  `ChangeSpeed`. A afirmação de que `Wait` numa `Succession` "custa frames de
  verdade" vem do desvio de código em `cairo_renderer.py:111-117` **[FONTE]**;
  quanto isso pesa em segundos é de `manim-performance-cache`, e não foi medido.
