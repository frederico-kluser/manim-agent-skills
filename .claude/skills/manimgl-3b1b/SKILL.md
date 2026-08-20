---
name: manimgl-3b1b
description: >-
  ManimGL, o motor original do 3Blue1Brown (pacote `manimlib`, CLI `manimgl`,
  venv `.venv-gl`) — quando ele é a resposta e quando é a resposta errada, o
  fluxo INTERATIVO que só existe aqui (`self.embed()`, `checkpoint_paste()`,
  gravar um bloco em `inserts/`, `reload()`, Shift+D copiando o `reorient(...)`
  da câmera), a janela wgpu/Vulkan com suas teclas, a CLI inteira flag a flag,
  o `custom_config.yml`, e a tradução GL ↔ CE conferida por reflexão dos dois
  pacotes instalados. Use ao ver `from manimlib import *`, `ShowCreation`,
  `TexMobject`, `TexText`, `OldTex`, `CONFIG = {...}`, `self.embed()`,
  `self.frame`, `reorient(`, `GlowDot`, `TransformMatchingStrings`; ao pedir
  "roda esse código do 3b1b", "abre a janela pra eu girar a cena", "quero o
  REPL do Grant", "quero mexer na cena ao vivo", "converte essa cena do 3b1b
  pro nosso Manim", "porta isso pro ManimCE", "por que a cena GL não roda com o
  bin/manim?", "o manimgl abriu uma janela cinza", "o vídeo do manimgl saiu
  sem alfa", "onde foi parar o mp4 do manimgl", "o manimgl ficou esperando eu
  digitar", "qual dos dois Manim eu uso pra isso?". Cobre também o que só o GL
  tem (`time_span`, `--subdivide`, colormaps, `SCENES_IN_ORDER`, widgets
  interativos) e o que ele NÃO tem (34 das 49 `rate_function` da CE, `Table`,
  `ManimColor`, `MovingCameraScene`). NÃO use para: escrever cena ManimCE
  (`manim-mobjects`, `manim-animations`), codec/NVENC/peso do arquivo
  (`manim-gpu-encoding` é dono), achar assinatura da CE (`manim-api-discovery`),
  cena em partes para slide (`manim-presentation-parts`), nem para o wrapper
  `mx` — ele não dirige o ManimGL.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
---

# ManimGL (3b1b) — o outro motor

> **Como esta skill foi conferida.** Tudo abaixo veio de LER o código instalado
> (`.venv-gl/lib/python3.12/site-packages/manimlib/`), o `custom_config.yml`
> deste repositório, os wrappers de `bin/` e os índices estáticos de `api/`
> (`manimgl-index.tsv`, `manimgl-methods.tsv`, `ce-vs-gl.md`). **Nenhum render
> foi executado nesta rodada.** Onde uma afirmação é dedução de leitura e não
> observação, ela está marcada **[não verificado]**. Onde é linha de fonte, o
> arquivo e a linha estão ao lado. Data: 2026-08-19.

---

## 1. Cartão de decisão — 20 segundos

| Você quer | Motor | Por quê |
|---|---|---|
| um mp4 para um slide, um deck, uma aula | **ManimCE** | é o que `mx`, `manimx` e o pipeline de `~/Projects/aulas` falam |
| rodar código do 3b1b como está | **ManimGL** | `ShowCreation`, `TexText`, `self.embed()` não existem na CE |
| girar/arrastar a cena com o mouse enquanto ela existe | **ManimGL** | a janela é do fluxo dele, não um extra |
| descobrir o ângulo de câmera experimentando | **ManimGL** | Shift+D copia o `reorient(...)` pronto para o clipboard (§6.3) |
| iterar num bloco de código com a cena viva | **ManimGL** | `checkpoint_paste()` — não há equivalente na CE (§5.3) |
| gravar só um trecho, sem re-rodar a cena | **ManimGL** | `checkpoint_paste(record=True)` → `inserts/` (§5.4) |
| vídeo vertical 9:16 com o palco acompanhando | **ManimGL** | `-r 1080x1920` REDIMENSIONA o palco no GL (§3.2); na CE não |
| NVENC, AV1, peso do arquivo, SSIM | **ManimCE** | a matriz medida está em `manim-gpu-encoding` |
| tabela, matriz, `Table`, `MathTable` | **ManimCE** | o GL não tem nenhuma delas (§10.3) |
| `ease_out_expo` e as outras 33 curvas | **ManimCE** | o GL tem 15 `rate_function`, a CE tem 49 (§10.5) |
| render em lote, paralelo, CI | **ManimCE** | `tools/batch_render.py`, skill `manim-batch-pipeline` |
| saída em JSON para um script consumir | **ManimCE** | o `manimgl` não tem `--json` (§8.1) |

**Padrão deste repositório: ManimCE.** Vá para o ManimGL por um motivo nomeado.

---

## 2. Primeiro: identifique QUAL ManimGL

Existem dois programas diferentes com o mesmo nome, o mesmo import e **a mesma
string de versão**:

| Origem | Rasterização | Versão que reporta |
|---|---|---|
| `pip install manimgl` (wheel de dez/2024) | OpenGL / ModernGL | `1.7.2` |
| `git clone` do master | **wgpu → Vulkan** (`glfw` + `rendercanvas`) | `1.7.2` |

Nenhuma release nova foi marcada em ~20 meses e o master ainda se autodeclara
`1.7.2`. **A versão não distingue os dois.** Qualquer afirmação genérica sobre
"o backend do ManimGL" está errada metade do tempo — inclusive as da internet.

Aqui está o **master (wgpu/Vulkan)**. Confirme sem render:

```bash
bin/mx doctor | grep manimgl        # -> "1.7.2 wgpu/Vulkan"
```

O que o `doctor` faz é exatamente isto (`manimx/cli.py:150-167`): importa
`manimlib` no `.venv-gl` e olha se `wgpu` ou `moderngl` está instalado. O
README do master **ainda lista "OpenGL" como requisito de sistema** embora o
`requirements.txt` já esteja em wgpu. Não confie nele.

Prova direta, se precisar (`window.py:3-6` importa `glfw`, `wgpu` e
`rendercanvas.glfw`):

```bash
ls .venv-gl/lib/python3.12/site-packages | grep -E '^(wgpu|moderngl|glfw|rendercanvas)$'
```

---

## 3. Arquitetura: por que os dois motores não se misturam

Três decisões de projeto do ManimGL explicam quase todas as armadilhas desta
skill. Vale ler as três antes de qualquer outra seção.

### 3.1 A configuração é um global montado NO IMPORT, a partir de `sys.argv`

A última linha de `manimlib/config.py` é:

```python
# manimlib/config.py:399
manim_config: Dict = initialize_manim_config()
```

e `initialize_manim_config()` (`config.py:23-50`) começa chamando `parse_cli()`,
que é um `argparse.ArgumentParser().parse_args()` sobre o `sys.argv` do processo.
**Importar `manimlib` parseia a linha de comando.** Consequências, todas reais:

1. **Qualquer script com CLI própria que importe `manimlib` morre no import**
   com `argparse: unrecognized arguments`. O antídoto é apagar o `argv` antes:

   ```python
   import sys; sys.argv = [sys.argv[0]]
   import manimlib
   ```

   (É por isso que o dump de API do GL não sai por `bin/mx` — ver
   `manim-project §14`, que traz o script pronto.)

2. **`mx` não dirige o ManimGL, e nunca vai.** `manimx` foi desenhado em cima da
   `ManimConfig` da CE, que é um objeto mutável em runtime; no GL não existe
   objeto equivalente para configurar depois do import. `mx render` de uma cena
   `manimlib` dá `ModuleNotFoundError` — ele roda no venv da CE.

3. **Não existe `tempconfig`.** Mudar configuração no meio de uma cena não é uma
   coisa que se faça no GL; o que existe são os context managers de `Scene`
   (`temp_skip`, `temp_record`, `temp_progress_bar` — §5.4).

### 3.2 As CONSTANTES derivam da configuração — inclusive o tamanho do palco

`manimlib/constants.py` não tem números fixos; ele lê o config já resolvido:

```python
# manimlib/constants.py:13-20
DEFAULT_RESOLUTION: tuple[int, int] = manim_config.camera.resolution
ASPECT_RATIO: float = DEFAULT_PIXEL_WIDTH / DEFAULT_PIXEL_HEIGHT
FRAME_HEIGHT: float = manim_config.sizes.frame_height     # 8.0
FRAME_WIDTH:  float = FRAME_HEIGHT * ASPECT_RATIO
```

E `SMALL_BUFF`, `MED_LARGE_BUFF`, `DEFAULT_STROKE_WIDTH` e **as 50 cores**
(`BLUE_D`, `RED_C`, `GREY_A`…) vêm do YAML do mesmo jeito (`constants.py:27-33`,
`:79+`). Duas consequências que a CE não tem:

- **`-r 1080x1920` muda o palco.** No GL, `update_camera_config` grava a
  resolução do `-r` em `manim_config.camera.resolution` *antes* de
  `constants.py` ser importado, então `FRAME_WIDTH` vira `8.0 × 1080/1920 =
  4.5`: o palco fica 4,5 × 8,0 e `to_edge(RIGHT)` continua acertando a borda.
  Na CE, `-r 1080x1920` mexe só no buffer de pixels e o palco continua 14,22 ×
  8,0 (`manim-project §9.3`). **Para vídeo vertical, o GL exige menos gambiarra.**
  [não verificado — deduzido da ordem de import; nenhum render rodou]
- **Redefinir cor é editar YAML**, não código: a seção `colors:` do
  `default_config.yml` (53 nomes) é a fonte de `BLUE_D` e companhia. A CE não
  tem esse gancho — lá a paleta é código (`manim-color-theming`).

### 3.3 Dois venvs, e eles não se visitam

| venv | pacote | disparado por |
|---|---|---|
| `.venv` | ManimCE 0.21.0 | `bin/manim`, `bin/mx` |
| `.venv-gl` | ManimGL 1.7.2 (git master, wgpu) | `bin/manimgl` |

Nunca instale os dois no mesmo ambiente: eles brigam por `pyglet`,
`moderngl-window` e afins. `from manimlib import *` num arquivo rodado pelo
`bin/manim` dá `ModuleNotFoundError`, e o contrário também.

**Use sempre `bin/manimgl`, nunca `.venv-gl/bin/manimgl` direto.** O wrapper
(`bin/manimgl` + `bin/manim-env.sh`) resolve três coisas, e a primeira é fatal:

1. põe `~/.TinyTeX/bin/x86_64-linux` no PATH — **`dvisvgm` não tem symlink em
   `~/.local/bin`** (`manim-project §3.1`), e o GL chama `dvisvgm` por nome
   (§9.1). Sem o wrapper, a primeira `Tex` da cena estoura com `FileNotFoundError`;
