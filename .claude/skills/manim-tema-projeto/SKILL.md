---
name: manim-tema-projeto
description: >-
  O `tema.py` como CONTRATO do projeto: um módulo que toda cena importa e de
  onde saem paleta, pilha de fontes com fallback, escala tipográfica, curvas e
  tempos, os helpers obrigatórios de texto, a classe-base de cena e os números
  que vêm de arquivo. Use quando o pedido soar como "monta o tema do projeto",
  "cria o tema.py", "cada cena está com uma cara diferente", "deixa todas as
  cenas iguais", "padroniza cor e fonte das animações", "muda o azul do projeto
  inteiro", "de qual classe minhas cenas herdam?", "faz uma cena-base", "o
  fundo branco não pegou em todas as cenas", "as letras estão soltas/espaçadas",
  "o texto do vídeo está tremido", "a fonte do vídeo não é a do site/slide",
  "instalei a fonte e ficou pior", "onde eu ponho os números da animação?", "o
  preço do vídeo está diferente do slide", "quero acelerar todas as animações
  de uma vez", "esse `config` no topo do arquivo não faz efeito", "o `-ql` não
  mudou a qualidade", "o `--theme` não pegou". Cobre o funil obrigatório de
  texto com a correção da grade do cairo (`_texto_nitido`, medida e conferida
  no fonte), `Text.font_list()` e o booleano de honestidade `FONTE_EXATA`, a
  escala ancorada no palco de 8 unidades, a cena-base que fixa o fundo nos dois
  lugares e é a ÚLTIMA palavra, a precedência de config no topo do módulo (que
  DIVERGE entre `manim` e `mx`), o carregamento defensivo de dados, e a
  medição de quais tokens se sustentam e quais vazam. Traz um `tema_base.py`
  pronto para copiar. NÃO use para: escolher a cor, medir contraste, gradiente,
  alfa ou a varredura de `set_default` (`manim-color-theming`, dona da cor);
  escolher a CLASSE de texto, `t2c`, LaTeX ou `register_font`
  (`manim-text-latex`); o catálogo das 49 `rate_function` e a composição
  temporal (`manim-composicao-ritmo`); o formato em partes para slide
  (`manim-presentation-parts`); o mapa das classes de `Scene` e `next_section`
  (`manim-cenas-secoes`); posicionar e enquadrar (`manim-layout-posicionamento`);
  trazer SVG/PNG/fonte de arquivo (`manim-svg-imagens`); flags de render
  (`manim-render-api`); cache e custo (`manim-performance-cache`); olhar o PNG
  (`manim-verificacao-visual`); ambiente, `cwd` e wrappers `bin/`
  (`manim-project`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# `tema.py` — o contrato visual do projeto

Um projeto de Manim com mais de duas cenas tem um problema que não aparece em
nenhum log: **cada cena vira um projeto diferente**. Um cinza aqui, outro ali;
um `font_size=24` numa legenda e `22` na seguinte; uma animação em 0,8 s e a
irmã em 0,42; um `Text(...)` sem cor que some no fundo branco. Nada disso dá
erro, e nada disso é barato de consertar depois — a correção é um `sed` sobre
milhares de linhas que você não pode conferir sem renderizar tudo de novo.

O conserto é estrutural: **um módulo, importado por toda cena, que é o único
lugar do projeto onde existe um hex, um nome de fonte, um tamanho, uma curva de
easing e um número de negócio.** Esta skill é sobre esse módulo — o que entra
nele, o que não entra, quais partes se sustentam na prática e quais vazam.

## Como ler esta skill

| Marca | Significa |
|---|---|
| **[FONTE]** | lido no ManimCE 0.21.0 instalado em `.venv/lib/python3.12/site-packages/manim/` ou em `manimx/`, com arquivo e linha. Afirmação forte, **não executada** |
| **[HOJE]** | reproduzido nesta sessão, 2026-08-19, com `grep`/`awk`/`ast`/Python puro e um `import manimpango`. **Nenhum render, nenhum `ffmpeg`, nenhuma GPU** |
| **[DECK]** | medição feita no projeto consumidor `~/Projects/aulas`, em outra sessão. Testemunho confiável, **não reproduzido aqui** |
| **[DERIVADO]** | conta minha, encadeando peças [FONTE] e [DECK]. Dá o número certo se as peças estiverem certas — e traz o teste que o confirma |
| **não verificado** | está escrito assim de propósito |

## Cartão de referência — o pedido manda na seção

| O que pediram | Onde ler |
|---|---|
| "monta o tema", "cria o `tema.py`" | §2 (o arquivo pronto) → §3 (anatomia) → §14 (a ordem) |
| "as cenas estão cada uma de um jeito" | §1, e depois §4 e §7 — é o funil que resolve, não a boa intenção |
| "as letras estão soltas", "o texto saiu tremido" | §4 — o funil de texto, e o `finally` que não pode faltar |
| "a fonte do vídeo não é a do site" | §5 — e §5.2, porque instalar a fonte pode PIORAR |
| "que tamanho eu uso?" | §6, a escala ancorada no palco |
| "quero acelerar tudo de uma vez" | §7 — e a medição de por que o token de tempo vaza |
| "de qual classe eu herdo?" | §8 |
| "o fundo não pegou", "o `--theme` não pegou" | §8.1 — a cena-base é a última palavra, e isso é de propósito |
| "esse `config` no topo do arquivo não faz efeito" | §9.3 — `manim` e `mx` divergem, com o fonte dos dois |
| "o número do vídeo está diferente do do slide" | §10 |
| "mudei o JSON e o vídeo saiu igual" | §10.3 — o cache não enxerga arquivo externo |
| "o tema está pronto? dá para conferir sem renderizar?" | §13 |
| "posso pôr X no tema?" | §12, a lista do que NÃO entra |

---

## 1. A tese, e ela é medida: só se sustenta o que passa por uma FUNÇÃO

Este é o achado que muda o desenho de um tema, e ele saiu de contar o projeto
consumidor — 11 arquivos de cena, **8.197 linhas** de código de cena contra
**424 linhas** de `tema.py` (~5% do código) [HOJE, `wc -l`].

O `tema.py` desse projeto publica **as duas formas** de token: funções
(`txt()`, `legenda()`, `sobretitulo()`) e constantes nomeadas (`BASE`,
`RAPIDO`, `SAIDA`, `PAUSA`). Contando as ocorrências nas cenas [HOJE, `grep`]:

| Token | Forma | Ocorrências | Pelo tema | Vazou |
|---|---|---:|---:|---:|
| texto | **função** `txt`/`legenda`/`sobretitulo` | 184 | 184 | **0** |
| hex de cor | — (só existe no tema) | 0 | — | **0** |
| `font_size=` nas cenas | — | 0 | — | **0** |
| `rate_func=` | constante `SAIDA`/`ENTRA_SAI` | 214 | 213 | 1 (0,5%) |
| `run_time=` | constante `RAPIDO`/`BASE`/`LENTO` | 325 | 222 | **103 (31,7%)** |
| `self.wait(…)` | constante `PAUSA`/`PAUSA_LONGA` | 135 | 20 | **115 (85,2%)** |

Os literais que vazaram não são poucos nem arrumados: **34 valores distintos**
de `run_time` e **19** de `wait`, contra 3 velocidades e 2 pausas nomeadas. E
entre eles estão `0.3` e `0.30`, `0.5` e `0.50`, `0.8` (que É o `BASE`) escrito
seis vezes à mão [HOJE].

A leitura:

- **`Text(...)` não vazou nenhuma vez** porque `txt()` é a forma mais curta de
  obter um texto com cor e fonte certas — escrever `Text(x, font=FONTE,
  color=TINTA, font_size=T_CORPO)` na mão é mais trabalho, e não dá nada em
  troca;
- **`rate_func=SAIDA` quase não vazou** porque a alternativa
  (`rate_functions.ease_out_expo`) é mais longa;
- **`run_time=BASE` vazou um terço** porque `run_time=0.8` é mais curto;
- **`self.wait(PAUSA)` vazou 85%** porque `self.wait(0.4)` é mais curto e mais
  direto.

> **A regra de desenho de tema:** *o que você quer garantir tem que ser também
> o caminho mais curto.* Um token que exige digitar mais que o literal perde
> — sempre, e sem discussão de disciplina. Por isso o `tema_base.py` de §2 põe
> o ritmo em **métodos da cena-base** (`self.beat()`, `self.entra(...)`) e não
> só em constantes: `self.beat()` é mais curto que `self.wait(0.7)`, e é essa
> a única razão pela qual ele é usado.

O corolário incômodo: **um tema que só publica constantes é metade de um
tema.** Ele arruma a cor (porque a cor já vinha por função) e não arruma o
tempo.

---

## 2. O arquivo de apoio: `tema_base.py`

Ao lado deste `SKILL.md` mora **`tema_base.py`** (434 linhas, com comentário
denso) — um tema **completo e genérico**, pronto para copiar:

```bash
cp .claude/skills/manim-tema-projeto/tema_base.py <seu-projeto>/cenas/tema.py
```

O que ele já traz, funcionando: carregamento defensivo de dados + `numero()`,
paleta por PAPEL com os contrastes WCAG calculados no comentário, pilha de
fontes resolvida por `Text.font_list()` com o booleano `FONTE_EXATA`, escala de
7 degraus com a tabela de quanto cada um ocupa do quadro, **`_texto_nitido()`
inteiro e comentado**, o vocabulário de movimento, os helpers `txt`/`legenda`/
`sobretitulo`/`fio`/`coluna`, a classe `CenaBase` com `setup()`, `beat()` e
`entra()`, o `__all__` explícito e um autorrelato (`python tema.py`) que
imprime fonte resolvida, palco e escala **sem construir Mobject nenhum**.

O que está marcado com `TODO` e você precisa trocar: os hex, a pilha de fontes,
o caminho do JSON de dados e os sete tamanhos.

**Procedência do arquivo.** Ele é um port generalizado de dois `tema.py` reais
em produção (`~/Projects/aulas/aulas/001-multi-work/manim/tema.py`, 393 linhas,
e `.../002-deepseek-harness/manim/tema.py`, 424 — os dois idênticos exceto pelo
bloco de dados [HOJE, `diff`]), com a paleta e o domínio daquele projeto
removidos. Foi conferido por `py_compile` e por um passo de `ast` que prova que
todo nome do `__all__` existe e que não há import morto [HOJE]. **Não foi
executado nem renderizado** — ver §17.

---

## 3. Anatomia: as nove faixas de um tema, nesta ordem

A ordem importa porque o arquivo é lido de cima para baixo por quem chega, e
porque as faixas de baixo dependem das de cima.

| # | Faixa | O que publica | Por que existe |
|---|---|---|---|
| 1 | **Onde estão as coisas** | `RAIZ`, `PASTA` | o tema precisa achar o JSON de dados sem depender do `cwd` (§9.2) |
| 2 | **Dados** | `numero()`, o dict cru | número redigitado numa cena diverge do resto do projeto (§10) |
| 3 | **Paleta** | `CANVAS` `TINTA` `TINTA_2` `TINTA_3` `DIVISORIA` `ACENTO` + sinais | um nome por PAPEL; a cor em si é de `manim-color-theming` §11.1 |
| 4 | **Fontes** | `FONTE` `FONTE_MONO` `FONTE_EXATA` | o Manim cai para outra fonte em silêncio (§5) |
| 5 | **Escala** | `T_MEGA`…`T_MIUDO` | 7 degraus; qualquer número fora deles é deriva (§6) |
| 6 | **Nitidez** | `_TAMANHO_RENDER` `_PALCO_TEXTO` `_texto_nitido` | a grade do cairo (§4) |
| 7 | **Movimento** | `SAIDA` `ENTRA_SAI` `RAPIDO/BASE/LENTO` `PAUSA` | a assinatura temporal do projeto (§7) |
| 8 | **Helpers** | `txt` `legenda` `sobretitulo` `fio` `coluna` + formatação | o FUNIL — é aqui que a disciplina vira mecanismo (§1) |
| 9 | **Cena-base** | `CenaBase(Scene)` | fundo, ritmo, e a última palavra sobre config (§8) |

Fecha com **`__all__` explícito**. Não é burocracia: sem ele,
`from tema import *` despeja `json`, `Path`, `Any` e `rate_functions` no espaço
de nomes de cada cena, e a primeira variável local chamada `config` numa cena
vira um bug de meia hora.

---

## 4. O funil de texto — a única parte realmente inegociável

### 4.1 O defeito, em três linhas

`Text(font_size=22)` sai com as letras soltas das palavras: o cairo grava a
posição X de **cada glifo** arredondada para inteiro, e em 22 o em mede ~6,1
unidades de dispositivo, então meia unidade de arredondamento vale **±8% do em
por letra**. Erro proporcional a 1/tamanho — a legenda sofre, o `T_MEGA` quase
não.

**O fenômeno inteiro, com as três hipóteses derrubadas por medição (não é a
fonte, não é o peso sintético, não é o hinting do fontconfig), está em
`manim-project` §10.5 e em `manim-text-latex`. Não o reescreva.** Aqui interessa
outra coisa: **como isso vira contrato de projeto.**

A resposta é que a correção **não pode morar na cena**. Se o conserto for "toda
vez que você escrever um `Text`, lembre de desenhar em 720 e encolher", ele
falha na primeira cena que alguém escreve com pressa, e falha **sem erro** —
o texto sai, só sai feio. A correção mora no funil, e o funil é obrigatório.

### 4.2 A função, e o `finally` que não pode faltar

```python
_TAMANHO_RENDER = 720.0            # 720/3.6 = 200 unidades de dispositivo por em
_PALCO_TEXTO = (65536, 36864)

def _texto_nitido(conteudo: str, tamanho: float, **kw: Any) -> Text:
    largura, altura = config.pixel_width, config.pixel_height
    try:
        config.pixel_width, config.pixel_height = _PALCO_TEXTO
        mob = Text(conteudo, font_size=_TAMANHO_RENDER, **kw)
    finally:
        config.pixel_width, config.pixel_height = largura, altura
    return mob.scale(tamanho / _TAMANHO_RENDER)
```

**O `try/finally` é load-bearing.** `config.pixel_width` é global e vive o
processo inteiro. Uma exceção dentro do `Text(...)` — uma fonte que o Pango
recusa, um `t2c` mal formado — deixaria o render seguinte num palco de
65.536 px. Sem o `finally`, o sintoma aparece **três cenas depois**, e nada no
traceback aponta para cá.

**Chamar isto 184 vezes por render é seguro** porque o vaivém é geometricamente
inerte: `frame_width`/`frame_height` são valores independentes em
`config._d`, derivados de `pixel_*` **uma única vez**, quando o `.cfg` é
digerido — `self["frame_width"] = self["frame_height"] * self["aspect_ratio"]`
[FONTE: `_config/utils.py:673-677`] — e depois disso os setters de `pixel_width`
e `pixel_height` não os recalculam [FONTE: `_config/utils.py:1104-1146`].

### 4.3 O que o palco gigante compra — são três coisas, não uma

O `_PALCO_TEXTO` costuma ser lido como enfeite. Não é. [FONTE:
`text_mobject.py:834-863`] `_text2svg` passa `config["pixel_width"]` e
`["pixel_height"]` ao `manimpango.text2svg` como **largura e altura de quebra
de linha**. Consequências:

1. **Sem palco fixo, a quebra de linha fica amarrada à QUALIDADE do render.**
   Com o texto 30× maior, uma frase longa quebraria sozinha em `-ql` (1280) e
   não em `-qh` (1920). O preview e a entrega sairiam com layouts diferentes.
2. **O cache de disco piora isso.** [FONTE: `text_mobject.py:689-701`] o
   `_text2hash` monta a chave com `font+slant+weight+color+t2*+line_spacing+
   font_size+ligatures+gradient+text` — **`pixel_width` não entra** — e
   `_text2svg` faz `if file_name.exists(): reusa` **antes** de ler a resolução
   [FONTE: `:843-851`]. Um `-qm` e um `-qh` servem o SVG um do outro. Um palco
   constante tira a resolução da equação de vez. *(A anatomia dos dois caches
   é de `manim-project` §10.6 — inclusive o detalhe de que
   `Text(use_svg_cache=False)`, que é o default na 0.21
   [FONTE: `text_mobject.py:472`], desliga só o cache **de memória**; o de
   disco é incondicional.)*
3. **Brinde: o cache colapsa.** Como `_font_size` é sempre 720, a **mesma
   string** em `T_LEGENDA` e em `T_CORPO` passa a compartilhar **um** SVG em
   disco em vez de gerar dois [FONTE: o `str(self._font_size)` do
   `_text2hash`].

### 4.4 As quatro maneiras de furar o funil

Todas silenciosas. Escreva-as no seu `tema.py`, ao lado da função.

| Furo | O que acontece | Defesa |
|---|---|---|
| **`stroke_width > 0`** | `VMobject.scale` tem **`scale_stroke=False`** por padrão [FONTE, assinatura]. Um texto contornado sai daqui com o contorno em tamanho ORIGINAL — 2 pt de traço sobre um glifo encolhido 32× engole a letra | `Text` nasce com `stroke_width=0`, então o caso normal está certo. Se precisar de contorno, `.scale(f, scale_stroke=True)` |
| **`height=` / `width=`** repassados ao `Text` | [FONTE: `text_mobject.py:615-616`] `if height is None and width is None: self.scale(TEXT_MOB_SCALE_FACTOR)` — passar qualquer um dos dois **pula** o fator 0,05 e depois o seu `.scale()` ainda multiplica por 1/720. O texto some | não repasse; dimensione depois, fora do funil |
| **outra classe de texto** | Só `Paragraph` (`text_mobject.py:165`) e `Code` (que constrói `Paragraph`, `code_mobject.py:241-292`) constroem `Text` por dentro — e **não pelo seu funil**, então saem com o defeito de volta | um funil por classe: envolva `Paragraph`/`Code` como você envolveu `Text` |

**Correção nesta linha.** Uma versão anterior incluía `MarkupText` e `Variable`
na lista, e mandava dar-lhes o mesmo funil. **As duas estão erradas, e a receita
QUEBRA a primeira:**

- **`MarkupText` não constrói `Text`.** `text_mobject.py:876` é
  `class MarkupText(SVGMobject)` — **irmã** de `Text` (`:302`), não filha. E o
  `_text2svg` dela (`:1380-1417`) **nunca lê o `config`**: passa literais
  `600` de largura, `400` de altura e `pango_width=500`. Aplicar aqui o
  `_texto_nitido` — que sobe `font_size` contando com um palco que escala junto —
  desenha uma fonte enorme contra um orçamento fixo de 500 unidades, e a linha
  quebra em 2 a 5 caracteres. Mexer em `config.pixel_*` é no-op nesse caminho.
  `manim-text-latex` já documenta isso: *"NÃO funciona em `MarkupText`"* — esta
  skill defere a ela.
- **`Variable` não passa por `Text`**: o rótulo é `MathTex` e o valor é
  `DecimalNumber` (`numbers.py:352-380`), ou seja o caminho de **LaTeX**, que é
  justamente o que a linha seguinte desta tabela diz **não** sofrer o
  arredondamento do cairo. Era contradição interna.
| **`Tex`/`MathTex`** | não passam pelo Pango: vão por LaTeX → dvisvgm, com coordenadas fracionárias | **não precisam** de `_texto_nitido`. Precisam de um helper PRÓPRIO só para cor e tamanho [DERIVADO — a ausência do arredondamento em dvisvgm não foi medida aqui] |

### 4.5 Depois do encolhimento, `mob.font_size` diz a verdade

[FONTE: `text_mobject.py:621-639`] `Text.font_size` é uma **propriedade
derivada** de `self.height / self.initial_height`, não um registro. Então:

```python
t = _texto_nitido("Reversibilidade", T_LEGENDA)
t.font_size          # → 22.0, e não 720
```

E o setter é `self.scale(font_val / self.font_size)` [FONTE: `:633-639`] — o que
significa que **`mob.font_size = tamanho` é uma implementação equivalente** de
`.scale(tamanho / 720)`. Use a que preferir; a segunda é mais explícita sobre o
que está acontecendo.

O que **não** muda é `mob._font_size`: continua 720, e é ele que entra no hash
do cache (§4.3).

### 4.6 Cor: o funil também fecha o buraco nº 1 de fundo claro

[FONTE: `text_mobject.py:538`] `parsed_color = ManimColor(color) if color else
VMobject().color` — `Text` sem `color=` nasce **branco**. Em fundo claro isso é
texto invisível, sem erro, sem aviso. O `txt()` do template tem
`cor: str = TINTA` como padrão posicional: é impossível chamá-lo e obter texto
branco por descuido.

*A varredura de `set_default` que alcança as classes que **não** passam pelo seu
funil (`Circle`, `Rectangle`, `Dot`, `Line`…) é de `manim-color-theming` §11.2,
com a lista das 39 classes que hard-codam cor em §10.2. As duas coisas são
complementares: o funil cuida do que você constrói, o `set_default` do que a
biblioteca constrói por você.*

---

## 5. Fontes: a pilha, e o booleano de honestidade

### 5.1 `Text.font_list()` é a via portátil

```python
_PILHA_SANS = ["Inter", "Fira Sans", "Cantarell", "DejaVu Sans"]

def _primeira_disponivel(pilha: list[str]) -> str:
    try:
        instaladas = set(Text.font_list())
    except Exception:
        return pilha[-1]
    for nome in pilha:
        if nome in instaladas:
            return nome
    return pilha[-1]
```

[FONTE: `text_mobject.py:444-446`] `Text.font_list()` é um `staticmethod` que
devolve `manimpango.list_fonts()`. É **a mesma lista** que o próprio Manim
consulta para decidir se avisa — logo, é a única checagem que não pode
divergir do comportamento real.

**Prefira-a ao `fc-list`**, que é o que os `tema.py` de referência usam [DECK]:
`fc-list` é um binário do fontconfig (não existe fora de Linux/BSD), custa um
`subprocess` no import, e faz *matching* de família por string minúscula, o que
não é exatamente a regra do Pango.

**[HOJE]** nesta máquina: `manimpango.list_fonts()` devolve **411 famílias**;
`Fira Sans`, `Cantarell`, `DejaVu Sans`, `Ubuntu`, `Liberation Sans`,
`JetBrains Mono`, `Fira Mono` e `Noto Sans` estão presentes; **`Inter` e
`Inter Variable` não**. Ou seja: o projeto consumidor renderiza hoje em
Fira Sans, e o `FONTE_EXATA` dele é `False`.

### 5.2 A fonte que o objeto declara pode ser mentira

[FONTE: `text_mobject.py:476-491`] o construtor tenta variações de
maiúsculas/minúsculas, e se nada casar emite
`logger.warning(f"Font {font} not in {fonts_list}.")` — e **na linha seguinte
faz `self.font = font`**, guardando o nome que você pediu. O Pango cai para o
padrão do sistema; o objeto continua dizendo `'Inter'`.

Daí o `FONTE_EXATA`: um booleano que qualquer script de entrega confere **sem
renderizar**, e que responde "este vídeo casa 100% com a identidade, ou é uma
aproximação?".

### 5.3 A armadilha que inverte a intuição: instalar a fonte pode PIORAR

[DECK] Uma pilha que põe `"Inter"` antes de `"Inter Variable"` resolve para o
pacote estático. Se esse pacote vier com **uma face só** (Regular), o Pango
resolve `NORMAL`, `SEMIBOLD` e `BOLD` todos para a Regular: o `SEMIBOLD` some
e o `BOLD` vira embolden **sintético**, mais feio que o fallback que estava
lá antes.

Ou seja: `Text.font_list()` responde por **família**, e a decisão real é por
**face**. Uma detecção honesta precisaria checar pesos, não nomes — e nenhuma
das duas implementações de referência faz isso. Está aqui como buraco
declarado, não como receita.

*Carregar um `.ttf`/`.otf` que não está instalado no sistema é `register_font`
(um context manager, `mobject/text`), e mora em `manim-svg-imagens` (assets) e
`manim-text-latex` (a classe de texto). O tema só **escolhe**.*

---

## 6. A escala: sete degraus ancorados no palco, não na tela

```python
T_MEGA, T_DISPLAY, T_H2, T_H3, T_CORPO, T_LEGENDA, T_MIUDO = 96, 60, 44, 34, 28, 22, 18
```

Sete degraus, e **nenhum número fora deles**. O motivo não é estético: com uma
escala fechada, "aumenta um pouco esse rótulo" é uma decisão de UM passo, que
alguém revisa lendo o diff. Com números livres, viram 34 valores distintos —
exatamente o que aconteceu com o tempo no projeto consumidor (§1).

### 6.1 Quanto vale um `font_size` no palco

**[DERIVADO]**, e a cadeia é esta: o Manim entrega ao Pango `font_size/4.8` pt
[FONTE: `text_mobject.py:85,838`]; a superfície do cairo trabalha a 96 dpi, o
que dá `font_size/3.6` unidades de dispositivo por em [DECK, medido no SVG]; o
`SVGMobject` importa coordenadas SVG 1:1 em unidades de palco [FONTE:
`svg_mobject.py:30-31`, `_convert_point_to_3d` sem fator]; e o `Text` aplica
`TEXT_MOB_SCALE_FACTOR = 0.05` quando `height` e `width` são `None` [FONTE:
`text_mobject.py:83,615-616`]. Logo:

```
em (unidades de palco) = font_size / 72
```

| degrau | `font_size` | em (un) | % da altura do quadro (8,0) |
|---|---:|---:|---:|
| `T_MEGA` | 96 | 1,333 | 16,7% |
| `T_DISPLAY` | 60 | 0,833 | 10,4% |
| `T_H2` | 44 | 0,611 | 7,6% |
| `T_H3` | 34 | 0,472 | 5,9% |
| `T_CORPO` | 28 | 0,389 | 4,9% |
| `T_LEGENDA` | 22 | 0,306 | 3,8% |
| `T_MIUDO` | 18 | 0,250 | 3,1% |

**Confirme antes de confiar** (uma linha, sem render):

```python
from manim import Text
print(Text("Hxg", font_size=72).height)   # esperado: ~0,7 (altura de TINTA, não do em)
print(Text("Hxg", font_size=144).height / Text("Hxg", font_size=72).height)  # 2,0
```

*Não executado nesta sessão* — a proporção é trivialmente 2; o que a primeira
linha confirma é a ordem de grandeza da constante.

### 6.2 A tabela não muda com a qualidade — e isso é [FONTE]

O setter de `config.quality` escreve `frame_size` (os `pixel_*`) e
`frame_rate`, e **nunca** `frame_height`/`frame_width`
[FONTE: `_config/utils.py:1344-1352`]. O palco lógico é 8,0 × 14,222 em `-ql`,
`-qm`, `-qh` e `-qk`, igual. Portanto **a escala tipográfica do seu tema é
independente da qualidade do render**, e você pode calibrá-la olhando um PNG
de `-ql` — que é a única razão pela qual iterar rápido funciona.

*(A exceção: um projeto vertical 9:16 muda `frame_height`/`frame_width` no
`manim.cfg`, e aí toda a coluna de porcentagem muda junto. Enquadramento
vertical é de `manim-layout-posicionamento`; o que é seu é lembrar que a
escala **tem que ser recalibrada** quando o palco muda.)*

### 6.3 Uma régua para "cabe na linha?"

[DERIVADO] Um sans típico tem avanço médio de ~0,5 em por caractere. Numa linha
útil de ~12,4 unidades (o quadro de 14,222 menos ~0,9 de margem de cada lado):

| degrau | avanço médio (un) | caracteres por linha |
|---|---:|---:|
| `T_CORPO` 28 | 0,19 | ~64 |
| `T_LEGENDA` 22 | 0,15 | ~81 |
| `T_H2` 44 | 0,31 | ~41 |

Serve como sanidade na hora de escrever a frase, não como garantia — e cai
dentro da faixa clássica de 45–75 caracteres por linha, o que é um bom sinal de
que a escala está calibrada. **Quem decide de verdade é o PNG**
(`manim-verificacao-visual`).

---

## 7. Movimento: o vocabulário, e por que ele vaza

```python
SAIDA = rate_functions.ease_out_expo         # a curva-assinatura
ENTRA_SAI = rate_functions.ease_in_out_sine
RAPIDO, BASE, LENTO = 0.45, 0.8, 1.4
PAUSA, PAUSA_LONGA = 0.7, 1.4
```

**Uma curva de entrada, e só uma.** Trocar de easing por cena é o equivalente
temporal de trocar de fonte por slide: ninguém sabe nomear o que está errado,
mas o conjunto parece montado por três pessoas. Duas curvas bastam para
praticamente todo projeto — uma para o que entra e sai (assimétrica), uma para
o que vai e volta (simétrica).

**Por que os nomes, e não os números.** `run_time=0.8` espalhado por 8 mil
linhas é irrevisável; `run_time=BASE` diz *por que* aquele tempo. E "o vídeo
corre e ninguém lê" — a devolução mais comum de qualquer apresentador — vira
uma edição em um lugar só.

**Mas o token de tempo vaza** (§1: 31,7% em `run_time`, 85,2% em `wait`). A
correção que funciona não é insistir na constante, é **encurtar o caminho**:

```python
class CenaBase(Scene):
    def beat(self, longa: bool = False) -> None:
        self.wait(PAUSA_LONGA if longa else PAUSA)

    def entra(self, *animacoes, tempo: float = BASE, **kw) -> None:
        self.play(*animacoes, run_time=tempo, rate_func=SAIDA, **kw)
```

`self.beat()` tem 12 caracteres contra 17 de `self.wait(0.7)`; `self.entra(a)`
tem 14 contra 47 de `self.play(a, run_time=BASE, rate_func=SAIDA)`. É isso, e
não boa vontade, que decide.

> **Fronteira.** O que cada uma das **49** `rate_function` faz, `lag_ratio`,
> `LaggedStart`, `Succession`, `path_func`, orçamento de segundos e o
> desenho do ritmo de uma cena: **`manim-composicao-ritmo`**. O tema **nomeia**
> duas ou três curvas e três durações; ele não ensina a escolhê-las.

---

## 8. A cena-base

```python
class CenaBase(Scene):
    FUNDO: str = CANVAS

    def setup(self) -> None:
        config.background_color = self.FUNDO
        self.camera.background_color = self.FUNDO
        super().setup()
```

### 8.1 Por que dois lugares, e por que ela é a ÚLTIMA palavra

**Os dois são necessários, e por motivos diferentes** [FONTE]:

- `self.camera.background_color` é **quem pinta**. A câmera lê o `config` uma
  única vez, no próprio `__init__` (`camera/camera.py:134-142`), e o setter
  dela re-executa `init_background()` (`camera/camera.py:172-175`);
- `config.background_color` é **quem outros consultam** — em especial
  `BackgroundRectangle` sem `color=`, que sem isso vira uma placa opaca
  visível no meio da cena.

*A demonstração em pixel de que `config.background_color` dentro do
`construct` não faz nada é de `manim-color-theming` §7.4. Aqui interessa a
consequência de PROJETO, que é a seguinte:*

**Este `setup()` ganha de tudo.** A ordem, conferida no fonte:

```
Scene.__init__            → constrói renderer e câmera        [scene.py:200-216]
   (mx render) tempconfig(cfg) + apply_theme(...)             [manimx/render.py:417-425]
scene_class()             → a câmera nasce com o tema vigente
scene.render()
   └─ self.setup()        → ← O SEU TEMA, e ele sobrescreve   [scene.py:257]
   └─ self.construct()
```

*(`manim-project` §10.1 documenta o outro lado dessa ordem: o `--theme` é
aplicado DEPOIS do import da cena, e por isso ele também não alcança um mobject
construído no topo do módulo.)*

Consequência prática: **`--theme 3b1b` não escurece uma cena que herda da sua
base.** Isso é o comportamento certo (um projeto com identidade não deve ser
alterado por uma flag de conveniência) e é uma surpresa garantida para quem
esperava a flag ganhar. Escreva no docstring da classe. Se quiser deixar a
flag mandar, o caminho é `FUNDO = None` com um `if` no `setup()`, não tirar o
`setup()`.

Os 8 temas do `mx` e o `apply_theme` são de `manim-color-theming` §8.

### 8.2 O que entra na cena-base — e o que NÃO entra

| Entra | Por quê |
|---|---|
| `setup()` fixando o fundo | é o único lugar que roda antes de toda cena |
| atalhos de ritmo (`beat`, `entra`) | encurtam o caminho certo (§7) |
| um `FUNDO` sobrescrevível por classe | a cena de capa costuma querer outro |
| `tear_down()` de sanidade, se você tiver invariantes | roda mesmo quando a cena termina normalmente |

| **NÃO entra** | Por quê |
|---|---|
| **um `titulo()` que desenha cabeçalho** | é o antipadrão mais comum. Vídeo dentro de slide **não tem título interno** — quem dá contexto é o `h2` do slide, e o título duplicado rouba 15% da altura do quadro. O `tema.py` de referência tem um, e ele só sobrevive por causa de 4 cenas monolíticas antigas que ninguém consome [DECK]. Regra de palco: `manim-presentation-parts` §5.1 |
| geometria de uma cena específica | constantes de layout moram no topo do arquivo da cena (`manim-layout-posicionamento`) |
| o mixin de partes (`_corte`, `PARTE`) | é de `manim-presentation-parts`, e **o mixin não pode herdar de `Scene`** — misturá-lo com a base o faria aparecer em `mx scenes` e renderizar uma cena inteira por engano |
| `config.quality`, `pixel_*`, `frame_rate` | §9.5 |

### 8.3 Herança quando o projeto também usa cena em partes

A ordem das bases é load-bearing e falha em silêncio:

```python
class MinhaCenaP1(_AtosDoAssunto, CenaBase):   # mixin PRIMEIRO
    PARTE = 1
```

Invertida, o MRO resolve `construct` em `Scene` e **o mp4 sai com ~0 s, sem
erro** [DECK]. O mecanismo inteiro é de **`manim-presentation-parts`** §3.3 —
aqui só fica registrado que a cena-base do tema é a **última** base, nunca a
primeira.

---

## 9. Precedência: onde o tema pode falar, e onde ele é atropelado

`manim-project` §5 é dono da cadeia e do achado de que **o `cwd` é parte da
configuração**. Esta seção cobre o pedaço que ele delega: **`config` no topo do
módulo e `tempconfig`** — e traz uma divergência entre os dois front-ends que
não está escrita em lugar nenhum.

### 9.1 A cadeia

```
1. defaults da biblioteca (_config/default.cfg)
2. ~/.config/manim/manim.cfg
3. ./manim.cfg                      ← do CWD, não do arquivo da cena
4. flags da CLI
5. config.<chave> = … no topo do módulo (o seu tema.py)   ← posição VARIÁVEL, ver §9.3
6. tempconfig(...)
7. Scene.setup()                    ← a última palavra sobre o que ele escreve
```

### 9.2 O `manim.cfg` do projeto é relativo ao CWD

[FONTE: `_config/utils.py:79-85`]

```python
folder_wide = Path("manim.cfg")     # relativo, resolvido contra o cwd
return [library_wide, user_wide, folder_wide]
```

**Caminho relativo, nada de `__file__`.** Rodar de outra pasta perde o
`manim.cfg` do projeto **inteiro** e em silêncio — media_dir, qualidade,
cache. A consequência para o tema: **o `tema.py` não pode depender de nada que
esteja no `manim.cfg`.** Se um valor é identidade do projeto (a paleta, a
escala, a fonte), ele mora no `tema.py`, que é importado por caminho e portanto
imune ao `cwd`. O `manim.cfg` fica com o que é infraestrutura (pastas, cache,
encoders). A tabela do que se perde fora da raiz está em `manim-project` §5.

### 9.3 `config` no topo do módulo: `manim` e `mx` DIVERGEM

Este é o achado desta seção, e ele é [FONTE] nos dois lados.

**CLI da CE** — `manim render`:

```python
config.digest_args(click_args)                    # cli/render/commands.py:95
...
for SceneClass in scene_classes_from_file(file):  # :104 e :121 — IMPORTA o módulo
    with tempconfig({}):                          # dict VAZIO
        scene = SceneClass()
```

O módulo (e portanto o seu `tema.py`) é importado **depois** de as flags serem
digeridas, e o `tempconfig({})` não reintroduz nada. Logo: **`config.X = …` no
topo do módulo VENCE a flag da linha de comando.**

**Camada `manimx`** — `mx render`:

```python
classes = load_scene_classes(path)   # manimx/render.py:495 → IMPORTA o módulo aqui
...
with tempconfig(cfg):                # :417 — cfg SEMPRE contém "quality"  [:195-206]
    apply_theme(theme)               # :421-422
    scene = scene_class(); scene.render()
```

Aqui o `tempconfig` entra **depois** do import e **sempre** carrega `quality`
(mais `renderer`, `verbosity`, `disable_caching`, `transparent`…). Logo: **a
flag VENCE o `config.X = …` do topo do módulo.**

| Você escreveu `config.frame_rate = 30` no `tema.py` e rodou com `-q h` | Resultado |
|---|---|
| `bin/manim render cena.py C -qh` | **30 fps** — o tema ganhou, o `-qh` foi atropelado |
| `bin/mx render cena.py C -q h` | **60 fps** — a flag ganhou |

O mesmo arquivo, dois resultados, nenhum aviso. É por isso que §9.5 existe.

### 9.4 `tempconfig` — o que é seu

`tempconfig(temp: ManimConfig | dict[str, Any])` é um context manager
[FONTE, assinatura]. No tema ele serve para **uma** coisa: isolar uma alteração
global que precisa ser desfeita — é a mesma técnica do `try/finally` de
`_texto_nitido` (§4.2), com a diferença de que o `tempconfig` restaura o
`config` inteiro, e o `finally` restaura só as duas chaves que você mexeu.
Prefira o `finally` quando as chaves são conhecidas: é mais barato e não
esconde efeitos colaterais de terceiros.

O que **não** é seu: `tempconfig` para trocar qualidade/codec/pasta é
`manim-render-api`; para isolar cache é `manim-performance-cache`; o vazamento
de `set_default` **através** do `tempconfig` (ele não é restaurado, porque não
vive no `config`) é `manim-color-theming` §12.1.

### 9.5 A regra: o tema NÃO mexe em qualidade, resolução nem fps

Nunca escreva no topo de um `tema.py`:

```python
config.quality = "high_quality"     # ✗
config.pixel_width = 1920           # ✗
config.frame_rate = 60              # ✗
config.media_dir = "..."            # ✗ — infraestrutura, vai no manim.cfg
```

Com `bin/manim` isso torna `-ql` inoperante e você itera em 1080p60 sem saber
por quê; com `mx` funciona por acidente. **Identidade visual (cor, fonte,
escala, tempo) mora no tema; parâmetros de saída moram no `manim.cfg` e nas
flags.** A única chave de aparência que o tema escreve é `background_color`, e
mesmo essa ele escreve dentro do `setup()` (§8.1), não no topo do módulo.

---

## 10. Números: uma fonte só

### 10.1 O mecanismo

```python
def numero(id_: str, campo: str = "valor") -> Any:
    if id_ not in NUMEROS:
        disponiveis = ", ".join(sorted(NUMEROS)) or "(nenhum)"
        raise KeyError(f"número {id_!r} não existe em {_ARQUIVO_DADOS}. Existem: {disponiveis}")
    return NUMEROS[id_][campo]
```

O defeito que isso impede é específico e caro: **o vídeo dizendo `$9,51` e o
slide dizendo `$9,48` na parede**, porque alguém corrigiu o preço num lado só.
O JSON é lido pelos dois consumidores — no projeto de referência, por
`dados/custos.ts` (TypeScript, para o slide) e por `tema.py` (Python, para o
vídeo) [DECK].

**A mensagem lista os ids disponíveis.** É o que transforma um erro de digitação
de dez minutos de caça em dois segundos de leitura. Vale para qualquer
carregador de dados que você escreva, não só para este.

### 10.2 Carregamento defensivo — e por que a versão obrigatória foi abandonada

```python
DADOS = json.loads(_ARQUIVO.read_text("utf-8")) if _ARQUIVO.exists() else {}
NUMEROS = {n["id"]: n for n in DADOS.get("numeros", [])}
```

A primeira versão do projeto de referência exigia as chaves **no import**:
`PRECOS["modelos"]`, `PRECOS["cenario"]`… A segunda trocou tudo por `.get`, e o
comentário explica por quê [DECK, `tema.py:53-60`]:

> *"Um `KeyError` no import derrubaria TODAS as cenas do arquivo, não só a que
> usa o dado — por isso `.get`, e por isso `PRECOS` vazio é um estado válido."*

**A regra que generaliza:** *um módulo importado por todo mundo não pode falhar
no import por causa de dado que a maioria dos importadores não usa.* Falhe
tarde, na função que consome, e com mensagem. Isso vale para o JSON, para a
detecção de fonte (por isso o `except Exception` no `_primeira_disponivel`) e
para qualquer leitura de ambiente que o tema faça.

### 10.3 O cache não enxerga o seu JSON

O Manim reaproveita *partial movies* por hash da chamada de `play`. Esse hash
**não** vê o conteúdo de um arquivo externo. Corrigiu o número, re-renderizou e
o vídeo saiu igual? É isso. Passe `--disable_caching` (ou `--no-cache` no `mx`)
em qualquer cena que leia dado de fora. A anatomia do cache e as chaves de poda
são de **`manim-performance-cache`**; o pitfall está registrado em
`manim-project` §10.7 e `manim-render-api`.

### 10.4 Formatação de rótulo mora no tema, não na cena

```python
def usd(valor: float) -> str: ...      # 1102.5 → "$1.102"  (sem centavos acima de 100)
def vezes(valor: float) -> str: ...    # 116.0  → "116×"
```

São regras de apresentação, e por isso são do tema — a mesma razão pela qual a
cor é. O corte de centavos acima de 100 é uma decisão de **palco** ("na parede
ninguém lê centavo"), não de domínio, e ela tem que valer para todas as cenas
ou não vale para nenhuma [DECK].

---

## 11. Espelhar um front-end: espelhe o PAPEL, nunca o número

Quando o vídeo entra dentro de um site, deck ou app, o tema do Manim vira o
**espelho** de um arquivo de tokens do outro lado (`tokens.ts`, `theme.css`,
`tailwind.config`). A tentação é copiar os valores. Não copie: os dois lados
medem em unidades diferentes.

No projeto de referência [HOJE, lendo `src/styles/tokens.ts`]:

| | front-end | Manim |
|---|---|---|
| unidade | px num palco CSS de 1280 | `font_size` num palco de 14,222 × 8 |
| `h2` | 40 px | `T_H2 = 44` |
| `legenda` | 17 px | `T_LEGENDA = 22` |
| cor | `#1d1d1f` | `#1D1D1F` — **essa sim é idêntica** |
| fonte | pilha CSS com `-apple-system`, `.woff2` do npm | **um** nome que o fontconfig resolva |

**O que espelha exatamente:** a cor (é a mesma coordenada nos dois espaços) e
os nomes dos papéis. **O que não espelha:** tamanho, entrelinha, espaçamento,
e a família — o Pango não lê `.woff2`, então a fonte do site pode
simplesmente não existir para o Manim (§5). O que se conserva é a **razão entre
degraus**, não o valor.

Escreva isso no topo do seu `tema.py`, apontando o arquivo espelhado pelo
caminho. É a única defesa contra alguém "sincronizar" os dois copiando números.

---

## 12. O que NÃO vai no tema

| Coisa | Onde vai |
|---|---|
| geometria de uma cena (coordenadas, larguras de faixa) | bloco de constantes no topo do arquivo da cena |
| um `titulo()` que desenha cabeçalho | lugar nenhum, em vídeo de slide (§8.2) |
| a fórmula de negócio de UMA cena | a cena, ou um módulo de domínio ao lado — o tema carrega o **dado**, não a regra |
| `config.quality` / `pixel_*` / `frame_rate` / `media_dir` | `manim.cfg` e flags (§9.5) |
| o mixin de partes (`_corte`, `PARTE`) | `manim-presentation-parts` |
| a varredura de `set_default` sobre 39 classes | `manim-color-theming` §11.2 (pode ser chamada do tema, mas o código é de lá) |
| helpers de anotação (`Brace`, `SurroundingRectangle`, seta que aponta) | hoje **órfãos**; ver §16 |
| qualquer coisa que precise renderizar para decidir | nada decide render no import |

---

## 13. Conferir o tema sem renderizar nada

Cinco checagens, todas em milissegundos, todas pegando defeito silencioso.

**1. Nenhum hex fora do tema.**

```bash
grep -rnE '#[0-9A-Fa-f]{3,8}\b' cenas/*.py | grep -v tema.py     # esperado: nada
```

**2. Nenhuma constante nativa de cor nas cenas** (o caso mais comum em fundo
claro — `WHITE` é o default e some):

```bash
grep -rnE '\b(WHITE|BLACK|YELLOW|BLUE|RED|GREEN|TEAL|GOLD|ORANGE)\b' cenas/*.py | grep -v tema.py
```

**3. Nenhum texto fora do funil, e nenhum tamanho solto.**

```bash
grep -rnE '\bText\(|\bMarkupText\(|font_size *=' cenas/*.py | grep -v tema.py
```
No projeto de referência isso devolve **0 linhas** em 8.197 linhas de cena
[HOJE].

**4. O tema é honesto sobre a fonte** — sem construir Mobject nenhum:

```bash
python cenas/tema.py       # o autorrelato do tema_base.py
```
Imprime a fonte resolvida, `FONTE_EXATA`, o palco, os pixels e a escala com a
porcentagem de altura de cada degrau.

**5. Quanto do tempo passa pelo tema** (a métrica de §1, para o seu projeto):

```bash
tot=$(grep -ohE 'run_time *= *[A-Za-z0-9_.]+' cenas/*.py | wc -l)
nom=$(grep -ohE 'run_time *= *(RAPIDO|BASE|LENTO)' cenas/*.py | wc -l)
echo "run_time nomeado: $nom / $tot"
grep -ohE 'run_time *= *[0-9][0-9.]*' cenas/*.py | sed 's/.*= *//' | sort -u | wc -l   # valores distintos soltos
```
Se o número de valores distintos passar de meia dúzia, o tema perdeu o tempo —
e a correção é §7, não uma conversa sobre disciplina.

**O que essas checagens NÃO pegam:** contraste ruim, texto cortado pela borda,
sobreposição, fonte trocada por fallback no meio de uma frase. Isso só o PNG
mostra — **`manim-verificacao-visual`**, e o ciclo é *escrever → renderizar
rápido → OLHAR o PNG → corrigir → render final*.

---

## 14. Receita: tema novo, na ordem que evita retrabalho

1. **Decida claro ou escuro antes do primeiro Mobject.** Trocar depois é
   reauditar a paleta inteira, porque contraste não é simétrico
   (`manim-color-theming` §5.3: das 89 cores nativas, 68 passam AA sobre preto,
   21 sobre branco, **nenhuma nos dois**).
2. **Copie o `tema_base.py`** para `cenas/tema.py`.
3. **Troque os sete hex** e rode a auditoria de contraste
   (`manim-color-theming` §5.2). Cole o resultado como comentário ao lado das
   constantes — assim ninguém muda um valor "só um tiquinho" sem ver a conta.
4. **Escolha a pilha de fontes** e rode `python cenas/tema.py`. Se
   `FONTE_EXATA` sair `False` e isso importar, resolva agora (§5), não depois
   de 12 cenas.
5. **Calibre a escala** com UMA cena de teste e um `--format png` em `-ql`:
   a `T_LEGENDA` é legível no destino real? O `T_H2` cabe em duas linhas?
   A tabela de §6.1 dá o chute inicial; o PNG decide.
6. **Escolha a curva e as três durações.** Uma curva de entrada, e só uma.
7. **Escreva a `CenaBase`** com `setup()` e os atalhos de ritmo (§7).
8. **Só então escreva a primeira cena de verdade** — e ela não deve conter
   nenhum hex, nenhum `font_size=`, nenhum `Text(`, nenhum nome de fonte.
9. **Rode as cinco checagens de §13** antes do primeiro commit. Elas são
   baratas e só ficam mais caras depois.

---

## 15. Sintomas → causa

| Sintoma | Causa provável | Seção |
|---|---|---|
| as letras se soltam das palavras, pior nas legendas | texto fora do funil, ou funil sem `_texto_nitido` | §4 |
| o texto sumiu no fundo claro | `Text` sem `color=` nasce branco | §4.6 e `manim-color-theming` §10 |
| um texto do projeto saiu com outra letra | `Paragraph`/`Code` não passam pelo funil (e `MarkupText` não pode passar — §4.4) | §4.4 |
| o texto encolheu até virar um risco | `height=`/`width=` repassados ao `Text` | §4.4 |
| um título contornado ficou ilegível | `scale_stroke=False` | §4.4 |
| a fonte mudou entre duas máquinas | pilha caiu para outro item; `FONTE_EXATA` é `False` | §5 |
| instalei a fonte e o SEMIBOLD sumiu | família com uma face só | §5.3 |
| o fundo saiu preto em uma cena e branco em outra | a cena não herda da base, ou define `setup()` sem `super()` | §8.1 |
| o `--theme` não pegou | a base é a última palavra — de propósito | §8.1 |
| o `-ql` não mudou nada | `config.quality`/`pixel_*` no topo do módulo, sob `bin/manim` | §9.3, §9.5 |
| a mesma frase quebra linha em `-ql` e não em `-qh` | `_PALCO_TEXTO` ausente, ou SVG servido do cache | §4.3 |
| corrigi o JSON e o vídeo saiu igual | cache de partial movie | §10.3 |
| o mp4 saiu com ~0 s e sem erro | ordem das bases invertida numa cena em partes | §8.3 |
| todo mundo importa o tema e nada funciona | `KeyError` no import por dado ausente | §10.2 |

---

## 16. Onde esta skill para

| Assunto | Skill dona | A fronteira, em uma frase |
|---|---|---|
| cor, contraste, gradiente, alfa, `set_default`, os 8 temas | **`manim-color-theming`** | ela decide **qual** cor e prova que dá para ler; eu decido **onde a cor mora** e quem a importa. §11 de lá (paleta) e §3 daqui (papéis) são o mesmo assunto visto de dois lados — não reescreva nenhuma das duas |
| a classe de texto, `t2c`, `{{ }}`, LaTeX, `register_font`, a nitidez do glifo | **`manim-text-latex`** | ela é dona do fenômeno e da API; eu sou dono do **funil obrigatório** que faz a correção valer para o projeto inteiro |
| as 49 `rate_function`, `lag_ratio`, `AnimationGroup`, `path_func`, ritmo | **`manim-composicao-ritmo`** | eu **nomeio** duas curvas e três durações; ela ensina a escolhê-las |
| o catálogo de animações, `Transform`, `.animate` | **`manim-animations`** | — |
| o formato em partes, `_corte`, a emenda, a granulação | **`manim-presentation-parts`** | a base do tema é a **última** base do MRO, nunca a primeira (§8.3) |
| o mapa das 13 classes de `Scene`, ciclo de vida, `next_section` | **`manim-cenas-secoes`** | ela diz de qual herdar; eu digo o que pôr dentro da SUA |
| posicionar, margens, "cabe na tela?", 9:16, z-index | **`manim-layout-posicionamento`** | a escala do tema muda quando o palco muda (§6.2) |
| SVG, PNG, `ImageMobject`, carregar um `.ttf` | **`manim-svg-imagens`** | o tema **escolhe** a fonte; carregar arquivo é de lá |
| `mx render`, qualidade, formato, caminho da saída | **`manim-render-api`** | a §9.5 **desta** skill: o tema não escreve parâmetro de saída |
| cache, `hash_obj`, custo de rasterizar | **`manim-performance-cache`** | §10.3 |
| olhar o PNG, medir o quadro, o ciclo de verificação | **`manim-verificacao-visual`** | §13 lista o que se pega sem render; o resto é lá |
| ambiente, `cwd`, wrappers `bin/`, a ficha da máquina | **`manim-project`** | §9.2 é o recorte do tema; a cadeia inteira é §5 de lá |
| codec, NVENC, peso do arquivo | **`manim-gpu-encoding`** | — |
| lote, pôsteres, o que entra no git | **`manim-batch-pipeline`** | — |

**Buracos declarados** — se o pedido cair aqui, diga que não há skill, não
improvise: ênfase e anotação (`Brace`, `SurroundingRectangle`, `Indicate`,
`Flash`, `Circumscribe`); `Code`, `Typst`, `Paragraph`, `Variable` na tela;
campos vetoriais e fluxo; `LinearTransformationScene`/`VectorScene`; os 48
mobjects `OpenGL*`; e uma skill dedicada à precedência de config (existe em
migalhas: `manim-project` §5, esta §9, `manim-performance-cache`).

---

## 17. O que NÃO foi verificado nesta sessão

Nenhum render, nenhum `ffmpeg`, nenhuma GPU, nenhum `mx bench` — por
proibição explícita. Em concreto:

1. **O `tema_base.py` não foi executado.** Passou por `py_compile` e por uma
   checagem `ast` (todo nome do `__all__` existe; nenhum import morto) [HOJE].
   Um `python tema.py` na sua máquina é o primeiro teste, e ele não renderiza
   nada.
2. **Os números de nitidez (5,53% → 0,13% rms, 43×) são [DECK]**, medidos em
   outro projeto e outra sessão. O **mecanismo** é [FONTE] e pode ser afirmado;
   a magnitude não foi reproduzida aqui.
3. **`em = font_size / 72` é [DERIVADO]**: o fator 0,05 e a ausência de
   conversão de unidade no import de SVG são [FONTE]; o `font_size/3.6` de
   unidades de dispositivo por em é [DECK]. §6.1 traz a linha que confirma.
4. **A régua de caracteres por linha (§6.3) é estimativa**, não medição — o
   avanço médio de 0,5 em varia com a fonte e com a frase.
5. **A afirmação de que `Tex`/`MathTex` não sofrem o arredondamento do cairo**
   é [DERIVADO] do caminho LaTeX → dvisvgm. Nenhum SVG de `MathTex` foi
   inspecionado aqui.
6. **A tabela de divergência `manim` × `mx` (§9.3)** é [FONTE] nos dois lados
   (`cli/render/commands.py:95,104` e `manimx/render.py:195-206,417,495`), mas
   **não foi executada**. Se for decidir algo caro sobre ela, confirme com um
   render de 1 s.
7. **Os contrastes WCAG do `tema_base.py`** são aritmética pura sobre os hex
   [HOJE], não pixel medido em PNG.
