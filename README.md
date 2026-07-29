# AI Leadership Credential Gap Analysis (ALCSM)

An MSc thesis project auditing the **credential signal** that people holding AI-leadership titles present on LinkedIn, and comparing that signal against what AI-leadership job postings require.

**Author:** Samiksha Dhere — MSc Applied Data Science & Analytics, SRH University Heidelberg (Campus Hamburg).

---

## Project purpose

People increasingly hold AI-leadership titles ("Chief AI Officer", "Head of AI", "VP of AI"). This project asks whether the **credentials they publicly present** match what such roles are advertised to require — and whether that presented signal can be scored consistently by humans and automatically by an NLP tool.

**Framing that governs everything here:** ALCSM measures the **observable credential *signal* on LinkedIn**, not a person's true competence or capability. All code, variable names, and UI text use signal language. This is a frozen, non-negotiable decision.

## Thesis objective

Deliver three research artefacts:

1. **ALCSM** — a six-dimension, 0–5 credential-signal scoring model (formative composite index).
2. **Credential-gap analysis** — required (200 job postings) vs. held (500 profiles), reported per dimension.
3. **NLP screening tool** — a local Streamlit application that scores a profile's six dimensions automatically.

**Research questions:** RQ1 credential patterns; RQ2 job requirements vs. held credentials; RQ3 ALCSM construction & validation; RQ4 correlation with observable professional-impact indicators; RQ5 NLP automation of scoring.

## Current status

| Task | Status |
|---|---|
| 1 — Literature review | ✅ Frozen |
| 2 — ALCSM dimension design | ✅ Frozen |
| 3 — Scoring framework v1.0 | ✅ Frozen |
| 4 — Database schema | ✅ Frozen at **v1.0.1** (22 tables, 5 views, validated on live PostgreSQL 16) |
| Governance / pre-implementation freeze | ✅ Complete (this handover) |
| **5 — Software implementation** | ⏳ **Ready to begin — not yet started** |

**Blocking gate before real data:** ethics / GDPR / DPIA approval (see `docs/ethics/`, `docs/gdpr/`). No LinkedIn profile is collected until that is granted.

## Repository structure

```
CLAUDE_CODE_IMPLEMENTATION_GUIDE.md   Technical spec — read every session
CLAUDE_CODE_RULES.md                  Hard rules for implementation
README.md                             This file
Document_Version_Policy.md            Canonical vs archived files
Task5_Implementation_Readiness_Checklist.md

docs/        framework (FROZEN), rulebook (FROZEN), ethics, gdpr, protocols
schema/      alcsm_schema_v1.0.1.sql  ← single source of truth
src/alcsm/   config, db, collection, reliability, taxonomy, nlp, analysis, app
tests/       pytest, mirrors src/
scripts/     backup_alcsm.sh
Archive/     superseded files (retained, never used)
data/        GITIGNORED — personal data lives in the SECURE STORE, not here
```

## How Claude Code should use the documentation

Read in this order at the start of any implementation session:

1. **`CLAUDE_CODE_RULES.md`** — the eight hard rules. Non-negotiable.
2. **`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`** — full technical context; §16 lists frozen boundaries.
3. **`Document_Version_Policy.md`** — always cite/edit the canonical file, never an archived one.
4. **`Task5_Implementation_Readiness_Checklist.md`** — what is ready and what is pending.

Then, for the specific task at hand, the governing frozen document:

- Methodology / measurement → `docs/framework/ALCSM_Measurement_Specification_v1.0.md`, `ALCSM_Measurement_Model_and_Validation_Note.md`
- Annotation → `docs/rulebook/ALCSM_Annotation_Handbook.md`
- Database → `schema/alcsm_schema_v1.0.1.sql` (authority) + `Task4c_ER_Design_Documentation.md`
- Collection → `Task5_LinkedIn_Collection_Workflow.md`, `collection_helper.py`

**Golden rule:** the schema DDL and the frozen framework are authoritative. If a task seems to require changing either, **stop and ask the author** — treat it as a version decision, not an implementation choice.

## Key constraints at a glance

- PostgreSQL schema is the single source of truth; **SQLAlchemy is an application layer only** and never generates or migrates the schema.
- **No single ALCSM composite score** is displayed; aggregation is exploratory until empirically validated.
- **No external-API processing of profile text**; local models only (spaCy, sentence-transformers, HuggingFace).
- **No personal data in Git**; it lives only in the approved, access-controlled secure store.

## Licensing / sharing

The framework, schema, taxonomies, and code are shareable research outputs. **Raw profile-level personal data is never shared or committed.** See `docs/gdpr/` (DMP).
