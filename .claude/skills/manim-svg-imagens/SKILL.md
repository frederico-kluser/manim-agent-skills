---
name: manim-svg-imagens
description: >-
  Trazer arquivo de FORA para dentro da cena do Manim: `SVGMobject` (logo,
  ícone, diagrama vetorial), `ImageMobject` (PNG, JPG, print de tela, foto,
  array numpy), imagem como fundo de cena, textura dentro de uma forma, e o
  `.ttf` do projeto por `register_font`. Use quando o pedido citar um ARQUIVO
  que a cena precisa carregar: "põe a logo da empresa nesse vídeo", "coloca o
  ícone do Docker/Python/GitHub", "insere esse print da tela", "usa essa foto
  de fundo", "quero o SVG do Inkscape/Figma/Illustrator dentro da animação",
  "carrega esse PNG", "essa imagem está gigante/minúscula/borrada/serrilhada",
  "o SVG não abriu", "OSError could not find", "o SVG entrou todo preto / todo
  branco / invisível", "sumiu o texto do meu SVG", "o gradiente do SVG virou
  nada", "o contorno do ícone desapareceu", "quero pintar só uma parte do
  logo", "TypeError Only values of type VMobject can be added as submobjects of
  VGroup", "Create only works for VMobjects", "Mobject pixel array shapes
  incompatible", "a imagem some quando eu giro", "quero uma fonte que não está
  instalada". Cobre a ordem EXATA de busca de arquivo (três regras diferentes:
  raster, vetor e fonte), o pipeline de import do SVG passo a passo com o que
  ele come e o que ele joga fora em silêncio, a regra de tamanho de cada um
  (`height=2` no SVG; `h_px/135` no `ImageMobject`), os três níveis de cor num
  SVG importado, o cache `SVG_HASH_TO_MOB_MAP`, o que anima e o que não anima
  numa imagem raster, e a diferença de renderer (SVG atravessa cairo e OpenGL;
  raster não). NÃO use para: escrever texto ou fórmula na tela e o `register_font`
  do lado tipográfico (`manim-text-latex`); escolher a cor, o contraste, o fundo
  e o tema (`manim-color-theming`); o catálogo de formas nativas e `Brace`
  (`manim-mobjects`); posicionar, alinhar, medir e enquadrar depois de
  carregado (`manim-layout-posicionamento`); animar (`manim-animations`);
  gráfico e eixo (`manim-graphs-plots`); som e legenda (`manim-som-legendas`);
  o `<Midia>` do deck `~/Projects/aulas`, que é HTML e tem skill própria
  (`aula-midia`, naquele repositório).
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Assets externos — SVG, imagem e fonte dentro da cena

Tudo nesta skill começa fora do Python: um arquivo no disco que a cena precisa
achar, decodificar e transformar em `Mobject`. É por isso que quase todos os
defeitos daqui são **silenciosos** — o Manim acha um jeito de continuar sem o
que faltou, e o erro só aparece no frame.

## Como ler este arquivo

ManimCE **0.21.0**, Python 3.12, renderer cairo, nesta máquina, 2026-08-19.
Bibliotecas que fazem o trabalho pesado e cuja versão importa:
**svgelements 1.9.6** (o parser de SVG), **Pillow 12.3.0** (o decodificador
raster), **manimpango 0.6.1** (o registro de fonte).

| Marca | O que significa |
|---|---|
| **[FONTE]** | li o código de `.venv/lib/python3.12/site-packages/…` — arquivo e linha citados. Afirmação forte |
| **[ÍNDICE]** | conferido em `api/manim-ce-index.tsv` / `api/manim-ce-methods.tsv` (assinatura, categoria, módulo, star import) |
| **[DERIVADO]** | aritmética minha sobre constantes lidas no fonte. Não executado |
| **[HOJE]** | `grep`/`awk`/`od`/Python puro rodado nesta sessão, sem render |
| **[NÃO VERIFICADO]** | encadeamento plausível a partir do fonte, com o mecanismo explicado, mas **nenhum render provou** |

**Esta rodada foi inteiramente sem render:** nenhum `mx render`, nenhum `manim`,
nenhum `ffmpeg`, nenhum navegador. Onde a prova exigiria um frame, está escrito
[NÃO VERIFICADO] — e a §12 diz exatamente o que rodar para fechar cada um.

## O resumo, para quem tem trinta segundos

1. **Vetor atravessa, raster não.** `SVGMobject` é um `VMobject`: escala sem
   perder, aceita `Create`/`Write`, entra em `VGroup`, funciona nos dois
   renderers. `ImageMobject` é um `Mobject` cru: não tem `set_fill`, não entra
   em `VGroup`, quebra em `Create`, e sob `--renderer opengl` é **outra classe**
   (§9).
2. **Cada tipo de asset tem uma regra de busca DIFERENTE**, e ninguém avisa:
   imagem e SVG procuram no `cwd` e no `assets_dir`; fonte procura ao lado do
   **arquivo da cena** (§2). É a causa nº 1 de `OSError: could not find`.
3. **O tamanho não é o do arquivo.** Um `SVGMobject` nasce com **2 unidades de
   altura**, sempre, seja um ícone de 24 px ou um mapa de 4000. Um
   `ImageMobject` nasce com `altura_px / 135` unidades (§4, §7.1).
4. **O importador de SVG joga coisa fora sem erro.** Texto vira aviso e some;
   `<image>` embutido some **sem nem aviso**; gradiente, `clip-path` e `mask`
   são ignorados (§3.4–§3.7).
5. **`svg_default` exige as SETE chaves.** Um dicionário parcial levanta
   `KeyError` num lugar que não parece ter nada a ver (§5.1).
6. **`stroke_width` cai para 0 no import.** Ícone feito só de contorno entra
   invisível (§5.3).
7. **`ImageMobject.set_color()` destrói a imagem** — ele sobrescreve o RGB de
   todos os pixels e deixa uma silhueta (§7.4). Às vezes é exatamente o que
   você quer.
8. **A imagem some sozinha em dois casos**, sem log nenhum: quando fica quase
   de perfil e quando três dos quatro cantos ficam colineares (§7.8).

## Cartão de referência — o sintoma manda na seção

| O que aconteceu / o que você quer | Onde ler |
|---|---|
| "SVG ou PNG? qual eu uso?" | §1 |
| `OSError: could not find …` | §2.1, §2.5 |
| a fonte do projeto não aparece | §2.4 |
| "como funciona o import de SVG por dentro?" | §3.2 |
| sumiu o **texto** do meu SVG | §3.5 |
| o SVG entrou **invisível** / só uma parte apareceu | §3.4, §5.3 (`fill="none"` sem traço) |
| o SVG virou uma **chapa preta** que cobre o resto | §3.6 — é gradiente, e o sintoma é tinta a MAIS |
| `PermissionError` ao carregar SVG, ou um `logo_.svg` estranho apareceu na pasta | §3.3 |
| o SVG entrou **gigante** ou **minúsculo** | §4 |
| quero pintar o logo inteiro de uma cor só | §5.2 |
| quero pintar **uma parte** do logo | §5.4 |
| `KeyError: 'color'` vindo de dentro do Manim | §5.1 |
| editei o `.svg` e a cena não mudou | §6 |
| a imagem está **borrada** / **serrilhada** | §7.1, §7.3 |
| `Create only works for VMobjects.` | §7.5 |
| `TypeError: Only values of type VMobject can be added as submobjects of VGroup` | §7.6 |
| `Mobject pixel array shapes incompatible for interpolation` | §7.5 |
| a imagem sumiu quando eu girei / achatei | §7.8 |
| quero uma foto de **fundo** de cena | §8 |
| `--renderer opengl` e a imagem quebrou | §9 |
| "põe a logo da empresa" — receita completa | §10 |
| tabela sintoma → causa → correção | §11 |
| o que dá para conferir **sem renderizar** | §12 |
| "isso é desta skill ou de outra?" | §13 |

---

## 1. A primeira decisão: vetor ou raster

Não é preferência estética. As duas classes têm modelos de objeto diferentes, e
metade das perguntas desta skill some quando a escolha está certa.

| | `SVGMobject` | `ImageMobject` |
|---|---|---|
| [ÍNDICE] herda de | `VMobject` | `Mobject` (via `AbstractImageMobject`) |
| [ÍNDICE] módulo | `manim.mobject.svg.svg_mobject` | `manim.mobject.types.image_mobject` |
| [ÍNDICE] categoria | `mobject/svg` | `mobject/core` |
| escala | sem perda, é geometria | reamostra; acima do nativo, borra ou serrilha |
| entra em `VGroup` | **sim** | **não** — `TypeError`; use `Group` (§7.6) |
| `set_fill` / `set_stroke` | sim | **não existem** — `AttributeError` |
| `Create`, `Write`, `DrawBorderThenFill` | sim | **`TypeError`** (§7.5) |
| `FadeIn`, `FadeOut`, `Transform`, `.animate` de posição/escala | sim | sim (com ressalva em §7.5) |
| `--renderer opengl` | funciona (metaclasse `ConvertToOpenGL`) | **classe diferente** (§9) |
| custo por frame | curvas de Bézier, como qualquer forma | uma transformação de perspectiva do Pillow **por frame** (§7.8) |
| formatos | `.svg` só | `.jpg .jpeg .png .gif .ico` por busca; qualquer coisa que o Pillow abra por caminho literal (§2.2) |

**A regra prática.** Logotipo, ícone, bandeira, diagrama desenhado à mão,
qualquer coisa que vá **crescer na tela**: SVG. Foto, captura de tela, print de
UI, gráfico exportado de outra ferramenta, textura: PNG/JPG. Um print de tela em
SVG não existe; um logotipo em PNG é dívida técnica que aparece no projetor.

**A terceira opção, que é quase sempre a melhor:** não carregar nada. Um
diagrama de cinco caixas com setas fica melhor desenhado com `Rectangle` +
`Arrow` do que importado de um Figma — ele herda a paleta do projeto, anima por
partes e não depende de um arquivo. Importe quando o desenho **não é seu**
(marca de terceiro, ícone de produto) ou quando refazer custaria mais do que
vale.

> [HOJE] O deck consumidor `~/Projects/aulas` tem **13 arquivos de cena Manim** e
> **nenhuma ocorrência** de `SVGMobject`, `ImageMobject`, `register_font` ou
> `background_image` — em nenhum arquivo do repositório inteiro. Não é
> esquecimento: naquele projeto a imagem mora no **slide** (componente
> `<Midia>`, HTML) e o vídeo do Manim só carrega desenho gerado. Vale como
> evidência de que, num deck, a resposta certa para "põe um GIF aqui"
> normalmente **não é** esta skill — é a skill `aula-midia` daquele repositório.
> Consequência honesta para este arquivo: **não há marca [DECK] em lugar nenhum
> aqui.** Nada nesta skill foi validado em produção; tudo é fonte lida.

