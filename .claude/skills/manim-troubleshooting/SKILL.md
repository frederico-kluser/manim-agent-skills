---
name: manim-troubleshooting
description: >-
  Diagnosticar uma falha CONCRETA do Manim e provar a causa antes de mexer no
  código — traceback, exit code, arquivo de saída que não aparece, vídeo vazio
  ou curto demais, cache servindo resultado velho, erro de LaTeX, render que
  trava ou come memória, GPU/codec, e a classe pior de todas: a cena que
  renderiza com `success: true` e sai ERRADA sem uma linha de aviso. Use SEMPRE
  que a frase for "o render falhou", "deu erro no Manim", "não acho o mp4", "o
  vídeo saiu vazio", "saiu preto/branco", "sumiu o texto", "cortou na borda",
  "mudei o código e o vídeo continua igual", "mudei o preço e o vídeo não
  mudou", "renderizou mas nada mudou", "a animação não acontece", "travou",
  "estourou a memória", "o LaTeX quebrou", "não acho o
  erro", "funciona no meu, não no CI", "roda uma vez e na segunda quebra". Traz
  o funil de diagnóstico, o mapa completo sintoma → causa → correção, o
  procedimento de bissecção em cinco eixos, a anatomia das TRÊS caches
  independentes, e a lista de defeitos que não levantam exceção nenhuma. NÃO use
  para: descobrir se um nome/assinatura/kwarg existe — um `AttributeError` ou
  `TypeError: unexpected keyword argument` de NOME é `manim-api-discovery`;
  escolher qualidade/formato e API de render é `manim-render-api`; **"está
  lento" tem três donos e esta skill não é nenhum deles**: se o gargalo é o
  ENCODE (codec, NVENC, peso do mp4) é `manim-gpu-encoding`, se é a cena
  DESENHAR ou o cache não acertar é `manim-performance-cache`, se são MUITAS
  cenas é `manim-batch-pipeline` — aqui só entra travamento/estouro de memória,
  que é falha, não lentidão; paralelismo e CI é
  `manim-batch-pipeline`; conferir o RESULTADO frame a frame (contraste, corte,
  sobreposição, comparação de imagens) é `manim-verificacao-visual`; e o mapa do
  repositório é `manim-project`.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Diagnóstico — o que quebrou, por quê, e como provar

> **Procedência.** Tudo marcado **[FONTE]** foi lido hoje (2026-08-19) no código
> instalado — `.venv/lib/python3.12/site-packages/manim/` (ManimCE 0.21.0) ou
> `manimx/` deste repositório — e vem com arquivo e linha. **[DECK]** vem de
> medição feita no projeto consumidor `~/Projects/aulas`, não reproduzida aqui.
> **[NV]** é hipótese de leitura, não verificada por execução. Nenhum render,
> benchmark ou ffmpeg rodou para escrever esta skill.

## 0. A única ideia que organiza tudo: falha barulhenta, falha muda, falha mentirosa

O Manim erra de três jeitos, e cada um pede um método diferente. Escolher o
método errado é o que faz uma sessão de depuração durar horas.

| Família | Como se manifesta | O que resolve | Seção |
|---|---|---|---|
| **Barulhenta** | traceback, exit ≠ 0, `success: false` | ler a mensagem certa e bisseccionar | §2, §9 |
| **Muda** | exit 0, `success: true`, e **nenhum arquivo** — ou um arquivo curto demais | entender o que o Manim considera "nada a fazer" | §7 |
| **Mentirosa** | exit 0, arquivo gerado, **conteúdo errado** | olhar o resultado; o terminal nunca vai contar | §4, §5, §10 |

A terceira é a mais cara e a mais frequente em código gerado por agente. **O exit
code do Manim não é um teste de qualidade.** Ele responde "o Python terminou sem
levantar exceção", nada mais. Texto branco em fundo branco, elemento cortado pela
borda, animação que não acontece, número velho vindo do cache — **nenhum desses
levanta erro**.

---

## 1. O funil de 60 segundos

Rode nesta ordem. Cada passo elimina uma família inteira de causas, e nenhum
custa mais que dois segundos.

```bash
bin/mx doctor                          # 1. o ambiente está de pé?   (~1,8 s)
bin/mx scenes scenes/cena.py           # 2. o ARQUIVO importa?       (~0,9 s)
bin/mx render scenes/cena.py Cena -q l --format png --json   # 3. a cena RODA?
```

**O que cada passo prova, e o que ele NÃO prova:**

| Passo | Prova | **Não** prova |
|---|---|---|
| `mx doctor` | Python, ManimCE, PyAV, Pango estão de pé | que o LaTeX funciona — o check dele **não é fatal** (§3.1) |
| `mx scenes` | o módulo importa, e quais classes o pipeline enxerga | que `construct` roda — ele só importa (`manimx/render.py:111-146`) |
| `mx render --format png` | `construct` executa do começo ao fim | que o vídeo sai — `--format png` **desliga o mp4** (§7.2) |

Se o `doctor` está verde e o `--format png` sai, o problema **não é o ambiente**:
é a cena, o cache ou o que você está olhando. Vá para §4, §5 ou §10.

### 1.1 Antes de qualquer outra coisa: confirme que você chamou o wrapper

Metade das falhas "misteriosas" desta máquina é ter chamado o binário errado.

```bash
bin/mx …          bin/manim …          bin/manimgl …      # ✅
.venv/bin/mx …    .venv/bin/manim …    manim …            # ❌
```

`bin/manim-env.sh` resolve três coisas que ninguém lembra: TinyTeX no PATH,
PRIME offload para a dGPU, e o venv à frente do Python do sistema. **[FONTE]**
`bin/manim-env.sh:13-27, 55-68`. Fora do wrapper você perde as três, **em
silêncio** — o detalhe de cada uma está em `manim-project` §3, que é o dono do
assunto.

E existe um `.venv/bin/mx` gerado pelo `[project.scripts]` que **não** é o
wrapper: ele roda, imprime "Ambiente pronto" e mente (`manim-project` §3.3).

---

## 2. Ler a falha direito

### 2.1 O `mx render` tem DUAS classes de falha, e só uma delas devolve JSON

Esta é a distinção que mais economiza tempo, e não está documentada em lugar
nenhum. **[FONTE]** `manimx/render.py:495` e `manimx/cli.py:540-548`:

```python
# manimx/render.py  (render_file)
classes = load_scene_classes(path)      # linha 495 — FORA de qualquer try

# manimx/render.py  (render_scene)
started = time.perf_counter()           # linha 417
try:                                    # linha 418
    ...
    scene = scene_class()
    scene.render()
except BaseException as exc:            # linha 452
    result.success = False
    result.error = f"{type(exc).__name__}: {exc}"
    result.traceback_text = traceback.format_exc()
```

| Onde a exceção nasce | Saída | exit | Como reconhecer |
|---|---|---|---|
| **dentro de `construct`** (ou `setup`/`tear_down`) | JSON válido, com `success:false`, `error`, `traceback_text` | 1 | stdout tem `[{...}]` |
| **no IMPORT do arquivo** (SyntaxError, ImportError, erro em código de nível de módulo) | **nada em stdout**; `erro: SyntaxError: …` em stderr | 1 | stdout **vazio** |

Consequência prática, e é a armadilha: com `--json`, um erro de import faz o seu
`json.load(sys.stdin)` estourar com `JSONDecodeError: Expecting value` — e você
vai depurar o seu parser em vez do arquivo de cena. **Sempre trate stdout vazio
como "falhou antes de importar" e leia o stderr.**

```bash
bin/mx render scenes/cena.py Cena -q l --json > /tmp/r.json 2> /tmp/r.err
[ -s /tmp/r.json ] || { echo "falhou no IMPORT:"; cat /tmp/r.err; }
```

E para ver o traceback do erro de import, não só a última linha:

```bash
bin/mx -v render scenes/cena.py Cena -q l      # -v faz o `main` RE-LEVANTAR
```

**[FONTE]** `manimx/cli.py:544-548`: `except Exception as exc: if args.verbose: raise`.
O `-v` funciona antes **ou** depois do subcomando (`cli.py:434-445`, parser-pai
com `default=SUPPRESS`).

### 2.2 Extrair o traceback de dentro do JSON

```bash
bin/mx render scenes/cena.py Cena -q l --json 2>/dev/null | python3 -c "
import json,sys
for r in json.load(sys.stdin):
    if not r['success']:
        print(r['scene_name'], '->', r['error'])
        print(r['traceback_text'])"
```

Com `--json`, todo log do Manim é redirecionado para stderr para não sujar o
stdout **[FONTE]** `manimx/cli.py:526-535` — por isso o `2>/dev/null` é seguro
aqui, e por isso ele é **perigoso** quando você está caçando um warning (§2.3).

### 2.3 A verbosidade padrão do `mx render` esconde exatamente a pista que você precisa

**[FONTE]** `manimx/cli.py:475`: `s.add_argument("--verbosity", default="WARNING")`.
O `manim.cfg` deste projeto usa `verbosity = INFO`. Ou seja, o `mx render`
**rebaixa** a verbosidade e engole as linhas de nível INFO — que são justamente
as que contam o que aconteceu:

