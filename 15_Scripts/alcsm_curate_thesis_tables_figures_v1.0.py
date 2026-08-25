"""Curates the final, manageable set of thesis-ready tables and
figures (Part 7 of the FINAL RESULTS CONSOLIDATION task) into
`13_Tables/` and `12_Figures/`, following those folders' own
established naming convention (`ALCSM_Tbl<Ch>.<N>_<Description>_v1.0`,
`ALCSM_Fig<Ch>.<N>_<Description>_v1.0`).

Deliberately curated, not exhaustive: copies only the strongest,
most-cited outputs from each RQ's already-produced tables/figures
(never recomputes a number), plus generates two new confusion-matrix
figures for RQ5 (D3 -- strongest NLP signal; D6 -- clearest below-
baseline failure) since none existed yet in image form. All source
numbers are read from the already-produced, already-verified RQ
outputs -- nothing here is a new statistic.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
TABLES_DIR = REPO_ROOT / "13_Tables"
FIGURES_DIR = REPO_ROOT / "12_Figures"

RQ1_TABLES = REPO_ROOT / "09_Statistical_Analysis" / "RQ1" / "Tables"
RQ1_FIGURES = REPO_ROOT / "09_Statistical_Analysis" / "RQ1" / "Figures"
RQ2_TABLES = REPO_ROOT / "09_Statistical_Analysis" / "RQ2" / "Tables"
RQ2_FIGURES = REPO_ROOT / "09_Statistical_Analysis" / "RQ2" / "Figures"
RQ3_RELIABILITY_TABLE = (
    REPO_ROOT / "09_Statistical_Analysis" / "RQ3" / "Table_Reliability_v1.0.xlsx"
)
SURVEY_RESULTS = (
    REPO_ROOT
    / "07_Reliability"
    / "Survey_Analysis"
    / "ALCSM_Survey_Analysis_Processed_v1.0.xlsx"
)
NLP_RESULTS = REPO_ROOT / "08_NLP_Development" / "NLP_Baseline_Results_v1.0.xlsx"


def copy_table(src: Path, dest_name: str) -> None:
    dest = TABLES_DIR / dest_name
    shutil.copy(src, dest)
    print(f"Table: {dest.name}")


def copy_figure(src: Path, dest_name: str) -> None:
    dest = FIGURES_DIR / dest_name
    shutil.copy(src, dest)
    print(f"Figure: {dest.name}")


def build_nlp_performance_table() -> None:
    """Only the aggregate `Per_Dimension_Metrics` sheet -- the full
    `NLP_Baseline_Results_v1.0.xlsx` also has `Predictions` and
    `Train_Test_Splits` sheets carrying individual profile IDs, which
    must not land in `13_Tables/` (a tracked, non-git-ignored folder;
    the source workbook itself stays git-ignored for exactly this
    reason)."""
    metrics = pd.read_excel(NLP_RESULTS, sheet_name="Per_Dimension_Metrics")
    dest = TABLES_DIR / "ALCSM_Tbl4.9_RQ5_NLPPerformance_v1.0.csv"
    metrics.to_csv(dest, index=False)
    print(f"Table: {dest.name}")


def build_survey_summary_table() -> None:
    relevance = pd.read_excel(SURVEY_RESULTS, sheet_name="Relevance")
    appropriateness = pd.read_excel(
        SURVEY_RESULTS, sheet_name="Overall_Appropriateness"
    )
    most_important = pd.read_excel(
        SURVEY_RESULTS, sheet_name="Most_Important_Dimension"
    )
    dest = TABLES_DIR / "ALCSM_Tbl4.8_ExpertSurveySummary_v1.0.xlsx"
    with pd.ExcelWriter(dest, engine="openpyxl") as writer:
        relevance.to_excel(writer, sheet_name="Relevance_By_Dimension", index=False)
        appropriateness.to_excel(
            writer, sheet_name="Overall_Appropriateness", index=False
        )
        most_important.to_excel(
            writer, sheet_name="Most_Important_Dimension", index=False
        )
    print(f"Table: {dest.name}")


def build_confusion_figure(dimension_label: str, dest_name: str, subtitle: str) -> None:
    matrix = pd.read_excel(
        NLP_RESULTS, sheet_name=f"Confusion_{dimension_label}", index_col=0
    )
    fig, ax = plt.subplots(figsize=(5.5, 5))
    im = ax.imshow(matrix.values, cmap="Blues")
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_yticks(range(len(matrix.index)))
    ax.set_xticklabels(matrix.columns)
    ax.set_yticklabels(matrix.index)
    ax.set_xlabel("Predicted score")
    ax.set_ylabel("Gold (human) score")
    ax.set_title(f"RQ5: {dimension_label} Confusion Matrix\n{subtitle}", fontsize=10)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix.values[i, j]
            color = "white" if value > matrix.values.max() / 2 else "black"
            ax.text(j, i, str(value), ha="center", va="center", color=color, fontsize=8)
    fig.colorbar(im, ax=ax, label="n profiles")
    fig.tight_layout()
    dest = FIGURES_DIR / dest_name
    fig.savefig(dest, dpi=150)
    plt.close(fig)
    print(f"Figure: {dest.name}")


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # --- RQ1: 3 tables, 2 figures
    copy_table(
        RQ1_TABLES / "Table1_Dimension_Score_Distribution.csv",
        "ALCSM_Tbl4.1_RQ1_DimensionScoreDistribution_v1.0.csv",
    )
    copy_table(
        RQ1_TABLES / "Table2_Missingness_By_Dimension.csv",
        "ALCSM_Tbl4.2_RQ1_MissingnessByDimension_v1.0.csv",
    )
    copy_table(
        RQ1_TABLES / "Table5_Mean_Dimension_By_Title_Category.csv",
        "ALCSM_Tbl4.3_RQ1_MeanScoreByTitleCategory_v1.0.csv",
    )
    copy_figure(
        RQ1_FIGURES / "Figure1_Dimension_Score_Distributions.png",
        "ALCSM_Fig4.1_RQ1_DimensionScoreDistributions_v1.0.png",
    )
    copy_figure(
        RQ1_FIGURES / "Figure2_Missingness_By_Dimension.png",
        "ALCSM_Fig4.2_RQ1_MissingnessByDimension_v1.0.png",
    )

    # --- RQ2: 3 tables, 2 figures
    copy_table(
        RQ2_TABLES / "Table1_Requirement_Counts_By_Dimension.csv",
        "ALCSM_Tbl4.4_RQ2_RequirementCountsByDimension_v1.0.csv",
    )
    copy_table(
        RQ2_TABLES / "Table4_Supply_vs_Demand_Frequency.csv",
        "ALCSM_Tbl4.5_RQ2_SupplyVsDemandFrequency_v1.0.csv",
    )
    copy_table(
        RQ2_TABLES / "Table6_D6_Profile_vs_Posting_Asymmetry.csv",
        "ALCSM_Tbl4.6_RQ2_D6ProfileVsPostingAsymmetry_v1.0.csv",
    )
    copy_figure(
        RQ2_FIGURES / "Figure1_Requirement_Volume_By_Dimension.png",
        "ALCSM_Fig4.3_RQ2_RequirementVolumeByDimension_v1.0.png",
    )
    copy_figure(
        RQ2_FIGURES / "Figure2_Supply_vs_Demand.png",
        "ALCSM_Fig4.4_RQ2_SupplyVsDemand_v1.0.png",
    )

    # --- RQ3: 1 reliability table, 1 survey table
    copy_table(RQ3_RELIABILITY_TABLE, "ALCSM_Tbl4.7_RQ3_Reliability_v1.0.xlsx")
    build_survey_summary_table()

    # --- RQ5: 1 performance table, 2 confusion-matrix figures
    build_nlp_performance_table()
    build_confusion_figure(
        "D3",
        "ALCSM_Fig4.5_RQ5_ConfusionMatrix_D3_v1.0.png",
        "Strongest genuine NLP signal (52.0% exact, kappa=.399)",
    )
    build_confusion_figure(
        "D6",
        "ALCSM_Fig4.6_RQ5_ConfusionMatrix_D6_v1.0.png",
        "Below majority baseline (44.0% exact, kappa=.238)",
    )

    print("\nCuration complete: 9 tables, 6 figures (RQ4: none -- no results to show).")


if __name__ == "__main__":
    main()