---

## 2. Onde o Manim procura o arquivo — três regras diferentes

Esta é a seção que resolve mais chamados, e a que mais surpreende: **imagem,
SVG e fonte usam três resoluções de caminho distintas**, escritas em três
lugares do código.

### 2.1 Imagem e SVG: `seek_full_path_from_defaults`

[FONTE] `utils/file_ops.py:167-181`, na íntegra:

```python
def seek_full_path_from_defaults(file_name, default_dir, extensions) -> Path:
    possible_paths = [Path(file_name).expanduser()]
    possible_paths += [
        Path(default_dir) / f"{file_name}{extension}" for extension in ["", *extensions]
    ]
    for path in possible_paths:
        if path.exists():
            return path
    raise OSError(
        f"From: {Path.cwd()}, could not find {file_name} at either "
        f"of these locations: {list(map(str, possible_paths))}"
    )
```

Leia a ordem com cuidado, porque ela tem três consequências:

1. **O primeiro candidato é o caminho literal**, com `~` expandido e **sem**
   acrescentar extensão. Relativo, ele é resolvido contra o **`cwd` do processo
   de render** — não contra o diretório do arquivo da cena. Rodar `mx render`
   de outra pasta muda o resultado. (O `cwd` como parte da configuração é
   assunto de `manim-project` §5; aqui ele morde de novo.)
2. **Só os candidatos dentro do `assets_dir` ganham extensão automática.**
   `ImageMobject("logo")` acha `assets/logo.png`; `ImageMobject("./logo")` não
   acha `./logo.png`, porque `./logo` já entrou como caminho literal e o
   `assets_dir` é outro prefixo.
3. **A extensão vazia vem primeiro** (`["", *extensions]`), então
   `assets_dir/logo` (um arquivo sem extensão, ou um diretório!) ganha de
   `assets_dir/logo.png`. Um diretório chamado `logo` faz `path.exists()` dar
   `True` e o `Image.open` estourar com `IsADirectoryError` — erro confuso,
   causa boba.

[FONTE] Os dois chamadores, em `utils/images.py:27-40`:

```python
get_full_raster_image_path(nome)  # extensions=[".jpg", ".jpeg", ".png", ".gif", ".ico"]
get_full_vector_image_path(nome)  # extensions=[".svg"]
```

[FONTE] `default_dir=config.get_dir("assets_dir")` nos dois casos.
[FONTE] `_config/default.cfg:86` → `assets_dir = ./`. [HOJE] O `manim.cfg`
**deste projeto não sobrescreve `assets_dir`** — logo, aqui o `assets_dir` é o
próprio `cwd`, e a busca por extensão automática acontece na pasta de onde você
rodou o comando.

### 2.2 As extensões — e a lista que engana

A lista de extensões governa **só o palpite dentro do `assets_dir`**. O primeiro
candidato é literal, e quem decodifica é o Pillow. Consequência prática:

| Você escreveu | Funciona? | Por quê |
|---|---|---|
| `ImageMobject("foto.webp")`, arquivo existe nesse caminho | **sim** | candidato literal existe; o Pillow abre webp |
| `ImageMobject("foto")`, existe `assets/foto.webp` | **não** | `.webp` não está na lista de palpite |
| `ImageMobject("captura.png")` | sim | — |
| `ImageMobject("animado.gif")` | sim, **primeiro quadro só** | [FONTE] `Image.open(path).convert(mode)` não itera quadros (`image_mobject.py`) |
| `SVGMobject("icone.svgz")` | **não** | o SVG é lido por `ET.parse`, que não descomprime gzip |
| `SVGMobject("icone")`, existe `assets/icone.svg` | sim | `.svg` está na lista |

**GIF animado é a pegadinha silenciosa**: ele carrega, não dá erro, e mostra o
primeiro quadro parado para sempre. Se a intenção era um GIF em movimento, a
resposta não é `ImageMobject` — é converter em `.mp4` e pôr no player que
consome o vídeo, ou refazer a animação em Manim.

### 2.3 Onde pôr o arquivo, na prática

Duas convenções funcionam; a terceira não.

```python
# A) caminho relativo ao cwd do render — explícito, e o que eu recomendo
logo = SVGMobject("assets/logo.svg")

# B) assets_dir + palpite de extensão — mais curto, mais frágil
logo = SVGMobject("logo")            # acha ./logo.svg  (assets_dir = ./)

# C) relativo ao arquivo .py da cena — NÃO existe para imagem/SVG
logo = SVGMobject("logo.svg")        # quebra se o cwd não for a pasta da cena
```

Se as cenas moram em `scenes/` e você renderiza da raiz do projeto, a forma (C)
é a que parece certa e é a que falha. O jeito robusto, quando o arquivo tem de
morar ao lado da cena:

```python
from pathlib import Path
AQUI = Path(__file__).resolve().parent
logo = SVGMobject(str(AQUI / "assets" / "logo.svg"))
```

Isso é imune ao `cwd` porque entra como caminho **absoluto** no primeiro
candidato. É a única forma que sobrevive a `mx render` chamado de qualquer
pasta, a lote paralelo e a alguém importando o módulo de outro lugar.

### 2.4 Fonte: outra regra, e ela olha para o arquivo da cena

[FONTE] `mobject/text/text_mobject.py`, em `register_font`:

```python
input_folder = Path(config.input_file).parent.resolve()
possible_paths = [
    Path(font_file),
    input_folder / "assets/fonts" / font_file,
    input_folder / "fonts" / font_file,
    input_folder / font_file,
]
```

**Repare na assimetria.** Aqui a âncora é `config.input_file` — o `.py` que está
sendo renderizado — e não o `cwd` nem o `assets_dir`. As subpastas procuradas
são `assets/fonts/` e `fonts/`, que **não** são as mesmas de imagem e SVG. Uma
fonte em `assets/` (sem o `fonts/`) não é encontrada.

Duas armadilhas mais, no fim da mesma função [FONTE]:

```python
try:
    assert manimpango.register_font(str(file_path))
    yield
finally:
    manimpango.unregister_font(str(file_path))
```

- o registro falho vira **`AssertionError` sem mensagem** — nada explica o que
  deu errado com o arquivo;
- sob `python -O` o `assert` é removido, e um registro falho vira **silêncio
  total**: o `with` entra, o `Text` cai na fonte substituta e ninguém sabe.

O que acontece **depois** que a família é registrada — o nome da família não ser
o nome do arquivo, o escopo do `with`, e o fato de que fonte ausente vira Noto
Sans enquanto `t.font` continua mentindo — é de **`manim-text-latex` §2.4**
(que é a dona) e de `manim-project` §10.4. Não repito aqui.

### 2.5 O erro quando não acha, e como lê-lo

```
OSError: From: /home/você/projeto, could not find logo at either of these
locations: ['logo', 'logo', 'logo.svg']
```

A mensagem já traz o `cwd` — é a informação mais útil dela. Três leituras:

- **os caminhos saem relativos**, então "existe aqui" é sempre relativo ao `From:`;
- **a lista repete o nome** porque o candidato literal e o `assets_dir/""`
  coincidem quando `assets_dir = ./`;
- **é `OSError`, não `FileNotFoundError`** — um `except FileNotFoundError` em
  volta do carregamento não pega (`FileNotFoundError` é subclasse de `OSError`,
  não o contrário).

Conferir sem render, do próprio Python:

```python
from manim.utils.images import get_full_raster_image_path, get_full_vector_image_path
print(get_full_vector_image_path("assets/logo.svg"))   # levanta OSError se não achar
```

Custa milissegundos e não constrói mobject nenhum.

---

## 3. `SVGMobject` — a assinatura e o pipeline

### 3.1 A assinatura completa

[ÍNDICE] `manim.mobject.svg.svg_mobject.SVGMobject`, categoria `mobject/svg`,
**no star import**:

```python
SVGMobject(
    file_name: str | os.PathLike | None = None,
    should_center: bool = True,
    height: float | None = 2,
    width: float | None = None,
    color: ParsableManimColor | None = None,
    opacity: float | None = None,
    fill_color: ParsableManimColor | None = None,
    fill_opacity: float | None = None,
    stroke_color: ParsableManimColor | None = None,
    stroke_opacity: float | None = None,
    stroke_width: float | None = None,
    svg_default: dict | None = None,
    path_string_config: dict | None = None,
    use_svg_cache: bool = True,
    **kwargs,
)
```

Só a categoria `mobject/svg` tem **7 classes** [HOJE, `awk` sobre o índice]:
`SVGMobject`, `VMobjectFromSVGPath` e as cinco chaves (`Brace`, `BraceLabel`,
`BraceText`, `BraceBetweenPoints`, `ArcBrace`). As chaves moram no módulo por
acidente histórico e são de **`manim-mobjects`**; desta skill são as duas
primeiras. As outras 65 entradas da categoria são constantes reexportadas
(`UP`, `PI`, `BLACK`…), não matéria de ninguém.

[ÍNDICE] `VMobjectFromSVGPath(path_obj: se.Path, long_lines=False,
should_subdivide_sharp_curves=False, should_remove_null_curves=False, **kwargs)`
— também no star import. É o que o `SVGMobject` usa para cada `<path>`; você só
o instancia à mão se estiver construindo geometria a partir de um `se.Path` já
parseado. **Duas ressalvas:** [FONTE] os três booleanos só têm efeito com o
renderer OpenGL (`svg_mobject.py`, `generate_points`: o bloco está dentro de
`if config.renderer == "opengl"`), e o objeto sai **de cabeça para baixo** — a
inversão do eixo Y mora no `SVGMobject`, não aqui (§3.2, passo 7).

### 3.2 O pipeline, passo a passo

[FONTE] `svg_mobject.py`, `__init__` → `init_svg_mobject` → `generate_mobject`.
Nove passos, e cada um deles é uma oportunidade de perder alguma coisa:

| # | Passo | Onde | O que pode dar errado |
|---|---|---|---|
| 1 | resolve o caminho (`get_file_path` → `get_full_vector_image_path`) | §2.1 | `OSError` |
| 2 | consulta o cache em memória por `hash_seed` | §6 | reaproveita versão velha do arquivo |
| 3 | `ET.parse(file_path)` | XML padrão | XML malformado → `ParseError`; `.svgz` não abre |
| 4 | `modify_xml_tree` embrulha tudo em dois `<g>` com o estilo padrão | §5.1 | `KeyError` se `svg_default` for parcial |
| 5 | **escreve um `.svg` temporário ao lado do original** e o reparseia com `svgelements` | §3.3 | pasta somente-leitura; corrida em lote |
| 6 | `get_mobjects_from` percorre a árvore e converte cada elemento | §3.4 | elemento não suportado some |
| 7 | `self.flip(RIGHT)` — inverte o Y, porque no SVG ele cresce para baixo | — | — |
| 8 | `set_style(...)` com os parâmetros do construtor, `family=True` | §5.2 | achata o desenho numa cor só |
| 9 | `move_into_position()` — centraliza e ajusta a altura | §4 | tamanho não é o do arquivo |

