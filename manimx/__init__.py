"""manimx — camada de API sobre o Manim para uso por agentes de código.

Este pacote NÃO substitui o Manim. Ele adiciona, por cima do Manim
Community Edition instalado em ``.venv``:

* :mod:`manimx.gpu`        — detecção de GPU e encoding NVENC (patch do PyAV)
* :mod:`manimx.render`     — renderização programática (sem CLI), com caminho
                             de saída determinístico
* :mod:`manimx.presets`    — presets de qualidade, tema e codec
* :mod:`manimx.introspect` — dump COMPLETO da superfície de API do Manim
* :mod:`manimx.cli`        — CLI ``mx``

Uso típico por um agente::

    from manimx import render_file, quality

    result = render_file("scenes/demo.py", "Demo", quality="h", gpu=True)
    print(result.output_file)   # caminho absoluto do .mp4

Ver ``.claude/skills/`` para os guias de uso orientados a agente.
"""

from __future__ import annotations

__version__ = "1.0.0"

from manimx.gpu import (
    GPUReport,
    detect_gpu,
    disable_nvenc,
    enable_nvenc,
    nvenc_available,
)
from manimx.presets import (
    CODEC_PRESETS,
    QUALITY_PRESETS,
    THEMES,
    apply_theme,
)
from manimx.render import (
    RenderResult,
    list_scenes,
    render_file,
    render_scene,
)

__all__ = [
    "__version__",
    # gpu
    "GPUReport",
    "detect_gpu",
    "enable_nvenc",
    "disable_nvenc",
    "nvenc_available",
    # render
    "RenderResult",
    "render_file",
    "render_scene",
    "list_scenes",
    # presets
    "QUALITY_PRESETS",
    "CODEC_PRESETS",
    "THEMES",
    "apply_theme",
]
