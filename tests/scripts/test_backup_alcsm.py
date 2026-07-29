"""Verification tests for 03_Database_Design/Backup/backup_alcsm.sh.

Run against a throwaway PostgreSQL 16 cluster with the frozen v1.0.1
schema deployed (see conftest.py) — never the real `alcsm_dev`
database, and no real personal data (CLAUDE_CODE_RULES.md rule 6).

Assertions target the script's specification (PROJECT_CONTEXT.md §35,
§45: backups must be produced, verifiable, prunable by retention
count, and never silently default to an unspecified destination) —
not this particular fix's internals.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.scripts.conftest import ThrowawayCluster

_REPO_ROOT = Path(__file__).resolve().parents[2]
_BACKUP_SCRIPT = _REPO_ROOT / "03_Database_Design" / "Backup" / "backup_alcsm.sh"


def _run_backup(
    cluster: ThrowawayCluster,
    backup_dir: Path,
    *,
    keep: int | None = 14,
    set_backup_dir: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["ALCSM_DB"] = cluster.db_name
    env["ALCSM_HOST"] = cluster.host
    env["ALCSM_PORT"] = str(cluster.port)
    # backup_alcsm.sh takes no -U flag by design (it relies on ambient
    # OS-user/PGUSER auth, matching the real deployment); PGUSER points
    # pg_dump/pg_restore at the throwaway cluster's role instead.
    env["PGUSER"] = cluster.superuser
    if set_backup_dir:
        env["ALCSM_BACKUP_DIR"] = str(backup_dir)
    else:
        env.pop("ALCSM_BACKUP_DIR", None)
    if keep is not None:
        env["ALCSM_KEEP"] = str(keep)
    return subprocess.run(
        ["bash", str(_BACKUP_SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
    )


def test_backup_runs_cleanly_with_no_stderr_errors(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path
) -> None:
    result = _run_backup(throwaway_cluster, backup_dir)
    assert result.returncode == 0, result.stderr
    assert "illegal option" not in result.stderr
    assert result.stderr == "" or "NOTICE" in result.stderr


def test_backup_produces_a_dump_file(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path
) -> None:
    _run_backup(throwaway_cluster, backup_dir)
    dumps = list(backup_dir.glob("alcsm_*.dump"))
    assert len(dumps) == 1
    assert dumps[0].stat().st_size > 0


def test_backup_output_reports_the_correct_nonzero_byte_count(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path
) -> None:
    result = _run_backup(throwaway_cluster, backup_dir)
    match = re.search(r"backup OK: (.+) \((\d+) bytes\)", result.stdout)
    assert match is not None, result.stdout
    dump_path = Path(match.group(1))
    reported_bytes = int(match.group(2))
    assert reported_bytes > 0
    assert reported_bytes == dump_path.stat().st_size


def test_dump_is_listable_by_pg_restore(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path, pg_binaries: dict[str, str]
) -> None:
    _run_backup(throwaway_cluster, backup_dir)
    (dump,) = backup_dir.glob("alcsm_*.dump")
    result = subprocess.run(
        [pg_binaries["pg_restore"], "--list", str(dump)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "dbname:" in result.stdout


def test_restore_round_trip_recreates_the_schema(
    throwaway_cluster: ThrowawayCluster,
    backup_dir: Path,
    pg_binaries: dict[str, str],
) -> None:
    """The documented restore procedure (script footer comment) must
    actually reconstruct the frozen schema: 22 tables, 5 views, and
    the DDL-seeded reference rows, intact."""
    _run_backup(throwaway_cluster, backup_dir)
    (dump,) = backup_dir.glob("alcsm_*.dump")

    restore_db = "alcsm_restore_roundtrip_test"
    common = [
        "-h",
        throwaway_cluster.host,
        "-p",
        str(throwaway_cluster.port),
        "-U",
        throwaway_cluster.superuser,
    ]
    subprocess.run(
        [pg_binaries["createdb"], *common, restore_db], check=True, capture_output=True
    )
    try:
        result = subprocess.run(
            [pg_binaries["pg_restore"], *common, "-d", restore_db, str(dump)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

        check = subprocess.run(
            [
                pg_binaries["psql"],
                *common,
                "-d",
                restore_db,
                "-t",
                "-c",
                "SELECT count(*) FROM information_schema.tables "
                "WHERE table_schema='alcsm' AND table_type='BASE TABLE'",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert check.stdout.strip() == "22"

        check = subprocess.run(
            [
                pg_binaries["psql"],
                *common,
                "-d",
                restore_db,
                "-t",
                "-c",
                "SELECT count(*) FROM information_schema.views "
                "WHERE table_schema='alcsm'",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert check.stdout.strip() == "5"

        check = subprocess.run(
            [
                pg_binaries["psql"],
                *common,
                "-d",
                restore_db,
                "-t",
                "-c",
                "SELECT count(*) FROM alcsm.dimension_ref",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        assert check.stdout.strip() == "6"
    finally:
        subprocess.run(
            [pg_binaries["dropdb"], *common, "--if-exists", restore_db],
            capture_output=True,
        )


def test_missing_backup_dir_env_var_fails_fast_with_a_clear_message(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path
) -> None:
    """PROJECT_CONTEXT.md §45: backups must never silently default to
    an unapproved location. The script must refuse to run at all
    rather than guess a destination."""
    result = _run_backup(throwaway_cluster, backup_dir, set_backup_dir=False)
    assert result.returncode != 0
    assert "ALCSM_BACKUP_DIR" in result.stderr


def test_retention_prunes_to_the_configured_keep_count(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path
) -> None:
    """Pre-seed 5 fake older dumps, run the real script once more with
    ALCSM_KEEP=2, and confirm only the newest 2 (the real run's dump
    plus the single newest fake one) survive."""
    now = time.time()
    for i in range(5):
        fake = backup_dir / f"alcsm_2020010{i}T000000Z.dump"
        fake.write_bytes(b"not a real dump, just for retention-pruning")
        # Stagger mtimes so `ls -1t` ordering is deterministic.
        os.utime(fake, (now - (10 - i), now - (10 - i)))

    _run_backup(throwaway_cluster, backup_dir, keep=2)

    remaining = sorted(backup_dir.glob("alcsm_*.dump"))
    assert len(remaining) == 2
    # The just-created real dump (newest by mtime) must be among the survivors.
    real_dumps = [p for p in remaining if "2020" not in p.name]
    assert len(real_dumps) == 1


@pytest.mark.parametrize("keep", [None])
def test_default_retention_keeps_fourteen_when_unset(
    throwaway_cluster: ThrowawayCluster, backup_dir: Path, keep: int | None
) -> None:
    for i in range(16):
        fake = backup_dir / f"alcsm_2020{i:04d}T000000Z.dump"
        fake.write_bytes(b"fake")
        os.utime(fake, (time.time() - (100 - i), time.time() - (100 - i)))

    _run_backup(throwaway_cluster, backup_dir, keep=keep)

    remaining = list(backup_dir.glob("alcsm_*.dump"))
    # 16 fakes + 1 real = 17 candidates; default ALCSM_KEEP=14 keeps 14.
    assert len(remaining) == 14
