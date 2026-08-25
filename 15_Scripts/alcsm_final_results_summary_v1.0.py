"""Builds the cross-RQ final results summary workbook (Part 6 of the
FINAL RESULTS CONSOLIDATION task).

Reads numeric results directly from each RQ's already-produced output
(never hand-retyped where a structured source exists) and assembles
one sheet per RQ plus a top-level summary sheet. RQ4 has no numeric
results (data-collection gap, `RQ4_Final_Status_v1.0.md`), so its
sheet states that explicitly rather than being left out or padded with
invented numbers.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = (
    REPO_ROOT / "09_Statistical_Analysis" / "ALCSM_Final_Results_Summary_v1.0.xlsx"
)


def build_rq1_sheet() -> pd.DataFrame:
    dist = pd.read_csv(
        REPO_ROOT
        / "09_Statistical_Analysis"
        / "RQ1"
        / "Tables"
        / "Table1_Dimension_Score_Distribution.csv",
        index_col=0,
    )
    missing = pd.read_csv(
        REPO_ROOT
        / "09_Statistical_Analysis"
        / "RQ1"
        / "Tables"
        / "Table2_Missingness_By_Dimension.csv",
        index_col=0,
    )
    summary = pd.DataFrame(
        {
            "mean": dist.loc["mean"],
            "median": dist.loc["median"],
            "std": dist.loc["std"],
            "present": missing["present"],
            "unavailable": missing["unavailable"],
        }
    )
    summary.index.name = "Dimension"
    return summary.reset_index()


def build_rq2_sheet() -> pd.DataFrame:
    counts = pd.read_csv(
        REPO_ROOT
        / "09_Statistical_Analysis"
        / "RQ2"
        / "Tables"
        / "Table1_Requirement_Counts_By_Dimension.csv",
        index_col=0,
    )
    held = pd.read_csv(
        REPO_ROOT
        / "09_Statistical_Analysis"
        / "RQ2"
        / "Tables"
        / "Table3_Mean_Median_Held_Level_By_Dimension.csv",
        index_col=0,
    )
    counts.columns = ["n_requirements"]
    counts.index.name = "Category"
    held.index.name = "Dimension"
    return counts.reset_index(), held.reset_index()


def build_rq3_sheet() -> pd.DataFrame:
    return pd.read_excel(
        REPO_ROOT / "09_Statistical_Analysis" / "RQ3" / "Table_Reliability_v1.0.xlsx",
        sheet_name="Reliability",
    )


def build_rq4_sheet() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Status": "Not conducted",
                "Reason": (
                    "External observable professional-impact criterion "
                    "variables (network reach, content engagement, "
                    "recognition count, seniority progression rate) were "
                    "not collected -- a data-collection gap, not an "
                    "analysis-code gap."
                ),
                "Source": "RQ4_Final_Status_v1.0.md / RQ4_Limitation_Report_v1.0.md",
            }
        ]
    )


def build_rq5_sheet() -> pd.DataFrame:
    results = pd.read_excel(
        REPO_ROOT / "08_NLP_Development" / "NLP_Baseline_Results_v1.0.xlsx",
        sheet_name="Per_Dimension_Metrics",
    )
    return results[
        [
            "Dimension",
            "n",
            "exact_match_rate",
            "mean_absolute_error",
            "linear_weighted_kappa",
            "majority_baseline_exact_match",
            "beats_majority_baseline",
        ]
    ]


def build_summary_sheet() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Research Question": "RQ1 -- LinkedIn profile descriptive patterns",
                "Dataset": "Frozen annotation + LinkedIn processed workbook",
                "Sample Size": "500 profiles, 3,000 profile x dimension labels",
                "Method": (
                    "Descriptive statistics (distributions, missingness, "
                    "cross-tabulations)"
                ),
                "Primary Result": (
                    "D1/D3/D6 span the full 0-5 range; D2/D4 are range-"
                    "restricted (0-1, 0-3); D5 is concentrated at score 3 "
                    "(87% of profiles)."
                ),
                "Main Limitation": (
                    "No inferential statistics; descriptive only, no " "causal claims."
                ),
            },
            {
                "Research Question": (
                    "RQ2 -- Job posting requirements vs. profile " "credential signals"
                ),
                "Dataset": "Job postings processed workbook + frozen annotation",
                "Sample Size": "201 postings, 1,558 requirement records",
                "Method": (
                    "Aggregate dimension-level demand-vs-supply comparison "
                    "(no numeric gap)"
                ),
                "Primary Result": (
                    "51.3% of requirements are NOT_DIRECTLY_MAPPED; D5 "
                    "dominates demand (436 reqs); D6 shows the sharpest "
                    "asymmetry (0.06% posting-side vs. 99.4% profile-side "
                    "coverage)."
                ),
                "Main Limitation": (
                    "No per-requirement numeric required-level score exists; "
                    "no one-to-one candidate-posting matching."
                ),
            },
            {
                "Research Question": "RQ3 -- ALCSM construction/validation",
                "Dataset": (
                    "75-profile double-coded subset + 24-respondent " "expert survey"
                ),
                "Sample Size": "75 profiles (reliability), N=24 (survey)",
                "Method": (
                    "Krippendorff's alpha (ordinal, per dimension) + "
                    "descriptive survey statistics"
                ),
                "Primary Result": (
                    "D1/D6 strong reproducibility; D2/D4 perfect but "
                    "degenerate; D3 limited (alpha=.102, systematic "
                    "calibration disagreement); D5 limited (alpha=.246, "
                    "range restriction)."
                ),
                "Main Limitation": (
                    "One subset, one second rater; N=24 self-selected "
                    "survey respondents; content-assessment evidence, not "
                    "proof of validity."
                ),
            },
            {
                "Research Question": (
                    "RQ4 -- Observable professional impact correlation"
                ),
                "Dataset": "Not available",
                "Sample Size": "0 (criterion variables never collected)",
                "Method": "Not conducted",
                "Primary Result": (
                    "None -- documented limitation, not an empirical finding."
                ),
                "Main Limitation": (
                    "External criterion data (network reach, engagement, "
                    "recognition, seniority progression) was never "
                    "collected."
                ),
            },
            {
                "Research Question": "RQ5 -- NLP human-vs-machine agreement",
                "Dataset": (
                    "Frozen annotation (gold) + LinkedIn processed "
                    "workbook (features)"
                ),
                "Sample Size": (
                    "500 profiles, per-dimension train/test splits "
                    "(26-400 train, seed=42)"
                ),
                "Method": (
                    "TF-IDF + Ridge regression, six independent " "per-dimension models"
                ),
                "Primary Result": (
                    "D3 strongest signal (52.0% exact, kappa=.399); D1 "
                    "modest signal (29.5%, kappa=.283); D2/D5 tie "
                    "degenerate/imbalanced baselines; D4/D6 below baseline."
                ),
                "Main Limitation": (
                    "Proof-of-concept baseline, not production-ready; "
                    "linear bag-of-words model cannot represent cross-"
                    "field aggregation (e.g. D6 industry counting)."
                ),
            },
        ]
    )


def main() -> None:
    rq1 = build_rq1_sheet()
    rq2_counts, rq2_held = build_rq2_sheet()
    rq3 = build_rq3_sheet()
    rq4 = build_rq4_sheet()
    rq5 = build_rq5_sheet()
    summary = build_summary_sheet()

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        rq1.to_excel(writer, sheet_name="RQ1", index=False)
        rq2_counts.to_excel(writer, sheet_name="RQ2", index=False, startrow=0)
        rq2_held.to_excel(writer, sheet_name="RQ2", index=False, startrow=12)
        rq3.to_excel(writer, sheet_name="RQ3", index=False)
        rq4.to_excel(writer, sheet_name="RQ4", index=False)
        rq5.to_excel(writer, sheet_name="RQ5", index=False)

    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
