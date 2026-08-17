"""Extração da superfície de API **completa** do Manim.

Motivação
---------
Um agente de código não consegue "lembrar" da API do Manim inteira, e a
documentação online fica atrás da versão instalada. Este módulo varre o
pacote instalado por reflexão e gera índices consultáveis:

* ``api/<pkg>-api.json.gz``     — tudo, estruturado. **Comprimido**: é lido
  por programa (``mx find`` / ``mx show``), nunca por ``grep``, e o JSON cru
  passa de 14 MiB.
* ``api/<pkg>-index.tsv``       — 1 símbolo por linha, ótimo para ``grep``
* ``api/<pkg>-methods.tsv``     — 1 método por linha, com assinatura
* ``api/<pkg>-toplevel.md``     — tudo que ``from <pkg> import *`` traz
* ``api/<pkg>-by-category.md``  — navegação humana/agente por categoria
* ``api/<pkg>-inheritance.txt`` — árvore de herança dos Mobjects/Animations

Os ``.tsv``/``.md`` ficam em texto puro justamente porque existem para
serem grepados.

A fonte da verdade é sempre o pacote instalado, não um snapshot escrito
à mão. Regenere com ``mx api-dump`` depois de atualizar o Manim.
"""

from __future__ import annotations

import dataclasses
import importlib
import inspect
import json
import logging
import pkgutil
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

logger = logging.getLogger("manimx.introspect")

__all__ = [
    "SymbolInfo",
    "walk_package",
    "collect_api",
    "dump_api",
    "categorize",
    "search",
]


@dataclasses.dataclass
class SymbolInfo:
    """Um símbolo público do Manim."""

    name: str
    kind: str  # class | function | constant | module
    module: str
    qualname: str
    signature: str | None = None
    doc: str | None = None
    bases: list[str] = dataclasses.field(default_factory=list)
    methods: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    properties: list[str] = dataclasses.field(default_factory=list)
    category: str = "other"
    value_repr: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


# --------------------------------------------------------------------------
# Categorização
# --------------------------------------------------------------------------

#: Prefixo de módulo -> categoria. A primeira correspondência mais longa vence.
_CATEGORY_BY_MODULE: dict[str, str] = {
    "manim.mobject.geometry": "mobject/geometry",
    "manim.mobject.graphing": "mobject/graphing",
    "manim.mobject.text": "mobject/text",
    "manim.mobject.svg": "mobject/svg",
    "manim.mobject.three_d": "mobject/3d",
    "manim.mobject.matrix": "mobject/matrix",
    "manim.mobject.table": "mobject/table",
    "manim.mobject.graph": "mobject/graph",
    "manim.mobject.logo": "mobject/logo",
    "manim.mobject.value_tracker": "mobject/value_tracker",
    "manim.mobject.vector_field": "mobject/vector_field",
    "manim.mobject.opengl": "mobject/opengl",
    "manim.mobject": "mobject/core",
    "manim.animation.transform_matching_parts": "animation/transform",
    "manim.animation.transform": "animation/transform",
    "manim.animation.creation": "animation/creation",
    "manim.animation.fading": "animation/fading",
    "manim.animation.growing": "animation/growing",
    "manim.animation.indication": "animation/indication",
    "manim.animation.movement": "animation/movement",
    "manim.animation.rotation": "animation/rotation",
    "manim.animation.composition": "animation/composition",
    "manim.animation.changing": "animation/changing",
    "manim.animation.numbers": "animation/numbers",
    "manim.animation.specialized": "animation/specialized",
    "manim.animation.updaters": "animation/updaters",
    "manim.animation.speedmodifier": "animation/speed",
    "manim.animation": "animation/core",
    "manim.scene": "scene",
    "manim.camera": "camera",
    "manim.renderer": "renderer",
    "manim.utils.rate_functions": "utils/rate_functions",
    "manim.utils.color": "utils/color",
    "manim.utils.space_ops": "utils/space_ops",
    "manim.utils.bezier": "utils/bezier",
    "manim.utils.tex": "utils/tex",
    "manim.utils": "utils/other",
    "manim.constants": "constants",
    "manim._config": "config",
    "manim.typing": "typing",
    "manim.plugins": "plugins",
}


