"""CollectionManager: batch lifecycle, status, progress, and recovery.

Orchestrates the primitives already validated and tested elsewhere —
it never re-implements validation or insertion logic itself:

    - ``collection.helper`` — the single write path for both corpora
      (``create_sampling_batch``, ``complete_sampling_batch``,
      ``insert_profile``, ``insert_job_posting``, ``verify_profile``,
      ``verify_posting``);
    - ``collection.audit`` — GDPR-safe structured event recording;
    - ``collection.checkpoint`` — save/load/validate checkpoints;
    - ``collection.quality`` — post-hoc consistency checks.

This module adds the orchestration layer on top: what to call when,
what to log, and how to report current status — nothing here talks to
PostgreSQL directly except the small, already-tested queries in
``collection.quality`` that it delegates to.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from psycopg2.extensions import connection as PGConnection

from alcsm.collection.audit import AuditEvent, AuditLog, is_pseudonymous_id
from alcsm.collection.checkpoint import (
    CollectionCheckpoint,
    validate_checkpoint_against_database,
    validate_checkpoint_shape,
)
from alcsm.collection.helper import (
    JobPostingRecord,
    ProfileRecord,
    ProfileValidationError,
    Rq4Criterion,
    SamplingBatch,
    complete_sampling_batch,
    create_sampling_batch,
    insert_job_posting,
    insert_profile,
)
from alcsm.collection.helper import (
    JobPostingValidationError as _JobPostingValidationError,
)
from alcsm.collection.quality import count_records_for_batch
from alcsm.constants import Corpus
from alcsm.logging_config import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class BatchStatus:
    """Current lifecycle status of one batch, derived entirely from
    existing frozen schema fields — no new stored status column
    (PROJECT_CONTEXT.md §17: no schema change without approval).

    ``started`` / ``completed`` are derived from
    ``collection_started_ts`` / ``collection_ended_ts`` being set;
    ``completion_percentage`` is derived from ``records_included`` /
    ``result_set_size`` where both are known.
    """

    sampling_batch_id: str
    corpus: Corpus
    started: bool
    completed: bool
    actual_record_count: int
    result_set_size: int | None
    completion_percentage: float | None


class CollectionManager:
    """Coordinates batch lifecycle, progress tracking, and recovery
    for one corpus's collection session, on top of the validated
    write path in ``collection.helper``.
    """

    def __init__(self, conn: PGConnection, audit_log: AuditLog | None = None) -> None:
        self._conn = conn
        self.audit_log = audit_log if audit_log is not None else AuditLog()

    def start_batch(self, batch: SamplingBatch) -> bool:
        """Register a new batch and record a ``batch_created`` audit event."""
        cur = self._conn.cursor()
        try:
            created = create_sampling_batch(cur, batch)
            self._conn.commit()
        finally:
            cur.close()

        self.audit_log.record(
            AuditEvent(
                event_type="batch_created",
                entity_id=batch.sampling_batch_id,
                timestamp=datetime.now(UTC),
                details={"corpus": batch.corpus, "already_existed": not created},
            )
        )
        return created

    def complete_batch(
        self,
        sampling_batch_id: str,
        result_set_size: int | None = None,
        records_included: int | None = None,
        notes: str | None = None,
    ) -> bool:
        """Mark a batch as ended and record a ``batch_completed`` event."""
        cur = self._conn.cursor()
        try:
            completed = complete_sampling_batch(
                cur,
                sampling_batch_id,
                collection_ended_ts=datetime.now(UTC),
                result_set_size=result_set_size,
                records_included=records_included,
                notes=notes,
            )
            self._conn.commit()
        finally:
            cur.close()

        self.audit_log.record(
            AuditEvent(
                event_type="batch_completed",
                entity_id=sampling_batch_id,
                timestamp=datetime.now(UTC),
                details={"records_included": records_included},
            )
        )
        return completed

    def insert_profile(
        self, record: ProfileRecord, criterion: Rq4Criterion | None = None
    ) -> str:
        """Insert one profile via ``collection.helper.insert_profile``,
        recording a ``record_inserted`` or ``record_validation_failed``
        audit event either way.
        """
        try:
            profile_id = insert_profile(self._conn, record, criterion=criterion)
        except ProfileValidationError as exc:
            # A validation failure can itself be *because* the id is
            # malformed — never pass a non-pseudonymous-shaped id
            # through as entity_id, or recording the failure would
            # raise AuditLogError and mask the original error.
            safe_id = (
                record.profile_id if is_pseudonymous_id(record.profile_id) else None
            )
            self.audit_log.record(
                AuditEvent(
                    event_type="record_validation_failed",
                    entity_id=safe_id,
                    timestamp=datetime.now(UTC),
                    details={
                        "corpus": "profile",
                        "sampling_batch_id": record.sampling_batch_id,
                        "problem_count": len(exc.problems),
                    },
                )
            )
            raise
        self.audit_log.record(
            AuditEvent(
                event_type="record_inserted",
                entity_id=profile_id,
                timestamp=datetime.now(UTC),
                details={
                    "corpus": "profile",
                    "sampling_batch_id": record.sampling_batch_id,
                },
            )
        )
        return profile_id

    def insert_job_posting(self, record: JobPostingRecord) -> str:
        """Insert one job posting via
        ``collection.helper.insert_job_posting``, recording a
        ``record_inserted`` or ``record_validation_failed`` audit
        event either way.
        """
        try:
            posting_id = insert_job_posting(self._conn, record)
        except _JobPostingValidationError as exc:
            safe_id = (
                record.posting_id if is_pseudonymous_id(record.posting_id) else None
            )
            self.audit_log.record(
                AuditEvent(
                    event_type="record_validation_failed",
                    entity_id=safe_id,
                    timestamp=datetime.now(UTC),
                    details={
                        "corpus": "job_posting",
                        "sampling_batch_id": record.sampling_batch_id,
                        "problem_count": len(exc.problems),
                    },
                )
            )
            raise
        self.audit_log.record(
            AuditEvent(
                event_type="record_inserted",
                entity_id=posting_id,
                timestamp=datetime.now(UTC),
                details={
                    "corpus": "job_posting",
                    "sampling_batch_id": record.sampling_batch_id,
                },
            )
        )
        return posting_id

    def get_status(self, sampling_batch_id: str, corpus: Corpus) -> BatchStatus:
        """Return the current lifecycle status of a batch, derived
        from existing schema fields only.
        """
        cur = self._conn.cursor()
        try:
            cur.execute(
                """SELECT collection_started_ts, collection_ended_ts,
                          result_set_size
                   FROM alcsm.sampling_batch WHERE sampling_batch_id=%s""",
                (sampling_batch_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"sampling_batch_id {sampling_batch_id!r} not found")
            started_ts, ended_ts, result_set_size = row
            actual_count = count_records_for_batch(cur, sampling_batch_id, corpus)
        finally:
            cur.close()

        completion_percentage = None
        if result_set_size:
            completion_percentage = round(100.0 * actual_count / result_set_size, 2)

        return BatchStatus(
            sampling_batch_id=sampling_batch_id,
            corpus=corpus,
            started=started_ts is not None,
            completed=ended_ts is not None,
            actual_record_count=actual_count,
            result_set_size=result_set_size,
            completion_percentage=completion_percentage,
        )

    def resume_batch(self, checkpoint: CollectionCheckpoint) -> list[str]:
        """Validate a checkpoint against both its own shape and the
        live database before resuming (restart safety, Task 2).

        Returns every problem found (empty means safe to resume) and
        records a ``recovery_started`` audit event; a caller decides
        what "resuming" concretely means for their own collection
        loop — this method only certifies whether it is safe to do so.
        """
        self.audit_log.record(
            AuditEvent(
                event_type="recovery_started",
                entity_id=checkpoint.sampling_batch_id,
                timestamp=datetime.now(UTC),
                details={
                    "processed_count": len(checkpoint.processed_ids),
                    "failed_count": len(checkpoint.failed_ids),
                },
            )
        )

        problems = validate_checkpoint_shape(checkpoint)
        cur = self._conn.cursor()
        try:
            problems += validate_checkpoint_against_database(checkpoint, cur)
        finally:
            cur.close()

        if problems:
            self.audit_log.record(
                AuditEvent(
                    event_type="checkpoint_validation_failed",
                    entity_id=checkpoint.sampling_batch_id,
                    timestamp=datetime.now(UTC),
                    details={"problem_count": len(problems)},
                )
            )
        else:
            self.audit_log.record(
                AuditEvent(
                    event_type="recovery_completed",
                    entity_id=checkpoint.sampling_batch_id,
                    timestamp=datetime.now(UTC),
                    details={},
                )
            )
        return problems
