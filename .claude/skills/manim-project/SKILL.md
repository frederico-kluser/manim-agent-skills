---
name: manim-project
description: >-
  Ponto de ENTRADA deste projeto Manim: o mapa do repositório, os dois motores
  instalados (ManimCE 0.21.0 e ManimGL 1.7.2 wgpu/Vulkan), os wrappers de `bin/`,
  o contrato do CLI `mx`, e o ROTEAMENTO para as outras 26 skills. Use SEMPRE
  que a tarefa envolver Manim, mesmo sem a palavra: "faz um vídeo explicando X",
  "anima essa fórmula", "gera uma animação disso", "renderiza essa cena", "cria
  um Mobject", "quero um vídeo vertical pro Shorts", "monta um gráfico animado",
  "põe uma imagem/SVG na cena", "quebra esse vídeo em partes pro slide", "o
  ambiente do Manim está ok?", "por que o vídeo saiu vazio?", "qual skill eu uso
  pra isso?", "onde eu ponho o arquivo da cena?", "monta o tema do projeto",
  "não sei por onde começar". Cobre o que quebra CALADO nesta máquina —
  `dvisvgm` fora do PATH, OpenGL caindo na Intel, `manim.cfg` que só vale se
  você rodar da raiz, `--codec av1` que grava libx264, `-r 1080x1920` que não
  mexe no palco, fonte ausente virando Noto Sans, `--theme` aplicado DEPOIS do
  import da cena, `mx doctor` que sai 0 mesmo com o LaTeX quebrado, o cairo
  arredondando a posição de cada glifo — e a regra de cor verdadeira
  (`#` obrigatório; hex de 3 dígitos FUNCIONA). Leia esta ANTES das outras.
  NÃO use para o assunto em si — ela roteia, não ensina: renderizar em detalhe é
  `manim-render-api`; achar classe/assinatura é `manim-api-discovery`; desenhar é
  `manim-mobjects`; enquadrar é `manim-layout-posicionamento`; animar é
  `manim-animations`; ritmo é `manim-composicao-ritmo`; conferir o que saiu é
  `manim-verificacao-visual`; falha concreta com traceback é
  `manim-troubleshooting`.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Projeto Manim — o mapa, os wrappers e o roteamento

Este repositório é um ambiente Manim pronto para uso, com uma camada de API
(`manimx`) desenhada para agentes. **Nada aqui precisa de instalação adicional.**

Esta skill é a portaria. Ela responde a três perguntas — *onde estão as coisas*,
*como se dispara o Manim sem quebrar nada*, e *qual das 26 skills irmãs resolve o
seu pedido* — e não a quarta (*como se faz o desenho*), que é sempre de outra.

## Como ler as marcas de verificação

Este projeto já perdeu tempo com número que envelheceu sem avisar. Por isso toda
afirmação abaixo carrega uma origem:

| Marca | O que significa |
|---|---|
| **[MEDIDO]** | rodado nesta máquina em **2026-08-19**, com o comando ao lado |
| **[FONTE]** | lido no código-fonte instalado (`.venv/…/manim/`, `manimx/`, `bin/`) ou no índice `api/`. Não executado, mas é afirmação forte |
| **[DECK]** | medido pelo projeto consumidor `~/Projects/aulas`, não reproduzido aqui. Testemunho confiável, não re-verificado |
| **[NÃO VERIF.]** | plausível, sem prova. Confirme antes de depender |

> **Ambiente das medições:** Pop!_OS 24.04, i9-14900HX 32 threads, RTX 4070
> Laptop 8188 MiB, driver 580.159.03 / CUDA 13.0, Python 3.12.3.
> Número sem comando ao lado não entra aqui — foi assim que a versão anterior
> desta skill envelheceu errada.

---

## 1. Cartão de referência — os dez subcomandos do `mx`

```bash
bin/mx doctor                     # o ambiente inteiro está de pé?   (~1,8 s)
bin/mx gpu                        # placa, driver, encoders do PyAV  (~2,8 s)
bin/mx find "bar chart"           # que classe faz isso?             (~0,2 s)
bin/mx show Axes                  # assinatura + 100% dos métodos    (~0,3 s)
bin/mx scenes arquivo.py          # que cenas esse arquivo expõe?    (~0,9 s)
bin/mx presets                    # qualidades, codecs, temas reais  (~0,1 s)
bin/mx render arquivo.py Cena -q h --codec nvenc --json    # o mp4
bin/mx api-dump                   # regenera api/manim-ce-*
bin/mx api-diff                   # regenera api/ce-vs-gl.md
bin/mx bench                      # CPU × GPU nesta máquina — CARO, ver §13
```

**[MEDIDO]** com `/usr/bin/time -f "%e" bin/mx <cmd>`, 3 execuções, máquina sob
carga leve: `presets` 0,11–0,12 s · `find` 0,19–0,35 s · `show` 0,20–0,40 s ·
`scenes` 0,86–0,98 s · `doctor` 1,84 s · `gpu` 2,81 s · `python -c "import manim"`
0,54 s.

`show`, `find` e `presets` leem um índice em disco e custam menos que um blink.
**`scenes` custa 4× mais porque IMPORTA o arquivo** — ver §9. Não existe desculpa
de custo para chutar nome de API.

### 1.1 Flags globais funcionam antes E depois do subcomando

**[FONTE]** `manimx/cli.py:428-438`. As duas globais (`--json`, `-v/--verbose`)
vivem num parser-pai com `default=argparse.SUPPRESS`:

```bash
bin/mx gpu --json      # funciona
bin/mx --json gpu      # funciona também
```

O `SUPPRESS` é o detalhe que faz isso: sem ele, o subparser escreveria
`json=False` por cima do `--json` global. Se você acrescentar uma flag global ao
`mx`, copie o `default=argparse.SUPPRESS` ou ela deixa de funcionar na primeira
posição, em silêncio.

### 1.2 Com `--json`, o stdout é só o JSON

