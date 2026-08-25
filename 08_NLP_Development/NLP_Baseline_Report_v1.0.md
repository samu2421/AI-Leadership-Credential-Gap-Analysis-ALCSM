# NLP Baseline Report v1.0

**Status:** A real, working, reproducible baseline has been trained and evaluated against the frozen 500-profile gold standard. **This is a minimal defensible baseline, not a finished or state-of-the-art model** — per this session's own priority: working, reproducible, interpretable > sophisticated and unfinished.
**Gold standard:** `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` (`Dimension_Evidence`, `Missing_Status == "present"` rows only).
**Source code:** `src/alcsm/nlp/baseline.py` (feature building, split, fit/predict), `15_Scripts/alcsm_nlp_baseline_v1.0.py` (runner — the sole source of every number in this report and in `NLP_Thesis_Results_v1.0.md`).
**Results workbook:** `NLP_Baseline_Results_v1.0.xlsx` (git-ignored, contains per-profile predictions).
**Local-only:** scikit-learn TF-IDF + Ridge regression, entirely in-process. No external API, no OpenAI/Claude call, on any profile text, anywhere in this pipeline.

---

## Part 1 — Input definition

**What the model receives, per profile, exactly:** a single concatenated text "document" built by `alcsm.nlp.baseline.build_profile_documents` from five raw processed fields only:

| Source sheet | Fields included | Fields explicitly excluded |
|---|---|---|
| `Profile_Master` | Current_Title, Industry, Company_Size, Title_Category | Country, Federal_State, City (not informative for any dimension; reduces identifiability) |
| `Education` | Degree_Level, Field_of_Study, University | Country, Start_Year/End_Year |
| `Certification` | Certification_Category, Certification_Name, Issuing_Organization | — |
| `Professional_Experience` | Job_Title, Industry, a derived tenure bucket (short/medium/long/very_long, from Duration_Months), Leadership_Role, AI_Related | Company (employer name) — not informative, reduces identifiability |
| `Technical_Contribution` | Contribution_Type, Title | — |

**What the model never receives, and why:** `Dimension_Evidence`'s `Evidence`, `Rationale`, `Confidence`, and `Decision` fields are never read by `build_profile_documents` — these are the annotation *process's own output* (a human or the AI-assisted first pass already interpreting the raw facts into a scoring justification). Feeding them to the model would leak the label's own reasoning into the input, not give the model a fair, comparable information base. This is a structural guarantee, not a runtime filter: the function's signature only accepts the five raw sheets above, which have no Evidence/Rationale/Confidence/Decision columns at all (verified in `tests/nlp/test_baseline.py::TestBuildProfileDocuments::test_never_includes_evidence_or_rationale_fields`).

**Human-vs-machine information comparability:** the human annotator (and the AI-assisted first pass before them) read the same underlying processed LinkedIn fields this model reads — job titles, education, certifications, experience history, technical contributions. The model does not receive anything the human didn't have access to, and receives strictly less (no free-form judgment, no cross-referencing, no external search).

**Coverage:** all 500 profiles produced a non-empty document (500/500) — every profile has at least one populated field among the five source sheets.

## Part 2 — Baseline architecture

