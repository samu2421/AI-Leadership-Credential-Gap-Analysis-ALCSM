# Consistency Review — Tasks 1–4 Documentation
### Pre-flight audit before authoring the Claude Code Implementation Guide

**Reviewer stance:** Lead Software/Research Architect. This report is delivered **separately** from the implementation guide, as instructed. I have **not** silently edited any document to fix these; each item below is reported for your decision. The implementation guide is written to be consistent with the *frozen v1.0.1 reality*, and where a legacy document disagrees, the guide follows the frozen reality and this report tells you which legacy text to reconcile.

Findings are grouped: **C = genuine contradiction** (must resolve), **D = duplication** (housekeeping), **M = missing implementation assumption** (decide before Task 5 code), **A = ambiguity** (clarify).

---

## C — Genuine contradictions (resolve before implementation relies on them)

### C-1 — "Revise the *criteria*" vs. "revise the *wording*, never the criteria" **(most important)**
- **`ALCSM_Coding_Rulebook_and_Pilot_Design.md` (line 134):** if a dimension scores α < .667, *"revise the scoring criteria and re-pilot."*
- **Every post-freeze document** (`Task5_PreCollection_Roadmap.md` L293, `ALCSM_Annotation_Handbook.md` L272, and the measurement spec): revise the **rulebook wording**, *"never the frozen criteria."*
- **Why it matters:** the coding rulebook was written **before** the framework was frozen ("Pre-v1.0 Validation Stage"), when criteria were still draft. After the Task-3/spec freeze, the 0–5 criteria are immutable and only *wording/annotation guidance* may change. The rulebook's original instruction now directly contradicts the freeze and, if followed literally, would authorise altering a frozen element.
- **Recommended resolution:** amend that single cell in the coding rulebook to read *"revise the rulebook wording (never the frozen criteria) and re-pilot,"* matching the post-freeze documents. This is a documentation reconciliation, not a methodological change. **Your approval requested — I did not make this edit.**

### C-2 — Table count: "eighteen" vs. "22"
- **`Task4_Data_Schema_Design.md` (line 19):** *"comprises eighteen tables and five analysis views."*
- **`Task4c_ER_Design_Documentation.md` (line 8)** and **`PATCH_NOTES_v1.0.1.md` (line 19):** **22 base tables** and 5 views (verified against the deployed catalogue).
- **Status:** already *diagnosed* in Task4c ("The earlier figure was an undercount, corrected here"), but the erroneous figure still stands uncorrected in `Task4_Data_Schema_Design.md`. A future reader opening that file first will get the wrong number.
- **Recommended resolution:** correct the count in `Task4_Data_Schema_Design.md` to 22, or add a one-line pointer to the Task4c correction. **Reported, not silently changed.**

---

## D — Duplication (housekeeping; pick a canonical file)

### D-1 — Two "measurement specification" files
- `ALCSM_Measurement_Specification_v1.0.md` (37,995 bytes) **and** `ALCSM_Measurement_Specification_v1.0_Final.md` (41,265 bytes) both exist. Two files claiming to be the definitive v1.0 spec is exactly the version ambiguity the project has otherwise avoided.
- **Recommended:** designate one canonical (the larger `_Final` appears to supersede, but **you** should confirm), and archive or delete the other. Until you do, the implementation guide cites `ALCSM_Measurement_Specification_v1.0.md` as canonical because that is the filename referenced by later documents; adjust if you decide otherwise.

### D-2 — Two literature files
- `Task1_Literature_Annotations_v1.md` (27,023 bytes) **and** `Literature_Remapping_and_Annotations_v1.md` (26,920 bytes). Near-identical size; likely one is a rename of the other.
- **Recommended:** keep `Literature_Remapping_and_Annotations_v1.md` (its title reflects the honest remapping that is the actual content) and archive the other.

### D-3 — Superseded schema and validation artefacts coexist with current ones
- `alcsm_schema_v1.sql` (v1.0.0) sits beside `alcsm_schema_v1.0.1.sql`; `alcsm_gap_probes.py` beside `alcsm_gap_probes_v1.0.1.py`; `alcsm_integrity_patch_OPTIONAL.sql` (the pre-consolidation proposal) beside `alcsm_optional_recommendations.sql`.
- **Recommended:** move superseded files into an `archive/` or `deprecated/` folder so no future session runs the wrong one. The implementation guide's repository layout does this explicitly.

---

## M — Missing implementation assumptions (decide before writing Task 5 code)

### M-1 — SQLAlchemy is requested but no ORM model layer exists yet
- Your implementation-guide request names **SQLAlchemy**, but every database artefact to date is **raw SQL DDL + psycopg2** (the collection helper, the validation harness). There is no ORM model, and none of the frozen decisions requires one.
- **Assumption the guide makes (flag for confirmation):** SQLAlchemy Core (not necessarily the full ORM) is introduced as a *thin* layer whose models are **generated from / validated against** the frozen DDL, and the DDL remains the source of truth — the ORM never redefines the schema. If you intended the ORM to *own* the schema, that conflicts with the freeze and we must discuss. **Confirm the direction.**