| Linha de log | Nível | Onde nasce | O que ela responde |
|---|---|---|---|
| `Animation N : Using cached data (hash : …)` | INFO | `renderer/cairo_renderer.py:92-95` | o cache foi usado nesta animação |
| `Caching disabled.` | INFO | `renderer/cairo_renderer.py:81` | `--no-cache` pegou |
| `No animations are contained in this scene.` | INFO | `scene/scene_file_writer.py:949` | **por isso não saiu mp4** |
| `The partial movie directory is full (> N files)…` | INFO | `scene/scene_file_writer.py:1073-1076` | a poda de cache rodou |
| `Cache flushed. N file(s) deleted…` | INFO | `scene/scene_file_writer.py:1087-1090` | o `--flush_cache` rodou |
| `Font X not in [… 411 nomes …]` | WARNING | `mobject/text/text_mobject.py:490` | a fonte não existe (§4.6) |

**Regra:** ao investigar cache ou arquivo ausente, **suba a verbosidade e leia o
stderr**:

```bash
bin/mx render scenes/cena.py Cena -q l --verbosity INFO 2>&1 | grep -E "cached|No animations|Cache"
bin/manim -ql -v INFO scenes/cena.py Cena 2>&1 | tail -40
```

### 2.4 `-v` significa duas coisas diferentes, e as duas existem

| Comando | Flag | Significado |
|---|---|---|
| `bin/mx -v render …` | `-v/--verbose` | log de debug **do próprio `mx`** + re-levanta a exceção **[FONTE]** `manimx/cli.py:435` |
| `bin/mx render … --verbosity DEBUG` | `--verbosity` | nível do logger **do Manim** |
| `bin/manim -v DEBUG …` | `-v/--verbosity` | nível do logger do Manim **[FONTE]** `cli/render/global_options.py:82-92` |

Escrever `bin/manim -v cena.py Cena` é erro: o `-v` do CLI cru **consome o
próximo token como o nível**, e `cena.py` não é um nível válido.

### 2.5 O aviso de depreciação: `bin/manim` liga, `mx render` NÃO

Descoberta desta rodada, e ela explica uma família inteira de "não deu erro
nenhum". O CLI cru do ManimCE registra um filtro de warnings para o módulo da
cena **[FONTE]** `manim/utils/module_ops.py:53-57`:

```python
warnings.filterwarnings("default", category=DeprecationWarning, module=module_name)
```

`manimx.render.load_scene_classes` (`manimx/render.py:111-146`) **não faz nada
disso**. E o Python ignora `DeprecationWarning` por padrão fora de `__main__` —
conferido nesta máquina, `.venv/bin/python -c "import warnings; print(*warnings.filters, sep='\n')"`:

```
('default', None, <class 'DeprecationWarning'>, '__main__', 0)      ← só em __main__
('ignore',  None, <class 'DeprecationWarning'>, None, 0)            ← em todo o resto
```

O módulo da cena nunca é `__main__` (o `mx` o nomeia
`_manimx_scene_<stem>_<hash>`, `manimx/render.py:123`), então o segundo filtro
vence.

**Consequência:** o `set_qualquercoisa()` sintetizado (§4.1) emite um
`DeprecationWarning` que o `bin/manim` mostra e o `bin/mx render` **come**.

```bash
# reproduza a MESMA cena pelos dois caminhos e compare o stderr
bin/manim -ql scenes/cena.py Cena 2>&1 | grep -i deprecat
PYTHONWARNINGS='default::DeprecationWarning' bin/mx render scenes/cena.py Cena -q l 2>&1 | grep -i deprecat
```

A segunda linha usa a variável de ambiente padrão do Python para reativar o
filtro globalmente. **[NV]** — o mecanismo é o do interpretador, mas não rodei.

---

## 3. Ambiente

```bash
bin/mx doctor          # 10 checks
bin/mx doctor --json | python3 -c "
import json,sys
for c in json.load(sys.stdin)['checks']:
    if not c['ok']: print('FALHOU', c['check'], '|fatal:', c['fatal'], '|', c['detail'])"
bin/mx gpu             # GPU, PRIME, encoders
```

### 3.1 Verde não quer dizer pronto — e o LaTeX **não** é fatal

**De acordo com `manim-project` §4.1**, que é a dona do `mx doctor` e já traz
esta correção: **são quatro** os checks fatais, e o LaTeX não está entre eles.
Repetimos a tabela aqui porque é o primeiro passo do funil de diagnóstico — não
como achado novo. **[FONTE]** `manimx/cli.py`:

| Check | linha do `add(...)` | fatal na FALHA? |
|---|---|---|
| `python >= 3.11` | `cli.py:69` | **sim** (default `fatal=True`, `cli.py:62`) |
| `manim (CE)` | `cli.py:97` | **sim** |
| `PyAV + libx264` | `cli.py:106` | **sim** |
| `Pango (Text)` | `cli.py:142` | **sim** |
| `manim atualizado` | `cli.py:90-94` | não |
| `NVENC (h264_nvenc)` | `cli.py:110-114` | não |
| `latex`, `dvisvgm`, `ffmpeg` | `cli.py:117-119` | não |
| **`LaTeX → SVG (MathTex)`** | `cli.py:126` (sucesso) / `cli.py:129-133` (falha) | **não** — no caminho de SUCESSO ele nasce com o `fatal=True` do default, e só o ramo de exceção passa `fatal=False` explícito. Ou seja: ele só é não-fatal exatamente quando falha |
| `manimgl` | `cli.py:167-171` | não |

`failed_fatal = [c for c in checks if not c["ok"] and c["fatal"]]` e
`return 1 if failed_fatal else 0` (`cli.py:173, 185`).

**Portanto: `bin/mx doctor` sai 0 com o LaTeX completamente quebrado.** Se o seu
sintoma envolve `Tex`/`MathTex`, **não confie no exit code** — itere `checks` e
leia `ok:false` mesmo com `fatal:false`.

Some a isso a armadilha do cache do check (`manim-project` §4.2): o check é
literalmente `MathTex(r"x^2")` (`cli.py:126`), e o SVG dele fica em `media/Tex`.
Rodando da raiz do projeto, com o cache quente, **ele passa sem tocar no
`dvisvgm`**. A linha `dvisvgm` do doctor é mais confiável que a linha
`LaTeX → SVG`. Se as duas discordarem, acredite na primeira.

### 3.2 `dvisvgm` — a correção do que esta skill dizia errado

**A versão anterior desta skill mandava `tlmgr install dvisvgm`. Está errado, e
não resolve nada nesta máquina.** O binário existe:

```
$ ls -la ~/.TinyTeX/bin/x86_64-linux/dvisvgm
.rwxr-xr-x 5.0M ondokai 18 Feb 20:25 /home/ondokai/.TinyTeX/bin/x86_64-linux/dvisvgm

$ ls -la ~/.local/bin/latex ~/.local/bin/dvisvgm
lrwxrwxrwx  latex -> /home/ondokai/.TinyTeX/bin/x86_64-linux/latex
(dvisvgm: No such file or directory)
```

O que falta é o **symlink em `~/.local/bin`**: o `latex` tem, o `dvisvgm` não.
Como `~/.local/bin` está no PATH normal e `~/.TinyTeX/bin/x86_64-linux` não, o
`latex` é encontrado e o `dvisvgm` não. **A correção é usar `bin/mx` ou
`bin/manim`**, que põem o diretório inteiro do TinyTeX à frente do PATH
(`bin/manim-env.sh:13-27`).

O sintoma é enganoso porque a falha acontece **no fim** do pipeline — o `.dvi`
compila, a conversão para SVG é que morre — então o traceback fala de
`subprocess`, não de LaTeX:

```
FileNotFoundError: [Errno 2] No such file or directory: 'dvisvgm'
```

### 3.3 Tabela de ambiente

| Sintoma | Causa | Correção |
|---|---|---|
| `FileNotFoundError: … 'dvisvgm'` | `~/.local/bin` não tem o symlink; o PATH normal não vê o TinyTeX | **`bin/mx` / `bin/manim`** — não `tlmgr install` (§3.2) |
| `FileNotFoundError: … 'latex'` | idem, num ambiente onde nem o symlink do `latex` existe | idem |
| `ModuleNotFoundError: No module named 'manim'` | venv errado | `bin/mx`, ou `.venv/bin/python` |
| `ModuleNotFoundError: No module named 'manimlib'` | está no venv da CE | `bin/manimgl`; `mx` **só** enxerga o venv da CE |
| `import manimlib` mata o argparse do seu script | o manimlib parseia `sys.argv` **no import** | `sys.argv = [sys.argv[0]]` antes do import (`manim-project` §11) |
| Manim antigo demais (0.18/0.19) | `pip install manim` em Python < 3.11 resolve para trás **sem erro** | `bin/mx doctor`; exige 3.11+ |
| `mx doctor` verde mas `MathTex` falha | o check de LaTeX **não é fatal** e ainda passa em cache | §3.1 |
| OpenGL rodando na Intel | notebook híbrido sem PRIME offload | `bin/*`; detalhes em `manim-project` §3.2 |
| Tudo funciona da raiz e quebra de outro `cwd` | o `manim.cfg` é lido do **CWD** | rode da raiz; `manim-project` §5 |

