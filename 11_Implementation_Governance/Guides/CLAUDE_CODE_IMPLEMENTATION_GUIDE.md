# CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
### ALCSM Thesis — Technical Specification for Implementation Sessions

> **Read this first, every session.** This document is the single source of technical context for implementing the ALCSM thesis software. It assumes no memory of prior chats. Where it says **FROZEN**, that element must not be changed without the thesis author's explicit written approval. Where it says **OPEN** or **TO BUILD**, that is implementation work for this phase.
>
> **Governance companions:** `Document_Version_Policy.md` (canonical files), `CLAUDE_CODE_RULES.md` (hard rules), `README.md` (orientation), `Consistency_Review_Tasks1-4.md` (historical audit trail). All architectural decisions in this guide are **final and author-approved**; there are no open confirmation items.

---

## 1. Project Overview and Research Objectives

**Thesis:** *The AI Leadership Credential Gap: An NLP Audit of 500 LinkedIn Profiles.*
**Author:** Samiksha Dhere, MSc Applied Data Science & Analytics, SRH University Heidelberg (Campus Hamburg).

**What the research does.** It audits the **credential signal** that people holding AI-leadership titles present on LinkedIn — *not* their true competence — and compares that signal against what 200 AI-leadership job postings require. It delivers three artefacts: (1) the **ALCSM** six-dimension scoring model; (2) a **credential-gap analysis** (required vs. held); (3) an **NLP screening tool** (Streamlit) that scores profiles automatically.

**The governing framing, which all code must respect.** ALCSM measures *observable credential signals on LinkedIn*, never "leadership competence" or "true capability." Variable names, UI labels, and outputs must use signal language. This is FROZEN and non-negotiable (see §16).

---

## 2. ALCSM Framework Overview and Frozen Methodological Decisions

**Six dimensions**, each scored **0–5** (integer, ordinal):

| Code | Dimension | Verifiability from text |
|---|---|---|
| D1 | Formal Education | High |
| D2 | Professional Certifications | High |
| D3 | Practical AI Experience | Medium |
| D4 | Technical Contributions | Medium–High |
| D5 | Leadership & Strategic Responsibility | Low |
| D6 | Professional Engagement & Continuous Development | Low–Medium |

**Measurement model (FROZEN):** ALCSM is a **formative composite index**, not a reflective scale. Consequence for code and analysis: **do not compute or report internal-consistency reliability (Cronbach's α) across the six dimensions** — it is inappropriate for a formative index. Inter-rater reliability (Krippendorff's α, per dimension) *is* appropriate and required. Reference: `ALCSM_Measurement_Model_and_Validation_Note.md`.

**Frozen decisions that touch code directly:**
- Scores are **ordinal 0–5**; means are descriptive only, inferential analysis uses ordinal-appropriate methods.
- **Six dimensions, no more, no fewer**; codes are fixed (`d1_education`…`d6_engagement`).
- **Verifiability gradient**; per-dimension reliability reported separately, never pooled.
- **Aggregation function, dimension weights, classification thresholds are OPEN** — no composite/weight/band is hard-coded anywhere. There is no `alcsm_total` column and there must not be one (§4).
- **Missing-data four states:** `present`, `absent_stated`, `unavailable`, `not_applicable` (last is posting-only). `absent_stated` (a stated absence) and `unavailable` (no evidence) are never conflated.
- **External verification permitted for D4 only**, never score-inflating.
- **Coding rulebook + precedent library P-01…P-15** govern human annotation (`ALCSM_Annotation_Handbook.md`).
- **Eight taxonomies** (degree, certification, AI-role, leadership-level, technical-contribution, professional-engagement, AI-keyword-ontology, automation/augmentation) are researcher-constructed and **anchored to the job-posting vocabulary** before term lists are frozen and version-stamped.

Full detail: `ALCSM_Measurement_Specification_v1.0.md` (canonical spec — see `Document_Version_Policy.md`), `ALCSM_Design_Decisions_and_Justification_v1.0.md`.

---

## 3. Research Questions and Implementation Scope

**Primary RQ:** the scale and structure of the AI-leadership credential gap, and whether credential *signal* quality relates to observable professional-impact indicators.

