"""Shared pytest fixtures. No real personal data is ever used here
(CLAUDE_CODE_RULES.md rule 6) — only constructed, non-personal values.

The throwaway-PostgreSQL-cluster fixtures below were originally local
to `tests/collection/conftest.py` (Phase P1), then generalised to this
top level (Phase P3 Session 2) so `tests/collection/`,
`tests/taxonomy/`, and any future test directory needing a real
database share one cluster per test session instead of each
reimplementing cluster bring-up. Phase P3 Session 4 extracted the
cluster-lifecycle logic itself into `alcsm.collection.devcluster`, so
this file and the standalone dry-run script
(`05_Data_Collection/Scripts/collection_dry_run.py`) share one
implementation rather than two. `tests/scripts/` deliberately keeps
its own, separate cluster (a different port, a different concern —
backup/restore, not the collection helper) and is unaffected by this
change.
"""

from __future__ import annotations

from collections.abc import Iterator

import pandas as pd
import psycopg2
import pytest

from alcsm.collection.devcluster import locate_pg_binaries
from alcsm.collection.devcluster import throwaway_database as _throwaway_database_cm
from alcsm.collection.helper import get_connection
from alcsm.config import DatabaseSettings, Settings

_TEST_DB_PORT = 55432
_TEST_DB_NAME = "alcsm_shared_test"

_ANALYSIS_FIXTURE_PROFILE_IDS = [f"PRF-{i:05d}" for i in range(1, 13)]


@pytest.fixture()
def synthetic_predictions() -> pd.DataFrame:
    """RQ5 fixture: constructed NLP predictions, one row per profile x
    dimension. Shared at the root level since both `tests/analysis/`
    and `tests/nlp/test_evaluate.py` need it."""
    rows = []
    for i, pid in enumerate(_ANALYSIS_FIXTURE_PROFILE_IDS):
        for dim_n in range(1, 7):
            rows.append(
                {
                    "profile_id": pid,
                    "dimension_number": dim_n,
                    "predicted_score": (i + dim_n) % 6,
                }
            )
    return pd.DataFrame(rows)


@pytest.fixture()
def synthetic_gold() -> pd.DataFrame:
    """Same shape, deliberately offset from `synthetic_predictions` so
    error/agreement metrics are exercised meaningfully (not trivially
    all-zero-error)."""
    rows = []
    for i, pid in enumerate(_ANALYSIS_FIXTURE_PROFILE_IDS):
        for dim_n in range(1, 7):
            predicted = (i + dim_n) % 6
            gold = predicted if i % 3 != 0 else max(0, predicted - 1)
            rows.append({"profile_id": pid, "dimension_number": dim_n, "score": gold})
    return pd.DataFrame(rows)


@pytest.fixture
def fake_db_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set constructed, non-secret DB environment variables for tests."""
    monkeypatch.setenv("DATABASE_NAME", "alcsm_test")
    monkeypatch.setenv("DATABASE_USER", "alcsm_test_user")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv("DATABASE_PASSWORD", "fake-test-password")


@pytest.fixture(scope="session")
def pg_binaries() -> dict[str, str]:
    """Locate initdb/pg_ctl/createdb/psql, or skip DB tests if absent."""
    found = locate_pg_binaries()
    missing = [name for name, path in found.items() if path is None]
    if missing:
        pytest.skip(
            f"PostgreSQL binaries not found ({missing}); "
            "skipping DB-integration tests."
        )
    return found  # type: ignore[return-value]


@pytest.fixture(scope="session")
def throwaway_database(
    pg_binaries: dict[str, str], tmp_path_factory: pytest.TempPathFactory
) -> Iterator[DatabaseSettings]:
    """Stand up a throwaway PostgreSQL 16 cluster with the frozen schema.

    Session-scoped: one cluster serves the whole test session (shared
    by every test directory that depends on it), then is stopped and
    its temp directory discarded. Deliberately separate from
    `alcsm_dev` (the real dev database) so test data never lands there
    (mirrors the harness-vs-dev separation used to validate the schema
    itself in Phase P0).
    """
    data_dir = tmp_path_factory.mktemp("alcsm_pgdata")
    with _throwaway_database_cm(
        pg_binaries, _TEST_DB_PORT, _TEST_DB_NAME, data_dir=data_dir
    ) as settings:
        yield settings


@pytest.fixture()
def db_connection(
    throwaway_database: DatabaseSettings,
) -> Iterator[psycopg2.extensions.connection]:
    """A fresh psycopg2 connection to the throwaway database, per test.

    Shared across every test directory that needs real-database access
    (`tests/collection/`, `tests/taxonomy/`) — each test gets its own
    connection to the one session-scoped cluster.
    """
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = get_connection(settings)
    try:
        yield conn
    finally:
        conn.close()
