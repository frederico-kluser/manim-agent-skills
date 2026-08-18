---
name: manim-presentation-parts
description: >-
  Cena Manim para PALESTRA/SLIDE (reveal.js, PowerPoint, qualquer deck): o
  formato em PARTES que o apresentador avança com a seta. Use SEMPRE que a cena
  vai parar dentro de uma apresentação — "vídeo para o slide", "animação da
  aula", "quebra em partes", "o apresentador avança por etapas", "o vídeo é
  longo demais para eu comentar". Cobre o padrão mixin + next_section
  skip_animations, a granulação certa (5–10 conjuntos), a proibição de título
  dentro do vídeo, saída-antes-de-entrada, caudas curtas, a armadilha da emenda
  e a métrica direcional para conferi-la. NÃO use para vídeo standalone
  (YouTube, demo contínua) — lá o corte em partes não se aplica.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cena de apresentação — nasce em partes

Uma animação de 40 s dentro de um slide não deixa o apresentador falar: ou ele
narra por cima do movimento, ou fica calado o filme inteiro. O formato que
resolve: a cena é UMA, escrita inteira num `construct`, mas renderizada em N
mp4s — um por "ato" — e cada parte termina num **frame parado**. O apresentador
avança com a seta, fala no frame parado, e o primeiro frame da parte N+1 é
pixel a pixel o último da parte N.

Este padrão nasceu no deck `~/Projects/aulas` (7 cenas, 52 partes em produção)
e cada regra abaixo veio de uma devolução real do apresentador.

## O padrão

```python
class _AtosMinhaCena:                      # MIXIN — NÃO herda de Scene!
    """Se herdasse, `mx scenes` o listaria e o pipeline renderizaria a
    cena inteira de novo, por engano. As subclasses P1..PN é que herdam."""

    PAUSA_ENTRE_PARTES = 0.25   # o respiro no FIM de cada ato (ver "caudas")
    PARTE = 0                   # 0 = cena contínua, sem cortes

    def _corte(self, n: int) -> None:
        """Fronteira entre o ato n-1 e o ato n. O wait vem ANTES do corte de
        propósito: pertence ao ato que termina e some junto quando ele é
        pulado — depois do corte, viraria pausa morta no começo da parte."""
        if n > 1:
            self.wait(self.PAUSA_ENTRE_PARTES)
        self.next_section(f"ato{n}", skip_animations=(self.PARTE != 0 and n != self.PARTE))

    def construct(self) -> None:
        self._corte(1)          # SEMPRE a primeira linha do construct
        ...ato 1...
        self._corte(2)
        ...ato 2...


class MinhaCenaP1(_AtosMinhaCena, Scene):   # ou da sua base de tema
    """Parte 1/N — o que esta parte mostra, em uma linha."""
    PARTE = 1
# ...uma classe por parte, até PN
```

Por que `next_section(skip_animations=...)` e não N `construct` separados: os
atos que não são o desta parte **rodam mesmo assim** — o estado do palco é
reconstruído animação por animação, só não escreve frame. Não existe uma
segunda versão do ato 1 para sair de sincronia com a primeira.

## As regras que vieram de devolução

1. **SEM TÍTULO NEM SUBTÍTULO dentro do vídeo.** O slide já tem título; o do
   vídeo duplica e rouba um quinto do quadro. O contexto é responsabilidade do
   título do SLIDE. Recentre o conteúdo — faixa morta no topo é defeito.
2. **Granulação: 5–10 conjuntos por cena.** Os dois excessos já foram
   devolvidos: 4 partes = "muita coisa de cada vez"; 17–18 = "muitas micro
   partes". Cada parte é um conjunto de 2–3 micro-beats que se falam, e cabe
   numa ideia FALADA. Dois conceitos independentes = duas partes; três
   animações do mesmo raciocínio = uma.
3. **Saída ANTES da entrada.** Informação velha e nova nunca se cruzam no mesmo
   `self.play` — o crossfade dá uma "piscada". `FadeOut` completa num play;
   `FadeIn` começa no seguinte.
3b. **UMA PARTE NÃO TROCA O RODAPÉ NO MEIO.** Texto de apoio novo é fala nova, e
   fala nova é clique novo. É o teste mais barato para saber se a parte tem uma
   ideia ou duas: **conte os recados — dois recados, duas partes.** A variante
   disfarçada da mesma falha: a parte que termina com um movimento que APAGA o
   que ela acabou de mostrar (uma janela descendo por cima do texto). Esse
   movimento é a CABEÇA da parte seguinte, não o rabo desta.
