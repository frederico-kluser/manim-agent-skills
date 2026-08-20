---
name: manim-som-legendas
description: >-
  Áudio e legenda numa cena Manim: `Scene.add_sound`, `Scene.add_subcaption`,
  `Scene.play(subcaption=…)`, o arquivo `.srt` que sai ao lado do mp4, e as SEIS
  formas de o som sumir sem erro nenhum. Use SEMPRE que o pedido envolver som,
  áudio, música, narração, efeito sonoro, "bip", trilha, volume, legenda ou
  `.srt` dentro de uma cena: "põe um som quando a barra cresce", "adiciona uma
  trilha de fundo", "sincroniza o áudio com a animação", "o som ficou adiantado",
  "abaixa o volume da música quando entra a voz", "o mp4 saiu mudo", "renderizei
  de novo e o som sumiu", "o som não aparece no gif", "as seções saíram sem
  áudio", "não achou o arquivo de som", "gera as legendas", "quero um .srt",
  "onde foi parar o arquivo de legenda", "legenda em cima do vídeo", "dá para
  narrar isso?". Cobre a superfície inteira da API (2 métodos de `Scene`, 6 de
  `SceneFileWriter`, `get_full_sound_file_path`, `convert_audio`), a semântica
  REAL de `time_offset`/`gain`/`gain_to_background` conferida no fonte (o
  docstring do Manim erra em `time_offset`), a cadeia pydub+PyAV+srt com
  versões, a interação FATAL com `skip_animations` e com o cache de partial
  movies, a tabela container→codec de áudio, e um verificador de faixa de áudio
  em PyAV puro (sem ffprobe). NÃO use para escolher codec de VÍDEO, NVENC ou
  peso do arquivo (`manim-gpu-encoding`); nem para texto DESENHADO na tela, que
  é `Text`/`MarkupText` (`manim-text-latex`); nem para cortar a cena em partes
  para slide (`manim-presentation-parts`) ou a API genérica de seções
  (`manim-cenas-secoes`); nem para o cache de partial movies em si
  (`manim-performance-cache`); nem para `manim-voiceover` e outros plugins, que
  NÃO estão instalados nesta máquina (`manim-project`).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Som e legenda — a superfície inteira, e por que ela quase sempre some

O ManimCE tem **duas** portas públicas de áudio e legenda, e as duas são
métodos de `Scene`: `add_sound` e `add_subcaption` (mais o atalho
`play(subcaption=…)`). Não há mobject de áudio, não há flag de CLI, não há
waveform na tela, não há sintetizador de voz. O que existe é uma trilha única
por cena, montada em memória com **pydub**, e um `.srt` de texto ao lado do
mp4.

E o assunto tem uma peculiaridade que decide tudo o resto: **som no Manim falha
em silêncio**. Não existe exceção para "seu áudio foi descartado" — existem seis
caminhos diferentes que jogam a trilha fora sem escrever uma linha no log. Esta
skill começa pela API, mas a seção que você vai reler é a §3.

## Procedência do que está escrito aqui

Três marcadores, válidos para o arquivo inteiro:

- **[FONTE]** — conferido lendo o ManimCE 0.21.0 instalado em
  `.venv/lib/python3.12/site-packages/manim/`, o ManimGL 1.7.2 em
  `.venv-gl/…/manimlib/`, as dependências em `site-packages/{pydub,srt}`, ou o
  índice estático de `api/`. Afirmação forte, com arquivo e linha.
- **[LEITURA]** — dedução minha a partir do fonte, sem execução. Sólida, mas é
  raciocínio, não observação.
- **[NÃO VERIFICADO]** — não dá para afirmar sem renderizar. Está listado
  inteiro na §13, e sinalizado no lugar onde aparece.

**Nada foi renderizado nesta sessão.** Nenhum `mx render`, nenhum `ffmpeg`,
nenhum `ffprobe`, nenhuma GPU. Os únicos comandos que rodaram foram `grep`,
`awk`, `sed` e três `import` de Python (`pydub`, `srt`, `av`) para ler
assinaturas. Todo exemplo de código deste arquivo foi escrito contra assinatura
conferida — e **nenhum foi executado**.

## Cartão de referência — o sintoma manda na seção

| O que aconteceu / o que você quer | Onde ler |
|---|---|
| "quero pôr um som na cena" — por onde começo | §0 → §2 → §7.1 |
| **o mp4 saiu mudo e não deu erro** | **§3** — a tabela das seis causas |
| **renderizei de novo e o som sumiu** | **§3.2** — cache hit. É esta, quase sempre |
| o som está adiantado/atrasado | §2.2 — `time_offset` não é o que o docstring diz |
| quero abaixar a música quando entra o efeito | §2.4 — `gain_to_background` |
| "não achou o arquivo de som" / `OSError` | §2.5 — os 4 caminhos e o `cwd` |
| mp3 / ogg / m4a servem? e `.raw`? | §2.6 — e o `.raw` **quebra** |
| o gif saiu sem áudio | §3.4 |
| `--save_sections` deu vídeos mudos | §3.5 |
| o áudio acaba antes do vídeo | §4.2 e §4.4 (a receita de padding) |
| dois sons ao mesmo tempo, mixagem, volume | §4.5 |
| quero legenda | §5 |
| cadê o `.srt`? | §5.2 — e por que às vezes ele não é escrito |
| a legenda tem que APARECER no vídeo | §5.6 — não é este arquivo |
| que codec de áudio saiu no meu mp4/webm/mov | §6 |
| conferir se o arquivo tem faixa de áudio, sem `ffprobe` | §8 |
| "devo mesmo pôr som?" (aula, slide, deck) | §9 |
| estou traduzindo de ManimGL/3b1b | §10 |
| erro/traceback com áudio | §11 |
| isso é meu ou de outra skill? | §12 |

---

## 0. Antes da API: você quer mesmo som embutido?

Três perguntas, nesta ordem. Elas economizam a maior parte do trabalho.

1. **O vídeo vai ser narrado ao vivo?** Se alguém vai falar por cima — aula,
   palestra, slide —, áudio embutido **briga** com a fala. Ver §9: no deck
   consumidor `~/Projects/aulas` os 77 vídeos são mudos de propósito, e o
   player ainda põe `muted` por cima.
2. **O som é conteúdo ou é enfeite?** Efeito sonoro que marca um beat é
   conteúdo (a plateia aprende a esperar o clique). Música de fundo genérica é
   peso de arquivo e risco de licença.
3. **Você controla o player?** Se o destino é um `<video muted>` de um deck, um
   GIF, ou um PNG de pôster, o áudio nunca vai tocar. Ver §3.4 e §3.3.

Se as três respostas mandarem seguir, siga. O resto do arquivo é como fazer
direito.

---

## 1. A superfície inteira da API

Levantada do índice estático (`api/manim-ce-index.tsv`,
`api/manim-ce-methods.tsv`) e conferida no fonte. **Isto é tudo o que existe** —
não há mais nada de áudio ou legenda no ManimCE 0.21.0.

### 1.1 As portas públicas (o que você chama de dentro do `construct`)

**[FONTE]** — assinaturas exatas do índice. Aparecem nas **7** classes de `Scene`
do índice — `Scene`, `ThreeDScene`, `SpecialThreeDScene`, `MovingCameraScene`,
`ZoomedScene`, `LinearTransformationScene`, `VectorScene` — e nas 6 últimas com
`inherited=1`: **nenhuma sobrescreve**, o comportamento é o mesmo em todas.
Qual `Scene` herdar é assunto de `manim-cenas-secoes`; para som, tanto faz.

```python
Scene.add_sound(self, sound_file: str,
                time_offset: float = 0,
                gain: float | None = None,
                **kwargs: Any) -> None

Scene.add_subcaption(self, content: str,
                     duration: float = 1,
                     offset: float = 0) -> None

Scene.play(self, *args: Animation | Mobject | _AnimationBuilder,
           subcaption: str | None = None,
           subcaption_duration: float | None = None,
           subcaption_offset: float = 0,
           **kwargs: Any) -> None

Scene.time -> float          # property; devolve self.renderer.time (scene.py:231)
```

