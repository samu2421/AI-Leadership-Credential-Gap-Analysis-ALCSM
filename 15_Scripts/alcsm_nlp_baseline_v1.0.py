"""Runs the minimal TF-IDF + Ridge NLP baseline (Part 2 of the FINAL
NLP IMPLEMENTATION task) against the real, frozen gold standard and
processed LinkedIn data, and writes the results workbook.

Six independent per-dimension models (never a composite/pooled
score), each trained and evaluated on its own reproducible,
leakage-safe train/test split (`alcsm.nlp.baseline`), then scored with
the existing, already-tested `alcsm.nlp.evaluate` module (exact-match
rate, MAE, linear-weighted Cohen's kappa, confusion matrices, largest
errors) -- none of that evaluation logic is reimplemented here.

Also computes each dimension's majority-class baseline (always predict
the most common training-set score) for direct comparison -- required
reading for D5 in particular, whose training set is dominated by a
single score.

Local-only: `scikit-learn` TF-IDF + Ridge, no network call, no
external API, ever.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from alcsm.constants import DIMENSIONS
from alcsm.nlp.baseline import (
    RANDOM_SEED,
    build_profile_documents,
    fit_predict_dimension,
)
from alcsm.nlp.evaluate import error_analysis, evaluate_predictions

REPO_ROOT = Path(__file__).resolve().parents[1]
ANNOTATION_PATH = REPO_ROOT / "06_Annotation" / "ALCSM_Final_Human_Annotation_v1.1.xlsx"
LINKEDIN_PATH = (
    REPO_ROOT
    / "05_Data_Collection"
    / "LinkedIn_Profiles"
    / "02_Processed"
    / "ALCSM_LinkedIn_Processed_v1.1.xlsx"
)
OUTPUT_DIR = REPO_ROOT / "08_NLP_Development"
RESULTS_XLSX = OUTPUT_DIR / "NLP_Baseline_Results_v1.0.xlsx"


def majority_class_baseline(train_labels: pd.Series, test_labels: pd.Series) -> dict:
    """Always predict the training set's most common score. The floor
    any real model must clear to be worth reporting -- especially for
    a dimension like D5 where one score dominates the population."""
    majority_value = int(train_labels.mode().iloc[0])
    predicted = pd.Series(majority_value, index=test_labels.index)
    exact_match = float((predicted == test_labels).mean())
    mae = float((predicted - test_labels).abs().mean())
    return {
        "majority_value": majority_value,
        "majority_baseline_exact_match": exact_match,
        "majority_baseline_mae": mae,
    }


def main() -> None:
    profile_master = pd.read_excel(LINKEDIN_PATH, sheet_name="Profile_Master")
    education = pd.read_excel(LINKEDIN_PATH, sheet_name="Education")
    certification = pd.read_excel(LINKEDIN_PATH, sheet_name="Certification")
    professional_experience = pd.read_excel(
        LINKEDIN_PATH, sheet_name="Professional_Experience"
    )
    technical_contribution = pd.read_excel(
        LINKEDIN_PATH, sheet_name="Technical_Contribution"
    )
    dimension_evidence = pd.read_excel(ANNOTATION_PATH, sheet_name="Dimension_Evidence")

    documents = build_profile_documents(
        profile_master,
        education,
        certification,
        professional_experience,
        technical_contribution,
    )
    print(f"Built {len(documents)} profile documents")
    print(
        f"Documents with non-empty text: "
        f"{(documents['Text'].str.len() > 0).sum()} / {len(documents)}"
    )

    gold_long = dimension_evidence[dimension_evidence["Missing_Status"] == "present"][
        ["Profile_ID", "Dimension", "Final_Score"]
    ].rename(columns={"Final_Score": "Score"})

    all_predictions = []
    all_artifacts = []
    all_splits = []

    for d in DIMENSIONS:
        predictions, split, artifacts = fit_predict_dimension(
            documents, gold_long, d.number, seed=RANDOM_SEED
        )
        all_predictions.append(predictions)

        gold_by_id = (
            gold_long[gold_long["Dimension"] == f"D{d.number}"]
            .set_index("Profile_ID")["Score"]
            .astype(int)
        )
        train_labels = gold_by_id.loc[list(split.train_profile_ids)]
        test_labels = gold_by_id.loc[list(split.test_profile_ids)]
        majority = majority_class_baseline(train_labels, test_labels)

        all_artifacts.append(
            {
                "Dimension": f"D{d.number}",
                "n_train": artifacts.n_train,
                "n_test": artifacts.n_test,
                "vocabulary_size": artifacts.vectorizer_vocabulary_size,
                "ridge_alpha": artifacts.ridge_alpha,
                "random_seed": RANDOM_SEED,
                "stratified_split": split.stratified,
                "split_note": split.note,
                "top_positive_terms": json.dumps(list(artifacts.top_positive_terms)),
                "top_negative_terms": json.dumps(list(artifacts.top_negative_terms)),
                **majority,
            }
        )
        all_splits.append(
            {
                "Dimension": f"D{d.number}",
                "train_profile_ids": json.dumps(list(split.train_profile_ids)),
                "test_profile_ids": json.dumps(list(split.test_profile_ids)),
            }
        )
        print(
            f"D{d.number}: n_train={artifacts.n_train} n_test={artifacts.n_test} "
            f"stratified={split.stratified} "
            f"vocab={artifacts.vectorizer_vocabulary_size} "
            f"majority_baseline="
            f"{majority['majority_baseline_exact_match']:.3f}"
        )

    predictions_df = pd.concat(all_predictions, ignore_index=True)
    gold_for_eval = gold_long.rename(
        columns={"Profile_ID": "profile_id", "Dimension": "Dimension_str"}
    )
    gold_for_eval["dimension_number"] = (
        gold_for_eval["Dimension_str"].str.lstrip("D").astype(int)
    )
    gold_for_eval = gold_for_eval[["profile_id", "dimension_number", "Score"]].rename(
        columns={"Score": "score"}
    )

    report = evaluate_predictions(
        predictions_df,
        gold_for_eval,
        "final_frozen",
        source_description="TF-IDF + Ridge baseline, seed=42, "
        "reproducible via 15_Scripts/alcsm_nlp_baseline_v1.0.py",
    )
    errors = error_analysis(predictions_df, gold_for_eval, "final_frozen", "same run")

    metrics_rows = []
    for dim_number in sorted(report.by_dimension):
        m = report.by_dimension[dim_number]
        artifacts_row = next(
            a for a in all_artifacts if a["Dimension"] == f"D{dim_number}"
        )
        metrics_rows.append(
            {
                "Dimension": m.dimension,
                "n": m.n,
                "exact_match_rate": m.exact_match_rate,
                "mean_signed_error": m.mean_signed_error,
                "mean_absolute_error": m.mean_absolute_error,
                "linear_weighted_kappa": m.linear_weighted_kappa,
                "majority_baseline_exact_match": artifacts_row[
                    "majority_baseline_exact_match"
                ],
                "majority_baseline_mae": artifacts_row["majority_baseline_mae"],
                "beats_majority_baseline": (
                    m.exact_match_rate > artifacts_row["majority_baseline_exact_match"]
                ),
            }
        )
    metrics_df = pd.DataFrame(metrics_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(RESULTS_XLSX, engine="openpyxl") as writer:
        metrics_df.to_excel(writer, sheet_name="Per_Dimension_Metrics", index=False)
        pd.DataFrame(all_artifacts).to_excel(
            writer, sheet_name="Model_Configuration", index=False
        )
        pd.DataFrame(all_splits).to_excel(
            writer, sheet_name="Train_Test_Splits", index=False
        )
        predictions_df.to_excel(writer, sheet_name="Predictions", index=False)
        errors.error_distribution_by_dimension.to_excel(
            writer, sheet_name="Error_Distribution"
        )
        pd.DataFrame([e.__dict__ for e in errors.largest_errors]).to_excel(
            writer, sheet_name="Largest_Errors", index=False
        )
        for dim_number, matrix in report.confusion_matrices.items():
            matrix.to_excel(writer, sheet_name=f"Confusion_D{dim_number}")

    print(f"\nWrote {RESULTS_XLSX}")
    print("\nPer-dimension metrics:")
    print(metrics_df.to_string(index=False))


if __name__ == "__main__":
    main()
