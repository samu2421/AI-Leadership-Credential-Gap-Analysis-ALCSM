# 04_Database_Design / 03_Validation

## Purpose
Evidence that the database schema behaves correctly: constraint checks, test results, and validation reports.

## What Belongs Here
- QA/test scripts and their output logs
- Constraint and referential-integrity check results
- Sample-data validation reports
- Sign-off records tied to the frozen v1.0.1 release

## Naming Conventions
- `ALCSM_DB_Validation_<Description>_v<Major>.<Minor>.<Patch>.<ext>`
  - e.g., `ALCSM_DB_Validation_ConstraintCheck_v1.0.1.md`

## Versioning Rules
- Validation reports are tied to the schema version they tested — a new schema migration requires a new validation report at the matching version number.
- Never overwrite a completed validation report; it is a permanent audit record. Superseded/obsolete reports move to `17_Archive/04_Database_Design/03_Validation/`.
