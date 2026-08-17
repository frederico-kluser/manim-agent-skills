---
name: manim-gpu-encoding
description: >-
  GPU e performance no Manim — NVENC (h264/hevc/av1 por hardware), renderer
  OpenGL, wgpu/Vulkan do ManimGL, PRIME render offload em notebook híbrido,
  encoding paralelo, e benchmark. Use quando a renderização estiver lenta,
  quando pedirem "usar a GPU"/"acelerar", ao escolher codec, ao investigar
  se a placa está mesmo sendo usada, ou ao configurar qualidade de encoding.
  Contém dados medidos nesta máquina (RTX 4070 Laptop) e desfaz a confusão
  comum entre acelerar a RASTERIZAÇÃO e acelerar o ENCODING.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# GPU e encoding

## O erro conceitual que custa tempo

Uma renderização do Manim tem **duas etapas caras e independentes**:

| Etapa | Quem faz | Como acelerar |
|---|---|---|
| **1. Rasterizar a geometria** em frames | Cairo (CPU) / ModernGL (GPU) / wgpu (GPU) | trocar o *renderer* |
| **2. Codificar os frames** em vídeo | libx264 (CPU) / NVENC (GPU) | trocar o *codec* |

"Usar a GPU" pode significar qualquer uma das duas. Trocar só o codec **não
acelera** uma cena pesada em geometria. Trocar só o renderer **não acelera**
uma cena longa e visualmente simples.

## Dados medidos nesta máquina

RTX 4070 Laptop (8 GiB), driver 580.159.03, 32 threads, ManimCE 0.21.0,
saída 1080p60. Reproduza com `bin/mx bench`.

| Cenário | Tempo | Conclusão |
|---|---|---|
| poucos mobjects, muitos frames — cairo + x264 | 5,68 s | baseline |
| poucos mobjects, muitos frames — cairo + **NVENC** | **2,92 s** | **−49%** |
| geometria pesada — cairo + x264 | 5,69 s | baseline |
| geometria pesada — cairo + **NVENC** | 6,34 s | **+11% (pior)** |
| geometria pesada — **opengl** + NVENC | **5,11 s** | **−19%** |

Leitura: em cena curta e pesada de geometria, o custo de inicializar o
NVENC supera o ganho. O NVENC brilha em cena **longa**.

```bash
bin/mx bench           # roda a matriz nesta máquina
bin/mx bench -q h --repeats 3 --json
```

## Como ligar cada coisa

### NVENC no ManimCE

O ManimCE **não usa o binário do `ffmpeg`** — ele usa **PyAV**, com o codec
fixo no código (`libx264`, `crf=23`, em
`manim/scene/scene_file_writer.py`). Não existe flag de CLI para trocar.
A camada `manimx` corrige isso.

```bash
bin/mx render cena.py Cena --codec nvenc            # equilibrado
bin/mx render cena.py Cena --codec nvenc-quality    # entrega
bin/mx render cena.py Cena --codec nvenc-fast       # preview
bin/mx render cena.py Cena --codec hevc             # ~30% menor
bin/mx render cena.py Cena --codec av1              # RTX 40+
```

```python
from manimx import enable_nvenc, disable_nvenc

enable_nvenc(codec="h264_nvenc", profile="quality")
# ... renderize ...
disable_nvenc()
```

Por que funciona: cada animação vira um *partial movie* codificado
separadamente, e a junção final é **stream copy** (`add_stream_from_template`),
sem recodificar. Trocar o codec dos parciais muda o arquivo final inteiro.

### NVENC no ManimGL — trivial

O ManimGL chama o binário do `ffmpeg`, então é só um flag:

```bash
bin/manimgl -w --vcodec h264_nvenc cena.py Cena
```

Ou permanente em `custom_config.yml` (já configurado neste projeto):

```yaml
file_writer:
  video_codec: "h264_nvenc"
```

### Renderer OpenGL no ManimCE

```bash
bin/manim -qh --renderer=opengl --write_to_movie cena.py Cena
bin/mx render cena.py Cena --renderer opengl --codec nvenc
```

`--write_to_movie` é obrigatório: sem ele o renderer opengl só abre janela.
O `bin/mx` já injeta.

### PRIME offload — obrigatório neste notebook

O OpenGL padrão desta máquina é **Intel Mesa**, não NVIDIA. Sem as
variáveis abaixo, `--renderer=opengl` roda no iGPU:

```bash
export __NV_PRIME_RENDER_OFFLOAD=1
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export __VK_LAYER_NV_optimus=NVIDIA_only
```

