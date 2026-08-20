---
name: manim-render-api
description: >-
  DISPARAR o render e SABER O QUE SAIU — as três portas (`bin/mx render`, a API
  Python `manimx.render_file`/`render_scene`, e o `bin/manim` cru), o contrato
  do `--json`, e o CAMINHO EXATO de cada arquivo que o Manim escreve. Use
  sempre que o pedido for "renderiza essa cena", "gera o mp4", "cadê o arquivo
  que saiu?", "quero só um frame para olhar", "faz um GIF disso", "exporta em
  webm/mov", "renderiza só as animações 4 a 7", "renderiza todas as cenas do
  arquivo", "isso saiu em 480p, quero 4K", "por que o vídeo foi parar em
  `720p15`?", "o render deu exit 0 e não tem mp4 nenhum", "o PNG do preview
  apagou o PNG bom", "como eu passo uma config que a CLI não expõe?", "o
  `manim` travou esperando eu digitar alguma coisa". Cobre as 5 qualidades e os
  apelidos, `-q` × `-r` × `--fps` (o `-r` NÃO ignora o `-q`), os 5 formatos
  (mp4/gif/webm/mov/png) e a diferença entre `mx --format png` (um frame) e
  `manim --format png` (sequência inteira), `-n a,b`, `-s`, `--dry_run`,
  `--save_sections`, `--no-cache`/`--flush_cache`/`--seed`, `-o`, `--media-dir`,
  `tempconfig`/`config_overrides` e o filtro que engole chave errada em
  silêncio, a tabela completa kwarg × flag `mx` × flag `manim`, e
  `get_video_metadata` para conferir o arquivo sem `ffprobe`. NÃO use para:
  codec, NVENC, "está lento" e peso do arquivo (skill `manim-gpu-encoding`);
  várias cenas em processos paralelos e CI (`manim-batch-pipeline`); o que o
  hash do cache enxerga e o custo de rasterizar (`manim-performance-cache`);
  de qual `Scene` herdar e a semântica de `next_section` (`manim-cenas-secoes`);
  OLHAR o frame e julgar o resultado (`manim-verificacao-visual`); o corte em
  partes para slide (`manim-presentation-parts`); traceback e ambiente quebrado
  (`manim-troubleshooting`); achar nome ou assinatura de API
  (`manim-api-discovery`); cor, tema e a decisão de transparência
  (`manim-color-theming`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Renderização — da chamada ao arquivo

Esta skill responde a duas perguntas, e só a essas duas:

1. **Como eu disparo o render exatamente do jeito que preciso?**
2. **Onde foi parar o que ele escreveu, e como eu provo isso sem adivinhar?**

Tudo o que é *desenho* é de outra skill. Tudo o que é *velocidade e codec* é de
`manim-gpu-encoding`. Aqui é a mecânica da invocação e a mecânica da saída.

> **Procedência.** As assinaturas, defaults, ordens de aplicação e caminhos
> abaixo foram lidos no código instalado nesta máquina — ManimCE **0.21.0** em
> `.venv/lib/python3.12/site-packages/manim/`, e a camada `manimx/` deste
> repositório. Cada afirmação forte traz o arquivo e a linha. **Nenhum render
> foi executado ao escrever esta versão** (rodada com CPU/GPU proibidas): onde o
> número vem de uma medição anterior, ele está atribuído (`manim-project`,
> `manim-gpu-encoding` ou o deck consumidor `~/Projects/aulas`), com a data. O
> que é dedução minha a partir do fonte está marcado **[LIDO, NÃO EXECUTADO]**.

---

## 1. As três portas para o mesmo motor

| | `bin/mx render` | `manimx.render_scene/_file` | `bin/manim` (CLI da CE) |
|---|---|---|---|
| para quem | **agente** | script Python | humano, e o que o `mx` não expõe |
| saída legível por máquina | `--json` | `RenderResult` | não (log colorido) |
| caminho do arquivo | **no resultado** | **no resultado** | você deduz ou lê o log |
| codec padrão | **`nvenc`** (`manimx/cli.py`, `--codec` default) | **`x264`** | libx264 fixo (sem flag de codec) |
| `-n a,b` (recorte) | ✗ | ✗ | ✓ |
| `--save_sections` | ✗ | ✓ (`save_sections=True`) | ✓ |
| `--flush_cache` | ✗ | ✓ (`flush_cache=True`) | ✓ |
| `--dry_run`, `-p`, `--log_to_file`, `-0` | ✗ | via `config_overrides` | ✓ |
| cena sem nome, arquivo com N cenas | `ValueError` listando as N | `ValueError` listando as N | **PERGUNTA no terminal** (§9.3) |

**Regra de bolso:** comece sempre no `bin/mx render --json`. Só desça para
`bin/manim` quando precisar de uma flag que o `mx` não tem — `-n`, `-s` com
sequência de PNGs, `--save_sections`, `--dry_run`, `--flush_cache`. E use a API
Python quando o render é um passo dentro de um script maior, ou quando você
precisa de uma chave de `config` que nenhuma CLI expõe (§11).

**Os defaults divergem de propósito e isso já custou tempo:** `mx render` sem
`--codec` sai em `h264_nvenc`; o mesmo trabalho por `render_scene()` sai em
`libx264`. Não é bug — é o default de cada porta. (`manim-project` §8.1 mediu o
efeito: "o mesmo render ficou 3× mais lento quando virei script".)

**Nunca chame `.venv/bin/manim` nem `.venv/bin/mx` direto.** Sem os wrappers de
`bin/` você perde o `dvisvgm` do TinyTeX e o PRIME offload da dGPU, e o `mx` do
venv ainda diz "Ambiente pronto" mentindo. Detalhe em `manim-project` §3.1 (dvisvgm), §3.2 (PRIME) e §3.4 (o `mx` do venv mentindo).

---

## 2. O contrato do `--json` — leia antes de parsear

```bash
bin/mx render scenes/exemplos.py OlaManim -q h --codec nvenc --json
```

```jsonc
[                                    // ← SEMPRE uma LISTA, mesmo com uma cena só
  {
    "scene_name": "OlaManim",
    "success": true,
    "output_file": "/…/media/videos/exemplos/1080p60/OlaManim.mp4",
    "image_file": null,
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

Os campos são exatamente os de `manimx.render.RenderResult` (dataclass, com
`as_dict()` convertendo `Path` para `str`). O objeto é **falsy quando falha**
(`__bool__` devolve `self.success`), então `if r:` funciona.

### 2.1 As cinco coisas que se descobrem parseando

**(a) É uma lista.** `json.load(...)[0]`, sempre. Uma cena só não vira objeto.

**(b) `--format png` inverte os campos.** `output_file` fica `null` e o caminho
está em **`image_file`**. Quem lê só `output_file` conclui que o render falhou.
Medido em `manim-project` §7.1:
`"image_file": "/…/media/images/demo/Demo_ManimCE_v0.21.0.png"`.

**(c) `success: true` com `output_file: null` é um estado real, e é o pior.**
`render_scene` só preenche `output_file` se o arquivo **existir no disco**
(`manimx/render.py`: `elif movie and Path(movie).exists()`). E o
`SceneFileWriter.combine_to_movie` desiste em silêncio quando nenhuma animação
foi escrita:

```python
if len(partial_movie_files) == 0:      # scene_file_writer.py
    logger.info("No animations are contained in this scene.")
    return
```

Isso acontece sempre que **todas** as animações foram puladas — o modo de falha
canônico de uma cena em partes com `PARTE` apontando para uma seção que não
existe (ver `manim-presentation-parts`). O resultado: exit 0, JSON válido,
`success: true`, e **nenhum mp4**.

> **Portanto o teste de sucesso de um agente é `success && output_file`, nunca
> só `success`.** Para `--format png`, `success && image_file`.

**(d) Falha DENTRO da cena devolve JSON; falha ao IMPORTAR o arquivo não.**
Esta é a distinção que quebra pipeline:

| o que quebrou | stdout com `--json` | exit |
|---|---|---|
| exceção dentro do `construct` | JSON válido, `success:false`, `error`, `traceback_text` | 1 |
| arquivo não existe / erro de sintaxe / `ImportError` no topo | **nada** (só uma linha em stderr) | 1 |
| nome de cena inexistente | **nada** (`ValueError` listando as cenas válidas, em stderr) | 1 |
| arquivo com N cenas e nenhum nome | **nada** (`ValueError` listando as N) | 1 |

O motivo está em `manimx/cli.py`: `cmd_render` chama `render_file` **fora** de
qualquer `try`; quem captura é o `main`, que imprime `erro: <Tipo>: <msg>` em
stderr e devolve 1 — sem passar pelo `_out`. Já uma exceção da cena é capturada
por `render_scene` e embrulhada no `RenderResult`.
**Consequência prática:** `json.loads(saida)` num pipeline precisa tratar
stdout vazio, e a mensagem útil está em **stderr**. As duas mensagens de
`ValueError` listam as cenas disponíveis — leia o erro em vez de chutar o nome.

**(e) Com `--json`, todo log vai para stderr.** `manimx/cli.py` redireciona
`sys.stdout` para `sys.stderr` durante o comando e escreve o JSON no stdout
real, guardado antes (`_REAL_STDOUT`). Isso existe porque o Manim escreve
avisos no stdout via `rich` (o clássico `Output format changed to '.mp4' to
support transparency`) e um `json.loads` displicente morreria neles. Então
`2>/dev/null` deixa o stdout puro — e joga fora o diagnóstico. Prefira
`2>/tmp/render.err`.

### 2.2 Exit codes

```
1 cena, arquivo com 1 cena, sem nomear    → 0
cena que levanta exceção                  → 1   (JSON com error/traceback)
render sem nomear num arquivo com N > 1   → 1   (sem JSON)
cena inexistente                          → 1   (sem JSON)
`mx render -a` com 1 de 6 cenas falhando  → 1   (JSON com 6 objetos, 1 com success:false)
```

`cmd_render` devolve `0 if all(r.success for r in results) else 1`. Repare:
**o exit code não sabe do caso (c)** — todas as cenas podem ter `success:true`
sem nenhum arquivo no disco.

---

## 3. Onde o arquivo cai — a fórmula inteira

Nunca deduza; leia `output_file`/`image_file` do resultado. Mas você precisa
entender a fórmula para depurar quando ela dá um lugar estranho.

### 3.1 A árvore

Templates de `manim/_config/default.cfg`, sobrescritos pelo `manim.cfg` deste
repositório (que só reescreve os mesmos valores, mais explícitos):

```
<media_dir>/                                    ./media
├── videos/<module_name>/<quality>/             {media_dir}/videos/{module_name}/{quality}
│   ├── <output_name>.mp4                       ← o vídeo
│   ├── <output_name>_ManimCE_v0.21.0.gif       ← o GIF (§5.3)
│   ├── sections/                               {video_dir}/sections
│   │   ├── <output_name>_0000_<nome>.mp4
│   │   └── <output_name>.json                  ← o índice das seções
│   └── partial_movie_files/<scene_name>/       {video_dir}/partial_movie_files/{scene_name}
│       ├── <hash>.mp4  ou  uncached_00000.mp4
│       └── partial_movie_file_list.txt
├── images/<module_name>/                       {media_dir}/images/{module_name}   ← SEM <quality>
│   ├── <output_name>_ManimCE_v0.21.0.png       ← o frame único (-s / mx --format png)
│   └── <output_name>0000.png …                 ← a sequência (manim --format png)
├── Tex/                                        {media_dir}/Tex
├── texts/                                      {media_dir}/texts
└── logs/                                       {media_dir}/logs   (só com --log_to_file)
```

`media/images/<module_name>/` é criado **em todo render**, mesmo num render de
mp4 puro — `init_output_directories` cria o diretório de imagens antes de
checar `write_to_movie()`. Um diretório vazio ali não significa nada.

### 3.2 `<quality>` não é a sua flag `-q`. É uma string derivada.

Este é o detalhe que mais confunde. O `{quality}` do template é montado em
`ManimConfig.get_dir` (`_config/utils.py:1682`):

```python
all_args["quality"] = f"{self.pixel_height}p{self.frame_rate:g}"
```

Ou seja: **altura em pixels + `p` + frame rate**, com formatação `:g` (que
imprime `60`, não `60.0`, e `59.94` quando for o caso). Consequências reais:

| comando | diretório |
|---|---|
| `-q h` | `1080p60` |
| `-q l` | `480p15` |
| `-q l -r 1280x720` | **`720p15`** — a altura veio do `-r`, o fps continuou do `-q` |
| `-q h --fps 30` | `1080p30` |
| `-r 1080x1920` (vertical) | **`1920p60`** — é a ALTURA, não a largura |

Existe também `SceneFileWriter.get_resolution_directory()`, que devolve
`f"{pixel_height}p{frame_rate}"` (sem o `:g`) — mas quem escreve o caminho é o
`get_dir`. Não é o método que você deve consultar.

### 3.3 `<module_name>` é o *stem* do arquivo de cena

`init_output_directories`: `module_name = config.get_dir("input_file").stem`.
Duas armadilhas:

- **Se `input_file` estiver vazio, o `<module_name>` some** e o caminho vira
  `media/videos//1080p60` → `media/videos/1080p60`. Existe uma pasta assim
  neste repositório, prova de que já aconteceu. Acontece ao chamar
  `render_scene(MinhaCena)` com uma classe cujo módulo não tem `__file__`
  (REPL, `exec`). O `manimx` se protege: `render_scene` preenche `input_file`
  a partir de `sys.modules[scene_class.__module__].__file__`, e `render_file`
  faz `kwargs.setdefault("input_file", path)`.
- `bin/manim -` (cena vinda do **stdin**) fixa `input_file = Path("-")`, cujo
  `.stem` é `"-"` → `media/videos/-/1080p60/`. **[LIDO, NÃO EXECUTADO]**

### 3.4 `<output_name>` e o `-o`

```python
if SceneFileWriter.force_output_as_scene_name:      # o prompt interativo liga isto
    self.output_name = Path(scene_name)
elif config["output_file"] and not config["write_all"]:
    self.output_name = config.get_dir("output_file")
else:
    self.output_name = Path(scene_name)
```

- Sem `-o`: o nome do arquivo é o **nome da classe**, tal e qual (`OlaManim.mp4`).
- Com `-o nome`: `nome.mp4`. A extensão é acrescentada só se faltar
  (`add_extension_if_not_present`).
- **`-o` com caminho absoluto escapa da árvore inteira.** O código faz
  `movie_dir / output_name`, e no `pathlib` um operando absoluto à direita
  vence: `-o /tmp/final.mp4` grava em `/tmp/final.mp4`. Útil e perigoso.
  **[LIDO, NÃO EXECUTADO]**
- **`-o` com subdiretório que não existe quebra**: só `movie_dir` é criado.
- **`-o` + várias cenas = colisão.** No `mx`, `write_all` nunca é ligado (o
  `_build_config` não o escreve), então `bin/mx render arq.py -a -o saida`
  manda **todas** as cenas para `saida.mp4` e só a última sobrevive. No
  `bin/manim -a -o saida` isso não acontece, porque ali `write_all` é `True` e
  o `elif` acima cai fora. **[LIDO, NÃO EXECUTADO]** — na dúvida, não combine
  `-o` com mais de uma cena.

### 3.5 O sufixo `_ManimCE_v0.21.0` — quando aparece e como sumir

`add_version_before_extension(file)` (`utils/file_ops.py:149`) devolve
`f"{stem}_ManimCE_v{__version__}{suffix}"`. Ele é aplicado em **dois** lugares,
e nos dois **só quando você NÃO passou `-o`**:

- `save_image` — o PNG de frame único;
- `init_output_directories` — o GIF.

O `.mp4` **não** recebe o sufixo. Então:

```
sem -o :  Demo.mp4    Demo_ManimCE_v0.21.0.png    Demo_ManimCE_v0.21.0.gif
com -o x:  x.mp4       x.png                        x.gif
```

Se o seu pipeline consome o PNG por nome, ou você passa `-o`, ou lê
`image_file` do JSON. Não escreva o número da versão à mão em script nenhum.

### 3.6 O PNG **não** é separado por qualidade — e isso apaga o seu preview

`images_dir = {media_dir}/images/{module_name}` — sem `{quality}`. Logo:

```bash
bin/mx render cena.py Demo -q l --format png    # media/images/cena/Demo_ManimCE_v0.21.0.png
bin/mx render cena.py Demo -q h --format png    # O MESMO ARQUIVO
```

O preview 480p e o frame de entrega 1080p disputam o mesmo caminho. Se você
precisa dos dois, use `-o` (`-o demo-480`, `-o demo-1080`) ou `--media-dir`
diferente. O `.mp4` não sofre disso: ele carrega o `<quality>` no caminho.

### 3.7 `media_dir` é resolvido contra o **CWD**, e o `mx` sempre o escreve

`bin/mx` **não faz `cd`** — ele monta o ambiente e dá `exec` de onde você
chamou. E `cmd_render` passa `media_dir` **sempre** (default `"media"`), que
`_build_config` transforma em `str(Path(media_dir).resolve())`. Duas
consequências:

1. `bin/mx render` de outro diretório escreve `./media` **ali**, não na raiz do
   projeto.
2. `media_dir` do `manim.cfg` é **sempre sobrescrito** pelo `mx` — configurar
   `media_dir` no arquivo não tem efeito nenhum sobre `mx render`.

Pior: fora da raiz o `manim.cfg` inteiro deixa de ser lido, porque a busca é
`folder_wide = Path("manim.cfg")`, relativa ao CWD (`_config/utils.py:84`).
`max_inflight_encoders` cai de 4 para 1 e `max_files_cached` de 200 para 100,
sem uma linha de aviso. A medição está em **`manim-project` §5** — não a
repita, referencie.

**Regra: rode `bin/mx` da raiz do projeto, com caminho absoluto para a cena se
ela morar fora.** Se o pipeline precisar de outro CWD, passe as chaves na mão
(`-j 4`, `--media-dir …`) ou use a API Python com `config_overrides=`.

---

## 4. Qualidade, resolução e FPS — os três não são a mesma coisa

### 4.1 Os cinco presets (e o sexto, invisível)

`manim/constants.py:206` (`QUALITIES`) e `manimx/presets.py:23`
(`QUALITY_PRESETS`) — os dois concordam nos cinco:

| `-q` | pixels | fps | nome interno | diretório |
|---|---|---|---|---|
| `l` | 854 × 480 | 15 | `low_quality` | `480p15` |
| `m` | 1280 × 720 | 30 | `medium_quality` | `720p30` |
| `h` | 1920 × 1080 | 60 | `high_quality` | `1080p60` |
| `p` | 2560 × 1440 | 60 | `production_quality` | `1440p60` |
| `k` | 3840 × 2160 | 60 | `fourk_quality` | `2160p60` |

Existe um sexto em `QUALITIES`, `example_quality` (854×480 **@30**), com
`"flag": None` — inalcançável por `-q`, e ausente do `QUALITY_PRESETS` do
`manimx`. Ele só aparece se você escrever `quality = example_quality` num
`.cfg`. Não use.

`DEFAULT_QUALITY = "high_quality"`, e o `manim.cfg` deste repositório fixa
`quality = high_quality` explicitamente.

### 4.2 Apelidos: só o `mx` os entende

`manimx.presets.resolve_quality` aceita, além de `l|m|h|p|k`:

```
low low_quality 480p draft            → l
medium medium_quality 720p            → m
high high_quality 1080p hd            → h
production production_quality 1440p 2k → p
fourk fourk_quality 2160p 4k uhd      → k
```

**`bin/manim -q 1080p` FALHA.** A opção lá é um `Choice` construído a partir
das flags (`render_options.py:136`), ou seja apenas `l m h p k`. Já
`manim.cfg` aceita o nome longo (`quality = high_quality`), porque o arquivo
passa por `_determine_quality`. Três vocabulários para a mesma coisa; use
`l|m|h|p|k` e você acerta nos três.

### 4.3 `-r` NÃO ignora o `-q`. Ele sobrescreve só a resolução.

*(Correção de uma afirmação errada da versão anterior desta skill.)* A ordem de
aplicação está no fonte, nos dois caminhos:

**No `bin/manim`** (`_config/utils.py`, `digest_args`):

```python
self.quality = _determine_quality(getattr(args, "quality", None))   # 1º
rflag = args.resolution
if rflag:
    self.pixel_width  = int(rflag[0])                               # 2º
    self.pixel_height = int(rflag[1])
fps = args.frame_rate
if fps:
    self.frame_rate = float(fps)                                    # 3º
```

O *setter* de `quality` escreve `frame_size` **e** `frame_rate`
(`utils.py:1344-1352`). O `-r` que vem depois só mexe em `pixel_*`. Logo o FPS
continua vindo do `-q`.

**No `bin/mx`**: `_build_config` monta um dict cuja **ordem de inserção** é
`quality` → … → `pixel_width`/`pixel_height` → `frame_rate`. E
`ManimConfig.update` aplica as chaves de `_OPTS` nessa ordem (`utils.py:387-391`)
— `quality`, `pixel_width` e `pixel_height` estão todas em `_OPTS`. Mesmo
resultado.

```bash
bin/mx render cena.py Demo -q l -r 1280x720      # 1280×720 @ 15 fps → 720p15
bin/mx render cena.py Demo -q h -r 1080x1920     # 1080×1920 @ 60 fps → 1920p60
bin/mx render cena.py Demo -q h --fps 24         # 1920×1080 @ 24 fps → 1080p24
```

Medição independente confirmando: `manim-project` §7.3 registra `-q l -r
1280x720` gravando em `720p15`.

**Para mudar o FPS existe `--fps`.** É a última das três a ser aplicada.

### 4.4 Sintaxe de `-r` — as duas CLIs diferem

| | aceita |
|---|---|
| `bin/manim -r` | `W,H`, `W;H`, `W-H` (regex `[;,\-]`, `render_options.py:97`) |
| `bin/mx render -r` | `WxH` ou `W,H` (`.lower().replace("x", ",").split(",")`) |

`bin/mx render -r 1920-1080` estoura com um `ValueError` de unpacking. Use
`1920x1080` no `mx` e `1920,1080` no `manim` e você nunca erra.

### 4.5 `-r` muda o buffer de pixels, **não o palco**

`pixel_width/height` é o tamanho do arquivo. O palco do Manim continua
14,222 × 8 unidades. Pedir `-r 1080x1920` para um Shorts dá um mp4 vertical com
a cena **esmagada**, não reenquadrada. Para 9:16 de verdade é preciso mexer em
`frame_width` também:

```python
config.frame_width = config.frame_height * 1080 / 1920   # 8 × 0,5625 = 4,5
```

A receita completa é de `manim-project` §10.3; a margem segura é de
`manim-layout-posicionamento`. Aqui interessa só o efeito no arquivo.

### 4.6 4K

`-q k` no renderer `opengl` estoura os 8 GiB de VRAM desta placa em cena com
muitos mobjects (registrado em `manim-gpu-encoding`). Renderize 4K em `cairo`,
ou entregue 1080p. E lembre que 4K muda o diretório: `2160p60`.

---

## 5. Formatos — os cinco, e como o Manim escolhe a extensão

### 5.1 O mecanismo, antes da tabela

Três coisas decidem o que sai:

1. **`config.format`** — `None|"png"|"gif"|"mp4"|"mov"|"webm"`
   (`utils.py:1060`, validado por `_set_from_list`).
2. **`config.transparent`** — propriedade derivada:
   `background_opacity < 1.0`. Setar `transparent = True` escreve
   `background_opacity = 0.0`.
3. **`config.movie_file_extension`** — `.mp4|.mov|.webm`, **recalculado
   sozinho** por `resolve_movie_file_extension` toda vez que `format`,
   `transparent` ou `background_opacity` mudam:

```python
if is_transparent:  ext = ".webm" if format == "webm" else ".mov"
elif format == "webm": ext = ".webm"
elif format == "mov":  ext = ".mov"
else:                  ext = ".mp4"
```

É por isso que **você nunca deve setar `movie_file_extension` na mão**: o
Manim o reescreve, com um aviso confuso (`Output format changed to '.mp4' to
support transparency`). O comentário de 8 linhas em `manimx/render.py` registra
essa lição. Use `format` e `transparent`, que são as entradas que ele respeita.

E o encode: o codec é escolhido **por partial movie**
(`open_partial_movie_stream`) — `libx264`/`yuv420p` por padrão, `libvpx-vp9`
para `.webm`, `qtrle`/`argb` quando transparente. A junção final é **cópia de
pacotes** (`add_stream_from_template` + `mux`), sem re-encode. A única exceção
é o GIF, que decodifica tudo de novo e passa por um filtergraph
`split → palettegen → paletteuse`. Detalhe de codec, peso e NVENC:
**`manim-gpu-encoding`**, que é dona do assunto.

### 5.2 A tabela

| Objetivo | `bin/mx render` | o que sai |
|---|---|---|
| MP4 (padrão) | *(nada)* | `.mp4` H.264, `h264_nvenc` no `mx` |
| MP4 de entrega | `--codec nvenc-quality` | `.mp4`, NVENC p7 + AQ |
| MP4 sem GPU | `--codec x264` | `.mp4`, libx264 crf 23 |
| Web leve | `--codec webm` ou `--format webm` | `.webm` VP9 |
| Transparente para NLE | `-t` | `.mov` qtrle/argb |
| GIF | `--format gif` | `.gif` paleta `rgb8` |
| **Um** frame (o último) | `--format png` | `.png` |
| **Todos** os frames | ✗ — use `bin/manim --format png` | `.png` numerado |
| QuickTime sem alfa | `--format mov` | `.mov` **H.264, sem canal alfa** |

**`--format mov` não é transparência.** Ele só troca o contêiner; o codec segue
`libx264`/`yuv420p`. Quem liga o canal alfa é `-t`. É o erro mais comum de quem
vem do ffmpeg.

**NVENC não faz alfa nem VP9.** Pedir `-t --codec nvenc` faz a camada `manimx`
ignorar o NVENC de propósito (`render.py`: `if use_gpu and not transparent and
fmt not in ("gif","png","webm")`) e registrar um `logger.info`. O JSON reporta
`"codec": "qtrle"` — honesto. **Não é falha.**

### 5.3 GIF: dois detalhes que estragam o arquivo

- **O nome ganha o sufixo da versão** (`Demo_ManimCE_v0.21.0.gif`) a menos que
  você passe `-o`. Só o GIF e o PNG sofrem disso, o mp4 não.
- **O GIF herda o frame rate do `-q`.** Um `-q h --format gif` gera um GIF de
  **60 fps** com paleta de 256 cores por frame — enorme e sem ganho visual.
  Para README, `-q m --format gif` (30 fps) ou `--fps 12`.

Os `partial_movie_files` de um render de GIF continuam sendo `.mp4`
(`resolve_movie_file_extension` cai no `else`); só o arquivo final é `.gif`.

### 5.4 PNG: `mx --format png` e `manim --format png` fazem **coisas
diferentes**

Esta é a descoberta que mais muda o dia a dia, e ela não está em documentação
nenhuma.

**No `bin/manim`**, `--format png` significa *sequência de imagens*:
`write_to_movie()` devolve `False` (`file_ops.py:121`), nenhum vídeo é escrito,
e `SceneFileWriter.write_frame` grava **cada frame** como PNG:

```python
if is_png_format() and not config["dry_run"]:
    target_dir = self.image_file_path.parent / self.image_file_path.stem
    self.output_image(image, target_dir, extension, config["zero_pad"])
```

`output_image` concatena — `target_dir` é um **prefixo**, não uma pasta — e
`zero_pad` vale **4** por padrão (`default.cfg:36`). Saída:
`media/images/<mod>/Demo0000.png`, `Demo0001.png`, … e no fim o log
`N images ready at …`. Uma cena de 10 s em `-q h` produz **600 arquivos**.

**No `bin/mx render --format png`**, o `manimx` acrescenta `save_last_frame`:

```python
save_last_frame=save_last_frame or fmt == "png",   # manimx/render.py
```

E `save_last_frame` liga `skip_animations` em **todas** as animações
(`cairo_renderer.py:255`), então `add_frame` sai cedo e nenhum frame vira
arquivo; no fim, `scene_finished` chama `file_writer.save_image(...)` e grava
**um** PNG. É por isso que `CODEC_PRESETS["png"]` diz *"Só o último frame, como
PNG (equivale a `-s`)"*.

| você quer | comando |
|---|---|
| um frame para OLHAR o layout | `bin/mx render cena.py Demo -q l --format png` |
| o último frame como pôster | idem (leia `image_file`) |
| a sequência inteira | `bin/manim -qh --format png cena.py Demo` |
| a sequência com N dígitos | `bin/manim -qh --format png -0 6 cena.py Demo` |

`-g/--save_pngs` e `-i/--save_as_gif` ainda existem, mas são **depreciados**:
`commands.py:78-84` só emite um warning e reescreve `format` para `png`/`gif`.
Use `--format`.

### 5.5 `-s` (`--save_last_frame`) é o atalho barato — e não é grátis

`-s` põe `skip_animations = True` para tudo e força `write_to_movie = False`
(`digest_args`). O `construct` **roda inteiro** — todos os mobjects são
construídos, todo `Text` vai ao Pango, todo `MathTex` vai ao LaTeX — mas nenhum
frame é rasterizado nem codificado. Numa cena pesada de texto, `-s` continua
pagando o custo do texto; ele economiza só a rasterização e o encode.

`bin/manim -ql -s cena.py Demo` e `bin/mx render cena.py Demo -q l --format png`
produzem **o mesmo arquivo, no mesmo caminho**.

---

## 6. Renderizar só um pedaço

### 6.1 `-n a,b` — só no `bin/manim`

```bash
bin/manim -ql -n 4,7 scenes/demo.py Demo    # animações 4, 5, 6 e 7
bin/manim -ql -n 4   scenes/demo.py Demo    # da 4 até o fim
```

Aceita `a`, `a,b`, `a;b`, `a-b` (mesma regex do `-r`). O `mx render` **não
expõe `-n`** — nem a CLI nem `render_scene` têm o parâmetro; pela API Python
seria `config_overrides={"from_animation_number": 4, "upto_animation_number": 7}`.

Semântica exata (`cairo_renderer.py`, `update_skipping_status`):

```python
if config.from_animation_number > 0 and self.num_plays < config.from_animation_number:
    self.skip_animations = True
if config.upto_animation_number >= 0 and self.num_plays > config.upto_animation_number:
    self.skip_animations = True
    raise EndSceneEarlyException()
```

- Índices são **0-based** e os **dois extremos entram**: `-n 4,7` grava as
  animações 4, 5, 6 e 7.
- `EndSceneEarlyException` é capturada por `Scene.render` — a cena **termina
  ali**, e o que vinha depois nunca roda.
- **Nada é "pulado" de verdade.** As animações antes de `a` são executadas
  normalmente; só não escrevem frame. O estado do palco é o mesmo de um render
  completo — é exatamente o mecanismo que faz as cenas em partes emendarem
  invisíveis (`manim-presentation-parts`). O preço é que `-n 8,9` numa cena de
  10 animações **não é 5× mais rápido**: você paga toda a lógica das oito
  primeiras.

**A armadilha:** o arquivo de saída tem o **mesmo nome** de um render completo.
Um `-n 4,7` sobrescreve calado o mp4 bom com um trecho de 4 animações. Sempre
combine `-n` com `-o` (`-o demo-trecho`) ou com `--media-dir /tmp/corte`.

### 6.2 `--dry_run` — renderiza e não escreve nada

Só no `bin/manim`. O *setter* de `dry_run` zera `write_to_movie` e `write_all`,
e `init_output_directories` retorna antes de criar qualquer pasta. Serve para
duas coisas: cronometrar a cena sem o custo do encode, e provar que ela
**constrói** sem erro antes de gastar um render de 4K.

```bash
bin/manim -ql --dry_run scenes/demo.py Demo
```

Pela API: `config_overrides={"dry_run": True}`.

### 6.3 `Scene(skip_animations=True)`

`Scene.__init__` aceita `skip_animations: bool = False`, que vira o
`_original_skipping_status` do renderer. É o caminho programático para o efeito
de `-s` sem tocar em `config`. Raramente é o que você quer — prefira
`--format png`.

---

## 7. Seções (capítulos) — o arquivo que elas produzem

A **semântica** de `next_section` (quando cortar, o que é um `DefaultSectionType`,
como o `skip_animations` das seções é usado para renderizar uma parte só) é de
**`manim-cenas-secoes`**, e o formato em partes para slide é de
**`manim-presentation-parts`**. Aqui está só o que sai no disco.

```python
class Aula(Scene):
    def construct(self):
        self.next_section("Introdução")
        ...
        self.next_section("Demonstração", skip_animations=False)
        ...
```

Assinatura conferida no índice:
`Scene.next_section(self, name: str = 'unnamed', section_type: str = DefaultSectionType.NORMAL, skip_animations: bool = False) -> None`.

```bash
bin/manim -qh --save_sections scenes/aula.py Aula
```

`mx render` **não tem a flag**; pela API é `render_scene(..., save_sections=True)`,
e aí o `RenderResult.sections` vem preenchido (`sorted(sections_dir.glob("*.mp4"))`).

O que aparece em `media/videos/<mod>/<quality>/sections/`:

- um mp4 por seção, nomeado
  `f"{output_name}_{índice:04}_{name}{ext}"` → `Aula_0000_Introdução.mp4`;
- um `Aula.json` com a lista de seções, cada uma com `name`, `type`, `video` e
  os metadados do vídeo (`width`, `height`, `nb_frames`, `duration`,
  `avg_frame_rate`, `codec_name`, `pix_fmt`), lidos por `get_video_metadata`.

Três detalhes que mordem:

1. **O nome da seção vai cru para o nome do arquivo** — espaço, acento e
   barra incluídos. `next_section("Passo 1/2")` cria um caminho com `/`.
   Use nomes de arquivo desde o começo (`"passo-1"`).
2. **Seção com `skip_animations=True` não gera vídeo nem entra no índice**
   (`video=None` em `SceneFileWriter.next_section`).
3. **Seção vazia é descartada** (`finish_last_section`), então os índices
   `0000, 0001, …` podem não bater com a ordem das suas chamadas.

O vídeo completo continua sendo gerado normalmente; `--save_sections` **soma**,
não substitui.

---

## 8. Cache pelo lado do render

O que o hash cobre, o que faz uma cena ser cara e como podar `media/` em
profundidade é de **`manim-performance-cache`**. Aqui: quais flags existem e o
que cada uma toca.

| flag | onde | efeito |
|---|---|---|
| `--no-cache` (`mx`) / `--disable_caching` (`manim`) | por render | não reaproveita partial movie; os arquivos passam a se chamar `uncached_00000.mp4` |
| `--flush_cache` | **só `bin/manim`** e a API | apaga TODOS os partial movies daquela cena, no fim do render |
| `max_files_cached` | `manim.cfg` (200 aqui, 100 no default) | poda os mais antigos por `st_atime` |
| `--seed N` | só `bin/manim` | `random.seed()` + `np.random.seed()` em `Scene.__init__` |

**Quando desligar o cache:** a cena lê CSV/JSON/API, usa `random` sem semente,
ou depende de data/arquivo em disco. O hash cobre a chamada de `play`, não o
mundo lá fora — senão você reaproveita o vídeo velho com o dado novo
(`manim-project` §10.7).

**`--seed` é a alternativa elegante** para o caso do `random`: com a semente
fixa a cena vira determinística e o cache volta a ser confiável, em vez de
ficar desligado para sempre. `Scene(random_seed=…)` faz o mesmo por cena
(`scene/scene.py:180, 222-224`).

Sobre `--flush_cache` e `clean_cache`, um detalhe do fonte que vale conhecer:
os dois filtram a lista com `if file_name != "partial_movie_file_list.txt"`,
mas `Path.iterdir()` devolve **`Path`**, e `Path != str` é sempre verdadeiro —
o filtro nunca exclui nada. Na prática o `.txt` conta para o `max_files_cached`
e é apagado junto. Inofensivo (ele é reescrito a cada junção), mas explica um
"200 arquivos" que na verdade são 199 vídeos. **[LIDO, NÃO EXECUTADO]**

E uma pegadinha de nomenclatura que já mandou gente para o lugar errado:
**`--no-cache`/`--disable_caching` NÃO tem nada a ver com o cache de LaTeX.**
O `.tex` compilado vive em `media/Tex` e obedece a outro mecanismo. Ver
`manim-text-latex`.

---

## 9. Várias cenas

### 9.1 Pelo `mx`

```bash
bin/mx render scenes/aula.py --all -q h --codec nvenc --json     # todas
bin/mx render scenes/aula.py Intro Meio Fim -q h --json          # três, nesta ordem
bin/mx scenes scenes/aula.py                                     # quais existem
```

`-a/--all` vence sobre nomes explícitos (`render_file` checa `all_scenes`
primeiro). O JSON é uma lista com um objeto por cena, na ordem de **definição
no arquivo** (`load_scene_classes` ordena por `__firstlineno__`, não
alfabeticamente). Exit 1 se qualquer uma falhar; as outras ainda rodam.

### 9.2 Em Python

```python
from manimx.render import render_many      # NÃO é exportado em `manimx`

results = render_many([
    {"file_path": "scenes/a.py", "scene_names": "A", "quality": "h"},
    {"file_path": "scenes/b.py", "all_scenes": True, "quality": "m"},
], stop_on_error=False)
```

`render_many` é **sequencial de propósito**: o `config` do Manim é um singleton
global e mutável; duas cenas ao mesmo tempo **no mesmo processo** corrompem o
estado uma da outra. Paralelismo real = processos separados, e isso é
**`manim-batch-pipeline`** (com `tools/batch_render.py`) — que também trata a
corrida de `media/Tex` entre workers e o teto de sessões NVENC.

### 9.3 O `bin/manim` PERGUNTA — e trava o agente

`manim/utils/module_ops.py:110` — se você não nomeia a cena, o arquivo tem mais
de uma e nenhuma casou, ele cai em `prompt_user_for_choice`, que faz
`console.input(...)`:

```
1: OlaManim
2: Pitagoras
...
Choice(s):
```

Num terminal isso **bloqueia**. Num pipe, o `EOFError` é capturado e vira
`sys.exit(1)` — silencioso o bastante para parecer outra coisa. O `mx` nunca
faz isso: ele levanta `ValueError` listando as cenas.

**Nunca chame `bin/manim arquivo.py` sem nomear a cena ou passar `-a`.**

O prompt também tem um efeito colateral: ele liga
`SceneFileWriter.force_output_as_scene_name = True`, atributo **de classe**,
que passa a ignorar o seu `-o` dali em diante no mesmo processo.

---

## 10. A API Python, inteira

### 10.1 As quatro funções

```python
from manimx import render_file, render_scene, list_scenes, RenderResult
from manimx.render import load_scene_classes, render_many   # não exportados no topo
```

| função | assinatura |
|---|---|
| `load_scene_classes` | `(file_path: str \| Path) -> list[type]` |
| `list_scenes` | `(file_path: str \| Path) -> list[str]` |
| `render_scene` | `(scene_class: type, *, …23 kwargs…) -> RenderResult` |
| `render_file` | `(file_path, scene_names=None, *, all_scenes=False, **kwargs) -> RenderResult \| list[RenderResult]` |
| `render_many` | `(jobs: Iterable[dict], *, stop_on_error=False) -> list[RenderResult]` |

`render_file` devolve **um** `RenderResult` quando você pediu uma cena só (nome
único ou arquivo com uma cena), e uma **lista** quando pediu várias ou
`all_scenes=True`. Trate os dois casos, ou normalize:
`res if isinstance(res, list) else [res]` — é o que o próprio `cmd_render` faz.

A docstring de `manimx/__init__.py` mostra `from manimx import render_file,
quality` — **`quality` não existe**; é erro do pacote, já registrado em
`manim-project` §8.3.

### 10.2 `render_scene` — kwarg × flag `mx` × flag `manim`

Esta é a tabela de tradução que evita ir procurar em três lugares.

| kwarg de `render_scene` | default | `bin/mx render` | `bin/manim` |
|---|---|---|---|
| `quality` | `"h"` | `-q/--quality` | `-q/--quality` |
| `renderer` | `"cairo"` | `--renderer {cairo,opengl}` | `--renderer` |
| `codec` | `"x264"` | `--codec` (default **`nvenc`**) | — (libx264 fixo) |
| `theme` | `None` | `--theme` | — |
| `gpu` | `None` | — (decide pelo codec) | — |
| `fmt` | `None` | `--format {mp4,gif,webm,mov,png}` | `--format` |
| `transparent` | `False` | `-t` | `-t/--transparent` |
| `fps` | `None` | `--fps` | `--fps/--frame_rate` |
| `resolution` | `None` | `-r WxH` | `-r W,H` |
| `media_dir` | `None` | `--media-dir` (default `"media"`) | `--media_dir` |
| `output_file` | `None` | `-o/--output` | `-o/--output_file` |
| `input_file` | auto | — (o arquivo posicional) | — (idem) |
| `disable_caching` | `False` | `--no-cache` | `--disable_caching` |
| `flush_cache` | `False` | **—** | `--flush_cache` |
| `save_last_frame` | `False` | via `--format png` | `-s/--save_last_frame` |
| `save_sections` | `False` | **—** | `--save_sections` |
| `background_color` | `None` | `--background` | — (`-c` é `--config_file`!) |
| `max_inflight_encoders` | `None` | `-j/--parallel-encoders` | `--max-inflight-encoders` |
| `encoder_queue_size` | `None` | **—** | `--encoder-queue-size` |
| `preview` | `False` | **—** | `-p/--preview` |
| `verbosity` | `"WARNING"` | `--verbosity` | `-v/--verbosity` |
| `config_overrides` | `None` | **—** | — |
| `raise_on_error` | `False` | — | — |

Quatro pegadinhas nesta tabela:

- **`--max-inflight-encoders` e `--encoder-queue-size` usam HÍFEN**, contra a
  convenção de sublinhado de todo o resto do CLI da CE
  (`--save_last_frame`, `--disable_caching`, `--media_dir`…). O `click` **não**
  aceita a forma com sublinhado.
- **`--media-dir` (mx, hífen) × `--media_dir` (manim, sublinhado).**
- **`-v` significa coisas diferentes.** No `mx` é `--verbose` (log de debug da
  camada, sem argumento). No `manim` é `--verbosity`, e **exige** um valor do
  conjunto `DEBUG|INFO|WARNING|ERROR|CRITICAL` — `bin/manim -v cena.py Cena`
  engole `cena.py` como verbosidade e falha.
- **`-c` no `manim` é `--config_file`**, não cor de fundo. `--background_color`
  não existe na CLI (`manim-troubleshooting` já registra).

### 10.3 O que o `mx render` impõe e você não escolhe

`_build_config` grava três chaves fixas em todo render pelo `mx`:

```python
"notify_outdated_version": False,   # nada de HTTP para o pypi.org
"progress_bar": "none",             # nada de barra
"verbosity": verbosity.upper(),     # default WARNING (o manim.cfg pede INFO)
```

Por isso `mx render` é mudo comparado a `bin/manim`, e por isso a linha
`File ready at '…'` (nível INFO) **não aparece** — o `mx` imprime o caminho por
conta própria.

O contraponto: `bin/manim` rodado **fora** da raiz do projeto herda
`notify_outdated_version = True` do `default.cfg` e faz um
`urllib.request.urlopen("https://pypi.org/pypi/manim/json", timeout=10)` no fim
de **cada** render (`cli/render/commands.py:130-140`). Numa máquina sem rede,
são 10 s de espera por render, depois do vídeo já pronto. `--silent` desliga.

### 10.4 Ler o resultado direito

```python
from manimx import render_file

r = render_file("scenes/demo.py", "Demo", quality="h", codec="nvenc")
if not r:                              # falsy quando success is False
    raise RuntimeError(r.error + "\n" + (r.traceback_text or ""))
if r.output_file is None:              # sucesso SEM arquivo — §2.1(c)
    raise RuntimeError("a cena não produziu animação nenhuma")
print(r.output_file)                   # pathlib.Path absoluto
```

`raise_on_error=True` propaga a exceção da cena em vez de embrulhá-la — útil
em teste, ruim em pipeline (você perde o `elapsed_s` e o resto do relatório).

---

## 11. `tempconfig` e `config_overrides` — a última milha

Quando a chave que você precisa não é kwarg de nada:

```python
from manimx.render import render_scene
from scenes.demo import Demo

r = render_scene(
    Demo,
    quality="h",
    config_overrides={
        "frame_width": 16,             # palco mais largo
        "zero_pad": 6,
        "from_animation_number": 4,    # o `-n` que a CLI do mx não tem
        "upto_animation_number": 7,
        "dry_run": False,
    },
)
```

`config_overrides` é despejado no dict que vai para `tempconfig(cfg)`
(`render.py`: `extra = dict(config_overrides or {})`, depois `cfg.update(extra)`),
e por ser o **último** `update` ele vence qualquer coisa que os kwargs tenham
posto.

### 11.1 Precedência completa, do mais fraco ao mais forte

```
1. manim/_config/default.cfg                       (biblioteca)
2. ~/.config/manim/manim.cfg                       (não existe nesta máquina)
3. ./manim.cfg                                     ← do CWD, não da raiz do projeto
4. -c/--config_file                                (substitui só o nível 3)
5. flags da CLI                                    (digest_args)
6. config.<chave> = … / tempconfig(…) / config_overrides
```

Os três primeiros são lidos **no `import manim`**, uma vez. Os níveis 3 e 4 são
mutuamente exclusivos: `make_config_parser(custom_file)` troca o `manim.cfg` do
CWD pelo arquivo passado, e **não** pelos níveis 1 e 2.

### 11.2 A armadilha silenciosa do `tempconfig`

`manim/_config/__init__.py:78`:

```python
temp = {k: v for k, v in temp.items() if k in original}
```

`original` é um `ManimConfig`, cujo `__contains__` (`utils.py:341`) tenta
`getattr(self, key)` e devolve `False` só em `AttributeError`. Traduzindo:

> **Qualquer chave que não seja uma propriedade de `ManimConfig` é descartada
> em silêncio.** Sem erro, sem warning, sem log.

`tempconfig({"backgroud_color": "#FFF"})` (com o typo) não faz nada e não
avisa. `config_overrides={"quality": "k"}` funciona; `{"qualidade": "k"}` não.
Confira o nome antes:

```python
from manim import config
print("frame_width" in config, "frame_size" in config, "typo_qualquer" in config)
# True True False
```

### 11.3 As duas classes de chave, e por que a ordem importa

`ManimConfig` tem **67** chaves em `_OPTS` (o dicionário interno `_d`) e **74**
propriedades. As **7 propriedades que NÃO estão em `_OPTS`** são derivadas:

```
aspect_ratio   bottom   frame_size   left_side   right_side   top   transparent
```

`ManimConfig.update` aplica em **dois passes** (`utils.py:387-395`): primeiro
as chaves de `_OPTS`, na ordem de inserção do dict; depois as sete derivadas.
Duas consequências práticas:

- `transparent` é sempre aplicado **depois** de `format` — é isso que faz
  `resolve_movie_file_extension` acertar a extensão. Se fosse antes, um
  `--format webm -t` sairia `.mov`.
- Entre chaves de `_OPTS`, quem manda é a **ordem em que você escreveu o
  dict**. `{"pixel_width": 1280, "quality": "h"}` termina em 1920×1080 (o
  `quality` reescreve `frame_size`); `{"quality": "h", "pixel_width": 1280}`
  termina em 1280. É a mesma mecânica de §4.3.

### 11.4 Ver a config de verdade

```bash
bin/manim cfg show          # NÃO mostra a config efetiva
```

`manim cfg show` imprime o **parser** — os arquivos `.cfg` mesclados que ele
encontrou a partir do CWD. Ele não sabe de flag de CLI, nem de `tempconfig`,
nem de `config.x = y`. Para a config efetiva, só Python:

```python
from manim import config
for k in sorted(config):
    print(f"{k:28s} {config[k]!r}")
```

Os outros subcomandos: `manim cfg write -l {user,cwd}` é **interativo** e
**sobrescreve um `manim.cfg`** — nunca rode isso num agente; `manim cfg export
-d DIR` copia o arquivo atual. Ainda existem `manim checkhealth` (use
`bin/mx doctor`, que é mais completo), `manim init project|scene` e
`manim plugins` (nenhum plugin instalado aqui — `manim-project` §13.7).

---

## 12. O `bin/manim` cru — o inventário completo das flags

Quatro grupos, definidos em `manim/cli/render/`. Tudo abaixo existe na 0.21.0;
os defaults vêm de `default.cfg` e do `manim.cfg` deste repositório.

### 12.1 Render (`render_options.py`)

| flag | o que faz |
|---|---|
| `-n, --from_animation_number a[,b]` | recorta o intervalo de animações (§6.1) |
| `-a, --write_all` | todas as cenas do arquivo |
| `--format {png,gif,mp4,webm,mov}` | formato de saída (§5) |
| `-s, --save_last_frame` | só o último frame, como PNG |
| `-q, --quality {l,m,h,p,k}` | preset (§4.1) |
| `-r, --resolution "W,H"` | resolução; **não** mexe no FPS |
| `--fps, --frame_rate` | frame rate |
| `--max-inflight-encoders N` | encoders simultâneos (**hífen**) |
| `--encoder-queue-size N` | buffers por encoder; ignorado se inflight = 1 |
| `--renderer {cairo,opengl}` | rasterizador |
| `-g, --save_pngs` | **depreciado** → `--format png` |
| `-i, --save_as_gif` | **depreciado** → `--format gif` |
| `--save_sections` | vídeos por seção (§7) |
| `-t, --transparent` | canal alfa (`.mov` qtrle) |
| `--use_projection_{fill,stroke}_shaders` | só opengl |

### 12.2 Saída (`output_options.py`)

`-o/--output_file` · `-0/--zero_pad {0..9}` · `--write_to_movie` ·
`--media_dir` · `--log_dir` · `--log_to_file`

`--write_to_movie` existe por causa do opengl, que **não escreve arquivo
sozinho** — ele abre janela. O `manimx` injeta a chave automaticamente
(`render.py`: `if renderer == "opengl" and fmt != "png" and not
save_last_frame: cfg["write_to_movie"] = True`); no CLI cru, `digest_args`
força `write_to_movie = False` quando o renderer é opengl e você não passou a
flag.

### 12.3 Globais (`global_options.py`)

`-c/--config_file` · `--custom_folders` · `--disable_caching` ·
`--flush_cache` · `--tex_template` · `-v/--verbosity {DEBUG…CRITICAL}` ·
`--notify_outdated_version/--silent` · `--enable_gui` · `--gui_location` ·
`--fullscreen` · `--enable_wireframe` · `--force_window` · `--dry_run` ·
`--no_latex_cleanup` · `--preview_command` · `--seed N`

`--custom_folders` troca toda a árvore de saída pela seção `[custom_folders]`
do `.cfg` — que por padrão achata tudo em `videos/` (sem `<module_name>` nem
`<quality>`). Útil para entregar num diretório limpo; péssimo para renderizar
em várias qualidades, porque elas passam a se sobrescrever.

`--no_latex_cleanup` preserva `.aux`/`.dvi`/`.log` em `media/Tex` — a flag que
`manim-troubleshooting` manda usar quando o LaTeX falha. Ela **não existe no
`mx render`**; use `bin/manim` para esse diagnóstico.

### 12.4 Facilidade (`ease_of_access_options.py`)

`--progress_bar {display,leave,none}` · `-p/--preview` ·
`-f/--show_in_file_browser` · `--jupyter`

`-p` abre o arquivo no player do sistema depois de renderizar (`open_file`).
Num agente é ruído — e com `--renderer opengl` ele abre uma **janela ao vivo**,
que não fecha sozinha.

### 12.5 O truque do `-`

```bash
echo 'class X(Scene):
    def construct(self):
        self.play(Write(Text("oi", color=BLACK)))' | bin/manim -ql --format png -
```

Com `-` no lugar do arquivo, o Manim lê o código do **stdin**, cria um módulo
`input_scenes` e ainda prepende `from manim import *` se você não escreveu.

**Atenção ao `-s` no exemplo acima, e é a §5.4 se aplicando aqui:** sem ele,
`--format png` cai no caminho de **sequência**, não no de frame único —
`scene_file_writer.py:572` (`if is_png_format() and not config["dry_run"]`)
grava **um PNG por frame**, e eles vão para `images_dir`
(`{media_dir}/images/{module_name}`, `default.cfg:91`), **não** para
`video_dir`. Com o módulo chamado `-`, isso é `media/images/-/X0000.png`,
`X0001.png`, … — dezenas de arquivos, não um.

Para o frame único que você provavelmente queria:

```bash
echo 'class X(Scene):
    def construct(self):
        self.play(Write(Text("oi", color=BLACK)))' | bin/manim -ql -s --format png -
```

**[LIDO, NÃO EXECUTADO]** Serve para um teste de uma linha sem sujar o
repositório; `mx render` não tem equivalente (e o `mx render --format png` passa
`-s` por baixo, por isso ele dá um frame só).

---

## 13. Provar o que saiu, sem `ffprobe`

O ManimCE traz um leitor de metadados baseado em PyAV, exportado no topo:

```python
from manim import get_video_metadata

m = get_video_metadata("media/videos/exemplos/1080p60/OlaManim.mp4")
# {'width': 1920, 'height': 1080, 'nb_frames': '...', 'duration': '...',
#  'avg_frame_rate': '60/1', 'codec_name': 'h264', 'pix_fmt': 'yuv420p'}
```

Assinatura conferida no índice:
`get_video_metadata(path_to_video: str | os.PathLike) -> VideoMetadata`
(`manim/utils/commands.py:47`). É o mesmo dicionário que vai para o
`sections/<Cena>.json`.

Isso responde, sem sair do venv, às três perguntas que mais aparecem depois de
um lote:

```python
# 1. tudo saiu na mesma resolução e no mesmo fps?
{(m["width"], m["height"], m["avg_frame_rate"]) for m in map(get_video_metadata, arquivos)}
#    esperado: um conjunto de UM elemento

# 2. isto saiu em NVENC mesmo?
get_video_metadata(f)["codec_name"]      # 'h264' — o container não distingue
                                          # nvenc de libx264; ver manim-gpu-encoding §17

# 3. o vídeo tem a duração que eu esperava?
float(get_video_metadata(f)["duration"])
```

Para listar o que foi escrito, existe `get_dir_layout(dirpath: Path) ->
Generator[str, None, None]` (caminhos relativos, recursivo).

**Isto NÃO substitui olhar o frame.** Metadado certo com texto branco no branco
é metadado certo. O ciclo de conferência visual — e a lista do que **não dá
erro nenhum** — é de **`manim-verificacao-visual`**.

---

## 14. O ciclo de iteração

Do mais barato ao mais caro. Só suba um degrau quando o anterior estiver certo.

```bash
# 0. a cena sequer constrói?  (sem escrever nada)
bin/manim -ql --dry_run scenes/demo.py Demo

# 1. um frame, para OLHAR o layout   (~1 s; e é o passo que ninguém pula impunemente)
bin/mx render scenes/demo.py Demo -q l --format png --json

# 2. rascunho 480p15
bin/mx render scenes/demo.py Demo -q l --codec nvenc-fast

# 3. revisão 720p30
bin/mx render scenes/demo.py Demo -q m --codec nvenc

# 4. entrega 1080p60
bin/mx render scenes/demo.py Demo -q h --codec nvenc-quality -j 4 --json
```

Custos de referência (medidos por `manim-project` em 2026-08-19, nesta máquina;
**não reexecutados aqui**): `mx scenes` 0,86–0,98 s (ele **importa** o arquivo),
`mx presets` 0,11 s, `mx doctor` 1,84 s; um render de 2 animações em `-q h`
levou 4,17 s de cena e 6,45 s de parede, gerando 66 KiB de mp4. O deck
consumidor `~/Projects/aulas` mediu 1080p60/NVENC em **0,29 MB por segundo de
vídeo**, com dispersão de 0,07 (cena quase parada) a 0,66 (palco inteiro em
movimento) — a régua para decidir o que entra no git.

**Duas armadilhas do ciclo, ambas do mundo real:**

1. **O passo 1 escreve no mesmo PNG do passo 4** (§3.6). Se você guardou o PNG
   de entrega e depois iterou em `-q l`, ele já foi.
2. **Os passos 2 e 3 escrevem em diretórios diferentes do 4** (`480p15`,
   `720p30`, `1080p60`) — então o mp4 do preview **não** sobrescreve o de
   entrega, mas fica no disco pesando. `media/videos/exemplos/` neste
   repositório tem quatro pastas de qualidade pelo mesmo motivo. Se o seu
   pipeline copia "o mp4 mais recente", ele vai pegar o errado: leia
   `output_file`.

---

## 15. Armadilhas, em uma tela

| Sintoma | Causa | Correção |
|---|---|---|
| exit 0, JSON ok, **nenhum mp4** | todas as animações puladas → `combine_to_movie` desiste | teste `success && output_file`; ver `manim-presentation-parts` |
| `--json` não imprimiu nada, exit 1 | erro de **import** / cena inexistente / cena ambígua | leia **stderr**; `mx scenes` para os nomes |
| "o render sumiu com o meu PNG" | `images_dir` não tem `{quality}` | `-o` diferente por qualidade |
| PNG chamado `X_ManimCE_v0.21.0.png` | `add_version_before_extension` quando não há `-o` | passe `-o`, ou leia `image_file` |
| GIF idem, e enorme | sufixo de versão + fps do `-q` | `-o nome --fps 12` |
| `--format png` gerou 600 arquivos | você usou `bin/manim`, não `mx` | `bin/mx … --format png`, ou `-s` |
| foi parar em `720p15` | `-r` mexe só na resolução; o fps veio do `-q` | acrescente `--fps` |
| `1920p60` num vídeo vertical | o diretório usa a **altura** | é o comportamento correto |
| `.mov` sem canal alfa | `--format mov` só troca o contêiner | use `-t` |
| `-t --codec nvenc` "ignorou a GPU" | NVENC não faz alfa; a camada avisa e usa qtrle | é o certo; `manim-gpu-encoding` |
| `manim` travado sem imprimir nada | prompt interativo de escolha de cena | nomeie a cena ou use `-a` |
| render "pendurado" 10 s no fim, offline | `notify_outdated_version` batendo no pypi.org | `--silent`, ou rode da raiz (o `manim.cfg` já desliga) |
| `--max_inflight_encoders` não existe | essa flag usa **hífen** | `--max-inflight-encoders` |
| `bin/manim -v cena.py Cena` falha | `-v` é `--verbosity` e exige valor | `-v INFO` ou nada |
| `tempconfig({...})` não fez efeito | chave que não é propriedade de `ManimConfig` → descartada calada | `print("chave" in config)` antes |
| `-o` com várias cenas: só sobrou uma | todas escreveram no mesmo nome | não combine, ou use `-a` no `bin/manim` |
| `-n 4,7` apagou o vídeo bom | mesmo nome de arquivo | `-n … -o trecho` |
| `-n 8,9` não ficou mais rápido | animações puladas ainda EXECUTAM | é por design |
| fora da raiz, tudo mais lento | `manim.cfg` é lido do CWD | rode da raiz (`manim-project` §5) |
| `--renderer=opengl` não gerou arquivo | opengl não escreve sem `--write_to_movie` | use `mx` (ele injeta) ou passe a flag |
| `-q k` no opengl estourou a VRAM | 8 GiB nesta placa | 4K em `cairo` |

---

## 16. Onde esta skill para

| A pergunta virou… | Skill |
|---|---|
| "qual codec?", "está lento", "o mp4 pesa demais", NVENC, `mx bench` | **`manim-gpu-encoding`** |
| muitas cenas em **processos** paralelos, CI, corrida de `media/Tex` | **`manim-batch-pipeline`** |
| o que o hash do cache enxerga, o que faz uma cena ser cara, podar `media/` | **`manim-performance-cache`** |
| de qual `Scene` herdar, `setup`/`construct`/`tear_down`, semântica de `next_section` | **`manim-cenas-secoes`** |
| cortar a cena em partes que o apresentador avança, medir a emenda | **`manim-presentation-parts`** |
| **olhar** o frame e julgar: cortou? sumiu? sobrepôs? contraste? | **`manim-verificacao-visual`** |
| traceback, `dvisvgm`, ambiente quebrado, bissecção | **`manim-troubleshooting`** |
| o nome/assinatura/kwarg de uma classe | **`manim-api-discovery`** |
| cor de fundo, tema, **decidir** por transparência/alfa | **`manim-color-theming`** |
| "cabe na tela?", margem, 9:16 de verdade | **`manim-layout-posicionamento`** |
| `run_time`, `rate_func`, `lag_ratio`, o ritmo do vídeo | **`manim-composicao-ritmo`** |
| o mapa do repositório e qual skill usar | **`manim-project`** |

**Buracos declarados** — assuntos vizinhos que hoje não têm dona; não invente
comportamento, confirme com `bin/mx show` antes de escrever:

- **`ManimConfig` como objeto** (as 74 propriedades, `parse_cli_ctx`,
  `parse_theme`, `make_config_parser`): esta skill cobre a precedência e o
  `tempconfig`, mas não há skill de configuração. O que está em §11 é o que
  existe.
- **Janela e preview interativo do ManimCE** (`--enable_gui`, `--force_window`,
  `--gui_location`, `--fullscreen`, `--jupyter`): as flags existem e estão
  listadas em §12.4, mas ninguém as documentou em profundidade. Para fluxo
  interativo de verdade, `bin/manimgl` (skill `manimgl-3b1b`).
- **`manim init project|scene`**: gera esqueleto de projeto. Não usado aqui — a
  convenção deste repositório é `scenes/<assunto>.py` (`manim-project` §6.3).
- **`--custom_folders`**: descrito em §12.3 a partir do `default.cfg`, nunca
  exercitado nesta máquina.
