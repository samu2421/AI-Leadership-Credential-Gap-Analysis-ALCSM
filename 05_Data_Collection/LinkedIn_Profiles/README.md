# LinkedIn_Profiles

## Purpose

Holds the LinkedIn profile corpus for the ALCSM study, in two distinct layers with different roles and different git-tracking status. **Neither layer is tracked in Git** — both are excluded via `.gitignore`, and no file under this folder has ever been committed (verified by direct `git log` inspection).

## Layers

| Layer | Folder | Role | Contains direct identifiers? |
|---|---|---|---|
| Raw | `01_Raw/` | **Archival evidence only.** The original, as-collected workbook (`ALCSM_LinkedIn_DataCollection_v1.0.xlsx`), read-only from this point forward. Never modified, annotated, cleaned, or deduplicated in place. | **Yes** — retains `LinkedIn_URL` and other collection-time fields. This is exactly why it is archival-only and excluded from Git. |
| Processed | `02_Processed/` | **The authoritative analytical working dataset.** The current version (`ALCSM_LinkedIn_Processed_v1.1.xlsx`) is what all downstream work — the supplementary evidence queue, and eventually P4 annotation — reads from. | No — `LinkedIn_URL`, `Collection_Date`, `Collector`, and free-text `Notes` have been removed at this layer; only the pseudonymous `Profile_ID` and analytical fields remain. |

**From this point forward, no downstream task should read `01_Raw/` as its analytical source.** Raw is retained permanently as historical evidence of what was actually collected — never deleted, never treated as interchangeable with the processed layer — but the processed workbook is the single working dataset for every subsequent step (supplementary evidence review, P4 annotation, and beyond).

## Current processed dataset

`02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` — 500 profiles (the included analytical population; excluded and cross-population-duplicate records identified in `P3_Final_Data_QA_Report.md` have been resolved at this layer), with `Education`, `Certification`, `Professional_Experience`, and `Technical_Contribution` child sheets keyed on `Profile_ID`.

## Known limitations carried forward from the raw-data audit

The processed layer inherits the structural evidence gaps documented in `P3_Final_Data_QA_Report.md` and addressed operationally in `D6_Observation_Rule_Decision_Proposal.md`: no verbatim profile text (headline/About/experience descriptions) exists at either layer, and D6 engagement evidence does not yet exist at all. See `11_Implementation_Governance/Reviews/Pre_P4_Data_Readiness_Status.md` for the current, consolidated status.

## Versioning

Processed workbook versions are dated in-filename (`v1.1`, and so on). A version increment accompanies any substantive change to the processed layer; the raw workbook's own version (`v1.0`) does not change, since raw is never edited.
