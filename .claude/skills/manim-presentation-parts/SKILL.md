---
name: manim-presentation-parts
description: >-
  Cena Manim para PALESTRA/SLIDE (reveal.js, PowerPoint, Beamer, qualquer deck):
  o formato em PARTES que o apresentador avança com a seta — um `construct`
  inteiro, N mp4s, cada um terminando num frame parado. Use SEMPRE que a cena
  vai PARAR dentro de uma apresentação e alguém vai FALAR por cima do frame
  congelado: "vídeo para o slide", "animação da aula", "quebra essa cena em
  partes", "o apresentador avança por etapas", "o vídeo é longo demais para eu
  comentar", "insere uma parte no meio", "funde a parte 3 com a 4", "re-renderiza
  só a parte 5", "quantas partes essa cena deveria ter?", "a emenda entre as
  partes pisca", "sumiu um desenho na troca de parte", "o mp4 saiu vazio e não
  deu erro", "o vídeo da parte tem 0 segundos", "apareceu um `_Atos…` na lista de
  cenas". Cobre o mecanismo `next_section(skip_animations=…)` conferido no
  fonte (o que é garantido, o que NÃO é e quanto custa), o padrão mixin +
  subclasses `P1..PN` com a ordem das bases, a granulação por RECADO FALADO, as
  regras de palco que vieram de devolução, a armadilha da emenda, a métrica
  DIRECIONAL para medi-la (nunca RMS), um conferidor ESTÁTICO por AST que acha
  corte órfão e MRO invertido sem renderizar nada, e os procedimentos de
  manutenção (inserir, remover, renumerar, alcance do re-render). NÃO use para
  vídeo standalone contínuo (YouTube, demo, loop) — lá o corte não se aplica;
  nem para a API genérica de seções e o mapa das classes de `Scene`
  (`manim-cenas-secoes`); nem para escolher `rate_func`/`run_time`/`lag_ratio`
  (`manim-composicao-ritmo`); nem para codec, GPU e peso do arquivo
  (`manim-gpu-encoding`); nem para o script que renderiza o lote e extrai
  pôsteres (`manim-batch-pipeline`); nem para OLHAR um frame e julgar se o
  desenho ficou certo em geral — contraste, corte na borda, sobreposição,
  comparar dois renders quaisquer — que é `manim-verificacao-visual` (a régua da
  emenda nasceu aqui, na §7, e é aqui que ela fica calibrada para o corte entre
  partes; lá ela é generalizada para um par antes/depois qualquer).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Cena de apresentação — nasce em partes

Uma animação de 40 s dentro de um slide não deixa o apresentador falar: ou ele
narra por cima do movimento, ou fica calado o filme inteiro. O formato que
resolve é este: a cena é **UMA**, escrita inteira num `construct`, mas
renderizada em **N mp4s** — um por ato — e cada parte termina num **frame
parado**. O apresentador avança com a seta, fala no frame parado, e o primeiro
frame da parte N+1 é, por construção, o último da parte N.

O padrão nasceu no deck consumidor `~/Projects/aulas`. **Inventário contado no
disco em 2026-08-19:** 11 arquivos de cena, **10 mixins `_Atos*`**, **77 classes
`PN`**, **75 chamadas textuais a `_corte(`** (a diferença são 2 cortes que saem de
um laço), **77 mp4 renderizados** (59 na aula 001 + 18 na aula 002) e **154 png**
(dois por parte). As cenas em partes têm entre **5 e 14 partes**. Cada regra
abaixo veio de uma devolução real do apresentador ou de um defeito que custou um
render.

## Procedência do que está escrito aqui

Três marcadores, e eles valem para o arquivo inteiro:

- **[FONTE]** — conferido lendo o ManimCE 0.21.0 instalado em
  `.venv/lib/python3.12/site-packages/manim/` ou o índice estático de `api/`.
  Afirmação forte, com arquivo e linha.
- **[DECK]** — medição feita no deck consumidor, em outra sessão. Testemunho
  confiável, **não reproduzido aqui**.
- **[HOJE]** — reproduzido nesta sessão, 2026-08-19, com `grep`/`sed`/`ast`/
  Python puro. **Nenhum render, nenhum ffmpeg, nenhuma GPU.**

## Cartão de referência — o sintoma manda na seção

| O que aconteceu | Onde ler |
|---|---|
| "quero fazer uma cena para slide" | §3 (esqueleto) → §4 (granulação) → §5 (regras de palco) |
| "quantas partes?" | §4 |
| o mp4 saiu **vazio / não foi escrito**, sem erro | §2.4 e §10 — corte órfão, e o conferidor de §8 acha em 20 ms |
| o mp4 tem **~0 s** e a cena parece vazia | §3.3 — bases na ordem errada; §10 traz a assinatura exata da falha |
| apareceu um `_Atos…` na lista de cenas / renderizou um mp4 de 35 s que ninguém usa | §3.2 |
| a troca de parte **pisca** ou some um desenho | §6 (a armadilha) e §7 (medir) |
| o PDF/pôster de backup saiu **em branco** | §7.4 e §11.3 |
| editei um ato — o que preciso re-renderizar? | §9.1, a tabela de alcance |
| inserir/remover/fundir uma parte | §9.2 e §9.3 (os dois laços NÃO são inversos) |
| "isso é caro? renderizar 9 partes custa 9×?" | §2.3, a conta com o fonte |
| "por que não `--save_sections`?" | §1 |

---

## 1. Por que PARTES, e não outra coisa

Há três formas de tirar N vídeos de uma explicação. Duas perdem, e é importante
saber por quê — porque a que perde parece mais simples.

| Forma | Como | Por que perde |
|---|---|---|
| **N cenas separadas** (`Ato1(Scene)`, `Ato2(Scene)`…) | cada uma reconstrói o palco onde a anterior parou | existem **duas versões do mesmo estado** e elas divergem na primeira edição. A emenda deixa de ser garantida e passa a ser mantida à mão, para sempre |
| **`--save_sections`** | um render, o Manim escreve um mp4 por seção | funciona, é **mais barato** (§2.3), e o naming é o problema: **[FONTE]** `scene_file_writer.py:346` monta `f"{output_name}_{len(sections):04}_{name}{ext}"` → `Worktrees_0005_ato6.mp4`, mais um `Worktrees.json` de índice. Um terceiro artefato para manter em sincronia, e um nome que o consumidor não escolhe. Além disso o `mx render` **não expõe** a flag (`manimx/cli.py:457-476`) — só `bin/manim --save_sections` ou `manimx.render_scene(save_sections=True)` |
| **mixin + `PARTE` + `next_section(skip_animations=…)`** ← este | uma classe por parte; cada render escreve **um** arquivo, com nome derivado da classe | o estado nunca diverge (é o MESMO código), o nome é `worktrees-p6.mp4` (§11.2), e **você pode re-renderizar UMA parte** em segundos durante a iteração sem tocar nas outras |

**A honestidade sobre o custo:** para o render em BLOCO, `--save_sections` é uma
passagem e o formato em partes são N. A conta está em §2.3. O formato em partes
paga isso de volta na EDIÇÃO — que é o que se faz todo dia — e no nome de
arquivo. Se o seu caso é "render único, nunca mais mexo", `--save_sections` é
uma escolha defensável; a API genérica de seções é de **`manim-cenas-secoes`**.

---

## 2. O mecanismo, conferido no fonte

### 2.1 As assinaturas reais

**[FONTE]** — `api/manim-ce-index.tsv` e `api/manim-ce-methods.tsv`:

```
Scene.next_section(self, name: str = 'unnamed',
                   section_type: str = DefaultSectionType.NORMAL,
                   skip_animations: bool = False) -> None
Scene.wait(self, duration: float = 1.0,
           stop_condition: Callable[[], bool] | None = None,
           frozen_frame: bool | None = None) -> None
Scene.play(self, *args, subcaption=None, subcaption_duration=None,
           subcaption_offset=0, **kwargs) -> None
Scene(renderer=None, camera_class=Camera, always_update_mobjects=False,
      random_seed=None, skip_animations: bool = False) -> None

SceneFileWriter.next_section(self, name: str, type_: str, skip_animations: bool) -> None
Section(type_: str, video: str | None, name: str, skip_animations: bool) -> None
DefaultSectionType            # StrEnum, um único membro: NORMAL = "default.normal"
```

Repare em dois detalhes que já custaram tempo a alguém:

