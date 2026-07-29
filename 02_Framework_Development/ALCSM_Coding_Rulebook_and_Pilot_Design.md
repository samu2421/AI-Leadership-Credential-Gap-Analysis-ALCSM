# ALCSM Measurement Protocol
### Coding Rulebook and Pilot Annotation Study Design (Pre-v1.0 Validation Stage)

**Scope note:** This document does not alter the six ALCSM dimensions, their draft 0–5 criteria, or their supporting literature (established in `ALCSM_Dimension_Design_Task2.md`). It also assigns no final dimension weights. Its sole purpose is to specify *how* the six dimensions should be applied consistently by human annotators, and *how* to test that consistency empirically, before the framework is formalized as v1.0. This sequencing follows Hinkin's (1998) established scale-development logic: item/criterion definition must be pilot-tested for reliability before a measurement instrument is finalized — you are currently between his "item generation" and "questionnaire administration/initial item reduction" stages, adapted here to a content-analytic coding task rather than a self-report survey.

Throughout, I mark each recommendation as either:
- **[ESTABLISHED]** — drawn directly from published methodological literature (cited), or
- **[THESIS-SPECIFIC]** — a decision I am proposing for your project that is not itself dictated by the literature and that you should be prepared to justify and defend independently.

---

# PART 1 — CODING RULEBOOK FOR HUMAN ANNOTATORS

## 1.1 Purpose and status of this rulebook

**[ESTABLISHED]** A codebook that operationalizes abstract constructs into explicit, rule-governed decision procedures is a standard precondition for reliable content analysis (Krippendorff, 2004, *Content Analysis: An Introduction to Its Methodology*, 2nd ed.). Without such a rulebook, disagreement between raters cannot be diagnosed as a rubric problem versus a rater-training problem.

**[THESIS-SPECIFIC]** This rulebook is written as a *living document*: version-controlled, dated, and revised only through the formal revision procedure in Part 2.6. Annotators must always code against the current version number, never from memory of an earlier draft.

## 1.2 General scoring principles

1. **Score what is written, not what is likely true.** **[ESTABLISHED]** This is the basic tenet of manifest-content coding in content analysis: coders record observable textual evidence, not inferred or assumed facts not stated in the text (Krippendorff, 2004). **[THESIS-SPECIFIC]** For ALCSM specifically: if a profile does not mention a Master's degree, score as if no Master's degree exists — even if the annotator personally happens to know (e.g., from external knowledge) that the person holds one. Score the *profile as an artifact*, not the *person*.

2. **One indicator, one piece of evidence, one score.** Each dimension's score must be traceable to specific text spans in the profile. Annotators log the exact phrase(s) that justify the assigned score (see coding log template, §1.6).

3. **Score independently per dimension.** Do not let a high score on one dimension "halo" another (e.g., an impressive PhD should not inflate the Leadership score). **[THESIS-SPECIFIC]** This is a deliberate methodological safeguard against halo-effect contamination across the six dimensions, and should be explicitly stated to annotators during training, not left implicit.

4. **Default to the lower score under genuine uncertainty.** **[THESIS-SPECIFIC]** Given that ALCSM's stated purpose is to detect credential *gaps* (i.e., overstatement of qualification), a conservative scoring default reduces the risk of the instrument itself inflating apparent credentials through generous interpretation. This is a deliberate, disclosed bias and must be reported as such in your Methods chapter — it is not a "neutral" default; state why you chose it.

5. **Do not average or split-score within a dimension.** Each dimension gets one integer 0–5 score per profile, not a fractional score. If evidence is genuinely mixed, use the tie-breaking procedure (§1.4), not an average.

## 1.3 Handling missing, ambiguous, or contradictory information

