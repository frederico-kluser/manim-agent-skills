#!/usr/bin/env python
"""Renderização em lote com paralelismo real (multi-processo).

Por que multi-processo e não threads: o ``config`` do Manim é um singleton
global mutável. Duas cenas renderizando no mesmo processo corrompem o
estado uma da outra (resolução, media_dir, codec). Cada worker aqui é um
processo separado com seu próprio ``config``.

Uso::

    python tools/batch_render.py scenes/*.py --quality h --codec nvenc -j 4
    python tools/batch_render.py scenes/aula.py --scenes Intro Fim --json
    python tools/batch_render.py scenes/ --all -q m --codec x264 -j 8

Sobre o paralelismo:

* O padrão de ``-j`` é ``min(4, cpus // 4)``. Cada worker do Manim já usa
  vários núcleos no Cairo e no encoder, então subir demais causa
  *thrashing* em vez de ganho.
* **NVENC tem limite de sessões simultâneas** nas GPUs de consumidor.
  Passar de ~3 encoders NVENC ao mesmo tempo costuma falhar com erro de
  inicialização. Este script detecta isso e recomenda ``--codec x264``
  para lotes largos — CPU sobra, e são processos independentes.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _discover(paths: list[str]) -> list[Path]:
    """Expande diretórios e globs em uma lista de arquivos .py."""
    files: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            files.extend(sorted(q for q in p.rglob("*.py") if not q.name.startswith("_")))
        elif p.is_file():
            files.append(p)
        else:
            files.extend(sorted(Path().glob(raw)))
    seen: set[Path] = set()
    out: list[Path] = []
    for f in files:
        r = f.resolve()
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def _worker_slot() -> int:
    """Índice estável do worker dentro do pool (1, 2, 3...).

    Usamos o índice, e não o PID, para que o diretório de LaTeX de cada
    worker seja o mesmo entre execuções — assim o cache de compilação do
    TeX continua sendo reaproveitado.
    """
    import multiprocessing

    ident = getattr(multiprocessing.current_process(), "_identity", ())
    return ident[0] if ident else 0


def _job(payload: dict[str, Any]) -> dict[str, Any]:
    """Executado em processo separado — importa o Manim do zero."""
    import warnings

    warnings.filterwarnings("ignore")
    sys.path.insert(0, str(REPO_ROOT))

    from manimx.render import render_file

    overrides: dict[str, Any] = {}
    if not payload["shared_tex"]:
        # Corrida real, reproduzida neste projeto: dois workers compilando
        # LaTeX no mesmo media/Tex colidem na limpeza dos .aux e um deles
        # morre com FileNotFoundError. Isolar o diretório por worker
        # resolve; o custo é um cache de TeX por slot.
        #
        # Os diretórios por worker ficam FORA de media/Tex de propósito.
        # `manim.utils.tex_file_writing` limpa o tex_dir com
        # `for f in tex_dir.iterdir(): f.unlink()` — sem checar se é
        # diretório. Um subdiretório dentro de media/Tex faz TODA
        # renderização de LaTeX posterior (inclusive fora do lote) morrer
        # com IsADirectoryError.
        slot = _worker_slot()
        media = Path(payload["media_dir"]).resolve()
        overrides["tex_dir"] = str(media / "_workers" / f"w{slot}" / "Tex")
        overrides["text_dir"] = str(media / "_workers" / f"w{slot}" / "texts")

    started = time.perf_counter()
    try:
        result = render_file(
            payload["file"],
            payload["scene"],
            quality=payload["quality"],
            codec=payload["codec"],
            renderer=payload["renderer"],
            media_dir=payload["media_dir"],
            disable_caching=payload["no_cache"],
            max_inflight_encoders=payload["encoders"],
            verbosity="CRITICAL",
            config_overrides=overrides,
        )
        d = result.as_dict()
    except BaseException as exc:  # noqa: BLE001
        d = {
            "scene_name": payload["scene"],
            "success": False,
            "error": f"{type(exc).__name__}: {exc}",
            "output_file": None,
        }
    d["file"] = str(payload["file"])
    d["wall_s"] = round(time.perf_counter() - started, 2)
    return d


def main(argv: list[str] | None = None) -> int:
    cpus = os.cpu_count() or 4
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("paths", nargs="+", help="arquivos .py, diretórios ou globs")
    p.add_argument("--scenes", nargs="*", default=None,
                   help="renderizar só estas cenas (por nome)")
    p.add_argument("-q", "--quality", default="h")
    p.add_argument("--codec", default="nvenc")
    p.add_argument("--renderer", default="cairo", choices=["cairo", "opengl"])
    p.add_argument("--media-dir", default="media")
    p.add_argument("--no-cache", action="store_true")
    p.add_argument("--encoders", type=int, default=2,
                   help="encoders paralelos DENTRO de cada worker")
    p.add_argument("-j", "--jobs", type=int, default=max(1, min(4, cpus // 4)))
    p.add_argument("--shared-tex", action="store_true",
                   help="usar um media/Tex único para todos os workers "
                        "(mais cache, mas causa corrida de LaTeX com -j > 1)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="só lista o que faria")
    args = p.parse_args(argv)

    import warnings

    warnings.filterwarnings("ignore")
    from manimx.render import list_scenes

    files = _discover(args.paths)
    if not files:
        print("nenhum arquivo .py encontrado", file=sys.stderr)
        return 1

    payloads: list[dict[str, Any]] = []
    for f in files:
        try:
            names = list_scenes(f)
        except Exception as exc:
            print(f"aviso: pulei {f}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        if args.scenes:
            names = [n for n in names if n in args.scenes]
        for n in names:
            payloads.append({
                "file": str(f), "scene": n,
                "quality": args.quality, "codec": args.codec,
                "renderer": args.renderer, "media_dir": args.media_dir,
                "no_cache": args.no_cache, "encoders": args.encoders,
                "shared_tex": args.shared_tex,
            })

    if not payloads:
        print("nenhuma cena para renderizar", file=sys.stderr)
        return 1

    if args.codec.startswith(("nvenc", "hevc", "av1")) and args.jobs > 4:
        print(
            f"aviso: {args.jobs} workers NVENC simultâneos. GPUs de consumidor "
            "limitam sessões de encoding; 4 foi verificado nesta máquina. "
            "Acima disso, se aparecer erro de inicialização do encoder, use "
            "--codec x264 — em lote o gargalo costuma ser a rasterização, "
            "não o encoding, então a diferença é pequena.",
            file=sys.stderr,
        )

    if args.dry_run:
        for pl in payloads:
            print(f"{Path(pl['file']).name}::{pl['scene']}")
        print(f"\n{len(payloads)} cena(s), {args.jobs} worker(s)")
        return 0

    started = time.perf_counter()
    results: list[dict[str, Any]] = []
    with cf.ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(_job, pl): pl for pl in payloads}
        for i, fut in enumerate(cf.as_completed(futures), 1):
            r = fut.result()
            results.append(r)
            if not args.json:
                mark = "OK   " if r.get("success") else "FALHA"
                print(f"[{i}/{len(payloads)}] {mark} {r['scene_name']:26s} "
                      f"{r['wall_s']:6.1f}s  {r.get('output_file') or r.get('error')}")

    elapsed = time.perf_counter() - started
    ok = sum(1 for r in results if r.get("success"))

    if args.json:
        print(json.dumps({
            "total": len(results), "ok": ok, "failed": len(results) - ok,
            "elapsed_s": round(elapsed, 2), "jobs": args.jobs,
            "results": results,
        }, indent=2, ensure_ascii=False, default=str))
    else:
        print(f"\n{ok}/{len(results)} cena(s) em {elapsed:.1f}s "
              f"com {args.jobs} worker(s)")

    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