def categorize(module_name: str) -> str:
    """Mapeia um nome de módulo do Manim para uma categoria legível."""
    best, best_len = "other", -1
    for prefix, cat in _CATEGORY_BY_MODULE.items():
        if module_name.startswith(prefix) and len(prefix) > best_len:
            best, best_len = cat, len(prefix)
    return best


# --------------------------------------------------------------------------
# Varredura
# --------------------------------------------------------------------------


def walk_package(package_name: str = "manim") -> Iterator[Any]:
    """Importa recursivamente todos os submódulos de um pacote."""
    try:
        root = importlib.import_module(package_name)
    except Exception as exc:
        logger.error("não consegui importar %s: %s", package_name, exc)
        return
    yield root

    paths = getattr(root, "__path__", None)
    if not paths:
        return

    for mod_info in pkgutil.walk_packages(paths, prefix=f"{package_name}."):
        name = mod_info.name
        # Módulos que abrem janela/GL ou dependem de extras opcionais.
        if any(s in name for s in (".opengl_", "dearpygui", ".cairo_")):
            pass  # ainda tentamos; falha é capturada abaixo
        try:
            yield importlib.import_module(name)
        except BaseException as exc:  # noqa: BLE001
            logger.debug("pulei %s: %s: %s", name, type(exc).__name__, exc)


def _safe_signature(obj: Any) -> str | None:
    """Assinatura como texto, com caminhos locais já saneados.

    Um valor padrão pode ser um ``Path`` apontando para dentro do venv
    (é o caso de algumas constantes do Manim), e isso apareceria no
    índice publicado com o nome de usuário da máquina. Hoje nenhum
    símbolo cai nesse caso, mas a varredura é barata e evita que uma
    versão futura reintroduza o vazamento sem ninguém perceber.
    """
    try:
        text = str(inspect.signature(obj))
    except (TypeError, ValueError):
        return None
    return _scrub_paths(text)


def _first_doc_line(obj: Any) -> str | None:
    doc = inspect.getdoc(obj)
    if not doc:
        return None
    for line in doc.splitlines():
        line = line.strip()
        if line:
            return line
    return None


def _class_members(cls: type) -> tuple[list[dict[str, Any]], list[str]]:
    """Métodos (com assinatura e origem) e propriedades de uma classe."""
    methods: list[dict[str, Any]] = []
    properties: list[str] = []

    for name, member in inspect.getmembers(cls):
        if name.startswith("_") and not (name.startswith("__") and name.endswith("__")):
            continue
        if name.startswith("__") and name not in ("__init__", "__call__"):
            continue

        if isinstance(member, property):
            properties.append(name)
            continue
        if isinstance(inspect.getattr_static(cls, name, None), (staticmethod, classmethod)):
            kind = "staticmethod" if isinstance(
                inspect.getattr_static(cls, name, None), staticmethod
            ) else "classmethod"
        elif inspect.isroutine(member):
            kind = "method"
        else:
            continue

        # Onde o método foi definido de fato (herança).
        owner = cls.__name__
        for klass in cls.__mro__:
            if name in vars(klass):
                owner = klass.__name__
                break

        methods.append(
            {
                "name": name,
                "kind": kind,
                "signature": _safe_signature(member),
                "doc": _first_doc_line(member),
                "defined_in": owner,
                "inherited": owner != cls.__name__,
            }
        )
    methods.sort(key=lambda m: (m["inherited"], m["name"]))
    return methods, sorted(properties)


