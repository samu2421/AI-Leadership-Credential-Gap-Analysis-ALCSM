"""Access separation between RQ4 criteria and annotation (frozen
constraint #2, PROJECT_CONTEXT.md §11: "Never display the RQ4 impact
values during scoring").

These are structural/static checks over the annotation package's own
source, not behavioural tests against a running UI (that would only
prove "the UI I built doesn't show it today", not "nothing in this
package can"). A source-level absence check is a stronger guarantee
here: it fails the moment anyone imports `rq4_impact_indicator` or
`alcsm.analysis.rq4` into the annotation path at all, not just when a
specific screen happens to render it.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import alcsm.annotation as annotation_pkg
from alcsm.app import annotation_app

_FORBIDDEN_IDENTIFIERS = ("rq4_impact_indicator", "rq4", "Rq4Criterion")


def _module_files() -> list[Path]:
    pkg_dir = Path(inspect.getfile(annotation_pkg)).parent
    return sorted(pkg_dir.glob("*.py"))


def test_no_annotation_module_imports_rq4_analysis() -> None:
    for path in _module_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                assert "rq4" not in node.module.lower(), (
                    f"{path.name} imports from {node.module!r} -- RQ4 must "
                    "stay isolated from annotation (frozen constraint #2)"
                )
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert (
                        "rq4" not in alias.name.lower()
                    ), f"{path.name} imports {alias.name!r}"


def _docstring_and_comment_free_source(path: Path) -> str:
    """Strip docstrings (and, by using `ast.unparse`, comments) so a
    module's own prose explaining the isolation rule (which necessarily
    names what must NOT appear in live code) doesn't trip this check."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                node.body[0].value.value = ""
    return ast.unparse(tree)


def test_no_annotation_module_references_rq4_table_or_type_names_in_live_code() -> None:
    for path in _module_files():
        code_only = _docstring_and_comment_free_source(path)
        assert "rq4_impact_indicator" not in code_only, path.name
        assert "Rq4Criterion" not in code_only, path.name


def test_annotation_app_does_not_import_rq4() -> None:
    source = inspect.getsource(annotation_app)
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "rq4" not in node.module.lower()
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "rq4" not in alias.name.lower()


def test_annotation_app_does_not_render_rq4_values() -> None:
    source = inspect.getsource(annotation_app).lower()
    assert "rq4_network_reach" not in source
    assert "rq4_content_engagement" not in source
    assert "rq4_recognition_count" not in source
    assert "rq4_seniority_progression_rate" not in source


def test_annotation_score_dataclass_has_no_rq4_field() -> None:
    from dataclasses import fields

    from alcsm.annotation.models import AnnotationScore

    field_names = {f.name for f in fields(AnnotationScore)}
    assert not any("rq4" in name.lower() for name in field_names)
