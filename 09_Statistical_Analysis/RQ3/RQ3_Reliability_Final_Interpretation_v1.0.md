# RQ3 Reliability — Final Interpretation v1.0

**Status:** Final diagnostic interpretation of the D1–D6 inter-rater reliability results, for direct use in the thesis. Supersedes the interpretation section of `Reliability_Report_v1.1.md` (§10) with a deeper, evidence-traced diagnosis of D3 and D5 specifically — the underlying alpha/agreement/variance figures are unchanged, only the interpretation is deepened.
**Author:** Samiksha Dhere (researcher) — analyzed with Claude Code assistance

**What this document does not do:** it does not claim "ALCSM is fully reliable." It does not modify D1–D6, the scoring criteria, or the framework. It does not trigger a new scoring round — the diagnosis below explains what is already in the data, using disagreement patterns present in the existing double-coded subset.

---

## 1. Overall reliability result

Six separate Krippendorff's alpha values (ordinal), never pooled, never averaged into one figure:

| Dim | α | n (paired) | Observed/exact agreement | Rater A variance | Rater B variance | Categories used (A / B) |
|---|---|---|---|---|---|---|
| D1 | 0.944 | 72 | 81.9% | 2.549 | 2.667 | 6 / 6 |
| D2 | 1.000 | 27 | 100.0% | 0.000 | 0.000 | 1 / 1 |
| D3 | **0.102** | 75 | 54.7% | 1.387 | 0.312 | 5 / 3 |
| D4 | 1.000 | 26 | 100.0% | 0.391 | 0.391 | 3 / 3 |
| D5 | **0.246** | 75 | 85.3% | 0.085 | 0.357 | 2 / 3 |
| D6 | 1.000 | 75 | 100.0% | 0.889 | 0.889 | 5 / 5 |

**No dimension is declared invalid on alpha alone.** Reading variance, category use, and disagreement pattern alongside alpha (below) produces four qualitatively different situations, not one "low alpha = bad" verdict.

## 2. Low-variance diagnosis (Part 4) — distinguishing restricted range from real disagreement