Duas coisas que essa ordem já entrega:

- **o cache guarda o desenho CRU.** [FONTE] `SVG_HASH_TO_MOB_MAP[hash_val] =
  self.copy()` acontece dentro do passo 2, **antes** dos passos 8 e 9. Cor e
  tamanho ficam de fora do que é reaproveitado — por isso duas instâncias do
  mesmo arquivo com cores diferentes não brigam;
- **`should_center` e `height` são aplicados por último**, então qualquer
  posicionamento seu tem de vir depois da construção, nunca por kwarg de
  `VMobject`.

### 3.3 O arquivo temporário escrito ao lado do original

O passo 5 é o único do Manim que **escreve no seu diretório de assets**.
[FONTE] `svg_mobject.py`, em `generate_mobject`:

```python
modified_file_path = file_path.with_name(f"{file_path.stem}_{file_path.suffix}")
new_tree.write(modified_file_path)
svg = se.SVG.parse(modified_file_path)
modified_file_path.unlink()
```

Para `assets/logo.svg` isso é **`assets/logo_.svg`** — mesmo diretório, nome com
sublinhado antes do ponto. Três consequências reais:

1. **A pasta do asset precisa ser gravável.** Um `assets/` montado somente-leitura
   (contêiner, volume, pacote instalado) dá `PermissionError` num ponto que não
   parece ter nada a ver com escrita — você só pediu para *ler* um SVG.
2. **Um crash entre a escrita e o `unlink` deixa o `logo_.svg` para trás** — e
   ele casa com `*.svg`, então entra em glob de asset, em `git status` e, se
   alguém o carregar, é um SVG válido com o estilo padrão já embutido. Se você
   achar arquivos `*_.svg` na pasta, é isto; podem ser apagados.
3. **[NÃO VERIFICADO] Em lote paralelo, dois processos que importam o MESMO
   `.svg` disputam o mesmo caminho temporário.** O nome não tem PID nem hash: um
   escreve enquanto o outro parseia, ou um dá `unlink` no arquivo que o outro
   ainda vai ler (`FileNotFoundError` no `se.SVG.parse`). O mecanismo é evidente
   no fonte; a corrida não foi reproduzida aqui. Se você renderiza cenas em
   paralelo (`manim-batch-pipeline`), este é o motivo mais provável de uma falha
   intermitente que some quando você roda uma cena de cada vez — e a mitigação
   barata é dar a cada worker uma **cópia própria** da pasta de assets, do mesmo
   jeito que aquela skill já isola `tex_dir`/`text_dir` por worker.

### 3.4 O que o importador come, e o que ele joga fora

[FONTE] `get_mobjects_from` só chama o conversor para esta lista de tipos do
svgelements, e `get_mob_from_shape_element` faz o despacho:

| Elemento SVG | Vira | Observação |
|---|---|---|
| `<path>` | `VMobjectFromSVGPath` | arcos são aproximados por quadráticas antes (`approximate_arcs_with_quads`) |
| `<line>` | `Line` | — |
| `<rect>` | `Rectangle`, ou `RoundedRectangle` se `rx` e `ry` forem ambos ≠ 0 | canto elíptico é aproximado: constrói com a altura distorcida e depois `stretch_to_fit_height` |
| `<circle>`, `<ellipse>` | `Circle` (+ `stretch_to_fit_height` se `rx ≠ ry`) | — |
| `<polygon>` | `Polygon` | — |
| `<polyline>` | `VMobject().set_points_as_corners(...)` | vira polilinha aberta |
| `<g>`, `<use>` | percorridos; viram `VGroup` no `id_to_vgroup_dict` (§5.4) | ordem do documento é preservada |
| `<text>`, `<tspan>` | **NADA** | avisa e some — §3.5 |
| `<image>` | **NADA** | **nem avisa** — §3.5 |
| `<clipPath>`, `<mask>`, `<pattern>`, `<filter>`, `<defs>`, gradientes | **NADA** | §3.6 |

A ordem dos submobjects é a ordem do documento, então **o que está por cima no
Inkscape continua por cima na cena** — o `z_index` interno do desenho é
preservado de graça.

### 3.5 Texto e `<image>` somem — um avisando, o outro não

[FONTE] `SVGMobject.text_to_mobject` é um toco:

```python
@staticmethod
def text_to_mobject(text: se.Text) -> VMobject:
    logger.warning(f"Unsupported element type: {type(text)}")
    return
```

Ele devolve `None`, o chamador descarta, e **a palavra some do desenho** com uma
linha de WARNING no log — que ninguém lê quando a barra de progresso está
rolando. Este é o defeito nº 1 de logotipo importado: a marca tem o símbolo e o
nome, e só o símbolo aparece.

**A correção é no arquivo, não no código:** converta o texto em contorno antes
de exportar.

| Ferramenta | Comando |
|---|---|
| Inkscape (GUI) | selecionar tudo → **Caminho → Objeto para Caminho** (`Shift+Ctrl+C`) |
| Inkscape (CLI) | `inkscape --export-type=svg --export-text-to-path -o saida.svg entrada.svg` |
| Illustrator | **Tipo → Criar contornos** (`Shift+Ctrl+O`) |
| Figma | selecionar o texto → **Flatten** antes de exportar SVG |

Depois disso o texto é `<path>` e entra normalmente — mas vira **geometria**, não
texto: `t2c`, troca de fonte e `TransformMatchingTex` deixam de existir. Se você
precisa disso, o texto não devia estar no SVG: desenhe-o com `Text`/`MathTex`
(matéria de `manim-text-latex`) e importe do SVG só o símbolo.

**`<image>` é pior porque é mudo.** O `logger.warning` mora dentro de
`get_mob_from_shape_element`, que **só é chamado para os tipos da lista**
[FONTE]. `se.Image` não está na lista, então o elemento é pulado antes de
qualquer log. Um "SVG" exportado com um bitmap embutido (o caso típico do
"Salvar como SVG" de editor raster) importa como um `SVGMobject` **vazio, sem
uma linha de aviso**. Se o seu SVG veio de um editor de imagem e não de um
editor vetorial, este é o primeiro suspeito.

### 3.6 Gradiente, `clip-path` e `mask` — a cadeia que termina em PRETO

[HOJE] O svgelements 1.9.6 tem **39 classes**, e entre elas há `ClipPath`,
`Pattern`, `Image`, `Text`, `Use`, `Group` — mas **não há `LinearGradient` nem
`RadialGradient`**. Gradiente não é modelado.

**ESTA SEÇÃO É UMA CORREÇÃO, e o sintoma é o INVERSO do que dizia.** A versão
anterior afirmava, marcada `[FONTE nos três elos]`, que gradiente entra
**invisível** — "um buraco do tamanho certo". O primeiro elo é falso, e com ele
cai a conclusão. Medido nesta máquina, sem render:

```console
$ .venv/bin/python -c "import svgelements as se; c=se.Color('url(#grad1)'); \
                       print(c.value, c.hexrgb, c.opacity)"
255 #000000 1.0
```

`Color.parse` só devolve `None` para `None` e para a string `"none"`; **qualquer
string que ele não reconhece cai no fallback `Color.rgb_to_int(0, 0, 0)`** — que
é preto, opaco. `url(#grad)` é uma dessas.

O encadeamento **real**:

1. `fill="url(#meuGradiente)"` não parseia como cor → o svgelements não devolve
   `None`, devolve `Color` **preto com opacidade 1,0**;
2. `shape.fill.hexrgb == "#000000"` e `shape.fill.opacity == 1.0`;
3. `SVGMobject.apply_style_to_mobject` (`svg_mobject.py:378-384`) repassa esses
   valores para `mob.set_style(fill_color="#000000", fill_opacity=1.0, …)`;
4. `update_rgbas_array` escreve normalmente — **não é no-op**, é um `set_style`
   efetivo.

**Resultado, medido no importador:** a forma entra como uma **chapa preta
opaca**. Num projeto de fundo branco — o padrão desta base — um logo com
gradiente vira um bloco preto que **cobre** o desenho em volta. Você vai
procurar tinta que falta e encontrar tinta a mais.

A correção não muda: achate o gradiente para cor sólida na exportação, ou
aceite a geometria e pinte você mesmo (`svg.set_fill(COR, 1)`). O que muda é o
que você procura na tela.

> **O caso que de fato some é `fill="none"`** — aí sim `Color.parse` devolve
> `None`, o `set_style` vira no-op, e a forma fica com o `fill_opacity = 0` de
> um `VMobject` recém-criado, com `stroke_width` 0 vindo do padrão do importador
> (§5.3). Os elos 2-5 da versão anterior descreviam **este** caso, não o do
> gradiente.

**`clip-path` e `mask` são ignorados, e isso é o oposto de sumir.** [HOJE] O
svgelements até resolve o `clip-path` e o pendura em `shape.clip_path`, mas
[FONTE] o `apply_style_to_mobject` do Manim lê **só** `stroke_width`, `stroke`,
`stroke.opacity`, `fill` e `fill.opacity` — o clip nunca é consultado. Logo: o
que o designer escondeu com máscara **volta a aparecer**. O sintoma é o
contrário do gradiente — em vez de faltar desenho, sobra: um retângulo de fundo
que deveria estar recortado, uma metade de círculo que vira círculo inteiro.
[NÃO VERIFICADO] por render, mas o `apply_style_to_mobject` está inteiro na §5 e
não há outro ponto onde o clip pudesse entrar.

### 3.7 O `except` que engole o elemento

[FONTE] Dentro do laço de `get_mobjects_from`:

```python
except Exception as e:
    logger.error(f"Exception occurred in 'get_mobjects_from'. Details: {e}")
```

Um `except Exception` por elemento. Qualquer falha na conversão de **um**
`<path>` — atributo estranho, transformação degenerada, número que não converte
— derruba aquele elemento e **o import continua**. O resultado é um desenho
parcial com uma linha de ERROR no meio do log, e um `SVGMobject` que parece ter
funcionado.

Isso muda como se depura SVG no Manim: **o exit code não vale nada aqui**.
Quando um desenho vem incompleto, o primeiro passo é reler o log inteiro
procurando `Exception occurred in 'get_mobjects_from'` e `Unsupported element
type`, não mexer no código:

```bash
bin/mx render cena.py Cena -q l 2>&1 | grep -iE "unsupported element|get_mobjects_from"
```

### 3.8 `modify_xml_tree` monta um SVG novo — e o `viewBox` fica para trás

[FONTE] O passo 4 cria a raiz assim:

