# 04_Database_Design / 02_Schema

## Purpose
The authoritative implementation of the ALCSM database schema.

## What Belongs Here
- DDL scripts (table/view/index definitions)
- Migration scripts
- Schema export snapshots (e.g., `.sql`, `.dbml`)

## Naming Conventions
- Baseline/frozen schema: `ALCSM_DB_Schema_v1.0.1_FROZEN.sql`
- Migrations: `ALCSM_DB_Migration_v<Major>.<Minor>.<Patch>_<description>.sql`
  - e.g., `ALCSM_DB_Migration_v1.0.2_add_competency_index.sql`

## Versioning Rules
- **v1.0.1 is frozen** — do not edit these files in place under any circumstances.
- Every schema change is a new, additive migration file that references the version it moves the schema to; the migration history plus the frozen baseline together form the complete schema record.
- Never delete a past migration file, even if later superseded.