`Scene.time` não é decoração: é o relógio contra o qual **as duas** portas
marcam posição. Toda a §4 e a §5.1 são aritmética em cima dele.

### 1.2 A camada de baixo (`SceneFileWriter`) — quando a porta pública não basta

**[FONTE]** — os 6 membros de áudio + 1 de legenda, com assinatura do índice:

```python
SceneFileWriter.init_audio(self) -> None                      # :417
SceneFileWriter.create_audio_segment(self) -> None            # :421
SceneFileWriter.add_audio_segment(self, new_segment: AudioSegment,
                                  time: float | None = None,
                                  gain_to_background: float | None = None) -> None   # :425
SceneFileWriter.add_sound(self, sound_file: StrPath,
                          time: float | None = None,
                          gain: float | None = None,
                          **kwargs: Any) -> None              # :468
SceneFileWriter.combine_to_movie(self) -> None                # :932  (faz a junção do áudio)
SceneFileWriter.write_subcaption_file(self) -> None           # :1092
```

Atributos que essas funções mantêm, e que valem para depurar:

| Atributo | Nasce em | O que é |
|---|---|---|
| `includes_sound: bool` | `init_audio`, chamado no `__init__` (`:239`) | `False` até o primeiro `add_audio_segment`. **É o interruptor** de todo o bloco de mux do §6 |
| `audio_segment: AudioSegment` | `create_audio_segment` (`:421`) | a trilha inteira da cena, em memória. Ver §4.1 — ela **não nasce vazia** |
| `subcaptions: list[srt.Subtitle]` | `__init__` (`:242`) | a lista de legendas, na ordem em que foram adicionadas |

**Repare na diferença de nome que já custou tempo a alguém:** o parâmetro de
posição chama-se **`time_offset`** em `Scene.add_sound` e **`time`** em
`SceneFileWriter.add_sound` — e eles **não significam a mesma coisa**.
`Scene.add_sound` faz `time = self.time + time_offset` (`scene.py:1804`); o do
writer é o instante ABSOLUTO na trilha. Ao ler um traceback, saiba qual é qual.

### 1.3 Onde o arquivo é procurado

**[FONTE]** — `manim/utils/sounds.py`, o módulo inteiro tem uma função:

```python
get_full_sound_file_path(sound_file_name: StrPath) -> Path
    # = seek_full_path_from_defaults(sound_file_name,
    #                                default_dir=config.get_dir("assets_dir"),
    #                                extensions=[".wav", ".mp3"])
```

E `seek_full_path_from_defaults` (`utils/file_ops.py:167-181`) monta esta lista
e devolve **o primeiro que existir**:

1. `Path(sound_file).expanduser()` — literalmente o que você passou, relativo ao
   **cwd do processo**;
2. `<assets_dir>/<nome>`;
3. `<assets_dir>/<nome>.wav`;
4. `<assets_dir>/<nome>.mp3`.

Falhando as quatro, levanta **`OSError`** (não `FileNotFoundError`) com a
mensagem `From: {cwd}, could not find …` — repare que ela imprime o `cwd`, o
que é exatamente o que você precisa saber.

**[FONTE]** `assets_dir` tem default `./` (`_config/default.cfg:86`), é
**config, não flag**: existe em `manim.cfg` e como `config.assets_dir = …`, mas
**não há opção de CLI** para ele (grep em `manim/cli/` não devolve nada;
o comentário `# --assets_dir` no `default.cfg` está obsoleto). E o `manim.cfg`
deste projeto **não o define** — ou seja, `assets_dir` é `./`, e "./" é o
**diretório de onde você chamou o comando**, não a pasta do `.py`. É o mesmo
`cwd` que `manim-project §5` documenta como parte da configuração.

### 1.4 A cadeia de dependências, com versões

**[FONTE]** — instaladas neste `.venv`:

| Pacote | Versão | Faz o quê |
|---|---|---|
| `pydub` | **0.25.1** | **a mixagem inteira**. `AudioSegment.silent/from_file/apply_gain/overlay/append/export` |
| `av` (PyAV) | **18.1.0** | decodificação de qualquer formato que não seja wav/raw (`convert_audio`), e o mux final |
| `srt` | **3.5.3** | serializa a lista de `srt.Subtitle` no arquivo `.srt` |

Duas consequências que ninguém espera:

- **o Manim não chama o binário `ffmpeg` para áudio.** `convert_audio`
  (`scene_file_writer.py:77-91`) é PyAV puro, e o import do `pydub` vem
  embrulhado num `warnings.catch_warnings()` que silencia justamente o
  `RuntimeWarning` "ffmpeg or avconv not found" (`:23-32`). Nesta máquina o
  ffmpeg até existe (`/usr/bin/ffmpeg`), mas o caminho normal não o usa;
- **`pydub` só dispensa o ffmpeg para `.wav` e `.raw`/`.pcm`**
  (`pydub/audio_segment.py:667-696`); qualquer outra coisa cai num
  `subprocess` de `ffmpeg`. É por isso que o Manim pré-converte com PyAV antes
  de entregar ao pydub. Ver §2.6.

Nota de portabilidade **[LEITURA]**: `pydub` importa `audioop`
(`pydub/utils.py:14`), removido da stdlib no Python 3.13. Este venv é 3.12 e
funciona; num 3.13 sem o pacote `audioop-lts` a mixagem quebra no import.

### 1.5 O que NÃO existe — e o que costumam pedir no lugar

Vale saber para não caçar:

| Não existe | O que costuma ser pedido no lugar |
|---|---|
| flag de CLI para som ou legenda | nada. É tudo código na cena (`grep` em `manim/cli/` não devolve `sound`, `audio`, `subcaption` nem `assets_dir`) |
| mobject de áudio, waveform, VU meter | desenhe com `Axes`/`Line` (`manim-graphs-plots`) a partir de um array — o Manim não te dá o array |
| tocar som durante o `--preview` | **[FONTE]** o ManimGL tem `manimlib.utils.sounds.play_sound()` (aplay/afplay/powershell); **o CE não tem nada equivalente**. Ver §10 |
| narração sintetizada / TTS | é o plugin `manim-voiceover`. **`manim-project` §13.7 registra que plugins de terceiros NÃO estão instalados nesta máquina** — não presuma que estão |
| legenda queimada no vídeo | `.srt` é arquivo separado. Para texto NA tela é `Text` (§5.6) |
| corte/seek dentro do arquivo de som | não há parâmetro. Fatie com pydub e use `add_audio_segment` (§7.3) |

---

## 2. `add_sound` — o que cada parâmetro realmente faz

### 2.1 O corpo inteiro, que cabe em quatro linhas

**[FONTE]** `scene.py:1802-1805`, depois de ~40 linhas de docstring:

```python
if self.renderer.skip_animations:
    return
time = self.time + time_offset
self.renderer.file_writer.add_sound(sound_file, time, gain, **kwargs)
```

Está tudo aqui. As três linhas geram, respectivamente: a §3 inteira, a §2.2 e a
§2.4.

### 2.2 `time_offset` é posição na LINHA DO TEMPO — o docstring do Manim erra

O docstring diz, literalmente:

> `time_offset` — The offset in the sound file after which the sound can be
> played.

**Isso está errado.** **[FONTE]** o código é `time = self.time + time_offset`:
`time_offset` é somado ao **relógio da cena**, não é um seek dentro do arquivo.
Não existe seek em `add_sound`; para tocar do segundo 3 de um arquivo você fatia
com pydub (§7.3).

O que isso significa na prática:

```python
self.play(Create(circulo))        # cena vai de 0 s a 1 s
self.add_sound("clique.wav")      # cai em t = 1,0 s (o AGORA)
self.add_sound("clique.wav", -0.15)   # cai em t = 0,85 s — ANTECIPA
self.add_sound("clique.wav", 0.40)    # cai em t = 1,40 s — no meio do próximo play
```

Três consequências:

- **`time_offset` negativo é legítimo e é a ferramenta certa** para casar um som
  de impacto com o instante em que a coisa bate, quando o ataque do arquivo tem
  uma latência de alguns quadros;
- **o tempo absoluto não pode ficar negativo.** `add_audio_segment` levanta
  `ValueError("Adding sound at timestamp < 0")` (`scene_file_writer.py:452-453`);
