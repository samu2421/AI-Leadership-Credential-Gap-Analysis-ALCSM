"""Operational collection reports.

These are operational status reports for the researcher running
collection — batches created, records processed, validation-failure
and duplicate counts, completion percentage — not thesis figures
(Task 6's explicit boundary). No plotting, no statistics beyond simple
counts and ratios, no ALCSM scoring of any kind.

Validation-failure and duplicate counts come from an :class:`AuditLog`
(Task 4), since a rejected/excluded candidate never reaches the
database and so cannot be counted from it; batch/record counts come
from the database directly via ``collection.quality``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from psycopg2.extensions import cursor as PGCursor

from alcsm.collection.audit import AuditLog
from alcsm.collection.quality import count_records_for_batch
from alcsm.constants import Corpus


@dataclass(frozen=True)
class CollectionReport:
    """A point-in-time operational summary for one batch."""

    sampling_batch_id: str
    corpus: Corpus
    records_processed: int
    validation_failures: int
    duplicate_count: int
    result_set_size: int | None
    completion_percentage: float | None
    generated_ts: datetime


def generate_batch_report(
    cur: PGCursor,
    sampling_batch_id: str,
    corpus: Corpus,
    audit_log: AuditLog | None = None,
) -> CollectionReport:
    """Build a :class:`CollectionReport` for one batch.

    ``audit_log`` is optional: without one, ``validation_failures``
    and ``duplicate_count`` are reported as 0 (unknown, not "none
    occurred") since that information genuinely does not exist outside
    an audit trail.
    """
    records_processed = count_records_for_batch(cur, sampling_batch_id, corpus)

    cur.execute(
        "SELECT result_set_size FROM alcsm.sampling_batch WHERE sampling_batch_id=%s",
        (sampling_batch_id,),
    )
    row = cur.fetchone()
    result_set_size = row[0] if row else None

    completion_percentage = None
    if result_set_size:
        completion_percentage = round(100.0 * records_processed / result_set_size, 2)

    if audit_log is None:
        validation_failures = 0
        duplicate_count = 0
    else:
        batch_events = [
            e
            for e in audit_log.events()
            if e.details.get("sampling_batch_id") == sampling_batch_id
        ]
        validation_failures = sum(
            1 for e in batch_events if e.event_type == "record_validation_failed"
        )
        duplicate_count = sum(
            1 for e in batch_events if e.event_type == "duplicate_detected"
        )

    return CollectionReport(
        sampling_batch_id=sampling_batch_id,
        corpus=corpus,
        records_processed=records_processed,
        validation_failures=validation_failures,
        duplicate_count=duplicate_count,
        result_set_size=result_set_size,
        completion_percentage=completion_percentage,
        generated_ts=datetime.now(UTC),
    )


def render_report_text(report: CollectionReport) -> str:
    """Human-readable, deterministic rendering of a report — for
    console/log output, never a thesis figure.
    """
    lines = [
        f"Collection Report — batch {report.sampling_batch_id} ({report.corpus})",
        f"  Records processed:      {report.records_processed}",
        f"  Result set size:        {report.result_set_size}",
        f"  Completion percentage:  {report.completion_percentage}",
        f"  Validation failures:    {report.validation_failures}",
        f"  Duplicates detected:    {report.duplicate_count}",
        f"  Generated:              {report.generated_ts.isoformat()}",
    ]
    return "\n".join(lines)
