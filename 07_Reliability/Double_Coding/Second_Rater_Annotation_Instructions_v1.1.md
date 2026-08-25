# Second Rater Annotation Instructions — ALCSM v1.1 Double-Coding Subset

**Purpose:** you have been asked to independently score a subset of 75 LinkedIn profiles using the ALCSM v1.1 scoring framework. Your scores will be compared against an existing, separately produced set of scores for the same 75 profiles to measure inter-rater reliability (Krippendorff's alpha, per dimension). **The comparison only has scientific value if your coding is genuinely independent** — please read this document in full before starting.

**Materials you should have received:**
- `Rater_A_Blank_Template.xlsx` (or a copy renamed for you specifically, e.g. `Rater_B_Blank_Template.xlsx`) — one row per profile, columns `Profile_ID, D1, D2, D3, D4, D5, D6`, all blank.
- Read-only access to the 75 profiles' LinkedIn content (via whatever source the researcher provides you — the processed workbook or original profile text), for the profiles listed in the template.
- The frozen ALCSM v1.1 framework documents (see §1 below).

**Materials you must NOT open or be shown before finishing:**
- `ALCSM_Reliability_Subset_75_v1.1.xlsx`'s `Existing_Scores_REFERENCE_ONLY` sheet, or any other record of how these 75 profiles were previously scored.
- `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx` in any form.

---

## 1. Use only the frozen v1.1 framework

Score strictly according to these three documents — do not use an earlier version, a personal interpretation, or a modified rubric:

- `02_Framework_Development/ALCSM_v1.1_Scoring_Framework.md` (D1–D5, unchanged from v1.0)
- `02_Framework_Development/ALCSM_D6_Industry_Breadth_v1.1.md` (D6, current proposed definition)
- `02_Framework_Development/ALCSM_Coding_Rulebook_v1.1_Addendum.md` (missing-status handling, D6 coding rules)

Each dimension is scored 0–5 against a fixed six-point criteria ladder. The ladders (for quick reference — the source documents above remain authoritative if anything here is ambiguous):

| Score | D1 Formal Education | D2 Certifications | D3 Practical AI Experience | D4 Technical Contributions | D5 Leadership & Strategic Responsibility | D6 AI Industry/Application Breadth |
|---|---|---|---|---|---|---|
| 0 | No higher ed, or unrelated field | None listed | No AI/ML roles | None discoverable | IC, no leadership language | No AI-related experience with identifiable industry context |
| 1 | Bachelor's, adjacent field, no AI coursework | One expired/low-credibility cert | AI-adjacent role only | Non-technical public content only | Team lead/informal only | Exactly one distinct industry/application domain |
| 2 | Bachelor's CS/quant, no AI specialization | One current recognized-vendor cert | 1–2 yrs explicit AI/ML role, IC scope | One verifiable technical artifact | Manager-level, team-scope | Exactly two distinct industries/domains |
| 3 | Bachelor's + AI specialization, or Master's adjacent | 2+ current general certs | 3+ yrs AI/ML, or 1–2 yrs with ownership language | Multiple artifacts, unverified | Director/Head, some strategic language | Exactly three distinct industries/domains |
| 4 | Master's AI/ML/DS, or PhD adjacent quant | Multiple current AI/ML-specific certs | Multi-yr, multi-role, ownership escalation | Multiple artifacts, ≥1 externally verifiable | VP/senior, explicit enterprise-strategy scope | Exactly four distinct industries/domains |
| 5 | PhD CS/AI/ML with AI-specific research | Multiple AI/ML certs + maintained professional-body credential | Sustained multi-yr AI/ML leadership, deployed systems at scale | Sustained, externally verifiable output (pubs/patents/high-engagement OSS) | C-level/CAIO-equivalent, strategic AND augmentation-aware framing | Five or more distinct industries/domains |

**Do not** redesign, reweight, or reinterpret any dimension. If you disagree with a criterion's wording, note it in a personal comment for the researcher afterward — do not silently apply a different rule.

## 2. Do not look at the primary researcher's existing scores

The entire point of this exercise is to measure how much two independent coders agree using only the framework and the source profile — not how well you can reproduce someone else's answer. Seeing the existing scores first, even briefly, would invalidate the comparison. If you have already seen them, tell the researcher before starting rather than proceeding.

## 3. Score each dimension independently

Score D1 through D6 for a given profile as six separate judgments. Do not let your score on one dimension anchor your score on another (e.g., a senior-sounding title should not by itself pull up your D1 or D3 score — only the evidence relevant to *that* dimension counts for it).

## 4. Use observable evidence only

Score what the profile actually states or shows — job titles, dates, described responsibilities, listed credentials, described projects/publications. Do not infer competence, seniority, or ability beyond what is written. Do not use outside knowledge about the person, their company, or their reputation.

## 5. No external research

Score from the profile content you were given only. Do not search LinkedIn, Google, company websites, or any other external source to fill in gaps or verify claims. If evidence for a dimension is not present in the profile, that is itself the finding — record it as unavailable (§7), not as an opportunity to look further.

## 6. Under genuine uncertainty, use the lower defensible band

If evidence could reasonably support either of two adjacent scores, choose the lower one. This is a deliberate, conservative convention used throughout this project (matches the primary researcher's own coding discipline) — it keeps scores anchored to what is clearly demonstrated rather than what is charitably inferred.

## 7. Preserve "unavailable" vs. observed zero — do not collapse the two

This is the most important mechanical rule in this document, and the reason your blank template only has plain score columns.

- If you looked for evidence relevant to a dimension and **found genuine evidence of the lowest band** (e.g., a profile that explicitly lists AI-related work history but it clearly amounts to "no AI/ML roles" for D3, or explicitly shows no higher education for D1) — **write `0`**. This is an observed score.
- If the profile **gives you nothing to evaluate that dimension on at all** (e.g., no Professional Experience section exists at all, so D3 and D6 cannot be assessed one way or the other) — **leave the cell blank**. Do not write `0`.

A blank cell and a written `0` mean two different things and will be treated differently in the reliability analysis: a written `0` is a real data point that counts toward agreement statistics; a blank cell is excluded from that dimension's comparison entirely, the same way it is excluded for the existing frozen annotation (three profiles in the full 500 — `LP0041`, `LP0170`, `LP0182` — have D3 and D6 recorded this way, because they have no Professional Experience section at all; if any of those three happen to be in your 75-profile subset, you may encounter the same situation and should record it the same way).

## 8. D6 counts AI-related industry/application breadth, not seniority or skill

D6 asks how many **distinct industries or application domains** the person has observable AI-related professional experience in — count the number of clearly different industry/domain contexts (e.g., healthcare AI, financial-services AI, retail AI, defense AI count as separate domains if each is evidenced). It is explicitly **not** a measure of how good, senior, or impressive that experience is — a person with AI work in five different industries at a junior level scores higher on D6 than a widely-respected AI leader who has only ever worked in one industry. Do not let D6 be influenced by D5-style seniority signals.

## 9. D5 requires more than title prestige

A senior-sounding title alone (e.g., "AI Director," "Head of AI Strategy") is not sufficient evidence for a high D5 score. Score D5 from the *described scope of responsibility and strategic framing language* in the profile — what the person says they were accountable for, not just what their title says they were called. A grand title with no described strategic content should be scored conservatively (§6); a modest title with clearly described enterprise-scope strategic responsibility can outscore it.

## 10. What you are not doing

- You are not producing a composite ALCSM score. Score each dimension separately; do not average, sum, or otherwise combine D1–D6 into one number.
- You are not assigning weights to any dimension.
- You are not judging whether the framework itself is good or complete — only applying it as given.

## Recording your scores

Fill in `Rater_A_Blank_Template.xlsx` directly:

1. One row per `Profile_ID` (already listed for you — do not add, remove, or reorder rows).
2. For each of D1–D6: write an integer 0–5 if you have observable evidence to score it, or leave the cell blank if the profile gives you nothing to assess that dimension on (§7).
3. Do not add extra columns, notes, or formatting — keep the file structurally identical to how you received it, so it can be read back programmatically.
4. When finished, return the file to the researcher. Do not rename it in a way that loses which rater it belongs to.

If you have any question about how to apply the framework to a specific profile, note the `Profile_ID` and your question for the researcher rather than guessing at an interpretation not covered by the rubric or the rulebook addendum.
