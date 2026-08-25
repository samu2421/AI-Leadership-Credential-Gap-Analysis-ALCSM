# ALCSM Coding Rulebook — v1.1 Addendum (D6 Only)

### Supplements `ALCSM_Coding_Rulebook_and_Pilot_Design.md`; does not modify it

**Version:** 1.1 Addendum
**Status:** PROPOSED / PILOT_REQUIRED, scoped to Dimension 6 only. Not yet binding for annotation — annotation has not begun under either the v1.0 or v1.1 rulebook.
**Scope note, mirrored from the original rulebook's own scope note:** this addendum does not alter Dimensions 1–5, their criteria, or their supporting literature. It does not touch the general scoring principles (§1.2), the tie-breaking escalation ladder (§1.5, restated by reference), or the pilot workflow (Part 2) of the original rulebook — those apply to D6 v1.1 exactly as written. This addendum adds D6-specific content only, in the same numbering convention as the parent document where a direct parallel exists.
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Date:** 2026-08-17

---

## 1. What counts as "AI-related experience" for D6

D6 v1.1 is computed **only** over employment records already classified `AI_Related = Yes` in the processed dataset (`Professional_Experience` sheet). This addendum does not define a new AI-relatedness test — it inherits whatever classification produced that flag. Two consequences follow directly:

- **D6 is derivative of, not independent from, the AI-relatedness judgment.** If a role's AI-relatedness is corrected during D3 annotation (e.g., an annotator determines a role coded `AI_Related = Yes` is actually AI-adjacent-only, or vice versa), that profile's D6 breadth count must be recomputed from the corrected set of AI-related rows before its D6 score is finalized. A D6 score computed against a since-corrected `AI_Related` flag is stale, not merely imprecise, and must not be reported as final.
- **Non-AI-related industries are never counted**, even if numerous or prestigious. A profile with fifteen years across five non-AI industries and one recent AI-related role in a sixth scores D6 = 1, not 6. This is the entire point of restricting to AI-related rows (`ALCSM_D6_Industry_Breadth_v1.1.md` §5, Question D) and must not be second-guessed case-by-case by annotators who feel a non-AI industry "should count" because it seems relevant to the person's overall career.

## 2. What counts as a "distinct industry"

Two `Professional_Experience` rows contribute to the same industry count if their `Industry` values are identical **after** applying the normalization table in `ALCSM_D6_Industry_Breadth_v1.1.md` §6. Annotators do not perform ad hoc normalization judgment calls during scoring — the table is the fixed reference, and it is deliberately short (four merges) precisely so this step is mechanical, not interpretive.

