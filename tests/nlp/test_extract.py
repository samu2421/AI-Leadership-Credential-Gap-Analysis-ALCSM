"""P0 skeleton test. Real coverage is added in Phase P7."""

from __future__ import annotations

import pytest

from alcsm.nlp.extract import extract_features


def test_extract_features_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        extract_features()
