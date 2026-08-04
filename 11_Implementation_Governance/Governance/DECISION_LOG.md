# DECISION_LOG.md
### Master Governance Decision Log — ALCSM Thesis Project

---

## 1. Project information

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles.*
**Author:** Samiksha Dhere, MSc Applied Data Science & Analytics, SRH University Heidelberg (Campus Hamburg).
**Repository:** `AI_Leadership_Credential_Gap_Analysis` (GitHub: `samu2421/AI-Leadership-Credential-Gap-Analysis-ALCSM-`).
**Governing documents:** `PROJECT_CONTEXT.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `CLAUDE_CODE_RULES.md`, `Document_Version_Policy.md`, `Implementation_Phase_Roadmap.md` (all in `11_Implementation_Governance/`).
**Current phase at time of writing:** P2 (Research Governance and Ethics) — P0 and P1 complete and tagged (`p0-complete`, `p1-complete`).

---

## 2. Purpose

This log is the single, permanent, chronological record of every consequential decision made across the life of this project — methodological, architectural, and procedural. It exists so that:

- no decision is ever re-litigated from memory or guesswork;
- every frozen or resolved item has one findable place recording *what* was decided, *why*, and *by whom*;
- a future reader (examiner, supervisor, or a later implementation session) can reconstruct the reasoning behind the current state of the repository without re-reading every historical document;
- decisions that are later superseded remain visible, not silently erased — the history of *why something changed* is as important as the current answer.

This log **records** decisions; it does not **make** them. Recording a decision here never substitutes for the approval process that decision required (author sign-off, committee approval, etc.) — the log is the audit trail of decisions made elsewhere, in the governing documents, in prior sessions, or by the author directly.

---

## 3. How decisions are recorded

- **Append-only.** New entries are added to the end of §7 in chronological order. An existing entry's core fields (ID, Date, Decision) are never rewritten after the fact.
- **Corrections happen by superseding, not editing.** If a recorded decision turns out to be wrong, incomplete, or reversed, a **new** entry is added referencing the old one (`Supersedes: D-00XX`), and the old entry's **Status** field is updated to `Superseded` with a pointer forward (`Superseded by: D-00YY`). The original entry's content is never deleted or rewritten.
- **One entry per decision**, not per document edit. A single decision may be reflected across several files (e.g. a schema freeze touches `VERSION.md`, `PROJECT_CONTEXT.md`, and the schema file's own header) — that is still one log entry, with all affected files listed under **References**.
- **Every entry states what governing document(s) it lives in**, so this log is a *pointer index* into the authoritative material, not a duplicate of it. Where this log's summary and a source document ever appear to differ, the source document governs — flag the discrepancy rather than trusting the log's paraphrase.
- **Entries are added at the time work is done or reviewed**, including retroactively for decisions made before this log existed (this initial population, §7, is exactly that: a retroactive, evidence-based reconstruction of every major decision from Task 1 through the end of Phase P1, sourced from `VERSION.md`, `Consistency_Review_Tasks1-4.md`, `Document_Version_Policy.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `P1_Completion_Summary.md`, and this repository's git history).

---

## 4. Decision numbering

- Format: **D-NNNN**, four digits, zero-padded, strictly sequential (`D-0001`, `D-0002`, …).
- Numbers are **never reused or renumbered**, even if a decision is later rejected or superseded — a rejected decision still occupied a real point in the project's history and keeps its number.
- Numbering is global across the whole project (methodology, schema, architecture, process) — there is deliberately no per-category sub-numbering, so the sequence itself is a chronological table of contents.

---

## 5. Decision template

Every entry in §7 uses this exact field set:

```
### D-NNNN — <short title>

- **Date:** YYYY-MM-DD (or "pre-P0, exact date not separately recorded" where genuinely unknown)
- **Status:** Approved | Rejected | Deprecated | Superseded | Pending
- **Category:** Methodology | Database | Architecture | Process | Governance
- **Decided by:** <person/role — the author, a named reviewer, or "Claude Code, per author instruction/session scope">
- **Context:** what situation or question prompted this decision
- **Decision:** the decision itself, stated plainly
- **Rationale:** why this and not an alternative
- **Consequences:** what this binds or rules out going forward
- **References:** the governing document(s)/file(s)/commit(s) this decision lives in
- **Supersedes / Superseded by:** (only if applicable)
```

---

## 6. Status values

| Status | Meaning |
|---|---|
| **Approved** | In force; the current, binding answer. |
| **Rejected** | Considered and explicitly declined — recorded so it is not proposed again without new information. |
| **Deprecated** | Was once in force, is no longer the recommended path, but nothing else has formally replaced it (weaker than Superseded — used when a thing is simply retired rather than swapped for a named alternative). |
| **Superseded** | Replaced by a specific, later decision — always paired with a `Superseded by:` pointer to the entry that replaced it. |
| **Pending** | Raised, not yet resolved — awaiting author/institutional decision. Tracked here so it isn't lost. |

---

## 7. Decision log (chronological)

### D-0001 — ALCSM Framework v1.0 frozen

- **Date:** 2026-07-26
- **Status:** Approved
- **Category:** Methodology
- **Decided by:** Samiksha Dhere (author)
- **Context:** Completion of Tasks 1–4 (literature review, dimension design, scoring framework, database design).
- **Decision:** The ALCSM conceptual model — six dimensions, their theoretical anchors, and their 0–5 scoring criteria — is frozen at v1.0. No in-place edits are permitted.
- **Rationale:** The dimensions are theory-derived (signalling theory, reputation theory, upper-echelons theory, AI-literacy framework), not arbitrary; freezing them before implementation prevents scope drift and keeps the research reproducible.
- **Consequences:** Every later phase (P3–P8) implements against these fixed criteria. Any change to a dimension or its criteria is a framework-version decision (v1.1/v2.0), never an implementation choice — see `CLAUDE_CODE_RULES.md` rule 1.
- **References:** `VERSION.md`; `PROJECT_CONTEXT.md` §41; `02_Framework_Development/`.

### D-0002 — ALCSM Database Schema v1.0.1 frozen

