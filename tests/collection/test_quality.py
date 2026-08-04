"""DB-integration tests for post-hoc collection quality-assurance
utilities. Run against the shared throwaway PostgreSQL 16 cluster
(tests/conftest.py). No real personal data; all fixture text is
synthetic (CLAUDE_CODE_RULES.md rule 6).
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2

from alcsm.collection.helper import (
    JobPostingRecord,
    ProfileRecord,
    ProfileSection,
    complete_sampling_batch,
    insert_job_posting,
    insert_profile,
)
from alcsm.collection.quality import (
    check_batch_consistency,
    check_duplicate_consistency,
    check_required_metadata_present,
    check_section_completeness,
    count_records_for_batch,
)


def _profile(
    profile_id: str, sampling_batch_id: str, **overrides: object
) -> ProfileRecord:
    defaults: dict[str, object] = dict(
        profile_id=profile_id,
        sampling_batch_id=sampling_batch_id,
        search_query='"Chief AI Officer"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Chief AI Officer"),
            "about": ProfileSection(available=True, text="Self-taught."),
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
        search_query='"Head of AI"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        raw_posting_text="Seeking a Head of AI. TensorFlow experience preferred.",
    )
    defaults.update(overrides)
    return JobPostingRecord(**defaults)  # type: ignore[arg-type]


class TestCountRecordsForBatch:
    def test_zero_for_a_batch_with_no_records(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-607"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"unused query" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        count = count_records_for_batch(cur, batch_id, "job_posting")
        cur.close()
        assert count == 0

    def test_counts_inserted_profiles_for_the_given_batch(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        cur = db_connection.cursor()
        before = count_records_for_batch(cur, sampling_batch_id, "profile")
        cur.close()

        insert_profile(db_connection, _profile(unique_profile_id, sampling_batch_id))

        cur = db_connection.cursor()
        after = count_records_for_batch(cur, sampling_batch_id, "profile")
        cur.close()
        assert after == before + 1


class TestCheckBatchConsistency:
    def test_uncompleted_batch_is_not_flagged_inconsistent(
        self,
        db_connection: psycopg2.extensions.connection,
        job_posting_batch_id: str,
        unique_posting_id: str,
    ) -> None:
        insert_job_posting(
            db_connection, _posting(unique_posting_id, job_posting_batch_id)
        )
        report = check_batch_consistency(
            db_connection.cursor(), job_posting_batch_id, "job_posting"
        )
        assert report.declared_records_included is None
        assert report.consistent is True

    def test_completed_batch_with_matching_count_is_consistent(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-601"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"VP of AI" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        cur = db_connection.cursor()
        complete_sampling_batch(
            cur,
            batch_id,
            collection_ended_ts=datetime.now(UTC),
            result_set_size=1,
            records_included=1,
        )
        db_connection.commit()

        report = check_batch_consistency(cur, batch_id, "job_posting")
        cur.close()
        assert report.consistent is True
        assert report.actual_record_count == 1

    def test_completed_batch_with_mismatched_count_is_inconsistent(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-602"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"Director of AI" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        cur = db_connection.cursor()
        complete_sampling_batch(
            cur,
            batch_id,
            collection_ended_ts=datetime.now(UTC),
            result_set_size=5,
            records_included=5,  # wrong: only 1 was actually inserted
        )
        db_connection.commit()

        report = check_batch_consistency(cur, batch_id, "job_posting")
        cur.close()
        assert report.consistent is False
        assert report.actual_record_count == 1
        assert any("declared records_included=5" in p for p in report.problems)

    def test_nonexistent_batch_is_reported(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        report = check_batch_consistency(cur, "BATCH-DOES-NOT-EXIST", "job_posting")
        cur.close()
        assert report.consistent is False
        assert any("does not exist" in p for p in report.problems)


class TestCheckRequiredMetadataPresent:
    def test_fully_populated_batch_has_no_missing_metadata(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-604"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"AI Lead" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_job_posting(db_connection, _posting(unique_posting_id, batch_id))

        cur = db_connection.cursor()
        problems = check_required_metadata_present(cur, batch_id, "job_posting")
        cur.close()
        assert problems == []


class TestCheckSectionCompleteness:
    def test_completeness_reflects_available_sections(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_profile_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-603"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"AI Lead"',
                platform="linkedin",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_profile(
            db_connection,
            _profile(
                unique_profile_id,
                batch_id,
                sections={
                    "headline": ProfileSection(available=True, text="AI Lead"),
                },
            ),
        )

        cur = db_connection.cursor()
        completeness = check_section_completeness(cur, batch_id)
        cur.close()
        assert completeness["headline"] == 1.0
        assert completeness["education"] == 0.0

    def test_empty_batch_reports_zero_for_every_section(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        cur = db_connection.cursor()
        completeness = check_section_completeness(cur, "BATCH-DOES-NOT-EXIST")
        cur.close()
        assert all(v == 0.0 for v in completeness.values())


class TestCheckDuplicateConsistency:
    def test_no_duplicates_in_a_clean_batch(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-605"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"ML Lead" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_job_posting(
            db_connection,
            _posting(unique_posting_id, batch_id, search_rank_position=1),
        )
        cur = db_connection.cursor()
        problems = check_duplicate_consistency(cur, batch_id, "job_posting")
        cur.close()
        assert problems == []

    def test_two_records_sharing_a_rank_and_query_are_flagged(
        self,
        db_connection: psycopg2.extensions.connection,
        unique_posting_id: str,
    ) -> None:
        cur = db_connection.cursor()
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch_id = "BATCH-606"
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id=batch_id,
                search_query='"Data Science Lead" job',
                platform="job_board",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
                corpus="job_posting",
            ),
        )
        db_connection.commit()
        cur.close()

        insert_job_posting(
            db_connection,
            _posting(
                unique_posting_id,
                batch_id,
                search_query='"Data Science Lead" job',
                search_rank_position=1,
            ),
        )
        insert_job_posting(
            db_connection,
            _posting(
                "JOB-90002",
                batch_id,
                search_query='"Data Science Lead" job',
                search_rank_position=1,
            ),
        )
        cur = db_connection.cursor()
        problems = check_duplicate_consistency(cur, batch_id, "job_posting")
        cur.close()
        assert any("duplicate search_rank_position 1" in p for p in problems)