- o parâmetro do `Scene` chama `name`; o do `SceneFileWriter` chama `type_` na
  segunda posição. Você nunca chama o segundo — mas ao ler traceback, saiba qual
  é qual;
- `Scene.__init__` também aceita `skip_animations`. **Não é esse** que corta em
  partes: ele desliga a escrita de frames da cena INTEIRA
  (`cairo_renderer.py:49`, `_original_skipping_status`). Quem corta por trecho é
  o `next_section`.

### 2.2 O caminho do código, do `_corte` ao mp4

**[FONTE]**, na ordem em que acontece:

1. `Scene.next_section(...)` (`scene/scene.py:362`) só delega:
   `self.renderer.file_writer.next_section(name, section_type, skip_animations)`.
2. `SceneFileWriter.next_section` (`scene_file_writer.py:332`) chama
   `finish_last_section()` — que **descarta a seção anterior se ela estiver
   vazia** — e empilha uma `Section` nova com a flag.
3. A CADA `self.play(...)` — e `self.wait()` **é** um play, ele monta um `Wait` e
   chama `self.play` (`scene.py:1250`) — o renderer faz, em
   `cairo_renderer.py:70-71`:

   ```python
   self.skip_animations = self._original_skipping_status   # reseta
   self.update_skipping_status()                           # lê a seção ATUAL
   ```

   e `update_skipping_status` (`:245-253`) começa com
   `if self.file_writer.sections[-1].skip_animations: self.skip_animations = True`.
   **A decisão é por `play`, relida da seção corrente** — por isso ela não
   "gruda" depois de uma seção pulada.
4. Pulando, `hash_current_animation = None` e
   `file_writer.add_partial_movie_file(None)` empilha `None` na lista
   (`scene_file_writer.py:376`) — o comentário do próprio Manim explica: o `None`
   existe para manter o índice alinhado com `scene.num_plays`.
5. No fim, `combine_to_movie` (`:937`) faz
   `partial_movie_files = [el for el in self.partial_movie_files if el is not None]`.

**Conclusão:** o mp4 final contém **apenas** os frames da seção não pulada. Não
há corte, não há concatenação a fazer — o Manim monta o vídeo só com o que
sobrou.

### 2.3 O que "pular" faz, o que NÃO faz, e quanto custa

Aqui mora a afirmação mais repetida e menos verificada deste formato. O fonte diz
exatamente o seguinte:

- **o código do ato pulado RODA.** `construct` é um método Python: os `Text`, os
  `VGroup`, os `Line`, os `.arrange()` são construídos igual. Pular é sobre
  ESCREVER FRAME, não sobre executar;
- **a animação chega ao estado final.** Duas garantias independentes:
  `get_time_progression` (`scene.py:1064-1098`) devolve
  `times = [run_time]` — **um único passo, no alfa final** — quando
  `skip_animations`; e `play_internal` (`:1390-1391`) roda
  `animation.finish()` + `animation.clean_up_from_scene(self)` para toda
  animação, pulada ou não;
- **nenhum frame é gravado.** `add_frame` (`cairo_renderer.py:181-193`) tem
  `if self.skip_animations: return` como primeira coisa depois de calcular `dt`;
- **mas UMA rasterização acontece.** `play_internal` chama
  `self.renderer.render(scene, t, ...)` para o único `t`, e `render` faz
  `update_frame(...)` + `add_frame(get_frame())`. O frame é desenhado pelo cairo
  e jogado fora. **[FONTE]**, `cairo_renderer.py:161-168`.

A conta que sai disso, e que decide se vale a pena:

| | render contínuo (1 mp4) | N renders em partes |
|---|---|---|
| import do módulo + construção dos mobjects | 1× | **N×** |
| rasterização de frames de conteúdo | `Σ run_time × fps` | `Σ run_time × fps` (cada parte só os seus) |
| rasterização DESPERDIÇADA | 0 | **1 frame por `play` pulado**, em cada render |
| encode | 1 passagem | N passagens (cada uma curta) |

Ou seja: **N partes custam N passagens pela lógica da cena**, e o desperdício de
rasterização é **1 frame por `play` pulado**, não `run_time × fps`. Numa cena de
9 partes e ~60 plays, o pior render (a última parte) joga fora ~55 frames — o
equivalente a menos de um segundo de vídeo. **Uma parte sozinha é barata em
encode, nunca de graça em CPU.** [DECK] media a mesma coisa por fora e chegava a
"N passagens"; o fonte diz de onde vem o custo.

### 2.4 O que o mecanismo garante — e o que NÃO garante

| Garantido | Como |
|---|---|
| **o ESTADO** do palco na fronteira | é o mesmo código, executado do começo; `finish()` fecha toda animação pulada |
| a montagem só com o ato certo | `combine_to_movie` filtra os `None` |
| a decisão por `play`, não "grudada" | `skip_animations` é resetado a cada `play` |

| **NÃO** garantido | Consequência |
|---|---|
| o **QUADRO** na fronteira | o último frame da parte N e o primeiro da N+1 são frames **diferentes**: um é o fim de uma animação, o outro é o alfa 0 da seguinte. É §6, a armadilha da emenda |
| que exista mp4 | se TODA seção for pulada, `combine_to_movie` loga `"No animations are contained in this scene."` e **retorna sem escrever nada** — §10 |
| que a cena tenha animação | se `num_plays == 0`, `scene_finished` (`cairo_renderer.py:269-273`) desliga `write_to_movie`, liga `save_last_frame` e escreve um **PNG** — §10 |

---

## 3. O esqueleto

Copie, troque o nome, e leia as três notas abaixo dele — cada uma é uma falha
silenciosa.

```python
"""
<A tese da cena em uma frase.>

Partes (uma por RECADO FALADO — ver §4):
    1  <o que o apresentador diz nesta parte>
    2  ...
Consumo: <MinhaCena partes={N}>  — ver §11.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import FadeIn, FadeOut, Scene, Text, VGroup  # noqa: E402


class _AtosMinhaCena:                       # ← MIXIN. NÃO herda de Scene. §3.2
    """<Resumo dos atos. Esta docstring é lida por quem edita, não pelo aluno.>"""

    PAUSA_ENTRE_PARTES = 0.25               # respiro no FIM de cada ato — §5.5
    PARTE = 0                               # 0 = cena contínua, sem cortes

    def _corte(self, n: int) -> None:
        """Fronteira entre o ato n-1 e o ato n.

        O `wait` vem ANTES do `next_section` de propósito: assim ele pertence ao
        ato que TERMINA e some junto quando esse ato é pulado. Depois do corte
        ele viraria pausa morta na abertura da parte seguinte. §3.4.
        """
        if n > 1:
            self.wait(self.PAUSA_ENTRE_PARTES)
        self.next_section(
            f"ato{n}", skip_animations=(self.PARTE != 0 and n != self.PARTE)
        )

    def _troca_recado(self, anterior) -> None:
        """Tira o recado do ato que acabou — no COMEÇO da parte, nunca no meio.

        Saída antes de entrada: no mesmo `self.play` os dois textos se cruzam em
        meia opacidade e o palco pisca. E uma parte não troca o rodapé no meio —
        texto de apoio novo é fala nova, e fala nova é clique novo. §5.3.
        """
        if anterior is not None:
            self.play(FadeOut(anterior, run_time=0.3))

    def construct(self) -> None:
        self._corte(1)                      # SEMPRE a primeira linha do construct

        # ═══ PARTE 1 — <o recado, em português da fala> ═════════════════════
        ...
        self.wait(0.4)                      # cauda: máx 0,4 s

        self._corte(2)
        # ═══ PARTE 2 — <o recado> ═══════════════════════════════════════════
        ...
        self.wait(0.8)                      # só a ÚLTIMA parte fecha em ~0,8 s


# ─────────────────────────────────────────────────────────────────────────────
# As partes. Uma classe por parte, `PARTE = N`, nome terminando em `PN`.
#   MinhaCenaP1 → minha-cena-p1.mp4 (+ os dois png — §11)
#
#   minha-cena-p1.mp4   <o recado desta parte, em uma linha>
#   minha-cena-p2.mp4   ...
# ─────────────────────────────────────────────────────────────────────────────


class MinhaCenaP1(_AtosMinhaCena, Scene):   # ← mixin PRIMEIRO. §3.3
    """Parte 1/N — <o recado>."""

    PARTE = 1


class MinhaCenaP2(_AtosMinhaCena, Scene):
    """Parte 2/N — <o recado>."""

    PARTE = 2
```

