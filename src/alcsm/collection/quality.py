"""Post-hoc quality-assurance utilities for already-inserted collection data.

Distinct from ``collection/helper.py``'s validators: those gate a
*single record* before insertion (pre-insertion, per-record). These
utilities check the *database's own state* after the fact, at the
batch/corpus level — did the declared counts match reality, are
sections complete, is a batch internally consistent. They reuse the
existing validators where a per-record check is needed
(``validate_profile_record``/``validate_job_posting_record``) rather
than re-implementing field-level rules.

These are validation/reporting tools only — no research scoring, no
ALCSM dimension logic, no aggregation of any kind (Task 5's explicit
boundary).
"""

from __future__ import annotations

from dataclasses import dataclass

from psycopg2.extensions import cursor as PGCursor

from alcsm.constants import PROFILE_SECTIONS, Corpus


def _table_and_id_column(corpus: Corpus) -> tuple[str, str]:
    if corpus == "profile":
        return "profile", "profile_id"
    return "job_posting", "posting_id"


def count_records_for_batch(
    cur: PGCursor, sampling_batch_id: str, corpus: Corpus
) -> int:
    """Return how many records of ``corpus`` actually exist in the
    database for ``sampling_batch_id`` — the ground truth a batch's
    own declared ``records_included`` is checked against.
    """
    table, _ = _table_and_id_column(corpus)
    cur.execute(
        f"SELECT count(*) FROM alcsm.{table} WHERE sampling_batch_id = %s",
        (sampling_batch_id,),
    )
    row = cur.fetchone()
    return int(row[0]) if row else 0


@dataclass(frozen=True)
class BatchConsistencyReport:
    """Whether a batch's declared counts match what is actually stored."""

    sampling_batch_id: str
    corpus: Corpus
    declared_records_included: int | None
    actual_record_count: int
    consistent: bool
    problems: tuple[str, ...] = ()


def check_batch_consistency(
    cur: PGCursor, sampling_batch_id: str, corpus: Corpus
) -> BatchConsistencyReport:
    """Compare ``sampling_batch.records_included`` to the real row count.

    A batch that has not yet been completed (``records_included`` is
    NULL) is not flagged as inconsistent — there is nothing to compare
    against yet; that is simply "not yet completed," not a QA failure.
    """
    cur.execute(
        "SELECT records_included FROM alcsm.sampling_batch WHERE sampling_batch_id=%s",
        (sampling_batch_id,),
    )
    row = cur.fetchone()
    if row is None:
        return BatchConsistencyReport(
            sampling_batch_id=sampling_batch_id,
            corpus=corpus,
            declared_records_included=None,
            actual_record_count=0,
            consistent=False,
            problems=(f"sampling_batch_id {sampling_batch_id!r} does not exist",),
        )
    declared = row[0]
    actual = count_records_for_batch(cur, sampling_batch_id, corpus)

    problems: list[str] = []
    if declared is not None and declared != actual:
        problems.append(
            f"declared records_included={declared} but {actual} row(s) actually "
            f"exist for batch {sampling_batch_id!r}"
        )

    return BatchConsistencyReport(
        sampling_batch_id=sampling_batch_id,
        corpus=corpus,
        declared_records_included=declared,
        actual_record_count=actual,
        consistent=not problems,
        problems=tuple(problems),
    )


def check_required_metadata_present(
    cur: PGCursor, sampling_batch_id: str, corpus: Corpus
) -> list[str]:
    """Confirm every record in a batch has its required provenance
    fields populated (a live-database re-check of what
    ``validate_profile_record``/``validate_job_posting_record`` should
    already have guaranteed pre-insertion — a "trust but verify against
    the live database" pass, not a duplicate gate).
    """
    table, id_column = _table_and_id_column(corpus)
    cur.execute(
        f"""SELECT {id_column} FROM alcsm.{table}
            WHERE sampling_batch_id = %s
              AND (search_query IS NULL OR search_query = ''
                   OR inclusion_reason IS NULL OR collection_ts IS NULL)""",
        (sampling_batch_id,),
    )
    missing = [row[0] for row in cur.fetchall()]
    return [
        f"{record_id}: missing required provenance metadata" for record_id in missing
    ]


def check_section_completeness(
    cur: PGCursor, sampling_batch_id: str
) -> dict[str, float]:
    """For a profile batch, the fraction of profiles with each of the
    seven sections marked available. Purely descriptive (no score, no
    threshold, no pass/fail) — a completeness *metric*, matching
    Task 5's "evidence completeness" ask without implying any ALCSM
    judgement (that is the separate, later annotation stage).
    """
    cur.execute(
        "SELECT count(*) FROM alcsm.profile WHERE sampling_batch_id=%s",
        (sampling_batch_id,),
    )
    row = cur.fetchone()
    total = int(row[0]) if row else 0
    if total == 0:
        return {section: 0.0 for section in PROFILE_SECTIONS}

    completeness: dict[str, float] = {}
    for section in PROFILE_SECTIONS:
        cur.execute(
            """SELECT count(*) FROM alcsm.profile_raw_section
               WHERE section_name = %s AND section_available = TRUE
                 AND profile_id IN (
                     SELECT profile_id FROM alcsm.profile
                     WHERE sampling_batch_id = %s
                 )""",
            (section, sampling_batch_id),
        )
        row = cur.fetchone()
        available = int(row[0]) if row else 0
        completeness[section] = available / total
    return completeness


def check_duplicate_consistency(
    cur: PGCursor, sampling_batch_id: str, corpus: Corpus
) -> list[str]:
    """Confirm no two records in a batch share the same
    ``(search_query, search_rank_position)`` pair — a defence-in-depth
    check that the session-local duplicate check
    (``collection.duplicates``) was actually effective, distinct from
    the database's own primary-key uniqueness (which only guarantees
    distinct ids, not distinct underlying candidates re-entered under
    a fresh id).
    """
    table, id_column = _table_and_id_column(corpus)
    cur.execute(
        f"""SELECT search_query, search_rank_position, array_agg({id_column})
            FROM alcsm.{table}
            WHERE sampling_batch_id = %s AND search_rank_position IS NOT NULL
            GROUP BY search_query, search_rank_position
            HAVING count(*) > 1""",
        (sampling_batch_id,),
    )
    problems = []
    for search_query, rank, ids in cur.fetchall():
        problems.append(
            f"duplicate search_rank_position {rank} for query {search_query!r}: "
            f"{sorted(ids)}"
        )
    return problems
