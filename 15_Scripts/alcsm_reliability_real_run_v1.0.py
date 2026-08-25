"""Real inter-rater reliability run: primary researcher (RATER_A) vs.
the friend's independent second-rater scores (RATER_B), for the
75-profile double-coding subset.

Data-recovery note (documented, not silent): the friend's completed
scores were entered directly into `ALCSM_Reliability_Subset_75_v1.1.
xlsx`'s `Subset_Roster` sheet, into the six columns that were
originally headed `D{n}_Missing_Status` (intended to hold `present`/
`unavailable` text). Those columns now hold plain integer scores
(0-5) instead -- confirmed with the researcher this is genuinely the
friend's independent scoring, not corruption (see
`Reliability_Subset_Verification_v1.1.md` Part B).

Consequence: the friend's raw data has no way to represent
"unavailable" separately from an observed 0 (no blank cells, no
sentinel value -- every one of the 450 cells is a plain 0-5 integer).
To preserve the present-vs-unavailable distinction this project
requires (Part 5 of the prior session's brief; restated in this
session's Part C), this script infers the friend's unavailable cases
from the PRIMARY RESEARCHER's own Missing_Status for the same profile
x dimension cell, on the grounds that "unavailable" in this project's
rubric is a structural fact about the source profile (e.g. no
Professional_Experience section) rather than a subjective per-rater
judgment call -- and empirically, every one of the friend's "0"
entries for D1/D2/D4 coincides exactly (100%, no exceptions) with a
profile the primary researcher independently marked unavailable for
that same dimension (D1: 3/3, D2: 48/48, D4: 49/49). D3/D5/D6 have
zero Rater-A-unavailable cases in this subset, so no exclusion applies
to them.

This is a documented interpretive decision, not a fabrication: every
excluded cell is excluded because the *primary researcher's own,
independently recorded* Missing_Status says so, not because this
script invented a threshold. The residual limitation -- a case where
the friend privately felt a dimension was unobservable but wrote 0
anyway, without that coinciding with Rater A's own unavailable flag --
cannot be detected from this file and is stated as a limitation in
`Reliability_Report_v1.1.md`.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from alcsm.reliability.subset_workflow import run_subset_reliability_analysis

REPO_ROOT = Path(__file__).resolve().parents[1]
SUBSET_PATH = (
    REPO_ROOT
    / "07_Reliability"
    / "Double_Coding"
    / "ALCSM_Reliability_Subset_75_v1.1.xlsx"
)
OUTPUT_DIR = REPO_ROOT / "07_Reliability"
RESULTS_XLSX = OUTPUT_DIR / "Reliability_Results_v1.1.xlsx"
RESULTS_JSON = (
    OUTPUT_DIR / "_reliability_results_v1.1.json"
)  # intermediate, git-ignored

DIMENSIONS = ["D1", "D2", "D3", "D4", "D5", "D6"]


def load_rater_a_long_and_status(
    subset_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Primary researcher's scores for the 75-profile subset, from the
    `Existing_Scores_REFERENCE_ONLY` sheet (already verified, in the
    prior session, to match the frozen annotation workbook exactly for
    these 75 profiles). Returns (long observed-scores frame, wide
    Missing_Status frame indexed by Profile_ID)."""
    ref = pd.read_excel(subset_path, sheet_name="Existing_Scores_REFERENCE_ONLY")
    status = ref.set_index("Profile_ID")[[f"{d}_Missing_Status" for d in DIMENSIONS]]

    rows = []
    for d in DIMENSIONS:
        observed = ref[ref[f"{d}_Missing_Status"] == "present"]
        for _, row in observed.iterrows():
            rows.append((row["Profile_ID"], d, row[f"{d}_Final"]))
    long = pd.DataFrame(rows, columns=["Profile_ID", "Dimension", "Score"])
    return long, status


def load_friend_long_with_inferred_unavailable(
    subset_path: Path, rater_a_status: pd.DataFrame
) -> tuple[pd.DataFrame, list[tuple[str, str, int]]]:
    """Friend's (RATER_B) scores from `Subset_Roster`'s mislabeled
    `D{n}_Missing_Status` columns, excluding any cell where the
    PRIMARY RESEARCHER's own Missing_Status for that same profile x
    dimension is 'unavailable' (see module docstring for the full
    justification)."""
    roster = pd.read_excel(subset_path, sheet_name="Subset_Roster")
    rows = []
    excluded = []
    for _, row in roster.iterrows():
        pid = row["Profile_ID"]
        for d in DIMENSIONS:
            value = row[f"{d}_Missing_Status"]
            a_status = rater_a_status.loc[pid, f"{d}_Missing_Status"]
            if a_status == "unavailable":
                excluded.append((pid, d, value))
                continue
            rows.append((pid, d, value))
    long = pd.DataFrame(rows, columns=["Profile_ID", "Dimension", "Score"])
    return long, excluded