### Missing information
- If a dimension has **no evidence at all** in the profile, score it 0 for that dimension (per the existing scoring tables) and mark the coding log field `missing = TRUE`.
- **[THESIS-SPECIFIC]** Distinguish explicitly between "no evidence found" (score 0, `missing = TRUE`) and "evidence found indicating absence" (e.g., a profile stating "no formal AI education, self-taught practitioner" — also score low, but `missing = FALSE`, because the absence is a positive textual claim, not a data gap). This distinction matters for your later discussion of data completeness/missingness patterns across the 500-profile sample, and should be analyzed separately from substantive scoring results.

### Ambiguous information
- If wording is vague enough to plausibly support two adjacent score levels (e.g., "involved in AI strategy" — could be scope 2 or 3 on Dimension 5), annotators select the **lower** of the two candidate scores by default (consistent with Principle 4), and flag the case as `ambiguous = TRUE` with both candidate scores logged.
- **[THESIS-SPECIFIC]** Do not attempt to resolve ambiguity through external searching at this stage (see §1.4 on verification) — record the ambiguity as a rubric-quality signal first. A rubric that produces frequent ambiguity flags on a given dimension is itself pilot-study evidence that the criteria need refinement (see §2.5).

### Contradictory information
- If different parts of a single profile contradict each other (e.g., job title says "Chief AI Officer" but the "About" section describes only junior analyst-level tasks), **do not average or split the difference.** Score based on the most specific, most behaviorally concrete evidence available, per dimension, and log the contradiction explicitly (`contradiction = TRUE`, with both conflicting text spans quoted in the log).
- **[THESIS-SPECIFIC]** Title–substance contradictions of this kind are not coding errors to be resolved away — they are very likely your primary unit of analysis for the credential-gap findings. Flagging them systematically (rather than silently resolving them during coding) preserves them as data for Chapter 4/5 analysis. Consider adding a derived variable, e.g. `title_substance_contradiction_flag`, at the profile level, distinct from the six ALCSM dimension scores.

## 1.4 External verification: when allowed, and how documented

