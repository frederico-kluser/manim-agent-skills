---
name: manim-gpu-encoding
description: >-
  GPU, codec, pix_fmt e PESO do arquivo no Manim — NVENC (h264_nvenc /
  hevc_nvenc), o teto de 8 sessões de encode desta placa, escolha de codec com
  tempo × peso × qualidade MEDIDOS, o orçamento de MB por segundo de vídeo, o
  inventário real de encoders desta build do PyAV, o caminho de alfa
  (qtrle × VP9 yuva420p), o GIF e a paleta que o Manim joga fora, o renderer
  OpenGL, wgpu/Vulkan do ManimGL, PRIME offload em notebook híbrido, encoding
  paralelo (`max_inflight_encoders`) e o `mx bench`. Use quando pedirem
  "usa a GPU", "acelera o render", "está lento demais", "qual codec eu uso?",
  "qual qualidade eu uso?", "posso renderizar em 4K?", "o mp4 ficou enorme",
  "quanto isso vai pesar?", "esse vídeo pesa demais para o slide/repositório",
  "dá para sair em AV1?", "o gradiente saiu com faixas", "o texto vermelho
  ficou borrado", "o GIF saiu sujo/serrilhado", "quero fundo transparente mas
  leve", "o .mov com alfa ficou gigante", "que encoders existem nesta
  máquina?", "dá para usar a Intel em vez da NVIDIA?", "a placa está sendo
  usada mesmo?", "renderiza tudo de uma vez sem estourar a GPU", "por que o
  NVENC não acelerou nada?" — ou quando o render morre com
  `avcodec_open2("h264_nvenc", ...)` / `Generic error in an external library` /
  `UnknownCodecError: libdav1d`. Desfaz a confusão que mais custa tempo aqui:
  acelerar a RASTERIZAÇÃO e acelerar o ENCODING são coisas diferentes, e
  trocar o renderer nunca conserta um gargalo de encoder. NÃO use para:
  caminho do arquivo de saída, `--format png`, `-n a,b` ou a API
  `render_file` (skill `manim-render-api`); rodar VÁRIAS cenas em processos
  paralelos (skill `manim-batch-pipeline`); o cache de partial movies e o
  custo de RASTERIZAR uma cena cara — `always_redraw`, `NumberPlane` fino
  (skill `manim-performance-cache`); olhar o frame para conferir o resultado
  (skill `manim-verificacao-visual`); cor de fundo, tema e transparência como
  decisão visual (skill `manim-color-theming`); áudio e legenda (skill
  `manim-som-legendas`); seções e `next_section` (skill `manim-cenas-secoes`);
  erro que não é de codec/GPU (skill `manim-troubleshooting`); a API do ManimGL
  em si (skill `manimgl-3b1b`); e o formato de vídeo em partes para slide
  (skill `manim-presentation-parts`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
---

# GPU, codec, pix_fmt e peso do arquivo

Tudo aqui foi medido nesta máquina — RTX 4070 Laptop (8188 MiB), driver
**580.159.03**, CUDA 13.0, i9-14900HX (32 threads), ManimCE **0.21.0**,
PyAV **18.1.0** (libavcodec **62**.28.102, libavformat 62.12.102,
libavfilter 11.14.102), `/usr/bin/ffmpeg` 6.1.1 (libavcodec **60**.31.102).
**Data das medições: 2026-08-19.** Onde algo não foi executado, está escrito
que não foi.

Marcadores usados no arquivo inteiro:

| Marcador | Quer dizer |
|---|---|
| **[MEDIDO]** | render/encode executado e cronometrado nesta máquina, na data |
| **[SONDADO]** | consultado ao vivo sem renderizar (abrir um `Codec`, `nvidia-smi`, `mx gpu`, `mx presets`) |
| **[FONTE-LIDA]** | lido no código do ManimCE/`manimx`/PyAV, com arquivo e linha |
| **[DECK]** | medido pelo repositório consumidor `~/Projects/aulas`, não reproduzido aqui |
| **[NÃO VERIFICADO]** | raciocínio coerente com o código, sem execução — trate como hipótese |

Aviso de método que vale para a skill inteira: as medições de **tempo** desta
sessão saíram com a máquina rodando outras renderizações em paralelo
(`load average` entre 14 e 52 num CPU de 32 threads). Peso de arquivo e
qualidade **não** dependem disso e são exatos; tempo depende, e por isso todo
número de tempo aqui vem com a carga ao lado. A lição não é o número: é que
você precisa medir **na sua máquina, em repouso**, com `bin/mx bench`.

---

## 0. O cartão de 30 segundos

Se você só precisa decidir agora:

| A pergunta | A resposta | Onde está o porquê |
|---|---|---|
| Vou iterar e jogar fora | `--codec nvenc-fast -q m` | §8 |
| Render de trabalho, ninguém versiona | `--codec nvenc` (o default do `mx`) | §8 |
| Entrega final, peso não importa | `--codec nvenc-quality` | §8 |
| **Vai entrar num repositório git** | `--codec x264` — ou NVENC + reencode | §8, §9 |
| Preciso do arquivo pequeno com qualidade | render em NVENC, reencode com `/usr/bin/ffmpeg -c:v libx264 -crf 20 -preset slow` | §8 |
| Preciso de alfa para a web | `-t --format webm` (VP9 yuva420p) e **não** `-t` sozinho | §10 |
| Preciso de alfa para NLE | `-t` sozinho (`.mov` + qtrle), e aceite o tamanho | §10 |
| Quero AV1 | **não pelo Manim.** Reencode a entrega | §12 |
| Preciso de GIF limpo | renderize mp4 e converta fora do Manim | §11 |
| Qual qualidade? | `-q h` é 1080p60 e é o teto útil de vídeo de aula. `-q p`/`-q k` custam 1,8× e 4× em pixels | §3 |
| "Está lento" | `bin/mx gpu` → `bin/mx bench` **com a máquina em repouso** | §19 |
| "Não acelerou nada" | seu gargalo não é o encoder: é rasterização ou texto/LaTeX | §1, §19 |
| Vou renderizar várias cenas ao mesmo tempo | `processos × max_inflight_encoders ≤ 6` | §13 |
| Quanto isso vai pesar? | ~0,29 MB por segundo de vídeo em 1080p60 nvenc-quality (conteúdo de aula real) | §9 |

E a regra que resolve metade das dúvidas desta skill:

> **NVENC não é "o mesmo arquivo, mais rápido". É um arquivo MUITO maior,
> mais rápido.** Encoder de hardware compra velocidade gastando bits.

---

## 1. As etapas de um render, e por que "usar a GPU" é ambíguo

Uma renderização do ManimCE tem etapas com custos **independentes**. A maior
parte da confusão vem de tratá-las como uma só.

| # | Etapa | Quem faz | Como acelerar | GPU ajuda? |
|---|---|---|---|---|
| 0 | **Texto e LaTeX** → SVG | Pango/cairo · dvisvgm | reaproveitar mobject, cache | **não** |
| 1 | **Rasterizar** a geometria em frames RGBA | Cairo (CPU) · ModernGL (GPU) · wgpu/Vulkan (ManimGL) | trocar o **renderer** | às vezes — meça |
| 2 | **Codificar** cada *partial movie* | libx264 (CPU) · NVENC (GPU) | trocar o **codec** | sim, e muito |
| 3 | **Juntar** os partial movies no arquivo final | libav, **stream copy** | nada a fazer | irrelevante |
| 4 | **Muxar o áudio** (só se a cena tiver som) | libav, segunda passada de mux | nada a fazer | irrelevante |

Consequências que economizam horas:

- trocar só o **codec** não acelera cena pesada de geometria;
- trocar só o **renderer** não acelera cena longa e visualmente simples;
- a etapa 3 é cópia de pacote, **sem recodificar** — por isso trocar o codec
  dos parciais troca o arquivo final inteiro sem passo extra;
- a etapa 3 é a única que **falha** por causa de codec exótico (§12);
- a etapa 0 é a que mais engana. Numa cena de aula com muito texto é comum o
  gargalo estar aí, e nesse caso NVENC, OpenGL e `-j` não mudam nada. Ver
  `manim-text-latex` para o custo do texto e `manim-performance-cache` para o
  cache que o evita.

A pergunta diagnóstica que separa tudo, em uma linha: **renderize a mesma cena
em `-q l` e em `-q h`.** Se o tempo mal muda, o gargalo é a etapa 0 (texto), que
não depende de resolução. Se o tempo escala com os pixels, é 1 ou 2 — e aí
`bin/mx bench` diz qual.

---

## 2. Como o ManimCE grava vídeo, por dentro

Você precisa disto para entender por que a camada `manimx` existe e por que
ela é um *monkeypatch* e não um flag.

**O ManimCE não chama mais o binário `ffmpeg`.** Ele usa **PyAV** direto, em
`manim/scene/scene_file_writer.py`. Consequência imediata: **não existe flag de
CLI para trocar o codec**, porque o valor está escrito no código.

### 2.1 A escolha de codec e pix_fmt, literal

[FONTE-LIDA] `scene_file_writer.py:656-672`, dentro de
`open_partial_movie_stream`:

```python
partial_movie_file_codec  = "libx264"
partial_movie_file_pix_fmt = "yuv420p"
av_options = {"an": "1", "crf": "23"}

if config.movie_file_extension == ".webm":
    partial_movie_file_codec = "libvpx-vp9"
    av_options["-auto-alt-ref"] = "1"
    if config.transparent:
        partial_movie_file_pix_fmt = "yuva420p"
elif config.transparent:
    partial_movie_file_codec = "qtrle"
    partial_movie_file_pix_fmt = "argb"
```

A tabela completa do que sai, por combinação de flags [FONTE-LIDA]:

| Flags | extensão | codec dos parciais | pix_fmt | quem escolhe |
|---|---|---|---|---|
| (nada) | `.mp4` | `libx264` crf 23 | `yuv420p` | `:656-658` |
| `--format mov` | `.mov` | `libx264` crf 23 | `yuv420p` | `resolve_movie_file_extension` |
| `--format webm` | `.webm` | `libvpx-vp9` | `yuv420p` | `:664-665` |
| `-t` | `.mov` | `qtrle` | `argb` | `:670-671` |
| `-t --format webm` | `.webm` | `libvpx-vp9` | **`yuva420p`** | `:664-667` |
| `--format gif` | `.gif` | mp4/libx264 **intermediário** → gif | `rgb8` na saída | §11 |
| `--format png` | `.png` | nenhum — não passa por encoder de vídeo | — | — |

Duas coisas para guardar desta tabela: **o pix_fmt nunca é escolha sua** (§7), e
**alfa tem dois caminhos com pesos que diferem por ordens de grandeza** (§10).

### 2.2 A ordem das operações

1. **cada `self.play` abre um container próprio** — o *partial movie file*.
   `open_partial_movie_stream()` chama `av.open(path, mode="w")` e
   `container.add_stream("libx264", rate=fps, options=av_options)`;
2. os frames vão para uma **fila**, e uma **thread** (`_PartialMovieEncodeJob`,
   `:94-190`) consome e codifica enquanto a cena continua sendo rasterizada;
3. no fim, `combine_files` (`:826`) abre o concat dos parciais e faz
   `output_container.add_stream_from_template(template=partial_movies_stream)`
   — **stream copy**, pacote a pacote, sem recodificar;
4. se a cena tem som, `combine_to_movie` (`:932-1010`) faz uma **segunda**
   passada de mux para um arquivo `_temp`, juntando vídeo (de novo por
   template, de novo sem recodificar) e o áudio já convertido para AAC.

Detalhes da etapa 2 que valem dinheiro:

- [FONTE-LIDA `:156-166`] cada frame vira
  `av.VideoFrame.from_ndarray(frame, format="rgba")` — **um objeto novo por
  frame**, com um comentário do próprio Manim explicando por que não dá para
  reaproveitar (`mux` consome o packet, e reusar o `av_frame` "renders
  weird-looking frames"). É por isso que a etapa 2 tem custo de CPU mesmo em
  NVENC: a conversão RGBA→yuv420p é do lado do host;
- [FONTE-LIDA `:176-186`] quando um job falha, o `join()` **apaga o arquivo
  parcial** — de propósito, para que uma execução posterior não acerte o cache
  num arquivo truncado. Se você ver um partial movie sumir depois de um erro,
  é isto, não corrupção;
- [FONTE-LIDA `:802-824`] `is_already_cached()` **espera** o job em voo daquele
  mesmo caminho antes de responder. Cache e encoding paralelo conversam; ver
  `manim-performance-cache`.

### 2.3 A alavanca que isso abre

Se você trocar o codec dos *partial movies*, o arquivo final sai naquele codec
**de graça**, porque a junção só copia. É exatamente o que
`manimx.gpu.enable_nvenc()` faz — e é por isso que ela é um patch de
`add_stream` e não uma reescrita do writer.

---

## 3. Qualidade e resolução: o orçamento de pixels

`bin/mx presets` [SONDADO hoje] imprime os cinco presets aceitos por `-q`:

```
  l  854x480 @ 15fps   (low_quality)
  m  1280x720 @ 30fps  (medium_quality)
  h  1920x1080 @ 60fps (high_quality)
  p  2560x1440 @ 60fps (production_quality)
  k  3840x2160 @ 60fps (fourk_quality)
```

A tabela que falta em todo lugar é a de **carga**, porque é ela que prevê
tempo, memória e peso — não a resolução sozinha:

| `-q` | resolução @ fps | px/frame | **px/s** | vs `-q h` | frame RGBA | fila de 8 frames |
|---|---|---:|---:|---:|---:|---:|
| `l` | 854×480 @15 | 0,41 M | **6,1 M** | 0,05× | 1,64 MB | 13 MB |
| `m` | 1280×720 @30 | 0,92 M | **27,6 M** | 0,22× | 3,69 MB | 30 MB |
| `h` | 1920×1080 @60 | 2,07 M | **124,4 M** | 1,00× | 8,29 MB | 66 MB |
| `p` | 2560×1440 @60 | 3,69 M | **221,2 M** | 1,78× | 14,75 MB | 118 MB |
| `k` | 3840×2160 @60 | 8,29 M | **497,7 M** | 4,00× | 33,18 MB | 265 MB |

(px/s = largura × altura × fps; "fila de 8 frames" é o custo de RAM de **um**
job de encode em voo, §14. Aritmética conferida, não medida.)

Leituras práticas:

- **`-q l` não é "um pouco pior": é 1/20 do trabalho de `-q h`.** É a
  qualidade certa para conferir composição, e péssima para conferir
  legibilidade de texto — em 480p um `font_size` pequeno some, e você vai
  "consertar" um problema que não existe em 1080p;
- **`-q m` é o meio-termo honesto para iterar** (0,22× do trabalho), e é o que
  o repositório de aulas usa no modo rápido [DECK];
- **`-q p` e `-q k` são armadilha para vídeo de slide.** Nenhum projetor de
  sala mostra mais que 1080p, o palco do reveal é 1280×720, e você paga 1,8×
  ou 4× em tempo, RAM e bytes por nada. [DECK] a skill do deck consumidor
  chega a escrever "**nunca renderize em `-q p` ou `-q k`**";
- em `-q k` com `-j` alto o que estoura **não é a VRAM, é a RAM**: 4 jobs em
  voo × 265 MB ≈ 1,06 GB só de filas de frame (§14).

### 3.1 O preset escondido

[FONTE-LIDA `manim/constants.py:206-243`] `QUALITIES` tem **seis** entradas, não
cinco. A sexta é `example_quality` (854×480 @ **30** fps) e ela tem
`"flag": None` — **não é alcançável por `-q`**. Ela existe para os exemplos da
documentação. Se você precisa de 480p a 30 fps, o caminho é
`-q l --fps 30` ou `config.frame_rate = 30`, não um nome de preset.

### 3.2 `-r` e `--fps` sobrescrevem `-q` — mas não a mesma coisa

Esta é a armadilha de configuração mais cara desta área, e ela tem uma
divergência conhecida entre skills.

[FONTE-LIDA] `manimx/render.py:_build_config` monta o dict com `"quality"`
como **primeira** chave e `pixel_width`/`pixel_height` depois.
`ManimConfig.update` (`_config/utils.py:387-395`) aplica em duas passadas: as
chaves que já existem em `_d` primeiro, **na ordem de inserção do dict**, e as
demais depois. `"quality"` está em `_OPTS` (`utils.py:298`), portanto em `_d`,
portanto é aplicada **antes**. E o setter de `quality` (`utils.py:1344-1352`)
escreve **frame_size e frame_rate**.

Resultado, e é contraintuitivo:

```bash
bin/mx render cena.py Cena -q l -r 1280x720
# resolução: 1280×720  (veio do -r)
# fps:          15      (continuou vindo do -q l)
# diretório de saída: .../720p15/
```

Ou seja: **`-r` sobrescreve a resolução e deixa o FPS do `-q` de pé.** Para
mudar o fps use `--fps`. `manim-render-api` diz na linha 57 que `-r` "ignora
`-q`" — **está errado**, e `manim-project:375` mediu o `720p15` que prova.
Onde divergirem, vale este parágrafo e a medição.

Por que isso está numa skill de encoding: fps é metade do orçamento de pixels
da tabela acima, e um `-r 3840x2160` deixado com `-q l` entrega 4K a 15 fps —
arquivo grande, movimento aos trancos, e a impressão de que "o NVENC não
adiantou".

---

## 4. Ligar NVENC no ManimCE

### 4.1 Pela CLI

```bash
bin/mx render cena.py Cena --codec nvenc            # p4 cq20 — o default do mx
bin/mx render cena.py Cena --codec nvenc-fast       # p1 cq26 — iterar
bin/mx render cena.py Cena --codec nvenc-quality    # p7 cq16 + AQ — entrega
bin/mx render cena.py Cena --codec hevc             # hevc_nvenc p7 cq16
bin/mx render cena.py Cena --codec x264             # CPU, o padrão do Manim
```

**`bin/mx render` já sai em `--codec nvenc` sem você pedir**
([FONTE-LIDA] `manimx/cli.py:463`, `default="nvenc"`). O `bin/manim` cru **não
tem** flag de codec e sempre grava `libx264` — e é assim de propósito: ele é
passthrough puro para o CLI do ManimCE, que não expõe codec nenhum.

### 4.2 Pela API Python

```python
from manimx.gpu import enable_nvenc, disable_nvenc, nvenc_options, active_encoder

enable_nvenc(codec="h264_nvenc", profile="quality")   # -> True se aplicou
try:
    ...                                               # renderize
finally:
    disable_nvenc()
```

Assinaturas reais [FONTE-LIDA `manimx/gpu.py`]:

```python
enable_nvenc(codec: str = "h264_nvenc",
             profile: str = "balanced",
             *,
             options: dict[str, str] | None = None,
             strict: bool = False) -> bool
disable_nvenc() -> None
nvenc_options(profile: str = "balanced", codec: str = "h264_nvenc") -> dict[str, str]
nvenc_available(codec: str = "h264_nvenc") -> bool
validate_encoder(codec: str, options: dict[str, str], *,
                 width: int = 256, height: int = 144) -> tuple[bool, str | None]
detect_gpu() -> GPUReport
prime_env() -> dict[str, str]
wgpu_adapters() -> list[str]
active_encoder() -> dict[str, Any]     # estado do patch; {} se inativo
```

- **`strict=True`** levanta `RuntimeError` em vez de cair em CPU calado. Use em
  CI, onde "saiu mais devagar" é melhor descoberto do que escondido;
- `enable_nvenc` é **idempotente**: chamar de novo só troca as opções;
- `options=` entra **por cima** do perfil — é como você aplica um `cq` seu sem
  reescrever o perfil inteiro:
  `enable_nvenc(profile="quality", options={"cq": "22"})`;
- **detalhe de import que morde:** `manimx.gpu.__all__` tem 8 nomes e **não
  inclui `validate_encoder` nem `active_encoder`** [FONTE-LIDA
  `manimx/gpu.py:46-55`]. Import explícito funciona; `from manimx.gpu import *`
  **não traz os dois**. Se você escreveu `import *` e recebeu
  `NameError: active_encoder`, é isso.

### 4.3 O que o patch faz, e o que ele NÃO toca

Em vez de reescrever `open_partial_movie_stream`, o `manimx` intercepta
`av.open` **só durante** aquela chamada e devolve um proxy cujo `add_stream`
reescreve o codec. Isso sobrevive a mudanças internas do Manim.

E o proxy tem um escopo estreito, de propósito
([FONTE-LIDA] `manimx/gpu.py:451-456`, dentro de `_StreamRewriteProxy.add_stream`):

```python
if requested != "libx264":
    return inner.add_stream(*args, **kwargs)   # qtrle e libvpx-vp9 passam intactos
merged.pop("crf", None)                        # crf é do x264; NVENC usa cq
```

Traduzindo: **`-t` (qtrle) e `--format webm` (VP9) nunca são reescritos.** Pedir
`--codec nvenc -t` não é erro — a camada ignora o NVENC de propósito e mantém
`qtrle`. [MEDIDO]:

```console
$ bin/mx render tiny.py Tiny -q l --codec nvenc -t --json | grep -E 'codec|output'
    "output_file": ".../Tiny.mov",
    "codec": "qtrle",
```

E há uma **cinta de segurança dupla**: além do proxy, `manimx/render.py:398` só
chama `enable_nvenc` quando `use_gpu and not transparent and fmt not in
("gif", "png", "webm")`. Ou seja, no caminho do `mx render` o patch nem chega a
ser aplicado nesses formatos [FONTE-LIDA].

**Por que o escopo estreito importa mais do que parece.** [SONDADO hoje]
`h264_nvenc` aceita `rgba` e `bgra` na lista de pix_fmts de entrada — mas H.264
não carrega canal alfa: o encoder converteria e **descartaria** o alfa. E o
`argb` que o Manim usa para `-t` nem está na lista. Se o proxy reescrevesse o
`qtrle`, o melhor caso seria um erro de pix_fmt e o pior seria um vídeo
silenciosamente **opaco**. A limitação não é "NVENC não abre o encoder": é
"H.264/HEVC não têm onde guardar o alfa".

### 4.4 O que acontece numa máquina sem NVIDIA

Nada quebra. `enable_nvenc()` devolve `False`, loga um `WARNING` e o render
continua em `libx264`. Os wrappers `bin/*` também são condicionais:
`manimx_enable_gpu` só exporta as variáveis de PRIME **depois** de confirmar a
placa com `manimx_has_nvidia` [FONTE-LIDA `bin/manim-env.sh`].

O preço dessa gentileza é o CI que "acelerou" e continua em CPU — para isso
existe `strict=True`.

---

## 5. Os perfis NVENC, opção por opção

[SONDADO hoje via `bin/mx presets`; a fonte é `manimx/gpu.py:NVENC_PROFILES`]

```python
NVENC_PROFILES = {
  "fast":     {"preset":"p1", "tune":"hq", "rc":"vbr", "cq":"26", "b":"0"},
  "balanced": {"preset":"p4", "tune":"hq", "rc":"vbr", "cq":"20", "b":"0",
               "spatial-aq":"1","temporal-aq":"1","rc-lookahead":"20","bf":"3"},
  "quality":  {"preset":"p7", "tune":"hq", "rc":"vbr", "cq":"16", "b":"0",
               "spatial-aq":"1","temporal-aq":"1","aq-strength":"12",
               "rc-lookahead":"32","bf":"3","multipass":"fullres"},
  "lossless": {"preset":"p7", "tune":"lossless"},
}
```

| Opção | O que faz | Por que está aí |
|---|---|---|
| `preset` `p1`…`p7` | velocidade × qualidade do encoder | `p1` é o mais rápido e o pior; `p7` é o mais lento e o melhor. Não confunda com os presets antigos (`slow`, `hq`, `llhq`) — são a escala legada |
| `tune=hq` | perfil de sintonia | as outras opções são `ll`, `ull` (streaming) e `lossless` |
| `rc=vbr` + `cq=N` + `b=0` | taxa por **qualidade constante** | `b=0` é obrigatório: sem ele o VBR mira um bitrate e o `cq` vira teto, não alvo |
| `spatial-aq` / `temporal-aq` | quantização adaptativa | é o que mata **banding** em gradiente liso — o defeito clássico do NVENC em animação |
| `aq-strength=12` | força da AQ (1–15) | só no perfil `quality` |
| `rc-lookahead` | quantos frames o RC olha à frente | 20/32; custa latência, não qualidade |
| `bf=3` | quadros B | ganho de compressão praticamente de graça em Ada |
| `multipass=fullres` | duas passadas em resolução plena | só no `quality`; é o que mais pesa no tempo |
| `profile` | `high` (H.264) / `main` (HEVC) / **inexistente** (AV1) | injetado por `nvenc_options`, não por você — §5.2 |

**`cq` não é `crf`.** As duas escalas vão de 0 a 51 e as duas são "menor =
melhor", mas os números **não** se traduzem: `cq 20` no NVENC produz arquivo
muito maior que `crf 23` no x264 (§8). Nunca copie um número de uma escala para
a outra "porque é parecido".

**`tune=lossless` é lossless de verdade — [MEDIDO], não presumido.** Um frame
de ruído aleatório 640×360 foi codificado e decodificado de volta:

```
lossless       max|delta| = 0    média = 0.0000   idêntico = True
quality cq16   max|delta| = 142  média = 11.5     idêntico = False
```

(Ruído é o pior caso possível para o cq 16; conteúdo de animação real erra
muito menos. O ponto é só que `lossless` é bit a bit.)

### 5.1 Como escolher um `cq` sem chutar

O caminho barato é medir **um** partial movie, não a cena:

```python
from manimx.gpu import validate_encoder, nvenc_options
for cq in ("16", "20", "23", "26", "30"):
    opts = nvenc_options("quality") | {"cq": cq}
    print(cq, validate_encoder("h264_nvenc", opts))
```

Isso só prova que a opção **abre**. Para o peso, renderize UMA cena curta
(≤ 3 s) com dois valores e compare `stat -c%s`. Não use a cena inteira para
calibrar: você paga o render completo duas vezes para descobrir um número que
uma cena de 3 s já entrega.

### 5.2 As três tabelas de compatibilidade por codec

[FONTE-LIDA `manimx/gpu.py`] `nvenc_options()` não é cosmética: ela consulta
três dicionários antes de devolver as opções.

```python
CODEC_PROFILE             = {"h264_nvenc": "high", "hevc_nvenc": "main"}
CODEC_UNSUPPORTED_OPTIONS = {"av1_nvenc": ("profile",)}
CODEC_PROFILE_FALLBACK    = {("av1_nvenc", "lossless"): "quality"}
```

O que cada uma evita:

- `profile=high` **só existe em H.264**. Em HEVC o nome é `main`; em AV1 a
  opção não existe. Passar o valor errado faz `avcodec_open2` devolver EINVAL —
  e como **o PyAV só abre o encoder no primeiro frame**, o erro apareceria no
  meio da renderização, com a cena inteira já computada;
- `av1_nvenc` não tem `tune=lossless`: o pedido cai para `quality` e o
  `logger.info` avisa.

**A lição transferível:** opção de encoder não é validada quando você a passa,
e sim quando o primeiro frame chega. Por isso `validate_encoder()` existe, e
por isso ele roda **antes** do render, não durante.

---

## 6. O inventário REAL de encoders desta build

`bin/mx gpu` sonda **10** nomes escolhidos a dedo
([FONTE-LIDA] `manimx/gpu.py:PROBE_ENCODERS`) — não é o inventário, é uma
lista curada.

**Correção de número.** Uma versão anterior desta seção dizia que o inventário
do PyAV 18.1.0 desta máquina "tem **37** encoders". É **3× menor que o real**.
Re-sondado hoje, `Codec(nome, "w")` sobre `av.codecs_available`:

```console
PyAV 18.1.0
encoders total (todos os tipos): 207
encoders de VÍDEO (nomes únicos): 115
```

A tabela abaixo é, portanto, uma **seleção** — os que importam para o Manim —
não o inventário. Faltam ~100 encoders de vídeo que existem e não estão aqui;
para varrer o conjunto todo, sonde você mesmo em vez de confiar na tabela:

```python
import av
from av.codec import Codec
for n in sorted(av.codecs_available):
    try: c = Codec(n, "w")
    except Exception: continue
    if c.type == "video":
        print(c.name, [f.name for f in (c.video_formats or [])])
```

Dos que interessam:

| Família | Encoders presentes | Serve para o Manim? |
|---|---|---|
| H.264 | `libx264`, **`libx264rgb`**, `h264_nvenc`, `h264_qsv`, `h264_amf`, `h264_v4l2m2m` | `libx264` (default) e `h264_nvenc` (§4). Os demais: §6.2 |
| HEVC | `libx265`, `hevc_nvenc`, `hevc_qsv`, `hevc_amf`, `hevc_v4l2m2m` | `hevc_nvenc` via `--codec hevc` |
| AV1 | `libsvtav1`, `av1_nvenc`, `av1_qsv`, `av1_amf` | **nenhum** — §12 |
| VP8/VP9 | `libvpx` (VP8), `libvpx-vp9`, `vp9_qsv`, `vp8_v4l2m2m` | `libvpx-vp9` via `--format webm` |
| Sem perdas / intermediário | `qtrle`, `ffv1`, `utvideo`, `huffyuv`, `prores`, `prores_aw`, `prores_ks`, `dnxhd`, `rawvideo` | só `qtrle` está no caminho do Manim; os outros são reencode (§10) |
| Imagem / animação | `png`, `apng`, `gif`, `mjpeg`, `mjpeg_qsv` | `png` e `gif` pelos formatos |

Notavelmente **ausentes**: `libaom-av1` e `librav1e` — [SONDADO]
`Codec("libaom-av1","w")` levanta `UnknownCodecError`. Eles existem no
`/usr/bin/ffmpeg` do sistema, não nesta build do PyAV. É por isso que o caminho
de AV1 é sempre "reencode fora do Manim" (§12).

### 6.1 O alias que engana o diagnóstico

[SONDADO hoje] `Codec(nome, "w")` **não é busca exata**: quando o nome é o de
um *codec* e não de um *encoder*, o PyAV resolve pelo descritor e devolve o
encoder padrão daquele codec.

```
Codec("h264", "w")    -> name='libx264'    (libx264 H.264 / AVC)
Codec("hevc", "w")    -> name='libx265'    (libx265 H.265 / HEVC)
Codec("av1",  "w")    -> name='libsvtav1'  (SVT-AV1)
Codec("vp9",  "w")    -> name='libvpx-vp9'
Codec("libdav1d","w") -> UnknownCodecError: libdav1d
```

Duas consequências:

1. um probe do tipo "existe encoder `h264`?" responde **sim** sem dizer qual —
   se você está escrevendo diagnóstico, imprima `Codec(n, "w").name`, não o
   nome que você pediu;
2. **é exatamente esse mecanismo que explica o buraco do AV1 (§12).** A junção
   procura um encoder com o nome do *decodificador* do stream de entrada.
   `h264` e `hevc` resolvem por acaso; `libdav1d` não resolve para nada.

### 6.2 QSV, AMF, V4L2: o segundo pool de encoders que ninguém liga

[SONDADO hoje] Esta máquina tem os encoders da **Intel Quick Sync** (`h264_qsv`,
`hevc_qsv`, `av1_qsv`, `vp9_qsv`) compilados no PyAV. Em tese isso é um pool de
sessões de encode **independente do NVENC** — o candidato natural para quando as
8 sessões da NVIDIA acabam (§13).

Na prática, **não está ligado, e não é drop-in.** O motivo é concreto e
[SONDADO]: os pix_fmts que `h264_qsv` aceita são `['nv12', 'qsv']` — e
`open_partial_movie_stream` escreve `stream.pix_fmt = "yuv420p"` **depois** que
o `_StreamRewriteProxy` já devolveu o stream. O proxy reescreve o codec e as
opções; ele **não** toca no pix_fmt. Um `enable_nvenc(codec="h264_qsv")`
abriria um stream QSV com um pix_fmt que ele não aceita.

Estado honesto: **[NÃO VERIFICADO]** — não renderizei com QSV, e nem sei se o
driver VA-API desta máquina expõe o dispositivo. Se alguém for tentar, o teste
barato que responde em segundos, sem render:

```python
from manimx.gpu import validate_encoder
print(validate_encoder("h264_qsv", {"preset": "medium", "global_quality": "23"}))
```

E o patch precisaria de um passo a mais que o atual não tem: forçar
`stream.pix_fmt = "nv12"`. Ver §20.

Os `*_amf` são de GPU AMD e os `*_v4l2m2m` são de SoC ARM/Raspberry — presentes
na build, inúteis nesta máquina.

### 6.3 A família sem perdas, e para que cada um serve

Os pix_fmts abaixo são [SONDADO hoje] direto do `Codec(...).video_formats`:

| Encoder | pix_fmts que interessam | Onde entra |
|---|---|---|
| `qtrle` | `rgb24`, `argb`, `rgb555be`, `gray` | é o que o Manim usa em `-t`. RLE simples: **enorme** (§10) |
| `ffv1` | `yuva420p`, `yuva422p`, `yuva444p`, `yuv444p`, `bgr0`… (61 formatos) | arquivamento sem perdas **com alfa**, muito menor que qtrle |
| `utvideo` | `gbrp`, `gbrap`, `yuv444p` | sem perdas com alfa, rápido de decodificar em NLE |
| `huffyuv` | `yuv422p`, `rgb24`, `bgra` | legado; use `ffv1` |
| `prores_ks` | `yuv422p10le`, `yuv444p10le`, **`yuva444p10le`** | 10 bits **com alfa** — o formato que um NLE realmente quer |
| `libx264rgb` | `bgr0`, `bgr24`, `rgb24` | H.264 em RGB (sem subamostragem de croma), `crf 0` = sem perdas. É o que o `custom_config.yml` sugere para o ManimGL |
| `libx265` | `yuv420p`, …, **`yuva420p`**, `yuv444p12le` | HEVC com alfa e 12 bits, se o destino aguentar |
| **`ffvhuff`** | 14 formatos com alfa: `yuva420p`, `yuva422p`, `yuva444p`, `gbrap`, `bgra`, `yuva420p10le`… | **sem perdas com alfa e muito mais rápido que `ffv1`** — o melhor candidato para intermediário local. Estava ausente desta tabela |
| **`magicyuv`** | `gbrap`, `yuva444p` | sem perdas com alfa, decodifica rápido. Também estava ausente |
| **`libwebp_anim`** | `bgra`, `yuva420p` | WebP **animado com alfa** — concorrente direto de `-t --format webm` para web. Também ausente |

**[SONDADO hoje]** dos 115 encoders de vídeo, **39** oferecem ao menos um
`pix_fmt` com canal alfa. Os três acima são os que faltavam nesta tabela e que
mudam a decisão do §10.3.

Nenhum deles está no caminho do ManimCE hoje. Eles importam para o **passo
seguinte**: reencodar a entrega (§9, §10).

---

## 7. `pix_fmt`: o eixo que ninguém olha

Você não escolhe o pix_fmt no Manim. Ele é escrito na mão em
`open_partial_movie_stream` (§2.1) e atribuído ao stream **depois** de ele ser
criado, o que quer dizer que nem o `options=` do `enable_nvenc` alcança —
`options` vai para o dicionário de opções privadas do codec, e `pix_fmt` é
atributo do stream.

Na prática, todo vídeo normal do Manim é **`yuv420p`, 8 bits**. Isso tem duas
consequências visuais que aparecem no palco e nunca no terminal.

### 7.1 4:2:0 — a croma tem metade da resolução

`yuv420p` guarda luminância em resolução plena e **cor em 1/4 dos pixels**
(metade em cada eixo). Para foto isso é invisível. Para o material do Manim —
traço fino saturado sobre fundo chapado — não é:

- linha vermelha de 2 px sobre branco ganha franja alaranjada;
- texto azul pequeno sobre preto perde definição de borda;
- duas cores de croma próximas em contorno fino se misturam.

O que **não** resolve: reencodar depois. A informação de croma foi jogada fora
no primeiro encode; `-pix_fmt yuv444p` no reencode só duplica pixels vazios.

O que resolve, em ordem de custo:

1. **subir a resolução do render** (`-q h` em vez de `-q m`): a croma continua
   em 1/4, mas 1/4 de 1080p já é 960×540, o que costuma bastar;
2. **evitar traço fino em cor saturada** — a mesma informação em traço mais
   grosso, ou em tinta menos saturada, atravessa o 4:2:0 intacta. Isto é
   decisão de tema; ver `manim-color-theming`;
3. escrever o seu próprio patch de pix_fmt (§20). É a única via para
   `yuv444p` de verdade, e `h264_nvenc` **aceita** `yuv444p` [SONDADO] — mas
   nem todo player aceita H.264 4:4:4, e o ganho quase nunca paga a
   incompatibilidade.

### 7.2 8 bits — o banding em gradiente é estrutural

Um gradiente liso de canto a canto num quadro 1080p atravessa mais posições do
que 256 níveis conseguem representar: as faixas são inevitáveis em 8 bits, e o
encoder só decide se elas ficam suaves ou nítidas. É isso que `spatial-aq` e
`temporal-aq` fazem — e é por isso que os perfis `balanced` e `quality` os
ligam e o `fast` não.

O que **não** funciona: subir o `cq`, trocar para HEVC, ou reencodar em 10 bits.
Nenhum deles devolve precisão que o render não gerou. O que funciona
[NÃO VERIFICADO — raciocínio, não medição]: **quebrar a banda na própria cena**,
com um ruído de amplitude ~1/255 por cima do gradiente, ou trocar o gradiente
liso por um com textura. Se o seu material tem gradiente grande e liso, esse é
o custo de fazer vídeo em 8 bits, não um defeito do NVENC.

### 7.3 O caminho RGBA → yuv420p custa CPU, e ele não é acelerado

[FONTE-LIDA `scene_file_writer.py:156-166`] o Manim entrega
`av.VideoFrame.from_ndarray(frame, format="rgba")` e o stream está em
`yuv420p`: a conversão de espaço de cor acontece **no host, por frame**, no
libswscale. Com NVENC ligado, essa parte continua na CPU. É uma das razões
pelas quais "liguei a GPU e só acelerou 40%" é o resultado normal, e não um
sintoma.

---

## 8. Codec × tempo × peso × qualidade — a matriz medida

[MEDIDO 2026-08-19] Cena de teste: 7,5 s a **1080p60 (450 frames)**, com
gradiente liso (expõe banding), cor chapada, bordas duras e texto. Todos os
renders com `--no-cache`. Peso e qualidade são exatos; o tempo saiu com a
máquina sob carga 28–46 e serve só para ordem de grandeza.

| preset `--codec` | encoder real | **peso** | vs `x264` | MB por s de vídeo | tempo (carga alta) |
|---|---|---:|---:|---:|---:|
| `x264` | `libx264` crf 23 | **0,99 MiB** | 1,0× | 0,14 | 23,4 s (load 29) |
| `nvenc-fast` | `h264_nvenc` p1 cq26 | **1,59 MiB** | 1,6× | 0,22 | 27,4 s (load 35) |
| `nvenc` | `h264_nvenc` p4 cq20 +AQ | **4,04 MiB** | 4,1× | 0,56 | 19,4 s (load 31) |
| `nvenc-quality` | `h264_nvenc` p7 cq16 +AQ +multipass | **6,63 MiB** | 6,7× | 0,93 | 30,6 s (load 40) |
| `hevc` | `hevc_nvenc` p7 cq16 | **5,03 MiB** | 5,1× | 0,70 | 26,2 s (load 39) |
| `av1` | **cai para `libx264`** (§12) | 0,99 MiB | 1,0× | 0,14 | 32,4 s (load 46) |
| `webm` | `libvpx-vp9` (CPU) | **1,16 MiB** | 1,2× | 0,16 | 57,2 s (load 49) — o mais lento |
| `-t` / `transparent` | `qtrle` RGBA em `.mov` | **100,01 MiB** | **101×** | 14,0 | 17,7 s (load 44) |
| (referência) | `h264_nvenc` `tune=lossless` | 13,50 MiB | 13,6× | 1,89 | 14,5 s (load 28) |

**O achado que muda decisão: NVENC não é "mais rápido pelo mesmo arquivo". Ele
é mais rápido por um arquivo MUITO maior.** O `nvenc-quality` desta tabela pesa
**6,7×** o que o `libx264 crf 23` pesa. Isso é irrelevante num vídeo solto e é
decisivo num deck com dezenas de vídeos versionados — um repositório de aulas
que trocou x264 por `nvenc-quality` sem reparar multiplica a pasta por seis.

Leituras práticas da tabela:

- **`hevc` é 24% menor que `nvenc-quality`** (5,03 contra 6,63 MiB) — a frase
  "HEVC é ~30% menor" vale contra **H.264 de hardware**, não contra
  `x264 crf 23`, que continua 5× menor que os dois;
- **`nvenc-fast` (cq 26) é o único preset de hardware com peso na mesma ordem
  do x264.** É a escolha certa para iterar, e não só por ser rápido;
- **`webm` é o mais lento de todos** (57,2 s) porque `libvpx-vp9` é encoder de
  CPU e mal paralelizado. Ele é para a entrega na web, nunca para iterar. O
  próprio Manim avisa: [FONTE-LIDA `_config/utils.py:1068-1071`] o setter de
  `format` loga *"Output format set as webm, this can be slower than other
  formats"*;
- se o objetivo é **arquivo pequeno com qualidade**, o caminho não é escolher
  outro preset de NVENC: é renderizar em NVENC (rápido) e **reencodar a entrega
  com o `/usr/bin/ffmpeg`**. Não é porque falte encoder no PyAV — é porque no
  caminho do Manim você não escolhe `-preset slow`, nem duas passadas, nem
  `libaom-av1`/`librav1e` (que nem existem nesta build do PyAV, §6).

```bash
# entrega leve a partir do master em NVENC
ffmpeg -i cena.mp4 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p entrega.mp4
```

### 8.1 Tabela de decisão

| Situação | Codec |
|---|---|
| iterar, olhar e jogar fora | `nvenc-fast` (+ `-q m`) |
| render de trabalho, ninguém vai versionar | `nvenc` (o default do `mx`) |
| entrega final, peso não importa | `nvenc-quality` |
| **vídeo que vai para dentro de um repositório** | `x264` — ou NVENC + reencode |
| arquivo menor com público controlado | `hevc` |
| compatibilidade máxima (celular velho, NLE antigo) | `x264` |
| composição com alfa em NLE | `-t` → `.mov` + `qtrle` (§10) |
| alfa para a web, ou alfa que precisa caber | `-t --format webm` → VP9 `yuva420p` (§10) |
| web leve, sem alfa | `--format webm` |
| masterizar para reencode posterior | `enable_nvenc(profile="lossless")` |
| GIF | renderize mp4 e converta fora (§11) |
| AV1 | **não pelo Manim** — §12 |

### 8.2 Qualidade objetiva — SSIM e PSNR contra o render lossless

[MEDIDO] O render `tune=lossless` da tabela acima é a referência (é bit a bit,
§5). Cada candidato foi comparado com ele:

```bash
REF=.../lossless/Vitrine.mp4
ffmpeg -hide_banner -i candidato.mp4 -i "$REF" -lavfi "[0:v][1:v]ssim" -f null - 2>&1 | grep SSIM
ffmpeg -hide_banner -i candidato.mp4 -i "$REF" -lavfi "[0:v][1:v]psnr" -f null - 2>&1 | grep PSNR
```

| preset | peso | SSIM (All) | PSNR médio | MiB por 0,001 de SSIM acima do x264 |
|---|---:|---:|---:|---|
| `x264` crf 23 | 0,99 MiB | 0,998298 | 50,15 dB | — (base) |
| `nvenc-fast` cq 26 | 1,59 MiB | **0,998076** | 51,81 dB | pior que a base, e 60% maior |
| `nvenc` cq 20 | 4,04 MiB | 0,999512 | 59,52 dB | ~2,5 MiB por 0,001 |
| `nvenc-quality` cq 16 | 6,63 MiB | 0,999787 | 61,88 dB | ~3,8 MiB por 0,001 |
| `hevc` cq 16 | 5,03 MiB | 0,999718 | 62,08 dB | ~2,9 MiB por 0,001 |
| `webm` VP9 | 1,16 MiB | 0,998476 | **42,01 dB** | ~1,0 MiB por 0,001 — mas veja abaixo |
| `transparent` qtrle | **100,01 MiB** | (RGBA sem perdas) | — | outro universo |

Três conclusões que só aparecem com a coluna de peso ao lado:

1. **`nvenc-fast` não é "x264 mais rápido": é x264 60% mais pesado e um
   tiquinho pior** (SSIM 0,998076 contra 0,998298). Ele serve para iterar
   porque é rápido, não porque é bom;
2. **O NVENC compra qualidade real acima de cq 20** — SSIM 0,9995 e 0,9998 são
   altos de verdade — mas paga com 4× a 6,7× o tamanho. Se o seu olho não
   distingue, você está pagando peso por nada;
3. **`qtrle` pesa 101× o x264** (100 MiB para 7,5 s). É o preço do RGBA sem
   perdas, e é por isso que `-t` sozinho é para entregar a um NLE, jamais para
   versionar ou para pôr numa página (§10).

E uma quarta, que é uma aula sobre a própria métrica: o **`webm` tem SSIM
ligeiramente MELHOR que o `x264` (0,998476 contra 0,998298) e PSNR muito
PIOR (42,0 contra 50,2 dB)**. As duas medidas discordam porque olham coisas
diferentes — o VP9 preserva estrutura e erra mais em valor absoluto. Quando
duas métricas discordam assim, quem decide é o olho no frame.

Aviso honesto sobre a métrica: SSIM/PSNR medem fidelidade ao **render**, não
qualidade percebida. Em animação com cor chapada os dois superestimam;
*banding* em gradiente aparece pouco no número e muito no olho. Para banding,
o teste que vale é olhar o frame — e a defesa é `spatial-aq`/`temporal-aq`,
que os perfis `balanced` e `quality` já ligam. Como olhar o frame direito é
assunto de `manim-verificacao-visual`.

---

## 9. Orçamento de peso: quantos MB por segundo de vídeo

A pergunta "quanto isso vai pesar?" tem resposta antes de renderizar, e ela é a
diferença entre um repositório saudável e um repositório de 800 MB.

**A conta:** `peso ≈ duração_em_segundos × taxa`, onde a taxa depende do codec
**e do conteúdo**.

| Fonte da taxa | Conteúdo | Codec | **MB por segundo** |
|---|---|---|---:|
| [MEDIDO] cena "vitrine" (§8) | gradiente + texto + bordas duras, movimento constante | `nvenc-quality` | **0,93** |
| [MEDIDO] cena "vitrine" (§8) | idem | `x264` crf 23 | **0,14** |
| [DECK] 59 mp4 de aula real, 216,9 s / 63,0 MB | slides animados, muito quadro quase parado | `nvenc-quality` | **0,29** |
| [DECK] extremo baixo (`worktrees-p2`) | quase estático | `nvenc-quality` | **0,07** |
| [DECK] extremo alto (`orquestrador-p5`) | palco inteiro em movimento | `nvenc-quality` | **0,66** |

Como usar:

- **material de aula em 1080p60 com `nvenc-quality`: conte 0,29 MB/s.** Um
  minuto de vídeo ≈ 17 MB; dez minutos ≈ 175 MB;
- **a dispersão é de quase 10×** entre uma cena parada e uma cena inteira em
  movimento. Não é o preset que decide o peso: é quanto da tela muda por frame.
  A mesma duração custa 0,07 ou 0,66 MB/s dependendo da coreografia;
- **a cena sintética da §8 pesa 3,2× a taxa do material real** (0,93 contra
  0,29). Ela foi desenhada para ser difícil. Não use os números dela para
  orçar um deck — use os do deck;
- para prever o `x264`, a razão medida na vitrine é 6,7× menor
  ([MEDIDO], mas **extrapolar essa razão para outro conteúdo é estimativa**, não
  medição: a razão depende de quanto o conteúdo comprime).

### 9.1 O que entra no git

A política que o repositório consumidor adotou depois de commitar 81 MB de mp4
numa aula [DECK]:

> **`.mp4` fica FORA do git; `.png` fica DENTRO.**

O raciocínio transfere inteiro, e é sobre reconstrutibilidade, não sobre
tamanho: o mp4 é **derivado** — o `.py` versionado o reconstrói na máquina de
quem clonar. O `.png` do último frame é **pôster**: sem ele, o fallback
estático (PDF de backup, `prefers-reduced-motion`, o quadro antes do play) não
existe, e nenhum arquivo do repositório o reconstrói sem uma GPU.

O número de apoio que permite decidir antes de commitar: a mesma pasta com 59
mp4 e 118 png dá 80,3 MB — **63,0 de vídeo e 17,2 de pôster** [DECK]. Quando o
vídeo sai do git, o custo cai para 17 MB e o repositório continua completo para
quem só quer ler.

### 9.2 Três formas de emagrecer, em ordem de eficiência

1. **Encurtar a cena.** É a única que reduz custo em todas as dimensões ao
   mesmo tempo (tempo de render, peso, atenção da plateia). Cortar em mais
   partes curtas é melhor que uma parte longa — ver
   `manim-presentation-parts`;
2. **Reencodar a entrega em `x264 crf 20 -preset slow`.** Ganho medido de ~6,7×
   sobre `nvenc-quality` na vitrine, sem perda visível;
3. **Baixar a qualidade do render.** `-q m` custa 0,22× dos pixels de `-q h`
   (§3) — mas mexe na nitidez, então é a última alavanca, não a primeira.

Não está na lista: mudar o `cq`. Entre `cq 16` e `cq 20` você economiza 39% no
NVENC e ainda fica 4× acima do x264. É afinar o parafuso errado.

---

## 10. Alfa e webm: o caminho de transparência inteiro

Este é o assunto onde a escolha errada custa **duas ordens de grandeza** de
peso, e onde o Manim tem um caminho bom que quase ninguém usa.

### 10.1 Os dois caminhos que o Manim oferece

[FONTE-LIDA `scene_file_writer.py:664-671` + `_config/utils.py:1475-1490`]

```bash
bin/mx render cena.py Cena -t                     # -> Cena.mov   qtrle   argb
bin/mx render cena.py Cena -t --format webm       # -> Cena.webm  VP9     yuva420p
```

| | `-t` sozinho | `-t --format webm` |
|---|---|---|
| container | `.mov` | `.webm` |
| codec | `qtrle` (RLE sem perdas) | `libvpx-vp9` |
| pix_fmt | `argb` (8 bits, RGB pleno + alfa) | `yuva420p` (4:2:0 + alfa) |
| peso [MEDIDO, 7,5 s 1080p60] | **100,01 MiB** | não medido nesta sessão |
| perdas | nenhuma | sim, com perdas |
| onde toca | NLE (Premiere, Resolve, AE) | navegador (`<video>` com fundo atrás) |
| NVENC ajuda? | **não** — H.264/HEVC não têm alfa (§4.3) | **não** — NVENC não faz VP9 |

A conclusão prática que quase ninguém tira: **se o destino é uma página web ou
um slide HTML, `-t --format webm` é a resposta, e `-t` sozinho é um erro de
100 MiB.** O caminho `.mov`/`qtrle` só se justifica quando um NLE vai ler o
arquivo e você precisa de alfa sem perdas.

[FONTE-LIDA `:912-916`] a junção também acerta o alfa: quando
`config.transparent and movie_file_extension == ".webm"`, o
`add_stream_from_template` é seguido de `output_stream.pix_fmt = "yuva420p"`.
Não é acidente; é suporte de primeira classe.

### 10.2 A ordem em que você liga as duas coisas importa

[FONTE-LIDA] o setter de `transparent` chama
`resolve_movie_file_extension(value)`; o setter de `format` chama
`resolve_movie_file_extension(self.transparent)`. E
`resolve_movie_file_extension` (`utils.py:1475-1484`) decide:

```python
if is_transparent:
    self.movie_file_extension = ".webm" if self.format == "webm" else ".mov"
```

Ou seja: **quem for aplicado por último ganha**. No caminho do `mx render` isso
está certo por construção — `_build_config` põe `transparent` cedo e `format`
por último, então `format="webm"` roda com `transparent` já `True` e a extensão
sai `.webm`. Num script seu, se você fizer `config.format = "webm"` **antes**
de `config.transparent = True`, a extensão volta para `.mov` e você ganha um
qtrle de 100 MiB sem aviso nenhum — só um `logger.warning` dizendo *"Output
format changed to '.mov' to support transparency"*, que passa despercebido no
meio do log.

**Regra:** ligue `transparent` primeiro, `format` depois. Ou use
`-t --format webm` na CLI e não pense mais nisso.

### 10.3 Depois do render: os formatos de alfa que valem a pena

Se você precisa de alfa sem perdas mas 100 MiB é inaceitável, o caminho é
reencodar o `.mov` com um dos encoders que [SONDADO hoje] existem nesta build:

```bash
# ProRes 4444 — 10 bits com alfa, é o que um NLE realmente quer
ffmpeg -i cena.mov -c:v prores_ks -profile:v 4444 -pix_fmt yuva444p10le entrega.mov

# FFV1 — sem perdas com alfa, arquivamento
ffmpeg -i cena.mov -c:v ffv1 -level 3 -pix_fmt yuva444p entrega.mkv

# VP9 com alfa, para web, se você não renderizou direto em webm
ffmpeg -i cena.mov -c:v libvpx-vp9 -pix_fmt yuva420p -crf 30 -b:v 0 entrega.webm
```

[NÃO VERIFICADO] os três comandos não foram executados nesta sessão; o que foi
verificado é que os encoders e os pix_fmts existem (§6.3). Confira o resultado
com `ffprobe -show_entries stream=codec_name,pix_fmt`.

E a armadilha que fecha o assunto: **`-t` muda o fundo, não só o container.**
`config.transparent` é derivado de `background_opacity < 1.0`
[FONTE-LIDA `utils.py:1355-1363`], então ligar transparência é uma decisão
**visual** antes de ser uma decisão de codec — e essa metade é de
`manim-color-theming §12`, que documenta a catraca do `background_opacity`.

---

## 11. GIF: por que o seu sai sujo

`--format gif` é a única saída que **não** é stream copy, e ela perde qualidade
em três lugares diferentes.

[FONTE-LIDA `scene_file_writer.py:865-910`] o que acontece:

1. os partial movies são gravados **normalmente**, em `libx264` com **`crf 23`**
   — ou seja, o seu GIF nasce de um intermediário **já com perdas**;
2. eles são **decodificados** e passados por um filtergraph:
   `split → palettegen(stats_mode=diff) → paletteuse(dither=bayer:bayer_scale=5:diff_mode=rectangle)`;
3. o resultado é **recodificado** no encoder `gif`.

A terceira perda é a que ninguém procura, e ela está em duas linhas:

```python
output_stream = output_container.add_stream(codec_name="gif")
output_stream.pix_fmt = "rgb8"
if config.transparent:
    output_stream.pix_fmt = "pal8"
```

[SONDADO] o encoder `gif` aceita `['rgb8', 'bgr8', 'rgb4_byte', 'bgr4_byte',
'gray', 'pal8']`. `pal8` é **paleta adaptativa** — é exatamente o que o
`palettegen` acabou de calcular. `rgb8` é uma paleta **fixa** de 8 bits
(3 bits de vermelho, 3 de verde, 2 de azul).

Conclusão, marcada com honestidade: **[FONTE-LIDA] o Manim escolhe `rgb8` para
GIF opaco e `pal8` só quando `transparent` está ligado.** [NÃO VERIFICADO — não
renderizei um GIF nesta sessão] a consequência esperada é que, no caminho
opaco, a paleta adaptativa calculada pelo `palettegen` seja descartada na
conversão final para `rgb8`, e o GIF saia com as faixas características de
paleta fixa. Se alguém for conferir, o teste é um `ffprobe -show_entries
stream=pix_fmt` no GIF de saída e um olho no gradiente.

O que fazer, independentemente de qual das três perdas domina:

```bash
# renderize vídeo de verdade e converta fora do Manim
bin/mx render cena.py Cena -q h --codec nvenc-quality
ffmpeg -i cena.mp4 -vf "fps=15,scale=800:-1:flags=lanczos,split[a][b];\
[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5" saida.gif
```

Duas coisas a mais sobre o caminho GIF:

- **`--codec nvenc --format gif` não faz nada.** [FONTE-LIDA
  `manimx/render.py:398`] o NVENC nem é ligado para `gif`. O intermediário sai
  em `libx264 crf 23` de qualquer jeito;
- **GIF perde o áudio.** [FONTE-LIDA `:961`] a mixagem só roda quando
  `self.includes_sound and config.format != "gif"`. Assunto de
  `manim-som-legendas`; aqui basta saber que não é bug.

---

## 12. AV1: por que não sai, e o que fazer

`--codec av1` **não produz AV1.** Ele grava `libx264` e o render sai `OK`:

```console
$ bin/mx render tiny.py Tiny -q l --codec av1 --json | grep -E 'codec|WARNING'
WARNING manimx.gpu: NVENC 'av1_nvenc' recusou as opções do perfil 'quality':
  remux: UnknownCodecError: libdav1d — o codec grava, mas o Manim não consegue
  juntar os partial movies com ele. Encoding continua em libx264 (CPU).
    "codec": "libx264",
```

**A causa não é o NVENC nem a placa.** A placa é Ada (compute 8.9), o PyAV
abre `av1_nvenc` sem reclamar, e o encoder grava o partial movie
perfeitamente. Quem quebra é a **etapa 3**, a junção. [MEDIDO/SONDADO]:

```
# encoder usado -> decodificador que o PyAV escolhe ao reabrir -> existe como encoder?
h264_nvenc  -> h264       -> True   (resolve para libx264)
libx264     -> h264       -> True
hevc_nvenc  -> hevc       -> True   (resolve para libx265)
libx265     -> hevc       -> True
av1_nvenc   -> libdav1d   -> False      <-- aqui
libsvtav1   -> libdav1d   -> False      <-- e aqui também
```

`add_stream_from_template()` resolve o codec do stream de entrada **pelo
nome**. H.264 e HEVC são decodificados pelos decodificadores nativos `h264` e
`hevc`, e — pelo mecanismo de §6.1 — esses nomes **também resolvem do lado do
encoder**, para `libx264` e `libx265`. AV1 é decodificado pelo **`libdav1d`**,
que é decodificador e só; [SONDADO hoje] `Codec("libdav1d", "w")` levanta
`UnknownCodecError`. Fim.

O corolário que economiza uma tarde: **isto não tem nada a ver com hardware.**
`libsvtav1` — encoder AV1 *de CPU*, presente nesta build do PyAV — falha
exatamente igual. **AV1 é inviável dentro do ManimCE nesta build, ponto.**
Não adianta procurar outro encoder AV1: [SONDADO] `libaom-av1` e `librav1e` nem
existem aqui.

Quem detecta é `manimx.gpu.validate_encoder()`, que **não** se contenta em
codificar um frame: ele reabre o arquivo e tenta o `add_stream_from_template`,
justamente para pegar esta classe de falha **antes** de a cena inteira ser
renderizada. É a segunda metade da função, e é o motivo de ela existir.

O caminho que funciona é reencodar a entrega com o `/usr/bin/ffmpeg`, que tem
`av1_nvenc`, `libsvtav1`, `librav1e` e `libaom-av1` — verificado nesta máquina
em sessão anterior:

```bash
bin/mx render cena.py Cena -q h --codec nvenc-quality        # master em H.264
ffmpeg -i cena.mp4 -c:v av1_nvenc -preset p7 -rc vbr -cq 30 -b:v 0 cena_av1.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of csv=p=0 cena_av1.mp4
# av1
```

---

## 13. O teto de sessões NVENC — 8 nesta placa, medido

Este é o modo de falha que mais assusta porque a mensagem não diz nada:

```
ExternalError: [Errno 542398533] Generic error in an external library:
  'avcodec_open2("h264_nvenc", {'an': '1', 'preset': 'p4', 'tune': 'hq', ...})'
```

Isso é **sessão de encode indisponível**, não opção inválida. A GPU tem um
número fixo de sessões NVENC simultâneas, e quando elas acabam o
`avcodec_open2` falha.

[MEDIDO] Medição direta (abrir encoders 1080p60 até estourar, contando as
sessões já em uso por outros processos via
`nvidia-smi --query-gpu=encoder.stats.sessionCount`):

| sessões de terceiros | sessões que consegui abrir | total |
|---:|---:|---:|
| 1 | 7 | **8** |
| 8 | 0 (falhou na primeira) | **8** |
| 5 | 7 | ≥ 8 (a leitura do `sessionCount` atrasa) |

**Teto desta placa e deste driver: 8 sessões simultâneas de `h264_nvenc`.**
Não é por processo — é por **GPU**, somando todo mundo na máquina (inclusive
o gravador de tela, a videochamada e o outro agente que está renderizando).

A conta que você precisa fazer antes de paralelizar:

```
sessões = processos_renderizando × max_inflight_encoders
```

Com o `manim.cfg` deste projeto (`max_inflight_encoders = 4`), **dois**
processos já pedem 8 e o terceiro morre.

### 13.1 O default do `batch_render.py` senta exatamente no teto

[FONTE-LIDA `tools/batch_render.py:140-142`]

```python
p.add_argument("--encoders", type=int, default=2)
p.add_argument("-j", "--jobs", type=int, default=max(1, min(4, cpus // 4)))
```

Nesta máquina (32 threads) o default de `-j` é `min(4, 8)` = **4**. Vezes
`--encoders 2` = **8 sessões na mosca**, sem folga nenhuma para o navegador com
vídeo, uma chamada, ou outro agente.

E o guarda-corpo não pega esse caso: [FONTE-LIDA `:182`] o aviso só dispara em
`args.jobs > 4`. **A configuração padrão fica exatamente no limite e nunca
avisa.**

Recomendação prática: **deixe 2 sessões de folga — mire em 6.** Por exemplo
`-j 3 --encoders 2`, ou `-j 6 --codec x264` (CPU sobra, são processos
independentes, e 6 workers de x264 num i9 de 32 threads é confortável).

Isto encerra uma divergência antiga que ainda está no disco: o docstring de
`tools/batch_render.py:20-24` diz "passar de ~3 encoders NVENC ao mesmo tempo
costuma falhar", e `manim-batch-pipeline:92-94` diz "4 workers verificados".
**Os dois números são o mesmo mal-entendido.** O limite não se conta em
workers — conta-se em **sessões**; o teto medido aqui é **8 por GPU** (driver
580.159.03); e o que consome sessão é `workers × max_inflight_encoders` somado
a tudo mais que estiver usando NVENC na máquina. O "3" é o teto histórico das
GeForce de consumidor; **não conferi em que versão de driver ele subiu** — só
que hoje, nesta máquina, são 8.

### 13.2 `validate_encoder()` não protege contra isso

[MEDIDO nesta sessão] Um `mx bench` rodando em paralelo com outros renders
morreu exatamente assim, na cena `opengl + NVENC`, com `validate_encoder()`
tendo passado no começo. E é isso que precisa ficar claro:

> **`validate_encoder()` abre uma sessão, testa e fecha.** Se entre o teste e o
> render as sessões acabarem, o `avcodec_open2` do partial movie falha. É uma
> corrida, não um bug — e ela é inevitável num recurso global da máquina.

Diagnóstico em 3 s:

```bash
nvidia-smi --query-gpu=encoder.stats.sessionCount,encoder.stats.averageFps --format=csv
# name, driver_version, sessionCount, averageFps  →  0, 0  quando a GPU está livre
```

[SONDADO hoje, máquina em repouso] `sessionCount = 0`, `averageFps = 0`,
`memory.used = 129 MiB` de 8188.

Se der 8, o problema não é o seu código. Se der 0 **durante** um render que
você acha que está em NVENC, o render está em CPU (§17).

### 13.3 Sessões, decodificação e o que NÃO conta

O teto é de sessões de **encode**. Decodificar não consome sessão de NVENC
(usa o NVDEC, que é outro bloco). Isso importa numa situação específica: um
pipeline que renderiza em NVENC e reencoda com `ffmpeg -c:v h264_nvenc`
consome **duas** sessões ao mesmo tempo se os dois rodarem em paralelo — e é
fácil não perceber, porque um deles é "só um ffmpegzinho".

---

## 14. Encoding paralelo dentro de um processo (`max_inflight_encoders`)

ManimCE ≥ 0.20 codifica vários *partial movies* enquanto a cena continua
sendo rasterizada. **Não depende de GPU** — vale para libx264 também.

```bash
bin/mx render cena.py Cena -j 4
bin/manim -qh --max-inflight-encoders 4 --encoder-queue-size 8 cena.py Cena
```

Fatos conferidos no fonte e no `--help`:

- **default do ManimCE é 1** (serial), [FONTE-LIDA `_config/default.cfg:137`].
  Quem põe 4 é o `manim.cfg` **deste projeto**;
- `--encoder-queue-size` default 8 (`default.cfg:141`), e é **ignorado quando
  inflight = 1** — nesse caso `frame_queue_size = 0`, que no `Queue` do Python
  quer dizer **ilimitada** [FONTE-LIDA `scene_file_writer.py:683-685`];
- são **threads no mesmo processo** (`_PartialMovieEncodeJob`), não processos;
- o Manim segura a cena quando a fila enche [FONTE-LIDA `:799-800`]:
  `while len(self._inflight_encode_jobs) >= config.max_inflight_encoders:
  self._join_job_and_drain_on_failure(...)`;
- **`mx render -j N` mexe só em `max_inflight_encoders`** [FONTE-LIDA
  `manimx/cli.py:233-234`]. O `mx` **não expõe** `encoder_queue_size`: para
  mudá-lo use `bin/manim --encoder-queue-size` ou
  `render_scene(..., encoder_queue_size=N)`.

**A conta de memória**, do comentário do próprio Manim [FONTE-LIDA `:110-111`],
conferida: oito frames RGBA de 1080p ≈ **66 MB por job** (1920×1080×4 =
8,29 MB × 8). Com `-j 4` são ~265 MB só de filas; em 4K, 4× isso (~1,06 GB).
A tabela por qualidade está em §3.

Quando ajuda e quando não:

| Cena | `-j 4` ajuda? |
|---|---|
| muitas animações **curtas** (uma cena de aula típica, 10–30 `play`) | sim |
| poucas animações **longas** (2 `play` de 10 s) | quase nada — só há 2 jobs para paralelizar |
| gargalo em LaTeX/Pango | nada |
| gargalo em geometria (`always_redraw`, `NumberPlane` fino) | nada — ver `manim-performance-cache` |
| cena com **1 só** `play` | nada, por definição |

**E a interação que morde:** com NVENC ligado, **cada job em voo é uma sessão
NVENC**. `-j 4` = 4 sessões deste processo. Some com os outros processos (§13).

Duas sutilezas que só aparecem lendo o writer:

- **paralelismo e cache conversam.** `is_already_cached()` espera o job em voo
  do mesmo caminho antes de responder [FONTE-LIDA `:802-824`]; sem isso um
  cache-hit poderia ler um arquivo ainda sendo escrito;
- **falha de job apaga o arquivo.** [FONTE-LIDA `:176-186`] o `join()` faz
  `Path(self.path).unlink(missing_ok=True)` quando o worker capturou uma
  exceção, "so a later run cannot cache-hit it". Um partial movie que
  desaparece depois de um erro está sendo protegido, não perdido.

---

## 15. Renderer: `cairo` × `opengl`

```bash
bin/manim -qh --renderer=opengl --write_to_movie cena.py Cena
bin/mx render cena.py Cena --renderer opengl --codec nvenc      # o mx injeta a flag
```

`--write_to_movie` é obrigatório no renderer opengl — sem ele o Manim só abre
janela e não grava nada. O `manimx` injeta sozinho [FONTE-LIDA
`manimx/render.py:231-232`], exceto quando o formato é `png` ou quando
`save_last_frame` está ligado.

**Não presuma que `opengl` é mais rápido.** A afirmação "o renderer opengl
economiza ~19% em cena pesada de geometria" circulava aqui e **não reproduz**.
O próprio `mx bench` imprime a conclusão do dia, e ela muda:

| medição | geometry cairo+NVENC | geometry opengl+NVENC | veredito impresso pelo bench |
|---|---:|---:|---|
| versão antiga desta skill | 6,34 s | 5,11 s | "economiza 19%" |
| auditoria de 2026-08-19 (2 runs) | 6,12 / 6,48 s | 7,14 / 6,55 s | "**custa** 17%" / "custa 1%" |
| esta sessão, `load` 16–24 | 7,47 s | **falhou** (sessões NVENC, §13) | — |
| esta sessão, `load` 27–46 | 16,55 s | **falhou** (sessões NVENC, §13) | — |

A regra que sobra: **meça, não escolha por fé.** O `opengl` vale a pena quando
a cena tem muitos vértices *e* poucos frames; o `cairo` ganha quando a cena é
longa. `manim-3d-camera:177` ainda carrega os "~19%" — o número está morto, e
esta skill é a dona declarada do assunto.

Três armadilhas conhecidas do caminho opengl:

- **`--format png` com `--renderer opengl` é ~100× mais lento que com cairo**
  ([MEDIDO 2026-08-19] 44 s contra 0,42 s em 4K; 16,5 s contra 0,07 s em
  1080p). O cairo pula as animações e desenha só o último frame; o opengl
  renderiza a cena inteira. **Para pôster e frame de conferência, sempre
  cairo.** Ver `manim-verificacao-visual` para o ciclo de conferência e
  `manim-render-api` para onde o arquivo cai (`image_file`, não
  `output_file`);
- o processo pode terminar com `X Error of failed request: BadMatch` no
  *teardown* do contexto GL. Observado na auditoria; o arquivo já está gravado
  quando isso acontece;
- **VRAM**: [SONDADO hoje] esta placa tem 8188 MiB, e o próprio `detect_gpu()`
  emite uma nota quando `vram_mib < 12000` dizendo que 4K com muitos mobjects
  no renderer opengl pode estourar. Em 4K o MAXRSS medido foi 4,3–4,5 GB de
  **RAM** mesmo em cena trivial — o teto que você encosta primeiro costuma ser
  o da RAM, não o da VRAM.

### 15.1 PRIME offload — obrigatório neste notebook

O OpenGL padrão de um shell limpo desta máquina é **Intel Mesa**, não NVIDIA:

```console
$ glxinfo -B | grep "OpenGL renderer"
OpenGL renderer string: Mesa Intel(R) Graphics (RPL-S)

$ __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo -B | grep "OpenGL renderer"
OpenGL renderer string: NVIDIA GeForce RTX 4070 Laptop GPU/PCIe/SSE2
```

As variáveis são exatamente estas [FONTE-LIDA `manimx.gpu.prime_env()`]:

```python
{"__NV_PRIME_RENDER_OFFLOAD": "1",
 "__GLX_VENDOR_LIBRARY_NAME": "nvidia",
 "__VK_LAYER_NV_optimus": "NVIDIA_only"}
```

`bin/manim-env.sh:manimx_enable_gpu` exporta as três **mais**
`WGPUPY_WGPU_ADAPTER_NAME=NVIDIA`, e é sourceado por `bin/mx`, `bin/manim` e
`bin/manimgl`. **Chamar `.venv/bin/manim` direto renderiza OpenGL na Intel, em
silêncio.**

Além disso, `manimx/render.py:390-395` faz `os.environ.setdefault` das mesmas
variáveis quando `renderer == "opengl"`, **antes** de criar o contexto GL — é
`setdefault`, então um valor que você já exportou vence.

Leia com cuidado a linha `OpenGL (padrão)` do `bin/mx gpu`: ela diz NVIDIA
porque o `mx` já roda **dentro** do ambiente offloadado. [SONDADO hoje] o
`mx gpu --json` desta máquina imprime `gl_renderer_default` e
`gl_renderer_offload` **iguais**, ambos NVIDIA — o que confirma exatamente esse
viés de medição. O padrão real de um shell limpo é Intel.

### 15.2 Duas lições de shell que estão no wrapper e valem em qualquer script

[FONTE-LIDA `bin/manim-env.sh`]

1. **`WGPUPY_WGPU_ADAPTER_NAME` é um filtro DURO do wgpu-py**
   (`raise ValueError(f"Adapter with name '{...}' not found.")`), então
   exportá-la cegamente quebraria o `manimgl` em qualquer máquina sem NVIDIA.
   Por isso `manimx_enable_gpu` só a exporta depois de confirmar a placa — e
   com `${WGPUPY_WGPU_ADAPTER_NAME:-NVIDIA}`, respeitando quem já escolheu;
2. **materialize a saída antes de filtrar.** O comentário do arquivo é
   explícito: nada de `produtor | grep -q`. Os wrappers rodam com
   `set -o pipefail`, e `nvidia-smi -L | grep -q` faz o `nvidia-smi` morrer de
   SIGPIPE quando o `grep` sai cedo — o que sob `pipefail` vira "falso" **mesmo
   com a GPU presente**. As duas funções capturam primeiro (`listing="$(...)"`)
   e testam depois. É a mesma classe de erro que transforma
   `comando | grep x || echo ok` em "ok" quando o comando falhou.

---

## 16. ManimGL: wgpu/Vulkan, e o codec pelo binário do ffmpeg

O ManimGL 1.7.2 (master) migrou de ModernGL/OpenGL para **wgpu**, que no Linux
fala **Vulkan**. Ele pede `power_preference="high-performance"` e cai na dGPU
sozinho — **não precisa de PRIME**. Para forçar:

```bash
WGPUPY_WGPU_ADAPTER_NAME=NVIDIA bin/manimgl -w cena.py Cena
```

Encoding no GL é trivial, porque o ManimGL chama o **binário** do `ffmpeg`:

```bash
bin/manimgl -w --vcodec h264_nvenc cena.py Cena
```

**O `custom_config.yml` deste repositório NÃO está em NVENC.** Ele fixa
`video_codec: "libx264"` **de propósito** — o arquivo é versionado e, numa
máquina sem NVIDIA, o ffmpeg abortaria com `Unknown encoder 'h264_nvenc'`. Quem
liga o NVENC é o wrapper `bin/manimgl`, que detecta a placa e injeta
`--vcodec h264_nvenc` **só se você não tiver passado `--vcodec`**
[FONTE-LIDA `bin/manimgl:20-31`]. Em máquina com NVIDIA você ganha NVENC sem
editar nada; em máquina sem, funciona igual. (`manimgl-3b1b:89-96` ainda diz
que o YAML já vem em NVENC — está errado; o arquivo desmente.)

### 16.1 A armadilha do `crf` no lado GL

[FONTE-LIDA `custom_config.yml:60-63`], e é um comentário que vale para
qualquer pipeline de ffmpeg:

> **O ffmpeg IGNORA `crf` silenciosamente quando o codec é NVENC.** Definir
> `crf` junto com `h264_nvenc` não dá erro nem aviso — só entrega o controle de
> taxa padrão do NVENC. Para qualidade em NVENC use `cq`.

É a mesma assimetria que o `_StreamRewriteProxy` trata no lado CE
(`merged.pop("crf", None)`, §4.3): lá o `crf` é removido explicitamente para
não virar lixo silencioso.

### 16.2 Sem perdas no lado GL

O `custom_config.yml` sugere `libx264rgb` com `pixel_format: rgb24` e `crf 0`.
[SONDADO hoje] `libx264rgb` aceita exatamente `['bgr0', 'bgr24', 'rgb24']` —
o `rgb24` do comentário é obrigatório, e um `yuv420p` ali daria erro. A
vantagem sobre `libx264` normal é que **não há subamostragem de croma** (§7.1),
o que para material de linha fina colorida é a diferença entre nítido e
franjado.

### 16.3 Listar os adapters — e a pegadinha do relatório

```bash
.venv-gl/bin/python -c "
import wgpu
for a in wgpu.gpu.enumerate_adapters_sync():
    print(a.summary)"
# Intel(R) Graphics (RPL-S) (IntegratedGPU) via Vulkan
# NVIDIA GeForce RTX 4070 Laptop GPU (DiscreteGPU) via Vulkan
# llvmpipe (LLVM 20.1.2, 256 bits) (CPU) via Vulkan
# Mesa Intel(R) Graphics (RPL-S) (IntegratedGPU) via OpenGL
```

**`bin/mx gpu` imprime `Adapters wgpu : -` SEMPRE, e isso é falso-negativo.**
[FONTE-LIDA `manimx/gpu.py:wgpu_adapters`] a função faz `import wgpu` dentro do
venv da **CE**, que não tem o pacote (`ModuleNotFoundError` capturado), e
devolve lista vazia. [SONDADO hoje] o JSON confirma: `"wgpu_adapters": []`. Não
conclua que o Vulkan está quebrado — rode o snippet acima no `.venv-gl`.

E **não** cite `vulkaninfo` como diagnóstico: ele não existe nesta máquina.
(`manimgl-3b1b:212` ainda o recomenda; use o snippet.)

Detalhes do ManimGL em si (flags, teclas da janela, `custom_config.yml`
inteiro, tradução GL↔CE) são da skill **`manimgl-3b1b`**. Aqui fica só o
encoding.

---

## 17. Provar que saiu mesmo em NVENC

**`ffprobe` não distingue.** Os dois gravam H.264 e ele mostra `h264` nos dois
casos — [MEDIDO] nos arquivos desta sessão:

```console
$ ffprobe -v error -select_streams v:0 \
    -show_entries stream=codec_name,width,height,pix_fmt,r_frame_rate,nb_frames \
    -of csv=p=0 Vitrine.mp4
h264,1920,1080,yuv420p,60/1,450        # x264 E nvenc dão exatamente isto
```

O discriminador confiável é a **assinatura SEI** que o x264 escreve no
bitstream e o NVENC não escreve:

```bash
grep -aqo "x264 - core" saida.mp4 && echo "libx264 (CPU)" || echo "NVENC (GPU)"
```

Bônus: essa string traz a configuração inteira do x264, e vale ler campo a
campo — é a única janela para dentro do encoder que o Manim não te dá:

```
x264 - core 165 ... threads=17 lookahead_threads=16 sliced_threads=1 slices=17
                    ... rc=crf mbtree=1 crf=23.0 qcomp=0.60 ... bframes=3
```

| Campo | O que você aprende |
|---|---|
| `crf=23.0` | confirma que o `av_options` do writer chegou intacto |
| `sliced_threads=1` `slices=17` | o x264 está em *slice threading* — §18, e é uma perna amarrada |
| `threads=17` | quantos núcleos o PyAV deu ao encoder |
| `bframes` `ref` `me` | o preset efetivo (o PyAV usa o `medium` do x264, não `slow`) |

Como a junção é stream copy, a SEI de **cada** partial movie sobrevive no
arquivo final — você vê uma cópia por `self.play`. Isso também é um contador
grátis de quantas animações a cena tem:

```bash
grep -aoc "x264 - core" saida.mp4      # ≈ número de self.play não cacheados
```

Ao vivo, durante o render:

```bash
nvidia-smi dmon -s u                                        # a coluna `enc` sobe
nvidia-smi --query-gpu=encoder.stats.sessionCount --format=csv,noheader
```

E pelo lado do `manimx`:

```python
from manimx.gpu import active_encoder
active_encoder()   # {} se o patch não está aplicado
# {'codec': 'h264_nvenc', 'profile': 'quality', 'options': {...}} quando ativo
```

Uma quarta via, que é a única que funciona **sem** olhar o arquivo nem a placa:
o JSON do `mx render` traz `"codec"`, e ele é calculado por
`_effective_codec()` [FONTE-LIDA `manimx/render.py:239-262`] a partir do que
realmente foi aplicado — se o `enable_nvenc` caiu para CPU, o JSON diz
`libx264`, não `h264_nvenc`.

---

## 18. A perna esquecida: o libx264 do PyAV roda em *slice threading*

Descoberto lendo a SEI de um arquivo x264 do próprio Manim:

```
threads=17 lookahead_threads=16 sliced_threads=1 slices=17
```

`sliced_threads=1` significa que o x264 está paralelizando **por fatia dentro
do frame**, não por frame. Isso não é escolha do Manim — é o default do PyAV:

```console
$ .venv/bin/python -c "
import av, io
c = av.open(io.BytesIO(), mode='w', format='mp4')
s = c.add_stream('libx264', rate=60, options={'crf':'23'})
print(s.codec_context.thread_count, s.codec_context.thread_type)"
0 ThreadType.SLICE
```

O `thread_count = 0` (automático) engana: o tipo é `SLICE`, e slice threading
escala mal *e* comprime pior, porque cada fatia reinicia o contexto de
entropia. [MEDIDO] — 240 frames de 1080p60 com detalhe real, `crf 23`, três
rodadas intercaladas:

| `thread_type` | tempo (mediana de 3) | tamanho |
|---|---:|---:|
| `SLICE` (default do PyAV) | 6,70 s | 1,00 MiB |
| `AUTO` (frame + slice) | **4,87 s** (−27%) | **0,77 MiB** (−23%) |

**Mais rápido e menor ao mesmo tempo.** Ou seja: parte da vantagem que o NVENC
parece ter sobre o x264 dentro do Manim é, na verdade, o x264 rodando amarrado.

Isso **não** está ligado hoje — nem no Manim, nem no `manimx`. O patch está
esboçado em §20. Marque como **experimental**: foi medido no encoder isolado,
**não** foi medido de ponta a ponta dentro de um render do Manim.

Regra de bolso enquanto isso: quando você quiser **arquivo pequeno**, o
caminho testado não é afinar o x264 do PyAV — é renderizar em NVENC e
reencodar com o `/usr/bin/ffmpeg`, que não tem essa amarra (§8).

---

## 19. Diagnóstico de lentidão — a ordem que funciona

```bash
bin/mx gpu       # a placa aparece? PRIME OK? quais encoders o PyAV abre?
bin/mx doctor    # o ambiente está inteiro?
bin/mx bench     # onde ESTÁ o gargalo nesta máquina, hoje
```

### 19.1 `mx gpu --json` — o relatório em forma de dado

Para um agente, o formato útil é o JSON. Os campos são os de
`manimx.gpu.GPUReport`. [SONDADO hoje], literal:

```json
{
  "nvidia_gpu": "NVIDIA GeForce RTX 4070 Laptop GPU",
  "nvidia_driver": "580.159.03",
  "cuda_version": "13.0",
  "vram_mib": 8188,
  "gl_renderer_default": "NVIDIA GeForce RTX 4070 Laptop GPU/PCIe/SSE2",
  "gl_renderer_offload": "NVIDIA GeForce RTX 4070 Laptop GPU/PCIe/SSE2",
  "prime_offload_works": true,
  "pyav_encoders": {"h264_nvenc": true, "hevc_nvenc": true, "av1_nvenc": true,
                    "libx264": true, "libx265": true, "libvpx-vp9": true,
                    "qtrle": true, "prores_ks": true, "png": true, "gif": true},
  "wgpu_adapters": [],
  "notes": ["VRAM de 8188 MiB: renderizar 4K com muitos mobjects pode estourar
             memória no renderer opengl. Prefira -qh e faça o upscale depois,
             ou renderize 4K no cairo."]
}
```

Quatro leituras que exigem cuidado, todas verificadas:

- **`gl_renderer_default` mente por construção.** Os dois campos vieram
  idênticos hoje porque o `mx` já roda **dentro** do ambiente offloadado
  (§15.1). Num shell limpo o `default` é Intel;
- **`wgpu_adapters` é sempre `[]`** — falso-negativo (§16.3);
- **`pyav_encoders["av1_nvenc"] = true` não quer dizer que AV1 funcione** — o
  probe só abre o encoder; quem quebra é a junção (§12);
- **`pyav_encoders` são 10 nomes curados, não o inventário.** `libsvtav1`,
  `libx264rgb`, `ffv1`, `ffvhuff`, `magicyuv`, `h264_qsv` e **mais ~105**
  existem e não aparecem aqui — são **115** encoders de vídeo na build (§6).
  Uma versão anterior desta linha dizia "e mais 20".

Numa máquina **sem** NVIDIA nada disso é fatal: `enable_nvenc()` devolve
`False`, loga um `WARNING` e o render continua em `libx264` (§4.4).

### 19.2 `mx bench`

`bin/mx bench` roda a matriz de 5 cenários e imprime a leitura em português.
Ele aceita `-q`, `--repeats` e `--media-dir`; o default é `-q h --repeats 1`,
`media_dir="media/_bench"`, e **todo render do bench é `--no-cache`**
[FONTE-LIDA `manimx/bench.py:85-88`] — o número não vem contaminado por cache.
O resultado reportado é a **mediana** das repetições.

Os 5 cenários [FONTE-LIDA `bench.py:123-134`]:

| # | rótulo | cena | renderer | codec |
|---|---|---|---|---|
| 1 | encode-bound cairo + x264 | `BenchEncode` | cairo | x264 |
| 2 | encode-bound cairo + NVENC | `BenchEncode` | cairo | nvenc |
| 3 | geometry cairo + x264 | `BenchGeometry` | cairo | x264 |
| 4 | geometry cairo + NVENC | `BenchGeometry` | cairo | nvenc |
| 5 | geometry opengl + NVENC | `BenchGeometry` | opengl | nvenc |

As duas cenas de teste estão em `manimx/bench.py` como strings:
`ENCODE_ONLY_SCENE` — um quadrado atravessando a tela em 8 s, poucos mobjects e
muitos frames; `GEOMETRY_HEAVY_SCENE` — `NumberPlane` de passo 0,25,
**700** `Dot` e **11** `FunctionGraph` (`range(1, 12)`).

Duas limitações do bench que você precisa saber antes de citá-lo:

- **não existe "encode-bound opengl"** na matriz. O bench nunca isola o
  renderer numa cena limitada por encoding, então a linha "opengl custa/economiza
  X%" fala **só** da cena pesada de geometria;
- se as suas cenas não se parecem com nenhuma das duas, o bench te diz menos do
  que você acha — nesse caso meça a sua cena real com `--no-cache` e dois
  codecs, alternando.

**Rode com a máquina em repouso.** [MEDIDO] Prova de que isso não é
preciosismo — o mesmo `bin/mx bench -q h --repeats 3`, na mesma máquina, no
mesmo dia, com três cargas diferentes (mediana; runs entre parênteses):

| cenário | `load` ~2 (auditoria, 2 runs) | `load` 16–24 | `load` 27–46 |
|---|---:|---:|---:|
| encode-bound cairo + x264 | 5,60 / 5,41 s | 6,84 s (7,06 · 5,31 · 6,84) | 6,78 s (11,29 · 5,96 · 6,78) |
| encode-bound cairo + NVENC | **2,92 / 2,92 s** | **4,53 s** (5,30 · 4,53 · 3,77) | 7,84 s (7,84 · 7,07 · 7,99) |
| geometry cairo + x264 | 6,05 / 6,34 s | 8,93 s | 24,35 s |
| geometry cairo + NVENC | 6,12 / 6,48 s | 7,47 s | 16,55 s |
| geometry opengl + NVENC | 7,14 / 6,55 s | **falhou** (§13) | **falhou** (§13) |

O que a tabela ensina, em três linhas:

- **com a máquina livre, o NVENC corta ~46%** do tempo na cena limitada por
  encoding (5,5 → 2,9 s); com carga média, corta 34%; com a máquina saturada,
  fica **mais lento** que o x264. O ganho do NVENC é **liberar CPU** — se não
  há CPU livre para colher, não há ganho;
- três repetições do *mesmo* cenário variando 2× (11,29 contra 5,96 s) é o
  aviso na cara de que aquele número não vale nada;
- as duas execuções desta sessão morreram no **último** cenário, sempre pelo
  mesmo motivo: outros processos da máquina tinham tomado as 8 sessões de
  NVENC (§13). Falha de bench não é necessariamente bug do bench.

### 19.3 As quatro caixas

Depois do bench, o gargalo cai numa destas quatro:

| O bench diz | Gargalo | O que fazer |
|---|---|---|
| NVENC economiza muito | **encoding** | `--codec nvenc` + `-j` dentro do orçamento de sessões (§13) |
| NVENC não muda nada, cairo e opengl parecidos | **rasterização** | baixe `-q`, simplifique a cena — a fundo em `manim-performance-cache` |
| tudo lento, inclusive `-q l` | **texto / LaTeX** | reaproveite mobjects de texto, mantenha o cache ligado; ver `manim-text-latex` |
| primeira execução lenta, as seguintes rápidas | **cache frio** | normal; não é gargalo. Ver `manim-performance-cache` |

Referência de custo de rasterização, só para calibrar expectativa [MEDIDO
2026-08-19, `-q h`, cairo + NVENC]: `Cascata` 3,44 s · `OlaManim` 3,65 s ·
`Pitagoras` 2,69 s · **`TangenteViva` 38,22 s**. A última é `ValueTracker` +
`always_redraw`: **~11× as outras no mesmo preset**. Redraw por frame não
escala, e nenhum flag de GPU conserta isso — o porquê e o conserto são de
`manim-performance-cache` e `manim-updaters-valuetracker`.

---

## 20. Estender: escrever o seu próprio patch de encoder

Se você precisa de algo que os perfis não alcançam — outro pix_fmt (§7), QSV
(§6.2), `thread_type=AUTO` no x264 (§18) — o gancho é sempre o mesmo, e vale a
pena entendê-lo antes de copiar.

**O ponto de interceptação** [FONTE-LIDA `manimx/gpu.py:enable_nvenc`]: em vez
de reescrever `SceneFileWriter.open_partial_movie_stream`, o `manimx` embrulha
o método e troca `av.open` **só durante a chamada dele**, devolvendo um proxy
cujo `add_stream` reescreve o que interessa. Isso sobrevive a mudanças internas
do Manim, e é o motivo de o patch não ter quebrado entre versões.

**O que o proxy atual alcança e o que não alcança:**

| Você quer mudar | Alcançável pelo proxy? | Por quê |
|---|---|---|
| codec | **sim** | é o 1º argumento de `add_stream` |
| opções libav (`cq`, `preset`, `bf`…) | **sim** | é o kwarg `options=` |
| `pix_fmt` | **não** | o Manim escreve `stream.pix_fmt = ...` **depois** que `add_stream` retornou |
| `thread_type` / `thread_count` | **não** | é atributo de `stream.codec_context`, escrito pelo próprio libav no `add_stream` |
| resolução, fps | não faz sentido aqui | vêm de `config` (§3) |

Para alcançar os dois de baixo o proxy precisa mexer no stream **depois** de
criá-lo — e aí você briga com a linha do Manim que sobrescreve `pix_fmt` logo
em seguida. As duas saídas honestas são: (a) embrulhar
`open_partial_movie_stream` inteiro e corrigir o stream **no retorno**, lendo
`self._current_encode_job.stream`; ou (b) aceitar que esse eixo não é
configurável e resolver no reencode.

Esqueleto de (a), **[NÃO VERIFICADO] — não executei**:

```python
import functools
from manim.scene.scene_file_writer import SceneFileWriter

_orig = SceneFileWriter.open_partial_movie_stream

@functools.wraps(_orig)
def patched(self, file_path=None):
    _orig(self, file_path)
    job = self._current_encode_job          # atributo privado: pode sumir
    job.stream.codec_context.thread_type = "AUTO"   # §18
    # job.stream.pix_fmt = "yuv444p"                # §7 — confira o encoder antes

SceneFileWriter.open_partial_movie_stream = patched
```

Três avisos, todos aprendidos com o patch que existe:

1. **`_current_encode_job` é privado.** O patch oficial evita atributo privado
   justamente por isso; se você usar, teste em cada atualização do Manim;
2. **monkeypatch é global e persistente.** Guarde o original e reverta num
   `finally`, como `disable_nvenc()` faz. `manimx.render` já faz isso por você
   no caminho do `mx render`;
3. **valide antes de renderizar.** `validate_encoder(codec, options)` custa um
   frame 256×144 e pega EINVAL de opção **e** falha de remux (§12). Rodar a
   cena inteira para descobrir que `profile=high` não existe em HEVC é o
   desperdício que essa função foi escrita para evitar.

---

## 21. Armadilhas verificadas

| Sintoma | Causa real | Conserto |
|---|---|---|
| `avcodec_open2("h264_nvenc", …)` → `Generic error in an external library` | **sessões NVENC esgotadas** (teto 8 por GPU, §13) | `nvidia-smi --query-gpu=encoder.stats.sessionCount`; reduza `processos × max_inflight_encoders` para ≤ 6 |
| Rodou `batch_render.py` no default e estourou | `-j 4 × --encoders 2 = 8` = exatamente o teto, e o aviso só dispara em `-j > 4` (§13.1) | `-j 3 --encoders 2`, ou `-j 6 --codec x264` |
| `--codec av1` sai `OK` mas o arquivo é H.264 | AV1 não sobrevive à junção (`libdav1d`, §12) | reencode com `/usr/bin/ffmpeg -c:v av1_nvenc` |
| `UnknownCodecError: libdav1d` num script seu | você tentou AV1 no caminho do Manim | idem — e não adianta trocar para `libsvtav1` |
| O mp4 ficou 5× maior depois que "liguei a GPU" | é o esperado: NVENC troca bits por velocidade (§8) | `nvenc-fast` para iterar, `x264` ou reencode para entregar |
| O repositório engordou 6× depois de um "upgrade de qualidade" | trocaram `x264` por `nvenc-quality` sem olhar o peso (§9) | política de git: mp4 fora, png dentro (§9.1) |
| `profile=high` estoura no meio da renderização | `profile=high` **só existe em H.264**; em HEVC é `main`, em AV1 a opção não existe. E o PyAV só abre o encoder **no primeiro frame** | use `nvenc_options(profile, codec)`, que já ajusta; `validate_encoder()` pega antes (§5.2) |
| `tune=lossless` recusado em AV1 | `av1_nvenc` não tem esse tune | `CODEC_PROFILE_FALLBACK` cai para `quality` e avisa no log |
| Pedi `--codec nvenc -t` e saiu `qtrle` | **H.264/HEVC não têm canal alfa** — é de propósito | correto; §10 |
| Pedi `--codec nvenc --format webm` e saiu VP9 | **NVENC não faz VP9** | correto |
| O `.mov` com alfa tem 100 MiB para 7,5 s | `qtrle` é RLE sem perdas em RGBA (§10) | se o destino é web, `-t --format webm`; se é NLE, reencode em `prores_ks`/`ffv1` |
| Liguei `format="webm"` e `transparent=True` num script e saiu `.mov` | a ordem importa: quem for aplicado por último ganha (§10.2) | ligue `transparent` primeiro, `format` depois |
| O GIF saiu com faixas mesmo em cena limpa | três perdas empilhadas: intermediário `crf 23`, quantização, e `pix_fmt=rgb8` (§11) | gere mp4 e converta fora do Manim |
| Texto vermelho fino ficou com franja | `yuv420p`: a croma tem 1/4 dos pixels (§7.1) | renderize em `-q h`, engrosse o traço, ou dessature |
| Gradiente grande com banding, mesmo em `nvenc-quality` | 8 bits é o teto do pix_fmt do Manim (§7.2) | `spatial-aq`/`temporal-aq` (já ligados em `balanced`/`quality`); ou textura no próprio gradiente |
| `-q l -r 3840x2160` saiu a 15 fps | `-r` sobrescreve resolução, **não** o fps (§3.2) | passe `--fps 60` junto |
| `ffprobe` diz `h264` e eu não sei quem gerou | `ffprobe` não distingue | `grep -aqo "x264 - core"` (§17) |
| `bin/mx gpu` mostra `Adapters wgpu : -` | falso-negativo: `wgpu` não existe no venv da CE | rode o snippet no `.venv-gl` (§16.3) |
| `bin/mx gpu` mostra `OpenGL (padrão)` = NVIDIA e ainda assim renderiza na Intel | o `mx` mede de dentro do ambiente offloadado (§15.1) | use os wrappers `bin/*`, nunca `.venv/bin/manim` direto |
| `--format png` demorando ~100× | `--format png` + `--renderer opengl` | use `cairo` para frame único |
| render 4K estourando memória | MAXRSS medido 4,3–4,5 GB **de RAM** mesmo em cena trivial; some ~265 MB por job de fila em 4K (§3, §14) | renderize 4K no cairo, `-j` menor, ou `-q h` + upscale |
| `X Error of failed request: BadMatch` ao fim de um render opengl | teardown do contexto GL | o arquivo já está gravado; ignore ou use cairo |
| Ligou NVENC num script e o próximo render também saiu NVENC | `enable_nvenc` é um monkeypatch **global e persistente** | sempre `disable_nvenc()` no `finally` (o `manimx.render` já faz) |
| CI "acelerou" mas continua em CPU | `enable_nvenc` cai para CPU só avisando | `enable_nvenc(..., strict=True)` |
| `from manimx.gpu import *` e `NameError: active_encoder` | `active_encoder` e `validate_encoder` não estão no `__all__` (§4.2) | importe por nome |
| Um partial movie sumiu depois de um erro | é de propósito: o `join()` apaga o arquivo truncado para não virar cache-hit (§14) | corrija a causa do erro; o arquivo se refaz |
| `crf` no ManimGL com NVENC não mudou nada | o ffmpeg **ignora `crf` em NVENC, sem avisar** (§16.1) | use `cq` |

---

## 22. Fronteiras — o que NÃO é desta skill

| Assunto | Skill dona |
|---|---|
| caminho exato da saída, `--format png`/`image_file`, `-n a,b`, `render_file`/`render_scene` | `manim-render-api` |
| rodar **várias cenas** em processos paralelos, corrida de LaTeX entre workers, CI em lote | `manim-batch-pipeline` |
| o cache de partial movies, `--no-cache`/`--flush_cache`, `max_files_cached`, e o **custo de rasterizar** (`always_redraw`, `VGroup` gigante, número de curvas) | `manim-performance-cache` |
| **olhar** o frame e decidir se está certo — o ciclo renderizar rápido → ver o PNG → corrigir | `manim-verificacao-visual` |
| `next_section`, `--save_sections`, o mapa das classes de `Scene` | `manim-cenas-secoes` |
| áudio, `add_sound`, legenda `.srt` | `manim-som-legendas` |
| transparência como decisão **visual**, temas, `apply_theme`, cor de fundo, a catraca de `background_opacity` | `manim-color-theming` |
| erro que não é de codec/GPU (LaTeX, mobject invisível, cena vazia) | `manim-troubleshooting` |
| custo do texto e do LaTeX, `t2c`, `TexTemplate` | `manim-text-latex` |
| API do ManimGL, flags do `manimgl`, teclas da janela, `custom_config.yml` inteiro | `manimgl-3b1b` |
| custo de rasterização de cena 3D, `Surface`, câmera 3D | `manim-3d-camera` |
| vídeo cortado em partes para slide, e a medição da emenda | `manim-presentation-parts` |
| descobrir assinatura de classe/função do Manim | `manim-api-discovery` |

**Buracos declarados** (nenhuma skill cobre, não invente): as 48 classes
`OpenGL*` de `mobject/opengl`; `Shader`, `ShaderWrapper`, `Mesh`, `Object3D`,
`Window`, `FullScreenQuad` — a API interna do renderer opengl. Aqui só se
decide **se** usar o renderer opengl, nunca como programá-lo.

Onde os números desta skill divergirem dos de outra, **vale o daqui** — mas
só porque estão datados e vêm com o comando ao lado. Se o comando não
reproduzir na sua máquina, o certo é remedir e atualizar a tabela, não abrir
uma terceira contagem.

**As três divergências que esta seção listava como abertas estão FECHADAS** — as
irmãs foram corrigidas e hoje concordam. Mantido aqui só o registro, porque o
número velho ainda circula em cenas antigas:

| Assunto | Estado | Onde a irmã concorda hoje |
|---|---|---|
| `opengl` × `cairo` "economiza ~19%" | **derrubado**, não reproduz (§15) | `manim-3d-camera` §... "a afirmação circulava NESTA skill e foi derrubada" |
| teto NVENC | **8 sessões por GPU**, `workers × encoders` (§13) | `manim-batch-pipeline` faz a conta `-j 4 × --encoders 2 = 8`. O `~3` de `tools/batch_render.py:20` é o docstring da ferramenta, conservador — não uma skill |
| `-r` × `-q` | `-r` troca só a resolução; o fps continua do `-q` (§3.2) | `manim-render-api` §4.3, com o mesmo título |

Se você reabrir uma delas medindo outra coisa, **remedir e atualizar as duas
skills** é o certo — não abrir uma terceira contagem.

---

## 23. Checklist antes de dizer "está acelerado"

```bash
# 1. a placa está visível e o PRIME funciona?
bin/mx gpu | grep -E "NVIDIA GPU|PRIME|Encoders"

# 2. quantas sessões NVENC estão livres agora?
nvidia-smi --query-gpu=encoder.stats.sessionCount --format=csv,noheader   # <= 6 é seguro

# 3. onde está o gargalo NESTA máquina, com ela em repouso?
uptime                        # load average baixo ANTES de medir
bin/mx bench -q h --repeats 3

# 4. o arquivo saiu no codec que você acha que saiu?
grep -aqo "x264 - core" saida.mp4 && echo "CPU" || echo "GPU"

# 5. resolução e fps são os que você pediu — em TODOS os arquivos?
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,pix_fmt -of csv=p=0 saida.mp4

# 6. quanto ele pesa, e isso cabe onde ele vai morar?
ffprobe -v error -show_entries format=duration,size,bit_rate -of default=nw=1 saida.mp4
```

Os itens 5 e 6 são os que mais se esquece.

O **5** pega o defeito mais silencioso deste fluxo: você iterou em `-q m` com
`nvenc-fast`, o preview **sobrescreveu o arquivo final** e ninguém percebeu até
o projetor. [DECK] o teste de uma linha, num diretório inteiro, é esperar
**uma linha só**:

```bash
for f in videos/*.mp4; do
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate \
    -of csv=p=0 "$f"; done | sort | uniq -c        # esperado: UMA linha
```

O **6** é o que separa "ficou rápido" de "ficou caro". "Ficou rápido" e "ficou
bom" são fáceis de ver; **"ficou 6,7× mais pesado" só aparece quando o
repositório já engordou** — e aí o histórico do git não desengorda.
