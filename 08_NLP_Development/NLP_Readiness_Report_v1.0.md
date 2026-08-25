# NLP Readiness Report v1.0

**RQ5:** Human-vs-machine agreement/evaluation of an NLP model predicting ALCSM dimension scores.
**Status:** **No model is trained in this report or anywhere in this session.** This report verifies the gold-standard dataset and existing NLP scaffolding, and recommends a minimal defensible baseline for the remaining three days — it does not build one.
**Author:** Samiksha Dhere (researcher) — investigated with Claude Code assistance

---

## 1. Gold-standard readiness (the frozen human annotation)

| Property | Value |
|---|---|
| Profiles | 500 |
| Dimensions | 6 (D1–D6), each independently labeled |
| Total labeled (profile, dimension) units | 3,000 |
| Score scale | Ordinal 0–5 |
| Missing-status vocabulary in use | `present`, `unavailable` (two of the four defined states; see `Final_Annotation_Audit_v1.1.md`) |

**The frozen `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` can serve as the gold-standard reference for RQ5** — every requirement `alcsm.nlp.evaluate` expects (`profile_id`, `dimension_number`, a gold score, shaped like `v_final_profile_score`) is already satisfied by `Profile_Scores`/`Dimension_Evidence`, confirmed working this session against the real file (`Final_Annotation_Audit_v1.1.md`, and reused throughout RQ1/RQ2's scripts without modification).

## 2. Label distributions and class imbalance (per dimension — reused from RQ1's Table 1, not recomputed differently)

| Dim | Majority class | Majority share | Distinct values used (of 6 possible) |
|---|---|---|---|
| D1 | 3 | 26.8% | 6 |
| D2 | 0 | 53.2% | 2 |
| D3 | 3 | 39.4% | 5 |
| D4 | 0 | 65.0% | 4 |
| D5 | 3 | **87.0%** | 5 |
| D6 | 1 | 47.8% | 6 |

**D5 is severely imbalanced** (87% of profiles score exactly 3) — a naive classifier that always predicts 3 for D5 would already score 87% raw accuracy without learning anything, so any D5 baseline must be evaluated against this majority-class floor, not against raw accuracy alone. D2 and D4 are also imbalanced (53% and 65% majority class respectively) and additionally use only 2 and 4 of the 6 possible score values — a 6-class ordinal classifier trained on D2 would never see examples of scores 2–5 at all. D1 and D6 are the most balanced and full-range dimensions, and are also the two dimensions with the strongest inter-rater reliability results this session (`Reliability_Report_v1.1.md` §10) — the same two properties (balance, range use) plausibly make them the more learnable targets too, though that is a hypothesis for the baseline to test, not a claim made here.

## 3. Missingness and evidence availability

| Dim | Present | Unavailable | Evidence text present (of "present" rows) |
|---|---|---|---|
| D1 | 471 | 29 | 471/471 (100%) |
| D2 | 234 | 266 | 234/234 (100%) |
| D3 | 497 | 3 | 497/497 (100%) |
| D4 | 175 | 325 | 175/175 (100%) |
| D5 | 500 | 0 | 500/500 (100%) |
| D6 | 497 | 3 | 497/497 (100%) |

Every "present" row has non-empty evidence text — the gold standard is not bare scores, it carries a real evidence span per observed label, which is what a feature-extraction stage (`alcsm.nlp.extract`) would need. D2 and D4's high unavailable rates (53%/65%) mean any model trained per-dimension will have a much smaller usable training set for those two dimensions than for D1/D3/D5/D6.

## 4. Existing NLP module inspection

| Module | State | What it does |
|---|---|---|
| `alcsm.nlp.extract.extract_features` | **Unimplemented stub** (`raise NotImplementedError`) | Intended to parse raw profile text into per-dimension candidate evidence spans. Explicitly not implemented in any phase before P7. |
| `alcsm.nlp.classify.classify_dimension` | **Unimplemented stub** (`raise NotImplementedError`) | Intended six-way ordinal 0–5 predictor per dimension. Same status. |
| `alcsm.nlp.evaluate` | **Fully implemented, tested** | Confusion matrices, exact-match rate, signed/absolute error, linear-weighted Cohen's kappa — all per dimension, ordinal-appropriate, no scipy/sklearn hard dependency. Evaluation-only: it never trains, loads, or runs a model (AST-checked). |

**Neither `extract.py` nor `classify.py` was touched or implemented in this session**, per the explicit "do not train a final NLP model yet" instruction. Both remain exactly as scaffolded.

## 5. Minimum viable baseline recommendation (not built — a recommendation only)

Given the three-day deadline, a defensible thesis baseline should prioritize being **simple, explainable, and honestly evaluated** over sophisticated:

1. **Model class:** a linear/logistic ordinal classifier (e.g. ordinal logistic regression, or six independent one-vs-rest logistic classifiers per dimension) over TF-IDF or local sentence-embedding features (`sentence-transformers`, already an approved local-only dependency per `pyproject.toml`'s `nlp` extra) — not a fine-tuned transformer. This is defensible as "a reasonable first attempt, correctly evaluated" without requiring GPU time, hyperparameter search, or multi-day training.
2. **Per-dimension, not joint:** train and evaluate six separate models (or six output heads), matching this project's standing "never pool across dimensions" discipline — an aggregate "NLP accuracy" number should not be reported any more than a pooled alpha should be.
3. **Respect missingness:** train only on `present`-labeled examples per dimension (do not treat `unavailable` as a training label); report each dimension's usable training-set size honestly given §3's numbers (D2/D4 will have small effective training sets).
4. **Baseline comparison is mandatory, not optional:** report each dimension's majority-class accuracy (§2's table) alongside the model's accuracy — this is the only way a reader can tell whether the model learned anything on D5 in particular.
5. **Evaluate with the existing, already-tested `alcsm.nlp.evaluate` module as-is** — confusion matrix, exact-match rate, mean absolute error, and linear-weighted Cohen's kappa per dimension. No new evaluation code should be needed.
6. **A simple train/test split** (e.g. 80/20 stratified by dimension score where feasible) is sufficient for a thesis-defensible baseline; k-fold cross-validation is a nice-to-have, not required given the time budget.

**This recommendation is not a commitment to build all of this** — it is the smallest scope that would let RQ5 report something real and honestly caveated (a baseline, explicitly not a production model) rather than nothing, if time allows in the remaining three days. If time does not allow, RQ5 can be reported in the thesis as "gold standard prepared and verified; baseline model scoped but not executed within the submission timeline" — a true, defensible statement, not a gap that needs to be hidden.

## 6. What this report does not do

- No model was trained, loaded, or run.
- No prediction was generated, real or synthetic.
- `alcsm.nlp.classify`/`extract` were not implemented.
- No claim is made about what accuracy a real model would achieve — §5's discussion of D5's majority-class floor is a property of the label distribution, not a forecast of model performance.

---

*Reproducible verification: the label-distribution and missingness figures above come directly from `09_Statistical_Analysis/RQ1/Tables/Table1_Dimension_Score_Distribution.csv` and `Table2_Missingness_By_Dimension.csv`, already produced this session — not recomputed separately, so the two reports cannot drift out of sync.*