- **onde você põe a chamada no `construct` importa mais do que o offset.** Um
  `add_sound` antes do `self.play` marca o começo da animação; depois dele,
  marca o fim. Não há terceira opção sem aritmética.

### 2.3 `gain` é **decibel**, não multiplicador

**[FONTE]** `scene_file_writer.py:507-508` faz `new_segment.apply_gain(gain)`,
e `AudioSegment.apply_gain(volume_change)` do pydub interpreta o argumento em
**dB**. Logo:

| `gain=` | Efeito |
|---|---|
| `-6` | metade da amplitude (≈ metade do volume percebido por passo de 10) |
| `-20` | fundo discreto |
| `0` | **nada** — e não porque 0 dB seja neutro, mas porque a guarda é `if gain:`, um teste de *falsy*. `gain=0` e `gain=0.0` pulam a chamada |
| `+6` | dobra a amplitude — e **estoura** se o arquivo já vinha perto de 0 dBFS |

Não existe normalização automática. Se você está misturando arquivos de fontes
diferentes, normalize antes (§7.4) ou aceite que o mais alto manda.

### 2.4 `gain_to_background` — o ducking escondido dentro do `**kwargs`

Este é o parâmetro que ninguém acha, porque ele não aparece na assinatura de
`Scene.add_sound`. **[FONTE]** a cadeia é:

```
Scene.add_sound(..., **kwargs)
  → SceneFileWriter.add_sound(sound_file, time, gain, **kwargs)
    → SceneFileWriter.add_audio_segment(new_segment, time, **kwargs)
        assinatura: (new_segment, time=None, gain_to_background: float | None = None)
          → AudioSegment.overlay(..., gain_during_overlay=gain_to_background)
```

Ou seja, **isto funciona** e é a única forma de fazer ducking no ManimCE:

```python
self.add_sound("trilha.wav", gain=-20)                     # a música, baixa
self.play(Create(barra))
self.add_sound("locucao.wav", gain_to_background=-12)      # a fala abaixa a música em 12 dB
```

**[FONTE]** `pydub/audio_segment.py:1232-1237`: `gain_during_overlay` atenua
`seg1` — **tudo o que já está na trilha** — apenas durante a extensão do
segmento novo. Não é um envelope: é um degrau, sem attack nem release.
[NÃO VERIFICADO] como isso soa; o mecanismo é o que está lido.

Armadilha: `if gain_during_overlay:` também é *falsy* (`:1233`) — `0` não
atenua, o que aqui é o comportamento certo.

### 2.5 O arquivo não foi achado — a checklist de 30 segundos

O `OSError` traz o `cwd`. Compare com os quatro candidatos da §1.3:

```python
# na dúvida, prove antes de renderizar (import puro, sem render):
from manim import config
from manim.utils.sounds import get_full_sound_file_path
print(config.get_dir("assets_dir"))
print(get_full_sound_file_path("clique.wav"))    # levanta OSError se não achar
```

As três causas, em ordem de frequência **[LEITURA]**:

1. **o `cwd` não é a pasta do `.py`.** Caminho relativo em `add_sound` é
   relativo a de onde você CHAMOU o comando. A defesa é o caminho absoluto
   derivado do arquivo:
   ```python
   from pathlib import Path
   SONS = Path(__file__).resolve().parent / "sons"
   self.add_sound(str(SONS / "clique.wav"))
   ```
   (É o mesmo idioma que o `tema.py` do deck usa para achar `dados/precos.json`
   — ver `manim-tema-projeto`.)
2. **a extensão não é `.wav` nem `.mp3`.** Só essas duas são tentadas
   automaticamente; um `clique.ogg` precisa do nome completo;
3. **`assets_dir` foi configurado e você esqueceu.** `config.assets_dir` só é
   consultado no candidato 2-4.

### 2.6 Formatos: o que entra direto, o que custa, e o que **quebra**

**[FONTE]** `scene_file_writer.py:493-506`:

```python
file_path = get_full_sound_file_path(sound_file)
if file_path.suffix not in (".wav", ".raw"):
    with NamedTemporaryFile(suffix=".wav", delete=False) as wav_file_path:
        convert_audio(file_path, wav_file_path, "pcm_s16le")   # PyAV
        new_segment = AudioSegment.from_file(wav_file_path.name)
        logger.info(f"Automatically converted {file_path} to .wav")
    Path(wav_file_path.name).unlink()
else:
    new_segment = AudioSegment.from_file(file_path)
```

| Extensão | O que acontece |
|---|---|
| `.wav` (PCM 8/16/32 bits) | leitura direta pelo `wave` da stdlib. **O caminho barato** |
| `.mp3`, `.ogg`, `.m4a`, `.flac`, `.opus`… | decodificado inteiro para um `.wav` temporário via PyAV, **a cada chamada**. O próprio Manim deixou um `# TODO: figure out a way to cache the wav file generated` (`:498`). Chamar 12 vezes o mesmo mp3 = 12 decodificações |
| `.wav` que **não é PCM** (float32, 24 bits, ou wav com mp3 dentro) | **[FONTE]** cai no `except:` mudo de `pydub` (`audio_segment.py:677`) e vai para o caminho do `subprocess` de `ffmpeg`. Funciona nesta máquina (o ffmpeg está em `/usr/bin`), **falha calado onde não estiver** |
| `.raw` / `.pcm` | **QUEBRA.** **[FONTE]** `add_sound` deixa `.raw` passar direto para `AudioSegment.from_file(file_path)`, que exige `kwargs['sample_width']`, `['frame_rate']` e `['channels']` (`audio_segment.py:680-682`) — e o `add_sound` do Manim **não os repassa** (o `**kwargs` dele vai para `add_audio_segment`, não para `from_file`). Resultado: `KeyError: 'sample_width'`. [NÃO VERIFICADO por execução, mas os dois trechos de código não têm como se encontrar] |

**A recomendação que sai disso:** converta seus sons para **`.wav` PCM 16 bits**
uma vez, fora do Manim, e guarde assim no repositório. É o único formato que
percorre o caminho curto, é o único que não depende de o ffmpeg estar no PATH,
e é o único que não paga decodificação por chamada.

---

## 3. As SEIS formas de o som sumir sem erro nenhum

Esta é a seção que importa. Nenhum dos seis casos escreve aviso, warning ou
linha de log. O sintoma é sempre o mesmo: **mp4 mudo, exit code 0**.

| # | Causa | Onde **[FONTE]** | Sinal externo |
|---|---|---|---|
| 1 | seção com `skip_animations=True` | `cairo_renderer.py:253` | nenhum |
| 2 | **animação servida pelo CACHE** | `cairo_renderer.py:96` | a linha `Using cached data` no log — que ninguém lê como "perdi o áudio" |
| 3 | `-s` / `--save_last_frame` | `cairo_renderer.py:255-256` | não há mp4 nenhum |
| 4 | `--format png` / `--dry_run` | `scene_file_writer.py:615-631` | não há mp4 nenhum |
| 5 | `--format gif` | `scene_file_writer.py:961` | o gif existe e é mudo |
| 6 | `--save_sections` | `scene_file_writer.py:1048-1051` | o mp4 principal tem áudio; os das seções, não |

### 3.1 Seção pulada — e por que este caso é o correto

**[FONTE]** `Scene.add_sound` começa com `if self.renderer.skip_animations:
return` (`scene.py:1802`). Dentro de uma seção marcada
`next_section(..., skip_animations=True)`, a flag está ligada, e o `add_sound`
retorna sem fazer nada.

Isso é **desejável** no formato em partes (`manim-presentation-parts`): a parte
6 não deve carregar o áudio dos atos 1 a 5. Mas tem uma consequência que
surpreende:

> Numa cena cortada em N partes, **cada parte carrega só o som do próprio ato**.
> O áudio nunca é contínuo entre partes, porque cada mp4 é um render separado.
> Se o seu efeito sonoro atravessa a emenda, ele será cortado — e não há
> mecanismo que emende áudio como o §2.2 de `manim-presentation-parts` emenda
> vídeo.

