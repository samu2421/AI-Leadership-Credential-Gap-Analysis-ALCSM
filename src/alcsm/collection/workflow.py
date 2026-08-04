"""CollectionWorkflow: the end-to-end orchestrator over everything
already built in P3 Sessions 1-3.

Phase P3 Session 4's entire purpose is integration, not new
capability: this module coordinates batch lifecycle, insertion,
duplicate detection, checkpointing, recovery, quality assurance,
reporting, and export by delegating to the already-validated,
already-tested modules built earlier in P3 — it adds no new database
access, no new validation rule, and no new write path of its own.

    - ``collection.manager.CollectionManager`` — batch lifecycle,
      validated insertion, audited status.
    - ``collection.duplicates.DuplicateRegistry`` — session-local
      deterministic duplicate detection.
    - ``collection.checkpoint`` — save/load/validate checkpoints.
    - ``collection.quality`` — post-hoc consistency checks.
    - ``collection.reporting`` — operational reports.
    - ``collection.export`` — versioned metadata export.

A checkpoint's ``processed_ids``/``failed_ids`` are derived from the
workflow's own audit log (``record_inserted``/``record_validation_failed``
events already produced by ``CollectionManager``) rather than tracked
a second time — the audit trail is the single source of truth for
"what happened," matching Task 1's "delegate, do not duplicate."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from itertools import count
from pathlib import Path

from psycopg2.extensions import connection as PGConnection

from alcsm.collection.audit import AuditEvent, AuditEventType, AuditLog
from alcsm.collection.checkpoint import (
    CollectionCheckpoint,
    load_checkpoint,
    save_checkpoint,
)
from alcsm.collection.duplicates import DuplicateCandidate, DuplicateRegistry
from alcsm.collection.export import ExportManifest, export_batch_metadata
from alcsm.collection.helper import (
    JobPostingRecord,
    ProfileRecord,
    ProfileSection,
    Rq4Criterion,
    SamplingBatch,
)
from alcsm.collection.manager import BatchStatus, CollectionManager
from alcsm.collection.quality import (
    BatchConsistencyReport,
    check_batch_consistency,
    check_duplicate_consistency,
    check_required_metadata_present,
    check_section_completeness,
)
from alcsm.collection.reporting import CollectionReport, generate_batch_report
from alcsm.constants import Corpus
from alcsm.logging_config import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class QualitySummary:
    """The combined output of every post-hoc QA check for one batch —
    a single object a researcher (or the dry run) can inspect instead
    of calling each ``collection.quality`` function separately.
    """

    consistency: BatchConsistencyReport
    missing_metadata: tuple[str, ...]
    duplicate_problems: tuple[str, ...]
    section_completeness: dict[str, float] | None

    @property
    def is_clean(self) -> bool:
        return (
            self.consistency.consistent
            and not self.missing_metadata
            and not self.duplicate_problems
        )


class CollectionWorkflow:
    """Coordinates the complete collection lifecycle for one corpus's
    batch, by delegating to the modules already built in Sessions 1-3.
    """

    def __init__(self, conn: PGConnection, audit_log: AuditLog | None = None) -> None:
        self._conn = conn
        self.manager = CollectionManager(conn, audit_log=audit_log)
        self.duplicate_registry = DuplicateRegistry()

    @property
    def audit_log(self) -> AuditLog:
        return self.manager.audit_log

    # ------------------------------------------------------------------
    # Batch lifecycle
    # ------------------------------------------------------------------

    def start_batch(self, batch: SamplingBatch) -> bool:
        """Register a new batch. Delegates to
        ``CollectionManager.start_batch``."""
        return self.manager.start_batch(batch)

    def complete_batch(
        self,
        sampling_batch_id: str,
        result_set_size: int | None = None,
        records_included: int | None = None,
        notes: str | None = None,
    ) -> bool:
        """Mark a batch as ended. Delegates to
        ``CollectionManager.complete_batch``."""
        return self.manager.complete_batch(
            sampling_batch_id, result_set_size, records_included, notes
        )

    def get_status(self, sampling_batch_id: str, corpus: Corpus) -> BatchStatus:
        """Delegates to ``CollectionManager.get_status``."""
        return self.manager.get_status(sampling_batch_id, corpus)

    # ------------------------------------------------------------------
    # Record collection, with duplicate detection folded in
    # ------------------------------------------------------------------

    def collect_profile(
        self,
        record: ProfileRecord,
        candidate: DuplicateCandidate | None = None,
        criterion: Rq4Criterion | None = None,
    ) -> str | None:
        """Check for a duplicate (if ``candidate`` is given), then
        insert via ``CollectionManager.insert_profile``.

        Returns the inserted ``profile_id``, or ``None`` if the
        candidate was excluded as a session-local duplicate (in which
        case nothing is inserted and a ``duplicate_detected`` audit
        event is recorded instead).
        """
        if candidate is not None:
            check = self.duplicate_registry.check(candidate)
            if check.is_duplicate:
                self.audit_log.record(
                    AuditEvent(
                        event_type="duplicate_detected",
                        entity_id=None,
                        timestamp=datetime.now(UTC),
                        details={
                            "corpus": "profile",
                            "sampling_batch_id": record.sampling_batch_id,
                            "matched_on": check.matched_on,
                        },
                    )
                )
                return None

        profile_id = self.manager.insert_profile(record, criterion=criterion)
        if candidate is not None:
            self.duplicate_registry.register(candidate)
        return profile_id

    def collect_job_posting(
        self,
        record: JobPostingRecord,
        candidate: DuplicateCandidate | None = None,
    ) -> str | None:
        """Job-posting counterpart to :meth:`collect_profile`."""
        if candidate is not None:
            check = self.duplicate_registry.check(candidate)
            if check.is_duplicate:
                self.audit_log.record(
                    AuditEvent(
                        event_type="duplicate_detected",
                        entity_id=None,
                        timestamp=datetime.now(UTC),
                        details={
                            "corpus": "job_posting",
                            "sampling_batch_id": record.sampling_batch_id,
                            "matched_on": check.matched_on,
                        },
                    )
                )
                return None

        posting_id = self.manager.insert_job_posting(record)
        if candidate is not None:
            self.duplicate_registry.register(candidate)
        return posting_id

    # ------------------------------------------------------------------
    # Checkpoint and resume
    # ------------------------------------------------------------------

    def build_checkpoint(
        self, sampling_batch_id: str, corpus: Corpus
    ) -> CollectionCheckpoint:
        """Derive a checkpoint from this workflow's own audit log —
        the audit trail already records every successful and failed
        insert, so nothing is tracked twice.
        """

        def _ids(event_type: AuditEventType) -> tuple[str, ...]:
            return tuple(
                e.entity_id
                for e in self.audit_log.events_of_type(event_type)
                if e.entity_id is not None
                and e.details.get("sampling_batch_id") == sampling_batch_id
                and e.details.get("corpus") == corpus
            )

        return CollectionCheckpoint(
            sampling_batch_id=sampling_batch_id,
            corpus=corpus,
            processed_ids=_ids("record_inserted"),
            failed_ids=_ids("record_validation_failed"),
        )

    def save_checkpoint(
        self, sampling_batch_id: str, corpus: Corpus, path: Path
    ) -> CollectionCheckpoint:
        """Build and persist a checkpoint, recording a
        ``checkpoint_saved`` audit event.
        """
        checkpoint = self.build_checkpoint(sampling_batch_id, corpus)
        save_checkpoint(checkpoint, path)
        self.audit_log.record(
            AuditEvent(
                event_type="checkpoint_saved",
                entity_id=sampling_batch_id,
                timestamp=datetime.now(UTC),
                details={"processed_count": len(checkpoint.processed_ids)},
            )
        )
        return checkpoint

    def resume_from_checkpoint(self, path: Path) -> list[str]:
        """Load a checkpoint, record a ``checkpoint_loaded`` event, and
        validate it (shape + live-database cross-check) via
        ``CollectionManager.resume_batch``.

        Returns every problem found (empty means safe to resume).
        """
        checkpoint = load_checkpoint(path)
        self.audit_log.record(
            AuditEvent(
                event_type="checkpoint_loaded",
                entity_id=checkpoint.sampling_batch_id,
                timestamp=datetime.now(UTC),
                details={"processed_count": len(checkpoint.processed_ids)},
            )
        )
        return self.manager.resume_batch(checkpoint)

    # ------------------------------------------------------------------
    # Quality assurance, reporting, export
    # ------------------------------------------------------------------

    def run_quality_checks(
        self, sampling_batch_id: str, corpus: Corpus
    ) -> QualitySummary:
        """Run every applicable post-hoc QA check
        (``collection.quality``) and combine the results."""
        cur = self._conn.cursor()
        try:
            consistency = check_batch_consistency(cur, sampling_batch_id, corpus)
            missing_metadata = check_required_metadata_present(
                cur, sampling_batch_id, corpus
            )
            duplicate_problems = check_duplicate_consistency(
                cur, sampling_batch_id, corpus
            )
            section_completeness = (
                check_section_completeness(cur, sampling_batch_id)
                if corpus == "profile"
                else None
            )
        finally:
            cur.close()

        return QualitySummary(
            consistency=consistency,
            missing_metadata=tuple(missing_metadata),
            duplicate_problems=tuple(duplicate_problems),
            section_completeness=section_completeness,
        )

    def generate_report(
        self, sampling_batch_id: str, corpus: Corpus
    ) -> CollectionReport:
        """Delegates to ``collection.reporting.generate_batch_report``,
        using this workflow's own audit log for failure/duplicate counts."""
        cur = self._conn.cursor()
        try:
            return generate_batch_report(cur, sampling_batch_id, corpus, self.audit_log)
        finally:
            cur.close()

    def export_metadata(
        self, sampling_batch_id: str, corpus: Corpus, output_path: Path
    ) -> ExportManifest:
        """Delegates to ``collection.export.export_batch_metadata``."""
        cur = self._conn.cursor()
        try:
            return export_batch_metadata(cur, sampling_batch_id, corpus, output_path)
        finally:
            cur.close()


