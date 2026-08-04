"""Seed the eight taxonomies' term lists from collected job postings.

This module has two distinct layers, deliberately kept separate:

INFRASTRUCTURE (built in Phase P3 Session 2, real and tested)
    Typed records for a taxonomy version and its terms
    (:class:`TaxonomyVersionRecord`, :class:`TaxonomyTermRecord`),
    their validators, and idempotent, atomic, phase-gated database
    write helpers (:func:`create_taxonomy_version`,
    :func:`insert_taxonomy_terms`, :func:`freeze_taxonomy_version`).
    These enforce the frozen rules mechanically — most importantly,
    that a frozen taxonomy version can never receive a new term
    (PROJECT_CONTEXT.md §27, §37) — regardless of what later calls
    them.

GENERATION (NOT built here — remains Phase P3, a later session)
    :func:`anchor_taxonomy_from_postings` is the actual term-extraction
    algorithm. It is intentionally still unimplemented: it requires
    ~200 real job postings (gated on ethics approval, PROJECT_CONTEXT.md
    §38, §46) and a decided extraction method (P3_Session1_Test_
    Strategy.md §8, deferred there). This session builds the plumbing
    that function will eventually call — it does not decide what the
    function does.

Must (once generation is implemented):
    - derive term lists only from evidenced job-posting vocabulary,
      never invent unevidenced terms (PROJECT_CONTEXT.md §27);
    - stamp a `taxonomy_version` and freeze it — no edits to a frozen
      version (PROJECT_CONTEXT.md §15, §37);
    - the eight taxonomies' *structure* is frozen; only term-list
      *content* is anchored here (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
      §2, §16) — this module never derives an ALCSM dimension score.

F-06 (`taxonomy_version_id NOT NULL`) is enabled only after a taxonomy
version is stamped and frozen here — not before (PROJECT_CONTEXT.md
§17, §44).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from psycopg2.extensions import connection as PGConnection
from psycopg2.extensions import cursor as PGCursor

from alcsm.collection.helper import JobPostingRecord
from alcsm.constants import TAXONOMY_NAMES, TaxonomyName
from alcsm.logging_config import get_logger

logger = get_logger(__name__)


class TaxonomyValidationError(ValueError):
    """A taxonomy version or term violates a frozen anchoring rule.

    Carries every problem found (not just the first), matching the
    contract of :class:`alcsm.collection.helper.CollectionValidationError`
    (Task 1: "Do not duplicate code where reusable abstractions
    exist" — the *shape* is reused even though this is a distinct
    exception hierarchy for a distinct module boundary).
    """

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("Validation failed:\n  - " + "\n  - ".join(problems))


@dataclass(frozen=True)
class AnchoringConfig:
    """Configuration for a future anchoring run.

    Deliberately minimal: only the one parameter already implied by
    the frozen design (`taxonomy_term.source_frequency` — Task5_P3_
    JobPosting_Collection_Plan.md §8) is captured. This is
    infrastructure for a decision the extraction algorithm will make
    later, not an attempt to pre-decide that algorithm.
    """

    minimum_source_frequency: int = 1


@dataclass(frozen=True)
class TaxonomyVersionRecord:
    """One versioned instance of a taxonomy, ready for validation and
    insertion (mirrors the `taxonomy_version` table exactly).

    ``frozen`` defaults to ``False``: a version is created open, terms
    are inserted into it, and it is frozen explicitly and separately
    via :func:`freeze_taxonomy_version` — freezing is a deliberate,
    logged, one-way action, never an insertion side effect.
    """

    taxonomy_version_id: str
    taxonomy_name: TaxonomyName
    version_label: str
    constructed_ts: datetime
    anchored_to_batch: str | None = None
    frozen: bool = False


@dataclass(frozen=True)
class TaxonomyTermRecord:
    """One candidate term belonging to a taxonomy version (mirrors the
    `taxonomy_term` table exactly).

    ``source_frequency`` is ``None`` only for a term added a priori
    (matching the schema column's own comment); anchored terms carry
    their observed frequency in the posting corpus.
    """

    taxonomy_version_id: str
    term: str
    tier_or_band: str | None = None
    source_frequency: int | None = None


def validate_taxonomy_version(record: TaxonomyVersionRecord) -> list[str]:
    """Return every rule violation found in ``record`` (empty if valid).

    Enforces: ``taxonomy_version_id``/``version_label``/
    ``constructed_ts`` are present, and ``taxonomy_name`` is one of
    the eight frozen taxonomies (never an invented ninth one).
    """
    errs: list[str] = []
    if not record.taxonomy_version_id:
        errs.append("missing field: taxonomy_version_id")
    if record.taxonomy_name not in TAXONOMY_NAMES:
        errs.append(
            f"taxonomy_name {record.taxonomy_name!r} is not one of the eight "
            f"frozen taxonomies: {TAXONOMY_NAMES}"
        )
    if not record.version_label:
        errs.append("missing field: version_label")
    if not record.constructed_ts:
        errs.append("missing field: constructed_ts")
    return errs


def validate_taxonomy_term(record: TaxonomyTermRecord) -> list[str]:
    """Return every rule violation found in ``record`` (empty if valid).

    Enforces: ``taxonomy_version_id`` present, ``term`` non-empty
    (after stripping whitespace), and ``source_frequency`` non-negative
    when set.
    """
    errs: list[str] = []
    if not record.taxonomy_version_id:
        errs.append("missing field: taxonomy_version_id")
    if not record.term or not record.term.strip():
        errs.append("term must be non-empty")
    if record.source_frequency is not None and record.source_frequency < 0:
        errs.append("source_frequency must be >= 0 when set")
    return errs


def create_taxonomy_version(cur: PGCursor, record: TaxonomyVersionRecord) -> bool:
    """Register a taxonomy version. Idempotent, cursor-based, caller
    owns the transaction — mirrors ``collection.helper.
    create_sampling_batch`` exactly (a one-time provenance-root-style
    registration, not a bulk content write).

    Returns True if a new row was inserted, False if the version
    already existed.
    """
    problems = validate_taxonomy_version(record)
    if problems:
        raise TaxonomyValidationError(problems)

    cur.execute(
        """
        INSERT INTO alcsm.taxonomy_version
          (taxonomy_version_id, taxonomy_name, version_label,
           constructed_ts, anchored_to_batch, frozen)
        VALUES (%(taxonomy_version_id)s, %(taxonomy_name)s, %(version_label)s,
                %(constructed_ts)s, %(anchored_to_batch)s, %(frozen)s)
        ON CONFLICT (taxonomy_version_id) DO NOTHING;
        """,
        {
            "taxonomy_version_id": record.taxonomy_version_id,
            "taxonomy_name": record.taxonomy_name,
            "version_label": record.version_label,
            "constructed_ts": record.constructed_ts,
            "anchored_to_batch": record.anchored_to_batch,
            "frozen": record.frozen,
        },
    )
    inserted = cur.rowcount == 1
    logger.info(
        "taxonomy version %s (%s): %s",
        record.taxonomy_version_id,
        record.taxonomy_name,
        "registered" if inserted else "already existed (skipped)",
    )
    return inserted


def _is_frozen(cur: PGCursor, taxonomy_version_id: str) -> bool:
    """Look up whether a taxonomy version is frozen. Raises if it does
    not exist at all — a caller referencing an unknown version is a
    bug to surface, not a silent False.
    """
    cur.execute(
        "SELECT frozen FROM alcsm.taxonomy_version WHERE taxonomy_version_id=%s",
        (taxonomy_version_id,),
    )
    row = cur.fetchone()
    if row is None:
        raise TaxonomyValidationError(
            [f"taxonomy_version_id {taxonomy_version_id!r} does not exist"]
        )
    return bool(row[0])


def insert_taxonomy_terms(
    conn: PGConnection, terms: Sequence[TaxonomyTermRecord]
) -> int:
    """Insert one or more taxonomy terms, atomically.

    Validates every term first (collecting all problems, not just the
    first — PROJECT_CONTEXT.md §32); rejects the whole batch if any
    referenced ``taxonomy_version_id`` is already frozen (the
    application-layer enforcement of "never edit a frozen version" —
    PROJECT_CONTEXT.md §27 — since the schema itself has no CHECK
    constraint that can see across the ``taxonomy_version``/
    ``taxonomy_term`` table boundary). The insert is one transaction:
    all terms commit together or none do, mirroring
    ``insert_profile``/``insert_job_posting`` exactly.

    Returns the number of terms inserted.
    """
    if not terms:
        return 0

    problems: list[str] = []
    for i, term in enumerate(terms):
        problems += [f"term[{i}]: {p}" for p in validate_taxonomy_term(term)]
    if problems:
        raise TaxonomyValidationError(problems)

    cur = conn.cursor()
    try:
        target_versions = sorted({t.taxonomy_version_id for t in terms})
        for version_id in target_versions:
            if _is_frozen(cur, version_id):
                raise TaxonomyValidationError(
                    [
                        f"taxonomy_version_id {version_id!r} is frozen — "
                        "no term may be added to it"
                    ]
                )

        for term in terms:
            cur.execute(
                """
                INSERT INTO alcsm.taxonomy_term
                  (taxonomy_version_id, term, tier_or_band, source_frequency)
                VALUES (%(taxonomy_version_id)s, %(term)s, %(tier_or_band)s,
                        %(source_frequency)s);
                """,
                {
                    "taxonomy_version_id": term.taxonomy_version_id,
                    "term": term.term,
                    "tier_or_band": term.tier_or_band,
                    "source_frequency": term.source_frequency,
                },
            )
        conn.commit()
        logger.info(
            "inserted %d taxonomy term(s) across %d version(s)",
            len(terms),
            len(target_versions),
        )
        return len(terms)
    except Exception as exc:
        conn.rollback()  # atomic: a failed batch leaves NO partial rows
        logger.error(
            "taxonomy term insertion failed, rolled back: %s", type(exc).__name__
        )
        raise
    finally:
        cur.close()


def freeze_taxonomy_version(conn: PGConnection, taxonomy_version_id: str) -> bool:
    """Freeze a taxonomy version, permanently. Idempotent-safe: freezing
    an already-frozen version is a logged no-op, not an error, but is
    always reported via the return value so a caller can tell the two
    cases apart.

    Once frozen, :func:`insert_taxonomy_terms` will refuse any further
    term for this version — this is the one-way action that makes
    that guarantee possible (PROJECT_CONTEXT.md §37).

    Returns True if this call performed the freeze, False if the
    version was already frozen. Raises if the version does not exist.
    """
    cur = conn.cursor()
    try:
        if _is_frozen(cur, taxonomy_version_id):
            logger.info(
                "taxonomy version %s already frozen (no-op)", taxonomy_version_id
            )
            return False
        cur.execute(
            "UPDATE alcsm.taxonomy_version SET frozen=TRUE "
            "WHERE taxonomy_version_id=%s",
            (taxonomy_version_id,),
        )
        conn.commit()
        logger.info("taxonomy version %s frozen", taxonomy_version_id)
        return True
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()


def anchor_taxonomy_from_postings(
    postings: Sequence[JobPostingRecord],
    taxonomy_name: TaxonomyName,
    config: AnchoringConfig | None = None,
) -> list[TaxonomyTermRecord]:
    """Derive a candidate term list for one taxonomy from posting text.

    NOT IMPLEMENTED — this is the generation layer, explicitly out of
    scope for Phase P3 Session 2 (see module docstring). This
    signature documents the intended interface (a later session's
    starting point) without deciding the extraction method:

    - ``postings`` would be the full, real ~200-posting corpus (never
      a partial batch — partial-corpus anchoring biases frequency
      counts toward whichever batches happened to run first,
      Task5_P3_JobPosting_Collection_Plan.md §7);
    - ``taxonomy_name`` selects which of the eight taxonomies to
      anchor;
    - the returned terms are not inserted by this function — a caller
      passes them to :func:`insert_taxonomy_terms` and then
      :func:`freeze_taxonomy_version` once satisfied, as two separate,
      deliberate steps.

    TODO (Phase P3, a later session): implement once ~200 real job
    postings are collected (gated on ethics approval) and an
    extraction method is decided (P3_Session1_Test_Strategy.md §8).
    """
    raise NotImplementedError(
        "Term generation is implemented in a later P3 session, after real "
        "job postings are collected and an extraction method is decided."
    )
