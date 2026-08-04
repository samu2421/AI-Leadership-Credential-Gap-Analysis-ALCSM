#!/usr/bin/env python3
"""Collection dry-run demonstration (Phase P3 Session 4).

Runs the complete collection workflow end to end, for both corpora,
against a brand-new, throwaway PostgreSQL 16 cluster that this script
creates and destroys itself — never against `alcsm_dev`, never with
real personal data (CLAUDE_CODE_RULES.md rule 6). Every profile and
job posting inserted here is synthetic, hard-coded, constructed data.

This script performs NO network access, NO scraping, NO browser
automation, and collects NO real LinkedIn profile or job posting. It
exists solely to prove — reproducibly, on demand, without ambiguity —
that the collection infrastructure built across P3 Sessions 1-3 works
correctly end to end, exactly as
`Task5_P3_Researcher_Operations_Manual.md` describes.

Usage (from the repository root, with the project's virtualenv active):

    python 05_Data_Collection/Scripts/collection_dry_run.py

Requires local PostgreSQL 16 binaries (initdb/pg_ctl/createdb/psql) on
PATH or at the standard Homebrew keg-only location. Prints a step-by-
step summary and exits non-zero if anything fails.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from alcsm.collection.devcluster import locate_pg_binaries, throwaway_database
from alcsm.collection.helper import get_connection
from alcsm.collection.workflow import DryRunResult, run_dry_run
from alcsm.config import Settings

_DRY_RUN_PORT = 55555
_DRY_RUN_DB_NAME = "alcsm_dry_run"


def _print_summary(result: DryRunResult) -> None:
    print()
    print("=" * 72)
    print("COLLECTION DRY RUN — SUMMARY")
    print("=" * 72)
    for step in result.steps:
        print(f"  [{step.name}] {step.detail}")
    print("-" * 72)
    print(f"Profile batch:  {result.profile_batch_id}")
    print(f"  Profiles inserted: {result.profile_ids}")
    print(f"  Quality clean:     {result.profile_quality.is_clean}")
    print(f"  Records processed: {result.profile_report.records_processed}")
    print(f"  Export written to: {result.profile_export.output_path}")
    print()
    print(f"Job posting batch: {result.posting_batch_id}")
    print(f"  Postings inserted: {result.posting_ids}")
    print(f"  Quality clean:      {result.posting_quality.is_clean}")
    print(f"  Records processed:  {result.posting_report.records_processed}")
    print(f"  Export written to:  {result.posting_export.output_path}")
    print("=" * 72)
    print("Dry run complete. No real data was collected.")
    print("=" * 72)


def main() -> int:
    pg_binaries = locate_pg_binaries()
    missing = [name for name, path in pg_binaries.items() if path is None]
    if missing:
        print(
            f"PostgreSQL binaries not found ({missing}); cannot run the dry run. "
            "Install PostgreSQL 16 (e.g. `brew install postgresql@16`) and retry.",
            file=sys.stderr,
        )
        return 1

    with tempfile.TemporaryDirectory(prefix="alcsm_dryrun_export_") as export_dir_str:
        export_dir = Path(export_dir_str)
        with throwaway_database(
            pg_binaries,  # type: ignore[arg-type]
            _DRY_RUN_PORT,
            _DRY_RUN_DB_NAME,
        ) as db_settings:
            settings = Settings(database=db_settings, log_level="INFO")
            conn = get_connection(settings)
            try:
                result = run_dry_run(conn, export_dir)
            finally:
                conn.close()

        _print_summary(result)

    print(
        "\nNote: the throwaway database and its export files have now been "
        "torn down — this script leaves nothing behind."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