---

## 4. O silêncio — defeitos que não levantam exceção nenhuma

Esta é a seção que justifica a skill. Todos os itens abaixo produzem **exit 0**.

### 4.1 `mob.set_qualquer_coisa(...)` SEMPRE "funciona"

**[FONTE]** `manim/mobject/mobject.py:729-774`. `Mobject.__getattr__` sintetiza
um método para qualquer atributo começando com `get_` ou `set_`:

```python
if attr.startswith("set_"):
    to_set = attr[4:]
    def setter(self, value):
        warnings.warn("This method is not guaranteed to stay around…",
                      DeprecationWarning, stacklevel=2)
        setattr(self, to_set, value)          # ← escreve QUALQUER coisa
        return self
    return types.MethodType(setter, self)
raise AttributeError(f"{type(self).__name__} object has no attribute '{attr}'")
```

Três comportamentos, e só um é o que você esperava:

| Você escreveu | O que acontece | Visível? |
|---|---|---|
| `mob.set_width(4)` | `setattr(mob, "width", 4)` → cai no `@width.setter` (`mobject.py:808-810`) → `scale_to_fit_width(4)` | **funciona**, com um `DeprecationWarning` que o `mx render` engole (§2.5) |
| `mob.set_raio(2)` | `setattr(mob, "raio", 2)` — atributo novo, ninguém lê | **nada acontece, sem erro** |
| `mob.set_center(ORIGIN)` | `setattr(mob, "center", ORIGIN)` — o array **sombreia o método `Mobject.center()`** | quebra depois, longe daqui: `TypeError: 'numpy.ndarray' object is not callable` **[NV]** |

E o `get_` tem um efeito colateral que confunde a leitura do traceback: o
`getattr(self, to_get)` interno falha e re-entra em `__getattr__`, então a
mensagem nomeia o atributo **sem o prefixo**:

```
mob.get_raio()   →   AttributeError: Circle object has no attribute 'raio'
                                                                    ^^^^ sem "get_"
```

A prova de que `set_width` é sintetizado no caminho cairo, conferida hoje no
índice (`api/manim-ce-methods.tsv`, colunas `class·method·kind·defined_in·
inherited·signature·doc`):

```
$ awk -F'\t' '$2=="set_width"{print $4}' api/manim-ce-methods.tsv | sort -u
OpenGLMobject                        # ← as 45 ocorrências, TODAS do OpenGL
$ awk -F'\t' '$1=="Circle" && $2=="set_width"' api/manim-ce-methods.tsv | wc -l
0                                    # ← o Circle do cairo NÃO tem esse método
```

**Diagnóstico:** procurar `set_` inventado é grep puro, custa milissegundos.

```bash
grep -noE '\.set_[a-z_]+\(' scenes/cena.py | sed -E 's/.*\.(set_[a-z_]+)\(/\1/' | sort -u \
  | while read -r m; do
      n=$(awk -F'\t' -v m="$m" '$2==m' api/manim-ce-methods.tsv | wc -l)
      [ "$n" -eq 0 ] && echo "SINTETIZADO (não existe): $m"
    done
```

Se o nome não aparece no índice como método real, ele está sendo sintetizado — e
o antídoto é o atributo direto (`mob.width = 4`), o `mob.set(width=4)` ou o
método explícito (`scale_to_fit_width(4)`). A varredura sistemática de nomes
inventados é de **`manim-api-discovery`** §8 — esta skill só diz como o sintoma
se apresenta.

### 4.2 `.animate` sem método, ou com método sintetizado

`mob.animate` devolve um `_AnimationBuilder`. **[FONTE]** `mobject.py:3466-3474`:

```python
def build(self):
    anim = self.overridden_animation or _MethodAnimation(self.mobject, self.methods)
```

- `self.play(mob.animate)` — `self.methods` vazio → uma animação **válida** que
  não faz nada por `run_time` segundos. Sem erro.
- `self.play(mob.animate.set_raio(2))` — `__getattr__` do builder faz
  `getattr(self.mobject.target, "set_raio")` (`mobject.py:3439-3440`), o
  `Mobject.__getattr__` sintetiza, o alvo ganha um atributo inútil e a
  interpolação não move nada. Sem erro.

**Diagnóstico:** se a animação "não acontece", troque `.animate` pela classe
explícita (`Rotate`, `Transform`, `FadeIn`) — se aí o erro aparece, era isto.
Catálogo de classes e a fronteira `.animate` × classe: **`manim-animations`**.

### 4.3 `Transform` e o alvo que nunca entrou na cena

**[FONTE]** docstring de `Transform` (`animation/transform.py`, parâmetro
`replace_mobject_with_target_in_scene`): *"Otherwise, `target_mobject` is never
added and `mobject` just takes its shape."*

```python
self.play(Transform(a, b))     # `a` fica com a APARÊNCIA de `b`; `b` NÃO está na cena
self.play(b.animate.shift(UP)) # anima um objeto invisível → nada na tela, sem erro
self.play(a.animate.shift(UP)) # ✅ é `a` que está lá
```

`ReplacementTransform(a, b)` faz o contrário: remove `a` e deixa `b`. A escolha
entre os dois é de **`manim-animations`**; aqui só interessa que o sintoma
("animei e não moveu") tem essa causa e não dá erro.

### 4.4 O vídeo vazio: dois mecanismos diferentes, e só um deixa um arquivo

Este é o "renderizou, exit 0, e não tem mp4" — e a explicação está em duas
linhas de código que quase ninguém leu.

**[FONTE]** `manim/renderer/cairo_renderer.py:269-282`:

```python
def scene_finished(self, scene):
    if self.num_plays:                    # houve pelo menos um self.play
        self.file_writer.finish()
    elif config.write_to_movie:           # NENHUM self.play
        config.save_last_frame = True     # ← vira PNG, calado
        config.write_to_movie = False
```

**[FONTE]** `manim/scene/scene_file_writer.py:937-950`:

```python
partial_movie_files = [el for el in self.partial_movie_files if el is not None]
if len(partial_movie_files) == 0:
    logger.info("No animations are contained in this scene.")
    return                                 # ← sai sem escrever NADA
```

| Situação | `num_plays` | Resultado | JSON do `mx` |
|---|---|---|---|
| cena só com `self.add(...)`, zero `self.play` | 0 | **um PNG**, silenciosamente | `output_file: null`, `image_file` preenchido |
| houve `play`, mas **todos** foram pulados — `-n` fora da faixa, ou toda seção com `skip_animations=True` (`cairo_renderer.py:253-254`) | ≥ 1 | **nada** — nem mp4 nem png | `output_file: null`, `image_file: null`, `success: true` |

O segundo caso é exatamente o modo de falha do formato de cena em partes quando
um `_corte(n)` fica órfão: `PARTE` não casa com seção nenhuma, todas as seções
pulam, e o mp4 sai **inexistente**, com sucesso aparente. O procedimento de
renumeração que evita isso é de **`manim-presentation-parts`**; o que esta skill
acrescenta é o mecanismo e o teste:

```bash
# A prova, em uma linha (a linha só aparece em INFO — §2.3):
bin/mx render scenes/cena.py CenaP7 -q l --verbosity INFO 2>&1 \
  | grep -q "No animations are contained" && echo "TODAS as animações foram puladas"
```

**E o contador que separa os dois casos: `num_animations` no JSON.** Ele lê
`scene.renderer.num_plays` (`manimx/render.py:450`), e esse contador é
incrementado **no fim de todo `play`, pulado ou não**
(`cairo_renderer.py:121`) — ou seja, ele conta *invocações*, não frames escritos:

| `num_animations` | Arquivo | Leitura |
|---:|---|---|
| **0** | um PNG | o `construct` não chamou nenhum `play`/`wait` — primeiro caso da tabela |
| **> 0** | **nenhum** | todas as invocações foram puladas — segundo caso |
| **> 0** | mp4 | normal; se o vídeo está curto demais, alguma faixa foi pulada (`-n` esquecido, §9.2) |

### 4.5 Branco no branco (e preto no preto)

O Manim escreve **branco** por padrão. Em tema claro, todo `Text`/`Mobject` sem
cor explícita desaparece **sem erro nenhum**.

Pior: `--theme whiteboard` é aplicado **depois** do import do módulo da cena
(`manim-project` §9.1), então qualquer mobject criado no nível do módulo fica com
a cor antiga. Medido lá: `cedo=#FFFFFF` sobre `bg=#FFFFFF`.

- **A defesa real é cor explícita em todo mobject**, centralizada num `tema.py`.
  Dono do assunto: **`manim-color-theming`** (paleta, contraste WCAG,
  `set_default` e o que ele não alcança).
- Truque de leitura que evita um falso negativo: `Text(...).color` do **grupo** é
  sempre `#000000`. A cor real mora nos glifos, em
  `.submobjects[i].fill_color`.

