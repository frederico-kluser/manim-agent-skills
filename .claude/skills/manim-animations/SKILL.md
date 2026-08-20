---
name: manim-animations
description: >-
  As 75 classes de animação do ManimCE 0.21, a sintaxe `.animate`, a família
  `Transform` inteira e a mecânica real de `self.play`. Use quando o pedido for
  "faz isso aparecer", "anima essa transição", "transforma A em B", "escreve o
  texto", "desenha o retângulo", "faz sumir", "destaca esse número", "pisca",
  "gira", "faz a barra crescer", "move ao longo da linha", "troca a fórmula",
  "essa animação não acontece", "o objeto some depois do play", "o alvo ficou
  na tela", "o `.animate.rotate` deforma", "a animação começa antes/depois do
  que eu quero", "`Create` deu TypeError", "por que o `Write` dura 2 segundos?",
  "o `Indicate` sumiu no fundo branco", "o `MoveToTarget` foi para o lugar
  errado", "quero que todas as animações do projeto tenham o mesmo tempo". Cobre
  o ciclo de vida de uma `Animation` (`__new__`/`begin`/`interpolate`/`finish`/
  `clean_up_from_scene`), os 9 parâmetros que TODA animação aceita, quem é
  `introducer`/`remover` (o que sobra na cena depois), `Animation.set_default`,
  e o catálogo completo com assinatura conferida no índice. NÃO use para: ritmo,
  `rate_func`, `path_func`, `AnimationGroup`/`Succession`/`LaggedStart`,
  `lag_ratio` de composição, `ChangeSpeed` e orçamento de tempo
  (skill `manim-composicao-ritmo`); estado reativo, `ValueTracker`, updaters,
  `always_redraw`, `TracedPath`, `AnimatedBoundary`, `DecimalNumber`
  (`manim-updaters-valuetracker`); criar, posicionar, agrupar ou medir mobject
  (`manim-mobjects`, `manim-layout-posicionamento`); escrever uma `Animation`
  própria ou `override_animation` (`manim-mobjects-customizados`); cortar a cena
  em partes para slide (`manim-presentation-parts`); cor e contraste
  (`manim-color-theming`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Animações — o catálogo, a família `Transform`, e `.animate`

Tudo abaixo foi conferido em **ManimCE 0.21.0** contra `api/manim-ce-index.tsv`,
`api/manim-ce-methods.tsv`, `api/manim-ce-inheritance.txt` e o fonte instalado em
`.venv/lib/python3.12/site-packages/manim/`. Onde a afirmação vem da leitura do
fonte e **não** de execução, está escrito **[fonte]**. Onde vem de medição feita
no deck consumidor `~/Projects/aulas` e não foi reproduzida aqui, está escrito
**[deck]**. Nesta rodada **nada foi renderizado** — nenhum número de tempo de
render aparece sem essa marca.

O resumo em cinco frases, para quem tem trinta segundos:

1. **Uma `Animation` interpola entre dois estados de um Mobject**, não repete o
   caminho do método. É por isso que `.animate.rotate(PI)` deforma e `Rotate`
   não.
2. **`self.play` adiciona sozinho** qualquer mobject animado que ainda não
   estava na cena — então "a animação não aconteceu" quase nunca é falta de
   `self.add`.
3. **O que sobra na cena depois do `play` é decidido por dois booleanos**,
   `introducer` e `remover`, e por `replace_mobject_with_target_in_scene`. É o
   §5 inteiro, e é a origem de "o objeto sumiu" e de "o alvo ficou na tela".
4. **`Transform.begin()` chama `align_data`**, que muda a estrutura de
   submobjects do mobject de origem. Depois de um `Transform`, `len(a.submobjects)`
   pode não ser mais o que era. **[fonte]**
5. **Toda cor default de ênfase é `PURE_YELLOW` (#FFFF00)** — contraste
   **1,07:1** sobre branco (19,56:1 sobre preto). `Indicate`, `Flash` e
   `Circumscribe` são invisíveis em tema claro sem `color=` explícito. A cura de projeto é `Indicate.set_default(...)`
   (§9), não repetir `color=` em cada chamada.

---

## 1. O modelo mental

Uma `Animation` guarda um mobject, um `run_time` e uma `rate_func`. O renderer a
percorre chamando `interpolate(alpha)` com `alpha` de 0 a 1, um por frame.
Nada acontece até `self.play`.

```python
self.play(Create(c))                    # uma
self.play(Create(c), Write(t))          # simultâneas: mesmo run_time, mesma janela
self.play(Create(c), run_time=2)        # duração
self.wait(1.5)                          # pausa
self.add(c)                             # sem animação, instantâneo
```

**As três formas de fazer algo se mexer**, e como escolher:

| Você quer | Ferramenta | Por quê |
|---|---|---|
| um efeito nomeado (aparecer, escrever, destacar) | **a classe** — `FadeIn`, `Write`, `Indicate` | o efeito é o produto, não o estado final |
| o mobject terminar num estado que você sabe descrever | **`.animate`** | você escreve o método que já usaria fora do `play` |
| o valor mudar e a cena reagir sozinha | **updater + `ValueTracker`** | ver `manim-updaters-valuetracker` — não é assunto desta skill |
| exatamente o caminho, não os extremos | a classe (`Rotate`, `MoveAlongPath`, `Homotopy`) | `.animate` interpola em linha reta ponto a ponto |

Uma quarta forma, `ApplyMethod(mob.shift, RIGHT)`, existe e **não está
depreciada** na biblioteca (§8.9) — mas `.animate` faz o mesmo com menos
cerimônia.

---

## 2. O ciclo de vida de uma `Animation`

Sete ganchos, nesta ordem. Saber qual roda quando é o que explica metade das
armadilhas desta skill. **[fonte: `animation/animation.py`]**

| Momento | Gancho | O que decide |
|---|---|---|
| você escreve `FadeIn(x)` | `Animation.__new__` | se o mobject registrou um **override** para esta classe, devolve OUTRA animação inteira (§6.7) |
| ainda no construtor | `Animation.__init__` | grava `run_time`, `rate_func`, `remover`, `introducer`… — **nada** de cópia de mobject aqui |
| `self.play(...)` | `Scene.compile_animations` | converte `.animate` em `Animation` e **sobrescreve** os kwargs do `play` em cada uma (§4) |
| antes do primeiro frame | `_setup_scene` | se `is_introducer()`, faz `scene.add(mobject)` |
| antes do primeiro frame | `begin()` | **aqui** nasce o `starting_mobject` (uma cópia), aqui `Transform` chama `create_target()` e `align_data`, e aqui os updaters do mobject são suspensos |
| um por frame | `interpolate(alpha)` → `interpolate_mobject` → `interpolate_submobject` | o desenho |
| depois do último frame | `finish()` | `interpolate(1)` + `resume_updating()`. No `.animate`, é aqui que os métodos são **reaplicados de verdade** (§6.3) |
| depois de `finish` | `clean_up_from_scene(scene)` | se `is_remover()`, `scene.remove(mobject)`. `ReplacementTransform` faz o `scene.replace` aqui |

Três consequências que se usam no dia a dia:

- **O alvo de um `Transform` é lido em `begin()`, não no construtor.** Você pode
  construir a animação, mexer no alvo, e só então tocar. É o que faz
  `MoveToTarget` funcionar.
- **`suspend_mobject_updating=True` é o default**: durante o `play`, os updaters
  **do mobject animado** não rodam. Se a sua animação precisa de um updater
  ativo, passe `suspend_mobject_updating=False`. Os updaters dos OUTROS mobjects
  da cena continuam rodando.
- **`begin()` copia o mobject.** Numa cena com um `VGroup` de milhares de
  submobjects, é aí que o custo aparece — não no construtor.

---

## 3. Os 9 parâmetros que TODA animação aceita

Assinatura real do `__init__`, de `api/manim-ce-methods.tsv`:

```
Animation.__init__(mobject, lag_ratio=0.0, run_time=1.0, rate_func=smooth,
                   reverse_rate_function=False, name=None, remover=False,
                   suspend_mobject_updating=True, introducer=False,
                   *, _on_finish=<lambda>, use_override=True)
```

**Não confunda com o que `bin/mx show Animation` mostra.** A linha `class` do
`api/manim-ce-index.tsv` traz `(mobject=None, *args, use_override=True, **kwargs)`
— que é a assinatura do **`__new__`** (§2), não a do construtor. Quando a
assinatura de uma animação parecer vazia demais, os parâmetros estão numa base:
`awk -F'\t' '$1=="Animation" && $2=="__init__"' api/manim-ce-methods.tsv`, ou a
varredura de kwargs pelo MRO de `manim-api-discovery §4`.

| Parâmetro | O que faz | Armadilha |
|---|---|---|
| `run_time` | duração em segundos | é uma **property** com setter que levanta `ValueError` para valor negativo **[fonte]**. Um kwarg de `play` sobrescreve o valor por-animação (§4) |
| `rate_func` | a curva do tempo | default **`smooth`** na `Animation` base, mas **`linear`** em `Write`, `Unwrite`, `Wait`, `Rotating`, `AddTextLetterByLetter` e `AnimationGroup` **[fonte]**. Catálogo e escolha: `manim-composicao-ritmo` |
| `reverse_rate_function` | roda a curva de trás para frente | é o mecanismo de `Uncreate`, `Unwrite`, `RemoveTextLetterByLetter`. **Não** é o mesmo que `rate_func=lambda t: 1-t`: ele age dentro do `get_sub_alpha`, depois do `lag_ratio` |
| `lag_ratio` | numa animação **sozinha**, atrasa **submobject a submobject** | é o que faz `Create(VGroup(a,b,c))` desenhar em sequência (`Create` tem `lag_ratio=1.0` de fábrica). Dentro de `AnimationGroup` o significado é outro — lá é `manim-composicao-ritmo` |
| `remover` | ao terminar, `scene.remove(mobject)` | §5 |
| `introducer` | antes de começar, `scene.add(mobject)` | §5 |
| `suspend_mobject_updating` | congela os updaters do mobject durante a animação | default **True**. É a resposta para "o meu updater parou durante o `play`" |
| `name` | rótulo na barra de progresso | cosmético |
| `use_override` | se `False`, ignora um override registrado pelo mobject | §6.7 |

O `lag_ratio` de uma animação isolada merece a conta, porque quase ninguém a
conhece. **[fonte: `Animation.get_sub_alpha`]**

```
full_length = (n_submobjects - 1) * lag_ratio + 1
sub_alpha_i = rate_func(alpha * full_length - i * lag_ratio)
```

Os "submobjects" aqui são `mobject.family_members_with_points()` — a família
**inteira e achatada**, não os filhos diretos. Num `Text`, isso é **um glifo por
elemento**. É por isso que `Write(texto, lag_ratio=0.3)` escreve letra a letra e
`Write(texto, lag_ratio=0)` faz o texto inteiro aparecer de uma vez.

Getters/setters, quando você guarda a animação numa variável:
`set_run_time` · `get_run_time` · `set_rate_func` · `get_rate_func` ·
`set_name` · `is_introducer` · `is_remover` · `copy` — todos devolvem `self`
(exceto os `get_*`/`is_*`), então encadeiam.

---

## 4. `self.play` — a mecânica real

```
Scene.play(*args: Animation | Mobject | _AnimationBuilder,
           subcaption=None, subcaption_duration=None, subcaption_offset=0,
           **kwargs) -> None
```

O que acontece com os argumentos, em ordem **[fonte: `Scene.compile_animations`]**:

1. **A lista de args é achatada um nível.** `self.play([a, b])`, `self.play(*[a, b])`
   e `self.play(a for a in anims)` são todos equivalentes.
2. Cada item passa por `prepare_animation`: um `_AnimationBuilder` (o `.animate`)
   vira `Animation` pelo `build()`; uma `Animation` passa direto; **qualquer
   outra coisa** levanta `TypeError: Object … cannot be converted to an animation`.
3. Se o item for um **método** (`self.play(sq.shift)`), a mensagem é específica:
   `TypeError: Passing Mobject methods to Scene.play is no longer supported. Use Mobject.animate instead.`
4. **Cada kwarg do `play` é escrito por `setattr` em TODAS as animações.**

O passo 4 é a armadilha, e é silenciosa:

```python
# ERRADO — o run_time=1 do play apaga o run_time=3 do Write
self.play(Write(t, run_time=3), Create(c), run_time=1)

# CERTO — sem kwarg no play, cada animação mantém o seu; a mais longa manda
self.play(Write(t, run_time=3), Create(c))
```

Duas notas que fecham o assunto:

- **`self.play(algum_mobject)` não funciona.** O type hint aceita `Mobject`, mas
  `prepare_animation` levanta `TypeError`. Para pôr na tela sem animar, use
  `self.add(m)`; para pôr na tela **dentro** de uma composição, use `Add(m)` (§7.8).
- **Duração de uma cena** = soma dos `run_time` + soma dos `wait`.
  `self.wait()` sem argumento espera 1 s (`DEFAULT_WAIT_TIME = 1.0`).
- `self.play(..., subcaption="texto")` grava legenda `.srt` — assunto de
  `manim-som-legendas`.

### `self.wait()` pode congelar o frame

`Scene.wait(duration=1.0, stop_condition=None, frozen_frame=None)`. Quando o
`wait` é a única animação, o Manim decide se precisa desenhar frames de verdade
ou repetir um só. A condição **[fonte: `Scene.should_update_mobjects`]**:

```
always_update_mobjects  or  self.updaters  or  stop_condition is not None
   or  any(mob.has_time_based_updater() for mob in família da cena)
```

Repare: **`has_time_based_updater`** — um updater cuja função recebe `dt`. Um
updater comum (`lambda m: ...`) **não** conta, e o `wait` congela. É a origem
clássica de "o `always_redraw` para de atualizar durante o `self.wait()`".
Detalhe e cura em `manim-updaters-valuetracker`; `frozen_frame=False` força o
desenho.

---

## 5. O que sobra na cena depois do `play`

Três mecanismos, todos lidos do fonte, e é aqui que nascem "o objeto sumiu" e
"o alvo ficou na tela".

- **`introducer=True`** → `_setup_scene` faz `scene.add(mobject)` antes do
  primeiro frame. Você **não precisa** de `self.add` antes.
- **`remover=True`** → `clean_up_from_scene` faz `scene.remove(mobject)`.
- **`replace_mobject_with_target_in_scene=True`** (só em `Transform`) →
  `scene.replace(mobject, target)`, que **preserva a ordem de desenho** e troca
  dentro do grupo pai, se houver **[fonte: `Scene.replace`]**.
- **Sem nada disso**, `Scene.add_mobjects_from_animations` adiciona qualquer
  mobject animado que ainda não estava na cena. Ou seja: `self.play(sq.animate.shift(RIGHT))`
  com `sq` nunca adicionado **funciona** — o quadrado simplesmente aparece.

A tabela, conferida classe a classe no fonte:

| Animação | `introducer` | `remover` | Fica na cena, ao final |
|---|:--:|:--:|---|
| `FadeIn` | ✔ | | o mobject, opaco |
| `FadeOut` | | ✔ | nada — **e o mobject é restaurado**: `clean_up_from_scene` chama `interpolate(0)`, então ele volta a opacidade/posição originais e pode ser reusado num `FadeIn` |
| `Create`, `DrawBorderThenFill` | ✔ | | o mobject |
| `Uncreate` | | ✔ | nada |
| `Write` | ✔ (se `reverse=False`) | ✔ (se `reverse=True`) | o mobject |
| `Unwrite` | | ✔ | nada |
| `GrowFrom*`, `GrowArrow`, `SpinInFromNothing`, `SpiralIn` | ✔ | | o mobject |
| `ShrinkToCenter` | | | **o mobject, com escala ~0** — `ScaleInPlace(0)` não remove nada. Combine com `FadeOut` ou `self.remove` |
| `AddTextLetterByLetter`, `TypeWithCursor` | ✔ | | o texto |
| `RemoveTextLetterByLetter`, `UntypeWithCursor` | | ✔ | nada |
| `ShowPassingFlash` | ✔ | ✔ | nada — e restaura o traço inteiro do mobject |
| `Flash` | — | — | nada (as linhas são `ShowPassingFlash`) |
| `FocusOn` | | ✔ | nada (o disco de foco some) |
| `Broadcast` | | ✔ | nada |
| `Circumscribe`, `Blink` | — | — | nada de novo (a moldura entra e sai) |
| `Indicate`, `Wiggle`, `ApplyWave` | | | o mobject, **de volta ao estado inicial** (a `rate_func` é `there_and_back`) |
| `Transform(a, b)` | | | **`a`**, com a aparência de `b`. `b` nunca entrou |
| `ReplacementTransform(a, b)` | | | **`b`**. `a` saiu |
| `TransformFromCopy(a, b)` | | | **`a` e `b`, os dois** |
| `TransformMatchingTex/Shapes` | | | **o alvo** — `clean_up_from_scene` remove a origem e adiciona o alvo |
| `Add(m)` | ✔ | | `m` |
| `Wait` | | | nada muda |

---

## 6. `.animate` — o caminho idiomático, e as seis armadilhas

### 6.1 O que ele é, por dentro

`mob.animate` devolve um `_AnimationBuilder` **[fonte: `mobject/mobject.py:3415`]**.
No construtor dele já acontece `mob.generate_target()`. Cada método que você
chama é aplicado **no `mob.target`** e guardado numa lista. No `play`, o
`build()` devolve um `_MethodAnimation`, que herda de `MoveToTarget`, que herda
de `Transform`. Ou seja: **`.animate` é um `Transform` do mobject para uma cópia
dele com os métodos aplicados.**

```python
self.play(sq.animate.shift(RIGHT * 2))
self.play(sq.animate.set_color(RED).scale(1.5))       # encadeado: um builder só
self.play(a.animate.shift(LEFT), b.animate.shift(RIGHT))
```

### 6.2 Passar `run_time`/`rate_func` no próprio `.animate`

A forma existe e está no docstring oficial da `Animation` **[fonte]**:

```python
self.play(grupo.animate(run_time=1.5, lag_ratio=0.1).shift(UP * 2))
```

**A ordem é obrigatória: os parênteses vêm ANTES do primeiro método.** O
`_AnimationBuilder.__call__` marca `cannot_pass_args = True` assim que qualquer
atributo é acessado, e a forma invertida levanta

```
ValueError: Animation arguments must be passed before accessing methods and can only be passed once
```

Isso vale quando você precisa de tempos **diferentes** para dois `.animate` no
mesmo `play` — um kwarg de `play` valeria para os dois (§4).

### 6.3 `.animate` interpola os EXTREMOS, não o caminho

Este é o motivo de metade dos "ficou estranho". O `Transform` interpola ponto a
ponto em linha reta. Consequências reais:

```python
self.play(sq.animate.rotate(PI))    # os pontos cruzam o centro: o quadrado
                                    # encolhe até virar uma linha e volta
self.play(Rotate(sq, PI))           # gira de verdade — Rotate é um Transform
                                    # com path_arc=angle (§8.4)
```

Outros casos do mesmo defeito: `.animate.arrange(...)` (os itens se atravessam),
`.animate.to_edge(...)` num objeto que precisa contornar outro, e qualquer coisa
com simetria de rotação (um `RegularPolygon` girado de `TAU/n` tem alvo idêntico
à origem — a animação existe e **não se vê nada**).

**Meia cura barata:** `.animate` aceita os kwargs de `Transform`, incluindo
`path_arc`:

```python
self.play(sq.animate(path_arc=PI / 2).shift(RIGHT * 4))   # sai pelo arco
```

### 6.4 No fim, os métodos são aplicados DE VERDADE

`_MethodAnimation.finish()` reexecuta cada método guardado sobre o mobject real
antes de chamar `super().finish()` **[fonte: `animation/transform.py:443`]**. Duas
consequências:

- o estado final é **exato**, não o resultado de uma interpolação — não sobra
  erro numérico;
- métodos com efeito colateral que a interpolação não captura (`add_updater`,
  `set_z_index`) **funcionam**, mas só a partir do último frame.

### 6.5 `.animate` destrói `mob.target`

Porque o builder chama `generate_target()`. Portanto:

```python
mob.generate_target()
mob.target.shift(UP * 2)
self.play(mob.animate.set_color(RED))   # <-- aqui mob.target foi refeito
self.play(MoveToTarget(mob))            # move para o alvo do .animate, não o seu
```

Escolha um dos dois idiomas por mobject: ou `generate_target()` + `MoveToTarget`,
ou `.animate`. Misturar não dá erro.

### 6.6 Dois `.animate` do MESMO mobject no mesmo `play`

```python
self.play(m.animate.shift(LEFT), m.animate.set_color(RED))   # ERRADO
```

Cada builder chama `generate_target()` de novo, e o segundo apaga o alvo do
primeiro. Como as duas animações acabam apontando para o mesmo `m.target` (o do
segundo), **o deslocamento não é animado** — ele só aparece de um salto no
último frame, quando `finish()` reaplica os métodos. **[fonte: derivado de
`_AnimationBuilder.__init__` + `MoveToTarget.__init__` + `_MethodAnimation.finish`;
não executado.]**

A forma certa é um builder só: `self.play(m.animate.shift(LEFT).set_color(RED))`.

### 6.7 `.animate` pode devolver outra animação inteira

Se o método do mobject foi decorado com `@override_animate`, o builder devolve o
que o decorador construiu, e **encadear passa a ser proibido**:

```
NotImplementedError: Method chaining is currently not supported for overridden animations
```

Na biblioteca isso existe em `Graph.add_vertices` / `remove_vertices` /
`add_edges` / `remove_edges` (**[fonte:** `mobject/graph.py:922,1003,1127,1182`**]**)
— então `grafo.animate.add_vertices(...)` é uma animação de verdade e
`grafo.animate.add_vertices(...).shift(UP)` não compila. O irmão desse mecanismo
é `@override_animation(Create)`, usado em `ManimBanner` **[fonte:
`mobject/logo.py:206`]**, e é ele que faz `Animation.__new__` devolver outra
classe. Escrever os seus: `manim-mobjects-customizados`.

### 6.8 Quando NÃO usar `.animate`

| Situação | Use |
|---|---|
| rotação | `Rotate` / `Rotating` |
| o objeto deve seguir um caminho | `MoveAlongPath` |
| trocar por outro objeto | `ReplacementTransform` |
| o método não muda pontos nem cor (`set_z_index`, `set_name`) | nada — `.animate` gera um `run_time` de tela parada |
| o mobject muda de número de submobjects no meio | `Transform` explícito, ou `become` fora do `play` |
| o alvo já foi construído à mão | `Transform(m, alvo)` |

---

## 7. O catálogo — 77 nomes, e 2 deles não são animação

Regenere a lista bruta a qualquer momento:

```bash
awk -F'\t' '$1=="class" && $3 ~ /^animation/ {print $3"\t"$2}' api/manim-ce-index.tsv | sort
```

Conferido em 2026-08-19: **77 classes** nas 14 categorias `animation/*`. Delas,
**75 são animações de verdade** (a base `Animation` + **72** descendentes na
árvore de herança + `FadeIn`/`FadeOut`, que a árvore omite porque a mãe delas,
`_Fade`, é privada — 1 + 72 + 2 = 75, e 77 − 2 = 75). As outras **duas —
`TracedPath` e `AnimatedBoundary` — NÃO são animações**: a árvore as põe sob `VMobject` e `VGroup`. Elas entram com
`self.add(...)`, nunca com `self.play(...)`. Ver §11, defeito nº 1.

```bash
sed -n '/^Animation$/,/^[A-Za-z]/p' api/manim-ce-inheritance.txt   # a árvore inteira
bin/mx show LaggedStart                                            # assinatura + herdados
bin/mx show TransformMatchingTex --own-only
```

### 7.1 Criação e escrita — `animation/creation` (14)

| Classe | Assinatura (kwargs próprios) | Para quê |
|---|---|---|
| `Create` | `(mobject, lag_ratio=1.0, introducer=True)` | desenhar o traço de um `VMobject` |
| `Uncreate` | `(mobject, reverse_rate_function=True, remover=True)` | desfazer o traço |
| `Write` | `(vmobject, rate_func=linear, reverse=False)` | texto e fórmula: contorno depois preenchimento |
| `Unwrite` | `(vmobject, rate_func=linear, reverse=True)` | apagar texto |
| `DrawBorderThenFill` | `(vmobject, run_time=2, rate_func=double_smooth, stroke_width=2, stroke_color=None, introducer=True)` | a mãe de `Write` |
| `ShowPartial` | `(mobject)` | **abstrata** — `_get_bounds` levanta `NotImplementedError`. Use `Create` ou `ShowPassingFlash` |
| `ShowIncreasingSubsets` | `(group, suspend_mobject_updating=False, int_func=np.floor)` | revelar itens de um grupo, um a um, **sem** desenhar traço |
| `ShowSubmobjectsOneByOne` | `(group, int_func=np.ceil)` | um item por vez, os anteriores somem |
| `SpiralIn` | `(shapes, scale_factor=8, fade_in_fraction=0.3)` | entrada em espiral |
| `AddTextLetterByLetter` | `(text, suspend_mobject_updating=False, int_func=np.ceil, rate_func=linear, time_per_char=0.1, run_time=None)` | máquina de escrever |
| `RemoveTextLetterByLetter` | idem, `reverse_rate_function=True, remover=True` | apagar letra a letra |
| `AddTextWordByWord` | `(text_mobject, run_time=None, time_per_char=0.06)` | palavra a palavra — **quebrada na 0.21**: o fonte traz `# TODO, this is broken...` e o docstring diz *"Note: currently broken."* **[fonte: `creation.py:653-655`]**. Não use |
| `TypeWithCursor` | `(text, cursor, buff=0.1, keep_cursor_y=True, leave_cursor_on=True, time_per_char=0.1)` | com cursor piscando |
| `UntypeWithCursor` | `(text, cursor=None, time_per_char=0.1)` | o inverso |

Quatro coisas que só se descobrem lendo o fonte:

- **`Create` só funciona em `VMobject`.** `ShowPartial.__init__` verifica
  `pointwise_become_partial` e levanta
  `TypeError: Create only works for VMobjects`. Um `ImageMobject` precisa de
  `FadeIn`.
- **`Create` tem `lag_ratio=1.0`**, que é *estritamente sequencial*.
  `Create(VGroup(a, b, c))` desenha os três em fila dentro do mesmo `run_time`.
  Para os três ao mesmo tempo: `Create(g, lag_ratio=0)`.
- **`Write` calcula o próprio `run_time`.**
  `run_time = 1 if len(family_members_with_points()) < 15 else 2`, e
  `lag_ratio = min(4 / length, 0.2)` **[fonte:
  `Write._set_default_config_from_length`]**. É a resposta exata para "por que
  esse `Write` dura 2 segundos?" — passe `run_time=` para mandar você.
- **`ShowIncreasingSubsets` e `ShowSubmobjectsOneByOne` escrevem opacidade
  absoluta**: o primeiro faz `set_opacity(1)` nos itens já revelados, o segundo
  faz `set_opacity(0)` nos anteriores e `set_opacity(1)` no atual **[fonte:
  `creation.py:537-539, 645-650`]**. Um grupo desenhado com transparência de
  propósito sai com ela apagada.
- **`SpiralIn` MUTA o mobject no construtor**: ele move cada filho para a
  posição inicial da espiral e chama `save_state()` neles **[fonte:
  `creation.py:451-470`]**. Construir a animação cedo e tocar tarde deixa o
  grupo teleportado no meio-tempo, e o `saved_state` anterior foi perdido.

### 7.2 Aparição e sumiço — `animation/fading` (2) + `animation/growing` (5)

```
FadeIn(*mobjects, shift=None, target_position=None, scale=1, **kwargs)
FadeOut(*mobjects, shift=None, target_position=None, scale=1, **kwargs)
```

**Estes três kwargs não aparecem no índice**, que mostra só
`(*mobjects, **kwargs)` para as duas — eles moram na base privada `_Fade`, que o
índice não lista. É o mesmo efeito do §3: assinatura curta demais quer dizer
"procure na base". Conferido em `manim/animation/fading.py:52-73`.

As duas aceitam **vários mobjects**: `FadeOut(a, b, c)` os embrulha num `Group`
**[fonte: `_Fade.__init__`]**. `FadeOut(*self.mobjects)` é o idioma de limpar a
tela. Sem nenhum mobject, `ValueError: At least one mobject must be passed.`

`shift` desloca durante o fade; `target_position` aponta para um ponto **ou
outro mobject** (usa o centro dele); `scale` é o fator inicial (`FadeIn`) ou
final (`FadeOut`). São o jeito mais barato de dar direção a uma entrada —
`FadeIn(x, shift=UP * 0.3)` é o idioma do deck **[deck]**.

| Classe | Assinatura | Nota |
|---|---|---|
| `GrowFromPoint` | `(mobject, point, point_color=None)` | a base: começa em `scale(0)` no ponto |
| `GrowFromCenter` | `(mobject, point_color=None)` | `point = mobject.get_center()` |
| `GrowFromEdge` | `(mobject, edge, point_color=None)` | `edge` é uma direção (`LEFT`, `DOWN`…) |
| `GrowArrow` | `(arrow, point_color=None)` | cresce da `arrow.get_start()`, com `scale_tips=True` |
| `SpinInFromNothing` | `(mobject, angle=PI/2, point_color=None)` | `GrowFromCenter` + rotação |
| `ShrinkToCenter` | `(mobject)` | é `ScaleInPlace(mobject, 0)` — **não remove nada** |

**Armadilha do `GrowFromEdge`, medida no deck [deck] e confirmada no fonte:** o
estado inicial é `start.scale(0)` — uma escala **uniforme, nos dois eixos**
**[fonte: `growing.py:93-96`]**. Numa barra fina de gráfico, a barra engorda
enquanto avança, e isso lê como defeito de render. O idioma correto para barra
que cresce está em §10.1.

### 7.3 Ênfase — `animation/indication` (9)

**Nenhuma skill deste projeto é dona de "apontar para a coisa".** Enquanto isso
não mudar, o catálogo mora aqui; os *mobjects* de anotação (`Brace`, `BraceLabel`,
`SurroundingRectangle`, `Underline`, `Cross`) são de `manim-mobjects`.

| Classe | Assinatura | Nota |
|---|---|---|
| `Indicate` | `(mobject, scale_factor=1.2, color=PURE_YELLOW, rate_func=there_and_back)` | `Transform` para uma cópia maior e colorida, e volta |
| `Flash` | `(point, line_length=0.2, num_lines=12, flash_radius=0.1, line_stroke_width=3, color=PURE_YELLOW, time_width=1, run_time=1.0)` | **recebe um PONTO**; passando um Mobject usa só o `get_center()` dele — ajuste `flash_radius` à mão |
| `Circumscribe` | `(mobject, shape=Rectangle, fade_in=False, fade_out=False, time_width=0.3, buff=0.1, color=PURE_YELLOW, run_time=1, stroke_width=4)` | é uma `Succession`; `shape=Circle` para circular |
| `FocusOn` | `(focus_point, opacity=0.2, color=GREY, run_time=2)` | um disco do tamanho da tela fecha sobre o ponto; `remover=True` |
| `Wiggle` | `(mobject, scale_value=1.1, rotation_angle=0.0628, n_wiggles=6, scale_about_point=None, rotate_about_point=None, run_time=2)` | chacoalhar |
| `ApplyWave` | `(mobject, direction=UP, amplitude=0.2, wave_func=smooth, time_width=1, ripples=1, run_time=2)` | é um `Homotopy` |
| `Blink` | `(mobject, time_on=0.5, time_off=0.5, blinks=1, hide_at_end=False)` | `Succession` de `UpdateFromFunc` que alterna `set_opacity(1.0)`/`set_opacity(0.0)` **[fonte]** — e por isso **destrói a opacidade de projeto** do mobject: ele termina em 1,0, não no valor que tinha |
| `ShowPassingFlash` | `(mobject, time_width=0.1)` | um pedaço do traço corre pelo caminho |
| `ShowPassingFlashWithThinningStrokeWidth` | `(vmobject, n_segments=10, time_width=0.1, remover=True)` | idem, com traço afinando |

**A armadilha que estraga o vídeo inteiro em tema claro:** `Indicate`, `Flash`,
`Circumscribe` e `SurroundingRectangle` têm `color=PURE_YELLOW` (`#FFFF00`) de
fábrica (`animation/indication.py:156, 229, 621`; `mobject/geometry/shape_matchers.py:53`).
O contraste de `#FFFF00` sobre branco é **1,07:1** [conta WCAG] — o piso teórico
é 1,00. O destaque acontece e **ninguém vê**, sem erro nenhum.

**Correção.** Uma versão anterior desta skill dizia 1,39:1 e creditava a medição
a `manim-color-theming`. O 1,39 é de **outra** cor: `YELLOW` = `#F7D96F`, a da
paleta comum. `PURE_YELLOW` é `#FFFF00`, e é ele que as quatro classes acima
hard-codam. O número certo é pior que o errado, e a conclusão não muda. Passe `color=` sempre, ou resolva de uma vez
no tema com `set_default` (§9).

### 7.4 Movimento — `animation/movement` (5)

| Classe | Assinatura | Nota |
|---|---|---|
| `MoveAlongPath` | `(mobject, path, suspend_mobject_updating=False)` | o **centro** do mobject segue `path.point_from_proportion(rate_func(alpha))`. Não gira para acompanhar a tangente. `path` precisa ser `VMobject` |
| `Homotopy` | `(homotopy, mobject, run_time=3, apply_function_kwargs=None)` | `f(x, y, z, t) -> (x, y, z)` |
| `SmoothedVectorizedHomotopy` | idem | suaviza as curvas depois de deformar |
| `ComplexHomotopy` | `(complex_homotopy, mobject)` | `f(z, t) -> complex` |
| `PhaseFlow` | `(function, mobject, virtual_time=1, suspend_mobject_updating=False, rate_func=linear)` | integra um campo vetorial |

`Homotopy`, `ComplexHomotopy` e `PhaseFlow` fazem parte do assunto "campos e
fluxo", que **não tem skill dona neste projeto** (§12). Aqui ficam a assinatura
e o aviso.

### 7.5 Rotação — `animation/rotation` (2)

```
Rotate(mobject, angle=PI, axis=OUT, about_point=None, about_edge=None, **kwargs)
Rotating(mobject, angle=TAU, axis=OUT, about_point=None, about_edge=None,
         run_time=5, rate_func=linear, **kwargs)
```

Não são a mesma coisa por dentro **[fonte: `animation/rotation.py`]**:

- **`Rotate` é um `Transform`** cujo alvo é a cópia rotacionada, com
  `path_arc=angle` e `path_arc_centers=about_point`. Os pontos viajam pelo arco
  — a rotação parece rotação. Se `about_point` for `None`, ele vira
  `mobject.get_center()` **no construtor** (então mover o mobject depois de
  construir a animação não muda o centro de rotação).
- **`Rotating` recalcula do zero a cada frame**: `become(starting_mobject)` e
  então `rotate(rate_func(alpha) * angle)`. É exato para qualquer ângulo,
  inclusive múltiplas voltas — e é a classe certa para giro contínuo. Default:
  `angle=TAU`, `run_time=5`, `rate_func=linear`.

**Ângulo é sempre em radianos.** `Rotate(m, 90)` são ~14,3 voltas. Use
`90 * DEGREES` ou `PI / 2`.

### 7.6 Números — `animation/numbers` (2)

`ChangingDecimal(decimal_mob, number_update_func, suspend_mobject_updating=False)`
e `ChangeDecimalToValue(decimal_mob, target_number)`. Existem, funcionam, e
**não** são o caminho recomendado: para número que conta, o idioma deste projeto
é `ValueTracker` + `DecimalNumber` com updater — assunto de
`manim-updaters-valuetracker`.

### 7.7 Especializada — `animation/specialized` (1)

`Broadcast(mobject, focal_point=ORIGIN, n_mobs=5, initial_opacity=1,
final_opacity=0, initial_width=0.0, remover=True, lag_ratio=0.2, run_time=3)`
— N cópias do mobject saem do ponto focal crescendo e sumindo (o "ping" de
radar). É um `LaggedStart` por dentro.

### 7.8 Estrutura — `animation/core` (3 classes + 2 funções)

| Nome | Assinatura | Para quê |
|---|---|---|
| `Animation` | ver §3 | a base |
| `Wait` | `(run_time=1, stop_condition=None, frozen_frame=None, rate_func=linear)` | pausa **como animação** — é o que se põe dentro de uma `Succession` |
| `Add` | `(*mobjects, run_time=0.0)` | `scene.add` **como animação**: aparece instantâneo no meio de uma composição |
| `prepare_animation` | `(anim) -> Animation` | converte `.animate` em `Animation`; é o que o `play` chama |
| `override_animation` | `(animation_class) -> decorator` | registra um substituto de classe inteira — `manim-mobjects-customizados` |

`Add(m, run_time=0.2)` é o idioma para "adiciona e espera um pouco" dentro de
uma `Succession`, sem gastar um `Wait` separado **[fonte: docstring de `Add`]**.

### 7.9 Composição, ritmo e velocidade — NÃO é aqui

`AnimationGroup`, `Succession`, `LaggedStart`, `LaggedStartMap`, `ChangeSpeed`,
as 49 `rate_function` e os 6 `path_func` são de **`manim-composicao-ritmo`**.
Duas notas de fronteira que pertencem a este catálogo:

- `Flash`, `Broadcast` e `ShowPassingFlashWithThinningStrokeWidth` **são**
  `AnimationGroup`; `Circumscribe` e `Blink` **são** `Succession`. Passar
  `run_time=` para elas funciona: `AnimationGroup.interpolate` reescala os
  tempos internos contra `max_end_time` **[fonte: `composition.py`]**.
- `AnimationGroup` tem `rate_func=linear` de fábrica, e não `smooth` — de
  propósito, para não empilhar duas curvas de suavização sobre as animações
  filhas.

### 7.10 Updaters — `animation/updaters` (3 classes)

`UpdateFromFunc(mobject, update_function, suspend_mobject_updating=False)`,
`UpdateFromAlphaFunc(...)` e `MaintainPositionRelativeTo(mobject, tracked_mobject)`.
São animações de verdade e entram no `play`. O resto do módulo (`always_redraw`,
`always_rotate`, `f_always`, `turn_animation_into_updater`,
`cycle_animation`) é de `manim-updaters-valuetracker`.

---

## 8. A família `Transform` — 24 classes, uma mecânica

Assinatura completa da base:

```
Transform(mobject, target_mobject=None, path_func=None, path_arc=0,
          path_arc_axis=OUT, path_arc_centers=None,
          replace_mobject_with_target_in_scene=False, **kwargs)
```

### 8.1 `Transform` × `ReplacementTransform` × `TransformFromCopy`

```python
self.play(Transform(a, b))
# `a` continua na cena, com a APARÊNCIA de `b`. `b` nunca entrou.
# Animar `b` depois disso não faz nada. Continue mexendo em `a`.

self.play(ReplacementTransform(a, b))
# `a` sai, `b` entra (via scene.replace, preservando a ordem de desenho).
# Continue mexendo em `b`.

self.play(TransformFromCopy(a, b))
# `a` fica INTACTO. `b` entra nascendo com a cara de `a` e virando `b`.
```

`ReplacementTransform.__init__` é literalmente
`super().__init__(mobject, target_mobject, replace_mobject_with_target_in_scene=True)`
**[fonte: `transform.py:301`]**. Nada mais.

`TransformFromCopy` é mais esperto do que parece: ele chama
`Transform.__init__(target_mobject, mobject)` — **os argumentos invertidos** — e
sobrescreve `interpolate(alpha)` com `super().interpolate(1 - alpha)` **[fonte:
`transform.py:307-314`]**. Duas consequências que aparecem no vídeo:

- o mobject animado é o **alvo**, e a origem nunca é tocada;
- **no alfa 0 a cópia é opaca e está exatamente em cima da origem.** Num vídeo
  contínuo isso dura 1/60 s e ninguém vê. Num vídeo **cortado em partes**, esse
  é o frame parado em que o apresentador fala — e o que estava atrás some.
  **[deck]** Foi assim que se achou o defeito: nunca corte imediatamente antes
  de um `TransformFromCopy` que atravessa o que já está na tela. Detalhe e
  medição em `manim-presentation-parts`.

Quando em dúvida entre os dois primeiros, use `ReplacementTransform` — é o que
corresponde à intuição, e é o único que deixa a cena com o objeto que você acha
que está lá.

### 8.2 `Transform.begin()` muda a estrutura do seu mobject

```python
self.target_mobject = self.create_target()
self.target_copy = self.target_mobject.copy()
self.mobject.align_data(self.target_copy)      # <-- aqui
```

O comentário no fonte é explícito: *"Note, this potentially changes the structure
of both mobject and target_mobject"* **[fonte: `transform.py:199-206`]**. Para
interpolar ponto a ponto, as duas famílias precisam ter o mesmo número de
submobjects e de pontos, e `align_data` **acrescenta submobjects vazios** onde
falta.

Consequências reais:

- depois de `Transform(a, b)`, `len(a.submobjects)` pode ter mudado, e `a[3]`
  pode não ser mais o que era;
- um `VGroup` que você indexava por posição vira uma bomba-relógio;
- `Transform.get_all_families_zipped` usa `zip(..., strict=True)` — se a
  estrutura divergir **depois** do `begin` (um updater que acrescenta filhos, por
  exemplo), o erro é um `ValueError` do `zip`, sem menção ao Manim.

A cura: guarde referências nomeadas para as peças (o idioma de `_pasta()` do
deck, que devolve `(grupo, moldura, linhas, selo)`), em vez de indexar
`grupo[0][2]` **[deck]**.

### 8.3 `create_target()` roda no `begin()`, não no construtor

É o que torna este idioma possível:

```python
anim = Transform(a, b)     # nada foi copiado ainda
b.shift(UP)                # ainda dá tempo
self.play(anim)            # o alvo é o b deslocado
```

E é também o que faz `MoveToTarget` funcionar sem gambiarra.

### 8.4 `path_arc`, `path_func`, `path_arc_centers` — a precedência

Os três controlam **por onde** os pontos viajam. A ordem de precedência, lida do
construtor **[fonte: `transform.py:147-158`]**: `path_func` > `path_arc_centers`
> `path_arc`. O `path_arc` é aplicado primeiro pelo *setter* da property (que
monta um `path_along_arc`), e é sobrescrito se qualquer um dos outros dois vier.

```python
self.play(Transform(a, b, path_arc=PI / 2))    # sai pela curva
self.play(sq.animate(path_arc=-PI).shift(RIGHT * 3))
```

`ClockwiseTransform` e `CounterclockwiseTransform` são exatamente
`Transform(..., path_arc=-PI)` e `path_arc=+PI`. O catálogo dos `path_func`
(`straight_path`, `spiral_path`, `path_along_circles`…) é de
`manim-composicao-ritmo`.

### 8.5 `MoveToTarget` e `generate_target`

```python
c = Circle()
c.generate_target()                       # cria c.target, uma cópia
c.target.set_fill(GREEN, opacity=0.5)
c.target.shift(2 * RIGHT + UP).scale(0.5)
self.add(c)
self.play(MoveToTarget(c))
```

Sem `generate_target()` antes:
`ValueError: MoveToTarget called on mobject without attribute 'target'`
(a mensagem no fonte vem sem espaço: `"mobjectwithout"` — útil para procurar).

É o idioma para quando o alvo é **complicado de descrever numa linha**. Para
alvos simples, `.animate` é menos código. Lembre do §6.5: os dois não se
misturam.

### 8.6 `Restore` e `save_state`

```python
sq.save_state()
self.play(sq.animate.scale(3).set_color(RED).shift(UP * 2))
self.play(Restore(sq))          # volta ao estado salvo
```

Por dentro, `Restore(mobject)` é `ApplyMethod(mobject.restore)` **[fonte:
`transform.py:620`]**, e `Mobject.restore()` é `self.become(self.saved_state)`.
Três armadilhas que saem daí:

- **`save_state` guarda UM estado só.** Um segundo `save_state()` sobrescreve o
  primeiro (o fonte até zera o anterior antes, "to prevent exponential growth of
  data").
- **Sem ter salvo**, `Exception: Trying to restore without having saved` — uma
  `Exception` crua, não uma exceção do Manim.
- **`restore` usa `become`**, que substitui pontos *e* estrutura de submobjects.
  Se você acrescentou filhos ao mobject depois do `save_state`, o `Restore` os
  apaga.

### 8.7 `TransformMatchingTex` e `TransformMatchingShapes`

```
TransformMatching*(mobject, target_mobject, transform_mismatches=False,
                   fade_transform_mismatches=False, key_map=None, **kwargs)
```

As duas herdam de `TransformMatchingAbstractBase`, que faz um dicionário
`chave -> pedaços` dos dois lados e monta a animação em três pilhas: o que casa
vira `Transform`, o que você mapeou à mão em `key_map` vira
`FadeTransformPieces`, e o que sobra vira `FadeOut` + `FadeIn` (ou `Transform`,
se `transform_mismatches=True`) **[fonte: `transform_matching_parts.py:86-140`]**.

A diferença está só na **chave**:

| Classe | `get_mobject_key` | `get_mobject_parts` |
|---|---|---|
| `TransformMatchingTex` | `mobject.tex_string` (uma string) | os submobjects de cada parte, com `assert hasattr(mobject, "tex_string")` |
| `TransformMatchingShapes` | hash dos pontos **normalizados** (centrado, altura 1, arredondado em 3 casas) | `family_members_with_points()` |

Quatro consequências:

- **`TransformMatchingTex` só funciona em `Tex`/`MathTex`.** Num `Text` o
  `assert` falha. Para texto simples, `TransformMatchingShapes`.
- **Chaves duplicadas são AGRUPADAS.** `shape_map[key].add(sm)` põe todos os
  pedaços com a mesma chave num `VGroup` só. Se `x` aparece três vezes na
  fórmula, os três `x` viram um grupo e se movem juntos — é a origem de "todos
  os meus `x` foram para o mesmo lugar". A cura é cortar a fórmula com
  `substrings_to_isolate` / `{{ }}` (assunto de `manim-text-latex`) e usar
  `key_map` para desempatar.
- **`TransformMatchingShapes` casa por forma normalizada**: duas cópias do mesmo
  símbolo em tamanhos diferentes casam; uma versão rotacionada não casa.
- **O que fica na cena é o alvo.** `clean_up_from_scene` interpola tudo de volta
  a 0, remove a origem e a cópia de fade, e adiciona o `target_mobject`. Ou seja,
  comporta-se como `ReplacementTransform`.

### 8.8 `FadeTransform` × `Transform`

`FadeTransform(mobject, target_mobject, stretch=True, dim_to_match=1)` funde por
**opacidade cruzada com escala**, em vez de interpolar ponto a ponto. É a escolha
quando as duas formas não têm nada a ver uma com a outra (um retângulo virando um
texto), porque a interpolação ponto a ponto entre formas dissimilares produz um
borrão. `FadeTransformPieces` faz o mesmo submobject a submobject.

### 8.9 `ApplyMethod` e os `Apply*`

| Classe | Assinatura | Nota |
|---|---|---|
| `ApplyMethod` | `(method, *args, **kwargs)` | recebe o **método ligado**: `ApplyMethod(sq.shift, RIGHT)`. Passar `sq.shift(RIGHT)` (já chamado) dá `ValueError: Whoops, looks like you accidentally invoked the method you want to animate` |
| `ApplyFunction` | `(function, mobject)` | a função recebe uma **cópia** e precisa **devolver um Mobject**, senão `TypeError` |
| `ApplyPointwiseFunction` | `(function, mobject, run_time=3.0)` | a função recebe e devolve um **ponto** (`np.array` de 3) |
| `ApplyPointwiseFunctionToCenter` | `(function, mobject)` | idem, aplicada só ao centro |
| `ApplyMatrix` | `(matrix, mobject, about_point=ORIGIN)` | matriz 2×2 ou 3×3; fora disso, `ValueError: Matrix has bad dimensions` |
| `ApplyComplexFunction` | `(function, mobject)` | plano complexo |
| `FadeToColor` | `(mobject, color)` | `ApplyMethod(mob.set_color, color)` |
| `ScaleInPlace` | `(mobject, scale_factor)` | |
| `ShrinkToCenter` | `(mobject)` | `ScaleInPlace(m, 0)` |
| `Restore` | `(mobject)` | §8.6 |
| `MoveToTarget` | `(mobject)` | §8.5 |
| `CyclicReplace` | `(*mobjects, path_arc=PI/2)` | cada um vai para o lugar do próximo |
| `Swap` | `(*mobjects, path_arc=PI/2)` | alias de `CyclicReplace` (sem corpo próprio) |
| `TransformAnimations` | `(start_anim, end_anim, rate_func=squish_rate_func(...))` | o fonte a marca com `# TODO, this may be deprecated...` — **evite** |

**Correção a uma afirmação que circulava nesta própria skill:** `ApplyMethod`
**não está depreciada**. Não há `@deprecated` em lugar nenhum de `manim/animation/`
— a única ocorrência da palavra no módulo inteiro é o comentário `# TODO` sobre
`TransformAnimations` **[fonte: `grep -rn deprecated manim/animation/`]**. O que
é verdade é que ela não é idiomática: `.animate` cobre o mesmo terreno.

---

## 9. `Animation.set_default` — o gancho de tema que quase ninguém usa

Existe, é `classmethod`, e é o irmão exato de `VMobject.set_default`:

```python
Rotate.set_default(run_time=2, rate_func=rate_functions.linear)
Indicate.set_default(color=ACENTO)
Circumscribe.set_default(color=ACENTO)
Flash.set_default(color=ACENTO)

Rotate.set_default()        # sem kwargs: RESTAURA o __init__ original
```

Por dentro é `cls.__init__ = partialmethod(cls.__init__, **kwargs)`, e o reset é
`cls.__init__ = cls._original__init__`, guardado por `__init_subclass__` no
momento em que a classe é definida **[fonte: `animation.py:494-540`]**. O
exemplo com `Indicate.set_default(color=…)` está na documentação da própria
biblioteca.

**Isto é a cura de projeto para o amarelo invisível do §7.3**: três linhas no
`tema.py` resolvem o deck inteiro, em vez de repetir `color=` em cada chamada.
Ver `manim-tema-projeto` e `manim-color-theming §11`.

**A armadilha, e é a mesma do tema de cor:** `set_default` muta a **classe**, que
é global ao processo. Num lote que renderiza várias cenas no mesmo interpretador
(`mx render` com várias cenas, `tools/batch_render.py` dentro de um worker), o
default vaza da cena A para a cena B. Se você usar `set_default`, chame-o no
`setup()` da sua cena-base — não no topo do módulo. `manim-color-theming §12`
documenta o mesmo vazamento do lado da cor.

---

## 10. Idiomas verificados em produção

Os três primeiros vêm do deck `~/Projects/aulas`, que roda este projeto em
produção. Marcados **[deck]** onde a medição foi lá.

### 10.1 Barra que cresce: `save_state` + `stretch` + `Restore`

```python
def _prepara_horizontal(barra: Rectangle) -> None:
    borda = barra.get_left()
    barra.save_state()                 # guarda o estado FINAL
    barra.stretch_to_fit_width(0.02)   # encolhe SÓ no eixo do crescimento
    barra.next_to(borda, RIGHT, buff=0)

# depois, no construct:
self.play(Restore(barra, rate_func=SAIDA))
```

**Por que não `GrowFromEdge`:** ele parte de `scale(0)`, uma escala uniforme nos
dois eixos **[fonte: `growing.py:95`]** — a barra engorda enquanto avança, e numa
barra fina isso lê como bug de render **[deck]**. Este idioma toca só o eixo que
deve crescer. Vale igual para `stretch_to_fit_height` + `get_bottom()`.

Assinaturas conferidas: `Mobject.save_state() -> Self`,
`Mobject.stretch_to_fit_width(width, **kwargs) -> Self`, `Restore(mobject, **kwargs)`.

### 10.2 A informação velha sai ANTES de a nova entrar

```python
self.play(FadeOut(rodape_antigo, run_time=0.3))
self.play(FadeIn(rodape_novo, run_time=0.4))
```

Não no mesmo `self.play`: no crossfade os dois se cruzam em meia opacidade e o
palco **pisca** **[deck]**. Vale para qualquer troca de texto de apoio. Em cena
cortada em partes há uma regra a mais — uma parte não troca o rodapé no meio —
e ela é de `manim-presentation-parts`.

### 10.3 Limpar a tela

```python
self.play(FadeOut(*self.mobjects))
```

`FadeOut` aceita vários mobjects e os agrupa **[fonte: `_Fade.__init__`]**. E como
`FadeOut.clean_up_from_scene` chama `interpolate(0)`, cada mobject volta ao estado
original — pode ser reusado num `FadeIn` depois, sem `set_opacity(1)` na mão.

### 10.4 Prato opaco atrás de texto que cruza uma linha de grade

```python
prato = Rectangle(width=texto.width + 0.22, height=texto.height + 0.16,
                  fill_color=CANVAS, fill_opacity=1.0, stroke_width=0.0
                  ).move_to(texto.get_center())
grupo = VGroup(prato, texto)     # prato ANTES do texto
```

Não é animação, mas é onde o defeito aparece: num frame de repouso, o tracejado
da grade atravessando a palavra lê como "texto quebrado". A correção não é mover
o número **[deck]**.

---

## 11. Armadilhas — a lista consolidada

**1. `TracedPath` e `AnimatedBoundary` NÃO são animações.** A árvore de herança
as põe sob `VMobject` e `VGroup`, não sob `Animation`. `self.play(TracedPath(...))`
dá `TypeError: Object … cannot be converted to an animation`. Entram com
`self.add(...)`. Uso correto e completo em `manim-updaters-valuetracker`.

**2. `.animate.rotate()` deforma.** Interpolação em linha reta ponto a ponto. Use
`Rotate` (§7.5). O mesmo defeito, disfarçado, em `.animate.arrange()`.

**3. `.animate` encadeado interpola o resultado FINAL**, não cada passo. Para
passos distintos e visíveis, dois `self.play` ou uma `Succession`.

**4. Dois `.animate` do mesmo mobject no mesmo `play`** perdem a animação do
primeiro (§6.6). Um builder só.

**5. `.animate` apaga `mob.target`** (§6.5). Não misture com `MoveToTarget`.

**6. `Transform` deixa o alvo fora da cena** e continua com a origem (§8.1). É a
causa de "eu animei `b` e não aconteceu nada".

**7. `Transform` muda a estrutura de submobjects da origem** via `align_data`
(§8.2). Índices guardados antes podem apontar para outra coisa depois.

**8. O `run_time` do `play` sobrescreve o das animações** (§4). Passe os tempos
por animação e **não** repita o kwarg no `play`.

**9. `Create` só funciona em `VMobject`.** `ImageMobject` precisa de `FadeIn`.

**10. `Create(VGroup(...))` é sequencial** — `lag_ratio=1.0` de fábrica. Para
simultâneo, `lag_ratio=0`.

**11. `Write` dura 2 s sozinho** em texto com ≥ 15 elementos com pontos (§7.1).

**12. `Indicate`/`Flash`/`Circumscribe`/`SurroundingRectangle` são
`PURE_YELLOW` (`#FFFF00`) de fábrica** — **1,07:1** sobre branco, invisível em
tema claro (não confunda com `YELLOW` `#F7D96F`, que mede 1,39:1). `set_default` no tema (§9).

**13. `ShrinkToCenter` não remove nada.** O mobject fica na cena com escala ~0 —
e volta a aparecer se algo o reescalar depois.

**14. `SpiralIn` teleporta o mobject já no construtor** e clobbera o
`saved_state` dele (§7.1).

**15. `Rotate(m, 90)` são 14 voltas.** Radianos sempre: `90 * DEGREES`.

**16. Os updaters do mobject animado ficam suspensos durante o `play`.**
`suspend_mobject_updating=False` para reativar (§3).

**17. `self.wait()` congela o frame** se nenhum mobject tiver updater
**time-based** (§4).

**18. `Restore` usa `become`** e apaga submobjects acrescentados depois do
`save_state` (§8.6).

**19. `TransformMatchingTex` agrupa chaves repetidas** — todos os `x` iguais
viajam juntos (§8.7).

**20. Nunca corte uma parte de vídeo imediatamente antes de um
`TransformFromCopy`** que atravessa o que já está na tela: o primeiro frame da
parte seguinte é a cópia opaca em cima do original (§8.1) **[deck]**.

**21. Cena "engasgada"**: `run_time` curto demais para o FPS. Em 15 fps (`-q l`),
`run_time=0.1` dá **um frame e meio**. Avalie ritmo em `-q m` no mínimo — e
lembre que `manim-project` mediu que `-r` sobrescreve a resolução mas **não** o
FPS, que continua vindo do `-q` (`-q l -r 1280x720` grava em `720p15`).

**22. Renderizou e não olhou = não terminou.** Nenhum dos defeitos 9, 12, 13 e 20
aparece no exit code. O ciclo (escrever → render rápido → **olhar o PNG** →
corrigir → render final) é de `manim-verificacao-visual`.

---

## 12. Onde esta skill para

| Assunto | Skill dona |
|---|---|
| `rate_func` (as 49), `path_func` (os 6), `AnimationGroup`, `Succession`, `LaggedStart`, `LaggedStartMap`, `ChangeSpeed`, `lag_ratio` de composição, orçamento de segundos | **`manim-composicao-ritmo`** |
| `ValueTracker`, updaters, `always_redraw`, `TracedPath`, `AnimatedBoundary`, `DecimalNumber`, contador que conta | **`manim-updaters-valuetracker`** |
| criar formas, `VGroup` × `Group`, submobjects, `Brace`, `SurroundingRectangle` | **`manim-mobjects`** |
| posicionar, medir, "cabe na tela?", `z_index` | **`manim-layout-posicionamento`** |
| escrever uma `Animation` própria, `interpolate_mobject`, `override_animation`, `override_animate` | **`manim-mobjects-customizados`** |
| escolher a classe de texto, `t2c`, `{{ }}`, `substrings_to_isolate` (o que faz `TransformMatchingTex` funcionar) | **`manim-text-latex`** |
| cor, contraste, fundo, `set_default` de cor | **`manim-color-theming`** |
| o `tema.py` como contrato do projeto (onde mora o `set_default` de animação) | **`manim-tema-projeto`** |
| cortar a cena em partes para slide, emenda, `next_section` | **`manim-presentation-parts`** |
| olhar o PNG, conferir que nada sumiu | **`manim-verificacao-visual`** |
| qualidade, formato, caminho do arquivo, `-q`/`-r`/`--fps` | **`manim-render-api`** |
| descobrir se um nome existe, assinatura, kwarg | **`manim-api-discovery`** |
| `ApplyMatrix` num contexto de álgebra linear (`LinearTransformationScene`, `VectorScene`) | **órfão** — não existe skill; aqui está só a assinatura |
| `Homotopy`, `PhaseFlow`, `ComplexHomotopy`, campos e fluxo | **órfão** — idem |
| ênfase e anotação como assunto (não como catálogo) | **órfão** — o catálogo de `animation/indication` ficou aqui (§7.3) |
