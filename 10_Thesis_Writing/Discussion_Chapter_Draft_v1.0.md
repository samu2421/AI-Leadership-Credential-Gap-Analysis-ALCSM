# Chapter 5: Discussion (Draft v1.0)

*Draft prose for the thesis Discussion chapter. Interpretive synthesis of the Results chapter (Chapter 4) — every factual claim here traces to a specific result already reported there; this chapter's own contribution is interpretation, explicitly flagged as such where it goes beyond the directly measured figures.*

---

## 5.1 ALCSM as a formative measure

This thesis constructed and evaluated ALCSM as a **formative index**: six distinct, non-interchangeable observable credential signals rather than reflective indicators of one latent "AI leadership" trait. The results are broadly consistent with this design choice. No cross-dimension correlation, internal-consistency statistic, or composite score was computed at any stage of this project — deliberately, since a formative index's dimensions are not expected to correlate, and treating them as if they should (e.g., via Cronbach's alpha) would apply the wrong statistical framework to the construct as designed. The uneven distributional shapes observed across D1–D6 (Chapter 4, §4.2) — some dimensions spanning the full range, others range-restricted or concentrated — are consistent with six genuinely different underlying signals rather than six noisy measures of the same thing.

## 5.2 Strongest dimensions: D1 and D6

D1 (Formal Education) and D6 (AI Industry/Application Breadth) show the clearest, most consistent evidence of measurement reproducibility across this thesis's independent lines of evidence: the strongest non-degenerate inter-rater reliability (α = .944 and α = 1.000 respectively), full use of the nominal scoring range in the population data, and — for D1 — the clearest interpretable NLP signal among the more-observable dimensions. This convergence across independently conducted analyses (human double-coding, population-level distribution, automated baseline) is read as reasonably strong evidence that these two dimensions can be scored with acceptable reproducibility from LinkedIn-derived evidence, within the scope this thesis tested.

## 5.3 D3: the importance and the ambiguity of practical AI experience

D3 (Practical AI Experience) occupies a genuinely interesting position in this thesis's findings. It was rated the single most relevant and most frequently "most important" dimension by the expert survey respondents (§4.4), and it produced the strongest NLP baseline signal of any dimension (§4.6). At the same time, it showed the weakest human inter-rater reliability of any dimension (α = .102), traced in this thesis's reliability diagnosis to a systematic, one-directional disagreement in how two independent raters computed cumulative AI-related experience duration and weighed senior-title language, concentrated specifically at the 3→4 score boundary.

Taken together, this suggests D3 captures something both experts and an automated model can partially latch onto from surface evidence, while the precise rubric-level threshold for "enough" practical experience remains under-specified enough that two careful human coders reach different conclusions on the same evidence. This is read as a rulebook-wording finding, not a reason to doubt the underlying construct's relevance — the content-assessment and NLP evidence both suggest D3 is measuring something real and important; the reliability evidence suggests the current scoring criteria need clearer operationalization of "cumulative" experience across multiple listed roles, a specific, actionable finding for any future revision of the ALCSM coding rulebook (not attempted in this thesis).

## 5.4 D5: coding ambiguity at the leadership boundary

D5 (Leadership & Strategic Responsibility) presents a different kind of limitation. Its low inter-rater alpha (.246) is substantially explained by range restriction — the population is heavily concentrated at a single score (87.0% at score 3) — rather than by the raw disagreement rate, which was in fact comparatively high (85.3% exact agreement between raters). The residual disagreement that does exist concentrates at a specific, identifiable judgment call: whether a senior title's own wording (e.g., "Chief of AI for X," "Group Manager") should be read as sufficient "strategic language" on its own, or whether separately stated strategic-responsibility content is required. This is consistent with D5 being the only dimension coded "low" verifiability in this project's own dimension configuration, and is discussed here as a genuine construct-level ambiguity in how leadership scope is inferred from LinkedIn text, distinct from D3's more mechanical duration-threshold issue.

## 5.5 D6: a strong, asymmetric signal