- **Date:** 2026-07-26
- **Status:** Approved
- **Category:** Database
- **Decided by:** Samiksha Dhere (author)
- **Context:** Completion of Task 4; schema validated on live PostgreSQL 16 with a 67-test harness.
- **Decision:** The schema — 22 base tables, 5 views, 33 `ON DELETE RESTRICT` foreign keys, 66 CHECK constraints — is frozen at v1.0.1, defined solely in `alcsm_schema_v1.0.1.sql`.
- **Rationale:** The schema encodes research rules (missing-data semantics, D4-only verification, additive adjudication) as constraints, not documentation, so they cannot silently erode across hundreds of records. Freezing it before implementation guarantees every later phase builds on the same structural guarantees.
- **Consequences:** No table/column/constraint/view may be added, altered, or removed without an explicit author-approved version bump. SQLAlchemy and all application code read and write through this structure; none of it owns or redefines it.
- **References:** `VERSION.md`; `PROJECT_CONTEXT.md` §13, §42; `03_Database_Design/02_Schema/alcsm_schema_v1.0.1.sql`.

### D-0003 — Numbered thesis-folder structure (00–17) adopted

- **Date:** 2026-07-26
- **Status:** Approved (see D-0018 for a later correction to this structure's documentation)
- **Category:** Process
- **Decided by:** Samiksha Dhere (author)
- **Context:** Need for a single, consistent folder organisation covering Task 5 through final submission.
- **Decision:** Adopt the `00_Project_Management` … `17_Archive` numbered folder scheme as the project-wide organisation, documented in `PROJECT_STRUCTURE.md`.
- **Rationale:** One consistent, numbered scheme keeps thesis-task material, governance material, and (later) software scaffolding separable but co-located.
- **Consequences:** All future work is organised under this scheme. Software engineering scaffolding (`src/alcsm/`, `tests/`) added later sits alongside it as additive, not a replacement (see D-0017).
- **References:** `VERSION.md`; `PROJECT_STRUCTURE.md`.

### D-0004 — Coding-rulebook revision rule reconciled: wording, never criteria (Consistency Review C-1)

- **Date:** pre-P0 (Consistency Review dated before Task 5 implementation guide authorship; exact calendar date not separately recorded)
- **Status:** Approved
- **Category:** Methodology
- **Decided by:** Samiksha Dhere (author), per the Consistency Review's recommendation
- **Context:** `ALCSM_Coding_Rulebook_and_Pilot_Design.md` (pre-freeze) instructed revising *"the scoring criteria"* on a failing reliability dimension; every post-freeze document instead says revise the *rulebook wording*, never the frozen criteria — a direct contradiction once the framework froze.
- **Decision:** The correct, binding rule is: a failing dimension (α < .667) triggers a revision to rulebook **wording/annotation guidance** only, followed by a re-pilot. The 0–5 criteria themselves are never altered in response to a reliability result.
- **Rationale:** The rulebook predates the framework freeze (D-0001); its literal text is a leftover from before criteria were fixed. Following it literally post-freeze would authorise altering a frozen element through the back door of a reliability failure.
- **Consequences:** `reliability/krippendorff.py` (P5) and any pilot-revision process must route changes through the wording-revision log, never a criteria edit. Binds `annotation_revision_log`.
- **References:** `Consistency_Review_Tasks1-4.md` C-1; `Task5_Implementation_Readiness_Checklist.md` §1 ("Approved reconciliation C-1 applied"); `PROJECT_CONTEXT.md` §41, §48.

### D-0005 — Table/view count corrected to 22 tables, 5 views (Consistency Review C-2)

- **Date:** pre-P0 (same review cycle as D-0004)
- **Status:** Approved
- **Category:** Database
- **Decided by:** Samiksha Dhere (author)
- **Context:** `Task4_Data_Schema_Design.md` stated "eighteen tables"; `Task4c_ER_Design_Documentation.md` and `PATCH_NOTES_v1.0.1.md` both independently gave 22, verified against the deployed catalogue.
- **Decision:** 22 base tables and 5 analysis views is the correct, authoritative figure everywhere.
- **Rationale:** The 22/5 figure is empirically verified against the live database catalogue; "eighteen" was an earlier undercount.
- **Consequences:** All forward-looking documents (`PROJECT_CONTEXT.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`) cite 22/5. `Task4_Data_Schema_Design.md` retains its original "eighteen" text as a historical document and is not rewritten (per `Document_Version_Policy.md`'s rule that historical documents are not retroactively corrected).
- **References:** `Consistency_Review_Tasks1-4.md` C-2; `Task5_Implementation_Readiness_Checklist.md` §1; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §4.

### D-0006 — Canonical literature file designated (Consistency Review D-2)

- **Date:** pre-P0
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author)
- **Context:** Two near-identical literature files existed: `Task1_Literature_Annotations_v1.md` and `Literature_Remapping_and_Annotations_v1.md`.
- **Decision:** `Literature_Remapping_and_Annotations_v1.md` is canonical; the other is archived.
- **Rationale:** Its title accurately reflects the actual content (an honest remapping), and it is the file all later documents already cite.
- **Consequences:** Only the canonical file is cited or edited going forward.
- **References:** `Consistency_Review_Tasks1-4.md` D-2; `Document_Version_Policy.md` canonical register.

### D-0007 — Archive policy established: superseded files retained, never deleted (Consistency Review D-3)

- **Date:** pre-P0
- **Status:** Approved (path corrected later — see D-0018)
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author)
- **Context:** Superseded schema/validation artefacts (`alcsm_schema_v1.sql`, old validation harness, old gap probes) sat alongside their canonical replacements with no formal archive location.
- **Decision:** Superseded files are moved (never deleted) into an archive location, retained permanently for history; `Document_Version_Policy.md` is the canonical register of what is current vs. archived.
- **Rationale:** Nothing in a research project's audit trail should be destroyed; a wrong-but-retained file is safe, a deleted one is not recoverable if a question arises later.
- **Consequences:** Every future version bump moves the prior canonical file to archive and updates the register; never leaves two files both claiming to be canonical.
- **References:** `Consistency_Review_Tasks1-4.md` D-3; `Document_Version_Policy.md`.

### D-0008 — SQLAlchemy is an application layer only; reflection, never schema ownership (Consistency Review M-1)

