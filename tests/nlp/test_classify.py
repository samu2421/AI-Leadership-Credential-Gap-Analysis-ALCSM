"""P0 skeleton test. Real coverage is added in Phase P7, after a human
gold standard exists (Phase P6) and taxonomies are anchored (Phase P3).
"""

from __future__ import annotations

import pytest

from alcsm.nlp.classify import classify_dimension


def test_classify_dimension_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        classify_dimension()