```python
new_root = ET.Element("svg", {})
config_style_node = ET.SubElement(new_root, "g", config_style_dict)
root_style_node = ET.SubElement(config_style_node, "g", root_style_dict)
root_style_node.extend(root)
```

A raiz nova nasce **sem atributo nenhum**: sem `viewBox`, sem `width`/`height`,
sem `preserveAspectRatio`. Só os atributos de **estilo** da raiz original são
copiados (`fill`, `fill-opacity`, `stroke`, `stroke-opacity`, `stroke-width`,
`style`).

Na prática isso quase nunca dói, porque o `move_into_position` reescala tudo
para `height=2` logo depois e uma escala uniforme perdida é irrelevante. Mas
explica duas coisas:

- **as coordenadas cruas do objeto importado são as do arquivo**, não as do
  `viewBox` — daí um ícone de 24×24 nascer com 24 unidades de altura quando
  você passa `height=None` (§4);
- **`preserveAspectRatio` e o recorte do `viewBox` não existem** para o Manim:
  o que estiver fora da moldura do desenho original vem junto e entra na caixa
  delimitadora. Se o seu ícone tem um retângulo transparente de 512×512 como
  "área de trabalho", ele conta no tamanho e o desenho visível fica menor do que
  você pediu. É o mesmo defeito que `manim-project` §10.9 documenta para
  elemento invisível dentro de `VGroup`, chegando por outra porta.

---

## 4. Tamanho: `height=2` manda, e o arquivo não opina

Esta é a regra que mais surpreende, e ela é de uma linha só. [FONTE]
`move_into_position`:

```python
if self.should_center:
    self.center()
if self.svg_height is not None:
    self.set(height=self.svg_height)     # svg_height = height, default 2
if self.svg_width is not None:
    self.set(width=self.svg_width)
```

| Você escreve | O que sai |
|---|---|
| `SVGMobject("logo.svg")` | **2 unidades de altura**, sempre. 25% da altura do quadro (8) |
| `SVGMobject("logo.svg", height=3.5)` | 3,5 de altura, largura proporcional |
| `SVGMobject("logo.svg", width=5)` | altura 2 aplicada, **depois** largura 5 aplicada — vence a largura, e o resultado é proporcional (não estica) |
| `SVGMobject("logo.svg", height=None, width=None)` | **as unidades cruas do arquivo** |

O caso interessante é o terceiro. [FONTE] `Mobject.width` é uma property cujo
setter é `self.scale_to_fit_width(value)` (`mobject.py:809-810`) — escala
**uniforme**. Então passar `height` e `width` juntos não distorce nada: são duas
escalas uniformes em sequência, e a segunda apaga a primeira. **Não existe jeito
de esticar um SVG pelo construtor**; para isso é `stretch_to_fit_width` depois
(matéria de `manim-layout-posicionamento`).

E o quarto é a armadilha. O quadro tem **8 unidades de altura** (14,222 × 8).
Com `height=None, width=None`:

| Arquivo | Altura resultante | O que aparece |
|---|---|---|
| ícone Material/Lucide, `viewBox="0 0 24 24"` | **24 unidades** | 3× o quadro — você vê um pedaço do meio |
| logo, `viewBox="0 0 512 512"` | **512 unidades** | 64× o quadro — a tela fica de uma cor só |
| desenho feito para o quadro, ~8 de altura | 8 | encaixa |

Ou seja: `height=None` só serve quando o SVG foi desenhado **nas unidades do
Manim**, o que é raro. Se você viu "o SVG entrou gigante", é isto — ou o §3.8
(uma área de trabalho transparente comendo o tamanho útil).

**Um detalhe que morde depois.** [FONTE] `VMobject.scale(scale_factor,
scale_stroke: bool = False, …)` — a espessura do traço **não** acompanha a
escala. Como o `move_into_position` chama `scale_to_fit_height` → `scale`, o
`stroke_width` que veio do arquivo sobrevive ao redimensionamento **em valor
absoluto**. Um SVG de 512 unidades com `stroke-width="2"` (fino lá dentro)
importa como traço 2 do Manim — que num objeto de 2 unidades de altura é
**grosso**. Se o contorno saiu pesado depois de encolher o logo, é isso; a
correção é `svg.set_stroke(width=…)` depois, ou passar `stroke_width=` no
construtor (§5.3).

---

## 5. Cor e estilo num SVG importado — três níveis que não se misturam

Existem **três** lugares para pintar um SVG, e eles agem em momentos
diferentes do pipeline. Escolher o errado é a origem de "pintei e não mudou" e
de "pintei e destruí o desenho".

| Nível | Como | Quando age | Efeito |
|---|---|---|---|
| **A. padrão do arquivo** | `svg_default={…}` | passo 4, **antes** do parse | só onde o SVG **não** declara nada (herança de CSS) |
| **B. sobrescrita global** | `color=`, `fill_color=`, `stroke_width=`… no construtor | passo 8, depois do parse | **achata**: pinta todo submobject igual |
| **C. depois, na mão** | `svg.set_fill(...)`, `svg[3].set_color(...)`, `svg.id_to_vgroup_dict[...]` | quando você quiser | cirúrgico |

### 5.1 `svg_default` exige as SETE chaves — `KeyError` garantido

[FONTE] `generate_config_style_dict`:

```python
keys_converting_dict = {
    "fill":           ("color", "fill_color"),
    "fill-opacity":   ("opacity", "fill_opacity"),
    "stroke":         ("color", "stroke_color"),
    "stroke-opacity": ("opacity", "stroke_opacity"),
    "stroke-width":   ("stroke_width",),
}
for svg_key, style_keys in keys_converting_dict.items():
    for style_key in style_keys:
        if svg_default_dict[style_key] is None:      # <- indexação DIRETA
            continue
        result[svg_key] = str(svg_default_dict[style_key])
```

O acesso é `svg_default_dict[style_key]`, sem `.get`. Se o seu dicionário não
tiver as **sete** chaves — `color`, `fill_color`, `opacity`, `fill_opacity`,
`stroke_color`, `stroke_opacity`, `stroke_width` — sai `KeyError` vindo de dentro
do construtor, num lugar que não parece ter relação com o que você passou.

```python
# QUEBRA: KeyError: 'color'
SVGMobject("logo.svg", svg_default={"fill_color": AZUL})

# CERTO: as sete, com None no que você não quer mexer
SVGMobject("logo.svg", svg_default={
    "color": None, "opacity": None,
    "fill_color": AZUL, "fill_opacity": 1,
    "stroke_color": None, "stroke_opacity": None, "stroke_width": 0,
})
```

Duas notas sobre esse dicionário:

- **a precedência dentro dele é a ordem do laço.** Para `fill`, ele lê `color`
  e depois `fill_color`; quem escreve por último vence. Ou seja `fill_color`
  ganha de `color`, e `stroke_color` ganha de `color`. Não há mistério, mas não
  está documentado em lugar nenhum;
- **o valor vira string de SVG.** [FONTE] `result[svg_key] = str(...)` e
  [FONTE] `ManimColor.__str__` devolve `self.to_hex()` (`utils/color/core.py:970`).
  Então `ManimColor` funciona (`#0071E3`), `"red"` funciona, e um número
  funciona para `stroke-width` — **em unidades do arquivo SVG**, não do Manim.
  Por isso `stroke_width` aqui é imprevisível: some no meio da reescala do §4.
  Para espessura, use o nível B.

**Quando o nível A é a resposta certa:** ícone monocromático que confia no
`currentColor` ou que não declara `fill` nenhum. Aí o SVG **não tem** cor
própria, e só a herança do `<g>` externo pode dar uma. Nível B também
funcionaria, mas o A preserva qualquer elemento que declare cor explícita — que
é justamente o comportamento que você quer num ícone com dois tons.

### 5.2 O construtor achata o desenho — `family=True` é o motivo

[FONTE] O passo 8 é literalmente:

```python
self.set_style(
    fill_color=fill_color, fill_opacity=fill_opacity,
    stroke_color=stroke_color, stroke_opacity=stroke_opacity,
    stroke_width=stroke_width,
)
```

e `VMobject.set_style` tem `family: bool = True`, que recursa em todos os
submobjects [FONTE `vectorized_mobject.py:409-421`]. Logo:

```python
SVGMobject("logo-colorido.svg", fill_color=TINTA)   # todo o logo vira TINTA
```

Isso é **desejável** para um ícone que você quer na cor do tema, e **destrutivo**
para uma marca de terceiro cujas cores são a marca. Não existe meio-termo pelo
construtor.

E o motivo de `SVGMobject("x.svg")` sem argumento nenhum **não** apagar as cores
do arquivo: [FONTE] `update_rgbas_array` só escreve quando o argumento não é
`None` (`vectorized_mobject.py:274-279`), então `set_style(None, None, …)` é um
no-op completo. É esse detalhe que faz o passo 8 ser inofensivo por padrão.

### 5.3 `stroke_width` cai para 0 — o contorno some

[FONTE] Duas linhas do `__init__`, com efeitos em pontos diferentes:

```python
self.stroke_width = stroke_width
if self.stroke_width is None:
    self.stroke_width = 0
...
svg_default = { ..., "stroke_width": 0, ... }   # o padrão do dicionário
```

O `stroke-width: 0` entra no `<g>` externo (passo 4) e é **herdado** por todo
elemento que não declare a sua própria espessura. Na especificação do SVG o
padrão é `1`; o Manim troca por `0`.

Consequência: **um ícone desenhado só com contorno, sem preenchimento, que
confia no `stroke-width` padrão, importa completamente invisível.** Nada de erro,
nada de aviso — a geometria está lá, a caixa delimitadora está certa, e a tela
está vazia. É o irmão do defeito clássico de fundo branco (`manim-color-theming`).

Três correções, em ordem de preferência:

```python
# 1. declare a espessura no nível B — em unidades do Manim, previsível
icone = SVGMobject("icone.svg", stroke_width=3, stroke_color=TINTA)

# 2. ou depois, com controle de família
icone = SVGMobject("icone.svg")
icone.set_stroke(color=TINTA, width=3)

# 3. ou conserte o arquivo: no editor, dê stroke-width explícito a cada traço
```

**O teste barato que separa "sumiu por contorno" de "sumiu por gradiente"** — e
que não precisa de render:

**Correção: leia as FOLHAS, não o contêiner.** A versão anterior imprimia
`svg.get_fill_opacity()` direto no `SVGMobject`. O `SVGMobject` é o pai; os
valores de estilo moram nos submobjects. Medido: um SVG de um quadrado vermelho
**perfeitamente visível** dá `fill_opacity=0.00, stroke_width=0.00` **no pai** —
o diagnóstico acusa invisibilidade em arquivo que está certo.

