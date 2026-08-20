# As 27 skills deste projeto Manim

Índice do conjunto. **Este arquivo é o mapa; quem roteia é `manim-project` §13.**
Se você só quer saber qual carregar, vá direto para lá — ou comece por
`manim-project`, que é a portaria e existe para isso.

Cada skill vive em `.claude/skills/<nome>/SKILL.md`, com frontmatter YAML
(`name`, `description`, `allowed-tools`). O campo que decide a invocação é a
`description`: ela diz o que a skill faz, traz gatilhos em português do jeito
que a pessoa pede de verdade, e termina com uma cláusula **NÃO use para…** que
entrega o pedido à irmã certa. Onde duas skills se tocam, **as duas** se
deferem — a fronteira está escrita nos dois lados, nunca em um só.

## Por onde começar

1. **`manim-project`** — leia esta antes de qualquer outra. Mapa do repositório,
   os dois motores, os wrappers de `bin/`, o contrato do `mx`, e o roteamento
   para as outras 26. A §14 dela é a sequência para "não sei por onde começar".
2. **`manim-api-discovery`** — antes de escrever a primeira linha de código:
   nenhuma assinatura entra num arquivo sem ter sido conferida.
3. A skill do **assunto** (as tabelas abaixo).
4. **`manim-verificacao-visual`** — renderizou e não olhou: não terminou.

## Fundamento e ferramenta

| Skill | Quando |
|---|---|
| **`manim-project`** | portaria: o mapa, os wrappers, o `mx`, e qual skill usar |
| **`manim-api-discovery`** | achar classe, método, kwarg, constante, assinatura — e **provar** que existe |
| **`manim-render-api`** | disparar o render e saber o que saiu: qualidade, formato, `-n a,b`, caminho do arquivo, API Python |
| **`manim-gpu-encoding`** | GPU, NVENC, escolha de codec, alfa, GIF, peso do arquivo, "está lento" por **encode** |
| **`manim-performance-cache`** | os cinco caches, o que invalida cada um, "está lento" por **rasterização** |
| **`manim-batch-pipeline`** | muitas cenas de uma vez: paralelismo entre processos, artefatos, CI |
| **`manim-verificacao-visual`** | provar que ficou certo: olhar o frame, medir tinta, comparar dois renders |
| **`manim-troubleshooting`** | falha concreta: traceback, exit code, saída errada, travamento |

## Desenhar

| Skill | Quando |
|---|---|
| **`manim-mobjects`** | o catálogo de formas, `VGroup` × `Group`, estilo, caixa delimitadora |
| **`manim-layout-posicionamento`** | compor no quadro: os cinco verbos, `buff`, `arrange`, z-index, "cabe na tela?", 9:16 |
| **`manim-text-latex`** | as nove classes de texto, `t2c`, `{{ }}`, `TexTemplate`, e a tipografia de precisão |
| **`manim-color-theming`** | cor de ponta a ponta: fundo, tinta, gradiente, alfa, contraste WCAG, temas |
| **`manim-tema-projeto`** | o `tema.py` como **contrato**: paleta + fonte + escala + tempos + classe-base + dados |
| **`manim-svg-imagens`** | trazer arquivo de fora: `SVGMobject`, `ImageMobject`, `register_font` |
| **`manim-graphs-plots`** | eixos, plano, `plot`, área, Riemann, tangente, escala log, `BarChart` |
| **`manim-tabelas-matrizes`** | `Table`, `Matrix`, célula destacada, colchetes |
| **`manim-grafos-redes`** | `Graph`/`DiGraph`, vértices e arestas, os 10 layouts, `from_networkx` |
| **`manim-mobjects-customizados`** | estender a biblioteca: classe própria, Bézier à mão, `Animation` própria, booleanos |
| **`manim-camera-2d`** | pan, zoom, seguir, `MovingCameraScene`, `ZoomedScene` e a lupa |
| **`manim-3d-camera`** | `ThreeDScene`, `phi`/`theta`, `Surface`, sólidos, texto fixo no quadro |

## Mover