Ou seja: **som + formato em partes só combinam se cada som couber inteiro dentro
de uma parte.** Trilha de fundo contínua é incompatível com o formato.

**A mesma flag, por dois outros caminhos.** `update_skipping_status`
(`cairo_renderer.py:245-266`) liga `skip_animations` em mais dois casos, e os
dois derrubam `add_sound` exatamente igual:

- **`-n a,b`** — `config.from_animation_number > 0 and self.num_plays < …`
  (`:257-261`): todo som colocado depois de uma animação pulada pelo `-n` é
  descartado. É o caminho normal de "renderiza só o pedaço que eu estou
  ajustando", e ele **muda o áudio** do que sai;
- **`-s` / `--save_last_frame`** (`:255-256`) — que é o caso 3 da tabela.

A leitura que amarra os três: **`add_sound` não pergunta "estamos gravando?",
pergunta "a última animação foi pulada?"**. Qualquer coisa que pule uma
animação come o som que vem depois dela.

### 3.2 O cache — o caso que morde de verdade

Este é o mais caro dos seis, porque ele **aparece só na segunda vez**.

**[FONTE]**, `cairo_renderer.py`, em ordem de execução dentro de `play()`:

```python
# :70-71  — no COMEÇO de cada play
self.skip_animations = self._original_skipping_status
self.update_skipping_status()
...
# :94-97  — quando o partial movie já existe em cache
if self.file_writer.is_already_cached(hash_current_animation):
    logger.info("Animation %s : Using cached data ...")
    self.skip_animations = True
    self.time += scene.duration
```

Junte com o fato de que `add_sound` é chamado **entre** `play`s, e leia o flag
que ele encontra: `renderer.skip_animations` guarda o valor deixado pelo
**último** `play`, e só é resetado no `play` seguinte. Portanto:

```python
self.play(Create(circulo))      # 2ª vez que você renderiza: CACHE HIT → skip = True
self.add_sound("clique.wav")    # ← skip ainda é True → DESCARTADO, sem aviso
self.play(FadeOut(circulo))     # aqui o flag é resetado
```

**A regra que sai disso, e ela é dura:**

> **Cena com som renderiza com o cache desligado.** `mx render … --no-cache`,
> ou `bin/manim … --disable_caching`, ou `config.disable_caching = True`.

Não é opcional e não é conservadorismo: o áudio **não vive dentro dos partial
movies** — **[FONTE]** eles são escritos com `av_options = {"an": "1"}`
(`scene_file_writer.py:659`), literalmente "sem áudio". A trilha é remontada do
zero a cada render (§6) e reaproveitar um partial movie significa exatamente
pular a chamada que a alimentaria.

O sintoma clássico: *"funcionou na primeira vez, mexi numa cor, renderizei de
novo e o som sumiu"* — porque a animação com o `add_sound` depois dela não
mudou de hash. Um render limpo "conserta" e o defeito volta na próxima.

Cruzamento: `manim-performance-cache` é dono do cache em si; `manim-project`
§10.7 já registra que **o hash não enxerga estado externo**. Áudio é mais um
item dessa lista — só que este some, em vez de ficar velho.

### 3.3 `-s`, `--format png`, `--dry_run` — sem filme, sem som

**[FONTE]** `SceneFileWriter.finish()` (`:615-631`) só chega ao bloco de áudio
por dentro de `combine_to_movie()`, e `combine_to_movie` só roda se
`write_to_movie()` for verdadeiro. Com `--format png`, `write_to_movie()`
devolve `False` já na primeira linha (`utils/file_ops.py:121-122`).

Com `-s`/`--save_last_frame` é ainda mais cedo: `update_skipping_status`
liga `skip_animations` para **toda** animação (`cairo_renderer.py:255-256`), e
aí é a §3.1 — nem chega a acumular.

Isso vale também para o pôster: **o PNG do último frame não carrega áudio nem
legenda**, obviamente, e é ele que vai para o `?print-pdf` e para o
`prefers-reduced-motion` no deck consumidor. Mais uma razão para o §9.

### 3.4 GIF — o áudio é acumulado e depois jogado fora

**[FONTE]** `scene_file_writer.py:961`:

```python
if self.includes_sound and config.format != "gif":
```

O `add_sound` roda, decodifica o arquivo, monta o `AudioSegment`… e o bloco de
mux é pulado inteiro. Você paga o custo e não leva o produto. **GIF não tem
faixa de áudio — é uma limitação do formato, não do Manim** — mas o Manim não
avisa que você pediu uma coisa impossível.

Curiosidade que confunde: **o `.srt` continua sendo escrito** para o gif (§5.2),
porque `write_subcaption_file` não olha o formato.

### 3.5 `--save_sections` — os vídeos de seção são sempre mudos

**[FONTE]** `combine_to_section_videos` (`:1040-1053`) chama:

```python
self.combine_files(
    section.get_clean_partial_movie_files(),
    self.sections_output_dir / section.video,
)
```

sem o terceiro e o quarto argumento — e a assinatura é
`combine_files(self, input_files, output_file, create_gif=False,
includes_sound=False)` (`:826`). Com `includes_sound=False`, `combine_files`
liga `av_options["an"] = "1"` (`:848-849`) e o bloco de mux de áudio nem existe
nesse caminho.

Consequência: **`--save_sections` produz o mp4 principal COM áudio e os mp4 de
seção SEM áudio, no mesmo render.** Se o seu pipeline consome os vídeos de
seção, som não é uma opção. (A API de seções em si é de `manim-cenas-secoes`;
o formato em partes que evita `--save_sections` por outros motivos é de
`manim-presentation-parts`.)

---

## 4. A linha do tempo do áudio, medida no código

Tudo o que segue está em `SceneFileWriter.add_audio_segment`
(`scene_file_writer.py:425-466`) — 20 linhas que decidem a duração e a mistura.

### 4.1 A trilha **não nasce vazia**: ela nasce com 1 segundo de silêncio

**[FONTE]** `create_audio_segment` (`:421-423`) é:

```python
self.audio_segment = AudioSegment.silent()
```

e **[FONTE]** `pydub/audio_segment.py:462`:

```python
def silent(cls, duration=1000, frame_rate=11025):
```

`duration=1000` **milissegundos**. O docstring do Manim diz "Creates an empty,
silent, Audio Segment" — **ele não é vazio, tem 1 s**. Além disso nasce
**mono, 16 bits, 11025 Hz**.

Isso importa em dois lugares:

- **piso de duração:** a trilha de uma cena nunca é menor que 1 s, mesmo que o
  único som dure 80 ms;
- **taxa de amostragem:** não se preocupe, ela sobe. **[FONTE]**
  `AudioSegment._sync` (`:435-443`) toma o **máximo** de canais, taxa e largura
  entre os dois segmentos antes de qualquer `overlay`/`append`. Um `.wav` 48 kHz
  estéreo puxa a trilha inteira para 48 kHz estéreo. O 11025 só sobrevive se
  **todos** os seus arquivos forem 11025.

### 4.2 O áudio **não** é esticado até o fim do vídeo — e o comentário do Manim diz o contrário

**[FONTE]** `combine_to_movie:962-964`:

```python
sound_file_path = movie_file_path.with_suffix(".wav")
# Makes sure sound file length will match video file
self.add_audio_segment(AudioSegment.silent(0))
```

O comentário promete casar as durações. Siga o código: `AudioSegment.silent(0)`
tem **0 ms**; em `add_audio_segment` com `time=None`, `time = curr_end`,
`new_end = curr_end + 0`, `diff = 0` → **nenhum padding acontece**. É um no-op.

Logo, **a duração da trilha é `max(fim de cada som adicionado, 1 s)`**, e nada
mais. Numa cena de 30 s cujo último clique cai aos 6 s, a faixa de áudio tem
~6 s e o vídeo tem 30 s.

### 4.3 `shortest: 1` — declarado no mux, efeito não verificado

**[FONTE]** `combine_to_movie:989-992` passa ao container de saída:

```python
av_options = {"shortest": "1", "metadata": f"comment=Rendered with Manim Community v{__version__}"}
```

Se essa opção fosse honrada, a §4.2 seria catastrófica: **o vídeo seria
truncado no fim do áudio**. Duas evidências de que ela provavelmente **não** é
honrada neste caminho **[LEITURA]**:

1. o mux é feito à mão, empacotando `demux`/`mux` pacote a pacote
   (`:1010-1029`) — `-shortest` é uma facilidade do binário `ffmpeg`, não uma
   opção de muxer de libavformat;
2. o exemplo oficial do próprio docstring de `Scene.add_sound` (3 cliques
   separados por `wait()`) produziria um vídeo visivelmente cortado, e é o
   exemplo publicado na documentação.

E há uma terceira, deliciosa: **[FONTE]** o ManimGL, que faz o mesmo mux pelo
CLI do ffmpeg, tem a flag **comentada** no fonte —
`.venv-gl/…/manimlib/scene/scene_file_writer.py:341`:

```python
            # "-shortest",
```

Alguém já se queimou com ela. **[NÃO VERIFICADO]** se o `shortest` do PyAV
trunca. Se um dia o seu vídeo sair mais curto que o esperado e tiver som, é
aqui que se olha.

### 4.4 A receita de padding, se você quiser a faixa do tamanho do vídeo

**[LEITURA]** — deriva do fonte de `add_audio_segment` (`:448-460`), que **de
fato** estica quando `diff > 0`:

```python
segment = segment.append(AudioSegment.silent(int(np.ceil(diff * 1000))), crossfade=0)
```

Então, no **fim** do `construct`:

```python
from pydub import AudioSegment          # já é dependência do Manim

def construct(self):
    ...                                  # sua cena
    self.wait(0.4)
    # estica a trilha até o instante atual da cena
    self.renderer.file_writer.add_audio_segment(
        AudioSegment.silent(0), time=self.time
    )
```

`time=self.time` faz `diff = self.time - curr_end > 0` → padding de silêncio até
lá; o overlay de um segmento de 0 ms é inofensivo (**[FONTE]**
`pydub/audio_segment.py:1216-1247`: com `seg2_len = 0` o laço não escreve nada e
o `output.write(seg1[pos:])` devolve a trilha intacta).

Use isto se: (a) o seu player se comporta mal com faixa mais curta que o vídeo,
ou (b) você quer se blindar contra o `shortest` da §4.3.
**Não** use se a cena não tem som nenhum — chamar `add_audio_segment` LIGA
`includes_sound` (`:445-447`) e faz o Manim exportar um wav e remuxar o arquivo
inteiro à toa (§6).

### 4.5 Mixagem: o que acontece quando dois sons se cruzam

**[FONTE]** `add_audio_segment:462-466` termina em:

```python
self.audio_segment = segment.overlay(
    new_segment, position=int(1000 * time), gain_during_overlay=gain_to_background
)
```

- **soma, não substitui.** Sons sobrepostos se somam amostra a amostra
  (`audioop.add`, `pydub:1239-1240`). Três efeitos no mesmo instante podem
  **clipar** — o pydub não limita;
- **a posição é em milissegundos inteiros** (`int(1000 * time)`). A resolução
  temporal do áudio é 1 ms, o que é ~6 % de um quadro a 60 fps: irrelevante;
- **a ordem das chamadas não importa para o resultado**, só a posição. Você pode
  adicionar o som do fim antes do som do começo;
- **não há fade automático.** Corte seco no começo e no fim de cada arquivo. Se
  o seu wav começa com um transiente, ele vai estalar. `fade_in`/`fade_out` do
  pydub resolvem (§7.4).

---

## 5. Legendas: `add_subcaption` e `play(subcaption=…)`

### 5.1 As duas portas, e a aritmética do offset

**[FONTE]** `Scene.add_subcaption` (`scene.py:1712-1758`) é literalmente:

```python
subtitle = srt.Subtitle(
    index=len(self.renderer.file_writer.subcaptions),
    content=content,
    start=datetime.timedelta(seconds=float(self.time + offset)),
    end=datetime.timedelta(seconds=float(self.time + offset + duration)),
)
self.renderer.file_writer.subcaptions.append(subtitle)
```

E **[FONTE]** o atalho dentro de `Scene.play` (`:1206-1219`):

```python
start_time = self.time
self.renderer.play(self, *args, **kwargs)
run_time = self.time - start_time
if subcaption:
    if subcaption_duration is None:
        subcaption_duration = run_time
    self.add_subcaption(content=subcaption,
                        duration=subcaption_duration,
                        offset=-run_time + subcaption_offset)
```

Traduzindo o `-run_time`: o `add_subcaption` é chamado **depois** de a animação
ter rodado, quando `self.time` já avançou. O `-run_time` desfaz esse avanço.
Portanto:

| Você escreve | A legenda começa em | Dura |
|---|---|---|
| `play(anim, subcaption="X")` | o **início** do `play` | o `run_time` medido |
| `play(anim, subcaption="X", subcaption_duration=3)` | o início do `play` | 3 s |
| `play(anim, subcaption="X", subcaption_offset=0.5)` | início + 0,5 s | o `run_time` |
| `add_subcaption("X", duration=2)` antes de um `play` | o instante da chamada | 2 s |

**`subcaption_offset` é medido a partir do começo da animação**, não do fim.
É a única leitura consistente com `start = self.time + (-run_time + offset)`.

Armadilha pequena: `if subcaption:` é *falsy* — `subcaption=""` some sem aviso.

### 5.2 Onde o `.srt` é escrito — e as três vezes em que ele não é

**[FONTE]** `SceneFileWriter.write_subcaption_file` (`:1092-1098`), completo:

```python
if config.output_file is None:
    return
subcaption_file = Path(config.output_file).with_suffix(".srt")
subcaption_file.write_text(srt.compose(self.subcaptions), encoding="utf-8")
logger.info(f"Subcaption file has been written as {subcaption_file}")
```

E ele é chamado no fim de `finish()` (`:633-634`), **depois** de
`combine_to_movie()`. Isso encadeia um detalhe: quem preenche
`config.output_file` é `print_file_ready_message` (`:1100-1103`), chamado no fim
de `combine_to_movie`. Logo:

- **caminho normal (mp4/webm/mov/gif):** o `.srt` sai ao lado do vídeo, mesmo
  nome, no diretório de qualidade —
  `media/videos/<módulo>/1080p60/<Cena>.srt`. Com `-o nome`, `nome.srt`;
- **`--format png`, `--dry_run`, `-s` sem `-o`:** `config.output_file` continua
  `None` e a função **retorna calada**. Nada de `.srt`. (Com `-s`, `save_image`
  até define `output_file` — mas **[FONTE]** `cairo_renderer.py:269-282` chama
  `file_writer.finish()` **antes** de `save_image`, então na hora que importa
  ainda é `None`);
- **gif:** o `.srt` **é** escrito, ao lado do gif que não tem áudio;
- **[LEITURA] o caminho `manimx`/`mx render` sem `-o` num formato sem filme**:
  `manimx/render.py:214-215` só põe `output_file` no config quando ele não é
  `None`, e o `manim.cfg` deixa a chave como string vazia (`_config/utils.py:641`,
  `fallback=""`). Com `""` a guarda `is None` não pega e
  `Path("").with_suffix(".srt")` levanta
  `ValueError: PosixPath('.') has an empty name`. Só acontece se houver legenda
  E não houver filme — combinação rara, mas é um `ValueError` sem relação
  aparente com legenda. [NÃO VERIFICADO por execução].

### 5.3 O índice começa em 0 e o `srt` conserta

**[FONTE]** o Manim monta `index=len(self.subcaptions)` — logo, a primeira
legenda tem índice **0**, o que é ilegal em SRT. Mas
**[FONTE]** `srt.compose(subtitles, reindex=True, start_index=1, strict=True,
eol=None, in_place=False)` tem `reindex=True` por default e reescreve os índices
a partir de 1. Não há nada a corrigir — só não estranhe o `index=0` ao inspecionar
`file_writer.subcaptions` no meio de um render.

Também **[FONTE]**: com `strict=True` (default) o `srt` roda `make_legal_content`
em cada bloco (`srt.py:164-165, 183-203`), que remove **linhas em branco** do
conteúdo. Legenda de duas linhas (`"linha 1\nlinha 2"`) passa; `"a\n\nb"` vira
`"a\nb"`.