2. exporta `WGPUPY_WGPU_ADAPTER_NAME=NVIDIA` e as variáveis de PRIME;
3. injeta `--vcodec h264_nvenc` quando há NVIDIA e você não pediu codec — e
   **essa injeção tem um efeito colateral que morde calado**, ver §8.3.


### 3.4 Os comandos que você realmente digita

```bash
bin/manimgl scenes/exemplos_gl.py GLOla                 # janela interativa
bin/manimgl -w scenes/exemplos_gl.py GLOla              # grava, headless
bin/manimgl -ws scenes/exemplos_gl.py GLOla             # só o PNG do último frame
bin/manimgl -w --hd scenes/exemplos_gl.py GLOla         # 1080p
bin/manimgl -w --uhd --vcodec hevc_nvenc … GLSuperficie # 4K, HEVC na GPU
bin/manimgl -w -n 3,7 … GLOla                           # só as animações 3..7
bin/manimgl -e 42 scenes/exemplos_gl.py                 # breakpoint IPython na linha 42
bin/manimgl                                             # quadro em branco interativo (§5.6)
```

`scenes/exemplos_gl.py` deste repositório tem três cenas comentadas (`GLOla`,
`GLSuperficie`, `GLInterativa`) que mostram as diferenças de API contra
`scenes/exemplos.py`, que é a versão CE das mesmas ideias. É o melhor lugar para
começar — os dois arquivos lado a lado ensinam o porte melhor que qualquer
tabela.
---

## 4. A CLI inteira, flag a flag

Fonte: `manimlib/config.py:54-229` (o `argparse` completo) e `:235-331` (o que
cada flag faz com a configuração). **Nenhuma flag foi inventada aqui.**

### 4.1 Tabela

| Flag | O que faz POR DENTRO |
|---|---|
| `arquivo.py Cena [Cena2 …]` | arquivo e nomes de cena; sem nome, ver §4.3 |
| `-w`, `--write_file` | `run.show_in_window = not write_file` → **headless**; `file_writer.write_to_movie = True` |
| `-s`, `--skip_animations` | pula as animações; **sozinho não grava nada** (§4.2) |
| `-o`, `--open` | abre o arquivo ao terminar — **e liga `-w` sozinho** (§4.2) |
| `--finder` | idem `-o`, mas revela a pasta (`xdg-open -R`); **também liga `-w`** |
| `-l` / `-m` / `--hd` / `--uhd` | 854×480 / 1280×720 / 1920×1080 / 3840×2160 (`resolution_options` do YAML) |
| `-r WxH` | resolução explícita, `"1920x1080"` — **`x` minúsculo, `split("x")`** |
| `--fps N` | frame rate (int). **Ignorado na janela**, ver §6.4 |
| `-c COR`, `--color` | cor de fundo, via `colour.Color(...)`; cor inválida → `sys.exit(2)` |
| `-t`, `--transparent` | `.mov` + `prores_ks` + `pixel_format=''` + `background_opacity=0` + `png_mode=RGBA` |
| `-i`, `--gif` | extensão `.gif` e **`video_codec = ''`** (deixa o ffmpeg inferir) |
| `--vcodec X` | codec do ffmpeg (é ele que vence `-t` e `-i`, ver §8.3) |
| `--pix_fmt X` | pixel format |
| `-n A[,B]` | começa na animação A (e termina em B); `-n 3,7` |
| `-e LINHA` | insere `self.embed()` depois da linha (§5.2) |
| `-p`, `--presenter_mode` | cada `wait` segura até Espaço/seta-direita. **Só com janela** (§4.4) |
| `-f`, `--full_screen` | janela em tela cheia |
| `-a`, `--write_all` | renderiza TODAS as cenas do arquivo |
| `--subdivide` | **um mp4 por `self.play()`**, numerados, numa pasta com o nome da cena |
| `--file_name NOME` | nome do arquivo de saída (sem extensão) |
| `--video_dir DIR` | diretório de saída, sobrepondo `directories.output` |
| `--config_file X.yml` | config extra, aplicada por último |
| `--prerun` | roda a cena INTEIRA antes, pulando animações, só para contar frames |
| `-q`, `--quiet` | some com a barra de progresso e com o `File ready at` |
| `--leave_progress_bars`, `--show_animation_progress` | barras |
| `--autoreload` | recarrega o módulo antes de cada célula do REPL (§5.5) |
| `--clear-cache` | apaga o cache de Tex/Text — **hífen, não underscore** |
| `--log-level NÍVEL` | DEBUG/INFO/WARNING/ERROR/CRITICAL — **hífen, não underscore** |
| `-v`, `--version` | versão. **`-v` do `manimgl` é versão; `-v` do `mx` é `--verbose`; `--verbosity` é da CE.** Três coisas diferentes |

Qualidade no GL é `-l -m --hd --uhd`; na CE é `-ql -qm -qh -qk`. Não são
sinônimos e não têm os mesmos valores.

**As duas flags de hífen são a armadilha boba.** Todas as outras usam
underscore (`--write_file`, `--file_name`, `--config_file`, `--pix_fmt`), e
essas duas não. `--log_level DEBUG` sai como `unrecognized arguments`, e como o
`parse_cli()` roda no import (§3.1), o erro aparece antes de qualquer coisa
sua rodar.

### 4.2 As três regras derivadas que não estão em nenhum `--help`

```python
# config.py:228    (o fim de parse_cli)
args.write_file = any([args.write_file, args.open, args.finder])
# config.py:271-273  (update_file_writer_config)
write_to_movie   = (not args.skip_animations) and args.write_file
save_last_frame  = args.skip_animations       and args.write_file
# config.py:324     (update_run_config)
show_in_window   = not args.write_file
```

Lidas juntas:

| Comando | O que acontece |
|---|---|
| `bin/manimgl a.py C` | **janela**, cena roda e a janela FICA ABERTA (`Scene.interact`) |
| `bin/manimgl -w a.py C` | headless, grava `C.mp4` |
| `bin/manimgl -s a.py C` | **janela**, avança até o fim; **não grava nada** |
| `bin/manimgl -ws a.py C` | headless, grava **só `C.png`** do último frame, sem mp4 |
| `bin/manimgl -so a.py C` | `-o` liga o `-w`: grava o PNG e **abre** |
| `bin/manimgl -o a.py C` | grava o mp4 e abre |

`bin/manimgl -ws arquivo.py Cena` é o **"renderize rápido e OLHE o PNG"** do
lado GL — é o ciclo que a skill `manim-verificacao-visual` descreve, e o único
jeito barato de pegar texto branco no branco, elemento cortado e sobreposição,
que não dão erro nenhum no terminal.

### 4.3 Sem nome de cena, ele PERGUNTA — e num agente isso trava

`extract_scene.get_scenes_to_render` (`extract_scene.py:94-107`):

- `--write_all`, ou **o arquivo tem exatamente uma cena** → roda o que existe;
- senão, casa os nomes que você passou;
- **se sobrar zero, chama `prompt_user_for_choice()`, que é um `input()`.**

Ou seja: `bin/manimgl -w arquivo.py` num arquivo com 3 cenas **fica esperando
você digitar**. Sob um agente ou num CI isso vira um processo pendurado — ou,
com stdin fechado, `EOFError → sys.exit(1)`. **Sempre passe o nome da cena, ou
`-a`.**

Para saber os nomes sem rodar nada, leia o arquivo: as cenas são as classes que
herdam de `Scene` e cujo `__module__` começa com o do módulo
(`extract_scene.py:28-36`). `bin/mx scenes` **não serve aqui** — ele importa
com o `manim` da CE.

Há um escape elegante e pouco conhecido: se o módulo define
`SCENES_IN_ORDER = [A, B, C]`, essa lista **substitui** a descoberta automática
(`extract_scene.py:116-117`). É o jeito do GL de dizer "estas, nesta ordem".

### 4.4 `-p` sem janela é um laço infinito

`presenter_mode` faz `wait()` chamar `hold_loop()`, e `hold_loop` só termina
quando `on_key_press` recebe Espaço ou seta-direita (`scene.py:614-617`,
`:843-845`). Sem janela não há teclado. **`bin/manimgl -w -p arquivo.py Cena`
fica girando para sempre**, sem gravar frame e sem erro.
[não verificado — deduzido de `scene.py:614` e `config.py:324`; não executado]

### 4.5 `--prerun` roda o `construct` DUAS vezes

`compute_total_frames` (`extract_scene.py:63-77`) instancia uma cópia da cena
com `skip_animations=True` e roda o `construct()` inteiro só para contar frames
e alimentar a barra de progresso. Numa cena com LaTeX pesado ou `always_redraw`
caro, isso **dobra o custo de CPU do render**. Em compensação, ele expõe
exceções antes de o encode começar. Use em cena longa; não use por hábito.

---

## 5. O fluxo interativo — a razão de existir do ManimGL

Isto é o que a CE não tem em nenhuma forma, e é o único motivo forte para trocar
de motor. O código todo mora em `manimlib/scene/scene_embed.py` (231 linhas) e
vale ler inteiro uma vez.

### 5.1 `self.embed()`

```python
# manimlib/scene/scene.py:203-221
def embed(self, close_scene_on_exit: bool = True,
          show_animation_progress: bool = False) -> None:
    if not self.window:
        return                      # <- NO-OP silencioso
    ...
    InteractiveSceneEmbed(self).launch()
    if close_scene_on_exit:
        raise EndScene()
```

Duas armadilhas nessas dez linhas:

- **`self.embed()` sob `-w` não faz absolutamente nada.** Sem janela, retorna na
  primeira linha. Ninguém avisa. Se você "pôs o embed e ele não abriu", olhe se
  há `-w`/`-o`/`--finder` na linha de comando (§4.2).
- **`embed()` encerra a cena ao sair do shell** (`raise EndScene()`), então tudo
  que vem depois dele no `construct` nunca roda. Quer continuar?
  `self.embed(close_scene_on_exit=False)`.

O shell que abre é um `InteractiveShellEmbed` do IPython com o **módulo da sua
cena** como namespace, mais as variáveis locais do `construct` no ponto da
chamada, mais **catorze atalhos injetados** (`scene_embed.py:61-79`):

```
play  wait  add  remove  remove_all_except  clear  focus
save_state  undo  redo  i2g  i2m
checkpoint_paste  clear_checkpoints  reload
```

Então no REPL você escreve `play(FadeIn(c))`, não `self.play(...)` — embora
`self` também esteja lá. `i2m(id)` devolve o mobject por `id()` e `i2g(*ids)`
devolve um grupo: é assim que o Ctrl+C da janela (§6.2) se liga ao teclado.

Enquanto o shell espera você digitar, um *inputhook* do prompt_toolkit redesenha
a janela no ritmo do `camera.fps` (`scene_embed.py:84-97`) — é por isso que a
cena continua viva e animável enquanto o cursor pisca.

