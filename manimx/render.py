"""Renderização programática do ManimCE — sem passar pela CLI.

Por que isto existe
-------------------
Um agente que dispara ``subprocess.run(["manim", ...])`` precisa depois
adivinhar onde o arquivo foi parar (o caminho depende de ``media_dir``,
``module_name``, ``quality``, ``output_file``, ``save_sections``...) e
parsear log colorido para saber se deu certo.

Aqui a gente renderiza no processo e lê o caminho **direto do
``SceneFileWriter``**, então :attr:`RenderResult.output_file` é sempre o
caminho real.

Exemplo
-------
::

    from manimx import render_file

    r = render_file("scenes/demo.py", "Demo", quality="h", codec="nvenc")
    assert r.success
    print(r.output_file)

Aviso sobre estado global
-------------------------
O ``config`` do Manim é global e mutável. Todas as funções daqui usam
``tempconfig``, então o estado é restaurado ao final — inclusive em caso
de exceção.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import inspect
import logging
import os
import sys
import time
import traceback
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

logger = logging.getLogger("manimx.render")

__all__ = [
    "RenderResult",
    "render_scene",
    "render_file",
    "list_scenes",
    "load_scene_classes",
]


@dataclasses.dataclass
class RenderResult:
    """Resultado de uma renderização.

    Attributes
    ----------
    scene_name
        Nome da classe de cena renderizada.
    success
        ``False`` se a cena levantou exceção.
    output_file
        Caminho absoluto do vídeo. ``None`` em modo ``png``/``dry_run``
        ou se a renderização falhou.
    image_file
        Caminho do PNG quando ``format="png"`` ou ``save_last_frame=True``.
    sections
        Vídeos de seção, se ``save_sections=True``.
    elapsed_s
        Tempo de parede da renderização.
    error / traceback_text
        Preenchidos quando ``success`` é ``False``.
    """

    scene_name: str
    success: bool = False
    output_file: Path | None = None
    image_file: Path | None = None
    sections: list[Path] = dataclasses.field(default_factory=list)
    elapsed_s: float = 0.0
    renderer: str = "cairo"
    codec: str = "libx264"
    quality: str = "h"
    resolution: tuple[int, int] = (1920, 1080)
    frame_rate: float = 60.0
    num_animations: int = 0
    error: str | None = None
    traceback_text: str | None = None

    def as_dict(self) -> dict[str, Any]:
        d = dataclasses.asdict(self)
        for key in ("output_file", "image_file"):
            if d[key] is not None:
                d[key] = str(d[key])
        d["sections"] = [str(p) for p in self.sections]
        return d

    def __bool__(self) -> bool:
        return self.success


# --------------------------------------------------------------------------
# Descoberta de cenas
# --------------------------------------------------------------------------


def load_scene_classes(file_path: str | Path) -> list[type]:
    """Importa um .py e devolve todas as subclasses de ``Scene`` definidas nele.

    Diferente de ``manim.utils.module_ops.scene_classes_from_file``, isto
    não depende do ``config`` global e não pede input interativo.
    """
    from manim import Scene

    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"arquivo de cena não encontrado: {path}")

    module_name = f"_manimx_scene_{path.stem}_{abs(hash(str(path)))}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"não consegui carregar {path} como módulo")
    module = importlib.util.module_from_spec(spec)

    # Deixa o diretório da cena importável (imports relativos do usuário).
    parent = str(path.parent)
    added = parent not in sys.path
    if added:
        sys.path.insert(0, parent)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        if added:
            sys.path.remove(parent)

    classes = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, Scene) and obj.__module__ == module_name
    ]
    # Ordem de definição no arquivo, não alfabética.
    classes.sort(key=lambda c: getattr(c, "__firstlineno__", 0) or _first_line(c))
    return classes


def _first_line(cls: type) -> int:
    try:
        return inspect.getsourcelines(cls)[1]
    except (OSError, TypeError):
        return 0


def list_scenes(file_path: str | Path) -> list[str]:
    """Nomes das cenas de um arquivo, na ordem em que aparecem."""
    return [c.__name__ for c in load_scene_classes(file_path)]


# --------------------------------------------------------------------------
# Renderização
# --------------------------------------------------------------------------


def _build_config(
    *,
    quality: str,
    renderer: str,
    fmt: str | None,
    transparent: bool,
    fps: float | None,
    resolution: tuple[int, int] | None,
    media_dir: str | Path | None,
    output_file: str | None,
    input_file: Path | None,
    disable_caching: bool,
    flush_cache: bool,
    save_last_frame: bool,
    save_sections: bool,
    background_color: str | None,
    max_inflight_encoders: int | None,
    encoder_queue_size: int | None,
    preview: bool,
    verbosity: str,
    extra: dict[str, Any] | None,
) -> dict[str, Any]:
    from manimx.presets import QUALITY_PRESETS, resolve_quality

    qkey = resolve_quality(quality)
    preset = QUALITY_PRESETS[qkey]

    cfg: dict[str, Any] = {
        "quality": preset["alias"],
        "renderer": renderer,
        "preview": preview,
        "verbosity": verbosity.upper(),
        "disable_caching": disable_caching,
        "flush_cache": flush_cache,
        "save_sections": save_sections,
        "transparent": transparent,
        "notify_outdated_version": False,
        "progress_bar": "none",
    }

    if resolution is not None:
        cfg["pixel_width"], cfg["pixel_height"] = resolution
    if fps is not None:
        cfg["frame_rate"] = fps
    if media_dir is not None:
        cfg["media_dir"] = str(Path(media_dir).resolve())
    if output_file is not None:
        cfg["output_file"] = output_file
    if input_file is not None:
        cfg["input_file"] = str(input_file)
    if background_color is not None:
        cfg["background_color"] = background_color
    if max_inflight_encoders is not None:
        cfg["max_inflight_encoders"] = max_inflight_encoders
    if encoder_queue_size is not None:
        cfg["encoder_queue_size"] = encoder_queue_size

    if fmt:
        cfg["format"] = fmt
    if save_last_frame:
        cfg["save_last_frame"] = True

    # O renderer opengl não escreve arquivo por padrão (ele abre janela).
    if renderer == "opengl" and fmt != "png" and not save_last_frame:
        cfg["write_to_movie"] = True

    if extra:
        cfg.update(extra)
    return cfg


def _effective_codec(
    cpreset: dict[str, Any],
    nvenc_on: bool,
    fmt: str | None,
    transparent: bool,
) -> str:
    """Codec que o Manim vai realmente usar, para reportar no resultado.

    O ManimCE escolhe o codec por formato/transparência dentro de
    ``open_partial_movie_stream``; dizer "libx264" para uma saída
    ``.webm`` ou ``.mov`` seria simplesmente errado no JSON.
    """
    if fmt == "png":
        return "png"
    if fmt == "gif":
        return "gif"
    if fmt == "webm":
        return "libvpx-vp9"
    if transparent:
        return "qtrle"
    if nvenc_on:
        return cpreset.get("codec", "h264_nvenc")
    return "libx264"


def render_scene(
    scene_class: type,
    *,
    quality: str = "h",
    renderer: str = "cairo",
    codec: str = "x264",
    theme: str | None = None,
    gpu: bool | None = None,
    fmt: str | None = None,
    transparent: bool = False,
    fps: float | None = None,
    resolution: tuple[int, int] | None = None,
    media_dir: str | Path | None = None,
    output_file: str | None = None,
    input_file: str | Path | None = None,
    disable_caching: bool = False,
    flush_cache: bool = False,
    save_last_frame: bool = False,
    save_sections: bool = False,
    background_color: str | None = None,
    max_inflight_encoders: int | None = None,
    encoder_queue_size: int | None = None,
    preview: bool = False,
    verbosity: str = "WARNING",
    config_overrides: dict[str, Any] | None = None,
    raise_on_error: bool = False,
) -> RenderResult:
    """Renderiza uma classe de cena já importada.

    Parameters
    ----------
    scene_class
        Subclasse de ``manim.Scene``.
    quality
        ``"l"``, ``"m"``, ``"h"``, ``"p"``, ``"k"`` ou apelidos
        (``"1080p"``, ``"4k"``, ``"draft"``…). Ver
        :data:`manimx.presets.QUALITY_PRESETS`.
    renderer
        ``"cairo"`` (CPU, padrão, mais estável) ou ``"opengl"``
        (GPU via ModernGL; em notebook híbrido exige PRIME offload —
        use :func:`manimx.gpu.prime_env` ou os wrappers em ``bin/``).
    codec
        Chave de :data:`manimx.presets.CODEC_PRESETS`
        (``"x264"``, ``"nvenc"``, ``"nvenc-quality"``, ``"hevc"``,
        ``"av1"``, ``"transparent"``, ``"webm"``, ``"gif"``, ``"png"``).
    theme
        Chave de :data:`manimx.presets.THEMES`, aplicada antes da cena.
    gpu
        Força ligar/desligar NVENC, ignorando o que o ``codec`` pede.
        ``None`` (padrão) = decide pelo preset de codec.
    fmt
        ``"mp4"``, ``"gif"``, ``"webm"``, ``"mov"``, ``"png"``.
        Sobrescreve o que veio do preset de codec.
    resolution
        ``(largura, altura)``, sobrescreve o preset de qualidade.
    media_dir
        Raiz da saída. Padrão: ``./media``.
    disable_caching
        Ignora *partial movies* em cache. Use quando a cena depende de
        estado externo (dados, arquivos) que o hash do Manim não vê.
    max_inflight_encoders
        Recurso do ManimCE ≥ 0.20: codifica N *partial movies* em paralelo
        enquanto a cena continua renderizando. ``4`` é um bom valor.
        Ganho grande em cenas com muitas animações curtas.
    raise_on_error
        Se ``True``, propaga a exceção da cena em vez de embrulhar em
        :class:`RenderResult`.

    Returns
    -------
    RenderResult
        Sempre retorna — cheque ``.success`` (ou o próprio objeto, que é
        *falsy* quando falha).
    """
    from manim import tempconfig

    from manimx.gpu import disable_nvenc, enable_nvenc
    from manimx.presets import CODEC_PRESETS, resolve_quality

    if codec not in CODEC_PRESETS:
        raise ValueError(
            f"codec desconhecido: {codec!r}. Use um de: {', '.join(CODEC_PRESETS)}"
        )
    cpreset = CODEC_PRESETS[codec]

    use_gpu = cpreset.get("gpu", False) if gpu is None else gpu
    fmt = fmt or cpreset.get("format")
    transparent = transparent or bool(cpreset.get("transparent", False))

    # Não defina `movie_file_extension` aqui. O Manim recalcula a extensão
    # em `ManimConfig.resolve_movie_file_extension`, que é disparado ao
    # setar `transparent` e deriva o valor de `config.format` — sobrescrevendo
    # qualquer extensão que a gente tivesse posto, com um aviso confuso
    # ("Output format changed to '.mp4' to support transparency").
    # Por isso os presets usam `format` (webm/gif/png) ou `transparent`,
    # que são as entradas que o Manim de fato respeita.
    extra = dict(config_overrides or {})

    if input_file is None:
        mod = sys.modules.get(scene_class.__module__)
        mod_file = getattr(mod, "__file__", None)
        if mod_file:
            input_file = Path(mod_file)

    cfg = _build_config(
        quality=quality,
        renderer=renderer,
        fmt=fmt,
        transparent=transparent,
        fps=fps,
        resolution=resolution,
        media_dir=media_dir,
        output_file=output_file,
        input_file=Path(input_file) if input_file else None,
        disable_caching=disable_caching,
        flush_cache=flush_cache,
        save_last_frame=save_last_frame or fmt == "png",
        save_sections=save_sections,
        background_color=background_color,
        max_inflight_encoders=max_inflight_encoders,
        encoder_queue_size=encoder_queue_size,
        preview=preview,
        verbosity=verbosity,
        extra=extra,
    )

    # PRIME offload precisa estar no ambiente ANTES de criar o contexto GL.
    if renderer == "opengl":
        from manimx.gpu import prime_env

        for k, v in prime_env().items():
            os.environ.setdefault(k, v)

    nvenc_on = False
    if use_gpu and not transparent and fmt not in ("gif", "png", "webm"):
        nvenc_on = enable_nvenc(
            codec=cpreset.get("codec", "h264_nvenc"),
            profile=cpreset.get("profile", "balanced"),
        )
    elif use_gpu:
        logger.info(
            "manimx: NVENC ignorado para transparent/gif/png/webm "
            "(o codec desses formatos não tem caminho por hardware)."
        )

    qkey = resolve_quality(quality)
    result = RenderResult(
        scene_name=scene_class.__name__,
        renderer=renderer,
        codec=_effective_codec(cpreset, nvenc_on, fmt, transparent),
        quality=qkey,
    )

    started = time.perf_counter()
    try:
        with tempconfig(cfg):
            from manim import config as live_config

            from manimx.presets import apply_theme

            if theme:
                apply_theme(theme)

            result.resolution = (live_config.pixel_width, live_config.pixel_height)
            result.frame_rate = float(live_config.frame_rate)

            scene = scene_class()
            scene.render()

            writer = getattr(scene.renderer, "file_writer", None)
            if writer is not None:
                movie = getattr(writer, "movie_file_path", None)
                gif = getattr(writer, "gif_file_path", None)
                image = getattr(writer, "image_file_path", None)

                if fmt == "gif" and gif:
                    result.output_file = Path(gif).resolve()
                elif movie and Path(movie).exists():
                    result.output_file = Path(movie).resolve()
                if image and Path(image).exists():
                    result.image_file = Path(image).resolve()

                sec_dir = getattr(writer, "sections_output_dir", None)
                if save_sections and sec_dir and Path(sec_dir).is_dir():
                    result.sections = sorted(Path(sec_dir).glob("*.mp4"))

            result.num_animations = getattr(scene.renderer, "num_plays", 0)
            result.success = True
    except BaseException as exc:  # noqa: BLE001 - queremos reportar tudo
        result.success = False
        result.error = f"{type(exc).__name__}: {exc}"
        result.traceback_text = traceback.format_exc()
        if raise_on_error:
            raise
    finally:
        result.elapsed_s = time.perf_counter() - started
        if nvenc_on:
            disable_nvenc()

    return result


def render_file(
    file_path: str | Path,
    scene_names: str | Sequence[str] | None = None,
    *,
    all_scenes: bool = False,
    **kwargs: Any,
) -> RenderResult | list[RenderResult]:
    """Renderiza uma ou mais cenas de um arquivo ``.py``.

    Parameters
    ----------
    file_path
        Caminho do módulo com as cenas.
    scene_names
        Um nome, uma lista de nomes, ou ``None``. Com ``None``:
        renderiza a única cena do arquivo, ou levanta ``ValueError`` se
        houver mais de uma (a menos que ``all_scenes=True``).
    all_scenes
        Renderiza todas as cenas do arquivo.
    **kwargs
        Repassados para :func:`render_scene`.

    Returns
    -------
    RenderResult | list[RenderResult]
        Um único resultado quando você pediu uma cena só; uma lista
        quando pediu várias ou ``all_scenes=True``.
    """
    path = Path(file_path).resolve()
    classes = load_scene_classes(path)
    if not classes:
        raise ValueError(f"nenhuma subclasse de Scene encontrada em {path}")

    by_name = {c.__name__: c for c in classes}

    if all_scenes:
        targets = classes
        single = False
    elif scene_names is None:
        if len(classes) > 1:
            raise ValueError(
                f"{path} tem {len(classes)} cenas ({', '.join(by_name)}). "
                "Passe scene_names=... ou all_scenes=True."
            )
        targets, single = classes, True
    elif isinstance(scene_names, str):
        if scene_names not in by_name:
            raise ValueError(
                f"cena {scene_names!r} não existe em {path}. "
                f"Disponíveis: {', '.join(by_name)}"
            )
        targets, single = [by_name[scene_names]], True
    else:
        missing = [n for n in scene_names if n not in by_name]
        if missing:
            raise ValueError(
                f"cenas ausentes em {path}: {', '.join(missing)}. "
                f"Disponíveis: {', '.join(by_name)}"
            )
        targets = [by_name[n] for n in scene_names]
        single = False

    kwargs.setdefault("input_file", path)
    results = [render_scene(c, **kwargs) for c in targets]
    return results[0] if single else results


def render_many(
    jobs: Iterable[dict[str, Any]],
    *,
    stop_on_error: bool = False,
) -> list[RenderResult]:
    """Executa vários :func:`render_file` em sequência.

    Cada item de ``jobs`` é um dict de kwargs para :func:`render_file`,
    com pelo menos a chave ``file_path``.

    Sequencial de propósito: o ``config`` do Manim é global, então rodar
    duas cenas em paralelo **no mesmo processo** corrompe o estado. Para
    paralelismo real, use vários processos (ver
    ``.claude/skills/manim-batch-pipeline/``).
    """
    out: list[RenderResult] = []
    for job in jobs:
        job = dict(job)
        fp = job.pop("file_path")
        res = render_file(fp, **job)
        out.extend(res if isinstance(res, list) else [res])
        if stop_on_error and not out[-1].success:
            break
    return out