| Dim | Modal-score share (A / B) | Diagnosis |
|---|---|---|
| D1 | 29.2% / 34.7% | **High information.** Wide spread, no restriction, both raters use the full 0–5 scale. Alpha reflects genuine, well-supported agreement. |
| D2 | 100.0% / 100.0% | **Degenerate zero-variance.** After excluding the 48 unavailable cases, every remaining rating from both raters is exactly `1`. Alpha = 1.0 is a mathematical artifact of zero observed and zero expected disagreement (Krippendorff's own defined convention for this case), not evidence of strong discrimination. Nothing was discriminated because nothing varied. |
| D3 | 45.3% / 85.3% | **Not a low-variance case.** Rater A's own variance (1.387) is the second-highest of any dimension in this subset — Rater A is clearly discriminating across a real range. The low alpha comes from Rater B's much narrower use of the scale (variance 0.312, only 3 of 6 categories) **combined with systematic disagreement between the two raters** (§3 below) — this is genuine rater disagreement, not "nothing to disagree about." |
| D4 | 69.2% / 69.2% | **Restricted range, but genuine (non-degenerate) agreement.** Only 26 paired units (49 of 75 unavailable), 3 categories used, but real spread exists (not zero variance) and both raters' distributions are identical. A milder version of D2's pattern — encouraging but based on a small, low-missingness-favorable sample. |
| D5 | 90.7% / 92.0% | **Primarily a low-variance/range-restriction case.** Rater A's variance (0.085) is the lowest of any non-degenerate dimension — Rater A scored 68 of 75 profiles as exactly `3`. This is the textbook "low variance deflates alpha despite high raw agreement" pattern (85.3% exact agreement, yet α = 0.246). Not the same failure mode as D3: here, the population itself is close to homogeneous on Rater A's side, so there is genuinely less for a chance-corrected statistic to reward. |
| D6 | 41.3% / 41.3% | **High information**, matching D1 — full range, identical distributions, no restriction. |

**Explicit answer to this session's Objective, per dimension:**

- **D3's low alpha is (A) genuine coder disagreement, not (B) a variance artifact, not (C) missing-data treatment, and only negligibly (D) a second-rater-encoding effect.** Rater A's own variance rules out "nothing to discriminate"; the disagreement is systematic and one-directional (§3).
- **D5's low alpha is primarily (B) a low-variance/range-restriction artifact on Rater A's side, with a smaller but real (A) substantive disagreement component layered on top** — i.e., a genuine combination (E), weighted toward (B).
- **(C) missing-data treatment plays no role in either dimension's alpha.** `Reliability_Subset_Verification_v1.2.md` Part 1 confirms the primary researcher recorded **zero** unavailable cases for D3 or D5 anywhere in this 75-profile subset — the unavailable-inference mechanism that affects D1/D2/D4 never touches D3 or D5 at all.
- **(D) second-rater-workbook encoding has at most a negligible residual effect on D3/D5**: each dimension has exactly one profile where the friend recorded a raw `0` that does not coincide with any Rater-A-unavailable flag (so it was kept as an observed score, per the documented rule) — 1 of 75 cases (1.3%) per dimension. This cannot explain the ~20–34 disagreeing cases in either dimension; it is reported as a genuine but minor residual ambiguity, not a driver.

## 3. D3 disagreement diagnosis (Part 3 + Part 5)

**The single most important fact about D3's disagreements: they are 100% one-directional.** Every one of the 34 disagreeing cases has **Rater B scoring higher than Rater A** — zero cases run the other way (`D3_D5_Disagreement_Analysis_v1.0.xlsx`, `Profile_Level_Disagreement` sheet). This is a systematic calibration difference between the two raters, not noisy scatter.

| Score pair (A → B) | n | % of disagreements |
|---|---|---|
| 3 → 4 | 18 | 52.9% |
| 1 → 4 | 11 | 32.4% |
| 1 → 3 | 4 | 11.8% |
| 2 → 4 | 1 | 2.9% |

Only 24.0% of D3 disagreements are exactly one ordinal point apart — the majority are 2–3 points apart, i.e., substantial, not borderline rounding.

**Two distinguishable sub-patterns emerge from reading the evidence text directly:**

1. **The 1→3/1→4 cases (15 of 34, 44%) — title-based inference vs. duration threshold.** These profiles typically show a senior-sounding AI title (`"Head of AI Regulatory Compliance Governance"`, `"Director of Artificial Intelligence"`, `"Global Director AI Automotive..."`) attached to a **short individual tenure** (2–10 months). Rater A appears to apply the duration threshold strictly (D3's own rubric: 1 = "AI-adjacent role only"; 4 requires "3+ yrs AI/ML, or 1–2 yrs with ownership language") and does not credit a brief tenure regardless of title. Rater B appears to credit these more generously — consistent with **title-based inference**: reading a senior AI title as sufficient evidence of practical ownership even when the stated duration is short.
2. **The 3→4 boundary cases (18 of 34, 53%) — this is the literal "boundary between score 3 and 4" this task asks about, and it dominates the disagreement count.** These profiles typically show **longer, and often multiple, listed AI-related roles** (durations of 16–167 months, frequently two or more separate AI-titled positions for the same person). Rater A appears to have scored from the single most relevant listed role rather than the cumulative pattern across roles; Rater B's higher score is consistent with crediting the **cumulative total of AI-related experience** across multiple listed positions, which the D3 rubric's "3+ yrs AI/ML" criterion for a 4 does not explicitly say how to compute when a profile lists several separate AI roles.

**Dominant disagreement pattern: a genuine, systematic difference in how "AI experience duration" is computed and how much weight a senior AI-related title carries on its own — not a distinction between AI-related and generic roles (both raters agree these roles are AI-related; the disagreement is about degree), and not a practical-ownership-language dispute in the sense of ambiguous wording.**

**Recommendation for how the thesis should report this:** report D3 as a **limited-reliability dimension with an identified, specific cause** — not a vaguely "unreliable" dimension. State plainly: (a) the disagreement is entirely one-directional, suggesting the two raters differ in how strictly they apply the duration/ownership threshold rather than disagreeing randomly; (b) the majority of the disagreement concentrates at the 3/4 boundary, specifically around whether multiple listed AI roles should be summed; (c) this is a rulebook-clarity finding (how to compute cumulative duration across multiple listed roles is not explicitly specified), not evidence that the underlying construct is unmeasurable. **D3 is not modified in this session** — this diagnosis is offered as a candidate explanation for a future rulebook wording clarification, not an instruction acted on now.

## 4. D5 disagreement diagnosis (Part 3 + Part 6)

D5's 11 disagreements are **bidirectional** (6 Rater-A-higher, 5 Rater-B-higher) — a materially different character from D3's one-sided pattern, and consistent with §2's "primarily range-restriction" diagnosis rather than a systematic calibration gap.

| Score pair | n | Direction |
|---|---|---|
| 2 → 3 | 5 | Rater B higher |
| 3 → 1 | 3 | Rater A higher |
| 2 → 1 | 2 | Rater A higher |
| 3 → 0 | 1 | Rater A higher |

90.7% of paired units land on Rater A's single modal value (3); disagreement only surfaces at the edges of that concentration. 93.3% of all D5 pairs agree exactly or are one point apart — the 3→0 case is the one clear outlier (see below).

**Reading the evidence text for the disagreeing cases:**

- **The `2 → 3` cases (Rater B higher, 5 cases)** all carry VP-level titles with an explicit AI/strategy scope in the title itself (`"Vice President & Chief of AI for SAP BTP Fabric"`, `"Vice President Project House AI"`, `"Vice President - AI Innovation & Digital Employee Experience"`). D5's rubric places "Manager-level, team-scope" at 2 and "Director/Head, some strategic language" at 3 — these are exactly **VP/Director boundary cases**, where Rater A reads the title as management-scope and Rater B reads the same title's explicit strategic/domain-ownership framing ("Chief of AI for...", "Project House AI") as crossing into strategic-language territory.
- **The `3 → 1`/`3 → 0` cases (Rater A higher, 4 cases)** include `"Head of Artificial Intelligence"` + `"Group Manager Artificial Intelligence"` (scored 3 by Rater A, 0 by Rater B) and `"Vice President Operations"` + `"Director Finance Analytics & Consulting"` (3 vs 1). These are cases where Rater A credited a Head/Director/VP title with "some strategic language" (D5's score-3 criterion) while Rater B appears to have required more explicit strategic-framing text than the title alone provides — the `"Group Manager"` case is specifically a **Global/Group-scope title** that the two raters read very differently (one as clear leadership signal, the other as insufficient).

**Dominant disagreement pattern: Director/Head/VP boundary judgment calls, specifically about how much weight a title's own wording (e.g., "Chief of AI for X," "Group Manager") carries as "strategic language" versus requiring separately stated strategic responsibility text.** This is a narrower, more genuinely ambiguous judgment call than D3's issue — it is not one-directional, and it sits on top of an already range-restricted, high-agreement dimension.

**Recommendation for how the thesis should report this:** report D5 as a dimension where **alpha is substantially deflated by range restriction** (85.3% raw agreement against α = 0.246) **and** where the residual real disagreement concentrates specifically at Director/Head/VP boundary judgments about title-embedded strategic language. This is best framed as **substantive ambiguity in a higher-order, lower-verifiability construct** (D5 is documented as "low" verifiability in the dimension config, unlike D1's "high") rather than as evidence the dimension fails — the raw agreement rate argues against "fails," while the alpha figure alone, unexplained, would overstate the problem.

## 5. Per-dimension interpretation (careful language, as instructed)

1. **D1 — Formal Education.** Strong reproducibility (α = 0.944). Wide range, high variance, both raters discriminating similarly across the full scale. No qualification needed beyond the normal caveats of a single 75-profile, one-second-rater subset (§7 of `Reliability_Report_v1.1.md`).
2. **D2 — Professional Certifications.** Perfect observed agreement, but on a degenerate zero-variance sample (100% of paired ratings are the same single value). **Not evidence of strong discrimination** — there was nothing to discriminate in this particular subsample. A population-wide property (D2's real range is only 0–1 across all 500 profiles), not new to this subset.
3. **D3 — Practical AI Experience. Limited reliability, with an identified cause: a systematic, one-directional calibration difference in how cumulative AI-related experience and senior-title-implied ownership are weighted**, concentrated at the 3/4 score boundary. Not random noise; not explainable by missingness or encoding.
4. **D4 — Technical Contributions.** Perfect agreement on a small (26-unit), moderately restricted-range sample. Encouraging, genuinely non-degenerate (3 categories, real variance), but based on too little data (only 26 of 75 profiles have any D4 evidence at all) to claim strong reliability with confidence.
5. **D5 — Leadership & Strategic Responsibility. Limited reliability, primarily driven by range restriction on top of a genuinely harder, lower-verifiability construct.** High raw agreement (85.3%) but low alpha because Rater A's ratings are heavily concentrated; the real disagreement that does exist is a specific, identifiable Director/Head/VP boundary judgment about title-embedded strategic language, not scattered noise.
6. **D6 — AI Industry/Application Breadth.** Strong reproducibility (α = 1.000, non-degenerate — full range, 5 categories, identical distributions). Alongside D1, the strongest evidence of reliable independent scoring in this subset.

## 6. Overall conclusion for RQ3

**ALCSM's reliability evidence, from this one 75-profile double-coded subset with one independent second rater, is dimension-dependent, not uniform, and this is reported as a genuine structural finding, not a weakness to be smoothed over.** Strong reproducibility is demonstrated for **D1, D4, and D6** (D4 with the caveat of a small usable sample). **D2 and D4's ceiling-case perfect agreement reflects low variance, not strong discrimination**, and should not be cited as if it were the same kind of evidence as D1's or D6's. **D3 and D5 show limited reliability, for two different and now-identified reasons**: D3's is a systematic, one-directional scoring-calibration difference concentrated at a specific score boundary; D5's is primarily a range-restriction effect layered with a narrower substantive ambiguity in how title-embedded strategic language is read. **ALCSM is not claimed to be "fully reliable"** — this evidence supports treating it as a formative index whose easier-to-verify dimensions (formal credentials, industry breadth) reproduce well under independent double coding, while its higher-order, judgment-dependent dimensions (practical experience depth, leadership scope) show real, specific, diagnosable reproducibility limits that a future rulebook revision — not attempted in this session — could plausibly narrow.

---

*Sources: `Reliability_Report_v1.1.md`, `Reliability_Results_v1.1.xlsx`, `Reliability_Subset_Verification_v1.2.md`, `D3_D5_Disagreement_Analysis_v1.0.xlsx`. No canonical source file was modified. D1–D6, their definitions, and their scoring criteria are unchanged.*