**TF-IDF + Ridge regression** (the first, preferred option in this session's brief; sentence-transformers was not used, since it is not already configured locally and the TF-IDF baseline did not fail completely — no justification to reach for the second, heavier option).

- Vectorizer: `TfidfVectorizer(max_features=2000, ngram_range=(1,2), min_df=2, stop_words="english")`.
- Model: `Ridge(alpha=1.0, random_state=42)` — a continuous linear model, since the target is ordinal (0–5), not nominal. Prediction is rounded to the nearest integer and clipped to `[0, 5]`.
- **Why Ridge regression over a plain multiclass classifier:** rounding a continuous prediction naturally respects the ordinal structure of the scale (a prediction of 3.6 is closer to 4 than to 0, which a nominal multiclass classifier does not know by construction). Simple, fast, fully interpretable (linear coefficients can be inspected directly — see Part 3's top terms).

## Part 3 — Dimension-specific models (never a composite)

**Six entirely independent models — one per dimension, six independent train/test splits, six independent predictions.** No ALCSM total or composite score is computed anywhere in this pipeline. Each dimension's model only ever sees that dimension's own gold labels.

| Dim | n train | n test | Vocabulary size | Top positive terms | Top negative terms |
|---|---|---|---|---|---|
| D1 | 376 | 95 | 2000 | phd, mathematics, physics, science, informatics | chemistry, management, administration, business administration, head |
| D2 | 187 | 47 | 2000 | zu berlin, executive education, essen, essentials, essentials business | 2010, physics, physical, philosophy, phd visible |
| D3 | 397 | 100 | 2000 | ai, data, scientist, data science, medium_tenure ai_related_yes | founder, ai_related_no leadership_role_yes, managing director, research ai_related_yes, logistics |
| D4 | 140 | 35 | 1860 | publication, patent, und, director, ai consulting | finance, law, chief, technical, automotive short_tenure |
| D5 | 400 | 100 | 2000 | head, director, transformation, transformation officer, tech | ai lead, lead, leitung, advisor consulting, data strategy |
| D6 | 397 | 100 | 2000 | ai_related_yes, research, ai_related_yes leadership_role_no, publication, leadership_role_no | ai_related_no, technology long_tenure, multinational, ai_related_no leadership_role_yes, director |

**These top terms are directly interpretable and mostly make intuitive sense** — D1's positive terms (phd, mathematics, physics) are exactly the kind of formal-education signal D1 is designed to capture; D5's positive terms (head, director, transformation officer) versus negative (ai lead, lead) mirror the same Director/Head/VP-vs-"Lead" distinction the inter-rater reliability diagnosis (`RQ3_Reliability_Final_Interpretation_v1.0.md` §4) independently found humans disagreeing about — a notable cross-check between two separate analyses.

## Part 4 — Ordinal evaluation (never raw accuracy alone)

Reused entirely from the existing, already-tested `alcsm.nlp.evaluate` module — exact-match rate, mean signed/absolute error, linear-weighted Cohen's kappa, and a full 6×6 confusion matrix per dimension. Compared against each dimension's own **majority-class baseline** (always predict the training set's most common score) — the floor any real signal must clear.

| Dim | n (test) | Exact match | MAE | Weighted κ | Majority-baseline exact match | Beats majority baseline? |
|---|---|---|---|---|---|---|
| D1 | 95 | 29.5% | 0.989 | 0.283 | 28.4% | **Yes**, marginally |
| D2 | 47 | 100.0% | 0.000 | 1.000 | 100.0% | **No — tie**, see note below |
| D3 | 100 | 52.0% | 0.570 | 0.399 | 35.0% | **Yes**, clearly |
| D4 | 35 | 62.9% | 0.371 | **−0.022** | 71.4% | **No** |
| D5 | 100 | 87.0% | 0.150 | 0.260 | 87.0% | **No — tie** |
| D6 | 100 | 44.0% | 0.640 | 0.238 | 48.0% | **No** |

**D2's tie is degenerate, not a modeling result.** The present-only D2 population is **100% score `1`** (all 234 profiles with any certification evidence score exactly 1 — D2's own real-world range is 0–1, and once "unavailable" cases are correctly excluded, only score 1 remains). There is nothing to predict — any constant model, including the majority baseline, scores 100%. This exactly mirrors the same degenerate/ceiling finding already documented for D2 in the inter-rater reliability diagnosis (`RQ3_Reliability_Final_Interpretation_v1.0.md` §2) — two independent analyses (human reliability, NLP baseline) converge on the same root cause.

**D5's near-tie is a class-imbalance artifact, discussed explicitly as required.** D5's training population is 87% one score (`3`) — the majority-class baseline already achieves 87.0% exact match by construction. The model's 87.0% is statistically indistinguishable from that floor; its weighted κ (0.260) is modest and positive, meaning it does capture *some* real signal (visible in the top terms: "head"/"director" vs. "lead"), but the headline exact-match number alone would overstate what the model has learned. This mirrors the same D5 range-restriction finding from the reliability diagnosis.

**D4 and D6 do not beat their majority baselines — reported honestly, not hidden.** D4's weighted κ is slightly negative (−0.022), meaning the model's errors are no better than chance-level disagreement once its small test set (n=35) and the majority baseline are accounted for. D6 underperforms its majority baseline by 4 points and its confusion matrix (below) shows the model rarely predicts scores above 2, even though real D6 scores range 0–5 — a plausible explanation is that D6 (counting *distinct* industries/domains across a profile's whole history) requires aggregating and counting across multiple experience rows, a signal bag-of-words TF-IDF is poorly suited to represent, unlike D1's single-value degree-level signal.

**D3 shows the clearest genuine positive signal** (52.0% vs. 35.0% majority baseline, κ=0.399) — notable because D3 also had the *worst* human inter-rater reliability (α=0.102, `RQ3_Reliability_Final_Interpretation_v1.0.md`). A plausible reading: the model latches onto surface lexical cues ("ai", "data scientist", tenure buckets) that correlate with the researcher's score even though two independent human raters genuinely disagreed on how to weigh those same cues. **This is not claimed as evidence the model "solves" D3's reliability problem** — it is reported as an interesting, honest contrast between two different kinds of agreement (human-human vs. model-vs-one-human).

### Confusion matrices (selected; full 6×6 for all six dimensions in `NLP_Baseline_Results_v1.0.xlsx`)

**D3** (rows = gold, columns = predicted): the model never predicts the extreme values 0, 1, or 5 — predictions cluster at 2/3/4. Gold=1 is frequently over-predicted upward (to 2 or 3); gold=3 and gold=4 are the best-predicted bands.

**D6**: predictions cluster almost entirely at 1/2 — the model essentially never predicts 3, 4, or 5, even though real profiles do reach those scores (67, 28, and 5 profiles respectively in the full 500). This is the clearest evidence of the "can't count distinct industries from bag-of-words" limitation above.

## Part 5 — Train/test split

Reproducible random seed **42**, fixed in `alcsm.nlp.baseline.RANDOM_SEED`. 80/20 split, attempted with stratification by score for every dimension. **Stratification succeeded for five of six dimensions** (D1, D2, D4, D5, D6); **D3 could not be stratified** because its present-only population has exactly one profile at score `0` (`split_note`: *"class(es) [0] have fewer than 2 members and cannot be split with at least one member per side"*) — scikit-learn's stratified split requires at least 2 members per class to place one in each side. D3 fell back to a plain random split, with this exact reason recorded in the results workbook (`Model_Configuration` sheet), not silently swallowed.

**No profile appears in both train and test for any dimension** — enforced structurally by `sklearn.model_selection.train_test_split`'s partition guarantee, and directly tested (`tests/nlp/test_baseline.py::TestSplitProfilesForDimension::test_no_profile_appears_in_both_train_and_test`).

Each dimension has its **own** split (not one split shared across all six) — this is deliberate: each dimension's "available" (non-unavailable) profile population differs (e.g., D2 has 234 present profiles, D4 has 175), so a single joint split would have prevented good stratification for most dimensions. A profile can be in D1's training set and D3's test set simultaneously — there is no leakage risk in this, since each dimension's model is entirely independent and never shares a vectorizer, model, or prediction with another dimension.

## Part 6 — Leakage discipline

- The `TfidfVectorizer` is `.fit_transform()`-ed on training documents only; test documents only ever see `.transform()` (never re-fit).
- The `Ridge` model is `.fit()` on training documents/labels only.
- Both are refit independently per dimension (six separate vectorizers, six separate models) — a dimension's vectorizer vocabulary is never influenced by another dimension's data, and never by any test-set document.
- No feature selection step beyond the vectorizer's own `max_features`/`min_df` (both are unsupervised, fit on train text only — they never see labels or test data).

## Part 7 output pointer

See `NLP_Thesis_Results_v1.0.md` for thesis-ready Methods/Results prose. `NLP_Baseline_Results_v1.0.xlsx` sheets: `Per_Dimension_Metrics`, `Model_Configuration`, `Train_Test_Splits`, `Predictions`, `Error_Distribution`, `Largest_Errors`, `Confusion_D1`…`Confusion_D6`.

## Part 8 — Minimum success criteria, checked

| Criterion | Met? |
|---|---|
| Reproducible baseline | Yes — fixed seed 42, deterministic TF-IDF/Ridge, re-run produces identical output (verified: `tests/nlp/test_baseline.py::test_reproducible_given_same_seed`, both at the split and prediction level). |
| Per-dimension predictions | Yes — six independent models, `Predictions` sheet. |
| Evaluation metrics | Yes — exact match, MAE, weighted κ, per dimension, `Per_Dimension_Metrics` sheet. |
| Confusion matrices | Yes — one 6×6 matrix per dimension. |
| Documented limitations | Yes — D2's degeneracy, D5's imbalance, D4/D6's below-baseline performance, all stated plainly above, none hidden. |
| Saved model configuration | Yes — `Model_Configuration` sheet: vectorizer vocabulary size, Ridge alpha, random seed, split strategy, per-dimension top coefficients (not a serialized binary — out of scope for a minimal baseline, but every hyperparameter needed to exactly re-fit is recorded). |
| Reproducible random seed | Yes — 42, `alcsm.nlp.baseline.RANDOM_SEED`, used for every split and the Ridge model itself. |

**This baseline does not achieve state-of-the-art performance, and is not claimed to.** Three of six dimensions (D2 degenerate-tie, D5 imbalance-tie, D4 and D6 below baseline) show the model provides little or no advantage over trivial guessing — reported as an honest, direct finding, not smoothed over. D1 and D3 show modest genuine positive signal.

---

*No canonical source file was modified. D1–D6, their definitions, and scoring criteria are unchanged. No composite score exists anywhere in this pipeline.*