### M-2 — Two collection paths exist; the guide must state which is authoritative
- `collection_helper.py` (psycopg2, tested) already inserts profiles. A future SQLAlchemy layer (M-1) could offer a second insertion path. Two write paths into a frozen schema is a data-integrity risk.
- **Assumption:** `collection_helper.py` remains authoritative for manual collection; any ORM layer is read/analysis-oriented, or the helper is *ported* onto the ORM but not duplicated. **Confirm.**

### M-3 — Python version, dependency manager, and environment unspecified
- No document fixes a Python version, dependency manager (pip/poetry/uv), or virtual-env convention. The user preferences note macOS/M3, zsh, Docker, AWS — but nothing is pinned for this repo.
- **Assumption in the guide:** Python 3.11+, a `requirements.txt` or `pyproject.toml` (guide recommends `pyproject.toml` + `uv`/`pip`), a project virtualenv, and Docker for PostgreSQL. **Confirm or override.**

### M-4 — Weighting/aggregation are OPEN, but the Streamlit tool must display *something*
- The RQ mentions a Streamlit scoring app, and aggregation function + weights are **frozen-OPEN** (deliberately unresolved). The app therefore cannot display a single composite score without silently choosing an aggregation method.
- **Assumption:** the Streamlit tool shows the **six dimension scores and flags** as the primary output, and presents composites only as an explicitly-labelled, user-selectable *exploratory* view across the three candidate aggregation functions — never one hard-coded number. This matches the frozen "dimension-level is primary" rule. **Confirm.**

### M-5 — NLP model choice is unspecified and interacts with GDPR transfer rules
- RQ5 needs an NLP pipeline, but no model/library is fixed. The Task 5 roadmap flags that any tooling outside the EEA engages GDPR Chapter V transfer rules.
- **Assumption:** the guide recommends EEA-resident or local models and **prohibits sending profile text to third-party APIs outside approved infrastructure** unless the DPO clears it. **Confirm this constraint is acceptable** — it may rule out some hosted LLM APIs for the profile-scoring step.

---

## A — Ambiguities (clarify to prevent divergent implementations)

### A-1 — Double-coding proportion stated three ways
- `Task4_Data_Schema_Design.md` F-10: *"~10–15%."*
- `Task5_PreCollection_Roadmap.md`: *"100% … or a randomly selected ≥15%."*
- `ALCSM_Annotation_Handbook.md`: *"a pre-registered random subset (or 100%)."*
- These are compatible in spirit (a pre-registered random subset, larger is better) but a coder could read "10–15%" and "≥15%" as different floors.
- **Recommended:** state one figure (e.g. *"100% if feasible, otherwise a pre-registered random ≥15%"*) and use it everywhere. The guide adopts that phrasing.

### A-2 — "Task 4 frozen" vs. the still-open F-06/F-07/F-08 items
- Task 4 is declared frozen, yet `alcsm_optional_recommendations.sql` leaves F-06 (taxonomy NOT NULL), F-07 (ISO/temporal hygiene), and F-08 (activity/ethics trigger) as *pending* actions to be applied at later stages.
- **Not a contradiction, but an ambiguity:** "frozen" here means *no conceptual/structural change*, while these are *deferred implementation hardening* to be enabled on schedule (F-06 after taxonomy anchoring, F-08 after ethics). The guide states this explicitly so a future session does not think the schema is "done" in a way that forbids enabling F-06 later.

### A-3 — Where RQ4 criterion extraction happens (collection vs. later pass)
- `Task5_PreCollection_Roadmap.md` says criterion extraction *may lag annotation*; `Task5_LinkedIn_Collection_Workflow.md` captures criterion values *at collection* (time-sensitive). Both are defensible; the schema allows either (nullable `rq4_impact_indicator`, optional at insert).
- **Recommended:** decide a default order. The guide's assumption: capture time-sensitive criterion values (reach, engagement) **at collection**; compute derived ones (progression rate) **later** from stored data. **Confirm.**

---

## Summary and gate

| Class | Count | Blocks implementation? |
|---|---|---|
| Contradictions (C) | 2 | C-1 should be resolved before any reliability-driven revision; C-2 is cosmetic-but-misleading |
| Duplications (D) | 3 | No — housekeeping, but do before the repo is populated |
| Missing assumptions (M) | 5 | **Yes for M-1, M-4, M-5** — they shape architecture and must be confirmed |
| Ambiguities (A) | 3 | No — but clarify to keep implementations from diverging |

**Nothing here requires changing a frozen conceptual or database element.** C-1 and C-2 are documentation reconciliations; the M-items are architecture confirmations for *new* code, not changes to frozen artefacts. My recommendation: approve the C-1/C-2 reconciliations and confirm M-1, M-4, M-5 before Task 5 coding begins. The implementation guide below is written to be correct under the *recommended* resolutions and flags each place where it depends on your confirmation.
