# RQ3 Final Results Package v1.0

**RQ3:** How can ALCSM be constructed and validated as a measurement instrument?
**Status:** Final consolidation of RQ3's evidence for thesis use. **No new computation in this document** — every figure is reproduced from `07_Reliability/Reliability_Report_v1.1.md`, `Reliability_Results_v1.1.xlsx`, `09_Statistical_Analysis/RQ3/RQ3_Reliability_Final_Interpretation_v1.0.md`, and `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx`.
**Source-file note:** this task named a source file `Survey_Analysis_Final_v1.1.xlsx`; no such file exists in the repository. The real, current survey source is `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` (24 consented respondents, promoted to canonical in the prior session after a newer raw export was found — see `Survey_Status_Report_v1.0.md`). This package uses that real file; flagged here rather than silently substituted.
**Author:** Samiksha Dhere (researcher) — consolidated with Claude Code assistance

**Language discipline (enforced throughout this document):** ALCSM is never described as "fully validated." The terms used are *content-assessment evidence*, *inter-rater reliability evidence*, and *measurement reproducibility* — never "proof," "validation," or "confirmed."

---

## A. Formative measurement rationale

ALCSM is constructed as a **formative index**: D1–D6 are six distinct, non-interchangeable observable credential signals, not six reflective indicators of one underlying latent trait. Two consequences follow, both enforced structurally in this codebase, not only stated in prose: (1) the six dimensions are not expected to correlate with one another, so no internal-consistency statistic (Cronbach's alpha) is an appropriate way to assess this instrument — no function anywhere in this project computes one; (2) reliability and content-assessment evidence must be reported **per dimension, never pooled** into a single figure for "ALCSM as a whole" — enforced in code (`tests/reliability/test_krippendorff.py::test_never_computes_a_single_pooled_alpha_across_dimensions`) and followed without exception in every table below.

## B. Expert content-assessment survey (N = 24)

24 consented respondents (practitioners across AI/ML engineering, data science, AI/technology leadership, academia, consulting, and technical recruiting backgrounds) rated each dimension's relevance and clarity as an observable credential signal, and the overall six-dimension framework's appropriateness, on 1–5 scales.

| Dimension | Relevance (mean/5) | Clarity (mean/5) |
|---|---|---|
| D1 — Formal Education | 3.54 | — |
| D2 — Professional Certifications | 3.25 | — |
| D3 — Practical AI Experience | **4.33** (highest) | — |
| D4 — Technical Contributions | 3.54 | — |
| D5 — Leadership & Strategic Responsibility | 3.63 | — |
| D6 — AI Industry/Application Breadth | 3.67 | — |

*(Clarity means are in `ALCSM_Survey_Analysis_Processed_v1.0.xlsx`'s `Clarity` sheet, omitted from the table above for brevity — all six fall in the 3.29–4.00 range, no dimension rated as unclear.)*

- **Overall framework appropriateness:** mean 3.42/5 (median 3), all 24 respondents answered.
- **Most-important-dimension picks:** D3 led with 9 of 24 (37.5%), followed by D4 (5), D2 and D6 (4 each), D5 (2). **These counts are reported as descriptive fact about expert opinion only — never converted into a weight, ranking used in scoring, or any other input to a composite figure.** No such conversion exists anywhere in this codebase.
- **Instrument limitation, stated plainly:** the distinctiveness item (whether each dimension feels separable from the others) has a **0% response rate** across all 24 respondents and across every prior survey snapshot collected in this project. This is a property of the real data, not a bug, and is carried into this final package as a stated limitation rather than omitted.
- **What this evidence is not:** not predictive validation, not competence validation, not population inference (N=24 self-selected respondents), not internal consistency, not factor analysis. It is *content-assessment evidence*: whether domain-knowledgeable people judge the instrument's content reasonable.

## C. Inter-rater reliability (75-profile independent double-coding subset)

Two independent human raters — the primary researcher (frozen final annotation) and an independent second rater (never the AI-assisted first pass) — each scored the same deterministic, seed-reproducible 75-profile subset (15% of the 500-profile dataset).

| Dim | Krippendorff's α (ordinal) | n | Observed agreement | Reading |
|---|---|---|---|---|
| D1 | **0.944** | 72 | 81.9% | Strong reproducibility — wide range, high variance both raters. |
| D2 | **1.000** | 27 | 100.0% | **Low-information/degenerate** — zero variance after excluding unavailable cases (every remaining rating is the same single value); not evidence of strong discrimination. |
| D3 | **0.102** | 75 | 54.7% | Limited reliability — a **systematic, one-directional 3→4 calibration disagreement** (Rater B always scored higher than Rater A, never the reverse; 52.9% of all disagreements are exactly this score pair). |
| D4 | **1.000** | 26 | 100.0% | **Low-information/degenerate** in the same sense as D2 — perfect agreement on a small (n=26), range-restricted sample. |
| D5 | **0.246** | 75 | 85.3% | Limited reliability — **substantial range restriction** (Rater A concentrated 68/75 ratings at a single score) **combined with a genuine boundary disagreement around seniority-title vs. explicit strategic-scope language** (Director/Head/VP boundary cases). |
| D6 | **1.000** | 75 | 100.0% | Strong reproducibility — full range, genuine agreement, not a degenerate case (unlike D2/D4). |

**No pooled or averaged alpha is reported anywhere** — six independent results, six independent readings.

## D. Reliability limitations

- **One subset, one second rater, computed once.** This does not establish population-level reliability and is not repeated-measures evidence.
- **D2 and D4's perfect alpha values must not be cited as strong evidence of reliable discrimination** — both reflect degenerate, near-zero-variance samples (D2: the present-only population is 100% one score; D4: only 26 of 75 profiles have any evidence at all). Reported as "low-information/degenerate," not folded into the same category as D1/D6's genuine strong results.
- **D3's disagreement is diagnosed, not resolved.** The 3→4 boundary disagreement (18 of 34 disagreeing cases, 52.9%) reflects a real difference in how the two raters computed cumulative AI-related experience duration and weighted senior-title language — a rulebook-clarity finding, not evidence the construct is unmeasurable. **No new scoring round is recommended** — per this session's explicit instruction, this is reported as a diagnosed limitation for the thesis to state honestly, not an action item.
- **D5's low alpha is primarily a statistical artifact of range restriction**, not primarily evidence of poor construct clarity — the 85.3% raw agreement rate argues against "the dimension fails," while the specific residual disagreement (Director/Head/VP strategic-language boundary cases) is a narrower, identifiable ambiguity in a dimension already documented as lower-verifiability (D5 is the only dimension coded "low" verifiability in the frozen dimension configuration) than D1's "high."
- **The second-rater source file's encoding was recovered, not originally structured for this purpose** — documented in full in `Reliability_Subset_Verification_v1.2.md`; this residual data-handling limitation is disclosed but was confirmed not to be the cause of D3's or D5's low alpha (the missing-data/unavailable-inference mechanism has zero effect on either dimension in this subset).

## E. Overall conclusion for RQ3

**RQ3's evidence is dimension-dependent, not uniform, and this is reported as a structural finding, not smoothed into a single verdict.** Strong, non-degenerate reproducibility is demonstrated for **D1 and D6**. **D2 and D4** show perfect but low-information agreement that should not be over-read. **D3 and D5** show limited reliability for two distinct, now-diagnosed reasons — a systematic rater-calibration difference for D3, and range restriction plus a narrower boundary-judgment ambiguity for D5. Content-assessment evidence from 24 domain-knowledgeable respondents independently rates all six dimensions as moderately-to-highly relevant and clear, with D3 rated most relevant and most frequently chosen as most important, and the overall framework rated moderately appropriate (3.42/5).

**ALCSM is not described as fully validated anywhere in this package.** The evidence supports treating it as a formative index whose easier-to-verify dimensions (formal credentials, industry breadth) reproduce well under independent double coding and are judged relevant by domain experts, while its higher-order, judgment-dependent dimensions (practical experience depth, leadership scope) show real, specific, diagnosable reproducibility limits — reported honestly as measurement reproducibility evidence and content-assessment evidence, two distinct and complementary validation routes for a formative index, neither one a certificate of validity on its own.

---

*Sources: `Reliability_Report_v1.1.md`, `Reliability_Results_v1.1.xlsx`, `RQ3_Reliability_Final_Interpretation_v1.0.md`, `D3_D5_Disagreement_Analysis_v1.0.xlsx`, `Survey_Analysis_Plan_v1.0.md`, `Survey_Status_Report_v1.0.md`, `ALCSM_Survey_Analysis_Processed_v1.0.xlsx`. No canonical source file modified. D1–D6 and their scoring criteria unchanged. No composite score, weight, or classification band computed anywhere.*