- **Date:** pre-P0
- **Status:** Approved — final, author-approved
- **Category:** Architecture
- **Decided by:** Samiksha Dhere (author)
- **Context:** The implementation guide requested SQLAlchemy, but every database artefact to date was raw DDL + psycopg2; no ORM model layer existed, and nothing in the frozen design required one.
- **Decision:** SQLAlchemy is used only for engine/session lifecycle (`db/engine.py`) and read access via models **reflected from** the deployed schema. It must never define tables declaratively, call `create_all()`, or run migrations (no Alembic) against the research database. If reflected models and the live schema ever disagree, fail fast — never "fix" the database to match the code.
- **Rationale:** The DDL file is the single source of truth (D-0002); an ORM that owns schema would create a second, competing source of truth.
- **Consequences:** `db/models.py` only reflects; no declarative `Base` classes defining columns anywhere in this codebase.
- **References:** `Consistency_Review_Tasks1-4.md` M-1; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §8; `PROJECT_CONTEXT.md` §23; `CLAUDE_CODE_RULES.md` rule 3.

### D-0009 — Single write path: the psycopg2 collection helper is sole authoritative insertion path (Consistency Review M-2)

- **Date:** pre-P0
- **Status:** Approved — final
- **Category:** Architecture
- **Decided by:** Samiksha Dhere (author)
- **Context:** `collection_helper.py` (psycopg2) already inserts profiles; a future SQLAlchemy layer (D-0008) could offer a second insertion path, which is a data-integrity risk for a frozen schema.
- **Decision:** `collection/helper.py` remains the single authoritative write path for profile collection. If it is ever ported onto SQLAlchemy Core, the psycopg2 version is retired in the same change — two write paths must never coexist.
- **Rationale:** Two independent paths writing to the same frozen structure can drift out of sync on validation rules; one path is the only way to guarantee every insert is validated identically.
- **Consequences:** `src/alcsm/collection/helper.py` (built in P1) is this path; `db/engine.py`'s SQLAlchemy engine is never used for writes.
- **References:** `Consistency_Review_Tasks1-4.md` M-2; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §8, §27; `P1_Completion_Summary.md` §5.

### D-0010 — Python 3.11+ and `pyproject.toml` fixed as the environment/dependency standard (Consistency Review M-3)

- **Date:** pre-P0 (decision fixed); executed 2026-07-28 (see D-0019)
- **Status:** Approved
- **Category:** Architecture
- **Decided by:** Samiksha Dhere (author)
- **Context:** No document fixed a Python version, dependency manager, or virtual-env convention before the implementation guide.
- **Decision:** Python 3.11+, with `pyproject.toml` as the single dependency/tooling configuration file (black, ruff, mypy, pytest).
- **Rationale:** Modern type-hinting features and a single-file config reduce ambiguity for a research codebase that must remain auditable.
- **Consequences:** All `src/alcsm/` code targets 3.11+ syntax; the actual development `.venv` was later rebuilt to match (D-0019).
- **References:** `Consistency_Review_Tasks1-4.md` M-3; `PROJECT_CONTEXT.md` §20; `pyproject.toml`.

### D-0011 — No composite ALCSM score, anywhere, ever (Consistency Review M-4)

- **Date:** pre-P0
- **Status:** Approved — final, non-negotiable
- **Category:** Methodology
- **Decided by:** Samiksha Dhere (author)
- **Context:** A Streamlit scoring app is planned (RQ5), but aggregation function and dimension weights are deliberately open research questions — the app cannot display one composite number without silently pre-choosing a method.
- **Decision:** The system reports six dimension scores; it never collapses them into one default number. If an aggregated view is ever shown, it must be a clearly-labelled, exploratory panel comparing candidate methods — never a single hard-coded "the ALCSM score."
- **Rationale:** Aggregation is an open empirical question (§44); hard-coding one method would silently commit the research to an unvalidated choice.
- **Consequences:** No table anywhere stores a composite/total/weight/band column (enforced structurally, D-0002); `app/streamlit_app.py` (P8) and `analysis/*` must never compute or display one.
- **References:** `Consistency_Review_Tasks1-4.md` M-4; `PROJECT_CONTEXT.md` §6, §8, §44; `CLAUDE_CODE_RULES.md` rule 2.

### D-0012 — No external-API processing of profile text; local/EEA models only (Consistency Review M-5)

- **Date:** pre-P0
- **Status:** Approved — final, GDPR-tied
- **Category:** Architecture
- **Decided by:** Samiksha Dhere (author)
- **Context:** RQ5 needs an NLP pipeline; sending profile text to a hosted third-party API would engage GDPR Chapter V international-transfer rules and is a data-protection risk, not just a technical preference.
- **Decision:** The NLP pipeline (P7) uses only local or explicitly EEA-approved models — spaCy, sentence-transformers, locally-run HuggingFace models — in that order of escalation. No LinkedIn profile text is ever sent to a hosted/third-party LLM or NLP API.
- **Rationale:** This is a hard constraint tied to the project's GDPR position, not overridable by convenience or performance.
- **Consequences:** Any future model choice for `nlp/classify.py` is checked against this constraint before adoption.
- **References:** `Consistency_Review_Tasks1-4.md` M-5; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §10; `PROJECT_CONTEXT.md` §25, §45; `CLAUDE_CODE_RULES.md` rule 8.

### D-0013 — Double-coding policy standardised (Consistency Review A-1)

- **Date:** pre-P0
- **Status:** Approved
- **Category:** Methodology
- **Decided by:** Samiksha Dhere (author)
- **Context:** Three different documents stated the double-coding proportion differently ("10–15%", "≥15%", "a pre-registered random subset (or 100%)").
- **Decision:** Canonical wording, used everywhere: *"100% double coding if feasible; otherwise a pre-registered random subset of at least 15%."*
- **Rationale:** A single figure prevents divergent implementations reading different floors into the requirement.
- **Consequences:** P4/P6's rater-assignment logic and pre-registration must match this exact wording.
- **References:** `Consistency_Review_Tasks1-4.md` A-1; `PROJECT_CONTEXT.md` §43, §48; `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` §15.

### D-0014 — Deferred schema hardening (F-06/F-07/F-08) is intentional, not a defect (Consistency Review A-2)

- **Date:** pre-P0
- **Status:** Approved
- **Category:** Database
- **Decided by:** Samiksha Dhere (author)
- **Context:** Task 4 is declared frozen, yet three hardening items (taxonomy NOT NULL, ISO/temporal hygiene, activity/ethics trigger) remain deliberately unapplied in `alcsm_optional_recommendations.sql`.
- **Decision:** "Frozen" means no conceptual/structural change to what's deployed; F-06/F-07/F-08 are deferred implementation hardening, enabled on schedule (F-06 after taxonomy anchoring/P3, F-08 after ethics/P2) — their current absence is not a defect to "fix" early.
- **Rationale:** Prevents a future session from either wrongly enabling them early or wrongly treating their absence as a bug.
- **Consequences:** F-06 is enabled only as part of P3's completion criteria; F-08 only after P2 clears.
- **References:** `Consistency_Review_Tasks1-4.md` A-2; `PROJECT_CONTEXT.md` §17, §44; `Implementation_Phase_Roadmap.md` §3 (P3).

