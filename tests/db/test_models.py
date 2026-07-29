"""Tests for alcsm.db.models — generic reflection only, never declarative
table ownership (CLAUDE_CODE_RULES.md rule 3).
"""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine, text

from alcsm.db.models import get_table, reflect_metadata


def test_reflect_metadata_picks_up_an_existing_table() -> None:
    # A throwaway in-memory database, not the ALCSM schema — this only
    # proves the generic reflection wrapper works.
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE sample (id INTEGER PRIMARY KEY)"))
    metadata = reflect_metadata(engine)
    table = get_table(metadata, "sample")
    assert table.name == "sample"


def test_get_table_raises_key_error_for_unknown_table() -> None:
    engine = create_engine("sqlite:///:memory:")
    metadata = reflect_metadata(engine)
    with pytest.raises(KeyError):
        get_table(metadata, "does_not_exist")
