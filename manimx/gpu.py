"""Detecção de GPU e encoding por hardware (NVENC) para o Manim Community.

Contexto técnico verificado nesta máquina (ManimCE 0.21.0 / PyAV 18.1.0):

* O ManimCE **não chama mais o binário ``ffmpeg``**. Desde as versões recentes
  ele usa **PyAV** (bindings de libav) direto em
  ``manim/scene/scene_file_writer.py``. Por isso não existe flag de CLI para
  trocar o codec: o valor está fixo no código
  (``partial_movie_file_codec = "libx264"``, ``crf=23``).
* Cada animação vira um *partial movie file* codificado individualmente.
  A junção final (``combine_files``) usa ``add_stream_from_template`` +
  ``mux`` de pacotes — ou seja, **stream copy, sem recodificar**.

  Consequência prática: basta trocar o codec dos *partial movies* para que o
  arquivo final inteiro saia em NVENC. É exatamente o que
  :func:`enable_nvenc` faz.

Estratégia do patch
-------------------
Em vez de reescrever ``open_partial_movie_stream`` (que mexe em estruturas
privadas como ``_PartialMovieEncodeJob``), interceptamos ``av.open`` **apenas
durante** a chamada desse método e devolvemos um proxy cujo ``add_stream``
reescreve codec/opções. Assim o patch sobrevive a mudanças internas do Manim.

Alpha / WebM
------------
NVENC **não codifica canal alfa**. Com ``-t/--transparent`` o Manim usa
``qtrle`` (RGBA lossless) e o patch se desliga sozinho para não quebrar a
transparência. WebM continua em ``libvpx-vp9`` pelo mesmo motivo (NVENC não
faz VP9).
"""

from __future__ import annotations

import dataclasses
import functools
import logging
import os
import shutil
import subprocess
from collections.abc import Iterable
from typing import Any

logger = logging.getLogger("manimx.gpu")

__all__ = [
    "GPUReport",
    "detect_gpu",
    "nvenc_available",
    "enable_nvenc",
    "disable_nvenc",
    "nvenc_options",
    "prime_env",
    "wgpu_adapters",
]


# --------------------------------------------------------------------------
# Detecção
# --------------------------------------------------------------------------


@dataclasses.dataclass
class GPUReport:
    """Resumo do que esta máquina consegue acelerar."""

    nvidia_gpu: str | None = None
    nvidia_driver: str | None = None
    cuda_version: str | None = None
    vram_mib: int | None = None
    gl_renderer_default: str | None = None
    gl_renderer_offload: str | None = None
    prime_offload_works: bool = False
    pyav_encoders: dict[str, bool] = dataclasses.field(default_factory=dict)
    wgpu_adapters: list[str] = dataclasses.field(default_factory=list)
    notes: list[str] = dataclasses.field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    def summary(self) -> str:
        lines = ["=== manimx GPU report ==="]
        lines.append(f"NVIDIA GPU        : {self.nvidia_gpu or '(não detectada)'}")
        lines.append(f"Driver / CUDA     : {self.nvidia_driver or '-'} / {self.cuda_version or '-'}")
        lines.append(f"VRAM              : {self.vram_mib or '-'} MiB")
        lines.append(f"OpenGL (padrão)   : {self.gl_renderer_default or '-'}")
        lines.append(f"OpenGL (offload)  : {self.gl_renderer_offload or '-'}")
        lines.append(f"PRIME offload     : {'OK' if self.prime_offload_works else 'indisponível'}")
        enc = ", ".join(k for k, v in self.pyav_encoders.items() if v) or "(nenhum)"
        lines.append(f"Encoders PyAV     : {enc}")
        lines.append(f"Adapters wgpu     : {', '.join(self.wgpu_adapters) or '-'}")
        for n in self.notes:
            lines.append(f"  ! {n}")
        return "\n".join(lines)


def _run(cmd: list[str], env: dict[str, str] | None = None, timeout: int = 20) -> str:
    try:
        full_env = {**os.environ, **(env or {})}
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, env=full_env
        )
        return out.stdout
    except (OSError, subprocess.SubprocessError):
        return ""


