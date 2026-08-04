"""Validated, atomic, privacy-enforcing collection insertion.

Production port of the manual-collection prototype at
``05_Data_Collection/Scripts/collection_helper.py`` (left unmodified
there as the historical implementation baseline). This module keeps
every rule that prototype enforced — pseudonymisation at capture,
atomic all-or-nothing writes, long-format section storage with an
explicit availability flag — and restructures it with types,
dataclasses, logging, and configuration via ``config.py``
(PROJECT_CONTEXT.md §27, §32; CLAUDE_CODE_IMPLEMENTATION_GUIDE.md §6, §8).

Covers both corpora the frozen schema defines under ``sampling_batch``
(``profile`` and, as of Phase P3 Session 2, ``job_posting``): profile
insertion (``insert_profile``) and job-posting insertion
(``insert_job_posting``) share the same validated, atomic, logged
pattern and the same generalised ``SamplingBatch``/``create_sampling_
batch`` provenance root — Task5_P3_JobPosting_Collection_Plan.md §5.

WHAT THIS IS
    A structured DATA-ENTRY write path. A human reads a public profile
    or job posting by eye and supplies the field values; this module
    validates and inserts them transactionally.

WHAT THIS IS NOT
    It performs no browsing, scraping, or automated retrieval of
    LinkedIn or any job board — there is deliberately no HTTP client
    here (PROJECT_CONTEXT.md §46). It does not score dimensions or
    anchor taxonomies (separate stages) and never stores names, URLs,
    photographs, contact details, or recruiter identifiers
    (PROJECT_CONTEXT.md §45; Task5_P3_JobPosting_Collection_Plan.md §6).

Single write path (final): this is the only path that writes profile
or job-posting records. SQLAlchemy (``db/engine.py``) is never used
for collection writes and never will be — CLAUDE_CODE_IMPLEMENTATION_
GUIDE.md §8.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import psycopg2
from psycopg2.extensions import connection as PGConnection
from psycopg2.extensions import cursor as PGCursor

from alcsm.config import Settings, load_settings
from alcsm.constants import INCLUSION_REASONS, PROFILE_SECTIONS, Corpus
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

# Job postings additionally require `posting_source` as caller-supplied
# input (unlike `profile_source`, which `insert_profile` hard-codes to
# 'linkedin' -- postings genuinely vary by source board/platform).
_REQUIRED_POSTING_PROVENANCE_FIELDS = (
    "sampling_batch_id",
    "search_query",
    "inclusion_reason",
    "collection_ts",
    "posting_source",
)

# Recruiter-identifying fields that must never appear on a job-posting
# record (Task5_P3_JobPosting_Collection_Plan.md §6 -- the unit of
# analysis is the posting's requirements, never the poster).
_FORBIDDEN_RECRUITER_FIELDS = (
    "recruiter_name",
    "recruiter_email",
    "recruiter_phone",
    "recruiter_profile_url",
    "contact_name",
    "contact_email",
    "contact_phone",
    "contact_profile_url",
)

_PROFILE_ID_PATTERN = re.compile(r"^PRF-\d{5}$")
_POSTING_ID_PATTERN = re.compile(r"^JOB-\d{5}$")
_LANGUAGE_PATTERN = re.compile(r"^[a-z]{2}$")
_GEOGRAPHY_PATTERN = re.compile(r"^[A-Z]{2}$")

# Deterministic, pattern-based scan for machine-detectable personal
# identifiers in job-posting free text. NOT a name detector -- reliably
# finding a bare recruiter name in unstructured text requires NLP
# (named-entity recognition), which is out of scope for this phase
# (PROJECT_CONTEXT.md §25, §46; CLAUDE_CODE_RULES.md rule 8). Free-text
# name redaction remains a human transcription-time QA discipline
# (Task5_P3_JobPosting_Collection_Plan.md §6), not an automated
# guarantee these patterns can honestly make.
_EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE_PATTERN = re.compile(
    r"(?<!\d)(?:\+?\d{1,3}[\s.-])?\(?\d{2,4}\)?[\s.-]\d{3,4}[\s.-]\d{3,4}(?!\d)"
)
_LINKEDIN_PROFILE_URL_PATTERN = re.compile(
    r"linkedin\.com/in/[A-Za-z0-9\-_%]+", re.IGNORECASE
)


def detect_recruiter_identifiers(text: str) -> list[str]:
    """Return every machine-detectable personal-identifier pattern found.

    Deterministic and content-based (Task 2: "validation should be
    deterministic") -- scans for email addresses, phone-number-shaped
    digit sequences, and LinkedIn personal-profile links. Returns an
    empty list if none are found. See the module-level pattern
    comments above for the honest limitation on free-text name
    detection.
    """
    findings: list[str] = []
    if _EMAIL_PATTERN.search(text):
        findings.append("email address pattern detected")
    if _PHONE_PATTERN.search(text):
        findings.append("phone-number-like pattern detected")
    if _LINKEDIN_PROFILE_URL_PATTERN.search(text):
        findings.append("LinkedIn personal-profile link detected")
    return findings


class CollectionValidationError(ValueError):
    """A collected record violates a frozen collection rule.

    Carries every problem found (not just the first), so a human
    data-entry mistake is reported all at once — matching the
    validate-before-transact discipline of PROJECT_CONTEXT.md §32.
    Base class shared by :class:`ProfileValidationError` and
    :class:`JobPostingValidationError` so both corpora's validators
    raise a consistently-shaped error.
    """

    def __init__(self, problems: list[str]) -> None:
        self.problems = list(problems)
        super().__init__("Validation failed:\n  - " + "\n  - ".join(problems))


class ProfileValidationError(CollectionValidationError):
    """A profile record violates a frozen collection rule."""


class JobPostingValidationError(CollectionValidationError):
    """A job-posting record violates a frozen collection rule."""


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
class JobPostingRecord:
    """A job posting ready for validation and insertion.

    No recruiter-identifying field exists on this type at all: passing
    ``recruiter_name=``, ``recruiter_email=``, etc. is a ``TypeError``
    from Python itself, not a runtime check (Task5_P3_JobPosting_
    Collection_Plan.md §6). Use :meth:`from_mapping` at the
    untrusted-input boundary, which additionally rejects such fields
    (plus the general direct-identifier fields, reused from the
    profile side) with a readable message before any value is touched
    further. ``raw_posting_text``/``raw_requirements_text`` are still
    scanned for machine-detectable identifier *content* by
    :func:`validate_job_posting_record` — field rejection alone cannot
    catch identifying text pasted into the posting body.
    """

    posting_id: str
    sampling_batch_id: str
    posting_source: str
    search_query: str
    inclusion_reason: str
    collection_ts: datetime
    raw_posting_text: str
    search_rank_position: int | None = None
    posting_language: str = "und"
    posting_geography: str | None = None
    posted_date: date | None = None
    seniority_label_raw: str | None = None
    raw_requirements_text: str | None = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> JobPostingRecord:
        """Build a record from an untrusted mapping (e.g. a form/CSV row).

        Rejects forbidden direct-identifier and recruiter-identifier
        fields and missing provenance fields with a combined, readable
        message before any value is touched further.
        """
        problems: list[str] = []

        forbidden_fields = (*_FORBIDDEN_IDENTIFIER_FIELDS, *_FORBIDDEN_RECRUITER_FIELDS)
        present_forbidden = [f for f in forbidden_fields if data.get(f)]
        problems += [
            f"forbidden identifier field present: {f!r} "
            "(never store direct or recruiter identifiers)"
            for f in present_forbidden
        ]
        for required in _REQUIRED_POSTING_PROVENANCE_FIELDS:
            if not data.get(required):
                problems.append(f"missing provenance field: {required}")
        if problems:
            raise JobPostingValidationError(problems)

        return cls(
            posting_id=data.get("posting_id") or "",
            sampling_batch_id=data["sampling_batch_id"],
            posting_source=data["posting_source"],
            search_query=data["search_query"],
            inclusion_reason=data["inclusion_reason"],
            collection_ts=data["collection_ts"],
            raw_posting_text=data.get("raw_posting_text") or "",
            search_rank_position=data.get("search_rank_position"),
            posting_language=data.get("posting_language", "und"),
            posting_geography=data.get("posting_geography"),
            posted_date=data.get("posted_date"),
            seniority_label_raw=data.get("seniority_label_raw"),
            raw_requirements_text=data.get("raw_requirements_text"),
        )


@dataclass(frozen=True)
class SamplingBatch:
    """One documented, reproducible search (PROJECT_CONTEXT.md §13).

    Provenance root for either corpus. ``corpus`` defaults to
    ``'profile'`` for backward compatibility with every existing
    caller that predates job-posting support — a batch is only ever
    registered for ``'job_posting'`` when explicitly constructed that
    way (Phase P3 Session 2 generalisation of what was previously a
    profile-only, hard-coded assumption).
    """

    sampling_batch_id: str
    search_query: str
    platform: str
    collection_started_ts: datetime
    inclusion_protocol_version: str
    corpus: Corpus = "profile"
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


@dataclass(frozen=True)
class PostingVerification:
    """Post-insertion check result for one job posting.

    ``recruiter_identifiers_detected`` is a defence-in-depth re-scan of
    the *stored* text (mirrors :func:`verify_profile`'s coherence
    re-check) — empty means the deterministic patterns in
    :func:`detect_recruiter_identifiers` found nothing, not an
    absolute guarantee (see that function's docstring).
    """

    has_raw_text: bool
    recruiter_identifiers_detected: tuple[str, ...] = ()


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

    Works for either corpus via ``batch.corpus`` (Phase P3 Session 2
    generalisation — previously hard-coded to ``'profile'``); existing
    callers that never set ``corpus`` are unaffected, since it
    defaults to ``'profile'`` on :class:`SamplingBatch` itself.

    Returns True if a new row was inserted, False if the batch already
    existed.
    """
    cur.execute(
        """
        INSERT INTO alcsm.sampling_batch
          (sampling_batch_id, corpus, search_query, platform,
           collection_started_ts, collection_ended_ts,
           result_set_size, records_included, inclusion_protocol_version, notes)
        VALUES (%(sampling_batch_id)s, %(corpus)s, %(search_query)s, %(platform)s,
                %(collection_started_ts)s, %(collection_ended_ts)s, %(result_set_size)s,
                %(records_included)s, %(inclusion_protocol_version)s, %(notes)s)
        ON CONFLICT (sampling_batch_id) DO NOTHING;
        """,
        {
            "sampling_batch_id": batch.sampling_batch_id,
            "corpus": batch.corpus,
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
        "sampling batch %s (%s): %s",
        batch.sampling_batch_id,
        batch.corpus,
        "registered" if inserted else "already existed (skipped)",
    )
    return inserted


def complete_sampling_batch(
    cur: PGCursor,
    sampling_batch_id: str,
    collection_ended_ts: datetime,
    result_set_size: int | None = None,
    records_included: int | None = None,
    notes: str | None = None,
) -> bool:
    """Mark a sampling batch as ended, recording its final counts.

    The lifecycle counterpart to :func:`create_sampling_batch` (Phase
    P3 Session 3 — a genuine gap, not duplication: nothing previously
    updated a batch after its initial registration). Cursor-based,
    caller owns the transaction, matching ``create_sampling_batch``'s
    contract exactly.

    Only updates a batch that is not yet ended (``collection_ended_ts
    IS NULL``) — completing an already-completed batch is a no-op,
    never a silent overwrite of a prior completion's counts, mirroring
    the "no edits to a frozen version" discipline applied here to a
    batch's own completion record.

    Returns True if this call completed the batch, False if it was
    already completed (or does not exist).
    """
    cur.execute(
        """
        UPDATE alcsm.sampling_batch
        SET collection_ended_ts = %(collection_ended_ts)s,
            result_set_size = %(result_set_size)s,
            records_included = %(records_included)s,
            notes = %(notes)s
        WHERE sampling_batch_id = %(sampling_batch_id)s
          AND collection_ended_ts IS NULL;
        """,
        {
            "sampling_batch_id": sampling_batch_id,
            "collection_ended_ts": collection_ended_ts,
            "result_set_size": result_set_size,
            "records_included": records_included,
            "notes": notes,
        },
    )
    completed = cur.rowcount == 1
    logger.info(
        "sampling batch %s: %s",
        sampling_batch_id,
        "completed" if completed else "not completed (already ended, or unknown id)",
    )
    return completed


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


def validate_job_posting_record(record: JobPostingRecord) -> list[str]:
    """Return every rule violation found in ``record`` (empty if valid).

    Runs regardless of how ``record`` was constructed — the sole gate
    ``insert_job_posting`` relies on before touching the database
    (PROJECT_CONTEXT.md §32, mirroring ``validate_profile_record``).
    Enforces:

    - ``posting_id`` matches ``JOB-#####`` (assigned at capture);
    - the five provenance fields are present (``sampling_batch_id``,
      ``search_query``, ``inclusion_reason``, ``collection_ts``,
      ``posting_source``);
    - ``inclusion_reason`` is in the controlled vocabulary (reused
      from the profile side — the schema's CHECK constraint is
      identical for both tables);
    - ``posting_language``/``posting_geography`` are valid ISO codes
      or unset;
    - ``raw_posting_text`` is non-empty (verbatim retention is
      required for taxonomy anchoring — schema column comment);
    - ``raw_posting_text``/``raw_requirements_text`` carry no
      machine-detectable recruiter-identifying content (Task5_P3_
      JobPosting_Collection_Plan.md §6).
    """
    errs: list[str] = []

    if not _POSTING_ID_PATTERN.fullmatch(record.posting_id):
        errs.append("posting_id must match JOB-##### (assign at capture)")

    if not record.sampling_batch_id:
        errs.append("missing provenance field: sampling_batch_id")
    if not record.search_query:
        errs.append("missing provenance field: search_query")
    if not record.inclusion_reason:
        errs.append("missing provenance field: inclusion_reason")
    if not record.collection_ts:
        errs.append("missing provenance field: collection_ts")
    if not record.posting_source:
        errs.append("missing provenance field: posting_source")
    if record.inclusion_reason not in INCLUSION_REASONS:
        errs.append("inclusion_reason not in the controlled vocabulary")

    lang = record.posting_language
    if lang != "und" and not _LANGUAGE_PATTERN.fullmatch(lang):
        errs.append("posting_language must be ISO 639-1 (2 lowercase letters) or 'und'")
    geo = record.posting_geography
    if geo is not None and not _GEOGRAPHY_PATTERN.fullmatch(geo):
        errs.append("posting_geography must be ISO 3166-1 alpha-2 or None")

    if not record.raw_posting_text or not record.raw_posting_text.strip():
        errs.append(
            "raw_posting_text must be non-empty "
            "(verbatim retention is required for taxonomy anchoring)"
        )

    for field_name, text in (
        ("raw_posting_text", record.raw_posting_text),
        ("raw_requirements_text", record.raw_requirements_text),
    ):
        if text:
            for finding in detect_recruiter_identifiers(text):
                errs.append(
                    f"{field_name}: {finding} — recruiter-identifying content "
                    "must not be stored (GDPR; "
                    "Task5_P3_JobPosting_Collection_Plan.md §6)"
                )

    return errs


def insert_job_posting(conn: PGConnection, record: JobPostingRecord) -> str:
    """Insert one job posting.

    Validates first; if any rule is violated, raises
    :class:`JobPostingValidationError` without touching the database.
    The insert is one transaction — atomic, rolled back whole on any
    error (PROJECT_CONTEXT.md §32), mirroring ``insert_profile``
    exactly. This is the single write path for job postings, just as
    ``insert_profile`` is for profiles (CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
    §8) — never duplicated by a second path.
    """
    problems = validate_job_posting_record(record)
    if problems:
        raise JobPostingValidationError(problems)

    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO alcsm.job_posting
              (posting_id, sampling_batch_id, posting_source, search_query,
               search_rank_position, inclusion_reason, collection_ts,
               posting_language, posting_geography, posted_date,
               seniority_label_raw, raw_posting_text, raw_requirements_text)
            VALUES (%(posting_id)s, %(sampling_batch_id)s, %(posting_source)s,
                    %(search_query)s, %(search_rank_position)s, %(inclusion_reason)s,
                    %(collection_ts)s, %(posting_language)s, %(posting_geography)s,
                    %(posted_date)s, %(seniority_label_raw)s, %(raw_posting_text)s,
                    %(raw_requirements_text)s);
            """,
            {
                "posting_id": record.posting_id,
                "sampling_batch_id": record.sampling_batch_id,
                "posting_source": record.posting_source,
                "search_query": record.search_query,
                "search_rank_position": record.search_rank_position,
                "inclusion_reason": record.inclusion_reason,
                "collection_ts": record.collection_ts,
                "posting_language": record.posting_language,
                "posting_geography": record.posting_geography,
                "posted_date": record.posted_date,
                "seniority_label_raw": record.seniority_label_raw,
                "raw_posting_text": record.raw_posting_text,
                "raw_requirements_text": record.raw_requirements_text,
            },
        )
        conn.commit()
        logger.info("job posting %s inserted", record.posting_id)
        return record.posting_id
    except Exception as exc:
        conn.rollback()  # atomic: a failed posting leaves NO partial rows
        logger.error(
            "job posting %s insertion failed, rolled back: %s",
            record.posting_id,
            type(exc).__name__,
        )
        raise
    finally:
        cur.close()


def verify_posting(conn: PGConnection, posting_id: str) -> PostingVerification:
    """Post-insertion sanity check for one job posting.

    Confirms ``raw_posting_text`` was actually stored and re-scans the
    stored text for recruiter-identifying content, as a defence-in-
    depth read-back mirroring ``verify_profile``'s coherence re-check.
    """
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT raw_posting_text, raw_requirements_text
               FROM alcsm.job_posting WHERE posting_id=%s""",
            (posting_id,),
        )
        row = cur.fetchone()
    finally:
        cur.close()

    if row is None:
        return PostingVerification(has_raw_text=False)

    raw_text, raw_requirements = row
    findings: list[str] = []
    if raw_text:
        findings.extend(detect_recruiter_identifiers(raw_text))
    if raw_requirements:
        findings.extend(detect_recruiter_identifiers(raw_requirements))
    return PostingVerification(
        has_raw_text=bool(raw_text),
        recruiter_identifiers_detected=tuple(findings),
    )