```python
svg = SVGMobject("icone.svg")
print("submobjects:", len(svg.submobjects))
for i, m in enumerate(svg.family_members_with_points()):      # as FOLHAS
    print(i, m.get_fill_color(), m.get_fill_opacity(),
             m.get_stroke_color(), m.get_stroke_width())
```

Leitura da saída:

- **zero folhas** → não é estilo, é o §3.4/§3.5 (nada foi convertido);
- folhas com `fill_opacity == 0` **e** `stroke_width == 0` → invisível por
  estilo: é `fill="none"` sem traço, ou o padrão de traço desta seção;
- folhas com **`#000000` e `fill_opacity == 1`** onde o arquivo tinha
  gradiente → é o §3.6, e o sintoma é chapa preta, não buraco.

### 5.4 Pintar só uma parte — `id_to_vgroup_dict`

O `SVGMobject` guarda um mapa dos `id` do arquivo para `VGroup`s com os mobjects
correspondentes. [FONTE] É montado em `get_mobjects_from` e atribuído em
`generate_mobject` / `init_svg_mobject`:

```python
self.id_to_vgroup_dict: dict[str, VGroup]
```

```python
logo = SVGMobject("marca.svg", height=2.4)
print(sorted(logo.id_to_vgroup_dict))        # os nomes disponíveis
logo.id_to_vgroup_dict["simbolo"].set_fill(ACENTO, 1)
logo.id_to_vgroup_dict["texto"].set_fill(TINTA, 1)
```

Isso vale ouro num logo de duas cores, porque o nome vem do **editor**: no
Inkscape é o rótulo do objeto/camada, no Illustrator o nome da camada, no Figma o
nome do frame ou grupo. Nomear as camadas antes de exportar é o que torna a cena
legível depois.

Três ressalvas, todas do fonte:

- **elementos sem `id` ganham `numbered_group_{n}`** — nomes que mudam se você
  reordenar o arquivo. Não escreva código contra eles;
- há sempre uma chave **`"root"`** com tudo dentro;
- os `VGroup`s do dicionário contêm os **mesmos objetos** que os submobjects do
  `SVGMobject` (é uma vista, não uma cópia). Pintar pelo dicionário pinta o
  desenho; **animar** o `VGroup` do dicionário anima peças que também pertencem
  ao pai — some com `self.play(FadeOut(vg))` e o pai fica com um buraco. Para
  animar um pedaço separado, `.copy()` primeiro.

O caminho alternativo, quando o SVG não tem `id` nenhum, é por índice —
`logo[0]`, `logo[3]` — e aí `index_labels(logo)` põe o número de cada submobject
na tela (é de `manim-layout-posicionamento`, e o `manim-verificacao-visual`
explica como olhar o PNG). Índice é frágil: qualquer reexportação do arquivo
pode reordenar.

---

## 6. O cache em memória `SVG_HASH_TO_MOB_MAP`

[FONTE] `svg_mobject.py`, no topo do módulo: `SVG_HASH_TO_MOB_MAP: dict[int,
SVGMobject] = {}`. [ÍNDICE] **não** está no star import — para tocá-lo é
`from manim.mobject.svg.svg_mobject import SVG_HASH_TO_MOB_MAP`.

A chave é o `hash_seed`, e ele é curto [FONTE]:

```python
@property
def hash_seed(self) -> tuple:
    return (
        self.__class__.__name__,
        self.svg_default,
        self.path_string_config,
        self.file_name,
        config.renderer,
    )
```

O que ele **vê**: a classe (subclasses não colidem com a base), o dicionário de
padrões, a config de path, o **nome** do arquivo e o renderer.

O que ele **não vê**, e cada omissão tem um efeito:

| Fora do hash | Efeito |
|---|---|
| **o conteúdo do arquivo** | editar o `.svg` e reconstruir o mobject **no mesmo processo** devolve a versão velha |
| `height` / `width` | inofensivo: aplicados depois do cache (§3.2) |
| `color`, `fill_*`, `stroke_*` | inofensivo, mesmo motivo |
| a resolução do render | inofensivo aqui — **diferente** do cache de SVG de *texto*, onde a resolução muda a quebra de linha e o hash a ignora (`manim-project` §10.6, `manim-text-latex`) |

**Onde o "conteúdo fora do hash" morde de verdade** é num processo de vida
longa: Jupyter, `manim --renderer=opengl` com janela, um script que
constrói várias cenas, ou qualquer loop de iteração que não reinicia o Python.
Você salva o SVG no editor, reconstrói, e vê o desenho antigo. Duas saídas:

```python
SVGMobject("logo.svg", use_svg_cache=False)      # esta instância não usa o cache

from manim.mobject.svg.svg_mobject import SVG_HASH_TO_MOB_MAP
SVG_HASH_TO_MOB_MAP.clear()                      # limpa tudo
```

Num `mx render` normal o processo morre a cada render, então o cache é só ganho —
ele existe para o caso de a mesma marca aparecer dez vezes na cena.

**Quando desligar de propósito:** [FONTE] a docstring do parâmetro diz "For
large SVGs which are used only once, this can be omitted to improve
performance". Faz sentido: com `use_svg_cache=True` o Manim faz um `copy.deepcopy`
**a mais** do desenho inteiro (para guardar) e outro na leitura. Num mapa com
milhares de caminhos usado uma vez só, os dois deepcopies custam mais do que
reparsear. [NÃO VERIFICADO] — não medi; o mecanismo é o `self.copy()` em
`init_svg_mobject`, e [FONTE] `Mobject.copy` é `copy.deepcopy(self)`
(`mobject.py:908`).

O `use_svg_cache` **não** tem nada a ver com o cache de partial movies
(`--disable_caching`) nem com `media/Tex`. Isso é `manim-performance-cache`.

---

## 7. `ImageMobject` — a imagem raster

### 7.1 A conta do tamanho: `altura_px / 135`

[ÍNDICE] A assinatura:

```python
ImageMobject(
    filename_or_array: StrPath | npt.NDArray,
    scale_to_resolution: int = 1080,   # = QUALITIES["high_quality"]["pixel_height"]
    invert: bool = False,
    image_mode: str = "RGBA",
    **kwargs,
)
```

[FONTE] `constants.py:206-245` — `DEFAULT_QUALITY = "high_quality"` e
`QUALITIES["high_quality"]["pixel_height"] = 1080`, daí o default.

[FONTE] `AbstractImageMobject.reset_points` decide o tamanho:

```python
h, w = self.get_pixel_array().shape[:2]
if self.scale_to_resolution:
    height = h / self.scale_to_resolution * config["frame_height"]
else:
    height = 3
self.stretch_to_fit_height(height)
self.stretch_to_fit_width(height * w / h)
```

[DERIVADO] Com os padrões (`scale_to_resolution=1080`, `frame_height=8`):

> **altura em unidades = altura_em_pixels / 135**

| PNG | Altura na cena | Fração do quadro |
|---|---|---|
| 135 px | 1,00 | 12,5% |
| 270 px | 2,00 | 25% |
| 540 px | 4,00 | 50% |
| **1080 px** | **8,00** | **100% — encosta em cima e embaixo** |
| 2160 px | 16,00 | 200% — metade fica fora do quadro |

E o par que enche o quadro exatamente: um PNG de **1920×1080** vira 8 de altura
por `8 × 1920/1080 = 14,222` de largura — que é exatamente o `frame_width`.
[DERIVADO]

**O que o `scale_to_resolution` significa de verdade.** [DERIVADO] Em pixels de
dispositivo, a imagem ocupa `h_px × pixel_height_do_render / scale_to_resolution`.
Quando os dois batem, é **1 pixel da imagem para 1 pixel do vídeo** — nitidez
máxima, sem reamostragem. Por isso o parâmetro existe: ele desacopla o tamanho
na cena da qualidade do render. Renderizar em `-ql` não muda o tamanho relativo
da imagem; só faz ela ser desenhada em menos pixels.

Três leituras práticas:

- **deixe `scale_to_resolution` no padrão 1080** se você entrega em 1080p;
  suba para 2160 se entrega em 4K e a arte é 4K. Mudar esse número **muda o
  tamanho na tela**, então não o use como controle de nitidez sem revisar o
  enquadramento;
- **`scale_to_resolution=0`** (ou `False`) cai no ramo `height = 3` — altura fixa
  de 3 unidades, independente dos pixels. É uma saída legítima quando você não
  quer que o tamanho dependa da arte;
- **a nitidez só existe se você não reescalar depois.** `img.height = 4` num PNG
  de 1080 px joga fora metade da resolução; `img.scale(1.5)` num PNG de 400 px
  aumenta 50% do que não existe.

**Para um asset novo, calcule ao contrário:** decida a altura em unidades,
multiplique por 135, e peça a arte nesse tamanho. Um logo que vai ocupar 1,5
unidade quer um PNG de ~200 px de altura em 1080p — pedir 4000 px "por
segurança" só desperdiça memória e faz o Pillow reamostrar todo frame.

### 7.2 Array numpy, `image_mode` e `invert`

[FONTE] `ImageMobject.__init__` aceita caminho **ou** array:

```python
ImageMobject(np.uint8([[0, 100, 30, 200], [255, 0, 5, 33]]))   # 2×4, escala de cinza
```

[FONTE] `change_to_rgba_array` (`utils/images.py:59-71`) normaliza qualquer
entrada para RGBA: 2D vira 3 canais repetidos, 3 canais ganham alfa 255. Então
um array `(h, w)` de `uint8` é lido como cinza, e um `(h, w, 3)` como RGB opaco.

- **`image_mode`** é passado direto ao `Image.open(path).convert(mode)` do
  Pillow. `"RGBA"` (padrão) preserva transparência; `"RGB"` a descarta e o PNG
  recortado vira um retângulo com fundo preto; `"L"` converte para cinza.
- **`invert=True`** inverte só os canais RGB (`max - valor`), preservando o alfa.
- **`pixel_array_dtype`** chega por `**kwargs` e vale `"uint8"` por padrão.

Um array é o caminho mais rápido para pôr um heatmap, uma matriz ou um frame de
vídeo já em memória na cena — sem passar por arquivo.

### 7.3 Reamostragem: a docstring do Manim mente

[FONTE] `constants.py:111-118`, o dicionário inteiro:

```python
RESAMPLING_ALGORITHMS = {
    "nearest": Resampling.NEAREST,   "none": Resampling.NEAREST,
    "bilinear": Resampling.BILINEAR, "linear": Resampling.BILINEAR,
    "bicubic": Resampling.BICUBIC,   "cubic": Resampling.BICUBIC,
}
```

**Seis chaves, três algoritmos.** [FONTE] Mas a docstring de
`AbstractImageMobject.set_resampling_algorithm` (`image_mobject.py`) anuncia
também `'box'`, `'hamming'` e `'lanczos'/'antialias'` — e a validação logo
abaixo é:

