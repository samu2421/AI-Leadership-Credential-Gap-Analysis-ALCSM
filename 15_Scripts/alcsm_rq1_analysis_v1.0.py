"""RQ1 descriptive analysis: what credential patterns exist among AI
leaders, as observed in the 500-profile frozen annotation?

Reuses `alcsm.analysis.rq1_descriptive` unchanged except for one
labeling fix (D6's display label now reads from the frozen v1.1
dimension config instead of the retired v1.0 constant -- a cosmetic
fix, not a change to D6's definition or criteria). Purely descriptive:
no composite score, no weights, no inferential statistic anywhere in
this script or the module it calls.

Reads directly from the canonical Excel workbooks; never writes to
either. Outputs tables (CSV, thesis-ready) and figures (PNG) under
`09_Statistical_Analysis/RQ1/`.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from alcsm.analysis.rq1_descriptive import (
    demographic_summary,
    dimension_distribution,
    dimension_level_comparison,
    dimension_missingness,
    industry_patterns,
    title_category_patterns,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
LINKEDIN_PATH = (
    REPO_ROOT
    / "05_Data_Collection"
    / "LinkedIn_Profiles"
    / "02_Processed"
    / "ALCSM_LinkedIn_Processed_v1.1.xlsx"
)
OUTPUT_DIR = REPO_ROOT / "09_Statistical_Analysis" / "RQ1"
TABLES_DIR = OUTPUT_DIR / "Tables"
FIGURES_DIR = OUTPUT_DIR / "Figures"

DIM_LABELS = {
    1: "D1 Formal Education",
    2: "D2 Certifications",
    3: "D3 Practical AI Experience",
    4: "D4 Technical Contributions",
    5: "D5 Leadership & Strategic Resp.",
    6: "D6 AI Industry/Application Breadth",
}


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    profile_scores = pd.read_excel(ANNOTATION_PATH, sheet_name="Profile_Scores")
    dimension_evidence = pd.read_excel(ANNOTATION_PATH, sheet_name="Dimension_Evidence")
    profile_master = pd.read_excel(LINKEDIN_PATH, sheet_name="Profile_Master")

    # --- Table 1: per-dimension score distribution (0-5 counts, mean, median, std)
    dd = dimension_distribution(profile_scores, "final_frozen", str(ANNOTATION_PATH))
    dist_table = dd.counts.copy()
    dist_table.loc["mean"] = dd.means
    dist_table.loc["median"] = dd.medians
    dist_table.loc["std"] = dd.std_devs
    dist_table.to_csv(TABLES_DIR / "Table1_Dimension_Score_Distribution.csv")
    print("Table 1 (dimension score distribution):")
    print(dist_table)

    # --- Table 2: missingness by dimension
    mr = dimension_missingness(dimension_evidence, "final_frozen", str(ANNOTATION_PATH))
    mr.by_dimension.to_csv(TABLES_DIR / "Table2_Missingness_By_Dimension.csv")
    print("\nTable 2 (missingness by dimension):")
    print(mr.by_dimension)

    # --- Table 3: dimension-level comparison (side by side, not combined)
    dc = dimension_level_comparison(
        profile_scores, dimension_evidence, "final_frozen", str(ANNOTATION_PATH)
    )
    dc.table.to_csv(TABLES_DIR / "Table3_Dimension_Level_Comparison.csv")
    print("\nTable 3 (dimension-level comparison):")
    print(dc.table)

    # --- Table 4: demographic summary
    ds = demographic_summary(profile_master)
    for name, series in [
        ("Country", ds.country_counts),
        ("Federal_State", ds.federal_state_counts),
        ("Company_Size", ds.company_size_counts),
        ("Industry", ds.industry_counts),
        ("Title_Category", ds.title_category_counts),
    ]:
        series.to_csv(TABLES_DIR / f"Table4_Demographics_{name}.csv")
    print(f"\nTable 4 (demographics, n={ds.n_profiles}): 5 CSVs written")

    # --- Table 5/6/7: substantively justified cross-tabulations
    # Title_Category: does formal seniority track with credential signals?
    tp = title_category_patterns(
        profile_master, profile_scores, "final_frozen", str(ANNOTATION_PATH)
    )
    tp.means.to_csv(TABLES_DIR / "Table5_Mean_Dimension_By_Title_Category.csv")
    print("\nTable 5 (mean D1-D6 by Title_Category):")
    print(tp.means)

    # Industry: does D6 (AI industry breadth) vary by the profile's own
    # current-employer industry -- a substantively justified check since
    # D6 is specifically about industry breadth.
    ip = industry_patterns(
        profile_master, profile_scores, "final_frozen", str(ANNOTATION_PATH)
    )
    ip.means.to_csv(TABLES_DIR / "Table6_Mean_Dimension_By_Industry.csv")
    print(
        "\nTable 6 (mean D1-D6 by Industry) written, "
        f"{len(ip.means)} industry levels"
    )

    # --- Figure 1: D1-D6 score distributions (small multiples)
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    for i, d in enumerate([1, 2, 3, 4, 5, 6]):
        ax = axes[i // 3][i % 3]
        col = f"D{d}"
        counts = dd.counts[col].reindex(range(6), fill_value=0)
        ax.bar(counts.index, counts.values, color="#2b6cb0")
        ax.set_title(DIM_LABELS[d], fontsize=9)
        ax.set_xlabel("Score")
        ax.set_ylabel("n profiles")
        ax.set_xticks(range(6))
    fig.suptitle(
        "RQ1: ALCSM v1.1 Dimension Score Distributions (n=500 profiles)",
        fontsize=12,
    )
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure1_Dimension_Score_Distributions.png", dpi=150)
    plt.close(fig)

    # --- Figure 2: missingness by dimension (stacked bar)
    fig, ax = plt.subplots(figsize=(8, 5))
    mr.by_dimension.plot(kind="bar", stacked=True, ax=ax, color=["#2b6cb0", "#e53e3e"])
    ax.set_title("RQ1: Missingness by Dimension (n=500 profiles)")
    ax.set_ylabel("n profiles")
    ax.set_xlabel("Dimension")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure2_Missingness_By_Dimension.png", dpi=150)
    plt.close(fig)

    # --- Figure 3: mean dimension score by Title_Category (top 8 by n)
    top_titles = tp.n_per_group.sort_values(ascending=False).head(8).index
    fig, ax = plt.subplots(figsize=(10, 5))
    tp.means.loc[top_titles].plot(kind="bar", ax=ax)
    ax.set_title(
        "RQ1: Mean Dimension Score by Title Category (top 8 by n, descriptive only)"
    )
    ax.set_ylabel("Mean score")
    ax.legend(loc="upper right", fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "Figure3_Mean_Score_By_Title_Category.png", dpi=150)
    plt.close(fig)

    print(f"\nWrote tables to {TABLES_DIR}")
    print(f"Wrote figures to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
