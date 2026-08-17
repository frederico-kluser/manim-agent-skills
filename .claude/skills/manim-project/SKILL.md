---
name: manim-project
description: >-
  Ponto de entrada deste projeto Manim. Use SEMPRE que a tarefa envolver
  gerar, renderizar, animar ou editar vídeo/animação matemática, cena,
  Mobject, Scene, Tex/MathTex, gráfico animado, ou os comandos `mx`,
  `manim`, `manimgl` neste repositório — mesmo que o usuário não diga
  "Manim". Explica o layout do projeto, os dois motores instalados
  (ManimCE 0.21 e ManimGL 1.7.2), como achar QUALQUER classe/método da
  API, e roteia para a skill específica. Leia esta antes das outras.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Projeto Manim — mapa e roteamento

Este repositório é um ambiente Manim pronto para uso, com uma camada de API
(`manimx`) desenhada para agentes. **Nada aqui precisa de instalação
adicional.**

## Regra número um

Use os wrappers em `bin/`, nunca o `manim` do sistema. Eles resolvem três
coisas que quebram silenciosamente:

| Wrapper | O que resolve |
|---|---|
| `bin/mx` | CLI da camada de API. LaTeX + GPU + venv no ambiente. Saída `--json`. |
| `bin/manim` | ManimCE cru, com TinyTeX no PATH e PRIME offload ligado. |
| `bin/manimgl` | ManimGL (3b1b), com GPU. |

Sem eles: `MathTex` falha (TinyTeX fora do PATH) e o renderer `opengl` cai
no iGPU Intel em vez da RTX 4070.

## Confira o ambiente antes de qualquer coisa

```bash
bin/mx doctor          # exit 0 = tudo pronto
bin/mx doctor --json   # para parsear
```

Se o `doctor` reclamar que falta venv (clone novo), rode o bootstrap:

```bash
bin/setup              # ManimCE + manimx
bin/setup --all        # + ManimGL + pacotes LaTeX
```

## Layout

```
bin/setup                 bootstrap a partir de um clone limpo
bin/                      wrappers: mx, manim, manimgl, manim-env.sh
manim.cfg                 config do ManimCE (projeto)
custom_config.yml         config do ManimGL
manimx/                   a camada de API (Python)
tools/batch_render.py     lote multi-processo
tools/check_publishable.sh  guarda de publicação
scenes/                   exemplos + suas cenas .py
media/  media-gl/         saída (gitignored)
api/                      índice COMPLETO da API — ver manim-api-discovery
.venv/                    ManimCE 0.21.0
.venv-gl/                 ManimGL 1.7.2 (master, wgpu/Vulkan)
```

## Os dois motores

| | ManimCE | ManimGL (3b1b) |
|---|---|---|
| import | `from manim import *` | `from manimlib import *` |
| CLI | `bin/manim` | `bin/manimgl` |
| versão aqui | 0.21.0 | 1.7.2 (git master) |
| rasterização | Cairo (CPU) ou ModernGL (`--renderer=opengl`) | **wgpu → Vulkan** |
| encoding | PyAV embutido, codec fixo no código | binário `ffmpeg`, `--vcodec` livre |
| fundo padrão | `#000000` | `#333333` |

**Eles não são compatíveis no nível de código-fonte.** Das 153 classes com
nome em comum, **todas as 153 têm assinatura diferente**. Ver
`api/ce-vs-gl.md` (gerado por reflexão, não escrito à mão).

**Padrão: use ManimCE.** Vá para ManimGL só se o usuário pedir o fluxo do
3b1b explicitamente, ou precisar da janela interativa com manipulação 3D.

## Caminho mais curto para um vídeo

```bash
cat > scenes/demo.py <<'PY'
from manim import *

class Demo(Scene):
    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=72)
        self.play(Write(eq))
        self.wait()
PY

bin/mx render scenes/demo.py Demo -q h --codec nvenc --json
```

A saída JSON traz `output_file` com o caminho absoluto real — não adivinhe
o caminho, leia dele.

## Roteamento — carregue a skill certa

| A tarefa é… | Skill |
|---|---|
| renderizar, controlar saída, batch, integrar por código | `manim-render-api` |
| achar uma classe/método/constante que você não lembra | `manim-api-discovery` |
| GPU, NVENC, performance, "está lento" | `manim-gpu-encoding` |
| formas, posicionamento, agrupamento, transformações | `manim-mobjects` |
| animar, timing, `rate_func`, composição | `manim-animations` |
| cor, fundo, tema, transparência, alfa | `manim-color-theming` |
| texto, LaTeX, colorir parte de uma fórmula | `manim-text-latex` |
| eixos, gráficos de função, dados | `manim-graphs-plots` |
| 3D, câmera, movimento de câmera | `manim-3d-camera` |
| valores dinâmicos, updaters, contadores | `manim-updaters-valuetracker` |
| erro, travamento, saída errada | `manim-troubleshooting` |
| código do 3b1b, `manimlib`, portar GL↔CE | `manimgl-3b1b` |
| muitos vídeos, paralelismo, CI | `manim-batch-pipeline` |

## O que NÃO fazer

- Não rode `pip install manim` — já está instalado nos venvs.
- Não use `python cena.py` direto; use `bin/mx` ou `bin/manim`.
- Não escreva hex de 3 dígitos (`#F00`). O parser de cor do Manim exige 6.
- Não misture `from manim import *` com `from manimlib import *`.
- Não invente nome de método. Confira com `bin/mx show <Classe>`.