### 3.1 `sys.path.insert` — redundante no render, necessário fora dele

**[FONTE]** os dois descobridores já inserem o diretório do arquivo em
`sys.path`: `manimx/render.py:130-134` e
`manim/utils/module_ops.py:63`. Então a linha é **redundante quando o render
importa a cena** — e **necessária** quando um script auxiliar (um medidor, um
conferidor) faz `import tema` direto. Mantenha, com esta nota: sem ela, alguém a
remove como código morto e quebra as ferramentas.

### 3.2 O mixin NÃO pode herdar de `Scene` — e isto é verificável

Se herdasse, os dois descobridores o listariam como cena e o pipeline
renderizaria a explicação inteira de novo, por engano, gerando um
`_atos-minha-cena.mp4` de ~35 s que ninguém consome. **[FONTE]**, as duas
condições:

```python
# manimx/render.py:141-145
classes = [obj for _, obj in inspect.getmembers(module, inspect.isclass)
           if issubclass(obj, Scene) and obj.__module__ == module_name]

# manim/utils/module_ops.py:75-81
inspect.isclass(obj) and issubclass(obj, Scene) and obj != Scene \
    and obj.__module__.startswith(module.__name__)
```

`issubclass(obj, Scene)` é a única peneira que interessa: uma classe sem base
`Scene` é **invisível** para ambos. Não confie no `_` do nome — é convenção, não
filtro.

Conferir custa 0,2 s e não renderiza nada:

```bash
bin/mx scenes aulas/001-multi-work/manim/aula_001_worktrees.py
# WorktreesP1  (_AtosWorktrees, CenaAula)  — Parte 1/9 — a pasta de hoje…
```

**[FONTE]** `manimx/cli.py:192-199`: a saída traz `name`, **`bases` na ordem
declarada** e a primeira linha da docstring. Ou seja, esse comando confere §3.2
**e** §3.3 de uma vez. Nenhum nome começando com `_` pode aparecer.

### 3.3 A ordem das bases é load-bearing, e falha em silêncio

`class MinhaCenaP1(_AtosMinhaCena, Scene)` — **mixin primeiro**. Invertida, o MRO
resolve `construct` em `Scene`, cujo corpo é só docstring
(**[FONTE]** `scene/scene.py:319-340`: nenhuma instrução) — a cena não faz nada,
e não há erro.

**[HOJE]** reproduzido em Python puro, sem manim, sem render:

```python
class Scene:
    def construct(self): return "Scene.construct (VAZIO)"
class CenaAula(Scene): pass
class Atos:
    def construct(self): return "Atos.construct (o conteudo)"

class Certo(Atos, CenaAula): pass       # MRO: Certo, Atos, CenaAula, Scene, object
class Errado(CenaAula, Atos): pass      # MRO: Errado, CenaAula, Scene, Atos, object
```

Saída medida: `Certo` → `"Atos.construct (o conteudo)"`; `Errado` →
`"Scene.construct (VAZIO)"`. A linearização C3 põe `Scene` **antes** do mixin
quando a base concreta vem primeiro, e `Scene.construct` ganha.

O sintoma no disco não é "mp4 de 0 s": com `num_plays == 0`, **[FONTE]**
`cairo_renderer.py:269-273` troca a saída por uma imagem
(`config.save_last_frame = True; config.write_to_movie = False`). Você fica com
**um PNG onde deveria haver um mp4** — e, se um mp4 antigo existir no caminho, com
o mp4 **velho**. ([DECK] relatou "vídeo de ~0 s"; a causa-raiz é a mesma, o
observável depende de haver arquivo anterior. Não executei.)

### 3.4 O `wait` mora ANTES do corte

`self.wait()` é um `play` (**[FONTE]** `scene.py:1249-1252`), logo pertence a uma
seção. Antes do `next_section`, ele é do ato que termina — e desaparece junto
quando esse ato é pulado. Depois, seria 0,25 s de tela parada na ABERTURA da
parte seguinte, exatamente onde o apresentador já está falando.

Duas cautelas do fonte, para caudas:

- `Scene.wait(0)` **levanta `ValueError`** — `validate_run_time` recusa
  `run_time <= 0` (`scene.py:1113-1123`, chamado em `scene.py:1249`). Cauda zero
  não existe: se não quer cauda, não escreva o `wait`;
- cauda **menor que `1/fps`** é **elevada** a `1/fps`, com warning alto.
  **Correção:** uma versão anterior desta linha dizia que ela grava *zero*
  frames e que o defeito é silencioso. As duas metades são falsas. `Scene.wait`
  chama `validate_run_time` **antes** de construir a `Wait` (`scene.py:1249`), e
  ela não só avisa como corrige:

  ```python
  # scene.py:1128-1137
  seconds_per_frame = 1 / fps
  if run_time < seconds_per_frame:
      logger.warning("... is too short for the current frame rate ... "
                     "Rendering with the shortest possible duration instead.")
      run_time = seconds_per_frame
  ```

  Logo `freeze_current_frame` recebe `1/fps` e
  `num_frames = int((1/fps)/(1/fps)) == 1`. A 60 fps, `self.wait(0.01)` grava
  **1 frame** e **grita no log**. Não é defeito calado; é uma cauda de 1 frame,
  curta demais para servir de frame parado, mas presente — e o pôster sai dela.

### 3.5 A variante em laço — quando três partes têm a mesma coreografia

Três atos com a mesma forma e só o número mudando não devem ser escritos três
vezes: a repetição é o que ensina a regra, e copiar-e-colar é convite a divergir.
Do deck (`aula_002_reversibilidade.py:452-505`, 3 partes num laço):

```python
for i in range(3):
    self._corte(2 + i)
    self._troca_recado(recado)
    ...                                    # a coreografia, idêntica
    recado = _recado(*recados_efeito[i])   # só o texto muda
    self.play(FadeIn(recado, run_time=RAPIDO))
    self.wait(0.4)
```

**O preço:** o conferidor estático de §8 não consegue provar a contiguidade dos
cortes quando o argumento é uma expressão — ele **avisa** e manda conferir à mão.
Foi exatamente o que aconteceu **[HOJE]** ao rodá-lo nos 11 arquivos do deck: 10
`ok`, e nesse um a nota `1 corte(s) com expressão (laço). Cortes literais:
[1, 5, 6, 7]; classes PN: [1..7]`. Use o laço quando ele economiza de verdade, e
saiba que trocou verificação automática por leitura.

### 3.6 O que NÃO vai no mixin

- **nada que dependa de `Scene`.** Se você precisa de `self.play` dentro de um
  helper do mixin, tudo bem (ele só existe em runtime, quando a subclasse já é
  `Scene`) — mas não escreva `super().__init__`, não herde, não anote tipo que
  force a base;
- **`PARTE` com valor diferente de 0.** O default do mixin é `0` = cena
  contínua; quem define é a subclasse;
- **título da cena.** §5.1.

---

## 4. Granulação: conte os RECADOS, não os segundos

**Uma parte = uma ideia FALADA.** Não é uma parte por ato, nem uma por `self.play`.

O procedimento, nesta ordem:

1. **Escreva o que você vai dizer**, frase a frase, antes de escrever a cena. Uma
   frase falada que se sustenta sozinha é um recado.
2. **Um recado = uma parte.** Dois recados numa parte = duas partes.
3. **Micro-beats do MESMO recado ficam juntos.** "a moldura entra → os arquivos
   caem em cascata → a pílula diz a branch" é UMA frase ("esta é a sua pasta, e
   ela está na main"), logo uma parte — mesmo sendo três `self.play`.
4. **Um acontecimento não se divide.** A pasta que se duplica E a árvore que
   ramifica no mesmo `self.play` são um beat só; cortar no meio destrói a
   explicação e ainda cai na armadilha da emenda (§6).

Diagnóstico de uma cena pronta:

| Sintoma | Leitura | Correção |
|---|---|---|
| parte com mais de ~7 s | provavelmente dois recados | divida no ponto de repouso do meio |
| parte com menos de ~1,5 s | micro-parte: gasta um clique para nada | funda com a vizinha do MESMO recado |
| você narra a parte com "e aí… e também…" | dois recados | divida |
| o rodapé troca no meio da parte | dois recados, garantido | divida (§5.3) |
| menos de 5 partes numa cena explicativa | cada parte é um assunto duplo | subdivida |
| mais de ~14 numa cena de ~35 s | micro-partes | funda por recado |

