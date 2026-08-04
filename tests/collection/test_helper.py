"""DB-integration tests for the collection helper.

Run against a throwaway PostgreSQL 16 cluster with the frozen schema
deployed (see conftest.py) — never against the real `alcsm_dev`
database, and never with real personal data (CLAUDE_CODE_RULES.md
rule 6). These tests exercise real constraint violations, real
transaction rollback, and real duplicate handling, per
PROJECT_CONTEXT.md §33 ("test against the specification"): mocking
the database here would only prove a mock behaves as expected, not
that this module interacts with PostgreSQL correctly.

Automatically skipped if no local PostgreSQL 16 binaries are found.
"""

from __future__ import annotations

from datetime import UTC, datetime

import psycopg2
import pytest

from alcsm.collection.helper import (
    ProfileRecord,
    ProfileSection,
    ProfileValidationError,
    Rq4Criterion,
    insert_profile,
    verify_profile,
)


def _record(
    profile_id: str, sampling_batch_id: str, **overrides: object
) -> ProfileRecord:
    defaults: dict[str, object] = dict(
        profile_id=profile_id,
        sampling_batch_id=sampling_batch_id,
        search_query='"Chief AI Officer"',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Chief AI Officer at Acme"),
            "about": ProfileSection(
                available=True, text="Self-taught, no formal AI degree."
            ),
            "education": ProfileSection(available=False, text=None),
        },
    )
    defaults.update(overrides)
    return ProfileRecord(**defaults)  # type: ignore[arg-type]