| Sub-RQ | Implementation surface |
|---|---|
| RQ1 credential patterns among AI leaders | Analysis over `alcsm_dimension_score` |
| RQ2 job requirements vs. held credentials | `job_requirement_score` vs. profiles; `v_credential_gap_by_dimension` |
| RQ3 ALCSM construction & validation | Reliability workflow; taxonomy anchoring |
| RQ4 correlation with impact indicators | `rq4_impact_indicator` (isolated); ordinal correlation |
| RQ5 NLP automation of scoring | NLP pipeline vs. human gold standard; `v_nlp_evaluation` |

**In scope for implementation:** collection tooling (manual-entry helper), annotation support, reliability computation, taxonomy anchoring, NLP pipeline, credential-gap analysis, Streamlit app.
**Out of scope / FROZEN-OPEN:** aggregation function, weights, classification bands — these are decided empirically later and must not be pre-committed in code.

---

## 4. Database Architecture, Schema Decisions, and Version History

**Engine:** PostgreSQL 16. **Schema is FROZEN at v1.0.1.** The DDL file `alcsm_schema_v1.0.1.sql` is the **single source of truth** for structure.

**Scale:** 22 base tables, 5 views, 66 CHECK constraints, 33 foreign keys (all `ON DELETE RESTRICT`). *(Note: `Task4_Data_Schema_Design.md` says "eighteen tables"; that is a known undercount — see Consistency Review C-2. The correct figure is 22.)*

**Version history:**
| Version | Change |
|---|---|
| v1.0.0 (`Archive/Superseded_Task1_Task4/alcsm_schema_v1.sql`) | Original frozen schema; archived. Retained only for the v1.0.0→v1.0.1 patch path. |
| **v1.0.1 (`alcsm_schema_v1.0.1.sql`)** | Implementation hardening F-01–F-05: corrected `v_profile_completeness` denominator (F-01); adjudication-role alignment (F-02); tie-break routing (F-03); missing-status/evidence coherence (F-04); ambiguity brackets score (F-05). **No conceptual change.** See `PATCH_NOTES_v1.0.1.md`. |

**Deferred hardening (apply on schedule, not now):** F-06 taxonomy `NOT NULL` (after taxonomy anchoring), F-07 ISO/temporal hygiene (optional), F-08 activity/ethics trigger (after Task 5 ethics). Menu: `alcsm_optional_recommendations.sql`. Enabling these later is *allowed* and does not violate the freeze (Consistency Review A-2).

**Load-bearing schema decisions (do not "optimise" away):**
- **No `alcsm_total`/composite/band/weight column** — aggregation is OPEN.
- **Long-format `profile_raw_section`** with explicit `section_available` — distinguishes empty from not-retrieved; underpins the missing-data logic.
- **`rq4_impact_indicator` physically separate** and never shown to raters — predictor/criterion independence.
- **Additive adjudication** (`is_adjudication` rows; originals never overwritten) — reliability integrity.
- **`v_reliability_input`** returns pre-adjudication independent rows only — query it, never the base table, for reliability.
- **Separate `job_requirement_score`** — required ≠ held (commensurability caveat).

**Known open weaknesses to disclose in the thesis (not to fix without approval):** 3NF `search_query` denormalisation (W-1), `taxonomy_version.anchored_to_batch` without FK (W-2), `rq4_seniority_progression_rate` shares source data with D5 (W-5). See `Task4c_ER_Design_Documentation.md` §14.

ER diagram: `alcsm_er_diagram.mermaid` (22 entities, 33 relationships, catalogue-verified).

---

## 5. Repository and Folder Structure