### D-0015 — RQ4 criterion-extraction timing fixed (Consistency Review A-3)

- **Date:** pre-P0
- **Status:** Approved
- **Category:** Methodology
- **Decided by:** Samiksha Dhere (author)
- **Context:** One document implied criterion extraction could lag annotation; another implied time-sensitive values must be captured at collection. The schema supports either (nullable `rq4_impact_indicator`).
- **Decision:** Time-sensitive criterion values (network reach, content engagement) are captured **at collection**; derived values (seniority-progression rate) are computed **later** from stored data.
- **Rationale:** Reach/engagement are point-in-time and decay in relevance if captured late; progression rate is inherently a later computation over historical data.
- **Consequences:** `collection/helper.py`'s optional `Rq4Criterion` insertion path captures the time-sensitive fields; a later pass (not yet built) derives the progression rate.
- **References:** `Consistency_Review_Tasks1-4.md` A-3; `src/alcsm/collection/helper.py` (`Rq4Criterion`).

### D-0016 — Measurement Specification canonical file designated as `_Final` (initial designation)

- **Date:** pre-P0 (recorded in `Document_Version_Policy.md` before the P0 cleanup session; exact date not separately recorded)
- **Status:** Superseded — see D-0026
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author), per the Consistency Review D-1 recommendation
- **Context:** Two files existed claiming to be the definitive v1.0 measurement specification: `ALCSM_Measurement_Specification_v1.0.md` (37,995 bytes) and `ALCSM_Measurement_Specification_v1.0_Final.md` (41,265 bytes, believed larger/superseding).
- **Decision (as originally recorded):** `ALCSM_Measurement_Specification_v1.0_Final.md` is canonical; the non-`_Final` file is archived.
- **Rationale (at the time):** The larger file was assumed to supersede the smaller one, pending author confirmation.
- **Consequences (at the time):** Governance documents (`PROJECT_CONTEXT.md`, `README.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`) cited the `_Final` filename.
- **References:** `Consistency_Review_Tasks1-4.md` D-1; `Document_Version_Policy.md` (original register entry).
- **Superseded by:** D-0026.

### D-0017 — Phase P0 (Environment) completed

- **Date:** 2026-07-29 (commit tagged `p0-complete`)
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code
- **Context:** First implementation phase per the roadmap.
- **Decision:** P0 is complete: `src/alcsm/` package scaffolding, `pyproject.toml`, `.gitignore`, module skeletons (`db/`, `reliability/`, `taxonomy/`, `nlp/`, `analysis/`, `app/`, `collection/`, all with TODO markers and no real logic), schema deployed to a local dev database, 67-test validation harness green, reference data (6 dimensions, 4 missing-status values) loaded.
- **Rationale:** Establishes tested foundations before any further software is built.
- **Consequences:** P1 (and onward) build on this baseline; tagged so it can always be returned to.
- **References:** `Implementation_Phase_Roadmap.md` §3 (P0); this repository's git history (`p0-complete`).

### D-0018 — Thesis-folder numbering documentation corrected; archive path corrected

- **Date:** 2026-07-28
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Claude Code, per author instruction (P0-cleanup governance session)
- **Context:** `PROJECT_STRUCTURE.md` and `VERSION.md` numbered folders `01`–`17` and omitted `11_Implementation_Governance` entirely; the actual repository is numbered `00`–`17` and includes that folder. Separately, `Document_Version_Policy.md` cited an archive path (`Archive/Superseded_Task1_Task4/`) that never existed on disk; the real archive root is `17_Archive/`.
- **Decision:** `PROJECT_STRUCTURE.md` and `VERSION.md` corrected to describe the actual `00`–`17` structure, including `11_Implementation_Governance`. Four superseded Task 1–4 database-design files moved into `17_Archive/Superseded_Task1_Task4/`; `Document_Version_Policy.md`'s register corrected to that path.
- **Rationale:** Documentation must describe the repository that actually exists; a navigation document that disagrees with disk misleads every future session.
- **Consequences:** Both documents now agree with each other and with the filesystem. This was a navigation-only correction — no thesis methodology or frozen framework/schema content was altered.
- **References:** `VERSION.md` Version Log (2026-07-28 row); `PROJECT_STRUCTURE.md` §2 correction note; `Document_Version_Policy.md` §Purpose/register.

### D-0019 — Python environment upgraded to 3.11 to satisfy D-0010

- **Date:** 2026-07-28 (confirmed working in the P0-cleanup session)
- **Status:** Approved
- **Category:** Architecture
- **Decided by:** Samiksha Dhere (author) — `.venv` rebuilt between sessions; confirmed and verified by Claude Code
- **Context:** `pyproject.toml` declares `requires-python = ">=3.11"` (D-0010), but the project's `.venv` was initially Python 3.9.6.
- **Decision:** The development virtual environment is rebuilt on Python 3.11.14 (Homebrew).
- **Rationale:** Brings the actual environment into compliance with the already-fixed technology-stack decision; avoids a latent mismatch between declared and actual requirements.
- **Consequences:** All P0/P1 tooling (black/ruff/mypy/pytest) verified green on 3.11.14.
- **References:** P0-cleanup session record (this conversation); `pyproject.toml`.

### D-0020 — Schema deployed to local development database (`alcsm_dev`); validation harness re-run clean