Diagnóstico rápido, sem render, dentro da cena:

```python
for m in self.mobjects:
    print(type(m).__name__, getattr(m, "fill_color", None), getattr(m, "stroke_color", None))
```

### 4.6 Fonte ausente vira outra fonte, e o objeto continua mentindo

**[FONTE]** `manim/mobject/text/text_mobject.py:476-491`: se a família não está
em `manimpango.list_fonts()`, o código tenta `capitalize()`, `lower()`,
`title()`, e se nada bater emite

```python
logger.warning(f"Font {font} not in {fonts_list}.")
```

— despejando **as 411 famílias** na mesma linha. É um WARNING que ninguém lê
porque é uma parede de texto. E `t.font` continua devolvendo o nome que você
pediu (`text_mobject.py:492`): o objeto não sabe que foi substituído.

```bash
bin/mx render scenes/cena.py Cena -q l 2>&1 | grep -oE "Font [^ ]+ not in" | sort -u
```

Nesta máquina **`Inter`, `SF Pro Text`, `Helvetica` e `Arial` NÃO existem**
(`manim-project` §10.4). Fonte, pilha de fallback e nitidez: **`manim-text-latex`**.

### 4.7 `-r 1080x1920` não deixa o vídeo vertical

Muda o buffer de pixels, não o palco: `frame_width` continua 14,222 e
`frame_height` 8,0, então `to_edge(UP)` cai a 37,7% do topo. Medido em
`manim-project` §9.3, com a correção (`config.frame_width = config.frame_height * 1080/1920`).
Enquadramento em profundidade: **`manim-layout-posicionamento`**.

### 4.8 `--codec av1` grava libx264 com `success: true`

A validação do `manimx` detecta que o remux dos partial movies falharia
(`UnknownCodecError: libdav1d`) e substitui o codec. O exit code não conta.
**[FONTE]** `manimx/gpu.py:248-310` — `validate_encoder` abre um encoder de
verdade, codifica 1 frame **e testa o `add_stream_from_template`**, porque o
libav só valida opções em `avcodec_open2`, que o PyAV chama preguiçosamente no
primeiro frame. Codec, NVENC e a matriz do que funciona: **`manim-gpu-encoding`**.

Para conferir o que de fato saiu no arquivo, sem `ffprobe`:

```bash
grep -aqo "x264 - core" saida.mp4 && echo libx264 || echo "NVENC ou outro"
```

### 4.9 Elemento invisível continua na caixa delimitadora

Um detalhe transparente (espaçador, lingueta) conta no bounding box do `VGroup`.
`VGroup.move_to()` desloca o grupo inteiro pelo tamanho do invisível — **4 px,
medidos, silenciosos** **[DECK]**. Posicione pelo **corpo visível**, não pelo
grupo. É a causa nº 1 de "o desenho está 4 px fora do lugar e eu não mexi nele".

### 4.10 `DashedVMobject` descarta o `color=` que você passou

**[FONTE]** `manim/mobject/types/vectorized_mobject.py:3042-3046`: o `__init__`
chama `super().__init__(color=color)` no começo mas **termina** com
`self.match_style(base_vmobject, family=False)`, que sobrescreve o estilo com o
da curva de origem. Em fundo branco, uma curva sem cor explícita vira tracinhos
brancos — invisível, sem erro.

```python
base = Rectangle(color=TINTA, stroke_width=2)   # estilize ANTES
tracejado = DashedVMobject(base, num_dashes=24)  # o color= aqui é DESCARTADO
```

### 4.11 `python cena.py` sai 0 e não faz nada

O arquivo só define classes. Sem `mx render`/`manim`, ninguém chama `construct`.
Sucesso aparente, zero saída (`manim-project` §10.8).

---

## 5. Cache — o mentiroso profissional

**Sintoma-mestre: "eu mudei o código (ou o dado) e o vídeo continua igual."**
Antes de acusar o cache, saiba que existem **três caches independentes**, com
mecanismos, chaves e comandos de limpeza diferentes. Confundi-los é o que faz
gente "limpar o cache" e o problema continuar.

| # | O quê | Onde | Chave | Como desligar | Como apagar |
|---|---|---|---|---|---|
| 1 | **partial movies** (um mp4 por `play`) | `media/videos/<mod>/<qual>/partial_movie_files/<Cena>/` | `crc32(camera)_crc32(anims)_crc32(mobjects)` | `--no-cache` (`mx`) / `--disable_caching` (CLI) | `rm -rf .../partial_movie_files` |
| 2 | **LaTeX compilado** | `media/Tex/<sha256[:16]>.svg` | sha256 do **texto .tex inteiro**, preâmbulo incluído | não tem flag | `rm -rf media/Tex` |
| 3 | **SVG de `Text`/Pango** | `media/texts/<sha256[:16]>.svg` | sha256 de `"PANGO"+font+slant+weight+cor+t2f+t2s+t2w+t2c+line_spacing+font_size+ligatures+gradient+texto` — **a resolução NÃO entra** | **não tem flag** | `rm -rf media/texts` |

### 5.1 Como a chave do cache 1 é montada

**[FONTE]** `manim/utils/hashing.py:445-461`:

```python
camera_json              = _get_json(camera_object, memoizer)
animations_list_json     = [_get_json(a, memoizer, include_pixel_array=True) for a in sorted(animations_list, key=str)]
current_mobjects_list_json = [_get_json(m, memoizer, include_pixel_array=True) for m in current_mobjects_list]
hash_complete = f"{crc32(camera)}_{crc32(anims)}_{crc32(mobjects)}"
```

Três coisas que se leem daí e valem ouro:

1. **A chave é o ESTADO, não o código.** Se você refatorou e o estado final é o
   mesmo, o hash é o mesmo e o Manim reaproveita — corretamente.
2. **`pixel_array` ENTRA** para mobjects e animações (`include_pixel_array=True`).
   Trocar o PNG de um `ImageMobject` **invalida** o cache. (Para a *câmera* ele
   é filtrado, via `KEYS_TO_FILTER_OUT`, `hashing.py:30-34`.)
3. É `crc32`, não hash criptográfico. Três campos de 32 bits. Colisão é
   irrelevante na prática, mas não é uma garantia forte.

### 5.2 O que a chave NÃO enxerga

A regra vem do serializador `_get_json`, e ela é mais estreita do que parece.
**[FONTE]** `manim/utils/hashing.py:264-302`, na ordem em que ele testa:

| O objeto é… | O que ENTRA no hash | linha |
|---|---|---|
| função ou método | `inspect.getsource(obj)` (o **texto do código**) + `getclosurevars` (globals e nonlocals do fecho, **menos módulos**) | `:265-283` |
| `np.ndarray` | sha256 do conteúdo canônico + dtype + shape | `:284-291`, `:71-87` |
| qualquer objeto **com `__dict__`** | o `__dict__` inteiro, recursivamente | `:292-297` |
| **todo o resto** | **`str(type(obj))` — só o NOME DO TIPO** | `:302` |

A última linha é a armadilha. Um valor sem `__dict__` — `datetime`, `Decimal`,
`pathlib.Path`, qualquer coisa de extensão C com `__slots__` — contribui apenas
`"<class 'datetime.datetime'>"`. **Dois valores diferentes desse tipo produzem o
mesmo hash.** Se um número que vem de fora vai decidir o que aparece na tela,
guarde-o como `str`/`int`/`float` antes de pendurá-lo no mobject.

E, acima de tudo: **o arquivo que a cena leu nunca entra.** O fecho de
`lambda: Text(carrega_preco())` contribui o *código-fonte* de `carrega_preco`,
não o conteúdo do CSV. Se o dado externo virar texto/posição de um mobject, o
hash muda por tabela e o cache acerta sozinho; se ele influenciar qualquer outra
coisa, o cache serve o vídeo velho com o dado novo — está em `manim.cfg` e em
`manim-project` §10.7. **Cena com dado de fora: `--no-cache`, sempre.** É barato e
elimina a dúvida.

Duas outras coisas que a chave não vê:

- **`random` sem semente.** **[FONTE]** `manim/scene/scene.py:180, 223-224`:
  `self.random_seed = random_seed if random_seed is not None else config.seed`, e
  o default de `config.seed` é `None` (`_config/utils.py:1854-1862`;
  `random.seed(None)` semeia da entropia do SO). Consequência dupla e
  contraintuitiva: uma cena com `random` **nunca acerta o cache** (o estado muda
  todo render) e **nunca reproduz** o vídeo anterior. Se você quer as duas
  coisas, passe `--seed`:
  ```bash
  bin/manim -ql --seed 0 scenes/cena.py Cena
  ```
  (`--seed` é do CLI cru; o `mx render` não expõe. Na API/`config`: `config.seed = 0`.)
