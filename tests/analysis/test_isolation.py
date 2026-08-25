"""Structural isolation checks across the RQ1-RQ5 analysis package.

Same AST-level technique `tests/annotation/test_access_separation.py`
already used for the P4 interface: checking that a forbidden import or
reference is structurally absent, not just that today's tests happen
not to exercise it.
"""

from __future__ import annotations

import ast
import inspect
from pathlib import Path

import alcsm.analysis as analysis_pkg


def _module_files() -> list[Path]:
    pkg_dir = Path(inspect.getfile(analysis_pkg)).parent
    return sorted(pkg_dir.glob("*.py"))


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
    return names


def test_rq4_module_is_the_only_one_importing_impact_indicator_shaped_data() -> None:
    for path in _module_files():
        if path.stem == "rq4":
            continue
        imports = _imports(path)
        assert not any(
            "rq4" in i.lower() for i in imports
        ), f"{path.name} imports something rq4-related: {imports}"


def test_rq4_module_imports_nothing_from_sibling_rq_modules() -> None:
    imports = _imports(Path(inspect.getfile(analysis_pkg)).parent / "rq4.py")
    sibling_modules = {"rq1_descriptive", "gap", "rq3_validation", "survey"}
    assert not any(
        i.startswith("alcsm.analysis.") and i.split(".")[-1] in sibling_modules
        for i in imports
    )


def test_no_analysis_module_computes_a_composite_score() -> None:
    """This task's explicit "do not calculate final composite score /
    invent weights" -- checked as a source-level absence, not just an
    absent test case."""
    forbidden_identifiers = ("alcsm_total", "composite_score", "weighted_sum")
    for path in _module_files():
        source = path.read_text(encoding="utf-8").lower()
        for term in forbidden_identifiers:
            assert term not in source, f"{path.name} contains forbidden term {term!r}"


def test_no_analysis_module_writes_to_the_review_workbook_or_processed_sources() -> (
    None
):
    """Every loader in `data_sources.py` is read-only (`pd.read_excel`
    only); no module anywhere in this package calls `to_excel` on a
    real-data path -- this task's "do not overwrite first-pass
    annotations" rule, checked structurally."""
    for path in _module_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute) and node.attr == "to_excel":
                raise AssertionError(
                    f"{path.name} calls .to_excel() -- analysis must be read-only"
                )


def test_gap_module_never_reads_job_requirement_scores_as_if_profile_scores() -> None:
    """RQ2's own explicit rule: "keep requirement-side and profile-side
    scoring conceptually distinct" -- checked by requiring the two
    input parameter names in `dimension_gap_from_scores` to stay
    distinct (`required_scores` vs `held_scores`), never a single
    unified `scores` parameter that could blur the two."""
    from alcsm.analysis.gap import dimension_gap_from_scores

    sig = inspect.signature(dimension_gap_from_scores)
    assert "required_scores" in sig.parameters
    assert "held_scores" in sig.parameters
    assert "scores" not in sig.parameters