**Exceção no REPL pisca a borda em vermelho** (`ensure_flash_on_error`,
`:110-118`): um `FullScreenRectangle` de stroke `RED` 30 em `VFadeInThenOut`,
meio segundo. Não é bug de render; é o retorno visual do erro.

### 5.2 `-e LINHA` — embed sem editar o arquivo

```bash
bin/manimgl -e 42 arquivo.py            # note: sem nome de cena
```

`insert_embed_line_to_module` (`extract_scene.py:146-172`) lê o fonte do módulo,
insere `self.embed()` depois da linha 42 com a indentação certa, recompila e
`exec`uta. E há um brinde: **se você não passar nome de cena, ele usa a última
`class` declarada acima da linha 42** — daí funcionar sem nome mesmo com o
arquivo cheio de cenas.

### 5.3 `checkpoint_paste()` — o fluxo do Grant, em uma função

Este é o coração do método, e ele é mais esperto do que parece:

```python
# scene_embed.py:208-221  (CheckpointManager.checkpoint_paste)
code_string = pyperclip.paste()          # o que está no CLIPBOARD
...
checkpoint_key = self.get_leading_comment(code_string)   # a 1ª linha, se for '#'
self.handle_checkpoint_key(scene, checkpoint_key)
shell.run_cell(code_string)
```

O uso é: você seleciona um bloco no editor, copia, e no REPL digita
`checkpoint_paste()`. Ele roda o bloco na cena viva. **E se o bloco começa com
um comentário, esse comentário vira uma chave de checkpoint:** na primeira vez o
estado da cena é salvo sob aquela chave; nas vezes seguintes, a cena é
**restaurada** para aquele estado antes de o bloco rodar (`:232-245`). É por
isso que os arquivos do 3b1b são cheios de comentários curtos abrindo blocos —
eles não são documentação, são pontos de retorno.

Rodar uma chave anterior **descarta** os checkpoints posteriores (`:236-240`),
o que mantém a linha do tempo consistente.

```python
checkpoint_paste()                      # roda o bloco copiado
checkpoint_paste(skip=True)             # roda pulando as animações (avanço rápido)
checkpoint_paste(record=True)           # roda GRAVANDO (§5.4)
checkpoint_paste(progress_bar=False)    # sem barra
clear_checkpoints()                     # esquece tudo
```

**Pré-requisito real:** `pyperclip` precisa de um backend de clipboard. Nesta
máquina existem `xclip`, `xsel` e `wl-copy`, e a sessão é X11 (`DISPLAY=:1`),
então funciona. Numa sessão sem eles, `pyperclip.paste()` levanta
`PyperclipException` e o método inteiro cai — inclusive o Shift+D da §6.3.

### 5.4 `record=True` grava só aquele bloco — o análogo GL da "cena em partes"

`checkpoint_paste(record=True)` entra em `Scene.temp_record()`:

```python
# scene.py:696-702
@contextmanager
def temp_record(self):
    with self.camera.at_output_resolution():
        self.file_writer.begin_insert()
        try: yield
        finally: self.file_writer.end_insert()
```

e `begin_insert` (`scene_file_writer.py:265-276`) abre um pipe de ffmpeg novo
apontando para `<saída>/inserts/<Cena>_<n>.mp4`, com `n` incrementando enquanto
o arquivo existir. Repare no `at_output_resolution()`: mesmo com a janela
pequena, o insert sai na resolução configurada.

Isto é a resposta do ManimGL ao problema que `manim-presentation-parts` resolve
na CE com mixin + `next_section(skip_animations=…)`: **um arquivo por beat, sem
re-rodar a cena inteira**. As duas abordagens não competem —

- a da CE é **reprodutível em lote** (um comando refaz tudo, o estado nunca
  diverge, o primeiro frame da parte N+1 é pixel a pixel o último da N);
- a do GL é **interativa e artesanal** (você grava o que acabou de ver).

Para um deck versionado, a da CE ganha — é ela que dá emenda invisível e
re-render determinístico. Para explorar antes de decidir, a do GL é imbatível.
`--subdivide` (§8.1) é a versão em lote disso: um mp4 por `self.play`.

### 5.5 `reload()` e `--autoreload`

`reload()` no REPL (`scene_embed.py:146-181`) **valida a sintaxe do arquivo
primeiro** (`compile()`, sem executar), e só então dispara o magic
`exit_raise` do IPython. Quem apara isso é o laço de `__main__.run_scenes()`,
que captura `KillEmbedded` e reinstancia a cena — **mantendo a mesma janela
aberta** (`Window.init_for_scene`, `window.py:139-147`). Sintaxe quebrada?
Ele recusa e diz onde, em vez de derrubar tudo:

```
[ERROR] Reload cancelled due to syntax errors.
```

`reload(37)` recarrega já com o embed na linha 37.

`--autoreload` (ou `embed.autoreload: True` no YAML) registra um hook
`pre_run_cell` que **recarrega o módulo antes de CADA célula** — útil quando
você edita funções auxiliares em outro arquivo, caro quando o módulo importa
coisa pesada.

### 5.6 `bin/manimgl` sozinho abre um quadro em branco interativo

Sem arquivo, `ModuleLoader.get_module(None)` devolve `None` e
`get_scene_classes` cai em `[BlankScene]` (`extract_scene.py:22-26`,
`module_loader.py:37-38`):

```python
class BlankScene(InteractiveScene):
    def construct(self):
        exec(manim_config.universal_import_line)   # "from manimlib import *"
        self.embed()
```

Então **`bin/manimgl` e mais nada** abre uma janela vazia com o namespace do
manimlib carregado e o REPL de pé. É o melhor lugar para conferir uma
assinatura, testar um mobject ou brincar com cor sem criar arquivo nenhum. E
como é uma `InteractiveScene`, todas as teclas de seleção da §6.2 valem.

---

## 6. A janela: teclas, mouse, e duas ligações mortas

### 6.1 O que vale em QUALQUER cena (`Scene.on_key_press`, `scene.py:819-845`)

| Tecla / gesto | Efeito | De onde vem |
|---|---|---|
| segurar `d` + mover o mouse | gira em 3D (`theta`/`phi` do frame) | `key_bindings.pan_3d` |
| segurar `f` + mover o mouse | arrasta o frame | `key_bindings.pan` |
| arrastar com o botão | arrasta o frame | `drag_to_pan = True` |
| roda do mouse | zoom (escala o frame no ponto do cursor) | `scroll_sensitivity = 20` |
| `r` | `frame.animate.to_default_state()` | `key_bindings.reset` |
| `Ctrl/Cmd + z` | `undo()` — pilha de até 50 estados | `max_num_saved_states = 50` |
| `Ctrl/Cmd + q` | sai | `key_bindings.quit` |
| Espaço ou seta-direita | libera o `wait` em presenter mode | `hold_on_wait = False` |

O log ao abrir também menciona `esc` para sair (`scene.py:187-198`).

`pan_sensitivity = 0.5`, `scroll_sensitivity = 20` e `invert_zoom_scroll = False`
são atributos de classe de `Scene` — sobrescreva na sua cena, não no YAML.

### 6.2 O que só vale em `InteractiveScene` (`interactive_scene.py:481-552`)

`InteractiveScene` é uma subclasse de `Scene` com uma UI de seleção por cima.
Herde dela (ou use `bin/manimgl` sem arquivo, §5.6) para ter:

| Tecla | Efeito |
|---|---|
| segurar `s` + varrer com o mouse | seleciona a região (soltar confirma) |
| `u` | limpa a seleção |
| segurar `g` / `h` / `v` / `z` | arrasta a seleção: livre / só X / só Y / só Z |
| segurar `t` (+`Shift`) | redimensiona (com `Shift`, a partir do canto) |
| `c` | abre a paleta de cores (as `MANIM_COLORS`) |
| `i` | mostra a caixa de informação enquanto pressionada |
| `k` | liga/desliga a cruz do cursor |
| setas (+`Shift`) | empurra a seleção 0,05 (mais, com `Shift`) |
| `Ctrl+c` | copia os **nomes** (ou `id()`) dos selecionados para o clipboard |
| `Ctrl+v` | cola: mobject por id; ou `Tex` se o texto tiver `\ ^ = +`; senão `Text` |
| `Ctrl+x` | copia e apaga · `Backspace` apaga |
| `Ctrl+a` | seleciona tudo |
| `Ctrl+g` | agrupa a seleção |
| `Ctrl+t` | alterna entre selecionar mobject de topo e peça interna |
| **`Shift+d`** | **copia o `reorient(...)` da câmera atual** — §6.3 |
| `Shift+c` | copia a coordenada do cursor, `"(x, y, z)"` |

O `Ctrl+c` é o par do `i2m`/`i2g` do REPL (§5.1): ele varre o `user_ns` do
IPython atrás de um nome que aponte para aquele mobject e, se achar, copia o
**nome da variável**; senão copia o `id()` (`interactive_scene.py:355-366`).

A docstring da classe (`:62-79`) diz "hold ctrl" para selecionar. **A docstring
está desatualizada** — o código usa `SELECT_KEY`, que vem de
`key_bindings.select` e é `s`. Acredite no código.

### 6.3 `Shift+D`: a tecla que justifica abrir a janela

```python
# interactive_scene.py:640-648
call = "reorient("
call += "%d, %d, %d" % tuple(angles / DEG)          # theta, phi, gamma
if any(center != 0):        call += ", (%.2f, %.2f, %.2f)" % tuple(center)
if height != FRAME_HEIGHT:  call += ", %.2f" % height
call += ")"
pyperclip.copy(call)
```

Você posiciona a câmera com o mouse até ficar bonito, aperta **Shift+D**, e cola
no arquivo uma linha pronta:

```python
self.frame.reorient(-30, 70, 0, (1.20, -0.40, 0.00), 6.50)
```

A assinatura real, conferida no índice (`api/manimgl-methods.tsv`,
`CameraFrame.reorient`):

```python
reorient(theta_degrees=None, phi_degrees=None, gamma_degrees=None,
         center=None, height=None)
```

Não existe equivalente na CE. Lá o ângulo se descobre renderizando PNG e
chutando de novo — que é exatamente o laço que esta tecla elimina. **Se a única
coisa que você precisa do ManimGL é achar um enquadramento 3D, ainda assim vale
abrir a janela.**

### 6.4 Na janela, o FPS é 30 e ponto

```python
# scene.py:103-107
if self.window:
    self.window.init_for_scene(self)
    self.camera_config["fps"] = 30       # sobrescreve tudo
```

`camera.fps: 60` no YAML e `--fps 60` na linha de comando são **ignorados
enquanto há janela**. Só o render com `-w` respeita o que você pediu. Se o
preview parece mais "duro" que o arquivo final, é isto — e não é defeito.

