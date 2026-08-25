"""RQ1 — What credential patterns exist among AI leaders?

Purely descriptive analysis over profile demographics and D1-D6
scores. Every function here returns counts, means, medians, and
cross-tabulations — never a causal claim. A dimension being higher on
average for one `Title_Category` than another describes an observed
association in this sample, not a cause; no function in this module
computes a p-value, effect size, or any other inferential statistic
that could be mistaken for one, and no docstring or field name here
uses causal language ("effect", "impact", "drives", "leads to").

Every top-level function's result carries `AnalysisRunMetadata`
(`alcsm.analysis.config`). Functions that consume D1-D6 scores call
`require_frozen_or_acknowledge_provisional` first — see that module's
docstring for why.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from alcsm.analysis.config import (
    AnalysisRunMetadata,
    DataStatus,
    make_metadata,
    require_frozen_or_acknowledge_provisional,
)
from alcsm.annotation.dimension_config import get_dimension_config
from alcsm.constants import DIMENSIONS

_DIMENSION_FINAL_COLUMNS = [f"D{d.number}_Final" for d in DIMENSIONS]
# Display labels are sourced from the versioned v1.1 config, not the
# frozen v1.0 `alcsm.constants.DIMENSIONS` labels -- D6's v1.0 label
# ("Professional Engagement & Continuous Development") was retired and
# replaced by "AI Industry/Application Breadth" for v1.1 (D-0038); D1-D5
# labels are identical across both sources either way. Same pattern
# already applied in `alcsm.analysis.survey`.
_DIMENSION_LABELS = {d.number: d.label for d in get_dimension_config("v1_1")}


@dataclass(frozen=True)
class DemographicSummary:
    metadata: AnalysisRunMetadata
    n_profiles: int
    country_counts: pd.Series
    federal_state_counts: pd.Series
    company_size_counts: pd.Series
    industry_counts: pd.Series
    title_category_counts: pd.Series


def demographic_summary(
    profile_master: pd.DataFrame,
    source_description: str = "LinkedIn processed workbook",
) -> DemographicSummary:
    """Counts of profiles by country, federal state, company size,
    industry, and title category. No score data involved -- always
    treated as collected fact, not a provisional score."""
    return DemographicSummary(
        metadata=make_metadata("final_frozen", source_description),
        n_profiles=len(profile_master),
        country_counts=profile_master["Country"].value_counts(dropna=False),
        federal_state_counts=profile_master["Federal_State"].value_counts(dropna=False),
        company_size_counts=profile_master["Company_Size"].value_counts(dropna=False),
        industry_counts=profile_master["Industry"].value_counts(dropna=False),
        title_category_counts=profile_master["Title_Category"].value_counts(
            dropna=False
        ),
    )


@dataclass(frozen=True)
class DimensionDistribution:
    metadata: AnalysisRunMetadata
    n_profiles: int
    counts: pd.DataFrame  # index=score 0-5, columns=D1..D6
    means: pd.Series  # index=D1..D6
    medians: pd.Series
    std_devs: pd.Series


def dimension_distribution(
    profile_scores: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> DimensionDistribution:
    """Score counts (0-5), mean, median, std per dimension.

    ``use_final=True`` reads the `D{n}_Final` columns (the researcher-
    review layer's running value); ``use_final=False`` reads
    `D{n}_FirstPass` instead, for explicitly comparing the two — never
    silently substituted for each other.
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    suffix = "Final" if use_final else "FirstPass"
    cols = [f"D{d.number}_{suffix}" for d in DIMENSIONS]
    counts = pd.DataFrame(
        {
            c: profile_scores[c].value_counts().reindex(range(6), fill_value=0)
            for c in cols
        }
    )
    counts.columns = [f"D{d.number}" for d in DIMENSIONS]
    means = pd.Series(
        {
            f"D{d.number}": profile_scores[f"D{d.number}_{suffix}"].mean()
            for d in DIMENSIONS
        }
    )
    medians = pd.Series(
        {
            f"D{d.number}": profile_scores[f"D{d.number}_{suffix}"].median()
            for d in DIMENSIONS
        }
    )
    stds = pd.Series(
        {
            f"D{d.number}": profile_scores[f"D{d.number}_{suffix}"].std()
            for d in DIMENSIONS
        }
    )
    return DimensionDistribution(
        metadata=make_metadata(data_status, source_description),
        n_profiles=len(profile_scores),
        counts=counts,
        means=means,
        medians=medians,
        std_devs=stds,
    )


@dataclass(frozen=True)
class MissingnessReport:
    metadata: AnalysisRunMetadata
    by_dimension: (
        pd.DataFrame
    )  # index=D1..D6, columns=missing_status values, values=counts


def dimension_missingness(
    dimension_evidence: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
) -> MissingnessReport:
    """Per-dimension count of each `Missing_Status` value.

    Reads `Missing_Status` as recorded (first-pass or reviewed,
    whichever is in `Dimension_Evidence` at call time) -- this function
    reports what is there, it does not distinguish first-pass from
    reviewed missingness itself (see `researcher_review_changes` in
    `rq3_validation.py` for tracking what the researcher actually
    changed).
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    table = (
        dimension_evidence.groupby(["Dimension", "Missing_Status"])
        .size()
        .unstack(fill_value=0)
    )
    table = table.reindex([f"D{d.number}" for d in DIMENSIONS])
    return MissingnessReport(
        metadata=make_metadata(data_status, source_description), by_dimension=table
    )


@dataclass(frozen=True)
class GroupedDimensionMeans:
    """Mean D1-D6 score per level of a grouping column (title category,
    company size, or industry) -- a descriptive cross-tabulation, not
    a claim that the grouping variable causes the score difference."""

    metadata: AnalysisRunMetadata
    group_column: str
    means: pd.DataFrame  # index=group level, columns=D1..D6
    n_per_group: pd.Series


def _grouped_dimension_means(
    profile_master: pd.DataFrame,
    profile_scores: pd.DataFrame,
    group_column: str,
    data_status: DataStatus,
    source_description: str,
    acknowledge_provisional: bool,
    use_final: bool,
) -> GroupedDimensionMeans:
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    suffix = "Final" if use_final else "FirstPass"
    score_cols = [f"D{d.number}_{suffix}" for d in DIMENSIONS]
    merged = profile_master[["Profile_ID", group_column]].merge(
        profile_scores[["Profile_ID", *score_cols]], on="Profile_ID", how="inner"
    )
    means = merged.groupby(group_column)[score_cols].mean()
    means.columns = [f"D{d.number}" for d in DIMENSIONS]
    n_per_group = merged.groupby(group_column).size()
    return GroupedDimensionMeans(
        metadata=make_metadata(data_status, source_description),
        group_column=group_column,
        means=means,
        n_per_group=n_per_group,
    )


def title_category_patterns(
    profile_master: pd.DataFrame,
    profile_scores: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> GroupedDimensionMeans:
    """Mean D1-D6 per `Title_Category`."""
    return _grouped_dimension_means(
        profile_master,
        profile_scores,
        "Title_Category",
        data_status,
        source_description,
        acknowledge_provisional,
        use_final,
    )


def company_size_patterns(
    profile_master: pd.DataFrame,
    profile_scores: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> GroupedDimensionMeans:
    """Mean D1-D6 per `Company_Size` band."""
    return _grouped_dimension_means(
        profile_master,
        profile_scores,
        "Company_Size",
        data_status,
        source_description,
        acknowledge_provisional,
        use_final,
    )


def industry_patterns(
    profile_master: pd.DataFrame,
    profile_scores: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> GroupedDimensionMeans:
    """Mean D1-D6 per current-employer `Industry` (single-industry field
    from `Profile_Master`, distinct from D6's AI-related industry
    *breadth* -- see `ALCSM_D6_Industry_Breadth_v1.1.md` §5 Question D
    for why the two must not be conflated)."""
    return _grouped_dimension_means(
        profile_master,
        profile_scores,
        "Industry",
        data_status,
        source_description,
        acknowledge_provisional,
        use_final,
    )


@dataclass(frozen=True)
class DimensionLevelComparison:
    """A side-by-side descriptive comparison of the six dimensions --
    explicitly not a composite score and not a claim that the
    dimensions are commensurable or summable (they are formative,
    non-interchangeable indicators; see `ALCSM_Measurement_Model_and_
    Validation_Note.md` §1)."""

    metadata: AnalysisRunMetadata
    table: (
        pd.DataFrame
    )  # index=D1..D6, columns=[mean, median, std, min, max, n_present]


def dimension_level_comparison(
    profile_scores: pd.DataFrame,
    dimension_evidence: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
    use_final: bool = True,
) -> DimensionLevelComparison:
    """One row per dimension: mean/median/std/min/max of the score,
    plus how many profiles have `present`/`absent_stated` (informative)
    evidence for it. Presented side by side for reporting only -- never
    summed, weighted, or otherwise combined into one number here."""
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    suffix = "Final" if use_final else "FirstPass"
    rows = []
    for d in DIMENSIONS:
        col = f"D{d.number}_{suffix}"
        series = profile_scores[col]
        n_present = (
            (dimension_evidence["Dimension"] == f"D{d.number}")
            & (dimension_evidence["Missing_Status"].isin(["present", "absent_stated"]))
        ).sum()
        rows.append(
            {
                "dimension": f"D{d.number}",
                "label": _DIMENSION_LABELS[d.number],
                "mean": series.mean(),
                "median": series.median(),
                "std": series.std(),
                "min": series.min(),
                "max": series.max(),
                "n_informative": n_present,
            }
        )
    table = pd.DataFrame(rows).set_index("dimension")
    return DimensionLevelComparison(
        metadata=make_metadata(data_status, source_description), table=table
    )