Os wrappers `bin/*` já exportam. Confirme:

```bash
bin/mx gpu
glxinfo -B | grep "OpenGL renderer"                       # Intel
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia \
  glxinfo -B | grep "OpenGL renderer"                     # NVIDIA
```

### ManimGL usa Vulkan, não OpenGL

O ManimGL 1.7.2 (master) migrou de ModernGL/OpenGL para **wgpu**, que no
Linux fala **Vulkan**. Ele pede `power_preference="high-performance"` e
seleciona a dGPU sozinho — **não precisa de PRIME**. Para forçar:

```bash
WGPUPY_WGPU_ADAPTER_NAME=NVIDIA bin/manimgl -w cena.py Cena
```

Liste os adapters:

```bash
.venv-gl/bin/python -c "
import wgpu
for a in wgpu.gpu.enumerate_adapters_sync():
    print(a.info)"
```

### Encoding paralelo — ganho gratuito

ManimCE ≥ 0.20 codifica vários parciais enquanto a cena continua
renderizando. **Não depende de GPU.**

```bash
bin/mx render cena.py Cena -j 4
bin/manim -qh --max-inflight-encoders 4 --encoder-queue-size 8 cena.py Cena
```

Já vale 4 no `manim.cfg` deste projeto. Ajuda mais em cenas com **muitas
animações curtas**; em cena com poucas animações longas, não muda nada.

## Escolhendo o codec

| Situação | Codec |
|---|---|
| iteração rápida | `nvenc-fast` |
| padrão | `nvenc` |
| entrega YouTube/cliente | `nvenc-quality` |
| arquivo menor, público controlado | `hevc` |
| máxima compatibilidade (celular velho, editor antigo) | `x264` |
| composição em NLE com alfa | `transparent` (qtrle) |
| web | `webm` |
| masterização sem perdas | `enable_nvenc(profile="lossless")` |

Perfis NVENC (`bin/mx presets`):

| Perfil | preset | cq | Uso |
|---|---|---|---|
| `fast` | p1 | 26 | preview |
| `balanced` | p4 | 20 | padrão |
| `quality` | p7 | 16 | entrega, com AQ espacial+temporal |
| `lossless` | p7 | — | masterização |

O AQ espacial/temporal do perfil `quality` importa: animação tem gradientes
lisos e cor chapada, onde o NVENC no automático produz *banding*.

## Verificar se saiu mesmo em NVENC

`ffprobe` mostra `h264` nos dois casos. O discriminador confiável é a
assinatura SEI que o x264 escreve no bitstream:

```bash
grep -aqo "x264 - core" saida.mp4 && echo "libx264 (CPU)" || echo "NVENC (GPU)"
```

Ou monitore a GPU durante a renderização:

```bash
nvidia-smi dmon -s u        # coluna `enc` sobe = NVENC ativo
```

## Diagnóstico de lentidão

```bash
bin/mx gpu           # a placa está visível? PRIME funciona?
bin/mx bench         # onde está o gargalo nesta máquina?
```

Se o gargalo é **geometria**: reduza `-q`, simplifique a cena, use
`--renderer=opengl`, evite `NumberPlane` de passo muito fino, prefira
`FunctionGraph` com `x_range` de passo maior.

Se o gargalo é **encoding**: `--codec nvenc` + `-j 4`.

Se é **LaTeX**: cada `MathTex` novo compila um documento. Reaproveite
objetos e mantenha o cache do Manim ligado.

## Armadilhas verificadas nesta máquina

- **`profile=high` só existe em H.264.** Em `hevc_nvenc` o nome é `main`;
  em `av1_nvenc` a opção **não existe** e passá-la dá `EINVAL`. Pior: o
  PyAV só abre o encoder no **primeiro frame**, então o erro apareceria no
  meio da renderização. Por isso `manimx.gpu.validate_encoder()` testa o
  encoder antes de começar.
- **`tune=lossless` não existe no `av1_nvenc`.** A camada cai para
  `quality` e avisa.
- **NVENC não codifica canal alfa.** Com `-t`, o `manimx` mantém `qtrle`
  de propósito.
- **NVENC não faz VP9.** `--codec webm` continua em `libvpx-vp9` (CPU).
- **8 GiB de VRAM** limitam 4K no renderer opengl. Renderize 4K no `cairo`.
- **NVENC de consumidor tem limite de sessões simultâneas.** Renderizar
  muitos processos em paralelo com NVENC pode falhar; ver
  `manim-batch-pipeline`.