```
alcsm-thesis/
├── CLAUDE_CODE_IMPLEMENTATION_GUIDE.md   ← this file (repo root)
├── README.md
├── pyproject.toml                        ← deps + tooling (Python 3.11+)
├── .gitignore                            ← MUST exclude data/, .env, secrets
├── .env.example                          ← config template (no real secrets)
│
├── docs/
│   ├── framework/        ← FROZEN: spec, design decisions, validation note
│   ├── rulebook/         ← FROZEN: annotation handbook, precedent library
│   ├── ethics/           ← ethics application, approvals, privacy notice
│   ├── gdpr/             ← LIA, DPIA, DMP
│   └── protocols/        ← sampling, collection, reliability
│
├── schema/
│   ├── alcsm_schema_v1.0.1.sql           ← SINGLE SOURCE OF TRUTH
│   ├── alcsm_patch_v1.0.0_to_v1.0.1.sql
│   └── alcsm_optional_recommendations.sql
│
├── src/alcsm/
│   ├── __init__.py
│   ├── config.py         ← env-driven settings (DB DSN, paths, model choice)
│   ├── db/
│   │   ├── engine.py     ← SQLAlchemy engine/session (app layer only; never DDL)
│   │   ├── models.py     ← ORM models GENERATED FROM the DDL, not owning it
│   │   └── queries.py    ← read queries over the frozen views
│   ├── collection/
│   │   └── helper.py     ← manual-entry insertion (port of collection_helper.py)
│   ├── reliability/
│   │   └── krippendorff.py   ← per-dimension α + bootstrap CI + variance
│   ├── taxonomy/
│   │   └── anchoring.py  ← seed term lists from job-posting vocabulary
│   ├── nlp/
│   │   ├── extract.py    ← section → features
│   │   ├── classify.py   ← per-dimension 0–5 predictors
│   │   └── evaluate.py   ← predictions vs. gold standard (v_nlp_evaluation)
│   ├── analysis/
│   │   ├── gap.py        ← credential-gap (v_credential_gap_by_dimension)
│   │   └── rq4.py        ← criterion correlation (ordinal)
│   └── app/
│       └── streamlit_app.py  ← screening tool (dimension-level primary)
│
├── tests/                ← pytest; mirrors src/alcsm/
├── scripts/
│   └── backup_alcsm.sh   ← verified pg_dump/restore
├── archive/              ← superseded files (v1.0.0 schema, old validation)
│
└── data/                 ← GITIGNORED. Personal data lives in the SECURE STORE,
                            not here. This dir is for local, non-personal fixtures only.
```

**Hard rule:** `data/`, `.env`, and any credentials are never committed. Verify `.gitignore` before the first push.

---

## 6. Python Architecture and Module Responsibilities

| Module | Responsibility | Must not |
|---|---|---|
| `config.py` | Load settings from env; expose typed config | Hard-code secrets or DSNs |
| `db/engine.py` | Provide engine/session; connection lifecycle | Define schema |
| `db/models.py` | ORM reflection/models aligned to the DDL | Create/alter tables (DDL owns structure) |
| `db/queries.py` | Read via frozen views | Bypass `v_reliability_input` for reliability |
| `collection/helper.py` | Validated, atomic manual-entry inserts | Scrape or automate LinkedIn |
| `reliability/krippendorff.py` | Per-dimension α, bootstrap CI, % agreement, variance | Pool dimensions; use adjudicated rows |
| `taxonomy/anchoring.py` | Build term lists from postings; stamp versions | Invent terms not evidenced or edit after freeze |
| `nlp/*` | Extract → classify → evaluate, per dimension | Use info the human coder could not see |
| `analysis/*` | Gap + RQ4, ordinal-appropriate | Compute a hard-coded composite |
| `app/streamlit_app.py` | Show six scores + flags; optional exploratory composites | Display one hard-coded aggregate |

**Separation of concerns:** DDL owns structure; Python owns behaviour. Analysis reads through views. Nothing computes a composite score without an explicit, user-selected, clearly-labelled aggregation method (§9, M-4).

---

## 7. PostgreSQL Implementation Conventions

- **DDL is authoritative.** Never create/alter tables from Python. Schema changes are DDL edits, versioned, and require author approval.
- **snake_case** identifiers; controlled vocabularies stored as `TEXT` + FK to reference tables (self-describing exports).
- **Timestamps** `TIMESTAMPTZ` in UTC, ISO 8601.
- **All FKs `ON DELETE RESTRICT`** — never cascade research data.
- **Query the views** for analysis: `v_reliability_input`, `v_final_profile_score`, `v_profile_completeness`, `v_credential_gap_by_dimension`, `v_nlp_evaluation`. They encode frozen rules so analysis code cannot violate them.
- **Every scored/predicted/collected row carries its versions** (`alcsm_version`, `rulebook_version`, `taxonomy_version_id`, model/run ids). Preserve this on every insert.
- **Deployment/testing:** deploy from `alcsm_schema_v1.0.1.sql` into a throwaway DB and run the validation harness (`alcsm_validation_harness_v1.0.1.py`, 67 tests) as a smoke check before trusting an environment.

---

## 8. SQLAlchemy Design Principles (FINAL)

**Author decision (final):** the PostgreSQL schema is the single source of truth. **SQLAlchemy is an application layer only. It must NOT generate, create, alter, or migrate the schema.**

