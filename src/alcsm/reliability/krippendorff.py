"""Per-dimension Krippendorff's alpha, bootstrap CI, % agreement, variance.

TODO (Phase P5): implement once pilot annotation data exists.

Must:
    - compute alpha separately per dimension, never pooled across the
      six dimensions (PROJECT_CONTEXT.md §27, §41 — formative index,
      dimensions are not expected to correlate);
    - read only pre-adjudication, independent rows via
      `db.queries.fetch_reliability_input` (i.e. `v_reliability_input`),
      never the base `alcsm_dimension_score` table and never
      adjudicated rows (PROJECT_CONTEXT.md §16, §27, §48);
    - never compute or report Cronbach's alpha across dimensions
      (PROJECT_CONTEXT.md §3, §41 — wrong statistic for a formative
      index);
    - store results (alpha, bootstrap CI bounds, % agreement, n,
      variance) into `reliability_result`, tagged with the thresholds
      from PROJECT_CONTEXT.md §48 (>= .80 proceed; .667-.80 acceptable
      with review; < .667 revise rulebook *wording*, never criteria).

Test against hand-worked small cases with a known alpha
(PROJECT_CONTEXT.md §33).

Not implemented in Phase P0 — repository scaffolding only.
"""

from __future__ import annotations


def compute_alpha_for_dimension(*args: object, **kwargs: object) -> float:
    """Placeholder for per-dimension Krippendorff's alpha. See module TODO."""
    raise NotImplementedError("Implemented in Phase P5 (reliability).")