class TestSuccessfulInsertion:
    def test_insert_profile_returns_the_profile_id(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        record = _record(unique_profile_id, sampling_batch_id)
        result = insert_profile(db_connection, record)
        assert result == unique_profile_id

    def test_all_seven_sections_are_written(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        record = _record(unique_profile_id, sampling_batch_id)
        insert_profile(db_connection, record)
        verification = verify_profile(db_connection, unique_profile_id)
        assert verification.section_count == 7
        assert verification.coherent is True

    def test_unspecified_sections_default_to_unavailable(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        record = _record(unique_profile_id, sampling_batch_id, sections={})
        insert_profile(db_connection, record)
        cur = db_connection.cursor()
        cur.execute(
            "SELECT section_available FROM alcsm.profile_raw_section "
            "WHERE profile_id=%s AND section_name='certifications'",
            (unique_profile_id,),
        )
        (available,) = cur.fetchone()
        cur.close()
        assert available is False

    def test_rq4_criterion_is_stored_isolated_from_scoring(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        record = _record(unique_profile_id, sampling_batch_id)
        criterion = Rq4Criterion(
            extraction_method="manual",
            extraction_ts=datetime.now(UTC),
            network_reach=5000,
            content_engagement=12.5,
            content_post_count=10,
            observation_window_days=90,
        )
        insert_profile(db_connection, record, criterion=criterion)
        cur = db_connection.cursor()
        cur.execute(
            "SELECT rq4_network_reach FROM alcsm.rq4_impact_indicator "
            "WHERE profile_id=%s",
            (unique_profile_id,),
        )
        (reach,) = cur.fetchone()
        cur.close()
        assert reach == 5000

    def test_insert_without_criterion_leaves_rq4_table_empty_for_that_profile(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))
        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.rq4_impact_indicator WHERE profile_id=%s",
            (unique_profile_id,),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0


class TestProvenanceRecording:
    def test_provenance_fields_persist_exactly_as_given(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        record = _record(
            unique_profile_id,
            sampling_batch_id,
            search_rank_position=3,
            profile_language="en",
            profile_geography="DE",
            observation_window_days=30,
        )
        insert_profile(db_connection, record)
        cur = db_connection.cursor()
        cur.execute(
            """SELECT sampling_batch_id, search_query, search_rank_position,
                      inclusion_reason, profile_language, profile_geography,
                      observation_window_days
               FROM alcsm.profile WHERE profile_id=%s""",
            (unique_profile_id,),
        )
        row = cur.fetchone()
        cur.close()
        assert row == (
            sampling_batch_id,
            '"Chief AI Officer"',
            3,
            "title_match",
            "en",
            "DE",
            30,
        )

    def test_profile_traces_back_to_its_sampling_batch(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        """PROJECT_CONTEXT.md §13/§14: every collected record traces back
        to the documented search that found it."""
        insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))
        cur = db_connection.cursor()
        cur.execute(
            """SELECT sb.search_query FROM alcsm.profile p
               JOIN alcsm.sampling_batch sb
                 ON sb.sampling_batch_id = p.sampling_batch_id
               WHERE p.profile_id = %s""",
            (unique_profile_id,),
        )
        (search_query,) = cur.fetchone()
        cur.close()
        assert search_query == '"Chief AI Officer"'


class TestPseudonymisationWorkflow:
    def test_no_direct_identifier_column_exists_to_receive_a_name(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        """The schema itself has no column for a name/URL/photo/contact
        detail on `profile` — confirmed structurally, not just by
        convention (PROJECT_CONTEXT.md §45)."""
        insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))
        cur = db_connection.cursor()
        cur.execute(
            """SELECT column_name FROM information_schema.columns
               WHERE table_schema='alcsm' AND table_name='profile'"""
        )
        columns = {row[0] for row in cur.fetchall()}
        cur.close()
        forbidden = {
            "name",
            "full_name",
            "profile_url",
            "url",
            "photo",
            "email",
            "phone",
        }
        assert columns.isdisjoint(forbidden)

    def test_only_a_pseudonymous_id_identifies_the_record(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))
        cur = db_connection.cursor()
        cur.execute(
            "SELECT profile_id FROM alcsm.profile WHERE profile_id=%s",
            (unique_profile_id,),
        )
        (stored_id,) = cur.fetchone()
        cur.close()
        assert stored_id == unique_profile_id
        assert stored_id.startswith("PRF-")


class TestDuplicateHandling:
    def test_duplicate_profile_id_is_rejected_by_the_database(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))
        with pytest.raises(psycopg2.errors.UniqueViolation):
            insert_profile(db_connection, _record(unique_profile_id, sampling_batch_id))

    def test_sampling_batch_registration_is_idempotent(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch = SamplingBatch(
            sampling_batch_id="BATCH-002",
            search_query='"VP of AI"',
            platform="linkedin",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
        )
        cur = db_connection.cursor()
        first = create_sampling_batch(cur, batch)
        db_connection.commit()
        second = create_sampling_batch(cur, batch)
        db_connection.commit()
        cur.close()
        assert first is True
        assert second is False


class TestTransactionRollback:
    def test_failed_insert_leaves_no_partial_rows(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        """A DB-level constraint violation not caught by Python-level
        validation (here: a nonexistent sampling_batch_id, an FK
        violation) must roll back the *whole* profile — no orphaned
        profile row and no orphaned section rows (PROJECT_CONTEXT.md §32)."""
        record = _record(unique_profile_id, "BATCH-999-DOES-NOT-EXIST")
        with pytest.raises(psycopg2.errors.ForeignKeyViolation):
            insert_profile(db_connection, record)

        # The connection is usable again (rollback happened) and no rows exist.
        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.profile WHERE profile_id=%s",
            (unique_profile_id,),
        )
        (profile_count,) = cur.fetchone()
        cur.execute(
            "SELECT count(*) FROM alcsm.profile_raw_section WHERE profile_id=%s",
            (unique_profile_id,),
        )
        (section_count,) = cur.fetchone()
        cur.close()
        assert profile_count == 0
        assert section_count == 0

    def test_connection_is_reusable_after_a_rolled_back_insert(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
        unique_profile_id: str,
    ) -> None:
        bad_record = _record(f"{unique_profile_id}", "BATCH-999-DOES-NOT-EXIST")
        with pytest.raises(psycopg2.errors.ForeignKeyViolation):
            insert_profile(db_connection, bad_record)

        good_id = "PRF-90001"
        good_record = _record(good_id, sampling_batch_id)
        assert insert_profile(db_connection, good_record) == good_id


class TestValidationFailuresBlockTheDatabase:
    def test_invalid_record_never_reaches_the_database(
        self, db_connection: psycopg2.extensions.connection, sampling_batch_id: str
    ) -> None:
        record = _record("NOT-A-VALID-ID", sampling_batch_id)
        with pytest.raises(ProfileValidationError):
            insert_profile(db_connection, record)

        cur = db_connection.cursor()
        cur.execute(
            "SELECT count(*) FROM alcsm.profile WHERE profile_id=%s",
            ("NOT-A-VALID-ID",),
        )
        (count,) = cur.fetchone()
        cur.close()
        assert count == 0


class TestSamplingBatchCorpusGeneralization:
    """Phase P3 Session 2: `SamplingBatch`/`create_sampling_batch` were
    generalised from a hard-coded `corpus='profile'` assumption to
    accept either corpus. These tests confirm both the new behaviour
    and that existing profile-side behaviour is unchanged (backward
    compatibility, Task 4's explicit requirement).
    """

    def test_sampling_batch_defaults_to_profile_corpus(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        """A `SamplingBatch` built with no `corpus=` argument (the
        pre-Session-2 calling convention, used throughout the rest of
        this file) must still register as `corpus='profile'`."""
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch = SamplingBatch(
            sampling_batch_id="BATCH-501",
            search_query='"Director of AI"',
            platform="linkedin",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
        )
        cur = db_connection.cursor()
        create_sampling_batch(cur, batch)
        db_connection.commit()
        cur.execute(
            "SELECT corpus FROM alcsm.sampling_batch WHERE sampling_batch_id=%s",
            ("BATCH-501",),
        )
        (corpus,) = cur.fetchone()
        cur.close()
        assert corpus == "profile"

    def test_sampling_batch_accepts_job_posting_corpus(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import SamplingBatch, create_sampling_batch

        batch = SamplingBatch(
            sampling_batch_id="BATCH-502",
            search_query='"Director of AI" job',
            platform="job_board",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
            corpus="job_posting",
        )
        cur = db_connection.cursor()
        create_sampling_batch(cur, batch)
        db_connection.commit()
        cur.execute(
            "SELECT corpus FROM alcsm.sampling_batch WHERE sampling_batch_id=%s",
            ("BATCH-502",),
        )
        (corpus,) = cur.fetchone()
        cur.close()
        assert corpus == "job_posting"

    def test_profile_batch_fixture_still_registers_as_profile_corpus(
        self,
        db_connection: psycopg2.extensions.connection,
        sampling_batch_id: str,
    ) -> None:
        """Regression guard: the existing `sampling_batch_id` fixture
        (BATCH-001, used throughout this file's profile tests) must
        still be a `corpus='profile'` row after the generalisation."""
        cur = db_connection.cursor()
        cur.execute(
            "SELECT corpus FROM alcsm.sampling_batch WHERE sampling_batch_id=%s",
            (sampling_batch_id,),
        )
        (corpus,) = cur.fetchone()
        cur.close()
        assert corpus == "profile"


class TestCompleteSamplingBatch:
    """Phase P3 Session 3: `complete_sampling_batch` is the lifecycle
    counterpart to `create_sampling_batch` — these tests exercise it
    directly, alongside its sibling function's existing coverage
    above."""

    def test_completes_a_started_batch(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import (
            SamplingBatch,
            complete_sampling_batch,
            create_sampling_batch,
        )

        cur = db_connection.cursor()
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id="BATCH-503",
                search_query='"AI Lead"',
                platform="linkedin",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
            ),
        )
        db_connection.commit()

        completed = complete_sampling_batch(
            cur,
            "BATCH-503",
            collection_ended_ts=datetime.now(UTC),
            result_set_size=10,
            records_included=8,
            notes="test completion",
        )
        db_connection.commit()
        cur.close()
        assert completed is True

    def test_completed_batch_persists_its_counts(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import (
            SamplingBatch,
            complete_sampling_batch,
            create_sampling_batch,
        )

        cur = db_connection.cursor()
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id="BATCH-504",
                search_query='"Director of AI"',
                platform="linkedin",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
            ),
        )
        db_connection.commit()

        complete_sampling_batch(
            cur,
            "BATCH-504",
            collection_ended_ts=datetime.now(UTC),
            result_set_size=20,
            records_included=15,
        )
        db_connection.commit()
        cur.execute(
            """SELECT result_set_size, records_included, collection_ended_ts
               FROM alcsm.sampling_batch WHERE sampling_batch_id=%s""",
            ("BATCH-504",),
        )
        result_set_size, records_included, ended_ts = cur.fetchone()
        cur.close()
        assert result_set_size == 20
        assert records_included == 15
        assert ended_ts is not None

    def test_completing_an_already_completed_batch_is_a_no_op(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import (
            SamplingBatch,
            complete_sampling_batch,
            create_sampling_batch,
        )

        cur = db_connection.cursor()
        create_sampling_batch(
            cur,
            SamplingBatch(
                sampling_batch_id="BATCH-505",
                search_query='"VP of AI"',
                platform="linkedin",
                collection_started_ts=datetime.now(UTC),
                inclusion_protocol_version="IP-1.0",
            ),
        )
        db_connection.commit()

        complete_sampling_batch(
            cur,
            "BATCH-505",
            collection_ended_ts=datetime.now(UTC),
            result_set_size=5,
            records_included=5,
        )
        db_connection.commit()

        second = complete_sampling_batch(
            cur,
            "BATCH-505",
            collection_ended_ts=datetime.now(UTC),
            result_set_size=999,  # must NOT overwrite the first completion
            records_included=999,
        )
        db_connection.commit()
        assert second is False

        cur.execute(
            "SELECT result_set_size FROM alcsm.sampling_batch "
            "WHERE sampling_batch_id=%s",
            ("BATCH-505",),
        )
        (result_set_size,) = cur.fetchone()
        cur.close()
        assert result_set_size == 5

    def test_completing_an_unknown_batch_is_a_no_op(
        self, db_connection: psycopg2.extensions.connection
    ) -> None:
        from alcsm.collection.helper import complete_sampling_batch

        cur = db_connection.cursor()
        completed = complete_sampling_batch(
            cur,
            "BATCH-DOES-NOT-EXIST",
            collection_ended_ts=datetime.now(UTC),
        )
        db_connection.commit()
        cur.close()
        assert completed is False
