"""P0 skeleton test. Real coverage is added in Phase P3, after job
postings are collected.
"""

from __future__ import annotations

import pytest

from alcsm.taxonomy.anchoring import anchor_taxonomy_from_postings


def test_anchor_taxonomy_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        anchor_taxonomy_from_postings()