**[THESIS-SPECIFIC — this is a methodological decision unique to your project, not something the literature mandates uniformly; scale-development guidance (Hinkin, 1998) assumes self-report survey data where external verification isn't normally at issue, so you are extending established practice into new territory here and should say so explicitly.**

- **Default position:** external verification (e.g., checking a linked GitHub repository, searching for a claimed publication on Google Scholar, confirming a certification against a vendor's public registry) is **permitted only for Dimension 4 (Technical Contributions)**, because this is the one dimension where your own dimension design (Task 2) explicitly names external verification as a construct-validity enhancement.
- **Verification is not permitted** for Dimensions 1, 2, 3, 5, and 6 during main annotation, to keep the measurement consistent with what an automated NLP pipeline can actually access (LinkedIn text alone) — if annotators verify facts the NLP pipeline cannot verify, human-coded "gold standard" scores and machine-predicted scores would not be measuring the same construct, undermining your Task on NLP pipeline evaluation (RQ5).
- **Documentation requirement when verification is used (Dimension 4 only):** annotators must log (a) what was verified, (b) the external source/URL consulted, (c) the date of verification, (d) whether verification confirmed, contradicted, or could not confirm the profile's claim. Unconfirmed claims are scored as if unverified (i.e., verification can only leave a score unchanged or lower it via a discovered contradiction — it should not be used to *inflate* a score beyond what the profile text itself would support, since inflating on the basis of information invisible to the automated pipeline would again break score comparability).

## 1.5 Tie-breaking rules and difficult cases

**[ESTABLISHED]** Formal tie-breaking and adjudication procedures for disagreement between independent coders are standard in content-analysis methodology (Krippendorff, 2004); the specific procedure below is my recommendation adapted to your two-rater pilot design.

1. **Minor disagreement (scores differ by 1 point on a 0–5 scale):** the two raters discuss briefly and attempt consensus. If consensus is reached, log the consensus score and the reason for the initial discrepancy. If not, escalate to Rule 3.
2. **Major disagreement (scores differ by 2+ points):** do not attempt informal consensus first. Escalate directly to Rule 3 — a 2+ point gap on a 0–5 scale usually signals a rubric ambiguity, not a simple judgment call.
3. **Escalation:** a third party (thesis supervisor, or you acting as adjudicator with your reasoning documented) reviews the specific text span and both raters' logged justifications, and assigns a final adjudicated score. The adjudication reason is added to the coding log — never silently overwritten.
4. **Systematic disagreement pattern:** if the *same type* of case produces disagreement across multiple profiles (e.g., every "Head of Data & AI" title produces a split between Dimension 5 scores of 2 and 4), this is not a series of isolated ties — it is evidence the rubric criterion itself needs revision (see §2.5), and should trigger a rubric-revision review rather than repeated case-by-case adjudication.

**Illustrative difficult cases (constructed examples for annotator training, not real profiles):**

- *Case A — Credential inflation via title only:* Profile lists title "AI Strategy Director" with an "About" section entirely about general project management, no AI-specific language anywhere. → Dimension 5 scored on title-seniority sub-criterion only (moderate), but overall profile should be flagged `contradiction = TRUE` for later credential-gap analysis.
- *Case B — Under-signaled genuine expertise:* Profile has minimal LinkedIn text, no listed certifications, but links to an active, well-documented GitHub repository of applied ML tools. → Certifications (Dimension 2) scored low per visible profile text (per Principle 1); Technical Contributions (Dimension 4) scored using the permitted external-verification pathway, since the GitHub link is himself part of the profile's own linked content, not an independent web search. Document this distinction clearly for annotators: *following a link the profile itself provides* is different from *searching the web for corroboration* — the former is within-profile evidence, the latter is the restricted "external verification" pathway defined in §1.4.
- *Case C — Field-adjacent but not AI-specific credential:* A PhD in Applied Statistics with no explicit AI/ML coursework or thesis topic mentioned. → Score conservatively per Principle 4 (lower of plausible scores: likely a 3, not a 4/5, per the Dimension 1 table), and flag `ambiguous = TRUE` since "Applied Statistics" sits close to the AI/ML boundary defined in your Dimension 1 taxonomy.

## 1.6 Coding log template

**[THESIS-SPECIFIC]** One row per profile per dimension (i.e., 6 rows per profile). Recommended fields:

| Field | Description |
|---|---|
| `profile_id` | Anonymized/pseudonymous profile identifier (never store real names in the coding log — see your Ethics documentation) |
| `dimension` | 1–6 |
| `rater_id` | Coder identifier (Rater A / Rater B) |
| `score` | Integer 0–5 |
| `evidence_text` | Verbatim short text span(s) from the profile supporting the score (keep brief — this is your working file, not a publishable quotation; do not reproduce large blocks of profile text) |
| `missing` | TRUE/FALSE (per §1.3) |
| `ambiguous` | TRUE/FALSE, plus both candidate scores if TRUE |
| `contradiction` | TRUE/FALSE, plus conflicting text spans if TRUE |
| `verification_used` | TRUE/FALSE (Dimension 4 only; all others must be FALSE by rule) |
| `verification_source` | URL/source, date (if `verification_used` = TRUE) |
| `notes` | Free-text field for anything not captured above |
| `timestamp` | Date/time of coding |

---

# PART 2 — PILOT ANNOTATION STUDY DESIGN

## 2.1 Purpose

**[ESTABLISHED]** Before large-scale data collection, a small pilot with independent raters is standard practice for establishing that a coding instrument produces reliable (reproducible) measurements — this is precisely the step Hinkin (1998) and Krippendorff (2004) both treat as a precondition for trusting subsequent large-N results. **[THESIS-SPECIFIC]** For your 500-profile main study, I recommend this pilot precede any large-batch annotation or NLP model training, since both downstream stages depend on having a stable, reliable human "gold standard."

## 2.2 Profile selection criteria (10–20 profiles)

**[THESIS-SPECIFIC — sampling for a reliability pilot serves a different goal than sampling for your final 500-profile study, and should not be treated as a miniature random sample of your target population.** A pilot should deliberately include difficult cases, not just typical ones, in order to stress-test the rubric.

Recommended composition for a 15-profile pilot (adjust proportionally for 10 or 20):
- **4–5 "clear" profiles**: unambiguous high or low scores across most dimensions, to confirm baseline agreement is achievable at all.
- **4–5 "boundary" profiles**: profiles that plausibly sit on a scoring boundary for at least one dimension (e.g., Bachelor's vs. Master's ambiguity, Director vs. VP title ambiguity).
- **3–4 "contradiction" profiles**: profiles with a visible title–substance mismatch, deliberately selected because your dimension design (Task 2) flags this as the core phenomenon of interest.
- **2–3 "sparse" profiles**: minimal profile content, to test the missing-data procedures in §1.3.

**[THESIS-SPECIFIC]** Do not select pilot profiles randomly from your eventual 500-profile sampling frame if that frame is not yet finalized — select purposively for rubric stress-testing, and state this sampling rationale explicitly in your thesis (purposive pilot sampling vs. probabilistic main-study sampling are different, both legitimate, and must not be conflated in your write-up).

## 2.3 Annotation workflow for two independent raters

1. **Rater training session**: both raters review the current rulebook version and score 2–3 non-pilot practice profiles together, discussing discrepancies openly (this training round is *not* included in reliability calculations).
2. **Independent coding**: raters code all pilot profiles independently, with no communication about specific profiles during this phase. Each rater completes the full coding log (§1.6) for every profile.
3. **Blind cross-check**: scores are compared only after both raters have submitted complete logs for all pilot profiles — never dimension-by-dimension in real time, to avoid one rater's early scores anchoring the other's later judgments.
4. **Disagreement resolution**: apply the tie-breaking rules in §1.5.
5. **Reliability calculation**: performed on the raters' *independent, pre-adjudication* scores, not the post-adjudication consensus scores (adjudicated scores would artificially inflate agreement statistics and defeat the purpose of measuring naturally occurring reliability).

## 2.4 Calculating inter-rater reliability separately per dimension

**[ESTABLISHED]** Reliability should be reported per-dimension, not pooled, because ALCSM's six dimensions have different verifiability profiles (as already established in Task 2's summary table) and pooling would mask this heterogeneity — a standard concern in multi-construct coding reliability reporting (Krippendorff, 2004).

- **Recommended statistic:** Krippendorff's alpha (α), computed separately for each of the six dimensions across the pilot profiles. Krippendorff's alpha is appropriate here because it (a) handles ordinal data correctly (your 0–5 scale is ordinal, not merely nominal), (b) tolerates the small sample size of a 10–20 profile pilot better than some alternatives, and (c) can handle any missing data cells (relevant given §1.3's missing-data procedure) (Krippendorff, 2004, *Content Analysis: An Introduction to Its Methodology*; see also Hayes & Krippendorff, 2007, *Communication Methods and Measures*, for computational guidance).
- **Alternative/supplementary statistic:** Cohen's weighted kappa (linear weighting, given the ordinal 0–5 scale) can be reported alongside alpha for readers more familiar with kappa (Cohen, 1960, *Educational and Psychological Measurement*).
- **Interpretation benchmarks [ESTABLISHED, with the caveat below]:** Landis & Koch's (1977, *Biometrics*, 33(1), 159–174) commonly cited benchmarks are: <0 poor, 0.00–0.20 slight, 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81–1.00 almost perfect. Krippendorff (2004, p. 241) separately suggests α ≥ .80 for confident conclusions, and treats .667 as a tentative lower bound for provisional conclusions.
  - **Important academic caveat you should state in your Methods chapter:** these benchmark tables are widely used but not universally endorsed — several methodologists (e.g., critiques cited in Landis & Koch discussions) argue the categorical labels ("moderate," "substantial") are somewhat arbitrary and that kappa/alpha values are sensitive to trait prevalence and rater bias, not purely to "true" reliability. State that you are using Landis & Koch/Krippendorff as conventional, widely cited reference points, not as an uncontested gold standard — this is the kind of nuance an examiner familiar with reliability statistics will expect you to know.
- **[THESIS-SPECIFIC] Minimum threshold decision for this project:** I recommend treating α ≥ .667 (Krippendorff's own "tentative" threshold) as the *minimum* bar for a dimension to proceed to main data collection without revision, and treating α ≥ .80 as the target for dimensions you intend to weight more heavily in Task 3. This threshold choice is a project-specific decision you are making, not a literature mandate, and should be justified in these terms in your thesis rather than presented as if it were an unambiguous external standard.

## 2.5 Criteria for deciding when a dimension or rubric requires revision

**[THESIS-SPECIFIC]** Building on the established reliability statistics above, I propose the following decision rule set for your project specifically:

| Pilot result for a given dimension | Action |
|---|---|
| α ≥ .80 | Rubric performs well; proceed to main data collection for this dimension as currently worded |
| .667 ≤ α < .80 | Acceptable for provisional/pilot conclusions, but review the disagreement cases for that dimension before scaling up; minor wording clarification recommended |
| α < .667 | Do not proceed to main data collection for this dimension; revise the rulebook wording (never the frozen scoring criteria) and re-pilot on a fresh (or partially overlapping) profile set |
| Any dimension where ambiguity/contradiction flags exceed ~30% of pilot profiles (regardless of α) | Treat as a rubric-clarity problem even if α happens to be acceptable — high flag rates suggest raters are reaching the same *scores* via inconsistent *reasoning*, which threatens construct validity even when it doesn't show up as disagreement |

Given the verifiability gradient already identified in Task 2 (Dimensions 1–2 high verifiability; Dimensions 5–6 low), you should **expect** lower alpha values for Dimensions 5 and 6 a priori. **[THESIS-SPECIFIC]** I recommend you state this expectation *before* running the pilot (as a pre-registered-style expectation in your thesis draft), so that a low alpha on Dimension 5/6 reads as a confirmed, anticipated limitation rather than an unexpected failure discovered post hoc — this materially strengthens the methodological credibility of your write-up.

## 2.6 Revision log template

**[THESIS-SPECIFIC]** To be completed any time a rubric wording, scoring boundary, or taxonomy (e.g., the certification taxonomy in Dimension 2) is changed as a result of pilot findings, before large-scale annotation begins.

| Field | Description |
|---|---|
| `revision_id` | Sequential identifier |
| `date` | Date of revision |
| `dimension_affected` | 1–6 |
| `rulebook_version_before` | Version number prior to change |
| `rulebook_version_after` | Version number after change |
| `trigger` | Which pilot finding prompted the change (e.g., "α = .52 on Dimension 5; disagreement clustered on Director vs. VP boundary") |
| `change_description` | Exact wording change made, ideally as a before/after diff |
| `rationale` | Why this specific change is expected to resolve the identified problem |
| `re-pilot_required` | TRUE/FALSE — whether the change is substantial enough to require re-testing reliability before proceeding |
| `approved_by` | Supervisor sign-off (recommended for MSc-level audit trail) |

**[THESIS-SPECIFIC]** Retain every version of the rulebook (not just the current one) in your project repository, with the revision log cross-referenced to specific rulebook versions. This gives you a defensible, transparent audit trail for your Methodology chapter and protects you if an examiner asks how or why the final rubric differs from your originally drafted Task 2 criteria.

---

## Summary of what remains open

This protocol deliberately does not:
- change any of the six ALCSM dimensions or their draft 0–5 criteria (per your instruction),
- assign dimension weights (reserved for Task 3),
- specify the mathematical form of the overall ALCSM score (also Task 3),
- resolve in advance what should happen if a dimension fails even after one rubric revision cycle (a second-pilot decision you may need to make empirically, once you have real pilot data in hand — I'd recommend deciding this only after seeing whether it actually occurs, rather than pre-committing to a hypothetical rule now).

I'll wait for your go-ahead before proceeding to Task 3 (ALCSM v1.0 scoring table, mathematical formula, annotation guidelines, and profile classification examples).
