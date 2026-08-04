"""Collection-specific fixtures.

DB-integration tests need a real PostgreSQL 16 instance with the
frozen schema deployed, so that constraint violations, rollback, and
duplicate handling are tested against the real specification rather
than a mock that only proves the mock behaves as expected
(PROJECT_CONTEXT.md §33: "test against the specification, not the
implementation").

The throwaway-cluster/`db_connection` fixtures this module depends on
now live in `tests/conftest.py` (Phase P3 Session 2 generalisation —
shared with `tests/taxonomy/`); this file keeps only what is specific
to the collection helper's profile and job-posting fixtures. If no
local PostgreSQL 16 binaries are available, DB-integration tests are
skipped with a clear reason rather than failing the whole suite —
pure-logic tests still run regardless.

No real personal data is used anywhere in these fixtures
(CLAUDE_CODE_RULES.md rule 6) — only constructed, synthetic values.
"""

from __future__ import annotations

import itertools
from datetime import UTC, datetime

import pytest

from alcsm.collection.helper import SamplingBatch, create_sampling_batch, get_connection
from alcsm.config import DatabaseSettings, Settings


@pytest.fixture(scope="session")
def sampling_batch_id(throwaway_database: DatabaseSettings) -> str:
    """A profile sampling batch registered once for the whole test session.

    Batch registration is idempotent (`ON CONFLICT DO NOTHING`), so
    sharing one batch id across tests is safe and mirrors real usage:
    one documented search underlies many collected profiles.
    """
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = get_connection(settings)
    try:
        batch = SamplingBatch(
            sampling_batch_id="BATCH-001",
            search_query='"Chief AI Officer"',
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
    return "BATCH-001"


@pytest.fixture(scope="session")
def job_posting_batch_id(throwaway_database: DatabaseSettings) -> str:
    """A job-posting sampling batch (`corpus='job_posting'`) registered
    once for the whole test session.

    Uses a distinct id range (`BATCH-1xx`) from the profile-side
    `sampling_batch_id` fixture (`BATCH-001`) since both share one
    throwaway database in the same test session and `sampling_batch_id`
    is a primary key (PROJECT_CONTEXT.md §13).
    """
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = get_connection(settings)
    try:
        batch = SamplingBatch(
            sampling_batch_id="BATCH-101",
            search_query='"Head of AI" job',
            platform="job_board",
            collection_started_ts=datetime.now(UTC),
            inclusion_protocol_version="IP-1.0",
            corpus="job_posting",
        )
        cur = conn.cursor()
        create_sampling_batch(cur, batch)
        conn.commit()
        cur.close()
    finally:
        conn.close()
    return "BATCH-101"


_profile_id_counter = itertools.count(1)


@pytest.fixture()
def unique_profile_id() -> str:
    """A fresh, non-colliding PRF-##### id for each test."""
    return f"PRF-{next(_profile_id_counter):05d}"


_posting_id_counter = itertools.count(1)


@pytest.fixture()
def unique_posting_id() -> str:
    """A fresh, non-colliding JOB-##### id for each test."""
    return f"JOB-{next(_posting_id_counter):05d}"