- **a resolução, no cache 3.** **[FONTE]** `Text._text2hash`
  (`mobject/text/text_mobject.py:689-701`) monta a chave sem
  `pixel_width`/`pixel_height`; `Text._text2svg` (`:834-865`) faz
  `if file_name.exists(): reusa` na **linha 846** e só depois, na 850-851, leria
  `config["pixel_width"]`/`["pixel_height"]` — que o Pango usa como **largura de
  quebra de linha**. Ou seja: um `-qm` (1280) e um `-qh` (1920) podem quebrar
  linha de formas diferentes e o segundo reaproveitar o SVG do primeiro
  (`manim-project` §10.6). O remédio é fixar `config.pixel_width/height` durante a
  construção do texto e devolver num `finally` — receita em **`manim-text-latex`**.
  Cuidado para não confundir com o kwarg `Text(..., use_svg_cache=…)`
  (`text_mobject.py:472`, default `False` na 0.21): esse controla o mapa
  **em memória** do `SVGMobject`, não este cache de disco, que não tem
  interruptor.

### 5.3 `--flush_cache` limpa DEPOIS de renderizar — correção nova

**Este é o achado que mais muda o dia a dia, e contradiz o que esta skill dizia.**

**[FONTE]** `manim/scene/scene_file_writer.py:620-632`, dentro de `finish()`:

```python
def finish(self):
    if write_to_movie():
        self.join_all_encode_jobs()
        self.combine_to_movie()            # ← o vídeo JÁ FOI montado aqui
        if config.save_sections: self.combine_to_section_videos()
        if config["flush_cache"]:
            self.flush_cache_directory()   # ← só agora apaga
        else:
            self.clean_cache()
```

E `grep -rn flush_cache` no pacote inteiro mostra que **este é o único ponto de
chamada**. Portanto:

- `--flush_cache` **não força** o render atual a ignorar o cache. Ele renderiza
  usando o cache velho e **depois** apaga os partial movies. Quem sai limpo é a
  **próxima** execução.
- Está dentro de `if write_to_movie():` — com `--format png` ou `-s`,
  **`--flush_cache` não faz absolutamente nada**.
- `flush_cache_directory` apaga só o diretório **desta cena**
  (`partial_movie_directory`), não o cache do projeto.

**Para forçar um render limpo AGORA, use `--no-cache` / `--disable_caching`,
não `--flush_cache`:**

```bash
bin/mx render scenes/cena.py Cena -q l --no-cache          # ignora o cache nesta execução
bin/manim -ql --disable_caching scenes/cena.py Cena        # idem, pelo CLI cru
```

(Detalhe do `--disable_caching`: o help é preciso — *"Disable the use of the
cache (still generates cache files)"* **[FONTE]** `cli/render/global_options.py:71-76`.
Ele continua **escrevendo** partial movies, com nomes posicionais
`uncached_00000.mp4` (`renderer/cairo_renderer.py:80-82`); só não **lê** os
antigos.)

### 5.4 Cache envenenado: o arquivo truncado que vira acerto

Os dois caches de arquivo têm o mesmo padrão de curto-circuito: *"se o arquivo
existe, use-o"* — sem conferir se ele está inteiro.

**[FONTE]** `manim/utils/tex_file_writing.py:60-62`:

```python
svg_file = tex_file.with_suffix(".svg")
if svg_file.exists():
    return svg_file           # não olha tamanho, não olha conteúdo
```

Mesmo padrão em `compile_tex` (`:204`) e em
`convert_to_svg` (`:244`).

**Consequência:** um `Ctrl+C`/`kill`/OOM no meio do `dvisvgm` deixa um `.svg`
parcial no disco, e **todo render seguinte o reaproveita**. Sintoma: a fórmula
sai vazia, cortada ou deformada, para sempre, e mexer no código não adianta
porque o hash do `.tex` não mudou. **[FONTE]** para o mecanismo, **[NV]** para o
sintoma exato.

Do lado do vídeo, a 0.21 já se defende: `abort_encode_jobs` sela o job corrente
e **apaga o partial** — a docstring diz o porquê com todas as letras
**[FONTE]** `scene/scene_file_writer.py:729-740`: *"an aborted partial is
structurally valid but truncated, so leaving it behind produces an erroneous
cache hit on a later run"*. Mas isso roda no caminho de exceção Python
(`scene/scene.py:275-278`). Um `kill -9` ou um OOM-killer **não** passa por ali:
o partial truncado fica.

**Regra prática: depois de qualquer render interrompido à força, apague o cache
antes de acreditar no próximo resultado.**

```bash
rm -rf media/Tex media/texts
rm -rf media/videos/*/*/partial_movie_files
```

### 5.5 Como PROVAR que o cache foi usado

Não deduza — leia o log (lembre da §2.3: precisa de INFO).

```bash
bin/manim -ql -v INFO scenes/cena.py Cena 2>&1 | grep -c "Using cached data"
# 0  = nada veio do cache
# N  = N animações foram servidas do disco
```

Ou conte os arquivos e compare com `num_animations` do JSON:

```bash
ls media/videos/cena/480p15/partial_movie_files/Cena/ | wc -l
```

### 5.6 A poda automática, e por que a ordem dela é frouxa

**[FONTE]** `scene/scene_file_writer.py:1056-1076`: quando o diretório passa de
`max_files_cached`, o Manim apaga os mais antigos ordenando por
**`path.stat().st_atime`** — tempo de *acesso*, não de modificação. Em sistemas
de arquivos montados com `relatime` (o padrão do Linux moderno) o atime só é
atualizado uma vez por dia, então a ordem de "mais antigo" é aproximada. **[NV]**
— não confirmei as opções de montagem desta máquina.

`max_files_cached` é **200 rodando da raiz do projeto e 100 fora dela**, porque o
`manim.cfg` só vale no CWD (`manim-project` §5).

Nota de fonte, para quem for ler o código: tanto `clean_cache` quanto
`flush_cache_directory` comparam um `Path` com a string
`"partial_movie_file_list.txt"` (`:1061`, `:1083`) — a comparação é sempre
verdadeira, então o arquivo de lista entra na conta e pode ser apagado junto. É
inofensivo (ele é regerado), mas explica contagens estranhas na mensagem de log.

---

## 6. LaTeX

### 6.1 O erro real está no `.log`, e só lá

**[FONTE]** `manim/utils/tex_file_writing.py:143-150`: o comando é montado com
`-interaction=batchmode` e `-halt-on-error`. **`batchmode` significa que o LaTeX
não imprime nada no terminal.** O que você recebe é:

```
ValueError: latex error converting to dvi. See log output above or the log file: media/Tex/<hash>.log
```

O "log output above" vem de `print_all_tex_errors` (`:285-304`), que varre o
`.log` procurando linhas começadas por `!` e imprime cada uma com três linhas de
contexto do `.tex`. Ele também emite duas "insights" úteis
(`:169-179`): caractere não suportado pelo `inputenc`, e pacote não instalado.

```bash
bin/manim -ql --no_latex_cleanup scenes/cena.py Cena 2>&1 | grep -A8 "LaTeX compilation error"
ls -t media/Tex/*.log | head -1 | xargs tail -60
```

**`--no_latex_cleanup` é do `bin/manim`, NÃO do `mx render`.** O `mx` não expõe
essa flag (`manimx/cli.py:453-476`) — passá-la lá dá
`unrecognized arguments`.

### 6.2 O `.log` só sobrevive quando a compilação FALHOU

**[FONTE]** `tex_file_writing.py:70-72` e `:269-282`:

```python
svg_file = convert_to_svg(dvi_file, tex_template.output_format)
if not config["no_latex_cleanup"]:
    delete_nonsvg_files()          # apaga TUDO que não é .svg/.tex
```

Como `compile_tex` **levanta antes** disso quando o LaTeX falha, o `.log` de uma
compilação quebrada fica no disco; o de uma compilação bem-sucedida é apagado.
Ou seja: `ls media/Tex/*.log` listando arquivos é, por si só, um sinal de que
houve falha (ou de que alguém usou `--no_latex_cleanup`).

### 6.3 A mensagem que culpa a versão errada

**[FONTE]** `tex_file_writing.py:246-263`: o `dvisvgm` é chamado com
`subprocess.run(command, stdout=subprocess.DEVNULL)` — **sem `check=`, sem
capturar o stderr**. Se o processo roda e falha, o Manim só vê que o `.svg` não
apareceu e levanta:

```
ValueError: Your installation does not support converting .dvi files to SVG.
Consider updating dvisvgm to at least version 2.4. …
```

**Essa mensagem culpa a versão do `dvisvgm` seja qual for a causa real.** Para
ver o erro de verdade, rode o comando à mão com o mesmo ambiente:

```bash
bin/manim -ql --no_latex_cleanup scenes/cena.py Cena   # deixa o .dvi no disco
source bin/manim-env.sh
dvisvgm --page=1 --no-fonts --verbosity=3 --output=/tmp/t.svg media/Tex/<hash>.dvi
```

### 6.4 `media/Tex` é compartilhado — e o Manim faz `unlink()` nele sem dó

**[FONTE]** `tex_file_writing.py:280-282`:

```python
for f in tex_dir.iterdir():
    if f.suffix not in file_suffix_whitelist:      # {".svg", ".tex"}
        f.unlink()
```

