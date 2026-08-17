---
name: manim-animations
description: >-
  Animar no Manim — a lista completa de classes de animação, a sintaxe
  `.animate`, controle de tempo (`run_time`, `lag_ratio`, `rate_func`),
  composição (`AnimationGroup`, `Succession`, `LaggedStart`), transformações
  entre objetos, e o fluxo `self.play` / `self.wait`. Use ao criar qualquer
  movimento, transição, aparição ou destaque; ao sincronizar várias
  animações; ao ajustar ritmo/duração; ou quando a animação sair
  instantânea, engasgada, na ordem errada, ou não acontecer.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Animações

## O modelo mental

Uma `Animation` recebe o estado inicial de um Mobject e interpola até um
estado final, dentro de `run_time` segundos. Nada anima até você passar por
`self.play`.

```python
self.play(Create(c))                       # uma
self.play(Create(c), Write(t))             # simultâneas
self.play(Create(c), run_time=2)           # duração
self.wait(1.5)                             # pausa
self.add(c)                                # sem animação, instantâneo
```

## `.animate` — o caminho idiomático

Qualquer método que muda o Mobject pode virar animação:

```python
self.play(sq.animate.shift(RIGHT * 2))
self.play(sq.animate.set_color(RED).scale(1.5).rotate(PI / 4))
self.play(a.animate.shift(LEFT), b.animate.shift(RIGHT))
```

`.animate` **interpola entre o estado antes e o estado depois**, não replica
o caminho do método. Consequência real: `.animate.rotate(PI)` interpola em
linha reta do começo ao fim e o objeto parece encolher e crescer. Para
rotação de verdade use a classe:

```python
self.play(Rotate(sq, PI))          # gira de verdade
self.play(sq.animate.rotate(PI))   # interpola direto: parece errado
```

## Catálogo completo (ManimCE 0.21)

Regenere com:
```bash
awk -F'\t' '$1=="class" && $3 ~ /^animation/ {print $3"\t"$2}' api/manim-ce-index.tsv | sort
```

**Criação** — `Create` `Uncreate` `Write` `Unwrite` `DrawBorderThenFill`
`ShowPartial` `ShowIncreasingSubsets` `ShowSubmobjectsOneByOne` `SpiralIn`
`AddTextLetterByLetter` `RemoveTextLetterByLetter` `TypeWithCursor`
`UntypeWithCursor` `AddTextWordByWord`

**Aparição** — `FadeIn` `FadeOut` `GrowFromCenter` `GrowFromEdge`
`GrowFromPoint` `GrowArrow` `SpinInFromNothing` `ShrinkToCenter`

**Transformação** — `Transform` `ReplacementTransform` `TransformFromCopy`
`TransformMatchingTex` `TransformMatchingShapes` `FadeTransform`
`FadeTransformPieces` `ClockwiseTransform` `CounterclockwiseTransform`
`ApplyFunction` `ApplyMatrix` `ApplyComplexFunction`
`ApplyPointwiseFunction` `CyclicReplace` `Swap` `FadeToColor`
`ScaleInPlace` `Restore` `MoveToTarget` `ApplyMethod` *(depreciada — use
`.animate`)*

**Destaque** — `Indicate` `Flash` `FocusOn` `Circumscribe` `Wiggle`
`ApplyWave` `ShowPassingFlash` `ShowPassingFlashWithThinningStrokeWidth`
`Blink`

**Movimento** — `MoveAlongPath` `Homotopy` `SmoothedVectorizedHomotopy`
`ComplexHomotopy` `PhaseFlow` `Rotate` `Rotating`

**Números** — `ChangingDecimal` `ChangeDecimalToValue`

**Composição** — `AnimationGroup` `Succession` `LaggedStart`
`LaggedStartMap`

**Updaters** — `UpdateFromFunc` `UpdateFromAlphaFunc`
`MaintainPositionRelativeTo`

**Outras** — `ChangeSpeed` `Broadcast` `TracedPath` `AnimatedBoundary`
`Wait` `Add`

Detalhe de qualquer uma:

```bash
bin/mx show LaggedStart
bin/mx show TransformMatchingTex --own-only
```

## Composição

