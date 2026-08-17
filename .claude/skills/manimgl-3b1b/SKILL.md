---
name: manimgl-3b1b
description: >-
  ManimGL, a versão original do 3Blue1Brown (`manimlib`, CLI `manimgl`) —
  quando usar em vez do ManimCE, a janela interativa com manipulação 3D e
  o REPL embutido, a configuração em custom_config.yml, NVENC via
  --vcodec, e a tradução de código entre ManimGL e ManimCE. Use ao lidar
  com código do 3b1b, ao ver `from manimlib import *`, `ShowCreation`,
  `TexMobject`, dicts `CONFIG` ou `self.embed()`, ao portar um script de
  uma edição para a outra, ou quando o usuário pedir o fluxo interativo do
  Grant Sanderson.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
---

# ManimGL (3b1b)

## Primeiro: identifique QUAL ManimGL

Existem dois programas diferentes com o mesmo nome e **a mesma string de
versão**:

| Origem | Backend | Versão que reporta |
|---|---|---|
| `pip install manimgl` (wheel de dez/2024) | OpenGL / ModernGL | `1.7.2` |
| `git clone` do master | **WebGPU (wgpu → Vulkan)** | `1.7.2` |

Nenhuma release nova foi marcada em ~20 meses, e o master ainda se
autodeclara `1.7.2`. **A versão não distingue os dois.** Qualquer
afirmação genérica sobre "o backend do ManimGL" está errada metade do
tempo.

Neste projeto está instalado o **master (wgpu/Vulkan)**. Confirme:

```bash
bin/mx doctor | grep manimgl        # -> "1.7.2 wgpu/Vulkan"
```

O README do master **ainda lista "OpenGL" como requisito de sistema**,
embora o `requirements.txt` já tenha migrado para wgpu. Não confie nele.

## Quando usar ManimGL em vez do ManimCE

Use ManimGL quando:

- o usuário trouxe código do 3b1b (`from manimlib import *`) e quer rodar
  como está;
- precisa da **janela interativa** para girar/arrastar a cena em 3D;
- quer o REPL embutido (`self.embed()`) para experimentar ao vivo.

Fique no ManimCE (o padrão) para o resto: documentação melhor, API estável,
plugins, e a camada `manimx` deste projeto.

## Uso

```bash
bin/manimgl scenes/demo.py Demo              # janela interativa
bin/manimgl -w scenes/demo.py Demo           # escreve arquivo (headless)
bin/manimgl -w --hd scenes/demo.py Demo      # 1080p
bin/manimgl -w --uhd --vcodec hevc_nvenc scenes/demo.py Demo
bin/manimgl -so scenes/demo.py Demo          # último frame + abre
bin/manimgl -w -n 3,7 scenes/demo.py Demo    # só as animações 3..7
bin/manimgl -e 42 scenes/demo.py Demo        # breakpoint IPython na linha 42
```

Flags de qualidade: `-l` 480p · `-m` 720p · `--hd` 1080p · `--uhd` 4K.
Note que são **diferentes** do ManimCE (`-ql/-qm/-qh/-qk`).

Verificado nesta máquina: `-w` renderiza **headless**, sem abrir janela.

### Teclas na janela interativa

`d` pan 3D · `f` pan · `r` reset · `s` select · `u` unselect · `g` grab ·
`h`/`v`/`z` grab por eixo · `t` resize · `c` color · `i` info ·
`Cmd/Ctrl+q` sair.

## NVENC — trivial aqui

O ManimGL chama o **binário do ffmpeg**, então trocar o encoder é um flag:

```bash
bin/manimgl -w --vcodec h264_nvenc scenes/demo.py Demo
```

Ou permanente em `custom_config.yml` (já configurado neste projeto):

```yaml
file_writer:
  ffmpeg_bin: "ffmpeg"
  video_codec: "h264_nvenc"
  pixel_format: "yuv420p"
```

**Armadilha real:** o ffmpeg **ignora silenciosamente `-crf` com
`h264_nvenc`**. Se você definir `crf` junto com `video_codec: h264_nvenc`,
o arquivo sai com o controle de taxa padrão do NVENC, não com a qualidade
que você pediu — e nenhum aviso aparece. Para qualidade em NVENC use `cq`
via NVENC, não `crf`.