**A faixa, com a origem.** [DECK], contado **[HOJE]** no disco: as 10 cenas em
partes do consumidor ficaram entre **5 e 14** partes, mediana **7,5**;
distribuição `5, 5, 6, 6, 7, 8, 8, 9, 9, 14`. Duração por parte **1,4 a 6,7 s**,
mediana 3,7 s [DECK, não remedido aqui — exigiria `ffprobe`]. Os dois excessos
foram devolvidos pelo apresentador: **4 partes** = "muita coisa de cada vez";
**17–18** = "muitas micro partes".

Trate 5–14 como **faixa observada de UM palco**, não como regra. O que transfere
é o critério (um recado = uma parte); o número é consequência do assunto e de
quem fala. Versões anteriores desta skill diziam "5–10" e "7 cenas, 52 partes" —
números de um inventário que já envelheceu duas vezes. **Não abra uma terceira
contagem:** se precisar de número, conte no disco na hora.

**O custo de errar para cima é real:** cada parte é um mp4 + dois png no
repositório do consumidor e uma passagem inteira pela lógica da cena a cada
render (§2.3). 18 partes não é só ruim de apresentar — é caro de manter.

---

## 5. As regras de palco (todas vieram de devolução)

### 5.1 SEM TÍTULO NEM SUBTÍTULO dentro do vídeo

O slide já tem título; o do vídeo duplica e rouba um quinto do quadro. O contexto
é responsabilidade do **título do slide**. Recentre o conteúdo — faixa morta no
topo é defeito, não respiro.

No deck isso apareceu como uma migração documentada em duas linhas: *"TODAS as
constantes de Y abaixo já estão +0,8 ACIMA dos valores da versão com título. Se o
título voltar um dia, desça tudo −0,8."* Se o seu tema tem um helper
`self.titulo(...)`, **nenhuma cena em partes o chama** — e vale deixar isso
escrito onde o próximo procura.

### 5.2 Saída ANTES da entrada

Informação velha e nova nunca se cruzam no mesmo `self.play`: o crossfade dá uma
"piscada" no palco. O `FadeOut` completa num play; o `FadeIn` começa no seguinte.
Nas cenas do deck isso virou um método (`_troca_recado`, §3) justamente para que
não haja onde errar.

### 5.3 UMA PARTE NÃO TROCA O RODAPÉ NO MEIO