3c. **Sem jargão do projeto no rodapé.** Nome de flag, de arquivo e de conceito
   interno vira comentário no código da cena — que é para quem edita. Na tela
   vai a coisa dita em língua corrente. E cada linha de apoio abaixo de ~62
   caracteres, quebrada onde a FALA respira, na mão.
4. **Caudas curtas.** Último `wait` de cada ato ≤ 0.4 s (última parte ~0.8). O
   player do deck segura o frame final parado de qualquer forma, e cauda longa
   atrasa o sinal de "terminou" que o apresentador usa para saber que pode
   falar.
5. **Nada vaza nem sobrepõe.** Frame: x ∈ [−7.11, +7.11], y ∈ [−4, +4]. Linha
   única de rodapé com mais de ~70 caracteres quebra em duas (`VGroup(...).
   arrange(DOWN)`). Nenhum elemento sobre outro num frame de repouso.
6. **O código é o produto tanto quanto o mp4.** A cena fica versionada com
   comentário farto por ato: o que aparece, por quê, de onde vem cada número.
   É o que torna a próxima edição barata.

## A armadilha da emenda

A emenda só é invisível se o primeiro frame da parte N+1 for IGUAL ao último da
parte N. O mecanismo garante o ESTADO, não o QUADRO:

> Um ato abria com `TransformFromCopy(objeto_opaco, ...)`. No alfa 0 a cópia é
> opaca e está exatamente EM CIMA do original — ela tapa o que o ato anterior
> construiu. Num vídeo contínuo, 1/60 s invisível; como primeiro frame de uma
> parte, é o quadro em que o vídeo fica PARADO com conteúdo faltando.

**Nunca corte imediatamente antes de animação que cobre o que já está na
tela.** Corte depois dela e deixe comentário — senão o próximo "conserta" de
volta.

## Conferir a emenda: métrica DIRECIONAL, nunca RMS

RMS da diferença entre frames acusa como defeito a animação seguinte COMEÇANDO
— que é o comportamento certo. O único defeito é **tinta que SOME**:

```python
import numpy as np
from PIL import Image
a = np.asarray(Image.open("fim-da-parte-N.png").convert("L"), dtype=np.int16)
b = np.asarray(Image.open("inicio-da-N+1.png").convert("L"), dtype=np.int16)
sumiu = int(((b - a) > 24).sum())   # pixels que CLAREARAM = tinta removida
# até ~400 px (em 2 M) é antialiasing; acima, alguma coisa desapareceu na troca
```

Pixels que escurecem são a próxima animação entrando — não contam. Extraia os
frames com ffmpeg (`-sseof -0.05` para o último; sem seek para o primeiro).

## Duas armadilhas de desenho, medidas

**Texto que cruza uma linha de grade.** Num gráfico com marcas tracejadas, o
número colado à barra pode cair em cima de uma marca; no frame de repouso isso
lê como texto quebrado. Não mova o número — dê a ele um **prato opaco na cor do
fundo**, adicionado ANTES do texto no `VGroup`, do tamanho do texto mais ~0,2 de
folga. O prato não aparece: ele só apaga a grade atrás das letras.

**Espaço dentro de um rótulo curto.** `f"{n//1000} K"` desenha "26  K" — a fonte
abre um vão largo o bastante para o olho ler duas coisas. Em legenda apertada,
cole (`26K`), e use buff LARGO entre os itens (~0,5) e curto dentro de cada item
(~0,1): é o agrupamento que faz a legenda ser lida como N coisas em vez de uma
faixa de texto.

**O pôster tem que ser o ÚLTIMO frame.** Se o pipeline extrai o pôster com
`ffmpeg -sseof -1 -i x.mp4 -update 1 -frames:v 1 x.png`, ele grava o primeiro
frame DEPOIS do seek — o de 1 s antes do fim. Numa parte que fecha com `FadeIn`,
o pôster sai com o texto lavado enquanto o vídeo está perfeito. Use `-update 1`
**sem** `-frames:v 1`.

## Nomes e integração com o deck

Classe `MinhaCenaP3` → arquivo `minha-cena-p3.mp4` (PascalCase → kebab). O deck
consumidor precisa, por parte: o mp4, o png do último frame (pôster/PDF) e o
png do PRIMEIRO frame (pôster da parte seguinte — sem ele a troca pisca em
branco). O exemplo completo de player e pipeline está em
`~/Projects/aulas` (`src/components/video-partes.tsx`,
`scripts/render-videos.sh`, skill `aula-videos`).
