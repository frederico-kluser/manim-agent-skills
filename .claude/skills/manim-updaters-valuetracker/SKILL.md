---
name: manim-updaters-valuetracker
description: >-
  Animação reativa no Manim — ValueTracker, updaters (add_updater,
  always_redraw), DecimalNumber/Integer para contadores, e objetos que se
  redesenham em função de um valor que muda. Use quando um elemento precisa
  SEGUIR outro, quando um número precisa contar/variar na tela, quando uma
  curva ou reta precisa se redesenhar continuamente, ou quando uma animação
  precisa depender de estado em vez de um alvo fixo. Também cobre por que
  updaters "param de funcionar" ou travam a renderização.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Updaters e ValueTracker — animação reativa

## Quando você precisa disto

Animações normais interpolam de um estado A para um estado B, ambos
conhecidos de antemão. Quando o alvo **depende de algo que muda durante a
animação**, `self.play(Transform(...))` não resolve. Aí entram os updaters.

Sintomas de que é este o caso: "a etiqueta tem que seguir o ponto", "o
número tem que contar", "a reta tangente tem que acompanhar o x", "a barra
tem que refletir o valor".

## `ValueTracker` — um número animável

```python
t = ValueTracker(0)

t.get_value()            # lê
t.set_value(5)           # escreve (instantâneo)
t.increment_value(1)
self.play(t.animate.set_value(10), run_time=3)   # anima o número
```

`ValueTracker` é um Mobject invisível. Ele existe só para carregar um
`float` que a animação consegue interpolar.

Também existe `ComplexValueTracker` para números complexos.

## `always_redraw` — reconstrói a cada frame

A forma mais legível. Passe uma função sem argumentos que **cria** o
objeto:

```python
x = ValueTracker(0)

ponto = always_redraw(lambda: Dot(ax.c2p(x.get_value(), f(x.get_value()))))
linha = always_redraw(lambda: ax.get_vertical_line(ponto.get_center()))

self.add(ponto, linha)
self.play(x.animate.set_value(5), run_time=4)
```

`always_redraw(f)` é açúcar para `f().add_updater(lambda m: m.become(f()))`.
Ele **descarta e recria** o mobject a cada frame — simples, mas caro.

## `add_updater` — modifica em vez de recriar

Mais eficiente quando você só precisa mover/ajustar:

```python
etiqueta = Text("aqui")
etiqueta.add_updater(lambda m: m.next_to(alvo, UP))
self.add(etiqueta)

self.play(alvo.animate.shift(RIGHT * 4))

etiqueta.clear_updaters()          # sempre limpe quando terminar
```

Com `dt` (tempo desde o frame anterior) para movimento contínuo:

```python
girando = Square()
girando.add_updater(lambda m, dt: m.rotate(dt * PI))   # meia volta/segundo
self.add(girando)
self.wait(4)
girando.clear_updaters()
```

A assinatura decide o comportamento: `lambda m:` roda a cada frame;
`lambda m, dt:` recebe também o delta de tempo. Use `dt` para velocidade
constante independente do FPS.

Gerenciamento:

```python
mob.add_updater(f)
mob.remove_updater(f)
mob.clear_updaters()
mob.suspend_updating()
mob.resume_updating()
mob.get_updaters()
```

## Contadores numéricos

```python
n = DecimalNumber(0, num_decimal_places=2, include_sign=False)
t = ValueTracker(0)
n.add_updater(lambda m: m.set_value(t.get_value()))
self.add(n)
self.play(t.animate.set_value(99.9), run_time=3)
```

Alternativas prontas:

```python
Integer(0)
DecimalNumber(3.14159, num_decimal_places=3, unit=r"\text{m}")
self.play(ChangeDecimalToValue(n, 100), run_time=2)
```

`Integer` e `DecimalNumber` recriam os glifos a cada mudança — em contagens
longas isso é o gargalo. Reduza `num_decimal_places` se estiver lento.

## Padrão completo: tangente que corre pela curva

```python
from manim import *

class Tangente(Scene):
    def construct(self):
        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 9, 2], x_length=10, y_length=5)
        f = ax.plot(lambda x: x**2, color=BLUE)
        self.add(ax, f)

        x = ValueTracker(-2.5)

        ponto = always_redraw(lambda: Dot(ax.i2gp(x.get_value(), f), color=YELLOW))
        tang  = always_redraw(lambda: ax.get_secant_slope_group(
            x=x.get_value(), graph=f, dx=0.001,
            secant_line_color=YELLOW, secant_line_length=4))
        lbl   = always_redraw(lambda: MathTex(
            f"f'({x.get_value():.2f}) = {2 * x.get_value():.2f}"
        ).to_corner(UL))

        self.add(ponto, tang, lbl)
        self.play(x.animate.set_value(2.5), run_time=5, rate_func=linear)
        self.wait()
```

## Outros mecanismos reativos

```python
# atualizar via função explícita, com controle do alpha da animação
self.play(UpdateFromAlphaFunc(mob, lambda m, a: m.set_opacity(a)))
self.play(UpdateFromFunc(mob, lambda m: m.next_to(alvo, UP)))

# manter posição relativa durante uma animação
self.play(MoveAlongPath(dot, caminho),
          MaintainPositionRelativeTo(lbl, dot))

# rastro deixado por um objeto
rastro = TracedPath(dot.get_center, stroke_color=YELLOW, stroke_width=3)
self.add(rastro)

# contorno animado
self.add(AnimatedBoundary(sq, colors=[RED, BLUE], cycle_rate=2))
```

## Updaters de cena (não ligados a um mobject)

```python
self.add_updater(lambda dt: print(self.renderer.time))
```

## Armadilhas

- **Updater não roda porque o objeto não está na cena.** `always_redraw`
  devolve um mobject; ele precisa de `self.add(...)`. Este é o erro nº 1.
- **Esqueceu `clear_updaters()`** e o objeto continua se mexendo nas
  animações seguintes — costuma aparecer como "a etiqueta grudou".
- **Updater + `self.play(mob.animate...)` no mesmo mobject** brigam entre
  si: o updater sobrescreve a interpolação a cada frame. Suspenda o updater
  ou anime só o `ValueTracker`.
- **Referência a variável de loop** dentro do lambda captura a variável, não
  o valor. Use `lambda m, i=i: ...`.
- **`always_redraw` é caro**: recria o mobject a cada frame. Em `MathTex`
  isso significa recompilar/reposicionar 60×/s. Prefira `add_updater` com
  `set_value` quando só o número muda.
- **`ValueTracker` sozinho não anima nada.** Ele precisa de alguém lendo o
  valor via updater.
- **`dt` só chega se o lambda tiver dois parâmetros.** `lambda m: m.rotate(0.1)`
  gira a mesma quantidade por frame — velocidade dependente do FPS, então
  a animação fica diferente entre `-q l` e `-q h`.
- **`.become()` substitui os pontos, não o objeto.** Referências antigas
  continuam válidas — é por isso que `always_redraw` funciona.
