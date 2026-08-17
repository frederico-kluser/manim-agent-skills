---
name: manim-troubleshooting
description: >-
  Diagnosticar e corrigir falhas no Manim — erros de LaTeX, objetos
  invisíveis ou fora do quadro, animações que não acontecem, arquivo de
  saída não encontrado, cache servindo resultado velho, travamentos,
  problemas de GPU/OpenGL, e erros de codec. Use SEMPRE que uma
  renderização falhar, produzir saída errada, ou quando um AttributeError
  /TypeError/ValueError vier do Manim. Traz uma tabela sintoma → causa →
  correção e o procedimento de bissecção.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
---

# Diagnóstico

## Comece sempre por aqui

```bash
bin/mx doctor          # exit != 0 aponta o que está quebrado
bin/mx gpu             # GPU, PRIME, encoders
```

Se o `doctor` estiver verde, o problema é da cena, não do ambiente.

## Tabela sintoma → causa → correção

### Ambiente

| Sintoma | Causa | Correção |
|---|---|---|
| `LaTeX Error` / `latex: command not found` | TinyTeX fora do PATH | use `bin/mx` ou `bin/manim`, nunca o `manim` do sistema |
| `ModuleNotFoundError: manim` | venv errado | `bin/mx`, ou `.venv/bin/python` |
| `ModuleNotFoundError: manimlib` | está no venv da CE | use `bin/manimgl` |
| Versão do Manim antiga demais | `pip install manim` em Python < 3.11 resolve para trás **sem erro** | confira com `bin/mx doctor`; exige 3.11+ |
| `dvisvgm not found` | pacote TeX faltando | `tlmgr install dvisvgm` com o PATH do TinyTeX |

### Nada aparece / aparece errado

| Sintoma | Causa | Correção |
|---|---|---|
| Objeto invisível | `set_fill` sem `opacity` | `set_fill(BLUE, opacity=1)` |
| Tudo invisível em fundo branco | traço branco em fundo branco | `Text.set_default(color=BLACK)` etc., ou `apply_theme("whiteboard")` |
| Objeto fora do quadro | coordenada além de ±7,1 / ±4 | `mob.get_center()`; use `ax.c2p()` em gráficos |
| Objeto no lugar errado | confundiu `move_to` (absoluto) com `shift` (relativo) | |
| Rotação de ~14 voltas | passou graus onde se espera radianos | `90 * DEGREES` |
| Objeto deforma ao girar | `.animate.rotate()` interpola em linha reta | use a classe `Rotate` |
| Animação não acontece | esqueceu `self.play`, ou usou `Transform` e depois animou o alvo | ver skill `manim-animations` |
| Etiqueta "grudou" e não para | updater não removido | `mob.clear_updaters()` |
| Updater não roda | o objeto não foi adicionado à cena | `self.add(always_redraw(...))` |
| Cor só no contorno de uma fórmula | precisa isolar submobjects | `MathTex(r"{{a}}+{{b}}")` + `set_color_by_tex` |
| `ValueError: Color X not found` | hex sem `#` | `"#FF0000"` |
| `FileNotFoundError` ao passar `-c COR` | na CE 0.21 `-c` é `--config_file`; `--background_color` foi **removido** | use `manim.cfg`, `config.background_color`, ou `mx render --background` |

### LaTeX

| Sintoma | Causa | Correção |
|---|---|---|
| `\i`, `\f`, `\n` sumiram | faltou raw string | `r"\int"` |
| `! Undefined control sequence` | pacote LaTeX faltando | `TexTemplate().add_to_preamble(r"\usepackage{...}")`, e `tlmgr install` |
| Fórmula renderiza como texto corrido | usou `Tex` onde queria `MathTex` | |
| Chaves literais somem | `{{ }}` é sintaxe do Manim, não do LaTeX | separe: `{ {` |
| Compilação lenta | cada string nova compila um documento | reaproveite objetos; use `Text` quando não for matemática |

Para ver o erro real do LaTeX:

```bash
bin/manim -ql --no_latex_cleanup cena.py Cena 2>&1 | grep -A5 "! LaTeX Error"
ls media/Tex/*.log && tail -40 media/Tex/*.log
```

### Saída