No mesmo espírito: com janela, a câmera desenha **no tamanho da janela**, não na
resolução configurada (`camera.py:140`: `draw_at_window_size = window is not
None`). Por isso o preview pode ter proporção diferente do arquivo, e por isso
`get_image()` e a abertura do pipe de vídeo entram num
`with self.camera.at_output_resolution():` antes de medir qualquer coisa.

### 6.5 Duas ligações de tecla são inalcançáveis

`Mods.CTRL_OR_CMD = CTRL | CMD` e `Mods.SHIFT` são bits independentes
(`event_keys.py:38-51`). Numa cadeia `elif`, o teste de `CTRL_OR_CMD` casa
**também** quando `Shift` está junto:

```python
# scene.py:838-841
elif char == "z" and (modifiers & Mods.CTRL_OR_CMD):                  # ← Ctrl+Shift+Z cai AQUI
    self.undo()
elif char == "z" and (modifiers & (Mods.CTRL_OR_CMD | Mods.SHIFT)):   # ← inalcançável
    self.redo()
```

O mesmo padrão em `interactive_scene.py:514-517` (`Ctrl+G` agrupa, e
`Ctrl+Shift+G` **também** agrupa em vez de desagrupar).

**Mas a conclusão de que "não têm tecla" é FALSA — e esta é uma correção.** O
segundo `elif` é alcançável: basta **Shift sozinho, sem Ctrl**. `window.py:54-62`
normaliza a letra:

```python
def to_key(name):
    # "A letter comes back the same whether or not shift was held, so that a
    #  binding tested while shift is down still matches."
    return ord(name.lower()) if len(name) == 1 else None
```

Então **Shift+Z** entrega `char == "z"` com `modifiers == Mods.SHIFT`:

- `scene.py:837` — `SHIFT & CTRL_OR_CMD` = 0 → **não** casa;
- `scene.py:839` — `SHIFT & (CTRL_OR_CMD | SHIFT)` = SHIFT → **casa, `redo()` roda**.

Idem `interactive_scene.py:516-517`: **Shift+G desagrupa**.

Consequência prática corrigida: as teclas existem, só não são as que o manual
mental sugere.

| Você quer | A tecla que funciona | A que NÃO funciona |
|---|---|---|
| desfazer | `Ctrl+Z` | — |
| **refazer** | **`Shift+Z`** | `Ctrl+Shift+Z` (cai no `undo`) |
| agrupar | `Ctrl+G` | — |
| **desagrupar** | **`Shift+G`** | `Ctrl+Shift+G` (cai no `group`) |

O que continua verdadeiro é o defeito: `Ctrl+Shift+Z` faz o **oposto** do que
você espera. No REPL, `redo()` e `self.ungroup_selection()` também resolvem.
[fonte lida em `scene.py:835-841`, `interactive_scene.py:513-517`,
`window.py:54-62`; nenhuma tecla foi apertada nesta rodada]

---

## 7. Configuração: `custom_config.yml`

### 7.1 A precedência, e o `cwd` como parte dela

```python
# config.py:35-39
config = Dict(merge_dicts_recursively(
    load_yaml(<manimlib>/default_config.yml),   # 1. defaults do pacote
    load_yaml("custom_config.yml"),             # 2. DO DIRETÓRIO ATUAL
    load_yaml(args.config_file) if args.config_file else dict(),   # 3.
))
# depois: as flags de CLI sobrescrevem campo a campo (:43-49)
```

**O `custom_config.yml` é procurado no diretório de onde você chamou o comando.**
Rodar `bin/manimgl` de dentro de `scenes/` não pega a config do repositório:
você volta ao fundo `#333333`, 30 fps, saída em `./videos/` e sem NVENC no YAML.
É o mesmo tipo de armadilha que o `manim.cfg` da CE tem (`manim-project §5`), e o
sintoma aqui é visual — "o fundo ficou cinza" —, não um erro.

Para não depender do `cwd`: `bin/manimgl --config_file "$PWD/custom_config.yml" …`.

### 7.2 As 14 seções e os 3 escalares soltos

`default_config.yml` tem **14 seções** — `directories` `window` `camera`
`file_writer` `scene` `vmobject` `mobject` `tex` `text` `embed`
`resolution_options` `sizes` `key_bindings` `colors` — **mais três chaves
escalares no topo**, que costumam passar despercebidas:

```yaml
log_level: "INFO"
universal_import_line: "from manimlib import *"   # o que a BlankScene executa
ignore_manimlib_modules_on_reload: True
```

O que morde, chave por chave:

| Chave | Default do pacote | Aqui | Por que importa |
|---|---|---|---|
| `camera.background_color` | **`#333333`** | `#000000` | o master trocou o preto por cinza escuro; sem dizer nada, seu vídeo sai cinza |
| `camera.fps` | **30** | 60 | e na janela vira 30 de novo (§6.4) |
| `camera.resolution` | `(1920, 1080)` | idem | **define o `FRAME_WIDTH`** (§3.2) |
| `camera.bundle_draws` / `draw_together` | `True` | `True` | otimizações de draw do wgpu; desligue só para depurar artefato |
| `text.font` | **`Consolas`** | idem | a fonte padrão de `Text` é MONOESPAÇADA. Não é a `Text` da CE |
| `tex.template` | `default` | idem | um dos **58 templates** de `tex_templates.yml` (§9.3) |
| `vmobject.default_stroke_color` | `#DDDDDD` | idem | quase branco: em fundo claro, some |
| `mobject.default_mobject_color` | `#FFFFFF` | idem | idem |
| `sizes.frame_height` | `8.0` | idem | com a resolução, define o palco inteiro |
| `directories.base` | `""` (o cwd) | `./media-gl` | |
| `directories.cache` | `""` | `""` | vazio → `appdirs.user_cache_dir("manim")` = `~/.cache/manim` (§9.4) |
| `directories.mirror_module_path` | `False` | `False` | **não ligue** — ver abaixo |
| `scene.show_animation_progress` | `False` | `True` | |
| `colors.*` | 53 nomes | herdados | é daqui que saem `BLUE_D`, `RED_C`, `GREY_A`… (§3.2) |
| `embed.exception_mode` | `Verbose` | idem | o `xmode` do IPython no REPL |
| `key_bindings.*` | 13 teclas | herdadas | inclui `cursor: "k"`, que quase nenhum guia cita |

**`mirror_module_path: True` provavelmente quebra.** `get_output_directory`
(`config.py:384-392`) lê `dir_config.removed_mirror_prefix`, e essa chave **não
existe em `default_config.yml`**. Como o config é um `addict.Dict`, o acesso
devolve um dicionário vazio em vez de erro, e `str(path).startswith({})` levanta
`TypeError`. Se você precisa espelhar a árvore de módulos, defina
`removed_mirror_prefix` explicitamente.
[não verificado — deduzido de `config.py:389` + ausência da chave no YAML]

### 7.3 O `custom_config.yml` deste repositório

Ele está comentado linha a linha; leia-o antes de mudar qualquer coisa. Os três
desvios deliberados:

- `directories.base: "./media-gl"` — a saída do GL **não** vai para `media/`,
  que é da CE;
- `camera.background_color: "#000000"` e `fps: 60`;
- `file_writer.video_codec: "libx264"` **de propósito** — o arquivo é versionado
  e precisa funcionar em máquina sem NVIDIA, onde `h264_nvenc` aborta com
  `Unknown encoder`. Quem liga o NVENC é o wrapper `bin/manimgl`, que detecta a
  placa e injeta `--vcodec h264_nvenc` **só se você não tiver passado `--vcodec`**
  (`bin/manimgl:20-31`).

> **Correção de uma versão anterior desta skill.** Ela afirmava que o
> `custom_config.yml` daqui "já vem com `video_codec: h264_nvenc`". **Não vem**,
> e não deve vir. `manim-project §11` e `manim-gpu-encoding §10` já haviam
> registrado o erro; agora ele está corrigido na fonte.

---

## 8. Saída, encoding e som

### 8.1 Onde o arquivo cai, e como um script descobre

`update_directory_config` concatena `base + subdirs.output`, então aqui a saída é
`media-gl/videos/<NomeDaCena>.mp4` (e `.png` para `-ws`). O nome vem de
`str(self.scene)`, que é o nome da classe; com `-n 3,7` vira `<Cena>_3_7.mp4`
(`scene_file_writer.py:102-124`).

**O ManimGL não tem `--json`.** Para capturar o caminho num script, ou você
define `--file_name` e monta o caminho, ou lê a linha

```
File ready at /caminho/Cena.mp4
```

que sai por `log.info` (`scene_file_writer.py:353-355`) — e o logger do GL usa um
`RichHandler`, que escreve em **stdout**. Com `-q` a linha some. Preferir
`--file_name` é mais robusto do que parsear.

`--subdivide` escreve um mp4 por `self.play()` numa pasta com o nome da cena,
numerados `00000.mp4`, `00001.mp4`… (`get_next_partial_movie_path`, `:126-128`).
É o irmão em lote do `record=True` da §5.4.

### 8.2 O comando de ffmpeg, na íntegra

```python
# scene_file_writer.py:216-240 (open_movie_pipe), abreviado
command = [ffmpeg_bin, '-y', '-f','rawvideo', '-s', f'{w}x{h}',
           '-pix_fmt','rgba', '-r', str(fps), '-i','-', '-an',
           '-loglevel','error']
if (saturation, gamma) != (1.0, 1.0):
    command += ['-vf', f'eq=saturation={saturation}:gamma={gamma}']
if self.video_codec:     command += ['-vcodec', self.video_codec]
if self.pixel_format:    command += ['-pix_fmt', self.pixel_format]
if self.crf is not None: command += ['-crf', str(self.crf)]
```

Três coisas se leem daí:

- **o GL chama o BINÁRIO do ffmpeg** — trocar codec é um flag, ao contrário da
  CE, que usa PyAV e precisa da camada `manimx` (`manim-gpu-encoding §2-3`);
- `crf` é parâmetro real do `SceneFileWriter`, default `None`, e **não está no
  YAML** — só um comentário mencionando-o. Para lossless, o próprio comentário do
  pacote recomenda `video_codec: libx264rgb` + `pixel_format: rgb24` + `crf: 0`
  (há até um atalho pronto, `use_fast_encoding()`, que faz `libx264rgb`/`rgb32`);
- `saturation`/`gamma` diferentes de 1,0 inserem um filtro `eq`, e o comentário do
  próprio pacote avisa que **até a identidade não é de graça**: o `eq` trabalha em
  YUV, então todo pixel sai de RGB e volta, movendo a maioria em 1 ou 2 de 255.

