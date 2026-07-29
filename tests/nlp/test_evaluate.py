"""P0 skeleton test. Real coverage (tiny fixture with known gold
scores, per PROJECT_CONTEXT.md §33) is added in Phase P7.
"""

from __future__ import annotations

import pytest

from alcsm.nlp.evaluate import evaluate_predictions


def test_evaluate_predictions_skeleton_raises_not_implemented() -> None:
    with pytest.raises(NotImplementedError):
        evaluate_predictions()
