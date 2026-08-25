# Job_Postings

## Purpose

Holds the job posting corpus for the ALCSM study, in two distinct layers with different roles and different git-tracking status. **Neither layer is tracked in Git** — both are excluded via `.gitignore`, and no file under this folder has ever been committed (verified by direct `git log` inspection).

## Layers

| Layer | Folder | Role |
|---|---|---|
| Raw | `01_Raw/` | **Archival evidence only.** The original, as-collected workbook (`ALCSM_JobPosting_DataCollection_v1.0.xlsx`), read-only from this point forward. Never modified, annotated, cleaned, or deduplicated in place. |
| Processed | `02_Processed/` | **The authoritative analytical working dataset.** The current version (`ALCSM_JobPosting_Processed_v1.1.xlsx`) is what all downstream work reads from, including the eventual taxonomy-anchoring step. |

**From this point forward, no downstream task should read `01_Raw/` as its analytical source.** Raw is retained permanently as historical evidence — never deleted — but the processed workbook is the single working dataset going forward.

## Current processed dataset

`02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` — 201 job postings (`Job_Master`) and 1,558 job-requirement records (`Requirements`), with `Final_ALCSM_Dimension` reflecting the completed requirement-to-dimension mapping pass (see `Pre_P4_Data_Readiness_Status.md` for the current mapping-completeness figures — a substantial majority of requirements are now mapped, though a "Not Directly Mapped" residual remains and is not remapped automatically by any process in this repository).

## Relationship to taxonomy anchoring

`Requirements.Requirement_Text` (verbatim, 1,558/1,558 populated) is the source corpus the still-unimplemented taxonomy-anchoring extraction algorithm (`src/alcsm/taxonomy/anchoring.py`) will eventually draw from, once built. This README does not authorize or perform that anchoring — see `Pre_P4_Data_Readiness_Status.md` §6 for current status.

## Versioning

Processed workbook versions are dated in-filename (`v1.1`, and so on). A version increment accompanies any substantive change to the processed layer; the raw workbook's own version (`v1.0`) does not change, since raw is never edited.
