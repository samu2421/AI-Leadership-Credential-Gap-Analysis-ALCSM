"""P0 skeleton test. Real coverage (hand-worked cases with a known
alpha, per PROJECT_CONTEXT.md §33) is added in Phase P5.
"""

from __future__ import annotations

import pytest

from alcsm.reliability.krippendorff import compute_alpha_for_dimension


def test_compute_alpha_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        compute_alpha_for_dimension()
