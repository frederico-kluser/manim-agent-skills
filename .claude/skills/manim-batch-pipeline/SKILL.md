---
name: manim-batch-pipeline
description: >-
  Renderizar MUITAS cenas do Manim de uma vez e transformar a saída bruta em
  ARTEFATOS entregáveis, de forma reprodutível: paralelismo multi-processo
  (`tools/batch_render.py`), descoberta automática de cenas, o contrato JSON,
  o script de exportação (slug do nome da classe, cópia para a pasta do
  consumidor, extração dos dois pôsteres), a conferência barata do lote e a
  política do que entra no git. Use quando pedirem "renderiza tudo", "gera
  todos os vídeos da aula", "processa essa pasta de cenas", "um vídeo por linha
  do CSV", "automatiza a entrega", "monta isso no CI", "quantos workers eu
  uso?", "o lote falhou pela metade", "o LaTeX quebrou quando paralelizei", "a
  segunda cena do lote saiu preta no preto", "o mp4 sumiu depois do render",
  "os vídeos ficaram com resoluções diferentes", "o que eu commito e o que eu
  reconstruo?". Cobre os quatro modos de falha REAIS deste cenário — a varredura
  global de `delete_nonsvg_files` entre workers, o `set_default` que vaza porque
  o `ProcessPoolExecutor` REUSA o processo, o `module_name` que colide quando
  dois arquivos têm o mesmo nome de arquivo, e a ordem não determinística do
  JSON — e a lista do que `tools/batch_render.py` NÃO faz (tema, formato,
  seções, nome de saída), que é o que decide entre lote paralelo e laço serial.
  NÃO use para: renderizar UMA cena e achar o caminho da saída (skill
  `manim-render-api`); escolher codec, medir GPU ou o teto de sessões NVENC
  (skill `manim-gpu-encoding`, dona do assunto); o cache por dentro (skill
  `manim-performance-cache`); cor, tema e fundo como decisão visual (skill
  `manim-color-theming`); cortar UMA cena em partes para slide (skill
  `manim-presentation-parts`); olhar o frame e julgar se ficou certo (skill
  `manim-verificacao-visual`); traceback de uma cena que quebrou (skill
  `manim-troubleshooting`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Lote e pipeline — de N cenas a N artefatos, sem surpresa

Esta skill trata do que acontece **entre** "a cena está pronta" e "o artefato
está no lugar onde alguém vai consumir". São três problemas distintos, e
confundi-los é a causa da maioria dos lotes que dão errado:

| Problema | Pergunta | Onde nesta skill |
|---|---|---|
| **Vazão** | como rodar N cenas sem serializar nem travar a máquina? | §1 a §5 |
| **Reprodutibilidade** | por que dois lotes do mesmo código diferem? | §6 e §7 |
| **Artefato** | como a saída bruta do Manim vira o arquivo que o consumidor espera? | §8 a §11 |

> **Método e data.** Tudo marcado **[FONTE]** foi conferido lendo o código —
> `tools/batch_render.py`, `manimx/render.py`, `manimx/cli.py`, o ManimCE 0.21.0
> em `.venv/`, a stdlib do CPython 3.12.3 em `/usr/lib/python3.12/` (é o mesmo
> interpretador do venv: `pyvenv.cfg` aponta `home = /usr/bin`), e o
> `api/manim-ce-index.tsv`. **[MEDIDO]** vem de execução anterior, com a data.
> **[DECK]** vem do projeto consumidor `~/Projects/aulas`, que mediu — eu não
> reproduzi. Nesta revisão (2026-08-19) **nada foi renderizado**; o que não pôde
> ser conferido por leitura está listado em §15.

---

## 0. A primeira decisão: lote paralelo ou laço serial?

Antes de escolher `-j`, escolha a **ferramenta**. As quatro existem e resolvem
coisas diferentes:

| Ferramenta | Paralelismo | Ganha quando | Perde porque |
|---|---|---|---|
| `tools/batch_render.py` | processos de verdade | muitas cenas, todas com a **mesma** configuração | não expõe tema, formato, `-o`, fps, resolução, transparência, seções |
| `bin/mx render ARQ.py --all` | nenhum (serial, 1 processo) | poucas cenas de um arquivo só | `set_default` vaza de uma cena para a seguinte (§5) |
| **`bin/mx render` num laço do shell**, uma invocação por cena | nenhum, mas **um processo por cena** | você precisa de `--theme`, `-o`, `--format` ou de isolamento total | paga o import do Manim (~1 s) por cena |
| orquestrador próprio com `render_scene` | você escolhe | cada cena precisa de kwargs diferentes | você reimplementa §4 e §5 na mão |

**O detalhe que decide, e que não está em lugar nenhum:** `tools/batch_render.py`
aceita **nove** flags — `--scenes -q --codec --renderer --media-dir --no-cache
--encoders -j --shared-tex` (mais `--json` e `--dry-run`) — e o `_job` monta o
`payload` só com essas **[FONTE: `tools/batch_render.py:170-176`]**. Não existe
`--theme`, `--format`, `-o/--output`, `--fps`, `-r/--resolution`,
`-t/--transparent`, `--background`, nem `--save-sections`. O `bin/mx render`
tem todas essas **[FONTE: `manimx/cli.py:457-476`]**.

É exatamente por isso que o deck consumidor (`~/Projects/aulas`,
`scripts/render-videos.sh:173`) **não usa o lote paralelo**: as cenas dele
precisam de `--theme whiteboard` como rede de segurança contra texto branco em
fundo branco, e o lote não sabe passar tema. Ele roda um laço serial de
`bin/mx render`, um processo por cena. Isso custa tempo e compra três coisas:
o tema, o isolamento contra o vazamento de `set_default` (§5) e um nome de
arquivo por cena. **Lote paralelo não é sempre a resposta certa.**

Regra prática:

- **mesma config para todas as cenas, e são muitas** → `tools/batch_render.py`;
- **precisa de tema, formato, ou nome de saída por cena** → laço de `bin/mx render`;
- **poucas cenas, um arquivo** → `bin/mx render ARQ.py --all`, sabendo do §5.

---

## 1. A regra estrutural: processos, nunca threads — e o que o processo *não* protege

**Nunca renderize duas cenas em paralelo dentro do mesmo processo Python.**
O `config` do Manim é um singleton global mutável: resolução, `media_dir`,
codec, diretórios e cache são estado compartilhado. Threads corrompem tudo, em
silêncio. É por isso que `manimx.render.render_many` é sequencial **de
propósito** **[FONTE: `manimx/render.py:543-546`]**, e é isso que
`tools/batch_render.py` resolve com `concurrent.futures.ProcessPoolExecutor`.

Duas consequências que quase ninguém tira, e que valem o resto desta skill:

**(a) `tempconfig` protege o `config`, e só o `config`.** Toda função de
`manimx.render` roda dentro de `with tempconfig(cfg)`
**[FONTE: `manimx/render.py:419`]**, então as chaves de config voltam ao normal
— inclusive em caso de exceção. O que **não** volta: `Text.set_default(...)` e
os outros defaults de classe, que são mutação de `classmethod` e sobrevivem ao
`with`. Isso é o §5.

**(b) Um processo do pool NÃO é um processo por cena.** O
`ProcessPoolExecutor` cria `max_workers` processos e cada um roda um laço
`while True: call_item = call_queue.get(block=True)` **[FONTE:
`/usr/lib/python3.12/concurrent/futures/process.py:249-262`]**. Ou seja: um
worker que renderizou a cena A **continua vivo** e renderiza depois a cena D,
com todo o estado de módulo que A deixou para trás. "Multi-processo" isola
*entre* workers, não *entre tarefas*.

---

## 2. `tools/batch_render.py` — o contrato completo

```bash
source bin/manim-env.sh; manimx_use_ce; manimx_enable_gpu

.venv/bin/python tools/batch_render.py scenes/exemplos.py -q h --codec nvenc -j 3
.venv/bin/python tools/batch_render.py scenes/ -q m --codec x264 -j 8
.venv/bin/python tools/batch_render.py 'scenes/*.py' --scenes Intro Fim
.venv/bin/python tools/batch_render.py scenes/ --dry-run
.venv/bin/python tools/batch_render.py scenes/ --json > resultado.json
```

O `source bin/manim-env.sh; manimx_use_ce` não é enfeite: ele põe o TinyTeX no
`PATH` (sem isso `MathTex` falha), aponta o venv e exporta
`PYTHONPATH=$MANIMX_ROOT` **[FONTE: `bin/manim-env.sh:13-26, 73-77`]**. É a
única exceção legítima à regra "não chame `.venv/bin/...` direto" de
`manim-project` §13 — o script não tem wrapper em `bin/`, então você monta o
ambiente na mão antes.

### 2.1 As flags e os defaults REAIS

Lidos do `argparse` **[FONTE: `tools/batch_render.py:132-148`]**:

| Flag | Default | O que faz |
|---|---|---|
| `paths` (posicional, 1+) | — | arquivos `.py`, diretórios ou globs |
| `--scenes N [N…]` | todas | filtra por nome de classe |
| `-q, --quality` | `h` | `l/m/h/p/k` ou apelidos (`1080p`, `4k`, `draft`…) |
| `--codec` | **`nvenc`** | chave de `CODEC_PRESETS` (`bin/mx presets`) |
| `--renderer` | `cairo` | `cairo` ou `opengl` |
| `--media-dir` | `media` | **relativo ao CWD** — veja §7 |
| `--no-cache` | desligado | `disable_caching` (partial movies) |
| `--encoders N` | **2** | `max_inflight_encoders` **dentro** de cada worker |
| `-j, --jobs N` | `max(1, min(4, cpus//4))` = **4** nesta máquina (32 CPUs) | processos |
| `--shared-tex` | desligado | volta ao `media/Tex` único |
| `--json` | desligado | imprime o relatório estruturado |
| `--dry-run` | desligado | lista o que faria e sai 0 |

Exit code: `0` só se **todas** as cenas passaram
**[FONTE: `tools/batch_render.py:223`]**.

Duas correções ao que o próprio arquivo diz sobre si mesmo — o docstring dele
está desatualizado e **não deve ser copiado**:

- ele documenta `--all` (linha 13). **Essa flag não existe**; o comportamento
  padrão já é "todas as cenas de todos os arquivos";
- ele diz "passar de ~3 encoders NVENC ao mesmo tempo costuma falhar"
  (linhas 20-24). Número obsoleto — a conta certa é em **sessões**, e está no §3.2.

### 2.2 O que ele silencia — e por que isso importa

Duas linhas do `_job` apagam justamente os avisos que dizem que o vídeo saiu
errado:

```python
warnings.filterwarnings("ignore")          # tools/batch_render.py:79 e :152
...
verbosity="CRITICAL",                      # tools/batch_render.py:113
```

**[FONTE]**, as três linhas. Com `verbosity="CRITICAL"` você não vê o
`WARNING` de fonte ausente caindo para Noto Sans (`manim-project` §10.4), nem
nada abaixo de crítico **que venha do logger do Manim**. O lote fica limpo e
mentiroso: **exit 0, 60 mp4 no disco, e a tipografia trocada em todos**. A
defesa é §9 — conferência explícita depois do lote, porque o log não vai te
contar.

**Correção — o aviso de NVENC NÃO é um desses.** Uma versão anterior o listava
junto com o da fonte. Ele sai por outro logger, que `config.verbosity` não
governa:

```python
# manimx/gpu.py:44
logger = logging.getLogger("manimx.gpu")
# manimx/gpu.py:527 e :542
logger.warning("manimx: %s", msg)   # "NVENC indisponível… continua em libx264 (CPU)"
```

`verbosity` é a configuração do logger **do Manim**; `manimx.gpu` é um logger da
stdlib, independente. Se o aviso de NVENC não apareceu no seu lote, a causa é a
configuração de logging do processo (ou o `stderr` do worker sendo engolido pelo
pool), **não** o `verbosity="CRITICAL"`. Isso importa na prática: é a diferença
entre "o lote inteiro caiu para CPU e ninguém viu" e "o aviso estava lá, no
worker errado".

E se você quer que a queda para CPU **falhe** em vez de avisar,
`enable_nvenc(..., strict=True)` levanta `RuntimeError` no lugar do
`logger.warning` (`gpu.py:525-526, 540-541`).

### 2.3 Descoberta de arquivos: as três formas e as três armadilhas

`_discover` **[FONTE: `tools/batch_render.py:41-59`]** trata cada argumento em
três casos:

```python
p = Path(raw)
if   p.is_dir():  files.extend(sorted(q for q in p.rglob("*.py")
                                      if not q.name.startswith("_")))
elif p.is_file(): files.append(p)
else:             files.extend(sorted(Path().glob(raw)))
```

1. **Diretório → `rglob` recursivo.** Ele desce a árvore inteira e pega
   *qualquer* `.py`, inclusive `conftest.py`, `setup.py` e o seu `tema.py`.
   O único filtro é o prefixo `_`. Consequência direta: **um `tema.py` que
   define uma classe-base `CenaAula(Scene)` vira uma "cena" e é renderizado**
   — 35 s de mp4 que ninguém consome. Isso é o mesmo mecanismo que
   `manim-presentation-parts` explora ao exigir que o mixin **não** herde de
   `Scene`: `load_scene_classes` filtra por `issubclass(obj, Scene) and
   obj.__module__ == module_name` **[FONTE: `manimx/render.py:141-145`]**, e
   uma classe-base passa nos dois testes.
   **Defesa:** aponte para um glob restrito (`'manim/aula_*.py'`), ou renomeie
   a base para `_tema.py`, ou passe `--scenes`.
2. **Glob → `Path().glob(raw)`, relativo ao CWD.** Padrão **absoluto** levanta
   `NotImplementedError: Non-relative patterns are unsupported`
   **[FONTE: `/usr/lib/python3.12/pathlib.py:1092`]** — traceback cru, sem
   mensagem amigável. Use caminho relativo, ou passe o diretório.
3. **Caminho que não existe** cai no ramo do glob, não casa com nada, e o lote
   termina em `nenhum arquivo .py encontrado` + exit 1. Um typo não faz barulho
   proporcional ao estrago.

A deduplicação é por caminho **resolvido** (`f.resolve()`), então o mesmo
arquivo passado duas vezes só entra uma. Ela **não** deduplica por
`(module_name, cena)` — o que nos leva à armadilha seguinte.

### 2.4 A colisão de `module_name` — dois arquivos, um diretório de saída

O diretório de saída sai de `video_dir = {media_dir}/videos/{module_name}/{quality}`
(`manim.cfg:22`), e:

```python
module_name = config.get_dir("input_file").stem if config["input_file"] else ""
```

**[FONTE: `manim/scene/scene_file_writer.py:263`]** — é o **stem do arquivo**,
sem nenhum componente de diretório. Portanto:

```
projeto/a/cena.py::Intro  →  media/videos/cena/1080p60/Intro.mp4
projeto/b/cena.py::Intro  →  media/videos/cena/1080p60/Intro.mp4   ← o MESMO
```

Com `rglob` recursivo (§2.3), essa é uma colisão fácil de produzir: dois
capítulos, dois diretórios, o mesmo `intro.py`. O segundo render sobrescreve o
primeiro, **sem erro, sem aviso, com `success: true` nos dois**. E como
`as_completed` não garante ordem (§2.5), qual dos dois sobrevive muda a cada
execução.

Sintoma correlato, que você vai encontrar no disco deste projeto:
`media/videos/1080p60/` — sem componente de módulo. É o caso `module_name = ""`,
que acontece quando `input_file` não está definido: uma classe criada
dinamicamente com `type()` fora de um arquivo, ou um render disparado de um
REPL. `render_scene` tenta deduzir `input_file` do
`sys.modules[scene_class.__module__].__file__` **[FONTE: `manimx/render.py:362-366`]**;
quando não consegue, todas as cenas caem no mesmo balde.

**Defesa:** nomes de arquivo únicos no lote inteiro, ou um `--media-dir` por
subárvore, ou — melhor — não confie no layout do `media/` e exporte por nome
(§8).

### 2.5 O JSON: a forma completa, a assimetria e a ordem

```bash
.venv/bin/python tools/batch_render.py scenes/ -q h --json > out.json
```

```json
{
  "total": 6, "ok": 6, "failed": 0, "elapsed_s": 57.9, "jobs": 4,
  "results": [
    {"scene_name": "OlaManim", "success": true,
     "output_file": "/.../media/videos/exemplos/1080p60/OlaManim.mp4",
     "image_file": null, "sections": [],
     "elapsed_s": 7.18, "renderer": "cairo", "codec": "h264_nvenc",
     "quality": "h", "resolution": [1920, 1080], "frame_rate": 60.0,
     "num_animations": 3, "error": null, "traceback_text": null,
     "file": "/.../scenes/exemplos.py", "wall_s": 7.2}
  ]
}
```

Os 14 primeiros campos vêm de `RenderResult.as_dict()`
**[FONTE: `manimx/render.py:79-100`]**; `file` e `wall_s` são acrescentados
pelo `_job` **[FONTE: `tools/batch_render.py:124-125`]**.

**Três coisas que quebram um consumidor ingênuo:**

**(a) A ordem de `results` é a ordem de TÉRMINO, não a de submissão.** O laço é
`for i, fut in enumerate(cf.as_completed(futures), 1): results.append(...)`
**[FONTE: `tools/batch_render.py:202-204`]**. Com `-j > 1` a lista muda de
ordem entre execuções idênticas. Um pipeline que faz `.results[0]` está
quebrado e só vai descobrir num dia ruim. Sempre indexe por nome:

```bash
jq -r '.results | map({(.scene_name): .output_file}) | add' out.json
jq -S '.results |= sort_by(.file, .scene_name)' out.json > out.ordenado.json
```

**(b) O resultado de falha tem duas formas diferentes.** Quando a **cena**
levanta, `render_scene` captura por dentro e devolve um `RenderResult`
completo, com `traceback_text` preenchido
**[FONTE: `manimx/render.py:452-457`]**. Quando falha **antes** da cena — arquivo
inexistente, nenhuma subclasse de `Scene`, nome de cena errado, erro de import
do módulo —, `render_file` levanta, o `_job` captura e monta um dict com
**quatro chaves apenas**: `scene_name`, `success`, `error`, `output_file`
**[FONTE: `tools/batch_render.py:117-125`]**. Não há `codec`, `resolution`,
`traceback_text`, `elapsed_s`. Um `jq '.results[].resolution'` estoura no
primeiro erro de import. Escreva defensivo:

```bash
jq -r '.results[] | select(.success | not) | "\(.scene_name)\t\(.error)"' out.json
jq -r '.results[] | select(.success) | .output_file' out.json
```

**(c) `--dry-run --json` NÃO imprime JSON.** O `if args.dry_run:` retorna antes
do bloco de JSON **[FONTE: `tools/batch_render.py:192-196`]**; a saída é
`arquivo.py::Cena`, uma por linha, e depois um resumo em prosa. Um pipeline que
faz `--dry-run --json | jq` morre em parse error. Para listar de forma
estruturada, use `bin/mx scenes ARQ.py --json`, que devolve
`[{"name", "bases", "doc"}]` **[FONTE: `manimx/cli.py:188-206`]**.

---

## 3. Paralelismo: quantos, e de quê

### 3.1 Existem dois `-j`, e eles significam coisas opostas

Esta é a confusão que mais custa tempo aqui:

| Comando | `-j` significa | Unidade |
|---|---|---|
| `tools/batch_render.py -j 4` | **workers** — processos do pool | processo |
| `bin/mx render ... -j 4` | **`--parallel-encoders`** = `max_inflight_encoders` | thread de encode **dentro** de um processo |

**[FONTE: `tools/batch_render.py:142` e `manimx/cli.py:473`]**. No lote, o
equivalente ao `-j` do `mx render` chama-se `--encoders`. Escrever `-j 8` num
lote achando que está pedindo encoders paralelos dá 8 **processos**, cada um
com 2 encoders = 16 sessões de GPU pedidas. É assim que se derruba o encoder
sem entender por quê.

### 3.2 A conta que decide: sessões, não workers

O limite do NVENC não se conta em workers. Conta-se em **sessões de encode por
GPU**, e o teto desta placa foi medido em **8**
(`manim-gpu-encoding` §7, que é a **dona do assunto** — vá lá para o método, o
diagnóstico com `nvidia-smi` e a matriz de codecs).

```
sessões = processos_renderizando × max_inflight_encoders
```

Aplicando aos defaults desta ferramenta: `-j 4` × `--encoders 2` = **8 sessões
na mosca**, sem folga nenhuma para o resto da máquina — navegador com vídeo,
videochamada, gravador de tela, outro agente renderizando. Some qualquer um
desses e o render morre com:

```
ExternalError: [Errno 542398533] Generic error in an external library:
  'avcodec_open2("h264_nvenc", {...})'
```

Que **não** quer dizer "opção inválida"; quer dizer "não há sessão livre".

**Recomendação: mire em 6, deixando 2 de folga** — `-j 3 --encoders 2`.

E repare no defeito do aviso embutido: ele só dispara com
`args.jobs > 4` **[FONTE: `tools/batch_render.py:182`]**, isto é, olha para
workers e ignora `--encoders`. Nos defaults (`-j 4 --encoders 2`, que já são 8
sessões) **nenhum aviso é impresso**. Não confie nele.

Complemento importante, também de `manim-gpu-encoding` §7:
`validate_encoder()` **não protege** contra o teto. Ele abre uma sessão, testa
e fecha; se as sessões acabarem entre o teste e o render, o `avcodec_open2` do
partial movie falha. É uma corrida, não um bug.

### 3.3 Memória: a conta que estoura antes da VRAM

Cada job de encode em voo segura oito frames RGBA. Em 1080p isso é
1920×1080×4 = 8,29 MB × 8 ≈ **66 MB por job**
(`manim-gpu-encoding` §8, conferido lá contra o comentário do próprio Manim).
Portanto:

```
RAM de filas ≈ processos × encoders × 66 MB          (1080p)
```

`-j 4 --encoders 2` ≈ **530 MB** só de fila, em 1080p. Em 4K, quatro vezes
isso: ≈ 2,1 GB. Em 4K com `-j` alto o que estoura é a **RAM**, não a VRAM — e o
sintoma é o OOM killer matando um worker, o que o `ProcessPoolExecutor` reporta
como `BrokenProcessPool` e derruba o lote inteiro, não só a cena.

### 3.4 O gargalo costuma ser a cena mais lenta, não o codec

**[MEDIDO — 2026-08-19, não re-executado nesta revisão]**, nesta máquina
(32 threads, RTX 4070 Laptop), sobre as 6 cenas de `scenes/exemplos.py`,
1080p60, sem cache:

| Configuração | Tempo total |
|---|---|
| `-j 4 --codec nvenc` | 57,9 s |
| `-j 4 --codec x264` | 59,2 s |

Praticamente empatados. O motivo está na distribuição, não no codec: duas
cenas — `TangenteViva` (`always_redraw` num `ValueTracker`) e `Superficie3D`
(3D) — consomem 46 s e 52 s **sozinhas**, e as outras quatro terminam em ~6 s.
Com 4 workers, o lote inteiro dura o que dura a cena mais longa mais um
respingo. Trocar o encoder mexe em ~7% de uma etapa que não é o gargalo.

A lição operacional: **antes de subir `-j`, descubra qual cena domina.** Um
lote de 60 cenas com uma de 90 s tem um piso de 90 s, com qualquer `-j`. Divida
a cena, ou aceite o piso. O `--json` já dá o material:

```bash
jq -r '.results | sort_by(-.wall_s) | .[:5][] | "\(.wall_s)s\t\(.scene_name)"' out.json
```

Para saber **onde** o tempo foi dentro da cena (rasterização × encode × junção),
o instrumento é `bin/mx bench` e o assunto é de `manim-gpu-encoding`.

### 3.5 Quando NÃO paralelizar

- **`--codec transparent`, `webm`, `gif`, `png`** — não usam NVENC de qualquer
  forma **[FONTE: `manimx/render.py:398`]**, então o teto de sessões some, mas
  o encode é todo CPU e vira a disputa entre workers;
- **cenas que dependem de LaTeX pesado** — cada worker paga a compilação do
  preâmbulo separadamente (§4.4);
- **lote com temas diferentes** — o vazamento do §5 é pior com worker reuso;
- **CI num runner de 2 vCPUs** — `-j 1` é honesto; cada worker do Manim já é
  multi-thread (Cairo + encoder), e sobrescrever isso é *thrashing*, não ganho.

---

## 4. Corrida de LaTeX entre workers — o mecanismo exato, e as três correções

### 4.1 Não é colisão de nome. É uma varredura global.

O erro que aparece:

```
FileNotFoundError: media/Tex/cd13fedd3f96aaa7.aux
```

**[MEDIDO, execução anterior]** com `-j 2`: serial dava 6/6; paralelo dava 5/6,
de forma não determinística.

A causa, lida no fonte **[FONTE:
`manim/utils/tex_file_writing.py:269-282`]**:

```python
def delete_nonsvg_files(additional_endings: Iterable[str] = ()) -> None:
    tex_dir = config.get_dir("tex_dir")
    file_suffix_whitelist = {".svg", ".tex", *additional_endings}
    for f in tex_dir.iterdir():
        if f.suffix not in file_suffix_whitelist:
            f.unlink()
```

E quem a chama **[FONTE: `tex_file_writing.py:70-71`]**, ao fim de **cada**
`tex_to_svg_file`:

```python
if not config["no_latex_cleanup"]:
    delete_nonsvg_files()
```

Ou seja: quando o worker B termina de compilar **a fórmula dele**, ele apaga
todo arquivo que não seja `.svg`/`.tex` do diretório **inteiro** — inclusive o
`.aux`, o `.log` e o `.dvi` que o worker A está usando neste instante para
outra fórmula. Não é uma colisão de hash; é um `rm` global disparado por um
vizinho. Por isso o erro é errático e proporcional a `-j`.

### 4.2 Correção A — um `tex_dir` por worker (o que a ferramenta faz)

`tools/batch_render.py` **já corrige**, isolando `tex_dir` e `text_dir`
**[FONTE: `tools/batch_render.py:97-100`]**:

```python
slot = _worker_slot()
media = Path(payload["media_dir"]).resolve()
overrides["tex_dir"]  = str(media / "_workers" / f"w{slot}" / "Tex")
overrides["text_dir"] = str(media / "_workers" / f"w{slot}" / "texts")
```

**Onde esses diretórios ficam é load-bearing.** Eles estão em
`media/_workers/wN/Tex`, e **não** dentro de `media/Tex`. Motivo: aquele
`f.unlink()` da §4.1 **não checa se `f` é diretório**. Um subdiretório dentro
de `media/Tex` faz o `unlink` levantar `IsADirectoryError`, e a partir daí
**toda** renderização de LaTeX posterior quebra — inclusive fora do lote,
inclusive no dia seguinte. Sintoma típico e desconcertante: o lote roda, e
depois `bin/mx doctor` começa a acusar falha em `MathTex`.

Se você escrever seu próprio orquestrador, replique assim:

```python
from manimx.render import render_file

render_file(arquivo, cena, config_overrides={
    "tex_dir":  f"{media_abs}/_workers/w{slot}/Tex",     # FORA de media/Tex
    "text_dir": f"{media_abs}/_workers/w{slot}/texts",
})
```

`--shared-tex` volta ao diretório único — **use só com `-j 1`**.

### 4.3 Correção B — desligar a varredura (`no_latex_cleanup`)

`no_latex_cleanup` é uma chave de config booleana real
**[FONTE: `manim/_config/utils.py:327, 1025-1031`; flag de CLI em
`manim/cli/render/global_options.py:137`]**. Com ela ligada, o
`delete_nonsvg_files` nunca roda e a corrida desaparece na raiz:

```python
render_file(arquivo, cena, config_overrides={"no_latex_cleanup": True})
```

Trade-off honesto: `media/Tex` acumula `.aux`, `.log`, `.dvi`, `.fls` para
sempre (o que, aliás, é útil para depurar LaTeX). E resta uma corrida menor,
que eu **não medi**: dois workers compilando **exatamente a mesma expressão**
ao mesmo tempo escrevem o mesmo `<hash>.dvi` — o nome do arquivo deriva do
`tex_hash` do conteúdo **[FONTE: `tex_file_writing.py:27-33, 108`]**, então
expressões *diferentes* nunca colidem, mas idênticas sim. Por isso a correção A
continua sendo a padrão.

`--no_latex_cleanup` como flag existe no `bin/manim`, **não** no `bin/mx render`
nem no `tools/batch_render.py`. Pela API, é `config_overrides`.

### 4.4 O custo da correção A: N caches de TeX, e um diretório que ninguém limpa

Isolar por worker significa **um cache de LaTeX por slot**. Com `-j 8`, a mesma
fórmula é compilada até 8 vezes na primeira passada. Em lote de cenas com muito
`MathTex`, isso é caro — e é mais um argumento para `-j` modesto.

O índice do worker é **estável entre execuções**, e é isso que salva o cache nas
passadas seguintes. Por quê, lido no CPython: `_worker_slot()` devolve
`multiprocessing.current_process()._identity[0]`
**[FONTE: `tools/batch_render.py:62-72`]**, e `_identity` é atribuído no
**processo pai** como `_current_process._identity + (next(_process_counter),)`
**[FONTE: `/usr/lib/python3.12/multiprocessing/process.py:83-84`]**, com
`_process_counter = itertools.count(1)` global do pai
**[FONTE: idem, linha 423]**. Como cada execução do lote é um pai novo, o
contador reinicia em 1 e o pool de N workers recebe sempre `w1..wN`.

**Duas condições em que essa estabilidade se perde** (e o `media/_workers/`
cresce sem limite):

1. você cria qualquer outro `multiprocessing.Process` antes do pool — o
   contador já andou, e os slots viram `w2..wN+1`;
2. você usa `max_tasks_per_child` (§5.2) — cada worker substituído puxa um
   número novo do contador, então um lote de 60 cenas com
   `max_tasks_per_child=1` gera `w1..w60`, isto é, **60 caches de TeX**.

E ninguém apaga `media/_workers/`. Se o lote fizer parte de um pipeline
recorrente, limpe você:

```bash
rm -rf media/_workers          # antes ou depois do lote, nunca durante
```

---

## 5. O vazamento que o processo NÃO isola: `set_default`

Este é o defeito de lote mais caro que existe neste repositório, porque produz
**vídeo inutilizável com exit code 0**.

### 5.1 O mecanismo, com o exemplo que já está no disco

`scenes/exemplos.py` traz **[FONTE: linhas 84-91]**:

```python
class LousaBranca(Scene):
    def construct(self):
        self.camera.background_color = "#FFFFFF"
        Text.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        VMobject.set_default(color=BLACK)
        ...
```

`set_default` é `classmethod` e muta a **classe**, não a instância nem o
`config`. Nada o desfaz: nem o fim do `construct`, nem o fim do `render()`, nem
o `tempconfig` **[`manim-color-theming` §12.A demonstra a ida e volta]**. E o
`background_color` volta para `BLACK` (o de `manim.cfg:57`) na cena seguinte,
porque *esse* é config.

Junte com o §1(b) — o worker é reusado — e o resultado é determinado:

> Um worker que rodou `LousaBranca` renderiza toda cena subsequente **com traço
> preto sobre fundo preto**. O mp4 sai do tamanho certo, com o número de
> animações certo, `success: true`, e completamente vazio para o olho.

Com `-j 4` e 6 cenas, quais cenas são atingidas depende de qual worker pegou
`LousaBranca` e do que veio depois — **muda a cada execução**. É o defeito
perfeito: silencioso, intermitente e invisível no log (que ainda por cima está
em `CRITICAL`, §2.2).

**Isto é uma armadilha do repositório, não uma hipótese:** `scenes/exemplos.py`
é o alvo padrão dos exemplos desta skill e contém a cena que envenena.

### 5.2 As três defesas, com o custo de cada uma

**(a) Um processo por tarefa** — a defesa completa:

```python
with cf.ProcessPoolExecutor(max_workers=3, max_tasks_per_child=1) as pool:
    ...
```

`max_tasks_per_child` existe desde o 3.11 e força o worker a morrer e ser
substituído **[FONTE: `/usr/lib/python3.12/concurrent/futures/process.py:657,
669-671`]**. Custos, todos verificados no mesmo arquivo:

- **exige start method diferente de `fork`**; sem `mp_context` explícito, o
  Python passa a usar `spawn` sozinho **[FONTE: linhas 693-698 e 709-718]**. O
  default no Linux/3.12 é `fork` **[FONTE:
  `/usr/lib/python3.12/multiprocessing/context.py:328`]**, então isso é uma
  mudança real de comportamento;
- com `spawn`, cada tarefa **re-importa o Manim do zero** (~1 s por cena);
- e os slots de worker explodem (§4.4) → um cache de TeX por cena.

**(b) Limpar o tema explicitamente** entre cenas — a defesa barata. É o
`limpa_tema()` de `manim-color-theming` §11: guarde as classes tocadas e chame
`cls.set_default()` sem argumentos em cada uma. Só funciona se **você** controla
o `set_default`; não pega o caso do §5.1, em que a mutação está dentro do
`construct` de uma cena de terceiro.

**(c) Um `initializer` no pool** que reseta os defaults antes de cada worker
começar. Ajuda contra herança do pai (§5.3), mas **não** contra o worker reuso —
o initializer roda uma vez por processo, não por tarefa
**[FONTE: `process.py:240-247`]**.

Para lote com **temas diferentes** a resposta certa continua sendo a mais
simples: **um processo por cena** — isto é, o laço serial de `bin/mx render`
do §0, que é o que o deck consumidor faz.

### 5.3 O vetor irmão: o pai importa TODOS os arquivos antes de bifurcar

`main()` chama `list_scenes(f)` para cada arquivo descoberto, **no processo pai**
**[FONTE: `tools/batch_render.py:163`]**, e `list_scenes` → `load_scene_classes`
executa o módulo inteiro **[FONTE: `manimx/render.py:136`]**. Depois disso o
pool é criado com start method `fork`, e cada worker herda o interpretador do
pai *como ele ficou*.

Consequência: **todo efeito colateral de nível de módulo dos seus arquivos de
cena acontece uma vez no pai e é herdado por todos os workers.** Um
`Text.set_default(...)` no topo de um `tema.py`, um `config.background_color =
...` fora de função, um `matplotlib.use(...)`, uma semente de `random` — tudo
isso passa a valer para o lote inteiro, inclusive para os arquivos que não
importam esse módulo.

Não é sempre ruim (é assim que um `tema.py` de projeto poderia aplicar-se a
todos de graça), mas é sempre **implícito**. Se um lote se comporta diferente de
uma renderização isolada da mesma cena, comece por aqui.

---

## 6. Cache em lote — o mínimo que você precisa saber aqui

> **Dono do assunto: `manim-performance-cache`.** O que segue são só as três
> interações com o lote. Hash do partial movie, `hash_obj`, poda, layout de
> `media/` e o custo de rasterizar são lá.

### 6.1 São três caches, não um

| Cache | Onde | Chave | Isolado por worker? |
|---|---|---|---|
| *partial movies* | `{video_dir}/partial_movie_files/{scene_name}` | hash da chamada `play`/`wait` | não — mas a chave inclui o nome da cena |
| **LaTeX** | `tex_dir` (`media/Tex`) | `tex_hash` do documento inteiro | **sim**, `media/_workers/wN/Tex` (§4.2) |
| **texto/Pango** | `text_dir` (`media/texts`) | `_text2hash` da string + estilo | **sim**, `media/_workers/wN/texts` (§4.2) |

`--no-cache` / `disable_caching` desliga **só o primeiro**. Ele não toca o
LaTeX nem o SVG de texto — esses dois só somem apagando o diretório.

O `max_files_cached` (200 na raiz deste projeto, 100 fora dela) é aplicado
**por cena**, não por lote: `clean_cache` opera sobre
`self.partial_movie_directory`, que já inclui `{scene_name}`
**[FONTE: `manim/scene/scene_file_writer.py:1056-1076` + `manim.cfg:26`]**. Num
lote de 60 cenas isso é um teto de 60 × 200 arquivos, não 200.

### 6.2 Lição 2: o hash do SVG de texto NÃO inclui a resolução

Esta é a que morde justamente em lote, porque lote é onde se mistura qualidade.

`Text._text2hash` monta a chave com fonte, slant, peso, cor, `t2c/t2s/t2w/t2f`,
`line_spacing`, `font_size`, ligaduras, gradiente e o texto
**[FONTE: `manim/mobject/text/text_mobject.py:689-701`]**. **`pixel_width` não
entra.** E `_text2svg` decide reusar antes de olhar a resolução
**[FONTE: idem, linhas 843-851]**:

```python
if file_name.exists():
    svg_file = str(file_name.resolve())
else:
    width  = config["pixel_width"]      # ← só chega aqui se NÃO havia cache
    height = config["pixel_height"]
    svg_file = manimpango.text2svg(settings, size, line_spacing, ..., width, height, self.text)
```

`pixel_width` é a **largura de quebra de linha** que o Manim passa ao Pango.
Logo: um preview `-q m` (1280) e a entrega `-q h` (1920) que compartilhem o
mesmo `text_dir` podem servir um o SVG do outro, **com a quebra de linha
errada** — frase que cabia numa linha em 1080p aparecendo quebrada em duas, sem
erro nenhum.

Em lote isso aparece de duas formas:

- **dentro de uma execução**, se você renderizar o mesmo arquivo em duas
  qualidades no mesmo worker;
- **entre execuções**, que é o caso comum: você iterou em `-q m` a tarde toda e
  fez a entrega em `-q h` reaproveitando `media/_workers/wN/texts`.

**Defesa em pipeline:** trate `text_dir` como derivado da qualidade, ou apague-o
ao trocar de qualidade.

```bash
rm -rf media/_workers media/texts     # ao mudar -q entre um lote e outro
```

A correção estrutural — desenhar todo texto em `font_size` grande e encolher —
é de `manim-text-latex` / `manim-tema-projeto`; ela tem o efeito colateral
feliz de fixar `pixel_width` durante a construção do texto e matar este bug de
raiz.

### 6.3 Dado externo: `--no-cache` não é opcional

O hash do partial movie **não enxerga estado que veio de fora** — CSV, JSON,
API, `random` sem semente, data/hora, arquivo em disco. Numa cena
data-driven (§11), o cache serve o vídeo **velho** com o dado **novo** e
reporta `success: true`. Em lote, sessenta vezes.

```bash
.venv/bin/python tools/batch_render.py scenes/gerado -q h --no-cache --json
```

Detalhe de `manim-project` §10.7 que vale repetir aqui: isso vale mesmo quando o
`.py` mudou, se o que mudou foi só o dado que ele lê.

---

## 7. Reprodutibilidade: por que dois lotes do mesmo código diferem

Um lote é reprodutível quando duas execuções produzem os mesmos artefatos.
Estas são as fontes de divergência, todas verificadas, e cada uma com a defesa:

| Fonte | Efeito | Defesa |
|---|---|---|
| **CWD** — `manim.cfg` é lido do diretório atual | fora da raiz: `max_files_cached` 200→100, diretórios viram os defaults (`manim-project` §5) | rode da raiz, ou passe tudo explícito |
| **`--media-dir` relativo** — `Path(media_dir).resolve()` **[FONTE: `manimx/render.py:213`]** | o `media/` nasce onde você chamou o comando | passe caminho **absoluto** em pipeline |
| **ordem de `as_completed`** (§2.5) | `results[]` muda de ordem | indexe por `scene_name`, nunca por posição |
| **`set_default` herdado ou vazado** (§5) | mesma cena, cor diferente conforme o worker | processo por cena, ou `limpa_tema()` |
| **cache de texto entre qualidades** (§6.2) | quebra de linha diferente | apague `text_dir` ao trocar `-q` |
| **cache de partial movie com dado externo** (§6.3) | vídeo velho com dado novo | `--no-cache` |
| **fonte ausente** vira Noto Sans, e `t.font` continua dizendo `"Inter"` (`manim-project` §10.4) | tipografia trocada em toda a máquina que não tem a fonte | fixe a pilha de fontes e exponha um booleano de "casou exato" (`manim-tema-projeto`) |
| **`random` sem semente** | frames diferentes a cada lote | `random.seed(...)` no `setup()` da cena |
| **colisão de `module_name`** (§2.4) | qual mp4 sobrevive muda por execução | nomes de arquivo únicos |
| **codec caindo por falta de sessão** (§3.2) | metade em `h264_nvenc`, metade em `libx264` | `-j 3 --encoders 2` e confira `.results[].codec` |

O teste de reprodutibilidade mais barato que existe roda em um segundo e pega
quase todos os itens acima:

```bash
jq -r '.results[] | [.codec, (.resolution|join("x")), (.frame_rate|tostring)] | @tsv' \
   out.json | sort | uniq -c
# esperado: UMA linha só
```

Duas linhas significam que o lote produziu artefatos heterogêneos — e é isso
que faz um deck ter um vídeo visivelmente mole no meio dos outros.

---

## 8. Do lote ao ARTEFATO: o script de exportação de referência

O `media/` é o layout do **Manim** — `media/videos/<módulo>/<altura>p<fps>/<Classe>.mp4`
—, não o do consumidor. Nenhum consumidor real (site, deck, CMS, editor) quer
esse caminho. A ponte entre os dois é um script de exportação, e ele tem
quatro decisões que valem mais que o resto:

### 8.1 A lista de cenas sai do introspector, nunca de um mapa escrito à mão

```bash
bin/mx scenes "$arquivo" --json    # [{"name","bases","doc"}, ...]
```

Um mapa escrito à mão apodrece silenciosamente. **[DECK]** a versão anterior da
skill de lá mandava medir um `worktrees-p10.mp4` que não existia mais, e o
`check=True` do script estourava — o mapa tinha uma parte a mais que a
realidade.

### 8.2 O nome do arquivo é DERIVADO da classe, nunca configurado

```bash
# CustoMensalComCache → custo-mensal-com-cache ; OndeVaiODinheiro → onde-vai-o-dinheiro
slug() {
  printf '%s' "$1" | sed -E 's/([a-z0-9])([A-Z])/\1-\2/g; s/([A-Z]+)([A-Z][a-z])/\1-\2/g' \
    | tr '[:upper:]' '[:lower:]'
}
```

A **segunda** substituição é a que trata sequências de maiúsculas
(`ODinheiro` → `O-Dinheiro`); sem ela, siglas grudam. Convenção substitui
configuração: zero mapeamentos para manter, e renomear a classe renomeia o
artefato.

### 8.3 O caminho de saída vem do JSON, e o campo depende do modo

```
--format mp4/gif/webm/mov  →  output_file        (image_file é null)
--format png               →  image_file         (output_file é null)
```

**[FONTE: `manimx/render.py:439-444`]** — o `output_file` só é preenchido quando
o arquivo de vídeo existe; o `image_file`, quando o PNG existe. Deduzir o
caminho a partir de `media_dir` + qualidade + nome da classe funciona até
alguém trocar `-q`, e aí o diretório muda de `1080p60` para `720p30` e o `cp`
copia o arquivo de ontem.

### 8.4 Falha de uma cena não aborta o lote

Conte as falhas, imprima o `tail -25` do erro, siga, e **saia não-zero no fim**.
Abortar no primeiro erro desperdiça as cenas boas que viriam depois; ignorar o
erro entrega um lote incompleto com exit 0.

### 8.5 Os dois pôsteres — e as flags do ffmpeg **precisam** ser diferentes

```bash
# ÚLTIMO frame — SEM `-frames:v 1`
ffmpeg -nostdin -loglevel error -y -sseof -1 -i "$SAIDA/$nome.mp4" \
  -update 1 "$SAIDA/$nome.png"

# PRIMEIRO frame — COM `-frames:v 1`, SEM `-sseof`
ffmpeg -nostdin -loglevel error -y -i "$SAIDA/$nome.mp4" \
  -frames:v 1 "$SAIDA/$nome-inicio.png"
```

**Por que a primeira não pode levar `-frames:v 1`:** com ele o ffmpeg grava o
**primeiro frame depois do seek** — o de 1 s antes do fim — e para. Numa parte
que fecha com um `FadeIn` de rodapé, o pôster sai com o texto lavado enquanto o
vídeo está perfeito. Só `-update 1` sobrescreve a cada frame e deixa o **último**
no disco. **[DECK]** foi assim que a parte 9 de uma cena saiu com o rodapé
lavado, e o defeito durou meses sem ninguém notar — porque o vídeo estava certo.

**Por que a segunda existe:** num vídeo cortado em partes
(`manim-presentation-parts`), o primeiro frame da parte N+1 é, por construção,
o último da parte N. O `poster` do `<video>` da parte N+1 tem que ser essa
imagem, senão a troca entre os dois elementos pisca. É um requisito **do
render**, não do player: o consumidor precisa de **três arquivos por parte** —
`mp4`, `png` do último frame e `png` do primeiro.

**Por que não `mx render --format png`:** ele também dá o último frame, mas
**re-renderiza a cena inteira**. O ffmpeg lê o arquivo que já existe. (E com
`--renderer opengl` o `--format png` é ~100× mais lento que com cairo — ver
`manim-gpu-encoding` §9.)

**Consequência de projeto, não de pipeline:** como o último frame vira o pôster
do PDF de backup e do `prefers-reduced-motion`, **a cena não pode fechar em
`FadeOut`**. Se fechar, o backup impresso sai em página branca e ninguém
descobre antes do palco.

### 8.6 O script inteiro

Reúne 8.1–8.5. Adapte `ENTRADA`, `SAIDA` e o glob; o resto é portátil.

```bash
#!/usr/bin/env bash
# exporta-cenas.sh — de um diretório de .py a um diretório de artefatos nomeados.
set -euo pipefail

MANIM="${MANIM_HOME:-$HOME/Projects/manim}"
ENTRADA="${1:?uso: exporta-cenas.sh <dir-de-cenas> <dir-de-saida>}"
SAIDA="${2:?}"
QUALIDADE="${QUALIDADE:-h}"
CODEC="${CODEC:-nvenc-quality}"

[ -x "$MANIM/bin/mx" ] && [ -d "$MANIM/manimx" ] || {
  echo "erro: projeto Manim não encontrado em $MANIM (esperava bin/mx + manimx/)" >&2
  exit 1; }
PY="$MANIM/.venv/bin/python"
mkdir -p "$SAIDA"

slug() {
  printf '%s' "$1" | sed -E 's/([a-z0-9])([A-Z])/\1-\2/g; s/([A-Z]+)([A-Z][a-z])/\1-\2/g' \
    | tr '[:upper:]' '[:lower:]'
}

TOTAL=0; FALHAS=0
shopt -s nullglob
for arquivo in "$ENTRADA"/cena_*.py; do          # glob RESTRITO: veja §2.3
  CENAS="$("$MANIM/bin/mx" scenes "$arquivo" --json 2>/dev/null \
    | "$PY" -c 'import json,sys
d = json.load(sys.stdin)
nomes = d if isinstance(d, list) else d.get("scenes", [])
print("\n".join(n if isinstance(n, str) else n.get("name","") for n in nomes))' || true)"

  [ -n "$CENAS" ] || { echo "· $(basename "$arquivo"): nenhuma cena"; continue; }

  while IFS= read -r cena; do
    [ -n "$cena" ] || continue
    nome="$(slug "$cena")"
    printf '▸ %s … ' "$cena"

    json="$("$MANIM/bin/mx" render "$arquivo" "$cena" \
      -q "$QUALIDADE" --codec "$CODEC" --json 2>&1)" || {
        echo "FALHOU"; printf '%s\n' "$json" | tail -25; FALHAS=$((FALHAS+1)); continue; }

    # O `mx` pode imprimir aviso antes do JSON: corte a partir do primeiro '['.
    mp4="$(printf '%s' "$json" | "$PY" -c 'import json,sys
bruto = sys.stdin.read(); i = bruto.find("[")
d = json.loads(bruto[i:]) if i >= 0 else []
print((d[0].get("output_file") or "") if d else "")' 2>/dev/null || true)"

    if [ -z "$mp4" ] || [ ! -f "$mp4" ]; then
      echo "FALHOU (sem output_file)"; printf '%s\n' "$json" | tail -25
      FALHAS=$((FALHAS+1)); continue
    fi

    cp -f "$mp4" "$SAIDA/$nome.mp4"

    if command -v ffmpeg >/dev/null 2>&1; then
      # ÚLTIMO frame (pôster do PDF/reduced-motion). SEM -frames:v 1 — §8.5.
      ffmpeg -nostdin -loglevel error -y -sseof -1 -i "$SAIDA/$nome.mp4" \
        -update 1 "$SAIDA/$nome.png" 2>/dev/null || true
      # PRIMEIRO frame (poster do <video>, mata a piscada na troca de parte).
      ffmpeg -nostdin -loglevel error -y -i "$SAIDA/$nome.mp4" \
        -frames:v 1 "$SAIDA/$nome-inicio.png" 2>/dev/null || true
    fi

    echo "ok → $SAIDA/$nome.mp4 ($(du -h "$SAIDA/$nome.mp4" | cut -f1))"
    TOTAL=$((TOTAL+1))
  done <<< "$CENAS"
done

echo; echo "$TOTAL artefato(s) em $SAIDA"
[ "$FALHAS" -eq 0 ] || { echo "$FALHAS falha(s)." >&2; exit 1; }
```

Uma decisão de projeto que este script **não** toma, e que vale considerar:
preview e entrega escrevem nos **mesmos** caminhos. Iterar a tarde toda em
720p30 e esquecer de refazer o render final entrega 720p30 no lugar da
entrega — visivelmente mole no projetor, e sem nenhum aviso. Um pipeline que escrevesse preview e final em pastas diferentes não
teria essa armadilha. Enquanto não tiver, a conferência do §9.2 é obrigatória.

---

## 9. Conferência do lote — quatro checagens que rodam em segundos

> **Julgar se o frame ficou CERTO é de `manim-verificacao-visual`** (olhar o
> PNG, contraste, corte na borda, sobreposição). O que segue são checagens de
> **integridade do lote**: contagem, uniformidade, artefato vazio, cena
> fantasma. Nenhuma delas re-renderiza — todas leem arquivos que já existem.
>
> **Nesta revisão nada foi executado.** Os comandos abaixo estão conferidos
> quanto às flags e ao contrato do JSON; os números de saída não foram
> reproduzidos hoje.

### 9.1 Contagem: classes × arquivos × o que o consumidor declara

O defeito mais comum do lote é a divergência de contagem, e é o único que o
consumidor **não** degrada graciosamente.

```bash
base=cena_minha            # prefixo dos arquivos de saída
classes=$(grep -cE '^class .*P[0-9]+\(' aulas/manim/aula_x.py)
arquivos=$(ls "$SAIDA/$base"-p*.mp4 2>/dev/null | wc -l)
echo "classes=$classes arquivos=$arquivos"
```

Leitura do resultado:

- `arquivos > classes` → sobrou órfão de uma remoção; apague o excedente;
- `arquivos < classes` → alguma parte não renderizou (procure a falha no JSON);
- iguais, mas o consumidor declara outro número → o consumidor está errado.

### 9.2 Uniformidade: resolução e fps têm que ser UMA linha

```bash
for f in "$SAIDA"/*.mp4; do
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate -of csv=p=0 "$f"
done | sort | uniq -c        # esperado: UMA linha só
```

Duas linhas = preview comitado por cima da entrega, ou lote rodado em duas
qualidades. Se você tiver o `--json` do lote, dá para conferir sem tocar em
arquivo nenhum (§7).

### 9.3 O pôster não pode estar vazio

Uma parte que fecha em `FadeOut` produz um `.png` em branco — e é ele que vai
para o PDF de backup. Meça a cobertura de tinta:

```bash
"$MANIM/.venv/bin/python" - "$SAIDA" <<'PY'
import sys, pathlib, numpy as np
from PIL import Image
for p in sorted(pathlib.Path(sys.argv[1]).glob("*.png")):
    a = np.asarray(Image.open(p).convert("L"))
    tinta = float((a < 235).mean())
    if tinta < 0.01:
        print(f"SUSPEITO {p.name}: {tinta:.3%} de tinta — fade-out disfarçado?")
PY
```

Pillow e numpy estão no `.venv` deste projeto. O limiar `< 235` e o piso de 1%
assumem **fundo claro**; em fundo escuro inverta (`a > 20`).

### 9.4 Nenhuma classe-base virou cena

```bash
bin/mx scenes aulas/manim/aula_x.py --json > /tmp/cenas.json   # MATERIALIZE
jq -r '.[].name' /tmp/cenas.json | grep -E '^_|Base$|Mixin$' && \
  echo "ATENÇÃO: classe-base sendo listada como cena"
```

**A lição transversal está no `>` daquela primeira linha.** Escrever
`bin/mx scenes ... | grep -E '^_' || echo ok` transforma **falha do comando** em
"ok": se o `mx` morrer, o pipe entrega vazio, o `grep` não acha nada, e o `||`
imprime sucesso. **Materialize a saída antes de filtrar.** Foi assim que um
`--aula` obrigatório passou despercebido num pipeline por semanas.

---

## 10. O que entra no git

A saída de um lote é **derivada**: o `.py` versionado a reconstrói. Mas nem
tudo é igualmente derivado, e a política que funciona distingue os dois casos.

**[DECK] O caso medido**, contado no disco em 2026-08-19 no projeto consumidor:

| Aula | mp4 | png | Política |
|---|---|---|---|
| `001-multi-work` | 59 arquivos, **63,0 MiB** | 118 arquivos, 17,3 MiB | tudo commitado |
| `002-deepseek-harness` | 18 arquivos, **16,0 MiB** | 36 arquivos, 3,6 MiB | **mp4 fora do git**, png dentro |

A aula 001 commitou os mp4 e custou 63 MiB de repositório para um artefato que
`npm run videos` reconstrói. A 002 mudou de política, e o raciocínio dela é a
regra que generaliza:

> **O mp4 sai; o png fica.** O mp4 é puro derivado. O png é **pôster** — é dele
> que vivem o `?print-pdf`, o `prefers-reduced-motion` e o primeiro quadro antes
> do play. Sem ele o fallback estático não existe, e o backup impresso sai em
> branco na máquina de quem clonou o repositório e ainda não renderizou.

Repare na proporção: são **dois png por mp4** (último e primeiro frame, §8.5), e
juntos eles pesam ~22–27% do que pesam os mp4. É um preço baixo por um fallback
que sempre funciona.

```gitignore
# saída bruta do Manim — sempre fora
media/
media-gl/
**/manim/media/

# artefatos entregáveis: o vídeo é reconstruível, o pôster é o fallback
public/videos/*.mp4
# (os .png NÃO entram nesta lista — de propósito)
```

Regra de bolso para estimar antes de decidir: **[DECK]** 1080p60 com
`nvenc-quality` rende ≈ **0,29 MB por segundo de vídeo**, com dispersão de 0,07
(cena quase estática) a 0,66 MB/s (palco inteiro em movimento). Multiplique pela
duração total do lote antes de commitar qualquer coisa.

E antes de publicar, o guarda deste repositório pega o que `grep -rn` não pega
(caminho de máquina dentro dos `.json.gz`, credencial, arquivo acima de 50 MiB,
wrapper sem bit de execução):

```bash
tools/check_publishable.sh
```

---

## 11. Pipeline orientado a dados — um vídeo por linha

### 11.1 Gerar os arquivos `.py` e renderizar em lote

O padrão mais simples e o mais depurável: o `.py` gerado fica no disco, você
pode abri-lo, e `mx scenes` o enxerga.

```python
from pathlib import Path
import csv, re

TEMPLATE = '''from manim import *

class {cls}(Scene):
    def construct(self):
        titulo = Text({titulo!r}, font_size=44, color=BLACK).to_edge(UP)
        valor  = MathTex(r"{formula}", font_size=72, color=BLACK)
        self.play(Write(titulo))
        self.play(Write(valor))
        self.wait()
'''

out = Path("scenes/gerado"); out.mkdir(parents=True, exist_ok=True)
with open("dados.csv", encoding="utf-8") as fh:
    for i, row in enumerate(csv.DictReader(fh)):
        cls = f"Item{i:03d}"                       # nome DERIVADO, não do CSV
        (out / f"{cls.lower()}.py").write_text(
            TEMPLATE.format(cls=cls, titulo=row["titulo"], formula=row["formula"]),
            encoding="utf-8",
        )
```

```bash
.venv/bin/python tools/batch_render.py scenes/gerado -q h --codec nvenc \
  -j 3 --encoders 2 --no-cache --json > out.json
```

Quatro coisas nesse comando não são opcionais:

- **`--no-cache`** — §6.3. Sem ele, mudar o CSV não muda o vídeo;
- **`-j 3 --encoders 2`** — §3.2, seis sessões, duas de folga;
- **`--json`** — o caminho de saída vem de lá, §8.3;
- **nome de classe derivado de um contador**, não do dado. Nome vindo do CSV
  vira caminho de arquivo: **valide, não sanitize** — recuse o que não casar
  com `^[a-z0-9-]+$` e diga qual foi, em vez de silenciosamente transformar
  `Relatório 2º/T` em algo que ninguém consegue procurar depois.

### 11.2 Parametrizar por atributo de classe, sem gerar arquivo

```python
from manim import *
from manimx.render import render_scene

class Card(Scene):
    titulo = "padrão"
    def construct(self):
        self.play(Write(Text(self.titulo, font_size=48, color=BLACK)))
        self.wait()

for i, t in enumerate(["Alfa", "Beta", "Gama"]):
    Sub = type(f"Card{i}", (Card,), {"titulo": t})
    r = render_scene(Sub, quality="h", codec="nvenc",
                     input_file=__file__, output_file=f"card_{i}")
    print(r.output_file)
```

`input_file=__file__` **não é opcional**: sem ele o `module_name` fica vazio e
todos os vídeos caem em `media/videos/<qualidade>/` (§2.4). E este laço roda
**sequencialmente num processo** — para paralelizar, distribua em processos, e
lembre que classes criadas com `type()` não são picláveis por referência, então
o worker precisa recriá-las a partir dos dados, não recebê-las prontas.

### 11.3 O carregador de dado: falhe tarde, e com mensagem

Um módulo de dados é importado por **todas** as cenas, então nada nele pode
falhar no import por causa de um valor que a maioria das cenas não usa.

```python
# dados.py — carregamento defensivo, erro claro no CONSUMO
import json
from pathlib import Path
from typing import Any

_ARQ = Path(__file__).resolve().parent / "dados" / "precos.json"
# .get, não []: um KeyError aqui derrubaria TODAS as cenas do arquivo,
# não só a que usa o dado. PRECOS vazio é um estado válido.
PRECOS: dict[str, Any] = json.loads(_ARQ.read_text(encoding="utf-8")).get("numeros", {}) \
    if _ARQ.exists() else {}

def numero(id_: str, campo: str = "valor") -> Any:
    if id_ not in PRECOS:
        disponiveis = ", ".join(sorted(PRECOS)) or "(nenhum)"
        raise KeyError(f"número '{id_}' não existe em {_ARQ.name}. Existem: {disponiveis}")
    return PRECOS[id_][campo]
```

O ganho não é estético: em lote, um `KeyError` no import derruba **todas** as
cenas do arquivo com a mesma mensagem inútil, e você perde a corrida inteira
para descobrir que faltava um preço numa cena só. A mensagem que lista os ids
disponíveis resolve o problema em uma leitura.

E o corolário que fecha o ciclo com §6.3: **a mesma fonte de dado é lida pelos
dois lados** — a cena Python e o consumidor (o slide, o site). Um número
redigitado dentro da cena é um bug esperando a próxima correção de preço.

---

## 12. Em CI

### 12.1 `bin/mx doctor` é um gate mais fraco do que parece

Ele tem 10 checagens, mas **só quatro são fatais**
**[FONTE: `manimx/cli.py:55-186`]**:

| Checagem | Fatal? |
|---|---|
| `python >= 3.11` | **sim** |
| `manim (CE)` importa | **sim** |
| `PyAV + libx264` | **sim** |
| `Pango (Text)` | **sim** |
| `NVENC (h264_nvenc)` | não |
| `latex` no PATH | não |
| `dvisvgm` no PATH | não |
| `ffmpeg` no PATH | não |
| `LaTeX → SVG (MathTex)` compila | não |
| `manimgl` | não |

Ou seja: **`mx doctor` sai 0 com o LaTeX quebrado, sem `dvisvgm` e sem
`ffmpeg`.** Se o seu lote usa `MathTex` — ou o seu script de exportação usa
`ffmpeg` para os pôsteres (§8.5) — o exit code do doctor não te protege.

Esta tabela concorda com `manim-project` §4.1, que é a **dona do `mx doctor`** e
traz a leitura do fonte linha a linha; ela está aqui só porque é o primeiro
passo de um gate de CI. Faça o gate nos campos certos:

```bash
# de propósito com media-dir FRIO: ver a nota abaixo
bin/mx doctor --json --media-dir /tmp/doctor-frio > build/doctor.json || true
jq -e '.checks[] | select(.check == "dvisvgm") | .ok' build/doctor.json \
  || { echo "sem dvisvgm: MathTex vai quebrar no lote"; exit 1; }
jq -e '.checks[] | select(.check == "LaTeX → SVG (MathTex)") | .ok' build/doctor.json \
  || { echo "LaTeX não compila neste runner"; exit 1; }
jq -e '.checks[] | select(.check == "ffmpeg") | .ok' build/doctor.json \
  || { echo "sem ffmpeg: os pôsteres não seriam gerados"; exit 1; }
```

> **Por que `dvisvgm` vem PRIMEIRO, e por que o `--media-dir` frio.**
> `manim-project` §4.3 **[MEDIDO]** mostra que o check `LaTeX → SVG (MathTex)`
> é literalmente `MathTex(r"x^2")`, e que o Manim guarda o SVG em
> `{media_dir}/Tex` com hash do LaTeX — **o hash não sabe se o `dvisvgm`
> existe**. Com `media/Tex` quente, o check passa mesmo sem o binário. E este
> gate roda `cd` para a raiz do projeto (§12.2), que é exatamente o cenário
> quente medido lá. Daí a regra da irmã, que esta skill adota:
> **se `dvisvgm` e `LaTeX → SVG` discordarem, acredite no primeiro.**

O JSON é `{"ok": bool, "checks": [{"check","ok","detail","fatal"}]}`
**[FONTE: `manimx/cli.py:176`]**.

### 12.2 O script

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."                       # a raiz: manim.cfg só vale daqui (§7)
source bin/manim-env.sh; manimx_use_ce; manimx_enable_gpu

mkdir -p build
bin/mx doctor --json --media-dir /tmp/doctor-frio > build/doctor.json || true   # §12.1: frio
jq -e '.ok' build/doctor.json > /dev/null
jq -e '.checks[] | select(.check=="dvisvgm") | .ok' build/doctor.json > /dev/null
jq -e '.checks[] | select(.check=="LaTeX → SVG (MathTex)") | .ok' build/doctor.json > /dev/null

.venv/bin/python tools/batch_render.py scenes/ \
    -q h --codec "${CODEC:-nvenc}" -j "${JOBS:-3}" --encoders 2 \
    --media-dir "$PWD/media" --json > build/render.json

jq -e '.failed == 0' build/render.json > /dev/null

# heterogeneidade = lote comprometido (§7)
n=$(jq -r '.results[] | select(.success) | [.codec,(.resolution|join("x"))] | @tsv' \
      build/render.json | sort -u | wc -l)
[ "$n" -eq 1 ] || { echo "lote heterogêneo: $n combinações de codec/resolução"; exit 1; }

jq -r '.results[] | select(.success) | .output_file' build/render.json
```

Três decisões:

- **`--media-dir "$PWD/media"`** absoluto — §7. Em CI o CWD costuma mudar entre
  passos;
- **`--codec x264` num runner sem GPU.** O `manimx` já cai em libx264 sozinho e
  só avisa, mas ser explícito evita um lote metade NVENC metade CPU e o ruído
  correspondente no log;
- **`--renderer opengl` fica de fora de CI headless.** Ele exige GPU e driver, e
  em notebook híbrido exige PRIME offload (`manim-gpu-encoding`).

### 12.3 Reencode só na entrega

Não escolha um codec pesado durante a produção. Renderize o master em H.264 e
reencode uma vez, no fim, com o `ffmpeg` do sistema:

```bash
ffmpeg -i entrada.mp4 -c:v hevc_nvenc -preset p7 -rc vbr -cq 24 -b:v 0 saida.mp4
```

A escolha de codec, os pesos medidos e o porquê de o `av1_nvenc` do PyAV não
servir são de **`manim-gpu-encoding`** (§5 e §6 de lá).

---

## 13. Sintoma → causa → correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| `FileNotFoundError: media/Tex/<hash>.aux`, errático | varredura global de `delete_nonsvg_files` entre workers (§4.1) | é o comportamento padrão do `tools/batch_render.py`; se for orquestrador próprio, `tex_dir` por worker **fora** de `media/Tex` |
| `IsADirectoryError` em qualquer render de LaTeX, **inclusive fora do lote** | alguém pôs os diretórios por worker **dentro** de `media/Tex` (§4.2) | `rm -rf media/Tex/*/` e mova para `media/_workers/` |
| `avcodec_open2("h264_nvenc", …)` / `Generic error in an external library` | sessões NVENC esgotadas (§3.2) | `-j 3 --encoders 2`; diagnóstico e teto em `manim-gpu-encoding` §7 |
| a 2ª cena do lote saiu preta no preto, exit 0 | `set_default` vazou pelo worker reusado (§5) | processo por cena, ou `max_tasks_per_child=1`, ou `limpa_tema()` |
| dois `.py` diferentes, um `.mp4` só | colisão de `module_name` (§2.4) | nomes de arquivo únicos, ou `--media-dir` por subárvore |
| `results[0]` é uma cena diferente a cada execução | ordem de `as_completed` (§2.5) | indexe por `scene_name` |
| `jq: Cannot index ... with "resolution"` | resultado de falha só tem 4 chaves (§2.5b) | filtre `select(.success)` antes |
| `--dry-run --json \| jq` → parse error | `--dry-run` não imprime JSON (§2.5c) | use `bin/mx scenes ARQ.py --json` |
| `NotImplementedError: Non-relative patterns are unsupported` | glob absoluto em `_discover` (§2.3) | caminho relativo, ou passe o diretório |
| uma classe-base virou vídeo de 35 s | `rglob` pegou `tema.py`, e a base herda de `Scene` (§2.3) | glob restrito, `--scenes`, ou prefixo `_` no nome do arquivo |
| lote com 60 vídeos e nenhum aviso, mas a fonte está errada | `verbosity="CRITICAL"` no `_job` (§2.2) | confira o artefato (§9), não o log |
| frase quebrada em duas linhas só na entrega | SVG de texto reaproveitado de outra resolução (§6.2) | `rm -rf media/_workers media/texts` ao trocar `-q` |
| dado do CSV mudou, vídeo não | cache de partial movie não vê estado externo (§6.3) | `--no-cache` |
| lote metade `h264_nvenc`, metade `libx264` | sessões acabaram no meio (§3.2) | reduza `-j`; confira `.results[].codec` |
| `BrokenProcessPool` no meio do lote | OOM killer levou um worker (§3.3) | reduza `-j × --encoders`, ou a resolução |
| pôster do PDF em branco | a cena fecha em `FadeOut` (§8.5) | não termine em fade-out; ou re-extraia com `-update 1` |
| pôster com o texto lavado, mas o vídeo certo | `-sseof -1` **com** `-frames:v 1` (§8.5) | tire o `-frames:v 1` da extração do último frame |
| um vídeo visivelmente mole no meio do deck | preview 720p30 sobrescreveu a entrega (§9.2) | `ffprobe … \| sort \| uniq -c` tem que dar uma linha |

---

## 14. Onde esta skill para

| Você precisa de | Skill |
|---|---|
| renderizar **uma** cena, achar o caminho da saída, `-n a,b`, `--format png`, seções | `manim-render-api` |
| escolher codec, NVENC, o teto de sessões, `max_inflight_encoders`, peso do arquivo, `mx bench` | **`manim-gpu-encoding`** (dona de tudo que é GPU/encode) |
| o cache por dentro: hash do partial movie, `hash_obj`, poda, o que custa rasterizar | `manim-performance-cache` |
| **olhar** o frame e julgar se ficou certo: contraste, corte na borda, sobreposição | `manim-verificacao-visual` |
| cortar **uma** cena em partes para slide, a emenda, a métrica direcional | `manim-presentation-parts` |
| tema, paleta, `set_default`, o que ele não alcança, os dois vazamentos | `manim-color-theming` |
| o `tema.py` como contrato de projeto: fonte, escala, tempos, classe-base, dado externo | `manim-tema-projeto` |
| um traceback concreto de uma cena que quebrou | `manim-troubleshooting` |
| achar nome de classe, assinatura, kwarg | `manim-api-discovery` |
| o mapa do repositório, os wrappers, o `cwd` como configuração | `manim-project` (§5 e §13) |

**Buracos declarados** — se a pergunta for uma destas, diga que não há skill em
vez de improvisar: precedência completa de config (`ManimConfig`,
`config_file_paths`, `make_config_parser`); som e legenda em lote; distribuição
do lote entre **máquinas** (aqui só há paralelismo local); e retomada de lote
interrompido (não existe checkpoint — `tools/batch_render.py` recomeça do zero,
e o que salva é o cache de partial movies).

---

## 15. O que NÃO foi verificado nesta revisão

Escrito para você não repetir a conferência achando que já foi feita:

1. **Nada foi renderizado.** Nenhum `mx render`, `batch_render.py`, `mx bench`,
   `ffmpeg` ou `ffprobe` rodou. Os comandos de §8, §9 e §12 estão conferidos
   quanto a flags e contrato de JSON, **não** quanto à saída.
2. **Os tempos de §3.4 (57,9 s / 59,2 s / 46 s / 52 s)** vêm de uma execução
   anterior nesta máquina e não foram reproduzidos. A distribuição das 6 cenas
   de `scenes/exemplos.py` foi conferida por leitura; os segundos, não.
3. **O teto de 8 sessões NVENC** é medição de `manim-gpu-encoding` §7, não
   minha. Não reabri encoders.
4. **O vazamento de `set_default` em lote (§5.1)** é dedução de duas leituras —
   o `construct` de `LousaBranca` e o laço de reuso do `ProcessPoolExecutor` —
   e **não** foi observado num lote real. A conclusão é forte, mas é inferência.
5. **A corrida residual com `no_latex_cleanup=True` (§4.3)** — dois workers
   compilando a mesma expressão simultaneamente — não foi provocada.
6. **`max_tasks_per_child` forçando `spawn` e multiplicando os slots de worker
   (§4.4, §5.2)** foi lido no CPython, não executado.
7. **Os números do §10** (59/18 mp4, 118/36 png, 63,0/16,0 MiB) foram contados
   no disco hoje com `find`+`du`. O **0,29 MB/s** é do deck e não foi
   recalculado.
8. **`tools/batch_render.py` tem dois defeitos de documentação interna** que
   esta skill descreve mas **não corrigiu no código** (a skill não edita o
   tool): o docstring cita uma flag `--all` que não existe (linha 13) e um
   limite de "~3 encoders NVENC" que está obsoleto (linhas 20-24). Um terceiro
   ponto é de comportamento, não de documentação: o aviso de NVENC dispara em
   `jobs > 4` e ignora `--encoders`, então os defaults (8 sessões) passam
   calados.
