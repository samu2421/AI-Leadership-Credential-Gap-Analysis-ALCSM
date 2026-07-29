"""Fixtures for operational-script tests (backup/restore).

Mirrors the throwaway-PostgreSQL pattern used in
tests/collection/conftest.py, kept self-contained here (rather than
shared) so this P1-closure change stays minimal and does not touch
already-verified collection tests.

A throwaway cluster is created per test session and torn down
afterwards. If no local PostgreSQL 16 binaries are available, these
tests are skipped with a clear reason. No real personal data is used
anywhere (CLAUDE_CODE_RULES.md rule 6) — the throwaway database only
ever holds the empty, schema-only structure plus its DDL-seeded
reference rows (dimension_ref, missing_status_ref).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[2]
_SCHEMA_FILE = (
    _REPO_ROOT / "03_Database_Design" / "02_Schema" / "alcsm_schema_v1.0.1.sql"
)
_BACKUP_SCRIPT = _REPO_ROOT / "03_Database_Design" / "Backup" / "backup_alcsm.sh"

_HOMEBREW_PG_BIN = Path("/opt/homebrew/opt/postgresql@16/bin")

_TEST_DB_PORT = 55433  # distinct from the collection tests' throwaway cluster
_TEST_DB_NAME = "alcsm_backup_script_test"
_TEST_DB_SUPERUSER = "postgres"


def _find_pg_binary(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    candidate = _HOMEBREW_PG_BIN / name
    return str(candidate) if candidate.exists() else None


@pytest.fixture(scope="session")
def pg_binaries() -> dict[str, str]:
    """Locate initdb/pg_ctl/createdb/psql/pg_dump/pg_restore, or skip."""
    names = ("initdb", "pg_ctl", "createdb", "dropdb", "psql", "pg_dump", "pg_restore")
    found = {name: _find_pg_binary(name) for name in names}
    missing = [name for name, path in found.items() if path is None]
    if missing:
        pytest.skip(
            f"PostgreSQL binaries not found ({missing}); "
            "skipping backup-script tests."
        )
    return found  # type: ignore[return-value]


@dataclass(frozen=True)
class ThrowawayCluster:
    """Connection parameters for the throwaway cluster used by these tests."""

    host: str  # a unix-socket directory path
    port: int
    db_name: str
    superuser: str


@pytest.fixture(scope="session")
def throwaway_cluster(
    pg_binaries: dict[str, str], tmp_path_factory: pytest.TempPathFactory
) -> Iterator[ThrowawayCluster]:
    """Stand up a throwaway PostgreSQL 16 cluster with the frozen schema
    deployed, for the whole test session. Never the real `alcsm_dev`.
    """
    data_dir = tmp_path_factory.mktemp("alcsm_backup_pgdata")
    # Unix-domain socket paths are capped at ~103 bytes on macOS; pytest's
    # own tmp path nests too deep, so the socket dir needs a short root.
    socket_dir = Path(tempfile.mkdtemp(prefix="alcsm_bkrun_", dir="/tmp"))

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

        yield ThrowawayCluster(
            host=str(socket_dir),
            port=_TEST_DB_PORT,
            db_name=_TEST_DB_NAME,
            superuser=_TEST_DB_SUPERUSER,
        )
    finally:
        subprocess.run(
            [pg_binaries["pg_ctl"], "-D", str(data_dir), "stop"],
            capture_output=True,
        )
        shutil.rmtree(socket_dir, ignore_errors=True)


@pytest.fixture()
def backup_dir(tmp_path: Path) -> Path:
    """A fresh, non-git, non-real-store directory for one test's dumps."""
    d = tmp_path / "backups"
    d.mkdir()
    return d
