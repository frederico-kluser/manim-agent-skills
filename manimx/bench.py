"""Benchmark honesto de CPU vs GPU nesta máquina.

Existe porque a afirmação "ManimGL/OpenGL usa a GPU, então é rápido"
circula muito e é imprecisa. Uma renderização do Manim tem **duas** etapas
com custos independentes:

1. **Rasterização da geometria** — Cairo (CPU) no renderer padrão do CE;
   ModernGL/OpenGL (GPU) com ``--renderer=opengl``; wgpu/Vulkan (GPU) no
   ManimGL master.
2. **Codificação de vídeo** — libx264 (CPU) por padrão; NVENC (GPU) com
   :func:`manimx.gpu.enable_nvenc`.

Trocar só a (2) não acelera cena pesada de geometria. Trocar só a (1) não
acelera cena leve com muitos frames. Este módulo mede as duas separadamente
para você decidir com dado, não com fé.
"""

from __future__ import annotations

import statistics
import time
from pathlib import Path
from typing import Any

__all__ = ["ENCODE_ONLY_SCENE", "GEOMETRY_HEAVY_SCENE", "run_benchmark"]


#: Cena leve em geometria e longa em duração — o gargalo é o encoder.
ENCODE_ONLY_SCENE = '''
from manim import *

class BenchEncode(Scene):
    """Poucos mobjects, muitos frames: mede o encoder."""
    def construct(self):
        sq = Square(side_length=2).set_fill(BLUE, 1)
        self.play(sq.animate.shift(RIGHT * 4), run_time=4)
        self.play(sq.animate.shift(LEFT * 4), run_time=4)
'''

#: Cena pesada em geometria — o gargalo é a rasterização.
GEOMETRY_HEAVY_SCENE = '''
from manim import *
import numpy as np

class BenchGeometry(Scene):
    """Milhares de vértices: mede a rasterização."""
    def construct(self):
        plane = NumberPlane(
            x_range=[-8, 8, 0.25], y_range=[-5, 5, 0.25],
            background_line_style={"stroke_width": 1},
        )
        dots = VGroup(*[
            Dot(np.array([x, np.sin(x * 2), 0]), radius=0.03)
            for x in np.linspace(-7, 7, 700)
        ])
        curves = VGroup(*[
            FunctionGraph(lambda x, k=k: np.sin(k * x) / (k + 1), x_range=[-7, 7, 0.02])
            for k in range(1, 12)
        ])
        self.add(plane)
        self.play(Create(curves), run_time=2)
        self.play(FadeIn(dots), run_time=1)
        self.play(Rotate(curves, PI / 6), run_time=1)
'''


