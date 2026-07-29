"""Validated, atomic, privacy-enforcing profile insertion.

Production port of the manual-collection prototype at
``05_Data_Collection/Scripts/collection_helper.py`` (left unmodified
there as the historical implementation baseline). This module keeps
every rule that prototype enforced — pseudonymisation at capture,
atomic all-or-nothing writes, long-format section storage with an
explicit availability flag — and restructures it with types,
dataclasses, logging, and configuration via ``config.py``
(PROJECT_CONTEXT.md §27, §32; CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §6, §8).

WHAT THIS IS
    A structured DATA-ENTRY write path. A human reads a public profile
    by eye and supplies the field values; this module validates and
    inserts them transactionally.

WHAT THIS IS NOT
    It performs no browsing, scraping, or automated retrieval of
    LinkedIn — there is deliberately no HTTP client here
    (PROJECT_CONTEXT.md §46). It does not score dimensions (that is
    the separate annotation stage) and never stores names, URLs,
    photographs, or contact details (PROJECT_CONTEXT.md §45).

Single write path (final): this is the only path that writes profile
records. SQLAlchemy (``db/engine.py``) is never used for collection
writes and never will be — CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §8.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extensions import cursor as PGCursor

from alcsm.config import Settings, load_settings
from alcsm.constants import INCLUSION_REASONS, PROFILE_SECTIONS
from alcsm.logging_config import get_logger

logger = get_logger(__name__)

# Direct-identifier fields that must never appear on a profile record
# (PROJECT_CONTEXT.md §45 — pseudonymisation at capture).
_FORBIDDEN_IDENTIFIER_FIELDS = (
    "name",
    "full_name",
    "profile_url",
    "url",
    "photo",
    "email",
    "phone",
)

# Provenance fields required on every record (PROJECT_CONTEXT.md §13,
# `sampling_batch (1) -> (many) profile`).
_REQUIRED_PROVENANCE_FIELDS = (
    "sampling_batch_id",
    "search_query",
    "inclusion_reason",
    "collection_ts",
)

_PROFILE_ID_PATTERN = re.compile(r"^PRF-\d{5}$")
_LANGUAGE_PATTERN = re.compile(r"^[a-z]{2}$")
_GEOGRAPHY_PATTERN = re.compile(r"^[A-Z]{2}$")


class ProfileValidationError(ValueError):
    """A profile record violates a frozen collection rule.

    Carries every problem found (not just the first), so a human
    data-entry mistake is reported all at once — matching the
    validate-before-transact discipline of PROJECT_CONTEXT.md §32.
    """

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("Validation failed:\n  - " + "\n  - ".join(problems))


@dataclass(frozen=True)
class ProfileSection:
    """One raw profile section: availability, plus text if available.

    ``available`` is a required field, so "a section with no
    availability flag" — one of the original prototype's error cases
    — is now a structural impossibility rather than a runtime check.
    """

    available: bool
    text: str | None = None


@dataclass(frozen=True)
class ProfileRecord:
    """A profile ready for validation and insertion.

    No direct-identifier field exists on this type at all: passing
    ``name=``, ``email=``, etc. is a ``TypeError`` from Python itself,
    not a runtime check (PROJECT_CONTEXT.md §45). Use
    :meth:`from_mapping` at the untrusted-input boundary (e.g. a form
    or CSV row arriving as a plain dict), which additionally rejects
    such fields with a readable message before they ever reach this
    type.
    """

    profile_id: str
    sampling_batch_id: str
    search_query: str
    inclusion_reason: str
    collection_ts: datetime
    sections: Mapping[str, ProfileSection] = field(default_factory=dict)
    search_rank_position: int | None = None
    profile_language: str = "und"
    profile_geography: str | None = None
    observation_window_days: int | None = None
    activity_data_collected: bool = False

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> ProfileRecord:
        """Build a record from an untrusted mapping (e.g. a form/CSV row).

        Rejects forbidden direct-identifier fields and missing
        provenance fields with a combined, readable message before
        any value is touched further (PROJECT_CONTEXT.md §32, §45).
        """
        problems: list[str] = []

        present_forbidden = [f for f in _FORBIDDEN_IDENTIFIER_FIELDS if data.get(f)]
        problems += [
            f"forbidden identifier field present: {f!r} "
            "(never store direct identifiers)"
            for f in present_forbidden
        ]
        for required in _REQUIRED_PROVENANCE_FIELDS:
            if not data.get(required):
                problems.append(f"missing provenance field: {required}")
        if problems:
            raise ProfileValidationError(problems)

        sections_in = data.get("sections") or {}
        sections = {
            name: (s if isinstance(s, ProfileSection) else ProfileSection(**s))
            for name, s in sections_in.items()
        }
        return cls(
            profile_id=data.get("profile_id") or "",
            sampling_batch_id=data["sampling_batch_id"],
            search_query=data["search_query"],
            inclusion_reason=data["inclusion_reason"],
            collection_ts=data["collection_ts"],
            sections=sections,
            search_rank_position=data.get("search_rank_position"),
            profile_language=data.get("profile_language", "und"),
            profile_geography=data.get("profile_geography"),
            observation_window_days=data.get("observation_window_days"),
            activity_data_collected=bool(data.get("activity_data_collected", False)),
        )


@dataclass(frozen=True)
class SamplingBatch:
    """One documented, reproducible search (PROJECT_CONTEXT.md §13).

    Provenance root for a corpus of profiles. This module always
    registers batches with ``corpus='profile'`` — job-posting batches
    are a separate, out-of-scope concern (Phase P3).
    """

    sampling_batch_id: str
    search_query: str
    platform: str
    collection_started_ts: datetime
    inclusion_protocol_version: str
    collection_ended_ts: datetime | None = None
    result_set_size: int | None = None
    records_included: int | None = None
    notes: str | None = None


@dataclass(frozen=True)
class Rq4Criterion:
    """RQ4 external impact-indicator values for one profile.

    Physically isolated from ALCSM scoring (PROJECT_CONTEXT.md §5,
    §15) — this module only stores these values; nothing here reads
    or uses them for a dimension score.
    """

    extraction_method: str
    extraction_ts: datetime
    network_reach: int | None = None
    network_reach_capped: bool | None = None
    content_engagement: float | None = None
    content_post_count: int | None = None
    recognition_count: int | None = None
    seniority_progression_rate: float | None = None
    observation_window_days: int | None = None
    extracted_by: str | None = None


@dataclass(frozen=True)
class ProfileVerification:
    """Post-insertion check result for one profile."""

    section_count: int
    coherent: bool


def get_connection(settings: Settings | None = None) -> PGConnection:
    """Open a new psycopg2 connection for the collection write path.

    Deliberately independent of ``db/engine.py``'s SQLAlchemy engine:
    the collection helper is the single authoritative, psycopg2-based
    write path and must never be duplicated by an ORM-based one
    (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §8).
    """
    settings = settings or load_settings()
    return psycopg2.connect(**settings.database.as_psycopg2_kwargs())


def validate_profile_record(record: ProfileRecord) -> list[str]:
    """Return every rule violation found in ``record`` (empty if valid).

    Runs regardless of how ``record`` was constructed — the sole gate
    ``insert_profile`` relies on before touching the database
    (PROJECT_CONTEXT.md §32). Enforces:

    - ``profile_id`` matches ``PRF-#####`` (assigned at capture);
    - the four provenance fields are present
      (``sampling_batch_id``, ``search_query``, ``inclusion_reason``,
      ``collection_ts``);
    - ``inclusion_reason`` is in the controlled vocabulary;
    - ``profile_language``/``profile_geography`` are valid ISO codes
      or unset;
    - every section name is recognised, and an unavailable section
      carries no text (PROJECT_CONTEXT.md §9 — empty vs. not-retrieved
      must be explicit and coherent);
    - the activity-ethics gate: captured activity text requires
      ``activity_data_collected=True`` (PROJECT_CONTEXT.md §46).
    """
    errs: list[str] = []

    if not _PROFILE_ID_PATTERN.fullmatch(record.profile_id):
        errs.append("profile_id must match PRF-##### (assign at capture)")

    if not record.sampling_batch_id:
        errs.append("missing provenance field: sampling_batch_id")
    if not record.search_query:
        errs.append("missing provenance field: search_query")
    if not record.inclusion_reason:
        errs.append("missing provenance field: inclusion_reason")
    if not record.collection_ts:
        errs.append("missing provenance field: collection_ts")
    if record.inclusion_reason not in INCLUSION_REASONS:
        errs.append("inclusion_reason not in the controlled vocabulary")

    lang = record.profile_language
    if lang != "und" and not _LANGUAGE_PATTERN.fullmatch(lang):
        errs.append("profile_language must be ISO 639-1 (2 lowercase letters) or 'und'")
    geo = record.profile_geography
    if geo is not None and not _GEOGRAPHY_PATTERN.fullmatch(geo):
        errs.append("profile_geography must be ISO 3166-1 alpha-2 or None")

    for name, section in record.sections.items():
        if name not in PROFILE_SECTIONS:
            errs.append(f"unknown section name: {name!r}")
        if section.available is False and section.text:
            errs.append(
                f"section {name!r}: available=False but text present "
                "(a not-retrieved section cannot have text)"
            )

    activity = record.sections.get("activity")
    if (
        activity is not None
        and activity.available
        and activity.text
        and not record.activity_data_collected
    ):
        errs.append(
            "activity section captured but activity_data_collected is False "
            "(post-level activity needs its own ethics justification)"
        )

    return errs


def create_sampling_batch(cur: PGCursor, batch: SamplingBatch) -> bool:
    """Register a sampling batch as the provenance root for a search.

    One-time per search (PROJECT_CONTEXT.md §13). Idempotent: a
    duplicate ``sampling_batch_id`` is silently skipped
    (``ON CONFLICT DO NOTHING``), so re-running collection setup is
    safe. Takes a cursor, not a connection — the caller owns the
    transaction boundary, matching the original prototype's contract.

    Returns True if a new row was inserted, False if the batch already
    existed.
    """
    cur.execute(
        """
        INSERT INTO alcsm.sampling_batch
          (sampling_batch_id, corpus, search_query, platform,
           collection_started_ts, collection_ended_ts,
           result_set_size, records_included, inclusion_protocol_version, notes)
        VALUES (%(sampling_batch_id)s, 'profile', %(search_query)s, %(platform)s,
                %(collection_started_ts)s, %(collection_ended_ts)s, %(result_set_size)s,
                %(records_included)s, %(inclusion_protocol_version)s, %(notes)s)
        ON CONFLICT (sampling_batch_id) DO NOTHING;
        """,
        {
            "sampling_batch_id": batch.sampling_batch_id,
            "search_query": batch.search_query,
            "platform": batch.platform,
            "collection_started_ts": batch.collection_started_ts,
            "collection_ended_ts": batch.collection_ended_ts,
            "result_set_size": batch.result_set_size,
            "records_included": batch.records_included,
            "inclusion_protocol_version": batch.inclusion_protocol_version,
            "notes": batch.notes,
        },
    )
    inserted = cur.rowcount == 1
    logger.info(
        "sampling batch %s: %s",
        batch.sampling_batch_id,
        "registered" if inserted else "already existed (skipped)",
    )
    return inserted


def insert_profile(
    conn: PGConnection,
    record: ProfileRecord,
    criterion: Rq4Criterion | None = None,
) -> str:
    """Insert one profile, its raw sections, and optional RQ4 criteria.

    Validates first; if any rule is violated, raises
    :class:`ProfileValidationError` without touching the database. The
    insert itself is one transaction — profile, all seven sections,
    and the optional RQ4 row all commit together or none do
    (PROJECT_CONTEXT.md §32): a failure leaves no partial rows, so
    retrying is always safe.

    The RQ4 table is written here only as an isolated, optional
    satellite; nothing in this function reads those values back or
    uses them for a dimension score (PROJECT_CONTEXT.md §5, §15).
    """
    problems = validate_profile_record(record)
    if problems:
        raise ProfileValidationError(problems)

    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO alcsm.profile
              (profile_id, sampling_batch_id, profile_source, search_query,
               search_rank_position, inclusion_reason, collection_ts,
               profile_language, profile_geography, observation_window_days,
               activity_data_collected)
            VALUES (%(profile_id)s, %(sampling_batch_id)s, 'linkedin', %(search_query)s,
                    %(search_rank_position)s, %(inclusion_reason)s, %(collection_ts)s,
                    %(profile_language)s, %(profile_geography)s,
                    %(observation_window_days)s, %(activity_data_collected)s);
            """,
            {
                "profile_id": record.profile_id,
                "sampling_batch_id": record.sampling_batch_id,
                "search_query": record.search_query,
                "search_rank_position": record.search_rank_position,
                "inclusion_reason": record.inclusion_reason,
                "collection_ts": record.collection_ts,
                "profile_language": record.profile_language,
                "profile_geography": record.profile_geography,
                "observation_window_days": record.observation_window_days,
                "activity_data_collected": record.activity_data_collected,
            },
        )

        for name in PROFILE_SECTIONS:
            section = record.sections.get(
                name, ProfileSection(available=False, text=None)
            )
            cur.execute(
                """
                INSERT INTO alcsm.profile_raw_section
                  (profile_id, section_name, section_text,
                   section_available, captured_ts)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    record.profile_id,
                    name,
                    section.text if section.available else None,
                    bool(section.available),
                    record.collection_ts,
                ),
            )

        if criterion is not None:
            cur.execute(
                """
                INSERT INTO alcsm.rq4_impact_indicator
                  (profile_id, rq4_network_reach, rq4_network_reach_capped,
                   rq4_content_engagement, rq4_content_post_count,
                   rq4_recognition_count, rq4_seniority_progression_rate,
                   rq4_observation_window_days, extraction_method,
                   extracted_by, extraction_ts)
                VALUES (%(profile_id)s, %(network_reach)s, %(network_reach_capped)s,
                        %(content_engagement)s, %(content_post_count)s,
                        %(recognition_count)s, %(seniority_progression_rate)s,
                        %(observation_window_days)s, %(extraction_method)s,
                        %(extracted_by)s, %(extraction_ts)s);
                """,
                {
                    "profile_id": record.profile_id,
                    "network_reach": criterion.network_reach,
                    "network_reach_capped": criterion.network_reach_capped,
                    "content_engagement": criterion.content_engagement,
                    "content_post_count": criterion.content_post_count,
                    "recognition_count": criterion.recognition_count,
                    "seniority_progression_rate": criterion.seniority_progression_rate,
                    "observation_window_days": criterion.observation_window_days,
                    "extraction_method": criterion.extraction_method,
                    "extracted_by": criterion.extracted_by,
                    "extraction_ts": criterion.extraction_ts,
                },
            )

        conn.commit()
        logger.info(
            "profile %s inserted (%d sections captured, rq4_criterion=%s)",
            record.profile_id,
            sum(1 for s in record.sections.values() if s.available),
            criterion is not None,
        )
        return record.profile_id
    except Exception as exc:
        conn.rollback()  # atomic: a failed profile leaves NO partial rows
        logger.error(
            "profile %s insertion failed, rolled back: %s",
            record.profile_id,
            type(exc).__name__,
        )
        raise
    finally:
        cur.close()


def verify_profile(conn: PGConnection, profile_id: str) -> ProfileVerification:
    """Post-insertion sanity check for one profile.

    Confirms the section count and that no section is simultaneously
    marked unavailable and carrying text (the coherence rule
    validated pre-insertion, re-checked here as a defence-in-depth
    read-back).
    """
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT count(*) FROM alcsm.profile_raw_section WHERE profile_id=%s",
            (profile_id,),
        )
        row = cur.fetchone()
        section_count = row[0] if row else 0

        cur.execute(
            """SELECT bool_or(section_text IS NOT NULL AND section_available=FALSE)
               FROM alcsm.profile_raw_section WHERE profile_id=%s""",
            (profile_id,),
        )
        row = cur.fetchone()
        incoherent = bool(row[0]) if row and row[0] is not None else False
    finally:
        cur.close()
    return ProfileVerification(section_count=section_count, coherent=not incoherent)