**A armadilha do `crf` com NVENC, agora com o mecanismo.** `-crf` é opção privada
do libx264/libx265; `h264_nvenc` não a conhece. O ffmpeg reclamaria — mas o
comando fixa **`-loglevel error`**, e a reclamação sai em nível *warning*. Ou
seja: o arquivo sai com o controle de taxa padrão do NVENC, **sem uma linha na
tela**. Para qualidade em NVENC o parâmetro seria `cq`, que o `SceneFileWriter`
não expõe. [o `-loglevel error` é fonte lida; o nível do aviso do ffmpeg não foi
observado nesta rodada]

### 8.3 `-t` e `-i` são silenciosamente anulados pelo wrapper nesta máquina

Esta é nova, e é a pior da seção. A escolha de codec é uma cadeia `elif`
(`config.py:283-289`):

```python
if args.vcodec:        file_writer_config.video_codec = args.vcodec
elif args.transparent: video_codec = 'prores_ks'; pixel_format = ''
elif args.gif:         video_codec = ''
```

`--vcodec` **vence** `-t` e `-i`. E o `bin/manimgl` injeta `--vcodec h264_nvenc`
sempre que há NVIDIA e você não passou codec (`bin/manimgl:20-31`). Logo, nesta
máquina:

| Comando | O que você pediu | O que sai |
|---|---|---|
| `bin/manimgl -w -t a.py C` | `.mov` ProRes com alfa | `.mov` **H.264 4:2:0** — o alfa some, sem aviso |
| `bin/manimgl -w -i a.py C` | `.gif` | `-vcodec h264_nvenc … saída.gif` — o ffmpeg não tem o que fazer com isso |

**Dizer o codec você mesmo desarma a injeção — mas, no caso do alfa, NÃO basta.**
Esta é uma correção: a versão anterior parava em `--vcodec prores_ks` e chamava
isso de correção. O `.mov` continua saindo **sem canal alfa**, pelas mesmas
linhas citadas acima.

O motivo está no `elif`. Quem zerava o `pixel_format` era **só** o ramo
`elif args.transparent` — e passar `--vcodec` faz o `if` casar primeiro, então
esse ramo nunca roda. E o `pixel_format` não é vazio por default: o
`default_config.yml:69` o fixa em `"yuv420p"`, que vira flag literal:

```python
# scene_file_writer.py:236-237
if self.pixel_format:  command += ['-pix_fmt', self.pixel_format]
```

O ffmpeg recebe `-vcodec prores_ks -pix_fmt yuv420p` — um pixel format **sem
plano alfa**. Precisa dos dois:

```bash
bin/manimgl -w -t --vcodec prores_ks --pix_fmt yuva444p10le a.py C   # alfa de verdade
bin/manimgl -w -i --vcodec ""       a.py C    # deixa o ffmpeg inferir pelo .gif
```

E note a assimetria que salva o caso do gif e **não** salva o do alfa:
`--pix_fmt ""` não serve de escape, porque `if args.pix_fmt:` é falso em string
vazia — ao contrário de `--vcodec ""`, que funciona justamente por cair no
`elif args.gif`.

[o comportamento do wrapper e a cadeia `elif` são fonte lida; o resultado dos dois
comandos NÃO foi executado nesta rodada]

### 8.4 Som existe no ManimGL, e é diferente da CE

```python
Scene.add_sound(sound_file, time_offset=0, gain=None, gain_to_background=None)
SceneFileWriter.add_sound(sound_file, time=None, gain=None, gain_to_background=None)
```

A CE não tem `gain_to_background` (lá são três parâmetros), e o parâmetro de
tempo muda de nome entre as duas camadas — `time_offset` na `Scene`, `time` no
writer. A mixagem é `pydub.AudioSegment`, exportada em WAV e remuxada no fim com
`-c:v copy -c:a aac -b:a 320k` (`scene_file_writer.py:317-346`). Também **não há
`add_subcaption` no GL** — legenda `.srt` é recurso só da CE.

`Scene.add_sound` **retorna sem fazer nada quando `skip_animations` está ligado**
(`scene.py:636-642`), então som e `-s` não convivem.

Codec, NVENC, peso do arquivo, matriz de qualidade: **`manim-gpu-encoding`** é a
dona. Não repita número dela aqui.
---

## 9. LaTeX e texto no ManimGL

### 9.1 Só `latex` e `xelatex` — e `dvisvgm` é obrigatório

```python
# utils/tex_file_writing.py:90-99
if   compiler == "latex":   dvi_ext = ".dvi"
elif compiler == "xelatex": dvi_ext = ".xdv"
else: raise NotImplementedError(f"Compiler '{compiler}' is not implemented")
```

Depois do `latex -interaction=batchmode -halt-on-error`, ele chama
**`dvisvgm <dvi> -n -v 0 --stdout`** (`:137-146`) e **não confere o código de
retorno**: `result = process.stdout.decode("utf-8")`, e pronto. Duas
consequências:

- `dvisvgm` ausente do PATH → `FileNotFoundError` cru. É exatamente o que
  acontece chamando `.venv-gl/bin/manimgl` sem o wrapper nesta máquina
  (`manim-project §3.1`);
- `dvisvgm` presente mas falhando por outro motivo → **SVG vazio, mobject sem
  pontos, nada na tela e nenhum erro**. Se uma `Tex` sumiu sem explicação, rode
  o `dvisvgm` na mão sobre o `.dvi` que ficou (§9.2).

Erro de LaTeX vira `LatexError` com o trecho extraído do `.log`
(`re.search(r"(?<=\n! ).*\n.*\n", …)`, `:128-135`) — só as duas linhas depois do
`!`. Para o log inteiro, vá ao arquivo (§9.2).

### 9.2 O `working.tex` é UM só — não paralelize

```python
temp_dir = Path(manim_config.directories.latex_cache)   # aqui: media-gl/latex_cache
tex_path = temp_dir / "working.tex"                     # nome FIXO
```

Dois processos `manimgl` compilando LaTeX ao mesmo tempo, do mesmo diretório,
sobrescrevem o `working.tex` um do outro. É o primo do problema que
`manim-batch-pipeline` documenta na CE (lá o `tex_dir` é *apagado* inteiro). No
GL não há isolamento por worker nenhum: **um render de cada vez, ou `--config_file`
apontando `directories.base` diferente por processo**.

O lado bom: depois de um erro, o `working.tex`, o `working.log` e o `.dvi`
continuam lá para você olhar.

### 9.3 O preâmbulo padrão compila nesta máquina — os 18 pacotes existem

`tex_templates.yml` traz **58 templates** (`default`, `ctex`, `basic`, `empty`,
e 54 de fonte: `palatino`, `libertine`, `comic_sans`, `papyrus`…). O `default`
carrega 18 pacotes, e todos os 18 têm `.sty` no TinyTeX daqui — verificado por
`find ~/.TinyTeX -name '<pkg>.sty'`, sem compilar nada:

```
babel inputenc fontenc amsmath amssymb dsfont setspace tipa relsize
textcomp mathrsfs calligra wasysym ragged2e physics xcolor microtype pifont
```

(É um contraste útil: `manim-text-latex` registra que **`siunitx` NÃO está**
instalado. O preâmbulo do GL não o usa; o exemplo daquela skill usava.)

Trocar de template é por config ou por argumento:

```yaml
tex:
  template: "palatino"
```

```python
Tex(r"\int_0^1 x^2\,dx", template="palatino",
    additional_preamble=r"\usepackage{physics}")
```

Nome desconhecido não é erro: cai para `default` com um `log.warning`
(`tex_file_writing.py:19-27`).

### 9.4 O cache do GL não está em `media-gl/`

`full_tex_to_svg` e `markup_to_svg` são decorados com `@cache_on_disk`, um
`diskcache.Cache` em `get_cache_dir()` com **limite de 1 GB**
(`utils/cache.py:17-18`). E `get_cache_dir()` devolve
`directories["cache"] or appdirs.user_cache_dir("manim")` — como `cache: ""` é o
default, o cache real fica em **`~/.cache/manim/cache.db`**, fora do repositório
e fora do `media-gl/`. Quem limpa é `manimgl --clear-cache` (que só chama
`_cache.clear()` e segue, `__main__.py:59-60`).

Ele é **independente** do cache de *partial movies* da CE, que vive em `media/`
e é controlado por `--disable_caching`/`--flush_cache`. As duas coisas não se
falam.

### 9.5 As quatro classes de texto do GL, e por que a nitidez é outra história

| GL | Papel | CE equivalente |
|---|---|---|
| `Text(text, isolate=(\w+, \S+), use_labelled_svg=True, …)` | texto puro, via Pango | `Text` |
| `MarkupText(text, font_size=48, …, t2c, t2f, t2g, t2s, t2w, …)` | markup do Pango; **`Text` herda dela** | `MarkupText` |
| `Tex(*tex, font_size=48, alignment='\\centering', template='', additional_preamble='', t2c, isolate)` | LaTeX **em modo matemático** | `MathTex` |
| `TexText(mesma assinatura)` | LaTeX **em modo texto** | `Tex` |
| `OldTex` / `OldTexText` | a API antiga (`arg_separator`, `isolate: List[str]`) | — |
| `Code(code, font='Consolas', font_size=24, language='python', code_style='monokai')` | via Pygments → markup do Pango | `Code` (assinatura totalmente diferente) |

`Text`, `MarkupText`, `Tex` e `TexText` herdam todas de **`StringMobject`**, que
é a peça central do GL: ela guarda o mapeamento string → glifos e é o que
permite `TransformMatchingStrings` (§11). A CE não tem análogo direto.

**A nitidez do texto é diferente entre os motores, e isso importa.** A CE entrega
a string ao Pango em `font_size / 4.8` pt (`TEXT2SVG_ADJUSTMENT_FACTOR`), o que
para `font_size=22` dá 4,58 pt — e o cairo arredonda a posição X de cada glifo
para inteiro, gastando ~8% do em por letra (o achado completo está em
`manim-project` §10.5, e a correção de referência em
`~/Projects/aulas/aulas/002-deepseek-harness/manim/tema.py`). O GL faz outra
conta:

```python
# mobject/svg/text_mobject.py:351
"font_size": str(round(self.font_size * 1024)),   # unidades do Pango = 1/1024 pt
# :90     — e o canvas é fixo
width=DEFAULT_CANVAS_WIDTH,   # 16384
height=DEFAULT_CANVAS_HEIGHT, # 16384
```

Ou seja: `font_size=48` no GL vira **48 pt de verdade**, num canvas de 16384 px,
e depois o mobject é escalado por `get_text_mob_scale_factor()` para que
`text.font_size_for_unit_height` (144) dê altura 1 unidade. Um em de 48 pt tem
ordem de dezenas de unidades de dispositivo, contra os ~6 da CE — o mesmo
arredondamento de meia unidade custa proporcionalmente muito menos. **Conclusão
prática: no ManimGL você não precisa do truque de "desenhar grande e encolher".**
[o mecanismo é fonte lida; a comparação numérica NÃO foi medida nesta rodada]