Isso contrasta com o ManimCE, onde o codec está fixo no código (PyAV) e
precisa da camada `manimx` — ver skill `manim-gpu-encoding`.

## Configuração

`custom_config.yml` no diretório de execução, ou `--config_file caminho.yml`.
Referência completa dos defaults:

```bash
bat .venv-gl/lib/python3.12/site-packages/manimlib/default_config.yml
```

Seções: `directories` `window` `camera` `file_writer` `scene` `vmobject`
`mobject` `tex` `text` `embed` `resolution_options` `sizes`
`key_bindings` `colors`.

Diferenças que pegam:

- **O fundo padrão do master é `#333333`**, não preto. Se você quer o preto
  clássico, escreva explicitamente (já está no `custom_config.yml` daqui).
- **As cores são redefiníveis no YAML** (seção `colors`) — recurso que o
  ManimCE não tem.
- **A fonte padrão de `Text` é `Consolas`.**
- `camera.bundle_draws` / `draw_together` são otimizações do renderer wgpu;
  desligue só para depurar artefato de renderização.

## Traduzindo GL ↔ CE

Mapa completo gerado por reflexão dos dois pacotes instalados:

```bash
bat api/ce-vs-gl.md
bin/mx api-diff          # regenera
```

Números medidos: **337 classes na CE, 270 no GL, 153 com nome em comum — e
as 153 têm assinatura diferente.** Portar não é trocar o import.

| ManimGL | ManimCE |
|---|---|
| `from manimlib import *` | `from manim import *` |
| `ShowCreation` | `Create` |
| `TexMobject` | `MathTex` |
| `TextMobject` / `TexText` | `Tex` |
| `GraphScene` | `Axes` dentro de uma `Scene` |
| `get_graph(f)` | `ax.plot(f)` |
| `CONFIG = {...}` | argumentos de `__init__` |
| `self.play(m.shift, UP)` | `self.play(m.animate.shift(UP))` |
| `self.embed()` | *(sem equivalente)* |
| `-l / -m / --hd / --uhd` | `-ql / -qm / -qh / -qk` |
| `--vcodec X` | *(use `mx render --codec`)* |

Verifique se um símbolo existe em cada edição:

```bash
bin/mx find ShowCreation --package manimgl
bin/mx find ShowCreation --package manim-ce      # não encontra
```

## Fluxo interativo do 3b1b

```python
from manimlib import *

class Demo(Scene):
    def construct(self):
        c = Circle()
        self.play(ShowCreation(c))
        self.embed()          # abre IPython aqui, com a cena viva
```

No shell que abre, `self.play(...)` renderiza na janela na hora.

`bin/manimgl -e 42 arquivo.py Cena` insere o breakpoint sem editar o
arquivo.

### Sobre o bug do IPython/SQLite

Guias antigos (e a própria FAQ do ManimCE, que segue desatualizada)
mandam fazer `pip install IPython==8.0.1` para contornar
`sqlite3.ProgrammingError: SQLite objects created in a thread can only be
used in that same thread`.

**Não faça isso preventivamente.** IPython 8.0.1 é de fevereiro de 2022 e
regride muita coisa. Só considere o downgrade se você reproduzir o erro,
e prefira isolar num venv separado.

## Dois motores, dois venvs

Nunca instale os dois no mesmo ambiente: eles brigam por
`moderngl-window`, `pyglet` e afins. Neste projeto:

- `.venv` → ManimCE 0.21.0
- `.venv-gl` → ManimGL master (wgpu)

Os wrappers `bin/manim` e `bin/manimgl` já apontam para o venv certo.

## Armadilhas

- **`from manimlib import *` num script rodado pelo `bin/manim`** dá
  `ModuleNotFoundError`. Cada wrapper vê só o seu venv.
- **A camada `manimx` é do ManimCE.** `mx render` não renderiza cena do
  ManimGL; use `bin/manimgl -w`.
- **A saída do ManimGL vai para `media-gl/`** (definido no
  `custom_config.yml`), não para `media/`.
- **O ManimGL não tem `--json`.** Para capturar o caminho, leia a linha
  `File ready at` do stdout, ou defina `--file_name`.
- **wgpu precisa de driver Vulkan funcional.** Se `manimgl` falhar ao criar
  o adapter, cheque `vulkaninfo` e o pacote do driver NVIDIA.