```python
# tudo junto
self.play(AnimationGroup(Create(a), Write(b)))

# uma depois da outra, dentro de um play só
self.play(Succession(Create(a), Write(b), FadeIn(c)))

# em cascata — o mais usado para listas e grupos
self.play(LaggedStart(*[FadeIn(m) for m in grupo], lag_ratio=0.2))

# cascata aplicando a mesma animação a cada membro
self.play(LaggedStartMap(FadeIn, grupo, lag_ratio=0.1))
```

`lag_ratio` controla a sobreposição: `0` = simultâneo, `1` = estritamente
sequencial, `0.1–0.3` = a cascata que fica boa na maioria dos casos.

## Ritmo — `rate_func`

```python
from manim import *
self.play(sq.animate.shift(RIGHT), rate_func=smooth)        # padrão
self.play(sq.animate.shift(RIGHT), rate_func=linear)
self.play(sq.animate.shift(RIGHT), rate_func=there_and_back)
self.play(sq.animate.shift(RIGHT), rate_func=rush_into)
self.play(sq.animate.shift(RIGHT), rate_func=ease_in_out_quad)
```

Todas as disponíveis:

```bash
awk -F'\t' '$3=="utils/rate_functions" {print $2}' api/manim-ce-index.tsv | sort -u
```

Úteis com frequência: `smooth` `linear` `rush_into` `rush_from`
`slow_into` `there_and_back` `there_and_back_with_pause` `wiggle`
`exponential_decay` `ease_in_sine` `ease_out_bounce` `ease_in_out_expo`.

Combinadores:

```python
rate_func=lambda t: smooth(t) ** 2
rate_func=squish_rate_func(smooth, 0.3, 0.7)   # só age no meio da janela
```

## Timing e sincronização

```python
self.play(A, run_time=3)
self.play(A, B, run_time=2)                      # ambas em 2s
self.play(Succession(A, B), run_time=4)          # 2s cada

# durações diferentes na mesma chamada
self.play(
    AnimationGroup(
        Create(a, run_time=1),
        Write(b, run_time=3),
        lag_ratio=0,
    )
)

# atraso
self.play(FadeIn(a), FadeIn(b, rate_func=squish_rate_func(smooth, 0.5, 1)))
```

Duração de uma cena = soma dos `run_time` + soma dos `wait`. `self.wait()`
sem argumento espera 1 s.

## `Transform` vs `ReplacementTransform`

```python
self.play(Transform(a, b))
# `a` continua na cena, com a APARÊNCIA de `b`. `b` nunca entrou.
# Animar `b` depois disso não faz nada. Continue mexendo em `a`.

self.play(ReplacementTransform(a, b))
# `a` sai, `b` entra. Continue mexendo em `b`.
```

Quando em dúvida, use `ReplacementTransform` — é o que corresponde à
intuição.

## `save_state` / `Restore`

```python
sq.save_state()
self.play(sq.animate.scale(3).set_color(RED).shift(UP * 2))
self.wait()
self.play(Restore(sq))       # volta ao estado salvo
```

## Animar em cima de dados que mudam

Para valores que evoluem (contadores, gráficos que se redesenham), a
ferramenta é `ValueTracker` + updaters — ver a skill
`manim-updaters-valuetracker`.

## Armadilhas

- **A animação não acontece**: você esqueceu `self.play`, ou usou
  `self.add`, ou o objeto já estava no estado final.
- **`.animate.rotate()` deforma**: use a classe `Rotate`.
- **`.animate` com vários métodos encadeados interpola o resultado final**,
  não cada passo. Para passos distintos, use `Succession`.
- **`Transform` deixa o alvo fora da cena** — ver acima.
- **`VGroup` anima como um objeto só.** Para cascata, use `LaggedStart`.
- **Ângulo em radianos** sempre. `Rotate(m, 90)` são ~14 voltas.
- **`ApplyMethod` está depreciada.** Existe no índice, mas escreva
  `.animate`.
- **Cena "engasgada"**: `run_time` muito curto para o FPS. Em 15 fps
  (`-q l`), `run_time=0.1` dá ~1 frame. Teste o ritmo em `-q m` no mínimo.
