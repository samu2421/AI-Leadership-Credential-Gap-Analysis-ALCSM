"""Build the P6 double-coding reliability subset (Part 2 of the
FINAL VALIDATION AND ANALYSIS STAGE task).

Selects a reproducible 15% (75-profile) random subset of the 500 frozen
profiles using the existing, already-tested selection mechanism
(``alcsm.annotation.pilot.select_pilot_subset``), then writes three
outputs under ``07_Reliability/Double_Coding/``:

- ``ALCSM_Reliability_Subset_75_v1.1.xlsx`` -- the selected roster plus
  the existing (frozen, primary-researcher / "Rater A") scores for
  those 75 profiles, kept on a separate reference sheet.
- ``Rater_A_Blank_Template.xlsx`` -- a blank double-coding template
  (Profile_ID, D1-D6, plus a status column per dimension so a rater can
  record "unavailable" rather than a false zero -- see Part 5 rule).
  Contains no scores. Reused as-is (duplicated/renamed) for any second
  coder.
- Selection metadata is also embedded in the roster workbook so the
  selection is independently reproducible without re-running this
  script.

This script never invents or fills in any second-rater score. It only
prepares the empty structure and selects which existing profiles the
double coding applies to.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from alcsm.annotation.pilot import select_pilot_subset

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
OUTPUT_DIR = REPO_ROOT / "07_Reliability" / "Double_Coding"

# Fixed, pre-registered seed. Chosen prospectively (the date this
# reliability package was prepared) and never tuned or resampled.
SEED = 20260824
FRACTION = 0.15

KNOWN_DATA_INTEGRITY_PROFILES = {"LP0041", "LP0170", "LP0182"}
DIMENSIONS = ["D1", "D2", "D3", "D4", "D5", "D6"]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    source_sha256 = _sha256(ANNOTATION_PATH)
    profile_scores = pd.read_excel(ANNOTATION_PATH, sheet_name="Profile_Scores")
    candidate_ids = profile_scores["Profile_ID"].tolist()
    assert (
        len(candidate_ids) == len(set(candidate_ids)) == 500
    ), "candidate pool must be exactly the 500 unique frozen profiles"

    selection = select_pilot_subset(
        candidate_profile_ids=candidate_ids,
        method="random_subset",
        seed=SEED,
        fraction=FRACTION,
    )
    assert selection.candidate_pool_size == 500
    assert len(selection.selected_profile_ids) == 75, (
        f"expected exactly 75 selected profiles, got "
        f"{len(selection.selected_profile_ids)}"
    )
    assert len(set(selection.selected_profile_ids)) == 75, "no duplicate IDs"

    selected_set = set(selection.selected_profile_ids)
    integrity_in_subset = sorted(KNOWN_DATA_INTEGRITY_PROFILES & selected_set)

    # Preserve the frozen file's row order (not the RNG's internal
    # sample order) so the roster reads the same way the source data
    # does.
    subset_rows = profile_scores[
        profile_scores["Profile_ID"].isin(selected_set)
    ].reset_index(drop=True)
    assert len(subset_rows) == 75

    roster_cols = ["Profile_ID"] + [f"{d}_Missing_Status" for d in DIMENSIONS]
    roster = subset_rows[roster_cols].copy()
    roster["In_Data_Integrity_Register"] = roster["Profile_ID"].isin(
        KNOWN_DATA_INTEGRITY_PROFILES
    )

    reference_cols = (
        ["Profile_ID"]
        + [f"{d}_Final" for d in DIMENSIONS]
        + [f"{d}_Missing_Status" for d in DIMENSIONS]
        + ["Overall_Review_Status", "Researcher_Confidence"]
    )
    reference = subset_rows[reference_cols].copy()

    metadata = pd.DataFrame(
        [
            {"Field": "Selection method", "Value": selection.method},
            {"Field": "Random seed", "Value": selection.seed},
            {"Field": "Fraction requested", "Value": selection.fraction},
            {"Field": "Candidate pool size", "Value": selection.candidate_pool_size},
            {
                "Field": "Profiles selected",
                "Value": len(selection.selected_profile_ids),
            },
            {
                "Field": "Actual fraction achieved",
                "Value": round(selection.actual_fraction, 4),
            },
            {
                "Field": "Selected at (UTC-naive, local run time)",
                "Value": str(selection.selected_at),
            },
            {
                "Field": "Selection mechanism",
                "Value": "alcsm.annotation.pilot.select_pilot_subset",
            },
            {
                "Field": "Candidate order source",
                "Value": (
                    "Profile_Scores sheet row order, "
                    "ALCSM_Final_Human_Annotation_v1.1.xlsx"
                ),
            },
            {"Field": "Source file SHA-256", "Value": source_sha256},
            {
                "Field": "Data-integrity-flagged profiles selected",
                "Value": (
                    ", ".join(integrity_in_subset) if integrity_in_subset else "none"
                ),
            },
            {
                "Field": "Reproduction note",
                "Value": (
                    "random.Random(20260824).sample(pool, k=75) against the 500 "
                    "Profile_IDs in Profile_Scores row order reproduces this exact "
                    "selection deterministically."
                ),
            },
        ]
    )

    roster_path = OUTPUT_DIR / "ALCSM_Reliability_Subset_75_v1.1.xlsx"
    with pd.ExcelWriter(roster_path, engine="openpyxl") as writer:
        roster.to_excel(writer, sheet_name="Subset_Roster", index=False)
        reference.to_excel(
            writer, sheet_name="Existing_Scores_REFERENCE_ONLY", index=False
        )
        metadata.to_excel(writer, sheet_name="Selection_Metadata", index=False)

    # Blank double-coding template: exactly the seven columns the task
    # specifies (Profile_ID, D1-D6). No scores are pre-filled. An empty
    # cell means "unavailable / no observable evidence"; a written 0-5
    # means an observed score -- this convention preserves the
    # unavailable-vs-observed-zero distinction (Part 5) without adding
    # columns beyond the specified seven. The convention is documented
    # in Second_Rater_Annotation_Instructions_v1.1.md and relied on by
    # the Part 4 reliability adapter.
    blank_cols = {"Profile_ID": subset_rows["Profile_ID"].tolist()}
    for d in DIMENSIONS:
        blank_cols[d] = [None] * len(subset_rows)
    blank = pd.DataFrame(blank_cols)

    blank_path = OUTPUT_DIR / "Rater_A_Blank_Template.xlsx"
    blank.to_excel(blank_path, sheet_name="Independent_Coding", index=False)

    n_selected = len(selection.selected_profile_ids)
    print(f"Selected {n_selected} / {selection.candidate_pool_size} profiles")
    print(f"Actual fraction: {selection.actual_fraction:.4f}")
    print(f"Data-integrity-flagged profiles in subset: {integrity_in_subset or 'none'}")
    print(f"Wrote {roster_path}")
    print(f"Wrote {blank_path}")


if __name__ == "__main__":
    main()
