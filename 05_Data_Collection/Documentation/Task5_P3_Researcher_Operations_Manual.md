# ALCSM Collection Software — Researcher Operations Manual

**Version:** 1.0
**Status:** Operational manual for the collection software built in Phase P3 (Sessions 1–4). This document tells you *how to run the software*; it is not a substitute for the design documents (`Task5_P3_Sampling_Framework_Design.md`, `Task5_P3_JobPosting_Collection_Plan.md`) that govern *what* to collect and *why*, nor for the ethics package that governs *whether* you may collect yet.
**Purpose:** a step-by-step operational reference for the researcher (or a future collaborator) actually running a collection session, written as a manual, not developer documentation.
**Last Updated:** 2026-08-02
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance, Phase P3 Session 4

---

## 0. Before you do anything: the ethics gate

**Do not run this software against real profiles or real job postings until real ethics-committee approval, DPO sign-off, and every item in the `Task5_Implementation_Readiness_Checklist.md` §3 blocker list is checked.** Everything below is safe to run today because it only ever touches synthetic, constructed data on a throwaway database. Pointing the same code at a real profile before that gate clears is a compliance incident, not a technicality (`Implementation_Phase_Roadmap.md` §7).

## 1. Prerequisites

- Python 3.11+, the project's virtual environment active (`source .venv/bin/activate`), dependencies installed (`pip install -e .`, which also makes the `alcsm` package importable without extra `PYTHONPATH` configuration — required for running scripts directly, e.g. `python 05_Data_Collection/Scripts/collection_dry_run.py`; `pytest` sets this up automatically for the test suite, but a standalone script invocation does not).
- PostgreSQL 16 client and server binaries (`initdb`, `pg_ctl`, `createdb`, `psql`) on `PATH`, or at the standard Homebrew keg-only location (`/opt/homebrew/opt/postgresql@16/bin`) on macOS.
- A deployed database — either a real, access-controlled, EEA-resident secure-store instance (for real collection, post-ethics-gate) or a local dev instance (`alcsm_dev`) for practice, or none at all if you're only running the dry run (which provisions and destroys its own throwaway instance).
- A configured `.env` (see `config.py`'s `DatabaseSettings`) pointing at whichever database you intend to write to — **never point it at a throwaway/test database by habit and never point it at a real database by accident**; double-check `DATABASE_NAME`/`DATABASE_HOST` before running anything that writes.

## 2. Try it safely first: the dry run

Before touching any real (or even `alcsm_dev`) database, run the dry-run demonstration. It provisions its own disposable PostgreSQL cluster, runs the complete two-corpus workflow with synthetic data, prints a summary, and destroys everything it created:

```bash
python 05_Data_Collection/Scripts/collection_dry_run.py
```

Expected output: a step-by-step log (`start_batch`, `insert synthetic profile`, `checkpoint`, `resume`, `insert additional synthetic profile`, `finish batch`, `quality checks`, `report`, `export`, repeated for both corpora), followed by a summary block, ending with *"Dry run complete. No real data was collected."* and a note that nothing was left behind. If this doesn't run cleanly, do not proceed to real collection — diagnose the environment first (see §9 Troubleshooting).

## 3. Creating a batch

Every collection session starts by registering a `SamplingBatch` — the provenance root every subsequent record traces back to. Use `CollectionWorkflow.start_batch()`:

```python
from datetime import UTC, datetime
from alcsm.collection.helper import SamplingBatch, get_connection
from alcsm.collection.workflow import CollectionWorkflow
from alcsm.config import load_settings

conn = get_connection(load_settings())
workflow = CollectionWorkflow(conn)

workflow.start_batch(SamplingBatch(
    sampling_batch_id="BATCH-001",       # must match BATCH-### (three digits)
    search_query='"Chief AI Officer"',    # exact, pre-registered query string
    platform="linkedin",
    collection_started_ts=datetime.now(UTC),
    inclusion_protocol_version="IP-1.0",  # ties this batch to a specific version
                                            # of Task5_P3_Sampling_Framework_Design.md
))
```

For a job-posting batch, add `corpus="job_posting"` and use a platform like `"job_board"`. **`sampling_batch_id` must match `BATCH-###` exactly (three digits) — this is enforced by the frozen schema, not a style preference.** Pick the next unused number in sequence; do not reuse one.

## 4. Collecting profiles

For each profile a human collector has read and transcribed by hand (per `Task5_P3_Sampling_Framework_Design.md` — never scraped, never automated):

```python
from alcsm.collection.helper import ProfileRecord, ProfileSection
from alcsm.collection.duplicates import DuplicateCandidate

record = ProfileRecord(
    profile_id="PRF-00001",              # assign at capture, PRF-#####
    sampling_batch_id="BATCH-001",
    search_query='"Chief AI Officer"',
    inclusion_reason="title_match",       # or title_variant_match / manual_review_included
    collection_ts=datetime.now(UTC),
    sections={
        "headline": ProfileSection(available=True, text="Chief AI Officer at Acme"),
        "about": ProfileSection(available=True, text="..."),
        # ...any of the other five sections; an unmentioned section
        # defaults to available=False (not retrieved), never fabricated.
    },
)

profile_id = workflow.collect_profile(
    record,
    candidate=DuplicateCandidate(title=record.sections["headline"].text),
)
if profile_id is None:
    print("Excluded: session-local duplicate.")
```

`workflow.collect_profile` validates the record (rejecting it, with every problem listed, before touching the database if anything is wrong — malformed id, missing provenance, an activity section captured without the ethics flag, etc.), checks it against the in-session duplicate registry if you pass a `candidate`, and inserts it atomically. A validation failure raises `ProfileValidationError` and is recorded in the audit log; nothing partial is ever left in the database.

## 5. Collecting job postings

Structurally identical, with the posting-specific fields:

```python
from alcsm.collection.helper import JobPostingRecord

record = JobPostingRecord(
    posting_id="JOB-00001",
    sampling_batch_id="BATCH-101",
    posting_source="example_job_board",   # required — postings have no default source
    search_query='"Head of AI" job',
    inclusion_reason="title_match",
    collection_ts=datetime.now(UTC),
    raw_posting_text="...",               # verbatim, required, non-empty
    raw_requirements_text="...",          # optional, verbatim
)

posting_id = workflow.collect_job_posting(record)
```

**Recruiter-privacy check is automatic.** If `raw_posting_text`/`raw_requirements_text` contains a detectable email address, phone-number-shaped sequence, or LinkedIn personal-profile link, the insert is rejected with a clear error naming which field and why (`Task5_P3_JobPosting_Collection_Plan.md` §6). This is a **pattern-based**, not name-detecting, check — a recruiter's bare name in free text is not something this software can catch automatically; redact it by hand before transcription, as the collection plan already specifies.

## 6. Checkpoints

Save progress periodically (recommended: after every batch, or every N records for a long session):

```python
from pathlib import Path

checkpoint = workflow.save_checkpoint(
    "BATCH-001", "profile", Path("/secure/store/checkpoints/BATCH-001.json")
)
```

**Where to put checkpoint files:** outside the Git repository, outside the database, in the same secure-store location as the collection log (`Task5_P3_Sampling_Framework_Design.md` §13) — a checkpoint file carries only pseudonymous ids and counts, never raw text, so it is safe to store there but is still an operational artefact, not something to commit.

## 7. Recovery after an interruption

If a session is interrupted (crash, closed terminal, power loss), start a **new** `CollectionWorkflow` against the same database and resume from the last saved checkpoint:

```python
new_workflow = CollectionWorkflow(conn)  # a fresh instance — this is expected
problems = new_workflow.resume_from_checkpoint(
    Path("/secure/store/checkpoints/BATCH-001.json")
)
if problems:
    print("Do not continue — checkpoint is stale or inconsistent:")
    for p in problems:
        print(f"  - {p}")
else:
    print("Safe to resume.")
    # continue calling collect_profile()/collect_job_posting() as normal
```

`resume_from_checkpoint` re-validates the checkpoint's own shape *and* cross-checks every claimed-processed id against the live database — if the checkpoint claims a record was captured that isn't actually there, you are told explicitly rather than silently continuing on stale information. **Never resume without checking `problems` first.**

## 8. Quality checks, reporting, and export

After a batch is complete (`workflow.complete_batch(...)`), before moving on:

```python
quality = workflow.run_quality_checks("BATCH-001", "profile")
print("Clean:", quality.is_clean)
print("Consistency:", quality.consistency)
print("Missing metadata:", quality.missing_metadata)
print("Duplicate problems:", quality.duplicate_problems)
print("Section completeness:", quality.section_completeness)  # profile batches only

report = workflow.generate_report("BATCH-001", "profile")
print(f"Processed: {report.records_processed}, "
      f"failures: {report.validation_failures}, "
      f"duplicates: {report.duplicate_count}")

manifest = workflow.export_metadata(
    "BATCH-001", "profile", Path("/secure/store/exports/BATCH-001.json")
)
print(f"Exported {manifest.record_count} record(s) to {manifest.output_path}")
```

**What gets exported:** batch provenance and per-record metadata only (ids, query, timestamps, language/geography, inclusion reason) — **never** raw profile section text or posting text. This is enforced by an explicit column allow-list in `collection/export.py`, not left to habit.

## 9. Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| `PostgreSQL binaries not found` | `initdb`/`pg_ctl`/`createdb`/`psql` not on `PATH` | Install PostgreSQL 16 (`brew install postgresql@16` on macOS) or add the install's `bin/` to `PATH`. |
| `ModuleNotFoundError: No module named 'alcsm'` running a script directly | Package not installed in the active environment | `pip install -e .` from the repository root, with the project's venv active. |
| `ProfileValidationError` / `JobPostingValidationError` on insert | The record itself violates a frozen rule (bad id format, missing provenance, recruiter content, etc.) | Read every listed problem (not just the first) — the error lists them all. Fix the record; nothing was written to the database. |
| `psycopg2.errors.UniqueViolation` on a batch or record id | You reused an id already in the database | Assign the next unused id in sequence; ids are never reused. |
| `psycopg2.errors.ForeignKeyViolation` inserting a profile/posting | `sampling_batch_id` doesn't match a batch you actually registered | Call `start_batch()` first, or check for a typo in the batch id. |
| `resume_from_checkpoint` returns non-empty `problems` | The checkpoint is stale, corrupted, or claims a record that isn't in the database | Do not continue collecting against that batch until you understand why — this is the restart-safety check working as intended, not a bug to route around. |
| `quality.is_clean` is `False` after completing a batch | Declared `records_included` doesn't match the actual row count, or a duplicate rank-position slipped through | Inspect `quality.consistency.problems`/`quality.duplicate_problems`; correct the completion call or investigate the duplicate before treating the batch as final. |
| Dry run (`collection_dry_run.py`) fails | Almost always an environment issue (missing PostgreSQL binaries, a port already in use) | Re-read the printed error; the dry run provisions its own cluster on port 55555 — confirm nothing else is bound to it. |

## 10. Expected outputs, summarised

| Action | Where the result lives |
|---|---|
| A registered batch | `alcsm.sampling_batch` (one row) |
| A collected profile/posting | `alcsm.profile`/`alcsm.job_posting` + (profile only) `alcsm.profile_raw_section` |
| A checkpoint | A JSON file at the path you chose (outside Git, outside the database) |
| An audit trail | In-memory on the `CollectionWorkflow`/`CollectionManager` instance (`workflow.audit_log`); persist explicitly via `AuditLog.save(path)` if you want it to survive process exit |
| A quality report | A `QualitySummary` object (inspect in-process or print) |
| An operational report | A `CollectionReport` object; render with `collection.reporting.render_report_text()` |
| An export | A versioned JSON file at the path you chose, metadata only |

---

*This manual documents how to operate software that is ready today; it does not itself authorise real collection. See §0.*
