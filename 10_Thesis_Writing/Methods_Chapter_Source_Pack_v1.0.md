# Methods Chapter Source Pack v1.0

**Purpose:** organized, cited raw material for Chapter 3 (Methods). Each subsection lists claims actually supported by an existing project document, with the exact source cited. **This is a source pack, not finished prose** — turn each bullet into thesis sentences in your own academic voice; do not copy verbatim without rewording. Items flagged **[NEEDS CITATION]** need an external literature reference this project's own documents don't supply. Items flagged **[NEEDS RESEARCHER INPUT]** need a fact only you can supply (a date, a name, a confirmation) — do not guess these.
**Author:** Samiksha Dhere (researcher) — prepared with Claude Code assistance

---

## 3.1 Research design

- Mixed-methods empirical audit: a structured human/AI-assisted annotation exercise (ALCSM scoring of 500 LinkedIn profiles), a comparative document analysis (LinkedIn profiles vs. job postings), a measurement-validation component (expert survey + inter-rater reliability), and an exploratory computational component (NLP baseline). Source: overall project structure, `RQ_Data_Mapping_v1.1.md`.
- No experimental manipulation, no random assignment — this is an observational, descriptive-and-comparative design throughout RQ1/RQ2, a measurement-reproducibility design for RQ3, an unrealized correlational design for RQ4, and a supervised-learning evaluation design for RQ5. Source: `Canonical_Analysis_Outputs_Register_v1.0.md`, per-RQ "Primary analysis" column.
- **[NEEDS RESEARCHER INPUT]** Formal research-design classification/terminology (e.g., how your department wants "mixed-methods," "sequential," etc. labeled) is a wording choice for you, not something the project documents dictate.

## 3.2 Research questions