def prime_env() -> dict[str, str]:
    """Variáveis que forçam o OpenGL a rodar na dGPU NVIDIA (PRIME offload).

    Necessário em notebooks híbridos Intel+NVIDIA, onde o renderer OpenGL
    padrão é o Mesa/Intel. Usado pelo renderer ``opengl`` do ManimCE.

    O ManimGL (wgpu/Vulkan) **não precisa** disso — ele já pede
    ``power_preference="high-performance"`` e cai na dGPU sozinho.
    """
    return {
        "__NV_PRIME_RENDER_OFFLOAD": "1",
        "__GLX_VENDOR_LIBRARY_NAME": "nvidia",
        "__VK_LAYER_NV_optimus": "NVIDIA_only",
    }


def _gl_renderer(env: dict[str, str] | None = None) -> str | None:
    if not shutil.which("glxinfo"):
        return None
    out = _run(["glxinfo", "-B"], env=env)
    for line in out.splitlines():
        if line.strip().startswith("OpenGL renderer string:"):
            return line.split(":", 1)[1].strip()
    return None


def wgpu_adapters() -> list[str]:
    """Lista os adapters wgpu visíveis (usado pelo ManimGL master)."""
    try:
        import wgpu  # type: ignore
    except Exception:
        return []
    try:
        result = []
        for a in wgpu.gpu.enumerate_adapters_sync():
            info = a.info
            result.append(
                f"{info.get('device', '?')} [{info.get('backend_type', '?')}/"
                f"{info.get('adapter_type', '?')}]"
            )
        return result
    except Exception:  # pragma: no cover - depende do driver
        return []


#: Encoders que valem a pena checar no PyAV instalado.
PROBE_ENCODERS = (
    "h264_nvenc",
    "hevc_nvenc",
    "av1_nvenc",
    "libx264",
    "libx265",
    "libvpx-vp9",
    "qtrle",
    "prores_ks",
    "png",
    "gif",
)


def _probe_pyav_encoders(names: Iterable[str] = PROBE_ENCODERS) -> dict[str, bool]:
    try:
        from av.codec import Codec
    except Exception:
        return {}
    found: dict[str, bool] = {}
    for name in names:
        try:
            Codec(name, "w")
            found[name] = True
        except Exception:
            found[name] = False
    return found


def detect_gpu() -> GPUReport:
    """Inspeciona a máquina e devolve um :class:`GPUReport`."""
    rep = GPUReport()

    if shutil.which("nvidia-smi"):
        q = _run(
            [
                "nvidia-smi",
                "--query-gpu=name,driver_version,memory.total",
                "--format=csv,noheader,nounits",
            ]
        ).strip()
        if q:
            parts = [p.strip() for p in q.splitlines()[0].split(",")]
            if len(parts) >= 3:
                rep.nvidia_gpu, rep.nvidia_driver = parts[0], parts[1]
                try:
                    rep.vram_mib = int(parts[2])
                except ValueError:
                    pass
        smi = _run(["nvidia-smi"])
        for line in smi.splitlines():
            if "CUDA Version:" in line:
                rep.cuda_version = line.split("CUDA Version:")[1].split("|")[0].strip()
                break

    rep.gl_renderer_default = _gl_renderer()
    rep.gl_renderer_offload = _gl_renderer(prime_env())
    rep.prime_offload_works = bool(
        rep.gl_renderer_offload and "NVIDIA" in rep.gl_renderer_offload
    )

    rep.pyav_encoders = _probe_pyav_encoders()
    rep.wgpu_adapters = wgpu_adapters()

    if rep.nvidia_gpu and not rep.pyav_encoders.get("h264_nvenc"):
        rep.notes.append(
            "GPU NVIDIA presente mas o PyAV instalado não expõe h264_nvenc; "
            "encoding vai cair em libx264 (CPU)."
        )
    if rep.gl_renderer_default and "NVIDIA" not in rep.gl_renderer_default:
        rep.notes.append(
            "OpenGL padrão não é NVIDIA (gráficos híbridos). Para o renderer "
            "opengl do ManimCE use manimx.gpu.prime_env() ou os wrappers em bin/."
        )
    if rep.vram_mib and rep.vram_mib < 12000:
        rep.notes.append(
            f"VRAM de {rep.vram_mib} MiB: renderizar 4K com muitos mobjects "
            "pode estourar memória no renderer opengl. Prefira -qh e faça o "
            "upscale depois, ou renderize 4K no cairo."
        )
    return rep