Dois efeitos colaterais do canvas fixo, ambos a favor: o SVG não muda de quebra
de linha conforme a qualidade do render (o bug latente que a CE tem, também em
`manim-project` §10.6), e o cache em `~/.cache/manim` é consistente entre
resoluções. A quebra de linha só entra em cena se você passar `line_width`, que é
convertido com `line_width / FRAME_WIDTH * DEFAULT_PIXEL_WIDTH`
(`text_mobject.py:75`) — e `FRAME_WIDTH` depende da resolução (§3.2), então
**`line_width` com `-r` vertical quebra em outro ponto**.

---

## 10. Traduzir GL ↔ CE de verdade

### 10.1 Os números, e o que eles querem dizer

Gerado por reflexão dos dois pacotes instalados (`bin/mx api-diff`, resultado em
`api/ce-vs-gl.md`):

| | ManimCE 0.21.0 | ManimGL 1.7.2 |
|---|---:|---:|
| classes públicas | 337 | 270 |
| funções públicas | 281 | 216 |
| nomes no `import *` | 588 | **704** |
| classes só nesta edição | 184 | 117 |
| classes com nome em comum | 153 | 153 |
| **dessas, com assinatura diferente** | **153** | **153** |

A última linha é a que dói: **não existe uma única classe homônima cuja
assinatura seja idêntica nos dois.** Portar não é trocar o import — o import é a
parte que funciona.

### 10.2 Renomeações, corrigidas

| ManimGL | ManimCE | observação |
|---|---|---|
| `from manimlib import *` | `from manim import *` | |
| `ShowCreation` | `Create` | `ShowCreation` **não existe** na CE |
| `Tex` (modo matemático) | `MathTex` | ⚠️ os nomes se cruzam: a `Tex` da CE é modo TEXTO |
| `TexText` | `Tex` | |
| `OldTex` / `OldTexText` | `MathTex` / `Tex` | a API antiga do GL, ainda exportada |
| `ax.get_graph(f)` | `ax.plot(f)` | ⚠️ `get_graph` **existe no GL** como método de `CoordinateSystem` — a tabela de `ce-vs-gl.md` marca "—" porque olha só o topo do módulo |
| `ax.get_area_under_graph` | `ax.get_area` | |
| `self.frame` / `self.camera.frame` | `self.camera.frame` **só** em `MovingCameraScene`/`ZoomedScene` | §10.6 |
| `frame.reorient(θ, φ, γ, centro, altura)` | `set_camera_orientation(phi=…, theta=…)` numa `ThreeDScene` | §10.6 |
| `mob.fix_in_frame()` | `self.add_fixed_in_frame_mobjects(mob)` | GL marca o mobject; CE marca na cena |
| `mob.set_width(4)` | `mob.width = 4` / `mob.set(width=4)` / `scale_to_fit_width(4)` | §10.7 |
| `TransformMatchingStrings` | `TransformMatchingTex` / `TransformMatchingShapes` | |
| `-l / -m / --hd / --uhd` | `-ql / -qm / -qh / -qk` | |
| `--vcodec X` | `mx render --codec …` | a CE usa PyAV, não o binário |
| `self.embed()`, `checkpoint_paste()`, `reload()` | **sem equivalente** | §5 |

Dois nomes que **não existem em NENHUM dos dois** e continuam circulando em
tutoriais de 2019: **`TexMobject`**, **`TextMobject`** e **`GraphScene`**.
Conferido nos dois índices. Se você viu num guia, o guia é de outra era.

### 10.3 O que falta de cada lado (o que realmente trava um porte)

**Não existe no ManimGL** (amostra útil das 184 classes só-CE): `Table`,
`MathTable`, `IntegerTable`, `DecimalTable`, `MobjectTable`, `Graph`, `DiGraph`,
`GenericGraph`, `LayoutFunction`, `ManimColor`, `ManimConfig`, `Section`,
`DefaultSectionType`, `MovingCamera`, `MovingCameraScene`, `ZoomedScene`,
`MultiCamera`, `SplitScreenCamera`, `LinearTransformationScene`, `VectorScene`,
`SpecialThreeDScene`, `Polygram`, `RegularPolygram`, `ConvexHull`, `Cutout`,
`Star`, `PolarPlane`, `Paragraph`, `Variable`, `Typst`, `MathTypst`,
`TexTemplate`, `VDict`, `Circumscribe`, `Wiggle`, `ChangeSpeed`, `Unwrite`,
`SpiralIn`, `ArcBrace`, `BraceBetweenPoints`, `LabeledDot`, `Dot3D`, `Arrow3D`,
`Icosahedron`, `Octahedron`, `Tetrahedron`, `Polyhedron`, `ManimBanner`, e os 44
`OpenGL*`.

**Não existe no ManimCE** (amostra das 117 só-GL): `ShowCreation`,
`TexText`, `OldTex`, `StringMobject`, `TransformMatchingStrings`,
`TransformMatchingParts`, `InteractiveScene`, `InteractiveSceneEmbed`,
`CheckpointManager`, `CameraFrame`, `Window`, `EventDispatcher`, `EventType`,
`EventListener`, `Keys`, `Mods`, `GlowDot`, `GlowDots`, `DotCloud` (existe na CE
só no lado OpenGL), `TracingTail`, `VShowPassingFlash`, `FlashAround`,
`FlashUnder`, `VFadeIn`/`VFadeOut`/`VFadeInThenOut`, `Bubble`, `SpeechBubble`,
`ThoughtBubble`, `DieFace`, `Checkmark`, `Exmark`, `Piano`, `Laptop`,
`Speedometer`, `Dartboard`, `Clock`, `VideoSeries`, `NewtonFractal`,
`MandelbrotFractal`, `JuliaFractal`, `Prismify`, `VCube`, `VPrism`, `VGroup3D`,
`SurfaceMesh`, `TexturedSurface`, `TimeVaryingVectorField`, `AnimatedStreamLines`,
`ControlPanel`, `Slider`, `Checkbox`, `Textbox`, `Button`, `ColorSliders`,
`ExponentialValueTracker`, `Updater`, `MotionMobject`.

### 10.4 As cinco armadilhas de assinatura que mordem calado

Todas de `api/ce-vs-gl.md`, seção "Nome igual, assinatura diferente":

| Classe | CE | GL | O que quebra |
|---|---|---|---|
| `FadeIn` | `(*mobjects, **kwargs)` | `(mobject, shift=ORIGIN, scale=1, **kwargs)` | `FadeIn(a, b)` no GL passa `b` como `shift` |
| `Circle` | `(radius=None, color=RED_C, **kw)` | `(start_angle=0, stroke_color=RED_C, **kw)` | **`Circle(2)` no GL é um ângulo inicial de 2 rad, não raio 2** |
| `Arc` | `(radius, start_angle, angle, …)` | `(start_angle, angle, radius, …)` | ordem posicional trocada |
| `AnnularSector` | `(inner_radius, outer_radius, angle, …)` | `(angle, start_angle, inner_radius, …)` | idem |
| `Cube` | `(side_length=2, fill_opacity=.75, …)` | `(color=BLUE_D, opacity=1, shading=…, …)` | `Cube(3)` no GL passa `3` como cor |

O padrão é sempre o mesmo: **argumento posicional que muda de posição**. A regra
de sobrevivência num porte é banal e funciona — **passe tudo por palavra-chave**.
Um `Circle(radius=2)` está certo nos dois; `Circle(2)` está certo em um só.

### 10.5 `rate_func`: 49 na CE, 15 no GL

O GL tem `linear smooth double_smooth rush_into rush_from slow_into
not_quite_there wiggle squish_rate_func lingering exponential_decay
there_and_back there_and_back_with_pause running_start` **+ `overshoot`** (que a
CE não tem).

**As 35 que só existem na CE** são exatamente a família `ease_*` inteira (30) mais
`smoothstep`, `smootherstep`, `smoothererstep`, `unit_interval` e `zero`. Ou
seja: uma cena da CE que usa `ease_out_expo` — como o `SAIDA` do tema de
`~/Projects/aulas` — **não roda no GL**, e o erro é um `NameError` limpo no
import, não um defeito visual. Substituir por `rush_from` é a aproximação mais
próxima; se você precisa da curva exata, copie a função (são 3 linhas de numpy
cada) para o seu módulo.

Aprofundamento sobre ritmo, `lag_ratio`, `path_func` e composição: skill
**`manim-composicao-ritmo`** (lado CE).

### 10.6 Câmera: no GL toda cena já tem `self.frame`

```python
# scene.py:109-116
self.camera: Camera = Camera(window=self.window, samples=self.samples, **cfg)
self.frame: CameraFrame = self.camera.frame
self.frame.reorient(*self.default_frame_orientation)
```

`CameraFrame` é um `Mobject` — então `self.frame.animate.reorient(...)`,
`save_state()`/`Restore`, updater seguindo alvo, tudo funciona, **em qualquer
cena**. Na CE isso só existe em `MovingCameraScene` e `ZoomedScene` (via
`MovingCamera`), e **não** existe em `ThreeDScene`, cuja `ThreeDCamera` só tem
`frame_center` — a skill `manim-3d-camera` está sendo corrigida nesse ponto.

`CameraFrame` tem 37 métodos próprios; os que se usam de fato:

```python
reorient(theta_degrees, phi_degrees, gamma_degrees, center, height)
set_euler_angles(theta, phi, gamma, units=DEG)  ·  increment_theta/phi/gamma
set_field_of_view(fov)  ·  set_focal_distance(d)  ·  set_euler_axes("zxz")
to_default_state()  ·  make_orientation_default()  ·  add_ambient_rotation(rate)
get_euler_angles()  ·  get_implied_camera_location()
to_fixed_frame_point(p, relative=False)  ·  from_fixed_frame_point(...)
```

`add_ambient_rotation(angular_speed=1*DEG)` é o equivalente de
`begin_ambient_camera_rotation` da CE, e `Scene.set_floor_plane("xz")`
(`scene.py:718-724`) troca os eixos de Euler para quem pensa em Y-up.

### 10.7 `set_width`/`set_height`: canônico no GL, sintetizado na CE

O `Mobject` do ManimGL tem **233 métodos próprios** contra **157** do da CE, e
entre eles estão `set_width`, `set_height`, `set_depth`, `set_min_width`,
`set_max_height`, `set_shape`, `arrange_to_fit_width`… Eles são a API normal ali.

Na CE, `set_width` **não existe no `Mobject` do cairo** — só em
`OpenGLMobject`. O que faz `mob.set_width(4)` "funcionar" na CE é o
`Mobject.__getattr__` (`manim/mobject/mobject.py:729+`), que sintetiza qualquer
`set_*`/`get_*` em cima do atributo homônimo e emite um `DeprecationWarning`
que ninguém lê. É a armadilha nº 1 documentada em `manim-api-discovery §8`.