For the five raw values the table explicitly leaves unmerged (`E-commerce` / `E-commerce and Retail` / `Retail`; `Travel Technology`; `Chemicals`; `Advertising and Marketing` / `Media`; `Professional Association`), annotators treat each as its **own** distinct category, exactly as it appears in the data — they do not merge these on their own judgment during scoring, even if a merge feels intuitive. Any annotator who believes one of these should be merged logs it as a rubric-quality note (§2.5 of the parent rulebook's revision-log logic) for the post-pilot normalization review named in `ALCSM_D6_Industry_Breadth_v1.1.md` §14, rather than silently applying a personal judgment that would differ from the other rater's.

## 3. Multiple roles, same industry

Multiple AI-related roles in the same normalized industry (e.g., two different employers, both `Technology`) count as **one** industry toward breadth, not two. D6 v1.1 counts distinct industry contexts, not distinct roles or employers — role count and tenure are D3's territory (`ALCSM_D6_Industry_Breadth_v1.1.md` §8), not D6's. Do not let a long, multi-employer career within a single industry inflate the D6 score; that pattern should instead be visible in a strong D3 score.

## 4. Unknown / "Not Visible" industry values

If a specific AI-related experience row's `Industry` value is a null, an explicit not-visible/unknown marker, or the non-informative literal `Other`, that **row** is excluded from the breadth count — it neither adds a new distinct industry nor is treated as evidence of zero. This mirrors §5 Question A of `ALCSM_D6_Industry_Breadth_v1.1.md`: 51 of 1,791 AI-related rows in the real dataset carry the placeholder `Other` and were excluded on exactly this basis. A profile can still score D6 > 0 from its other, usable AI-related rows even if one row's industry is unusable — exclude the row, not the profile.

## 5. Missing-status handling: the two zero-evidence sub-cases

D6 v1.1 inherits the project's four-state missing-data framework (`missing_status_ref`: `present` / `absent_stated` / `unavailable` / `not_applicable`), applied as follows — this is the proposed treatment flagged as open in `ALCSM_D6_Industry_Breadth_v1.1.md` §14, item 6, pending pilot confirmation:

| Case | Missing-status | Score | Rationale |
|---|---|---|---|
| Profile has ≥1 AI-related experience row with a usable `Industry` value | `present` | Count of distinct normalized industries (§7 of the definition doc), banded 0–5 | Genuine, evidenced finding. |
| Profile has AI-related experience, but *every* such row's `Industry` is unusable (null/placeholder) | `present` | 0 | The experience section was observed and reviewed; the finding is "AI-related work exists but its industry context is not stated," which is itself an observation, not a data gap. Do **not** code this `unavailable` — the profile was not unreachable, the field within it was simply not populated. |
| Profile has no AI-related experience record at all | `present` | 0 | Equally a genuine, observed finding (the full experience history was reviewed and contains no AI-related roles), not a collection failure. This is the same logic already applied to D3 scoring a 0 for "no AI/ML roles" (`ALCSM_v1.1_Scoring_Framework.md` §1) — D6 should not be treated any more cautiously than D3 is for the structurally identical situation. |
| The profile's experience section itself could not be retrieved at collection (`profile_raw_section.section_available = FALSE` for `'experience'`) | `unavailable` | 0, but flagged distinctly | A genuine data gap, not a finding. Rare in the current dataset (experience data was collected for all 500 included profiles) but the distinction must still be coded correctly if it occurs, per precedent P-13's general handling of `present`-vs-`unavailable`. |

Unlike the original D6 (where `unavailable` was the dominant real-world case, since activity data was never collected), `unavailable` should be a rare code under v1.1 — most zero-evidence profiles are legitimately `present`/score 0, not data gaps. An annotator who finds themselves coding many D6 rows `unavailable` should treat that as a signal something is wrong with how they are applying this table, not as an expected pattern.

## 6. Ambiguous industry labels

If an `Industry` value is genuinely ambiguous in a way this addendum's normalization table does not resolve (e.g., a value not seen in the original 1,740-row inspection, or a boundary case among the five deliberately-unmerged groups in §2), annotators apply the same conservative default already established in the parent rulebook (§1.2, Principle 4: "default to the lower score under genuine uncertainty"): when uncertain whether two values represent the same or different industries, treat them as the **same** industry (i.e., do not count the ambiguous case as adding a new distinct industry) rather than inflating breadth on an unresolved judgment call. Flag `ambiguous = TRUE` in the coding log with both candidate readings, exactly as the parent rulebook's §1.3 already requires for other dimensions.

## 7. Evidence requirements

Per the parent rulebook's Principle 2 ("one indicator, one piece of evidence, one score"), a D6 score must be traceable to the specific `Experience_ID` row(s) that produced each counted industry — not just a final number. The coding log entry for D6 records, at minimum, the list of `Experience_ID` values contributing to the count and their (raw, normalized) `Industry` pair, so any score can be reconstructed and audited back to source rows, consistent with how evidence citation already works for D1–D5.

## 8. Conservative scoring default

Consistent with §1.2 Principle 4 of the parent rulebook, all D6 v1.1 judgment calls — normalization ambiguity (§6), unusable-value exclusion (§4), and the zero-evidence sub-cases (§5) — default toward the **lower** breadth count, never the higher one. This is a deliberate, disclosed conservative bias, carried over from the same stated rationale as the rest of the rulebook: ALCSM's purpose is credential-gap detection, and an instrument that resolves ambiguity generously risks manufacturing the very inflation it is designed to detect.

## 9. Tie-breaking: the D5/D6 boundary case

`ALCSM_D6_Industry_Breadth_v1.1.md` §10 identifies one job-posting requirement ("Proven senior experience defining AI technical strategy across multiple domains") that plausibly evidences either D5 (strategic scope) or D6 (industry breadth). Proposed tie-breaking rule, pending pilot confirmation:

- If the language describes **organizational/strategic scope** ("enterprise-wide," "cross-functional mandate," "budget ownership") without naming specific industries or domains, it is D5 evidence only.
- If the language names or clearly implies **specific distinct industry/domain contexts** (e.g., "across automotive, healthcare, and financial services"), it is D6 evidence only.
- If the language is genuinely both (names specific domains **and** frames it as strategic authority over them), log it as evidence for **both** dimensions rather than forcing a single assignment — this is consistent with the parent rulebook's general position that dimensions are scored independently (§1.2, Principle 3) and a single text span is permitted to support more than one dimension's score when it genuinely does.
- The single real occurrence of this pattern in the current job-posting corpus (§10 of the definition document) should be treated as a pilot test case for this rule, not resolved definitively until the pilot confirms whether the rule is workable across more than one instance.

## 10. Worked examples (constructed, for annotator training only)

Same disclaimer as the parent rulebook's §1.5 illustrative cases: these are constructed for training purposes, not real profiles.

- **Example 1 — straightforward breadth:** Three AI-related experience rows: `(Company X, Industry="Financial Services")`, `(Company Y, Industry="Healthcare")`, `(Company Z, Industry="Financial Services")`. Distinct normalized industries = 2 (Financial Services, Healthcare) → D6 = 2. The repeated Financial Services employer does not double-count (§3).
- **Example 2 — unusable-row exclusion:** Four AI-related rows: two with `Industry="Technology"`, one with `Industry="Other"`, one with `Industry=null`. Usable rows = 2, both Technology → D6 = 1, not `unavailable` (§4, §5) — the profile has usable evidence, it just happens to point to one industry.
- **Example 3 — normalization applied:** Two AI-related rows: `Industry="Telecommunications"` and `Industry="Telecommunication"`. Per the normalization table (§2), these merge to one distinct industry → D6 = 1, not 2. An annotator who scores this D6 = 2 without applying the table has made a rubric-compliance error, not a defensible judgment call.
- **Example 4 — deliberately-unmerged case:** Two AI-related rows: `Industry="E-commerce"` and `Industry="E-commerce and Retail"`. Per §2, these are **not** merged by annotator judgment → D6 = 2, and the annotator additionally logs a rubric-quality note per §2, since this is exactly the kind of case the post-pilot normalization review (`ALCSM_D6_Industry_Breadth_v1.1.md` §14) needs visibility into.
- **Example 5 — zero AI-related experience:** Profile's experience history contains five non-AI-related roles (retail, logistics, education, manufacturing, insurance) and no AI-related role at all. D6 = 0, `missing_status = present` (§5) — not `unavailable`, despite the score being zero and the underlying career being broad. Breadth of a *non-AI* career is not D6 evidence, however extensive.

---

## What this addendum does not do

- It does not modify the coding log template (§1.6 of the parent rulebook) beyond adding the D6-specific traceability requirement in §7 above; the same `profile_id` / `dimension` / `rater_id` / `score` / `evidence_text` / `missing` / `ambiguous` / `contradiction` / `notes` / `timestamp` structure applies to D6 rows exactly as it does to D1–D5.
- It does not change the tie-breaking escalation ladder (minor vs. major disagreement, adjudication) — §9 above is a content rule about which dimension a specific piece of evidence belongs to, not a change to how rater disagreement within D6 itself is resolved.
- It does not perform any actual annotation, and no profile has been scored under this addendum.
- It does not add or alter any entry in the frozen precedent library (P-01…P-15); if the pilot reveals a genuinely new, recurring situation D6 v1.1 creates, a new precedent would be proposed separately and go through the same author-approval path as this entire v1.1 revision.

*This addendum governs Dimension 6 coding only, pending the pilot in `D6_v1.1_Implementation_Assessment.md` §Pilot Design. `ALCSM_Coding_Rulebook_and_Pilot_Design.md` remains unmodified and fully governs Dimensions 1–5.*
