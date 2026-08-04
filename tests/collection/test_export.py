"""DB-integration tests for metadata export infrastructure.

No real dataset is exported anywhere in these tests — every export
below is of constructed, synthetic fixture data to a temporary path
(pytest's `tmp_path`), confirming the export contains only the
allow-listed metadata columns and never raw posting/profile text.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import psycopg2

from alcsm.collection.export import EXPORT_FORMAT_VERSION, export_batch_metadata
from alcsm.collection.helper import (
    JobPostingRecord,
    SamplingBatch,
    create_sampling_batch,
    insert_job_posting,
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
        raw_posting_text="Seeking a Head of AI. This text must never be exported.",
        raw_requirements_text="5+ years AI/ML experience required for this role.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


def _fresh_job_posting_batch(cur, db_connection, batch_id: str) -> None:
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


class TestExportBatchMetadata:
    def test_export_writes_a_file_with_the_expected_record_count(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
        tmp_path: Path,
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-801"
        _fresh_job_posting_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        output_path = tmp_path / "export.json"
        cur = db_connection.cursor()
        manifest = export_batch_metadata(cur, batch_id, "job_posting", output_path)
        cur.close()

        assert manifest.record_count == 1
        assert output_path.exists()

    def test_exported_file_never_contains_raw_posting_text(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
        tmp_path: Path,
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-802"
        _fresh_job_posting_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        output_path = tmp_path / "export.json"
        cur = db_connection.cursor()
        export_batch_metadata(cur, batch_id, "job_posting", output_path)
        cur.close()

        content = output_path.read_text()
        assert "must never be exported" not in content
        assert "5+ years AI/ML experience" not in content
        assert "raw_posting_text" not in content
        assert "raw_requirements_text" not in content

    def test_exported_file_contains_the_expected_metadata_fields(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
        tmp_path: Path,
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-803"
        _fresh_job_posting_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        output_path = tmp_path / "export.json"
        cur = db_connection.cursor()
        export_batch_metadata(cur, batch_id, "job_posting", output_path)
        cur.close()

        payload = json.loads(output_path.read_text())
        assert payload["export_format_version"] == EXPORT_FORMAT_VERSION
        assert payload["sampling_batch_id"] == batch_id
        assert payload["record_count"] == 1
        record = payload["records"][0]
        assert record["posting_id"] == unique_posting_id
        assert record["posting_source"] == "example_job_board"
        assert "raw_posting_text" not in record

    def test_export_is_deterministic_for_the_same_database_state(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
        tmp_path: Path,
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-804"
        _fresh_job_posting_batch(cur, db_connection, batch_id)
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        first_path = tmp_path / "export1.json"
        second_path = tmp_path / "export2.json"
        cur = db_connection.cursor()
        export_batch_metadata(cur, batch_id, "job_posting", first_path)
        export_batch_metadata(cur, batch_id, "job_posting", second_path)
        cur.close()

        first = json.loads(first_path.read_text())
        second = json.loads(second_path.read_text())
        assert first["records"] == second["records"]

    def test_export_manifest_reports_the_output_path(
        self,
        db_connection: psycopg2.extensions.connection,
        tmp_path: Path,
    ) -> None:
        cur = db_connection.cursor()
        batch_id = "BATCH-805"
        _fresh_job_posting_batch(cur, db_connection, batch_id)
        output_path = tmp_path / "export.json"
        manifest = export_batch_metadata(cur, batch_id, "job_posting", output_path)
        cur.close()
        assert manifest.output_path == str(output_path)
        assert manifest.record_count == 0
