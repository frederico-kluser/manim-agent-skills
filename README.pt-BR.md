# Manim Agent Skills

> Ambiente [Manim](https://www.manim.community/) com aceleração por GPU, **14 Agent Skills** e um
> **índice offline de 5.523 símbolos** — para um agente de código dirigir o Manim como API, em vez
> de chutar nome de método a partir de treino desatualizado.

[![Manim CE](https://img.shields.io/badge/Manim_CE-0.21.0-blue)](https://github.com/ManimCommunity/manim)
[![ManimGL](https://img.shields.io/badge/ManimGL-master_(wgpu)-blueviolet)](https://github.com/3b1b/manim)
[![Skills](https://img.shields.io/badge/agent_skills-14-orange)](#as-14-skills)
[![API](https://img.shields.io/badge/símbolos_de_API-5.523-teal)](#o-índice-de-api)
[![NVENC](https://img.shields.io/badge/NVENC-verificado-brightgreen)](#gpu-o-que-de-fato-acelera)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

🇬🇧 **[README in English](README.md)** · As 14 skills estão escritas em português.

---

## O problema

Peça uma animação Manim a um agente e três coisas dão errado:

1. **Ele inventa API.** `ShowCreation` × `Create`, `TexMobject` × `MathTex`, `get_graph` ×
   `ax.plot` — os dois forks divergiram, e metade dos tutoriais descreve uma versão que não
   existe mais.
2. **Ele não acha o arquivo gerado.** O caminho depende de `media_dir` × nome do módulo ×
   qualidade × `output_file`. O agente chama `manim`, depois adivinha, e adivinha errado.
3. **Ele não sabe o que está lento.** "Usar a GPU" não é uma coisa só. O Manim tem *duas* etapas
   caras independentes, e o conselho popular embaralha as duas.

Este repo resolve os três, com tudo verificado contra os pacotes realmente instalados.

## Começando

```bash
git clone https://github.com/frederico-kluser/manim-agent-skills.git
cd manim-agent-skills
bin/setup                    # ManimCE + manimx   (--with-gl para o ManimGL, --all para tudo)
bin/mx doctor                # exit 0 = pronto

bin/mx render scenes/exemplos.py OlaManim -q h --codec nvenc --json
```

```json
[{ "scene_name": "OlaManim", "success": true,
   "output_file": "/caminho/abs/media/videos/exemplos/1080p60/OlaManim.mp4",
   "codec": "h264_nvenc", "resolution": [1920, 1080], "elapsed_s": 2.41 }]
```

O caminho vem do próprio `SceneFileWriter`. Sem adivinhação.

**Requisitos:** Python ≥ 3.11 (o ManimCE 0.21 exige), mais LaTeX e `ffmpeg` se você quiser
`MathTex` e o ManimGL. **GPU não é obrigatória** — tudo degrada para CPU. O `bin/setup` avisa o
que falta em vez de quebrar.

## GPU: o que de fato acelera

Uma renderização tem **duas etapas caras e independentes**. Confundir as duas é o motivo de
"é só usar a GPU" tantas vezes não acelerar nada.

| Etapa | Padrão | Acelerada por |
|---|---|---|
| **1. Rasterizar a geometria** em frames | Cairo (CPU) | `--renderer opengl` (ModernGL) · ManimGL (wgpu/Vulkan) |
| **2. Codificar** os frames em vídeo | libx264 (CPU) | `--codec nvenc` (NVENC) |

Medido com `bin/mx bench` numa RTX 4070 Laptop, 1080p60, em várias execuções:

| Cenário | Tempo |
|---|---|
| limitado por encoding — cairo + x264 | ~5,0–5,7 s |
| limitado por encoding — cairo + **NVENC** | **~2,7–3,0 s** (≈ −45%) |
| limitado por geometria — cairo + x264 | ~5,7–5,8 s |
| limitado por geometria — cairo + NVENC | ~5,9–6,3 s (**sem ganho**) |
| limitado por geometria — **opengl** + NVENC | ~5,1–5,4 s (≈ −10%) |

**O ganho do NVENC em cena limitada por encoding é grande e consistente. Em cena limitada por
geometria ele não faz nada** — ali quem ajuda é o renderer, e esse ganho é real porém modesto e
ruidoso. Os números variam entre execuções; `bin/mx bench` mede a *sua* máquina em vez de pedir
que você acredite nestes.

### Fazer o NVENC funcionar foi a parte difícil

O ManimCE **não chama mais o binário do `ffmpeg`**. Desde a 0.19 ele usa **PyAV** direto, com o
codec fixo em `scene_file_writer.py` (`libx264`, `crf=23`). O `config.ffmpeg_executable` foi
removido. Toda receita de "aponte o ffmpeg para um wrapper NVENC" que circula por aí está morta.

O `manimx.gpu` resolve sem tocar nas entranhas do Manim: intercepta `av.open` **apenas durante**
`open_partial_movie_stream` e devolve um proxy que reescreve o `add_stream`. Como a concatenação
final do Manim é *stream copy* puro (`add_stream_from_template`), trocar o codec de cada animação
muda o arquivo inteiro.

```python
from manimx import enable_nvenc
enable_nvenc(codec="hevc_nvenc", profile="quality")
```

O ManimGL é o oposto — ele ainda chama o binário do `ffmpeg`, então é um flag
(`--vcodec h264_nvenc`), que o `bin/manimgl` injeta sozinho quando há GPU NVIDIA.

## O índice de API

Gerado por reflexão sobre os pacotes **instalados** (`bin/mx api-dump`), não raspado da
documentação — o que importa, porque as classes OpenGL do ManimCE (`OpenGLMobject`,
`OpenGLRenderer`, …) **não têm página nenhuma** no site oficial.

| Arquivo | O que é | Tamanho |
|---|---|---|
| `api/manim-ce-index.tsv` | 1 símbolo por linha — **grepe aqui** | 528 KiB |
| `api/manim-ce-methods.tsv` | 1 método por linha, com classe e assinatura | 6,8 MiB |
| `api/manim-ce-toplevel.md` | tudo que `from manim import *` traz | 33 KiB |
| `api/manim-ce-by-category.md` | navegação por categoria | 570 KiB |
| `api/manim-ce-inheritance.txt` | árvore de herança | 6 KiB |
| `api/manim-ce-api.json.gz` | tudo, estruturado (lido pela CLI) | 1,4 MiB |
| `api/manimgl-*` | o mesmo, para o ManimGL | |
| `api/ce-vs-gl.md` | mapa de compatibilidade entre os forks | |

**Cobertura:** 338 classes · 285 funções · 4.900 constantes · 5.523 símbolos.
Com métodos herdados — só o `Circle` indexa **264 métodos** (4 próprios, 260 herdados). É esse o
ponto: um agente que só enxerga os métodos próprios conclui que a API não existe.

```bash
bin/mx find "transform" --kind class     # busca por nome, docstring ou nome de método
bin/mx show Circle                       # assinatura completa + todos os métodos
bin/mx show Axes --own-only --json

# ou simplesmente grep
awk -F'\t' '$1=="class" && $3 ~ /^animation/ {print $2}' api/manim-ce-index.tsv
```

## As 14 skills

Em `.claude/skills/`, no formato [Agent Skills](https://code.claude.com/docs/en/skills). A porta
de entrada é **`manim-project`**, que roteia para as demais.

| Skill | Assunto |
|---|---|
| **`manim-project`** | mapa do projeto e roteamento — **comece por esta** |
| `manim-api-discovery` | achar qualquer classe/método/constante sem chutar |
| `manim-render-api` | renderizar, controlar saída, formatos, cache |
| `manim-gpu-encoding` | NVENC, renderers, PRIME offload, benchmark |
| `manim-mobjects` | formas, posicionamento, grupos, submobjects |
| `manim-animations` | catálogo completo de animações, timing, composição |
| `manim-color-theming` | cor, fundo, tema, canal alfa |
| `manim-text-latex` | Text/MarkupText/Tex/MathTex, colorir parte de fórmula |
| `manim-graphs-plots` | eixos, gráficos de função, dados, grafos |
| `manim-3d-camera` | cenas 3D e movimento de câmera |
| `manim-updaters-valuetracker` | animação reativa |
| `manim-troubleshooting` | sintoma → causa → correção |
| `manimgl-3b1b` | ManimGL e tradução GL ↔ CE |
| `manim-batch-pipeline` | lote, paralelismo, CI |

Cada uma foi escrita contra *esta* instalação, com as armadilhas verificadas em vez de repetidas
de blog.

## Correções à documentação que todo mundo repete

Tudo verificado no ManimCE 0.21.0 / ManimGL master. Tutoriais de 2024–2025 erram nestes pontos:

| Afirmação comum | Na realidade |
|---|---|
| `manim -c WHITE arq.py Cena` muda o fundo | `-c` virou `--config_file`. **`--background_color` foi removido.** |
| Hex de 3 dígitos (`#F00`) quebra o parser | Funciona: resolve para `#FF0000`. O que quebra é hex **sem** `#`. |
| O Manim canaliza frames para o binário `ffmpeg` | A CE usa **PyAV** desde a 0.19; `config.ffmpeg_executable` não existe mais. |
| Dá para trocar o codec por config na CE | Não dá — é fixo no código. Por isso existe o `manimx.gpu`. |
| ManimGL é OpenGL | **O master é wgpu/Vulkan.** O wheel do PyPI é OpenGL. Os dois dizem `1.7.2`. |
| O fundo padrão do ManimGL é preto | É `#333333`. |
| A CE removeu `--renderer=opengl` | Não removeu — ele recebeu correções na 0.21.0. |
| ManimCE roda em Python 3.8+ | Exige **3.11+**. Em Python antigo o `pip` instala uma CE velha **sem erro**. |
| Faça `pip install IPython==8.0.1` | Conselho de 2022 que a FAQ oficial ainda repete. Só se você reproduzir o bug. |

Duas pegadinhas de encoder, ambas encontradas durante o desenvolvimento:

- **`profile=high` só existe em H.264.** HEVC quer `main`; AV1 não tem a opção e devolve `EINVAL`.
  Como o PyAV abre o encoder preguiçosamente *no primeiro frame*, isso estouraria no meio da
  renderização — então o `manimx.gpu.validate_encoder()` faz um encode de teste **e o remux**
  antes. É assim também que ele detecta que AV1 é inutilizável aqui (a concatenação precisa de um
  *encoder* `libdav1d` que não existe) e cai no libx264 de forma limpa.
- **O ffmpeg ignora `-crf` em silêncio com NVENC.** Sem erro, sem aviso — você só não recebe a
  qualidade que pediu. Use `cq`.

## Estrutura

```
bin/setup              bootstrap a partir de um clone limpo
bin/mx                 a CLI para agentes (saída JSON)
bin/manim  bin/manimgl wrappers: LaTeX no PATH, ambiente de GPU, venv certa
manimx/                a camada de API
  gpu.py                 detecção de GPU + o patch NVENC
  render.py              renderização programática, caminho real de saída
  presets.py             presets de qualidade / codec / tema
  introspect.py          o extrator de API
  apidiff.py             mapa de compatibilidade CE ↔ GL
  bench.py               benchmark CPU vs GPU
  cli.py                 `mx`
tools/batch_render.py  renderização em lote multi-processo
tools/check_publishable.sh  guarda de publicação (segredos, caminhos, tamanhos)
scenes/                6 exemplos CE + 3 exemplos ManimGL
api/                   o índice gerado (versionado de propósito)
.claude/skills/        as 14 skills
manim.cfg              config do ManimCE   custom_config.yml   config do ManimGL
pyproject.toml         pacote `manimx`     uv.lock
```

`media/` e `media-gl/` aparecem depois da primeira renderização; estão no `.gitignore`.

## Renderização em lote

```bash
.venv/bin/python tools/batch_render.py scenes/ -q h --codec nvenc -j 4 --json
```

Multi-processo de propósito: o `config` do Manim é um global mutável, então duas cenas no mesmo
processo se corrompem. Dois modos de falha que este script já trata, ambos reproduzidos aqui:

- **Corrida de LaTeX.** Dois workers compilando no mesmo `media/Tex` colidem na limpeza dos `.aux`
  (`FileNotFoundError`), de forma não determinística. Resolvido isolando o `tex_dir` por worker —
  colocado **fora** de `media/Tex`, porque a limpeza do Manim faz
  `for f in tex_dir.iterdir(): f.unlink()` sem checar se é diretório, o que quebraria toda
  renderização de LaTeX seguinte.
- **Limite de sessões NVENC.** GPUs de consumidor limitam encoders simultâneos; 4 workers
  verificados aqui.

## Manutenção

```bash
VIRTUAL_ENV=.venv    uv pip install -U manim
VIRTUAL_ENV=.venv-gl uv pip install -U "manimgl @ git+https://github.com/3b1b/manim.git"
bin/mx api-dump && bin/mx api-diff     # o índice precisa acompanhar a instalação
bin/mx doctor
```

## Licença e atribuição

MIT — veja [LICENSE](LICENSE). Avisos de terceiros em [NOTICE.md](NOTICE.md).

**Sem afiliação, endosso ou relação de fork** com a [Manim
Community](https://github.com/ManimCommunity/manim) ou o
[3Blue1Brown](https://github.com/3b1b/manim). Nenhum código upstream é embutido aqui: o `manimx`
chama e faz patch do Manim instalado em tempo de execução. O `api/` contém nomes, assinaturas e a
primeira linha de cada docstring, extraídos por reflexão desses projetos (MIT), e o
`custom_config.yml` deriva do `default_config.yml` do ManimGL.