def collect_api(
    package_name: str = "manim",
    *,
    include_inherited_methods: bool = True,
    top_level_only: bool = False,
) -> dict[str, SymbolInfo]:
    """Varre o pacote e devolve ``{qualname: SymbolInfo}``.

    Parameters
    ----------
    include_inherited_methods
        Se ``False``, lista só os métodos definidos na própria classe.
        Manter ``True`` é o que dá o "acesso a TODOS os métodos", já que
        boa parte da API de um ``Mobject`` vem de ``Mobject``/``VMobject``.
    top_level_only
        Se ``True``, indexa só o que ``from manim import *`` traz.
    """
    symbols: dict[str, SymbolInfo] = {}
    root = importlib.import_module(package_name)
    top_level_names = {n for n in dir(root) if not n.startswith("_")}

    modules = [root] if top_level_only else list(walk_package(package_name))

    for module in modules:
        mod_name = module.__name__
        for name, obj in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if top_level_only and name not in top_level_names:
                continue

            # Só o que pertence ao pacote (evita reexports do numpy etc.).
            obj_module = getattr(obj, "__module__", None)
            if inspect.isclass(obj) or inspect.isfunction(obj):
                if not obj_module or not obj_module.startswith(package_name):
                    continue
                qualname = f"{obj_module}.{name}"
            else:
                qualname = f"{mod_name}.{name}"

            if qualname in symbols:
                continue

            if inspect.isclass(obj):
                methods, properties = _class_members(obj)
                if not include_inherited_methods:
                    methods = [m for m in methods if not m["inherited"]]
                symbols[qualname] = SymbolInfo(
                    name=name,
                    kind="class",
                    module=obj_module or mod_name,
                    qualname=qualname,
                    signature=_safe_signature(obj),
                    doc=_first_doc_line(obj),
                    bases=[b.__name__ for b in obj.__bases__ if b is not object],
                    methods=methods,
                    properties=properties,
                    category=categorize(obj_module or mod_name),
                )
            elif inspect.isfunction(obj):
                symbols[qualname] = SymbolInfo(
                    name=name,
                    kind="function",
                    module=obj_module or mod_name,
                    qualname=qualname,
                    signature=_safe_signature(obj),
                    doc=_first_doc_line(obj),
                    category=categorize(obj_module or mod_name),
                )
            elif not inspect.ismodule(obj) and not callable(obj):
                if name.isupper() or _looks_like_color(obj):
                    symbols[qualname] = SymbolInfo(
                        name=name,
                        kind="constant",
                        module=mod_name,
                        qualname=qualname,
                        category=categorize(mod_name),
                        value_repr=_short_repr(obj),
                    )
    return symbols


def _looks_like_color(obj: Any) -> bool:
    return type(obj).__name__ in ("ManimColor", "Color")


def _machine_paths() -> list[tuple[str, str]]:
    """Prefixos de caminho local -> marcador portátil.

    Constantes como ``MANIM_ROOT`` e ``SHADER_FOLDER`` têm ``PosixPath``
    apontando para dentro do venv. Publicar isso vazaria o nome de usuário
    da máquina e não diria nada a quem clonou — o caminho dele é outro.
    Do mais longo para o mais curto, para o prefixo mais específico vencer.
    """
    import site
    import sysconfig

    candidates: list[tuple[str, str]] = []
    for path in filter(None, (sysconfig.get_paths().get("purelib"),
                              sysconfig.get_paths().get("platlib"))):
        candidates.append((path, "<site-packages>"))
    for path in (getattr(site, "getsitepackages", lambda: [])() or []):
        candidates.append((path, "<site-packages>"))
    candidates.append((str(Path(__file__).resolve().parent.parent), "<repo>"))
    candidates.append((str(Path.home()), "<home>"))
    return sorted(set(candidates), key=lambda c: -len(c[0]))


_PATH_REWRITES = _machine_paths()


def _scrub_paths(text: str) -> str:
    """Troca caminhos desta máquina por marcadores portáteis."""
    for prefix, marker in _PATH_REWRITES:
        if prefix and prefix in text:
            text = text.replace(prefix, marker)
    return text


def _short_repr(obj: Any, limit: int = 120) -> str:
    try:
        text = repr(obj)
    except Exception:
        return "<repr falhou>"
    text = _scrub_paths(text)
    return text if len(text) <= limit else text[: limit - 3] + "..."


# --------------------------------------------------------------------------
# Busca
# --------------------------------------------------------------------------


def search(
    symbols: dict[str, SymbolInfo],
    query: str,
    *,
    kind: str | None = None,
    category: str | None = None,
    include_methods: bool = True,
    limit: int = 50,
) -> list[str]:
    """Busca por substring em nomes, docs e nomes de métodos."""
    q = query.lower()
    hits: list[tuple[int, str]] = []

    for qualname, sym in symbols.items():
        if kind and sym.kind != kind:
            continue
        if category and not sym.category.startswith(category):
            continue

        score = None
        if sym.name.lower() == q:
            score = 0
        elif sym.name.lower().startswith(q):
            score = 1
        elif q in sym.name.lower():
            score = 2
        elif sym.doc and q in sym.doc.lower():
            score = 3
        elif include_methods and any(q in m["name"].lower() for m in sym.methods):
            score = 4

        if score is not None:
            hits.append((score, qualname))

    hits.sort(key=lambda h: (h[0], h[1]))
    return [q for _, q in hits[:limit]]


