"""D3/D5 profile-level disagreement analysis (Part 3 of the FINAL
RELIABILITY DIAGNOSIS task).

Builds a row-per-(profile, dimension) table for D3 and D5 specifically
-- the two dimensions with low Krippendorff's alpha -- showing both
raters' scores, the disagreement magnitude and direction, the primary
researcher's evidence text (Rater A only -- the friend's raw file
carries no evidence text, so Evidence_B is honestly reported as not
recorded, never fabricated), and review-history context where the
researcher's own score was itself revised from an AI-assisted first
pass.

No direct identifiers: only Profile_ID (already the project's
standard pseudonymous key throughout) and evidence text drawn from
`Dimension_Evidence.Evidence`, which contains only structured feature
summaries (job titles, durations, boolean flags) -- the same field
already verified elsewhere in this project to contain zero email/URL
patterns.

Reuses `alcsm.reliability.subset_workflow`'s loaders unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from alcsm.reliability.subset_workflow import load_primary_scores_long

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
SUBSET_PATH = (
    REPO_ROOT
    / "07_Reliability"
    / "Double_Coding"
    / "ALCSM_Reliability_Subset_75_v1.1.xlsx"
)
OUTPUT_PATH = REPO_ROOT / "07_Reliability" / "D3_D5_Disagreement_Analysis_v1.0.xlsx"

TARGET_DIMENSIONS = ["D3", "D5"]


def load_second_rater_scores_long_from_roster(subset_path: Path) -> pd.DataFrame:
    """Friend's (RATER_B) scores for D3/D5 specifically -- these two
    dimensions have zero Rater-A-unavailable cases in this subset
    (`Reliability_Subset_Verification_v1.2.md`), so no unavailable-
    inference exclusion is needed or applied for them; every one of
    the 75 profiles' D3/D5 raw values is used as-is."""
    roster = pd.read_excel(subset_path, sheet_name="Subset_Roster")
    dims = ["D1", "D2", "D3", "D4", "D5", "D6"]
    long = roster.melt(
        id_vars="Profile_ID",
        value_vars=[f"{d}_Missing_Status" for d in dims],
        var_name="Dimension",
        value_name="Score",
    )
    long["Dimension"] = long["Dimension"].str.replace(
        "_Missing_Status", "", regex=False
    )
    return long


def main() -> None:
    roster = pd.read_excel(SUBSET_PATH, sheet_name="Subset_Roster")
    subset_profile_ids = set(roster["Profile_ID"])
    assert len(subset_profile_ids) == 75

    primary_long = load_primary_scores_long(ANNOTATION_PATH, subset_profile_ids)
    friend_long = load_second_rater_scores_long_from_roster(SUBSET_PATH)

    dimension_evidence = pd.read_excel(ANNOTATION_PATH, sheet_name="Dimension_Evidence")
    review_changes = pd.read_excel(ANNOTATION_PATH, sheet_name="Review_Changes")

    rows = []
    for dim in TARGET_DIMENSIONS:
        a = primary_long[primary_long["Dimension"] == dim].set_index("Profile_ID")[
            "Score"
        ]
        b = friend_long[friend_long["Dimension"] == dim].set_index("Profile_ID")[
            "Score"
        ]
        paired_ids = sorted(set(a.index) & set(b.index))
        for pid in paired_ids:
            score_a = int(a.loc[pid])
            score_b = int(b.loc[pid])
            abs_disagreement = abs(score_a - score_b)
            if score_a == score_b:
                direction = "Agree"
            elif score_b > score_a:
                direction = "Rater_B_Higher"
            else:
                direction = "Rater_A_Higher"

            ev_row = dimension_evidence[
                (dimension_evidence["Profile_ID"] == pid)
                & (dimension_evidence["Dimension"] == dim)
            ]
            evidence_a = (
                ev_row["Evidence"].iloc[0]
                if len(ev_row) and pd.notna(ev_row["Evidence"].iloc[0])
                else None
            )

            rc_row = review_changes[
                (review_changes["Profile_ID"] == pid)
                & (review_changes["Dimension"] == dim)
            ]
            if len(rc_row):
                r = rc_row.iloc[0]
                review_context = (
                    f"REVIEWED: FirstPass={r['FirstPass_Score']}, "
                    f"Final={r['Final_Score']}, Decision={r['Decision']}"
                )
            else:
                review_context = (
                    "CARRIED_FORWARD (no first-pass score change on record)"
                )

            rows.append(
                {
                    "Profile_ID": pid,
                    "Dimension": dim,
                    "Rater_A": score_a,
                    "Rater_B": score_b,
                    "Absolute_Disagreement": abs_disagreement,
                    "Direction": direction,
                    "Evidence_A": evidence_a if evidence_a else "NOT AVAILABLE",
                    "Evidence_B": (
                        "NOT RECORDED (friend's raw file has no evidence text field)"
                    ),
                    "FirstPass_Final_Context": review_context,
                }
            )

    disagreement_table = pd.DataFrame(rows)

    magnitude_summary = []
    for dim in TARGET_DIMENSIONS:
        dim_rows = disagreement_table[disagreement_table["Dimension"] == dim]
        n = len(dim_rows)
        counts = (
            dim_rows["Absolute_Disagreement"]
            .value_counts()
            .reindex(range(6), fill_value=0)
        )
        one_apart_pct = counts.get(1, 0) / n if n else float("nan")
        magnitude_summary.append(
            {
                "Dimension": dim,
                **{f"{k}_point_disagreement": int(counts.get(k, 0)) for k in range(6)},
                "n_paired": n,
                "pct_exactly_one_apart": one_apart_pct,
            }
        )
    magnitude_df = pd.DataFrame(magnitude_summary)

    with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
        disagreement_table.to_excel(
            writer, sheet_name="Profile_Level_Disagreement", index=False
        )
        magnitude_df.to_excel(writer, sheet_name="Magnitude_Summary", index=False)

    print(f"Wrote {OUTPUT_PATH}")
    print(
        f"\n{len(disagreement_table)} profile x dimension rows "
        f"({len(disagreement_table[disagreement_table.Dimension=='D3'])} D3, "
        f"{len(disagreement_table[disagreement_table.Dimension=='D5'])} D5)"
    )
    print("\nMagnitude summary:")
    print(magnitude_df.to_string(index=False))


if __name__ == "__main__":
    main()
