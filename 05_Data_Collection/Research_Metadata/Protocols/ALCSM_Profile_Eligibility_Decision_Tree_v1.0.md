# ALCSM Profile Eligibility Decision Tree

**Version:** 1.0
**Status:** Final for Step 3 — governance-layer research documentation.
**Document type:** Reference document (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This document represents the LinkedIn profile eligibility-screening workflow as a decision tree, sequencing the criteria defined in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md` and `ALCSM_AI_Leadership_Title_Dictionary_v1.0.md` into a single, ordered procedure. It exists so that any collector — the author or a future researcher — applies the same criteria in the same order to every candidate profile.

## 2. Decision Tree

```
Candidate profile identified via pre-registered search
    │
    ▼
[1] Is the profile publicly accessible under default view settings?
    │
    ├── NO  ──► EXCLUDE  (EC-01 — not publicly accessible)
    │
    ▼ YES
[2] Is the organization associated with the individual's current role
    operating in Germany (headquarters or verifiable German operations),
    regardless of global headquarters location?
    │
    ├── NO  ──► EXCLUDE  (EC-02 — no verifiable German operations)
    │
    ▼ YES
[3] Does the current job title match a Tier 1 (Core) entry in the
    AI Leadership Title Dictionary?
    │
    ├── YES ──► proceed to [5]
    │
    ▼ NO
[4] Does the current job title match a Tier 2 (Conditional) entry?
    │
    ├── NO  ──► EXCLUDE  (EC-03 — no qualifying title)
    │
    ▼ YES
    Conduct manual review of the profile's publicly stated content
    (headline, about, experience) against the Tier 2 review question
    (ALCSM_AI_Leadership_Title_Dictionary_v1.0.md §4).
    │
    ├── Leadership responsibility NOT evidenced ──► EXCLUDE (EC-03)
    │
    ▼ Leadership responsibility evidenced
[5] Does the profile's publicly stated content evidence leadership,
    strategic, managerial, or organizational responsibility for AI,
    ML, advanced analytics, or AI strategy (as opposed to a purely
    individual-contributor technical role)?
    │
    ├── NO  ──► EXCLUDE  (EC-04 — no leadership-scope evidence)
    │
    ▼ YES
[6] Is the profile a unique individual not already represented
    elsewhere in the dataset, and is profile content available in a
    language the research team can accurately transcribe?
    │
    ├── NO  ──► EXCLUDE  (EC-06 duplicate / EC-07 language)
    │
    ▼ YES
INCLUDE
    Assign pseudonymous identifier at point of capture.
    Record inclusion_reason:
        Tier 1 match  → title_match
        Tier 2 match  → manual_review_included
    Proceed to transcription per the LinkedIn Collection Protocol §8.
```

## 3. Correspondence to the Inclusion/Exclusion Criteria

Each decision point above corresponds to one or more numbered criteria in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md`:

| Decision Point | Criteria Applied |
|---|---|
| [1] Public accessibility | IC-01, EC-01 |
| [2] German operations | IC-02, EC-02 |
| [3]–[4] Qualifying title | IC-03, IC-04, EC-03 |
| [5] Leadership-scope evidence | IC-05, IC-06, EC-04 |
| [6] Uniqueness and language | IC-07, IC-08, EC-06, EC-07 |

## 4. Methodological Note: Reproducibility Through Sequencing

Presenting eligibility screening as an ordered decision tree, rather than an unordered checklist, serves two methodological purposes:

- **Consistency across collectors and over time.** A fixed sequence removes ambiguity about which criterion controls when a profile could plausibly satisfy or fail multiple criteria at once — every profile is evaluated in the same order, so two collectors (or the same collector at two different times) reach the same inclusion decision from the same profile content.
- **Bounding the one point of judgement.** The only step in this workflow that is not a mechanical check is the Tier 2 manual review at decision point [4]. Confining judgement to a single, narrowly defined, documented step — rather than allowing it to recur at multiple points — keeps the overall procedure objective and auditable: a reviewer can verify that every inclusion decision followed this exact sequence and that any judgement applied was the one judgement the procedure permits.

## 5. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial decision tree, sequencing the finalized Step 3 eligibility criteria and title dictionary. | Samiksha Dhere |

---

*This document sequences existing eligibility criteria for reproducibility. It does not itself define new inclusion or exclusion criteria beyond those in `ALCSM_Inclusion_Exclusion_Criteria_v1.0.md`.*
