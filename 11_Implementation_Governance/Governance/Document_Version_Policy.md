# Document Version Policy
### Canonical Files and Archive Register — ALCSM Thesis Project

**Purpose.** Eliminate version ambiguity. For every artefact that once had more than one version, exactly **one canonical file** is authoritative. Superseded files are **retained** (never deleted) under `17_Archive/Superseded_Task1_Task4/`.

**Path correction (P0 cleanup, this session):** this register previously read `Archive/Superseded_Task1_Task4/`, a path that never existed in this repository. The actual archive root is `17_Archive/` (see `PROJECT_STRUCTURE.md`). The four superseded database-design files below were moved from `03_Database_Design/` into `17_Archive/Superseded_Task1_Task4/` in this session; all paths in this register are corrected to match.

**Rule for all future work (human and Claude Code):** cite and edit only the canonical file. If a historical document references an archived filename, that reference is *correct in its historical context* and is not to be rewritten; only *live, forward-looking* documents (the implementation guide, README, rules) point to canonical paths.

---

## Canonical register

| Artefact | CANONICAL (use this) | Archived (retained, do not use) |
|---|---|---|
| Literature review | `Literature_Remapping_and_Annotations_v1.md` | `17_Archive/Superseded_Task1_Task4/Task1_Literature_Annotations_v1.md` |
| Measurement specification | `ALCSM_Measurement_Specification_v1.0.md` (in `02_Framework_Development/`) — see note 5 | *(none — the `_Final` variant this register once cited does not exist; nothing to archive)* |
| Database schema | `alcsm_schema_v1.0.1.sql` | `17_Archive/Superseded_Task1_Task4/alcsm_schema_v1.sql` (v1.0.0) — moved this session |
| Validation harness | `alcsm_validation_harness_v1.0.1.py` | `17_Archive/Superseded_Task1_Task4/alcsm_validation_harness.py` — moved this session |
| Gap probes | `alcsm_gap_probes_v1.0.1.py` | `17_Archive/Superseded_Task1_Task4/alcsm_gap_probes.py` — moved this session |
| Validation tests (SQL) | *(superseded by the v1.0.1 harness)* | `17_Archive/Superseded_Task1_Task4/alcsm_validation_tests.sql` — moved this session |
| Integrity patch (pre-consolidation) | *(superseded by `alcsm_optional_recommendations.sql`)* | `17_Archive/Superseded_Task1_Task4/alcsm_integrity_patch_OPTIONAL.sql` ⚠️ **not found anywhere in this repository — see note 6** |

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
- Move the prior canonical file to `17_Archive/Superseded_Task1_Task4/` (or a task-appropriate archive folder).
- Update this policy's register and the three forward-looking governance files.
- Never leave two files both claiming to be canonical.
