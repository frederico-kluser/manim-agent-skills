"""Presets de qualidade, codec e tema para o ManimCE.

Tudo aqui é dicionário puro — um agente pode ler, imprimir e editar sem
importar o Manim.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "QUALITY_PRESETS",
    "CODEC_PRESETS",
    "THEMES",
    "resolve_quality",
    "apply_theme",
    "theme_config",
]


#: Presets de qualidade do ManimCE. As chaves curtas são as aceitas por
#: ``-q/--quality``. ``fourk``/``k`` = 2160p.
QUALITY_PRESETS: dict[str, dict[str, Any]] = {
    "l": {"pixel_width": 854, "pixel_height": 480, "frame_rate": 15, "alias": "low_quality"},
    "m": {"pixel_width": 1280, "pixel_height": 720, "frame_rate": 30, "alias": "medium_quality"},
    "h": {"pixel_width": 1920, "pixel_height": 1080, "frame_rate": 60, "alias": "high_quality"},
    "p": {"pixel_width": 2560, "pixel_height": 1440, "frame_rate": 60, "alias": "production_quality"},
    "k": {"pixel_width": 3840, "pixel_height": 2160, "frame_rate": 60, "alias": "fourk_quality"},
}

#: Apelidos aceitos por :func:`resolve_quality`.
_QUALITY_ALIASES = {
    "low": "l", "low_quality": "l", "480p": "l", "draft": "l",
    "medium": "m", "medium_quality": "m", "720p": "m",
    "high": "h", "high_quality": "h", "1080p": "h", "hd": "h",
    "production": "p", "production_quality": "p", "1440p": "p", "2k": "p",
    "fourk": "k", "fourk_quality": "k", "2160p": "k", "4k": "k", "uhd": "k",
}


def resolve_quality(quality: str) -> str:
    """Normaliza ``"1080p"``, ``"high"``, ``"hd"``… para a chave curta ``"h"``."""
    q = str(quality).strip().lower()
    if q in QUALITY_PRESETS:
        return q
    if q in _QUALITY_ALIASES:
        return _QUALITY_ALIASES[q]
    raise ValueError(
        f"qualidade desconhecida: {quality!r}. "
        f"Use {sorted(QUALITY_PRESETS)} ou {sorted(_QUALITY_ALIASES)}"
    )


#: Combinações codec × container × transparência que fazem sentido.
#:
#: ``gpu`` indica se o preset usa NVENC (ver :func:`manimx.gpu.enable_nvenc`).
CODEC_PRESETS: dict[str, dict[str, Any]] = {
    "x264": {
        "gpu": False,
        "transparent": False,
        "desc": "Padrão do Manim. libx264 crf 23, CPU. Compatibilidade total.",
    },
    "nvenc": {
        "gpu": True,
        "codec": "h264_nvenc",
        "profile": "balanced",
        "transparent": False,
        "desc": "H.264 por hardware NVIDIA. ~2-3x mais rápido no encode.",
    },
    "nvenc-fast": {
        "gpu": True,
        "codec": "h264_nvenc",
        "profile": "fast",
        "transparent": False,
        "desc": "NVENC preset p1. Para iteração/preview, não para entrega.",
    },
    "nvenc-quality": {
        "gpu": True,
        "codec": "h264_nvenc",
        "profile": "quality",
        "transparent": False,
        "desc": "NVENC p7 + AQ espacial/temporal. Entrega final.",
    },
    "hevc": {
        "gpu": True,
        "codec": "hevc_nvenc",
        "profile": "quality",
        "transparent": False,
        "desc": "H.265 por hardware. ~30% menor, menos compatível.",
    },
    "av1": {
        "gpu": True,
        "codec": "av1_nvenc",
        "profile": "quality",
        "transparent": False,
        "desc": (
            "AV1 por hardware (Ada / RTX 40+). INDISPONÍVEL nesta build do "
            "PyAV: o encoder grava, mas a junção dos partial movies falha "
            "(UnknownCodecError: libdav1d). A validação detecta e cai em "
            "libx264. Para AV1 de verdade, reencode o MP4 final com ffmpeg."
        ),
    },
    "transparent": {
        "gpu": False,
        "transparent": True,
        "desc": "qtrle RGBA em .mov. Para compor em NLE. NVENC não faz alfa.",
    },
    "webm": {
        "gpu": False,
        "format": "webm",
        "transparent": False,
        "desc": "libvpx-vp9. Para web. NVENC não faz VP9.",
    },
    "gif": {
        "gpu": False,
        "format": "gif",
        "desc": "GIF com paleta gerada por palettegen/paletteuse.",
    },
    "png": {
        "gpu": False,
        "format": "png",
        "desc": "Só o último frame, como PNG (equivale a -s).",
    },
}


#: Temas prontos. Aplicados com :func:`apply_theme` **antes** de instanciar
#: qualquer Mobject (eles mexem em ``set_default`` das classes).
THEMES: dict[str, dict[str, Any]] = {
    "3b1b": {
        "background_color": "#000000",
        "text_color": "#FFFFFF",
        "desc": "Padrão do canal: lousa preta, traço branco.",
    },
    "whiteboard": {
        "background_color": "#FFFFFF",
        "text_color": "#000000",
        "desc": "Lousa branca corporativa/artigo. Inverte texto e traço.",
    },
    "paper": {
        "background_color": "#F4F1EA",
        "text_color": "#1C1B19",
        "desc": "Papel creme, tinta quase-preta. Bom para print.",
    },
    "slate": {
        "background_color": "#1E1E2E",
        "text_color": "#CDD6F4",
        "desc": "Escuro suave estilo Catppuccin Mocha.",
    },
    "solarized-dark": {
        "background_color": "#002B36",
        "text_color": "#93A1A1",
        "desc": "Solarized Dark.",
    },
    "solarized-light": {
        "background_color": "#FDF6E3",
        "text_color": "#586E75",
        "desc": "Solarized Light.",
    },
    "nord": {
        "background_color": "#2E3440",
        "text_color": "#ECEFF4",
        "desc": "Nord.",
    },
    "transparent": {
        "background_color": "#000000",
        "background_opacity": 0.0,
        "text_color": "#FFFFFF",
        "desc": "Fundo transparente; use junto com o codec 'transparent'.",
    },
}


def theme_config(name: str) -> dict[str, Any]:
    """Devolve o dict do tema (sem a chave ``desc``)."""
    if name not in THEMES:
        raise ValueError(
            f"tema desconhecido: {name!r}. Use um de: {', '.join(sorted(THEMES))}"
        )
    return {k: v for k, v in THEMES[name].items() if k != "desc"}


def apply_theme(name: str, *, set_defaults: bool = True) -> dict[str, Any]:
    """Aplica um tema ao ``config`` global do Manim.

    Parameters
    ----------
    name
        Chave em :data:`THEMES`.
    set_defaults
        Se ``True`` (padrão), também roda ``set_default`` em ``Text``,
        ``Tex``, ``MathTex`` e ``VMobject`` para que o traço/preenchimento
        contraste com o novo fundo. Precisa rodar **antes** de instanciar
        qualquer Mobject.

    Returns
    -------
    dict
        O dicionário do tema efetivamente aplicado.

    Warnings
    --------
    Cores hexadecimais precisam do prefixo ``#``. Na ManimCE 0.21 tanto
    ``"#FF0000"`` quanto ``"#F00"`` funcionam (a forma curta é expandida),
    mas ``"FF0000"`` sem ``#`` é lido como *nome* de cor e levanta
    ``ValueError``.
    """
    from manim import config as _config

    theme = theme_config(name)
    _config.background_color = theme["background_color"]
    if "background_opacity" in theme:
        _config.background_opacity = theme["background_opacity"]

    if set_defaults:
        from manim import MathTex, Tex, Text, VMobject

        fg = theme["text_color"]
        Text.set_default(color=fg)
        Tex.set_default(color=fg)
        MathTex.set_default(color=fg)
        VMobject.set_default(color=fg)
    return theme
