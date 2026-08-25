# RQ5 Final Results — NLP Baseline v1.0

**RQ5:** Does a human-vs-machine comparison of NLP-predicted ALCSM scores against the human gold standard reveal usable automated-scoring signal?
**Status:** Final consolidation for thesis use. **No new computation** — every figure below is reproduced from `08_NLP_Development/NLP_Baseline_Report_v1.0.md`, `NLP_Thesis_Results_v1.0.md`, and `NLP_Baseline_Results_v1.0.xlsx`.
**Explicit framing (stated once here, applies to the whole document): this is a proof-of-concept baseline for RQ5, not a production-ready AI leadership assessment system.** TF-IDF + Ridge regression, six independent per-dimension models, local-only (no external API), leakage-safe train/test split, fixed seed 42.
**Author:** Samiksha Dhere (researcher) — consolidated with Claude Code assistance

---

## Per-dimension results

| Dim | n (test) | Exact agreement | Weighted κ | Majority-class baseline | Interpretation |
|---|---|---|---|---|---|
| D1 | 95 | **29.5%** | **0.283** | 28.4% | Modest signal above baseline. |
| D2 | 47 | **100.0%** | **1.000** | 100.0% | **Degenerate** — the evaluated data are effectively one-class (every present-labeled profile in the training population scores exactly 1), so any constant predictor, including the majority baseline, reaches 100%. Not evidence of model competence. |
| D3 | 100 | **52.0%** | **0.399** | 35.0% | **Strongest genuine NLP signal** of any dimension — model exceeds its majority baseline by the widest margin. |
| D4 | 35 | **62.9%** | **−0.022** | 71.4% | Below baseline — the model's errors are no better than chance-level disagreement on this small (n=35), evidence-sparse dimension. |
| D5 | 100 | **87.0%** | **0.260** | 87.0% | Ties its majority baseline exactly. **87% exact agreement must not be read as strong predictive performance** — it is the floor set by D5's 87% population-level class imbalance (nearly all profiles score exactly 3), not a demonstration of learned discrimination. The modestly positive κ indicates some real signal exists, but it is not visible in the raw exact-match figure. |
| D6 | 100 | **44.0%** | **0.238** | 48.0% | Below baseline — predictions cluster at scores 1–2, rarely reaching the higher scores (3–5) that occur in the real population; plausibly because D6 requires counting distinct industries across a profile's full history, a signal bag-of-words TF-IDF does not explicitly aggregate. |

**No dimension is pooled with any other. No composite NLP accuracy figure exists anywhere in this project.**

## Cross-check with the human reliability findings (RQ3)

Two independent analyses converge on the same finding for D2: both the human inter-rater reliability subset (`RQ3_Final_Results_Package_v1.0.md` §C) and this NLP baseline find D2's present-only population effectively one-class, producing a perfect-but-meaningless agreement figure in both cases. This is a genuine property of the underlying data (D2's real-world observed range is 0–1 across all 500 profiles), not a coincidence between two different pipelines.

D3 shows a genuinely interesting asymmetry: it is simultaneously the dimension with the **worst** human-human reliability (α=0.102) and the dimension with the **strongest** NLP-vs-human signal (κ=0.399, the largest margin over its majority baseline of any dimension). This is reported as an interesting contrast, not a resolution — a model trained against one rater's scores can find consistent lexical correlates (terms like "ai," "data scientist," tenure-length indicators) even where two independent human raters genuinely disagreed on how to weigh those same cues at score boundaries.

## Limitations

- **Six independent models on relatively small per-dimension training sets** (as few as 140 training profiles for D4, since usable evidence coverage varies sharply by dimension) — not a large-scale training exercise, and not claimed to be.
- **TF-IDF + Ridge is a linear, bag-of-words baseline** — it cannot represent cross-field aggregation (e.g., counting distinct industries for D6) or long-range contextual meaning. A more sophisticated architecture (e.g., contextual embeddings) might close some of this gap, but was explicitly out of scope for this thesis's time budget, per the deliberate choice to prioritize a working, interpretable baseline over an unfinished sophisticated model.
- **D2's and D4's perfect/near-perfect results are explicitly caveated as degenerate**, not cited as evidence of strong model performance anywhere in this document or the thesis prose it feeds.
- **D5's headline accuracy is explicitly caveated against the 87% class-imbalance floor** — reported alongside its majority baseline in every table, never presented as a bare accuracy figure.
- **This is one train/test split per dimension**, not cross-validated — a defensible minimal-baseline choice given the 3-day thesis timeline, not presented as a rigorous generalization estimate.

## What this baseline does and does not establish

**Does establish:** a working, fully reproducible, local-only, leakage-safe automated scoring attempt exists for all six ALCSM dimensions, with per-dimension performance that is honestly reported against an appropriate majority-class floor rather than raw accuracy alone. Two dimensions (D1, D3) show genuine positive signal; two (D2, D5) tie a degenerate or imbalanced floor; two (D4, D6) underperform their floor.

**Does not establish:** that ALCSM can be automated in a production sense, that the model's predictions should replace human scoring, or any claim about ALCSM's construct validity (a separate question addressed in RQ3).

---

*Sources: `08_NLP_Development/NLP_Baseline_Report_v1.0.md`, `NLP_Thesis_Results_v1.0.md`, `NLP_Baseline_Results_v1.0.xlsx`. No canonical annotation or LinkedIn source file modified. No composite score computed anywhere.*
