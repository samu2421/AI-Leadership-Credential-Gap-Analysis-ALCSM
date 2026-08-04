"""Taxonomy-specific fixtures.

Shares the throwaway-cluster/`db_connection` fixtures defined in
`tests/conftest.py` (Phase P3 Session 2) with `tests/collection/`,
rather than standing up a second cluster. No real personal data or
real job-posting text is used anywhere here (CLAUDE_CODE_RULES.md rule
6) — only constructed, synthetic values.
"""

from __future__ import annotations

import itertools

import pytest

_taxonomy_version_id_counter = itertools.count(1)


@pytest.fixture()
def unique_taxonomy_version_id() -> str:
    """A fresh, non-colliding taxonomy_version_id for each test."""
    return f"TAX-TEST-{next(_taxonomy_version_id_counter):04d}"