def nvenc_available(codec: str = "h264_nvenc") -> bool:
    """``True`` se o PyAV consegue abrir o encoder NVENC pedido."""
    try:
        from av.codec import Codec

        Codec(codec, "w")
        return True
    except Exception:
        return False


def validate_encoder(
    codec: str,
    options: dict[str, str],
    *,
    width: int = 256,
    height: int = 144,
) -> tuple[bool, str | None]:
    """Abre um encoder de verdade e tenta codificar 1 frame.

    Existe porque o libav só valida as opções em ``avcodec_open2``, que o
    PyAV chama **preguiçosamente, no primeiro frame**. Sem esta checagem,
    uma opção inválida (ex.: ``profile=high`` em HEVC) só estoura no meio
    da renderização, depois de a cena inteira já ter sido computada.

    Returns
    -------
    (ok, motivo)
        ``motivo`` é ``None`` quando ``ok`` é ``True``.
    """
    try:
        import av
        import numpy as np
    except Exception as exc:  # pragma: no cover
        return False, f"import falhou: {exc}"

    import io

    try:
        buf = io.BytesIO()
        container = av.open(buf, mode="w", format="mp4")
        stream = container.add_stream(codec, rate=30, options=dict(options))
        stream.pix_fmt = "yuv420p"
        stream.width, stream.height = width, height
        frame = av.VideoFrame.from_ndarray(
            np.zeros((height, width, 3), dtype=np.uint8), format="rgb24"
        )
        for packet in stream.encode(frame):
            container.mux(packet)
        for packet in stream.encode():
            container.mux(packet)
        container.close()
    except Exception as exc:
        return False, f"encode: {type(exc).__name__}: {exc}"

    # Segunda metade: o Manim junta os partial movies com
    # `add_stream_from_template(template=<stream de entrada>)`. Para alguns
    # codecs (AV1 nesta build do PyAV) o stream de entrada resolve para um
    # DECODER cujo nome não existe como encoder — e o remux estoura com
    # UnknownCodecError, depois de a cena inteira já ter sido renderizada.
    # Testamos esse caminho aqui.
    try:
        buf.seek(0)
        src = av.open(buf, mode="r")
        out = av.open(io.BytesIO(), mode="w", format="mp4")
        out.add_stream_from_template(template=src.streams.video[0])
        out.close()
        src.close()
        return True, None
    except Exception as exc:
        return False, (
            f"remux: {type(exc).__name__}: {exc} — o codec grava, mas o Manim "
            "não consegue juntar os partial movies com ele"
        )


# --------------------------------------------------------------------------
# Opções de encoding
# --------------------------------------------------------------------------

#: Perfis NVENC afinados para conteúdo de animação (cores chapadas, bordas
#: duras, gradientes lisos) — onde NVENC costuma sofrer com banding se
#: configurado no automático.
NVENC_PROFILES: dict[str, dict[str, str]] = {
    # Iteração rápida: prioriza velocidade.
    "fast": {
        "preset": "p1",
        "tune": "hq",
        "rc": "vbr",
        "cq": "26",
        "b": "0",
    },
    # Padrão: bom equilíbrio, praticamente indistinguível de x264 crf 23.
    "balanced": {
        "preset": "p4",
        "tune": "hq",
        "rc": "vbr",
        "cq": "20",
        "b": "0",
        "spatial-aq": "1",
        "temporal-aq": "1",
        "rc-lookahead": "20",
        "bf": "3",
    },
    # Entrega final: qualidade máxima que o NVENC dá.
    "quality": {
        "preset": "p7",
        "tune": "hq",
        "rc": "vbr",
        "cq": "16",
        "b": "0",
        "spatial-aq": "1",
        "temporal-aq": "1",
        "aq-strength": "12",
        "rc-lookahead": "32",
        "bf": "3",
        "multipass": "fullres",
    },
    # Sem perdas: arquivo grande, para masterização / reencode posterior.
    "lossless": {
        "preset": "p7",
        "tune": "lossless",
    },
}