### 5.4 O que o `.srt` NÃO valida

- **sobreposição temporal.** Duas legendas com intervalos que se cruzam são
  escritas como estão; o comportamento é do player;
- **ordem — e aqui há uma correção.** Uma versão anterior dizia que as legendas
  "saem na ordem em que foram adicionadas" e que o Manim **não** chama
  `sort_and_reindex`. As duas metades são falsas, e contradiziam a §5.3 deste
  mesmo arquivo. O que o Manim escreve é
  `srt.compose(self.subcaptions)` (`scene_file_writer.py:1097`), e
  `compose` tem `reindex=True` por default (`srt.py:439-441`), que chama
  `sort_and_reindex` (`:471-474`), que faz `sorted(subtitles)` (`:294`) —
  ordenando por `(start, end, index)` (`:131-136`). Ou seja: **o `.srt` sai
  sempre ordenado por tempo**, e um `offset` negativo grande reordena o arquivo
  em silêncio em vez de produzir um `.srt` fora de ordem;
- **`compose` também DESCARTA legendas, e este é o modo de falha calado que
  importa.** `skip=True` é default em `sort_and_reindex`, e o filtro é
  (`srt.py:80-84`):

  ```python
  SUBTITLE_SKIP_CONDITIONS = (
      ("No content",                      lambda sub: not sub.content.strip()),
      ("Start time < 0 seconds",          lambda sub: sub.start < ZERO_TIMEDELTA),
      ("Subtitle start time >= end time", lambda sub: sub.start >= sub.end),
  )
  ```

  Logo `add_subcaption("texto", duration=0)` (`start == end`) **some do `.srt`**
  sem erro — só um `LOG.info` (`srt.py:298-311`), invisível no
  `--verbosity WARNING` que o `mx render` usa por default. Idem para conteúdo
  só de espaços, e para um `offset` negativo que jogue o início antes de zero.
  Os índices dos que sobram são renumerados, então nem o `.srt` denuncia o
  buraco;
- **duração mínima.** `duration=0.05` gera uma legenda de 50 ms que nenhum
  humano lê — e `duration=0` não gera legenda nenhuma (acima).

### 5.5 A assimetria que ninguém espera: legenda **ignora** `skip_animations`

Compare:

```python
Scene.add_sound:        if self.renderer.skip_animations: return     # scene.py:1802
Scene.add_subcaption:   (nenhuma guarda)                             # scene.py:1712-1758
```

**[FONTE]**, e a consequência é direta: **numa cena cortada em partes, o `.srt`
de CADA parte contém as legendas de TODAS as partes** — porque `self.time`
avança normalmente durante os atos pulados (`cairo_renderer.py:78`,
`self.time += scene.duration`) e o `add_subcaption` é executado do mesmo jeito.

Na prática isso é até útil (o `.srt` da última parte é o roteiro completo com os
tempos certos do vídeo contínuo), mas é uma armadilha se você espera que o `.srt`
da parte 6 descreva só a parte 6. **Ele não descreve** — e os tempos dele são do
vídeo INTEIRO, não do mp4 daquela parte.

### 5.6 Legenda `.srt` não é texto na tela

O `.srt` é um arquivo irmão. Ele não aparece no mp4, não é queimado, e depende
de o player carregá-lo. Se o que você quer é **texto visível dentro do vídeo**,
isto aqui é a skill errada: use `Text`/`MarkupText` e a tipografia de
`manim-text-latex` (que também é dona da armadilha de nitidez do cairo, a
correção `_texto_nitido` de renderizar em `font_size` grande e encolher).

Casos em que `.srt` é a resposta certa: publicação em plataforma que aceita
legenda (YouTube, Vimeo), acessibilidade, e **como roteiro cronometrado** — é o
uso mais subestimado: `play(anim, subcaption="…")` te dá, de graça, um arquivo
com o que se fala em cada instante do vídeo, sem nada mudar na imagem.

---

## 6. O que sai no arquivo: containers, codecs e o custo

**[FONTE]** `combine_to_movie:960-1032`. Quando `includes_sound` é verdadeiro e
o formato não é gif, o Manim:

1. exporta a trilha inteira para um `.wav` ao lado do vídeo
   (`audio_segment.export(..., format="wav", bitrate="312k")` — `bitrate` é
   ignorado em wav);
2. converte esse wav para o codec que o container aceita (tabela abaixo), com
   `convert_audio`, que é PyAV;
3. abre o mp4 já pronto, abre o áudio, cria um arquivo `<nome>_temp<ext>`,
   copia **os pacotes de vídeo sem recodificar** (`add_stream_from_template`) e
   depois os de áudio, fecha, e faz `shutil.move` por cima do original;
4. apaga o wav.

| `movie_file_extension` | Quando | Codec de áudio no arquivo final |
|---|---|---|
| `.mp4` (default) | tudo o que não for os de baixo | **AAC** (`convert_audio(..., "aac")`, `:984`) |
| `.webm` | `--format webm`, ou `-t` + webm | **Vorbis** (`libvorbis`, `:978`) |
| `.mov` | `-t/--transparent` sem webm, ou `--format mov` | **o WAV cru** — não há branch de conversão para `.mov`; entra `pcm_s16le` no container. Legal, mas pesado |
| `.gif` | `--format gif` | **nenhum** — §3.4 |

Três consequências operacionais:

- **som custa uma passagem extra sobre o arquivo final.** O vídeo inteiro é
  remuxado (copiado, não recodificado) para poder ganhar a faixa de áudio.
  Numa cena grande isso é I/O sério, e é **por render**, sempre;
- **NVENC e áudio não colidem.** **[FONTE]** o patch do `manimx` instala o
  `_StreamRewriteProxy` **apenas durante `open_partial_movie_stream`**
  (`manimx/gpu.py:424-483`), e ele só reescreve chamadas a `add_stream` com
  `codec_name == "libx264"`. O mux final usa `add_stream_from_template` e nem
  passa pelo proxy. Codec de vídeo é assunto de `manim-gpu-encoding`; áudio não
  interfere nele e vice-versa;
- **transparência + som = arquivo grande.** `.mov` com `qtrle` (vídeo lossless)
  e `pcm_s16le` (áudio lossless). Se o peso importa, ver `manim-gpu-encoding`.

---

## 7. Receitas

Todas escritas contra assinatura conferida no índice. **Nenhuma foi executada**
— trate-as como referência de API, não como teste.

### 7.1 Um clique marcando o beat de uma animação

```python
class Beat(Scene):
    def construct(self):
        barra = Rectangle(width=0.4, height=1.0, color=BLUE, fill_opacity=1)
        self.add(barra)

        # o clique cai no INÍCIO do crescimento: chamada antes do play
        self.add_sound("sons/clique.wav", gain=-8)
        self.play(barra.animate.stretch_to_fit_height(3.0), run_time=0.6)

        # e este cai 120 ms ANTES do fim do próximo play
        self.add_sound("sons/clique.wav", time_offset=0.48, gain=-8)
        self.play(barra.animate.set_color(RED), run_time=0.6)
```

Renderize com `mx render arquivo.py Beat --no-cache` (§3.2).

### 7.2 Trilha de fundo com ducking na hora do efeito

```python
self.add_sound("sons/trilha.wav", gain=-22)          # entra em t=0, bem baixa
self.play(Create(eixos))
self.add_sound("sons/impacto.wav", gain=-4,
               gain_to_background=-10)               # abaixa a trilha durante o impacto
```

`gain_to_background` chega por `**kwargs` (§2.4). Lembre que a trilha inteira é
somada de uma vez em t=0: se ela for mais longa que o vídeo, sobra áudio depois
do último quadro (o container guarda; o player para no fim do vídeo).

### 7.3 Tocar só um trecho de um arquivo (o `add_sound` não tem seek)

Use a camada de baixo com pydub — o fatiamento é em **milissegundos**:

```python
from pydub import AudioSegment
from manim.utils.sounds import get_full_sound_file_path

trecho = AudioSegment.from_file(get_full_sound_file_path("sons/musica.wav"))[3000:8500]
trecho = trecho.apply_gain(-14)
self.renderer.file_writer.add_audio_segment(trecho, time=self.time)
```