- **Date:** 2026-07-28/29
- **Status:** Approved
- **Category:** Database
- **Decided by:** Claude Code, per author instruction
- **Context:** P0 requires a working dev database from the frozen schema.
- **Decision:** `alcsm_schema_v1.0.1.sql` deployed to a local PostgreSQL 16 database (`alcsm_dev`); the 67-test validation harness and gap-integrity probes were re-run against a separate throwaway cluster (never against `alcsm_dev` itself, to avoid seeding it with the harness's synthetic test rows) — 67/67 tests passed; integrity probes showed only the already-documented deferred-hardening gaps (D-0014).
- **Rationale:** Confirms the frozen schema deploys clean in this environment before any application code depends on it.
- **Consequences:** `alcsm_dev` holds only the DDL-seeded reference rows (`dimension_ref`, `missing_status_ref`) — zero profile or research data, confirmed repeatedly across sessions.
- **References:** P0-cleanup session record; `03_Database_Design/03_Validation/alcsm_validation_harness_v1.0.1.py`.

### D-0021 — Phase P1 (Collection tooling) completed

- **Date:** 2026-07-29 (commit tagged `p1-complete`)
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code
- **Context:** Second implementation phase per the roadmap.
- **Decision:** P1 is complete: `collection_helper.py` ported into `src/alcsm/collection/helper.py` as a production module (dataclasses, typed exceptions, logging, config-driven connection factory); 60 tests (46 pure-logic + 14 real-database integration); backup script (`backup_alcsm.sh`) verified and one portability bug fixed (D-0023).
- **Rationale:** Proves the write path against constructed fixtures before any real data touches it.
- **Consequences:** P2 may now begin; P3/P4/P6 will use this tooling operationally, not rebuild it.
- **References:** `Implementation_Phase_Roadmap.md` §3 (P1); `P1_Completion_Summary.md`; this repository's git history (`p1-complete`).

### D-0022 — Historical collection-helper prototype retained unmodified

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Claude Code, within session scope; not challenged by author
- **Context:** `05_Data_Collection/Scripts/collection_helper.py` was the prototype described as "the implementation baseline" to port *from* into `src/alcsm/collection/helper.py`.
- **Decision:** The original prototype file is left byte-identical; only the new, ported module is treated as production code.
- **Rationale:** Nothing instructed modifying or archiving the prototype; the collection workflow documentation still cites it as the original reference implementation.
- **Consequences:** Two files with overlapping logic now exist by design — the prototype (historical reference, never executed) and the production module (`src/alcsm/collection/helper.py`, the only one imported/tested/used).
- **References:** `P1_Completion_Summary.md` §3.

### D-0023 — Backup script portability fix: `stat -c%s` replaced with `wc -c`

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Architecture
- **Decided by:** Claude Code, per explicit P1-closure instruction ("if modifications are required, explain why first, make only minimal changes")
- **Context:** `backup_alcsm.sh` used `stat -c%s` (GNU-only syntax) to report a dump's byte size; confirmed by direct execution to fail with `illegal option -- c` on macOS/BSD, producing a spurious error and a blank byte count (the script did not hard-crash, but its output was wrong).
- **Decision:** Replaced with `wc -c < "${DUMP}" | tr -d '[:space:]'`, portable across GNU/Linux and BSD/macOS with no new dependency. A second suspected issue, `xargs -r`, was investigated and confirmed to be an intentional, documented BSD/macOS compatibility no-op — left unchanged.
- **Rationale:** Minimal, explained, verified-necessary fix; no schema, methodology, or behavioural change beyond correct byte-count reporting.
- **Consequences:** The script now runs cleanly (verified via 8 new automated tests) on this development platform and remains correct on Linux.
- **References:** `P1_Completion_Summary.md` §5–6; `03_Database_Design/Backup/backup_alcsm.sh`; `tests/scripts/test_backup_alcsm.py`.

### D-0024 — DB-integration tests use real throwaway PostgreSQL clusters, not mocks

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Process
- **Decided by:** Claude Code, applying `PROJECT_CONTEXT.md` §33's existing testing-strategy principle
- **Context:** Testing constraint violations, transaction rollback, and duplicate handling meaningfully requires a real database enforcing the real schema; mocking psycopg2 would only prove a mock behaves as expected.
- **Decision:** Both the collection-helper tests and the backup-script tests provision a disposable, auto-torn-down PostgreSQL 16 cluster (with the real v1.0.1 schema deployed) per test session, entirely separate from `alcsm_dev`.
- **Rationale:** Directly implements the project's own stated principle: "test against the specification, not the implementation."
- **Consequences:** The test suite has an environmental dependency on local PostgreSQL 16 binaries; DB-integration tests skip (not fail) with a clear reason if those binaries are absent, keeping pure-logic tests portable regardless.
- **References:** `PROJECT_CONTEXT.md` §33; `tests/collection/conftest.py`; `tests/scripts/conftest.py`.

### D-0025 — `Implementation_Phase_Roadmap.md` created as the authoritative P0–P8 roadmap

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (governance-only session)
- **Context:** A governance review found the P0–P8 roadmap phrased slightly differently across `PROJECT_CONTEXT.md`, `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, and `PROJECT_STRUCTURE.md` (see the three findings recorded in that document's §9).
- **Decision:** `11_Implementation_Governance/Roadmaps/Implementation_Phase_Roadmap.md` is created as the consolidated, authoritative phase-by-phase reference (purpose, objectives, allowed/out-of-scope work, deliverables, dependencies, completion criteria, git tag per phase for P0–P8), explicitly following the "P0 through P8" framing given in that session's instructions, with the P8/P9 disagreement flagged rather than silently resolved.
- **Rationale:** Formalises what already existed across multiple documents into one place without inventing, merging, or splitting any phase; makes the known cross-document disagreements visible rather than hiding them.
- **Consequences:** This document is the reference point for "what phase am I in and what may I do" going forward; the underlying disagreement it documents (P8-bundles-the-app vs. a separate P9) remains open for the author to confirm.
- **References:** `Implementation_Phase_Roadmap.md` (full document, especially §9).

### D-0026 — Measurement Specification canonical decision finalised: surviving file is canonical, `_Final` confirmed lost

- **Date:** 2026-07-28
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author), confirmed during the P0-cleanup governance session
- **Context:** A repository-wide search found no `ALCSM_Measurement_Specification_v1.0_Final.md` anywhere (live, archived, or under any other name) — only the 37,995-byte non-`_Final` file exists, live in `02_Framework_Development/`. The author confirmed the `_Final` version is lost and not recoverable from this repository.
- **Decision:** `ALCSM_Measurement_Specification_v1.0.md` (the surviving file) is now the canonical measurement specification. All citations in `README.md`, `PROJECT_CONTEXT.md`, and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` were corrected to reference this filename. No content was rewritten — only the canonical designation and citations changed.
- **Rationale:** A canonical designation pointing at a file that does not exist is worse than designating the file that actually survives; citing a real, present document is the only workable resolution once the alternative is confirmed unrecoverable.
- **Consequences:** This decision reverses D-0016. Any historical document (e.g. `Consistency_Review_Tasks1-4.md`) that still describes the two-file situation as it stood *at the time* is not rewritten — that description was accurate when written.
- **References:** `Document_Version_Policy.md` note 5; P0-cleanup session record.
- **Supersedes:** D-0016.

### D-0027 — P2 Session 1 completed: roadmap consistency review + this log's own creation

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (governance-only session)
- **Context:** First session of Phase P2 (Research Governance and Ethics). Objective was to verify roadmap numbering consistency, establish a permanent decision log, review the repository for missing governance folders, and propose (not create) a folder structure for `04_Ethics/`.
- **Decision:** `DECISION_LOG.md` itself created (this file), populated retroactively with D-0001–D-0026 covering every decision from Task 1 through the end of Phase P1. Roadmap numbering re-verified consistent with `Implementation_Phase_Roadmap.md`'s prior findings (no change). A nine-subfolder structure for `04_Ethics/` (`01_Ethics_Approval` through `09_Review_Logs`) was proposed and documented, but deliberately **not** instantiated this session — folder creation was left for explicit author approval first.
- **Rationale:** Establishes the permanent decision-history record before further P2 governance work proceeds, and separates "propose a structural change" from "make it," consistent with this project's standing practice of not silently acting on structural recommendations.
- **Consequences:** `04_Ethics/`'s proposed structure became the basis for P2 Session 2 (D-0028) once approved.
- **References:** this file's own creation; the P2 Session 1 conversation record.

### D-0028 — P2 Session 2 completed: `04_Ethics/` folder structure instantiated; governance/GDPR documentation package drafted

- **Date:** 2026-07-29
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author), executed by Claude Code
- **Context:** The nine-subfolder `04_Ethics/` structure proposed in P2 Session 1 (D-0027) was approved; the session's objective was to instantiate it and draft the full governance documentation package needed before real-data collection can begin.
- **Decision:** Nine subfolders created under `04_Ethics/`, each with its own `README.md`. Eleven substantive draft documents created: the Ethics Application and its LinkedIn Collection Protocol annex, a DPIA screening note and full DPIA, a Legitimate Interests Assessment, a public Article 14 privacy notice, a survey participant information sheet and consent form, a Data Management Plan, a GDPR compliance checklist, and a governance consistency review. Every document uses placeholder fields (`[INSERT: ...]`) for institution-specific information and is explicitly marked as an unapproved draft — no approval, committee name, or reference number is fabricated anywhere.
- **Rationale:** Operationalises the governance content already reasoned through in `Task5_PreCollection_Roadmap.md` and `Task5_LinkedIn_Collection_Workflow.md` into standalone, submission-shaped documents, so the package is ready for supervisor/DPO/committee review once real institutional details are supplied.
- **Consequences:** This package became the subject of the QA review in P2 Session 3 (D-0029) and the cleanup in P2 Session 4.
- **References:** `04_Ethics/` (full tree); the P2 Session 2 conversation record.