```python
if resampling_algorithm not in RESAMPLING_ALGORITHMS.values():
    raise ValueError(...)
```

Como `Resampling.LANCZOS`, `Resampling.BOX` e `Resampling.HAMMING` **não estão**
entre os valores, passá-los levanta `ValueError` — apesar da docstring dizer que
são aceitos. A mensagem de erro, essa sim, lista só os três de verdade. Se você
leu a documentação e escreveu `lanczos`, o erro é da documentação, não seu.

```python
from manim import RESAMPLING_ALGORITHMS
pixelart = ImageMobject("sprite.png")
pixelart.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])   # sem borrar
pixelart.height = 5
```

**`nearest` é a escolha certa** para pixel art, sprite, QR-Code e captura de tela
ampliada — qualquer coisa em que a borda dura é a informação. `bicubic` (padrão)
é certo para foto. `bilinear` quase nunca ganha de um dos dois.

### 7.4 Cor e opacidade — `set_color` destrói a imagem

[FONTE] `ImageMobject.set_color`:

```python
rgb = color_to_int_rgb(color)
self.pixel_array[:, :, :3] = rgb        # TODOS os pixels
```

Ele **sobrescreve o RGB de cada pixel**, mantendo só o alfa. O resultado é uma
silhueta sólida no formato da transparência do PNG. Isso é destrutivo e
**in-place**: o `pixel_array` original se perde, e não há como voltar sem
recarregar.

Duas leituras:

- **como defeito:** `img.set_color(AZUL)` porque "queria dar um tom azulado"
  apaga a foto;
- **como recurso:** é exatamente o jeito de transformar um PNG com alfa num
  ícone monocromático na cor do tema. Se você tem um logo em PNG recortado e
  precisa dele em cinza, é uma linha.

O resto da paleta:

| Método | [FONTE] o que faz |
|---|---|
| `set_opacity(alpha)` | `pixel_array[:,:,3] = orig_alpha * alpha`. Reversível: parte do alfa **original**, guardado em `orig_alpha_pixel_array` |
| `fade(darkness=0.5)` | chama `set_opacity(1 - darkness)`. Apesar do nome, é **opacidade**, não escurecimento |
| `get_pixel_array()` | devolve o array vivo — mexer nele mexe na imagem |
| `get_style()` | só `{"fill_color", "fill_opacity"}`, para o maquinário de `Transform` |
| `set_fill` / `set_stroke` | **não existem.** `AttributeError` — é `Mobject`, não `VMobject` |

### 7.5 O que anima, e o que estoura

| Animação | `ImageMobject` | Motivo [FONTE] |
|---|---|---|
| `FadeIn`, `FadeOut` | **sim** | `_Fade` é um `Transform` que faz `copy()` + `fade(1)`; o `ImageMobject` tem `fade` próprio |
| `.animate.shift/scale/rotate`, `MoveAlongPath`, `Rotate` | **sim** | mexem nos 4 pontos de canto |
| `GrowFromCenter`, `ScaleInPlace` | **sim** | são `Transform` de escala |
| `Transform(imgA, imgB)` | **só com arrays do mesmo tamanho** | `interpolate_color` tem `assert mobject1.pixel_array.shape == mobject2.pixel_array.shape` |
| `Create`, `Write`, `DrawBorderThenFill`, `ShowPassingFlash`, `Uncreate` | **`TypeError`** | `ShowPartial.__init__` procura `pointwise_become_partial`, que só existe em `VMobject` |
| `Indicate`, `Circumscribe`, `Flash` | ver nota | `Circumscribe`/`Flash` desenham um `VMobject` **em volta** e funcionam; `Indicate` mexe na cor (§7.4) |

As duas mensagens exatas, para quem chegou aqui pelo traceback:

```
TypeError: Create only works for VMobjects.
AssertionError: Mobject pixel array shapes incompatible for interpolation.
Mobject 1 (ImageMobject) : (512, 512, 4)
Mobject 2 (ImageMobject) : (256, 256, 4)
```

A segunda tem correção direta: redimensione as duas imagens **em pixels** para o
mesmo tamanho antes de carregar (`Image.resize` do Pillow, ou o próprio
exportador), não com `.height =` na cena — a cena escala a caixa, não o array.
Ou troque `Transform` por um `FadeOut` + `FadeIn` cruzados, que não têm essa
exigência.

### 7.6 `VGroup` recusa; `Group` aceita

`ImageMobject` não é `VMobject`, então:

```
TypeError: Only values of type VMobject can be added as submobjects of VGroup,
but the value ImageMobject (at index 0 of parameter 0) is of type ImageMobject.
```

[FONTE] a mensagem vem de `get_type_error_message` em
`vectorized_mobject.py:2332-2339`. Use `Group`, que aceita qualquer `Mobject`:

```python
cartao = Group(ImageMobject("foto.png"), Text("Legenda", color=TINTA)).arrange(DOWN)
```

`Group` × `VGroup` em profundidade é de **`manim-mobjects`**; aqui interessa só
que a imagem é a causa mais comum desse `TypeError`. Efeito colateral: um
`Group` não tem `set_fill`/`set_stroke`, então misturar imagem e vetor num grupo
custa o estilo em bloco — estilize os filhos vetoriais antes de agrupar.

### 7.7 Ordem de desenho: `z_index` funciona entre os tipos

Uma dúvida legítima, já que imagem e vetor são desenhados por funções
diferentes. [FONTE] `Camera.capture_mobjects`:

```python
mobjects = self.get_mobjects_to_display(mobjects, **kwargs)   # ordena por z_index
for group_type, group in it.groupby(mobjects, self.type_or_raise):
    self.display_funcs[group_type](list(group), self.pixel_array)
```

O `groupby` agrupa **em blocos consecutivos preservando a ordem**, e a ordenação
por `z_index` acontece antes (dentro de `extract_mobject_family_members`, com
`use_z_index=self.use_z_index`). Então `img.set_z_index(-1)` de fato põe a
imagem atrás de um `Text`, e `Group(img, texto)` desenha na ordem que você
escreveu. Não há um "as imagens vão todas para trás".

Ainda em `type_or_raise` [FONTE], o mapa de despacho tem uma linha que vale
conhecer:

```python
Mobject: lambda batch, pa: batch,   # Do nothing
```

Um `Mobject` que não seja `VMobject`, `PMobject` nem `AbstractImageMobject`
é **silenciosamente não desenhado**. Se você herdou de `Mobject` direto e nada
aparece, é isto (e a matéria é de `manim-mobjects-customizados`).

### 7.8 Os dois retornos silenciosos — a imagem some sozinha

[FONTE] `Camera.display_image_mobject` desenha a imagem aplicando uma
**transformação de perspectiva do Pillow** sobre os quatro cantos, e tem dois
`return` sem log:

```python
if height_from_longest_side_in_pixels < 0.5:
    return                       # o quadrilátero é fino demais para conter pixel
...
try:
    transform_coefficients = np.linalg.solve(A, b)
except np.linalg.LinAlgError:
    return                       # três cantos colineares: matriz singular
```

Em português: **uma imagem quase de perfil, ou achatada até virar linha, deixa de
ser desenhada — sem erro, sem aviso.** Isso aparece em três situações reais:

- `Rotate(img, PI/2, axis=UP)` numa `ThreeDScene` — no meio do giro a imagem
  fica de canto e pisca fora;
- `img.stretch(0, dim=1)` ou uma animação que escala até 0 — o último frame
  some antes de chegar a zero;
- imagem com `scale` muito pequeno num render `-ql`: com poucos pixels de
  dispositivo, a altura efetiva cai abaixo de 0,5 px e ela desaparece **só na
  qualidade baixa**. Esse é traiçoeiro: iterando em `-ql` você "conserta" um
  defeito que não existe em `-qh`.

E o custo: essa transformação de perspectiva roda **por imagem, por frame**, no
Pillow, em CPU. Uma cena com muitas `ImageMobject` grandes é lenta por um motivo
que não aparece em nenhum profiler de Manim. Se a imagem está parada, o cache de
partial movies ajuda (`manim-performance-cache`); se ela se move, não há atalho
além de reduzir os pixels do arquivo.

---

## 8. Imagem de fundo — três caminhos, e o certo é o primeiro

### 8.1 `ImageMobject` atrás de tudo (recomendado)

```python
class ComFundo(Scene):
    def construct(self):
        fundo = ImageMobject("assets/fundo.jpg")
        fundo.height = config.frame_height            # 8 — cobre a altura
        fundo.set_z_index(-10)
        self.add(fundo)                               # adicionar primeiro já o põe atrás
        self.play(FadeIn(Text("olá", color=WHITE)))
```

É o único caminho que se comporta como qualquer outro mobject: anima, escala,
recebe `set_opacity`, respeita `z_index` (§7.7) e sobrevive a `Scene.clear()` só
se você quiser. **Cuidado com a proporção:** ajustar a altura para
`frame_height` deixa faixas laterais se a imagem não for 16:9. Para cobrir o
quadro inteiro sem deformar, escale pela dimensão que falta e aceite o corte:

```python
fundo.height = config.frame_height
if fundo.width < config.frame_width:
    fundo.width = config.frame_width      # agora sobra em cima e embaixo — cortado pela câmera
```

(Enquadramento e a conta de "cabe na tela" são de `manim-layout-posicionamento`.)

### 8.2 `Camera(background_image=…)` — corta, não redimensiona

[FONTE] `camera/camera.py`, em `init_background`:

```python
if self.background_image is not None:
    path = get_full_raster_image_path(self.background_image)
    image = Image.open(path).convert(self.image_mode)
    # TODO, how to gracefully handle backgrounds with different sizes?
    self.background = np.array(image)[:height, :width]
```

O `TODO` no fonte é a documentação honesta desta função. Ela **recorta a partir
do canto superior esquerdo** e nunca redimensiona. Portanto:

- a imagem tem de ter **exatamente a resolução do render**. Em `-qh` são
  1920×1080; em `-qm`, 1280×720; em `-ql`, 854×480. **Trocar de qualidade troca
  o enquadramento do seu fundo**;
- imagem **maior**: você vê só o canto superior esquerdo;
- imagem **menor**: [NÃO VERIFICADO] `self.background` fica com a forma da
  imagem, e `Camera.reset` faz `set_pixel_array(self.background)` — que, com
  formas diferentes, **substitui o buffer inteiro** pelo array menor
  (`camera.py:359-366`). O render passa a produzir frames do tamanho errado. O
  mecanismo está no fonte; a falha exata não foi reproduzida.

Como acionar, já que não há flag de CLI nem chave de `manim.cfg` para isso
[HOJE, `grep` em `_config/default.cfg`]:

```python
class ComFundo(Scene):
    def setup(self):
        self.camera.background_image = "assets/fundo-1920x1080.png"
        self.camera.init_background()
        super().setup()
```

