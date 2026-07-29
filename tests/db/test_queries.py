"""P0 skeleton tests: each query function is unimplemented until its
owning phase (PROJECT_CONTEXT.md §38).
"""

from __future__ import annotations

import pytest

from alcsm.db import queries


@pytest.mark.parametrize(
    "func",
    [
        queries.fetch_reliability_input,
        queries.fetch_final_profile_scores,
        queries.fetch_profile_completeness,
        queries.fetch_credential_gap_by_dimension,
        queries.fetch_nlp_evaluation,
    ],
)
def test_query_skeleton_raises_not_implemented(func: object) -> None:
    with pytest.raises(NotImplementedError):
        func(None)  # type: ignore[arg-type]
