# Document Version Policy
### Canonical Files and Archive Register — ALCSM Thesis Project

**Purpose.** Eliminate version ambiguity. For every artefact that once had more than one version, exactly **one canonical file** is authoritative. Superseded files are **retained** (never deleted), under task-appropriate subfolders of the archive root.

**Archive root correction (2026-08-24, this session):** the archive root is `16_Archive/`. The P0-era register below still names `17_Archive/Superseded_Task1_Task4/...` — at some point after that register was written, the archive root was renamed from `17_Archive/` to `16_Archive/` (confirmed: `17_Archive/` no longer exists anywhere in this repository; `16_Archive/Superseded_Task1_Task4/` holds the same four files this register lists). Per this document's own rule (§ "Rule for all future work"), this file is itself a live, forward-looking governance document, not a historical narrative — its path references are corrected below rather than left stale, exactly as the rule already requires for documents of this kind. The P0-era table's *content* (which artefact is canonical) is unchanged; only the archive root folder name is corrected, `17_Archive` → `16_Archive`, everywhere it appears below.

**Rule for all future work (human and Claude Code):** cite and edit only the canonical file. If a historical document references an archived filename, that reference is *correct in its historical context* and is not to be rewritten; only *live, forward-looking* documents (this file, the implementation guide, README, rules) point to canonical paths.

---

## Current (v1.1) canonical register — added 2026-08-24

This is the register that matters for all work from this point forward. See §"P0-era register" below for the original schema/framework-artefact history, preserved for continuity.

| Category | CANONICAL (use this) | Notes |
|---|---|---|
| **Framework — scoring** | `02_Framework_Development/ALCSM_v1.1_Scoring_Framework.md` | Restates D1–D5 unchanged from v1.0; D6 replaced. `ALCSM_v1.0_Scoring_Framework_Task3.md` remains the frozen historical predecessor, not archived (still the authoritative record of the original, now-superseded-for-D6-only v1.0 scoring table). |
| **Framework — D6 construct** | `02_Framework_Development/ALCSM_D6_Industry_Breadth_v1.1.md` | Status: PROPOSED/PILOT_REQUIRED (`DECISION_LOG.md` D-0038) — canonical as the *current proposed* D6 definition, not yet a frozen final one. |
| **Framework — D6 coding rules** | `02_Framework_Development/ALCSM_Coding_Rulebook_v1.1_Addendum.md` | Supplements, does not replace, `ALCSM_Coding_Rulebook_and_Pilot_Design.md` (still canonical for D1–D5). |
| **Data — LinkedIn processed** | `05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` | Git-ignored (real data). The authoritative analytical source for profile demographics/experience; `01_Raw/` is permanent archival evidence, never an analytical source. |
| **Data — job postings processed** | `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` | Git-ignored (real data). `Requirements.Final_ALCSM_Dimension` reflects the completed requirement-remapping pass (799/1,558 currently `NOT_DIRECTLY_MAPPED`) — see `16_Archive/Superseded_JobRequirement_Mapping/` for the remapping methodology trail, already fully merged into this file. |
| **Annotation — final scores** | `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` | Git-ignored (real data). **Frozen** as of `Final_Annotation_v1.1_Freeze_Report.md` (2026-08-24, SHA-256 `0e2a2842f0d4744681432c8be77b36cc09948e7b65e79fe4ae14d7965e6a412f`) — the canonical analytical scoring baseline for all downstream reliability/RQ1–RQ5/NLP work. Never modify. `ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` (same folder) remains canonical as the permanent, separate, immutable first-pass baseline — not archived, not superseded, a different artefact serving a different permanent purpose (the audit trail the final scores were reviewed against). |
| **Survey — raw responses** | `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` | Git-ignored (real data). **24 consented respondents as of 2026-08-25** (updated this session from a 23-respondent snapshot, itself an update from a 12-respondent snapshot — see `16_Archive/Superseded_Survey_Responses/`). Same survey instrument (`v1.0`), more responses collected; not a new instrument version. |
| **Survey — processed/analysis-ready** | `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` | Git-ignored (real data, aggregate). Reproducibly derived from the raw file above via `15_Scripts/alcsm_survey_analysis_v1.0.py` — never a second raw source, never hand-edited. **This is the canonical file for N=24 survey statistics cited in thesis writing** (relevance/clarity means, appropriateness, most-important-dimension counts, participant background). `Survey_Analysis_Final_v1.1.xlsx`, referenced in some task briefs, does not exist anywhere in this repository and has never been created — any reference to it should be read as referring to this file. |
| **Database — schema** | `03_Database_Design/02_Schema/alcsm_schema_v1.0.1.sql` | Frozen. No DDL change has been made — see `PostgreSQL_ProfileID_Compatibility_Audit.md` for the open Profile_ID-format question, investigated but not yet resolved. |

**Never create a second file claiming to be canonical for any row above.** If a newer version of any of these is produced, it replaces the file at the same canonical path (or, if the filename must change, this table is updated in the same edit) — the prior version is archived under a task-appropriate `16_Archive/` subfolder, exactly as this policy has always required.

### Archive subfolders created/used this session (2026-08-24)

