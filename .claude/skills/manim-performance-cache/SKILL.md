---
name: manim-performance-cache
description: >-
  Render RÁPIDO e REPRODUTÍVEL: os cinco caches do Manim (partial movie, LaTeX,
  texto Pango, SVG em memória, frame estático), a chave EXATA de cada um, o que
  invalida cada um, e o que de fato custa caro numa cena. Use quando pedirem "o
  render está lento", "por que a segunda vez demorou o mesmo tanto?", "o vídeo
  saiu com o número velho", "mudei o CSV e nada mudou na tela", "mudei o preço e
  o mp4 continua igual", "dá para reaproveitar o que já renderizei?", "o
  `media/` está com N gigas", "posso apagar `media/`?", "o que é
  `partial_movie_files`?", "o que é `uncached_00000.mp4`?", "apareceu 'Using
  cached data', está certo?", "quando eu uso `--no-cache`?", "essa cena tem
  objetos demais", "apareceu um aviso de 'a lot of sub-mobjects'", "o texto saiu
  com a quebra de linha errada depois que eu troquei a qualidade", "o LaTeX
  saiu vazio depois que eu dei Ctrl+C", "sobrou `.tex` sem `.svg` em
  `media/Tex`", "o `self.wait(3)` custa 180 frames?", "`always_redraw` é caro?",
  "como eu MEÇO isso em vez de chutar?". Cobre `disable_caching` ×
  `flush_cache` × `--seed` × `max_files_cached`, os três CRC32 de
  `get_hash_from_play_call`, os quatro buracos reais onde o hash NÃO enxerga o
  mundo de fora, o hash de texto que ignora a resolução, o cache de frame
  estático que a ordem de `self.add()` liga e desliga, e os comandos de medição
  (que quem roda é você, o usuário — a skill só os escreve). NÃO use para:
  escolher codec, NVENC, peso do arquivo e `mx bench` (skill
  `manim-gpu-encoding`, dona de tudo que é ENCODE); rodar N cenas em processos
  paralelos e a corrida de `media/Tex` entre workers (`manim-batch-pipeline`);
  disparar UM render e achar o arquivo de saída (`manim-render-api`); `t2c`,
  `TexTemplate`, pacote de LaTeX faltando e o palco fixo do texto nítido
  (`manim-text-latex`); traceback, `dvisvgm` ausente, ambiente quebrado
  (`manim-troubleshooting`); `run_time`/`rate_func`/`lag_ratio`
  (`manim-composicao-ritmo`); olhar o frame e julgar o desenho
  (`manim-verificacao-visual`); cortar a cena em partes para slide
  (`manim-presentation-parts`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cache e custo — por que o segundo render é rápido, e quando ele está errado

Duas perguntas, e só essas duas:

1. **O que o Manim reaproveita, com que chave, e o que faz ele parar de
   reaproveitar?**
2. **Onde vai o tempo de um render, e como eu MEÇO isso em vez de chutar?**

Tudo que é *encode* (codec, NVENC, bitrate, peso do mp4) é de
`manim-gpu-encoding`. Tudo que é *disparar o render e achar o arquivo* é de
`manim-render-api`. Aqui é o que acontece **entre** os dois: o que já estava
pronto, o que precisou ser feito de novo, e por quê.

> **Procedência.** Três marcas, e valem para o arquivo inteiro.
>
> - **[FONTE]** — lido no código instalado nesta máquina: ManimCE **0.21.0** em
>   `.venv/lib/python3.12/site-packages/manim/` (CPython 3.12.3, `pyvenv.cfg`
>   aponta `home = /usr/bin`), mais `manimx/` e `manim.cfg` deste repositório.
>   Vem com arquivo e linha. É afirmação forte.
> - **[DISCO]** — contado em `media/` deste repositório em **2026-08-19**, com
>   `ls`/`find`/`du`. É um fato desta máquina, não uma lei do Manim.
> - **[INFERIDO]** — dedução minha a partir do fonte, **não executada**.
>
> **Nesta sessão nada foi renderizado.** Nenhum `mx render`, `manim`, `ffmpeg`,
> `ffprobe`, `mx bench`. Todos os comandos de medição da §9 estão escritos para
> **você** rodar; eu não rodei nenhum. O que ficou por conferir está listado na
> §13.

---

## 1. Cartão de referência — os cinco caches, numa tela

O Manim chama de "cache" só o primeiro. Os outros quatro existem, mordem, e não
têm flag.

| # | Cache | Onde vive | Chave exata | Invalidado por | Podado por | Vida |
|---|---|---|---|---|---|---|
| 1 | **partial movie** | `media/videos/<mod>/<qual>/partial_movie_files/<Cena>/<hash>.mp4` | `crc32(camera)_crc32(anims)_crc32(mobjects)` | qualquer atributo serializável da câmera, das animações ou dos mobjects em cena | `max_files_cached` (LRU por `atime`), `--flush_cache` | disco |
| 2 | **LaTeX / Typst** | `media/Tex/<sha256[:16]>.svg` (+ `.tex`/`.typ`) | sha256 do **fonte `.tex` inteiro**, preâmbulo incluído | mudar a expressão, o `tex_environment` ou o `TexTemplate` | **ninguém** | disco, para sempre |
| 3 | **texto Pango** | `media/texts/<sha256[:16]>.svg` | sha256 de `texto+fonte+slant+weight+cor+t2*+line_spacing+font_size+ligatures+gradient` | qualquer um desses | **ninguém** | disco, para sempre |
| 4 | **SVG → mobject** | `SVG_HASH_TO_MOB_MAP`, dict de módulo | `hash((classe, svg_default, path_string_config, file_name, renderer))` | trocar o **caminho**; **não** o conteúdo do arquivo | GC do processo | processo |
| 5 | **frame estático** | `CairoRenderer.static_image`, um `ndarray` | recomputado a cada `play` | qualquer coisa que mova ou tenha updater | — | uma animação |

**A regra de ouro, e ela resolve 80% dos casos:** o cache #1 é **por cena, por
qualidade e por conteúdo da chamada de `play`**; os caches #2 e #3 são
**globais, eternos e cegos à resolução**. Quando um número mudou na fonte e o
vídeo não mudou, o suspeito é o #1. Quando a *quebra de linha* ou a *tipografia*
mudou sozinha entre dois renders, o suspeito é o #3.

---

## 2. O cache de partial movies — o único que o Manim chama de "cache"

### 2.1 A unidade é a chamada de `play`, não a cena

Cada `self.play(...)` — e cada `self.wait(...)`, que é `self.play(Wait(...))`
(`scene/scene.py:1222-1252`) — vira **um mp4 próprio** no diretório de partials.
No fim, `combine_to_movie` concatena todos num só.

```
media/videos/exemplos/1080p60/partial_movie_files/OlaManim/     ← [DISCO], real
├── 4234509111_125152860_1286214886.mp4      ← um play, com hash
├── 4234509111_611562911_1546638049.mp4      ← outro play da MESMA cena
├── 4234509111_304666266_172856349.mp4
├── uncached_00000.mp4                        ← um play, com o cache desligado
└── partial_movie_file_list.txt               ← a lista para o concat
```

**[DISCO]** Repare que os três hashes começam com o mesmo `4234509111`: é o
CRC32 da **câmera**, idêntico nos três porque a resolução, o fps e a cor de
fundo não mudaram entre as animações. Só o segundo e o terceiro campo variam.
É a estrutura da §2.2 visível a olho nu — e o motivo de trocar o fundo
invalidar tudo de uma vez.

O template vem de `manim.cfg` deste repositório (e é igual ao default):
`partial_movie_dir = {video_dir}/partial_movie_files/{scene_name}`, com
`video_dir = {media_dir}/videos/{module_name}/{quality}` **[FONTE:
`_config/default.cfg:89,94`]**.

**Consequência que economiza uma pergunta inteira:** o caminho já separa por
arquivo de cena, por qualidade **e** por nome de cena. Iterar em `-q l` e
entregar em `-q h` **não reaproveita nada** — são dois diretórios. Isso é
correto e é de propósito; não tente "aproveitar" o preview.

**[DISCO]** Neste repositório existem hoje **8** diretórios de partials, com
**113 mp4** ao todo: **60** com nome de hash e **53** `uncached_*`. Os
`uncached_*` são a assinatura de renders feitos com `--no-cache`/`--disable_caching`.

### 2.2 A chave: três CRC32, e o que entra em cada um

**[FONTE: `utils/hashing.py:416-464`]**

```python
memoizer.mark_as_processed(scene_object)          # a SCENE não é serializada
camera_json              = _get_json(camera_object, memoizer)
animations_list_json     = [_get_json(a, memoizer, include_pixel_array=True)
                            for a in sorted(animations_list, key=str)]
current_mobjects_list_json = [_get_json(m, memoizer, include_pixel_array=True)
                              for m in current_mobjects_list]
hash_complete = f"{crc32(camera)}_{crc32(anims)}_{crc32(mobs)}"
```

Assinatura conferida no índice:

```
get_hash_from_play_call(scene_object: Scene,
                        camera_object: Camera | OpenGLCamera,
                        animations_list: Iterable[Animation],
                        current_mobjects_list: Iterable[Mobject]) -> str
get_json(obj: Any, *, include_pixel_array: bool = False) -> str
hash_obj(obj: object) -> int
```

Quatro detalhes que decidem o comportamento:

1. **A `Scene` é marcada como processada ANTES de tudo.** Estado guardado em
   `self.qualquer_coisa` dentro da cena é **invisível** ao hash — e qualquer
   referência de volta à cena vira o placeholder `"AP"`.
2. **A câmera carrega a resolução.** `Camera.__init__` grava `pixel_width`,
   `pixel_height`, `frame_width`, `frame_height`, `frame_rate`,
   `_background_color`, `_background_opacity` no `__dict__`
   (`camera/camera.py:100-142`). Logo: mudar `-q`, `--fps`, `-r` ou a cor de
   fundo **invalida TODOS os partials daquela cena**. Trocar o tema é um render
   frio inteiro — não é bug, é o hash fazendo o certo.
3. **A lista de mobjects é a `scene.mobjects` INTEIRA**, não só a que anima. Uma
   cena que acumula 300 mobjects paga a serialização dos 300 em **cada** `play`.
4. **`sorted(animations_list, key=str)`** — a ordem em que você passa as
   animações ao `play` não muda o hash. A ordem em que os mobjects entraram na
   cena, muda.

### 2.3 O que o hash ENXERGA — a lista honesta

`_CustomEncoder.default` (`utils/hashing.py:243-302`) resolve, nesta ordem:

| Tipo do objeto | Vira | Nota |
|---|---|---|
| função / método / lambda | `{"code": inspect.getsource(obj), "nonlocals": {globals+nonlocals}}` | **o texto do fonte**, não o comportamento |
| `np.ndarray` puro, dtype numérico | `NDARRAY:<descritor>:<shape>:<sha256 do buffer>` (`:71-89`) | conteúdo INTEIRO, sem truncar |
| subclasse de ndarray, ou dtype com objeto | `repr`, e se `size > 1000` vira `np.resize(obj,(100,100))` + `"TRUNCATED ARRAY"` (`:286-290`) | **aqui sim há truncamento** |
| qualquer objeto com `__dict__` | o `__dict__`, recursivamente | é o caso de 99% dos mobjects |
| `np.uint8` | `int` | |
| **qualquer outra coisa** | `str(type(obj))` (`:302`) | **só o nome do tipo** |

E `KEYS_TO_FILTER_OUT` (`:30-35`) descarta, em todo dicionário:
`original_id`, `background`, `pixel_array`, `pixel_array_to_cairo_context` — mas
`pixel_array` volta a entrar para animações e mobjects, porque eles são
serializados com `include_pixel_array=True`. Ou seja: **o `pixel_array` de um
`ImageMobject` é hasheado por inteiro, com sha256, a cada `play`.** Uma imagem
4K em cena custa ~33 MB de sha256 por chamada de `play`. **[INFERIDO]** — o
mecanismo está lido; o custo em segundos não foi medido (§9.3 mede).

### 2.4 Os quatro buracos onde o hash NÃO enxerga o mundo de fora

`manim-project` §10.7 e `manim-render-api` §8 dão a regra prática — *"cena com
dado externo precisa de `--no-cache`"* — e ela está certa. Esta skill deve o
**mecanismo**, porque a regra crua confunde: na maior parte dos casos o dado
externo **é** visto, e o cache erra por outro motivo.

Se o CSV muda `9,51` para `9,48`, o `Text("9,48")` tem outro `text` e outros
`points`; o `__dict__` muda, o CRC32 muda, o cache **erra e refaz**. Correto.
Os buracos reais são estes quatro:

**(a) O dado só existe num objeto sem `__dict__`.** `set`, `frozenset`,
`pathlib.Path` (tem `__slots__`), `datetime.date`, `Decimal`, qualquer classe
com `__slots__`. Todos caem no `str(type(obj))` da linha 302 — **o valor some,
sobra o nome do tipo**.

**Correção:** `functools.partial` estava nesta lista e **não pertence a ela** —
ele TEM `__dict__`. Medido:

```console
$ python3 -c "from functools import partial; p=partial(print,1); print(hasattr(p,'__dict__'), p.__dict__)"
True {}
```

Ele cai no ramo `elif hasattr(obj, "__dict__")` (`utils/hashing.py:293`) e
serializa como `{}` — vazio, porque `func`, `args` e `keywords` são slots do C,
não entradas de `__dict__`. **A conclusão sobrevive** (dois `partial` com
argumentos diferentes serializam igual, e o cache não os distingue), mas por
outro caminho: não é o fallback de tipo, é um `__dict__` vazio.

**(b) O dado só afeta um arquivo cujo próprio cache é cego a conteúdo.** Trocar
o `.svg` do logo, a fonte instalada, ou a imagem de fundo (`Camera(background_image=…)`)
mantém o **caminho** igual. O cache #4 é chaveado pelo caminho (§6) e o hash da
câmera guarda a string do caminho. O partial velho continua válido para o Manim
e errado para você.

**(c) `inspect.getsource` falhou.** No REPL, em `exec`, em doctest ou em célula
de Jupyter, o fonte de um lambda pode não ser recuperável; o encoder grava
`code = ""` (`:280-284`) — com um comentário do próprio ManimCE dizendo que isso
**causa colisão de hash** e apontando o PR 402. Duas funções diferentes viram a
mesma string. É o único caminho conhecido para um **acerto falso** do cache #1.

**(d) O dado é aleatório ou depende do relógio.** Aqui não há acerto falso: há
**erro permanente**. Toda execução gera um hash novo, o cache nunca acerta, e o
diretório enche de partials que ninguém vai reusar. A correção não é
`--no-cache`; é **`--seed N`** (§3).

### 2.5 O que acontece num acerto

`CairoRenderer.play` (`renderer/cairo_renderer.py:62-120`):

```python
if config["disable_caching"]:
    hash_current_animation = f"uncached_{self.num_plays:05}"
else:
    hash_current_animation = get_hash_from_play_call(...)
    if self.file_writer.is_already_cached(hash_current_animation):
        logger.info(f"Animation {self.num_plays} : Using cached data (hash : ...)")
        self.skip_animations = True
        self.time += scene.duration
```

Repare no que **não** é pulado: `scene.compile_animation_data(...)` já rodou, o
hash foi calculado (com o custo da §2.3), `begin_animations()` e
`save_static_frame_data` rodam, e a animação é executada com `skip_animations`
— ou seja, ela **vai até o estado final sem escrever frame**. O que se economiza
é a **rasterização e o encode**, que é a maior parte, mas não é tudo.

E a junção final é barata: `combine_files` faz **stream copy** — abre os partials
com o demuxer `concat` e remuxa pacotes via `add_stream_from_template`, sem
reencodar (`scene_file_writer.py:911-927`). **Exceção:** `--format gif`
**decodifica e reencoda tudo** através do grafo `split → palettegen → paletteuse`
(`:857-909`). Num GIF, o cache economiza a rasterização e nada do encode final.

### 2.6 Onde os partials nunca nascem

`add_partial_movie_file` e `is_already_cached` começam com
`if not hasattr(self, "partial_movie_directory") or not write_to_movie(): return`
(`:374`, `:815`). E `write_to_movie()` (`utils/file_ops.py:110-129`) é **False**
quando:

| Situação | Efeito no cache |
|---|---|
| `--format png` | `is_png_format()` tem precedência: nada é lido nem escrito |
| `-s` / `--save_last_frame` | o setter zera `write_to_movie` (`_config/utils.py:807-808`) |
| `--dry_run` | zera `write_to_movie` **e** `save_last_frame` (`:1374-1376`) |
| `--renderer=opengl` sem `--write_to_movie` | zerado na leitura da CLI (`:855-857`) |

Duas consequências práticas:

- **Um preview em PNG não aquece o cache** e não se beneficia dele. Se o seu
  ciclo é "olha o frame → conserta → olha de novo", cada olhada paga o desenho
  inteiro. É o preço certo a pagar; só não espere que a terceira seja rápida.
- **`--dry_run` continua calculando o hash** (o `if` do `disable_caching` roda
  antes de qualquer checagem de `write_to_movie`) e continua rasterizando cada
  frame — ele só não escreve nada. É por isso que ele é o cronômetro certo para
  "quanto custa DESENHAR esta cena" (§9.4).

### 2.7 Poda: `max_files_cached`, `atime` e `flush`

`SceneFileWriter.finish()` (`:615-630`), no fim de todo render que escreve vídeo:

```python
self.join_all_encode_jobs()
self.combine_to_movie()
if config.save_sections: self.combine_to_section_videos()
if config["flush_cache"]: self.flush_cache_directory()
else:                     self.clean_cache()
```

- `clean_cache()` (`:1056-1076`) conta os arquivos **daquele diretório de cena**,
  e se passarem de `max_files_cached` apaga os mais antigos **por `st_atime`**.
- Quem atualiza o `atime` é `combine_to_movie`, que chama `modify_atime(file_path)`
  em cada partial que entrou no vídeo final (`:1036-1038`). Ou seja: a política é
  **LRU de verdade** — o partial usado na última junção fica; o de uma versão
  antiga da cena envelhece e cai.
- `max_files_cached` aceita `-1` para infinito (`_set_pos_number(..., allow_inf=True)`,
  `_config/utils.py:508-517`). O default da biblioteca é **100**; o `manim.cfg`
  deste repositório sobe para **200** — e isso só vale rodando da raiz
  (`manim-project` §5).
- **Um detalhe do fonte que explica um "200 que são 199":** os dois métodos
  filtram com `if file_name != "partial_movie_file_list.txt"`, mas `iterdir()`
  devolve `Path`, e `Path != str` é sempre verdadeiro — o filtro nunca exclui
  nada, e o `.txt` conta e é apagado junto. Inofensivo (ele é reescrito a cada
  junção). Já registrado em `manim-render-api` §8; repito aqui porque é aqui que
  alguém vai contar arquivos. **[FONTE + INFERIDO na consequência]**

### 2.8 O partial truncado — o que esta versão conserta

Um encode que morre no meio deixa um mp4 **estruturalmente válido e truncado**.
Se ele ficar no disco com o nome do hash, o próximo render acerta o cache e
monta um vídeo com um pedaço faltando — sem erro nenhum. Nesta 0.21 há duas
defesas explícitas **[FONTE]**:

- `_PartialMovieEncodeJob.join()` (`:176-190`) apaga o arquivo quando o worker levanta;
- `abort_encode_jobs()` (`:734-770`) sela o job corrente e apaga o parcial
  **incondicionalmente** — o docstring diz por quê: *"an aborted partial is
  structurally valid but truncated, so leaving it behind produces an erroneous
  cache hit on a later run"*.

**O que isso NÃO cobre:** `kill -9`, falta de energia, disco cheio. Se você
matou o processo com força e o render seguinte saiu com um trecho estranho,
apague o diretório da cena (§10.5) antes de investigar qualquer outra coisa.

---

## 3. As três alavancas: `disable_caching`, `flush_cache`, `--seed`

| Alavanca | `bin/mx render` | `bin/manim` | API `manimx` | `manim.cfg` | O que faz |
|---|---|---|---|---|---|
| não reusar | `--no-cache` | `--disable_caching` | `disable_caching=True` | `disable_caching` | os partials passam a se chamar `uncached_00000.mp4`; não lê e sobrescreve |
| apagar tudo no fim | **✗** | `--flush_cache` | `flush_cache=True` | `flush_cache` | `flush_cache_directory()` no lugar do `clean_cache()` |
| determinismo | **✗** | `--seed N` | via `config_overrides` | — | `random.seed()` + `np.random.seed()` |
| tamanho do LRU | **✗** | **✗** | `config_overrides={"max_files_cached": N}` | `max_files_cached` | quantos partials sobrevivem por cena |
| calar o aviso | **✗** | **✗** | via `config_overrides` | `disable_caching_warning` | some o aviso de "a lot of sub-mobjects" (§8.4) |

**[FONTE]** `manimx/cli.py:473` expõe só `--no-cache`, mapeado em
`cmd_render` para `disable_caching=args.no_cache` (`cli.py:217`). As demais
existem em `render_scene(..., disable_caching=False, flush_cache=False, ...)`
(`manimx/render.py:279-280`) e em `bin/manim`
(`cli/render/global_options.py:72,78,148`).

### 3.1 Quando desligar o cache — e quando NÃO

**Desligue** quando o desenho depende de algo que a §2.4 lista como invisível:
arquivo de asset que você acabou de trocar mantendo o nome, fonte reinstalada,
imagem de fundo por caminho, ou lambda escrito no REPL.

**Não desligue** por medo genérico de "dado externo". Se o dado vira texto,
número, posição ou cor de um mobject, o hash o enxerga. Desligar sem motivo
custa **o render inteiro, toda vez** — é a forma mais cara de resolver um
problema que você não tem.

**Nunca desligue como forma de "limpar"**: `--no-cache` não apaga nada, só
escreve por cima dos `uncached_*`. Quem limpa é `--flush_cache` (por cena) ou
`rm -rf` (§10.5).

### 3.2 `--seed` é quase sempre melhor que `--no-cache`

Para cena com `random`/`np.random`, `--no-cache` trata o sintoma e mata o cache
para sempre. `--seed 42` torna a cena determinística: o hash volta a ser estável
e o cache volta a funcionar. Existe também `Scene(random_seed=…)`
(`scene/scene.py:180, 222-224`), que fixa a semente por cena em vez de por
invocação — melhor ainda, porque viaja junto com o código.

---

## 4. O cache de LaTeX e o de Typst — `media/Tex`

### 4.1 A chave é o fonte `.tex` inteiro

**[FONTE: `utils/tex_file_writing.py:27-73, 100-115`]**

```python
def tex_hash(expression: Any) -> str:
    return hashlib.sha256(str(expression).encode()).hexdigest()[:16]
```

O que entra em `expression` **não é a sua string** — é a saída de
`tex_template.get_texcode_for_expression_in_env(expression, environment)`, ou
seja o **documento `.tex` completo**, com preâmbulo, `\documentclass` e
`\begin{align*}`. Consequências:

- trocar o `TexTemplate` (ou acrescentar um `\usepackage`) invalida **tudo**;
- trocar `tex_environment` de `align*` para `center` gera outro arquivo;
- a **cor** não entra: `SingleStringMathTex` compila em preto e colore depois.
  `MathTex("x", color=RED)` e `MathTex("x", color=BLUE)` compartilham o `.svg`.

O fluxo é `generate_tex_file` (escreve o `.tex` se faltar) → `if svg_file.exists():
return svg_file` → `compile_tex` → `convert_to_svg` → `delete_nonsvg_files`.
**O `.svg` existente curto-circuita tudo**, inclusive a checagem do compilador —
é por isso que o check de LaTeX do `mx doctor` passa em cache (`manim-project` §4.3).

Typst é o mesmo desenho: `_typst_hash(full_source)` = sha256[:16] do documento
montado, mesmo diretório `tex_dir`, mesmo `if svg_file.exists(): return`
(`utils/typst_file_writing.py:30-33, 78-106`). Assinatura conferida:
`typst_to_svg_file(typst_code, preamble='', text_size=10, font_paths=None)`.
**Armadilha [INFERIDO]:** `font_paths` **não entra no hash** — trocar a fonte de
um `Typst` mantendo o código não recompila.

### 4.2 Ninguém poda `media/Tex`

`max_files_cached` só olha o diretório de partials. `media/Tex` cresce para
sempre. `delete_nonsvg_files` (`:269-283`) apaga tudo que **não** for `.svg`
nem `.tex` — ela limpa `.dvi`/`.log`/`.aux`, não o cache.

**[DISCO]** aqui: `media/Tex` tem **88 arquivos / 368 KiB** (42 `.svg` + 46
`.tex`) e `media/texts` **42 `.svg` / 256 KiB**. É pequeno; num projeto com
muita fórmula, não é.

### 4.3 `.tex` sem `.svg` é a impressão digital de uma compilação que morreu

`generate_tex_file` grava o `.tex` **antes** de compilar. Se o LaTeX ou o
`dvisvgm` falhar, o `.tex` fica e o `.svg` não nasce. Ele é inofensivo (o
próximo render tenta de novo), mas é forense grátis:

```bash
comm -23 <(ls media/Tex/*.tex | xargs -n1 basename | sed 's/\.tex$//' | sort) \
         <(ls media/Tex/*.svg | xargs -n1 basename | sed 's/\.svg$//' | sort)
```

**[DISCO]** neste repositório devolve **4 órfãos**, e dois deles são
`a^2 + b^2 = c^2` e `x = 0.000` — expressões perfeitamente válidas. A causa mais
provável é a ausência do symlink de `dvisvgm` (`manim-project` §3.1), não erro
de LaTeX. **[INFERIDO]** na causa; o fato é medido.

### 4.4 O único cache que envenena de verdade: o `.svg` truncado

`convert_to_svg` (`:226-265`) chama

```python
subprocess.run(["dvisvgm", ..., f"--output={result.as_posix()}", ...],
               stdout=subprocess.DEVNULL)
```

— **sem `check=True`, e escrevendo direto no caminho final**. Não é atômico. Um
`dvisvgm` interrompido no meio deixa um `.svg` parcial; a partir daí,
`tex_to_svg_file` devolve esse arquivo **para sempre**, e o `SVGMobject` ou
levanta `ET.ParseError` ou monta um mobject com metade dos glifos.

**Sintoma:** uma fórmula que era certa passou a aparecer cortada, vazia, ou a
quebrar com erro de XML — e mexer no código não adianta, porque o hash não mudou.
**Correção:** apague o par:

```bash
grep -l 'a\^2 + b\^2' media/Tex/*.tex          # ache o hash pelo conteúdo
rm media/Tex/<hash>.svg media/Tex/<hash>.tex   # e recompile
```

**[FONTE]** no mecanismo; **[INFERIDO]** no sintoma (não reproduzido aqui).

### 4.5 `delete_nonsvg_files` é uma varredura GLOBAL

Ela itera `tex_dir` inteiro e apaga tudo fora do whitelist — inclusive os
`.dvi` **de outro processo** compilando ao mesmo tempo. Em render paralelo isso
é uma corrida real; quem trata é `manim-batch-pipeline` (isolamento de
`tex_dir`/`text_dir` por worker em `media/_workers/wN/`). Não reimplemente aqui.

---

## 5. O cache de texto — e a resolução que não entra na chave

### 5.1 A chave exata, e por que só o `Text` tem o defeito

**[FONTE: `mobject/text/text_mobject.py:689-701` e `:834-866`]**

```python
def _text2hash(self, color):                       # class Text
    settings  = "PANGO" + self.font + self.slant + self.weight + str(color)
    settings += str(self.t2f) + str(self.t2s) + str(self.t2w) + str(self.t2c)
    settings += str(self.line_spacing) + str(self._font_size)
    settings += str(self.disable_ligatures) + str(self.gradient)
    id_str = self.text + settings                  # ← pixel_width NÃO entra
```

```python
def _text2svg(self, color):
    ...
    if file_name.exists():
        svg_file = str(file_name.resolve())        # ← curto-circuito ANTES de ler a config
    else:
        width  = config["pixel_width"]             # ← largura de QUEBRA DE LINHA
        height = config["pixel_height"]
        svg_file = manimpango.text2svg(settings, size, line_spacing,
                                       self.disable_ligatures,
                                       str(file_name.resolve()),
                                       START_X, START_Y, width, height, self.text)
```

O `config["pixel_width"]` é passado ao Pango como **largura de quebra**, e não
está no hash. Um render em `-q m` (1280) e um em `-q h` (1920) podem quebrar a
mesma frase em lugares diferentes, e o segundo reaproveita o SVG do primeiro.
É a lição registrada em `manim-project` §10.6; aqui vai a metade que faltava:

**`MarkupText` NÃO tem esse defeito.** O `_text2svg` dele (`:1380-1417`) passa
`600`, `400` e `pango_width=500` **fixos**, sem tocar na config. A quebra de
linha de um `MarkupText` é a mesma em qualquer qualidade. **[FONTE]** — e é uma
razão legítima para preferir `MarkupText` quando o texto tem mais de uma linha e
o projeto renderiza em qualidades diferentes.

Diferença menor mas real: `Text._text2hash` usa `str(color)`, `MarkupText`
usa `ManimColor(color).to_hex().lower()` (`:1363-1378`). E o prefixo do hash
difere (`"PANGO"` × `"MARKUPPANGO"`), então os dois nunca colidem entre si.

### 5.2 `use_svg_cache` desliga o cache errado

`Text.__init__` tem **`use_svg_cache: bool = False`** e `SVGMobject.__init__`
tem **`use_svg_cache: bool = True`** (assinaturas conferidas no índice). Essa
flag governa **apenas** o cache #4, em memória. O cache #3, em disco, é
**incondicional** — não existe flag que o desligue. Para forçar um texto a ser
regerado, apague o `.svg` de `media/texts` (ou o diretório inteiro; ele se
reconstrói).

### 5.3 A correção estrutural

Se o projeto fixa `config.pixel_width/height` durante a construção do texto — que
é o que o palco fixo do "texto nítido" faz, pelo motivo do arredondamento de
glifo do cairo — o defeito desta seção **desaparece de brinde**: com a largura
de quebra constante, o hash cego à resolução passa a ser inofensivo, e a mesma
frase em dois tamanhos passa a compartilhar um SVG só (porque o `font_size`
gravado é sempre o mesmo). O mecanismo do arredondamento é de
`manim-text-latex`; a disciplina de projeto é de `manim-tema-projeto`. Aqui
fica só o efeito colateral no cache. **[INFERIDO]** — dedução direta das duas
funções acima, não medida.

---

## 6. Os caches em memória: `SVG_HASH_TO_MOB_MAP` e o contexto cairo

**[FONTE: `mobject/svg/svg_mobject.py:29, 161-195`]**

```python
SVG_HASH_TO_MOB_MAP: dict[int, SVGMobject] = {}

@property
def hash_seed(self) -> tuple:
    return (self.__class__.__name__, self.svg_default,
            self.path_string_config, self.file_name, config.renderer)
```

e a chave é `hash_obj(self.hash_seed)` — `hash_obj(obj: object) -> int`
(`utils/iterables.py:469-480`) desce recursivamente em dict/set/tuple/list para
conseguir hashear o `svg_default` mutável.

**A armadilha, e ela é do tamanho de um dia de trabalho:** a chave tem o
**`file_name`**, não o conteúdo do arquivo. Dentro de um mesmo processo — um
script que constrói cenas em laço, um notebook, o `render_many` — editar o
`.svg` no disco **não** invalida nada: a segunda `SVGMobject("logo.svg")` vem do
dicionário, com os pontos antigos. Entre processos o problema some, porque o
dict morre junto. Para forçar: `SVGMobject("logo.svg", use_svg_cache=False)`.

Quem se beneficia disso sem risco é `Tex`/`MathTex`: `SingleStringMathTex` não
passa `use_svg_cache` (fica no `True` do `SVGMobject`), mas o `file_name` dele já
é **derivado do conteúdo** (`media/Tex/<sha256>.svg`), então caminho igual
significa conteúdo igual. É o desenho certo.

O quinto cache pequeno é `Camera.pixel_array_to_cairo_context`
(`camera/camera.py:150`, `591-633`), um dict `id(pixel_array) → cairo.Context`
que evita recriar o contexto a cada frame. Você não mexe nele; ele aparece aqui
só porque está na lista `KEYS_TO_FILTER_OUT` do hash (§2.3) — sem isso, o hash
de todo `play` mudaria a cada execução por causa de um `id()`.

---

## 7. O frame estático — o cache que ninguém sabe que existe

Este não tem nome, não tem flag, e é o que mais muda o tempo de uma cena grande.

Antes de cada animação, `CairoRenderer.play` chama
`self.save_static_frame_data(scene, scene.static_mobjects)`
(`renderer/cairo_renderer.py:110, 218-243`): os mobjects que **não** vão se mexer
são rasterizados **uma vez**, viram um `ndarray`, e a cada frame o Manim começa
desse bitmap em vez de redesenhar tudo (`:153-154`).

Quem decide o que é estático é `Scene.get_moving_and_static_mobjects`
(`scene/scene.py:948-966`), e o coração é `get_moving_mobjects`
(`:899-946`):

```python
mobjects = self.get_mobject_family_members()
for i, mob in enumerate(mobjects):
    update_possibilities = [
        mob in animation_mobjects,             # participa da animação
        len(mob.get_family_updaters()) > 0,    # tem QUALQUER updater
        mob in self.foreground_mobjects,       # está em primeiro plano
    ]
    if any(update_possibilities):
        return mobjects[i:]                    # ← daqui para FRENTE, tudo é "móvel"
return []
```

**Leia de novo a última linha.** Não é "os que se mexem"; é **"do primeiro que se
mexe em diante"**. A lista está em ordem de desenho (z-order). Portanto:

| Se você… | Efeito |
|---|---|
| adiciona o mobject que vai animar **por último** | tudo antes dele fica estático → um bitmap + um objeto por frame |
| adiciona o que vai animar **primeiro**, e depois 40 rótulos | os 40 rótulos entram em "móvel" e são redesenhados em **todo** frame |
| põe um `always_redraw` no fundo da cena | a cena inteira vira móvel, para sempre |
| chama `add_foreground_mobject(x)` | `x` e tudo depois dele viram móveis |

Isto é **grátis de arrumar** e não muda um pixel da imagem: é ordem de
`self.add`. Em cena de aula, com fundo fixo e um elemento animando, a diferença
é entre redesenhar 3 objetos por frame e redesenhar 300.

### 7.1 O `wait` congelado — e a regra do updater com `dt`

`Scene.wait(duration=1.0, stop_condition=None, frozen_frame=None)` vira
`self.play(Wait(...))`. Se a espera é **estática**, o renderer desenha **um**
frame e o escreve N vezes:

```python
def freeze_current_frame(self, duration: float) -> None:      # cairo_renderer.py:197-209
    dt = 1 / self.camera.frame_rate
    self.add_frame(self.get_frame(), num_frames=int(duration / dt))
```

Um `self.wait(3)` a 60 fps custa **1 rasterização + 180 encodes**, não 180
rasterizações. E como é um `play` como outro qualquer, ele tem partial e hash
próprios — waits acertam o cache com facilidade.

Quando ele deixa de ser estático (`Scene.should_update_mobjects`,
`scene/scene.py:419-446`):

```python
should_update = (self.always_update_mobjects
                 or self.updaters                        # updaters DA CENA
                 or wait_animation.stop_condition is not None
                 or any(mob.has_time_based_updater()
                        for mob in self.get_mobject_family_members()))
```

**Repare na assimetria, porque ela é contraintuitiva e está no fonte:**

| Mecanismo | O que conta |
|---|---|
| frame estático (§7) | `get_family_updaters()` — **qualquer** updater |
| wait congelado (§7.1) | `has_time_based_updater()` — **só** os que recebem `dt` |

Ou seja: um `mob.add_updater(lambda m: m.next_to(outro, UP))` mata o cache de
frame estático mas **não** desmonta o `wait` congelado; um
`mob.add_updater(lambda m, dt: ...)` mata os dois. Se um `self.wait(3)` da sua
cena passou de instantâneo a 180 frames desenhados, procure o `dt`.

---

## 8. O que custa caro — o orçamento de uma cena

Sem medição não há ordem; o que segue é **o mecanismo**, com o instrumento de
medida ao lado (§9). Nenhum número de segundos aqui é meu.

### 8.1 Rasterizar: o custo é curva, não objeto

O cairo desenha cada `VMobject` como um caminho de béziers cúbicas. A régua é
`get_num_curves()` somado sobre `family_members_with_points()`, não o número de
`VGroup`s. Um `Text` de 30 caracteres é ~30 submobjects com dezenas de curvas
cada; um `NumberPlane` denso pode ter centenas de linhas. Métodos relevantes,
todos conferidos no índice:

```
VMobject.get_num_curves(self) -> int
VMobject.insert_n_curves(self, n: int) -> Self
VMobject.pointwise_become_partial(self, vmobject: VMobject, a: float, b: float) -> Self
Mobject.family_members_with_points(self) -> list[Mobject]
Mobject.get_family(self, recurse: bool = True) -> list[Mobject]
```

`insert_n_curves` é o que o `Transform` chama para casar dois mobjects de
tamanhos diferentes: transformar um `Circle` (4 curvas) num `Text` de 200 curvas
**engorda o círculo até 200** e desenha 200 curvas por frame durante toda a
animação. Transformar coisas de complexidade parecida é mais barato **e** fica
melhor.

### 8.2 Hashear: o custo cresce com a cena, não com a animação

O hash serializa **`scene.mobjects` inteira** a cada `play` (§2.2). Uma cena que
só acumula paga cada vez mais caro por animação cada vez menor. Duas
consequências:

- `self.remove(...)` / `self.clear()` do que já saiu de cena não é higiene, é
  desempenho;
- **`--no-cache` corta esse custo por inteiro**: com `disable_caching` o
  `get_hash_from_play_call` nem chega a ser chamado — o `if` da linha 80 de
  `cairo_renderer.py` desvia antes. Em cena com dezenas de milhares de
  submobjects, `--no-cache` pode sair **mais rápido** que o cache, mesmo
  refazendo tudo. É o único caso em que desligar o cache é uma otimização, e não
  uma renúncia. Meça com §9.3 antes de acreditar.

### 8.3 `always_redraw` e updaters

`always_redraw(func: Callable[[], M]) -> M` (`animation/updaters/mobject_update_utils.py`)
constrói o mobject e pendura um updater que faz `become(func())` a cada frame:
reconstrução completa, do zero, 60 vezes por segundo. Além do custo direto, ele
liga os dois gatilhos da §7. Quando o que muda é só uma posição ou um número,
um updater cirúrgico (`m.next_to(...)`, `DecimalNumber` com
`ValueTracker`) é ordens de grandeza mais barato. Assunto é de
`manim-updaters-valuetracker`; a conta de custo é daqui.

### 8.4 O aviso de "muitos submobjects"

`_Memoizer.THRESHOLD_WARNING = 170_000` (`utils/hashing.py:105`). Quando a
serialização de **um** `play` passa de 170 mil objetos distintos, o Manim
avisa uma vez:

> *It looks like the scene contains a lot of sub-mobjects. Caching is sometimes
> not suited to handle such large scenes, you might consider disabling caching
> with --disable_caching…*

Não é erro. É o único sinal automático de que você cruzou a fronteira em que o
hash custa mais que a rasterização. Ele sai por `logger.warning` e é silenciado
por `disable_caching_warning = True` no `manim.cfg` — silencie só depois de ter
medido, não antes.

### 8.5 Imagem grande

Um `ImageMobject` é serializado **com o `pixel_array`** (§2.3). O custo do hash
passa a incluir um sha256 sobre a imagem inteira, em cada `play`, enquanto ela
estiver em cena. Redimensionar o PNG para o tamanho em que ele aparece na tela
resolve tanto isso quanto a memória. **[INFERIDO]** — mecanismo lido, custo não
medido.

---

## 9. MEDIR, em vez de adivinhar

**Quem roda isto é você.** Os comandos abaixo estão escritos, conferidos contra
as flags que existem, e **não foram executados** nesta sessão. Todos usam os
wrappers de `bin/` — `.venv/bin/manim` direto perde LaTeX e GPU
(`manim-project` §3).

### 9.1 O que já existe no disco

```bash
du -sh media/videos media/Tex media/texts
find media -path '*partial_movie_files*' -name '*.mp4' | wc -l
find media -path '*partial_movie_files*' -name 'uncached_*.mp4' | wc -l   # renders com --no-cache
find media -name partial_movie_files -type d -exec sh -c \
  'echo "$(find "$1" -name "*.mp4" | wc -l)  $1"' _ {} \; | sort -rn | head
```

### 9.2 Quantos acertos o render teve

A mensagem é `logger.info` (`cairo_renderer.py:92-95`), então basta a
verbosidade padrão:

```bash
bin/mx render scenes/aula.py Cena -q h --verbosity INFO 2>&1 \
  | tee /tmp/render.log | grep -c 'Using cached data'
grep -c 'Partial movie file written' /tmp/render.log     # os que foram refeitos
```

Acertos + escritos deve bater com o número de `play`+`wait` da cena. Se
acertos == 0 num segundo render idêntico, alguma coisa na §2.4 está mordendo.

### 9.3 Quanto custou o hash

`logger.debug("Hashing done in %(time)s s.")` (`utils/hashing.py:462`) — precisa
de DEBUG, e o `mx render` expõe `--verbosity`:

```bash
bin/mx render scenes/aula.py Cena -q l --verbosity DEBUG 2>&1 \
  | grep 'Hashing done' | sed -E 's/.*in ([0-9.]+).*/\1/' \
  | awk '{s+=$1; n++} END {printf "%d plays, %.2f s de hash, %.3f s por play\n", n, s, s/n}'
```

Compare com o tempo total. Se o hash for uma fração relevante, teste
`--no-cache` (§8.2) e compare de novo.

### 9.4 Quanto custa DESENHAR, sem encode nenhum

`--dry_run` rasteriza tudo e não escreve nada (`_config/utils.py:1374-1376`).
É a medida limpa do custo de desenho, sem NVENC no meio:

```bash
time bin/manim --dry_run -q h scenes/aula.py Cena           # desenho + hash
time bin/manim --dry_run --disable_caching -q h scenes/aula.py Cena   # só desenho
time bin/mx render scenes/aula.py Cena -q h --codec nvenc    # com encode
```

A diferença entre a primeira e a terceira é o encode — e aí o assunto vira
`manim-gpu-encoding`. `--dry_run` só existe no `bin/manim`.

### 9.5 O custo fixo de subir o Python

Todo render paga import de `manim`, `numpy`, `cairo`, `av`, `manimpango` antes
de desenhar um pixel. Num lote de cenas curtas, esse é o custo dominante — e é o
argumento para `render_many`/`--all` em vez de N processos:

```bash
.venv/bin/python -X importtime -c "import manim" 2>&1 | tail -15
```

**[DISCO]** `bin/` tem exatamente cinco entradas — `manim`, `manim-env.sh`,
`manimgl`, `mx`, `setup` — não há wrapper de `python`. Aqui chamar o
interpretador do venv direto é legítimo: a ressalva de `manim-project` §3 é
sobre LaTeX e PRIME offload, e um `import manim` não usa nenhum dos dois.

### 9.6 Contar curvas e submobjects SEM renderizar

Constrói mobjects e imprime; não abre renderer, não escreve arquivo, roda em
segundos:

```python
# /tmp/custo.py  →  .venv/bin/python /tmp/custo.py   (bin/ NÃO tem wrapper de python, §9.5)
from manim import *

def custo(nome, mob):
    fam = mob.family_members_with_points()
    curvas = sum(m.get_num_curves() for m in fam if hasattr(m, "get_num_curves"))
    pontos = sum(len(m.points) for m in fam)
    print(f"{nome:24} {len(mob.get_family()):5} na família  "
          f"{len(fam):5} com pontos  {curvas:6} curvas  {pontos:7} pontos")

custo("Circle()",            Circle())
custo("Square()",            Square())
custo("Text 30 caracteres",  Text("A pasta se multiplica. O repo", font_size=28))
custo("MathTex simples",     MathTex(r"a^2 + b^2 = c^2"))
custo("NumberPlane()",       NumberPlane())
```

Use isso antes de culpar a GPU: se o `NumberPlane` sozinho tem mais curvas que o
resto da cena somado, é ele.

### 9.7 Quanto pesa hashear um mobject

```python
# mede o TAMANHO da serialização, que é o que o crc32 vai percorrer
from manim import *
from manim.utils.hashing import get_json
for nome, mob in [("Circle", Circle()), ("Text(30)", Text("A pasta se multiplica. O repo")),
                  ("NumberPlane", NumberPlane())]:
    print(f"{nome:14} {len(get_json(mob, include_pixel_array=True)):>10} bytes de JSON")
```

`get_json(obj, *, include_pixel_array=False)` é a mesma função que o hash usa
(§2.2), com o mesmo `include_pixel_array=True` das listas de animação e de
mobjects. É a régua direta do custo da §8.2.

### 9.8 O experimento A/B honesto

Cache é medido comparando **duas execuções consecutivas idênticas**, com o
diretório de partials no estado certo:

```bash
S=scenes/aula.py; C=Cena
rm -rf media/videos/*/*/partial_movie_files/$C          # começa frio
time bin/mx render $S $C -q h --verbosity INFO          # 1ª: tudo escrito
time bin/mx render $S $C -q h --verbosity INFO          # 2ª: tudo acertado
time bin/mx render $S $C -q h --verbosity INFO --no-cache  # 3ª: nada reusado
```

A 2ª mede *hash + concat + import*; a 3ª mede *desenho + encode*. A diferença
entre 3ª e 1ª mede o custo do próprio hash. Rode cada uma **duas vezes** e fique
com a segunda: o primeiro `import manim` de um boot frio paga o page cache do
sistema de arquivos.

---

## 10. Receitas

### 10.1 Iterar rápido

```bash
bin/mx render scenes/aula.py Cena -q l                   # 480p15, diretório próprio
bin/mx render scenes/aula.py Cena -q l --format png      # só o último frame (não usa cache)
```

Use `-q l` e **não** mexa no cache. O diretório de `480p15` é separado do de
entrega, então o preview nunca contamina o final — mas também nunca acelera o
final. O ciclo de olhar o frame é de `manim-verificacao-visual`.

### 10.2 Render de entrega reprodutível

```bash
bin/manim -q h --seed 42 --flush_cache scenes/aula.py Cena
```

`--flush_cache` apaga os partials **no fim**, deixando o diretório limpo para a
próxima. Combine com `--seed` se a cena usa aleatoriedade. Se o pipeline é
automatizado, prefira `render_scene(..., flush_cache=True)`, porque o `mx render`
não expõe a flag.

### 10.3 Cena que depende de asset trocado com o mesmo nome

```bash
bin/mx render scenes/aula.py Cena -q h --no-cache
```

É o caso (b) da §2.4: você trocou `logo.svg`/a fonte/o PNG de fundo mantendo o
caminho. Alternativa mais barata e mais correta: **versione o nome do arquivo**
(`logo-v2.svg`) — aí o hash muda sozinho e você não perde o cache do resto.

### 10.4 CI limpo

```bash
bin/manim -q h --flush_cache --disable_caching scenes/aula.py Cena
```

Em CI o disco é novo a cada execução; o cache não tem o que reusar e só custa
hash. `--disable_caching` corta esse custo, `--flush_cache` garante que nada
sobra para o artefato. Paralelismo entre cenas é `manim-batch-pipeline`.

### 10.5 Limpar `media/` sem quebrar nada

Da mais segura para a mais radical:

```bash
find media -path '*partial_movie_files*' -name '*.mp4' -delete   # sempre seguro
rm -rf media/texts                                                # regerado do zero
rm -rf media/Tex                                                  # recompila o LaTeX (lento)
rm -rf media                                                      # tudo, inclusive os mp4 finais
```

**O que NUNCA está no cache e some junto:** `media/videos/<mod>/<qual>/<Cena>.mp4`
(o vídeo final), `media/images/<mod>/*.png` (os frames salvos) e
`media/videos/<mod>/<qual>/sections/` (as seções). Esses são **saída**, não
cache. Antes de `rm -rf media`, confira se o consumidor já copiou o que
precisava (no fluxo do deck de aulas, quem copia é o script de exportação —
`manim-batch-pipeline`).

**[DISCO]** aqui `media/` inteiro tem **26 MiB**, dos quais **25 MiB** são
`videos/` (14,5 MiB só de partials) — a proporção típica: o cache pesa mais que
a entrega.

---

## 11. Armadilhas, em uma tela

| Sintoma | Causa | Correção |
|---|---|---|
| mudei o preço/CSV e o vídeo saiu igual | dado invisível ao hash: §2.4 (a)/(b) | `--no-cache` neste render, e versione o nome do asset |
| a cena tem `random` e **nunca** acerta o cache | hash muda toda execução | `--seed N` ou `Scene(random_seed=…)`, não `--no-cache` |
| segundo render idêntico não acelerou nada | mudou `-q`/`--fps`/`-r`/cor de fundo → outro diretório **e** outro hash de câmera | é o certo; compare no mesmo `-q` |
| segundo render idêntico não acelerou, mesmo `-q` | `--format png`, `-s`, `--dry_run` ou opengl sem `--write_to_movie` → `write_to_movie()` False | use mp4 para exercitar o cache |
| `uncached_00000.mp4` no diretório | alguém rodou com `--no-cache` | inofensivo; some com `--flush_cache` |
| trecho faltando/estranho no vídeo montado | partial truncado por `kill -9`/disco cheio | `rm -rf` o diretório da cena e refaça (§2.8) |
| fórmula que era certa saiu vazia/cortada | `.svg` truncado em `media/Tex` por `dvisvgm` interrompido | apague o par `<hash>.svg`/`.tex` (§4.4) |
| `.tex` sem `.svg` sobrando | compilação que morreu antes do SVG | forense, não defeito (§4.3) |
| troquei a fonte e o texto não mudou | `media/texts/<hash>.svg` não vê a fonte instalada, só o **nome** dela | `rm -rf media/texts` |
| a quebra de linha mudou sozinha entre dois renders | hash de texto cego à resolução (§5.1) | palco fixo, ou `MarkupText`, ou `rm -rf media/texts` |
| editei o `.svg` e o mobject continua o antigo | `SVG_HASH_TO_MOB_MAP` é chaveado pelo caminho, e o processo é o mesmo | `use_svg_cache=False`, ou processo novo |
| aviso "a lot of sub-mobjects" | >170 000 objetos num `play` | meça (§9.3); talvez `--no-cache` seja **mais rápido** |
| cena grande ficou lenta e nada anima | frame estático desligado por updater ou ordem de `add` (§7) | anime por último; `clear_updaters()` no que parou |
| `self.wait(2)` custa 120 frames desenhados | algum mobject tem updater **com `dt`** (§7.1) | remova o `dt`, ou `frozen_frame=True` |
| `media/` cresceu para gigas | ninguém poda `Tex`/`texts`; partials só até `max_files_cached` **por cena** | §10.5 |
| apaguei `media/` e perdi o vídeo | `media/` guarda cache **e** entrega | copie a saída antes; §10.5 |
| `--no-cache` "não limpou" nada | ele não apaga, só escreve `uncached_*` por cima | `--flush_cache` ou `rm` |
| `mx render --flush_cache` não existe | o `mx` só expõe `--no-cache` | `bin/manim --flush_cache` ou a API |
| roda fora da raiz e o cache some | `manim.cfg` e `media_dir` vêm do **cwd** | rode da raiz (`manim-project` §5) |

---

## 12. Onde esta skill para

| A pergunta virou… | Skill |
|---|---|
| "qual codec", "está lento por causa da GPU", peso do mp4, NVENC, `mx bench` | **`manim-gpu-encoding`** — dona de tudo que é ENCODE |
| N cenas em processos paralelos, CI, a corrida de `media/Tex` entre workers | **`manim-batch-pipeline`** |
| disparar UM render, escolher qualidade/formato, achar o arquivo de saída | **`manim-render-api`** |
| `t2c`, `TexTemplate`, pacote de LaTeX faltando, o palco fixo do texto nítido | **`manim-text-latex`** |
| `dvisvgm` ausente, traceback, bissecção, ambiente quebrado | **`manim-troubleshooting`** |
| updater cirúrgico × `always_redraw`, `ValueTracker` | **`manim-updaters-valuetracker`** |
| `run_time`, `rate_func`, `lag_ratio`, o ritmo | **`manim-composicao-ritmo`** |
| olhar o frame e julgar se o desenho ficou certo | **`manim-verificacao-visual`** |
| cortar a cena em partes e medir a emenda | **`manim-presentation-parts`** |
| `next_section`, `--save_sections`, de qual `Scene` herdar | **`manim-cenas-secoes`** |
| o `tema.py` como contrato do projeto, dado de fonte única | **`manim-tema-projeto`** |
| achar o nome/assinatura de qualquer coisa | **`manim-api-discovery`** |
| o mapa do repositório e qual skill usar | **`manim-project`** |

**Fronteiras que já se confundiram, resolvidas aqui:**

- **`--no-cache` × cache de LaTeX.** `disable_caching` governa **só** os partial
  movies, e `--flush_cache` também. O `.tex` compilado em `media/Tex` não tem
  flag nenhuma: sai com `rm`, e só. Confundir os dois é o mal-entendido mais
  comum deste assunto.
- **"o render está lento" é ambíguo.** Se o gargalo é o `.mp4` sair grande e o
  encoder engasgar, é `manim-gpu-encoding`. Se é a cena demorar a **desenhar** ou
  o cache não acertar, é aqui. `--dry_run` (§9.4) é o desempate: ele tira o
  encode da conta.
- **Nomes.** Esta ressalva ficou obsoleta e foi fechada: as 27 skills existem no
  disco e a tabela de roteamento de `manim-project` §13 usa os nomes reais.
  Os nomes provisórios `manim-ritmo-e-secoes` e `manim-assets-externos` **nunca
  existiram** — o assunto do primeiro está repartido entre
  **`manim-composicao-ritmo`** (tempo) e **`manim-cenas-secoes`** (`next_section`);
  o do segundo é **`manim-svg-imagens`**.

**Buracos declarados** — se o pedido cair aqui, diga que não tem skill em vez de
improvisar: `ManimConfig` como objeto e a precedência completa de configuração;
o renderer OpenGL do CE (os 48 mobjects `OpenGL*`, `Shader`, `Mesh`) e o cache
dele — `handle_caching_play` (`utils/caching.py`) existe e é **só** do caminho
OpenGL, com um comentário do próprio ManimCE dizendo que o cairo foi refatorado e
não precisa mais dele; assets externos (SVG, imagem, fonte) como assunto de
projeto; som e legenda.

---

## 13. O que NÃO foi verificado nesta sessão

Uma afirmação marcada como não verificada vale mais que uma afirmação falsa.

- **Nada foi renderizado.** Nenhum `mx render`, `manim`, `ffmpeg`, `ffprobe`,
  `mx bench`, `mx doctor`. **Todos os comandos da §9 estão escritos e não
  executados** — as flags foram conferidas uma a uma contra
  `manimx/cli.py:453-476` e `manim/cli/render/global_options.py`, mas a saída
  real não foi vista.
- **Nenhum número de segundos** aparece nesta skill, de propósito. Não há
  medição de tempo de hash, de desenho, de encode ou de acerto de cache — nem
  minha nem herdada. Onde a §8 fala de custo, ela fala de **mecanismo**.
- **[INFERIDO], não reproduzido:** o `functools.partial` sem `func` no `__dict__`
  (§2.4a); o sintoma do `.svg` truncado de LaTeX (§4.4); o custo do sha256 sobre
  o `pixel_array` de um `ImageMobject` (§2.3, §8.5); o efeito colateral benéfico
  do palco fixo sobre o cache de texto (§5.3); a causa dos 4 `.tex` órfãos
  (§4.3 — o **fato** é medido, a causa é dedução).
- **[CORRIGIDO nesta rodada]:** `bin/manim-python` **não existe** — `bin/` tem
  cinco entradas (`manim`, `manim-env.sh`, `manimgl`, `mx`, `setup`), como a
  §9.5 já dizia com `[DISCO]`. O comando da §9.6 foi trocado por
  `.venv/bin/python`. E o `functools.partial` da §2.4a foi medido: ele **tem**
  `__dict__`.
- **[DISCO], desta máquina em 2026-08-19:** 113 partials (60 hash + 53
  `uncached`), 8 diretórios de partials, `media/Tex` 42 `.svg` + 46 `.tex`,
  `media/texts` 42 `.svg`, `media/` 26 MiB. São fatos deste repositório, não
  constantes do Manim.
- **O que FOI conferido lendo o fonte**, com arquivo e linha: os três CRC32 e
  toda a política de serialização (`utils/hashing.py`), o fluxo de `play` do
  cairo (`renderer/cairo_renderer.py:62-120`), o frame estático
  (`:110,153-154,218-243`) e o recorte de `get_moving_mobjects`
  (`scene/scene.py:899-946`), a regra do wait congelado (`:419-446`,
  `cairo_renderer.py:197-209`), toda a poda (`scene_file_writer.py:615-630,
  1036-1038, 1056-1090`), a limpeza de partial truncado (`:176-190, 734-770`),
  o concat por stream copy (`:911-927`) e o reencode do GIF (`:857-909`),
  `write_to_movie()` (`utils/file_ops.py:110-129`) e os setters que o zeram
  (`_config/utils.py:807-808, 855-857, 1374-1376`), o cache de LaTeX e Typst
  (`utils/tex_file_writing.py`, `utils/typst_file_writing.py`), os dois
  `_text2hash`/`_text2svg` (`mobject/text/text_mobject.py:689-701, 834-866,
  1363-1417`), o `hash_seed` do SVG (`mobject/svg/svg_mobject.py:161-195`) e os
  atributos da câmera que entram no hash (`camera/camera.py:100-150`).