Texto de apoio novo é fala nova, e fala nova é clique novo. Nasceu de **quatro
devoluções seguidas na mesma cena** ("mostra um texto e depois ele é trocado por
outro", "troca o texto embaixo muito rápido").

É o teste mais barato que existe para saber se uma parte tem uma ideia ou duas, e
o único que se resolve com `grep`:

```bash
# dois `_troca_recado` (ou dois FadeIn de rodapé) entre dois `_corte` = duas partes
awk '/_corte\(/{p=$0} /_troca_recado|FadeIn\(recado/{print NR": "p" -> "$0}' cena.py
```

**A variante disfarçada:** a parte que termina com um movimento que APAGA o que
ela mesma acabou de mostrar — uma janela descendo por cima do texto. Aquilo é a
**cabeça** da parte seguinte, não o rabo desta.

### 5.4 Sem jargão do projeto no rodapé

Nome de flag, de arquivo e de conceito interno vira **comentário no código da
cena** — que é para quem edita. Na tela vai a coisa dita em língua corrente. A
plateia lê de pé, uma vez, de longe.

E cada linha de apoio **abaixo de ~62 caracteres**, quebrada onde a FALA respira,
na mão — nunca deixe o Manim decidir a quebra. O limite físico medido no palco de
14,22 unidades é ~70; 62 dá folga para a fonte variar entre máquinas.

### 5.5 Caudas curtas

`PAUSA_ENTRE_PARTES = 0.25`; último `wait` de cada ato **≤ 0,4 s**; só a última
parte da cena fecha em ~0,8 s. O player segura o frame final parado de qualquer
forma, e cauda longa **atrasa o sinal de "terminou"** que o apresentador usa para
saber que o palco é dele.

**[HOJE]**, auditado estaticamente nos 11 arquivos do deck: das 39 caudas
imediatamente anteriores a um `_corte`, **37 são `0.4` e 2 são `0.35`** — nenhuma
acima. E há exatamente **10 `self.wait(0.8)`**, um por mixin: o fecho de cada
cena. A disciplina é conferível por `grep`:

```bash
grep -B2 -h "self\._corte(" cena.py | grep -oE "self\.wait\([0-9.]+\)" | sort | uniq -c
```

### 5.6 Nada vaza, e nada sobrepõe num frame de REPOUSO

Palco padrão: **x ∈ [−7,11, +7,11]**, **y ∈ [−4, +4]** (frame 14,222 × 8,0). Uma
linha de rodapé acima de ~70 caracteres quebra em duas (`VGroup(...).arrange(DOWN)`).

O que é específico deste formato: em vídeo contínuo, uma sobreposição de 1/60 s
não é vista por ninguém. **No fim de uma parte, o quadro fica PARADO por dez
segundos enquanto alguém fala.** Todo defeito de layout que o vídeo contínuo
perdoa, o frame de repouso publica. A conferência de enquadramento em si é de
**`manim-layout-posicionamento`**; a regra daqui é *onde* olhar: o último frame
de cada parte.

### 5.7 Corte em ponto de REPOUSO

Depois de um `self.play` completo, nunca no meio de um `LaggedStart` que só faz
sentido inteiro. E — a mais cara delas — **nunca imediatamente antes de uma
animação que atravessa o que já está na tela**: é a §6.

### 5.8 O código é o produto tanto quanto o mp4

Cinco convenções observadas em todos os 11 arquivos do deck, sem exceção:

1. **docstring de arquivo** com a tese em uma frase, a lista numerada das partes
   com o recado FALADO de cada uma, a linha de consumo, e quais dados a cena toca;
2. **índice das partes repetido no rodapé do arquivo**, em kebab, imediatamente
   antes das classes `PN`;
3. **docstring por classe `PN`** com o denominador (`Parte 6/9 — …`);
4. **comentário por ato dizendo o recado falado**, em português da fala, não em
   jargão;
5. **comentário que explica por que uma escolha estranha existe**, com o defeito
   que ela evitou, plantado no ponto onde o próximo editor "consertaria" de volta.

O custo é real (os arquivos têm 25–44 KB). O retorno é que **inserir uma parte no
meio de uma cena de 9 vira uma operação segura** (§9.2). A armadilha embutida:
esses três textos (docstring, índice do rodapé, docstrings das classes) **mentem
em conjunto** quando alguém insere ou remove uma parte, e nenhum `grep` pega — é
por isso que §9 é um procedimento e não uma dica.

### 5.9 Geometria em constantes, antes do `construct`

Todo arquivo de cena do deck abre com 60–110 linhas de constantes nomeadas e um
mapa em ASCII das zonas, com o quadro declarado:

```python
# Geometria — coordenadas do Manim (quadro de 14,22 × 8: x de −7,11 a +7,11,
# y de −4 a +4). Nada aqui é em fração da tela: o quadro é fixo.
#
#   coluna esquerda            faixa dos fios         o sistema
#   ─────────────────────────────  y = −2,35  (a divisória do rodapé)
CENTRO_SISTEMA = [2.55, 0.80, 0]
BORDA_SISTEMA = -1.60   # x da borda esquerda: é onde os fios se prendem
```

Vale por si em qualquer cena, e vale **duas vezes** aqui: com o palco em
constantes, mover uma faixa inteira entre duas partes é editar um número, e o
enquadramento se revisa **lendo**, sem render.

E uma peça de desenho devolve o grupo **E as referências internas**:

```python
def _pasta(...) -> tuple[VGroup, VGroup, VGroup, VGroup]:
    """Devolve (grupo, moldura, linhas, selo). As três referências extras não são
    luxo: a parte 1 monta a pasta em tempos (moldura → linhas → selo) e o ato 2
    troca linhas e selo sem tocar no resto."""
```

`grupo[0][2]` no meio de um `self.play` quebra em silêncio quando alguém
acrescenta um submobject — e numa cena em partes isso é pior, porque uma parte
precisa animar exatamente uma peça de algo que **outra parte** construiu.

---

## 6. A armadilha da emenda

A emenda só é invisível se o **primeiro frame da parte N+1 for igual ao último da
parte N**. O mecanismo garante o **ESTADO**, não o **QUADRO** (§2.4) — e a
diferença aparece assim:

> Um ato abria com `TransformFromCopy(semente, pasta_b)`. **No alfa 0 a cópia é
> opaca e está exatamente EM CIMA do original**, com os glifos do destino
> interpolados para as posições da origem. Ela tapa o que o ato anterior
> construiu. Num vídeo contínuo isso dura 1/60 s e ninguém vê. Como **primeiro
> frame de uma parte**, é o quadro em que o vídeo fica PARADO esperando a fala —
> e o conteúdo aparece embolado, ou some.

**[FONTE]** `TransformFromCopy(mobject, target_mobject, **kwargs)` — a assinatura
confere; a cópia entra na cena no `begin()` da animação, com o estilo do alvo e a
geometria da origem.

**A família inteira**, para você reconhecer antes de cortar. Qualquer animação que
no alfa 0 desenha algo **opaco por cima do palco existente**:

| Animação | Por que tapa no alfa 0 |
|---|---|
| `TransformFromCopy(a, b)` | a cópia nasce opaca sobre `a` |
| `Transform(a, b)` / `ReplacementTransform(a, b)` | se `b` for maior que `a`, o interpolado cobre vizinhos |
| `FadeIn(x, shift=...)` de um objeto com `fill_opacity=1` grande | entra em opacidade baixa, mas o `shift` o traz de fora do quadro cruzando o resto |
| `GrowFromCenter` / `GrowFromEdge` de painel opaco | escala de 0, mas o retângulo já é sólido |
| `MoveAlongPath` de um objeto sólido | o trajeto atravessa a tela inteira |
| qualquer `.animate` que aumenta um objeto com `fill_opacity=1` | idem |

**A regra:** *não corte imediatamente antes de um movimento que atravessa ou cobre
o que já está na tela.* Corte **depois** dele, e deixe o comentário dizendo por
quê — senão o próximo a mexer "conserta" de volta. No deck, isso é literalmente um
bloco de comentário de 10 linhas dentro do `construct`, imediatamente acima do
`self._corte(7)`.

**O efeito colateral que você vai querer:** o comando/rótulo que ANUNCIA o beat
tem de morar na **mesma parte** que o beat. Se o beat não pode abrir uma parte, o
que vem antes dele também não pode fechar uma.

---

## 7. Medir a emenda — métrica DIRECIONAL, nunca RMS

### 7.1 Por que RMS falha

O RMS da diferença entre os dois frames acusa como defeito **a animação seguinte
COMEÇANDO** — que é o comportamento certo. [DECK]: a parte 2 de uma cena dava
RMS 4,4 e estava perfeita. Toda métrica simétrica tem esse falso positivo.

O único defeito que importa é **tinta que SOME**: algo que existia no último frame
da parte N e não existe no primeiro da N+1.

### 7.2 O medidor

Em fundo claro, "sumiu" = pixel que **clareou**:

```python
import numpy as np
from PIL import Image

a = np.asarray(Image.open("fim-da-parte-N.png").convert("L"), dtype=np.int16)
b = np.asarray(Image.open("inicio-da-N+1.png").convert("L"), dtype=np.int16)
sumiu = int(((b - a) > 24).sum())    # pixels que CLAREARAM = tinta removida
```

Pixels que ESCURECEM são a próxima animação entrando — **não contam**. É por isso
que a expressão é `b - a`, direcional, e nunca `abs()` nem RMS.

Varrendo um diretório inteiro, com a lista saindo do **disco** e não de um mapa
escrito à mão (um mapa desatualizado já mandou medir um `*-p10.mp4` inexistente e
estourou o `check=True`):

```python
import glob, os, re, subprocess
import numpy as np
from PIL import Image

D, T = "public/videos/", "/tmp/emenda-"

def frame(src, args, out):
    subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", *args,
                    "-i", D + src, "-update", "1", "-frames:v", "1", T + out],
                   check=True)

ult = {}
for p in glob.glob(D + "*-p*.mp4"):
    m = re.match(r"(.+)-p(\d+)\.mp4$", os.path.basename(p))
    if m:
        ult[m.group(1)] = max(ult.get(m.group(1), 0), int(m.group(2)))

pior = 0
for base, n in sorted(ult.items()):
    for k in range(1, n):
        frame(f"{base}-p{k}.mp4", ["-sseof", "-0.05"], "f.png")   # último de N
        frame(f"{base}-p{k+1}.mp4", [], "i.png")                  # primeiro de N+1
        a = np.asarray(Image.open(T + "f.png").convert("L"), dtype=np.int16)
        b = np.asarray(Image.open(T + "i.png").convert("L"), dtype=np.int16)
        sumiu = int(((b - a) > 24).sum())
        pior = max(pior, sumiu)
        if sumiu > 400:
            print(f"EMENDA COM PERDA: {base} p{k}->p{k+1}: {sumiu} px sumiram")
print(f"pior emenda: {pior} px  ({'REPROVA' if pior > 400 else 'ok'})")
```

Este script **lê arquivos que já existem** — ele nunca re-renderiza. `numpy` e
`Pillow` estão no `.venv` deste projeto.

### 7.3 O limiar, e como recalibrá-lo

**400 px em 2,07 M (1920×1080), fundo claro.** [DECK]: até aí é antialiasing;
acima, alguma coisa desapareceu na troca. A pior emenda medida no deck foi **118
px** — folga de 3,4×; emendas boas ficam entre **4 e 27 px**.

Três ajustes obrigatórios se o seu caso difere:

| Situação | Ajuste |
|---|---|
| outra resolução | o limiar escala com a ÁREA: 400 × (w·h / 2 073 600) |
| **fundo escuro** | o sinal inverte: `((a - b) > 24)` — tinta clara sobre fundo escuro SOME quando o pixel ESCURECE |
| cena colorida | `.convert("L")` pode empatar duas cores de luminância parecida; compare por canal e some |

**O falso positivo conhecido, e ele é traiçoeiro:** se você editou um ato e
re-renderizou **só** a parte dele, a parte anterior no disco ainda é a versão
velha, e a medição estoura. **Investigue antes de "consertar" a cena** — foi
assim que se achou um defeito real (um elemento invisível entrando na caixa
delimitadora e deslocando o grupo 4 px; ver §10). A ordem certa é: re-renderize o
alcance inteiro (§9.1), **depois** meça.

### 7.4 O pôster não pode estar vazio

O último frame da última parte é o pôster do PDF de backup e do
`prefers-reduced-motion` (§11.3). Se a cena fecha em `FadeOut`, o backup impresso
sai em página branca — e ninguém descobre antes do palco.

```python
a = np.asarray(Image.open(f"{base}-p{n}.png").convert("L"))
tinta = float((a < 235).mean())      # < 1 % é fade-out disfarçado
```

[DECK]: a cobertura das cenas do consumidor vai de **2,9 %** a **21 %**.

### 7.5 Extrair os frames sem `ffmpeg` — alternativa NÃO EXECUTADA

O ManimCE já traz um leitor de vídeo em PyAV: **[FONTE]**
`get_video_metadata(path_to_video) -> VideoMetadata` (`manim/utils/commands.py:47`)
abre o arquivo com `av.open` e devolve `width, height, nb_frames, duration,
avg_frame_rate, codec_name, pix_fmt` **sem chamar ffprobe**. Isso substitui o
`ffprobe` dos itens de checklist "duração por parte" e "resolução uniforme":

```python
from manim import get_video_metadata
print(get_video_metadata("public/videos/worktrees-p6.mp4"))
```

Pelo mesmo caminho dá para decodificar o primeiro e o último frame com `av`
diretamente. **Eu não executei nem o metadata nem a decodificação nesta sessão** —
a assinatura e a implementação estão lidas, o comportamento não foi observado.
Trate como caminho a validar, e mantenha o `ffmpeg` como o procedimento conhecido.

---

## 8. Conferir SEM renderizar — o conferidor estático

Metade dos defeitos deste formato é **estrutural** e se prova no texto do arquivo:
corte órfão, `PARTE` sem seção, MRO invertido, mixin herdando de `Scene`,
`_corte(1)` fora da primeira linha. Nada disso precisa de render, e todos falham
em silêncio.

O conferidor abaixo lê o arquivo com `ast` — **não importa o manim**, não
renderiza, roda em milissegundos. **[HOJE]** rodado nos 11 arquivos de cena do
deck: **10 `ok`**, 1 com a nota do laço (§3.5).

```python
#!/usr/bin/env python3
"""Confere uma cena em partes SEM importar o manim e SEM renderizar nada.
Uso:  python3 confere_partes.py cena.py [outra.py ...]     Sai 1 se reprovar."""

from __future__ import annotations
import ast, re, sys
from pathlib import Path


def _cortes(fn):
    """Números LITERAIS passados a self._corte(n), na ordem textual."""
    ns = []
    for no in ast.walk(fn):
        if (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)
                and no.func.attr == "_corte" and no.args
                and isinstance(no.args[0], ast.Constant)
                and isinstance(no.args[0].value, int)):
            ns.append(no.args[0].value)
    return ns


def _dinamicos(fn):
    """Quantos self._corte(<expressão>) existem — o laço `_corte(2 + i)`."""
    return sum(
        1 for no in ast.walk(fn)
        if (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)
            and no.func.attr == "_corte" and no.args
            and not isinstance(no.args[0], ast.Constant))
    )


def confere(caminho: Path) -> list[str]:
    arvore = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    erros: list[str] = []
    classes = {n.name: n for n in arvore.body if isinstance(n, ast.ClassDef)}
    mixins = {nome: c for nome, c in classes.items()
              if any(isinstance(f, ast.FunctionDef) and f.name == "_corte" for f in c.body)}
    if not mixins:
        return []                                   # não é cena em partes

    for nome_mixin, mixin in mixins.items():
        bases = [ast.unparse(b) for b in mixin.bases]
        suspeitas = [b for b in bases if "Scene" in b or "Cena" in b]
        if suspeitas:
            erros.append(f"{nome_mixin}: mixin herda de {suspeitas} — `mx scenes` "
                         f"vai listá-lo e o pipeline renderiza a cena inteira por engano")

        construct = next((f for f in mixin.body
                          if isinstance(f, ast.FunctionDef) and f.name == "construct"), None)
        if construct is None:
            erros.append(f"{nome_mixin}: sem `construct`")
            continue

        corpo = [s for s in construct.body
                 if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
        if not (corpo and isinstance(corpo[0], ast.Expr)
                and isinstance(corpo[0].value, ast.Call)
                and getattr(corpo[0].value.func, "attr", None) == "_corte"):
            erros.append(f"{nome_mixin}: `self._corte(1)` não é a primeira linha do construct")

        ns, din = _cortes(construct), _dinamicos(construct)
        if sorted(ns) != ns:
            erros.append(f"{nome_mixin}: cortes fora de ordem textual: {ns}")
        if len(set(ns)) != len(ns):
            erros.append(f"{nome_mixin}: corte repetido: "
                         f"{sorted({n for n in ns if ns.count(n) > 1})}")

        partes: dict[int, str] = {}
        for nome_cls, cls in classes.items():
            bn = [ast.unparse(b) for b in cls.bases]
            if nome_mixin not in bn:
                continue
            if bn[0] != nome_mixin:
                erros.append(f"{nome_cls}: bases em {bn} — o mixin tem de vir PRIMEIRO, "
                             f"senão o MRO resolve `construct` em Scene e nada é escrito")
            valor = next((s.value.value for s in cls.body
                          if isinstance(s, ast.Assign) and len(s.targets) == 1
                          and isinstance(s.targets[0], ast.Name)
                          and s.targets[0].id == "PARTE"
                          and isinstance(s.value, ast.Constant)), None)
            if valor is None:
                erros.append(f"{nome_cls}: sem `PARTE = n`")
                continue
            if valor in partes:
                erros.append(f"{nome_cls}: PARTE = {valor} duplica {partes[valor]}")
            partes[valor] = nome_cls
            m = re.search(r"P(\d+)$", nome_cls)
            if m and int(m.group(1)) != valor:
                erros.append(f"{nome_cls}: nome diz P{m.group(1)} mas `PARTE = {valor}`")

        if din == 0:
            cortes = set(ns)
            if sorted(set(partes) - cortes):
                erros.append(f"{nome_mixin}: PARTE {sorted(set(partes) - cortes)} não casa "
                             f"com corte nenhum — TODAS as seções serão puladas e "
                             f"NENHUM mp4 é escrito")
            if sorted(cortes - set(partes)):
                erros.append(f"{nome_mixin}: corte {sorted(cortes - set(partes))} sem classe PN")
            if cortes and sorted(cortes) != list(range(1, max(cortes) + 1)):
                erros.append(f"{nome_mixin}: cortes não são 1..N contíguos: {sorted(cortes)}")
        else:
            erros.append(f"{nome_mixin}: NOTA — {din} corte(s) com expressão (laço). "
                         f"Literais: {sorted(set(ns))}; classes PN: {sorted(partes)}. "
                         f"Confira à mão.")
    return erros


def main(argv):
    ruim = 0
    for arg in argv[1:]:
        p = Path(arg)
        erros = confere(p)
        if erros:
            ruim = 1
            for e in erros:
                print(f"{p.name}: {e}")
        else:
            print(f"{p.name}: ok")
    return ruim


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
```

### 8.1 O que ele pega — provado por injeção de defeito

**[HOJE]**, injetando cada defeito numa cópia de uma cena real de 9 partes:

| Defeito injetado | Saída do conferidor |
|---|---|
| renumeração com o laço errado (§9.2) | `PARTE [9] não casa com corte nenhum — TODAS as seções serão puladas e NENHUM mp4 é escrito` + `corte [10] sem classe PN` + `cortes não são 1..N contíguos: [1, 2, 3, 4, 5, 6, 7, 8, 10]` |
| mixin com `class _AtosX(CenaAula)` | `mixin herda de ['CenaAula'] — mx scenes vai listá-lo…` |
| bases invertidas nas 9 subclasses | 9 linhas `bases em ['CenaAula', '_AtosWorktrees'] — o mixin tem de vir PRIMEIRO…` |
| `PARTE = 33` numa classe `…P3` | `nome diz P3 mas PARTE = 33` + `PARTE [33] não casa com corte nenhum` + `corte [3] sem classe PN` |

### 8.2 O que ele NÃO pega

Escreva isso onde você o guardar, para ninguém confiar demais:

- **cortes em laço** — ele avisa e para (§3.5);
- **o alcance do re-render** — é semântico (§9.1);
- **um recado a mais na parte** — é sobre a FALA, não sobre o código; o único
  proxy é o `awk` de §5.3;
- **a emenda** — precisa dos frames (§7);
- **enquadramento, cor, sobreposição** — precisa OLHAR o PNG
  (**`manim-verificacao-visual`**).

### 8.3 Os greps de bolso

```bash
# a sequência de cortes, com o buraco visível
grep -oE '_corte\([0-9]+\)' cena.py | sort -t'(' -k2 -n | uniq

# classes PN × cortes
grep -cE '^class [A-Za-z0-9]+P[0-9]+\(' cena.py
grep -c '_corte(' cena.py

# o mixin não pode aparecer aqui, e as bases saem na ordem declarada
bin/mx scenes cena.py

# ninguém chamou o título dentro de uma cena em partes
grep -n 'self\.titulo(' cena.py
```

---

## 9. Manutenção

O formato existe para o palco, mas o que ele paga de volta todo dia é **edição
barata**: o ato errado é um trecho identificado do `construct`, e o vídeo dele é
um arquivo com nome próprio.

### 9.1 Editar UMA parte — a tabela de alcance

Não é o tamanho da edição que decide. **É o que ela deixa na tela no instante do
corte.**

| A sua edição no ato 5 | Re-renderize |
|---|---|
| só ritmo: `run_time`, `rate_func`, um `wait` interno | **só a P5** |
| algo que entra e SAI dentro do próprio ato 5 | **só a P5** |
| qualquer coisa que **sobreviva** ao ato 5 — moveu, recoloriu, acrescentou ou apagou um elemento que continua na tela | **P5 até a ÚLTIMA** |
| texto de rodapé, número, geometria do palco | **P5 até a ÚLTIMA** |

O motivo não é o vídeo da parte 5, é o da 6: `…-p6.mp4` é produzido pelo render
de `…P6`, que replica o ato 5 **antigo** enquanto você não o refizer. O resultado
é a emenda quebrando no pior lugar possível — a parte 5 termina no estado novo, a
6 abre no velho, e o salto acontece no **frame parado**, com o apresentador
falando por cima. Na dúvida, `P5..P9`: o custo é linear e o erro é silencioso.

Duas coisas que **não** se atualizam ao renderizar uma parte só:

- **o pôster da última parte** — o que vai para o PDF de backup. Editou um ato
  cujo desenho sobrevive até o fim? O PDF continua com o quadro velho até a última
  parte ser refeita, e isso não aparece na tela;
- as partes anteriores, que estão certas e devem mesmo ficar como estão.

Depois, **re-meça as DUAS emendas vizinhas** (P4→P5 e P5→P6) com §7.

### 9.2 Inserir uma parte no meio

Exemplo: uma parte nova entre a 5 e a 6, numa cena de 9. **A ordem importa** — a
inversão dos dois primeiros passos renumera duas vezes.

**1. Renumere os cortes seguintes PARA CIMA, de trás para frente.** De trás para
frente porque `6→7` antes de `7→8` transformaria a mesma linha duas vezes:

```bash
f=cena.py
for n in 9 8 7 6; do sed -i -E "s/_corte\($n\)/_corte\($((n+1))\)/" "$f"; done
grep -oE '_corte\([0-9]+\)' "$f" | sort -t'(' -k2 -n | uniq    # confira o buraco
```

> **O laço da remoção NÃO é o inverso deste.** Cada um está certo para o seu
> caso, e por isso mesmo eles não se cancelam. Depois da inserção os cortes são
> `1..5, 7..10`, e `for n in 6 7 8 9` **nem alcança o `_corte(10)`** — sobra um
> corte órfão. Como `_corte` faz
> `skip_animations=(self.PARTE != 0 and n != self.PARTE)`, a classe `…P9` deixa de
> casar com seção nenhuma, **TODAS** são puladas, e nada é escrito.
>
> Para DESFAZER só este passo, o laço é `for n in 7 8 9 10; do … $((n-1)) …`.
> **[HOJE]** reproduzido sobre uma cena real de 9 partes: inserção seguida do
> inverso CORRETO devolve o arquivo byte a byte (`diff` mudo); com `6 7 8 9` o
> `diff` acusa exatamente `_corte(9)` → `_corte(10)`, e o conferidor de §8 imprime
> as três linhas da tabela em §8.1.

**2. Só então insira o corte novo**, num ponto de REPOUSO, com a cauda do ato que
passa a terminar ali:

```python
        self.wait(0.4)   # cauda: máx 0,4 s
        self._corte(6)
```

**3. NÃO renomeie classe nenhuma. Acrescente UMA no fim:** `…P10`, com
`PARTE = 10`. Aqui é onde a intuição erra — a tentação é criar um `…P5b` ou
renomear em cadeia, e nenhuma das duas coisas existe neste formato. **As classes
são POSIÇÕES, não conteúdos:** a partir da inserção, o significado de cada uma
desliza sozinho (`…P6` passa a renderizar o ato novo, `…P7` o que era da P6, e
assim por diante). Não existe `P5b`.

**4. Acerte o texto que agora mente** — e cuidado, aqui NÃO é só trocar número. O
denominador (`Parte N/9` → `N/10`) muda em todas as dez, mas **a DESCRIÇÃO de
cada docstring acompanha o CONTEÚDO, não a posição**: a descrição da antiga P6
DESCE para a P7, e a P6 recebe a do ato novo. Vale também para o índice de partes
no rodapé do arquivo e para o resumo do mixin (§5.8).

**5. Re-renderize da inserção até o fim.** As partes 1 a 5 continuam válidas —
nada antes do corte novo mudou.

**6. Só DEPOIS avise o consumidor** que agora são 10. Invertido, o player pede um
`…-p10.mp4` que ainda não existe. §11.

**7. Meça as emendas novas** (5→6 e 6→7). As demais são os mesmos frames de antes.

Inserir **não deixa órfão**: N só cresce.

### 9.3 Remover ou fundir uma parte

O caso comum é fundir uma micro-parte na vizinha. Fundir a 5 na 4, na cena de 9:

**1. Apague `self._corte(5)`** e, com ele, **a cauda `self.wait(0.4)`
imediatamente anterior** — senão sobram 0,65 s de pausa morta no meio do ato
fundido (a cauda mais o `PAUSA_ENTRE_PARTES` que o corte somava).

**2. Renumere os seguintes PARA BAIXO, agora de frente para trás:**

```bash
for n in 6 7 8 9; do sed -i -E "s/_corte\($n\)/_corte\($((n-1))\)/" "$f"; done
```

**3. Apague a ÚLTIMA classe (`…P9`), não a `…P5`.** Mesma lógica invertida da
inserção: você tira uma posição do fim, e o conteúdo se redistribui sozinho.

**4. Docstrings:** denominador `N/9` → `N/8` em todas, e as descrições **SOBEM**
uma posição a partir da fusão. A parte fundida ganha a descrição dos dois recados
que agora são um — e se você não consegue escrever essa descrição numa frase, a
fusão estava errada (§4).

**5. Re-renderize da fusão até o fim** (P4..P8).

**6. Apague os órfãos.** Os arquivos da antiga parte 9 continuam no disco.
Sobrando sempre são os de índice **maior** que a contagem de classes:

```bash
ls public/videos/cena-p9.*        # mp4 + os dois png
```

**Apagar um ATO inteiro (e não só o corte) é o único caso desta skill que falha
ALTO:** os atos seguintes referenciam os mobjects que o ato apagado criava, e o
Python levanta `NameError` no render. Aproveite — é a única rede que o
interpretador te dá aqui.

### 9.4 Depois de qualquer uma das três operações

```bash
python3 confere_partes.py cena.py     # §8 — estrutura
bin/mx scenes cena.py                 # §3.2 — nenhum `_` na lista, bases na ordem
# … re-render do alcance …
python3 mede_emendas.py               # §7 — nenhuma linha EMENDA COM PERDA
```

---

## 10. O que quebra CALADO

Tabela mestre. A coluna do meio é o que você **observa**; a da direita é o que
**pega**.

| Defeito | Sintoma observável | Como pegar |
|---|---|---|
| **corte órfão** (`PARTE` sem seção correspondente) | **[FONTE]** todas as seções são puladas → `combine_to_movie` vê 0 arquivos parciais, loga `"No animations are contained in this scene."` e **retorna sem escrever mp4**. `mx render` sai **0** com `success: true` e `output_file: null` — ou, se um mp4 antigo estiver no caminho, reporta o **arquivo velho** (`manimx/render.py:441`: `elif movie and Path(movie).exists()`) | §8, em 20 ms |
| **bases na ordem errada** | **[FONTE]** `num_plays == 0` → `cairo_renderer.py:269-273` desliga `write_to_movie` e grava um **PNG** em `media/images/…`. Nenhum mp4 novo; nenhum erro | §8; ou `bin/mx scenes` (as bases saem na ordem) |
| **mixin herdando de `Scene`** | `mx scenes` lista `_AtosX`, e um render de lote cospe um mp4 de ~35 s que ninguém consome | §8; `bin/mx scenes \| grep '^_'` |
| **corte imediatamente antes de animação que atravessa a tela** | a parte abre num quadro PARADO com algo tapado ou embolado — e é nesse quadro que se fala | §7, métrica direcional |
| **editou o ato N, re-renderizou só a parte N** | a emenda N→N+1 salta: N termina no estado novo, N+1 abre no velho | §7 — mas cuidado com o falso positivo de §7.3 |
| **editou qualquer ato e não refez a ÚLTIMA parte** | só o PDF de backup sai com o desenho antigo; na tela está tudo certo | conferir o pôster da última parte (§7.4) |
| **cena fechando em `FadeOut`** | pôster quase branco → página em branco no PDF | §7.4 |
| **último `wait` longo demais** | nada quebra — o apresentador espera calado e a plateia acha que travou | §5.5, o `grep` das caudas |
| **a parte troca o rodapé no meio** | **nenhum defeito na tela.** O defeito acontece na FALA, e só aparece no palco | §5.3, o `awk` dos recados |
| **elemento invisível na caixa delimitadora** | um detalhe transparente (lingueta, espaçador) continua contando no bounding box; `VGroup.move_to()` desloca o grupo inteiro por causa dele — **4 px, medidos, silenciosos**. Posicione pelo CORPO visível, não pelo grupo | §7 acusa como perda de tinta na emenda |
| **preview rápido comitado por cima do final** | 720p30 no repositório; visivelmente mole no projetor | `get_video_metadata` de cada mp4 (§7.5) — esperado **uma** resolução/fps |
| **cauda menor que `1/fps`** | **[FONTE]** `validate_run_time` ELEVA para `1/fps` e emite warning — grava **1** frame, e falha ALTO no log, não calado. Cauda de 1 frame não segura o olho | `grep 'self.wait(0.0'`, e o warning "too short for the current frame rate" no log |
| **`self.wait(0)`** | `ValueError` de `validate_run_time` — este falha ALTO | o render para |

---

## 11. Entregar ao consumidor

### 11.1 Três arquivos por parte

O player de um deck precisa, **por parte**:

| Arquivo | Para quê |
|---|---|
| `nome-pN.mp4` | o vídeo |
| `nome-pN.png` (**último** frame) | pôster do PDF, do `prefers-reduced-motion` e do estado "terminou" |
| `nome-pN-inicio.png` (**primeiro** frame) | pôster do `<video>` da parte N **durante a troca** — como o primeiro frame da parte N é o último da N−1, é a imagem que já está na tela. Sem ele, a troca pisca |

Isso é requisito **do render**, não do player: o pipeline tem de produzir os três.

### 11.2 Nome: a classe manda

Classe `MinhaCenaP3` → `minha-cena-p3.mp4`. PascalCase → kebab, com o segundo
`s///` tratando siglas (`OndeVaiODinheiro` → `onde-vai-o-dinheiro`):

```bash
slug() {
  printf '%s' "$1" | sed -E 's/([a-z0-9])([A-Z])/\1-\2/g; s/([A-Z]+)([A-Z][a-z])/\1-\2/g' \
    | tr '[:upper:]' '[:lower:]'
}
```

**Convenção substitui configuração:** zero mapeamentos para manter, e a lista de
cenas sai de `mx scenes … --json`, nunca de um mapa escrito à mão. O script de
lote completo é de **`manim-batch-pipeline`**.

### 11.3 Os dois pôsteres têm flags DIFERENTES, e uniformizá-las quebra calado

```bash
# ÚLTIMO frame — SEM `-frames:v 1`
ffmpeg -nostdin -loglevel error -y -sseof -1 -i "$n.mp4" -update 1 "$n.png"

# PRIMEIRO frame — COM `-frames:v 1`, SEM `-sseof`
ffmpeg -nostdin -loglevel error -y -i "$n.mp4" -frames:v 1 "$n-inicio.png"
```

`-sseof -1 -frames:v 1` grava o **primeiro frame depois do seek** — o de 1 s antes
do fim — e para. Numa parte que fecha com um `FadeIn` de rodapé, o pôster sai com
o texto lavado enquanto o vídeo está perfeito. [DECK]: esse defeito durou meses.
Só `-update 1` (sobrescreve a cada frame) deixa o **último** no disco.

**Não use `mx render --format png` para isto:** ele também dá o último frame, mas
**re-renderiza a cena inteira**. O ffmpeg lê o arquivo que já existe.

**Consequência de projeto, não de pipeline:** o último frame vira o pôster do PDF,
então **nenhuma parte pode fechar em `FadeOut`** — e a última, menos ainda.

### 11.4 O que entra no git

[DECK], a política que a segunda aula adotou depois da primeira: **`.mp4` fora do
git, `.png` dentro.** O raciocínio: o mp4 é derivado e o `.py` versionado o
reconstrói; o png é **pôster**, e sem ele o fallback estático não existe.
Número de apoio para estimar antes de decidir: **0,29 MB por segundo** de vídeo
1080p60/NVENC em média, dispersão de 0,07 (cena quase estática) a 0,66 (palco
inteiro em movimento). O assunto peso/codec é de **`manim-gpu-encoding`**.

---

## 12. Onde esta skill para

Escreva o formato aqui; para o resto, vá à dona. Onde a matéria já existe do lado
de lá, **aponte, não reescreva**.

| Você precisa de | Skill |
|---|---|
| a API genérica de seções (`Section`, `DefaultSectionType`, `--save_sections`, o JSON do Segmented Video API) e o mapa das 13 classes de `Scene` | `manim-cenas-secoes` |
| `rate_func`, `run_time`, `lag_ratio`, `AnimationGroup`/`Succession`/`LaggedStart`, `path_func`, orçamento de tempo | `manim-composicao-ritmo` |
| o catálogo de animações e `Transform` × `ReplacementTransform` | `manim-animations` |
| "cabe na tela?", margem, `to_edge`, `arrange`, z-index, 9:16 | `manim-layout-posicionamento` |
| escolher qualidade/formato, achar o caminho do arquivo, `-n a,b` | `manim-render-api` |
| codec, NVENC, peso do mp4, `--rapido` × entrega | `manim-gpu-encoding` |
| o script que renderiza o lote, o slug, os pôsteres, o exit code | `manim-batch-pipeline` |
| paralelismo entre processos e o teto de sessões de encode | `manim-batch-pipeline` + `manim-gpu-encoding` |
| OLHAR o PNG, o ciclo escrever→render rápido→olhar→corrigir | `manim-verificacao-visual` |
| um `tema.py` como contrato (paleta, fonte, escala, classe-base, dado externo) | `manim-tema-projeto` |
| cor, contraste, "sumiu no fundo branco" | `manim-color-theming` |
| texto nítido (o arredondamento de X do cairo), `Text`/`Tex`/`t2c` | `manim-text-latex` |
| cache, `--no-cache`, hash que não enxerga dado externo | `manim-performance-cache` |
| descobrir se um nome/kwarg existe | `manim-api-discovery` |
| traceback, bissecção, erro de ambiente | `manim-troubleshooting` |

**Nomes:** ressalva fechada. As 27 skills existem no disco e a tabela de
roteamento é `manim-project` **§13** (não §12). Os nomes provisórios citados
numa versão anterior **nunca existiram**; os reais são
**`manim-composicao-ritmo`** (ritmo), **`manim-cenas-secoes`** (seções),
**`manim-layout-posicionamento`** (enquadramento) e **`manim-som-legendas`**
(áudio e legenda).

**Buracos declarados** — se o pedido cair aqui, diga que não tem skill em vez de
improvisar: ênfase e anotação (`Flash`, `Indicate`, `Circumscribe`, `Brace*`,
`SurroundingRectangle`); `Code`/`Typst`/`Paragraph` na tela; campos e fluxo;
`LinearTransformationScene`/`VectorScene`; os 48 mobjects `OpenGL*`.

**Do lado do consumidor:** o player, o componente de slide, a troca de `<video>` e
a política de `.gitignore` do deck são do repositório `~/Projects/aulas` (skill
`aula-videos`). Onde o número de partes divergir entre as duas skills, **vale o
inventário contado no disco na hora** — não abra uma terceira contagem.

---

## 13. O que NÃO foi verificado nesta sessão

Escrito porque uma afirmação marcada como não verificada vale mais que uma
afirmação falsa:

- **nenhum render foi executado.** Nada de `mx render`, `manim`, `ffmpeg`,
  `ffprobe` ou GPU. Toda a mecânica de §2 vem de LEITURA do fonte do ManimCE
  0.21.0 instalado, com arquivo e linha;
- os **limiares e números de pixel** de §7 (400 px, 118 px de pior emenda, 4–27 px
  de emenda boa, cobertura de tinta 2,9–21 %) são [DECK], de outra sessão. O
  raciocínio da métrica foi conferido; os valores, não remedidos;
- as **durações por parte** (1,4 a 6,7 s) são [DECK] — remedi-las exigiria
  `ffprobe`;
- os **0,29 MB/s** de §11.4 são [DECK];
- as **flags de ffmpeg** de §11.3 não foram executadas aqui; a semântica de
  `-sseof`/`-update`/`-frames:v` é a documentada, e o defeito é [DECK];
- o caminho **PyAV** de §7.5 (`get_video_metadata` e decodificação de frame sem
  ffmpeg) está lido no fonte e **não executado**;
- o sintoma exato do MRO invertido no disco (**PNG em vez de mp4**) é dedução
  direta de `cairo_renderer.py:269-273`; [DECK] relatou "mp4 de ~0 s". A
  causa-raiz é a mesma; **o observável depende de haver arquivo anterior no
  caminho, e eu não confirmei rodando**.

O que **foi** reproduzido nesta sessão, com `sed`, `grep`, `ast` e Python puro:
o inventário do deck (11 arquivos, 10 mixins, 77 classes `PN`, 75 `_corte`
textuais, 77 mp4, 154 png), a auditoria das caudas (37×0,4 + 2×0,35, e 10×0,8),
o conferidor de §8 nos 11 arquivos, a injeção dos quatro defeitos de §8.1, a
reprodução byte a byte do laço de renumeração errado, e a prova de MRO de §3.3.
