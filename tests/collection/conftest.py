"""Fixtures for collection-helper tests.

DB-integration tests need a real PostgreSQL 16 instance with the
frozen schema deployed, so that constraint violations, rollback, and
duplicate handling are tested against the real specification rather
than a mock that only proves the mock behaves as expected
(PROJECT_CONTEXT.md §33: "test against the specification, not the
implementation").

A throwaway cluster is created for the test session (never the real
dev database `alcsm_dev`) and torn down afterwards. If no local
PostgreSQL 16 binaries are available, DB-integration tests are skipped
with a clear reason rather than failing the whole suite — pure-logic
tests (test_validation.py) still run regardless.

No real personal data is used anywhere in these fixtures
(CLAUDE_CODE_RULES.md rule 6) — only constructed, synthetic values.
"""

from __future__ import annotations

import itertools
import shutil
import subprocess
import tempfile
import time
from collections.abc import Iterator
from datetime import UTC
from pathlib import Path

import psycopg2
import pytest

from alcsm.collection.helper import create_sampling_batch, get_connection
from alcsm.config import DatabaseSettings, Settings

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_FILE = (
    _REPO_ROOT / "03_Database_Design" / "02_Schema" / "alcsm_schema_v1.0.1.sql"
)

_HOMEBREW_PG_BIN = Path("/opt/homebrew/opt/postgresql@16/bin")

_TEST_DB_PORT = 55432
_TEST_DB_NAME = "alcsm_collection_test"
_TEST_DB_SUPERUSER = "postgres"


def _find_pg_binary(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    candidate = _HOMEBREW_PG_BIN / name
    return str(candidate) if candidate.exists() else None


@pytest.fixture(scope="session")
def pg_binaries() -> dict[str, str]:
    """Locate initdb/pg_ctl/createdb/psql, or skip DB tests if absent."""
    names = ("initdb", "pg_ctl", "createdb", "psql")
    found = {name: _find_pg_binary(name) for name in names}
    missing = [name for name, path in found.items() if path is None]
    if missing:
        pytest.skip(
            f"PostgreSQL binaries not found ({missing}); "
            "skipping DB-integration collection tests."
        )
    return found  # type: ignore[return-value]


@pytest.fixture(scope="session")
def throwaway_database(
    pg_binaries: dict[str, str], tmp_path_factory: pytest.TempPathFactory
) -> Iterator[DatabaseSettings]:
    """Stand up a throwaway PostgreSQL 16 cluster with the frozen schema.

    Session-scoped: one cluster serves the whole test session, then is
    stopped and its temp directory discarded. Deliberately separate
    from `alcsm_dev` (the real dev database) so test data never lands
    there (mirrors the harness-vs-dev separation used to validate the
    schema itself in Phase P0).
    """
    data_dir = tmp_path_factory.mktemp("alcsm_pgdata")
    # Unix-domain socket paths are capped at ~103 bytes on macOS; pytest's
    # own tmp_path_factory nests deep enough to exceed that, so the
    # socket directory (unlike the data directory) must live under a
    # short, fixed root instead.
    socket_dir = Path(tempfile.mkdtemp(prefix="alcsm_pgrun_", dir="/tmp"))

    subprocess.run(
        [
            pg_binaries["initdb"],
            "-D",
            str(data_dir),
            "-U",
            _TEST_DB_SUPERUSER,
            "--auth=trust",
            "--no-instructions",
        ],
        check=True,
        capture_output=True,
    )

    log_file = data_dir / "log.txt"
    subprocess.run(
        [
            pg_binaries["pg_ctl"],
            "-D",
            str(data_dir),
            "-o",
            f"-p {_TEST_DB_PORT} -k {socket_dir} -h ''",
            "-l",
            str(log_file),
            "start",
        ],
        check=True,
        capture_output=True,
    )

    try:
        for _ in range(50):
            ready = subprocess.run(
                ["pg_isready", "-h", str(socket_dir), "-p", str(_TEST_DB_PORT)],
                capture_output=True,
            )
            if ready.returncode == 0:
                break
            time.sleep(0.1)
        else:
            raise RuntimeError("throwaway PostgreSQL cluster did not become ready")

        subprocess.run(
            [
                pg_binaries["createdb"],
                "-h",
                str(socket_dir),
                "-p",
                str(_TEST_DB_PORT),
                "-U",
                _TEST_DB_SUPERUSER,
                _TEST_DB_NAME,
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                pg_binaries["psql"],
                "-h",
                str(socket_dir),
                "-p",
                str(_TEST_DB_PORT),
                "-U",
                _TEST_DB_SUPERUSER,
                "-d",
                _TEST_DB_NAME,
                "-v",
                "ON_ERROR_STOP=1",
                "-f",
                str(_SCHEMA_FILE),
            ],
            check=True,
            capture_output=True,
        )

        yield DatabaseSettings(
            name=_TEST_DB_NAME,
            user=_TEST_DB_SUPERUSER,
            host=str(socket_dir),
            port=_TEST_DB_PORT,
            password="",
        )
    finally:
        subprocess.run(
            [pg_binaries["pg_ctl"], "-D", str(data_dir), "stop"],
            capture_output=True,
        )
        shutil.rmtree(socket_dir, ignore_errors=True)


@pytest.fixture()
def db_connection(
    throwaway_database: DatabaseSettings,
) -> Iterator[psycopg2.extensions.connection]:
    """A fresh psycopg2 connection to the throwaway database, per test."""
    settings = Settings(database=throwaway_database, log_level="INFO")
    conn = get_connection(settings)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture(scope="session")
def sampling_batch_id(throwaway_database: DatabaseSettings) -> str:
    """A sampling batch registered once for the whole test session.

    Batch registration is idempotent (`ON CONFLICT DO NOTHING`), so
    sharing one batch id across tests is safe and mirrors real usage:
    one documented search underlies many collected profiles.
    """
    from datetime import datetime

    from alcsm.collection.helper import SamplingBatch

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


_profile_id_counter = itertools.count(1)


@pytest.fixture()
def unique_profile_id() -> str:
    """A fresh, non-colliding PRF-##### id for each test."""
    return f"PRF-{next(_profile_id_counter):05d}"