**Quando vale a pena:** quando o fundo é literalmente o papel de parede, não
participa de nada e você quer que ele nem entre na lista de mobjects (uma coisa
a menos para o `z_index` e para o `Transform` esbarrarem). Fora disso, §8.1.

### 8.3 `color_using_background_image` — a imagem DENTRO da forma

[ÍNDICE] `VMobject.color_using_background_image(background_image: Image | str)`,
mais `get_background_image()` e `match_background_image(vmobject)`. Também
chega por `set_style(background_image=…)` e pelo construtor de `VMobject`.

```python
titulo = Text("MANIM", font_size=144)
titulo.color_using_background_image("assets/textura.jpg")
```

Duas coisas que o fonte revela e que mudam o uso:

1. **[FONTE] ele faz `self.set_color(WHITE)` e propaga para os submobjects**
   (`vectorized_mobject.py:773-778`). Ou seja, **descarta a cor que o objeto
   tinha**. Aplique-o **antes** de qualquer estilo, nunca depois — senão você
   perde a pintura sem entender por quê. (`manim-color-theming` também registra
   esse efeito colateral; a fronteira está na §13.)
2. **[FONTE] é um estêncil em espaço de TELA, não uma textura colada no objeto.**
   Em `BackgroundColoredVMobjectDisplayer.display` a forma é desenhada branca num
   array auxiliar e multiplicada pela imagem **redimensionada para o quadro
   inteiro** (`resize_background_array_to_match(back_array, pixel_array)`).
   Consequência: **mover a forma revela outra parte da foto**, e girar não gira a
   textura. Para uma palavra parada com textura é perfeito; para um objeto que
   se desloca, o efeito parece um recorte de papel deslizando sobre uma foto
   fixa — que às vezes é o que se quer, mas nunca por acidente.

[FONTE] O caminho da imagem passa por `get_full_raster_image_path` (as mesmas
regras da §2.1) e o array fica em cache por `str(image)` dentro do displayer.

---

## 9. Renderer: o vetor atravessa, o raster não

| Classe | Metaclasse `ConvertToOpenGL`? | Sob `--renderer opengl` |
|---|---|---|
| `SVGMobject` | **sim** [FONTE `svg_mobject.py`: `class SVGMobject(VMobject, metaclass=ConvertToOpenGL)`] | vira a variante OpenGL sozinho |
| `VMobjectFromSVGPath` | **sim** [FONTE, mesma linha de declaração] | idem — e só aqui os três booleanos dele passam a ter efeito |
| `AbstractImageMobject` / `ImageMobject` | **não** [FONTE `image_mobject.py`: `class AbstractImageMobject(Mobject)`] | ver abaixo |

[HOJE] Existe uma classe separada — [ÍNDICE] `OpenGLImageMobject`, em
`manim.mobject.opengl.opengl_image_mobject`, categoria `mobject/opengl`, **fora
do star import** — e ela herda de `OpenGLTexturedSurface`. Não é uma tradução
transparente:

```python
OpenGLImageMobject(filename_or_array, width=None, height=None,
                   image_mode="RGBA", resampling_algorithm=Resampling.BICUBIC,
                   opacity=1, gloss=0, shadow=0, **kwargs)
```

[FONTE] **A regra de tamanho é outra**: sem `width` nem `height`, ela nasce com
**4 unidades de altura** e largura proporcional — não tem `scale_to_resolution` e
não depende dos pixels do arquivo. Trocar de renderer troca o tamanho da imagem
na tela.

[NÃO VERIFICADO] `ImageMobject` sob `--renderer opengl`: o renderer OpenGL
desenha por `get_shader_wrapper_list`, que só existe em `OpenGLMobject`
[FONTE `opengl_mobject.py:2944`], e [HOJE] `grep -rn "ImageMobject" renderer/*.py`
**não devolve nada** — o renderer OpenGL não conhece a classe. O resultado mais
provável é `AttributeError`; não renderizei para confirmar. **A recomendação
prática independe do resultado:** se a cena carrega raster e você precisa de
OpenGL, importe `OpenGLImageMobject` explicitamente e ajuste o tamanho na mão.

Isso reforça a §1: **em projeto que pode trocar de renderer, o SVG é o formato
seguro.** Escolha de renderer, custo e NVENC são de `manim-gpu-encoding`.

---

## 10. Receitas

### 10.1 O logotipo de terceiro, do arquivo ao palco

```python
from pathlib import Path
from manim import SVGMobject, Scene, FadeIn, UR

AQUI = Path(__file__).resolve().parent

class Abertura(Scene):
    def construct(self):
        logo = SVGMobject(str(AQUI / "assets" / "marca.svg"), height=1.2)
        logo.to_corner(UR, buff=0.5)
        self.play(FadeIn(logo, run_time=0.6))
        self.wait()
```

Antes de escrever a cena, **prepare o arquivo** — cinco minutos que economizam
três renders:

1. **converta texto em contorno** (§3.5). Sem isso, some;
2. **achate gradientes** para cor sólida (§3.6). Sem isso, some;
3. **aplique/remova `clip-path` e `mask`** (§3.6). Sem isso, sobra;
4. **remova a área de trabalho transparente** (`viewBox` justo no desenho, §3.8).
   Sem isso, o tamanho mente;
5. **nomeie as camadas** que você vai querer pintar (§5.4).

No Inkscape, o passo 1 e o 4 saem de um comando só:

```bash
inkscape --export-type=svg --export-text-to-path --export-area-drawing \
         -o marca-limpa.svg marca.svg
```

[NÃO VERIFICADO] — o Inkscape não foi executado nesta sessão, e nem sei se ele
está instalado nesta máquina. Confira as flags com `inkscape --help` antes.

Depois, o teste sem render (§12) confirma que sobrou desenho.

### 10.2 O ícone monocromático que segue o tema

Ícone de biblioteca (Lucide, Feather, Material) costuma ser traço puro, sem
preenchimento, `viewBox="0 0 24 24"` — exatamente o caso que entra invisível
(§5.3). A forma que funciona:

```python
def icone(nome: str, altura: float = 0.9, cor=TINTA) -> SVGMobject:
    """Ícone de contorno da pasta assets/icones, na cor do tema."""
    return SVGMobject(
        str(AQUI / "assets" / "icones" / f"{nome}.svg"),
        height=altura,
        stroke_color=cor,
        stroke_width=2.5,      # unidades do Manim, aplicadas depois da escala
        fill_opacity=0,
    )
```

Esse helper é o lugar certo para o padrão — e ele pertence ao `tema.py` do
projeto, ao lado de `txt()` e da paleta (matéria de **`manim-tema-projeto`**).
Escrever `SVGMobject(...)` cru dentro de uma cena é o começo de doze ícones com
doze espessuras diferentes.

### 10.3 A captura de tela

```python
print_ = ImageMobject(str(AQUI / "assets" / "terminal-1080.png"))
print_.height = 5.4                     # 67,5% do quadro
moldura = SurroundingRectangle(print_, color=DIVISORIA, buff=0, stroke_width=2)
self.play(FadeIn(Group(print_, moldura)))
```

Três regras que economizam retrabalho:

- **capture na resolução da entrega ou acima** e **não amplie na cena** (§7.1).
  Um print de 800 px esticado para 5,4 unidades num render 1080p é reamostrado
  para cima e o texto do terminal fica ilegível;
- **corte no editor de imagem, não com a câmera.** Recortar movendo o
  `ImageMobject` para fora do quadro deixa pixels sendo transformados a cada
  frame sem aparecer (§7.8);
- **`SurroundingRectangle` funciona sobre `ImageMobject`** (ele lê a caixa
  delimitadora, que existe). É o jeito barato de dar borda a um print — mas
  `Group`, nunca `VGroup` (§7.6).

### 10.4 O que NÃO fazer entrar por aqui

| Tentação | Por que não | O que fazer |
|---|---|---|
| GIF animado como animação | carrega o primeiro quadro e para (§2.2) | refaça em Manim, ou entregue o GIF ao player do slide |
| "SVG" exportado de editor raster | é um `<image>` embrulhado: importa vazio e mudo (§3.5) | exporte PNG e use `ImageMobject` |
| diagrama do Figma com texto | o texto some (§3.5) | símbolo do SVG + `Text` do Manim por cima |
| logo em PNG num vídeo 4K | reamostra e borra (§7.1) | peça o SVG, ou um PNG com 2× a altura final em pixels |
| foto como `SVGMobject` | não existe | `ImageMobject` |
| fundo em `Camera(background_image=)` num projeto que renderiza em duas qualidades | o recorte muda com `-q` (§8.2) | `ImageMobject` no fundo (§8.1) |

---

## 11. Sintoma → causa → correção

| Sintoma | Causa provável | Correção |
|---|---|---|
| `OSError: … could not find X at either of these locations` | `cwd` diferente do que você imagina; extensão só é adivinhada no `assets_dir` | §2.1; use caminho absoluto derivado de `__file__` (§2.3) |
| `PermissionError` ao carregar SVG | o passo 5 escreve `nome_.svg` ao lado do original | §3.3; torne a pasta gravável ou copie o asset para uma pasta de trabalho |
| apareceram arquivos `*_.svg` na pasta de assets | render anterior morreu entre a escrita e o `unlink` | §3.3; podem ser apagados |
| `xml.etree.ElementTree.ParseError` | SVG malformado, ou `.svgz` (gzip) | descomprima; valide o XML |
| `KeyError: 'color'` / `'opacity'` / `'stroke_width'` vindo do construtor | `svg_default` parcial | §5.1 — as sete chaves |
| SVG entrou **vazio** (0 submobjects) | `<image>` embutido, ou tudo era `<text>` | §3.5; confira o log por `Unsupported element type` |
| sumiu **o nome da marca**, o símbolo ficou | `<text>` não é suportado | §3.5 — converter em contorno |
| SVG entrou com a **geometria certa e nada desenhado** | `fill` por gradiente + `stroke-width` herdado 0 | §3.6 e §5.3 |
| **sobrou** desenho que devia estar escondido | `clip-path`/`mask` ignorados | §3.6 — achatar no editor |
| parte do desenho veio, parte não | um elemento estourou e foi engolido pelo `except` | §3.7 — `grep` no log por `get_mobjects_from` |
| SVG **gigante** | `height=None` com unidades do arquivo | §4 |
| SVG **pequeno demais dentro da caixa certa** | área de trabalho transparente entra na caixa | §3.8 |
| contorno do SVG **grosso** depois de encolher | `scale` não escala `stroke_width` | §4, nota final |
| pintei o logo e ele virou um bloco de uma cor | `set_style(family=True)` do construtor | §5.2; use `id_to_vgroup_dict` (§5.4) |
| pintei e **não mudou** | você pintou no nível A um elemento que declara a própria cor | §5 — troque de nível |
| editei o `.svg` e a cena não mudou | cache em memória por nome de arquivo | §6 — `use_svg_cache=False` ou reiniciar o processo |
| imagem **borrada** | ampliada além dos pixels que tem | §7.1 |
| imagem **serrilhada** onde devia ser dura | reamostragem bicúbica em pixel art | §7.3 — `nearest` |
| `ValueError` ao pedir reamostragem `lanczos`/`box`/`hamming` | a docstring anuncia, o dicionário não tem | §7.3 |
| a foto virou uma silhueta colorida | `ImageMobject.set_color` sobrescreve o RGB | §7.4 |
| `AttributeError: 'ImageMobject' object has no attribute 'set_fill'` | não é `VMobject` | §1, §7.4 |
| `TypeError: Only values of type VMobject …` | `ImageMobject` num `VGroup` | §7.6 — `Group` |
| `TypeError: Create only works for VMobjects.` | `Create`/`Write` em imagem | §7.5 — `FadeIn` |
| `AssertionError: Mobject pixel array shapes incompatible` | `Transform` entre imagens de tamanhos diferentes em **pixels** | §7.5 |
| a imagem **some** no meio de um giro 3D | quadrilátero fino demais / matriz singular | §7.8 |
| a imagem some **só em `-ql`** | altura efetiva < 0,5 px de dispositivo | §7.8 |
| o fundo mudou de enquadramento ao trocar `-q` | `Camera(background_image=)` recorta | §8.2 |
| a textura "escorrega" quando a forma se move | `color_using_background_image` é estêncil de tela | §8.3 |
| a cor do objeto sumiu ao aplicar textura | `color_using_background_image` faz `set_color(WHITE)` | §8.3 |
| a imagem quebrou/mudou de tamanho ao trocar para `--renderer opengl` | outra classe, outra regra de tamanho | §9 |
| falha intermitente em lote, some ao rodar sequencial | corrida no `.svg` temporário | §3.3 |