Ele varre o diretório **inteiro**, não os arquivos daquele render. Dois processos
Manim rodando ao mesmo tempo com o mesmo `tex_dir` apagam o `.dvi` um do outro no
meio do voo — e o sintoma é um `ValueError: latex error converting to dvi`
**intermitente**, que some quando você roda sozinho. A correção (isolar
`tex_dir`/`text_dir` por worker) é de **`manim-batch-pipeline`**.

### 6.5 Tabela de LaTeX

| Sintoma | Causa | Correção |
|---|---|---|
| `\i`, `\f`, `\n` sumiram do resultado | faltou raw string: o Python comeu a barra | `r"\int"` |
| `! Undefined control sequence` | pacote não instalado, ou macro digitada errada | leia o `.log` (§6.1); `TexTemplate().add_to_preamble(r"\usepackage{...}")` + `tlmgr install` |
| `TexTemplate does not support character '…'` | caractere fora do `inputenc` do template | template com `fontenc`/`babel` adequado — **`manim-text-latex`** |
| Fórmula sai como texto corrido | usou `Tex` onde queria `MathTex` | — |
| Chaves literais somem | `{{ }}` é sintaxe de **isolamento de substring do Manim**, não do LaTeX | separe: `{ {` |
| Erro fala de `dvisvgm` mas o `.dvi` existe | `dvisvgm` fora do PATH, **ou** rodou e falhou | §3.2 e §6.3 |
| Fórmula sai vazia/cortada e mexer no código não muda | `.svg` truncado em cache | `rm -rf media/Tex` (§5.4) |
| `latex error converting to dvi` **intermitente** | dois renders dividindo `media/Tex` | §6.4 → `manim-batch-pipeline` |
| Cada render demora 20 s a mais | cada string nova compila um documento inteiro | reaproveite mobjects; use `Text` quando não for matemática |

---

## 7. A saída: o arquivo que não aparece

### 7.1 Nunca adivinhe o caminho — leia o JSON

```bash
bin/mx render scenes/cena.py Cena -q h --json 2>/dev/null \
  | python3 -c "import json,sys; r=json.load(sys.stdin)[0]; print(r['output_file'] or r['image_file'])"
```

O padrão é `<media-dir>/videos/<módulo>/<altura>p<fps>/<Cena>.mp4`, com `<módulo>`
= *stem* do arquivo. `-r` mexe nele (`-q l -r 1280x720` grava em `720p15`).
Detalhes de formato, seções e API programática: **`manim-render-api`**.

### 7.2 A árvore de decisão do `output_file: null`

```
output_file é null?
├─ image_file preenchido?
│  ├─ SIM → você pediu PNG, ou a cena não tem nenhum self.play (§4.4).
│  │        --format png e -s DESLIGAM o mp4:
│  │        [FONTE] _config/utils.py:807-808  → if save_last_frame: write_to_movie = False
│  │        [FONTE] utils/file_ops.py:110-118 → is_png_format() vence write_to_movie
│  └─ NÃO  → nenhum arquivo saiu.
│            ├─ num_animations > 0 → TODAS as animações foram puladas (§4.4):
│            │  `-n` fora da faixa, ou toda seção com skip_animations=True
│            └─ renderer == "opengl" → falta write_to_movie
│               [FONTE] _config/utils.py:855-857 — com --renderer=opengl e
│               --write_to_movie ausente na CLI, o Manim zera write_to_movie.
│               O `mx render` já injeta (manimx/render.py:231-232); o CLI cru não.
└─ preenchido → o arquivo existe. Se o CONTEÚDO está errado, vá para §5 e §10.
```

### 7.3 Tabela de saída

| Sintoma | Causa | Correção |
|---|---|---|
| "não acho o arquivo" | o caminho depende de `media_dir` + módulo + qualidade + `-r` | `--json` e leia `output_file` / `image_file` |
| `--format png` e `output_file` é `null` | em PNG o campo é **`image_file`** | leia os dois campos, sempre |
| `-s` gerou PNG e nenhum mp4 | `save_last_frame` desliga `write_to_movie` | escolha um; para os dois, dois renders |
| `--renderer=opengl` não gera arquivo | falta `write_to_movie` | `bin/mx render --renderer opengl` (já injeta) |
| Transparência não funciona | saiu `.mp4`; alfa exige `.mov`+`qtrle` (ou `.webm`+VP9) | `bin/mx render -t`; decisão de alfa é **`manim-color-theming`** |
| Último frame cortado / pôster em branco | a cena termina junto com a animação, ou termina em fade-out | `self.wait(0.3)` no fim, e **nunca** feche em `FadeOut` se o último frame vira pôster **[DECK]** |
| GIF gigante | GIF com paleta em 1080p60 | `--format gif -q m`, menos duração — o filtergraph é fixo (**`manim-gpu-encoding`**) |
| Vídeo com metade da duração esperada | metade das animações veio do cache com estado velho | §5 |
| Só saiu uma parte do vídeo | `-n a,b` ainda ativo, ou `EndSceneEarlyException` | §9.2 |

---

## 8. Trava, pendura, come memória

| Sintoma | Causa | Correção |
|---|---|---|
| O processo termina o render e **não sai** | um worker de encode não-daemon esperando na fila | é bug de caminho de exceção; a 0.21 já sela em `abort_encode_jobs` **[FONTE]** `scene_file_writer.py:729-758`. Se acontecer, capture o traceback com `bin/mx -v` |
| Abre uma janela e para | `-p/--preview` ou `--enable_gui` **[FONTE]** `cli/render/ease_of_access_options.py:19-27` | não use no automático; `manim.cfg` já tem `preview = False` |
| `mx scenes` "trava" ou faz coisas estranhas | **`mx scenes` EXECUTA o arquivo** (`manimx/render.py:136`) | nada no nível do módulo pode abrir arquivo, fazer rede ou instanciar mobject pesado |
| Memória explode em 4K | 8 GiB de VRAM; RGBA 3840×2160 = ~33 MB **por frame na fila** | `encoder_queue_size` menor, ou renderize 4K em `cairo`, ou entregue 1080p — **`manim-gpu-encoding`** |
| Vários renders paralelos falham juntos | teto de sessões NVENC da GPU | conta em **sessões**, não em workers: **`manim-gpu-encoding`** §7 é o dono; lote é **`manim-batch-pipeline`** |
| Render "está lento" e a GPU está ociosa | a cena é limitada por **geometria/rasterização**, não por encoding | trocar codec não ajuda; meça — **`manim-gpu-encoding`**; custo de curvas e `always_redraw`: **`manim-performance-cache`** |
| Cada `play` demora e o log não anda | um updater caro rodando 60×/s, ou `always_redraw` reconstruindo tudo | **`manim-updaters-valuetracker`** |

Um aviso do próprio Manim que é fácil não ver **[FONTE]** `scene/scene.py:1130-1137`:

```
The original run_time of Scene.play(), 0.01 seconds, is too short for the current
frame rate of 60 FPS. Rendering with the shortest possible run_time of 0.0167 …
```

`run_time` menor que um frame é **silenciosamente elevado**. Se o seu ritmo não
bate com a conta, é isto. Ritmo em profundidade: **`manim-composicao-ritmo`**.

---

## 9. Bissecção — cinco eixos, um de cada vez

A regra que faz a bissecção funcionar: **mude um eixo por vez e anote o
resultado.** Duas mudanças simultâneas transformam a próxima medição em ruído.

### 9.1 Eixo ambiente — o problema é meu ou da máquina?

```bash
bin/mx doctor --json | python3 -c "
import json,sys
[print('FALHOU', c['check'], c['detail']) for c in json.load(sys.stdin)['checks'] if not c['ok']]"
bin/mx render scenes/exemplos.py --all -q l --format png   # cenas testadas do repo
```

Se `scenes/exemplos.py` também falha, o problema **não é a sua cena**.

### 9.2 Eixo tempo — qual `play` quebra?

**[FONTE]** `manim/renderer/cairo_renderer.py:245-267`:

```python
if config.from_animation_number > 0 and self.num_plays < config.from_animation_number:
    self.skip_animations = True
if config.upto_animation_number >= 0 and self.num_plays > config.upto_animation_number:
    self.skip_animations = True
    raise EndSceneEarlyException()
```

Três coisas que essa leitura entrega e que mudam como se usa o `-n`:

1. **`skip_animations` não pula a lógica** — a animação é computada e o estado
   avança; só não se escreve frame. Por isso o estado nunca diverge, e por isso
   `-n 5,5` ainda paga o custo de construir tudo até a 5.
2. **O limite superior levanta `EndSceneEarlyException`**, capturada em
   `Scene.render` (`scene/scene.py:259-261`). Logo, tudo que vem depois no
   `construct` **não roda** — inclusive um `raise` que você estava caçando.
3. **`-s` (`--save_last_frame`)** seta `skip_animations = True` para **todas**
   (`cairo_renderer.py:254-255`) — é por isso que ele é rápido e ainda assim
   executa o `construct` inteiro. **Correção:** uma versão anterior desta linha
   dizia "`--format png`/`-s`". O teste no fonte é
   `if config["save_last_frame"]`, e `save_last_frame` só é ligado por `-s`
   (`cli/render/render_options.py:129`); nada no caminho de `--format` o toca.
   `--format png` **sozinho** renderiza a sequência inteira de PNGs, um por
   frame — é o comportamento que `manim-render-api` §5.4 documenta, e a razão de
   `bin/manim --format png` encher `media/images/`. O atalho de um frame só é o
   `mx render --format png`, que passa `-s` por baixo.

