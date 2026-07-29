# 04_Database_Design / 01_Documentation

## Purpose
Narrative and reference documentation explaining the ALCSM database's design, structure, and intended use.

## What Belongs Here
- Data dictionary (tables, columns, types, constraints, relationships)
- Design rationale / architecture decision records
- Setup and usage instructions for standing up the database
- Frozen-release notes for Database Schema v1.0.1

## Naming Conventions
- `ALCSM_DB_Doc_<Description>_v<Major>.<Minor>.<Patch>.<ext>`
  - e.g., `ALCSM_DB_Doc_DataDictionary_v1.0.1.md`

## Versioning Rules
- Documentation version numbers track the schema version they describe — update documentation whenever `02_Schema` changes, using the matching version number.
- Never edit the v1.0.1 documentation set in place; superseded documentation moves to `17_Archive/04_Database_Design/01_Documentation/`.
