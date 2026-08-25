"""Credential gap per dimension (RQ2): mean required - mean held.

Two genuinely different measurements live on the two sides of this
question, and this module keeps them in separate fields everywhere
rather than blending them into one number:

- **Requirement-side (demand):** `Requirements.Final_ALCSM_Dimension`
  is a *mapping* of each requirement's text to one of the six
  dimensions (or "Not Directly Mapped") — a frequency/volume signal,
  not a 0-5 required *level*. The frozen schema's `job_requirement_
  score` table (with a numeric `required_score` 0-5) is where a true
  required-level score would live, but it has not been populated —
  requirement-level 0-5 scoring is its own annotation-like process
  that has not been built or run yet (mirrors the profile-side P4
  interface, but for postings; out of scope for this task).
- **Profile-side (supply):** `Profile_Scores` D1-D6, 0-5, from the
  researcher-review layer — reuses `alcsm.analysis.rq1_descriptive.
  dimension_distribution` directly rather than reimplementing it.

`supply_vs_demand_frequency` compares requirement *counts* against
profile *score distributions* — explicitly not a "gap" (they are not
the same unit) and labelled as such. `dimension_gap_from_scores`
computes the true `mean(required) - mean(held)` gap
(`v_credential_gap_by_dimension`'s own formula, via
`db.queries.fetch_credential_gap_by_dimension` once that view has real
data) but requires a required-score table shaped like
`job_requirement_score`; until that table is populated for real, this
function is exercised only against synthetic fixtures (see
`tests/analysis/test_gap.py`) — it is built and ready, not a
placeholder, but it has no real input yet.

Must never treat a job posting's silence about a dimension
(`not_applicable`) as "requires 0" — it is excluded from the gap
calculation entirely (PROJECT_CONTEXT.md §9, §27, common mistake #7 in
§39).
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
from alcsm.analysis.rq1_descriptive import DimensionDistribution
from alcsm.constants import DIMENSIONS

NOT_DIRECTLY_MAPPED = "NOT_DIRECTLY_MAPPED"


@dataclass(frozen=True)
class RequirementCounts:
    metadata: AnalysisRunMetadata
    n_requirements: int
    counts_by_dimension: (
        pd.Series
    )  # index = Final_ALCSM_Dimension values incl. "Not Directly Mapped"
    counts_by_dimension_and_category: (
        pd.DataFrame
    )  # index=dimension, columns=Requirement_Category


def requirement_counts_by_dimension(
    requirements: pd.DataFrame,
    source_description: str = "Job postings processed workbook",
) -> RequirementCounts:
    """Count of requirement records per `Final_ALCSM_Dimension` value,
    and the same broken down by `Requirement_Category`. Requirement
    text mapping is not under researcher review the way profile scores
    are, so this is always `final_frozen` relative to its own source
    file (the mapping itself may still be revised by the researcher in
    a future pass — that revision, if it happens, is a new data version,
    not something this function infers)."""
    by_dim = requirements["Final_ALCSM_Dimension"].value_counts(dropna=False)
    by_dim_cat = (
        requirements.groupby(["Final_ALCSM_Dimension", "Requirement_Category"])
        .size()
        .unstack(fill_value=0)
    )
    return RequirementCounts(
        metadata=make_metadata("final_frozen", source_description),
        n_requirements=len(requirements),
        counts_by_dimension=by_dim,
        counts_by_dimension_and_category=by_dim_cat,
    )


@dataclass(frozen=True)
class NotDirectlyMappedReport:
    metadata: AnalysisRunMetadata
    n_total: int
    n_not_mapped: int
    fraction_not_mapped: float
    not_mapped_by_category: pd.Series


def not_directly_mapped_report(
    requirements: pd.DataFrame,
    source_description: str = "Job postings processed workbook",
) -> NotDirectlyMappedReport:
    """How many, and what fraction, of requirement records carry
    `Final_ALCSM_Dimension == 'Not Directly Mapped'`, broken down by
    `Requirement_Category`. A large "Not Directly Mapped" share is a
    property of the requirement-mapping pass, reported honestly here,
    not something this function tries to reduce or reinterpret."""
    mask = requirements["Final_ALCSM_Dimension"] == NOT_DIRECTLY_MAPPED
    n_total = len(requirements)
    n_not_mapped = int(mask.sum())
    return NotDirectlyMappedReport(
        metadata=make_metadata("final_frozen", source_description),
        n_total=n_total,
        n_not_mapped=n_not_mapped,
        fraction_not_mapped=(n_not_mapped / n_total if n_total else 0.0),
        not_mapped_by_category=requirements.loc[
            mask, "Requirement_Category"
        ].value_counts(),
    )


@dataclass(frozen=True)
class RequirementIntensity:
    """How insistently each dimension's requirements are stated --
    `Mandatory_or_Preferred` counts per dimension, e.g. what fraction
    of a dimension's requirement records are stated as required versus
    preferred/unspecified. A frequency/intensity signal, not a 0-5
    level -- kept separate from `DimensionGap` for the same reason
    `supply_vs_demand_frequency` keeps counts separate from scores."""

    metadata: AnalysisRunMetadata
    # index=D1..D6 (+ NOT_DIRECTLY_MAPPED), columns=Mandatory_or_Preferred values
    table: pd.DataFrame


def requirement_intensity_by_dimension(
    requirements: pd.DataFrame,
    source_description: str = "Job postings processed workbook",
) -> RequirementIntensity:
    """Count of requirement records per `Final_ALCSM_Dimension` x
    `Mandatory_or_Preferred`, e.g. how many of D5's requirement records
    are stated as required vs. preferred vs. not specified."""
    table = (
        requirements.groupby(["Final_ALCSM_Dimension", "Mandatory_or_Preferred"])
        .size()
        .unstack(fill_value=0)
    )
    return RequirementIntensity(
        metadata=make_metadata("final_frozen", source_description), table=table
    )


@dataclass(frozen=True)
class SupplyDemandFrequencyComparison:
    """Requirement *count* (demand-side volume) next to profile *score
    distribution* (supply-side, 0-5) per dimension. The two columns are
    different units by design -- this table is for side-by-side
    reporting, never combined into a single number."""

    metadata: AnalysisRunMetadata
    # index=D1..D6, columns=[n_requirements, profile_mean_score, profile_median_score]
    table: pd.DataFrame


def supply_vs_demand_frequency(
    requirement_counts: RequirementCounts,
    profile_distribution: DimensionDistribution,
) -> SupplyDemandFrequencyComparison:
    """Combine an already-computed :class:`RequirementCounts` and
    :class:`DimensionDistribution` into one side-by-side table.

    Deliberately takes already-computed results rather than raw
    DataFrames, so the caller's `data_status`/provisional
    acknowledgement for the profile side is visible in
    ``profile_distribution.metadata`` and cannot be silently dropped.
    """
    rows = []
    for d in DIMENSIONS:
        code = next(
            (
                idx
                for idx in requirement_counts.counts_by_dimension.index
                if str(idx).startswith(f"D{d.number} ")
            ),
            None,
        )
        n_req = (
            int(requirement_counts.counts_by_dimension[code]) if code is not None else 0
        )
        rows.append(
            {
                "dimension": f"D{d.number}",
                "n_requirements": n_req,
                "profile_mean_score": profile_distribution.means[f"D{d.number}"],
                "profile_median_score": profile_distribution.medians[f"D{d.number}"],
            }
        )
    table = pd.DataFrame(rows).set_index("dimension")
    return SupplyDemandFrequencyComparison(
        metadata=make_metadata(
            profile_distribution.metadata.data_status,
            f"requirements: {requirement_counts.metadata.source_description}; "
            f"profiles: {profile_distribution.metadata.source_description}",
        ),
        table=table,
    )


@dataclass(frozen=True)
class DimensionGap:
    metadata: AnalysisRunMetadata
    # columns: mean_required, mean_held, gap_value, n_postings, n_profiles
    table: pd.DataFrame


def dimension_gap_from_scores(
    required_scores: pd.DataFrame,
    held_scores: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
) -> DimensionGap:
    """The true `v_credential_gap_by_dimension` formula: `mean(required)
    - mean(held)`, per dimension.

    ``required_scores`` must have columns `dimension_number`,
    `required_score` (0-5), `missing_status` -- shaped like
    `job_requirement_score`. ``held_scores`` must have columns
    `dimension_number`, `score`, `missing_status` -- shaped like
    `v_final_profile_score`. Both are filtered to
    `missing_status in ('present', 'absent_stated')` before averaging
    (`unavailable`/`not_applicable` rows are excluded, never read as
    zero -- PROJECT_CONTEXT.md §9/§27, the same rule the view itself
    encodes). No real `job_requirement_score` data exists yet (see
    module docstring); this function is ready and tested against
    synthetic fixtures for when it does.
    """
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    include_statuses = {"present", "absent_stated"}
    req_included = required_scores[
        required_scores["missing_status"].isin(include_statuses)
    ]
    held_included = held_scores[held_scores["missing_status"].isin(include_statuses)]

    rows = []
    for d in DIMENSIONS:
        req_d = req_included[req_included["dimension_number"] == d.number]
        held_d = held_included[held_included["dimension_number"] == d.number]
        mean_required = req_d["required_score"].mean() if len(req_d) else float("nan")
        mean_held = held_d["score"].mean() if len(held_d) else float("nan")
        gap = (
            mean_required - mean_held
            if mean_required == mean_required and mean_held == mean_held
            else float("nan")
        )
        rows.append(
            {
                "dimension": f"D{d.number}",
                "mean_required": mean_required,
                "mean_held": mean_held,
                "gap_value": gap,
                "n_postings": len(req_d),
                "n_profiles": len(held_d),
            }
        )
    table = pd.DataFrame(rows).set_index("dimension")
    return DimensionGap(
        metadata=make_metadata(data_status, source_description), table=table
    )


@dataclass(frozen=True)
class D6Asymmetry:
    """D6 (AI Industry/Application Breadth) is reported separately from
    the generic gap table because its asymmetry is qualitatively
    different: it is not "required more than held" or vice versa, it
    is "observable on one side of the corpus and nearly absent on the
    other" (see `ALCSM_D6_Industry_Breadth_v1.1.md` §5 Question G and
    `D6_v1.1_Implementation_Assessment.md` §5 for the original finding
    this reproduces as a reusable function)."""

    metadata: AnalysisRunMetadata
    n_profiles_with_d6_evidence: int
    n_profiles_total: int
    profile_side_coverage: float
    n_requirements_d6_mappable: int
    n_requirements_total: int
    posting_side_coverage: float


def d6_profile_vs_posting_asymmetry(
    profile_scores: pd.DataFrame,
    dimension_evidence: pd.DataFrame,
    requirements: pd.DataFrame,
    data_status: DataStatus,
    source_description: str,
    *,
    acknowledge_provisional: bool = False,
) -> D6Asymmetry:
    """Compare how observable D6 is on the profile side (fraction of
    profiles with `present`/`absent_stated` D6 evidence) versus the
    posting side (fraction of requirements mapped to D6)."""
    require_frozen_or_acknowledge_provisional(
        data_status, acknowledge_provisional=acknowledge_provisional
    )
    d6_evidence = dimension_evidence[dimension_evidence["Dimension"] == "D6"]
    n_with_evidence = (
        d6_evidence["Missing_Status"].isin(["present", "absent_stated"]).sum()
    )
    n_profiles = len(profile_scores)

    d6_code = next(
        (
            c
            for c in requirements["Final_ALCSM_Dimension"].unique()
            if str(c).startswith("D6 ")
        ),
        None,
    )
    n_mappable = (
        int((requirements["Final_ALCSM_Dimension"] == d6_code).sum()) if d6_code else 0
    )
    n_requirements = len(requirements)

    return D6Asymmetry(
        metadata=make_metadata(data_status, source_description),
        n_profiles_with_d6_evidence=int(n_with_evidence),
        n_profiles_total=n_profiles,
        profile_side_coverage=(n_with_evidence / n_profiles if n_profiles else 0.0),
        n_requirements_d6_mappable=n_mappable,
        n_requirements_total=n_requirements,
        posting_side_coverage=(n_mappable / n_requirements if n_requirements else 0.0),
    )
