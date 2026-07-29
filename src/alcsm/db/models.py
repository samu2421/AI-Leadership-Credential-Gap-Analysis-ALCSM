"""Models reflected from the deployed schema.

TODO (Phase P0, after schema deploy): once
`schema/alcsm_schema_v1.0.1.sql` has been deployed to a running
PostgreSQL instance, wire this module to reflect the live schema and
assert it matches expectations, per PROJECT_CONTEXT.md §23:

    "If reflected models and the live schema ever disagree, fail
    fast — never 'fix' the database to match the code."

Do NOT author declarative `Base`/`Table` classes that define columns
here — that would make SQLAlchemy own structure, which is forbidden
(CLAUDE_CODE_RULES.md rule 3). This module only reflects what the DDL
already created.
"""

from __future__ import annotations

from sqlalchemy import Engine, MetaData, Table


def reflect_metadata(engine: Engine) -> MetaData:
    """Reflect all tables and views from the live database.

    Thin wrapper around SQLAlchemy's reflection; carries no
    ALCSM-specific structure of its own.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata


def get_table(metadata: MetaData, name: str) -> Table:
    """Look up a reflected table/view by name.

    Raises KeyError if `name` is not present in the live schema —
    treat that as "fail fast", not as something to work around.
    """
    return metadata.tables[name]


# TODO (P0, post schema-deploy): add a `verify_schema_matches(engine)`
# check that reflects the live catalogue and asserts the 22 expected
# base tables and 5 expected views (PROJECT_CONTEXT.md §13, §16) are
# all present, failing fast on any mismatch. Left unimplemented here
# because it depends on the schema actually being deployed first.