**E a armadilha de contagem, que faz todo mundo errar o índice na primeira
tentativa: `self.wait()` CONTA como animação.** **[FONTE]**
`manim/scene/scene.py`, `Scene.wait` é literalmente
`self.play(Wait(run_time=duration, stop_condition=…, frozen_frame=…))` — e
`Scene.pause` é `wait(frozen_frame=True)`. Quem conta só os `self.play` do
`construct` erra a numeração por um a cada `wait`. Conte os dois, na ordem,
começando do **zero**.

```bash
bin/manim -ql -n 0,3  scenes/cena.py Cena     # renderiza as animações 0,1,2,3 e PARA
bin/manim -ql -n 4,7  scenes/cena.py Cena     # pula 0-3 (mas as executa), grava 4-7
bin/manim -ql -n 6,6  scenes/cena.py Cena     # UMA animação só
bin/manim -ql -n 4    scenes/cena.py Cena     # da 4 até o fim
```

Os defaults, para entender os limites **[FONTE]** `_config/default.cfg:70,73`:
`from_animation_number = 0` e `upto_animation_number = -1`. Os testes são
`from > 0` e `upto >= 0` (`cairo_renderer.py:257-267`), ou seja: 0 desliga o
limite de baixo e −1 desliga o de cima. Aceita `start`, `start,end`, `start;end`
e `start-end` (`cli/render/render_options.py:20-25`).

`-n` é do CLI cru. O `mx render` não expõe (`manimx/cli.py:453-476`) — pela API
Python, `render_scene(..., extra={"from_animation_number": 4, "upto_animation_number": 7})`
(as duas são chaves válidas de `ManimConfig`, `_config/utils.py:279, 310`).

### 9.3 Eixo espaço — que mobject quebra?

```python
class Debug(Scene):
    def construct(self):
        self.add(NumberPlane())                      # a grade de referência
        self.add(Dot(ORIGIN, color=RED))             # a origem
        eq = MathTex(r"a^2 + b^2 = c^2", color=BLACK)
        self.add(eq, index_labels(eq[0], color=BLACK, background_stroke_color=WHITE))
```

Três notas conferidas:

- `index_labels(mobject, label_height=0.15, background_stroke_width=5, background_stroke_color=BLACK, **kwargs)`
  **[FONTE]** `api/manim-ce-index.tsv`, categoria `utils/other`.
- Ele numera os **submobjects diretos**. Num `MathTex` de várias partes, `eq`
  são as partes e `eq[0]` são os glifos da primeira. **[FONTE]**
  `utils/debug.py`, `for n, submob in enumerate(mobject)`.
- Ele constrói `Integer`, que é `DecimalNumber(mob_class=MathTex)` — ou seja,
  **`index_labels` exige LaTeX funcionando**, e nasce **branco** (default de
  `VMobject`). Em fundo claro passe `color=BLACK, background_stroke_color=WHITE`.

Duas réguas baratas para "isso cabe na tela?":

```python
print(mob.get_corner(UL), mob.get_corner(DR))
print(config.frame_x_radius, config.frame_y_radius)   # 7.1111, 4.0
print(mob.is_off_screen())
```

**Cuidado com `is_off_screen()`**: **[FONTE]** `mobject/mobject.py` — ele só
devolve `True` quando o mobject está **inteiramente** fora. Um elemento
**cortado pela borda** devolve `False`. Para "cabe?", compare os cantos.
Enquadramento é de **`manim-layout-posicionamento`**.

### 9.4 Eixo config — é a minha cena ou a configuração?

```python
from manim import tempconfig
with tempconfig({"disable_caching": True, "quality": "low_quality"}):
    ...
```

Ou pelo lado de fora, mudando **uma** coisa por vez:

```bash
bin/mx render scenes/cena.py Cena -q l                     # base
bin/mx render scenes/cena.py Cena -q l --no-cache          # +cache
bin/mx render scenes/cena.py Cena -q l --codec x264        # +codec
bin/mx render scenes/cena.py Cena -q l --renderer opengl   # +renderer
```

E lembre que **o `cwd` é configuração**: rodar de fora da raiz troca
`max_files_cached`, `max_inflight_encoders` e os diretórios de saída, calado
(`manim-project` §5).

### 9.5 Eixo redução — a cena mínima

Corte pela metade até o erro sumir. Uma cena mínima que reproduz o defeito é o
único artefato que sobrevive à sessão: ela vira teste, vira relatório de bug, e
prova que a causa é a que você acha que é.

```python
from manim import *
class Min(Scene):
    def construct(self):
        m = Circle(color=BLACK)
        self.play(Create(m))
```

### 9.6 A ordem que economiza tempo

```
1. doctor            → ambiente
2. mx scenes         → o arquivo importa?
3. --format png      → construct roda inteiro?
4. -n a,b            → qual play?
5. --no-cache        → é cache?
6. cena mínima       → é a lógica
```

Passar do 3 direto para o 6 é o erro comum: você reescreve a cena inteira para
descobrir que era cache.

---

## 10. Renderizou e não olhou: não terminou

O ciclo que funciona, e ele não é opcional:

```
escrever → renderizar rápido (-q l --format png) → OLHAR O PNG → corrigir → render final
```

**[DECK]** Numa investigação real de um deck de aulas, **três defeitos apareceram
só ao olhar a imagem; nenhum deu erro no terminal.** A lista do que o terminal
nunca conta:

- texto branco em fundo branco (§4.5);
- elemento cortado pela borda (`is_off_screen()` devolve `False`, §9.3);
- dois textos sobrepostos;
- fonte trocada por outra em silêncio (§4.6);
- barra estourando o eixo, rótulo atravessado pela grade;
- pôster/PDF em branco porque o último frame é um fade-out.

```bash
bin/mx render scenes/cena.py Cena -q l --format png --json 2>/dev/null \
  | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['image_file'])"
# → abra esse arquivo com a ferramenta Read do agente e OLHE
```

E uma armadilha operacional do ciclo **[DECK]**: se o preview rápido escreve nos
**mesmos caminhos** da entrega, terminar de iterar e esquecer o render final
deixa 720p30 no lugar do 1080p60 — visivelmente mole no projetor e invisível no
terminal. Ou separe os diretórios, ou confira antes de entregar.

**Verificação profunda do resultado — comparar frames, medir contraste, medir
emenda entre partes, checar cobertura de tinta do pôster — é da skill
`manim-verificacao-visual`.** Aqui a regra é só uma: *olhe*.

---

## 11. Diagnósticos que mentem

Três formas de escrever um comando de diagnóstico que devolve "ok" quando não
está ok. As três já custaram tempo neste projeto.

**1. `comando | grep x || echo ok`** — o `||` cobre a falha do **pipeline
inteiro**. Se o `comando` explodir, o `grep` não acha nada, e você imprime "ok"
para um comando que morreu. **Materialize antes de filtrar:**

```bash
bin/mx render … --json > /tmp/r.json 2>/tmp/r.err || { echo "FALHOU"; cat /tmp/r.err; exit 1; }
[ -s /tmp/r.json ] || { echo "stdout vazio → falhou no import (§2.1)"; cat /tmp/r.err; exit 1; }
python3 -c "
import json,sys
rs=json.load(open('/tmp/r.json'))
bad=[r for r in rs if not r['success'] or not (r['output_file'] or r['image_file'])]
sys.exit(1 if bad else 0)" && echo ok
```

(`_out` usa `json.dumps(..., indent=2)` — `manimx/cli.py`, então `grep '\"success\": true'`
até funciona; mas ele não distingue `success:true` **sem arquivo**, que é
exatamente o caso mudo da §4.4.)

**2. `produtor | grep -q padrao` sob `set -o pipefail`** — o `grep -q` sai no
primeiro acerto, o produtor morre de SIGPIPE, e o `pipefail` transforma isso em
falha do pipeline. **[FONTE]** `bin/manim-env.sh:39-48` documenta exatamente esse
caso (foi o que fez a detecção de NVIDIA dar falso-negativo). Capture primeiro,
teste depois:

```bash
listing="$(nvidia-smi -L 2>/dev/null)" || return 1
case "$listing" in *"GPU 0"*) : ;; esac
```

**3. `mx find … | grep`** — `mx find` sem resultado **não imprime nada e sai 1**
(`manim-project` §2). Um grep displicente lê isso como "não existe", quando muitas
vezes é só o termo em português (o índice é em inglês).

---

## 12. Índice reverso — sintoma → seção