`add_audio_segment(new_segment, time=None, gain_to_background=None)` — com
`time=self.time`, o trecho entra no instante corrente da cena.

**Atenção:** este caminho **não** passa pela guarda de `skip_animations` da §3.1
(a guarda mora em `Scene.add_sound`, não no writer). Numa cena em partes, isso
significa que o trecho entra em **todas** as partes. Se você quiser o
comportamento normal, replique a guarda:

```python
if not self.renderer.skip_animations:
    self.renderer.file_writer.add_audio_segment(trecho, time=self.time)
```

### 7.4 Fade e normalização, para não estalar

```python
from pydub import AudioSegment
from manim.utils.sounds import get_full_sound_file_path

seg = AudioSegment.from_file(get_full_sound_file_path("sons/whoosh.wav"))
seg = seg.fade_in(15).fade_out(60)            # ms
seg = seg.apply_gain(-3.0 - seg.max_dBFS)     # pico em -3 dBFS
self.renderer.file_writer.add_audio_segment(seg, time=self.time)
```

`fade_in(duration)`, `fade_out(duration)`, `apply_gain(volume_change)`,
`max_dBFS` (property) — **[FONTE]**, todos do `AudioSegment` 0.25.1.

### 7.5 Legendar a cena inteira como roteiro cronometrado

```python
class Aula(Scene):
    def construct(self):
        self.play(Create(eixos),   subcaption="Os eixos vão de zero a dez.")
        self.play(Create(curva),   subcaption="A curva é o custo por mês.")
        self.add_subcaption("Repare no ponto de inflexão.", duration=2.5)
        self.wait(2.5)
```

Sai um `.srt` ao lado do mp4 com os tempos exatos do vídeo. Zero impacto na
imagem, zero impacto no áudio, custo ~zero de render.

### 7.6 O padrão de projeto: um `SONS` no `tema.py`

Repetir `"sons/clique.wav"` em 12 cenas é a mesma doença que repetir um hex.
No idioma deste projeto (ver `manim-tema-projeto` para o contrato completo):

```python
# tema.py
from pathlib import Path
_RAIZ = Path(__file__).resolve().parent
SONS = _RAIZ / "sons"

def som(nome: str) -> str:
    """Caminho absoluto de um som. Falha com a lista do que existe."""
    p = SONS / nome
    if not p.exists():
        existe = ", ".join(sorted(f.name for f in SONS.glob("*"))) or "(nenhum)"
        raise FileNotFoundError(f"som '{nome}' não existe em {SONS}. Existem: {existe}")
    return str(p)
```

Duas razões, as duas já pagas neste projeto: (1) caminho absoluto derivado de
`__file__` imuniza contra o `cwd` (§2.5); (2) erro que **lista o que existe** é
o mesmo idioma do `numero()` do `tema.py` do deck consumidor. E como o `tema.py`
é importado por todas as cenas, **a checagem mora na função, nunca no import** —
um `FileNotFoundError` no import derrubaria cenas que nem usam som.

---

## 8. Verificar o resultado — sem `ffprobe`

`get_video_metadata` **não serve aqui**: **[FONTE]**
`manim/utils/commands.py:47-67` lê só `container.streams.video[0]` e devolve
largura, altura, frames, duração, codec de vídeo e `pix_fmt`. Nada de áudio.

Use PyAV direto — é a mesma biblioteca que o Manim usa, só lê o cabeçalho, não
decodifica nada, e **não é o `ffprobe`**:

```python
# confere_audio.py  — leitura de cabeçalho, ~milissegundos por arquivo
import sys
import av

for caminho in sys.argv[1:]:
    with av.open(caminho) as c:
        linhas = []
        for s in c.streams:
            dur = float(s.duration * s.time_base) if s.duration else None
            linhas.append(f"{s.type}:{s.codec_context.name}"
                          + (f" {dur:.2f}s" if dur else ""))
        print(caminho, "|", " + ".join(linhas) or "(sem streams)")
```

O que você quer ver num mp4 com som: `video:h264 30.00s + audio:aac 6.02s`.
Se a segunda metade não aparecer, volte para a **§3** e percorra as seis causas
na ordem da tabela.

Para o `.srt`, a conferência é ainda mais barata — e vale ler o arquivo, porque
número de blocos e tempo final são exatamente o que se erra:

```bash
f=media/videos/aula/1080p60/Cena.srt
grep -c ' --> ' "$f"        # quantas legendas
tail -4 "$f"                # o último tempo bate com a duração do vídeo?
```

**A regra transversal continua valendo:** renderizou e não conferiu = não
terminou. Para o lado visual desse ciclo (olhar o PNG, o pôster em branco, o
corte na borda) a dona é **`manim-verificacao-visual`**; esta skill só acrescenta
o eixo do áudio.

---

## 9. Quando som é a resposta ERRADA — o caso medido do deck consumidor

O consumidor real deste projeto Manim é `~/Projects/aulas`: um deck reveal.js
com **77 vídeos renderizados** por este pipeline. **Nenhum deles tem áudio**, e
isso é decisão, não esquecimento.

Três evidências, conferidas no disco:

1. `grep -rn "add_sound\|add_subcaption" aulas/*/manim/*.py` → **nada**. Nem uma
   chamada em 11 arquivos de cena;
2. o player **força o silêncio**: `src/components/video.tsx:112` e
   `src/components/video-partes.tsx:279` renderizam `<video … muted playsInline>`.
   Mesmo que houvesse áudio, ele não tocaria;
3. o formato do deck é o **em partes** (`manim-presentation-parts`): o vídeo para
   num frame congelado e **o professor fala por cima**. Áudio embutido brigaria
   com a fala ao vivo, e — pela §3.1 — a trilha nem seria contínua entre as
   partes.

A lição transferível, e ela é mais geral que este deck:

> **Se existe um humano narrando, o vídeo é mudo.** Som embutido serve para
> vídeo que roda sozinho (YouTube, loop de feira, demo assíncrona). Para
> apresentação ao vivo, a trilha certa é a voz de quem está no palco, e a
> legenda certa é a nota do slide.

O corolário para legendas: num deck ao vivo o `.srt` também não serve — o que
serve é a prop `notes` do slide. Mas o `.srt` **é** útil como subproduto: se um
dia a aula virar vídeo assíncrono, `play(..., subcaption=…)` já deixou o roteiro
cronometrado pronto (§7.5).

---

## 10. ManimGL (3b1b): a mesma ideia, quatro diferenças

Quem traduz cena de um lado para o outro precisa desta tabela.
**[FONTE]** `.venv-gl/…/manimlib/scene/scene.py:636-646`,
`scene_file_writer.py:169-181, 317-345`, `utils/sounds.py`.

| | ManimCE 0.21 | ManimGL 1.7.2 |
|---|---|---|
| assinatura | `add_sound(sound_file, time_offset=0, gain=None, **kwargs)` | `add_sound(sound_file, time_offset=0, gain=None, gain_to_background=None)` — **explícito**, não escondido no `**kwargs` |
| guarda de skip | `if self.renderer.skip_animations: return` | `if self.skip_animations: return` — mesma ideia |
| onde procura o arquivo | `assets_dir` (default `./`), extensões `.wav`/`.mp3` | `sounds:` do `default_config.yml` (default `"sounds"`), extensões `.wav`/`.mp3`/`""` |
| conversão | PyAV pré-converte tudo que não é wav/raw | nenhuma: entrega direto ao pydub, que chama o **binário `ffmpeg`** |
| mux final | PyAV, `-c:a aac` implícito via `convert_audio` | CLI do ffmpeg: `-c:v copy -c:a aac -b:a 320k`, com `# "-shortest"` **comentado** |
| **legendas** | `add_subcaption` + `.srt` | **não existem.** `grep -rn "subcaption\|srt"` em `manimlib/` → zero |
| **tocar no preview** | não existe | `manimlib.utils.sounds.play_sound(f)` — dispara `aplay`/`afplay`/PowerShell num `subprocess` |

O `play_sound` do GL é a única coisa desta lista que o CE não tem e que dá
saudade: no CE não há como ouvir o som durante o `--preview`; a única forma de
conferir é abrir o mp4 renderizado.

