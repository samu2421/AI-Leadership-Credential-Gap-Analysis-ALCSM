"""DB-integration tests for operational collection reports.

Run against the shared throwaway PostgreSQL 16 cluster
(tests/conftest.py). These are operational status reports, not thesis
figures — tests confirm counts/percentages, never any ALCSM scoring.
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2

from alcsm.collection.audit import AuditEvent, AuditLog
from alcsm.collection.helper import (
    JobPostingRecord,
    SamplingBatch,
    complete_sampling_batch,
    create_sampling_batch,
    insert_job_posting,
)
from alcsm.collection.reporting import generate_batch_report, render_report_text


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


def _fresh_batch(cur, db_connection, batch_id: str) -> None:
    create_sampling_batch(
        cur,
        SamplingBatch(
            sampling_batch_id=batch_id,
            search_query='"Head of AI" job',
            platform="job_board",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
            corpus="job_posting",
        ),
    )
    db_connection.commit()


class TestGenerateBatchReportWithoutAuditLog:
    def test_records_processed_matches_actual_count(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-701"
        _fresh_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        cur = db_connection.cursor()
        report = generate_batch_report(cur, batch_id, "job_posting")
        cur.close()
        assert report.records_processed == 1
        assert report.validation_failures == 0
        assert report.duplicate_count == 0

    def test_completion_percentage_is_none_without_result_set_size(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-702"
        _fresh_batch(cur, db_connection, batch_id)
        report = generate_batch_report(cur, batch_id, "job_posting")
        cur.close()
        assert report.completion_percentage is None

    def test_completion_percentage_is_computed_once_result_set_size_is_known(
        self, db_connection: psycopg2.extensions.connection, unique_posting_id: str
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-703"
        _fresh_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        cur = db_connection.cursor()
        complete_sampling_batch(
            cur,
            batch_id,
            collection_ended_ts=datetime.now(UTC),
            result_set_size=4,
            records_included=1,
        )
        db_connection.commit()

        report = generate_batch_report(cur, batch_id, "job_posting")
        cur.close()
        assert report.completion_percentage == 25.0


class TestGenerateBatchReportWithAuditLog:
    def test_validation_failures_and_duplicates_come_from_the_audit_log(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-704"
        _fresh_batch(cur, db_connection, batch_id)
        cur.close()

        audit_log = AuditLog()
        audit_log.record(
            AuditEvent(
                event_type="record_validation_failed",
                entity_id=None,
                timestamp=datetime.now(UTC),
                details={"sampling_batch_id": batch_id},
            )
        )
        audit_log.record(
            AuditEvent(
                event_type="duplicate_detected",
                entity_id=None,
                timestamp=datetime.now(UTC),
                details={"sampling_batch_id": batch_id},
            )
        )
        audit_log.record(
            AuditEvent(
                event_type="duplicate_detected",
                entity_id=None,
                timestamp=datetime.now(UTC),
                details={"sampling_batch_id": "BATCH-OTHER"},
            )
        )

        cur = db_connection.cursor()
        report = generate_batch_report(cur, batch_id, "job_posting", audit_log)
        cur.close()
        assert report.validation_failures == 1
        assert report.duplicate_count == 1  # the BATCH-OTHER event must not count


class TestRenderReportText:
    def test_render_includes_batch_id_and_counts(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-705"
        _fresh_batch(cur, db_connection, batch_id)
        report = generate_batch_report(cur, batch_id, "job_posting")
        cur.close()

        text = render_report_text(report)
        assert batch_id in text
        assert "Records processed" in text