**Ao portar GL → CE, `set_width`/`set_height` são o primeiro `grep`.** Troque por
`mob.width = 4`, `mob.set(width=4)` ou `scale_to_fit_width(4)`.

Outros métodos GL sem par na CE, e que aparecem em qualquer código do 3b1b:
`fix_in_frame()` / `unfix_from_frame()` / `is_fixed_in_frame()`,
`apply_depth_test()` / `deactivate_depth_test()`, `set_shading(...)`,
`set_gloss`, `set_shadow`, `set_reflectiveness`, `set_clip_plane`,
`set_flat_stroke`, `replicate(n)`, `looks_identical(other)`, `is_changing()`,
`insert_updater`, `serialize`/`deserialize`, `set_color_by_rgba_func`.

### 10.8 `ThreeDScene` tem o mesmo nome e não é a mesma coisa

```python
# manimlib/scene/scene.py:922-940
class ThreeDScene(Scene):
    samples = 4                          # MSAA
    default_frame_orientation = (-30, 70)
    always_depth_test = True
    def add(self, *mobjects, set_depth_test=True, perp_stroke=True):
        ...  # aplica depth test em cada submobject não fixo
        ...  # e set_flat_stroke(False) em todo VMobject com stroke
```

A da CE (`ThreeDScene(camera_class=ThreeDCamera, ambient_camera_rotation=None,
default_angled_camera_orientation_kwargs=None)`) não faz nada disso: ela troca a
classe de câmera e oferece `set_camera_orientation`/`move_camera`/
`add_fixed_in_frame_mobjects`. **Herdar de `ThreeDScene` significa coisas
diferentes nos dois motores**, e um porte que só troca o import herda o
comportamento errado sem erro nenhum.

### 10.9 O procedimento de porte, em ordem

1. **Decida o sentido pela feature, não pelo gosto.** Precisa de `Table`,
   `Graph`, `ease_out_*`, seções, lote, `mx`? → CE. Precisa de embed,
   `checkpoint_paste`, janela? → GL.
2. `grep` nos nomes que só existem de um lado (§10.3). Cada acerto é uma decisão,
   não uma substituição.
3. `grep -nE '\b(Circle|Arc|AnnularSector|Cube|FadeIn)\(' arquivo.py` e **passe
   tudo por palavra-chave** (§10.4).
4. `grep -nE '\.set_(width|height|depth)\(' arquivo.py` (§10.7).
5. `grep -nE 'rate_func\s*=\s*ease_' arquivo.py` — se for GL→CE, tudo bem; se for
   CE→GL, cada um desses é um `NameError` (§10.5).
6. Câmera: `self.frame` ↔ `MovingCameraScene`/`ThreeDScene` (§10.6).
7. `CONFIG = {...}` (dicts do manim pré-2021) → argumentos de `__init__` nos
   **dois** motores. Nenhum dos dois lê `CONFIG` hoje.
8. `self.play(mob.metodo, arg)` — o idioma antigo do 3b1b — **está morto nos
   dois**: `prepare_animation` (`animation/animation.py:237-244`) aceita só
   `Animation` ou `_AnimationBuilder` e levanta
   `TypeError: Object … cannot be converted to an animation`. Use `.animate`.
9. Confira o nome no índice antes de escrever:
   `bin/mx find <Nome> --package manimgl` e `--package manim-ce` (§12).
10. Renderize barato e **olhe o PNG**: `bin/manimgl -ws` no GL,
    `bin/mx render … --format png` na CE.

---

## 11. O que só existe no ManimGL e vale saber que existe

Não é catálogo completo — é a lista do que muda uma decisão.

### 11.1 `time_span`: agendar uma animação dentro do `play`

```python
# animation/animation.py:29 e :68-70
Animation(mobject, run_time=1.0, time_span=(start, end), lag_ratio=0,
          rate_func=smooth, name="", remover=False,
          final_alpha_value=1.0, suspend_mobject_updating=False)
```

`time_span=(0.5, 2.0)` faz a animação acontecer **entre 0,5 s e 2,0 s** do
`play`, e o `begin()` estica o `run_time` para caber (`run_time = max(end,
run_time)`). Coreografia de várias animações com tempos diferentes vira uma
linha, sem `AnimationGroup` aninhado nem `lag_ratio` calculado na mão. A CE não
tem isso: lá é `AnimationGroup(..., lag_ratio=…)` ou `Succession` com `Wait`.

### 11.2 `play()` aceita os parâmetros de ritmo direto

```python
# scene.py:568-585
def play(self, *proto_animations, run_time=None, rate_func=None, lag_ratio=None)
```

`self.play(FadeIn(a), FadeIn(b), run_time=2, lag_ratio=0.3)` aplica os três a
**todas** as animações do `play` (`anim.update_rate_info(...)`). Na CE isso vai
em cada animação. Detalhe: `update_rate_info` usa `or`
(`self.run_time = run_time or self.run_time`), então **`run_time=0` é ignorado**.

### 11.3 `SCENES_IN_ORDER`

Uma lista no topo do módulo substitui a descoberta automática de cenas
(`extract_scene.py:116-117`). É o gancho para dizer "estas cenas, nesta ordem" —
inclusive para `-a`.

### 11.4 `--subdivide`, `inserts/` e a gravação por bloco

Ver §5.4 e §8.1. O GL tem duas maneiras nativas de sair com **um arquivo por
trecho**, enquanto na CE isso é construído com `next_section` + mixin
(`manim-presentation-parts`).

### 11.5 Colormaps

`get_color_map(name)`, `get_colormap_list(map_name="viridis", n_colors=9)`,
`get_colormap_from_colors(colors)` e a constante `COLORMAP_3B1B`
(`['#1C758A', '#83C167', '#FFFF00', '#FC6255']`). Junto com
`Mobject.set_color_by_rgba_func` / `set_color_by_xyz_func`, é como o 3b1b pinta
superfície e campo por valor. A CE não tem colormap nomeado
(`manim-color-theming` é a dona do assunto cor do lado de lá).

### 11.6 Widgets e eventos — uma UI dentro da cena

`manimlib.mobject.interactive` traz `ControlPanel`, `LinearNumberSlider`,
`ColorSliders`, `Checkbox`, `Textbox`, `Button(mobject, on_click)`,
`EnableDisableButton`, todos sobre `ControlMobject(value, *mobjects)`. Por baixo
há um sistema de eventos de verdade: `EventDispatcher`, `EventType`,
`EventListener`, e os métodos `Mobject.add_mouse_press_listner(...)`,
`add_key_press_listner(...)`, `clear_event_listners()` — **sim, "listner", o erro
de digitação está na biblioteca**, inclusive no nome do módulo
(`manimlib.event_handler.event_listner`).

Isso só faz sentido com janela: num `-w` não há mouse. É ferramenta de
exploração e de aula ao vivo, não de vídeo.

### 11.7 Mobjects que só existem aqui

`GlowDot`/`GlowDots` (ponto com halo, marca registrada do canal), `TracingTail`
(rastro que desvanece: `TracingTail(mob, time_traced=1.0, stroke_width=(0,3))`),
`Bubble`/`SpeechBubble`/`ThoughtBubble` (balões com `content=`), `DieFace(value)`,
`Checkmark`/`Exmark`, `Clock`/`ClockPassesTime`, `Speedometer`, `Dartboard`,
`Piano`/`Piano3D`, `Laptop`, `VideoSeries`, `NewtonFractal`/`MandelbrotFractal`/
`JuliaFractal`, `Prismify(vmobject, depth)`, `VCube`, `VPrism`, `VGroup3D`,
`SurfaceMesh`, `TexturedSurface`, `TimeVaryingVectorField`, `AnimatedStreamLines`,
`ExponentialValueTracker`, `MotionMobject`.

E as animações: `VFadeIn`/`VFadeOut`/`VFadeInThenOut` (que animam **opacidade**
sem trocar o mobject, ao contrário do `FadeIn`), `FlashAround`, `FlashUnder`,
`VShowPassingFlash`, `ShowCreationThenDestruction`, `ShowCreationThenFadeAround`,
`TurnInsideOut`, `CountInFrom`, `TransformMatchingStrings`,
`TransformMatchingParts`.

### 11.8 Material, sombreamento e profundidade

`Mobject.set_shading(reflectiveness, gloss, shadow)`, `set_gloss`, `set_shadow`,
`apply_depth_test()`, `set_clip_plane(...)`, `set_flat_stroke(False)` e a classe
`Material` do renderer. É o que dá ao 3D do GL aquela aparência que a `Surface`
da CE não tem de graça. Cena 3D no GL herda de `ThreeDScene`, que já liga
`samples = 4` e depth test em tudo que entra (§10.8).

---

## 12. Descobrir a API do GL sem chutar

O índice do ManimGL já está em disco e custa milissegundos. **Assinatura que
você não conferiu não entra no código** — a regra é a mesma da CE
(`manim-project §2`), só muda o `--package`.

```bash
bin/mx find ShowCreation --package manimgl      # existe no GL
bin/mx find ShowCreation --package manim-ce     # nada, exit 1
bin/mx show CameraFrame  --package manimgl      # assinatura + métodos
bin/mx api-diff                                  # regenera api/ce-vs-gl.md
bat api/ce-vs-gl.md
```

O default de `--package` é `manim-ce` (`manimx/cli.py:492, 500`). **Esquecer o
`--package manimgl` faz você conferir a biblioteca errada** e concluir que um
símbolo do GL não existe.

Direto nos TSV, quando quiser varredura:

```bash
cd /home/ondokai/Projects/manim/api

# assinatura de uma classe do GL
awk -F'\t' '$2=="Circle"' manimgl-index.tsv

# tudo de uma categoria (as 29 categorias do GL)
awk -F'\t' '$3=="animation/indication"{print $1, $2}' manimgl-index.tsv

# os métodos PRÓPRIOS de uma classe do GL (coluna 5 = herdado)
awk -F'\t' '$1=="CameraFrame" && $5=="0"{print $2, $6}' manimgl-methods.tsv

# um nome existe em qual edição?
grep -Pc "\tShowCreation\t" manimgl-index.tsv manim-ce-index.tsv
```

Composição do índice do GL: **270 classes, 217 funções, 754 constantes**, 704
nomes no `from manimlib import *`, 29 categorias. As maiores: `mobject/core`
(250), `other` (219), `constants` (117), `mobject/svg` (115), `utils/other` (74),
`renderer` (61).

Receitas mais fundas de `awk`, homônimos, herança e o conferidor estático:
**`manim-api-discovery`** — ela cobre os dois pacotes.

### 12.1 Como o GL escolhe o que é "cena" (e o mixin que se esconde)

```python
# extract_scene.py:28-36
def is_child_scene(obj, module):
    return (inspect.isclass(obj) and issubclass(obj, Scene)
            and obj != Scene
            and obj.__module__.startswith(module.__name__))
```

