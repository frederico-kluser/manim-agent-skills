---
name: manim-render-api
description: >-
  Renderizar cenas do Manim de forma controlada e programática — pela CLI
  `mx render`, pela API Python `manimx.render_file`, ou pelo `manim` cru.
  Use sempre que precisar gerar o arquivo de vídeo/imagem, escolher
  qualidade/resolução/FPS/formato, saber o CAMINHO EXATO da saída,
  renderizar só um trecho de animações, renderizar várias cenas, controlar
  cache, ou capturar sucesso/erro de forma estruturada. Cobre também
  transparência, GIF, PNG do último frame e seções.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
---

# Renderização — controle total da saída

## Sempre pegue o caminho da saída do resultado, nunca por dedução

O caminho depende de `media_dir`, nome do módulo, qualidade e
`output_file`. Deduzir dá errado. A camada `manimx` devolve o caminho real.

### Pela CLI (recomendado para agentes)

```bash
bin/mx render scenes/demo.py Demo -q h --codec nvenc --json
```

```json
[{"scene_name": "Demo", "success": true,
  "output_file": "/abs/path/to/repo/media/videos/demo/1080p60/Demo.mp4",
  "elapsed_s": 2.41, "codec": "h264_nvenc", "resolution": [1920, 1080],
  "frame_rate": 60.0, "num_animations": 3, "error": null}]
```

Exit code: `0` se todas as cenas passaram, `1` se alguma falhou.

### Pela API Python

```python
from manimx import render_file

r = render_file("scenes/demo.py", "Demo", quality="h", codec="nvenc")
if r:                       # RenderResult é falsy quando falha
    print(r.output_file)    # pathlib.Path absoluto
else:
    print(r.error, r.traceback_text)
```

## Flags que importam

```bash
bin/mx render ARQ.py [CENA...] \
  -q h                    # l|m|h|p|k  ou 1080p/4k/draft/hd…
  -r 2560x1440            # resolução explícita (ignora -q)
  --fps 30
  --codec nvenc           # ver `bin/mx presets`
  --renderer opengl       # rasterização na GPU
  --theme whiteboard      # ver skill manim-color-theming
  --format gif            # mp4|gif|webm|mov|png
  -t                      # transparente (.mov + qtrle)
  -o nome_saida
  --media-dir media
  --no-cache              # ignora partial movies em cache
  -j 4                    # encoders paralelos (ManimCE >= 0.20)
  --all                   # todas as cenas do arquivo
  --json
```

Descubra tudo o que existe:

```bash
bin/mx presets      # qualidade, codecs, perfis NVENC, temas
bin/mx scenes scenes/demo.py     # quais cenas o arquivo tem
```

## Ciclo de iteração eficiente

Nesta ordem, do mais rápido ao mais caro:

```bash
# 1. só o último frame, como PNG — valida layout em ~1s
bin/mx render scenes/demo.py Demo -q l --format png

# 2. rascunho 480p15
bin/mx render scenes/demo.py Demo -q l --codec nvenc-fast

# 3. revisão 720p30
bin/mx render scenes/demo.py Demo -q m --codec nvenc

# 4. entrega 1080p60
bin/mx render scenes/demo.py Demo -q h --codec nvenc-quality -j 4
```

Renderizar só um trecho (o `mx` não expõe; use o `manim` cru):

```bash
bin/manim -ql -n 4,7 scenes/demo.py Demo   # animações 4 a 7
bin/manim -ql -s scenes/demo.py Demo       # só o último frame
```

## Formatos

| Objetivo | Comando |
|---|---|
| MP4 padrão | `--codec nvenc` |
| MP4 entrega | `--codec nvenc-quality` |
| Transparente para NLE | `-t` (vira `.mov` + qtrle RGBA) |
| Web leve | `--codec webm` |
| GIF para README | `--format gif -q m` |
| PNG do último frame | `--format png` |
| Sequência de PNGs | `bin/manim -qh --save_pngs ...` |

**NVENC não faz canal alfa nem VP9.** Pedir `-t --codec nvenc` faz a camada
ignorar o NVENC de propósito e usar `qtrle`, que é o certo. Isso é avisado
no log, não é falha.

## Escrevendo uma cena para ser renderizada por agente

```python
from manim import *

class Demo(Scene):
    """Uma linha de docstring aparece em `mx scenes`."""

    def construct(self):
        # tudo acontece aqui; nada é desenhado até um self.play/self.add
        eq = MathTex(r"\int_0^1 x^2\,dx = \frac{1}{3}")
        self.play(Write(eq))
        self.wait(0.5)
```

Regras:

- Uma classe = um vídeo. Nomes de classe viram nomes de arquivo.
- `self.wait()` no fim evita corte seco no último frame.
- Não chame `config.*` dentro de `construct` — use `tempconfig` ou os
  parâmetros de `render_file`.

## Cache — quando desligar

O Manim reaproveita *partial movies* pelo hash da animação. O hash **não
enxerga estado externo**. Desligue o cache quando a cena:

- lê CSV/JSON/API,
- usa `random` sem seed fixa,
- depende de data/hora ou de arquivo em disco.

```bash
bin/mx render ... --no-cache
bin/manim --flush_cache ...     # apaga o cache existente
```

## Renderizar várias cenas

```bash
bin/mx render scenes/aula.py --all -q h --codec nvenc --json
bin/mx render scenes/aula.py Intro Meio Fim -q h
```

Em Python:

```python
from manimx.render import render_many

results = render_many([
    {"file_path": "scenes/a.py", "scene_names": "A", "quality": "h"},
    {"file_path": "scenes/b.py", "all_scenes": True, "quality": "m"},
])
```

`render_many` é **sequencial de propósito**: o `config` do Manim é global,
então duas cenas no mesmo processo corrompem o estado uma da outra. Para
paralelismo real, ver a skill `manim-batch-pipeline`.

## Seções (capítulos)

```python
class Aula(Scene):
    def construct(self):
        self.next_section("Introdução")
        ...
        self.next_section("Demonstração", skip_animations=False)
        ...
```

```bash
bin/manim -qh --save_sections scenes/aula.py Aula
```

## Controle fino via `tempconfig`

Quando precisar de uma chave que a `mx` não expõe:

```python
from manim import tempconfig
from manimx.render import render_scene
from scenes.demo import Demo

r = render_scene(
    Demo,
    quality="h",
    config_overrides={"frame_width": 16, "save_last_frame": True},
)
```

Veja todas as chaves com `.venv/bin/manim cfg show`.

## Armadilhas

- **`--renderer=opengl` não escreve arquivo sozinho.** Precisa de
  `--write_to_movie`. A camada `manimx` já injeta isso.
- **Renderizar duas cenas em paralelo no mesmo processo Python corrompe o
  `config` global.** Use processos separados.
- **`-q k` (4K) com muitos mobjects estoura os 8 GiB de VRAM** no renderer
  opengl desta máquina. Renderize 4K no `cairo`, ou entregue 1080p.
- **O nome do diretório de saída inclui a qualidade** (`1080p60`), então
  trocar `-q` muda o caminho. Mais um motivo para ler `output_file`.
