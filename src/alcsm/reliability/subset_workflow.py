"""Two-file (primary researcher + independent second rater) reliability
workflow for the P6 double-coding subset.

This module does not reimplement Krippendorff's alpha, the RATER_A/
RATER_B human-only guard, the decision-threshold verdict, or the
per-dimension-only discipline -- all of that already exists and is
already tested in `alcsm.reliability.krippendorff` and
`alcsm.analysis.rq3_validation.inter_rater_reliability` (built in an
earlier phase). This module reuses `inter_rater_reliability` directly
and only adds the piece it did not need before: reading the *real*
two-file shape this task's Part 2 produces (the frozen annotation
workbook's `Dimension_Evidence` sheet for the primary researcher's
scores, and a filled-in `Rater_A_Blank_Template.xlsx`-shaped wide
sheet for the second rater), converting both into the long
`Profile_ID, Dimension, Score` shape `ratings_from_dimension_evidence`
already expects, and adding the descriptive statistics (score
distribution, missing/unavailable counts) the task also asks for but
that were not previously computed anywhere.

Missing-data handling (Part 5 of the FINAL VALIDATION AND ANALYSIS
STAGE task): a profile x dimension unit is included in a dimension's
alpha computation ONLY if BOTH raters recorded an observed score for
it. A unit where either rater's value is `unavailable` (primary:
`Missing_Status == "unavailable"`; second rater: a blank cell) is
excluded from that dimension's `Ratings` entirely -- never coerced to
0. This preserves exactly the distinction the frozen annotation
already encodes for `LP0041`/`LP0170`/`LP0182`'s D3/D6 cells, and
applies the identical rule to whichever profiles the second rater
marks unavailable.

Nothing in this module is run against real second-rater data anywhere
in this repository -- no genuinely independent second-rater dataset
exists yet. It is exercised only against synthetic fixtures in
`tests/reliability/test_subset_workflow.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from alcsm.analysis.rq3_validation import (
    NotAHumanRaterError,
    inter_rater_reliability,
    ratings_from_dimension_evidence,
)
from alcsm.constants import DIMENSIONS

PRIMARY_RATER_ID = "RATER_A"
SECOND_RATER_ID = "RATER_B"

__all__ = [
    "PRIMARY_RATER_ID",
    "SECOND_RATER_ID",
    "NotAHumanRaterError",
    "DimensionReliabilitySummary",
    "load_primary_scores_long",
    "load_second_rater_scores_long",
    "run_subset_reliability_analysis",
]


def load_primary_scores_long(
    annotation_path: Path | str, profile_ids: set[str]
) -> pd.DataFrame:
    """Primary researcher's ("RATER_A") observed scores for
    ``profile_ids``, read directly from the frozen annotation
    workbook's `Dimension_Evidence` sheet.

    Rows with `Missing_Status == "unavailable"` are dropped -- they are
    not observed scores and must not enter the coincidence matrix as a
    disguised 0. Returns columns `Profile_ID, Dimension, Score`.
    """
    de = pd.read_excel(annotation_path, sheet_name="Dimension_Evidence")
    de = de[de["Profile_ID"].isin(profile_ids)]
    observed = de[de["Missing_Status"] == "present"]
    return observed[["Profile_ID", "Dimension", "Final_Score"]].rename(
        columns={"Final_Score": "Score"}
    )


def load_second_rater_scores_long(template_path: Path | str) -> pd.DataFrame:
    """Second rater's observed scores from a filled-in
    `Rater_A_Blank_Template.xlsx`-shaped sheet (wide: `Profile_ID, D1..
    D6`, blank cell = unavailable, per
    `Second_Rater_Annotation_Instructions_v1.1.md` §7).

    Blank cells (NaN after `pandas` reads an empty Excel cell) are
    dropped, not coerced to 0. Returns columns `Profile_ID, Dimension,
    Score`.
    """
    wide = pd.read_excel(template_path, sheet_name="Independent_Coding")
    dim_cols = [f"D{d.number}" for d in DIMENSIONS]
    long = wide.melt(
        id_vars="Profile_ID",
        value_vars=dim_cols,
        var_name="Dimension",
        value_name="Score",
    )
    return long.dropna(subset=["Score"])


@dataclass(frozen=True)
class DimensionReliabilitySummary:
    """Everything the task's Part 4 output list asks for, for ONE
    dimension. Never combined or averaged with any other dimension's
    summary anywhere in this module."""

    dimension_number: int
    n_units: int  # profiles with an observed score from BOTH raters
    krippendorff_alpha: float
    alpha_ci_lower: float | None
    alpha_ci_upper: float | None
    percent_agreement: float  # == exact agreement fraction (Po), paired units
    score_variance: float  # pooled across both raters' ratings
    verdict: str
    primary_score_distribution: dict[int, int]
    second_rater_score_distribution: dict[int, int]
    primary_unavailable_count: int
    second_rater_unavailable_count: int
    both_unavailable_count: int
    rater_a_variance: float  # Rater A's own ratings only
    rater_b_variance: float  # Rater B's own ratings only
    rater_a_n_categories: int  # distinct score values Rater A actually used
    rater_b_n_categories: int
    exact_agreement_count: int  # raw count, companion to percent_agreement's fraction
    disagreement_magnitude_distribution: dict[
        int, int
    ]  # |A-B| -> count, paired units only


def _distribution(scores: pd.Series) -> dict[int, int]:
    counts = scores.astype(int).value_counts().sort_index()
    return {int(score): int(n) for score, n in counts.items()}


def _variance(scores: pd.Series) -> float:
    if len(scores) < 2:
        return float("nan")
    values = scores.astype(float)
    mean = values.mean()
    return float(((values - mean) ** 2).mean())


def run_subset_reliability_analysis(
    primary_long: pd.DataFrame,
    second_rater_long: pd.DataFrame,
    subset_profile_ids: set[str],
    rulebook_version: str = "v1.1",
    source_description: str = "P6 double-coding subset (RATER_A vs RATER_B)",
) -> dict[int, DimensionReliabilitySummary]:
    """Per-dimension (never pooled) Krippendorff's alpha, agreement, n,
    score distribution, variance, and missing/unavailable counts, for
    the double-coding subset.

    ``primary_long`` / ``second_rater_long``: `Profile_ID, Dimension,
    Score` frames as produced by `load_primary_scores_long` /
    `load_second_rater_scores_long` -- already stripped of unavailable
    entries. ``subset_profile_ids``: the full subset roster (used only
    to compute unavailable counts -- a profile that contributed no row
    to a rater's `*_long` frame for a dimension is unavailable for that
    rater on that dimension).

    Alpha/CI/agreement/n/verdict are computed entirely by
    `alcsm.analysis.rq3_validation.inter_rater_reliability`, unchanged
    -- including its `NotAHumanRaterError` guard, which fires here too
    if either input frame were ever mislabeled. A dimension with fewer
    than two comparable units (e.g. every profile in the subset is
    unavailable for that rater pair) is simply absent from the
    returned dict, matching `inter_rater_reliability`'s own behavior.
    """
    ratings_by_dimension = ratings_from_dimension_evidence(
        {PRIMARY_RATER_ID: primary_long, SECOND_RATER_ID: second_rater_long}
    )
    report = inter_rater_reliability(
        ratings_by_dimension,
        analysis_stage="main_double_coded",
        corpus="profile",
        rulebook_version=rulebook_version,
        source_description=source_description,
    )

    results: dict[int, DimensionReliabilitySummary] = {}
    for d in DIMENSIONS:
        verdict = report.by_dimension.get(d.number)
        if verdict is None:
            continue
        result = verdict.result
        dim_label = f"D{d.number}"

        primary_scored = set(
            primary_long.loc[primary_long["Dimension"] == dim_label, "Profile_ID"]
        )
        second_scored = set(
            second_rater_long.loc[
                second_rater_long["Dimension"] == dim_label, "Profile_ID"
            ]
        )
        primary_unavailable = subset_profile_ids - primary_scored
        second_unavailable = subset_profile_ids - second_scored
        both_unavailable = primary_unavailable & second_unavailable

        primary_dim_scores = primary_long.loc[
            primary_long["Dimension"] == dim_label, ["Profile_ID", "Score"]
        ]
        second_dim_scores = second_rater_long.loc[
            second_rater_long["Dimension"] == dim_label, ["Profile_ID", "Score"]
        ]
        paired = primary_dim_scores.merge(
            second_dim_scores, on="Profile_ID", suffixes=("_a", "_b")
        )
        disagreement = (paired["Score_a"] - paired["Score_b"]).abs().astype(int)

        results[d.number] = DimensionReliabilitySummary(
            dimension_number=d.number,
            n_units=result.n_units,
            krippendorff_alpha=result.krippendorff_alpha,
            alpha_ci_lower=result.alpha_ci_lower,
            alpha_ci_upper=result.alpha_ci_upper,
            percent_agreement=result.percent_agreement,
            score_variance=result.score_variance,
            verdict=verdict.verdict,
            primary_score_distribution=_distribution(primary_dim_scores["Score"]),
            second_rater_score_distribution=_distribution(second_dim_scores["Score"]),
            primary_unavailable_count=len(primary_unavailable),
            second_rater_unavailable_count=len(second_unavailable),
            both_unavailable_count=len(both_unavailable),
            rater_a_variance=_variance(primary_dim_scores["Score"]),
            rater_b_variance=_variance(second_dim_scores["Score"]),
            rater_a_n_categories=primary_dim_scores["Score"].nunique(),
            rater_b_n_categories=second_dim_scores["Score"].nunique(),
            exact_agreement_count=int((disagreement == 0).sum()),
            disagreement_magnitude_distribution=_distribution(disagreement),
        )
    return results
