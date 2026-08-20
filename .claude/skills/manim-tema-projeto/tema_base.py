"""
tema_base.py — TEMPLATE de tema de projeto para ManimCE 0.21.

    Copie este arquivo para o SEU projeto como `tema.py`, ao lado das cenas,
    e edite os blocos marcados com `TODO`. Depois disso, TODA cena começa com

        from tema import *

        class MinhaCena(CenaBase):
            def construct(self) -> None:
                self.add(txt("A tese em uma frase", T_H2, TINTA, "SEMIBOLD"))

    e NENHUMA cena volta a escrever um hex, um `font_size=`, um nome de
    fonte, uma curva de easing ou um `Text(...)` cru.

POR QUE ISSO EXISTE (o resumo; a skill `manim-tema-projeto` traz a evidência)

  1. Em fundo claro, todo Mobject sem cor explícita SOME — o Manim escreve
     branco por padrão e não avisa. Um funil obrigatório (`txt()`) fecha o
     buraco na origem.
  2. `Text(font_size=22)` sai com as letras soltas das palavras: o cairo
     arredonda a posição X de cada glifo para inteiro, e em 22 o em mede ~6
     unidades de dispositivo. `_texto_nitido()` desenha em 720 e encolhe.
  3. Cor, fonte, tamanho e tempo espalhados por 8 mil linhas de cena não têm
     conserto barato. Aqui têm: um arquivo, uma edição.

O QUE ESTE ARQUIVO **NÃO** FAZ, DE PROPÓSITO

  - não mexe em `config.quality`, `pixel_width`, `pixel_height` nem
    `frame_rate` no topo do módulo (isso atropela o `-q` da linha de comando
    no CLI da CE — ver a skill, §9.3);
  - não define um `titulo()` que desenha cabeçalho: vídeo de slide não tem
    título interno (o `h2` do slide dá o contexto);
  - não carrega dados de um domínio específico. `numero()` é o mecanismo;
    o esquema do JSON é seu.

Este arquivo foi conferido por `py_compile` e por leitura do fonte do
ManimCE 0.21; ele NÃO foi executado nem renderizado na sessão que o escreveu.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    Line,
    Scene,
    Text,
    VGroup,
    config,
    rate_functions,
)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Onde estão as coisas
# ─────────────────────────────────────────────────────────────────────────────

#: A pasta deste arquivo (onde moram as cenas, se você seguiu a sugestão).
PASTA = Path(__file__).resolve().parent

#: A raiz do projeto. TODO: ajuste se o layout for outro.
RAIZ = PASTA.parent


# ─────────────────────────────────────────────────────────────────────────────
# 2. Números: uma fonte só, e um erro que se lê
# ─────────────────────────────────────────────────────────────────────────────
#
# Redigitar um número dentro de uma cena é o defeito que este bloco existe
# para impedir: o slide, o relatório e o vídeo têm que dizer a mesma coisa, e
# a única forma de garantir isso é os três lerem o mesmo arquivo.
#
# CARREGAMENTO DEFENSIVO, e isto é load-bearing: `tema.py` é importado por
# TODAS as cenas do projeto. Um `KeyError` aqui no import derruba o arquivo
# inteiro, inclusive as cenas que não tocam em número nenhum. Portanto:
# falhe TARDE (na função que consome) e com mensagem, nunca no import.

_ARQUIVO_DADOS = RAIZ / "dados" / "numeros.json"   # TODO: o seu caminho

DADOS: dict[str, Any] = (
    json.loads(_ARQUIVO_DADOS.read_text("utf-8")) if _ARQUIVO_DADOS.exists() else {}
)

#: Esquema sugerido: {"numeros": [{"id": "...", "valor": 42, "unidade": "%"}]}
NUMEROS: dict[str, dict[str, Any]] = {n["id"]: n for n in DADOS.get("numeros", [])}


def numero(id_: str, campo: str = "valor") -> Any:
    """O número `id_` do JSON de dados. Erro CLARO quando não existe.

    A mensagem LISTA os ids disponíveis — é o que transforma um erro de
    digitação de 10 minutos de caça em 2 segundos de leitura.
    """
    if id_ not in NUMEROS:
        disponiveis = ", ".join(sorted(NUMEROS)) or "(nenhum)"
        raise KeyError(
            f"número {id_!r} não existe em {_ARQUIVO_DADOS}. Existem: {disponiveis}"
        )
    return NUMEROS[id_][campo]


# ─────────────────────────────────────────────────────────────────────────────
# 3. Paleta — um nome por PAPEL, não por cor
# ─────────────────────────────────────────────────────────────────────────────
#
# TODO: troque os valores. Estes são PLACEHOLDERS neutros, escolhidos só para
# o arquivo rodar de cara e para as contas de contraste abaixo serem
# verdadeiras. O que você deve copiar são os NOMES, não os hex.
#
# Contraste WCAG sobre CANVAS, calculado (não medido em pixel):
#   TINTA 18,40 · TINTA_2 6,85 · TINTA_3 4,90 · ACENTO 5,90
#   VERDE 5,02 · VERMELHO 5,58 · LARANJA 5,17 · DIVISORIA 1,48
# Pisos: 4,5 para texto, 3,0 para barra/traço/fio. A DIVISORIA fica abaixo dos
# dois de propósito: fio de grade não é informação, é enquadramento.
# Para fechar a SUA paleta com medição, use `manim-color-theming` §5.2.

CANVAS = "#FFFFFF"        # o fundo
CANVAS_SUAVE = "#F4F4F6"  # a placa/faixa que não é o fundo, mas quase
TINTA = "#141416"         # texto e traço principais
TINTA_2 = "#5A5A60"       # texto secundário
TINTA_3 = "#70707A"       # legenda, metadado
DIVISORIA = "#D4D4D8"     # fio, grade, borda
ACENTO = "#0B62C4"        # UM destaque. Dois acentos é o começo de seis.

#: Cores de SINAL — só para elemento gráfico (barra, seta, marcação).
#: Rótulo em cima de barra colorida usa TINTA, nunca a cor do sinal.
VERDE = "#1B7F4B"
VERMELHO = "#C0342A"
LARANJA = "#A85800"

# Variante escura, se o projeto for de fundo escuro. Contraste sobre #121316:
#   TINTA 16,62 · TINTA_2 7,87 · TINTA_3 5,73 · ACENTO 6,59
# TODO: para usá-la, troque os sete nomes acima por estes valores — não
# mantenha as duas paletas vivas ao mesmo tempo, ou metade das cenas usa uma.
#   CANVAS="#121316" CANVAS_SUAVE="#1B1C21" TINTA="#F2F2F4" TINTA_2="#A8A8B0"
#   TINTA_3="#8E8E98" DIVISORIA="#33343A" ACENTO="#4C9DF5"


# ─────────────────────────────────────────────────────────────────────────────
# 4. Tipografia: a pilha de fontes, resolvida no import
# ─────────────────────────────────────────────────────────────────────────────
#
# `Text(font="Inter")` com Inter ausente emite um WARNING, cai para a fonte
# padrão do fontconfig e **`t.font` continua devolvendo `'Inter'`** — o objeto
# mente [fonte: text_mobject.py:476-491, o `self.font = font` roda depois do
# aviso]. A defesa é resolver a pilha AQUI e publicar um booleano honesto.
#
# `Text.font_list()` é `manimpango.list_fonts()` [fonte: text_mobject.py:444]
# e é a via PORTÁTIL — `fc-list` só existe onde há fontconfig.

_PILHA_SANS = ["Inter", "Fira Sans", "Cantarell", "DejaVu Sans"]   # TODO
_PILHA_MONO = ["JetBrains Mono", "Fira Mono", "DejaVu Sans Mono"]  # TODO


def _primeira_disponivel(pilha: list[str]) -> str:
    """O primeiro nome da pilha que o Pango realmente resolve.

    O último item da pilha é o fallback incondicional: escolha um que exista
    em qualquer Linux (DejaVu) para que a função nunca devolva algo que o
    Manim vá recusar.
    """
    try:
        instaladas = set(Text.font_list())
    except Exception:                      # manimpango indisponível: não trave
        return pilha[-1]
    for nome in pilha:
        if nome in instaladas:
            return nome
    return pilha[-1]


FONTE = _primeira_disponivel(_PILHA_SANS)
FONTE_MONO = _primeira_disponivel(_PILHA_MONO)

#: `True` quando o render vai sair com a fonte de PRIMEIRA escolha do projeto.
#: Um script de entrega pode conferir isto sem renderizar nada.
FONTE_EXATA = FONTE == _PILHA_SANS[0]


# ─────────────────────────────────────────────────────────────────────────────
# 5. Escala tipográfica — sete degraus, e nenhum número fora deles
# ─────────────────────────────────────────────────────────────────────────────
#
# Um `font_size` F do Manim vale, na tela, um em de F/72 unidades de palco.
# Como o palco tem 8,0 unidades de altura em QUALQUER qualidade (o setter de
# `config.quality` mexe em pixel_* e frame_rate, nunca em frame_height
# [fonte: _config/utils.py:1344-1352]), a tabela abaixo não muda com `-ql`
# ou `-qh`:
#
#     T_MIUDO    18  → em 0,250 un → 3,1% da altura do quadro
#     T_LEGENDA  22  → em 0,306 un → 3,8%
#     T_CORPO    28  → em 0,389 un → 4,9%
#     T_H3       34  → em 0,472 un → 5,9%
#     T_H2       44  → em 0,611 un → 7,6%
#     T_DISPLAY  60  → em 0,833 un → 10,4%
#     T_MEGA     96  → em 1,333 un → 16,7%
#
# TODO: recalibre para o SEU destino. Estes valores foram calibrados para
# vídeo dentro de slide projetado; para leitura em celular, suba tudo.

T_MEGA = 96
T_DISPLAY = 60
T_H2 = 44
T_H3 = 34
T_CORPO = 28
T_LEGENDA = 22
T_MIUDO = 18


# ── 5.1 Nitidez: por que todo texto nasce grande e é encolhido ───────────────
#
# O ManimCE entrega a string ao Pango em `font_size / 4.8` pt
# (`TEXT2SVG_ADJUSTMENT_FACTOR` [fonte: text_mobject.py:85,838]) e o cairo
# grava o SVG com a posição X de CADA glifo arredondada para INTEIRO. Dá para
# ver no cache do render, em `{media_dir}/texts/*.svg`:
#
#     <use xlink:href="#glyph-0-0" x="30" y="28.830078"/>
#     <use xlink:href="#glyph-0-1" x="34" y="28.830078"/>   ← x inteiro, y não
#
# Em font_size 22 o em mede 22/3.6 ≈ 6,1 unidades de dispositivo, então meia
# unidade de arredondamento vale ±8% do em POR LETRA — é isso, e não a fonte,
# que faz a legenda sair "o a r q u i v o". Erro proporcional a 1/tamanho.
#
# A correção é mexer na GRADE, não na fonte: desenhar em 720 (= 200 px de
# dispositivo por em) e encolher o mobject. rms medido em outro projeto:
# 5,53% → 0,13%, constante em todos os tamanhos.

#: Tamanho ÚNICO em que todo texto é rasterizado antes de ser encolhido.
_TAMANHO_RENDER = 720.0

#: Palco em que o Pango faz a quebra de linha DURANTE esse render.
#: O Manim passa `config["pixel_width"]`/`["pixel_height"]` ao
#: `manimpango.text2svg` como largura e altura de quebra
#: [fonte: text_mobject.py:849-863]. Sem fixar isto, a quebra de linha ficaria
#: amarrada à QUALIDADE do render — a mesma frase quebrando em `-ql` e não em
#: `-qh`. 65536/200 ≈ 327 em antes de quebrar: nenhuma linha de tela chega lá.
_PALCO_TEXTO = (65536, 36864)


def _texto_nitido(conteudo: str, tamanho: float, **kw: Any) -> Text:
    """Um `Text` desenhado em `_TAMANHO_RENDER` e encolhido até `tamanho`.

    O `try/finally` é obrigatório: `config.pixel_width`/`pixel_height` são
    globais e uma exceção no meio deixaria o render inteiro num palco de
    65536 px. Devolver os valores no `finally` é o que torna a função segura
    de chamar 200 vezes por cena.

    O vaivém é geometricamente INERTE: `frame_width`/`frame_height` são
    valores independentes no `config`, derivados de `pixel_*` uma única vez,
    quando o `.cfg` é digerido [fonte: _config/utils.py:673-677 e 1140-1146].
    Mexer em `pixel_*` depois disso não recalcula o palco lógico.

    ARMADILHA: `VMobject.scale` tem `scale_stroke=False` por padrão
    [fonte, assinatura]. `Text` nasce com `stroke_width=0`, então o caso
    normal está certo — mas um texto contornado (`stroke_width=2`) sairia
    daqui com o contorno em tamanho ORIGINAL, engolindo o glifo. Se precisar
    de contorno, passe `scale_stroke=True` no `.scale` abaixo.
    """
    largura, altura = config.pixel_width, config.pixel_height
    try:
        config.pixel_width, config.pixel_height = _PALCO_TEXTO
        mob = Text(conteudo, font_size=_TAMANHO_RENDER, **kw)
    finally:
        config.pixel_width, config.pixel_height = largura, altura
    return mob.scale(tamanho / _TAMANHO_RENDER)


# ─────────────────────────────────────────────────────────────────────────────
# 6. Movimento — o vocabulário do projeto
# ─────────────────────────────────────────────────────────────────────────────
#
# TODO: escolha UMA curva de entrada e fique com ela. É a assinatura do
# projeto; trocar de curva por cena é o equivalente temporal de trocar de
# fonte por slide. O catálogo das 49 está em `manim-composicao-ritmo`.

SAIDA = rate_functions.ease_out_expo        # desaceleração longa, decidida
ENTRA_SAI = rate_functions.ease_in_out_sine  # para movimento que vai e volta

RAPIDO, BASE, LENTO = 0.45, 0.8, 1.4         # run_time
PAUSA, PAUSA_LONGA = 0.7, 1.4                # respiro depois de cada beat


# ─────────────────────────────────────────────────────────────────────────────
# 7. Helpers — o FUNIL por onde todo texto passa
# ─────────────────────────────────────────────────────────────────────────────
#
# A regra que se sustenta na prática: o que você quer garantir tem que passar
# por uma FUNÇÃO. Constante nomeada não basta — medido num projeto real, o
# texto (que só nasce por `txt()`) teve 0 escapes em 8.197 linhas, enquanto
# `run_time=` (constante nomeada, mas com um literal mais curto de digitar)
# vazou em 31,7% das ocorrências.


def txt(
    conteudo: str,
    tamanho: float = T_CORPO,
    cor: str = TINTA,
    peso: str = "NORMAL",
    mono: bool = False,
    **kw: Any,
) -> Text:
    """O ÚNICO caminho para pôr texto em cena. `Text(...)` cru é bug."""
    return _texto_nitido(
        conteudo,
        tamanho,
        font=FONTE_MONO if mono else FONTE,
        color=cor,
        weight=peso,
        **kw,
    )


def legenda(conteudo: str) -> Text:
    """Rótulo pequeno e apagado: eixo, unidade, metadado."""
    return txt(conteudo, T_LEGENDA, TINTA_3)


def sobretitulo(conteudo: str) -> Text:
    """Eyebrow: rótulo pequeno, no acento, acima de um bloco."""
    return txt(conteudo.upper(), T_LEGENDA, ACENTO, "SEMIBOLD")


def fio(largura: float = 12.0) -> Line:
    """O fio fino que separa blocos. Nunca `Line()` sem cor: nasce branco."""
    return Line(
        LEFT * largura / 2, RIGHT * largura / 2, color=DIVISORIA, stroke_width=1.5
    )


def coluna(*mobs: Any, buff: float = 0.28) -> VGroup:
    """Empilha alinhado à esquerda — o arranjo mais usado de qualquer deck."""
    return VGroup(*mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)


# ─────────────────────────────────────────────────────────────────────────────
# 8. A cena-base
# ─────────────────────────────────────────────────────────────────────────────


class CenaBase(Scene):
    """Base de TODA cena do projeto.

    `setup()` fixa o fundo em DOIS lugares, e os dois são necessários:

      - `self.camera.background_color` é quem PINTA. A câmera lê o `config`
        uma única vez, no próprio `__init__` [fonte: camera/camera.py:134-142],
        que roda antes daqui; o setter dela re-executa `init_background()`
        [fonte: camera/camera.py:172-175];
      - `config.background_color` é quem outros objetos CONSULTAM — em
        especial `BackgroundRectangle` sem `color=`, que sem isto vira uma
        placa opaca visível no meio da cena.

    E este `setup()` é a ÚLTIMA palavra: ele roda dentro de `Scene.render()`
    [fonte: scene/scene.py:257], depois de qualquer `--theme`, `tempconfig`
    ou flag de linha de comando. Um `--theme 3b1b` NÃO escurece uma cena que
    herda daqui — o que é o comportamento certo para um projeto com
    identidade própria, e uma surpresa para quem esperava a flag ganhar.
    """

    #: TODO: se alguma cena precisar de outro fundo, sobrescreva só isto.
    FUNDO: str = CANVAS

    def setup(self) -> None:
        config.background_color = self.FUNDO
        self.camera.background_color = self.FUNDO
        super().setup()

    # ── atalhos de ritmo: são FUNÇÃO de propósito ────────────────────────
    # `self.beat()` é mais curto que `self.wait(0.7)`. Essa é a única razão
    # pela qual ele é usado, e é a razão pela qual ele funciona.

    def beat(self, longa: bool = False) -> None:
        """O respiro entre dois passos."""
        self.wait(PAUSA_LONGA if longa else PAUSA)

    def entra(self, *animacoes: Any, tempo: float = BASE, **kw: Any) -> None:
        """`self.play` já com a curva e o tempo do projeto.

        Existe para que `rate_func=` e `run_time=` não precisem ser digitados
        — e, portanto, não possam ser esquecidos.
        """
        self.play(*animacoes, run_time=tempo, rate_func=SAIDA, **kw)


# ─────────────────────────────────────────────────────────────────────────────
# 9. O que sai daqui com `from tema import *`
# ─────────────────────────────────────────────────────────────────────────────
#
# `__all__` explícito NÃO é burocracia: sem ele, o star-import despeja também
# tudo que este módulo importou (`json`, `Path`, `rate_functions`…) no espaço
# de nomes de cada cena.

__all__ = [
    "RAIZ", "PASTA", "DADOS", "NUMEROS", "numero",
    "CANVAS", "CANVAS_SUAVE", "TINTA", "TINTA_2", "TINTA_3", "DIVISORIA",
    "ACENTO", "VERDE", "VERMELHO", "LARANJA",
    "FONTE", "FONTE_MONO", "FONTE_EXATA",
    "T_MEGA", "T_DISPLAY", "T_H2", "T_H3", "T_CORPO", "T_LEGENDA", "T_MIUDO",
    "SAIDA", "ENTRA_SAI", "RAPIDO", "BASE", "LENTO", "PAUSA", "PAUSA_LONGA",
    "txt", "legenda", "sobretitulo", "fio", "coluna",
    "CenaBase",
]


# ─────────────────────────────────────────────────────────────────────────────
# 10. Autorrelato — roda em milissegundos, não renderiza nada
# ─────────────────────────────────────────────────────────────────────────────
#
#     python tema.py
#
# Confere o que só se descobre tarde: a fonte caiu para o fallback? o palco é
# o que você pensa? Nenhum Mobject é construído aqui.

if __name__ == "__main__":                                    # pragma: no cover
    print(f"fonte      : {FONTE}   (exata: {FONTE_EXATA})")
    print(f"mono       : {FONTE_MONO}")
    print(f"palco      : {config.frame_width:.3f} x {config.frame_height:.3f} un")
    print(f"pixels     : {config.pixel_width} x {config.pixel_height} @ "
          f"{config.frame_rate} fps")
    print(f"fundo      : {CANVAS}")
    print(f"dados      : {_ARQUIVO_DADOS} "
          f"({'ok, ' + str(len(NUMEROS)) + ' números' if NUMEROS else 'AUSENTE'})")
    print("escala     :")
    for nome, v in [("T_MEGA", T_MEGA), ("T_DISPLAY", T_DISPLAY), ("T_H2", T_H2),
                    ("T_H3", T_H3), ("T_CORPO", T_CORPO),
                    ("T_LEGENDA", T_LEGENDA), ("T_MIUDO", T_MIUDO)]:
        em = v / 72.0
        print(f"  {nome:11s} {v:3d}  em={em:.3f} un  "
              f"{100 * em / config.frame_height:.1f}% da altura")
