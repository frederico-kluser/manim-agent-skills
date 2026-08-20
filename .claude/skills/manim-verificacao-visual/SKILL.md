---
name: manim-verificacao-visual
description: >-
  Provar que a cena Manim ficou CERTA sem assistir ao vídeo inteiro: renderizar
  um quadro só, OLHAR a imagem, e medir quando o olho não basta — cobertura de
  tinta (pôster e PDF em branco), tinta encostando na borda, enquadramento
  conferido sem renderizar nada, e a comparação DIRECIONAL entre dois quadros
  (antes/depois, emenda entre partes). Use SEMPRE que a frase for "confere se
  ficou bom", "renderiza uma imagem para eu ver", "olha esse frame", "como eu
  sei que não cortou?", "o texto sumiu no fundo", "o PDF
  saiu em branco nesse slide", "o pôster do vídeo está vazio", "compara com o
  render anterior", "mudei o código, o que mudou na tela?", "a emenda entre as
  partes piscou", "sumiu um desenho e não deu erro", "tem sobreposição?", "antes
  de commitar o vídeo, o que eu confiro?", "isso saiu em 720p sem querer?".
  Traz a escada de conferência do mais barato ao mais caro, como pegar
  exatamente o quadro que interessa, a lista dos defeitos que NÃO levantam
  exceção nenhuma, a prova no fonte de que `is_off_screen()` não é um teste de
  enquadramento, a métrica direcional e por que RMS e SSIM mentem aqui, as
  tolerâncias do próprio comparador de frames do ManimCE, e quatro ferramentas
  em `assets/`. NÃO use para: ler traceback, exit code, cache servindo resultado
  velho ou render que falhou (`manim-troubleshooting`); escolher qualidade,
  formato e caminho de saída (`manim-render-api`); a conta de contraste WCAG e o
  desenho da paleta (`manim-color-theming`); a emenda como parte do FORMATO em
  partes e a manutenção dele (`manim-presentation-parts`); a emenda entre PARTES de um vídeo de slide — o formato, a régua
  calibrada e o conferidor são de `manim-presentation-parts` §7, que nasceu
  com eles; aqui fica só a generalização para um par antes/depois qualquer;
  "isso CABE na tela?" ANTES de renderizar — margem, `arrange`, encolher o
  bloco — é `manim-layout-posicionamento` §9 (aqui só se PROVA, no pixel que
  saiu, que não coube); as conferências de
  LOTE — contagem, uniformidade, extração de pôster (`manim-batch-pipeline`);
  codec, GPU e peso do arquivo (`manim-gpu-encoding`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Verificação visual — renderizou e não olhou, não terminou

O Manim tem uma propriedade que muda como se trabalha com ele: **quase nenhum
defeito visual levanta exceção.** Texto branco em fundo branco sai com
`success: true`. Um título cortado ao meio pela borda sai com `success: true`.
Dois blocos sobrepostos, uma barra estourando o eixo, uma fonte trocada em
silêncio, um pôster em branco que vira página vazia no PDF de backup — todos
saem com `success: true`, exit 0, e um log que diz `File ready at …`.

O exit code prova que o **programa** rodou. Ele não prova nada sobre a
**imagem**. Esta skill é sobre fechar esse buraco: como pegar o quadro certo,
como olhar, e o que medir quando o olho não basta.

## Procedência do que está escrito aqui

Três marcadores, e valem para o arquivo inteiro:

- **[FONTE]** — lido hoje (2026-08-19) no ManimCE 0.21.0 instalado em
  `.venv/lib/python3.12/site-packages/manim/`, ou no índice estático de `api/`.
  Vem com arquivo e linha. Afirmação forte.
- **[DECK]** — medição feita no projeto consumidor `~/Projects/aulas`, em outra
  sessão. Testemunho confiável, **não reproduzido aqui**.
- **[NV]** — leitura de código sem execução, ou afirmação que depende de rodar.

**Nesta sessão nenhum render, nenhum `ffmpeg`, nenhum benchmark e nenhuma GPU
foram executados.** Os quatro scripts de `assets/` passaram por
`python -m py_compile` e nada além disso. Todo comando neste arquivo é para
**você** rodar; eu não rodei nenhum.

## Cartão de referência — o sintoma manda na seção

| O que aconteceu | Onde ler |
|---|---|
| "renderizei; e agora, como sei que está certo?" | §1, a escada |
| quero um PNG para olhar, rápido | §2.2 |
| quero o quadro de um instante específico, não o último | §2.3 e §2.4 |
| `mob.save_image()` estourou um `KeyError` | §2.5 |
| o PNG bom sumiu depois de um preview | §2.6 |
| "eu OLHO como?" (sou um agente) | §3.1 |
| o PDF/pôster saiu em **branco** | §4.1 |
| sumiu texto e não deu erro | §4.2 e §5.7 |
| **cortou na borda** | §4.3 (pixel) e §5 (sem render) |
| `is_off_screen()` disse que está tudo bem e não está | §5.1 — ele não faz o que você acha |
| dois desenhos sobrepostos | §4.4 |
| um `VGroup` desloca 4 px sem motivo | §5.4 |
| "mudei o código; o que mudou na tela?" | §6 |
| a emenda entre partes piscou | §6.2 e §6.3 (o formato é `manim-presentation-parts`) |
| RMS/SSIM acusou defeito e a imagem está boa | §6.1 |
| o vídeo saiu em 720p30 sem querer | §7 |
| "o que eu confiro antes de commitar?" | §9 |

---

## 0. A lista: o que NÃO dá erro nenhum

Decore esta tabela. Ela é o motivo da skill existir.

| Defeito | Por que o terminal cala | Como se pega |
|---|---|---|
| texto/forma na cor do fundo | o Manim escreve **branco** por padrão; em tema claro isso é invisível e legal | §4.1, §4.2 |
| `fill_opacity=0` num `VMobject` | é o **default** de `VMobject` (`fill_opacity: float = 0.0`) [FONTE] | §4.1 |
| elemento cortado pela borda | o cairo não desenha o que caiu fora do buffer; `is_off_screen()` é `False` | §4.3, §5.1 |
| dois textos sobrepostos | são dois desenhos válidos no mesmo lugar | §4.4 |
| fonte ausente trocada por Noto Sans | warning, e `t.font` continua devolvendo o nome pedido (`manim-project` §10.4) | §3.2, e comparar com o render anterior (§6) |
| pôster/PDF em branco | o último quadro é um `FadeOut` — é um quadro válido | §4.1 |
| preview 720p30 comitado por cima da entrega | os dois caminhos são legítimos | §7 |
| emenda que perde tinta entre partes | os dois vídeos existem e tocam | §6.2 |
| `VGroup` deslocado por submobject invisível | o transparente conta na caixa delimitadora | §5.4 |
| cena inteira pulada → **nenhum** mp4 | `combine_to_movie` desiste e loga em INFO | `manim-presentation-parts` §10 |
| MRO invertido → cena vazia | `Scene.construct` é só docstring [FONTE] | `manim-presentation-parts` §3.3 |

Repare no padrão: **todos são estados legais do programa.** Não existe conserto
no nível de exceção; só medição.

---

## 1. A escada de conferência

Do mais barato ao mais caro. Suba um degrau só quando o de baixo estiver limpo —
e note que os dois primeiros degraus nem renderizam.

| # | Degrau | Custo | O que PROVA | O que não prova |
|---|---|---|---|---|
| 0 | conferidor estático (AST, `grep`) | ms | estrutura: corte órfão, MRO, mixin virando cena | nada visual |
| 1 | geometria contra o quadro (§5) | o custo de construir os mobjects | cabe / não cabe, com margem | cor, sobreposição, legibilidade |
| 2 | `--dry_run` (§2.1) | render sem escrita | que a cena CONSTRÓI (LaTeX, fonte, dado externo) | nada visual |
| 3 | **um quadro** + **OLHAR** (§2.2, §3) | ~1 s em `-q l` | tudo que um humano vê num quadro | movimento, emenda, ritmo |
| 4 | medir o quadro (§4) | ms sobre o PNG | vazio, borda, tinta — em número, repetível | intenção |
| 5 | comparar dois quadros (§6) | ms sobre dois PNG | o que MUDOU / o que SUMIU | se a mudança era desejada |
| 6 | render final e assistir | minutos | ritmo, emenda, som | — |

**O degrau 3 é o que ninguém pula impunemente.** [DECK] Numa investigação real
num deck de aulas, **três defeitos apareceram só ao olhar a imagem; nenhum deu
erro no terminal.**

---

## 2. Conseguir EXATAMENTE o quadro que você quer

### 2.1 `--dry_run` — prova que constrói, não escreve nada

```bash
bin/manim -ql --dry_run scenes/cena.py Cena
```

Roda `construct` inteiro — todo `Text` vai ao Pango, todo `MathTex` vai ao
LaTeX, todo dado externo é lido — e não grava arquivo nenhum. É o teste de
"isso sequer monta?" antes de gastar disco. Não substitui olhar: um `dry_run`
verde com texto branco no branco é um `dry_run` verde.

### 2.2 Um quadro para OLHAR

Três comandos, e eles fazem coisas diferentes. A mecânica completa é de
**`manim-render-api` §5.4**; aqui está o recorte que interessa.

| Você quer | Comando | Sai |
|---|---|---|
| **um** PNG do último quadro | `bin/mx render cena.py Cena -q l --format png --media-dir /tmp/olhar --json` | um arquivo; o caminho vem em **`image_file`**, não em `output_file` (que é `null` em png) |
| o mesmo, pelo CLI cru | `bin/manim -ql -s cena.py Cena` | **o mesmo arquivo, no mesmo caminho** |
| a sequência inteira de quadros | `bin/manim -ql --format png cena.py Cena` | N arquivos numerados — uma cena de 10 s em `-q h` produz **600** |

Ler o caminho sem adivinhar:

```bash
bin/mx render scenes/cena.py Cena -q l --format png --media-dir /tmp/olhar --json 2>/dev/null \
  | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['image_file'])"
```

**Use `-q l` para olhar layout.** 854×480 mostra corte na borda, sobreposição e
branco-no-branco tão bem quanto 1920×1080, e custa uma fração. Suba a qualidade
só quando o assunto for nitidez de texto (aí o dono é `manim-text-latex`).

### 2.3 Escolher o INSTANTE: `-n a,b`

O quadro que interessa quase nunca é o último. `-n` limita quais animações
rodam de verdade:

```bash
bin/manim -ql -s -n 4,4 scenes/cena.py Cena -o passo-04   # o palco AO FIM da animação 4
bin/manim -ql    -n 4,7 scenes/cena.py Cena -o trecho     # um mp4 curtinho do trecho
```

Três detalhes que economizam tempo:

- **`-n` só existe no `bin/manim`.** O `mx render` não expõe a flag; pela API
  Python seria `config_overrides={"from_animation_number": 4, "upto_animation_number": 7}`
  (`manim-render-api` §6.1).
- **use `-o`**, senão o preview grava por cima do arquivo bom (§2.6).
- as animações fora da faixa **ainda executam** — pular é sobre não escrever
  quadro, não sobre não rodar. `-n 8,9` não fica mais rápido em cena longa.

Numa cena cortada em seções (`next_section`), a mesma pergunta se responde
renderizando **a parte**: `PARTE = 5` e o último quadro dela é o quadro do ato
5. O formato é de `manim-presentation-parts`.

### 2.4 Capturar de DENTRO do `construct`

Quando você quer o palco num ponto que não é fronteira de animação — por
exemplo, logo depois de posicionar tudo e antes do primeiro `play`:

```python
# no meio do construct, para depurar:
self.renderer.update_frame(self)                      # cairo_renderer.py:123  [FONTE]
self.camera.get_image().save("/tmp/palco-montado.png")  # camera.py:301        [FONTE]
```

Assinaturas reais [FONTE]:

```
CairoRenderer.update_frame(self, scene, mobjects=None, include_submobjects=True,
                           ignore_skipping=True, **kwargs) -> None
CairoRenderer.get_frame(self) -> PixelArray
Camera.get_image(self, pixel_array=None) -> Image.Image
```

Duas notas:

- `ignore_skipping=True` é o **padrão** — a captura funciona mesmo quando a
  seção está sendo pulada por `skip_animations`. Isso é útil e é uma armadilha:
  você pode acabar com um PNG de um ato que não virou vídeo nenhum.
- o docstring de `get_frame` diz que a forma é `height x width x 3`; a `Camera`
  nasce com `n_channels: int = 4` e `image_mode: str = 'RGBA'`, e
  `init_background` monta o fundo com `color_to_int_rgba` (`camera.py:275-293`).
  **O docstring parece desatualizado e o arranjo real é RGBA.** [NV — não
  executei; se for medir, imprima `.shape` antes de indexar canal.]

### 2.5 `Mobject.get_image()` e `Mobject.save_image()` — as duas armadilhas

```python
# manim/mobject/mobject.py:878-893  [FONTE]
def get_image(self, camera: Camera | None = None) -> Image.Image:
    if camera is None:
        camera = Camera()
    camera.capture_mobject(self)
    return camera.get_image()

def save_image(self, name: str | None = None) -> None:
    self.get_image().save(
        Path(config.get_dir("video_dir")).joinpath((name or str(self)) + ".png"),
    )
```

**`get_image()` monta uma `Camera()` NOVA** quando você não passa uma. Três
consequências:

1. o fundo vem de `config["background_color"]` **no momento da chamada**
   (`camera.py:134-139`) — **não** do fundo da sua cena. Se a cena fixou só
   `self.camera.background_color`, o PNG sai com outro fundo, e o seu
   diagnóstico de "branco no branco" inverte de sinal;
2. a resolução vem de `config.pixel_width/height`;
3. ele captura **só aquele mobject**. Serve para conferir a forma de uma peça;
   **não serve** para conferir sobreposição com o resto do palco — o resto do
   palco não está lá.

Para conferir contra o fundo real: `mob.get_image(camera=self.camera)`.

**`save_image()` é pior, e é o tipo de API que parece pronta.** Ela escreve em
`video_dir` (o diretório dos **vídeos**, não `images_dir`), e o template padrão
desse diretório é `{media_dir}/videos/{module_name}/{quality}`
(`_config/default.cfg:89`). `ManimConfig.get_dir` levanta quando falta um
argumento do template:

```
KeyError: 'video_dir {media_dir}/videos/{module_name}/{quality} requires the
following keyword arguments: module_name'
```

— e esse traceback está literalmente no **docstring do próprio método**
(`_config/utils.py:1614-1618`). Nada no caminho de render reescreve `video_dir`
para um caminho literal: `SceneFileWriter.init_output_directories` passa
`module_name` como **kwarg** e não grava de volta (`scene_file_writer.py:282-287`).
**Logo `mob.save_image()` estoura**, a menos que você faça
`config.video_dir = "/tmp/x"` antes. [FONTE por leitura, **[NV]** por execução.]

E, mesmo funcionando, o nome padrão é `str(self)` → `Mobject.__repr__` devolve
`self.name`, que nasce como o **nome da classe** (`mobject.py:453-454`). Dois
`Circle` gravam um por cima do outro.

**O que usar:** `mob.get_image(camera=self.camera).save("/tmp/peca.png")`.

### 2.6 O preview SOBRESCREVE a entrega

`images_dir = {media_dir}/images/{module_name}` — **sem `{quality}`**
(`_config/default.cfg:91` e o `manim.cfg` deste repositório). O PNG de `-q l` e
o de `-q k` caem no **mesmo arquivo**. Guardou o pôster de entrega, iterou em
`-q l`, e ele já era.

Duas defesas, e a primeira é grátis:

```bash
--media-dir /tmp/olhar     # todo o preview num lugar descartável
-o passo-04                # ou um nome por quadro conferido
```

Vídeo não tem esse problema — `video_dir` **tem** `{quality}` —, mas tem o
inverso: o preview em `480p15` fica no disco pesando, e um pipeline que copia
"o mp4 mais recente" pega o errado. Leia `output_file`. (Detalhe completo:
`manim-render-api` §3.6 e §14.)

---

## 3. OLHAR — o passo que não se delega a um número

### 3.1 Como um agente olha

Se você é um agente com a ferramenta `Read`: **`Read` no caminho do PNG.** Ela
apresenta a imagem visualmente. Esse é o passo, e ele é literal:

```
1. bin/mx render … --format png --json   →   pegue `image_file`
2. Read(image_file)                      →   OLHE
3. corrija
```

Não relate "renderizado com sucesso" antes do passo 2. `success: true` é
informação sobre o processo, não sobre a imagem — e é exatamente o que a §0
mostra ser insuficiente.

Se você **não pode** olhar (sessão sem visão, CI headless), então a §4 deixa de
ser complemento e vira o método: meça tinta, borda e diferença contra um
baseline, e diga no relatório que a conferência foi numérica.

### 3.2 A ordem de leitura de um quadro

Sete perguntas, nesta ordem — a primeira que falhar já te dá o conserto:

1. **Tem alguma coisa?** Quadro vazio ou quase vazio → §4.1.
2. **Falta alguma coisa que deveria estar?** Compare com a lista de mobjects do
   ato. Sumido em fundo da mesma cor → §4.2.
3. **Alguma coisa toca a borda?** Título, rodapé, barra longa → §4.3.
4. **Alguma coisa está por cima de outra?** Texto sobre linha de grade, rótulo
   sobre barra, legenda sobre eixo → §4.4.
5. **Dá para LER?** Contraste, tamanho, fonte trocada. A conta é de
   `manim-color-theming` §5.
6. **Está onde você mandou?** Alinhamento, `buff`, simetria entre colunas.
7. **É o quadro certo?** Um pôster que pega o meio de um `FadeIn` está correto
   como imagem e errado como pôster (§7).

### 3.3 Quando o olho basta, e quando não basta

| O olho resolve | Precisa de número |
|---|---|
| sobreposição, corte, texto ausente, feiúra | "isto está 1 % mais vazio que ontem?" |
| um quadro | 60 quadros, ou 77 arquivos de um lote |
| "isto está errado" | "isto REGRIDIU em relação ao commit anterior" |
| a primeira vez | toda vez, em pre-commit/CI |

A regra prática: **olhe uma vez, meça sempre.** O que você olhou vira um número
que a máquina repete.

---

## 4. Medir o quadro

Todas as medições abaixo rodam sobre um PNG que já existe, com `numpy` e
`Pillow` — os dois estão no `.venv` deste projeto. Nenhuma re-renderiza nada.

### 4.1 Cobertura de tinta: o quadro está vazio?

```python
import numpy as np
from PIL import Image

lum = np.asarray(Image.open("quadro.png").convert("L"), dtype=np.int16)
tinta = float((lum < 235).mean())      # fundo CLARO: tinta é o que escurece
print(f"{tinta * 100:.2f}%  min={lum.min()} max={lum.max()}")
```

Em fundo escuro o sinal inverte: `(lum > 20).mean()`.

Calibragem [DECK], **não reproduzida aqui**: a cobertura das cenas em produção
de um deck real vai de **2,9 %** a **21 %**. **Abaixo de 1 % é fade-out
disfarçado** — e é isso que produz a página branca no PDF de backup.

Um quadro com **zero** pixels abaixo de 128 num tema claro é um quadro vazio,
por mais que a cena tenha 40 mobjects. (Foi assim que `manim-color-theming` §10.3
provou que 39 classes hard-codam cor.)

**Onde isso morde de verdade:** o último quadro da última parte é o pôster do
PDF, do `prefers-reduced-motion` e do `<video poster>`. Se a cena fecha em
`FadeOut`, o backup impresso sai em branco e ninguém descobre antes do palco.
Regra que sai daqui: **nenhuma parte pode terminar em fade-out.**

Ferramenta: `assets/mede_tinta.py` (§8).

### 4.2 Branco no branco: `min`, `max` e o histograma

Cobertura de tinta acusa o quadro **inteiro** vazio. Ela não acusa **um** texto
que sumiu num quadro cheio. Para isso:

```python
import numpy as np
from PIL import Image

lum = np.asarray(Image.open("quadro.png").convert("L"))
hist = np.bincount(lum.ravel(), minlength=256)
print("níveis com pixel:", int((hist > 0).sum()))
print("os 5 mais frequentes:", np.argsort(hist)[-5:][::-1])
```

O que você procura: **um tema tem poucos níveis dominantes.** Um quadro de tema
claro saudável tem um pico enorme perto de 255 (o fundo), um pico na tinta, e
uma cauda de antialiasing. Se o pico de tinta **não existe**, o texto que
deveria estar ali está na cor do fundo.

Dois complementos que fecham o diagnóstico:

- **recorte a região**: `lum[y0:y1, x0:x1]` onde o texto deveria estar, e meça
  `min()` ali. Converter unidade de palco em pixel: `px = (u + frame_x_radius) *
  pixel_width / frame_width` para x, e `py = (frame_y_radius - v) * pixel_height
  / frame_height` para y (o eixo y da imagem cresce **para baixo**);
- **compare com o render anterior** (§6): texto que sumiu aparece como tinta que
  sumiu, e a métrica direcional já é exatamente essa conta.

A causa mais comum não é bug de layout, é cor: `manim-color-theming` §9 e §10.

### 4.3 A borda: a caixa da tinta e as quatro faixas

Duas medidas diferentes, e você quer as duas:

```python
import numpy as np
from PIL import Image

lum = np.asarray(Image.open("quadro.png").convert("L"), dtype=np.int16)
tinta = lum < 235
linhas, colunas = np.flatnonzero(tinta.any(axis=1)), np.flatnonzero(tinta.any(axis=0))
h, w = tinta.shape
print("folga topo", linhas[0], "base", h - 1 - linhas[-1],
      "esq", colunas[0], "dir", w - 1 - colunas[-1])       # em PIXELS
print("tinta na faixa de 24px da direita:", int(tinta[:, -24:].sum()))
```

A **caixa** diz onde o conteúdo termina; a **faixa** diz se alguma coisa está
grudada na borda. Régua de conversão: o palco padrão do ManimCE é 14,222 × 8,0
unidades, então em **1920×1080, 1 unidade = 135 px**; o `buff` padrão de
`to_edge` é 0,5 unidade = **67,5 px**. Uma folga de 6 px em 1080p é
praticamente encostado.

**Cuidado com o falso positivo legítimo:** cena com grade de fundo, ou
`NumberPlane`, tem tinta na borda de propósito. Nesses casos meça a faixa só
onde o conteúdo mora, ou use `--margem 0` e leia apenas a caixa.

Ferramenta: `assets/confere_borda.py` (§8).

### 4.4 Sobreposição: o pixel NÃO responde — a caixa responde

Não existe medida de pixel que diga "estes dois textos estão sobrepostos": dois
desenhos no mesmo lugar produzem um quadro perfeitamente válido. O que responde
é a **geometria**, antes de rasterizar:

```python
def sobrepoe(a, b, folga=0.0) -> bool:
    """Caixas alinhadas aos eixos se cruzam? (unidades de palco)"""
    return not (
        a.get_right()[0] + folga <= b.get_left()[0]
        or b.get_right()[0] + folga <= a.get_left()[0]
        or a.get_top()[1] + folga <= b.get_bottom()[1]
        or b.get_top()[1] + folga <= a.get_bottom()[1]
    )

for i, m in enumerate(self.mobjects):
    for n in self.mobjects[i + 1:]:
        assert not sobrepoe(m, n, folga=0.05), (type(m).__name__, type(n).__name__)
```

Assinaturas [FONTE]: `Mobject.get_left/get_right/get_top/get_bottom(self) -> Point3D`;
a forma geral é `get_critical_point(self, direction: Vector3DLike) -> Point3D`.

**As três ressalvas, e elas importam:**

1. a caixa é alinhada aos eixos. Um losango e um texto podem ter caixas que se
   cruzam sem nenhum pixel em comum — falso positivo;
2. sobreposição **de propósito** é comum e correta: o *prato* opaco atrás de um
   rótulo que cruza uma linha de grade existe justamente para se sobrepor. Não
   automatize a proibição; automatize a **lista** e revise;
3. um pai e seus filhos sempre se cruzam. Compare `get_top_level_mobjects()`
   (`Scene.get_top_level_mobjects(self) -> list[Mobject]`, [FONTE]) ou peças que
   você escolheu, nunca a família inteira.

### 4.5 Legibilidade: quem é o dono

A conta de contraste WCAG, os patamares (4,5 · 3,0 · 7,0) e o medidor pronto
são de **`manim-color-theming` §5**. Esta skill **usa** o medidor, não o
reescreve. O recorte que é daqui: medir o contraste **no pixel medido**, e não
na paleta declarada — porque antialiasing, `sheen`, gradiente e imagem de fundo
mudam o que chega ao olho:

```python
recorte = lum[y0:y1, x0:x1]                 # onde o texto está
fundo, frente = int(np.percentile(recorte, 90)), int(np.percentile(recorte, 10))
print("níveis:", frente, "sobre", fundo)    # depois passe para razao() da outra skill
```

---

## 5. Conferir SEM renderizar — geometria contra o quadro

### 5.1 `is_off_screen()` NÃO é um teste de enquadramento

Esta é a armadilha mais cara desta skill, porque o nome do método promete o
contrário do que ele faz.

```python
# manim/mobject/mobject.py:1744-1752   [FONTE]
def is_off_screen(self) -> bool:
    if self.get_left()[0]   >  config["frame_x_radius"]: return True
    if self.get_right()[0]  < -config["frame_x_radius"]: return True
    if self.get_bottom()[1] >  config["frame_y_radius"]: return True
    rv: bool = self.get_top()[1] < -config["frame_y_radius"]
    return rv
```

Leia os quatro testes: **borda esquerda depois da direita do quadro**, **borda
direita antes da esquerda do quadro**, e assim por diante. Ele responde
*"está INTEIRAMENTE fora?"*. Um título que passa 300 px da borda direita, com o
resto dentro, devolve **`False`**. Um `Text` cortado ao meio devolve `False`.
Uma barra que estoura o eixo devolve `False`.

**`is_off_screen() == False` não quer dizer "cabe".** Quer dizer "aparece pelo
menos um pedaço".

### 5.2 `Camera.is_in_frame` — a mesma lógica, com uma diferença que morde

```python
# manim/camera/camera.py:485-510   [FONTE]
def is_in_frame(self, mobject: Mobject) -> bool:
    fc, fh, fw = self.frame_center, self.frame_height, self.frame_width
    return not reduce(op.or_, [
        mobject.get_right()[0]  < fc[0] - fw / 2,
        mobject.get_bottom()[1] > fc[1] + fh / 2,
        mobject.get_left()[0]   > fc[0] + fw / 2,
        mobject.get_top()[1]    < fc[1] - fh / 2,
    ])
```

É a **negação literal** dos mesmos quatro testes — mesma semântica frouxa. A
diferença que importa: `is_in_frame` mede contra **`self.frame_center`**, e o
`is_off_screen` do Mobject mede contra o `config` global.

**Consequência:** sob `MovingCameraScene` / `ZoomedScene`, com a câmera
deslocada ou com zoom, **`Mobject.is_off_screen()` mente** — ele continua
comparando com o quadro da origem. Se a câmera se move, o teste correto é
contra o `self.camera.frame` daquele instante. (A câmera 2D é assunto da skill
de câmera; aqui só o alerta de que o medidor errado responde com confiança.)

### 5.3 O teste que você quer: contenção com margem

```python
from manim import config

def cabe(mob, margem: float = 0.0) -> bool:
    rx, ry = config.frame_x_radius, config.frame_y_radius
    return (
        mob.get_left()[0]   >= -rx + margem
        and mob.get_right()[0]  <=  rx - margem
        and mob.get_bottom()[1] >= -ry + margem
        and mob.get_top()[1]    <=  ry - margem
    )
```

[FONTE] `config.frame_x_radius` e `frame_y_radius` são propriedades reais de
`ManimConfig` (`_config/utils.py:1149-1166`) e acompanham `frame_width` /
`frame_height`; `config.top`, `bottom`, `left_side`, `right_side` devolvem os
mesmos números como vetores (`:1152-1188`).

**Escolha da margem.** A caixa vem dos **pontos** da curva, e a espessura do
traço é desenhada para **fora** deles: um `Line(stroke_width=8)` colado no
limite perde metade do traço, e `cabe(..., margem=0)` aprova. Em 1080p,
8 px = 0,06 unidade — então uma margem de 0,1 já cobre traço grosso, e 0,25
é um respiro visual honesto.

O parente pronto na biblioteca é `Mobject.shift_onto_screen(**kwargs) -> Self`
(`mobject.py:1733-1742`, [FONTE]): ele **corrige** em vez de avisar, usando
`DEFAULT_MOBJECT_TO_EDGE_BUFFER` e chamando `to_edge` no lado que estourou.
Bom para salvar um layout; ruim como teste, porque some com a evidência.

### 5.4 A caixa mente quando existe elemento invisível

Um detalhe transparente — espaçador, lingueta, retângulo de `fill_opacity=0` —
**continua contando** na caixa delimitadora do `VGroup`. `VGroup.move_to()`
desloca o grupo inteiro pelo tamanho do invisível. [DECK] 4 px, medidos,
silenciosos — e o defeito só foi achado porque a métrica de emenda (§6) estourou.

Posicione e confira pelo **corpo visível**:

```python
def _visivel(m):
    if not m.has_points():
        return False
    fo = getattr(m, "get_fill_opacity", None)
    so, sw = getattr(m, "get_stroke_opacity", None), getattr(m, "get_stroke_width", None)
    if fo is None:                       # não é VMobject — não dá para julgar
        return True
    return float(fo()) > 0 or (float(so()) > 0 and float(sw()) > 0)
```

[FONTE] `VMobject.get_fill_opacity(self) -> ManimFloat`,
`get_stroke_opacity(self, background: bool = False) -> ManimFloat`,
`get_stroke_width(self, background: bool = False) -> float`. E lembre que
`VMobject.__init__` nasce com **`fill_opacity: float = 0.0`** — forma sem
`set_fill(..., opacity=…)` é contorno, não bloco.

Ferramenta: `assets/guarda_enquadramento.py` já implementa `caixa`, `cabe`,
`estouro` e `relatorio` com esse filtro (§8).

### 5.5 Achar o submobject certo: `index_labels` e `print_family`

```
index_labels(mobject, label_height: float = 0.15, background_stroke_width: float = 5,
             background_stroke_color: ManimColor = ManimColor('#000000'), **kwargs) -> VGroup
print_family(mobject, n_tabs: int = 0) -> None
```

[FONTE] `manim/utils/debug.py`. `index_labels` percorre `enumerate(mobject)` —
ou seja, os **submobjects diretos**, um nível só — e devolve um `VGroup` de
`Integer` posicionado sobre cada um. Você o **adiciona à cena** e renderiza um
quadro:

```python
self.add(formula, index_labels(formula[0], color=BLACK))
```

Duas notas de uso:

- os `**kwargs` vão para o `Integer`, então `color=BLACK` é como você faz os
  rótulos aparecerem num tema claro (o preenchimento padrão é branco; o
  contorno de fundo preto de largura 5 salva a leitura na maioria dos casos,
  mas não em todos);
- é o antídoto para `mob[0][2]` escrito no chute — o índice errado não dá erro,
  anima a peça errada.

`print_family` imprime a árvore no terminal e não precisa de render nenhum. Use
para saber **quantos** submobjects existem antes de indexar.

### 5.6 O guarda de cena

O teste da §5.3 vira automático se rodar depois de cada `play`. O padrão é um
**mixin que NÃO herda de `Scene`**:

```python
class GuardaEnquadramento:          # NÃO herda de Scene — de propósito
    MARGEM = 0.25
    def play(self, *a, **k):
        r = super().play(*a, **k)
        self._confere_palco("play")
        return r

class MinhaCena(GuardaEnquadramento, Scene):   # mixin PRIMEIRO
    ...
```

As duas regras são as mesmas do formato em partes, e as duas falham em silêncio:
uma base que herda de `Scene` aparece em `mx scenes` e vira uma cena renderizada
por engano (o descobridor é `issubclass(obj, Scene)`, `manimx/render.py:141-145`);
e com as bases invertidas o MRO resolve os métodos em `Scene` e o guarda nunca
roda. Detalhe completo em **`manim-presentation-parts` §3.2 e §3.3**.

Implementação pronta: `assets/guarda_enquadramento.py`.

### 5.7 O que o estático NÃO alcança

| Alcança | Não alcança |
|---|---|
| cabe / não cabe, com margem | se **dá para ler** |
| caixas que se cruzam | se a sobreposição era intencional |
| submobject invisível na caixa | cor, contraste, gradiente, `sheen` |
| contagem de submobjects | fonte trocada em silêncio |
| a cor **declarada** de um mobject | a cor que o antialiasing entregou |

Por isso a §5 é o degrau 1 da escada, e não o topo dela.

---

## 6. Comparar dois quadros

> **Fronteira, e ela é o contrário do que esta skill dizia.** A métrica
> direcional NASCEU em `manim-presentation-parts` §7 ("Por que RMS falha", "O
> medidor", "O limiar, e como recalibrá-lo"), que é onde a anedota do RMS 4,4, o
> `((b - a) > 24).sum()`, os números de calibragem e a régua de tinta foram
> escritos primeiro. Uma versão anterior desta seção afirmava o oposto — que
> `manim-presentation-parts` era dona só da "regra do formato" e esta skill, da
> "régua". **Não é.** O que esta seção acrescenta é a **generalização**: usar a
> mesma régua para qualquer par antes/depois, não só para uma emenda entre
> partes. Se você chegou aqui por causa de uma emenda entre partes de um vídeo
> de slide, **a skill é `manim-presentation-parts`** — ela tem o limiar
> calibrado para esse caso e o conferidor de corte órfão. Se você chegou por
> "mudei o código, o que mudou na tela?", é aqui.

### 6.1 As três métricas, e quando cada uma mente

| Métrica | Fórmula | Mente quando |
|---|---|---|
| **RMS** / MSE | `sqrt(((a-b)**2).mean())` | **sempre que houver mudança legítima.** É simétrica: acusa a próxima animação COMEÇANDO. [DECK] uma emenda perfeita deu RMS 4,4 e foi reprovada |
| **abs / contagem de diferentes** | `(abs(a-b) > d).sum()` | idem — simétrica |
| **SSIM / perceptual** | estrutural | idem, e ainda depende de biblioteca externa que **não está no `.venv`** |
| **direcional** | `((b-a) > d).sum()` (fundo claro) | quase nunca no caso "sumiu"; não vê o que APARECEU |

A pergunta certa quase nunca é "os quadros são iguais?". É **"alguma coisa
DESAPARECEU?"** — porque conteúdo que aparece é o comportamento esperado, e
conteúdo que some é o defeito.

Faça a escolha explícita antes de medir:

| Você quer saber | Métrica |
|---|---|
| a emenda entre partes perdeu conteúdo? | direcional "sumiu" |
| a refatoração mudou o quadro? | contagem de diferentes, com baseline |
| a cena ficou igualzinha (teste de regressão)? | tolerância absoluta + razão de mismatch (§6.4) |
| o quadro está vazio? | não é comparação — é §4.1 |

### 6.2 A métrica DIRECIONAL

Em fundo claro, "sumiu" = o pixel **clareou**:

```python
import numpy as np
from PIL import Image

a = np.asarray(Image.open("antes.png").convert("L"), dtype=np.int16)   # o quadro que TINHA
b = np.asarray(Image.open("depois.png").convert("L"), dtype=np.int16)  # o quadro que TEM
sumiu = int(((b - a) > 24).sum())      # clareou = perdeu tinta
```

O `int16` não é detalhe: em `uint8`, `b - a` dá a volta e o sinal se perde.

Em **fundo escuro** o sinal inverte: `((a - b) > 24).sum()`. Em cena colorida,
`convert("L")` pode empatar duas cores de luminância parecida — compare por
canal e some.

Casos de uso, os dois com a mesma conta:

- **emenda entre partes**: `antes` = último quadro da parte N, `depois` =
  primeiro da N+1. O formato, a granulação e a manutenção são de
  **`manim-presentation-parts`**; aqui está a régua;
- **antes/depois de uma edição**: `antes` = PNG guardado do render anterior,
  `depois` = PNG novo. Tinta que sumiu é conteúdo que você perdeu sem querer.

Ferramenta: `assets/mede_emenda.py` (§8), que faz os dois modos e escala o
limiar pela área.

### 6.3 O limiar e as três recalibragens

**400 px em 1920×1080 (2 073 600 px), fundo claro** [DECK, **não reproduzido
aqui**]. Abaixo disso é antialiasing; acima, alguma coisa desapareceu. Emendas
boas ficavam entre **4 e 27 px**; a pior aprovada foi **118 px** — folga de 3,4×.

| Situação | Ajuste |
|---|---|
| outra resolução | escala com a **área**: `400 × (w·h / 2 073 600)` |
| fundo escuro | inverta o sinal: `((a - b) > 24)` |
| cena colorida | compare por canal e some, em vez de `convert("L")` |
| traço fino / muito texto pequeno | mais antialiasing ⇒ suba o `delta` de 24 antes de subir o limiar |

**O falso positivo que você vai encontrar, e é traiçoeiro:** se você editou um
ato e re-renderizou **só** a parte dele, a parte vizinha no disco ainda é a
versão velha e a medição estoura. **Investigue antes de "consertar" a cena** —
[DECK] foi assim que se achou um defeito real (o elemento invisível da §5.4). A
ordem certa é: re-renderize o alcance inteiro, **depois** meça.

### 6.4 O que o PRÓPRIO Manim usa — e por que não roda aqui

O ManimCE tem um comparador de quadros embutido, usado nos testes gráficos dele.
Vale conhecer as **tolerâncias**, que são a coisa mais transferível do arquivo:

```python
# manim/utils/testing/_frames_testers.py   [FONTE]
FRAME_ABSOLUTE_TOLERANCE = 1.01        # np.testing.assert_allclose(atol=...)
FRAME_MISMATCH_RATIO_TOLERANCE = 1e-5  # < 0,001 % dos VALORES podem divergir
```

Como funciona [FONTE]: `_FramesTester.check_frame` roda
`np.testing.assert_allclose(frame, controle, atol=1.01)`; se falhar, conta
quantos valores estão fora e **tolera** até `1e-5` do total, com um warning, "to
account for minor OS dependent inconsistencies". O dado de controle é um `.npz`
gravado por `np.savez_compressed(file, frame_data=frames)`
(`_ControlDataWriter.save_contol_data`), regerado com `pytest --set_test`, e o
diff visual sai com `--show_diff` via `matplotlib`.

O decorador é
`frames_comparison(func=None, *, last_frame=True, renderer_class=CairoRenderer, base_scene=Scene, **custom_config)`
[FONTE], e ele roda a cena em resolução minúscula: **854×480 a 6 fps** para
teste de um quadro, **427×240 a 6 fps** para vários
(`config_graphical_tests_monoframe.cfg` / `_multiframes.cfg`), sempre com
`disable_caching = True`.

**E aqui vem a parte honesta: isso não roda nesta máquina.**
`frames_comparison.py` faz `import pytest` no topo, e `_show_diff.py` importa
`matplotlib` dentro da função. **Nenhum dos dois está instalado no `.venv`** —
confirmado listando `site-packages`. Instalar está fora de escopo. Então:

- **`manim.utils.testing.frames_comparison` é inimportável aqui** [FONTE, por
  ausência de dependência];
- `manim.utils.testing._frames_testers` **é** importável (só precisa de `numpy`;
  o `matplotlib` é lazy) — mas é privado e o caminho do `.npz` de controle é
  fixado em `tests/control_data/graphical_units_data`, que este repositório não
  tem;
- **o que transfere são os números e o formato**: `atol` ~1, razão de mismatch
  ~1e-5, baseline em `.npz` comprimido, e uma resolução de teste propositalmente
  pequena.

### 6.5 Regressão visual caseira

Com o de cima, um baseline em 20 linhas e sem dependência nova:

```python
# grava o baseline  (uma vez, com a versão que você aprovou olhando)
import numpy as np
from PIL import Image
np.savez_compressed("baseline/cena.npz",
                    frame=np.asarray(Image.open("quadro.png").convert("RGB")))

# confere  (em pre-commit / CI)
esperado = np.load("baseline/cena.npz")["frame"].astype(np.int16)
atual = np.asarray(Image.open("quadro.png").convert("RGB"), dtype=np.int16)
assert atual.shape == esperado.shape, (atual.shape, esperado.shape)
fora = int((np.abs(atual - esperado) > 1).sum())
razao = fora / atual.size
print(f"{fora} valores fora ({razao:.2e})")
assert razao < 1e-5, "o quadro REGRIDIU — olhe os dois antes de regravar o baseline"
```

Três regras para isso não virar ruído:

1. **fixe a resolução do baseline.** Quadro de outra resolução não é
   comparável — o `assert` de forma acima é o guarda;
2. **regravar o baseline é uma decisão, não um reflexo.** Regrave só depois de
   OLHAR os dois quadros;
3. **cena com dado externo (CSV, API, `random` sem semente, data de hoje) não
   tem baseline estável.** E, pior, o cache do Manim não enxerga esse dado —
   render com dado de fora precisa de `--no-cache` (`manim-troubleshooting` §5.2).

---

## 7. O que se prova sem abrir a imagem

O ManimCE traz um leitor de metadados em **PyAV** — sem `ffprobe`, sem sair do
venv:

```
get_video_metadata(path_to_video: str | os.PathLike) -> VideoMetadata   [FONTE]
# manim/utils/commands.py:47 — abre com av.open e devolve:
# width, height, nb_frames, duration, avg_frame_rate, codec_name, pix_fmt
```

```python
from manim import get_video_metadata
metadados = [get_video_metadata(f) for f in arquivos]
print({(m["width"], m["height"], m["avg_frame_rate"]) for m in metadados})
# esperado: um conjunto de UM elemento
```

Isso responde à pergunta "alguém commitou um preview 720p30 por cima da
entrega?" — o sintoma é **duas linhas** onde deveria haver uma. [DECK] num deck
real, 59 arquivos, uma linha só: `1920,1080,60/1`.

**Três coisas que o metadado NÃO prova**, e por isso ele nunca fecha a
conferência:

1. **nada sobre a imagem.** Metadado certo com texto branco no branco é
   metadado certo;
2. **o codec no contêiner não distingue NVENC de libx264** — os dois gravam
   `h264` (`manim-gpu-encoding` é o dono desse assunto);
3. **a duração não diz se o quadro final é o certo.** Um pôster tirado com
   `-sseof -1 -frames:v 1` pega o quadro de 1 s **antes** do fim, não o último —
   só `-update 1` (que sobrescreve a cada quadro) deixa o último no disco. As
   duas linhas de `ffmpeg` e o porquê de elas **precisarem** ser diferentes são
   de **`manim-batch-pipeline` §8.5**; a consequência de projeto — *a cena não
   pode fechar em `FadeOut`* — é a §4.1 daqui.

Para listar o que foi escrito: `get_dir_layout(dirpath: Path) -> Generator[str, None, None]`
[FONTE], caminhos relativos, recursivo.

---

## 8. Os arquivos de apoio desta skill

Quatro arquivos em `assets/`, ao lado deste. Todos dependem só de `numpy` e
`Pillow` (presentes no `.venv`); só o `--extrair` do medidor de emenda usa `av`.
Nenhum re-renderiza cena. **Nenhum foi executado** na sessão em que foram
escritos — passaram por `python -m py_compile` e nada mais.

| Arquivo | Responde | Chamada típica | Saída |
|---|---|---|---|
| `assets/mede_tinta.py` | "este quadro está vazio?" | `python assets/mede_tinta.py saida/*.png --minimo 1.0` | uma linha por arquivo com % de tinta; **exit 1** se alguma ficar abaixo |
| `assets/confere_borda.py` | "a tinta encosta na borda?" | `python assets/confere_borda.py quadro.png --margem 24` | folga por lado em px e %, tinta em cada faixa; **exit 1** se estourar |
| `assets/mede_emenda.py` | "o que SUMIU entre dois quadros?" | `python assets/mede_emenda.py antes.png depois.png`<br>`python assets/mede_emenda.py --dir public/videos/` | px de tinta perdida contra o limiar escalado por área; **exit 1** se passar |
| `assets/guarda_enquadramento.py` | "cabe no quadro, com margem?" — **sem renderizar** | `from guarda_enquadramento import cabe, estouro, relatorio`<br>ou o mixin `GuardaEnquadramento` | `bool`, dicionário de estouro por lado, ou tabela do palco |

Os três primeiros detectam fundo claro × escuro sozinhos (mediana dos quatro
cantos) e aceitam `--claro` / `--escuro` para forçar. Todos aceitam `--limiar`.

O quarto é módulo, não script: ele importa `manim` e lê `config`, então precisa
rodar com o Python do `.venv` e com a mesma resolução configurada do render.

---

## 9. O checklist antes de dar um vídeo por pronto

Sete itens. Os cinco primeiros rodam em segundos e não renderizam nada.

**1 · Você OLHOU.** O PNG de cada quadro que você mexeu, com `Read`. Sem isso os
outros seis itens são teatro. §3.

**2 · Nenhum quadro está vazio.**

```bash
python .claude/skills/manim-verificacao-visual/assets/mede_tinta.py saida/*.png --minimo 1.0
```

Esperado: `ok` em toda linha. Abaixo de 1 % é fade-out disfarçado → o PDF de
backup sai em branco. §4.1.

**3 · Nada encosta na borda.**

```bash
python .claude/skills/manim-verificacao-visual/assets/confere_borda.py saida/*.png --margem 24
```

Falso positivo legítimo em cena com grade de fundo — nesse caso `--margem 0` e
leia a caixa. §4.3.

**4 · Nenhuma emenda perde tinta** (só para cena em partes).

```bash
python .claude/skills/manim-verificacao-visual/assets/mede_emenda.py --dir saida/
```

Antes de "consertar" uma emenda que estourou, confirme que as duas partes foram
renderizadas na **mesma** versão do código. §6.3.

**5 · A saída é uniforme.**

```python
from manim import get_video_metadata
print({(m["width"], m["height"], m["avg_frame_rate"])
       for m in map(get_video_metadata, arquivos)})   # esperado: UM elemento
```

Duas linhas = tem preview comitado por cima da entrega. §7.

**6 · O quadro cabe** — se a cena tem geometria calculada, rode `relatorio()` do
`guarda_enquadramento` ou deixe o mixin ligado durante a escrita. §5.3.

**7 · A contagem bate** — classes × arquivos no disco × o que o consumidor
declara. Este item é de **`manim-batch-pipeline` §9.1**; ele não é visual, mas é
a divergência mais comum e a de pior sintoma.

---

## 10. Diagnósticos que mentem

Três formas de escrever uma conferência que devolve "ok" quando não está ok. As
três já custaram tempo neste projeto e nos consumidores dele.

**1. `comando | grep x || echo ok`.** O `||` cobre a falha do **pipeline
inteiro**: se o `comando` explodir, o `grep` não acha nada e você imprime "ok".
**Materialize a saída antes de filtrar:**

```bash
bin/mx scenes cena.py > /tmp/cenas.txt || { echo "O COMANDO FALHOU"; exit 1; }
grep -E '^\s+_' /tmp/cenas.txt && echo "MIXIN VIROU CENA" || echo ok
```

**2. Medir contra um mapa escrito à mão.** A lista de arquivos tem de sair do
**disco** (`glob`), nunca de uma constante. [DECK] uma lista desatualizada
mandava medir um `*-p10.mp4` inexistente e o `check=True` estourava — o script
morria antes de conferir os que existiam.

**3. Comparar imagens de tamanhos diferentes.** `numpy` faz *broadcast* em
alguns casos e explode em outros; quando faz, a conta sai e o número não quer
dizer nada. Compare a forma **antes** de subtrair (`assets/mede_emenda.py` já
levanta nesse caso).

**Bônus, específico daqui:** medir tinta sem declarar o fundo. Um script
calibrado para tema claro rodando sobre um quadro de tema escuro devolve
"100 % de tinta" e passa em qualquer limiar mínimo. Os scripts de `assets/`
detectam e **imprimem** qual fundo assumiram — leia essa coluna.

---

## 11. Sintoma → o que medir

| Sintoma | Primeira medida | Depois |
|---|---|---|
| "o slide sai em branco no PDF" | §4.1 tinta do pôster | a cena fecha em `FadeOut`? |
| "sumiu um texto" | §4.2 histograma; §6.2 contra o render anterior | cor: `manim-color-theming` §9 |
| "cortou na borda" | §4.3 faixas; §5.3 `cabe()` | margem < `stroke_width/2`? |
| "está embolado" | §4.4 caixas que se cruzam | ordem de `z_index`, ou prato opaco faltando |
| "a emenda piscou" | §6.2 direcional | animação que **tapa** no alfa 0: `manim-presentation-parts` §6 |
| "mudei uma linha e o vídeo mudou inteiro" | §6.5 baseline | cache servindo velho: `manim-troubleshooting` §5 |
| "o vídeo está mole no projetor" | §7 metadado | preview comitado: §2.6 |
| "renderizou e não tem arquivo" | não é visual | `manim-troubleshooting` §7 |
| "o `VGroup` desalinhou 4 px" | §5.4 caixa só do visível | `index_labels` para achar o culpado |
| "o texto está com as letras soltas" | não é isto | `manim-text-latex` (o arredondamento do cairo) |

---

## 12. Onde esta skill para

| A pergunta virou… | Skill |
|---|---|
| o render **falhou**, traceback, exit code, arquivo que não aparece | `manim-troubleshooting` |
| cache servindo resultado velho, bissecção, LaTeX quebrado | `manim-troubleshooting` |
| escolher qualidade/formato, onde o arquivo cai, `image_file` × `output_file`, `-n`, `tempconfig` | `manim-render-api` |
| a **conta** de contraste WCAG, a paleta, `set_default`, fundo da cena | `manim-color-theming` |
| a **nitidez** do texto, o arredondamento do cairo, `t2c` | `manim-text-latex` |
| o **formato** em partes: granulação, `_corte`, manutenção, e a emenda como regra de composição | `manim-presentation-parts` |
| conferências de **lote**: contagem, extração de pôster, paralelismo, CI | `manim-batch-pipeline` |
| codec, NVENC, peso do arquivo, `mx bench` | `manim-gpu-encoding` |
| descobrir se um nome/assinatura/kwarg existe | `manim-api-discovery` |
| o mapa do repositório e qual skill chamar | `manim-project` |
| posicionar o mobject para que ele CAIBA (em vez de descobrir que não coube), a margem segura, `arrange`, z-index, e o "cabe na tela?" **sem renderizar** | **`manim-layout-posicionamento`**, §9 — ela já traz a mesma citação `mobject.py:1744-1752` e a receita de encolher antes |
| escolher a FORMA, `VGroup` × `Group`, `scale_to_fit_*` | `manim-mobjects` |

**A fronteira em uma frase:** as skills vizinhas produzem o arquivo; esta
pergunta se o que está dentro dele está certo. Onde `manim-troubleshooting` para
("*olhe*"), esta começa ("*olhe assim, e meça isto*").

E duas fronteiras que costumam confundir:

- **contraste**: `manim-color-theming` é dona da **conta** e dos patamares; esta
  skill é dona de medir o contraste **no pixel que saiu**, que é outra coisa
  (§4.5);
- **emenda**: `manim-presentation-parts` é dona da emenda **inteira** — a regra
  do formato *e* a régua (§7 dela: por que RMS falha, o medidor, o limiar, a
  cobertura de tinta do pôster). Esta skill **reproduz** essa régua e a
  generaliza para qualquer par antes/depois (§6). Emenda entre partes de slide
  → vá para lá; comparação genérica de dois frames → fique aqui;
- **enquadramento**: `manim-layout-posicionamento` §9 é dona de "cabe na tela?"
  **antes** de renderizar (a caixa, a margem, o encolhimento). Esta skill é dona
  de provar, **no pixel que saiu**, que não coube (§4, §7).

---

## 13. O que ficou NÃO VERIFICADO nesta sessão

Escrito porque uma skill que não diz o que não sabe é pior que uma skill curta.

1. **Nada foi renderizado.** Nenhum `mx render`, nenhum `manim`, nenhum
   `ffmpeg`, nenhum `ffprobe`, nenhuma GPU. Todos os comandos são para você
   rodar.
2. **Os quatro scripts de `assets/` não foram executados** — só
   `python -m py_compile`. As assinaturas que eles usam (`numpy`, `Pillow`,
   `av.open`, `VideoFrame.to_ndarray(format="rgb24")`) foram conferidas por
   leitura, não por chamada. Confira a primeira saída de cada um.
3. **`Mobject.save_image()` levantar `KeyError`** é dedução do código
   (`mobject.py:887-893` + `_config/utils.py:1686-1694` + o docstring do próprio
   `get_dir`). O encadeamento é inequívoco, mas **não executei**.
4. **A forma do `renderer.get_frame()`** (RGBA vs RGB) é leitura contra um
   docstring que parece desatualizado. Imprima `.shape` antes de indexar canal.
5. **Os limiares numéricos são [DECK]**: 400 px de emenda em 1080p, 118 px de
   pior caso, 1 % de tinta mínima, 2,9 %–21 % de cobertura observada. Medições
   de outro projeto, outra máquina-hora, **não reproduzidas aqui**. Recalibre
   no seu caso e anote a data.
6. **`pytest` e `matplotlib` ausentes** foi confirmado listando `site-packages`
   — mas não tentei importar. A consequência (o `frames_comparison` do Manim ser
   inimportável) segue do `import pytest` no topo do módulo.
7. **`get_video_metadata`** teve assinatura e implementação lidas; o
   comportamento **não** foi observado.
