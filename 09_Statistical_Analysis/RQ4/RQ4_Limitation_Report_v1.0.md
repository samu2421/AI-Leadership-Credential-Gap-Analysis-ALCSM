# RQ4 Limitation Report v1.0 — Observable Professional Impact Indicators

**RQ4:** Do ALCSM credential signals correlate with observable professional impact?
**Status:** **Not runnable against real data. This report documents why, rather than inventing a substitute criterion.**
**Author:** Samiksha Dhere (researcher) — investigated with Claude Code assistance

---

## 1. What RQ4 needs

`alcsm.analysis.rq4.correlate_with_impact_indicators` computes Spearman rank correlation between each ALCSM dimension score (D1–D6) and four **external, non-ALCSM** criterion variables — the complete, closed list defined by the frozen `rq4_impact_indicator` schema table:

| Variable | Intended meaning |
|---|---|
| `rq4_network_reach` | Connection/follower count (capped flag for very large networks) |
| `rq4_content_engagement` | Engagement (likes/comments/shares) on posted content |
| `rq4_recognition_count` | External recognition signals (e.g. endorsements, awards, mentions) |
| `rq4_seniority_progression_rate` | Rate of career seniority progression over time |

These are deliberately **physically isolated** from every ALCSM-scoring module in this codebase (`tests/analysis/test_isolation.py` enforces this at the AST level) — the entire point of RQ4 is to correlate ALCSM scores against something ALCSM did not itself measure, so none of D1–D6's own inputs can legitimately stand in as a criterion.

## 2. What was checked for this session

Searched every real, currently available data source for any of the four criterion variables, or anything that could serve as a non-circular equivalent:

- **`alcsm.rq4_impact_indicator` (database table):** 0 rows. `alcsm.profile` itself has 0 rows (the Profile_ID `LP####`-vs-`PRF-#####` incompatibility, `Postgres_Profile_ID_Compatibility_Status.md`), so no impact-indicator row could exist even if the data had been collected separately.
- **`05_Data_Collection/LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx`** — all five sheets inspected column-by-column (`Profile_Master`, `Education`, `Certification`, `Professional_Experience`, `Technical_Contribution`). **None of the four criterion variables, or anything resembling them (no follower/connection counts, no engagement metrics, no recognition/award fields), appear anywhere in this workbook.** This is not a loading gap — the data was not collected in the first place, at least not in a form that reached this processed workbook.
- **`06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`** — contains only D1–D6 scores and evidence, which are exactly what RQ4 must *not* use as its own criterion (that would make the correlation circular, `PROJECT_CONTEXT.md` §5/§15/§27, restated in `rq4.py`'s own module docstring).

## 3. What was explicitly NOT done

Per this session's explicit instruction:

- **`D4` (Technical Contributions) was not reused as an external criterion.** Even though `Technical_Contribution`'s raw rows (publication/patent/OSS mentions) might superficially resemble "recognition" or "impact," D4 is scored directly from this same sheet — using it as RQ4's criterion would correlate an ALCSM dimension against its own source data, which is circular by construction, not a genuine external validation.
- **No criterion was invented.** `Professional_Experience`'s raw employment dates and titles could, in principle, be used to *derive* something progression-rate-like, but doing so would mean defining a new metric's exact formula (window, weighting, how a title change counts) without any prior specification, review, or validation — exactly the kind of ad hoc invention this session's brief prohibits ("do not invent it").

## 4. Conclusion

**RQ4 cannot be run against real data in this session, or at all until new data is collected.** This is a **data-collection gap**, not a code gap — `alcsm.analysis.rq4.correlate_with_impact_indicators` is fully implemented, tested against synthetic fixtures (`tests/analysis/test_rq4.py`), and ready to run the moment real `rq4_impact_indicator`-shaped data exists for at least a meaningful number of profiles. Nothing about this session's work changes that readiness state — it remains exactly where it was reported at the end of the prior session (`FINAL_ANALYSIS_HANDOVER.md` limitation 4).

## 5. What would be needed to unblock RQ4 (for future reference, not started here)

1. A dedicated data-collection pass gathering network reach, content engagement, recognition signals, and a defined seniority-progression measure for some subset of the 500 profiles (or a documented sampling plan for a smaller RQ4-specific subset) — this is new fieldwork, not a re-analysis of existing data.
2. Resolution of the Profile_ID database-loading issue, only if the collected data is meant to be stored via `rq4_impact_indicator` rather than a standalone Excel workbook (per `Postgres_Profile_ID_Compatibility_Status.md`, this is not itself a blocker for analysis if the data were instead kept in Excel and read directly, matching how every other RQ in this session was analyzed).

Given the three-day thesis deadline, this report's function is to **close this line of inquiry cleanly for the current submission** — RQ4 should be described in the thesis as a documented, data-driven limitation (what was intended, why it cannot be run now, and what a future extension would require), not silently dropped or filled with a substitute analysis that was not actually requested.
