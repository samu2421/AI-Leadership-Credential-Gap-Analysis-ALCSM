"""Tests for alcsm.db.engine — engine/session lifecycle only, no schema
ownership (PROJECT_CONTEXT.md §23).
"""

from __future__ import annotations

import alcsm.db.engine as engine_module
from alcsm.config import DatabaseSettings, Settings
from alcsm.db.engine import get_engine


def test_get_engine_builds_from_settings_without_connecting(
    monkeypatch: object,
) -> None:
    # Reset process-wide singleton so this test is independent of order.
    engine_module._engine = None
    settings = Settings(
        database=DatabaseSettings(
            name="alcsm_test",
            user="u",
            host="localhost",
            port=5432,
            password="p",
        ),
        log_level="INFO",
    )
    engine = get_engine(settings)
    assert engine.dialect.name == "postgresql"
    engine_module._engine = None