- Use **Core** or **reflected/`Automap`** models generated *from* the deployed schema. **Never** author declarative models that define tables and call `create_all()`/`metadata.create_all()`, and never wire in Alembic or any migration tool against the research database — schema changes are DDL edits requiring author approval, not ORM migrations.
- If declarative models are used for ergonomics, add a startup check that reflects the live schema and asserts the models match it; on mismatch, fail fast rather than "fixing" the database.
- **Single write path (final):** the existing validated `collection/helper.py` (psycopg2) remains the **authoritative insertion path**. Do not create a second, ORM-based write path. If the helper is later ported onto SQLAlchemy Core, the psycopg2 version is retired in the same change — never run two write paths concurrently.
- Sessions: short-lived, explicit commit/rollback; mirror the atomic-per-profile pattern proven in `collection_helper.py`.

---

## 9. Streamlit Application Architecture (FINAL)

**Purpose (RQ5 artefact):** score a profile's text on the six dimensions and present results honestly.

**The dashboard MUST display (author decision, final):**
1. the **six ALCSM dimension scores** (0–5 each);
2. **missingness status** per dimension (`present` / `absent_stated` / `unavailable`);
3. the **completeness index** (informative dimensions ÷ 6);
4. **evidence summaries** — the span(s) supporting each dimension's score, for transparency;
5. **validation indicators** — flags (ambiguity, contradiction), and NLP confidence where available.

**The dashboard MUST NOT display a single ALCSM composite score.** Aggregation remains **exploratory only** until empirical validation. If any aggregated view is offered, it is a clearly-labelled exploratory panel letting the user compare the three candidate aggregation functions (compensatory / partially compensatory / conjunctive) — never one hard-coded number presented as "the" score.

- **No RQ4 impact values** are used as scoring inputs or shown as if part of ALCSM.
- **Signal language** throughout (credential signal, not competence).
- Structure: input pane → NLP scoring (§10) → per-dimension result cards (score + missingness + evidence + flags) → completeness index → optional labelled exploratory aggregation view.
- No browser storage of personal data; process in-session; same data-protection rules as the pipeline (§10).

---

## 10. NLP Pipeline Architecture and Stages (FINAL)

**Goal (RQ5):** replicate the human gold-standard 0–5 scoring per dimension, evaluated via `v_nlp_evaluation`.

**Comparability rule:** the pipeline must operate on the **same information base** as human coders (`information_base = 'profile_text_only'` unless links are explicitly in scope). Record it on every `nlp_model_run`.

**Data-protection rule (author decision, final):** **No external-API processing of LinkedIn profile text.** Profile text must never be sent to third-party/hosted LLM or NLP APIs. Use **local or explicitly approved models only.** Prioritise, in this order: **spaCy**, **sentence-transformers**, and **HuggingFace models** run locally (or on approved EEA-resident infrastructure). This is a hard constraint tied to the GDPR position; it is not optional and is not overridden by convenience or performance.

**Planned stages:**
1. **Extraction** — parse `profile_raw_section` text into per-dimension features; use the AI keyword ontology to *locate* evidence (never to score).
2. **Per-dimension classifiers** — six ordinal 0–5 predictors. Start simple with the approved local stack: spaCy for parsing/NER, sentence-transformers or local HuggingFace embeddings for representation, then an ordinal classifier; escalate only if justified and only with local/approved models. Each records `predicted_score`, optional confidence, `predicted_missing_status`.
3. **Evaluation** — against the human gold standard via `v_nlp_evaluation`: per-dimension agreement, signed/absolute error, exact-match; ordinal-appropriate metrics. Reproducibility: fix `random_seed`, record `code_commit_hash`.
4. **Job-posting side (separate validation)** — requirement-mining is a *different* task from profile self-presentation; do not assume classifier transfer; validate on its own small pilot.

**Sequencing:** the NLP pipeline depends on (a) a human gold standard existing and (b) taxonomies anchored and version-stamped. Do not train before those exist.

---

## 11. Coding Standards, Naming, Documentation, Testing

