"""Validated, atomic annotation-score writes and blinding-safe reads.

Mirrors ``collection/helper.py``'s pattern exactly (validate -> single
transaction -> commit or full rollback, PROJECT_CONTEXT.md §32) and
uses the same psycopg2 connection style. This is a NEW write path for
a table ``collection/helper.py`` never touches (``alcsm_dimension_
score``, not ``profile``/``job_posting``) -- it does not duplicate or
compete with the "single write path" collection/helper.py already
owns for collection data (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §8).

Rater blinding (frozen constraint #3, PROJECT_CONTEXT.md §11): this
module never exposes one rater's score to a caller asking on behalf of
another rater before both have submitted. ``fetch_rater_score`` is the
only read that returns a score value, and it is always scoped to the
exact ``rater_id`` asking for its own submission -- there is no
function anywhere in this module that returns "the other rater's
score". ``has_other_rater_submitted`` answers only a yes/no completion
question, never the value.
"""

from __future__ import annotations

from dataclasses import replace

import psycopg2
from psycopg2.extensions import connection as PGConnection

from alcsm.annotation.models import AnnotationScore
from alcsm.annotation.validation import (
    AnnotationValidationError,
    validate_annotation_score,
)
from alcsm.logging_config import get_logger

logger = get_logger(__name__)

_COLUMNS = (
    "profile_id",
    "dimension_number",
    "rater_id",
    "score",
    "evidence_text",
    "missing_status",
    "ambiguity_flag",
    "ambiguity_candidate_low",
    "ambiguity_candidate_high",
    "contradiction_flag",
    "contradiction_text",
    "verification_used",
    "verification_source",
    "verification_ts",
    "verification_outcome",
    "precedent_applied",
    "alcsm_version",
    "rulebook_version",
    "taxonomy_version_id",
    "coding_ts",
    "is_adjudication",
    "notes",
)


class DuplicateScoreError(RuntimeError):
    """Raised when (profile_id, dimension_number, rater_id, rulebook_version)
    already has a row -- the schema's own UNIQUE constraint caught it.

    A duplicate submission is refused, never silently overwritten
    (this task's explicit "accidental overwriting of first-pass data"
    /"duplicate prevention" rule, applied here to rater submissions:
    the fix for a wrong submission is an explicit correction workflow,
    not a second insert racing the first).
    """


def insert_annotation_score(conn: PGConnection, record: AnnotationScore) -> int:
    """Insert one rater's score for one profile x dimension.

    Validates first (:func:`validate_annotation_score`); if any rule
    is violated, raises :class:`AnnotationValidationError` without
    touching the database. On the schema's own UNIQUE constraint
    firing (a duplicate submission), raises :class:`DuplicateScoreError`
    instead of the raw ``psycopg2.errors.UniqueViolation``. Returns the
    new ``score_record_id``.
    """
    problems = validate_annotation_score(record)
    if problems:
        raise AnnotationValidationError(problems)

    cur = conn.cursor()
    try:
        placeholders = ", ".join(f"%({c})s" for c in _COLUMNS)
        cur.execute(
            f"""
            INSERT INTO alcsm.alcsm_dimension_score ({", ".join(_COLUMNS)})
            VALUES ({placeholders})
            RETURNING score_record_id;
            """,
            {c: getattr(record, c) for c in _COLUMNS},
        )
        row = cur.fetchone()
        assert row is not None
        score_record_id: int = row[0]
        conn.commit()
        logger.info(
            "annotation score inserted: profile=%s dim=%d rater=%s "
            "adjudication=%s record_id=%d",
            record.profile_id,
            record.dimension_number,
            record.rater_id,
            record.is_adjudication,
            score_record_id,
        )
        return score_record_id
    except psycopg2.errors.UniqueViolation as exc:
        conn.rollback()
        raise DuplicateScoreError(
            f"profile={record.profile_id} dimension={record.dimension_number} "
            f"rater={record.rater_id} rulebook_version={record.rulebook_version} "
            "already has a submitted score -- refused, not overwritten"
        ) from exc
    except Exception:
        conn.rollback()  # atomic: a failed insert leaves no partial row
        logger.error(
            "annotation score insert failed, rolled back: profile=%s dim=%d rater=%s",
            record.profile_id,
            record.dimension_number,
            record.rater_id,
        )
        raise
    finally:
        cur.close()


