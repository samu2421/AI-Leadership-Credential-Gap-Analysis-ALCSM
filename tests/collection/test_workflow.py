"""Comprehensive integration tests for CollectionWorkflow — full
end-to-end workflows, not individual functions.

Run against the shared throwaway PostgreSQL 16 cluster
(tests/conftest.py) — never against `alcsm_dev`, exactly as every
prior P3 session's tests. No real personal data anywhere
(CLAUDE_CODE_RULES.md rule 6): every profile/posting below is
synthetic, constructed fixture data.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import psycopg2
import pytest

from alcsm.collection.duplicates import DuplicateCandidate
from alcsm.collection.helper import (
    JobPostingRecord,
    ProfileRecord,
    ProfileSection,
    SamplingBatch,
)
from alcsm.collection.workflow import CollectionWorkflow, run_dry_run


def _profile_batch(batch_id: str) -> SamplingBatch:
    return SamplingBatch(
        sampling_batch_id=batch_id,
        search_query='"Head of AI"',
        platform="linkedin",
        collection_started_ts=datetime.now(UTC),
        inclusion_protocol_version="IP-1.0",
    )


def _posting_batch(batch_id: str) -> SamplingBatch:
    return SamplingBatch(
        sampling_batch_id=batch_id,
        search_query='"Head of AI" job',
        platform="job_board",
        collection_started_ts=datetime.now(UTC),
        inclusion_protocol_version="IP-1.0",
        corpus="job_posting",
    )


def _profile(
    profile_id: str, sampling_batch_id: str, **overrides: object
) -> ProfileRecord:
    defaults: dict[str, object] = dict(
        profile_id=profile_id,
        sampling_batch_id=sampling_batch_id,
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Head of AI"),
        },
    )
    defaults.update(overrides)
    return ProfileRecord(**defaults)  # type: ignore[arg-type]


def _posting(
    posting_id: str, sampling_batch_id: str, **overrides: object
) -> JobPostingRecord:
    defaults: dict[str, object] = dict(
        posting_id=posting_id,
        sampling_batch_id=sampling_batch_id,
        posting_source="example_job_board",
        search_query='"Head of AI" job',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI. TensorFlow experience preferred.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


class TestFullProfileCollectionWorkflow:
    def test_start_insert_complete_report_export(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        batch_id = "BATCH-920"
        workflow = CollectionWorkflow(db_connection)

        assert workflow.start_batch(_profile_batch(batch_id)) is True
        profile_id = workflow.collect_profile(_profile("PRF-80001", batch_id))
        assert profile_id == "PRF-80001"

        assert (
            workflow.complete_batch(batch_id, result_set_size=1, records_included=1)
            is True
        )

        status = workflow.get_status(batch_id, "profile")
        assert status.completed is True
        assert status.actual_record_count == 1

        quality = workflow.run_quality_checks(batch_id, "profile")
        assert quality.is_clean is True

        report = workflow.generate_report(batch_id, "profile")
        assert report.records_processed == 1

        manifest = workflow.export_metadata(
            batch_id, "profile", tmp_path / "profile_export.json"
        )
        assert manifest.record_count == 1


class TestFullJobPostingCollectionWorkflow:
    def test_start_insert_complete_report_export(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        batch_id = "BATCH-921"
        workflow = CollectionWorkflow(db_connection)

        assert workflow.start_batch(_posting_batch(batch_id)) is True
        posting_id = workflow.collect_job_posting(_posting("JOB-80001", batch_id))
        assert posting_id == "JOB-80001"

        workflow.complete_batch(batch_id, result_set_size=1, records_included=1)

        quality = workflow.run_quality_checks(batch_id, "job_posting")
        assert quality.is_clean is True
        assert quality.section_completeness is None  # postings have no sections

        report = workflow.generate_report(batch_id, "job_posting")
        assert report.records_processed == 1

        manifest = workflow.export_metadata(
            batch_id, "job_posting", tmp_path / "posting_export.json"
        )
        assert manifest.record_count == 1


class TestInterruptionAndResume:
    def test_checkpoint_then_resume_in_a_fresh_workflow(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        batch_id = "BATCH-922"
        first_workflow = CollectionWorkflow(db_connection)
        first_workflow.start_batch(_profile_batch(batch_id))
        first_workflow.collect_profile(_profile("PRF-80002", batch_id))

        checkpoint_path = tmp_path / "checkpoint.json"
        checkpoint = first_workflow.save_checkpoint(
            batch_id, "profile", checkpoint_path
        )
        assert checkpoint.processed_ids == ("PRF-80002",)

        # Simulate a new process: a fresh workflow with an empty audit log.
        second_workflow = CollectionWorkflow(db_connection)
        problems = second_workflow.resume_from_checkpoint(checkpoint_path)
        assert problems == []

        # Continue collecting after resume.
        second_workflow.collect_profile(_profile("PRF-80003", batch_id))
        second_workflow.complete_batch(batch_id, result_set_size=2, records_included=2)

        status = second_workflow.get_status(batch_id, "profile")
        assert status.actual_record_count == 2

    def test_resume_with_a_checkpoint_claiming_a_phantom_record_reports_problems(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        from alcsm.collection.checkpoint import CollectionCheckpoint, save_checkpoint

        batch_id = "BATCH-923"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_profile_batch(batch_id))

        bad_checkpoint = CollectionCheckpoint(
            sampling_batch_id=batch_id,
            corpus="profile",
            processed_ids=("PRF-99999",),  # never actually inserted
        )
        checkpoint_path = tmp_path / "bad_checkpoint.json"
        save_checkpoint(bad_checkpoint, checkpoint_path)

        problems = workflow.resume_from_checkpoint(checkpoint_path)
        assert len(problems) > 0
        assert workflow.audit_log.count_of_type("checkpoint_validation_failed") == 1


class TestDuplicateHandlingInWorkflow:
    def test_second_matching_candidate_is_excluded_not_inserted(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-924"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_posting_batch(batch_id))

        first = workflow.collect_job_posting(
            _posting("JOB-80002", batch_id),
            candidate=DuplicateCandidate(source="board_x", external_id="555"),
        )
        assert first == "JOB-80002"

        second = workflow.collect_job_posting(
            _posting("JOB-80003", batch_id),
            candidate=DuplicateCandidate(source="board_x", external_id="555"),
        )
        assert second is None  # excluded as a duplicate, never inserted

        status = workflow.get_status(batch_id, "job_posting")
        assert status.actual_record_count == 1

    def test_duplicate_exclusion_is_audited(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-925"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_posting_batch(batch_id))
        candidate = DuplicateCandidate(title="Head of AI")
        workflow.collect_job_posting(
            _posting("JOB-80004", batch_id), candidate=candidate
        )
        workflow.collect_job_posting(
            _posting("JOB-80005", batch_id), candidate=candidate
        )

        assert workflow.audit_log.count_of_type("duplicate_detected") == 1


class TestRollbackInWorkflow:
    def test_invalid_record_leaves_no_partial_row_and_reraises(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-926"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_profile_batch(batch_id))

        from alcsm.collection.helper import ProfileValidationError

        bad_record = _profile("NOT-VALID", batch_id)
        with pytest.raises(ProfileValidationError):
            workflow.collect_profile(bad_record)

        status = workflow.get_status(batch_id, "profile")
        assert status.actual_record_count == 0

    def test_foreign_key_violation_rolls_back_and_workflow_stays_usable(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        workflow = CollectionWorkflow(db_connection)
        bad_record = _profile("PRF-80006", "BATCH-DOES-NOT-EXIST")
        with pytest.raises(psycopg2.errors.ForeignKeyViolation):
            workflow.collect_profile(bad_record)

        # the connection/workflow must still be usable afterward
        batch_id = "BATCH-927"
        workflow.start_batch(_profile_batch(batch_id))
        good_id = workflow.collect_profile(_profile("PRF-80007", batch_id))
        assert good_id == "PRF-80007"


class TestQualityVerificationInWorkflow:
    def test_mismatched_records_included_is_flagged(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-928"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_profile_batch(batch_id))
        workflow.collect_profile(_profile("PRF-80008", batch_id))
        workflow.complete_batch(batch_id, result_set_size=5, records_included=5)

        quality = workflow.run_quality_checks(batch_id, "profile")
        assert quality.is_clean is False
        assert quality.consistency.consistent is False


class TestReportingInWorkflow:
    def test_report_reflects_validation_failures_and_duplicates(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-929"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_posting_batch(batch_id))

        candidate = DuplicateCandidate(title="Duplicate Role")
        workflow.collect_job_posting(
            _posting("JOB-80008", batch_id), candidate=candidate
        )
        workflow.collect_job_posting(
            _posting("JOB-80009", batch_id), candidate=candidate
        )

        from alcsm.collection.helper import JobPostingValidationError

        with pytest.raises(JobPostingValidationError):
            workflow.collect_job_posting(_posting("BAD-ID", batch_id))

        report = workflow.generate_report(batch_id, "job_posting")
        assert report.records_processed == 1
        assert report.duplicate_count == 1
        assert report.validation_failures == 1


class TestExportInWorkflow:
    def test_export_never_contains_raw_text(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        batch_id = "BATCH-930"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_posting_batch(batch_id))
        workflow.collect_job_posting(
            _posting(
                "JOB-80010",
                batch_id,
                raw_posting_text="This exact phrase must not leak into the export.",
            )
        )
        output_path = tmp_path / "export.json"
        workflow.export_metadata(batch_id, "job_posting", output_path)
        content = output_path.read_text()
        assert "must not leak into the export" not in content


class TestBatchCompletionInWorkflow:
    def test_completing_twice_is_a_no_op_the_second_time(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        batch_id = "BATCH-931"
        workflow = CollectionWorkflow(db_connection)
        workflow.start_batch(_profile_batch(batch_id))
        assert workflow.complete_batch(batch_id, records_included=0) is True
        assert workflow.complete_batch(batch_id, records_included=99) is False


class TestRunDryRun:
    """End-to-end execution of the full dry-run demonstration
    (Task 3), against the real schema on the throwaway cluster —
    the strongest proof available that the infrastructure behaves
    correctly without any real data."""

    def test_dry_run_completes_and_reports_two_records_per_corpus(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        result = run_dry_run(
            db_connection,
            tmp_path,
            profile_batch_id="BATCH-992",
            posting_batch_id="BATCH-993",
        )

        assert len(result.profile_ids) == 2
        assert len(result.posting_ids) == 2
        assert result.profile_quality.is_clean is True
        assert result.posting_quality.is_clean is True
        assert result.profile_report.records_processed == 2
        assert result.posting_report.records_processed == 2
        assert Path(result.profile_export.output_path).exists()
        assert Path(result.posting_export.output_path).exists()
        # every step in the documented flow actually ran
        step_names = [s.name for s in result.steps]
        assert "start_batch (profile)" in step_names
        assert "resume (profile)" in step_names
        assert "resume (job_posting)" in step_names
        assert "finish batch (profile)" in step_names
        assert "finish batch (job_posting)" in step_names

    def test_dry_run_exports_contain_no_raw_text(
        self, db_connection: psycopg2.extensions.connection, tmp_path: Path
    ) -> None:
        result = run_dry_run(
            db_connection,
            tmp_path,
            profile_batch_id="BATCH-994",
            posting_batch_id="BATCH-995",
        )
        posting_export_content = Path(result.posting_export.output_path).read_text()
        assert "TensorFlow experience preferred" not in posting_export_content
