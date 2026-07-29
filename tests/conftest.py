"""Shared pytest fixtures. No real personal data is ever used here
(CLAUDE_CODE_RULES.md rule 6) — only constructed, non-personal values.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def fake_db_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set constructed, non-secret DB environment variables for tests."""
    monkeypatch.setenv("DATABASE_NAME", "alcsm_test")
    monkeypatch.setenv("DATABASE_USER", "alcsm_test_user")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv("DATABASE_PASSWORD", "fake-test-password")