Tradução de cena e o resto das diferenças CE↔GL: **`manimgl-3b1b`**.

---

## 11. Diagnóstico: sintoma → causa → correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| mp4 mudo, exit 0, primeira vez que renderiza | formato (gif/png), ou `-s`, ou seção pulada | §3, tabela das seis |
| **mudo só a partir da segunda vez** | **cache hit** (§3.2) | `--no-cache` / `--disable_caching`. Sempre, em cena com som |
| `OSError: From: /x/y, could not find …` | caminho relativo ao `cwd` errado, ou extensão fora de `.wav`/`.mp3` | §2.5 — caminho absoluto por `Path(__file__)` |
| `KeyError: 'sample_width'` | arquivo `.raw`/`.pcm` (§2.6) | converta para `.wav` PCM 16 bits |
| `ValueError: Adding sound at timestamp < 0` | `time_offset` negativo maior que `self.time` | §2.2 — o absoluto não pode ser negativo |
| `CouldntDecodeError` / `FileNotFoundError: 'ffmpeg'` no meio do pydub | wav não-PCM caindo no fallback de `subprocess` (§2.6) | reexporte como PCM 16 bits |
| som adiantado/atrasado em ~1 animação | a chamada está do lado errado do `self.play` | §2.2 — antes = início, depois = fim |
| o volume de um som some no meio | outro `add_sound` com `gain_to_background` está atenuando (§2.4) | tire o ducking, ou ajuste |
| estalo no começo/fim de um som | corte seco, sem fade (§4.5) | `fade_in(15).fade_out(60)` (§7.4) |
| o gif não tem som | limitação do formato + §3.4 | exporte mp4 |
| vídeos de seção mudos, mp4 principal com som | §3.5, `--save_sections` não passa `includes_sound` | não há flag; consuma o mp4 principal |
| `.srt` não apareceu | `--format png`/`-s`/`--dry_run` → `config.output_file is None` (§5.2) | renderize em formato de filme |
| `ValueError: PosixPath('.') has an empty name` | §5.2, caminho `manimx` sem filme e sem `-o` | passe `-o nome`, ou renderize em mp4 |
| `.srt` da parte 6 tem legenda das outras partes | §5.5 — legenda não respeita `skip_animations` | é o comportamento; use o `.srt` da última parte |
| `ImportError: audioop` | Python 3.13 sem `audioop-lts` (§1.4) | fixe o Python em 3.12, ou instale `audioop-lts` |

Traceback que **não** é de áudio, erro de ambiente/codec/saída, bissecção:
**`manim-troubleshooting`**. Erro de **nome ou assinatura**:
**`manim-api-discovery`**.

---

## 12. Onde esta skill para

A fronteira, e de que lado cada coisa cai:

| Assunto | Skill dona | A fronteira |
|---|---|---|
| **codec de VÍDEO, NVENC, peso do arquivo, `mx bench`** | `manim-gpu-encoding` | tudo que é **faixa de vídeo** é de lá. A tabela container→codec de **áudio** da §6 é daqui, e as duas não interferem uma na outra (§6, o proxy) |
| **texto DESENHADO na tela** (`Text`, `MarkupText`, `Tex`, `t2c`, nitidez) | `manim-text-latex` | `.srt` é arquivo irmão, nunca pixel. Qualquer coisa que a plateia LÊ na imagem é de lá (§5.6) |
| **cortar a cena em partes para slide** | `manim-presentation-parts` | o mixin, o `_corte`, a emenda e a métrica direcional são de lá. Daqui vem só o que o corte faz com o **áudio** (§3.1) e com o **`.srt`** (§5.5) |
| **`next_section`, `Section`, `--save_sections`, o mapa das classes de `Scene`** | `manim-cenas-secoes` | a API genérica de seções é de lá. Daqui vem o fato de que os vídeos de seção são **mudos** (§3.5) |
| **cache de partial movies, `hash_obj`, `max_files_cached`** | `manim-performance-cache` | o cache em si é de lá. Daqui vem por que ele **come o áudio** (§3.2) — a causa é a flag `skip_animations`, não o cache |
| **`--format`, `-q`, caminho da saída, o JSON do `mx render`** | `manim-render-api` | escolher formato é de lá; o que cada formato faz **com o áudio** é daqui (§3.3, §3.4, §6) |
| **imagens, SVG, fontes, `assets_dir` como pasta de assets** | `manim-svg-imagens` | ela é dona de `assets_dir` para imagem/SVG/fonte. Daqui vem só a resolução de caminho **de som** (§1.3) — mesma função de baixo, `seek_full_path_from_defaults`, usos diferentes |
| **o `tema.py` como contrato do projeto** | `manim-tema-projeto` | o `SONS`/`som()` da §7.6 é uma peça daquele contrato, escrita aqui porque é sobre som |
| **"renderizou e não olhou = não terminou"**, o PNG, o pôster | `manim-verificacao-visual` | o ciclo é de lá; a §8 é o eixo de **áudio** desse mesmo ciclo |
| **`rate_func`, `run_time`, `lag_ratio`, ritmo temporal** | `manim-composicao-ritmo` | sincronizar som é aritmética de `self.time`; escolher o tempo da ANIMAÇÃO é de lá |
| **`manim-voiceover` e plugins de terceiros** | `manim-project` §13.7 | **não estão instalados nesta máquina.** Não presuma. TTS, alinhamento forçado e gravação de voz não existem aqui |
| **tradução ManimGL ↔ ManimCE** | `manimgl-3b1b` | a §10 é só o recorte de áudio dessa tradução |

**Buracos que continuam abertos depois desta skill**, e que valem ser ditos em
voz alta em vez de improvisados:

- **não há edição de áudio de verdade.** Sem envelope, sem EQ, sem compressor,
  sem limitador, sem crossfade entre sons — só `overlay`, `apply_gain`,
  `fade_in`/`fade_out` e fatiamento do pydub;
- **não há sincronização automática.** Nada casa um beat de música com um
  `play`; você escreve os números;
- **não há visualização de áudio.** Waveform, espectro e VU meter são desenhos
  que você faz com `Axes` a partir de um array que você mesmo extrai
  (`AudioSegment.get_array_of_samples()` existe, mas isso é
  `manim-graphs-plots` fazendo gráfico, não esta skill);
- **não há legenda queimada.** Nem estilo, nem posição, nem fonte no `.srt`
  (é SRT puro, sem tags).

---

## 13. O que ficou NÃO VERIFICADO nesta sessão

Explícito, para ninguém citar como fato:

1. **Se o `shortest: 1` do mux (§4.3) trunca o vídeo.** O mecanismo está lido e
   há três indícios de que não trunca — inclusive a flag comentada no ManimGL —
   mas só um render com áudio mais curto que o vídeo decide.
2. **O `KeyError` do `.raw` (§2.6).** Os dois trechos de código foram lidos e
   não têm como se encontrar; a exceção exata não foi provocada.
3. **O `ValueError: empty name` do `.srt` pelo caminho `manimx` sem filme
   (§5.2).** Deduzido de `manimx/render.py:214-215` + `_config/utils.py:641`;
   `Path('').with_suffix('.srt')` foi confirmado levantando `ValueError` em
   Python puro, mas o caminho completo não foi percorrido.
4. **Como o ducking soa** (§2.4). O `gain_during_overlay` é um degrau sem
   attack/release — está no código; o resultado auditivo não foi ouvido.
5. **Qualquer número de tempo, de peso de arquivo ou de bitrate.** Nada foi
   renderizado, nada foi medido. Os únicos números deste arquivo vindos de
   medição são de contagem estática (77 vídeos, 11 arquivos de cena, versões de
   pacote) e do próprio fonte (1000 ms, 11025 Hz, `crf 23`, `-b:a 320k` do GL).
6. **O comportamento de players reais** com faixa de áudio mais curta que o
   vídeo, e com `.srt` de índices sobrepostos.

Se você for executar qualquer um destes, o ciclo é: um render curto (`-ql`, uma
cena de 3 s), `--no-cache`, e o script de PyAV da §8 — nunca `ffprobe`.
