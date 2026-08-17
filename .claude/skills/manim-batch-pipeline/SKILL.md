---
name: manim-batch-pipeline
description: >-
  Renderizar muitos vídeos do Manim de uma vez — paralelismo multi-processo,
  descoberta automática de cenas, saída em JSON, e integração em pipeline
  ou CI. Use ao gerar uma série de vídeos, processar um diretório de
  cenas, criar vídeos a partir de dados, automatizar entrega, ou quando
  precisar de throughput em vez de latência de uma cena só. Documenta a
  corrida de LaTeX entre workers paralelos e o limite de sessões NVENC —
  os dois modos de falha reais deste cenário.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Lote e pipeline

## A regra estrutural

**Nunca renderize duas cenas em paralelo dentro do mesmo processo Python.**
O `config` do Manim é um singleton global mutável — resolução, `media_dir`,
codec e diretórios são estado compartilhado. Threads corrompem tudo.

Paralelismo real = **processos separados**. É o que `tools/batch_render.py`
faz.

## Uso

```bash
source bin/manim-env.sh; manimx_use_ce; manimx_enable_gpu

.venv/bin/python tools/batch_render.py scenes/exemplos.py -q h --codec nvenc -j 4
.venv/bin/python tools/batch_render.py scenes/ -q m --codec x264 -j 8
.venv/bin/python tools/batch_render.py 'scenes/*.py' --scenes Intro Fim
.venv/bin/python tools/batch_render.py scenes/ --dry-run
.venv/bin/python tools/batch_render.py scenes/ --json > resultado.json
```

Flags: `-q` qualidade · `--codec` · `--renderer` · `--media-dir` ·
`--no-cache` · `--encoders N` (encoders paralelos **dentro** de cada worker)
· `-j N` (workers) · `--json` · `--dry-run` · `--shared-tex`.

Exit code `0` só se todas as cenas passaram.

## Os dois modos de falha reais

### 1. Corrida de LaTeX entre workers

Reproduzido neste projeto: com `-j 2`, dois workers compilando `MathTex`
no mesmo `media/Tex` colidem na limpeza dos arquivos auxiliares:

```
FileNotFoundError: media/Tex/cd13fedd3f96aaa7.aux
```

Serial dava 6/6; paralelo dava 5/6, de forma não determinística.

`tools/batch_render.py` **já corrige** isolando `tex_dir` e `text_dir` por
worker. O índice do worker é estável entre execuções, então o cache de
LaTeX continua sendo reaproveitado.

**Onde colocar esses diretórios importa.** Eles ficam em
`media/_workers/wN/Tex`, e **não** dentro de `media/Tex`. Motivo, verificado
no código do Manim (`manim/utils/tex_file_writing.py`):

```python
for f in tex_dir.iterdir():
    if f.suffix not in file_suffix_whitelist:
        f.unlink()            # <- sem checar se é diretório
```

Um subdiretório dentro de `media/Tex` faz `f.unlink()` levantar
`IsADirectoryError` — e aí **toda** renderização de LaTeX posterior quebra,
inclusive fora do lote. Sintoma típico: o lote roda, e depois
`bin/mx doctor` começa a acusar falha em MathTex.

Se você escrever seu próprio orquestrador, replique assim:

```python
render_file(..., config_overrides={
    "tex_dir":  f"media/_workers/w{slot}/Tex",     # FORA de media/Tex
    "text_dir": f"media/_workers/w{slot}/texts",
})
```

`--shared-tex` volta ao diretório único — use só com `-j 1`.

### 2. Limite de sessões NVENC

GPUs de consumidor limitam encoders simultâneos. **4 workers NVENC foram
verificados funcionando** nesta RTX 4070; acima disso pode falhar na
inicialização do encoder. Se acontecer, use `--codec x264`.

## Quanto paralelismo usar

O padrão é `min(4, cpus // 4)`. Cada worker do Manim já usa vários núcleos
(Cairo + encoder), então subir demais causa disputa em vez de ganho.

Medido nesta máquina (32 threads, RTX 4070, 6 cenas, 1080p60, sem cache):

| Configuração | Tempo total |
|---|---|
| `-j 4 --codec nvenc` | 57,9 s |
| `-j 4 --codec x264` | 59,2 s |

Praticamente empatados — porque **este lote é limitado por geometria**, não
por encoding: duas cenas (`always_redraw` pesado e 3D) consomem 46 s e 52 s
sozinhas, e as outras quatro terminam em ~6 s.

