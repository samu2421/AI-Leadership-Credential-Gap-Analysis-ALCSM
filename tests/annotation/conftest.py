"""Annotation-specific fixtures.

Shares the session-scoped throwaway PostgreSQL cluster from the
top-level `tests/conftest.py` (same pattern as `tests/collection/
conftest.py`). Reference-data seeding (rater_ref, precedent_ref) is
idempotent, so it is safe to call once per session; profile ids use a
distinct counter range (80001+) from `tests/collection/conftest.py`'s
`unique_profile_id` (which starts at 1) so the two test directories
can never collide inside the one shared cluster, even if pytest runs
them in the same session.

No real personal data anywhere in this file (CLAUDE_CODE_RULES.md rule
6) — only constructed, synthetic values.
"""

from __future__ import annotations

import itertools
from collections.abc import Iterator
from datetime import UTC, datetime

import psycopg2
import pytest
from sqlalchemy.orm import Session

import alcsm.db.engine as engine_module
from alcsm.annotation.seed import seed_reference_data
from alcsm.collection.helper import (
    ProfileRecord,
    ProfileSection,
    SamplingBatch,
    create_sampling_batch,
    get_connection,
    insert_profile,
)
from alcsm.config import DatabaseSettings, Settings
from alcsm.db.engine import get_engine


@pytest.fixture(scope="session")
def annotation_sampling_batch_id(throwaway_database: DatabaseSettings) -> str:
    """A profile sampling batch registered once, for annotation-test profiles."""
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = get_connection(settings)
    try:
        batch = SamplingBatch(
            sampling_batch_id="BATCH-950",
            search_query='"AI Leader" (annotation test fixture)',
            platform="linkedin",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
        )
        cur = conn.cursor()
        create_sampling_batch(cur, batch)
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return "BATCH-950"


@pytest.fixture(scope="session", autouse=True)
def seeded_reference_data(throwaway_database: DatabaseSettings) -> None:
    """Seed rater_ref (RATER_A/RATER_B/ADJUDICATOR) and precedent_ref
    (P-01..P-15) once for the whole annotation test session. Idempotent,
    so autouse is safe even if other fixtures also touch the DB first.
    """
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = psycopg2.connect(**settings.database.as_psycopg2_kwargs())
    try:
        seed_reference_data(conn)
    finally:
        conn.close()


_annotation_profile_id_counter = itertools.count(60001)


@pytest.fixture()
def unique_annotation_profile_id() -> str:
    """A fresh, non-colliding PRF-##### id. 60001+ is clearly disjoint
    from every other literal/counter-based id range in the test suite:
    `tests/collection`'s own counter starts at 1; `tests/collection/
    test_workflow.py` hardcodes PRF-80001..80008; `alcsm.annotation.
    fixtures` hardcodes PRF-90001..90005 for the Streamlit dry run."""
    return f"PRF-{next(_annotation_profile_id_counter):05d}"


@pytest.fixture()
def inserted_profile_id(
    db_connection: psycopg2.extensions.connection,
    unique_annotation_profile_id: str,
    annotation_sampling_batch_id: str,
) -> Iterator[str]:
    """Insert one minimal, constructed profile and yield its id.

    A prerequisite for any test that inserts an `alcsm_dimension_score`
    row, since that table's `profile_id` is `REFERENCES profile
    (profile_id) ON DELETE RESTRICT` -- a score cannot exist for a
    profile that was never inserted.
    """
    record = ProfileRecord(
        profile_id=unique_annotation_profile_id,
        sampling_batch_id=annotation_sampling_batch_id,
        search_query='"AI Leader" (annotation test fixture)',
        inclusion_reason="title_match",
        collection_ts=datetime.now(UTC),
        sections={
            "headline": ProfileSection(available=True, text="Fixture headline"),
            "experience": ProfileSection(
                available=True, text="Fixture experience text"
            ),
        },
    )
    insert_profile(db_connection, record)
    yield unique_annotation_profile_id


@pytest.fixture()
def sqlalchemy_session(throwaway_database: DatabaseSettings) -> Iterator[Session]:
    """A SQLAlchemy Session bound to the throwaway cluster, for the
    view-reading functions in `db/queries.py` (reliability export).

    Resets `db.engine`'s process-wide singleton before and after, so
    this test module never picks up a stale engine left behind by
    another test file, and never leaves one behind for the next
    (mirrors `tests/db/test_engine.py`'s established reset pattern).
    """
    engine_module._engine = None
    engine_module._session_factory = None
    settings = Settings(database=throwaway_database, log_level="INFO")
    engine = get_engine(settings)
    session = Session(bind=engine, future=True)
    try:
        yield session
    finally:
        session.close()
        engine_module._engine = None
        engine_module._session_factory = None