- **Style:** PEP 8; `black` formatting; `ruff` linting; type hints on public functions; `mypy` where practical.
- **Naming:** modules/functions `snake_case`; dimension references use the fixed codes `d1_education`…`d6_engagement` everywhere — never ad-hoc labels like `education_score`.
- **Docstrings:** every public function; state inputs, outputs, and any frozen rule it enforces. Cross-reference the governing doc (e.g. "enforces D4-only verification, see spec §2.5").
- **Testing (`pytest`):**
  - Unit tests for validation logic (the collection helper's validators are a model — they already pass 8/8).
  - Schema smoke test: deploy DDL to a throwaway DB, run the 67-test harness.
  - Reliability math tested against hand-worked small cases.
  - NLP evaluation tested on a tiny fixture with known gold scores.
  - **No test may contain real personal data**; use constructed fixtures (the 18 worked example profiles are the model).
  - **Caution learned in Task 4:** do not write test assertions *against the implementation* — write them against the *specification*, or you will validate your own bugs (this actually happened; see `PATCH_NOTES_v1.0.1.md` §4.2).

---

## 12. Version Control and Git Workflow

- **Git for code, schema, docs; never personal data.** `.gitignore` excludes `data/`, `.env`, secrets.
- **Tag frozen states:** `framework-v1.0`, `schema-v1.0.1`. The schema records `code_commit_hash` on NLP runs, so keep `main` clean and commits meaningful.
- **Branching:** lightweight; `main` always runnable; short-lived feature branches per module.
- **Commit messages:** reference the module and, where relevant, the guide section or frozen rule.
- **Superseded files** live in `archive/`, not deleted from history but out of the working path (Consistency Review D-3).

---

## 13. Logging, Configuration, Error Handling

- **Config:** all secrets and the DB DSN from environment (`.env`, never committed); `.env.example` documents keys. Config is typed and loaded in `config.py`.
- **Logging:** standard `logging`; structured where useful; **never log profile text or any personal data** at INFO or above; scrub identifiers from error messages.
- **Error handling:** fail loud and atomic — the collection helper's pattern (validate → transaction → rollback-on-any-error) is the template. A failed operation leaves no partial rows. Surface readable messages, not raw tracebacks, to end users of the Streamlit app.
- **Data-protection in errors:** an exception must never dump a profile's contents into a log or a UI stack trace.

---

## 14. Implementation Roadmap (Milestones and Dependencies)

Aligns with `Task5_Implementation_Plan.md`. Governance (ethics/GDPR) gates any real-data step.

| Phase | Deliverable | Depends on |
|---|---|---|
| P0 Environment | repo, `pyproject.toml`, DDL deployed, harness green | — |
| P1 Collection tooling | `collection/helper.py` ported + tested; backup verified | P0 |
| P2 Governance | ethics/GDPR/DPIA approved | (external) — BLOCKS real data |
| P3 Job postings + taxonomy anchoring | postings collected; term lists stamped; F-06 enabled | P2 |
| P4 Annotation + pilot | interface honours 4 constraints; pilot coded | P2, P3 |
| P5 Reliability | per-dimension α + CIs + variance stored | P4 |
| P6 Main collection + coding | 500 profiles; sustained reliability | P5 gate |
| P7 NLP pipeline | extract/classify/evaluate vs. gold standard | P6 |
| P8 Analysis | gap (RQ2), RQ4 correlation, patterns (RQ1) | P6, P7 |
| P9 Streamlit app | dimension-level scoring tool | P7 |

**Non-negotiable ordering:** no real profile data before P2; no scoring before taxonomies anchored (P3); no NLP training before a gold standard exists (P6).

---

## 15. Validation and Quality Assurance Strategy

- **Schema:** the 67-test harness (`alcsm_validation_harness_v1.0.1.py`) + gap probes; run on any new environment. Verified against live PostgreSQL 16.
- **Collection:** helper validators (8/8 tests) + the Task 5 data-quality checklist.
- **Reliability:** per-dimension α with bootstrap CIs, % agreement, `n_units`, variance — stored in `reliability_result`, computed only via `v_reliability_input`.
- **Double-coding policy (final, canonical wording):** *"100% double coding if feasible; otherwise a pre-registered random subset of at least 15%."* A sampled subset must be random and pre-registered (record method and seed), or reliability will not generalise to the full corpus.
- **NLP:** per-dimension evaluation via `v_nlp_evaluation`; report where the model fails, per dimension, honestly.
- **Analysis:** ordinal-appropriate methods; means descriptive only; `not_applicable`/`unavailable` excluded from `Gap_i`, never read as zero.
- **Backups:** `scripts/backup_alcsm.sh` — verified dump/restore round-trip; runs to the secure store only.

---

## 16. Project Freeze Boundaries — DO NOT CHANGE WITHOUT EXPLICIT AUTHOR APPROVAL

A future Claude Code session **must never** alter any of the following. If a task seems to require it, **stop and ask the author**; treat it as a framework-version decision, not an implementation choice.

**Conceptual / methodological (FROZEN):**
1. The six dimensions, their definitions, theoretical anchors, and **0–5 criteria**.
2. The **formative** measurement-model specification (and therefore: **never** report Cronbach's α across dimensions as a quality metric).
3. The verifiability gradient and per-dimension (never pooled) reliability reporting.
4. The signal-not-competence terminology.
5. The coding rulebook rules, the precedent library **P-01…P-15**, and the missing-data four-state semantics.
6. The eight taxonomies' **structure** (term lists are anchored then frozen with a version stamp).
7. The research questions and sub-questions.
8. External verification permitted for **D4 only**, never score-inflating.
9. The reliability decision thresholds (α ≥ .80 / .667–.80 / < .667) and the rule that a failing dimension triggers **rulebook-wording** revision, **never** criteria revision.

**Database (FROZEN at Schema v1.0.1):**
10. All 22 tables, keys, 33 FKs (`ON DELETE RESTRICT`), 66 CHECK constraints, and the 5 views — structure and semantics.
11. **No `alcsm_total`/composite/weight/band column** may be added (aggregation is OPEN).
12. Long-format `profile_raw_section` with `section_available`; separate `rq4_impact_indicator`; additive adjudication; `v_reliability_input` semantics; separate `job_requirement_score`.
13. The DDL file is the single source of truth; ORM never owns or emits schema.

**Deliberately OPEN (implement, but do not resolve without author):**
- Aggregation function, dimension weights, classification thresholds — never hard-code a choice.
- Deferred hardening F-06/F-07/F-08 — enable on schedule, do not treat their absence as a defect.

**Allowed without special approval:** writing new Python modules, tests, the NLP pipeline, the Streamlit app, analysis code, and docs — provided they honour every boundary above and read through the frozen views.

---

## 17. Expected Deliverables per Phase

| Phase | Concrete deliverables |
|---|---|
| P0 | Running repo; DDL deployed; harness green; `README.md` |
| P1 | Tested collection helper; verified backup; data-quality checklist wired |
| P3 | Anchored taxonomies + stamped `taxonomy_version`; F-06 enabled |
| P4 | Annotation interface (4 constraints); coded pilot |
| P5 | `reliability_result` populated; per-dimension α report |
| P6 | 500 profiles collected + coded; sustained-reliability report |
| P7 | NLP pipeline + `v_nlp_evaluation` results per dimension |
| P8 | Gap analysis (RQ2), RQ4 correlation, RQ1 patterns |
| P9 | Streamlit screening tool (dimension-level primary) |

Each phase: code + tests + a short docs note recording decisions and any author-confirmed assumptions.

---

## 18. Keeping Implementation Aligned with Thesis Chapters

| Thesis chapter | Backed by |
|---|---|
| Ch. 2 Literature | `Literature_Remapping_and_Annotations_v1.md` |
| Ch. 3 Methodology / Measurement | spec, design-decisions, validation note, ER documentation |
| Ch. 3/4 Database Design | `Task4c_ER_Design_Documentation.md` (§13 has drop-in prose) |
| Ch. 4 Reliability & Validation | `reliability/` outputs; pilot results |
| Ch. 4/5 Credential Gap (RQ2) | `analysis/gap.py`, `v_credential_gap_by_dimension` |
| Ch. 5 RQ4 correlation | `analysis/rq4.py` |
| Ch. 5 NLP automation (RQ5) | `nlp/`, `v_nlp_evaluation` |
| Ch. 6 Tool | Streamlit app |
| Limitations | disclosed weaknesses W-1/W-2/W-5; sampling biases; D5/D6 verifiability |

**Practice:** when a module produces a result that will appear in the thesis, write the short docs note in the same commit, in signal language, citing the governing frozen document. This keeps code and thesis synchronised and makes Chapter 3/4 write-up a matter of assembling notes rather than reconstructing decisions.

---

*This guide reflects frozen ALCSM v1.0 and Schema v1.0.1. All architectural decisions are final and author-approved (SQLAlchemy = app layer only; single write path via the collection helper; Streamlit shows six dimensions + missingness + completeness + evidence + validation indicators, never a single composite; NLP is local-only via spaCy / sentence-transformers / HuggingFace; double-coding 100% or pre-registered random ≥15%). No frozen methodological or database element was modified in authoring this guide.*