---

## 12. Conferir sem renderizar

Quase tudo desta skill se verifica construindo o mobject e lendo atributos —
sem escrever um frame. Custa milissegundos e não usa GPU.

```python
# confere_assets.py
#   .venv/bin/python confere_assets.py
# (aqui o venv cru basta: nada disto toca LaTeX nem GPU. Se a cena também
#  usar Tex/MathTex, `source bin/manim-env.sh` antes — ver `manim-project` §3)
from manim import SVGMobject, ImageMobject, config

svg = SVGMobject("assets/marca.svg")
print("submobjects :", len(svg.submobjects))          # 0 => nada foi convertido (§3.4/§3.5)
print("ids         :", sorted(svg.id_to_vgroup_dict)) # nomes para pintar (§5.4)
print("tamanho     :", round(svg.width, 3), "x", round(svg.height, 3))
print("fill/stroke :", svg.get_fill_opacity(), svg.get_stroke_width())

img = ImageMobject("assets/print.png")
print("pixels      :", img.get_pixel_array().shape)   # (h, w, 4)
print("unidades    :", round(img.width, 3), "x", round(img.height, 3))
print("quadro      :", config.frame_width, "x", config.frame_height)
```

O que cada linha decide:

| Leitura | Conclusão |
|---|---|
| `len(svg.submobjects) == 0` | o arquivo não rendeu geometria — §3.5 é o primeiro suspeito |
| nas FOLHAS, `fill_opacity == 0 and stroke_width == 0` | vai entrar invisível — §5.3. **Leia as folhas**: no pai esses dois são 0 mesmo num SVG visível |
| nas folhas, `fill == #000000` onde o arquivo tinha gradiente | vai entrar como chapa preta — §3.6 |
| `svg.height > 8` | não cabe no quadro |
| `img.height > 8` | idem — e a conta está na §7.1 |
| `img.get_pixel_array().shape[0]` menor que `altura_desejada × 135` | vai borrar ao ampliar |

E o log, que é onde o importador confessa:

```bash
bin/mx render cena.py Cena -q l 2>&1 \
  | grep -iE "unsupported element|get_mobjects_from|could not find"
```

**O que esta seção NÃO substitui.** Nada aqui prova que o desenho está *certo* —
só que ele existe, tem tamanho e tem tinta. Contraste, sobreposição, corte na
borda e "ficou feio" só aparecem no PNG, e o ciclo **escrever → renderizar
rápido → OLHAR o PNG → corrigir** é de **`manim-verificacao-visual`**.
Renderizou e não olhou: não terminou.

**Os itens que ficaram [NÃO VERIFICADO] nesta redação**, e o experimento mínimo
de cada um, para quem puder gastar CPU:

| Afirmação | Como fechar |
|---|---|
| ~~gradiente → forma invisível~~ **FECHADO, e deu o contrário**: gradiente → preto opaco (§3.6) | `se.Color('url(#g)')` devolve `#000000`, opacidade 1,0. Medido — a linha está na §3.6 |
| `clip-path` ignorado (§3.6) | SVG com um círculo recortando um quadrado; comparar `len(submobjects)` e um PNG |
| corrida do `.svg` temporário (§3.3) | dois processos importando o mesmo SVG em laço, à espera de `FileNotFoundError` |
| `Camera(background_image)` menor que o quadro (§8.2) | um PNG 100×100 como fundo em `-ql`; ver se o mp4 sai e com que tamanho |
| `ImageMobject` sob `--renderer opengl` (§9) | uma cena de uma linha com `-ql --renderer opengl` |
| as flags do Inkscape (§10.1) | `inkscape --help` |

---

## 13. Onde esta skill para

A fronteira, assunto por assunto. Onde a linha é fina, ela está explicada.

| Assunto | Skill dona | A linha |
|---|---|---|
| escrever texto/fórmula na tela, `t2c`, fonte, nitidez do glifo | **`manim-text-latex`** | ela é dona do `register_font` como **tipografia** (o `with`, o nome da família, a fonte que vira Noto Sans); **eu** sou dono do `register_font` como **caminho de arquivo** (§2.4). Texto *dentro* de um SVG é meu — e a resposta é "ele some" (§3.5) |
| escolher cor, contraste, paleta, fundo, alfa | **`manim-color-theming`** | ela decide **qual** cor; eu digo **como** a cor chega num SVG importado (§5) e por que `color_using_background_image` apaga a que havia (§8.3) |
| catálogo de formas, `VGroup` × `Group`, `Brace*` | **`manim-mobjects`** | as cinco classes `Brace*` moram em `mobject/svg` mas são dela. A regra `VGroup` × `Group` é dela; aqui aparece só porque a imagem é a causa mais comum do `TypeError` (§7.6) |
| posicionar, alinhar, medir, enquadrar, `z_index`, `index_labels` | **`manim-layout-posicionamento`** | tudo que acontece **depois** que o asset virou mobject |
| `tema.py`: o helper `icone()`, a paleta, a escala | **`manim-tema-projeto`** | eu dou o corpo da função (§10.2); ela diz onde a função mora |
| animar, `Transform`, `rate_func` | **`manim-animations`** / **`manim-composicao-ritmo`** | a §7.5 **desta** skill é só a lista do que **quebra** com raster; escolher a animação é lá |
| olhar o PNG, comparar frames, achar corte na borda | **`manim-verificacao-visual`** | a §12 confere só o que dá para conferir **sem** render |
| cache de partial movies, custo de rasterizar, `media/` | **`manim-performance-cache`** | o `SVG_HASH_TO_MOB_MAP` (§6) é um cache **em memória, do import**, sem relação com `--disable_caching` |
| lote, paralelismo, isolar diretório por worker | **`manim-batch-pipeline`** | a corrida do `.svg` temporário (§3.3) é minha para diagnosticar e dela para resolver |
| codec, NVENC, renderer, peso do arquivo | **`manim-gpu-encoding`** | a §9 diz **qual classe** sobrevive à troca de renderer, não qual renderer escolher |
| som, música, legenda `.srt` | **`manim-som-legendas`** | outro tipo de asset, outra resolução de caminho (`get_full_sound_file_path`) |
| descobrir se um nome existe / qual é a assinatura | **`manim-api-discovery`** | — |
| render que falhou por ambiente, traceback, bissecção | **`manim-troubleshooting`** | a §11 é específica de asset; erro de ambiente é lá |
| o `<Midia>` do deck `~/Projects/aulas` (GIF, foto, QR no **slide**) | **`aula-midia`**, naquele repositório | é HTML/React, não Manim. Um GIF num slide **não passa** por esta skill (§1) |

**Buracos declarados que encostam aqui** e que não têm skill dona — não invente
uma, diga que não tem:

- **`ImageMobjectFromCamera`** [ÍNDICE, `mobject/core`] existe e é como a
  `ZoomedScene` mostra o conteúdo da câmera ampliada dentro do quadro. A classe é
  desta família, mas o uso é de **`manim-camera-2d`**; nenhuma das duas a cobre
  em profundidade hoje;
- os **48 mobjects `OpenGL*`**, incluindo `OpenGLImageMobject` e
  `OpenGLTexturedSurface`, são **buraco declarado de propósito**
  (`manim-project` §13.7). A §9 cobre só o suficiente para você não ser
  surpreendido;
- `VectorField` e `StreamLines` usam `color_using_background_image` por dentro
  [FONTE `mobject/vector_field.py:821, 864`], mas campos e fluxo são buraco
  declarado;
- `drag_pixels`, `invert_image`, `change_to_rgba_array` [ÍNDICE, todos no star
  import] são utilitários de pixel de `utils/images.py` que ninguém documenta.
  Estão aqui pelo nome e pela assinatura; para que servem de verdade, leia o
  fonte — são 20 linhas cada.

---

## 14. Antes de dar por pronto

1. o caminho do asset é **absoluto derivado de `__file__`** ou você conferiu de
   qual `cwd` o render roda? (§2.3)
2. o SVG passou pelas cinco preparações — texto em contorno, gradiente achatado,
   clip aplicado, área de trabalho justa, camadas nomeadas? (§10.1)
3. `len(svg.submobjects)` é maior que zero, e `fill_opacity`/`stroke_width` não
   são ambos zero? (§12)
4. o tamanho foi **declarado** (`height=` no SVG, altura em unidades na imagem) e
   não herdado por acaso? (§4, §7.1)
5. a imagem tem pixels suficientes para o tamanho que vai ocupar
   (`altura_em_unidades × 135` no mínimo, em 1080p)? (§7.1)
6. imagem raster está em `Group`, nunca em `VGroup`, e não recebe `Create`? (§7.5, §7.6)
7. o log do render está limpo de `Unsupported element type` e de
   `Exception occurred in 'get_mobjects_from'`? (§3.7)
8. sobrou algum `*_.svg` na pasta de assets? (§3.3)
9. você **olhou o PNG**? (`manim-verificacao-visual`)