D6 (AI Industry/Application Breadth) shows strong reproducibility on the profile side (§5.2) but reveals a striking asymmetry when compared against job-posting demand (§4.3, §5.6): it is observable in nearly every profile (99.4%) yet almost never explicitly requested in job postings (0.06% of requirement records). This asymmetry is not evidence against D6 as a construct — it plausibly reflects how job postings are conventionally written (industry breadth is rarely phrased as a discrete, checkable requirement the way a degree or certification is) rather than a flaw in scoring D6 from profile evidence. It does suggest that if ALCSM's dimensions were ever used to characterize *job market demand* rather than *candidate supply*, D6 would need a different evidentiary source than job-posting text.

## 5.6 Job-demand vs. profile-supply asymmetry (RQ2)

More broadly, the RQ2 findings show demand and supply signals do not move uniformly across dimensions. D5 and D3 show demand and supply pointing the same direction (both heavily represented on both sides); D2 shows both sides agreeing it is a comparatively minor signal; D6 shows the sharp one-sided asymmetry just discussed. Over half of all requirement text (51.3%) does not map to any ALCSM dimension at all, underscoring that job postings request many things — generic technical skills, communication ability — that this thesis's six-dimension AI-leadership-specific framework was never designed to capture, and this limitation is stated plainly rather than papered over by forcing those requirements into an ill-fitting dimension.

## 5.7 RQ4: a genuinely open question

This thesis does not provide criterion-validity evidence for ALCSM, because the necessary external professional-impact data (network reach, content engagement, recognition, seniority progression) was never collected. This is reported as a limitation of scope, not as a negative or null finding — whether ALCSM's dimensions correlate with observable professional outcomes remains an open empirical question this thesis is not positioned to answer, and is named explicitly as a direction for future data collection.

## 5.8 NLP baseline: promising but limited

The RQ5 baseline demonstrates that automated scoring is not uniformly out of reach for ALCSM's dimensions — D1 and D3 show genuine positive signal over a majority-class floor — but is also not close to a general solution. D2 and D5's high accuracy figures are explicitly not read as strong performance (both reflect a degenerate or heavily imbalanced target, discussed in §4.6); D4 and D6 underperform even trivial guessing. The most likely structural explanation for D6's weak performance — that counting distinct industries requires aggregating across a profile's full experience history, a capability a bag-of-words linear model does not have — points toward a specific, testable direction for a future, more structured feature representation, rather than a general indictment of the automation approach.

## 5.9 Limitations

Beyond the dimension-specific limitations already discussed: this thesis's reliability evidence rests on a single 75-profile subset scored by one independent second rater, not a repeated program of double coding; the expert survey drew on 24 self-selected respondents, not a representative sample of any defined population; the NLP baseline uses one train/test split per dimension rather than cross-validation, chosen deliberately to prioritize a working, interpretable, reproducible result within this thesis's time constraints over a more elaborate but unfinished evaluation design; and RQ4 could not be addressed at all for the reasons stated in §5.7. None of these limitations were resolved by expanding scope in this thesis — each is reported as a bounded, specific gap rather than smoothed over.

## 5.10 Future work

Directions for future research, none of which this thesis attempts: (1) a rulebook revision targeting D3's specific cumulative-duration-counting ambiguity and D5's title-language-vs-strategic-scope boundary, followed by a re-run of the same double-coding design to test whether reliability improves; (2) a dedicated data-collection pass for RQ4's external criterion variables; (3) a more structured NLP feature representation (e.g., one that can explicitly count or aggregate across a profile's listed experience entries) targeted specifically at D6 and D4's weaker baseline results; (4) an expert survey with a larger, more representative respondent pool and a redesigned distinctiveness item, given the 0% response rate observed here.

---

*Sources: Chapter 4 (Results) and its cited RQ-specific final-results documents. No canonical source file modified; no composite score, weight, or classification band computed anywhere. ALCSM is not described as "fully validated" anywhere in this chapter.*
