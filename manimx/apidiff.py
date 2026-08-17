"""Mapa de compatibilidade ManimCE ↔ ManimGL, gerado por reflexão.

Serve para responder, sem chutar, a pergunta que mais quebra código de
agente: *"esse símbolo existe na versão que eu estou usando, e com a
mesma assinatura?"*
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = ["RENAMES", "build_diff", "write_diff"]


#: Renomeações e mudanças de fluxo entre os dois projetos.
#:
#: A coluna de existência é preenchida por reflexão em :func:`build_diff`,
#: então uma linha errada aqui aparece como ``—`` no relatório em vez de
#: virar afirmação falsa.
RENAMES: list[tuple[str, str, str]] = [
    ("ShowCreation", "Create", "renomeada na CE; `ShowCreation` não existe lá"),
    ("TexMobject", "MathTex", "LaTeX em modo matemático"),
    ("TextMobject", "Tex", "LaTeX em modo texto"),
    ("TexText", "Tex", "nome do 3b1b para texto LaTeX"),
    ("GraphScene", "Axes", "`GraphScene` foi removida da CE; use `Axes` numa `Scene`"),
    ("get_graph", "Axes.plot", "virou método do `Axes`"),
    ("get_graph_label", "Axes.get_graph_label", "método do `Axes`"),
    ("CONFIG = {...}", "argumentos de __init__", "a CE removeu os dicts `CONFIG`"),
    ("ApplyMethod(m.shift, UP)", "m.animate.shift(UP)", "sintaxe `.animate`"),
    ("self.play(m.shift, UP)", "self.play(m.animate.shift(UP))", "GL aceita método cru"),
    ("interactive_embed()", "--renderer=opengl", "fluxos interativos diferentes"),
    ("checkpoint_paste()", "(sem equivalente)", "recurso do fluxo pessoal do 3b1b"),
    ("Group", "Group / VGroup", "na CE, `VGroup` só aceita `VMobject`"),
    ("self.embed()", "(sem equivalente)", "REPL embutido do ManimGL"),
    ("Mobject.set_color", "Mobject.set_color", "existe nos dois; assinatura difere"),
]


def _load(path: str | Path) -> dict[str, Any]:
    """Lê o índice de API, aceitando ``.json`` ou ``.json.gz``.

    Decide pelo SUFIXO, não só por existência: o caminho recebido já pode
    ser o ``.gz``, e aí ``read_text`` estouraria com ``UnicodeDecodeError``
    ao tratar bytes comprimidos como UTF-8.
    """
    import gzip

    p = Path(path)

    def read(target: Path) -> dict[str, Any]:
        if target.suffix == ".gz":
            with gzip.open(target, "rt", encoding="utf-8") as fh:
                return json.load(fh)
        return json.loads(target.read_text(encoding="utf-8"))

    if p.exists():
        return read(p)

    # Aceita tanto "passei .json e só existe .json.gz" quanto o inverso.
    alt = (
        p.with_suffix("") if p.suffix == ".gz" else Path(str(p) + ".gz")
    )
    if alt.exists():
        return read(alt)

    raise FileNotFoundError(
        f"nem {p.name} nem {alt.name} existem — rode `mx api-dump` antes."
    )


def _by_kind(data: dict[str, Any], kind: str) -> dict[str, dict[str, Any]]:
    return {s["name"]: s for s in data["symbols"].values() if s["kind"] == kind}


def build_diff(ce_path: str | Path, gl_path: str | Path) -> str:
    """Monta o markdown do mapa de compatibilidade."""
    ce, gl = _load(ce_path), _load(gl_path)
    ce_c, gl_c = _by_kind(ce, "class"), _by_kind(gl, "class")
    ce_f, gl_f = _by_kind(ce, "function"), _by_kind(gl, "function")

    only_ce = sorted(set(ce_c) - set(gl_c))
    only_gl = sorted(set(gl_c) - set(ce_c))
    common = sorted(set(ce_c) & set(gl_c))

    ce_all = set(ce_c) | set(ce_f)
    gl_all = set(gl_c) | set(gl_f)

    lines: list[str] = [
        f"# ManimCE v{ce['version']} × ManimGL v{gl['version']}",
        "",
        "Mapa de compatibilidade gerado por reflexão dos dois pacotes "
        "instalados (`mx api-diff`) — não escrito à mão, não copiado de blog.",
        "",
        "## Resumo",
        "",
        "| | ManimCE | ManimGL |",
        "|---|---:|---:|",
        "| import | `from manim import *` | `from manimlib import *` |",
        "| CLI | `manim` | `manimgl` |",
        f"| classes públicas | {len(ce_c)} | {len(gl_c)} |",
        f"| funções públicas | {len(ce_f)} | {len(gl_f)} |",
        f"| classes só nesta edição | {len(only_ce)} | {len(only_gl)} |",
        f"| classes com nome em comum | {len(common)} | {len(common)} |",
        "",
        "> **Os dois não são compatíveis no nível de código-fonte.** "
        "Um script escrito para um não roda no outro sem tradução.",
        "",
        "## Renomeações e mudanças de fluxo",
        "",
        "Coluna de existência verificada contra os pacotes instalados: "
        "`✓` existe, `—` não existe.",
        "",
        "| ManimGL (3b1b) | existe? | ManimCE | existe? | observação |",
        "|---|:-:|---|:-:|---|",
    ]

    def exists(expr: str, universe: set[str]) -> str:
        token = expr.split("(")[0].split(".")[0].split(" ")[0].strip()
        return "✓" if token in universe else "—"

    for gl_name, ce_name, note in RENAMES:
        lines.append(
            f"| `{gl_name}` | {exists(gl_name, gl_all)} "
            f"| `{ce_name}` | {exists(ce_name, ce_all)} | {note} |"
        )

    def block(title: str, names: list[str]) -> list[str]:
        out = ["", f"## {title} ({len(names)})", ""]
        if not names:
            out.append("_(nenhuma)_")
            return out
        out.append("```")
        for i in range(0, len(names), 6):
            out.append(", ".join(names[i : i + 6]))
        out.append("```")
        return out

    lines += block("Classes só no ManimCE", only_ce)
    lines += block("Classes só no ManimGL", only_gl)

    diffs = [
        (n, ce_c[n].get("signature") or "", gl_c[n].get("signature") or "")
        for n in common
        if ce_c[n].get("signature") != gl_c[n].get("signature")
    ]
    lines += [
        "",
        f"## Nome igual, assinatura diferente ({len(diffs)} de {len(common)})",
        "",
        "Esta é a armadilha silenciosa: o import funciona, o construtor aceita, "
        "e o resultado sai errado.",
        "",
        "| classe | assinatura CE | assinatura GL |",
        "|---|---|---|",
    ]
    for name, a, b in diffs[:80]:
        lines.append(f"| `{name}` | `{a[:100]}` | `{b[:100]}` |")
    if len(diffs) > 80:
        lines.append("")
        lines.append(f"_… e mais {len(diffs) - 80}. Veja `api/*-index.tsv` para a lista completa._")

    lines.append("")
    return "\n".join(lines) + "\n"


def write_diff(
    ce_path: str | Path,
    gl_path: str | Path,
    out_path: str | Path,
) -> Path:
    """Escreve o mapa de compatibilidade e devolve o caminho."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_diff(ce_path, gl_path), encoding="utf-8")
    return out
