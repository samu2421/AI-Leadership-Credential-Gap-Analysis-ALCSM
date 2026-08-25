"""RQ2 gap analysis: job-posting requirements vs. profile credential
signals, at the dimension level (aggregate, never one-to-one).

Reuses `alcsm.analysis.gap` and `alcsm.analysis.rq1_descriptive`
unchanged, plus one new small function added this session
(`requirement_intensity_by_dimension` -- Mandatory/Preferred/Not
Specified counts per dimension, a frequency signal, not a 0-5 level).

No individual profile is matched against an individual posting
anywhere in this script -- every comparison is an aggregate,
dimension-level statistic. `NOT_DIRECTLY_MAPPED` requirements are
reported as their own category, never forced into a dimension.

A true numeric "required level" (0-5) does not exist anywhere in this
project's data -- `job_requirement_score.required_score` has never
been populated (a separate, unbuilt requirement-scoring pass). This
script therefore does NOT compute `dimension_gap_from_scores` against
real data (that function remains fixture-tested only, per
`gap.py`'s own docstring) and does NOT report a numeric "gap value".
Instead, "gap direction" is described qualitatively by comparing
requirement volume/intensity (demand) against profile held-score
level (supply) -- explicitly labeled as a qualitative comparison of
two different units, not a subtraction.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from alcsm.analysis.gap import (
    d6_profile_vs_posting_asymmetry,
    not_directly_mapped_report,
    requirement_counts_by_dimension,
    requirement_intensity_by_dimension,
    supply_vs_demand_frequency,
)
from alcsm.analysis.rq1_descriptive import dimension_distribution

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
JOB_POSTINGS_PATH = (
    REPO_ROOT
    / "05_Data_Collection"
    / "Job_Postings"
    / "02_Processed"
    / "ALCSM_JobPosting_Processed_v1.1.xlsx"
)
OUTPUT_DIR = REPO_ROOT / "09_Statistical_Analysis" / "RQ2"
TABLES_DIR = OUTPUT_DIR / "Tables"
FIGURES_DIR = OUTPUT_DIR / "Figures"


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    requirements = pd.read_excel(JOB_POSTINGS_PATH, sheet_name="Requirements")
    profile_scores = pd.read_excel(ANNOTATION_PATH, sheet_name="Profile_Scores")
    dimension_evidence = pd.read_excel(ANNOTATION_PATH, sheet_name="Dimension_Evidence")

    # --- Table 1: requirement counts by dimension (demand-side volume)
    rc = requirement_counts_by_dimension(requirements)
    rc.counts_by_dimension.to_csv(
        TABLES_DIR / "Table1_Requirement_Counts_By_Dimension.csv"
    )
    print(f"Table 1 (n={rc.n_requirements} requirements):")
    print(rc.counts_by_dimension)

    # --- Table 2: Not Directly Mapped, explicitly reported
    ndm = not_directly_mapped_report(requirements)
    print(
        f"\nTable 2: Not Directly Mapped = {ndm.n_not_mapped}/{ndm.n_total} "
        f"({ndm.fraction_not_mapped:.1%})"
    )
    ndm.not_mapped_by_category.to_csv(
        TABLES_DIR / "Table2_NotDirectlyMapped_By_Category.csv"
    )
    print(ndm.not_mapped_by_category)

    # --- Table 3: profile-side held level (mean/median) by dimension
    dd = dimension_distribution(profile_scores, "final_frozen", str(ANNOTATION_PATH))
    held_table = pd.DataFrame({"mean_held": dd.means, "median_held": dd.medians})
    held_table.to_csv(TABLES_DIR / "Table3_Mean_Median_Held_Level_By_Dimension.csv")
    print("\nTable 3 (mean/median HELD level, profile side):")
    print(held_table)

    # --- Table 4: supply (held level) vs. demand (requirement count) side by side
    svd = supply_vs_demand_frequency(rc, dd)
    svd.table.to_csv(TABLES_DIR / "Table4_Supply_vs_Demand_Frequency.csv")
    print("\nTable 4 (supply vs. demand, different units, side by side):")
    print(svd.table)

    # --- Table 5: requirement intensity (Mandatory/Preferred/Not
    # Specified) by dimension
    ri = requirement_intensity_by_dimension(requirements)
    ri.table.to_csv(TABLES_DIR / "Table5_Requirement_Intensity_By_Dimension.csv")
    print("\nTable 5 (requirement intensity by dimension):")
    print(ri.table)

    # --- Table 6: D6 profile-vs-posting asymmetry
    d6a = d6_profile_vs_posting_asymmetry(
        profile_scores,
        dimension_evidence,
        requirements,
        "final_frozen",
        str(ANNOTATION_PATH),
    )
    d6_row = pd.Series(
        {
            "n_profiles_with_d6_evidence": d6a.n_profiles_with_d6_evidence,
            "n_profiles_total": d6a.n_profiles_total,
            "profile_side_coverage": d6a.profile_side_coverage,
            "n_requirements_d6_mappable": d6a.n_requirements_d6_mappable,
            "n_requirements_total": d6a.n_requirements_total,
            "posting_side_coverage": d6a.posting_side_coverage,
        }
    )
    d6_row.to_csv(TABLES_DIR / "Table6_D6_Profile_vs_Posting_Asymmetry.csv")
    print("\nTable 6 (D6 asymmetry):")
    print(d6_row)

    # --- Figure 1: requirement volume by dimension (incl. Not Directly Mapped)
    fig, ax = plt.subplots(figsize=(9, 5))
    rc.counts_by_dimension.sort_values(ascending=False).plot(
        kind="bar", ax=ax, color="#2b6cb0"
    )
    ax.set_title(f"RQ2: Requirement Volume by Dimension (n={rc.n_requirements})")
    ax.set_ylabel("n requirements")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure1_Requirement_Volume_By_Dimension.png", dpi=150)
    plt.close(fig)

    # --- Figure 2: supply vs demand, dual-axis (explicitly two different units)
    fig, ax1 = plt.subplots(figsize=(9, 5))
    dims = svd.table.index
    ax1.bar(
        dims,
        svd.table["n_requirements"],
        color="#2b6cb0",
        alpha=0.6,
        label="n requirements (demand)",
    )
    ax1.set_ylabel("n requirements (demand volume)", color="#2b6cb0")
    ax2 = ax1.twinx()
    ax2.plot(
        dims,
        svd.table["profile_mean_score"],
        color="#e53e3e",
        marker="o",
        label="mean held score (supply)",
    )
    ax2.set_ylabel("mean held score, 0-5 (supply level)", color="#e53e3e")
    ax1.set_title(
        "RQ2: Requirement Demand Volume vs. Profile Held Level\n"
        "(two different units -- not a subtracted gap)"
    )
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure2_Supply_vs_Demand.png", dpi=150)
    plt.close(fig)

    # --- Figure 3: requirement intensity stacked bar
    fig, ax = plt.subplots(figsize=(9, 5))
    ri.table.drop(index="NOT_DIRECTLY_MAPPED", errors="ignore").plot(
        kind="bar", stacked=True, ax=ax
    )
    ax.set_title(
        "RQ2: Requirement Intensity by Dimension (Mandatory/Preferred/Not Specified)"
    )
    ax.set_ylabel("n requirements")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure3_Requirement_Intensity.png", dpi=150)
    plt.close(fig)

    print(f"\nWrote tables to {TABLES_DIR}")
    print(f"Wrote figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