### D-0029 — P2 Session 3 completed: governance QA review performed (findings only, no fixes applied)

- **Date:** 2026-07-30
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (governance-validation-only session, no documents modified)
- **Context:** Before freezing the P2 documentation-drafting stage, a comprehensive QA pass was run over every document from P2 Sessions 1–2, plus a repository-wide consistency check against the nine core governance documents.
- **Decision:** `11_Implementation_Governance/Reviews/P2_Governance_QA_Report.md` created, recording: zero legal/methodological defects found; four minor documentation-hygiene issues (a naming-convention self-contradiction, one missing document header, one placeholder-punctuation outlier, a stale `PROJECT_STRUCTURE.md` folder-tree diagram); two moderate content gaps worth strengthening before real submission (the Collection Protocol's silence on logged-in/out browsing policy, and the Full DPIA's missing consultation section); a consolidated 39-field placeholder checklist; and a "Ready to Freeze, conditional on fixes" recommendation. Per this session's explicit instruction, every finding was reported, none was silently fixed.
- **Rationale:** Separates *finding* issues from *fixing* them, so the author retains an explicit approval point before any of the governance package's content changes.
- **Consequences:** Every finding in this review became a scoped task in P2 Session 4 (see the corresponding session-4 entries once logged).
- **References:** `11_Implementation_Governance/Reviews/P2_Governance_QA_Report.md` (full document).

### D-0030 — P2 Session 4 completed: governance documentation cleanup closed; P2 documentation stage assessed as ready for P3

- **Date:** 2026-07-30
- **Status:** Approved
- **Category:** Governance
- **Decided by:** Samiksha Dhere (author), executed by Claude Code
- **Context:** Closing out every documentation-quality finding from the Session 3 QA report before treating the P2 documentation-drafting stage as frozen.
- **Decision:** All four documentation-hygiene findings (naming-convention self-contradiction, missing document header, placeholder-punctuation outlier, header-spacing inconsistency) fixed; both moderate content gaps closed (Collection Protocol §2 rewritten with nine explicit collection-method boundaries including a stated logged-out-preferred/logged-in-fallback browsing policy; Full DPIA given a new Part F — Consultation section addressing Art 35(9)); `PROJECT_STRUCTURE.md`'s `04_Ethics/` tree expanded to match actual disk structure; all 11 substantive ethics documents given a uniform five-field metadata header (Version, Status, Purpose, Last Updated, Author). `11_Implementation_Governance/Reviews/P2_Final_Governance_Review.md` created recording the closure and a **READY FOR P3** (documentation-readiness) verdict. One new, minor issue was found and deliberately left unfixed (a stale `# 05_Ethics` heading in `04_Ethics/README.md`, outside this session's pre-approved scope) — reported, not silently corrected.
- **Rationale:** Every fix applied was either explicitly pre-approved by name in this session's instructions or a direct, scoped resolution of a specific Session 3 QA finding; nothing outside that scope was changed, consistent with this project's standing "report first" discipline for anything not explicitly authorised.
- **Consequences:** The P2 documentation package is now internally consistent and ready for supervisor/DPO/committee review. Real ethics approval, DPO sign-off, and placeholder resolution remain outstanding and are unaffected by this session — P2 itself does not clear, and P3 does not actually begin, until those external steps complete.
- **References:** `11_Implementation_Governance/Reviews/P2_Final_Governance_Review.md` (full document); `04_Ethics/` (all files touched this session).

### D-0031 — P3 Session 1 completed: collection infrastructure audited, profile-sampling and job-posting design documents drafted, no real data collected