| Subfolder | Contents |
|---|---|
| `16_Archive/Superseded_Annotation_Drafts/` | The incomplete `_REVIEW` draft of the final annotation workbook; a precursor per-dimension review draft; one redundant partial first-pass export. |
| `16_Archive/Superseded_Supplementary_Review_Drafts/` | Two precursor drafts of the Supplementary Evidence Collection workbook. |
| `16_Archive/Superseded_JobRequirement_Mapping/` | The requirement-remapping methodology trail (rationale/confidence/precedent per requirement) — already fully merged into the canonical job-postings workbook. |
| `16_Archive/Superseded_Survey_Responses/` | The 12- and 23-respondent survey snapshots, superseded by the current 24-respondent export. |
| `16_Archive/Superseded_D6_Professional_Engagement/` | `D6_Observation_Rule_Decision_Proposal.md` — the retired D6 (Professional Engagement) construct's observation-rule proposal, fully superseded by D6 v1.1. |

Full provenance for every file in these folders: `Repository_Cleanup_Report.md`.

---

## P0-era register (original schema/framework artefacts — preserved for continuity)

| Artefact | CANONICAL (use this) | Archived (retained, do not use) |
|---|---|---|
| Literature review | `Literature_Remapping_and_Annotations_v1.md` | `16_Archive/Superseded_Task1_Task4/Task1_Literature_Annotations_v1.md` |
| Measurement specification | `ALCSM_Measurement_Specification_v1.0.md` (in `02_Framework_Development/`) — see note 5 | *(none — the `_Final` variant this register once cited does not exist; nothing to archive)* |
| Database schema | `alcsm_schema_v1.0.1.sql` | `16_Archive/Superseded_Task1_Task4/alcsm_schema_v1.sql` (v1.0.0) |
| Validation harness | `alcsm_validation_harness_v1.0.1.py` | `16_Archive/Superseded_Task1_Task4/alcsm_validation_harness.py` |
| Gap probes | `alcsm_gap_probes_v1.0.1.py` | `16_Archive/Superseded_Task1_Task4/alcsm_gap_probes.py` |
| Validation tests (SQL) | *(superseded by the v1.0.1 harness)* | `16_Archive/Superseded_Task1_Task4/alcsm_validation_tests.sql` |
| Integrity patch (pre-consolidation) | *(superseded by `alcsm_optional_recommendations.sql`)* | `16_Archive/Superseded_Task1_Task4/alcsm_integrity_patch_OPTIONAL.sql` ⚠️ **not found anywhere in this repository — see note 6** |

---

## Important retention notes

1. **The archived v1.0.0 schema is still functional and intentionally kept.** `alcsm_patch_v1.0.0_to_v1.0.1.sql` upgrades a v1.0.0 database to v1.0.1; that upgrade path needs the v1.0.0 schema. For a **fresh install, always use the canonical `alcsm_schema_v1.0.1.sql`** — it already includes F-01–F-05. The patch path exists only for a pre-existing v1.0.0 deployment.

2. **Historical documents legitimately reference archived filenames.** `ALCSM_Design_Decisions_and_Justification_v1.0.md`, `Task4_Data_Schema_Design.md`, `Task4b_Database_Validation_Plan.md`, and `Consistency_Review_Tasks1-4.md` mention archived files because those were the current files when written. These references are historically accurate and are **not** rewritten. Only forward-looking governance files (`CLAUDE_CODE_IMPLEMENTATION_GUIDE.md`, `README.md`, `CLAUDE_CODE_RULES.md`) are kept pointed at canonical paths.

3. **Filename note for the ER documentation.** The governance instruction referenced `Task4C_ER_Design_Documentation_v1.0.1.md`; the actual canonical file is **`Task4c_ER_Design_Documentation.md`** (lower-case `c`, already updated to v1.0.1 content internally). Treat that file as the canonical ER documentation. No rename is performed to avoid breaking existing references; if a rename is desired later it must be done atomically across all citing documents.

4. **Nothing is deleted.** Archiving is a move, not a delete. The archive is under version control and recoverable.

5. **Resolved — measurement specification canonical designation corrected (2026-07-28, author-confirmed).** `Consistency_Review_Tasks1-4.md` (§D-1) recorded that **two different files** once existed: `ALCSM_Measurement_Specification_v1.0.md` (37,995 bytes) and `ALCSM_Measurement_Specification_v1.0_Final.md` (41,265 bytes, believed at the time to supersede the former, pending author confirmation). This register previously recorded that confirmation as if already made — canonical `_Final`, archived non-`_Final` — but a repository-wide search found **no `_Final` file anywhere** (not live, not archived, not under any other name). The author confirmed the `_Final` version is lost and not recoverable from this repository. **Decision: the surviving `ALCSM_Measurement_Specification_v1.0.md` (37,995 bytes, live in `02_Framework_Development/`) is now the canonical measurement specification**, effective this date. All citations in `README.md`, `PROJECT_CONTEXT.md`, and `CLAUDE_CODE_IMPLEMENTATION_GUIDE.md` that referenced the `_Final` filename have been corrected to cite this file. No content was rewritten — only the canonical designation and citations changed.

6. **Open finding — integrity patch file not found.** `alcsm_integrity_patch_OPTIONAL.sql` is recorded here as archived but was not found anywhere in this repository during the P0 archive-integrity check. Its designated replacement, `alcsm_optional_recommendations.sql`, is present and canonical, so this does not block anything — flagged for completeness only.

---

## When a new version is created in future

- Increment the version in the filename (e.g. `_v1.0.2`).
- Move the prior canonical file to `16_Archive/Superseded_Task1_Task4/` (or a task-appropriate archive folder).
- Update this policy's register and the three forward-looking governance files.
- Never leave two files both claiming to be canonical.
