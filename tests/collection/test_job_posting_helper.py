"""DB-integration tests for the job-posting write path.

Run against the shared throwaway PostgreSQL 16 cluster with the frozen
schema deployed (see tests/conftest.py) — never against the real
`alcsm_dev` database, and never with real personal data
(CLAUDE_CODE_RULES.md rule 6). These tests exercise real constraint
violations, real transaction rollback, and real duplicate handling,
mirroring test_helper.py's profile-side coverage exactly
(PROJECT_CONTEXT.md §33: "test against the specification").

Automatically skipped if no local PostgreSQL 16 binaries are found.
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2
import pytest

from alcsm.collection.helper import (
    JobPostingRecord,
    JobPostingValidationError,
    insert_job_posting,
    verify_posting,
)


def _record(
    posting_id: str, sampling_batch_id: str, **overrides: object
) -> JobPostingRecord:
    defaults: dict[str, object] = dict(
        posting_id=posting_id,
        sampling_batch_id=sampling_batch_id,
        posting_source="example_job_board",
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI to lead a 12-person applied-ML "
        "team. TensorFlow and Kubernetes experience preferred.",
        raw_requirements_text="5+ years AI/ML experience; team leadership required.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


class TestSuccessfulInsertion:
    def test_insert_job_posting_returns_the_posting_id(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = _record(unique_posting_id, job_posting_batch_id)
        result = insert_job_posting(db_connection, record)
        assert result == unique_posting_id

    def test_raw_posting_text_is_stored_verbatim(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = _record(unique_posting_id, job_posting_batch_id)
        insert_job_posting(db_connection, record)
        cur = db_connection.cursor()
        cur.execute(
            "SELECT raw_posting_text FROM alcsm.job_posting WHERE posting_id=%s",
            (unique_posting_id,),
        )
        (stored_text,) = cur.fetchone()
        cur.close()
        assert stored_text == record.raw_posting_text

    def test_optional_fields_default_correctly(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = _record(unique_posting_id, job_posting_batch_id)
        insert_job_posting(db_connection, record)
        cur = db_connection.cursor()
        cur.execute(
            """SELECT posting_language, posting_geography, posted_date,
                      seniority_label_raw
               FROM alcsm.job_posting WHERE posting_id=%s""",
            (unique_posting_id,),
        )
        row = cur.fetchone()
        cur.close()
        assert row == ("und", None, None, None)


class TestProvenanceRecording:
    def test_provenance_fields_persist_exactly_as_given(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = _record(
            unique_posting_id,
            job_posting_batch_id,
            search_rank_position=2,
            posting_language="en",
            posting_geography="DE",
        )
        insert_job_posting(db_connection, record)
        cur = db_connection.cursor()
        cur.execute(
            """SELECT sampling_batch_id, posting_source, search_query,
                      search_rank_position, inclusion_reason,
                      posting_language, posting_geography
               FROM alcsm.job_posting WHERE posting_id=%s""",
            (unique_posting_id,),
        )
        row = cur.fetchone()
        cur.close()
        assert row == (
            job_posting_batch_id,
            "example_job_board",
            '"Head of AI"',
            2,
            "title_match",
            "en",
            "DE",
        )

    def test_posting_traces_back_to_its_sampling_batch(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        """PROJECT_CONTEXT.md §13/§14: every collected record traces back
        to the documented search that found it."""
        insert_job_posting(
            db_connection, _record(unique_posting_id, job_posting_batch_id)
        )
        cur = db_connection.cursor()
        cur.execute(
            """SELECT sb.corpus FROM alcsm.job_posting jp
               JOIN alcsm.sampling_batch sb
                 ON sb.sampling_batch_id = jp.sampling_batch_id
               WHERE jp.posting_id = %s""",
            (unique_posting_id,),
        )
        (corpus,) = cur.fetchone()
        cur.close()
        assert corpus == "job_posting"


class TestVerification:
    def test_verify_posting_reports_raw_text_present(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        insert_job_posting(
            db_connection, _record(unique_posting_id, job_posting_batch_id)
        )
        verification = verify_posting(db_connection, unique_posting_id)
        assert verification.has_raw_text is True
        assert verification.recruiter_identifiers_detected == ()

    def test_verify_posting_on_nonexistent_id_reports_no_text(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        verification = verify_posting(db_connection, "JOB-99999")
        assert verification.has_raw_text is False


class TestDuplicateHandling:
    def test_duplicate_posting_id_is_rejected_by_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        insert_job_posting(
            db_connection, _record(unique_posting_id, job_posting_batch_id)
        )
        with pytest.raises(psycopg2.errors.UniqueViolation):
            insert_job_posting(
                db_connection, _record(unique_posting_id, job_posting_batch_id)
            )


class TestTransactionRollback:
    def test_failed_insert_leaves_no_partial_rows(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        """A DB-level constraint violation not caught by Python-level
        validation (here: a nonexistent sampling_batch_id, an FK
        violation) must roll back the whole posting insert."""
        record = _record(unique_posting_id, "BATCH-999-DOES-NOT-EXIST")
        with pytest.raises(psycopg2.errors.ForeignKeyViolation):
            insert_job_posting(db_connection, record)

        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.job_posting WHERE posting_id=%s",
            (unique_posting_id,),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0

    def test_connection_is_reusable_after_a_rolled_back_insert(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        bad_record = _record(unique_posting_id, "BATCH-999-DOES-NOT-EXIST")
        with pytest.raises(psycopg2.errors.ForeignKeyViolation):
            insert_job_posting(db_connection, bad_record)

        good_id = "JOB-90001"
        good_record = _record(good_id, job_posting_batch_id)
        assert insert_job_posting(db_connection, good_record) == good_id


class TestValidationFailuresBlockTheDatabase:
    def test_invalid_record_never_reaches_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
    ) -> None:
        record = _record("NOT-A-VALID-ID", job_posting_batch_id)
        with pytest.raises(JobPostingValidationError):
            insert_job_posting(db_connection, record)

        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.job_posting WHERE posting_id=%s",
            ("NOT-A-VALID-ID",),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0

    def test_recruiter_email_in_posting_text_never_reaches_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        record = _record(
            unique_posting_id,
            job_posting_batch_id,
            raw_posting_text="Great role, apply to jane@acme.com directly.",
        )
        with pytest.raises(JobPostingValidationError):
            insert_job_posting(db_connection, record)

        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.job_posting WHERE posting_id=%s",
            (unique_posting_id,),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0