Duas notas para quem vem do padrão de cena em partes:

- **um mixin que NÃO herda de `Scene` é invisível** aos dois descobridores — o do
  GL acima e o de `manimx/render.py:142-145`. É o que sustenta o formato de
  `manim-presentation-parts`;
- mas o GL usa `startswith`, não `==`. Uma classe importada de um submódulo cujo
  nome comece com o do módulo **aparece** na lista do GL e não apareceria na da
  CE. Diferença pequena e silenciosa.

---

## 13. Armadilhas verificadas

| Sintoma | Causa | Correção |
|---|---|---|
| `ModuleNotFoundError: manimlib` | rodou com `bin/manim`/`mx` | `bin/manimgl`; os venvs não se visitam (§3.3) |
| `FileNotFoundError: dvisvgm` na primeira `Tex` | chamou `.venv-gl/bin/manimgl` direto | `bin/manimgl` — o wrapper põe o TinyTeX no PATH (§9.1) |
| o comando fica parado sem imprimir nada | arquivo com >1 cena e sem nome de cena → `input()` | passe o nome, ou `-a` (§4.3) |
| `unrecognized arguments` antes de qualquer coisa sua | `--log_level`/`--clear_cache` com underscore; **ou** um script que importa `manimlib` com CLI própria | hífen nessas duas; `sys.argv = [sys.argv[0]]` antes do import (§3.1, §4.1) |
| `self.embed()` "não abriu nada" | havia `-w`/`-o`/`--finder`: sem janela, `embed` é no-op | rode sem `-w` (§5.1) |
| o código depois do `self.embed()` nunca roda | `embed()` levanta `EndScene` ao sair | `self.embed(close_scene_on_exit=False)` (§5.1) |
| fundo cinza em vez do preto do projeto | rodou de outro diretório: sem `custom_config.yml`, o default do master é `#333333` | rode da raiz, ou `--config_file "$PWD/custom_config.yml"` (§7.1) |
| o preview parece mais duro que o mp4 | com janela, o FPS é forçado a 30 | é esperado; só o `-w` respeita `--fps` (§6.4) |
| `-t` saiu sem canal alfa | o wrapper injetou `--vcodec h264_nvenc`, que vence o `-t` | `--vcodec prores_ks` **e** `--pix_fmt yuva444p10le` — só o codec não devolve o alfa (§8.3) |
| `-i` (gif) falhou ou saiu estranho | idem: `--vcodec` injetado vence o `-i` | `--vcodec ""` (§8.3) |
| `crf` definido e o arquivo saiu com outra qualidade | `-crf` não existe em NVENC, e `-loglevel error` engole o aviso | use `libx264` para `crf`; em NVENC o parâmetro seria `cq` (§8.2) |
| `Circle(2)` virou um arco esquisito | no GL o 1º posicional de `Circle` é `start_angle` | `Circle(radius=2)`; passe tudo por palavra-chave (§10.4) |
| `NameError: ease_out_expo` | o GL só tem 15 `rate_function` | §10.5 |
| `TypeError: Object … cannot be converted to an animation` | `self.play(mob.metodo, arg)`, idioma morto | `.animate` (§10.9) |
| `Ctrl+Shift+Z` desfaz em vez de refazer | cadeia `elif` com `CTRL_OR_CMD` casando antes | **`Shift+Z`** (sem Ctrl) — ou `redo()` no REPL (§6.5) |
| dois renders GL em paralelo estragam a `Tex` | `working.tex` de nome fixo | um de cada vez (§9.2) |
| `Adapter with name 'NVIDIA' not found.` | `WGPUPY_WGPU_ADAPTER_NAME=NVIDIA` é filtro **duro** do wgpu-py, exportado pelo wrapper quando `nvidia-smi` responde | driver caiu ou pede reboot: liste os adapters (§14) e, em último caso, `WGPUPY_WGPU_ADAPTER_NAME= bin/manimgl …` |
| o mp4 não está em `media/` | a saída do GL é `media-gl/videos/` (§8.1) | |
| não consigo capturar o caminho num script | o `manimgl` não tem `--json` | `--file_name` e monte o caminho (§8.1) |
| `checkpoint_paste()` levanta `PyperclipException` | sessão sem backend de clipboard | instale `xclip`/`wl-clipboard` (aqui os três existem, §5.3) |
| `mirror_module_path: True` estoura com `TypeError` | falta `removed_mirror_prefix` no YAML | defina a chave (§7.2) |
| `-p` com `-w` fica girando para sempre | presenter mode espera tecla e não há janela | `-p` só sem `-w` (§4.4) |
| a `Tex` sumiu, sem erro | o GL não confere o retorno do `dvisvgm`: SVG vazio → mobject sem pontos | rode o `dvisvgm` na mão sobre `media-gl/latex_cache/working.dvi` (§9.1) |
| texto saiu monoespaçado sem você pedir | `text.font` do GL é **`Consolas`** | defina `font=` ou mude o YAML (§7.2) |

---

## 14. Diagnóstico do wgpu/Vulkan

Não existe `vulkaninfo` nesta máquina — **não o cite**. O diagnóstico real é
listar os adapters de dentro do venv do GL:

```bash
.venv-gl/bin/python -c "
import wgpu
for a in wgpu.gpu.enumerate_adapters_sync(): print(a.summary)"
```

Saída registrada nesta máquina (`manim-gpu-encoding §10`): Intel integrada,
NVIDIA RTX 4070 discreta e `llvmpipe` (CPU), todas via Vulkan.

`bin/mx gpu` imprime `Adapters wgpu : -` **sempre**, e é falso-negativo:
`manimx.gpu.wgpu_adapters()` faz `import wgpu` dentro do venv da **CE**, que não
tem o pacote. Isso não diz nada sobre o Vulkan.

O ManimGL pede `power_preference="high-performance"` e cai na dGPU sozinho; o
wrapper ainda fixa `WGPUPY_WGPU_ADAPTER_NAME=NVIDIA` quando `nvidia-smi`
responde (`bin/manim-env.sh:56-68`). Como esse nome é filtro duro, é a única
variável capaz de **quebrar** o `manimgl` num ambiente que funcionaria: se a
NVIDIA sumir da lista, o processo aborta em vez de cair na Intel.

---

## 15. Fronteiras — o que NÃO é desta skill

| Assunto | Skill dona |
|---|---|
| escolher motor, wrappers, ambiente, roteamento geral | `manim-project` |
| NVENC, codec, peso, SSIM, `mx bench`, PRIME | `manim-gpu-encoding` (§10 dela cobre o encoding do GL) |
| achar classe/assinatura, os TSV em profundidade | `manim-api-discovery` |
| desenhar, posicionar e agrupar na **CE** | `manim-mobjects`, `manim-layout-posicionamento` |
| animar na **CE**, `rate_func`, composição | `manim-animations`, `manim-composicao-ritmo` |
| `Text`/`Tex` da **CE**, `t2c`, TinyTeX, nitidez do glifo | `manim-text-latex` (+ `manim-project` §10.5) |
| cena cortada em partes para slide | `manim-presentation-parts` |
| render em lote e CI | `manim-batch-pipeline` |
| `mx render`, qualidade, formato, cache da CE | `manim-render-api` |
| traceback e bissecção de falha | `manim-troubleshooting` |
| câmera 3D e 2D **da CE** | `manim-3d-camera`, `manim-camera-2d` |
| o deck de aulas que consome tudo isso | repo `~/Projects/aulas`, skills `aula-videos` / `aula-slides` |

**Buracos declarados**, para não improvisar: o renderer wgpu por dentro
(`Renderer`, `Shader`, `PipelineState`, `SharedBuffer`, `Material`,
`RenderPass`) não tem skill nenhuma, nem aqui nem na CE; e o
`manimlib.event_handler` só é descrito na superfície da §11.6.

---

## 16. Checklist antes de dizer "está rodando no ManimGL"

```bash
# 1. é o master wgpu, e não o wheel OpenGL?
bin/mx doctor | grep manimgl                      # -> 1.7.2 wgpu/Vulkan

# 2. está usando o wrapper? (senão a primeira Tex morre em dvisvgm)
type bin/manimgl

# 3. você está no diretório que tem o custom_config.yml?
ls custom_config.yml || echo "vai sair cinza, 30fps, em ./videos"

# 4. o nome da cena está na linha de comando? (senão ele PERGUNTA)
grep -nE '^class .*\(.*Scene' arquivo.py

# 5. olhou o frame antes de gastar o render inteiro?
bin/manimgl -ws arquivo.py Cena      # PNG do último frame, headless
```

E o passo que não é comando: **olhe o PNG.** Texto branco em fundo branco,
elemento cortado pela borda, sobreposição e contraste ruim não dão erro no
terminal em motor nenhum — e o ManimGL, com `default_mobject_color: #FFFFFF` e
`default_stroke_color: #DDDDDD`, é ainda mais fácil de perder em fundo claro que
a CE.

---

## 17. O que ficou NÃO VERIFICADO nesta rodada

A proibição de CPU/GPU vigente impediu qualquer render, benchmark ou abertura de
janela. Está marcado no texto, e repetido aqui para quem for continuar:

1. **§3.2** — que `-r 1080x1920` redimensiona o palco do GL para 4,5 × 8,0. A
   cadeia de import (`config.py:399` → `constants.py:13-20`) é fonte lida; o
   resultado no arquivo não foi observado. **Confira com um `-ws` e um
   `FullScreenRectangle`.**
2. **§4.4** — `-p` com `-w` como laço infinito.
3. **§6.5** — que `Shift+Z` e `Shift+G` alcançam `redo`/`ungroup`. A cadeia
   `elif`, os bits de `Mods` e a normalização de `to_key` são fonte lida;
   ninguém apertou a tecla.
4. **§7.2** — o `TypeError` de `mirror_module_path: True`.
5. **§8.2** — que o ffmpeg emite o aviso de `-crf` inútil em nível *warning*
   (o `-loglevel error` que o esconderia é fonte lida; o nível do aviso, não).
6. **§8.3** — os dois comandos `-t` e `-i` com a injeção do wrapper. O mecanismo
   (cadeia `elif` + `bin/manimgl:20-31`) é fonte lida; a saída não foi produzida.
7. **§9.5** — a comparação numérica de nitidez GL × CE. O que está conferido é o
   mecanismo (`font_size * 1024` no GL contra `font_size / 4.8` na CE) e o canvas
   fixo de 16384. **Ninguém mediu erro de avanço de glifo no GL.** Quem for medir,
   use a métrica direcional descrita em `manim-text-latex` — o desvio-padrão de
   par repetido é cego para esse defeito.
8. Nada de tempo de render, peso de arquivo ou sessão NVENC foi medido aqui;
   esses números são de `manim-gpu-encoding`, que é a dona.
