"""Minimal, defensible local NLP baseline (Phase P7, first real
implementation -- explicitly authorized this session, "FINAL NLP
IMPLEMENTATION").

Architecture note (why this is a new module, not `extract.py`/
`classify.py`): those two stubs were scaffolded for a more elaborate,
not-yet-authorized future approach -- `extract.py`'s docstring
describes parsing `profile_raw_section` (a raw-scraped-text database
table that has never been populated) via keyword-anchored span
extraction, and `classify.py` a from-scratch ordinal classifier
interface. Neither of those inputs or interfaces matches what this
session actually builds: a simple, interpretable TF-IDF + linear
model baseline over the *already-structured* processed Excel fields
(Part 2's own explicit preference: "TF-IDF + supervised classifier/
regressor" first, sentence-transformers only if already configured
locally -- it is not). Rather than force-fit a simpler approach into
scaffolding designed for a more sophisticated one, this module is
added alongside them, clearly scoped, leaving `extract.py`/
`classify.py` untouched for whatever more elaborate approach a future
phase may still build.

Local-only, no external API: everything here is `scikit-learn`
(TF-IDF vectorizer + Ridge regression), run entirely in-process. No
network call, no OpenAI/Claude/any hosted model is used anywhere in
this module or its callers.

Part 1 -- exactly what the model receives (and does not):
the per-profile "document" fed to the vectorizer is built ONLY from
`alcsm.analysis.data_sources`-shaped raw processed fields (`Profile_
Master`, `Education`, `Certification`, `Professional_Experience`,
`Technical_Contribution` -- see `build_profile_documents`) -- the same
underlying LinkedIn-derived facts a human annotator would have read.
It explicitly EXCLUDES `Dimension_Evidence`'s `Evidence`/`Rationale`/
`Confidence`/`Decision` fields, which are the annotation PROCESS's own
output (a human or the AI-assisted first pass already interpreting
the raw facts into a justification for a specific score) -- feeding
those to the model would leak the label's own reasoning into the
input, not give the model a fair, comparable information base. It
also excludes direct-identifier-adjacent fields not needed for any
dimension (Country/Federal_State/City, employer Company name) on the
same "comparable, not more, not less" principle -- see
`build_profile_documents`'s docstring for the exact field list.

Ordinal target handling: scores are 0-5 ordinal, not nominal classes.
This baseline uses Ridge regression (a continuous linear model) whose
prediction is rounded to the nearest integer and clipped to [0, 5] --
a standard, simple, interpretable way to respect ordinal structure
without requiring a specialized ordinal-classification dependency.
Never a composite/combined score across dimensions: six independent
models, six independent predictions, never pooled or averaged.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

from alcsm.constants import SCORE_MAX, SCORE_MIN

RANDOM_SEED = 42
TEST_SIZE = 0.2


def _duration_bucket(months: object) -> str:
    if months is None or (isinstance(months, float) and months != months):
        return ""
    try:
        m = float(months)
    except (TypeError, ValueError):
        return ""
    if m < 12:
        return "short_tenure"
    if m < 36:
        return "medium_tenure"
    if m < 72:
        return "long_tenure"
    return "very_long_tenure"


def build_profile_documents(
    profile_master: pd.DataFrame,
    education: pd.DataFrame,
    certification: pd.DataFrame,
    professional_experience: pd.DataFrame,
    technical_contribution: pd.DataFrame,
) -> pd.DataFrame:
    """One text "document" per profile, built only from raw processed
    fields (never from `Dimension_Evidence`'s Evidence/Rationale, and
    never from `Profile_Master`'s Country/Federal_State/City or
    `Professional_Experience`'s employer `Company` name -- excluded as
    not informative for any dimension and to reduce identifiability).

    Fields used, by source sheet:
    - `Profile_Master`: Current_Title, Industry, Company_Size,
      Title_Category.
    - `Education`: Degree_Level, Field_of_Study, University (one line
      per row; a profile may have several).
    - `Certification`: Certification_Category, Certification_Name,
      Issuing_Organization (one line per row).
    - `Professional_Experience`: Job_Title, Industry, a duration
      bucket derived from Duration_Months (short/medium/long/very_long
      tenure -- a simple, documented feature-engineering choice, not
      the raw number, since TF-IDF treats numeric tokens as opaque
      strings), Leadership_Role, AI_Related (one line per row).
    - `Technical_Contribution`: Contribution_Type, Title (one line per
      row).

    Returns columns `Profile_ID, Text`. A profile with no rows in any
    of these five sheets still gets a row here (`Text` may be empty or
    near-empty) -- excluding it here would need to be a modeling
    decision, not a text-building one.
    """
    parts: dict[str, list[str]] = {}

    def _add(profile_id: str, text: str) -> None:
        if not text:
            return
        parts.setdefault(profile_id, []).append(text)

    for row in profile_master.itertuples(index=False):
        bits = [
            str(getattr(row, "Current_Title", "") or ""),
            str(getattr(row, "Industry", "") or ""),
            str(getattr(row, "Company_Size", "") or ""),
            str(getattr(row, "Title_Category", "") or ""),
        ]
        _add(row.Profile_ID, " ".join(b for b in bits if b))

    for row in education.itertuples(index=False):
        bits = [
            str(getattr(row, "Degree_Level", "") or ""),
            str(getattr(row, "Field_of_Study", "") or ""),
            str(getattr(row, "University", "") or ""),
        ]
        _add(row.Profile_ID, " ".join(b for b in bits if b))

    for row in certification.itertuples(index=False):
        bits = [
            str(getattr(row, "Certification_Category", "") or ""),
            str(getattr(row, "Certification_Name", "") or ""),
            str(getattr(row, "Issuing_Organization", "") or ""),
        ]
        _add(row.Profile_ID, " ".join(b for b in bits if b))

    for row in professional_experience.itertuples(index=False):
        duration_token = _duration_bucket(getattr(row, "Duration_Months", None))
        ai_related = getattr(row, "AI_Related", None)
        leadership = getattr(row, "Leadership_Role", None)
        bits = [
            str(getattr(row, "Job_Title", "") or ""),
            str(getattr(row, "Industry", "") or ""),
            duration_token,
            f"ai_related_{ai_related}" if pd.notna(ai_related) else "",
            f"leadership_role_{leadership}" if pd.notna(leadership) else "",
        ]
        _add(row.Profile_ID, " ".join(b for b in bits if b))

    for row in technical_contribution.itertuples(index=False):
        bits = [
            str(getattr(row, "Contribution_Type", "") or ""),
            str(getattr(row, "Title", "") or ""),
        ]
        _add(row.Profile_ID, " ".join(b for b in bits if b))

    all_ids = set(profile_master["Profile_ID"])
    rows = [
        {"Profile_ID": pid, "Text": " . ".join(parts.get(pid, []))} for pid in all_ids
    ]
    return pd.DataFrame(rows).sort_values("Profile_ID").reset_index(drop=True)


@dataclass(frozen=True)
class DimensionSplit:
    dimension_number: int
    train_profile_ids: tuple[str, ...]
    test_profile_ids: tuple[str, ...]
    stratified: bool
    note: str


def split_profiles_for_dimension(
    profile_ids: list[str],
    labels: list[int],
    dimension_number: int,
    seed: int = RANDOM_SEED,
    test_size: float = TEST_SIZE,
) -> DimensionSplit:
    """Reproducible, profile-level train/test split for one dimension's
    available (non-unavailable) profiles. Stratifies by score where
    every class has at least 2 members (scikit-learn's own minimum for
    a stratified split to place at least one member in each side);
    falls back to a plain random split, with the reason recorded on
    the returned object, when a class is too sparse to stratify.

    No profile can appear in both the returned train and test sets --
    enforced structurally: `train_test_split` partitions its input
    into two disjoint sets by construction.
    """
    value_counts = pd.Series(labels).value_counts()
    can_stratify = bool((value_counts >= 2).all())

    if can_stratify:
        train_ids, test_ids = train_test_split(
            profile_ids,
            test_size=test_size,
            random_state=seed,
            stratify=labels,
        )
        note = "stratified by score"
    else:
        sparse_classes = sorted(value_counts[value_counts < 2].index.tolist())
        train_ids, test_ids = train_test_split(
            profile_ids,
            test_size=test_size,
            random_state=seed,
        )
        note = (
            f"NOT stratified -- class(es) {sparse_classes} have fewer than 2 "
            "members and cannot be split with at least one member per side; "
            "fell back to a plain random split"
        )

    return DimensionSplit(
        dimension_number=dimension_number,
        train_profile_ids=tuple(train_ids),
        test_profile_ids=tuple(test_ids),
        stratified=can_stratify,
        note=note,
    )


@dataclass(frozen=True)
class DimensionModelArtifacts:
    """What was fitted, for the "saved model configuration" success
    criterion -- not a serialized binary (out of scope for a minimal
    baseline), but every hyperparameter and the resulting vocabulary
    size/top coefficients, sufficient to describe and re-fit the exact
    same model."""

    dimension_number: int
    vectorizer_vocabulary_size: int
    ridge_alpha: float
    n_train: int
    n_test: int
    top_positive_terms: tuple[str, ...]
    top_negative_terms: tuple[str, ...]


def fit_predict_dimension(
    documents: pd.DataFrame,
    gold_long: pd.DataFrame,
    dimension_number: int,
    seed: int = RANDOM_SEED,
    ridge_alpha: float = 1.0,
) -> tuple[pd.DataFrame, DimensionSplit, DimensionModelArtifacts]:
    """Fit one dimension's TF-IDF + Ridge model and predict on its held-
    out test set. Returns (predictions, split, artifacts).

    ``gold_long``: columns `Profile_ID, Dimension, Score` -- already
    restricted to `Missing_Status == "present"` rows for this
    dimension by the caller (an `unavailable` case is not a training
    or evaluation label; it is not present in this frame at all).

    Leakage discipline: the `TfidfVectorizer` and `Ridge` model are
    both `.fit()` ONLY on the training profiles' documents/labels.
    `.transform()` (never `.fit_transform()`) is the only thing ever
    called on the test documents.
    """
    dim_label = f"D{dimension_number}"
    dim_gold = gold_long[gold_long["Dimension"] == dim_label]
    profile_ids = dim_gold["Profile_ID"].tolist()
    labels = dim_gold["Score"].astype(int).tolist()

    split = split_profiles_for_dimension(profile_ids, labels, dimension_number, seed)

    doc_by_id = documents.set_index("Profile_ID")["Text"]
    label_by_id = dim_gold.set_index("Profile_ID")["Score"].astype(int)

    train_docs = doc_by_id.loc[list(split.train_profile_ids)].tolist()
    train_labels = label_by_id.loc[list(split.train_profile_ids)].to_numpy()
    test_docs = doc_by_id.loc[list(split.test_profile_ids)].tolist()

    vectorizer = TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 2),
        min_df=2,
        stop_words="english",
    )
    x_train = vectorizer.fit_transform(train_docs)
    x_test = vectorizer.transform(test_docs)

    model = Ridge(alpha=ridge_alpha, random_state=seed)
    model.fit(x_train, train_labels)
    raw_pred = model.predict(x_test)
    clipped_pred = np.clip(np.round(raw_pred), SCORE_MIN, SCORE_MAX).astype(int)

    predictions = pd.DataFrame(
        {
            "profile_id": list(split.test_profile_ids),
            "dimension_number": dimension_number,
            "predicted_score": clipped_pred,
            "predicted_score_raw": raw_pred,
        }
    )

    feature_names = vectorizer.get_feature_names_out()
    coefs = model.coef_
    order = np.argsort(coefs)
    top_negative = tuple(feature_names[order[:5]])
    top_positive = tuple(feature_names[order[-5:][::-1]])

    artifacts = DimensionModelArtifacts(
        dimension_number=dimension_number,
        vectorizer_vocabulary_size=len(feature_names),
        ridge_alpha=ridge_alpha,
        n_train=len(train_docs),
        n_test=len(test_docs),
        top_positive_terms=top_positive,
        top_negative_terms=top_negative,
    )
    return predictions, split, artifacts
