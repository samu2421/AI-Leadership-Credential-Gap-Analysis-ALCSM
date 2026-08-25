"""Data structures and export views preparing for P5 reliability analysis.

Scope, per this task: "Prepare data structures and export views for
Rater A / Rater B / Adjudicator. Support per-dimension Krippendorff's
alpha analysis later. Do not calculate or interpret final reliability
yet." This module shapes and exports rows -- it never computes alpha,
percentage agreement, or any other reliability statistic. That
remains :mod:`alcsm.reliability.krippendorff`'s job, entirely
unimplemented here (Phase P5, gated on P4 pilot data existing).

Reads exclusively through ``v_reliability_input`` (via
:func:`alcsm.db.queries.fetch_reliability_input`), never the base
``alcsm_dimension_score`` table directly -- the view already excludes
adjudicated rows and non-primary/secondary raters, which is exactly
the "never pool dimensions, never use adjudicated rows" rule P5 must
follow (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §6, §15).
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from psycopg2.extensions import connection as PGConnection
from sqlalchemy.orm import Session

from alcsm.annotation.store import fetch_both_rater_scores_for_adjudication
from alcsm.db.queries import fetch_reliability_input


@dataclass(frozen=True)
class ReliabilityInputRow:
    """One row of ``v_reliability_input``, typed for downstream use."""

    unit_id: str  # profile_id or posting_id
    corpus: str  # 'profile' or 'job_posting'
    dimension_number: int
    rater_id: str
    score: int
    rulebook_version: str


def build_reliability_export_rows(session: Session) -> list[ReliabilityInputRow]:
    """Long-format export of every pre-adjudication, independent-rater row.

    Thin typed wrapper over :func:`alcsm.db.queries.fetch_reliability_input`
    -- this is the "export view" the P5 alpha computation will read
    from later; it is deliberately dumb (no grouping, no statistics).
    """
    raw_rows = fetch_reliability_input(session)
    return [
        ReliabilityInputRow(
            unit_id=r.unit_id,
            corpus=r.corpus,
            dimension_number=r.dimension_number,
            rater_id=r.rater_id,
            score=r.score,
            rulebook_version=r.rulebook_version,
        )
        for r in raw_rows
    ]


def group_by_dimension(
    rows: list[ReliabilityInputRow],
) -> dict[int, list[ReliabilityInputRow]]:
    """Split export rows by dimension_number.

    P5's alpha computation must run separately per dimension, never
    pooled (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §15) -- this grouping
    is the structural precondition for that, not the computation
    itself.
    """
    grouped: dict[int, list[ReliabilityInputRow]] = defaultdict(list)
    for row in rows:
        grouped[row.dimension_number].append(row)
    return dict(grouped)


@dataclass(frozen=True)
class RaterComparisonRow:
    """Wide, human-readable view: one profile x dimension, all raters side by side.

    For export/inspection only -- explicitly not an input to any
    reliability statistic (that reads the long-format
    :class:`ReliabilityInputRow` rows above, through the view, per the
    frozen rule). Useful for a researcher preparing an adjudication
    session, or for a CSV a supervisor can read directly.
    """

    profile_id: str
    dimension_number: int
    rater_a_score: int | None
    rater_b_score: int | None
    adjudicator_score: int | None


def build_rater_comparison_view(
    conn: PGConnection, profile_ids: list[str], dimension_numbers: list[int]
) -> list[RaterComparisonRow]:
    """Build a Rater A / Rater B / Adjudicator wide comparison for export.

    Intended for use once both raters have submitted (see
    :func:`alcsm.annotation.store.has_other_rater_submitted`) -- calling
    this earlier simply yields ``None`` for whichever rater has not
    submitted yet; it never blocks or raises, since "not yet submitted"
    is a legitimate, common state, not an error.
    """
    out: list[RaterComparisonRow] = []
    for profile_id in profile_ids:
        for dimension_number in dimension_numbers:
            scores = fetch_both_rater_scores_for_adjudication(
                conn, profile_id, dimension_number
            )
            by_rater = {s.rater_id: s.score for s in scores}
            adjudicator_scores = [
                s.score
                for s in _fetch_adjudication_only(conn, profile_id, dimension_number)
            ]
            out.append(
                RaterComparisonRow(
                    profile_id=profile_id,
                    dimension_number=dimension_number,
                    rater_a_score=by_rater.get("RATER_A"),
                    rater_b_score=by_rater.get("RATER_B"),
                    adjudicator_score=(
                        adjudicator_scores[0] if adjudicator_scores else None
                    ),
                )
            )
    return out


def _fetch_adjudication_only(
    conn: PGConnection, profile_id: str, dimension_number: int
) -> list:
    """Local helper: the one adjudication row, if any, for a profile x dimension."""
    from alcsm.annotation.models import AnnotationScore
    from alcsm.annotation.store import (
        _COLUMNS,
    )  # noqa: PLC0415 (avoid import cycle at module load)

    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT {", ".join(_COLUMNS)}
            FROM alcsm.alcsm_dimension_score
            WHERE profile_id = %s AND dimension_number = %s
              AND is_adjudication = TRUE;
            """,
            (profile_id, dimension_number),
        )
        rows = cur.fetchall()
        return [
            AnnotationScore(**dict(zip(_COLUMNS, row, strict=True))) for row in rows
        ]
    finally:
        cur.close()
