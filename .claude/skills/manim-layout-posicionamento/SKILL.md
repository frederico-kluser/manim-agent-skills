---
name: manim-layout-posicionamento
description: >-
  Compor no quadro: o sistema de coordenadas real (14,2222 × 8 unidades,
  x ∈ [−7,11; +7,11], y ∈ [−4; +4]), os cinco verbos de posicionamento
  (`shift`, `move_to`, `next_to`, `align_to`, `to_edge`/`to_corner`), `buff` e
  as quatro constantes de margem, `arrange` e `arrange_in_grid`, a caixa
  delimitadora e os 9 pontos críticos, `z_index` e a ordem de desenho,
  alinhamento de texto (a caixa é de TINTA, não de tipografia), e como manter o
  layout estável quando o conteúdo muda de tamanho. Use quando o pedido soar
  como "põe isso no canto", "alinha esses dois", "centraliza", "isso está
  cortado na borda", "o elemento saiu do quadro", "encaixa lado a lado", "monta
  uma grade de 3 por 4", "empilha esses textos", "os itens ficaram torto",
  "o espaçamento está irregular", "esse rótulo ficou por baixo do retângulo",
  "o texto sumiu atrás da caixa", "quero isso na frente de tudo", "a legenda
  encostou no gráfico", "sobrou um vazio enorme em cima", "o grupo pulou de
  lugar quando eu chamei arrange", "o bloco se desloca quando o texto cresce",
  "quantas unidades tem a tela?", "onde fica a margem segura?", "isso cabe na
  tela?", "vídeo vertical / 9:16 / Shorts / Reels", "as linhas do parágrafo
  ficaram com espaço desigual", "por que `mob.width` não bate com
  `get_right() − get_left()`". NÃO use para: escolher a FORMA e agrupar
  (`manim-mobjects`, dona de `VGroup` × `Group`, `scale_to_fit_*` e da caixa
  delimitadora como conceito); mover a CÂMERA, zoom e pan (`manim-camera-2d`);
  `phi`/`theta` e 3D (`manim-3d-camera`); animar o movimento, `Transform`,
  `.animate` (`manim-animations`) e `rate_func`/`path_func`
  (`manim-composicao-ritmo`); eixos, `c2p` e coordenadas de GRÁFICO
  (`manim-graphs-plots`); layout automático de rede (`manim-grafos-redes`);
  grade de TABELA (`manim-tabelas-matrizes`); cor e contraste
  (`manim-color-theming`); `t2c`, LaTeX e nitidez de glifo (`manim-text-latex`);
  olhar o PNG e conferir o resultado (`manim-verificacao-visual`); cortar a cena
  em partes para slide (`manim-presentation-parts`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Layout e posicionamento — o quadro manda

O Manim não tem *layout engine*. Não há fluxo, não há caixa flexível, não há
margem que empurra vizinho. Há **um plano cartesiano fixo** e um punhado de
métodos que **transladam** um mobject até que um ponto dele coincida com um
ponto de outro. Todo o resto — grade, coluna, rodapé, respiro — é você quem
escreve, em números.

Isso é bom: nada se move sozinho. E é a fonte de quase todo defeito de
enquadramento, porque **nada disso levanta exceção**. O que passa da borda é
cortado em silêncio; o que fica por baixo simplesmente não aparece; o rodapé que
cresceu uma linha atravessa a divisória sem um aviso no terminal.

## Procedência do que está escrito aqui

Três marcadores, válidos para o arquivo inteiro:

- **[FONTE]** — conferido lendo o ManimCE 0.21.0 instalado em
  `.venv/lib/python3.12/site-packages/manim/`, ou o índice estático de `api/`
  (`manim-ce-index.tsv`, `manim-ce-methods.tsv`). Afirmação forte, com arquivo e
  linha.
- **[DECK]** — medido no deck consumidor `~/Projects/aulas` (11 arquivos de
  cena, 77 classes de parte em produção). Eles mediram; **não foi reproduzido
  aqui**.
- **[NÃO VERIFICADO]** — derivado da leitura do fonte, sem execução.

**Nesta redação nenhum render, nenhum `ffmpeg`, nenhum benchmark foi
executado.** Onde um número dependeria de rodar alguma coisa, ele está marcado.

Esta skill não traz arquivo de apoio: tudo o que ela ensina são cinco métodos e
um punhado de constantes que já existem na biblioteca. O que ela porta do deck é
um **padrão** — posicionar pelo corpo visível, ancorar pela borda que não pode
se mexer — e padrão mora em prosa, não em `assets/`.

---

## 1. O quadro: os números que você precisa saber de cor

### 1.1 O palco

[FONTE] `_config/utils.py:673-678`, na digestão do arquivo de configuração:

```python
self["frame_height"] = parser["CLI"].getfloat("frame_height", 8.0)
width = parser["CLI"].getfloat("frame_width", None)
if width is None:
    self["frame_width"] = self["frame_height"] * self["aspect_ratio"]
```

Ou seja: **a altura do mundo é 8,0 unidades por decreto**, e a largura sai da
proporção em PIXELS. Com os 1920×1080 que este projeto fixa em `manim.cfg`:

| Grandeza | Valor | De onde vem |
|---|---|---|
| `config.frame_height` | **8,0** | fixo, default da biblioteca |
| `config.frame_width` | **14,2222** | 8 × 1920/1080 |
| `config.frame_y_radius` | **4,0** | `frame_height / 2` [FONTE] `utils.py:1149-1152` |
| `config.frame_x_radius` | **7,1111** | `frame_width / 2` [FONTE] `utils.py:1160-1163` |
| x visível | **−7,1111 … +7,1111** | — |
| y visível | **−4,0 … +4,0** | — |
| pixels por unidade | **135** | 1080/8 = 1920/14,2222 |

Os 135 px/unidade são a régua mental que falta na documentação: `SMALL_BUFF`
(0,1) são **13,5 px**; um `buff=0.5` de `to_edge` são **67,5 px**; um deslize de
0,03 unidades é **4 px** — exatamente a ordem de grandeza do defeito silencioso
de §2.5.

### 1.2 A resolução NÃO redimensiona o mundo

`frame_width` é calculado **uma única vez**, quando os arquivos de configuração
são digeridos. Depois disso, mudar a resolução não o toca:

[FONTE] `_config/utils.py:1344-1352` — o setter de `quality` chama
`self.frame_size = (pw, ph)`, e `frame_size` (`:1329-1332`) escreve **só**
`pixel_width` e `pixel_height`. Nenhum dos dois recalcula `frame_width`.

Consequências, as duas boas e a ruim:

1. **`-ql`, `-qm`, `-qh`, `-qk` desenham o MESMO mundo.** Uma coordenada
   conferida no preview vale no render final. É por isso que o ciclo "render
   rápido → olhar → corrigir" funciona.
2. **`-r LARGURAxALTURA` também não muda o mundo** — muda só o buffer de pixels.
3. **Pedir 9:16 não dá vídeo vertical.** É o defeito de §1.5.

### 1.3 As âncoras prontas do `config`

[FONTE] `_config/utils.py:1170-1188` — quatro propriedades que devolvem
**vetores**, não escalares:

```python
config.top          # frame_y_radius * UP     → [0, 4, 0]
config.bottom       # frame_y_radius * DOWN   → [0, −4, 0]
config.left_side    # frame_x_radius * LEFT   → [−7.1111, 0, 0]
config.right_side   # frame_x_radius * RIGHT  → [+7.1111, 0, 0]
```

Use-as em vez de digitar `7.11`: se um dia a cena virar vertical, o código
acompanha. Elas são a diferença entre uma constante que envelhece e uma que se
recalcula.

### 1.4 As direções, e por que coordenada é sempre 3D

[FONTE] `constants` (índice `api/manim-ce-index.tsv`, categoria `constants`) —
todas são `np.ndarray` de **três** componentes:

| Constante | Valor | | Constante | Valor |
|---|---|---|---|---|
| `UP` | `[0, 1, 0]` | | `UL` | `[−1, 1, 0]` |
| `DOWN` | `[0, −1, 0]` | | `UR` | `[1, 1, 0]` |
| `LEFT` | `[−1, 0, 0]` | | `DL` | `[−1, −1, 0]` |
| `RIGHT` | `[1, 0, 0]` | | `DR` | `[1, −1, 0]` |
| `IN` | `[0, 0, −1]` | | `ORIGIN` | `[0, 0, 0]` |
| `OUT` | `[0, 0, 1]` | | `X_AXIS` `Y_AXIS` `Z_AXIS` | os três unitários |

**Ponto literal é sempre 3D**: `[x, y, 0]`, nunca `[x, y]`. Uma tupla de dois
elementos dá erro de *broadcast* do numpy num lugar que não tem nada a ver com o
seu código, e a mensagem não ajuda.

E direções **somam**: `UL == UP + LEFT`, `aligned_edge=LEFT + UP` é o canto
superior esquerdo. É essa aritmética que faz `next_to` e `move_to` terem uma
gramática só.

### 1.5 Vertical (9:16), e a régua que mente junto

O caso "quero um vídeo pro Shorts". **[MEDIDO em `manim-project` §10.3]**
`bin/mx render vert.py Vert -r 1080x1920 --format png` imprime
`frame 14.222 x 8.000 | pixel 1080x1920`: o mundo continua paisagem, um
`Dot().to_edge(UP)` cai a **37,7% do topo** do PNG, e nada distorce — só sobra
mundo em cima e embaixo. **`manim-project` §10.3 é o pré-requisito desta
seção; não o reescreva, leia-o.** A correção é uma linha no topo do módulo:

```python
config.frame_width = config.frame_height * 1080 / 1920      # 8 × 0,5625 = 4,5
```

O que é matéria **desta** skill é o que quebra DEPOIS da correção, e são três
coisas:

1. **Metade das suas coordenadas x viram lixo.** O mundo passou de 14,22 para
   4,5 de largura: x = 6,0 agora está fora da tela. Se as constantes de
   geometria vieram de `config.frame_x_radius` (§1.3), sobrevivem; se foram
   digitadas, não.
2. **`FullScreenRectangle` deixa de cobrir a tela.** [FONTE] `mobject/frame.py`
   — `ScreenRectangle(aspect_ratio=16/9, height=4)` e `FullScreenRectangle`
   apenas faz `self.height = config["frame_height"]`, o que é o *setter* de
   `height`, isto é, `scale_to_fit_height` — **proporção 16:9 preservada**. Com
   `frame_height=8` e `frame_width=4.5`, ele sai 8 × 14,22: três vezes mais
   largo que o quadro. Para um véu de tela cheia em formato vertical use
   `Rectangle(width=config.frame_width, height=config.frame_height)`.
3. **A câmera móvel nasce 16:9 pelo mesmo motivo.** [FONTE]
   `camera/moving_camera.py:52-53` — o `frame` default é
   `ScreenRectangle(height=config["frame_height"])`. Detalhe de
   **`manim-camera-2d`**; aqui fica só o aviso de que o sintoma é o mesmo.

---

## 2. A caixa delimitadora é a única régua — e ela mede duas coisas diferentes

Nenhum método de posicionamento conhece a forma do seu objeto. Todos falam com
a **caixa** dele.

### 2.1 Os nove pontos críticos, e por que só o SINAL importa

[FONTE] `mobject.py:2266-2293`. `get_critical_point(direction)` percorre as três
dimensões e, para cada uma, chama `get_extremum_along_dim(..., key=direction[dim])`,
cuja regra (`:2247-2265`) é:

```python
if key < 0:   return np.min(values)      # borda de baixo / da esquerda
elif key == 0: return (min + max) / 2    # o meio
else:          return np.max(values)     # borda de cima / da direita
```

Três consequências que economizam confusão:

- A caixa tem exatamente **9** pontos endereçáveis: 4 cantos, 4 centros de
  aresta, 1 centro. Não existe "20% da largura" — para isso você faz a conta.
- **A magnitude do vetor é ignorada.** `get_corner(UR)` e `get_corner(UR*17)`
  devolvem o mesmo ponto. Isso é o que permite somar direções sem normalizar.
- Todos os *getters* de canto são **apelidos** do mesmo método [FONTE]
  `:2295-2360`: `get_edge_center`, `get_corner`, `get_center`, `get_top`,
  `get_bottom`, `get_left`, `get_right`, `get_zenith` (OUT), `get_nadir` (IN).
  Nomes diferentes, uma implementação. `get_corner(UP)` funciona e devolve o
  centro da aresta de cima — o nome é que engana.

```python
mob.get_center()          # == get_critical_point(ORIGIN)
mob.get_corner(UL)        # canto superior esquerdo
mob.get_edge_center(DOWN) # centro da aresta de baixo
mob.get_x(RIGHT)          # só o escalar x da borda direita   [FONTE] :2370-2376
mob.get_y(UP)             # só o escalar y do topo
```

### 2.2 `width` e `get_right() − get_left()` podem NÃO bater

Esta é a assimetria mais surpreendente do conjunto, e ela é [FONTE]:

| Consulta | Caminho | O que entra na conta |
|---|---|---|
| `mob.width` | `length_over_dim(0)` → `reduce_across_dimension` (`mobject.py:2168-2211`) | **`self.points` inteiro**, alças de Bézier incluídas |
| `mob.get_right()` | `get_critical_point` → `get_points_defining_boundary` | em `VMobject` (`vectorized_mobject.py:1793-1797`), **só as âncoras** |

O `Mobject` genérico define `get_points_defining_boundary = get_all_points`
(`mobject.py:2241`), mas o `VMobject` **sobrescreve** para devolver apenas
`get_anchors()` de toda a família. Então, num `VMobject` cujas curvas estufam
entre âncoras, `width` é maior que a distância entre `get_left()` e
`get_right()`.

Onde isso morde: `scale_to_fit_width` / `match_width` / `replace` / `surround`
passam por `rescale_to_fit` → `length_over_dim` (alças), enquanto `next_to`,
`align_to` e `move_to` passam por pontos críticos (âncoras). **Ajustar o
tamanho e depois encostar não fecha exatamente.**

**Correção: `SurroundingRectangle` está do lado das ALÇAS, não das âncoras.**
Uma versão anterior desta linha o listava com `next_to`/`align_to`. É o
contrário, e nos dois eixos (`geometry/shape_matchers.py:71-79`):

```python
group = Group(*mobjects)
super().__init__(width=group.width + 2*buff_x,       # → length_over_dim → ALÇAS
                 height=group.height + 2*buff_y, ...)
self.move_to(group)                                  # → get_critical_point de um Group
```

O `move_to` seria régua de âncora **se** o alvo fosse `VMobject` — mas o alvo é
um `Group` cru, e `class Group(Mobject)` (`mobject.py:3400`) **não** sobrescreve
`get_points_defining_boundary`; cai no `mobject.py:2241 → get_all_points()`,
alças incluídas de novo. Só `VMobject` sobrescreve
(`vectorized_mobject.py:1793`, devolvendo `get_anchors()`).

**O corolário que vale para todo o resto desta skill:** a régua também troca
pelo CONTÊINER. `VGroup(a, b).get_center()` mede por âncoras;
`Group(a, b).get_center()` mede por todos os pontos. Se um grupo "pula" ao ser
centralizado e o outro não, é isto — e não um `buff` errado. Nas §2.5 e §8.3,
onde se posiciona **pelo grupo**, prefira `VGroup` quando todos os filhos forem
vetoriais.

**[NÃO VERIFICADO]** — o mecanismo está lido no fonte; a magnitude do desvio em
um caso concreto não foi medida (exigiria executar). Para formas fechadas
comuns (`Circle`, `Square`, `Rectangle`) as alças não ultrapassam as âncoras nos
eixos, e a diferença é zero; o risco vive em `CubicBezier` com alças longas e em
caminhos importados de SVG.

### 2.3 `get_boundary_point` ≠ `get_corner`

[FONTE] `mobject.py:2310-2314`:

```python
def get_boundary_point(self, direction):
    index = np.argmax(np.dot(all_points, direction))
    return all_points[index]
```

Devolve **um ponto que está sobre o desenho**, o mais avançado naquela direção —
não um canto da caixa. É o que você quer para encostar uma seta na borda de um
círculo (`get_corner(UR)` de um círculo é um canto no vazio, fora da linha).

### 2.4 `get_center` ≠ `get_center_of_mass`

[FONTE] `:2303-2309`. `get_center()` é o centro da CAIXA; `get_center_of_mass()`
é a média aritmética de **todos** os pontos (`get_all_points`), portanto
enviesada para onde há mais pontos de controle. Num "L" de duas pernas, os dois
ficam em lugares visivelmente diferentes. Para centralizar use `get_center`;
`get_center_of_mass` é para achar "o miolo" de uma nuvem.

Para pôr um rótulo DENTRO de um polígono irregular (onde nem um nem outro cai em
lugar bom), a biblioteca tem o polo de inacessibilidade:

```python
from manim.utils.polylabel import polylabel
cell = polylabel([vertices2d], precision=0.01)   # [FONTE] utils/polylabel.py:180
centro = np.array([*cell.c, 0])                  # cell.c é 2D; cell.d é a folga
```

É o mesmo algoritmo que `LabeledPolygram` usa por dentro [FONTE]
`mobject/geometry/labeled.py:374`. A classe `LabeledPolygram` em si é órfã (§11).

### 2.5 O membro invisível entra na caixa — e a API tem o antídoto

Opacidade 0 e `stroke_width=0` **não** removem âncoras. Uma lingueta
transparente, um espaçador, um `VectorizedPoint` de ancoragem: todos contam.
**[DECK]** um detalhe transparente dentro de um `VGroup` fez `VGroup.move_to()`
deslocar o grupo inteiro **4 px** — silenciosos, descobertos só pela métrica de
emenda entre partes de vídeo. O mecanismo está detalhado em `manim-mobjects`
§5.3, que é a dona da caixa delimitadora como conceito.

**A regra: posicione pelo CORPO VISÍVEL, não pelo grupo.** O deck faz isso na
mão:

```python
grupo = VGroup(corpo, lingueta_invisivel)
grupo.shift(alvo - corpo.get_center())      # certo: mede o corpo, move o grupo
# grupo.move_to(alvo)                       # errado: mede a lingueta junto
```

E o `next_to` já tem o parâmetro embutido para isso — pouco conhecido, e é
exatamente esta a hipótese de uso. [FONTE] `mobject.py:1723-1730`:

```python
if submobject_to_align is not None:
    aligner = submobject_to_align
elif index_of_submobject_to_align is not None:
    aligner = self[index_of_submobject_to_align]
else:
    aligner = self
point_to_align = aligner.get_critical_point(np_aligned_edge - np_direction)
self.shift((target_point - point_to_align + buff * np_direction) * coor_mask)
```

O `shift` é do grupo inteiro; a MEDIDA sai do submobject. Então:

```python
grupo.next_to(ancora, DOWN, buff=0.3, submobject_to_align=corpo)
```

Duas ressalvas [FONTE], as duas na leitura do mesmo trecho:

- **`move_to` não tem esse parâmetro** (`:1904-1918`). Lá continua valendo o
  `shift` manual acima.
- **`index_of_submobject_to_align` vale para os DOIS lados.** Quando ele é
  passado, o alvo também é medido por `mob[índice]` (`:1712-1717`). Se você quer
  medir só o seu lado, use `submobject_to_align=`, que só afeta `self`.

---

## 3. Os cinco verbos

Tudo que posiciona no Manim é, no fim, `Mobject.shift`. Os outros quatro
calculam o vetor.

| Verbo | Assinatura [FONTE] `mobject/mobject.py` | Pergunta que responde |
|---|---|---|
| `shift` | `shift(*vectors) -> Self` (`:1262`) | "mexe daqui pra lá" |
| `move_to` | `move_to(point_or_mobject, aligned_edge=ORIGIN, coor_mask=[1,1,1])` (`:1904`) | "vai para ESTE ponto" |
| `next_to` | `next_to(mobject_or_point, direction=RIGHT, buff=0.25, aligned_edge=ORIGIN, submobject_to_align=None, index_of_submobject_to_align=None, coor_mask=[1,1,1])` (`:1679`) | "fica ao lado daquele" |
| `align_to` | `align_to(mobject_or_point, direction=ORIGIN)` (`:2474`) | "encosta a borda na borda dele" |
| `to_edge` / `to_corner` | `to_edge(edge=LEFT, buff=0.5)` (`:1649`) · `to_corner(corner=DL, buff=0.5)` (`:1621`) | "vai para a borda do QUADRO" |

### 3.1 `shift` — o primitivo

```python
mob.shift(RIGHT * 2)            # dois à direita
mob.shift(UP * 0.5, LEFT * 3)   # aceita vários; soma todos [FONTE] :1262
```

Único verbo que é **relativo**. Usar `shift` para chegar a uma posição absoluta
é o erro estrutural mais comum em cena que vai ser editada: `shift(UP*1.3)`
depois de trocar o tamanho do objeto vai para outro lugar; `move_to([x, y, 0])`
não.

### 3.2 `move_to` — absoluto, com dois parâmetros que ninguém usa e deviam

[FONTE] `:1904-1918`:

```python
target = point_or_mobject.get_critical_point(aligned_edge)   # se for Mobject
point_to_align = self.get_critical_point(aligned_edge)
self.shift((target - point_to_align) * coor_mask)
```

- **`aligned_edge`** troca qual dos 9 pontos vai coincidir. `move_to(p)` alinha
  centros; `move_to(p, aligned_edge=LEFT+UP)` põe o **canto superior esquerdo**
  do objeto no ponto `p`. É o idioma de ancoragem do deck (§8.1).
- **`coor_mask`** filtra eixos. `move_to(alvo, coor_mask=[1,0,0])` copia só o x.

```python
titulo.move_to([-6.21, 3.10, 0], aligned_edge=LEFT + UP)   # canto ancorado
barra.move_to(referencia, coor_mask=[0, 1, 0])             # só a altura
```

O segundo caso também se escreve `barra.match_y(referencia)` — §3.6.

### 3.3 `next_to` — e as duas coisas que ele faz e você não pediu

[FONTE] `:1712-1731`. Ele calcula:

```
alvo  = outro.get_critical_point(aligned_edge + direction)
meu   = self .get_critical_point(aligned_edge − direction)
shift = alvo − meu + buff * direction
```

**`aligned_edge` tem de ser PERPENDICULAR a `direction`.** A soma e a diferença
acima são o que faz a mágica funcionar: com `direction=DOWN` e
`aligned_edge=LEFT`, o alvo é o canto `DL` do outro e o meu é o canto `UL` — e
as bordas esquerdas ficam alinhadas. Se `aligned_edge` tiver componente ao longo
de `direction`, os sinais se cancelam: `next_to(m, RIGHT, aligned_edge=RIGHT)`
manda o **centro** do seu objeto para a borda direita do outro, e eles se
sobrepõem. Não dá erro.

**`buff` é multiplicado pelo vetor CRU, não pela direção normalizada.**
`buff * np_direction` no fonte, sem `normalize`. Daí:

```python
a.next_to(b, RIGHT * 2)        # NÃO é "2 unidades à direita"
                               # é next_to(b, RIGHT, buff=0.5)  — buff × 2
a.next_to(b, UR, buff=0.2)     # 0,2 em x E 0,2 em y → folga diagonal 0,283
```

O primeiro engana porque *funciona*: o objeto de fato se afasta mais, então
ninguém investiga. Quando você quer distância absoluta, é `next_to(b, RIGHT,
buff=…)` ou `move_to`.

`next_to` também aceita **um ponto** no lugar do mobject — `next_to(ORIGIN, UP)`
é válido e não tem nada a ver com o objeto que está na origem.

### 3.4 `align_to` — e o default que não faz nada

[FONTE] `:2474-2493`:

```python
point = mobject_or_point.get_critical_point(direction)
for dim in range(self.dim):
    if direction[dim] != 0:
        self.set_coord(point[dim], dim, direction)
```

Move **só nos eixos em que `direction` é diferente de zero**. Logo:

- `a.align_to(b, LEFT)` — as bordas ESQUERDAS de a e b passam a ter o mesmo x; o
  y de `a` não é tocado.
- `a.align_to(b, UP)` — os TOPOS passam a ter o mesmo y.
- `a.align_to(b, UL)` — as duas coisas ao mesmo tempo.
- **`a.align_to(b)` — não faz nada.** O default é `ORIGIN`, e nenhum componente
  é diferente de zero. Silencioso.

O par mais útil de toda a skill é `next_to` + `align_to`, e é o que o deck
escreve [DECK] `aula_001_mcp.py:522`:

```python
risco.next_to(catalogo, DOWN, buff=0.20).align_to(catalogo, LEFT)
```

`next_to` resolve a distância vertical, `align_to` resolve o alinhamento
horizontal. Fazer as duas coisas com `next_to(..., aligned_edge=LEFT)` também
funciona; a versão em dois passos é mais fácil de reajustar depois, porque cada
linha responde por um eixo.

### 3.5 `to_edge`, `to_corner`, `center` — a borda do QUADRO

Os dois primeiros são fachadas de `align_on_border`. [FONTE] `:1604-1620`:

```python
target_point   = np.sign(direction) * (frame_x_radius, frame_y_radius, 0)
point_to_align = self.get_critical_point(direction)
shift_val      = target_point - point_to_align - buff * np.array(direction)
shift_val      = shift_val * abs(np.sign(direction))
```

Quatro leituras:

1. **Só mexe nos eixos da direção.** `to_edge(UP)` não altera o x — é isso que
   a docstring promete e o `abs(np.sign(direction))` cumpre.
2. **`buff` também aqui multiplica o vetor cru.** `to_edge(UP*2, buff=0.5)`
   afasta 1,0 do topo. Mesmo defeito de §3.3.
3. **O z é sempre zerado** no `target_point`: `to_edge(OUT)` não faz nada útil.
4. **É cego para a câmera.** Ele lê `config`, nunca `self.camera.frame`. Numa
   `MovingCameraScene` com a câmera deslocada ou com zoom, `to_edge(UP)` continua
   mirando o topo do MUNDO, que pode estar fora do enquadramento. Quem posiciona
   relativo ao que se vê é **`manim-camera-2d`**.

`center()` [FONTE] `:1593-1601` é literalmente `self.shift(-self.get_center())`
— leva o CENTRO DA CAIXA para a origem. Num grupo com membro invisível, leva o
centro da caixa que inclui o invisível (§2.5).

Buffs default: `to_edge`/`to_corner` usam `DEFAULT_MOBJECT_TO_EDGE_BUFFER = 0.5`;
`next_to`/`arrange` usam `DEFAULT_MOBJECT_TO_MOBJECT_BUFFER = 0.25`. [FONTE]
categoria `constants` do índice.

### 3.6 Coordenada única: `set_x`, `set_coord`, `match_*`

[FONTE] `:1877-1896` e `:2452-2473`. O parâmetro `direction` decide **qual borda
do seu objeto** vai para a coordenada pedida:

```python
mob.set_x(0)                    # centro em x = 0
mob.set_x(-6.21, LEFT)          # borda ESQUERDA em x = −6,21
mob.set_y(3.5, UP)              # TOPO em y = 3,5
mob.set_coord(v, dim, direction)  # a forma geral; dim 0=x 1=y 2=z

barra.match_y(eixo)             # centros no mesmo y
rotulo.match_x(coluna, LEFT)    # bordas esquerdas no mesmo x
```

`match_coord(mob, dim, direction)` é a forma geral; `match_x`/`match_y`/`match_z`
são fachadas. Note que `match_*` copia **posição**; `match_width`/`match_height`/
`match_depth` copiam **tamanho** e são de `manim-mobjects`.

`set_x(v, LEFT)` é a maneira mais barata de fixar uma margem: o objeto pode
crescer para a direita à vontade que a borda esquerda não sai do lugar. É o
mesmo princípio da §8.1, em um eixo só.

### 3.7 O guia rápido

| Você quer | Escreva |
|---|---|
| deslocar em relação a onde está | `shift(RIGHT * 2)` |
| pôr o centro num ponto | `move_to([x, y, 0])` |
| pôr um CANTO num ponto | `move_to([x, y, 0], aligned_edge=UL)` |
| copiar só o x (ou só o y) de outro | `move_to(m, coor_mask=[1,0,0])` ou `match_x(m)` |
| encostar ao lado, com folga | `next_to(m, RIGHT, buff=0.3)` |
| empilhar alinhando pela esquerda | `next_to(m, DOWN, aligned_edge=LEFT)` |
| medir por uma peça, mover o grupo | `next_to(m, DOWN, submobject_to_align=corpo)` |
| igualar bordas (um eixo) | `align_to(m, LEFT)` |
| igualar bordas (dois eixos) | `align_to(m, UL)` |
| fixar uma margem em um eixo | `set_x(-6.21, LEFT)` |
| grudar na borda do quadro | `to_edge(UP, buff=0.7)` |
| grudar num canto do quadro | `to_corner(UR, buff=0.5)` |
| voltar ao meio do quadro | `center()` |
| espalhar os filhos sem redimensioná-los | `space_out_submobjects(1.5)` |
| ordenar os filhos por posição | `sort(point_to_num_func=lambda p: p[1])` |

`space_out_submobjects(factor=1.5)` tem uma pegadinha [FONTE] `:1898-1903`: ele
escala o pai por `factor` e cada filho por `1/factor`. Se o **pai tiver pontos
próprios** (um `Rectangle(grid_xstep=…)`, por exemplo), esses pontos ficam
escalados e não voltam. Em `VGroup` puro, que não tem pontos, o resultado é o
esperado.

`sort(point_to_num_func=lambda p: p[0], submob_func=None)` [FONTE] `:2883-2891`
reordena `self.submobjects` — o que muda **a ordem de desenho** (§6.4) e a ordem
que `LaggedStart` vai usar. Não muda posição nenhuma.

---

## 4. `buff`: a gramática das margens

Quatro constantes, e usá-las em vez de números soltos é o que faz duas cenas
diferentes parecerem do mesmo material. [FONTE] categoria `constants`:

| Constante | Valor | px a 1080p | Uso típico |
|---|---|---|---|
| `SMALL_BUFF` | 0,1 | 13,5 | rótulo colado no seu objeto |
| `MED_SMALL_BUFF` | 0,25 | 33,75 | default de `next_to` e `arrange` |
| `MED_LARGE_BUFF` | 0,5 | 67,5 | default de `to_edge`; separar blocos |
| `LARGE_BUFF` | 1,0 | 135 | separar assuntos |

Regra prática que sai da tabela: **espaçamentos devem formar uma escala, não uma
nuvem.** Três blocos com 0,22, 0,25 e 0,3 de respiro não leem como "iguais";
leem como "torto". Escolha dois ou três valores para a cena inteira e nomeie-os
no topo do arquivo (§8.2) — que é exatamente o que o deck faz.

Onde `buff` NÃO é aditivo por lado:

- `SurroundingRectangle(mob, buff=b)` [FONTE] `geometry/shape_matchers.py:50-81`
  monta `width = group.width + 2*buff_x` — **`buff` por lado**, e aceita tupla
  `(buff_x, buff_y)`. `BackgroundRectangle` herda dele com `buff=0` e
  `fill_opacity=0.75`.
- `Mobject.surround(mob, buff=0.25)` [FONTE] `mobject.py:1936-1943` faz
  `scale((length + buff) / length)` — o buff é somado à medida TOTAL, então a
  folga por lado é **buff/2**. Os dois nomes iguais, duas semânticas. Se você
  quer moldura, use `SurroundingRectangle`.

---

## 5. `arrange` e `arrange_in_grid` — o layout automático que existe

### 5.1 `arrange` é um `next_to` encadeado

[FONTE] `:2598-2626`, o corpo inteiro:

```python
for m1, m2 in zip(self.submobjects[:-1], self.submobjects[1:], strict=True):
    m2.next_to(m1, direction, buff, **kwargs)
if center:
    self.center()
```

```
Mobject.arrange(direction=RIGHT, buff=0.25, center=True, **kwargs) -> Self
```

Três leituras diretas do corpo:

1. **Os `**kwargs` vão para o `next_to`.** Por isso
   `arrange(DOWN, aligned_edge=LEFT)` é válido — e é o idioma de coluna
   alinhada à esquerda, o mais usado do deck [DECK] (`tema.py:368`,
   `aula_001_custo.py:206`, `aula_001_mcp.py:488`, …).
2. **`center=True` joga fora a sua posição.** Depois de arranjar, o grupo pula
   para a ORIGEM. Se você já tinha posicionado, passe `center=False` — aí a
   âncora vira o PRIMEIRO filho, que não se move.
3. **Arranja `submobjects`, não a família.** Netos não entram.

O idioma completo, e a ordem importa: **arranje primeiro, ancore depois.**

```python
bloco = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
bloco.move_to([-6.21, -2.53, 0], aligned_edge=LEFT + UP)     # [DECK]
```

### 5.2 `arrange_in_grid` — e ele preserva a posição

```
Mobject.arrange_in_grid(rows=None, cols=None, buff=0.25,
                        cell_alignment=ORIGIN,
                        row_alignments=None, col_alignments=None,
                        row_heights=None, col_widths=None,
                        flow_order="rd", **kwargs) -> Self
```

[FONTE] `:2628-2882`. O que o corpo revela:

- **Ele guarda `start_pos = self.get_center()` e faz `self.move_to(start_pos)` no
  fim.** Ou seja: `arrange_in_grid` **preserva** a posição do grupo, enquanto
  `arrange` a destrói. Duas funções irmãs, comportamentos opostos, nenhuma
  documentação avisando.
- **Dimensão automática:** sem `rows` nem `cols`, `cols = ceil(sqrt(n))` e
  `rows = ceil(n/cols)`. Com poucos itens isso dá grade quase quadrada, o que
  quase nunca é o que uma cena de palestra quer — declare `cols=`.
- **`rows*cols < n` levanta `ValueError`**; sobra de células é preenchida por um
  `Mobject()` vazio de largura e altura 0, que é **pulado** na hora de posicionar
  (`if grid[r][c] is not placeholder`) mas continua consumindo a célula. Logo:
  **uma última linha incompleta fica encostada no começo do `flow_order`, nunca
  centralizada.** Se você quer os três últimos cartões centrados, é um segundo
  `arrange` só para eles.
- **`buff` aceita tupla** `(buff_x, buff_y)`.
- **`row_alignments` usa as letras `"ucd"`** (up/center/down) e
  **`col_alignments` usa `"lcr"`** (left/center/right), uma letra por linha ou
  coluna; tamanho errado levanta `ValueError`. `cell_alignment` é o fallback
  quando você não passa as strings.
- **`row_heights` / `col_widths`** aceitam `None` por posição — "esta linha eu
  fixo, as outras que se meçam".
- **`flow_order`** aceita exatamente `"rd" "dr" "ld" "dl" "ru" "ur" "lu" "ul"`
  (`:2813-2816`, com `ValueError` nomeando os oito). `"rd"` = preencher para a
  direita e depois para baixo.

```python
VGroup(*cartoes).arrange_in_grid(
    cols=3, buff=(0.4, 0.25),
    col_alignments="lcr", row_heights=[1.2, None],
)
```

### 5.3 Quando NÃO usar `arrange`

`arrange` responde "estes itens ficam um depois do outro e eu não me importo com
onde exatamente". Ele **não** responde:

- **"cada linha tem de cair numa altura fixa"** — porque o espaçamento é entre
  CAIXAS, e caixa de texto varia com as letras (§7). Aí é slot fixo (§8.4).
- **"a coluna da direita começa onde a da esquerda começa"** — `arrange` não
  conversa entre grupos. Use `align_to` entre os dois.
- **"quero reordenar depois sem remontar"** — `arrange` fixa posições; mudar a
  ordem exige chamar de novo, e se você já tinha ancorado, ancore de novo.
- **"o item do meio pode sumir"** — remover um filho e rearranjar move todos os
  outros. Numa cena em partes isso é uma emenda quebrada. [DECK] o padrão de lá
  é dar posição própria a cada peça e animar só a que muda.

---

## 6. Ordem de desenho e `z_index`

### 6.1 O mecanismo, em cinco linhas de fonte

[FONTE] `utils/family.py:12-42`, chamado pela câmera a cada frame
(`camera/camera.py:471-475`):

```python
extracted = remove_list_redundancies(
    list(it.chain(*(Mobject.family_members_with_points(m) for m in mobjects)))
)
if use_z_index:
    return sorted(extracted, key=lambda m: m.z_index)
return extracted
```

Leia na ordem em que acontece, porque cada passo tem consequência:

1. **Achata a família.** O `VGroup` deixa de existir na hora de pintar: o que vai
   para a lista são as FOLHAS com pontos.
2. **Remove duplicatas**, mantendo a primeira ocorrência.
3. **Ordena por `z_index` com `sorted`, que é ESTÁVEL.** Empate mantém a ordem de
   inserção.

### 6.2 As quatro regras que saem daí

1. **`z_index` é global e plano.** Como o achatamento vem ANTES da ordenação, um
   submobject com `z_index=5` lá dentro de um grupo é desenhado por cima de
   qualquer coisa com `z_index` menor que esteja FORA dele. Não existe
   "empilhamento local" como o `z-index` do CSS.
2. **`z_index` vence a ordem da cena, sempre.** `self.bring_to_front(x)` é
   [FONTE] `scene/scene.py:844-861` literalmente `self.add(x)` — reordena
   `self.mobjects`, e a reordenação só decide empates. Se `x` tem `z_index=0` e o
   retângulo tem `z_index=1`, `bring_to_front` não muda nada. **Este é o defeito
   nº 1 desta seção**: "eu mandei para a frente e continua atrás".
3. **`add_foreground_mobjects` também só reordena.** [FONTE] `:773-790` guarda a
   lista e reanexa no fim a cada `Scene.add`. Mesmo teto: perde para `z_index`.
4. **Ordem de inserção decide o resto.** Dentro de um `VGroup`, o filho de índice
   maior é desenhado depois — por isso o "prato" opaco de fundo entra ANTES do
   texto (§8.5). `Mobject.add_to_back(x)` põe na frente da lista (= atrás no
   desenho); `Scene.bring_to_back(x)` faz o mesmo no nível da cena
   (`scene.py:863-880`).

### 6.3 A API

```
Mobject.__init__(..., z_index: float = 0)                 # [FONTE] índice
Mobject.set_z_index(z_index_value, family=True) -> Self   # [FONTE] :3344-3384
Mobject.set_z_index_by_z_Point3D() -> Self                # usa o z do centro
Mobject.get_z_index_reference_point() -> Point3D
```

```python
Circle(z_index=2)                    # no construtor
rotulo.set_z_index(10)               # depois
```

**`family=True` é o default e propaga para todos os filhos.** Um
`grupo.set_z_index(3)` carimba o 3 em cada folha; se você depois quiser um filho
acima dos irmãos, tem de carimbá-lo de novo. E `set_z_index(3, family=False)`
num `VGroup` é quase sempre inútil: o pai não tem pontos, não é desenhado, e as
folhas continuam com o valor antigo.

`z_index` é `float` — dá para usar 1,5 para enfiar algo entre dois níveis sem
renumerar o resto.

A câmera tem o interruptor `Camera(use_z_index=True)` [FONTE]
`camera/camera.py:91,108`; com ele desligado só sobra a ordem de inserção. Não
mexa nisso a menos que saiba por quê.

### 6.4 Quando `z_index` é a resposta errada

- **Para dar fundo a um texto**, `z_index` não basta: você precisa de um objeto
  opaco atrás. É `BackgroundRectangle(texto)` ou
  `mob.add_background_rectangle(color=None, opacity=0.75, **kwargs)`
  [FONTE] `mobject.py:1979`, ou o prato manual de §8.5.
- **Para "sempre por cima" numa cena em partes**, carimbar `z_index` alto em
  tudo que é rótulo funciona até você precisar de duas camadas de rótulo. Melhor
  é declarar **três ou quatro níveis nomeados** no topo do arquivo
  (`Z_FUNDO = 0`, `Z_CORPO = 1`, `Z_ROTULO = 2`, `Z_DESTAQUE = 3`) e nunca
  escrever número solto.
- **Para 3D**, `z_index` não é profundidade: quem decide oclusão em
  `ThreeDScene` é a câmera. `set_z_index_by_z_Point3D()` é uma ponte grosseira
  entre os dois mundos. Assunto de **`manim-3d-camera`**.

---

## 7. Texto: a caixa é de TINTA, não de tipografia

Esta é a seção que explica por que colunas de texto ficam tortas no Manim
mesmo quando o código está "certo".

### 7.1 O mecanismo

[FONTE] `mobject/text/text_mobject.py:614-640`. Um `Text` é um `VGroup` de
glifos vindos de SVG; a caixa dele é o retângulo da **tinta desenhada**. O
`font_size` sequer é armazenado como medida: é **derivado da altura**.

```python
@property
def font_size(self) -> float:
    return (self.height / self.initial_height / TEXT_MOB_SCALE_FACTOR
            * 2.4 * self._font_size / DEFAULT_FONT_SIZE)

@font_size.setter
def font_size(self, font_val):
    self.scale(font_val / self.font_size)          # é um scale, nada mais
```

[FONTE] `TEXT_MOB_SCALE_FACTOR = 0.05` (`:83`) e `DEFAULT_FONT_SIZE = 48`; note
que 2,4/48 = 0,05, que é o que faz o getter devolver o valor pedido no momento da
construção. `Tex`/`MathTex` usam o mesmo esquema com
`SCALE_FACTOR_PER_FONT_POINT = 1/960` [FONTE] `tex_mobject.py:113-119`,
`constants.py:185`.

Consequências, todas [FONTE] por construção:

- **`Text("nome").height` depende das LETRAS.** Uma linha sem ascendente nem
  descendente ("_o o o_") é mais baixa que uma com "Ág". Mesmo `font_size`,
  alturas diferentes.
- **Não existe *baseline*.** O Manim não guarda métrica tipográfica nenhuma para
  `Text` e `Tex`; só a caixa de tinta. Não há `get_baseline()`.
- **Alinhar pelo centro alinha o centro da TINTA**, que sobe e desce conforme o
  texto. Duas legendas centralizadas lado a lado, uma com "g" e outra sem, ficam
  com a linha de base desencontrada.

### 7.2 O que isso quebra na prática

```python
VGroup(*linhas).arrange(DOWN, buff=0.2)
```

Parece um parágrafo. Não é: o `buff` é a distância entre **caixas de tinta**, e
a distância entre linhas de base fica irregular — apertada onde não há
descendente, folgada onde há. O olho lê isso como "espaçamento errado" sem saber
por quê.

### 7.3 Os quatro remédios, do mais barato ao mais correto

**1. Alinhe pela borda, não pelo centro.** Resolve o eixo horizontal por
completo:

```python
VGroup(*linhas).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
```

**2. Passo fixo em vez de fluxo.** Cada linha vai para uma altura declarada; a
variação de caixa deixa de importar. É o que o deck faz [DECK]
(`aula_001_custo_tarefa.py:167-173`: `Y_NOME`, `Y_FORN`, `Y_TOKENS`, `Y_FIO`,
`Y_RODAPE` — cinco alturas nomeadas, nenhuma calculada):

```python
for i, linha in enumerate(linhas):
    linha.move_to([X_MARGEM, Y0 - i * PITCH, 0], aligned_edge=LEFT)
```

**3. `Paragraph`, quando as linhas são um bloco só.** [FONTE]
`Paragraph(*text, line_spacing=-1, alignment=None, **kwargs)` — `alignment`
aceita `"left"`, `"center"`, `"right"` e resolve o alinhamento **dentro** do
bloco. (A classe é órfã de skill — §11.)

**4. Um *strut* deliberado**, quando você precisa de caixas de altura constante:
um retângulo invisível de altura fixa dentro do grupo, do jeito que o TeX faz.
**Isto é a armadilha de §2.5 usada DE PROPÓSITO** — e por isso exige um
comentário no código dizendo que o membro invisível é intencional, senão o
próximo editor o remove como lixo e o layout desmonta. Regra: strut é aceitável
quando ele é o ÚNICO invisível do grupo e está nomeado.

**Alinhamento óptico de verdade** — o ajuste fino em que uma aspa ou um "T"
saliente é puxado meio ponto para fora da margem para a coluna *parecer* reta —
não existe no Manim. Você faz na mão, com um `shift` pequeno, e não há régua que
o justifique além do olho. **[OPINIÃO, não medição]** o deslocamento que resolve
em textos de palestra costuma ficar entre 0,02 e 0,05 unidades (3 a 7 px a
1080p); acima disso já se percebe como erro.

A única classe da biblioteca com métrica de baseline real é `Typst`: [FONTE]
`Typst(typst_code, *, font_size=48, ..., track_baselines=False, ...)` e
`Typst.get_baseline_frame(submobject) -> (origem, direita, cima)`. Se um projeto
depende de alinhar fórmula com texto pela linha de base, é ali que existe
suporte — e é território **órfão** (§11), então confira antes de prometer.

Tudo sobre `t2c`, quebra de linha, fonte ausente e nitidez de glifo é de
**`manim-text-latex`**. Aqui só o que a caixa faz com o layout.

---

## 8. Layout que não quebra quando o conteúdo muda de tamanho

Cena de palestra é editada dezenas de vezes: um preço muda, um recado ganha uma
linha, um rótulo fica mais longo. Layout bom é o que **absorve** isso. Cinco
padrões, todos com origem em código de produção.

### 8.1 Ancore pela borda que NÃO pode se mexer

O princípio: quando um bloco cresce, ele cresce **para longe** da âncora. Se
você ancora pelo centro, ele cresce para os dois lados e come os dois vizinhos.

```python
# ERRADO: uma linha a mais no recado empurra o conteúdo de cima
recado.move_to([X_MARGEM, Y_RODAPE, 0])

# CERTO: cresce para BAIXO; nada acima se mexe
recado.move_to([X_MARGEM, Y_RODAPE, 0], aligned_edge=LEFT + UP)
```

O deck registrou o raciocínio no próprio arquivo [DECK]
(`aula_001_worktrees.py:172-175`):

> *"O recado cresce PARA BAIXO a partir de `CANTO_RECADO` (alinhado ao topo),
> então uma linha a mais de detalhe não empurra nada para cima."*

A tabela de decisão:

| O que pode crescer | Ancore por |
|---|---|
| lista/rodapé que ganha linhas | `LEFT + UP` (cresce para baixo) |
| valor numérico que ganha dígitos | `RIGHT` (cresce para a esquerda) |
| rótulo à esquerda de uma barra | `RIGHT` |
| título de uma ou duas linhas no topo | `LEFT + UP` |
| coluna que cresce a partir da base | `DOWN` |

### 8.2 Geometria em constantes, antes do `construct`

O padrão de produção [DECK]: 60 a 110 linhas de constantes nomeadas no topo de
cada arquivo de cena, com um mapa em ASCII das faixas e o quadro declarado
explicitamente.

```python
# Geometria — coordenadas do Manim (quadro de 14,22 × 8: x de −7,11 a +7,11,
# y de −4 a +4). Nada aqui é em fração da tela: o quadro é fixo.
#
#   coluna esquerda          faixa dos fios        o sistema
#   x ≈ −4,30                x de −2,95 a 0,42     x de 0,42 a 6,27
#   ─────────────────────────────── y = −2,35 (a divisória do rodapé)
X_MARGEM = -6.21          # espelha o to_edge(LEFT, buff=0.9) do slide
Y_DIVISORIA = -1.72       # nada desce daqui
```

Por que compensa: mover uma faixa inteira vira editar uma constante, e **revisar
o enquadramento passa a ser possível sem renderizar** — dá para conferir no
mapa se algo passa de 7,11 ou de 4,0.

A melhor peça desse padrão é o comentário que registra uma migração com o delta
[DECK] (`aula_001_worktrees.py:104-112`): *"TODAS as constantes de Y abaixo já
estão +0,8 ACIMA dos valores da versão com título… Se o título voltar um dia,
desça tudo −0,8."* Duas linhas que tornam uma decisão reversível.

E repare no `X_MARGEM = -6.21`: são `frame_x_radius − 0.9`, escolhidos para
espelhar a margem que o deck usa no HTML. **A margem do vídeo tem de ser a mesma
do slide que o contém**, senão o corte se vê na troca.

### 8.3 Posicione pelo corpo visível

§2.5, em uma linha: `grupo.shift(alvo - corpo.get_center())` ou
`next_to(..., submobject_to_align=corpo)`. É a regra que evita os 4 px [DECK].

### 8.4 Slot fixo em vez de fluxo, quando o conteúdo varia

Se a peça pode mudar de tamanho entre renders (um número que vem de JSON, um
rótulo traduzido), **não** encadeie `next_to` a partir dela: o resto da linha
inteira anda junto. Dê a ela uma posição própria e uma borda de ancoragem:

```python
# [DECK] aula_001_custo.py:391-397 — quatro colunas, quatro x fixos
amostra.move_to([0.40, y, 0], aligned_edge=LEFT)
nome   .move_to([0.82, y, 0], aligned_edge=LEFT)
valor  .move_to([4.60, y, 0], aligned_edge=RIGHT)   # números alinham à DIREITA
fatia  .move_to([5.90, y, 0], aligned_edge=RIGHT)
```

Coluna de número alinha pela direita; coluna de texto, pela esquerda. Com isso,
`$9,51` e `$11,03` continuam com as vírgulas na mesma vertical.

### 8.5 Quando o layout não cabe, decida onde ceder — não deixe estourar

Três saídas legítimas, nesta ordem de preferência:

1. **Tirar conteúdo.** Quase sempre a certa numa cena de palestra.
2. **Encolher com teto**, para o texto não virar ilegível:

```python
if bloco.width > LARGURA_MAX:
    bloco.scale_to_fit_width(LARGURA_MAX)
```
   Cuidado: `VMobject.scale(scale_factor, scale_stroke=False, ...)` [FONTE]
   `vectorized_mobject.py` — o traço **não** encolhe junto por default. Encolher
   um grupo 30% deixa as linhas proporcionalmente 30% mais grossas, e isso lê
   como "borrado". Dimensionamento em profundidade é de **`manim-mobjects`**.
3. **Quebrar em duas partes da cena.** Se dois recados não cabem, são dois
   momentos — regra de **`manim-presentation-parts`**.

E o padrão que resolve texto cruzando uma grade [DECK] — o **prato opaco**:

```python
prato = Rectangle(width=texto.width + 0.22, height=texto.height + 0.16,
                  fill_color=CANVAS, fill_opacity=1.0, stroke_width=0.0
                  ).move_to(texto.get_center())
grupo = VGroup(prato, texto)      # prato ANTES do texto: ordem = desenho (§6.2)
```

Ele não aparece: tem a cor do fundo daquela região e só apaga a grade atrás das
letras. A correção **não** é mover o número. (`SurroundingRectangle` e
`BackgroundRectangle` fazem o mesmo com API pronta, mas com a cor de fundo global
— o prato manual existe para quando a região tem cor própria.)

---

## 9. "Cabe na tela?" — conferir sem renderizar

### 9.1 `is_off_screen()` não responde essa pergunta

[FONTE] `mobject.py:1744-1752`:

```python
if self.get_left()[0] > config["frame_x_radius"]:  return True
if self.get_right()[0] < -config["frame_x_radius"]: return True
if self.get_bottom()[1] > config["frame_y_radius"]: return True
return self.get_top()[1] < -config["frame_y_radius"]
```

Ele devolve `True` só quando o objeto está **inteiramente fora**. Um retângulo
com metade do corpo cortado pela borda devolve `False`. Para enquadramento, o
que você quer é o contrário — que **caiba inteiro, com margem**:

```python
def cabe(mob, margem=0.3) -> bool:
    """True se o mobject inteiro está dentro do quadro, com folga."""
    return (mob.get_left()[0]   >= -config.frame_x_radius + margem
        and mob.get_right()[0]  <=  config.frame_x_radius - margem
        and mob.get_bottom()[1] >= -config.frame_y_radius + margem
        and mob.get_top()[1]    <=  config.frame_y_radius - margem)
```

Seis linhas, nenhum render, e pegam o defeito de enquadramento mais comum. Rodar
isso dentro do `construct` (e levantar `AssertionError` com o nome da peça)
transforma "cortou na borda" em erro de terminal — que é a única categoria de
defeito de layout que dá para automatizar. **[NÃO VERIFICADO]** — a função é
leitura direta dos getters de §2.1; não foi executada nesta redação.

Lembre da assimetria de §2.2: para um `VMobject`, esses getters usam âncoras, e
uma curva pode estufar um pouco além. Deixe a `margem` cobrir isso.

### 9.2 `shift_onto_screen` conserta, com um efeito colateral

[FONTE] `:1733-1743`. Para cada uma das quatro direções, se o centro da aresta
passou do limite menos o buff, ele chama `to_edge(vect)`. É um empurrão de
emergência — e ele **muda a posição relativa do objeto para todo o resto**, o
que numa cena em partes desalinha a emenda. Use para conferir, não como layout.

### 9.3 Réguas visuais que você desenha e apaga

| Régua | Assinatura [FONTE] | Para quê |
|---|---|---|
| `FullScreenRectangle()` | `mobject/frame.py` | os limites — **mas 16:9 fixo, veja §1.5** |
| `ScreenRectangle(aspect_ratio=16/9, height=4)` | `mobject/frame.py` | uma "tela dentro da tela" |
| `SurroundingRectangle(*mobs, color=PURE_YELLOW, buff=0.1, corner_radius=0.0)` | `geometry/shape_matchers.py:50` | ver a caixa de **alças** de um grupo — **não** a caixa que `next_to`/`align_to` usam (§2.2) |
| `BackgroundRectangle(*mobs, color=None, fill_opacity=0.75, buff=0)` | idem `:83` | fundo por trás de texto |
| `index_labels(mob, label_height=0.15, background_stroke_width=5, background_stroke_color=BLACK)` | `utils/debug.py:25` | descobrir o índice de cada submobject |
| `print_family(mob)` | `utils/debug.py:18` | a árvore no terminal, sem render |

`SurroundingRectangle` em volta de um grupo suspeito é o jeito mais rápido de
enxergar um membro invisível (§2.5): se a caixa é maior que o desenho, tem
alguém invisível dentro.

Duas notas sobre `index_labels`, as duas [FONTE] `utils/debug.py:74-82`:

- ele itera com `for n, submob in enumerate(mobject)`, e `Mobject.__iter__`
  **inclui o próprio nó** quando ele tem pontos (o mecanismo está em
  `manim-mobjects` §1.1). Num `Rectangle(grid_xstep=1)` o índice 0 é o próprio
  retângulo, não a grade.
- os números nascem brancos com contorno preto. **Em fundo branco eles somem
  dentro do contorno** — passe `index_labels(mob, color=BLACK,
  background_stroke_color=WHITE)`.

O ciclo completo de conferência (renderizar rápido, **olhar o PNG**, corrigir) é
de **`manim-verificacao-visual`**; o comando cru, de **`manim-render-api`**.
Esta skill entrega as consultas que respondem ANTES do render.

### 9.4 Vetores auxiliares que evitam trigonometria na mão

De `utils/space_ops` [FONTE], os que são de posicionamento:

```
midpoint(point1, point2)                    # o meio entre dois pontos
center_of_mass(points)                      # a média de uma nuvem
compass_directions(n=4, start_vect=RIGHT)   # n direções em volta do círculo
line_intersection(line1, line2)             # onde dois segmentos se cruzam
perpendicular_bisector(line, norm_vector=OUT)
normalize(vect, fall_back=None)
rotate_vector(vector, angle, axis=OUT)
```

`compass_directions(6)` distribui seis peças em círculo sem uma linha de seno.
O resto de `utils/space_ops` (36 funções) e todo o `utils/bezier` são de
**`manim-mobjects-customizados`**.

---

## 10. Armadilhas, em uma lista

Nenhuma levanta exceção. Cada linha custou pelo menos um render.

| Armadilha | Sintoma | Correção |
|---|---|---|
| **`align_to(m)` sem direção** | não acontece nada | o default é `ORIGIN`; passe `LEFT`/`UP`/… (§3.4) |
| **`next_to(m, RIGHT*2)`** | folga estranha, "quase certa" | é `buff × 2`, não 2 unidades (§3.3) |
| **`to_edge(UP*2)`** | margem dobrada | idem: `buff * direction` cru (§3.5) |
| **`aligned_edge` paralelo à direção** | os objetos se sobrepõem | `aligned_edge` ⟂ `direction` (§3.3) |
| **`arrange` depois de posicionar** | o grupo pula para a origem | `arrange(..., center=False)` (§5.1) |
| **`arrange_in_grid` sem `cols`** | grade quase quadrada inesperada | `cols = ceil(sqrt(n))` é o default (§5.2) |
| **`bring_to_front` não traz** | continua atrás | `z_index` vence a ordem da cena (§6.2) |
| **`set_z_index` num `VGroup`** | um filho fica fora da camada | `family=True` carimba todos; recarimbe o filho (§6.3) |
| **Membro invisível no grupo** | grupo desloca ~4 px [DECK] | posicione pelo corpo visível (§2.5) |
| **`arrange(DOWN, buff=…)` de texto** | entrelinha irregular | a caixa é de tinta; use passo fixo (§7.2) |
| **`move_to` centrado num bloco que cresce** | o conteúdo vizinho é empurrado | ancore por `LEFT + UP` (§8.1) |
| **`to_edge` numa `MovingCameraScene`** | some do enquadramento | `to_edge` é cego para a câmera (§3.5) |
| **`-r 1080x1920` para vertical** | conteúdo no meio, sobra em cima e embaixo | corrija `config.frame_width` (§1.5) |
| **`FullScreenRectangle` em 9:16** | o véu vaza dos lados | ele é 16:9 fixo (§1.5) |
| **`is_off_screen()` como teste de "cabe"** | metade cortada passa no teste | escreva o `cabe()` de §9.1 |
| **Coordenada 2D** | erro de broadcast do numpy | `[x, y, 0]`, sempre (§1.4) |
| **`mob.width` ≠ `get_right()−get_left()`** | encaixe não fecha | duas réguas diferentes (§2.2) |
| **`surround(buff=b)` vs `SurroundingRectangle(buff=b)`** | folga metade do esperado | `surround` divide o buff pelos dois lados (§4) |
| **`space_out_submobjects` num pai com pontos** | o pai fica escalado | só use em `VGroup` puro (§3.7) |
| **`index_labels` em fundo branco** | números invisíveis | `color=BLACK, background_stroke_color=WHITE` (§9.3) |

**A armadilha estrutural, que vale por todas:** layout errado não aparece no
terminal. Renderizar e não olhar a imagem é não ter terminado.

---

## 11. Onde esta skill para

| O assunto | A skill |
|---|---|
| que forma usar, `VGroup` × `Group`, submobjects, `scale_to_fit_*`, `match_width`, a caixa delimitadora como conceito, `Arrow`/`Brace`/`SurroundingRectangle` como objetos | **`manim-mobjects`** |
| animar o movimento, `.animate`, `Transform` × `ReplacementTransform` | **`manim-animations`** |
| `rate_func`, `lag_ratio`, `run_time`, `path_func`, composição | **`manim-composicao-ritmo`** |
| mover a CÂMERA, `self.camera.frame`, zoom, pan, `ZoomedScene` | **`manim-camera-2d`** |
| `phi`/`theta`, `move_camera`, `add_fixed_in_frame_mobjects`, 3D | **`manim-3d-camera`** |
| `Text` `Tex` `MathTex`, `t2c`, fonte, nitidez do glifo, quebra de linha | **`manim-text-latex`** |
| `Axes`, `c2p`, coordenadas de GRÁFICO (que não são as da cena) | **`manim-graphs-plots`** |
| grade de `Table`/`Matrix`, `v_buff`/`h_buff` | **`manim-tabelas-matrizes`** |
| layout automático de rede, `Graph(layout=…)`, `LayoutFunction` | **`manim-grafos-redes`** |
| cor, contraste, "sumiu no fundo branco", `set_default`, tema | **`manim-color-theming`** |
| `Scene.add`/`remove`/`bring_to_front`/`add_foreground_mobject`, seções, de qual `Scene` herdar | **`manim-cenas-secoes`** |
| escrever `VMobject` próprio, `utils/bezier`, o resto de `utils/space_ops`, booleanos | **`manim-mobjects-customizados`** |
| `SVGMobject`, `ImageMobject`, `register_font` | **`manim-svg-imagens`** |
| olhar o PNG, comparar frames, conferir o resultado | **`manim-verificacao-visual`** |
| cortar a cena em partes para slide, emenda, `next_section` | **`manim-presentation-parts`** |
| `ValueTracker`, updater que reposiciona a cada frame | **`manim-updaters-valuetracker`** |
| descobrir se um nome/kwarg existe, regenerar o índice | **`manim-api-discovery`** |
| renderizar, qualidade, formato, onde o arquivo saiu | **`manim-render-api`** |
| erro de ambiente, codec, LaTeX, traceback | **`manim-troubleshooting`** |
| o mapa geral, a ficha da máquina, precedência de config, o caso 9:16 medido (§10.3) | **`manim-project`** |

**Fronteiras que valem explicitar, porque são as que colidem:**

- **`manim-mobjects` × esta skill.** Lá: *que objeto é este e que tamanho ele
  tem*. Aqui: *onde ele fica*. `scale_to_fit_width` é de lá; `move_to` é daqui.
  A caixa delimitadora aparece nas duas: `manim-mobjects` §5.3 explica **de que
  ela é feita** (âncoras, traço que não conta, invisível que conta); esta skill
  explica **o que ela faz com o layout**. Não reescreva a de lá.
- **`manim-camera-2d` × esta skill.** Se a resposta for "mexe no objeto", é
  daqui. Se for "mexe no que se vê", é de lá. `to_edge` é daqui **e é cego para
  a câmera** — o par das duas skills é que fecha o assunto.
- **`manim-graphs-plots` × esta skill.** Um `Axes` tem um sistema de coordenadas
  PRÓPRIO; `ax.c2p(3, 5)` devolve um ponto DESTE plano. Converter é de lá; o que
  fazer com o ponto depois é daqui.
- **`manim-presentation-parts` × esta skill.** Lá: quando cortar. Aqui: por que
  um deslocamento de 4 px estraga a emenda.
- **`manim-color-theming` × esta skill.** A escala tipográfica e a paleta do
  `tema.py` são de lá (§11 daquela skill). Aqui ficam as constantes de
  GEOMETRIA — margem, divisória, passo, faixa — que moram no mesmo topo de
  arquivo mas respondem outra pergunta.

**Buracos declarados — não invente skill que não existe.** `Paragraph`, `Title`,
`Code`, `Typst`, `MathTypst`, `BulletedList` e `Variable` **não têm skill dona**
hoje, apesar de `Paragraph(alignment=…)` e `Typst(track_baselines=True)`
aparecerem aqui como ferramenta de layout — confira a assinatura no índice antes
de prometer comportamento. `LabeledPolygram`/`LabeledLine`/`LabeledArrow`
também são órfãs. Ênfase animada (`Flash`, `Indicate`, `Circumscribe`,
`FocusOn`), campos vetoriais e os 45 mobjects `OpenGL*` seguem sem dona.