#: Nomes de *profile* válidos por codec. Isto é uma pegadinha real do NVENC:
#: ``profile=high`` só existe em H.264. Passar "high" para ``hevc_nvenc`` ou
#: ``av1_nvenc`` faz o ``avcodec_open2`` retornar EINVAL (22) e a
#: renderização morre no meio, já com frames na fila.
#: (verificado nesta máquina: RTX 4070 Laptop / driver 580 / PyAV 18.1.0)
CODEC_PROFILE: dict[str, str] = {
    "h264_nvenc": "high",
    "hevc_nvenc": "main",
    # av1_nvenc não expõe a opção `profile` — passá-la dá EINVAL.
}

#: Opções que cada encoder NVENC rejeita, verificado empiricamente com
#: :func:`validate_encoder`.
CODEC_UNSUPPORTED_OPTIONS: dict[str, tuple[str, ...]] = {
    "av1_nvenc": ("profile",),
}

#: Perfis que um codec não suporta — caem no substituto indicado.
CODEC_PROFILE_FALLBACK: dict[tuple[str, str], str] = {
    # AV1 NVENC não tem `tune=lossless`.
    ("av1_nvenc", "lossless"): "quality",
}


def nvenc_options(profile: str = "balanced", codec: str = "h264_nvenc") -> dict[str, str]:
    """Opções libav para um perfil NVENC, já ajustadas ao ``codec`` alvo.

    O ajuste por codec não é cosmético. ``profile=high`` só existe em
    H.264; em HEVC o nome é ``main`` e em AV1 a opção nem existe. Passar
    o valor errado faz ``avcodec_open2`` devolver EINVAL — e como o PyAV
    só abre o encoder no primeiro frame, o erro apareceria no meio da
    renderização. Ver :data:`CODEC_PROFILE` e
    :data:`CODEC_UNSUPPORTED_OPTIONS`.
    """
    if profile not in NVENC_PROFILES:
        raise ValueError(
            f"perfil NVENC desconhecido: {profile!r}. "
            f"Use um de: {', '.join(NVENC_PROFILES)}"
        )

    effective = CODEC_PROFILE_FALLBACK.get((codec, profile))
    if effective:
        logger.info(
            "manimx: %s não suporta o perfil %r; usando %r.", codec, profile, effective
        )
        profile = effective

    opts = dict(NVENC_PROFILES[profile])

    if profile != "lossless" and codec in CODEC_PROFILE:
        opts["profile"] = CODEC_PROFILE[codec]

    for bad in CODEC_UNSUPPORTED_OPTIONS.get(codec, ()):
        opts.pop(bad, None)
    return opts


# --------------------------------------------------------------------------
# O patch
# --------------------------------------------------------------------------


class _StreamRewriteProxy:
    """Proxy de ``av.container.OutputContainer`` que reescreve ``add_stream``.

    Delega tudo o mais (``mux``, ``close``, ``metadata``...) para o container
    real, então o resto do Manim não percebe diferença.
    """

    __slots__ = ("_inner", "_codec", "_options", "_applied")

    def __init__(self, inner: Any, codec: str, options: dict[str, str]):
        object.__setattr__(self, "_inner", inner)
        object.__setattr__(self, "_codec", codec)
        object.__setattr__(self, "_options", options)
        object.__setattr__(self, "_applied", False)

    def add_stream(self, *args: Any, **kwargs: Any) -> Any:
        inner = object.__getattribute__(self, "_inner")
        codec = object.__getattribute__(self, "_codec")
        options = object.__getattribute__(self, "_options")

        # Descobre qual codec o Manim pediu (posicional ou nomeado).
        requested = kwargs.get("codec_name")
        if requested is None and args:
            requested = args[0]

        # Só reescrevemos H.264. qtrle (alpha) e libvpx-vp9 (webm) ficam
        # intactos — NVENC não cobre esses casos.
        if requested != "libx264":
            logger.debug("manimx: codec %r mantido (fora do escopo NVENC)", requested)
            return inner.add_stream(*args, **kwargs)

        merged = dict(kwargs.get("options") or {})
        merged.pop("crf", None)  # crf é do x264; NVENC usa cq
        merged.update(options)

        new_kwargs = dict(kwargs)
        new_kwargs["options"] = merged
        new_kwargs.pop("codec_name", None)
        new_args = args[1:] if (args and requested == args[0]) else args

        object.__setattr__(self, "_applied", True)
        return inner.add_stream(codec, *new_args, **new_kwargs)

    def __getattr__(self, item: str) -> Any:
        return getattr(object.__getattribute__(self, "_inner"), item)

    def __setattr__(self, key: str, value: Any) -> None:
        setattr(object.__getattribute__(self, "_inner"), key, value)

    def __enter__(self) -> Any:
        return object.__getattribute__(self, "_inner").__enter__()

    def __exit__(self, *exc: Any) -> Any:
        return object.__getattribute__(self, "_inner").__exit__(*exc)


