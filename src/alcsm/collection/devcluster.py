"""Disposable PostgreSQL cluster provisioning, for tests and demos alike.

Extracted from ``tests/conftest.py`` (Phase P3 Session 4): both the
pytest fixtures (which need one cluster shared across a whole test
session) and the standalone dry-run script
(``05_Data_Collection/Scripts/collection_dry_run.py``, which needs one
cluster for a single script run) now share this one implementation
rather than two near-identical copies — this session's own "reuse,
don't duplicate" principle applied to test/demo infrastructure parity.

Deliberately independent of pytest (no pytest import here) so the
standalone script can use it without pulling in the test framework.

Never touches ``alcsm_dev`` or any other real database — every cluster
this module creates is brand new, in a fresh temporary directory, and
destroyed on exit regardless of success or failure. No real personal
data is ever involved (CLAUDE_CODE_RULES.md rule 6).
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from alcsm.config import DatabaseSettings

_REPO_ROOT = Path(__file__).resolve().parents[3]
_SCHEMA_FILE = (
    _REPO_ROOT / "03_Database_Design" / "02_Schema" / "alcsm_schema_v1.0.1.sql"
)
_HOMEBREW_PG_BIN = Path("/opt/homebrew/opt/postgresql@16/bin")
_DEFAULT_SUPERUSER = "postgres"

_PG_BINARY_NAMES = ("initdb", "pg_ctl", "createdb", "psql")


def find_pg_binary(name: str) -> str | None:
    """Locate one PostgreSQL binary via PATH, falling back to the
    common Homebrew keg-only install location on macOS.
    """
    found = shutil.which(name)
    if found:
        return found
    candidate = _HOMEBREW_PG_BIN / name
    return str(candidate) if candidate.exists() else None


def locate_pg_binaries() -> dict[str, str | None]:
    """Return ``{name: path_or_None}`` for initdb/pg_ctl/createdb/psql.

    Never raises — callers decide how to handle an absent binary
    (``pytest.skip`` in tests; a clear printed message in the
    standalone script).
    """
    return {name: find_pg_binary(name) for name in _PG_BINARY_NAMES}


@contextmanager
def throwaway_database(
    pg_binaries: dict[str, str],
    port: int,
    db_name: str,
    data_dir: Path | None = None,
) -> Iterator[DatabaseSettings]:
    """Stand up a throwaway PostgreSQL 16 cluster with the frozen
    schema deployed, yield its connection settings, then tear it down.

    If ``data_dir`` is not given, a fresh temporary directory is
    created and removed on exit; if it is given (e.g. pytest's
    ``tmp_path_factory``), the caller owns its cleanup and this
    function only stops the running cluster.
    """
    owns_data_dir = data_dir is None
    if data_dir is None:
        data_dir = Path(tempfile.mkdtemp(prefix="alcsm_pgdata_"))
    # Unix-domain socket paths are capped at ~103 bytes on macOS; a
    # deeply-nested data directory can exceed that, so the socket
    # directory always lives under a short, fixed root instead.
    socket_dir = Path(tempfile.mkdtemp(prefix="alcsm_pgrun_", dir="/tmp"))

    subprocess.run(
        [
            pg_binaries["initdb"],
            "-D",
            str(data_dir),
            "-U",
            _DEFAULT_SUPERUSER,
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
            f"-p {port} -k {socket_dir} -h ''",
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
                ["pg_isready", "-h", str(socket_dir), "-p", str(port)],
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
                str(port),
                "-U",
                _DEFAULT_SUPERUSER,
                db_name,
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
                str(port),
                "-U",
                _DEFAULT_SUPERUSER,
                "-d",
                db_name,
                "-v",
                "ON_ERROR_STOP=1",
                "-f",
                str(_SCHEMA_FILE),
            ],
            check=True,
            capture_output=True,
        )

        yield DatabaseSettings(
            name=db_name,
            user=_DEFAULT_SUPERUSER,
            host=str(socket_dir),
            port=port,
            password="",
        )
    finally:
        subprocess.run(
            [pg_binaries["pg_ctl"], "-D", str(data_dir), "stop"],
            capture_output=True,
        )
        shutil.rmtree(socket_dir, ignore_errors=True)
        if owns_data_dir:
            shutil.rmtree(data_dir, ignore_errors=True)