A lição: em lote, o gargalo costuma ser a **cena mais lenta**, não o codec.
Otimize a cena antes de mexer no encoder. Use `bin/mx bench` para descobrir
onde está o custo.

## Saída JSON para pipeline

```bash
.venv/bin/python tools/batch_render.py scenes/ -q h --json > out.json
```

```json
{
  "total": 6, "ok": 6, "failed": 0, "elapsed_s": 57.9, "jobs": 4,
  "results": [
    {"scene_name": "OlaManim", "success": true,
     "output_file": "/.../media/videos/exemplos/1080p60/OlaManim.mp4",
     "file": "/.../scenes/exemplos.py", "wall_s": 7.2,
     "codec": "h264_nvenc", "resolution": [1920,1080], "error": null}
  ]
}
```

```bash
jq -r '.results[] | select(.success) | .output_file' out.json
jq -r '.results[] | select(.success | not) | "\(.scene_name): \(.error)"' out.json
```

## Gerar cenas a partir de dados

O padrão para "um vídeo por linha do CSV": gere os arquivos `.py` e depois
renderize em lote.

```python
from pathlib import Path
import csv

TEMPLATE = '''from manim import *

class {cls}(Scene):
    def construct(self):
        titulo = Text({titulo!r}, font_size=44).to_edge(UP)
        valor  = MathTex(r"{formula}", font_size=72)
        self.play(Write(titulo))
        self.play(Write(valor))
        self.wait()
'''

out = Path("scenes/gerado"); out.mkdir(parents=True, exist_ok=True)
with open("dados.csv") as fh:
    for i, row in enumerate(csv.DictReader(fh)):
        cls = f"Item{i:03d}"
        (out / f"{cls.lower()}.py").write_text(
            TEMPLATE.format(cls=cls, titulo=row["titulo"], formula=row["formula"]),
            encoding="utf-8",
        )
```

```bash
.venv/bin/python tools/batch_render.py scenes/gerado -q h --codec nvenc -j 4 --json
```

Alternativa sem gerar arquivos — parametrize a cena por atributo de classe:

```python
from manim import *
from manimx.render import render_scene

class Card(Scene):
    titulo = "padrão"
    def construct(self):
        self.play(Write(Text(self.titulo, font_size=48)))
        self.wait()

for i, t in enumerate(["Alfa", "Beta", "Gama"]):
    Sub = type(f"Card{i}", (Card,), {"titulo": t})
    r = render_scene(Sub, quality="h", codec="nvenc",
                     input_file=__file__, output_file=f"card_{i}")
    print(r.output_file)
```

Rode isso **sequencialmente** num processo, ou distribua em processos.

## Cache em lote

O cache de *partial movies* é por hash da animação e é compartilhado. Ele
ajuda muito em re-execuções.

Desligue (`--no-cache`) quando as cenas leem estado externo — CSV, API,
data/hora — porque o hash não enxerga isso e você recebe vídeo velho sem
aviso.

```bash
bin/manim --flush_cache -ql scenes/exemplos.py OlaManim   # limpa
```

## Em CI

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source bin/manim-env.sh; manimx_use_ce; manimx_enable_gpu

bin/mx doctor                       # falha cedo se o ambiente estiver ruim

.venv/bin/python tools/batch_render.py scenes/ \
    -q h --codec nvenc -j 4 --json > build/render.json

jq -e '.failed == 0' build/render.json > /dev/null
jq -r '.results[].output_file' build/render.json
```

Num runner **sem GPU**, troque para `--codec x264`: o `manimx` já cai em
libx264 sozinho e apenas avisa, mas ser explícito evita ruído no log.
`--renderer opengl` exige GPU/driver e deve ficar de fora de CI headless
comum.

## Arquivo grande demais no fim

Reencode só na entrega, não durante a produção:

```bash
ffmpeg -i entrada.mp4 -c:v hevc_nvenc -preset p7 -rc vbr -cq 24 -b:v 0 saida.mp4
```

## Armadilhas

- **Threads em vez de processos** → `config` global corrompido, resultado
  silenciosamente errado.
- **`media/Tex` compartilhado com `-j > 1`** → `FileNotFoundError` errático.
- **Muitos workers NVENC** → falha de inicialização do encoder.
- **`-j` alto demais** → disputa de CPU; cada worker já é multi-thread.
- **Cache servindo vídeo velho** em pipeline orientado a dados → `--no-cache`.
- **Deduzir o caminho de saída** → leia `output_file` do JSON.
- **Uma cena lenta domina o lote.** Perfile antes de escalar workers.