Five research questions, stated exactly as used throughout the analysis outputs (source: `RQ_Data_Mapping_v1.1.md`, every `RQ{n}_Final_Results`/`Final_Status` document's own header):

- **RQ1:** What credential patterns exist among self-identified AI leaders, as observable on LinkedIn?
- **RQ2:** How do stated job-posting requirements compare to the credential signals held by AI leaders on LinkedIn?
- **RQ3:** How can ALCSM be constructed and validated as a measurement instrument?
- **RQ4:** Do ALCSM credential signals correlate with observable professional impact?
- **RQ5:** Does a human-vs-machine comparison of NLP-predicted ALCSM scores against the human gold standard reveal usable automated-scoring signal?

## 3.3 Data sources

Four primary data sources, none overlapping in purpose (source: `Canonical_Analysis_Outputs_Register_v1.0.md`):

1. 500 LinkedIn profiles (processed workbook) — RQ1, RQ5 feature input.
2. 201 job postings / 1,558 requirement records — RQ2.
3. The frozen human annotation (3,000 profile×dimension scores) — gold standard for RQ1, RQ3 (reliability comparison side), RQ5.
4. Expert survey (N=24) — RQ3 content-assessment evidence.

## 3.4 LinkedIn profile dataset

- **Sampling frame:** purposive, title-gated, non-probability sampling — individuals publicly presenting a qualifying AI-leadership title on LinkedIn (e.g., Chief AI Officer, Head of AI, VP of Machine Learning). Explicitly **not** a random or representative sample; this must be stated as a limitation, not implied otherwise. Source: `05_Data_Collection/Documentation/Task5_P3_Sampling_Framework_Design.md` §1–§2.
- **Inclusion rule:** exact match or documented variant match to a pre-registered title list; publicly viewable; in-scope language; not already in the sample. Source: same document §3–§4.
- **Collection organized in batches**, one `sampling_batch` row per documented, reproducible search query, never one undocumented sweep. Source: same document §2.
- **Target size:** ~500 profiles (met). Source: same document §2; `Final_Annotation_Audit_v1.1.md` confirms exactly 500 in the frozen dataset.
- **Processed dataset structure:** `Profile_Master`, `Education`, `Certification`, `Professional_Experience`, `Technical_Contribution` sheets. Source: directly inspected in `NLP_Baseline_Report_v1.0.md` Part 1, `RQ1_Final_Results_v1.0.md`.
- **[NEEDS RESEARCHER INPUT / DISCREPANCY TO RESOLVE]** `05_Data_Collection/Documentation/Task5_P3_Sampling_Framework_Design.md`'s own header states "No real data has been collected under this framework" and "Status: Design document only" — but 500 real profiles were in fact collected and are the basis of the entire project. Either (a) this document was the design later executed largely as specified and its header is simply stale/never updated after collection began, or (b) actual collection deviated from this design in some way not documented elsewhere. **This should be confirmed by the researcher before citing this document as the authoritative account of how the real 500 profiles were actually sampled** — do not present this design document's procedure as a verified factual account of what happened without that confirmation.
- **[NEEDS RESEARCHER INPUT]** Exact collection date range, final pre-registered title list, and language-scope decision are marked `[INSERT]` in the source document and were never filled in there — needed for a complete Methods account.

## 3.5 Job posting dataset

- 201 postings, 1,558 individual requirement records extracted and mapped to D1–D6 or `NOT_DIRECTLY_MAPPED`. Source: `RQ2_Final_Results_v1.0.md` §1, direct counts from `ALCSM_JobPosting_Processed_v1.1.xlsx`.
- Requirement-level fields: `Requirement_Text`, `Requirement_Category`, `Mandatory_or_Preferred`, `Final_ALCSM_Dimension`. Source: `alcsm_rq2_analysis_v1.0.py` (direct schema inspection).
- Collection plan document exists (`05_Data_Collection/Documentation/Task5_P3_JobPosting_Collection_Plan.md`) — **[NEEDS RESEARCHER INPUT]** not read in full detail for this source pack; recommend reviewing it directly for the exact job-posting sampling procedure to cite alongside the profile sampling frame in §3.4.

## 3.6 ALCSM v1.1 framework

- Six dimensions, each scored 0–5 ordinal: D1 Formal Education, D2 Professional Certifications, D3 Practical AI Experience, D4 Technical Contributions, D5 Leadership & Strategic Responsibility, D6 AI Industry/Application Breadth. Full criteria table (all six score bands, all six dimensions) source: `02_Framework_Development/ALCSM_v1.1_Scoring_Framework.md` §1.
- D1–D5 unchanged from the frozen v1.0 framework (`ALCSM_v1.0_Scoring_Framework_Task3.md`); only D6 was replaced for v1.1, from "Professional Engagement & Continuous Development" to "AI Industry/Application Breadth," derived from the structured `Professional_Experience.Industry` field rather than posting-activity data (avoiding a platform-usage confound the original D6 risked). Source: `ALCSM_v1.1_Scoring_Framework.md` header and §1; `ALCSM_D6_Industry_Breadth_v1.1.md`.
- **No weights, aggregation function, or classification bands are defined anywhere in this framework or this project** — deliberately left open pending dedicated future validation. Source: `ALCSM_v1.1_Scoring_Framework.md` §2 ("Weights Left Open"), restated in every RQ output this session (e.g. `RQ1_Final_Results_v1.0.md` "What this document does not do").
- Verifiability gradient across dimensions is an explicit, documented design property: D1/D2/D4 high–medium verifiability; D3 medium; D5 low; D6 (v1.1) closer to the D1/D2/D4 tier than its predecessor. Source: `ALCSM_v1.1_Scoring_Framework.md` §1, "Verifiability annotation."

## 3.7 Formative measurement model

- ALCSM is specified as a **formative composite index** (indicators constitute the construct) rather than a **reflective scale** (construct causes interchangeable indicators) — citing Bollen & Lennox (1991), Diamantopoulos & Winklhofer (2001), Jarvis, MacKenzie & Podsakoff (2003). Source: `02_Framework_Development/ALCSM_Measurement_Model_and_Validation_Note.md` §1.1. **These three citations are already present in the source document and can be cited directly** — verify exact reference details against the original works before final submission.
- Direct consequence: internal-consistency reliability (Cronbach's alpha) is **not an appropriate criterion** for ALCSM and is never computed anywhere in this project. Source: same document §1.1, restated structurally in code comments throughout `src/alcsm/`.
- Hinkin (1998) is cited and explicitly re-scoped: its construct/item-development and reliability-discipline guidance is retained; its internal-consistency validation stage is explicitly **not** adopted, since it presupposes a reflective model. Source: same document §1.2. **[NEEDS CITATION VERIFICATION]** — confirm the exact Hinkin (1998) reference details for the bibliography.
- Inter-rater reliability (Krippendorff's alpha) remains appropriate under a formative model because it answers a different question (coding-procedure reproducibility) than internal consistency (co-variance among indicators) — citing Krippendorff (2004). Source: same document §1.3.
- Formal validation strategy for a formative index: content/theoretical validity (primary evidence), coding rulebook (reproducibility precondition), pilot annotation (reproducibility precondition), inter-rater reliability per dimension (reproducibility evidence, benchmarked against Landis & Koch 1977 conventions with the caveat that these are conventional, not uncontested). Source: same document §2.1–§2.4.

## 3.8 Data preprocessing

- Raw collected data is processed into structured Excel workbooks (`02_Processed/` folders) distinct from permanent `01_Raw/` archival evidence, which is never used as an analytical source directly. Source: `Document_Version_Policy.md` canonical register.
- Job-requirement text underwent a remapping pass to assign each requirement to D1–D6 or `NOT_DIRECTLY_MAPPED`; the methodology trail for this pass is archived (`16_Archive/Superseded_JobRequirement_Mapping/`), fully merged into the canonical file. Source: `Document_Version_Policy.md`.
- NLP baseline input construction (per-profile text document from five structured fields, excluding annotation-evidence fields) is a preprocessing step specific to RQ5, documented separately in §3.13.

## 3.9 Annotation procedure

- Two-stage process: (1) an AI-assisted first pass applying the frozen v1.0 rubric (D1–D5) and proposed v1.1 rubric (D6) mechanically and conservatively, with no LinkedIn browsing, no web research, no prestige assumptions, default-low under uncertainty; (2) full researcher review of every flagged case. Source: `Human_Annotation_Review_Protocol_v1.1.md` §1.
- First-pass workbook is permanently read-only, verified byte-identical (SHA-256) throughout; review happens in a separate workbook. Source: same document §2.
- **Review queue construction:** not every one of the 3,000 profile×dimension records needed review — the queue (685 rows, 425 profiles) was built from five explicit conditions (first-pass `Review_Required=YES`; `Confidence=LOW`; genuinely uncertain `unavailable` cases; a D6 label-ambiguity case; the three Professional_Experience-missing profiles), each verified directly against the first-pass data rather than assumed. Source: same document §5.
- **Reviewer decisions:** ACCEPT / CHANGE / DEFER, with every CHANGE requiring a corresponding `Review_Changes` audit-trail row in the same sitting. Source: same document §8.
- **Final outcome:** 28 retained score changes across the whole dataset (D5=22, D1=4, D3=2), zero unresolved cases. Source: `Final_Annotation_Audit_v1.1.md` §"28 retained score changes."
- Reviewing a profile's six dimensions together (not one dimension across many profiles) was the recommended practice, to reduce sequential-context bias. Source: `Human_Annotation_Review_Protocol_v1.1.md` §8, citing `ALCSM_Coding_Rulebook_and_Pilot_Design.md` §1.2.

## 3.10 Missing-data handling

- Four-state missing-data framework: `present`, `absent_stated`, `unavailable`, `not_applicable`. Only `present` and `unavailable` are actually used on the profile side in the frozen dataset (`absent_stated`/`not_applicable` defined but never triggered). Source: `alcsm.constants.MISSING_STATUSES`; `Final_Annotation_Audit_v1.1.md`.
- **Critical distinction, stated explicitly throughout every analysis this project produced:** an observed score of 0 (evidence was found and genuinely supports the lowest band) is never conflated with `unavailable` (no evidence exists to score at all) — enforced structurally in every analysis module (`alcsm.reliability.subset_workflow`, `alcsm.nlp.baseline`, `alcsm.analysis.rq1_descriptive`) and tested directly. Source: `ALCSM_Coding_Rulebook_v1.1_Addendum.md` §5 (D6-specific table, generalizing the project-wide rule); `RQ3_Reliability_Final_Interpretation_v1.0.md` §4 (Part 5 rule).
- Real-world example: LP0041, LP0170, LP0182 have zero `Professional_Experience` rows; D3 and D6 are coded `unavailable` (a data gap), not an observed 0. Source: `Final_Annotation_Audit_v1.1.md`.
- Population-wide unavailable rates: D1 5.8%, D2 53.2%, D3 0.6%, D4 65.0%, D5 0.0%, D6 0.6%. Source: `RQ1_Final_Results_v1.0.md` §2.
- Conservative default under genuine ambiguity: score/classify toward the lower band, never the higher, when uncertain. Source: `ALCSM_Coding_Rulebook_v1.1_Addendum.md` §6, §8 (D6-specific restatement of the parent rulebook's Principle 4).

## 3.11 Inter-rater reliability

- Design: deterministic, seeded 15% (75-profile) random subset of the 500-profile population, double-coded by the primary researcher (Rater A, the frozen final scores) and an independent second rater (Rater B), never the AI-assisted first pass. Source: `Reliability_Subset_Selection_Report.md`; `RQ3_Final_Results_Package_v1.0.md` §C.
- Statistic: Krippendorff's alpha, ordinal metric, computed **separately per dimension, never pooled**. Source: `Reliability_Report_v1.1.md`; `alcsm.reliability.krippendorff` (validated against Krippendorff's own published worked example to within 0.001).
- A profile×dimension unit is included in a dimension's alpha only if **both** raters recorded an observed (non-unavailable) score for it — an unavailable case is excluded, never coerced to 0. Source: `Reliability_Subset_Verification_v1.2.md` Part 1.
- Bootstrap 95% confidence intervals (2,000 resamples, seed 42) reported alongside each alpha. Source: `alcsm.reliability.krippendorff.bootstrap_alpha_ci`; `Reliability_Results_v1.1.xlsx`.
- Results (all six, non-pooled): D1 α=.944, D2 α=1.000 (degenerate), D3 α=.102, D4 α=1.000 (degenerate), D5 α=.246, D6 α=1.000. Source: `RQ3_Final_Results_Package_v1.0.md` §C.
- **Data-provenance note requiring careful, honest wording in the thesis**: the second rater's completed scores were recovered from a workbook sheet whose column headers were not updated to reflect their new content (documented fully in `Reliability_Subset_Verification_v1.1.md`/`v1.2.md`); confirmed with the researcher to be genuine independent scoring, not corruption. **[NEEDS RESEARCHER INPUT]** — decide how much of this data-handling detail belongs in the thesis Methods text itself versus only in supporting documentation; at minimum, the "unavailable status for the second rater was inferred from the primary rater's own missing-status flags, not independently encoded" limitation (§4 of `Reliability_Subset_Verification_v1.2.md`) should be stated as a methodological limitation.

## 3.12 Expert survey

- N=24 consented respondents (of the raw export; all 24 rows had consent recorded). Source: `Survey_Status_Report_v1.0.md`; `ALCSM_Survey_Analysis_Processed_v1.0.xlsx`.
- Instrument: relevance (1–5) and clarity (1–5) ratings per dimension, an overall framework-appropriateness rating (1–5), a most-important-dimension single-choice item, a distinctiveness rating per dimension (0% answered — an instrument limitation), and an open "missing signal" free-text item (content never read into any automated analysis — only presence/absence of a comment is counted). Source: `Survey_Analysis_Plan_v1.0.md` §2; `alcsm.analysis.survey` module docstring.
- Consent filter: only rows where the consent column exactly equals the stated consent string are retained. Source: `alcsm.analysis.survey.reshape_survey_responses`.
- Explicit scope: content-assessment evidence only — not predictive validation, not competence validation, not population inference (self-selected N=24), not internal consistency, not factor analysis. Source: `Survey_Analysis_Plan_v1.0.md` §1.
- **[NEEDS RESEARCHER INPUT]** Recruitment method/channel for survey respondents is not documented in any project file found for this source pack — needed for a complete Methods account of the survey sample.

## 3.13 NLP baseline

- Architecture: TF-IDF (unigrams+bigrams, 2,000-term vocabulary cap, min document frequency 2) + Ridge regression (continuous prediction, rounded and clipped to [0,5]) — chosen as the "simplest defensible baseline," explicitly preferred over a heavier architecture per this project's own stated priority (working, reproducible, interpretable over sophisticated-and-unfinished). Source: `NLP_Baseline_Report_v1.0.md` Part 2.
- Input: a per-profile text document built only from raw processed fields (title, industry, company size, title category, education, certifications, experience job titles/industry/tenure-bucket/leadership/AI-relatedness flags, technical contributions) — explicitly excluding the annotation's own Evidence/Rationale/Confidence/Decision text, to avoid leaking label justification into the model input, and matching the same underlying information a human annotator had. Source: `NLP_Baseline_Report_v1.0.md` Part 1.
- Six independent per-dimension models, never a composite prediction. Source: same document Part 3.
- Reproducible seed=42; per-dimension stratified 80/20 train/test split (stratified where every score category has ≥2 members; documented fallback to plain random split for D3, whose present-only population has exactly one profile scored 0). Source: same document Part 5.
- Leakage discipline: TF-IDF vectorizer and Ridge model both fit on training data only; test data only ever transformed, never used to fit. Source: same document Part 6.
- Evaluation: exact-match rate, mean absolute error, linear-weighted Cohen's kappa, full confusion matrix, each compared against a majority-class baseline. Source: `alcsm.nlp.evaluate` module (pre-existing, reused unchanged).

## 3.14 Ethical and data protection considerations

**This subsection requires the most careful, honest wording in the entire Methods chapter — do not overstate approval status.**

- **Formal institutional ethics-committee approval has not been documented anywhere in this project as of the current state of the repository.** This finding (GOV-01) was first raised in `P3_Final_Data_QA_Report.md` and remains **explicitly open** in `DECISION_LOG.md` (most recent restatement: "General ethics/DPO approval status is undocumented... Status: Pending author confirmation"). **[NEEDS RESEARCHER INPUT — CRITICAL]**: before finalizing the thesis Methods chapter, confirm the actual, current, real-world ethics/DPO approval status with your institution and supervisor, and word this subsection to reflect the true state, not the state as last recorded in this repository — this is exactly the kind of fact this project's own documents cannot verify for you.
- A thesis supervisor is recorded as having reviewed the ethics documentation package informally and given a positive indication to proceed, **explicitly not described as, and not equivalent to, formal ethics-committee approval**. Source: `DECISION_LOG.md` D-0036; `04_Ethics/07_Institutional_Correspondence/ALCSM_Ethics_SupervisorReviewRecord_v0.1-DRAFT.md` (itself still marked DRAFT with unfilled placeholder fields for meeting date/supervisor name).
- Full draft ethics package exists (application, DPIA screening + full DPIA, legitimate-interest assessment, privacy notice, GDPR compliance checklist, data management plan, LinkedIn collection protocol, survey consent materials) — **every one of these documents is explicitly marked `v0.1-DRAFT`, "not yet submitted, not yet reviewed, not yet approved."** Source: `04_Ethics/` directory, each document's own header.
- No individual is identifiable by direct identifiers in any analytical dataset used in this thesis — verified by direct regex scan for email/URL patterns across the entire frozen annotation workbook (zero matches). Source: `Final_Annotation_Audit_v1.1.md`.
- Survey consent: only respondents whose consent column exactly matches the required affirmative string are included in any analysis; free-text comment content is never read into any automated analysis pipeline (structural guarantee, tested). Source: `alcsm.analysis.survey` module, §3.12 above.

## 3.15 Analytical methods

Summary list, each detailed in its own subsection or RQ-specific document:

- Descriptive statistics (means, medians, standard deviations, frequency/cross-tabulations) — RQ1, RQ2. No inferential/significance testing anywhere in this project.
- Krippendorff's alpha (ordinal), bootstrap confidence intervals — RQ3 reliability.
- Descriptive survey statistics (means, medians, counts) — RQ3 content-assessment.
- Supervised regression (Ridge) with ordinal-appropriate evaluation (exact-match, MAE, linear-weighted Cohen's kappa) — RQ5.
- No composite score, weighting, or classification band is computed anywhere in this project — a standing, deliberate, repeatedly-stated methodological position, not an oversight. Source: every RQ document's "What this document does not do" section.

## 3.16 Limitations

Consolidated from every RQ-specific limitation section (full detail in each; do not re-derive, cite the specific document per limitation in the thesis text):

- Non-probability, title-gated sampling frame for LinkedIn profiles — not representative of any defined population (§3.4).
- Single 75-profile reliability subset, single independent second rater — not a repeated-measures reliability program (§3.11).
- N=24 self-selected survey respondents — not population-representative; distinctiveness item unanswered by all 24 (§3.12).
- RQ4 could not be conducted — external criterion data never collected (`RQ4_Final_Status_v1.0.md`).
- NLP baseline is a linear, bag-of-words proof-of-concept — not evaluated with cross-validation, not a production system (§3.13).
- Formal ethics-committee approval status undocumented/unresolved as of the last recorded project state (§3.14) — **the single most important item in this list for you to personally resolve before submission.**

---

*This source pack introduces no new statistic and modifies no canonical source file. Every "NEEDS RESEARCHER INPUT" or "NEEDS CITATION" flag above marks a genuine gap this project's own documents cannot close — resolve these before treating the Methods chapter as final.*