| Skill | Quando |
|---|---|
| **`manim-animations`** | **qual** animação usar: as 75 classes, `.animate`, a família `Transform`, `self.play` |
| **`manim-composicao-ritmo`** | **quanto** tempo e em que ordem: `run_time`, as 49 `rate_func`, `lag_ratio`, `LaggedStart` |
| **`manim-updaters-valuetracker`** | valor que muda: `ValueTracker`, updaters, `always_redraw`, contador na tela |

## Estruturar e entregar

| Skill | Quando |
|---|---|
| **`manim-cenas-secoes`** | de qual `Scene` herdar, ciclo de vida, `add`/`remove`, `next_section` |
| **`manim-presentation-parts`** | cena para PALESTRA: o formato em partes que o apresentador avança |
| **`manim-som-legendas`** | `add_sound`, `add_subcaption`, o `.srt`, e as seis formas de o som sumir |
| **`manimgl-3b1b`** | o outro motor: `manimlib`, o REPL do Grant, portar GL ↔ CE |

## Os três desempates que mais custam

Estão completos em `manim-project` §13.5; estes são os que mais confundem:

| Sintoma | Vai para | Não vai para |
|---|---|---|
| "está lento" por **encode** (codec, NVENC, peso) | `manim-gpu-encoding` | `manim-performance-cache` |
| "está lento" por **rasterização** (curvas demais, cache frio) | `manim-performance-cache` | `manim-gpu-encoding` |
| `AttributeError`/`TypeError` de **nome ou assinatura** | `manim-api-discovery` | `manim-troubleshooting` |
| falha de **render, ambiente, codec, saída** | `manim-troubleshooting` | `manim-api-discovery` |
| **QUAL** animação usar | `manim-animations` | `manim-composicao-ritmo` |
| **QUANTO** tempo, que curva, em que ordem | `manim-composicao-ritmo` | `manim-animations` |
| "cabe na tela?" **antes** de renderizar | `manim-layout-posicionamento` | `manim-verificacao-visual` |
| provar **no pixel que saiu** que não coube | `manim-verificacao-visual` | `manim-layout-posicionamento` |
| a emenda entre **partes de um vídeo de slide** | `manim-presentation-parts` | `manim-verificacao-visual` |
| comparar dois renders quaisquer | `manim-verificacao-visual` | `manim-presentation-parts` |
| **5 caixas e setas** de um diagrama | `manim-layout-posicionamento` | `manim-grafos-redes` |

> A última linha é a decisão que mais custa em aula: um diagrama de arquitetura
> com 5 caixas rotuladas **não é** um `Graph`. Layout automático briga com
> legibilidade e muda de lugar a cada render.

## Assuntos sem skill dona

Declarados de propósito, para ninguém improvisar. A lista viva está em
`manim-project` §13.7. Os principais: **ênfase e anotação** (`Flash`,
`Indicate`, `Circumscribe`, `Brace*`, `SurroundingRectangle`) — órfão e muito
usado; **campos vetoriais** (`VectorField`, `StreamLines`, `PhaseFlow`);
**álgebra linear de cena** (`LinearTransformationScene`, `VectorScene`,
`ApplyMatrix`); **precedência de config** (`ManimConfig`, `tempconfig`); o
**renderer OpenGL do CE** (órfão de propósito — aqui o renderer é cairo); e
**plugins de terceiros**, que **[MEDIDO] não estão instalados nesta máquina**.

Se o pedido cair num deles: confirme com `bin/mx show` antes de escrever, e
diga ao usuário que a área não tem guia. Não invente comportamento.

## Convenções que valem para todas

- **Assinatura não conferida não entra no código.** O índice estático de `api/`
  responde em milissegundos; `bin/mx show <Nome>` custa 0,2 s.
- **Toda afirmação carrega procedência**: `[FONTE]` (lido no fonte instalado),
  `[ÍNDICE]`, `[MEDIDO]`, `[DISCO]`, `[DECK]` (veio do repositório consumidor
  `~/Projects/aulas`), `[NÃO VERIFICADO]`. Uma skill que não diz o que não sabe
  é pior que uma skill curta.
- **Correção é escrita, não apagada.** Onde uma versão anterior errou, o texto
  diz o que dizia, por que estava errado e qual é a evidência — é o que impede
  o erro de voltar na próxima rodada.
- **O Manim escreve branco por padrão.** Em fundo claro, mobject sem cor
  explícita some sem erro nenhum. Isso atravessa quase todas as skills.