_ORIGINAL_OPEN_STREAM: Any = None
_ACTIVE: dict[str, Any] = {}


def enable_nvenc(
    codec: str = "h264_nvenc",
    profile: str = "balanced",
    *,
    options: dict[str, str] | None = None,
    strict: bool = False,
) -> bool:
    """Faz o ManimCE codificar os *partial movies* com NVENC.

    Parameters
    ----------
    codec
        ``h264_nvenc`` (padrão, compatibilidade máxima), ``hevc_nvenc``
        (~30% menor, menos compatível) ou ``av1_nvenc`` (só Ada/RTX 40+).
    profile
        Um de ``fast``, ``balanced``, ``quality``, ``lossless``.
        Ver :data:`NVENC_PROFILES`.
    options
        Opções libav extras/sobrescritas, aplicadas por cima do perfil.
    strict
        Se ``True``, levanta ``RuntimeError`` quando NVENC não estiver
        disponível, em vez de só avisar e seguir em CPU.

    Returns
    -------
    bool
        ``True`` se o patch foi aplicado; ``False`` se caiu no fallback CPU.

    Notes
    -----
    * Idempotente: chamar duas vezes só atualiza as opções.
    * Não afeta ``--transparent`` (qtrle) nem ``--format webm`` (vp9).
    * Reverta com :func:`disable_nvenc`.
    """
    global _ORIGINAL_OPEN_STREAM

    if not nvenc_available(codec):
        msg = (
            f"NVENC indisponível: o PyAV instalado não abre {codec!r}. "
            "Encoding continua em libx264 (CPU)."
        )
        if strict:
            raise RuntimeError(msg)
        logger.warning("manimx: %s", msg)
        return False

    opts = nvenc_options(profile, codec)
    if options:
        opts.update(options)

    ok, why = validate_encoder(codec, opts)
    if not ok:
        msg = (
            f"NVENC {codec!r} recusou as opções do perfil {profile!r}: {why}. "
            "Encoding continua em libx264 (CPU)."
        )
        if strict:
            raise RuntimeError(msg)
        logger.warning("manimx: %s", msg)
        return False

    from manim.scene.scene_file_writer import SceneFileWriter

    if _ORIGINAL_OPEN_STREAM is None:
        _ORIGINAL_OPEN_STREAM = SceneFileWriter.open_partial_movie_stream

    original = _ORIGINAL_OPEN_STREAM

    @functools.wraps(original)
    def patched(self: Any, file_path: Any = None) -> Any:
        import av

        real_open = av.open

        def open_proxy(*args: Any, **kwargs: Any) -> Any:
            container = real_open(*args, **kwargs)
            if kwargs.get("mode") == "w" or (len(args) > 1 and args[1] == "w"):
                return _StreamRewriteProxy(container, codec, opts)
            return container

        av.open = open_proxy  # type: ignore[assignment]
        try:
            return original(self, file_path)
        finally:
            av.open = real_open  # type: ignore[assignment]

    SceneFileWriter.open_partial_movie_stream = patched  # type: ignore[method-assign]
    _ACTIVE.update({"codec": codec, "profile": profile, "options": opts})
    logger.info("manimx: NVENC ativo — %s / perfil %s", codec, profile)
    return True


def disable_nvenc() -> None:
    """Reverte :func:`enable_nvenc` e volta ao libx264 padrão do Manim."""
    global _ORIGINAL_OPEN_STREAM
    if _ORIGINAL_OPEN_STREAM is None:
        return
    from manim.scene.scene_file_writer import SceneFileWriter

    SceneFileWriter.open_partial_movie_stream = _ORIGINAL_OPEN_STREAM  # type: ignore[method-assign]
    _ORIGINAL_OPEN_STREAM = None
    _ACTIVE.clear()
    logger.info("manimx: NVENC desativado (voltou para libx264)")


def active_encoder() -> dict[str, Any]:
    """Estado atual do patch NVENC (vazio se inativo)."""
    return dict(_ACTIVE)