- **Date:** 2026-08-02
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (infrastructure-and-design-only session; explicitly no real data collection)
- **Context:** First session of Phase P3 ("Job postings and taxonomy anchoring"). Real ethics approval remains pending, so this session was scoped to infrastructure audit and design preparation only, per explicit instruction.
- **Decision:** Repository audited and confirmed internally consistent post-P2 (95/95 tests green, clean git state); P1 collection infrastructure reviewed and confirmed reusable for the profile side, with a documented (not implemented) gap on the job-posting side; `Task5_P3_Sampling_Framework_Design.md` and `Task5_P3_JobPosting_Collection_Plan.md` drafted, formalising and extending `Task5_PreCollection_Roadmap.md` §5/§7 without any schema change; `P3_Session1_Test_Strategy.md` drafted defining the testing approach for Session 2's implementation work; roadmap phase ordering re-confirmed (no renumbering, no merging). Five pre-existing or newly-surfaced issues reported without being fixed (a stray `requirements.txt` contradicting D-0010/D-0008; a never-created `.env.example`; a third instance of the stale-README-heading pattern already tracked in §8 below; a third data point for the open F-1 P8/P9 disagreement; the concrete job-posting/anchoring code gaps).
- **Rationale:** Matches this project's standing practice of separating "prepare infrastructure and design" from "execute on real data," and of reporting issues before fixing them absent explicit pre-approval — none of the five issues found were clearly P3-scoped, so none were fixed this session.
- **Consequences:** P3 Session 2 may proceed to implement the job-posting write path and `taxonomy/anchoring.py` against the designs and test strategy produced here. Real job-posting/profile collection remains blocked on real ethics approval, unaffected by this session.
- **References:** `11_Implementation_Governance/Reviews/P3_Session1_Infrastructure_Readiness_Report.md` (full document); `05_Data_Collection/Documentation/Task5_P3_Sampling_Framework_Design.md`; `05_Data_Collection/Documentation/Task5_P3_JobPosting_Collection_Plan.md`; `11_Implementation_Governance/Guides/P3_Session1_Test_Strategy.md`.

### D-0032 — P3 Session 2 completed: job-posting collection infrastructure built (no real data, no term generation)

- **Date:** 2026-08-02
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (engineering-infrastructure-only session; explicitly no real data collection, no taxonomy term generation, no NLP)
- **Context:** Second session of Phase P3, building on the design documents and gap analysis from Session 1 (D-0031). Objective was to bring job-posting collection tooling to the same maturity as the P1 profile-collection tooling, plus taxonomy-anchoring *infrastructure* (not generation).
- **Decision:** `src/alcsm/collection/helper.py` extended with `JobPostingRecord`, its validator, `insert_job_posting`, `verify_posting`, and deterministic (non-NLP) recruiter-identifier detection; `SamplingBatch`/`create_sampling_batch` generalized to a `corpus` field defaulting to `'profile'` (backward compatible, confirmed by regression tests); `src/alcsm/taxonomy/anchoring.py` rewritten from a bare stub into real, tested infrastructure (`TaxonomyVersionRecord`, `TaxonomyTermRecord`, `create_taxonomy_version`, `insert_taxonomy_terms`, `freeze_taxonomy_version`) that mechanically enforces "never edit a frozen version" at the application layer, while `anchor_taxonomy_from_postings` itself remains `NotImplementedError` pending real postings and a decided extraction method. Test-fixture cluster bring-up was generalized from `tests/collection/conftest.py` into the shared `tests/conftest.py`. Full suite: 202/202 passing (up from 95); `black`/`ruff`/`mypy` clean on `src`.
- **Rationale:** Matches this project's standing practice of building infrastructure ahead of the ethics gate using only constructed fixtures, and of keeping one write path per corpus (mirroring D-0009's principle without violating it — a separate module owning a separate table's writes is not a second write path for the same data). The recruiter-name-detection limitation (regex cannot reliably catch bare names in free text without NLP, which is out of scope) was disclosed rather than silently overclaimed.
- **Consequences:** Job-posting collection tooling and taxonomy-anchoring plumbing are ready for a future session to (a) decide and implement the extraction algorithm and (b) execute real collection once ethics approval clears. A pre-existing, unrelated `mypy` failure in `tests/db/test_queries.py` (unmodified since the P0 baseline commit) was found and reported, not fixed, as out of this session's scope.
- **References:** `11_Implementation_Governance/Reviews/P3_Session2_Completion_Summary.md` (full document); `src/alcsm/collection/helper.py`; `src/alcsm/taxonomy/anchoring.py`; `tests/collection/test_job_posting_validation.py`; `tests/collection/test_job_posting_helper.py`; `tests/taxonomy/test_anchoring.py`.
- **Supersedes:** none. Builds on D-0031.

### D-0033 — P3 Session 3 completed: collection operations infrastructure built (manager, checkpoint/resume, duplicates, audit, QA, reporting, export)

- **Date:** 2026-08-02
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (operational-infrastructure-only session; explicitly no real data collection, no scoring, no aggregation)
- **Context:** Third session of Phase P3, building on the job-posting write path from Session 2. Objective was the operational layer around collection: batch lifecycle, checkpoint/resume, deduplication, audit logging, QA, reporting, and export — all infrastructure, no real collection.
- **Decision:** Seven new modules added under `src/alcsm/collection/` (`manager.py`, `checkpoint.py`, `duplicates.py`, `audit.py`, `quality.py`, `reporting.py`, `export.py`), plus `complete_sampling_batch` added to `collection/helper.py` as the lifecycle counterpart to `create_sampling_batch`. Every new "status"/"progress" concept is derived from existing frozen schema columns — no new stored field. Checkpoints and the audit log are file-based, outside the database, carrying only pseudonymous ids and counts. `CollectionManager` delegates to `collection.helper`'s existing validated write path rather than reimplementing it. Full suite: 294/294 passing (up from 202); `black`/`ruff`/`mypy` clean on `src`.
- **Rationale:** Matches this project's standing practice of building auditable, reproducible infrastructure ahead of the ethics gate, and of deriving new operational concepts from the frozen schema rather than extending it. Two real bugs (an audit-masking failure mode in `CollectionManager`'s error path, and a test-fixture violating the Session 2 recruiter-privacy rule) were found and fixed during this session's own verification — both are recorded as an example of the test suite functioning as intended, not silently patched.
- **Consequences:** P3's software readiness is now comprehensive across both corpora's collection, lifecycle, and operational reporting. Remaining P3 work is real ethics approval, real collection, and the still-unimplemented taxonomy-anchoring generation algorithm.
- **References:** `11_Implementation_Governance/Reviews/P3_Session3_Completion_Summary.md` (full document); `src/alcsm/collection/manager.py`; `src/alcsm/collection/checkpoint.py`; `src/alcsm/collection/duplicates.py`; `src/alcsm/collection/audit.py`; `src/alcsm/collection/quality.py`; `src/alcsm/collection/reporting.py`; `src/alcsm/collection/export.py`.
- **Supersedes:** none. Builds on D-0031, D-0032.

