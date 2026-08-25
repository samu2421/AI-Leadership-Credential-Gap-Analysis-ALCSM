"""Ordinal correlation between credential signal and RQ4 impact indicators.

The four criterion variables are already defined and frozen
(`rq4_impact_indicator`, `ALCSM_Measurement_Model_and_Validation_Note.md`
§3) — this module introduces no new ones and provides no mechanism to
add one; `CRITERION_VARIABLES` below is the complete, closed list.

**Physical/conceptual isolation, enforced by import structure, not just
convention:** this is the only module in `alcsm.analysis` that reads
anything shaped like `rq4_impact_indicator`. Nothing here is imported
by `rq1_descriptive.py`, `gap.py`, `rq3_validation.py`, or
`alcsm.nlp.evaluate`, and this module imports nothing from them either
— a correlation input and an ALCSM score never flow through the same
function. `tests/analysis/test_isolation.py` checks this at the AST
level, the same technique `tests/annotation/test_access_separation.py`
already used for the P4 interface's RQ4 isolation.

`rq4_impact_indicator` values are *external validation criteria*,
physically isolated from the ALCSM dimensions — they must never be
used as a scoring input, and mixing them into a dimension score would
make the validation circular (PROJECT_CONTEXT.md §5, §15, §27).

Ordinal-appropriate correlation only (Spearman's rank correlation,
computed via rank-transformed Pearson to avoid a hard `scipy`
dependency — the same technique used earlier in this project's D6 v1.1
distinctiveness analysis). **A correlation coefficient describes an
association observed in this sample; it is not evidence of a causal
relationship, and no function here computes or implies one** (this
task's explicit "do not introduce new criterion variables" sits
alongside RQ1's "do not create unsupported causal interpretations" —
the same discipline applies here).

No real `rq4_impact_indicator` data exists yet (no profile has been
loaded into the database — see `P4_Implementation_Completion_Report.md`
§3.2 for why). This module is built and tested against synthetic
fixtures, ready to run once real data exists.
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass

import pandas as pd

from alcsm.analysis.config import (
    AnalysisRunMetadata,
    DataStatus,
    make_metadata,
    require_frozen_or_acknowledge_provisional,
)
from alcsm.constants import DIMENSIONS

# The complete, closed set of RQ4 criterion variables
# (rq4_impact_indicator's own columns, minus metadata columns).
# PROJECT_CONTEXT.md §15/§45: never used as a scoring input; never
# shown to a rater; never a sixth "dimension".
CRITERION_VARIABLES: tuple[str, ...] = (
    "rq4_network_reach",
    "rq4_content_engagement",
    "rq4_recognition_count",
    "rq4_seniority_progression_rate",
)


def _spearman(a: pd.Series, b: pd.Series) -> tuple[float, int]:
    """Spearman's rank correlation via rank-transformed Pearson (no
    scipy dependency). Rows where either value is NaN are dropped
    pairwise before ranking, matching pandas' own default `.corr()`
    pairwise-deletion behaviour."""
    paired = pd.DataFrame({"a": a, "b": b}).dropna()
    n = len(paired)
    if n < 2:
        return float("nan"), n
    # A zero-variance column (e.g. a criterion that is constant across
    # every paired profile in a small fixture) correctly yields NaN
    # here -- numpy's underlying divide-by-zero warning is expected
    # noise for that case, not a sign of a computation error.
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        rho = paired["a"].rank().corr(paired["b"].rank(), method="pearson")
    return float(rho), n


@dataclass(frozen=True)
class CriterionCorrelation:
    dimension: str
    criterion_variable: str
    spearman_rho: float
    n_paired_observations: int


@dataclass(frozen=True)
class RQ4CorrelationReport:
    metadata: AnalysisRunMetadata
    table: (
        pd.DataFrame
    )  # index=D1..D6, columns=CRITERION_VARIABLES, values=spearman_rho
    n_table: pd.DataFrame  # same shape, values=n_paired_observations
    correlations: list[CriterionCorrelation]


def correlate_with_impact_indicators(
    profile_scores: pd.DataFrame,
    impact_indicators: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> RQ4CorrelationReport:
    """Spearman correlation between each ALCSM dimension score and each
    RQ4 criterion variable, per dimension x criterion pair.

    ``profile_scores`` needs `Profile_ID` and `D{n}_Final`/`D{n}_
    FirstPass` columns (the researcher-review layer's shape).
    ``impact_indicators`` needs `profile_id` plus the columns named in
    `CRITERION_VARIABLES` (the `rq4_impact_indicator` shape). Merged on
    profile id; a profile missing from either side is excluded from
    every correlation it would have contributed to (pairwise, per
    dimension x criterion combination, computed independently -- never
    one blanket listwise-deletion pass that could silently shrink an
    unrelated pair's sample size).
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    suffix = "Final" if use_final else "FirstPass"
    merged = profile_scores.merge(
        impact_indicators, left_on="Profile_ID", right_on="profile_id", how="inner"
    )

    correlations: list[CriterionCorrelation] = []
    dims = [f"D{d.number}" for d in DIMENSIONS]
    table = pd.DataFrame(index=dims, columns=CRITERION_VARIABLES, dtype=float)
    n_table = pd.DataFrame(index=dims, columns=CRITERION_VARIABLES, dtype=int)

    for d in DIMENSIONS:
        score_col = f"D{d.number}_{suffix}"
        for criterion in CRITERION_VARIABLES:
            rho, n = _spearman(merged[score_col], merged[criterion])
            table.loc[f"D{d.number}", criterion] = rho
            n_table.loc[f"D{d.number}", criterion] = n
            correlations.append(
                CriterionCorrelation(
                    dimension=f"D{d.number}",
                    criterion_variable=criterion,
                    spearman_rho=rho,
                    n_paired_observations=n,
                )
            )

    return RQ4CorrelationReport(
        metadata=make_metadata(data_status, source_description),
        table=table,
        n_table=n_table,
        correlations=correlations,
    )
