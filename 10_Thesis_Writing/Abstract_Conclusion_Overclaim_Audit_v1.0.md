# Abstract + Conclusion Overclaim Audit v1.0

**Purpose:** line-by-line audit of `Abstract_Draft_v1.0.md` and `Conclusion_Draft_v1.0.md` against the final evidence, checking for overclaiming on six axes: validity, predictive ability, competence, effectiveness, NLP performance, generalisability. **No file was rewritten as part of this task** — corrections are recommended, not applied, per this task's explicit instruction.
**Author:** Samiksha Dhere (researcher) — audited with Claude Code assistance

---

## Overall finding

**Both drafts hold up well.** Neither claims ALCSM is validated, neither claims the NLP model predicts real-world competence or effectiveness, and neither claims the sample generalizes beyond this study. The explicit disclaimer "This thesis does not claim ALCSM is fully validated" (Abstract) and "ALCSM is not presented... as a fully validated instrument" (Conclusion) are exactly the framing this project has required throughout and should be kept verbatim.

Two moderate wording concerns were found in the Conclusion (none in the Abstract) — both are precision/calibration issues, not clear violations, and are reported as recommendations below.

## Abstract — clause-by-clause check

| Clause | Axis checked | Finding |
|---|---|---|
| "operationalized through... six independent, non-interchangeable 0–5 ordinal scores rather than a single composite score" | Validity | No overclaim — accurately states no composite exists. |
| "ALCSM's measurement properties were assessed through..." + full alpha table in prose | Validity, effectiveness | No overclaim — every figure matches `RQ3_Final_Results_Package_v1.0.md` exactly, degenerate cases explicitly flagged as degenerate. |
| "A planned criterion-validity analysis... could not be conducted... reported as an open limitation rather than an estimated result" | Predictive ability | No overclaim — explicitly disclaims any RQ4 result. |
| "evaluated against the human-coded gold standard as a proof-of-concept for automated ALCSM scoring, not a production system" | NLP performance, effectiveness | No overclaim — explicit production-readiness disclaimer present. |
| "D3 showed the strongest genuine signal (52.0% exact agreement, weighted κ = .399)... while D4 and D6 underperformed a majority-class baseline" | NLP performance | No overclaim — states the actual figures, does not characterize 52.0%/κ=.399 as "good" or "strong" in an absolute sense, only relative to baseline. |
| "This thesis does not claim ALCSM is fully validated" | Validity | Explicit, correct disclaimer — keep as-is. |
| No statement anywhere claims the 500-profile or 201-posting sample is representative or generalizable | Generalisability | No overclaim — silence here is appropriate for an abstract; the non-representativeness is stated in Methods, not required to be restated in the Abstract. |

**Minor, optional note (not an overclaim on the six audited axes):** the Abstract describes all 24 survey respondents collectively as "domain-expert survey respondents." The actual role breakdown includes one respondent in "Recruiter/talent/HR in technology" — arguably domain-adjacent rather than a technical AI/leadership expert in the same sense as the other 23. This is a precision-of-terminology point, not a validity/effectiveness/competence overclaim, and is flagged only for completeness. No correction required unless you want tighter wording.

## Conclusion — clause-by-clause check

| Clause | Axis checked | Finding |
|---|---|---|
| "six genuinely distinct dimensions rather than a single underlying trait" | Validity | No overclaim — directly supported by RQ1's differing distributions/missingness rates, consistent with the formative-index framing already established in `Methods_Chapter_Source_Pack_v1.0.md` §3.7. |
| "job-posting text as a data source is poorly suited to capturing some credential signals (D6 in particular)" | Generalisability | No overclaim — claim is about the data source, not about ALCSM or about job markets generally; directly supported by the 0.06% D6-mapping figure. |
| "two dimensions (D1, D6) show strong, well-supported reproducibility; two (D2, D4) show perfect but statistically uninformative agreement; and two (D3, D5) show specific, diagnosed reliability limitations" | Validity | No overclaim — accurate, appropriately differentiated, matches the six alpha values exactly. |
| "RQ4 remains genuinely open, owing to a data-collection gap rather than a negative finding" | Predictive ability | No overclaim — correctly avoids implying any correlation result. |
| **"The NLP baseline (RQ5) demonstrates that automated approximation of ALCSM scores is possible for some dimensions and not others"** | **NLP performance** | **Recommendation 1 (see below) — "demonstrates... is possible" reads slightly more confident than the underlying modest/mixed signal (D1 κ=.283, D3 κ=.399) supports.** |
| "the D3 result — strongest NLP signal, weakest human reliability — standing out as a finding worth further investigation rather than a resolved contradiction" | NLP performance | No overclaim — explicitly hedged as "worth further investigation," matches the interpretive-statement flag already recorded in `Final_Thesis_Evidence_Audit_v1.0.md` §8. |
| "ALCSM is not presented... as a fully validated instrument" | Validity | Explicit, correct disclaimer — keep as-is. |
| **"it tells a future user of ALCSM... precisely which dimensions can currently be trusted for what purpose"** | **Effectiveness, competence** | **Recommendation 2 (see below) — "can currently be trusted" implies an operational-use endorsement stronger than one reliability subset + one survey supports.** |
| "No composite ALCSM score, weighting scheme, or classification band was introduced at any point in this thesis" | Validity | No overclaim — accurate, reinforces the standing no-composite rule. |

## Recommended corrections (not applied — your decision)

**Recommendation 1 — soften the RQ5 summary sentence.**

> Current: *"The NLP baseline (RQ5) demonstrates that automated approximation of ALCSM scores is possible for some dimensions and not others..."*
>
> Suggested: *"The NLP baseline (RQ5) shows modest, dimension-dependent signal — genuine positive signal above a majority-class baseline for D1 and D3, no advantage over that baseline for D2, D4, D5, or D6 — with the D3 result..."*
>
> **Why:** "demonstrates... is possible" reads as a stronger claim of capability than a κ of .283–.399 on two dimensions supports; naming the actual pattern (2 of 6 dimensions show signal, matching Results §4.6/§4.9) is more precisely calibrated to the evidence and avoids a reader inferring "NLP works" as a general takeaway.

**Recommendation 2 — soften "can currently be trusted."**

> Current: *"...precisely which dimensions can currently be trusted for what purpose..."*
>
> Suggested: *"...precisely which dimensions currently have stronger versus weaker reproducibility evidence, and why..."*
>
> **Why:** "trusted... for what purpose" implies an operational-use recommendation (effectiveness/competence-adjacent framing) that this thesis's evidence base — one 75-profile reliability subset, one second rater, N=24 survey respondents — does not support making. "Reproducibility evidence" keeps the same substantive point (D1/D6 stronger, D3/D5 weaker) without implying a usage endorsement.

Both recommendations are wording-precision changes, not corrections of a factual error — nothing in either draft is false or contradicted by the evidence. Apply them, adjust the wording differently, or leave as-is; all three are defensible, and the choice is a voice/register decision for you as the author, not a data-integrity issue.

---

*No file was modified by this audit. `Abstract_Draft_v1.0.md` and `Conclusion_Draft_v1.0.md` remain exactly as they were.*