### D-0034 — P3 Session 4 completed: end-to-end collection workflow orchestrator built; Phase P3 implementation complete

- **Date:** 2026-08-02
- **Status:** Approved
- **Category:** Process
- **Decided by:** Samiksha Dhere (author), executed by Claude Code (integration-only session; explicitly no new capability, no real data collection)
- **Context:** Fourth and final planned session of Phase P3. Objective was to integrate everything built in Sessions 1-3 (job-posting write path, CollectionManager, checkpoint/resume, duplicates, audit, QA, reporting, export) into one coherent, demonstrable, reproducible end-to-end workflow, and to close out P3's software readiness.
- **Decision:** `src/alcsm/collection/workflow.py` added (`CollectionWorkflow` orchestrator, `run_dry_run()`), delegating entirely to existing Session 1-3 modules — no new validation rule, no new write path, no new database access beyond what already existed. `src/alcsm/collection/devcluster.py` extracted the throwaway-PostgreSQL-cluster logic previously duplicated only inside `tests/conftest.py`, so both the test suite and the new standalone dry-run script (`05_Data_Collection/Scripts/collection_dry_run.py`) share one implementation. The dry-run script was executed manually end to end against a real (throwaway, disposable) PostgreSQL cluster and confirmed to work — not merely written but proven. A researcher-facing operations manual (`Task5_P3_Researcher_Operations_Manual.md`) and this Phase P3 final completion report (`P3_Final_Completion_Report.md`) were produced. Full suite: 308/308 passing (up from 294); `black`/`ruff`/`mypy` clean on `src`.
- **Rationale:** Completes P3's software-readiness objective (Milestone 6 of `Task5_Implementation_Plan.md`, engineering side) without touching the ethics-gated real-data side of that milestone. Reusing the cluster-provisioning logic between tests and the demo script, rather than writing a third copy, follows this project's standing DRY discipline.
- **Consequences:** Phase P3's software implementation is complete: both corpora have a validated write path, an orchestrated operational layer, comprehensive tests, and researcher documentation. What remains for P3's *research* completion — real ethics approval, real ~200-posting collection, real taxonomy anchoring — is unchanged and still gated. `p3-complete` should be tagged only once that real-data work is done (`Implementation_Phase_Roadmap.md` §5), not at this software-readiness milestone; see `P3_Final_Completion_Report.md` for the explicit readiness/gating distinction.
- **References:** `11_Implementation_Governance/Reviews/P3_Final_Completion_Report.md` (full document); `src/alcsm/collection/workflow.py`; `src/alcsm/collection/devcluster.py`; `05_Data_Collection/Scripts/collection_dry_run.py`; `05_Data_Collection/Documentation/Task5_P3_Researcher_Operations_Manual.md`.
- **Supersedes:** none. Builds on D-0031, D-0032, D-0033.

---

## 8. Open items carried forward (not decisions — tracked for visibility)

These are flagged inconsistencies or pending confirmations raised during governance review that have **not** been resolved as of this log's creation. They are listed here for visibility, not logged as decisions, because no decision has actually been made yet:

- **P8/P9 phase-count disagreement** between `PROJECT_CONTEXT.md` (P0–P8, app bundled into P8) and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`/`PROJECT_STRUCTURE.md` (P0–P9, app as its own P9). See `Implementation_Phase_Roadmap.md` §9, finding F-1. **Status: Pending author confirmation.**
- **P4 scope granularity**: the primary roadmap tables gate the whole of P4 (interface build *and* pilot coding) on P2+P3, while `Task5_Implementation_Plan.md` Milestone 5 explicitly allows interface-build-and-dry-run to proceed without that gate. `Implementation_Phase_Roadmap.md` §3 (P4) already carries the more granular reading forward as the working definition. **Status: Pending author confirmation of the source-document footnote fix.**
- **`00_Project_Management/README.md`** still titles itself "01_Project_Management" and references an archive path "`17_Archive/01_Project_Management/`", both stale from before the D-0018 renumbering correction — found during this session's governance review, outside that correction's original scope. **Status: Pending — reported, not fixed (see this session's Governance Review Report).**
- **`04_Ethics/README.md`** still titles itself "# 05_Ethics", the same class of stale pre-D-0018 numbering as the item above — found during the P2 Session 4 naming-convention fix, outside that session's pre-approved scope. **Status: Pending — reported, not fixed (see `P2_Final_Governance_Review.md` §6.1). Recommend a single future sweep of all folder READMEs for this pattern, rather than fixing instances one at a time as they are incidentally discovered.**
- **`05_Data_Collection/README.md`** still titles itself "# 06_Data_Collection" — a third instance of the same stale-numbering pattern as the two items above, found during P3 Session 1's repository audit. **Status: Pending — reported, not fixed; recommend including it in the same future README-numbering sweep.**
- **Root `requirements.txt`** duplicates `pyproject.toml`'s role as the single dependency file (D-0010) and pins `alembic`, contradicting D-0008; present since the P0 baseline commit. **Status: Pending — reported (P3 Session 1), not fixed; predates P3, recommend a future P0/P1-era hygiene pass.**
- **`.env.example`** referenced by `PROJECT_CONTEXT.md` §18 and by `config.py`'s own error message but never created, since before P0. **Status: Pending — reported (P3 Session 1), not fixed; same recommended hygiene pass as above.**
- **Pre-existing `mypy` failure in `tests/db/test_queries.py:24`** (`"object" not callable`), unrelated to any P3 session change — confirmed unmodified since the P0 baseline commit. **Status: Pending — reported (P3 Session 2), not fixed; out of scope for a job-posting-infrastructure session.**

---

*This log is maintained going forward as new decisions are made in each subsequent phase (P2 onward). Add new entries at the end of §7 in the format given in §5; never edit a past entry except to update its Status and add a Superseded-by pointer.*