**[FONTE]** `manimx/cli.py:35-41`. `_out()` escreve num `_REAL_STDOUT` capturado
antes de qualquer redirecionamento, e o `main()` desvia todo log do Manim (que o
rich manda para o stdout — ex.: *"Output format changed to '.mp4' to support
transparency"*) para o stderr. Consequência prática:

```bash
bin/mx render cena.py Cena --json 2>/dev/null | jq '.[0].output_file'
```

`2>/dev/null` deixa o stdout puro. Nunca parseie sem isso na primeira vez que
um render falhar — o traceback do Manim é longo.

### 1.3 As qualidades e os apelidos que o `-q` aceita

**[FONTE]** `manimx/presets.py:23-38`. Cinco presets, e uma tabela de apelidos que
economiza uma consulta:

| `-q` | resolução | fps | alias interno | também aceita |
|---|---|---|---|---|
| `l` | 854×480 | 15 | `low_quality` | `low`, `480p`, `draft` |
| `m` | 1280×720 | 30 | `medium_quality` | `medium`, `720p` |
| `h` | 1920×1080 | **60** | `high_quality` | `high`, `1080p`, `hd` |
| `p` | 2560×1440 | 60 | `production_quality` | `production`, `1440p`, `2k` |
| `k` | 3840×2160 | 60 | `fourk_quality` | `fourk`, `2160p`, `4k`, `uhd` |

Apelido desconhecido levanta `ValueError` **listando todos os aceitos**
(`resolve_quality`) — leia o erro em vez de adivinhar.

Repare que `h` é o único degrau onde o fps **dobra** (30 → 60). Quem itera em `-q m`
e entrega em `-q h` está trocando duas coisas ao mesmo tempo, não uma.

### 1.4 Os dez codecs do `--codec`

**[FONTE]** `manimx/presets.py:57-125`. Só existem estes; qualquer outro nome é erro.

| `--codec` | motor | o que é |
|---|---|---|
| `x264` | CPU | padrão do Manim. libx264 crf 23. Compatibilidade total |
| `nvenc` | **GPU** | h264_nvenc, perfil `balanced`. **Default do `mx render`** |
| `nvenc-fast` | GPU | preset p1. Iteração/preview, **não** entrega |
| `nvenc-quality` | GPU | p7 + AQ espacial/temporal. Entrega final |
| `hevc` | GPU | hevc_nvenc, ~30% menor, menos compatível |
| `av1` | GPU | **INDISPONÍVEL nesta build** — cai em libx264, ver §10.2 |
| `transparent` | CPU | qtrle RGBA em `.mov`. NVENC não faz alfa |
| `webm` | CPU | libvpx-vp9. NVENC não faz VP9 |
| `gif` | CPU | paleta por `palettegen`/`paletteuse` |
| `png` | — | só o último frame (equivale a `-s`) |

A escolha entre eles, com tempo × peso × qualidade medidos: **`manim-gpu-encoding`**,
que é a dona do assunto. Aqui está só a lista, para você não inventar um nome.

---

## 2. A regra de ouro: assinatura que você não conferiu não entra no código

As duas edições do Manim divergiram e metade dos tutoriais da internet descreve
uma API que não existe mais. Nome de método inventado custa um render inteiro e
só aparece no fim.

```bash
bin/mx find <termo>          # busca por nome, docstring E nome de método
bin/mx show <Classe>         # assinatura, bases, propriedades, métodos herdados
```

**[MEDIDO]** `bin/mx show Circle` devolve **4 métodos próprios e 260 herdados** — a
herança é onde mora quase tudo que você quer chamar, e é o que nenhuma memória
cobre.

**`mx find` busca em INGLÊS.** O índice guarda os nomes e docstrings da
biblioteca, que são em inglês. **[MEDIDO]**, e custa tempo:

```
$ bin/mx find barra -n 3          →  (nada)          exit 1
$ bin/mx find "bar chart" -n 3    →  class BarChart  mobject/graphing
```

Nada encontrado sai **sem imprimir nada e com exit 1** — um `mx find ... | grep`
displicente lê isso como "não existe". Traduza o termo antes de concluir.

**`mx find` trunca em 30 por padrão** (`-n/--limit`, `cli.py:495`). Uma busca larga
(`mx find color --kind class` dá 209 resultados) mostra 30 e não avisa que cortou.

Aprofundamento — as receitas de `awk` sobre os TSV, a introspecção ao vivo, o
conferidor estático de cena, a varredura de kwargs pelo MRO, como regenerar o
índice: **`manim-api-discovery`**, que é a skill mais precisa do conjunto.

---

## 3. Os wrappers de `bin/` — e a prova de que eles importam

| Wrapper | O que roda | O que ele conserta |
|---|---|---|
| `bin/mx` | `.venv/bin/python -m manimx.cli` | camada de API + LaTeX + GPU + venv |
| `bin/manim` | `.venv/bin/manim` (CLI cru da CE) | TinyTeX no PATH + PRIME offload |
| `bin/manimgl` | `.venv-gl/bin/manimgl` | idem + injeta `--vcodec h264_nvenc` |
| `bin/setup` | bootstrap | idempotente; **faz `cd` para a raiz sozinho** |

Os três primeiros fazem `source bin/manim-env.sh`. O comentário do arquivo diz
que ele resolve três coisas; **[FONTE]** lendo o script inteiro, são **cinco**.

### 3.1 LaTeX: o que falta no PATH é o `dvisvgm`, não o `latex`

Uma versão anterior desta skill dizia "sem o wrapper o `latex` não é encontrado".
**Está errado nesta máquina, e a skill `manim-troubleshooting` ainda carrega uma
variante do mesmo erro** (ela manda `tlmgr install dvisvgm`, que não resolve nada
aqui — o binário já está instalado).

**[MEDIDO]** `~/.local/bin` tem **78 symlinks para o TinyTeX**, e `latex` é um
deles. `dvisvgm` **não é**:

```
$ ls -la ~/.local/bin | grep -c TinyTeX        →  78
$ ls -la ~/.local/bin/latex                    →  → ~/.TinyTeX/bin/x86_64-linux/latex
$ ls -la ~/.local/bin/dvisvgm                  →  No such file or directory
$ ls ~/.TinyTeX/bin/x86_64-linux/ | grep dvisvgm  →  dvisvgm      ← existe lá
```

O binário está instalado; o que falta é **o symlink**. O sintoma real, reproduzido
com `MathTex` num PATH limpo:

```
FileNotFoundError: [Errno 2] No such file or directory: 'dvisvgm'
```

O `manim-env.sh` põe `~/.TinyTeX/bin/x86_64-linux` **inteiro** à frente do PATH, e
aí os dois aparecem. **A falha é no fim do pipeline** (o `.dvi` compila, a conversão
para SVG é que morre), então o traceback fala de `subprocess`, não de LaTeX — e é
por isso que o erro engana.

Confirmação programática sem render, **[FONTE]** `api/manim-ce-index.tsv` +
`manim/cli/checkhealth/checks.py:189`:

```python
from manim.cli.checkhealth.checks import is_dvisvgm_available   # () -> bool
```

**Correção.** Uma versão anterior desta skill escrevia
`from manim.utils.tex_file_writing import ...` — esse módulo **não** define a
função, e a linha levanta `ImportError`. O índice sempre disse o certo:
`awk -F'\t' '$2=="is_dvisvgm_available"' api/manim-ce-index.tsv` devolve
`manim.cli.checkhealth.checks`. É a §2 desta skill se aplicando a ela mesma.

O `manim-env.sh` também tenta, em ordem, `~/.TinyTeX/bin/x86_64-linux`,
`~/.TinyTeX/bin/universal-darwin` e `/usr/local/texlive/2026/bin/x86_64-linux`,
e para no primeiro que existir — o script é portátil, a máquina é que não.

### 3.2 GPU: sem PRIME offload, o OpenGL cai na Intel — em silêncio

Notebook híbrido. **[MEDIDO]** com `glxinfo -B` num ambiente limpo:

```
sem offload : OpenGL renderer string: Mesa Intel(R) Graphics (RPL-S)
com offload : OpenGL renderer string: NVIDIA GeForce RTX 4070 Laptop GPU/PCIe/SSE2
```

`manimx_enable_gpu` exporta `__NV_PRIME_RENDER_OFFLOAD=1`,
`__GLX_VENDOR_LIBRARY_NAME=nvidia`, `__VK_LAYER_NV_optimus=NVIDIA_only` e
`WGPUPY_WGPU_ADAPTER_NAME=NVIDIA`.

**Tudo isso é condicional a existir uma NVIDIA**, e o motivo está comentado no
próprio script: o `wgpu-py` trata `WGPUPY_WGPU_ADAPTER_NAME` como **filtro DURO**
(`raise ValueError(f"Adapter with name '{adapter_name}' not found.")`), então
exportá-la cegamente faria o `manimgl` abortar em qualquer máquina sem placa.

Chamar `.venv/bin/manim --renderer=opengl` direto renderiza na Intel sem uma linha
de aviso. Detalhe importante: **[FONTE]** `manimx/render.py:390` monta o ambiente
de PRIME **antes** de criar o contexto GL — depois disso, exportar a variável não
adianta mais.

### 3.3 Venv, `PYTHONPATH` e `PYTHONWARNINGS` — as duas coisas que ninguém conta

**[FONTE]** `bin/manim-env.sh`, funções `manimx_use_ce` / `manimx_use_gl`:

```bash
export VIRTUAL_ENV="$MANIMX_ROOT/.venv"          # ou .venv-gl
export PATH="$VIRTUAL_ENV/bin:$PATH"
export PYTHONPATH="$MANIMX_ROOT${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONWARNINGS="${PYTHONWARNINGS:-ignore::SyntaxWarning}"
```

Duas consequências que valem ouro:

1. **`PYTHONPATH` inclui a raiz do repositório.** É por isso que `import manimx`
   funciona de qualquer cwd **quando você passou por um wrapper** — e por isso que
   um script rodado com `.venv/bin/python` cru pode não achar `manimx`.
2. **`PYTHONWARNINGS=ignore::SyntaxWarning`** silencia um `SyntaxWarning` do
   `pydub` (dependência transitiva) que polui todo stderr. Se você depurar
   parseando stderr e "sumiu um warning", foi isto.

### 3.4 A armadilha do `.venv/bin/mx`

O `pyproject.toml` declara `[project.scripts] mx = "manimx.cli:main"`, então
**existe um `.venv/bin/mx` que NÃO é o wrapper**. Ele roda, e mente. **[MEDIDO]**:

```
$ env -i PATH="$HOME/.local/bin:/usr/bin:/bin" HOME=$HOME .venv/bin/mx doctor
[aviso] dvisvgm                não encontrado no PATH
[OK   ] LaTeX → SVG (MathTex)  compila e converte
Ambiente pronto.                        ← exit 0
```

Duas linhas contraditórias, e a boa é a errada — ver §4.3. **Sempre `bin/mx`.**

### 3.5 Duas armadilhas de shell que o próprio wrapper documenta

Valem para qualquer script novo em `bin/`, e estão comentadas no `manim-env.sh`
porque já custaram um diagnóstico errado:

1. **`produtor | grep -q` sob `set -o pipefail` mente.** O `grep -q` sai assim que
   acha, o produtor morre de `SIGPIPE`, e sob `pipefail` o pipeline inteiro vira
   falso — *mesmo com a GPU presente*. Por isso `manimx_has_nvidia` captura numa
   variável primeiro (`listing="$(nvidia-smi -L)"`) e testa depois, com `case`.
2. **Materialize a saída antes de filtrar.** `comando | grep x || echo ok`
   transforma **falha do comando** em "ok". A mesma lição aparece do lado
   consumidor **[DECK]**, onde um `--aula` obrigatório passou despercebido dentro
   de um pipe exatamente assim.

---

## 4. `mx doctor` — e o que ele NÃO diz

```bash
bin/mx doctor          # legível
bin/mx doctor --json   # {"ok": bool, "checks": [{check, ok, detail, fatal}, …]}
```

**[MEDIDO]**, saída de hoje: 10 checks, todos OK, `"ok": true`.

```
[OK] python >= 3.11  3.12.3          [OK] latex     ~/.TinyTeX/bin/x86_64-linux/latex
[OK] manim (CE)      v0.21.0         [OK] dvisvgm   ~/.TinyTeX/bin/x86_64-linux/dvisvgm
[OK] PyAV + libx264  PyAV 18.1.0     [OK] ffmpeg    /usr/bin/ffmpeg
[OK] NVENC (h264_nvenc) disponível   [OK] LaTeX → SVG (MathTex)  compila e converte
[OK] manimgl         1.7.2 wgpu      [OK] Pango (Text)           ok
```

Existe um **11º check condicional**, `manim atualizado`, que só é acrescentado se
o ManimCE resolvido for **< 0.20** — nesta máquina ele nunca aparece.

### 4.1 Só QUATRO checks derrubam o exit code — e não são os que você imagina

**Esta é uma correção.** A versão anterior desta skill dizia **cinco**, e incluía
`LaTeX → SVG (MathTex)` na lista. **Está errado**, e a leitura do fonte prova.

**[FONTE]** `manimx/cli.py:173` — o veredito é
`failed_fatal = [c for c in checks if not c["ok"] and c["fatal"]]`. Um check só
conta se estiver **reprovado E marcado como fatal**. Agora olhe o registro do
check de LaTeX (`cli.py:122-137`):

```python
try:
    with tempconfig({"verbosity": "CRITICAL"}):
        MathTex(r"x^2")
    add("LaTeX → SVG (MathTex)", True, "compila e converte")     # fatal=True (default)
except Exception as exc:
    add("LaTeX → SVG (MathTex)", False,
        f"{type(exc).__name__}: {str(exc)[:200]}",
        fatal=False)                                             # ← fatal=False AO FALHAR
```

O check nasce fatal **quando passa** e não-fatal **quando falha**. Como o filtro
exige as duas condições, **um LaTeX quebrado nunca muda o exit code**.

O conjunto real de checks que podem fazer `bin/mx doctor` sair ≠ 0:

| Check | Fatal ao falhar? |
|---|---|
| `python >= 3.11` | **sim** |
| `manim (CE)` | **sim** |
| `PyAV + libx264` | **sim** |
| `Pango (Text)` | **sim** |
| `NVENC (h264_nvenc)` | não |
| `latex` · `dvisvgm` · `ffmpeg` | não (o laço passa `fatal=False` para os três) |
| `LaTeX → SVG (MathTex)` | **não** (fatal só no caminho de sucesso) |
| `manimgl` | não |
| `manim atualizado` (condicional) | não |

**[MEDIDO]**, e é a demonstração:

```
$ .venv/bin/mx doctor --json | jq '.ok'     # com dvisvgm fora do PATH
true                                         # e exit 0
```

**Regra: leia os `checks`, não o exit code.** Em `--json`, itere a lista e trate
`ok:false` mesmo com `fatal:false`. Um pipeline de CI que confia no exit code
deste comando publica vídeo sem fórmula nenhuma e não percebe.

### 4.2 Como um agente deve consumir o doctor

```bash
bin/mx doctor --json 2>/dev/null \
  | jq -r '.checks[] | select(.ok == false) | "\(.check): \(.detail)"'
```

Vazio = pronto de verdade. Qualquer linha = decida se ela importa para a SUA
tarefa: `manimgl` reprovado é irrelevante se você só vai usar a CE; `dvisvgm`
reprovado condena qualquer cena com `Tex`/`MathTex`.

### 4.3 O check de LaTeX passa em cache

**[MEDIDO]**, e combina com §4.1 para formar a pior armadilha do doctor. O check é
literalmente `MathTex(r"x^2")` (`cli.py:126`). O Manim guarda o SVG resultante em
`{media_dir}/Tex`, com hash do LaTeX — **e o hash não sabe se o `dvisvgm` existe**.
Com o cache quente, o check passa sem tocar no binário:

```
# mesmo PATH sem dvisvgm, dois cwd diferentes
cwd = /tmp (media_dir frio)  → FileNotFoundError [Errno 2] 'dvisvgm'
cwd = raiz do projeto        → MathTex COMPILOU (cache de media/Tex)
```

Junte com §4.1: o check de LaTeX **pode passar por cache** e, quando falha,
**não muda o exit code**. Consequência prática:

> **A linha `dvisvgm` do doctor é mais confiável que a linha `LaTeX → SVG`.**
> Se as duas discordarem, acredite na primeira.

Para forçar um teste frio, aponte o media dir para um lugar vazio:
`bin/mx render … --media-dir /tmp/frio`. Cache em profundidade:
**`manim-performance-cache`**.

### 4.4 Bootstrap num clone limpo

```bash
bin/setup             # ManimCE + manimx (o essencial)
bin/setup --with-gl   # + ManimGL num venv separado, do git (não do PyPI)
bin/setup --with-tex  # + os pacotes LaTeX que o Manim exige, via tlmgr
bin/setup --all       # tudo
bin/setup --help      # imprime as linhas 2–12 do próprio script
```

**[FONTE]** `bin/setup:13-14` — ele faz `cd "$ROOT"` logo no começo. É o **único**
executável de `bin/` que ignora o cwd; os outros três respeitam de onde você
chamou (§5). Argumento desconhecido sai com **exit 2** e mensagem, não com
comportamento surpresa.

Idempotente. Usa `uv` se existir, `venv`+`pip` se não. Ele **exige Python ≥ 3.11**
antes de instalar qualquer coisa, e o motivo está no `pyproject.toml`: num
interpretador velho o pip **não falha** — ele resolve silenciosamente para um
Manim 0.18/0.19 e você descobre depois. O `mx doctor` checa a **versão resolvida**
justamente por isso, não só se o import funcionou.

O `--with-gl` instala do **git**, não do PyPI: o wheel 1.7.2 (dez/2024) ainda é
OpenGL/ModernGL enquanto o master migrou para wgpu/Vulkan — **e os dois se
autodeclaram `1.7.2`**. **[FONTE]** `cli.py:139-171`: só dá para distinguir olhando
se `wgpu` (ou `moderngl`) está instalado no `.venv-gl`, e é exatamente isso que o
doctor faz, num subprocesso.

---

## 5. O `cwd` é parte da configuração — e ninguém avisa

**[MEDIDO]**, e é a descoberta que mais rende. O ManimCE lê `manim.cfg` do
**diretório atual**, não do diretório do script nem da raiz do projeto. E
`bin/mx` **não faz `cd`**: ele só monta o ambiente e dá `exec` a partir de onde
você o chamou.

```bash
# a MESMA cena, o MESMO comando, dois cwd
cd ~/Projects/manim && bin/mx render /tmp/cfg.py Cfg -q l --format png
    →  max_files_cached=200   max_inflight_encoders=4

cd /tmp && ~/Projects/manim/bin/mx render /tmp/cfg.py Cfg -q l --format png
    →  max_files_cached=100   max_inflight_encoders=1
```

Fora da raiz você perde, calado:

| chave | na raiz | fora | consequência |
|---|---|---|---|
| `max_inflight_encoders` | **4** | **1** | encoding paralelo desligado |
| `encoder_queue_size` | 8 | 8 (ignorado) | com 1 encoder a fila não é usada |
| `max_files_cached` | 200 | 100 | poda mais agressiva do cache |
| `media_dir`, `video_dir`, `tex_dir`, `text_dir`… | os do projeto | os defaults | **o mp4 aparece em outro lugar** |
| `quality` / `frame_rate` / `pixel_*` | 1080p60 | os defaults da lib | outra resolução |
| `background_color` | `BLACK` | `BLACK` | igual, por coincidência |
| `notify_outdated_version` | False | True | ruído no stdout |

Nada disso levanta erro. O render sai — só mais devagar, em outra resolução e em
outro lugar.

**Regra: rode `bin/mx` a partir da raiz do projeto**, com caminho absoluto para a
cena se ela morar fora. Se o pipeline precisar rodar de outro cwd, passe as
chaves na mão (`-j 4`, `--media-dir …`, `-q h`) ou use a API Python com
`config_overrides=` (§8.4).

A cadeia de precedência completa está comentada no topo de `manim.cfg`:

```
1. defaults da biblioteca
2. ~/.config/manim/manim.cfg          ([MEDIDO] não existe nesta máquina)
3. ./manim.cfg                        ← do CWD
4. flags da CLI
5. config.<chave> = … no Python / tempconfig(…)
```

**Não existe skill dedicada a essa cadeia** — é um buraco declarado (§13.7),
não um arquivo que falta: nenhum `manim-config-precedencia` existe ou está
planejado. O essencial está aqui; o que sobra está repartido entre
**`manim-tema-projeto`** (config no topo do módulo, `tempconfig`),
**`manim-render-api`** (flag × kwarg × `config_overrides`) e
**`manim-performance-cache`** (as chaves de cache). Para ver o valor efetivo de
qualquer chave:

```bash
bin/manim cfg show          # do cwd atual — o resultado MUDA com o cwd
```

---

## 6. Layout do repositório

```
bin/setup                   bootstrap a partir de um clone limpo (faz cd sozinho)
bin/manim-env.sh            PATH do TinyTeX + PRIME + venv + PYTHONPATH  (sourced)
bin/mx  bin/manim  bin/manimgl
manim.cfg                   config do ManimCE — lido do CWD (§5)
custom_config.yml           config do ManimGL — lido do CWD também
pyproject.toml              manimx 1.0.0, requires-python >=3.11, ruff
manimx/                     a camada de API
  ├─ cli.py                 os 10 subcomandos do `mx`
  ├─ render.py              load_scene_classes, render_scene, render_file, render_many
  ├─ gpu.py                 detect_gpu, enable_nvenc, prime_env, wgpu_adapters
  ├─ presets.py             QUALITY_PRESETS, CODEC_PRESETS, THEMES, apply_theme
  ├─ introspect.py          dump_api — quem gera api/
  ├─ apidiff.py             quem gera ce-vs-gl.md
  └─ bench.py               os 5 cenários do `mx bench`
tools/batch_render.py       lote multi-processo   → manim-batch-pipeline
tools/check_publishable.sh  guarda de publicação  → §15
scenes/exemplos.py          6 cenas de exemplo, testadas — o modelo de estilo
scenes/exemplos_gl.py       exemplos do ManimGL (só pelo bin/manimgl)
api/                        índice COMPLETO, versionado → manim-api-discovery
media/  media-gl/           saída (gitignored)
.venv/                      ManimCE 0.21.0
.venv-gl/                   ManimGL 1.7.2 (git master, wgpu/Vulkan)
```

### 6.1 `api/` é gerado e versionado DE PROPÓSITO

Está escrito no `.gitignore`: é o índice offline que um agente consulta sem
precisar do venv. **É o produto, não um artefato de build.**

**[MEDIDO]** com `stat -c%s`, hoje — 13 arquivos, ~16 MiB:

| Arquivo | Tamanho | Conteúdo |
|---|---:|---|
| `manim-ce-index.tsv` | 528,2 KiB | 5.523 símbolos: kind, name, category, **signature**, module, doc |
| `manim-ce-methods.tsv` | 7.006,2 KiB | 50.945 métodos com `inherited` e `defined_in` |
| `manim-ce-by-category.md` | 585,3 KiB | tudo agrupado nas **41** categorias |
| `manim-ce-toplevel.md` | 35,5 KiB | os **588** nomes do `from manim import *` |
| `manim-ce-inheritance.txt` | 5,9 KiB | a árvore de herança |
| `manim-ce-api.json.gz` | 1.422,9 KiB | o dump bruto |
| `ce-vs-gl.md` | 22,1 KiB | o mapa CE × GL |
| `manimgl-*` (6 arquivos) | 6,4 MiB | o mesmo, do lado GL |

**[MEDIDO]** composição do índice CE (`awk -F'\t'` sobre o TSV): **338 classes,
285 funções, 4.900 constantes, 2.662 nomes únicos**, em **41 categorias**.

Três contagens que se confundem, e a confusão custa:

- **2.662** = nomes distintos no índice, incluindo o que não é reexportado no topo;
- **588** = o que o `from manim import *` realmente traz;
- **4.900** constantes ≠ 4.900 nomes: a coluna `category` conta cada constante
  re-exportada em **toda** categoria onde ela aparece (`DOWN`, `PI`, `BLACK`…).
  Por isso `utils/color` mostra 2.335 linhas mas só **19** classes+funções.

Ao decidir se um assunto "tem matéria", conte **classes + funções**, nunca o total.

### 6.2 `.gitattributes` faz duas coisas que não são cosméticas

**[FONTE]**:

```
bin/*  *.sh  *.py       text eol=lf
api/*.tsv|md|txt|json.gz   linguist-generated=true -diff
.claude/skills/**       linguist-documentation=true
```

O `eol=lf` existe porque num clone Windows com `core.autocrlf=true` os wrappers
virariam CRLF e o bash falharia com `bad interpreter: /usr/bin/env bash^M`. O
`-diff` existe porque ~13 dos ~16 MiB do repositório são índices gerados: sem
ele, todo diff de `api/` polui a revisão inteira.

### 6.3 Onde pôr uma cena nova

`scenes/<assunto>.py`. Um arquivo por assunto, uma docstring de módulo com o
comando de render, e **uma docstring por classe** — **[FONTE]** `cli.py:192-205`,
é a **primeira linha** da docstring que o `mx scenes` imprime ao lado do nome, e é
o único resumo que um agente futuro vai ler antes de abrir o arquivo.

Se a cena for para **slide de palestra**, o layout é outro (mixin + `P1..PN`) e
quem manda é **`manim-presentation-parts`**.

---

## 7. Do zero ao mp4

```bash
cat > scenes/demo.py <<'PY'
from manim import *

class Demo(Scene):
    """Menor cena útil: uma fórmula sendo escrita."""

    def construct(self):
        eq = MathTex(r"e^{i\pi} + 1 = 0", font_size=72)
        self.play(Write(eq))
        self.wait(0.2)
PY

bin/mx render scenes/demo.py Demo -q h --codec nvenc --json
```

**[MEDIDO]**: cena 4,17 s, wall 6,45 s, `h264_nvenc`, 1920×1080@60, 66 KiB de mp4.

### 7.1 O contrato do `--json` — leia isto antes de parsear

```jsonc
[                                   // ← SEMPRE uma LISTA, mesmo com uma cena só
  {
    "scene_name": "Demo",
    "success": true,
    "output_file": "/…/videos/demo/1080p60/Demo.mp4",   // vídeo
    "image_file": null,                                 // PNG
    "sections": [],
    "elapsed_s": 4.17,
    "renderer": "cairo",
    "codec": "h264_nvenc",
    "quality": "h",
    "resolution": [1920, 1080],
    "frame_rate": 60.0,
    "num_animations": 2,
    "error": null,
    "traceback_text": null
  }
]
```

Cinco coisas que só se descobrem rodando ou lendo o fonte:

1. **É uma lista.** `json.load(...)[0]`, sempre. Uma cena só não vira objeto.
2. **`--format png` inverte os campos**: `output_file` fica `null` e o caminho
   está em **`image_file`**. **[MEDIDO]**:
   `"image_file": "/…/images/demo/Demo_ManimCE_v0.21.0.png"`. Quem lê só
   `output_file` acha que o render falhou. Este é, disparado, o erro nº 1 de quem
   escreve pipeline pela primeira vez.
3. **Falha também devolve JSON válido**, em stdout, com exit 1:
   ```
   success: False
   error: AttributeError: Circle object has no attribute 'nao_existe'
   traceback_text: <o traceback inteiro>
   ```
4. **O campo `codec` é uma DEDUÇÃO, não uma leitura do arquivo.** **[FONTE]**
   `manimx/render.py:239-261`, `_effective_codec()` decide por formato e
   transparência (`png`→`png`, `gif`→`gif`, `webm`→`libvpx-vp9`,
   transparente→`qtrle`, senão NVENC ou `libx264`). Ele é honesto sobre a
   INTENÇÃO; para saber o que **de fato** ficou no arquivo, veja §8.2.
5. **Nunca adivinhe o caminho de saída.** Ver §7.3.

### 7.2 Exit codes, medidos

```
render de 1 cena, arquivo com 1 cena, sem nomear     → 0
render sem nomear num arquivo com 6 cenas            → 1   ValueError listando as 6
render de cena inexistente                           → 1   ValueError listando as válidas
cena que levanta exceção                             → 1   JSON com error/traceback
argumento desconhecido no bin/setup                  → 2
```

As duas mensagens de erro **listam as cenas disponíveis**. Não invente o nome:
leia o erro, ou rode `mx scenes`.

### 7.3 O caminho de saída, e o `<módulo>` que pode ficar vazio

O padrão vem do `manim.cfg`:
`video_dir = {media_dir}/videos/{module_name}/{quality}`.

**[FONTE]** `manim/scene/scene_file_writer.py:263` — e esta linha é a que ninguém
espera:

```python
module_name = config.get_dir("input_file").stem if config["input_file"] else ""
```

Três consequências:

- O `<módulo>` é o **stem do arquivo de entrada**, não o nome do módulo Python
  que o `manimx` sintetiza internamente (§9). Renomear `demo.py` → `intro.py`
  muda o diretório de saída inteiro.
- **`-r` mexe no `{quality}` do caminho**, porque esse componente é
  `<altura>p<fps>`. **[MEDIDO]**: `-q l -r 1280x720` grava em **`720p15`** — 720 do
  `-r`, 15 do `-q`. O `-r` sobrescreve só a resolução; o **fps continua vindo do
  `-q`**, e para mudá-lo é `--fps`. *(A skill `manim-render-api` diz na linha 57
  que `-r` "ignora `-q`" — está errado, e esta medição é a prova. Enquanto ela não
  for corrigida, vale o que está aqui.)*
- **Sem `input_file`, o componente vira string vazia** e o caminho colapsa para
  `media/videos//1080p60/`. Isso acontece quando você chama `render_scene()` com
  uma classe já importada e não passa `input_file=`. Passe sempre.

Leia o caminho do JSON. Sempre. Formatos, seções, `-n a,b`, transparência,
`--save_sections`: **`manim-render-api`**.

---

## 8. As duas portas para o mesmo motor

### 8.1 Defaults DIFERENTES nas duas portas

| | `bin/mx render` (CLI) | `manimx.render_scene` (Python) |
|---|---|---|
| codec padrão | **`nvenc`** (`cli.py:463`) | **`x264`** (`render.py:269`) |
| renderer padrão | `cairo` | `cairo` |
| qualidade padrão | `h` | `h` |
| verbosidade padrão | `WARNING` | `WARNING` |

**[FONTE]**, e explica um relato recorrente: *"o mesmo render ficou 3× mais lento
quando virei script"*. Um `mx render` sem `--codec` já sai em `h264_nvenc`; o
mesmo trabalho pela API Python sai em `libx264`. Não é bug, é default divergente.

### 8.2 Para conferir o que de fato saiu no arquivo

```bash
grep -aqo "x264 - core" saida.mp4 && echo libx264 || echo NVENC
```

**[MEDIDO]** nos dois arquivos: acerta os dois. O libx264 grava a própria
assinatura no container; o NVENC não. É o teste mais barato que existe e não
precisa de `ffprobe`.

### 8.3 A API Python, com as assinaturas reais

**[FONTE]** `manimx/render.py`:

```python
load_scene_classes(file_path) -> list[type]        # importa e filtra (§9)
list_scenes(file_path) -> list[str]                # só os nomes
render_scene(scene_class, *, quality="h", renderer="cairo", codec="x264",
             theme=None, gpu=None, fmt=None, transparent=False, fps=None,
             resolution=None, media_dir=None, output_file=None, input_file=None,
             disable_caching=False, flush_cache=False, save_last_frame=False,
             save_sections=False, background_color=None,
             max_inflight_encoders=None, encoder_queue_size=None,
             preview=False, verbosity="WARNING",
             config_overrides=None, raise_on_error=False) -> RenderResult
render_file(file_path, scene_names=None, *, all_scenes=False, **kwargs)
             -> RenderResult | list[RenderResult]
render_many(...)                                   # existe, fora do __all__
```

**Armadilha documental:** a docstring de `manimx/__init__.py` mostra
`from manimx import render_file, quality` — **`quality` não existe**
(`ImportError` reproduzido; **[FONTE]** o `__all__` do pacote não a inclui).
O exemplo do próprio pacote está errado. O que existe no topo é:
`GPUReport`, `detect_gpu`, `enable_nvenc`, `disable_nvenc`, `nvenc_available`,
`RenderResult`, `render_file`, `render_scene`, `list_scenes`, `QUALITY_PRESETS`,
`CODEC_PRESETS`, `THEMES`, `apply_theme`.

### 8.4 `config_overrides` é a saída para o problema do cwd

Como o `manim.cfg` só vale a partir da raiz (§5), um script que precisa rodar de
outro lugar deve declarar as chaves explicitamente:

```python
from manimx import render_file

render_file(
    "/caminho/absoluto/cena.py", "Cena",
    quality="h", codec="nvenc", input_file="/caminho/absoluto/cena.py",
    config_overrides={"max_inflight_encoders": 4, "max_files_cached": 200},
)
```

Tudo o que é render em profundidade: **`manim-render-api`**. Lote e paralelismo
entre processos: **`manim-batch-pipeline`**.

---

## 9. Como o `mx` enxerga uma cena — e onde ele diverge do CLI da CE

### 9.1 O filtro do `manimx`

**[FONTE]** `manimx/render.py:111-145`. O módulo é importado sob um nome
sintetizado, e o filtro é uma linha:

```python
module_name = f"_manimx_scene_{path.stem}_{abs(hash(str(path)))}"
...
if issubclass(obj, Scene) and obj.__module__ == module_name
```

**[MEDIDO]** com um experimento (`bin/mx scenes` num arquivo que importa uma base
e define um mixin):

```python
# tema.py
class CenaBase(Scene): ...

# cena.py
from tema import CenaBase
class _Atos:                     # mixin, NÃO herda de Scene
    def construct(self): ...
class FilhaDaBase(CenaBase): ...
class ParteUm(_Atos, CenaBase): ...
```
```
$ bin/mx scenes cena.py
FilhaDaBase   (CenaBase)
ParteUm       (_Atos, CenaBase)
```

- **`CenaBase` não aparece** — ela é `Scene`, mas o `__module__` dela é `tema`.
  Base compartilhada importada de outro arquivo fica fora da listagem de graça.
- **`_Atos` não aparece** — não é `Scene`. É por isso que o formato de cena em
  partes usa mixin: se o mixin herdasse de `Scene`, o pipeline renderizaria a
  cena inteira de novo por engano, gerando um mp4 que ninguém consome.
  **`manim-presentation-parts`** é a dona dessa regra.

Duas notas de mecânica que valem para quem escreve `tema.py` ao lado da cena:

- **[FONTE]** `render.py:130-139` — o diretório da cena entra em `sys.path` **só
  durante o import** e é removido num `finally`. Um `import tema` dentro da cena
  funciona; um script auxiliar que rode depois e queira `import tema` precisa do
  próprio `sys.path.insert`.
- A ordenação é **por linha de definição no arquivo**, não alfabética
  (`classes.sort(key=... __firstlineno__ ...)`). `P1..P10` saem na ordem certa
  sem esforço; `P10` não vem antes de `P2`.

### 9.2 A divergência com `bin/manim` — igualdade × prefixo

**[FONTE]**, não executado. O CLI da própria CE usa outro filtro
(`manim/utils/module_ops.py:72-79`):

```python
inspect.isclass(obj) and issubclass(obj, Scene) and obj != Scene \
    and obj.__module__.startswith(module.__name__)
```

E o nome do módulo é `".".join(file_name.with_suffix("").parts)`
(`module_ops.py:51`) — para `scenes/demo.py`, `"scenes.demo"`.

`startswith` **não é** `==`. Cenário concreto: você roda `bin/manim demo.py`
(caminho relativo, sem diretório) → `module.__name__ == "demo"`. Se `demo.py`
fizer `from demo_utils import Base`, então `"demo_utils".startswith("demo")` é
**True** — o CLI da CE **lista** classes vindas de `demo_utils.py`, e o
`mx scenes` **não**.

Consequência: `bin/manim` e `bin/mx scenes` podem discordar sobre quais cenas um
arquivo expõe. Se um pipeline usa um para descobrir e o outro para renderizar,
isso vira cena órfã ou cena faltando. **Use um só dos dois para descobrir** — e
neste projeto o canônico é `bin/mx scenes --json`. **[NÃO VERIF.]** o cenário do
prefixo não foi reproduzido; a leitura dos dois filtros é que é firme.

### 9.3 `mx scenes` EXECUTA o arquivo

**[MEDIDO]** — um `print` no topo do módulo sai na listagem. Se o módulo abre
arquivo, faz requisição de rede ou instancia mobject no nível do módulo, isso
acontece **só por listar**. Daí os ~0,9 s de latência (4× os outros comandos de
introspecção). Duas leituras:

- é um custo aceitável e não tem substituto: só existe uma forma de saber quais
  classes um `.py` define, e é executá-lo;
- é um motivo forte para **não fazer trabalho no nível do módulo**. Ver §10.1,
  onde isso vira um defeito silencioso de cor.

Saída em JSON, para pipeline:

```bash
bin/mx scenes cena.py --json 2>/dev/null | jq -r '.[].name'
```
**[FONTE]** `cli.py:192-199` — cada item tem `name`, `bases` (lista de nomes) e
`doc` (a **primeira linha** da docstring, ou `null`).

---

## 10. Os defeitos que não dão erro nenhum

Esta é a seção que justifica a skill. Todos foram reproduzidos; cada um aponta a
skill dona.

### 10.1 `--theme` é aplicado DEPOIS do import da cena

**[FONTE]** — a ordem está invertida em relação à intuição. `render_file` chama
`load_scene_classes()` (`render.py:495`), que **executa o módulo da cena inteiro**;
só depois `render_scene` entra no `tempconfig` e chama `apply_theme`
(`render.py:424-425`). Ou seja: **todo código no nível do módulo roda antes de o
tema existir**. Um Mobject criado ali não recebe as cores do tema:

```python
CEDO = Text("cedo")                    # criado no import

class T(Scene):
    def construct(self):
        tarde = Text("tarde")
```
```
$ bin/mx render tema2.py T --theme whiteboard --format png
MXTEMA cedo=#FFFFFF  tarde=#000000  bg=#FFFFFF
```

**[MEDIDO]**: `cedo` ficou **branco sobre fundo branco** — invisível, sem erro,
sem warning.

Corolário maior, e é a regra da casa: **`--theme whiteboard` é rede de segurança,
não solução.** **[FONTE]** `presets.py:183-222` — ele mexe em `config` e roda
`set_default` em `Text`, `Tex`, `MathTex` e `VMobject`, o que só alcança quem for
instanciado depois. Em fundo claro, **passe cor explícita em todo mobject**.

Os 8 temas, **[FONTE]** `presets.py:129-170`:

| tema | fundo | tinta |
|---|---|---|
| `3b1b` | `#000000` | `#FFFFFF` |
| `whiteboard` | `#FFFFFF` | `#000000` |
| `paper` | `#F4F1EA` | `#1C1B19` |
| `slate` | `#1E1E2E` | `#CDD6F4` |
| `solarized-dark` | `#002B36` | `#93A1A1` |
| `solarized-light` | `#FDF6E3` | `#586E75` |
| `nord` | `#2E3440` | `#ECEFF4` |
| `transparent` | `#000000` + `opacity 0.0` | `#FFFFFF` |

Cor, contraste, paleta e a disciplina do tema: **`manim-color-theming`**.
O `tema.py` como contrato de projeto (fonte, escala, tempos, classe-base, dados):
**`manim-tema-projeto`**.

*(Nota de leitura que já custou uma investigação: `Text(...).color` do **grupo** é
sempre `#000000` — a cor real mora nos glifos, em `.submobjects[i].fill_color`.
Medir a cor no grupo dá falso negativo.)*

### 10.2 `--codec av1` grava libx264, com `success: true`

**[MEDIDO]**:

```
$ bin/mx render demo.py Demo --codec av1 --json
pedi av1, saiu: libx264 | success True
```

O hardware tem `av1_nvenc` (Ada, cc 8.9) e o PyAV lista o encoder, mas a junção
dos partial movies falha (`UnknownCodecError: libdav1d`) — a validação do
`manimx` detecta e substitui. **[FONTE]** `presets.py:91-102`: o próprio
`CODEC_PRESETS["av1"]["desc"]` documenta isso, e é o que `mx presets` imprime.
O exit code, não. Para AV1 de verdade, reencode o mp4 final com `/usr/bin/ffmpeg`.
Codec e GPU: **`manim-gpu-encoding`**.

### 10.3 `-r 1080x1920` muda o buffer de pixels, não o palco

Pedido comum ("um vídeo pro Shorts") e defeito silencioso. **[MEDIDO]**:

```
$ bin/mx render vert.py Vert -r 1080x1920 --format png
MXV frame 14.222 x 8.000 | pixel 1080x1920
```

`config.frame_width` continua **14,222** e `frame_height` **8,0**. O mundo segue
paisagem: um `Dot().to_edge(UP)` foi parar a **37,7% do topo** do PNG, medido em
pixel. Nada distorce (o círculo sai com proporção 1,000) — simplesmente sobra
mundo em cima e embaixo, e todo `to_edge`/`frame_height` mente.

A correção, **[MEDIDO]** (o ponto passou para 8,7% do topo, que é o esperado):

```python
from manim import *

# 9:16 de verdade: o palco tem de acompanhar o buffer.
config.frame_width = config.frame_height * 1080 / 1920      # 8 × 0,5625 = 4,5
```
```bash
bin/mx render cena.py Cena -r 1080x1920 -q h --codec nvenc
```

Enquadramento, margem segura, "cabe na tela?", grade e z-index:
**`manim-layout-posicionamento`**.

### 10.4 Fonte ausente vira Noto Sans, e o objeto continua dizendo que é Inter

**[MEDIDO]**: `manimpango.list_fonts()` vê **411 famílias** aqui. **`Inter`,
`SF Pro Text`, `Helvetica` e `Arial` NÃO existem.** `Text(..., font="Inter")`
emite um `WARNING` no logger e segue:

```
fc-match Inter        → Noto Sans Regular
fc-match "SF Pro Text"→ Noto Sans Regular
fc-match Helvetica    → Nimbus Sans Regular
fc-match Arial        → Liberation Sans Regular
```

E `t.font` continua devolvendo `'Inter'` — **o objeto não sabe que foi
substituído**, então nenhuma asserção sobre `.font` pega o defeito. Se o vídeo
precisa casar com um slide em Inter, ou instale a fonte, ou escolha uma que
existe (**Fira Sans** é a sans com mais pesos reais aqui: 32 faces).

**Armadilha de segunda ordem, [DECK]:** instalar a fonte "certa" pode **piorar**.
Um pacote de Inter só-Regular faz o Pango resolver os três pesos para a Regular —
`SEMIBOLD` some e `BOLD` vira embolden sintético. Quem detecta fonte deveria
checar **faces**, não famílias. A defesa que o projeto consumidor usa é uma pilha
de fallback resolvida no import mais um booleano honesto (`FONTE_EXATA`), padrão
que mora em **`manim-tema-projeto`**.

Texto, `t2c`, LaTeX, `register_font`: **`manim-text-latex`**.

### 10.5 O cairo arredonda a posição X de cada glifo para INTEIRO

Reproduzido nesta máquina, olhando o SVG que o próprio Manim põe em cache.

**[FONTE]** `manim/mobject/text/text_mobject.py:85,838` — o ManimCE entrega a
string ao Pango em `font_size / TEXT2SVG_ADJUSTMENT_FACTOR` pt, com
`TEXT2SVG_ADJUSTMENT_FACTOR = 4.8`. **[MEDIDO]** no SVG resultante:

```
font_size=22   → <use x="30"/> <use x="34"/> <use x="36"/> <use x="39"/>   y="26.532227"
font_size=720  → <use x="30"/> <use x="145"/> <use x="197"/> <use x="310"/> y="233.799805"
```

**X inteiro, Y fracionário.** Em `font_size=22` o em mede ~6,1 unidades de
dispositivo, então meia unidade de arredondamento é **±8% do em por letra** — as
letras se soltam das palavras. Em 720 o em mede 200 unidades e o mesmo
arredondamento vale 0,25%. O erro é proporcional a 1/tamanho: **[DECK]** 9,30% em
18 · 8,02% em 22 · 3,80% em 44 · 1,86% em 96.

**Três hipóteses derrubadas por medição** **[DECK]** (`~/Projects/aulas`,
2026-08-19) — registre-as, são exatamente as que dá vontade de tentar:

- **não é a fonte**: seis fontes, todas ~8% (Fira Sans 8,02 · Cantarell 8,10 ·
  DejaVu 8,02 · Liberation 6,55 · Ubuntu 8,02 · Inter 7,36);
- **não é peso sintético**: mesmo erro em NORMAL/SEMIBOLD/BOLD, e `fc-match`
  devolve face REAL;
- **não é hinting do fontconfig**: `FONTCONFIG_FILE` com `hinting=false` gera SVG
  **idêntico**. Quem arredonda é o `hint_metrics` do cairo, que o manimpango nunca
  configura — não dá para desligar de fora.

**A correção é mexer na GRADE**, não na fonte: desenhar todo texto num tamanho
único e grande (`font_size=720` = 200 px de dispositivo por em) e encolher o
mobject com `.scale(alvo/720)`. **[DECK]** erro rms **5,53% → 0,13%** (43× melhor),
constante em todos os tamanhos.

Ao fazer isso é **obrigatório** trocar `config.pixel_width`/`pixel_height` por um
palco enorme durante a construção e devolvê-los num `finally`. O motivo é
**[FONTE]** `text_mobject.py:846-863`: o Manim passa `config["pixel_width"]` e
`["pixel_height"]` ao `manimpango.text2svg` como **largura e altura de quebra de
linha**. Com o texto 30× maior, uma frase longa quebraria sozinha.

Receita completa e implementação de referência: **`manim-text-latex`** e
**`manim-tema-projeto`**.

### 10.6 O cache de SVG de texto ignora a resolução — e a flag que você acharia que desliga não desliga

**[FONTE]**, e vale corrigir um mal-entendido que já circulou: existem **dois**
caches de SVG e eles não são o mesmo.

| Cache | Onde | Chave | Controlado por |
|---|---|---|---|
| de **mobject**, em memória | `SVG_HASH_TO_MOB_MAP` (`svg_mobject.py:29`) | hash do arquivo+config | `use_svg_cache` |
| de **arquivo**, em disco | `{media_dir}/texts/<hash>.svg` (`text_mobject.py:834-851`) | `_text2hash` | **nada — é incondicional** |

Na 0.21 `Text.__init__` tem `use_svg_cache: bool = False` (`text_mobject.py:472`),
mas isso só desliga o **primeiro**. O segundo continua ligado, e é ele que morde:

```python
def _text2hash(self, color):
    settings = "PANGO" + self.font + self.slant + self.weight + str(color)
    settings += str(self.t2f) + str(self.t2s) + str(self.t2w) + str(self.t2c)
    settings += str(self.line_spacing) + str(self._font_size)
    settings += str(self.disable_ligatures) + str(self.gradient)
    id_str = self.text + settings          # ← pixel_width NÃO entra
```

E o `_text2svg` faz `if file_name.exists(): reusa` **antes** de ler
`config["pixel_width"]`. Ou seja: um render `-qm` (1280) e um `-qh` (1920) podem
**quebrar linha de formas diferentes** e o segundo reaproveitar o SVG do primeiro.
Bug latente, silencioso, real — e mais um motivo para o palco fixo de §10.5.

*(O mesmo vale para o cache de LaTeX em `{media_dir}/Tex`, com hash do fonte
`.tex` — é ele que faz o check do doctor passar sem `dvisvgm`, §4.3.)*

### 10.7 O cache de partial movies não enxerga dado que veio de fora

O hash cobre a chamada de `play`, não o CSV/API/arquivo que a cena leu. Cena que
depende de dado externo precisa de `--no-cache` (`--disable_caching` no CLI cru),
senão ela reaproveita o vídeo velho com o dado novo. Está escrito no `manim.cfg`.

O mesmo vale para `random` sem semente e para qualquer coisa que dependa da data.
Cache, poda, `max_files_cached` e o que custa rasterizar:
**`manim-performance-cache`**.

### 10.8 `python cena.py` não faz nada — e sai 0

**[MEDIDO]**:

```
$ .venv/bin/python scenes/demo.py
exit=0    (nenhuma saída, nenhum mp4)
```

O arquivo só define classes. Sem `mx render`/`manim`, ninguém chama `construct`.
É a pior forma de falha: **sucesso aparente**.

### 10.9 Elemento invisível entra na caixa delimitadora

**[DECK]**, e não tem erro nem warning: um detalhe transparente (lingueta,
espaçador, `VectorizedPoint`) continua contando no bounding box do `VGroup`.
`VGroup.move_to()` desloca o grupo inteiro pelo tamanho do invisível — **4 px,
medidos**. Posicione pelo **corpo visível**, não pelo grupo.
Dono: **`manim-layout-posicionamento`**.

### 10.10 Renderizou e não olhou: não terminou

Texto branco no branco, elemento cortado pela borda, sobreposição, barra
estourando o eixo, fonte trocada por Noto Sans, pôster do PDF em branco porque o
último frame é um fade-out — **nada disso dá erro no terminal**. Confiar no exit
code não pega nenhum deles.

O ciclo que funciona:

```
escrever → renderizar rápido (-q l --format png) → OLHAR o PNG → corrigir → render final
```

**[DECK]** três defeitos reais de uma investigação só apareceram ao olhar o PNG;
nenhum deu erro no terminal. Método completo, o que dá para conferir **sem**
render (`is_off_screen`, `get_corner` contra os limites, `index_labels`) e como
comparar frames: **`manim-verificacao-visual`**.

---

## 11. Cor: a regra verdadeira

**Uma versão anterior desta skill dizia "não escreva hex de 3 dígitos (`#F00`); o
parser exige 6". Isso é FALSO** e contradizia o `manim.cfg`, o docstring de
`manimx.presets.apply_theme` e a skill `manim-color-theming`. Corrigido, com as
cinco provas **[MEDIDO]**:

```
ManimColor("#F00")    → #FF0000            ✅ expande
ManimColor("#0071E3") → #0071E3            ✅
ManimColor("F00")     → ValueError: Color F00 not found
ManimColor("0071E3")  → ValueError: Color 0071E3 not found
ManimColor("#12345")  → ValueError: Hex colors must be … 6 or 8 hexadecimal numbers
```

**O que quebra é a falta do `#`, não a contagem de dígitos.** Sem `#`, a string é
lida como *nome* de cor e some no meio de um `ValueError` que fala de "Color não
encontrada" — mensagem que manda você procurar no lugar errado.

Vale igual pela CLI, apesar de o `--help` do `mx render` dizer "cor hex de 6
dígitos" (**[FONTE]** `cli.py:471`; o texto é conservador demais):

```
bin/mx render … --background "#F00"     → pixel (0,0) = (255, 0, 0)  ✅
bin/mx render … --background "FF0000"   → success False, ValueError: Color FF0000 not found
```

E lembre de §10.1: em fundo claro, `--theme` não substitui cor explícita.
Paleta, gradiente, alfa, contraste WCAG, aritmética de cor:
**`manim-color-theming`** (1113 linhas, é a dona).

---

## 12. Os dois motores

| | ManimCE | ManimGL (3b1b) |
|---|---|---|
| import | `from manim import *` | `from manimlib import *` |
| CLI | `bin/manim` | `bin/manimgl` |
| versão aqui | **0.21.0** | **1.7.2** (git master) |
| rasterização | Cairo (CPU) ou ModernGL (`--renderer=opengl`) | **wgpu → Vulkan** |
| encoding | PyAV embutido, codec fixo no código | binário `ffmpeg`, `--vcodec` livre |
| fundo padrão da biblioteca | `#000000` | `#333333` |
| fundo NESTE projeto | `#000000` (`manim.cfg`) | `#000000` (`custom_config.yml` força) |
| saída | `media/` | `media-gl/` |
| `mx` enxerga? | sim | **não** |

**Não são compatíveis no nível de código-fonte.** **[MEDIDO]** `api/ce-vs-gl.md`
(gerado por reflexão, não escrito à mão): **337** classes públicas na CE, **270**
na GL, **153 com nome em comum — e todas as 153 com assinatura diferente**. Essa
última é a armadilha silenciosa: o import funciona, o construtor aceita, e o
resultado sai errado.

**Padrão: use ManimCE.** Vá para ManimGL só se o usuário pedir o fluxo do 3b1b
explicitamente, ou precisar da janela interativa com manipulação 3D e do REPL
(`self.embed()`).

Três fatos do lado GL que já custaram caro:

- **`custom_config.yml` deste repo usa `video_codec: "libx264"` DE PROPÓSITO.**
  **[MEDIDO]** hoje: `grep video_codec custom_config.yml` → `libx264`. O arquivo é
  versionado e numa máquina sem NVIDIA o ffmpeg abortaria com "Unknown encoder
  'h264_nvenc'". Quem liga o NVENC é o **wrapper**: **[FONTE]** `bin/manimgl:20-31`
  detecta a placa **e** confirma o encoder no ffmpeg, e só então injeta
  `--vcodec h264_nvenc` — a menos que você já tenha passado `--vcodec`.
  *(A skill `manimgl-3b1b` ainda afirma que o YAML já vem com NVENC. **Não vem.**
  Onde as duas divergirem, vale esta: a evidência é o arquivo.)*
- **`ffmpeg` ignora `crf` em silêncio com NVENC.** Para qualidade em NVENC use
  `cq`. Está comentado no próprio YAML.
- **`import manimlib` parseia `sys.argv` NO IMPORT** e mata o processo:
  ```
  $ .venv-gl/bin/python -c "import manimlib" --package x
  -c: error: unrecognized arguments: --package
  ```
  Qualquer script com CLI própria que importe manimlib precisa de
  `sys.argv = [sys.argv[0]]` antes do import (**[MEDIDO]**: com isso funciona).

E: **`mx` só enxerga o venv da CE.** **[MEDIDO]**
`bin/mx scenes scenes/exemplos_gl.py` devolve
`erro: ModuleNotFoundError: No module named 'manimlib'`. Cena GL só pelo
`bin/manimgl`. Tudo mais do lado GL: **`manimgl-3b1b`**.

---

## 13. Roteamento — carregue a skill certa

A regra é: **esta skill não ensina o assunto, ela entrega a porta.** Se o pedido
cabe numa linha abaixo, carregue a skill **antes** de escrever código.

São **27 skills** neste projeto: a portaria (esta) + 26. **[DISCO, conferido na
costura de 2026-08-19]** todas existem em `.claude/skills/<nome>/SKILL.md`, e
`ls .claude/skills/ | wc -l` devolve 27. Toda linha das tabelas abaixo aponta
para um arquivo real, e as 26 aparecem em pelo menos uma delas — não há assunto
de fazer vídeo sem porta.

O índice legível do conjunto, agrupado por tema e com por onde começar, está em
**`.claude/skills/README.md`**. Esta seção é o roteador; o README é o mapa.

### 13.1 Fundamento e ferramenta

| A tarefa é… | Skill |
|---|---|
| achar classe/método/constante/assinatura que você não confirmou | **`manim-api-discovery`** |
| renderizar, escolher qualidade/formato, saber o caminho da saída, API Python | **`manim-render-api`** |
| GPU, NVENC, escolha de codec, "está lento", peso do arquivo, benchmark | **`manim-gpu-encoding`** |
| muitos vídeos de uma vez, paralelismo entre processos, CI | **`manim-batch-pipeline`** |
| cache, hash de partial movie, `max_files_cached`, o que custa rasterizar | **`manim-performance-cache`** |
| conferir o que SAIU: olhar o PNG, comparar frames, achar corte na borda | **`manim-verificacao-visual`** |
| erro concreto, traceback, saída errada, travamento | **`manim-troubleshooting`** |

### 13.2 Desenhar

| A tarefa é… | Skill |
|---|---|
| formas prontas, agrupamento, submobjects, `VGroup` × `Group` | **`manim-mobjects`** |
| "cabe na tela?", margem, `arrange_in_grid`, `scale_to_fit_*`, z-index, 9:16 | **`manim-layout-posicionamento`** |
| texto, LaTeX, colorir parte de uma fórmula, `{{ }}`, fonte, nitidez do glifo | **`manim-text-latex`** |
| cor, fundo, tema, gradiente, transparência/alfa, contraste, aritmética de cor | **`manim-color-theming`** |
| o `tema.py` do projeto: paleta + fonte + escala + tempos + classe-base + dados | **`manim-tema-projeto`** |
| trazer arquivo de fora: SVG, PNG/JPG, `ImageMobject`, `register_font` | **`manim-svg-imagens`** |
| eixos, plot de função, área, riemann, tangente, `BarChart` | **`manim-graphs-plots`** |
| `Table`, `MathTable`, `Matrix`, célula destacada, colchete | **`manim-tabelas-matrizes`** |
| `Graph`/`DiGraph`, layout de grafo, rede, árvore | **`manim-grafos-redes`** |
| Mobject PRÓPRIO, caminho de Bézier, `Animation` própria, booleanos de forma | **`manim-mobjects-customizados`** |
| 3D, `ThreeDScene`, superfície, sólido, `phi`/`theta`, `move_camera` | **`manim-3d-camera`** |
| zoom e pan em **2D**: `MovingCameraScene`, `ZoomedScene`, `self.camera.frame` | **`manim-camera-2d`** |

### 13.3 Mover

| A tarefa é… | Skill |
|---|---|
| animar, `.animate`, `Transform`, qual classe de animação usar | **`manim-animations`** |
| RITMO: as 49 `rate_function`, `lag_ratio`, `LaggedStart`, `ChangeSpeed`, `path_func` | **`manim-composicao-ritmo`** |
| valor que muda: `ValueTracker`, updaters, `always_redraw`, contador | **`manim-updaters-valuetracker`** |

### 13.4 Estruturar e entregar

| A tarefa é… | Skill |
|---|---|
| de qual `Scene` eu herdo? ciclo de vida, `add`/`remove`, `next_section`, seções | **`manim-cenas-secoes`** |
| cena para PALESTRA/SLIDE — partes que o apresentador avança | **`manim-presentation-parts`** |
| som, narração, legenda: `add_sound`, `add_subcaption`, `.srt` | **`manim-som-legendas`** |
| código do 3b1b, `manimlib`, `ShowCreation`, portar GL↔CE | **`manimgl-3b1b`** |

### 13.5 Desempate dos pares que se confundem

Os gatilhos abaixo colidem entre duas skills. Decida por aqui:

| Sintoma | Vai para | Não vai para |
|---|---|---|
| `AttributeError`/`TypeError` de **nome ou assinatura** | `manim-api-discovery` | `manim-troubleshooting` |
| falha de **render, ambiente, codec, arquivo de saída** | `manim-troubleshooting` | `manim-api-discovery` |
| "renderiza rápido só um frame para eu ver" | `manim-render-api` | `manim-verificacao-visual` |
| "olhei o frame e está feio/cortado/sobreposto" | `manim-verificacao-visual` | `manim-render-api` |
| "está lento" por **encode** (codec, NVENC) | `manim-gpu-encoding` | `manim-performance-cache` |
| "está lento" por **rasterização** (curvas demais, cache frio) | `manim-performance-cache` | `manim-gpu-encoding` |
| **uma** cena lenta | `manim-gpu-encoding` | `manim-batch-pipeline` |
| **muitas** cenas, throughput | `manim-batch-pipeline` | `manim-gpu-encoding` |
| "onde eu ponho esse objeto em relação àquele" | `manim-layout-posicionamento` | `manim-mobjects` |
| "que classe desenha um losango?" | `manim-mobjects` | `manim-layout-posicionamento` |
| "isso está estourando o quadro / cabe?" | `manim-layout-posicionamento` | `manim-mobjects` |
| usar forma pronta | `manim-mobjects` | `manim-mobjects-customizados` |
| escrever uma classe de Mobject nova | `manim-mobjects-customizados` | `manim-mobjects` |
| `Transform` × `ReplacementTransform` | `manim-animations` | `manim-mobjects` |
| QUAL animação usar | `manim-animations` | `manim-composicao-ritmo` |
| QUANTO tempo, que curva, em que ordem | `manim-composicao-ritmo` | `manim-animations` |
| animar uma troca de cor | `manim-animations` | `manim-color-theming` |
| escolher a cor / o contraste | `manim-color-theming` | `manim-animations` |
| a paleta e a escala do **projeto inteiro** | `manim-tema-projeto` | `manim-color-theming` |
| transparência / alfa / `.mov` como decisão visual | `manim-color-theming` | `manim-render-api` |
| mover a CÂMERA em 2D (zoom, pan, seguir) | `manim-camera-2d` | `manim-3d-camera` |
| `phi`/`theta`/`gamma`, `add_fixed_in_frame_mobjects` | `manim-3d-camera` | `manim-camera-2d` |
| ritmo de **um vídeo corrido** | `manim-composicao-ritmo` | `manim-presentation-parts` |
| corte em **partes que o apresentador avança** | `manim-presentation-parts` | `manim-cenas-secoes` |
| `next_section` como recurso da biblioteca | `manim-cenas-secoes` | `manim-presentation-parts` |
| eixos e plot de função, `BarChart` | `manim-graphs-plots` | `manim-tabelas-matrizes` |
| grade de células com texto | `manim-tabelas-matrizes` | `manim-graphs-plots` |
| vértices e arestas | `manim-grafos-redes` | `manim-tabelas-matrizes` |
| **5 caixas e setas** de um diagrama de arquitetura | `manim-layout-posicionamento` | `manim-grafos-redes` |
| pôr um logo/print/SVG na cena | `manim-svg-imagens` | `manim-mobjects` |
| `Text(font=…)` e a fonte não apareceu | `manim-text-latex` | `manim-svg-imagens` |

> A última linha do bloco de grafos é a decisão que mais custa em aula: um
> diagrama de arquitetura com 5 caixas rotuladas **não é** um `Graph`. Layout
> automático briga com legibilidade e muda de lugar a cada render.

### 13.6 Roteamento por PEDIDO em português

O usuário raramente diz o nome da classe. Esta tabela mapeia o que ele diz:

| Ele diz | Comece por |
|---|---|
| "faz um vídeo explicando X" | esta skill → `manim-cenas-secoes` → o assunto |
| "anima essa fórmula" | `manim-text-latex` + `manim-animations` |
| "monta um gráfico animado" | `manim-graphs-plots` + `manim-composicao-ritmo` |
| "põe isso num slide", "quebra em partes" | `manim-presentation-parts` |
| "o vídeo está feio/cortado" | `manim-verificacao-visual` |
| "o texto sumiu" | `manim-color-theming` (§10.1 aqui explica por quê) |
| "as letras estão soltas" | `manim-text-latex` — a §10.5 **desta** skill explica por quê |
| "deixa as cores iguais em todas as cenas" | `manim-tema-projeto` |
| "usa a GPU", "acelera" | `manim-gpu-encoding` |
| "renderiza tudo" | `manim-batch-pipeline` |
| "vídeo pro Shorts/Reels" (9:16) | `manim-layout-posicionamento` — a §10.3 **desta** skill é o pré-requisito |
| "dá um zoom nisso" | `manim-camera-2d` |
| "põe a logo da empresa" | `manim-svg-imagens` |
| "narra isso" | `manim-som-legendas` |
| "não sei por onde começar" | fique aqui, §14 |

### 13.7 Buracos declarados — assuntos SEM skill dona

Assuntos reais da API 0.21 que **não têm skill dedicada**. Não invente
comportamento: confirme com `bin/mx show` antes de escrever, e diga ao usuário
que a área não tem guia.

| Assunto | Símbolos | Como proceder |
|---|---|---|
| **ênfase e anotação** | `Flash` `Indicate` `Circumscribe` `FocusOn` `Wiggle` `ApplyWave` `Blink` `ShowPassingFlash`; `Brace` `BraceLabel` `BraceText` `BraceBetweenPoints` `ArcBrace`; `SurroundingRectangle` `Underline` `Cross` | órfão **e muito usado em aula**. `mx show` em cada um; `Brace*` moram em `mobject/svg`, não em `geometry` |
| **código e Typst na tela** | `Code` `Typst` `MathTypst` `Paragraph` `Variable` `BulletedList` `Title` | órfão. `manim-text-latex` cobre as 4 classes de texto, **não** o `Code` |
| **campos e fluxo** | `VectorField` `ArrowVectorField` `StreamLines` `PhaseFlow` `Homotopy` `ComplexHomotopy` `TracedPath` `AnimatedBoundary` | órfão. Atenção: `TracedPath`/`AnimatedBoundary` são **Mobjects** (`self.add`), não animações |
| **álgebra linear de cena** | `LinearTransformationScene` `VectorScene` `ApplyMatrix` `ApplyComplexFunction` | órfão. `manim-cenas-secoes` lista as classes, não ensina |
| **precedência de config** | `ManimConfig` (74 propriedades) `tempconfig` `config_file_paths` `parse_cli_ctx` | órfão. O essencial está em §5 |
| **renderer OpenGL do CE** | 45 classes `mobject/opengl` + `Shader` `ShaderWrapper` `Mesh` `Object3D` `Window` `FullScreenQuad` `OpenGLCamera` `OpenGLRenderer` | órfão **de propósito**: no fluxo deste projeto o renderer é cairo |
| **câmeras exóticas** | `MultiCamera` `SplitScreenCamera` `MappingCamera` `OldMultiCamera` | `manim-camera-2d` cobre `MovingCamera`/`MultiCamera` via `ZoomedScene`; as outras não |
| `Broadcast`, `ManimBanner`, `SampleSpace` | 3 classes | órfãos triviais |
| **plugins de terceiros** | `get_plugins()` `list_plugins()` | **[MEDIDO] não instalados nesta máquina**. Não presuma que `manim-voiceover` & cia. funcionam |
| **janela/preview interativo do CE** | `--enable_gui` `--force_window` `-p` `--fullscreen` | as flags existem em `bin/manim --help`; para interativo de verdade prefira `bin/manimgl` |

**Correção de rota, [FONTE]:** `Shader`, `ShaderWrapper`, `Mesh`, `Object3D`,
`Window`, `FullScreenQuad`, `OpenGLCamera` e `OpenGLRenderer` estão na categoria
**`renderer`**, não em `mobject/opengl`. Uma versão anterior desta skill mandava
procurá-los com `mx find --category mobject/opengl`, onde eles **não aparecem**.
O comando certo:

```bash
bin/mx find "" --category renderer --kind class -n 30
bin/mx find "" --category mobject/opengl --kind class -n 60     # as 45 classes OpenGL*
```

---

## 14. Não sei por onde começar — a sequência

Quando o pedido é grande e vago ("faz um vídeo explicando worktrees"), esta é a
ordem que funciona. Cada passo carrega uma skill; nenhum passo escreve código
antes do anterior terminar.

1. **Decida o formato.** É vídeo corrido ou peça de palestra que o apresentador
   avança? Se houver um humano falando por cima, é o segundo, e o formato em
   partes é obrigatório desde a primeira linha — retrofitar depois é caro.
   → **`manim-presentation-parts`**
2. **Decida a identidade visual antes do primeiro Mobject.** Fundo claro ou
   escuro, paleta, fonte, escala de tamanhos, tempos. Em fundo claro, todo
   mobject precisa de cor explícita (§10.1) — descobrir isso depois de 400 linhas
   é um `sed` arriscado. → **`manim-tema-projeto`** e **`manim-color-theming`**
3. **Declare a geometria antes de desenhar.** Um bloco de constantes nomeadas no
   topo do arquivo, com o quadro real escrito no comentário (x ∈ [−7,11, +7,11],
   y ∈ [−4, +4]). **[DECK]** todos os 12 arquivos de cena em produção abrem com
   60–110 linhas assim, e é o que permite revisar enquadramento **sem
   renderizar**. → **`manim-layout-posicionamento`**
4. **Confira cada assinatura** antes de usá-la. `bin/mx show` custa 0,2 s.
   → **`manim-api-discovery`**
5. **Renderize rápido e OLHE.** `-q l --format png`. → **`manim-verificacao-visual`**
6. **Só então** o render final, `-q h --codec nvenc`. → **`manim-render-api`**

Duas regras que valem em todos os passos, e que **[DECK]** foram pagas caro:

- **Todo número da cena vem de UM arquivo** (um JSON ao lado), lido por função
  que levanta erro **listando os ids disponíveis**. Redigitar um número dentro de
  uma cena é como o slide passa a dizer `$9,51` e o vídeo `$9,48` na parede.
  E um módulo importado por todas as cenas **não pode falhar no import** por
  causa de um dado que a maioria delas não usa: falhe tarde, na função que
  consome. → **`manim-tema-projeto`**
- **O código da cena é o produto tanto quanto o mp4.** Docstring de módulo com a
  tese em uma frase, docstring por classe, comentário por ato dizendo o recado
  **falado**, e comentário explicando *por que* uma escolha estranha existe —
  sempre no ponto onde o próximo editor "consertaria" de volta.

---

## 15. O que NÃO fazer

- **Não rode `pip install manim`.** Já está nos dois venvs; `bin/setup` cuida.
- **Não use `python cena.py`.** Ele sai 0 sem gerar nada (§10.8).
- **Não chame `.venv/bin/manim`, `.venv/bin/manimgl` ou `.venv/bin/mx` direto.**
  Perde LaTeX (`dvisvgm`), perde a dGPU, perde o `PYTHONPATH`, e o `mx` do venv
  ainda diz "Ambiente pronto" mentindo (§3.4).
  **Exceção única:** subcomandos que só imprimem configuração e não tocam em
  LaTeX, GPU nem render — `manim cfg show` é o caso. Ainda assim prefira
  `bin/manim cfg show`, por uniformidade e porque o resultado depende do cwd (§5).
- **Não rode `bin/mx` de fora da raiz do projeto** sem saber que está abrindo mão
  do `manim.cfg` — encoding paralelo cai de 4 para 1, a resolução muda e o mp4
  aparece em outro lugar (§5). *(`bin/setup` é a exceção: ele faz `cd` sozinho.)*
- **Não confie no exit code do `mx doctor`.** Só quatro checks o derrubam, e
  LaTeX quebrado **não é um deles** (§4.1).
- **Não escreva hex sem `#`.** Três dígitos funcionam; sem `#` quebra (§11).
- **Não misture `from manim import *` com `from manimlib import *`.**
- **Não presuma que `--renderer=opengl` acelera.** **[MEDIDO]** com `mx bench -q h`:
  `geometry cairo+NVENC 15,80 s` × `geometry opengl+NVENC 15,97 s` — o próprio
  bench imprime *"renderer opengl custa 1% vs cairo"*. (Esta execução rodou com a
  máquina ocupada, então os absolutos estão inflados; o **sinal** é o que importa.)
  Números atuais e a decisão de codec: **`manim-gpu-encoding`**, que é dona do
  assunto — meça, não repita. *(A skill `manim-3d-camera` ainda carrega um
  "opengl economiza ~19%" que não reproduz. Onde divergirem, vale
  `manim-gpu-encoding`.)*
- **Não rode `mx bench` de leve.** Ele renderiza 5 cenários (`NumberPlane` com
  passo 0,25, 700 `Dot`, 11 `FunctionGraph`…) e ocupa CPU e GPU por minutos. Numa
  máquina que está fazendo outra coisa, ele é a diferença entre "lento" e
  "travado".
- **Não dispare renders em paralelo com NVENC sem contar as sessões.** O limite
  desta placa se conta em **sessões de encode**, e a conta é
  `processos × max_inflight_encoders`. Com os defaults do `batch_render.py`
  (`-j 4`, `--encoders 2`) dá exatamente 8, sem folga. Conta e teto:
  **`manim-gpu-encoding`**.
- **Não invente nome de método.** `bin/mx show <Classe>` custa 0,2 s.
- **Não renderize duas vezes o mesmo trabalho.** Se você já iterou em `--rapido`/
  `-q l`, o arquivo de entrega **é o mesmo caminho**: refazer sem a flag é
  obrigatório, senão fica 720p30 no lugar do 1080p60 e ninguém vê até o projetor.
  **[DECK]** o teste é uma linha de `ffprobe` que espera **uma** linha de saída.

---

## 16. Antes de commitar ou publicar

```bash
tools/check_publishable.sh
```

**[FONTE]**, quatro coisas que `grep -rn` não pega:

1. **caminho de máquina dentro dos `.json.gz`** de `api/` — ele usa `zgrep` para
   os `.gz`, porque `grep -r` normal nunca acha nada dentro de um binário mesmo
   quando o `/home/usuario/` está lá;
2. padrões de credencial (`ghp_`, `github_pat_`, `sk-`, `AKIA`, `AIza`, `xox`,
   `glpat-`, chave privada PEM);
3. arquivo acima de **50 MiB** (limite do GitHub), e imprime o total versionado;
4. bit de execução em `bin/mx`, `bin/manim`, `bin/manimgl`, `bin/setup`.

Exit ≠ 0 se algo aparecer. Detalhe de implementação que vale copiar: ele trata
`grep -c` com cuidado, porque **`grep -c` imprime `0` E sai 1** quando não acha —
um `|| echo 0` displicente produziria `"0\n0"` e quebraria a comparação numérica.

Regenerar o índice depois de atualizar o Manim:

```bash
bin/mx api-dump                          # api/manim-ce-*  (CE, do .venv)
bin/mx api-diff                          # api/ce-vs-gl.md
```

O dump do **ManimGL** não sai por `bin/mx` (o wrapper entra sempre no venv da CE)
nem por `python -m manimx.cli` no `.venv-gl` (o `import manimlib` mata o argparse,
§12). Receita que funciona:

```python
# dump_gl.py — rode com .venv-gl/bin/python
import sys, warnings; warnings.filterwarnings("ignore")
sys.argv = [sys.argv[0]]                       # manimlib parseia sys.argv NO IMPORT
sys.path.insert(0, "/caminho/para/o/projeto/manim")
from manimx.introspect import dump_api
print(dump_api("api", "manimlib", label="manimgl"))
```

### 16.1 O contrato de descoberta invertido

**[DECK]** — vale saber, porque quebra fora daqui. Projetos consumidores
localizam **este** repositório assim, nesta ordem:

```
$MANIM_HOME  →  ~/Projects/manim  →  candidatos  →  find ~ -maxdepth 3 -path '*/bin/mx'
```

e confirmam com `[ -x "$1/bin/mx" ] && [ -d "$1/manimx" ]`. **Se o layout deste
repositório mudar — `bin/mx` executável, pasta `manimx/` — consumidores externos
quebram em silêncio.** Trate esses dois caminhos como API pública.

---

## 17. Ficha desta máquina — copie daqui, não da memória

Levantada em **2026-08-19**, cada linha com o comando que a produziu.

| Item | Valor | Comando |
|---|---|---|
| ManimCE | **0.21.0** | `bin/mx doctor` |
| ManimGL | **1.7.2** wgpu/Vulkan (git master) | `bin/mx doctor` |
| Python (ambos os venvs) | 3.12.3 | `.venv/bin/python -V` |
| GPU | RTX 4070 Laptop, **8188 MiB**, driver 580.159.03 / CUDA 13.0 | `bin/mx gpu` |
| CPU / RAM | i9-14900HX, 32 threads / 31 GiB | `lscpu`, `free -h` |
| Encoders PyAV | h264_nvenc, hevc_nvenc, av1_nvenc, libx264, libx265, libvpx-vp9, qtrle, prores_ks, png, gif | `bin/mx gpu` |
| LaTeX | TinyTeX (TeX Live **2026**), **203** pacotes | `tlmgr list --only-installed \| wc -l` |
| Symlinks do TinyTeX em `~/.local/bin` | **78** — com `latex`, **sem `dvisvgm`** | `ls -la ~/.local/bin \| grep -c TinyTeX` |
| Fontes visíveis ao Pango | **411** famílias (`Inter`/`Arial`/`Helvetica` AUSENTES) | `manimpango.list_fonts()` |
| Palco padrão | **14,2222 × 8,0** unidades (`frame_x_radius` 7,1111) | `config.frame_width` |
| Qualidades | `l` 854×480@15 · `m` 1280×720@30 · `h` 1920×1080@**60** · `p` 2560×1440@60 · `k` 3840×2160@60 | `bin/mx presets` |
| Temas | `3b1b` `whiteboard` `paper` `slate` `solarized-dark` `solarized-light` `nord` `transparent` | `bin/mx presets` |
| Símbolos indexados (CE) | 5.523 — 338 classes, 285 funções, 4.900 constantes, 2.662 nomes únicos | `awk` sobre `api/manim-ce-index.tsv` |
| Métodos indexados (CE) | 50.945 em 334 classes — **1.901 próprios**, 49.044 herdados | `awk` sobre `api/manim-ce-methods.tsv` |
| `from manim import *` | **588** nomes | `api/manim-ce-toplevel.md` |
| Categorias | **41** | `awk -F'\t' 'NR>1{print $3}' … \| sort -u \| wc -l` |
| `vulkaninfo` | **AUSENTE** | `command -v vulkaninfo` |
| `glxinfo` | `/usr/bin/glxinfo` | `command -v glxinfo` |

Três leituras enganosas, todas verificadas:

1. **`mx gpu` diz `OpenGL (padrão) : NVIDIA`** — é artefato de medição. O `mx`
   roda dentro do ambiente já offloadado pelo próprio wrapper. Num shell limpo o
   padrão é **Intel** (§3.2).
2. **`mx gpu` diz `Adapters wgpu : -`** — falso-negativo permanente:
   **[FONTE]** `manimx/gpu.py` faz `import wgpu` dentro do venv da **CE**, que não
   tem `wgpu`. A listagem real sai do outro venv:
   ```bash
   .venv-gl/bin/python -c "import wgpu; [print(a.summary) for a in wgpu.gpu.enumerate_adapters_sync()]"
   ```
   (**[MEDIDO]**: 4 adapters, a RTX 4070 entre eles.)
3. **`vulkaninfo` não existe nesta máquina** — não o cite como diagnóstico; use o
   snippet acima. *(A skill `manimgl-3b1b` ainda manda checar `vulkaninfo`. Onde
   divergirem, vale esta: `command -v vulkaninfo` não devolve nada.)*

---

## 18. Onde esta skill para

Ela responde *onde*, *como disparar* e *qual porta*. Ela **não** responde:

- como desenhar, animar, posicionar ou colorir → §13;
- por que **este** traceback aconteceu → **`manim-troubleshooting`**;
- se **esta** assinatura existe → **`manim-api-discovery`**;
- quanto tempo **este** codec leva → **`manim-gpu-encoding`** (meça, não repita).

E ela guarda quatro divergências abertas com skills irmãs, listadas aqui para que
ninguém as re-litigue sem evidência nova. Em todas, a medição está deste lado:

| Assunto | Diz a irmã | Diz esta skill | Prova |
|---|---|---|---|
| `custom_config.yml` vem com NVENC? | `manimgl-3b1b`: sim | **não**, é `libx264` de propósito | o arquivo (§12) |
| `vulkaninfo` como diagnóstico | `manimgl-3b1b`: use | **não existe aqui** | `command -v` (§17) |
| `-r` ignora o `-q`? | `manim-render-api`: sim | **não** — só a resolução; o fps vem do `-q` | `720p15` (§7.3) |
| opengl economiza ~19%? | `manim-3d-camera`: sim | **não reproduz** (custa 1%) | `mx bench` (§15) |

E duas correções que esta skill fez em **si mesma**, para que não voltem:

- **`mx doctor` tem QUATRO checks fatais, não cinco.** O de LaTeX é registrado
  com `fatal=False` justamente no caminho de falha (§4.1). Versões anteriores
  desta skill — e a auditoria — diziam cinco.
- **`Shader` & cia. estão em `category=renderer`, não em `mobject/opengl`**
  (§13.7). O comando que a versão anterior sugeria não os encontrava.