@dataclass(frozen=True)
class DryRunStep:
    """One completed step of the dry run, for a human-readable summary."""

    name: str
    detail: str


@dataclass(frozen=True)
class DryRunResult:
    """The complete outcome of :func:`run_dry_run`."""

    profile_batch_id: str
    posting_batch_id: str
    profile_ids: tuple[str, ...]
    posting_ids: tuple[str, ...]
    profile_quality: QualitySummary
    posting_quality: QualitySummary
    profile_report: CollectionReport
    posting_report: CollectionReport
    profile_export: ExportManifest
    posting_export: ExportManifest
    steps: tuple[DryRunStep, ...] = field(default_factory=tuple)


_dry_run_record_counter = count(1)


def run_dry_run(
    conn: PGConnection,
    export_dir: Path,
    profile_batch_id: str = "BATCH-990",
    posting_batch_id: str = "BATCH-991",
) -> DryRunResult:
    """Simulate a realistic collection session end to end, for both
    corpora, using only synthetic, constructed data.

    Follows exactly the flow demonstrated in
    Task5_P3_Researcher_Operations_Manual.md: start batch -> insert
    synthetic records -> checkpoint -> (simulated interruption) ->
    resume -> insert more records -> QA -> report -> export -> finish
    batch. No real profile or posting is collected, no network access
    occurs, and nothing here is a placeholder — every step below
    executes for real against whatever (throwaway) database ``conn``
    is connected to.

    ``profile_batch_id``/``posting_batch_id`` must each match the
    schema's ``BATCH-###`` shape (exactly three digits); the four
    inserted record ids are generated from a module-level counter so
    repeated calls within one process (e.g. two tests, or a script run
    twice) never collide on a primary key.
    """
    steps: list[DryRunStep] = []
    workflow = CollectionWorkflow(conn)

    def _next_id(prefix: str) -> str:
        # 96000+ is reserved for the dry run, clear of every hardcoded
        # id used elsewhere in the test suite (which cluster around
        # 90000-90002 and use 99999 only as a never-inserted phantom).
        return f"{prefix}-{96000 + next(_dry_run_record_counter):05d}"

    # --- Profile corpus -------------------------------------------------
    workflow.start_batch(
        SamplingBatch(
            sampling_batch_id=profile_batch_id,
            search_query='"Head of AI"',
            platform="linkedin",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0-DRYRUN",
        )
    )
    steps.append(DryRunStep("start_batch (profile)", profile_batch_id))

    first_profile = ProfileRecord(
        profile_id=_next_id("PRF"),
        sampling_batch_id=profile_batch_id,
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Head of AI at Acme"),
            "about": ProfileSection(
                available=True, text="Self-taught, no formal AI degree."
            ),
        },
    )
    first_profile_id = workflow.collect_profile(
        first_profile,
        candidate=DuplicateCandidate(title="Head of AI"),
    )
    steps.append(DryRunStep("insert synthetic profile", str(first_profile_id)))

    checkpoint_path = export_dir / f"{profile_batch_id}.checkpoint.json"
    workflow.save_checkpoint(profile_batch_id, "profile", checkpoint_path)
    steps.append(DryRunStep("checkpoint (profile)", str(checkpoint_path)))

    # Simulate an interruption: a brand-new workflow/manager instance
    # (a fresh audit log, as a new process would have) resumes from
    # the checkpoint just saved.
    resumed_workflow = CollectionWorkflow(conn)
    resume_problems = resumed_workflow.resume_from_checkpoint(checkpoint_path)
    steps.append(
        DryRunStep(
            "resume (profile)",
            "safe to resume" if not resume_problems else f"problems: {resume_problems}",
        )
    )

    second_profile = ProfileRecord(
        profile_id=_next_id("PRF"),
        sampling_batch_id=profile_batch_id,
        search_query='"Head of AI"',
        inclusion_reason="title_variant_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(
                available=True, text="Director of AI at OtherCo"
            ),
        },
    )
    second_profile_id = resumed_workflow.collect_profile(second_profile)
    steps.append(
        DryRunStep("insert additional synthetic profile", str(second_profile_id))
    )

    resumed_workflow.complete_batch(
        profile_batch_id, result_set_size=2, records_included=2
    )
    steps.append(DryRunStep("finish batch (profile)", profile_batch_id))

    profile_quality = resumed_workflow.run_quality_checks(profile_batch_id, "profile")
    steps.append(
        DryRunStep(
            "quality checks (profile)",
            "clean" if profile_quality.is_clean else "problems found",
        )
    )
    profile_report = resumed_workflow.generate_report(profile_batch_id, "profile")
    steps.append(DryRunStep("report (profile)", str(profile_report.records_processed)))
    profile_export = resumed_workflow.export_metadata(
        profile_batch_id, "profile", export_dir / f"{profile_batch_id}.export.json"
    )
    steps.append(DryRunStep("export (profile)", profile_export.output_path))

    # --- Job-posting corpus ----------------------------------------------
    workflow.start_batch(
        SamplingBatch(
            sampling_batch_id=posting_batch_id,
            search_query='"Head of AI" job',
            platform="job_board",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0-DRYRUN",
            corpus="job_posting",
        )
    )
    steps.append(DryRunStep("start_batch (job_posting)", posting_batch_id))

    first_posting = JobPostingRecord(
        posting_id=_next_id("JOB"),
        sampling_batch_id=posting_batch_id,
        posting_source="example_job_board",
        search_query='"Head of AI" job',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI. TensorFlow experience preferred.",
    )
    first_posting_id = workflow.collect_job_posting(
        first_posting,
        candidate=DuplicateCandidate(source="example_job_board", external_id="123"),
    )
    steps.append(DryRunStep("insert synthetic posting", str(first_posting_id)))

    posting_checkpoint_path = export_dir / f"{posting_batch_id}.checkpoint.json"
    workflow.save_checkpoint(posting_batch_id, "job_posting", posting_checkpoint_path)
    steps.append(DryRunStep("checkpoint (job_posting)", str(posting_checkpoint_path)))

    resumed_posting_workflow = CollectionWorkflow(conn)
    posting_resume_problems = resumed_posting_workflow.resume_from_checkpoint(
        posting_checkpoint_path
    )
    steps.append(
        DryRunStep(
            "resume (job_posting)",
            (
                "safe to resume"
                if not posting_resume_problems
                else f"problems: {posting_resume_problems}"
            ),
        )
    )

    second_posting = JobPostingRecord(
        posting_id=_next_id("JOB"),
        sampling_batch_id=posting_batch_id,
        posting_source="example_job_board",
        search_query='"Head of AI" job',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Director of AI needed. PyTorch and Kubernetes a plus.",
    )
    second_posting_id = resumed_posting_workflow.collect_job_posting(second_posting)
    steps.append(
        DryRunStep("insert additional synthetic posting", str(second_posting_id))
    )

    resumed_posting_workflow.complete_batch(
        posting_batch_id, result_set_size=2, records_included=2
    )
    steps.append(DryRunStep("finish batch (job_posting)", posting_batch_id))

    posting_quality = resumed_posting_workflow.run_quality_checks(
        posting_batch_id, "job_posting"
    )
    steps.append(
        DryRunStep(
            "quality checks (job_posting)",
            "clean" if posting_quality.is_clean else "problems found",
        )
    )
    posting_report = resumed_posting_workflow.generate_report(
        posting_batch_id, "job_posting"
    )
    steps.append(
        DryRunStep("report (job_posting)", str(posting_report.records_processed))
    )
    posting_export = resumed_posting_workflow.export_metadata(
        posting_batch_id,
        "job_posting",
        export_dir / f"{posting_batch_id}.export.json",
    )
    steps.append(DryRunStep("export (job_posting)", posting_export.output_path))

    return DryRunResult(
        profile_batch_id=profile_batch_id,
        posting_batch_id=posting_batch_id,
        profile_ids=tuple(
            i for i in (first_profile_id, second_profile_id) if i is not None
        ),
        posting_ids=tuple(
            i for i in (first_posting_id, second_posting_id) if i is not None
        ),
        profile_quality=profile_quality,
        posting_quality=posting_quality,
        profile_report=profile_report,
        posting_report=posting_report,
        profile_export=profile_export,
        posting_export=posting_export,
        steps=tuple(steps),
    )