def fetch_rater_score(
    conn: PGConnection, profile_id: str, dimension_number: int, rater_id: str
) -> AnnotationScore | None:
    """Return ``rater_id``'s own submitted score, or None if not yet submitted.

    Always scoped to the exact ``rater_id`` passed in -- calling this
    with Rater A's id never returns Rater B's row. This is the only
    function in this module that returns a score value.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT {", ".join(_COLUMNS)}
            FROM alcsm.alcsm_dimension_score
            WHERE profile_id = %s AND dimension_number = %s AND rater_id = %s
            ORDER BY coding_ts DESC
            LIMIT 1;
            """,
            (profile_id, dimension_number, rater_id),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return AnnotationScore(**dict(zip(_COLUMNS, row, strict=True)))
    finally:
        cur.close()


def has_other_rater_submitted(
    conn: PGConnection, profile_id: str, dimension_number: int, this_rater_id: str
) -> bool:
    """Yes/no only: has any independent rater OTHER than ``this_rater_id``
    already submitted this profile x dimension?

    Deliberately returns a boolean, never a score -- the annotation UI
    may use this to decide whether it is now safe to reveal both
    scores for adjudication purposes (both have submitted), but must
    never use it to leak one rater's value to the other beforehand.
    Excludes adjudication rows: an adjudicator's prior ruling is not
    "another rater" for blinding purposes.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM alcsm.alcsm_dimension_score
                WHERE profile_id = %s AND dimension_number = %s
                  AND rater_id <> %s AND is_adjudication = FALSE
            );
            """,
            (profile_id, dimension_number, this_rater_id),
        )
        row = cur.fetchone()
        assert row is not None
        return bool(row[0])
    finally:
        cur.close()


def fetch_both_rater_scores_for_adjudication(
    conn: PGConnection, profile_id: str, dimension_number: int
) -> list[AnnotationScore]:
    """Return every independent (non-adjudication) rater score on record.

    Intended only for the adjudication step, which by definition needs
    to see both raters' work (ALCSM_Coding_Rulebook_and_Pilot_Design.md
    §1.5 Rule 3) -- callers must not use this during ordinary scoring
    to peek at a still-in-progress rater.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            f"""
            SELECT {", ".join(_COLUMNS)}
            FROM alcsm.alcsm_dimension_score
            WHERE profile_id = %s AND dimension_number = %s
              AND is_adjudication = FALSE
            ORDER BY rater_id;
            """,
            (profile_id, dimension_number),
        )
        rows = cur.fetchall()
        return [
            AnnotationScore(**dict(zip(_COLUMNS, row, strict=True))) for row in rows
        ]
    finally:
        cur.close()


def fetch_adjudication_score(
    conn: PGConnection, profile_id: str, dimension_number: int
) -> AnnotationScore | None:
    """Return the adjudicator's ruling for one profile x dimension, if any."""
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
        row = cur.fetchone()
        if row is None:
            return None
        return AnnotationScore(**dict(zip(_COLUMNS, row, strict=True)))
    finally:
        cur.close()


def insert_adjudication(conn: PGConnection, record: AnnotationScore) -> int:
    """Insert the adjudicator's ruling for one profile x dimension.

    Thin wrapper over :func:`insert_annotation_score` that forces
    ``rater_id='ADJUDICATOR'``/``is_adjudication=True`` regardless of
    what the caller passed, so an adjudication can never accidentally
    be inserted as an ordinary rater row (which would corrupt
    ``v_reliability_input``, which explicitly excludes adjudicated rows).
    """
    adjudication_record = replace(record, rater_id="ADJUDICATOR", is_adjudication=True)
    return insert_annotation_score(conn, adjudication_record)