| Sintoma | Causa | Correção |
|---|---|---|
| Não acho o arquivo gerado | o caminho depende de `media_dir` + módulo + qualidade | `bin/mx render --json` e leia `output_file` |
| Renderizou mas nada mudou | cache servindo *partial movie* antigo | `--no-cache`, ou `bin/manim --flush_cache` |
| `--renderer=opengl` não gera arquivo | falta `--write_to_movie` | use `bin/mx render --renderer opengl` (já injeta) |
| Transparência não funciona | saiu `.mp4`; alfa exige `.mov`+qtrle | `bin/mx render -t` |
| Último frame cortado | cena acaba junto com a animação | `self.wait(0.5)` no fim |
| GIF gigante | GIF com paleta em 1080p60 | `--format gif -q m` e reduza a duração |

### GPU e codec

| Sintoma | Causa | Correção |
|---|---|---|
| OpenGL usa a Intel | notebook híbrido, sem PRIME | use `bin/*`, ou exporte `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia` |
| `avcodec_open2(...) returned 22` | opção inválida para aquele codec (ex.: `profile=high` em HEVC/AV1) | a camada `manimx` já valida antes; se for manual, ver `manimx.gpu.CODEC_PROFILE` |
| Erro de codec no meio da renderização | PyAV só abre o encoder no 1º frame | `manimx.gpu.validate_encoder()` antes |
| NVENC "não acelerou" | a cena é limitada por geometria, não por encoding | `bin/mx bench`; troque o **renderer**, não o codec |
| 4K trava / estoura memória | 8 GiB de VRAM | renderize 4K no `cairo`, ou entregue 1080p |
| ManimGL ignora o `crf` | o ffmpeg descarta `-crf` com `h264_nvenc`, **em silêncio** | use as opções de `cq` do NVENC |
| Muitos renders paralelos falham | limite de sessões NVENC | reduza a concorrência, ou use `x264` no batch |

## Procedimento de bissecção

Quando a cena falha e a mensagem não ajuda:

```bash
# 1. o ambiente está bom?
bin/mx doctor

# 2. o arquivo importa?
bin/mx scenes scenes/cena.py

# 3. isole o traceback completo
bin/mx render scenes/cena.py Cena -q l --json | python3 -c "
import json,sys; r=json.load(sys.stdin)[0]
print(r['error']); print(r.get('traceback_text'))"

# 4. só o último frame (pula toda a animação)
bin/mx render scenes/cena.py Cena -q l --format png

# 5. corte a cena ao meio com -n
bin/manim -ql -n 0,3 scenes/cena.py Cena
bin/manim -ql -n 3,6 scenes/cena.py Cena

# 6. cena mínima que reproduz
```

## Verbosidade e logs

```bash
bin/manim -ql -v DEBUG cena.py Cena
bin/manim -ql --log_to_file cena.py Cena && ls media/logs/
bin/mx render cena.py Cena --verbosity DEBUG
bin/mx -v render cena.py Cena          # traceback do próprio mx
```

## Inspeção visual — a ferramenta mais subestimada

Muito "bug" é só posicionamento. Renderize um PNG e olhe:

```python
class Debug(Scene):
    def construct(self):
        eq = MathTex(r"a^2 + b^2 = c^2")
        self.add(eq, index_labels(eq[0]))       # numera os glifos
        self.add(NumberPlane())                 # grade de referência
        self.add(Dot(ORIGIN, color=RED))        # origem
```

```bash
bin/mx render scenes/debug.py Debug --format png -q l
```

## Limpar tudo e recomeçar

```bash
rm -rf media/videos media/images media/Tex media/texts
bin/manim --flush_cache -ql cena.py Cena
```

Cuidado: `media/Tex` guarda o LaTeX compilado. Apagar torna a próxima
renderização bem mais lenta.

## Quando nada disso resolve

1. Confirme a versão: `bin/mx doctor`. Tutoriais de 2024-2025 descrevem
   ManimCE 0.18/0.19 e ManimGL OpenGL — as duas coisas mudaram.
2. Confirme que o símbolo existe **nesta** versão: `bin/mx show <Nome>`.
3. Confirme a assinatura: os parâmetros mudam entre versões.
4. Leia o código-fonte: `.venv/lib/python3.12/site-packages/manim/`.