def _write_scene(directory: Path, name: str, source: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.py"
    path.write_text(source, encoding="utf-8")
    return path


def _time_render(
    scene_file: Path,
    scene_name: str,
    *,
    repeats: int,
    **kwargs: Any,
) -> dict[str, Any]:
    from manimx.render import render_file

    times: list[float] = []
    last = None
    for _ in range(repeats):
        result = render_file(
            scene_file, scene_name, disable_caching=True, verbosity="CRITICAL", **kwargs
        )
        last = result
        if not result.success:
            return {"ok": False, "error": result.error, "seconds": None}
        times.append(result.elapsed_s)

    size = None
    if last and last.output_file and Path(last.output_file).exists():
        size = Path(last.output_file).stat().st_size

    return {
        "ok": True,
        "seconds": round(statistics.median(times), 3),
        "all_seconds": [round(t, 3) for t in times],
        "bytes": size,
        "codec": last.codec if last else None,
        "output": str(last.output_file) if last and last.output_file else None,
    }


def run_benchmark(
    *,
    quality: str = "h",
    repeats: int = 1,
    media_dir: str | Path = "media/_bench",
) -> dict[str, Any]:
    """Roda a matriz de benchmark e devolve resultados + texto formatado."""
    from manimx.gpu import detect_gpu

    bench_dir = Path(media_dir)
    scenes_dir = bench_dir / "_scenes"
    enc = _write_scene(scenes_dir, "bench_encode", ENCODE_ONLY_SCENE)
    geo = _write_scene(scenes_dir, "bench_geometry", GEOMETRY_HEAVY_SCENE)

    gpu = detect_gpu()
    matrix: list[dict[str, Any]] = [
        {"label": "encode-bound  cairo + x264", "file": enc, "scene": "BenchEncode",
         "renderer": "cairo", "codec": "x264"},
        {"label": "encode-bound  cairo + NVENC", "file": enc, "scene": "BenchEncode",
         "renderer": "cairo", "codec": "nvenc"},
        {"label": "geometry      cairo + x264", "file": geo, "scene": "BenchGeometry",
         "renderer": "cairo", "codec": "x264"},
        {"label": "geometry      cairo + NVENC", "file": geo, "scene": "BenchGeometry",
         "renderer": "cairo", "codec": "nvenc"},
        {"label": "geometry      opengl + NVENC", "file": geo, "scene": "BenchGeometry",
         "renderer": "opengl", "codec": "nvenc"},
    ]

    results: list[dict[str, Any]] = []
    for row in matrix:
        started = time.perf_counter()
        outcome = _time_render(
            row["file"], row["scene"],
            repeats=repeats,
            quality=quality,
            renderer=row["renderer"],
            codec=row["codec"],
            media_dir=str(bench_dir),
            output_file=row["label"].split()[0] + "_" + row["renderer"] + "_" + row["codec"],
        )
        outcome["label"] = row["label"]
        outcome["renderer"] = row["renderer"]
        outcome["codec_preset"] = row["codec"]
        outcome["wall_s"] = round(time.perf_counter() - started, 3)
        results.append(outcome)

    lines = [
        "=== mx bench ===",
        f"GPU        : {gpu.nvidia_gpu or '(nenhuma)'}",
        f"qualidade  : {quality}   repetições: {repeats}",
        "",
        f"{'cenário':32s} {'seg':>8s} {'MiB':>8s}  codec",
        "-" * 66,
    ]
    for r in results:
        if r["ok"]:
            mib = f"{r['bytes'] / 1048576:.2f}" if r.get("bytes") else "-"
            lines.append(f"{r['label']:32s} {r['seconds']:8.2f} {mib:>8s}  {r['codec']}")
        else:
            lines.append(f"{r['label']:32s} {'FALHA':>8s}  {str(r['error'])[:40]}")

    def find(label_prefix: str) -> dict[str, Any] | None:
        return next((r for r in results if r["label"].startswith(label_prefix)
                     and r["ok"]), None)

    lines.append("")
    lines.append("Leitura:")
    e_cpu, e_gpu = find("encode-bound  cairo + x264"), find("encode-bound  cairo + NVENC")
    if e_cpu and e_gpu and e_gpu["seconds"]:
        delta = (e_cpu["seconds"] - e_gpu["seconds"]) / e_cpu["seconds"] * 100
        lines.append(
            f"  · cena limitada por encoding: NVENC {'economiza' if delta > 0 else 'custa'} "
            f"{abs(delta):.0f}% do tempo."
        )
    g_cairo, g_gl = find("geometry      cairo + NVENC"), find("geometry      opengl + NVENC")
    if g_cairo and g_gl and g_gl["seconds"]:
        delta = (g_cairo["seconds"] - g_gl["seconds"]) / g_cairo["seconds"] * 100
        lines.append(
            f"  · cena pesada em geometria: renderer opengl "
            f"{'economiza' if delta > 0 else 'custa'} {abs(delta):.0f}% vs cairo."
        )
    lines.append(
        "  · NVENC troca CPU por GPU no encoding; não acelera a rasterização "
        "da geometria."
    )
    lines.append(
        "  · em cena curta o overhead de inicializar o NVENC pode superar o ganho."
    )

    return {
        "gpu": gpu.as_dict(),
        "quality": quality,
        "repeats": repeats,
        "results": results,
        "text": "\n".join(lines),
    }
