"""Tests for alcsm.config — spec: env-driven, no hard-coded secrets/DSN."""

from __future__ import annotations

import pytest

from alcsm.config import load_settings


def test_load_settings_succeeds_with_all_vars_set(fake_db_env: None) -> None:
    settings = load_settings()
    assert settings.database.name == "alcsm_test"
    assert settings.database.port == 5432
    assert settings.log_level == "INFO"


def test_to_dsn_builds_a_postgresql_dsn(fake_db_env: None) -> None:
    settings = load_settings()
    dsn = settings.database.to_dsn()
    assert dsn.startswith("postgresql+psycopg2://")
    assert "alcsm_test_user" in dsn
    assert "alcsm_test" in dsn


def test_missing_required_var_raises_readable_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_NAME", raising=False)
    monkeypatch.setenv("DATABASE_USER", "u")
    monkeypatch.setenv("DATABASE_HOST", "h")
    monkeypatch.setenv("DATABASE_PASSWORD", "p")
    with pytest.raises(RuntimeError, match="DATABASE_NAME"):
        load_settings()
