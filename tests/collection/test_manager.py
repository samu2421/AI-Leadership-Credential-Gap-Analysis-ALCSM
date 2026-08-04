"""DB-integration tests for CollectionManager: batch lifecycle, status,
progress, recovery, and the audit trail it produces. Runs against the
shared throwaway PostgreSQL 16 cluster (tests/conftest.py). No real
collection occurs — every record below is synthetic.
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2
import pytest

from alcsm.collection.checkpoint import CollectionCheckpoint
from alcsm.collection.helper import (
    JobPostingRecord,
    JobPostingValidationError,
    SamplingBatch,
)
from alcsm.collection.manager import CollectionManager


def _batch(batch_id: str) -> SamplingBatch:
    return SamplingBatch(
        sampling_batch_id=batch_id,
        search_query='"Head of AI" job',
        platform="job_board",
        collection_started_ts=datetime.now(UTC),
        inclusion_protocol_version="IP-1.0",
        corpus="job_posting",
    )


def _posting(
    posting_id: str, sampling_batch_id: str, **overrides: object
) -> JobPostingRecord:
    defaults: dict[str, object] = dict(
        posting_id=posting_id,
        sampling_batch_id=sampling_batch_id,
        posting_source="example_job_board",
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI. TensorFlow experience preferred.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


class TestBatchLifecycle:
    def test_start_batch_registers_a_new_batch(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        assert manager.start_batch(_batch("BATCH-901")) is True

    def test_start_batch_is_idempotent(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        batch = _batch("BATCH-902")
        assert manager.start_batch(batch) is True
        assert manager.start_batch(batch) is False

    def test_start_batch_records_a_batch_created_audit_event(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-903"))
        events = manager.audit_log.events_of_type("batch_created")
        assert len(events) == 1
        assert events[0].entity_id == "BATCH-903"

    def test_complete_batch_marks_the_batch_ended(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-904"))
        completed = manager.complete_batch(
            "BATCH-904", result_set_size=10, records_included=0
        )
        assert completed is True

    def test_complete_batch_records_a_batch_completed_audit_event(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-905"))
        manager.complete_batch("BATCH-905", result_set_size=1, records_included=1)
        events = manager.audit_log.events_of_type("batch_completed")
        assert len(events) == 1
        assert events[0].entity_id == "BATCH-905"

    def test_complete_batch_twice_is_a_no_op_the_second_time(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-906"))
        assert manager.complete_batch("BATCH-906", records_included=0) is True
        assert manager.complete_batch("BATCH-906", records_included=99) is False


class TestInsertProfileAndJobPostingViaManager:
    def test_insert_job_posting_returns_the_posting_id(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-907"))
        result = manager.insert_job_posting(_posting(unique_posting_id, "BATCH-907"))
        assert result == unique_posting_id

    def test_successful_insert_records_a_record_inserted_event(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-908"))
        manager.insert_job_posting(_posting(unique_posting_id, "BATCH-908"))
        events = manager.audit_log.events_of_type("record_inserted")
        assert any(e.entity_id == unique_posting_id for e in events)

    def test_failed_validation_records_a_validation_failed_event_and_reraises(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-909"))
        bad_record = _posting("NOT-A-VALID-ID", "BATCH-909")
        with pytest.raises(JobPostingValidationError):
            manager.insert_job_posting(bad_record)
        events = manager.audit_log.events_of_type("record_validation_failed")
        assert len(events) == 1
        assert events[0].details["corpus"] == "job_posting"


class TestGetStatus:
    def test_status_before_completion(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-910"))
        manager.insert_job_posting(_posting(unique_posting_id, "BATCH-910"))

        status = manager.get_status("BATCH-910", "job_posting")
        assert status.started is True
        assert status.completed is False
        assert status.actual_record_count == 1

    def test_status_after_completion_with_percentage(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-911"))
        manager.insert_job_posting(_posting(unique_posting_id, "BATCH-911"))
        manager.complete_batch("BATCH-911", result_set_size=4, records_included=1)

        status = manager.get_status("BATCH-911", "job_posting")
        assert status.completed is True
        assert status.completion_percentage == 25.0

    def test_status_for_unknown_batch_raises(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        with pytest.raises(ValueError):
            manager.get_status("BATCH-DOES-NOT-EXIST", "job_posting")


class TestResumeBatch:
    def test_resume_with_a_valid_checkpoint_reports_no_problems(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-912"))
        manager.insert_job_posting(_posting(unique_posting_id, "BATCH-912"))

        checkpoint = CollectionCheckpoint(
            sampling_batch_id="BATCH-912",
            corpus="job_posting",
            processed_ids=(unique_posting_id,),
        )
        problems = manager.resume_batch(checkpoint)
        assert problems == []

    def test_resume_records_recovery_started_and_completed_events(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-913"))
        manager.insert_job_posting(_posting(unique_posting_id, "BATCH-913"))

        checkpoint = CollectionCheckpoint(
            sampling_batch_id="BATCH-913",
            corpus="job_posting",
            processed_ids=(unique_posting_id,),
        )
        manager.resume_batch(checkpoint)
        assert manager.audit_log.count_of_type("recovery_started") == 1
        assert manager.audit_log.count_of_type("recovery_completed") == 1

    def test_resume_with_a_stale_checkpoint_reports_problems_and_logs_failure(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-914"))

        checkpoint = CollectionCheckpoint(
            sampling_batch_id="BATCH-914",
            corpus="job_posting",
            processed_ids=("JOB-99999",),  # never actually inserted
        )
        problems = manager.resume_batch(checkpoint)
        assert len(problems) > 0
        assert manager.audit_log.count_of_type("checkpoint_validation_failed") == 1
        assert manager.audit_log.count_of_type("recovery_completed") == 0


class TestManagerReusesHelperNotDuplicatesIt:
    """Task 1's explicit instruction: CollectionManager must not
    duplicate logic already in helper.py. These tests confirm the
    manager's insert path enforces the exact same validation rules as
    calling helper.insert_job_posting directly — i.e. it delegates
    rather than reimplements."""

    def test_manager_enforces_the_same_recruiter_privacy_rule_as_helper(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        manager = CollectionManager(db_connection)
        manager.start_batch(_batch("BATCH-915"))
        record = _posting(
            unique_posting_id,
            "BATCH-915",
            raw_posting_text="Great role, contact jane@acme.com directly.",
        )
        with pytest.raises(JobPostingValidationError):
            manager.insert_job_posting(record)
