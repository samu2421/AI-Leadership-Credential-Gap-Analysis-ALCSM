"""Database access layer.

SQLAlchemy here is an application layer only: engine/session lifecycle
and reads through the frozen views. It never defines, creates, or
migrates schema — the DDL (schema/alcsm_schema_v1.0.1.sql) is the
single source of truth (PROJECT_CONTEXT.md §23, CLAUDE_CODE_RULES.md
rule 3).
"""
