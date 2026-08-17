"""CLI ``mx`` — a porta de entrada para agentes.

Tudo devolve JSON quando você passa ``--json``, então um agente não
precisa parsear log colorido.

Comandos::

    mx doctor                 # o ambiente está sadio? (exit != 0 se não)
    mx gpu                    # relatório de GPU
    mx scenes ARQ.py          # lista cenas
    mx render ARQ.py [CENA]   # renderiza
    mx api-dump               # regenera api/
    mx api-diff               # regenera api/ce-vs-gl.md
    mx find TERMO             # busca na API do Manim
    mx show CLASSE            # métodos/assinatura de uma classe
    mx presets                # qualidade / codecs / temas
    mx bench                  # compara CPU vs GPU nesta máquina
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

#: stdout real, guardado antes de qualquer redirecionamento (ver `main`).
_REAL_STDOUT = sys.stdout


def _out(data: Any, as_json: bool) -> None:
    """Escreve o resultado no stdout **real**, mesmo sob redirecionamento."""
    stream = _REAL_STDOUT if as_json else sys.stdout
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False, default=str), file=stream)
    else:
        print(data, file=stream)


# --------------------------------------------------------------------------


def cmd_gpu(args: argparse.Namespace) -> int:
    from manimx.gpu import detect_gpu

    rep = detect_gpu()
    _out(rep.as_dict() if args.json else rep.summary(), args.json)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Checa tudo que o Manim precisa e devolve exit != 0 se algo faltar."""
    import shutil
    import subprocess

    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str, fatal: bool = True) -> None:
        checks.append({"check": name, "ok": ok, "detail": detail, "fatal": fatal})

    # ManimCE 0.19.2+ exige Python >= 3.11. Em interpretador antigo o
    # `pip install manim` NÃO falha: ele resolve silenciosamente para uma
    # versão velha (0.18/0.19). Por isso checamos a versão resolvida, não
    # só se o import funcionou.
    add(
        "python >= 3.11",
        sys.version_info >= (3, 11),
        sys.version.split()[0]
        + ("" if sys.version_info >= (3, 11) else "  (ManimCE 0.21 exige 3.11+)"),
    )

    try:
        import manim

        parts = tuple(
            int(x) for x in manim.__version__.split(".")[:2] if x.isdigit()
        )
        recent = parts >= (0, 20)
        add(
            "manim (CE)",
            True,
            f"v{manim.__version__}"
            + ("" if recent else "  (ANTIGA — pip resolveu para trás?)"),
        )
        if not recent:
            add(
                "manim atualizado",
                False,
                "0.20+ traz encoding paralelo e o Cairo 2.2x mais rápido",
                fatal=False,
            )
    except Exception as exc:
        add("manim (CE)", False, str(exc))

    try:
        import av
        from av.codec import Codec

        Codec("libx264", "w")
        add("PyAV + libx264", True, f"PyAV {av.__version__}")
    except Exception as exc:
        add("PyAV + libx264", False, str(exc))

    from manimx.gpu import nvenc_available

    add(
        "NVENC (h264_nvenc)",
        nvenc_available(),
        "encoding por GPU disponível" if nvenc_available() else "cai em libx264 (CPU)",
        fatal=False,
    )

    for exe, fatal in (("latex", False), ("dvisvgm", False), ("ffmpeg", False)):
        path = shutil.which(exe)
        add(exe, path is not None, path or "não encontrado no PATH", fatal=fatal)

    # LaTeX de verdade: compila um documento mínimo igual ao do Manim.
    try:
        from manim import MathTex, tempconfig

        with tempconfig({"verbosity": "CRITICAL"}):
            MathTex(r"x^2")
        add("LaTeX → SVG (MathTex)", True, "compila e converte")
    except Exception as exc:
        add(
            "LaTeX → SVG (MathTex)",
            False,
            f"{type(exc).__name__}: {str(exc)[:200]}",
            fatal=False,
        )

    try:
        from manim import Text

        Text("abc")
        add("Pango (Text)", True, "ok")
    except Exception as exc:
        add("Pango (Text)", False, str(exc)[:200])

    # ManimGL: a versão NÃO distingue os dois backends. O wheel do PyPI
    # (1.7.2, dez/2024) é OpenGL/ModernGL; o git master é WebGPU — e o
    # master ainda se autodeclara 1.7.2. Só dá para saber olhando as
    # dependências instaladas.
    try:
        gl_py = REPO_ROOT / ".venv-gl" / "bin" / "python"
        if gl_py.exists():
            probe = subprocess.run(
                [
                    str(gl_py),
                    "-c",
                    "import warnings;warnings.filterwarnings('ignore');"
                    "import manimlib,importlib.util as u;"
                    "b='wgpu/Vulkan' if u.find_spec('wgpu') else "
                    "('OpenGL/ModernGL' if u.find_spec('moderngl') else '?');"
                    "print(manimlib.__version__, b)",
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            out = (probe.stdout or probe.stderr).strip().splitlines()
            detail = out[-1][:80] if out else "sem saída"
            add("manimgl", probe.returncode == 0, detail, fatal=False)
        else:
            add("manimgl", False, "venv .venv-gl ausente", fatal=False)
    except Exception as exc:
        add("manimgl", False, str(exc)[:120], fatal=False)

    failed_fatal = [c for c in checks if not c["ok"] and c["fatal"]]

    if args.json:
        _out({"ok": not failed_fatal, "checks": checks}, True)
    else:
        print("=== mx doctor ===")
        for c in checks:
            mark = "OK  " if c["ok"] else ("FALHA" if c["fatal"] else "aviso")
            print(f"[{mark:5s}] {c['check']:22s} {c['detail']}")
        print()
        print("Ambiente pronto." if not failed_fatal
              else f"{len(failed_fatal)} verificação(ões) obrigatória(s) falhou/falharam.")
    return 1 if failed_fatal else 0


def cmd_scenes(args: argparse.Namespace) -> int:
    from manimx.render import load_scene_classes

    classes = load_scene_classes(args.file)
    data = [
        {
            "name": c.__name__,
            "bases": [b.__name__ for b in c.__bases__],
            "doc": (c.__doc__ or "").strip().splitlines()[0] if c.__doc__ else None,
        }
        for c in classes
    ]
    if args.json:
        _out(data, True)
    else:
        for d in data:
            print(f"{d['name']:34s} ({', '.join(d['bases'])})"
                  + (f"  — {d['doc']}" if d["doc"] else ""))
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    from manimx.render import render_file

    kwargs: dict[str, Any] = {
        "quality": args.quality,
        "renderer": args.renderer,
        "codec": args.codec,
        "media_dir": args.media_dir,
        "disable_caching": args.no_cache,
        "verbosity": args.verbosity,
    }
    if args.theme:
        kwargs["theme"] = args.theme
    if args.fps:
        kwargs["fps"] = args.fps
    if args.resolution:
        w, h = args.resolution.lower().replace("x", ",").split(",")
        kwargs["resolution"] = (int(w), int(h))
    if args.format:
        kwargs["fmt"] = args.format
    if args.output:
        kwargs["output_file"] = args.output
    if args.transparent:
        kwargs["transparent"] = True
    if args.parallel_encoders:
        kwargs["max_inflight_encoders"] = args.parallel_encoders
    if args.background:
        kwargs["background_color"] = args.background

    res = render_file(
        args.file,
        args.scenes or None,
        all_scenes=args.all,
        **kwargs,
    )
    results = res if isinstance(res, list) else [res]

    if args.json:
        _out([r.as_dict() for r in results], True)
    else:
        for r in results:
            if r.success:
                print(f"OK    {r.scene_name:28s} {r.elapsed_s:6.2f}s  "
                      f"{r.codec:11s} {r.resolution[0]}x{r.resolution[1]}@{r.frame_rate:g}"
                      f"  -> {r.output_file}")
            else:
                print(f"FALHA {r.scene_name:28s} {r.error}", file=sys.stderr)
    return 0 if all(r.success for r in results) else 1


def cmd_api_dump(args: argparse.Namespace) -> int:
    from manimx.introspect import dump_api

    written = dump_api(args.out, args.package, label=args.label or args.package)
    _out({k: str(v) for k, v in written.items()}, args.json)
    return 0


def cmd_api_diff(args: argparse.Namespace) -> int:
    from manimx.apidiff import write_diff

    path = write_diff(args.ce, args.gl, args.out)
    _out(str(path), args.json)
    return 0


def _load_index(package: str = "manim-ce") -> dict[str, Any]:
    """Carrega o índice de API, aceitando ``.json`` ou ``.json.gz``.

    O ``mx api-dump`` grava a forma comprimida (14 MiB -> 1,4 MiB) e apaga
    qualquer ``.json`` cru que tenha sobrado, para não servir um índice
    velho. A leitura ainda aceita a forma crua — para o caso de um dump
    feito à mão — e ela tem precedência quando existe.
    """
    base = REPO_ROOT / "api"
    plain = base / f"{package}-api.json"
    packed = base / f"{package}-api.json.gz"

    if plain.exists():
        return json.loads(plain.read_text(encoding="utf-8"))
    if packed.exists():
        import gzip

        with gzip.open(packed, "rt", encoding="utf-8") as fh:
            return json.load(fh)

    raise SystemExit(
        f"índice não encontrado ({plain.name} nem {packed.name}). "
        "Rode `mx api-dump` para gerar."
    )


def cmd_find(args: argparse.Namespace) -> int:
    data = _load_index(args.package)
    q = args.query.lower()
    hits = []
    for s in data["symbols"].values():
        if args.kind and s["kind"] != args.kind:
            continue
        if args.category and not s["category"].startswith(args.category):
            continue
        name = s["name"].lower()
        doc = (s.get("doc") or "").lower()
        if name == q:
            score = 0
        elif name.startswith(q):
            score = 1
        elif q in name:
            score = 2
        elif q in doc:
            score = 3
        elif any(q in m["name"].lower() for m in s.get("methods", [])):
            score = 4
        else:
            continue
        hits.append((score, s))
    hits.sort(key=lambda h: (h[0], h[1]["name"]))
    hits = hits[: args.limit]

    if args.json:
        _out([h[1] for h in hits], True)
    else:
        for _, s in hits:
            print(f"{s['kind']:8s} {s['name']:32s} {s['category']:22s} "
                  f"{s.get('signature') or s.get('value_repr') or ''}"[:190])
            if s.get("doc"):
                print(f"         {s['doc']}"[:190])
    return 0 if hits else 1


def cmd_show(args: argparse.Namespace) -> int:
    data = _load_index(args.package)
    matches = [s for s in data["symbols"].values() if s["name"] == args.name]
    if not matches:
        print(f"{args.name!r} não encontrado. Tente `mx find {args.name}`.", file=sys.stderr)
        return 1
    s = matches[0]
    if args.json:
        _out(s, True)
        return 0

    print(f"{s['kind']} {s['name']}{s.get('signature') or ''}")
    print(f"módulo   : {s['module']}")
    print(f"categoria: {s['category']}")
    if s.get("bases"):
        print(f"herda de : {', '.join(s['bases'])}")
    if s.get("doc"):
        print(f"doc      : {s['doc']}")
    methods = s.get("methods", [])
    own = [m for m in methods if not m["inherited"]]
    inherited = [m for m in methods if m["inherited"]]
    if s.get("properties"):
        print(f"\npropriedades ({len(s['properties'])}): {', '.join(s['properties'])}")
    if own:
        print(f"\nmétodos próprios ({len(own)}):")
        for m in own:
            print(f"  {m['name']}{m['signature'] or '()'}"
                  + (f"\n      {m['doc']}" if m["doc"] else ""))
    if inherited and not args.own_only:
        print(f"\nmétodos herdados ({len(inherited)}):")
        for m in inherited:
            print(f"  [{m['defined_in']}] {m['name']}{m['signature'] or '()'}")
    elif inherited:
        print(f"\n(+{len(inherited)} métodos herdados — rode sem --own-only para ver)")
    return 0


def cmd_presets(args: argparse.Namespace) -> int:
    from manimx.gpu import NVENC_PROFILES
    from manimx.presets import CODEC_PRESETS, QUALITY_PRESETS, THEMES

    data = {
        "quality": QUALITY_PRESETS,
        "codec": CODEC_PRESETS,
        "nvenc_profiles": NVENC_PROFILES,
        "themes": THEMES,
    }
    if args.json:
        _out(data, True)
        return 0
    print("QUALIDADE (-q / quality=)")
    for k, v in QUALITY_PRESETS.items():
        print(f"  {k}  {v['pixel_width']}x{v['pixel_height']} @ {v['frame_rate']}fps"
              f"   ({v['alias']})")
    print("\nCODEC (codec=)")
    for k, v in CODEC_PRESETS.items():
        gpu = "GPU" if v.get("gpu") else "CPU"
        print(f"  {k:16s} [{gpu}] {v['desc']}")
    print("\nPERFIS NVENC")
    for k, v in NVENC_PROFILES.items():
        print(f"  {k:10s} {v}")
    print("\nTEMAS (theme=)")
    for k, v in THEMES.items():
        print(f"  {k:18s} bg={v['background_color']}  {v['desc']}")
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    """Mede, nesta máquina, CPU vs GPU nos eixos que realmente mudam."""
    from manimx.bench import run_benchmark

    report = run_benchmark(
        quality=args.quality,
        repeats=args.repeats,
        media_dir=args.media_dir,
    )
    if args.json:
        _out(report, True)
    else:
        print(report["text"])
    return 0


# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    # Flags globais também vivem num parser-pai, para que funcionem TANTO
    # antes quanto depois do subcomando. Sem isto, `mx gpu --json` falha
    # com "unrecognized arguments" — argparse só aceitaria `mx --json gpu`,
    # que é a ordem menos intuitiva.
    # `default=SUPPRESS` é o detalhe que faz isto funcionar nas duas
    # posições: quando a flag não é passada, ela não é escrita no namespace,
    # então o valor definido em `p.set_defaults` sobrevive em vez de o
    # subparser sobrescrever um `--json` global com False.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true",
                        default=argparse.SUPPRESS, help="saída em JSON")
    common.add_argument("-v", "--verbose", action="store_true",
                        default=argparse.SUPPRESS, help="log de debug")

    p = argparse.ArgumentParser(
        prog="mx",
        description="Camada de API do Manim para agentes de código.",
        parents=[common],
    )
    p.set_defaults(json=False, verbose=False)
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("gpu", help="relatório de GPU e encoders",
                   parents=[common]).set_defaults(func=cmd_gpu)
    sub.add_parser("doctor", help="checa o ambiente inteiro",
                   parents=[common]).set_defaults(func=cmd_doctor)

    s = sub.add_parser("scenes", help="lista as cenas de um arquivo", parents=[common])
    s.add_argument("file")
    s.set_defaults(func=cmd_scenes)

    s = sub.add_parser("render", help="renderiza cena(s)", parents=[common])
    s.add_argument("file")
    s.add_argument("scenes", nargs="*", help="nomes das cenas (vazio = a única)")
    s.add_argument("-a", "--all", action="store_true", help="todas as cenas do arquivo")
    s.add_argument("-q", "--quality", default="h", help="l|m|h|p|k ou 1080p/4k/draft…")
    s.add_argument("--renderer", default="cairo", choices=["cairo", "opengl"])
    s.add_argument("--codec", default="nvenc", help="ver `mx presets`")
    s.add_argument("--theme", default=None, help="ver `mx presets`")
    s.add_argument("--format", default=None, choices=["mp4", "gif", "webm", "mov", "png"])
    s.add_argument("--fps", type=float, default=None)
    s.add_argument("-r", "--resolution", default=None, help='ex: "1920x1080"')
    s.add_argument("-o", "--output", default=None, help="nome do arquivo de saída")
    s.add_argument("--media-dir", default="media")
    s.add_argument("-t", "--transparent", action="store_true")
    s.add_argument("--background", default=None, help='cor hex de 6 dígitos, ex "#FFFFFF"')
    s.add_argument("--no-cache", action="store_true", help="ignora partial movies em cache")
    s.add_argument("-j", "--parallel-encoders", type=int, default=None,
                   help="encoders simultâneos (ManimCE >= 0.20). 4 é um bom valor.")
    s.add_argument("--verbosity", default="WARNING")
    s.set_defaults(func=cmd_render)

    s = sub.add_parser("api-dump", help="regenera os índices em api/", parents=[common])
    s.add_argument("--package", default="manim")
    s.add_argument("--label", default=None)
    s.add_argument("--out", default=str(REPO_ROOT / "api"))
    s.set_defaults(func=cmd_api_dump)

    s = sub.add_parser("api-diff", help="regenera api/ce-vs-gl.md", parents=[common])
    s.add_argument("--ce", default=str(REPO_ROOT / "api" / "manim-ce-api.json.gz"))
    s.add_argument("--gl", default=str(REPO_ROOT / "api" / "manimgl-api.json.gz"))
    s.add_argument("--out", default=str(REPO_ROOT / "api" / "ce-vs-gl.md"))
    s.set_defaults(func=cmd_api_diff)

    s = sub.add_parser("find", help="busca na API indexada", parents=[common])
    s.add_argument("query")
    s.add_argument("--package", default="manim-ce", help="manim-ce | manimgl")
    s.add_argument("--kind", default=None, choices=["class", "function", "constant"])
    s.add_argument("--category", default=None, help="ex: animation/ ou mobject/geometry")
    s.add_argument("-n", "--limit", type=int, default=30)
    s.set_defaults(func=cmd_find)

    s = sub.add_parser("show", help="detalha uma classe/função", parents=[common])
    s.add_argument("name")
    s.add_argument("--package", default="manim-ce")
    s.add_argument("--own-only", action="store_true", help="esconde métodos herdados")
    s.set_defaults(func=cmd_show)

    sub.add_parser("presets", help="qualidade, codecs, temas", parents=[common]).set_defaults(func=cmd_presets)

    s = sub.add_parser("bench", help="mede CPU vs GPU nesta máquina", parents=[common])
    s.add_argument("-q", "--quality", default="h")
    s.add_argument("--repeats", type=int, default=1)
    s.add_argument("--media-dir", default="media/_bench")
    s.set_defaults(func=cmd_bench)

    return p


def main(argv: list[str] | None = None) -> int:
    import contextlib
    import warnings

    warnings.filterwarnings("ignore", category=SyntaxWarning)
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    # Com --json, o stdout precisa conter SÓ o JSON. O Manim escreve avisos
    # no stdout via rich (ex.: "Output format changed to '.mp4' to support
    # transparency"), o que quebraria qualquer agente fazendo json.loads.
    # Mandamos tudo isso para o stderr; `_out` escreve no stdout real.
    redirect = (
        contextlib.redirect_stdout(sys.stderr)
        if args.json
        else contextlib.nullcontext()
    )

    try:
        with redirect:
            return int(args.func(args) or 0)
    except KeyboardInterrupt:
        return 130
    except SystemExit:
        raise
    except Exception as exc:
        if args.verbose:
            raise
        print(f"erro: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
