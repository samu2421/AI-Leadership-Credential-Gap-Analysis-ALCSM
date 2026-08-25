"""Reliability data structures and export views: Rater A/B/Adjudicator,
reading through v_reliability_input, never computing alpha itself
(that stays Phase P5's job).
"""

from __future__ import annotations

from datetime import datetime

import psycopg2
from sqlalchemy.orm import Session

from alcsm.annotation.models import AnnotationScore
from alcsm.annotation.reliability_export import (
    build_rater_comparison_view,
    build_reliability_export_rows,
    group_by_dimension,
)
from alcsm.annotation.store import insert_adjudication, insert_annotation_score

_NOW = datetime.now()


def _score(
    profile_id: str, dimension_number: int, rater_id: str, score: int
) -> AnnotationScore:
    return AnnotationScore(
        profile_id=profile_id,
        dimension_number=dimension_number,
        rater_id=rater_id,
        score=score,
        missing_status="present",
        rulebook_version="1.0",
        coding_ts=_NOW,
        evidence_text="fixture evidence",
    )


def test_export_rows_include_independent_rater_submissions(
    db_connection: psycopg2.extensions.connection,
    inserted_profile_id: str,
    sqlalchemy_session: Session,
) -> None:
    insert_annotation_score(db_connection, _score(inserted_profile_id, 1, "RATER_A", 3))
    insert_annotation_score(db_connection, _score(inserted_profile_id, 1, "RATER_B", 4))

    rows = build_reliability_export_rows(sqlalchemy_session)
    matching = [
        r for r in rows if r.unit_id == inserted_profile_id and r.dimension_number == 1
    ]
    assert {r.rater_id for r in matching} == {"RATER_A", "RATER_B"}
    assert {r.score for r in matching} == {3, 4}


def test_export_rows_exclude_adjudicated_rows(
    db_connection: psycopg2.extensions.connection,
    inserted_profile_id: str,
    sqlalchemy_session: Session,
) -> None:
    """v_reliability_input's own [F] comment: adjudicated rows are
    excluded, or agreement would be inflated artificially."""
    insert_annotation_score(db_connection, _score(inserted_profile_id, 2, "RATER_A", 2))
    insert_annotation_score(db_connection, _score(inserted_profile_id, 2, "RATER_B", 5))
    insert_adjudication(db_connection, _score(inserted_profile_id, 2, "RATER_A", 3))

    rows = build_reliability_export_rows(sqlalchemy_session)
    matching = [
        r for r in rows if r.unit_id == inserted_profile_id and r.dimension_number == 2
    ]
    assert len(matching) == 2
    assert all(r.rater_id != "ADJUDICATOR" for r in matching)


def test_group_by_dimension_never_pools_dimensions(
    db_connection: psycopg2.extensions.connection,
    inserted_profile_id: str,
    sqlalchemy_session: Session,
) -> None:
    insert_annotation_score(db_connection, _score(inserted_profile_id, 1, "RATER_A", 3))
    insert_annotation_score(db_connection, _score(inserted_profile_id, 6, "RATER_A", 5))

    rows = build_reliability_export_rows(sqlalchemy_session)
    grouped = group_by_dimension(rows)
    for dim, dim_rows in grouped.items():
        assert all(r.dimension_number == dim for r in dim_rows)


def test_this_module_never_computes_an_alpha_value() -> None:
    """Structural guard: reliability_export.py must not import or call
    anything from reliability/krippendorff.py -- shaping data and
    computing a statistic are two different phases (P4 vs P5). Checks
    live imports/calls only; the module's own docstring is allowed to
    explain the boundary in prose using the word "krippendorff"."""
    import ast
    import inspect

    from alcsm.annotation import reliability_export

    tree = ast.parse(inspect.getsource(reliability_export))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert "krippendorff" not in node.module.lower()
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert "krippendorff" not in alias.name.lower()
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "compute_alpha_for_dimension"


class TestRaterComparisonView:
    def test_shows_none_for_a_rater_that_has_not_submitted(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 3, "RATER_A", 2)
        )
        rows = build_rater_comparison_view(db_connection, [inserted_profile_id], [3])
        assert len(rows) == 1
        assert rows[0].rater_a_score == 2
        assert rows[0].rater_b_score is None
        assert rows[0].adjudicator_score is None

    def test_shows_all_three_once_present(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 4, "RATER_A", 2)
        )
        insert_annotation_score(
            db_connection, _score(inserted_profile_id, 4, "RATER_B", 3)
        )
        insert_adjudication(db_connection, _score(inserted_profile_id, 4, "RATER_A", 3))
        rows = build_rater_comparison_view(db_connection, [inserted_profile_id], [4])
        assert rows[0].rater_a_score == 2
        assert rows[0].rater_b_score == 3
        assert rows[0].adjudicator_score == 3

    def test_does_not_raise_or_block_when_nothing_submitted_yet(
        self, db_connection: psycopg2.extensions.connection, inserted_profile_id: str
    ) -> None:
        rows = build_rater_comparison_view(db_connection, [inserted_profile_id], [5])
        assert rows[0].rater_a_score is None
        assert rows[0].rater_b_score is None