| O que você digitou / viu | Vá para |
|---|---|
| "o render falhou" / traceback | §2.1, §9 |
| `JSONDecodeError` ao parsear o `--json` | §2.1 — falhou no import, stdout vazio |
| "não acho o mp4" | §7.2 |
| "o vídeo saiu vazio / não saiu nada" | §4.4, §7.2 |
| "mudei o código e o vídeo é o mesmo" | §5 |
| "mudei o preço/dado e o vídeo não mudou" | §5.2 → `--no-cache` |
| "usei `--flush_cache` e continuou igual" | §5.3 — ele limpa **depois** |
| "a animação não acontece" | §4.1, §4.2, §4.3 |
| "sumiu o texto / saiu tudo branco" | §4.5, §4.6, §4.10 |
| "cortou na borda" | §9.3 (e `is_off_screen` mente) |
| `AttributeError: X object has no attribute 'y'` | §4.1 se você escreveu `get_y`; senão **`manim-api-discovery`** |
| `TypeError: unexpected keyword argument` | **`manim-api-discovery`** |
| `TypeError: Only values of type VMobject can be added…` | pôs `ImageMobject` num `VGroup` → use `Group`; **`manim-mobjects`** |
| `TypeError: Animation only works on Mobjects` | passou algo que não é Mobject para uma animação (`animation/animation.py:187`) |
| `TypeError: Unexpected argument … passed to Scene.play()` | `self.play(Circle())` — Mobject cru onde se espera animação. A **causa encadeada** (`__cause__`) é `Object … cannot be converted to an animation` (`animation/animation.py:581`); leia o traceback inteiro (`scene/scene.py:993-1004`) |
| `TypeError: Passing Mobject methods to Scene.play is no longer supported` | `self.play(mob.shift, UP)` da API velha → `mob.animate.shift(UP)` (`scene/scene.py:997-999`) |
| `ValueError: Called Scene.play with no animations` | `self.play()` vazio (`scene/scene.py:1318`) |
| `ValueError: Scene.play() has a run_time of 0 <= 0 seconds which Manim cannot render` | `run_time=0` (`scene/scene.py:1119-1124`) — use `self.wait` |
| `ValueError: Could not find <mob> in scene` | `Scene.replace` num mobject que não está lá — em geral porque um `Transform` já o substituiu (§4.3) (`scene/scene.py:643`) |
| `ValueError: Specified mobjects cannot be None` | `Scene.replace(None, …)` — quase sempre um `_pega_peca()` que devolveu `None` (`scene/scene.py:600-601`) |
| `Exception: Trying to restore without having saved` | `Restore`/`restore()` sem `save_state()` antes (`mobject.py:2164`) |
| `Exception: Cannot call Mobject.<m> for a Mobject with no points` | mobject vazio (`VGroup()` sem filhos, `Text("")`) (`mobject.py:3336-3341`) |
| `ValueError: Color X not found` | faltou o `#`. Três dígitos funcionam (`manim-project` §10) |
| `FileNotFoundError` ao passar `-c COR` | `-c` é `--config_file`; `--background_color` foi removido da CLI |
| `LaTeX Error` / `latex error converting to dvi` | §6 |
| `Your installation does not support converting … to SVG` | §6.3 — a mensagem culpa a versão, quase nunca é ela |
| `avcodec_open2(...) returned 22` | opção inválida para o codec — **`manim-gpu-encoding`** |
| "travou / não sai / come memória" | §8 |
| "está lento" | §8 e **`manim-gpu-encoding`** / **`manim-performance-cache`** |
| "funciona sozinho, quebra em paralelo" | §6.4 → **`manim-batch-pipeline`** |
| "renderizou mas está feio" | §10 → **`manim-verificacao-visual`** |
| `python cena.py` não fez nada | §4.11 |

---

## 13. Onde esta skill para

Esta skill diagnostica **uma falha concreta**. Ela não ensina o assunto. Quando o
diagnóstico terminar, a correção quase sempre mora em outro lugar:

| Depois de diagnosticar… | Vá para |
|---|---|
| nome, assinatura ou kwarg inexistente | `manim-api-discovery` |
| escolher qualidade/formato, API de render, seções | `manim-render-api` |
| codec, NVENC, "está lento", benchmark | `manim-gpu-encoding` |
| lote, paralelismo, isolamento de `tex_dir`, CI | `manim-batch-pipeline` |
| conferir o resultado frame a frame, contraste, comparar imagens | `manim-verificacao-visual` |
| cor, tema, fundo, alfa, "sumiu no branco" como decisão de projeto | `manim-color-theming` |
| texto, fonte, LaTeX, `t2c`, nitidez de glifo | `manim-text-latex` |
| forma, grupo, `VGroup` × `Group`, submobject | `manim-mobjects` |
| "cabe na tela?", margem, 9:16 | `manim-layout-posicionamento` |
| classe de animação, `Transform` × `ReplacementTransform`, `.animate` | `manim-animations` |
| `run_time`, `rate_func`, `lag_ratio`, ritmo | `manim-composicao-ritmo` |
| updater, `ValueTracker`, `always_redraw` | `manim-updaters-valuetracker` |
| cena em partes, `next_section`, emenda entre partes | `manim-presentation-parts` |
| custo de rasterizar, cache em profundidade, `max_files_cached` | `manim-performance-cache` |
| ManimGL / `manimlib` | `manimgl-3b1b` |
| onde estão as coisas, wrappers, `cwd`, ficha da máquina | `manim-project` |

**Desempate com `manim-api-discovery`**, porque os gatilhos colidem de verdade:

| O erro é sobre… | Skill |
|---|---|
| **um nome** (`AttributeError`, `ImportError: cannot import name`, `TypeError: unexpected keyword argument`) | `manim-api-discovery` |
| **um comportamento** (render falhou, arquivo não saiu, resultado errado, ambiente, codec) | **esta** |

Regra curta: *"esse nome existe?"* é `api-discovery`. *"por que isso aconteceu?"*
é aqui.

---

## 14. Limpar tudo e recomeçar

Do menos ao mais destrutivo. **Não pule direto para o último** — apagar
`media/Tex` custa uma recompilação inteira de LaTeX no próximo render.

```bash
# 1. ignorar o cache de partial movies nesta execução (não apaga nada)
bin/mx render scenes/cena.py Cena -q l --no-cache

# 2. apagar os partial movies de UMA cena
rm -rf media/videos/cena/480p15/partial_movie_files/Cena

# 3. apagar todos os partial movies do projeto
rm -rf media/videos/*/*/partial_movie_files

# 4. apagar o cache de LaTeX e de texto (o mais caro de reconstruir)
rm -rf media/Tex media/texts

# 5. terra arrasada
rm -rf media
```

---

## 15. O que ficou NÃO VERIFICADO nesta rodada

Escrito sob proibição de gastar CPU/GPU: **nenhum render, benchmark, `ffmpeg`,
navegador ou `mx bench` rodou.** As afirmações abaixo são leitura de código ou
testemunho de terceiros, e merecem uma medição antes de virarem certeza:

1. **[NV]** `mob.set_center(ORIGIN)` sombreando o método `center()` e causando
   `TypeError: 'numpy.ndarray' object is not callable` — o mecanismo está lido
   (`mobject.py:729-773`), o sintoma exato não foi reproduzido.
2. **[NV]** `PYTHONWARNINGS='default::DeprecationWarning'` reativando o aviso sob
   `mx render` — é comportamento padrão do interpretador, não testado aqui.
3. **[NV]** O `.svg` truncado por `kill -9` produzindo fórmula quebrada
   permanente. O curto-circuito `if svg_file.exists(): return` está lido
   (`tex_file_writing.py:60-62`); a truncagem em si não foi provocada.
4. **[NV]** A ordem de poda por `st_atime` degradada por `relatime` — o código
   está lido (`scene_file_writer.py:1069-1071`); as opções de montagem desta
   máquina não foram consultadas.
5. **[DECK]** Os 4 px de deslocamento causados por elemento invisível na caixa
   delimitadora, e os três defeitos que só apareceram ao olhar o PNG — medições
   do projeto consumidor `~/Projects/aulas`, em 2026-08-19, não reproduzidas.
6. **Pendência para o orquestrador:** `manim-project` §4.1 afirma que são **cinco**
   os checks fatais do `mx doctor`, incluindo `LaTeX → SVG (MathTex)`. Conferido
   em `manimx/cli.py:129-133`, esse check passa `fatal=False`; os fatais são
   **quatro**. Corrigido aqui (§3.1); a skill irmã precisa da mesma emenda.
7. **Pendência para o orquestrador:** quatro skills citadas neste arquivo ainda
   podem não existir no disco — `manim-verificacao-visual`,
   `manim-layout-posicionamento`, `manim-composicao-ritmo`,
   `manim-performance-cache`. Se alguma não chegar nesta onda, os ponteiros das
   seções §10, §7.3, §8 e §9.3 viram becos sem saída e devem cair para
   `manim-render-api` / `manim-mobjects` / `manim-animations` /
   `manim-gpu-encoding`.
8. **Correção interna que vale registrar:** a versão anterior desta skill dizia
   que "renderizou mas nada mudou" se resolve com `--no-cache` **ou**
   `bin/manim --flush_cache`. A segunda metade estava errada pelo motivo da
   §5.3 — o flush roda em `finish()`, depois do vídeo montado. Se você viu essa
   recomendação em outro lugar, é a versão velha.