def main() -> None:
    primary_long, rater_a_status = load_rater_a_long_and_status(SUBSET_PATH)
    friend_long, excluded = load_friend_long_with_inferred_unavailable(
        SUBSET_PATH, rater_a_status
    )

    subset_profile_ids = set(rater_a_status.index)
    assert len(subset_profile_ids) == 75

    print(f"Primary (RATER_A) observed-score rows: {len(primary_long)}")
    print(
        f"Friend (RATER_B) observed-score rows (after inferred-unavailable exclusion): "
        f"{len(friend_long)}"
    )
    print(f"Cells excluded as inferred-unavailable for the friend: {len(excluded)}")
    for d in DIMENSIONS:
        n = sum(1 for _, dim, _ in excluded if dim == d)
        print(f"  {d}: {n} excluded")

    results = run_subset_reliability_analysis(
        primary_long,
        friend_long,
        subset_profile_ids,
        rulebook_version="v1.1",
        source_description=(
            "P6 double-coding subset (75/500, seed=20260824) -- RATER_A = "
            "primary researcher (frozen annotation), RATER_B = independent "
            "friend second-rater (recovered from Subset_Roster sheet, "
            "unavailable cells inferred from RATER_A's own Missing_Status)"
        ),
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for dim_number in sorted(results):
        s = results[dim_number]
        rows.append(
            {
                "Dimension": f"D{dim_number}",
                "n_units": s.n_units,
                "krippendorff_alpha_ordinal": s.krippendorff_alpha,
                "alpha_ci_lower": s.alpha_ci_lower,
                "alpha_ci_upper": s.alpha_ci_upper,
                "observed_agreement": s.percent_agreement,
                "exact_agreement": s.percent_agreement,
                "exact_agreement_count": s.exact_agreement_count,
                "score_variance_pooled": s.score_variance,
                "rater_a_variance": s.rater_a_variance,
                "rater_b_variance": s.rater_b_variance,
                "rater_a_n_categories": s.rater_a_n_categories,
                "rater_b_n_categories": s.rater_b_n_categories,
                "verdict": s.verdict,
                "rater_a_unavailable": s.primary_unavailable_count,
                "rater_b_unavailable_inferred": s.second_rater_unavailable_count,
                "both_unavailable": s.both_unavailable_count,
                "rater_a_distribution": json.dumps(s.primary_score_distribution),
                "rater_b_distribution": json.dumps(s.second_rater_score_distribution),
                "disagreement_magnitude_distribution": json.dumps(
                    s.disagreement_magnitude_distribution
                ),
            }
        )
    results_df = pd.DataFrame(rows)

    magnitude_rows = []
    for dim_number in sorted(results):
        s = results[dim_number]
        dist = s.disagreement_magnitude_distribution
        n_paired = sum(dist.values())
        n_one_apart = dist.get(1, 0)
        magnitude_rows.append(
            {
                "Dimension": f"D{dim_number}",
                **{f"{k}_point_disagreement": dist.get(k, 0) for k in range(6)},
                "n_paired": n_paired,
                "pct_exactly_one_apart": (
                    n_one_apart / n_paired if n_paired else float("nan")
                ),
            }
        )
    magnitude_df = pd.DataFrame(magnitude_rows)

    with pd.ExcelWriter(RESULTS_XLSX, engine="openpyxl") as writer:
        results_df.to_excel(writer, sheet_name="Per_Dimension_Reliability", index=False)
        magnitude_df.to_excel(writer, sheet_name="Disagreement_Magnitude", index=False)
        primary_long.to_excel(writer, sheet_name="Rater_A_Long", index=False)
        friend_long.to_excel(writer, sheet_name="Rater_B_Long", index=False)
        pd.DataFrame(
            excluded, columns=["Profile_ID", "Dimension", "Raw_Value"]
        ).to_excel(writer, sheet_name="Inferred_Unavailable_Exclusions", index=False)

    results_df.to_json(RESULTS_JSON, orient="records", indent=2)
    print(f"\nWrote {RESULTS_XLSX}")
    print(results_df.to_string(index=False))
    print("\nDisagreement magnitude by dimension:")
    print(magnitude_df.to_string(index=False))


if __name__ == "__main__":
    main()
