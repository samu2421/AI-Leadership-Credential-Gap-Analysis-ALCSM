# P4 Annotation Interface — Dry Run Instructions

**Status:** Interface build complete, fixture-only dry run available now. Pilot coding on real profiles remains blocked on P2 (ethics) and P3 (taxonomy anchoring) both clearing (`Implementation_Phase_Roadmap.md`, "P4 — Annotation interface and pilot coding").
**Audience:** anyone (researcher, supervisor, examiner) who wants to see the P4 interface working today, against constructed data only.

---

## 1. Prerequisites

```bash
cd "AI_Leadership_Credential_Gap_Analysis"
python3 -m venv .venv && source .venv/bin/activate   # if not already set up
pip install -e ".[app,reliability,dev]"
```

For the database-backed parts of the dry run (score storage, duplicate prevention, rater blinding, reliability export), a local PostgreSQL 16 is needed only to run the automated tests — the Streamlit UI itself runs entirely from in-memory fixtures and needs no database connection at all.

```bash
brew install postgresql@16   # macOS, if not already installed
```

## 2. Run the annotation interface

```bash
streamlit run src/alcsm/app/annotation_app.py
```

Opens at `http://localhost:8501`. Everything shown is constructed, non-personal data (`alcsm.annotation.fixtures`, five profiles reusing the same composites already published in `ALCSM_v1.0_Scoring_Framework_Task3.md` §4 / `ALCSM_v1.1_Scoring_Framework.md` §4). Try:

- **Switch dimension-config version** (sidebar) between `v1_1` and `v1_0` to see D6 change from "AI Industry/Application Breadth" (marked PROPOSED/PILOT_REQUIRED) to the original, retired "Professional Engagement & Continuous Development" — proving the versioned-config design (no code change needed to compare the two).
- **Switch rater** (sidebar) between RATER_A, RATER_B, ADJUDICATOR.
- **Score a dimension**: pick a decision (ACCEPT/CHANGE/DEFER), adjust the score/missing-status/rationale, click Save. Invalid combinations (e.g. score=9, or `unavailable` with a score other than 0) are rejected with a readable message before anything is "saved" — this is the same validation `alcsm.annotation.validation.validate_annotation_score` will run against the real database later.
- **Watch the progress metric** (sidebar) — it will not read "6/6" until every one of the six dimensions has a decision, which is the four-frozen-constraints rule ("show one profile's six dimensions together") made visible.

Note the explicit on-screen statement that no RQ4 impact indicators are shown (frozen constraint #2), and that `FIRST_PASS_SCORE` (read-only reference) and `FINAL_HUMAN_SCORE` (what you enter) are labelled as distinct concepts throughout.

This dry-run mode keeps decisions in Streamlit's in-session state only — nothing is written to a database, since none is required to run it. The database-backed write path (`alcsm.annotation.store`) is exercised by the automated test suite instead (§3), and would be wired into the UI's "Save" button once P2/P3 clear and real pilot coding is authorized (see the completion report §4 for exactly what that wiring involves).

## 3. Run the automated test suite

```bash
python3 -m pytest tests/annotation/ tests/app/test_annotation_app.py tests/db/test_queries.py -v
```

This spins up a throwaway PostgreSQL 16 cluster (via `alcsm.collection.devcluster`, the same mechanism `tests/collection/` already uses), deploys the frozen schema (`alcsm_schema_v1.0.1.sql`) into it fresh, and tears it down afterward — no real database, and no data survives the test run. If PostgreSQL 16 binaries are not found on `PATH` (or the standard Homebrew keg-only location), the database-backed tests are skipped with a clear reason; the pure-logic tests (validation, dimension config, pilot selection, audit, export, fixtures) still run regardless.

Run the whole project's suite to confirm nothing else regressed:

```bash
python3 -m pytest tests/ -q
black --check src tests
ruff check src tests
mypy src
```

## 4. Inspect the audit trail from a dry run

The Streamlit app's in-session "Save" actions write to a git-ignored JSONL file:

```bash
cat 06_Annotation/audit_log/annotation_audit.jsonl
```

Each line is one structured, PII-free event (`actor`, `action`, `profile_id`, `dimension_number`, `detail` — never evidence text). Delete this file freely between dry runs; it is not a research artifact.

## 5. What this dry run does and does not prove

**Proves:** the interface renders all six dimensions with evidence/missing-status/first-pass-reference; validation rejects malformed scores before they would reach the database; the D6 versioned config correctly separates display text from the frozen DB vocabulary; no RQ4 value appears anywhere in the rendered page; the audit trail records every save.

**Does not prove:** anything about real inter-rater reliability, real annotation throughput, or how the interface behaves against the actual 500-profile dataset — those all require real profiles loaded into a real database, which is exactly what remains blocked (see `P4_Implementation_Completion_Report.md` §3 for the precise blockers and §4 for the activation sequence once they clear).
