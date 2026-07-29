# 04_Database_Design

## Purpose
Home of the ALCSM database implementation: schema, documentation, validation evidence, and entity-relationship diagrams. **The schema is frozen at v1.0.1 as of Task 4.**

## What Belongs Here
This folder is organized into four subfolders:
- `01_Documentation/` — data dictionary, design rationale, setup/usage docs
- `02_Schema/` — DDL scripts, migrations, schema exports
- `03_Validation/` — QA/test results, constraint checks, sample-data validation reports
- `04_ER_Diagram/` — entity-relationship diagrams (source files and exported images)

See each subfolder's own README.md for specifics.

## Naming Conventions
- `ALCSM_DB_<Subarea>_<Description>_v<Major>.<Minor>.<Patch>.<ext>`
- Three-part version numbers match the schema's semantic versioning scheme (e.g., `v1.0.1`).

## Versioning Rules
- **v1.0.1 is frozen.** Do not edit frozen DDL/schema files in place.
- Any schema change is delivered as a new migration file, never as an edit to a frozen file — e.g., `ALCSM_DB_Migration_v1.0.2_<description>.sql`.
- The frozen v1.0.1 baseline is retained permanently in `02_Schema/` as the historical record.
- Superseded documentation/diagrams move to `17_Archive/04_Database_Design/`.