# --------------------------------------------------------------------------
# Escrita dos índices
# --------------------------------------------------------------------------


def dump_api(
    out_dir: str | Path = "api",
    package_name: str = "manim",
    *,
    label: str | None = None,
) -> dict[str, Path]:
    """Gera todos os índices de API em ``out_dir``.

    Returns
    -------
    dict
        ``{nome_lógico: caminho}`` de cada arquivo escrito.
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    prefix = label or package_name

    try:
        version = getattr(importlib.import_module(package_name), "__version__", "?")
    except Exception:
        version = "?"

    logger.info("varrendo %s ...", package_name)
    symbols = collect_api(package_name)
    logger.info("%d símbolos encontrados", len(symbols))

    written: dict[str, Path] = {}

    # --- JSON completo -----------------------------------------------------
    payload = {
        "package": package_name,
        "version": version,
        "python": sys.version.split()[0],
        "symbol_count": len(symbols),
        "method_count": sum(len(s.methods) for s in symbols.values()),
        "symbols": {k: v.as_dict() for k, v in sorted(symbols.items())},
    }
    # Gravado comprimido: o JSON cru passa de 14 MiB e comprime ~90%, e
    # este arquivo é lido por programa (`mx find`/`mx show`), nunca por
    # `grep`. Os índices .tsv/.md, que existem justamente para serem
    # grepados, seguem em texto puro.
    import gzip

    p = out / f"{prefix}-api.json.gz"
    with gzip.open(p, "wt", encoding="utf-8", compresslevel=9) as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
    written["json"] = p
    # Um dump cru anterior teria precedência na leitura e ficaria velho.
    stale = out / f"{prefix}-api.json"
    if stale.exists():
        stale.unlink()

    # --- TSV de símbolos (grep-friendly) -----------------------------------
    lines = ["kind\tname\tcategory\tsignature\tmodule\tdoc"]
    for sym in sorted(symbols.values(), key=lambda s: (s.category, s.name)):
        doc = (sym.doc or "").replace("\t", " ").replace("\n", " ")
        sig = (sym.signature or sym.value_repr or "").replace("\t", " ")
        lines.append(
            f"{sym.kind}\t{sym.name}\t{sym.category}\t{sig}\t{sym.module}\t{doc}"
        )
    p = out / f"{prefix}-index.tsv"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    written["index"] = p

    # --- TSV de métodos ----------------------------------------------------
    mlines = ["class\tmethod\tkind\tdefined_in\tinherited\tsignature\tdoc"]
    for sym in sorted(symbols.values(), key=lambda s: s.name):
        if sym.kind != "class":
            continue
        for m in sym.methods:
            doc = (m.get("doc") or "").replace("\t", " ").replace("\n", " ")
            sig = (m.get("signature") or "").replace("\t", " ")
            mlines.append(
                f"{sym.name}\t{m['name']}\t{m['kind']}\t{m['defined_in']}\t"
                f"{int(bool(m['inherited']))}\t{sig}\t{doc}"
            )
    p = out / f"{prefix}-methods.tsv"
    p.write_text("\n".join(mlines) + "\n", encoding="utf-8")
    written["methods"] = p

    # --- Markdown por categoria -------------------------------------------
    by_cat: dict[str, list[SymbolInfo]] = {}
    for sym in symbols.values():
        by_cat.setdefault(sym.category, []).append(sym)

    md = [
        f"# API de `{package_name}` v{version}",
        "",
        f"{len(symbols)} símbolos públicos · "
        f"{payload['method_count']} métodos indexados · "
        f"Python {payload['python']}",
        "",
        "Gerado por `mx api-dump` a partir do pacote instalado. "
        "Regenere após atualizar o Manim.",
        "",
        "## Categorias",
        "",
    ]
    for cat in sorted(by_cat):
        md.append(f"- [`{cat}`](#{cat.replace('/', '')}) — {len(by_cat[cat])} símbolos")
    md.append("")

    for cat in sorted(by_cat):
        md.append(f"## {cat}")
        md.append("")
        entries = sorted(by_cat[cat], key=lambda s: (s.kind, s.name))
        for sym in entries:
            if sym.kind == "class":
                bases = f" ← {', '.join(sym.bases)}" if sym.bases else ""
                md.append(f"### `{sym.name}{sym.signature or '()'}`{bases}")
                if sym.doc:
                    md.append(f"> {sym.doc}")
                own = [m for m in sym.methods if not m["inherited"]]
                if own:
                    md.append("")
                    md.append("<details><summary>métodos próprios "
                              f"({len(own)}) · herdados: "
                              f"{len(sym.methods) - len(own)}</summary>")
                    md.append("")
                    for m in own:
                        md.append(f"- `{m['name']}{m['signature'] or '()'}`"
                                  + (f" — {m['doc']}" if m["doc"] else ""))
                    md.append("")
                    md.append("</details>")
                md.append("")
            elif sym.kind == "function":
                md.append(f"- **`{sym.name}{sym.signature or '()'}`**"
                          + (f" — {sym.doc}" if sym.doc else ""))
            else:
                md.append(f"- `{sym.name}` = `{sym.value_repr}`")
        md.append("")

    p = out / f"{prefix}-by-category.md"
    p.write_text("\n".join(md) + "\n", encoding="utf-8")
    written["by_category"] = p

    # --- Árvore de herança -------------------------------------------------
    children: dict[str, list[str]] = {}
    known = {s.name for s in symbols.values() if s.kind == "class"}
    for sym in symbols.values():
        if sym.kind != "class":
            continue
        for base in sym.bases or ["(raiz)"]:
            children.setdefault(base if base in known else "(raiz)", []).append(sym.name)

    tree: list[str] = [f"Árvore de herança — {package_name} v{version}", ""]
    seen: set[str] = set()

    def emit(node: str, depth: int) -> None:
        if depth > 12 or node in seen:
            return
        seen.add(node)
        tree.append("  " * depth + node)
        for child in sorted(set(children.get(node, []))):
            if child != node:
                emit(child, depth + 1)

    for root_name in sorted(set(children.get("(raiz)", []))):
        emit(root_name, 0)
    p = out / f"{prefix}-inheritance.txt"
    p.write_text("\n".join(tree) + "\n", encoding="utf-8")
    written["inheritance"] = p

    # --- Namespace de topo (`from <pkg> import *`) -------------------------
    # Garantia de completude: qualquer nome exposto no topo aparece aqui,
    # inclusive submódulos, instâncias e aliases de tipo que a varredura por
    # reflexão de classes/funções não captura.
    tl_lines = [f"# `from {package_name} import *` — v{version}", ""]
    indexed_names = {s.name for s in symbols.values()}
    groups: dict[str, list[str]] = {}
    pkg_root = importlib.import_module(package_name)
    for name in sorted(n for n in dir(pkg_root) if not n.startswith("_")):
        obj = getattr(pkg_root, name, None)
        if inspect.ismodule(obj):
            group = "submódulo / paleta"
            detail = getattr(obj, "__name__", "")
        elif inspect.isclass(obj):
            group = "classe"
            detail = f"{obj.__module__}.{obj.__qualname__}"
        elif inspect.isroutine(obj):
            group = "função"
            detail = _safe_signature(obj) or ""
        elif _looks_like_color(obj):
            group = "cor"
            detail = _short_repr(obj)
        else:
            group = "constante / instância"
            detail = f"{type(obj).__name__} = {_short_repr(obj, 60)}"
        flag = "" if name in indexed_names else "  [só no topo]"
        groups.setdefault(group, []).append(f"- `{name}` — {detail}{flag}")

    for group in sorted(groups):
        tl_lines.append(f"## {group} ({len(groups[group])})")
        tl_lines.append("")
        tl_lines.extend(groups[group])
        tl_lines.append("")
    p = out / f"{prefix}-toplevel.md"
    p.write_text("\n".join(tl_lines) + "\n", encoding="utf-8")
    written["toplevel"] = p

    return written
