# P3 Final Dataset QA, Data Integrity Audit, Taxonomy Readiness Audit, and Data-Freeze Preparation Report

**Version:** 1.0
**Status:** Final for this audit session. Audit only — no data was modified, cleaned, deduplicated, annotated, or scored. The two raw workbooks were opened strictly read-only throughout (confirmed via file modification timestamps and `git status`, both unchanged by this session).
**Scope:** `05_Data_Collection/LinkedIn_Profiles/01_Raw/ALCSM_LinkedIn_DataCollection_v1.0.xlsx` and `05_Data_Collection/Job_Postings/01_Raw/ALCSM_JobPosting_DataCollection_v1.0.xlsx`.
**Last Updated:** 2026-08-16
**Author:** Samiksha Dhere (researcher) — audit executed with Claude Code assistance

---

## 1. Executive Summary

This audit independently recalculated every headline collection statistic directly from the raw workbook data (not from the workbooks' own Dashboard sheets), performed a full duplicate inventory across both datasets and all child sheets, quantified missingness separately for included and excluded populations, assessed evidentiary readiness for each of the six frozen ALCSM dimensions, verified referential integrity between master and child/requirement records, and audited the job-requirement-to-dimension mapping and controlled vocabularies.

**Headline result: the independently calculated collection counts match the figures you supplied (611 / 500 / 111 / 201 / 201) exactly. The workbooks' own Dashboard sheets do not match either figure and are stale.** Beyond that reconciliation, the audit surfaced a set of structural and governance findings — most importantly, an absence of any documented ethics-approval record, an active `.gitignore` gap over the raw-data folders now in use, the presence of uncontrolled direct identifiers in the raw workbook, cross-population duplicate individuals, child records belonging to excluded profiles, an almost complete absence of raw verbatim evidence text required by the Annotation Handbook, and a job-requirement-to-dimension mapping in which the majority of records are unmapped and no records at all are mapped to Leadership (D5) despite 221 requirements being explicitly categorized as leadership-related.

**Overall assessment: NOT READY FOR DATA FREEZE.** See §14 for the full blocker list.

---

## 2. Actual Collection Counts (Independently Calculated)

Calculated directly from `Profile_Master`, `Job_Master`, and their child/requirement sheets — not from any Dashboard cell.

| Metric | Calculated Value | Your Stated Value | Match |
|---|---|---|---|
| Total LinkedIn records (`Profile_Master` rows) | 611 | 611 | ✅ |
| Included profiles (`Included = Yes`) | 500 | 500 | ✅ |
| Excluded profiles (`Included = No`) | 111 | 111 | ✅ |
| Duplicate profiles (exact-duplicate `Profile_ID`) | 0 | — | — |
| Duplicate profiles (same individual, by normalized `LinkedIn_URL`) | 16 groups / 40 rows | — | (not previously reported) |
| Total job postings (`Job_Master` rows) | 201 | 201 | ✅ |
| Included postings (`Included = Yes`) | 201 | 201 | ✅ |
| Excluded postings (`Included = No`) | 0 | 0 (implied) | ✅ |
| Duplicate postings (exact-duplicate `Job_ID`) | 0 | — | — |
| Duplicate postings (normalized `Posting_URL`) | 3 | — | (not previously reported) |
| Job requirement records | 1,558 | 1,558 | ✅ |

Child-sheet row counts (LinkedIn): Education 1,082; Certifications 685; Professional_Experience 2,164; Technical_Contributions 571.

---

## 3. Dashboard Reconciliation

The workbooks' own `Dashboard` sheets were read in full and compared against the independently calculated figures above.

| Workbook | Dashboard Metric | Dashboard Value | Calculated Value | Discrepancy |
|---|---|---|---|---|
| LinkedIn | Profiles Collected | 500 | 611 | **-111** |
| LinkedIn | Profiles Included | 500 | 500 | Match |
| LinkedIn | Profiles Excluded | 0 | 111 | **-111** |
| LinkedIn | Duplicate Profiles | 0 | 16 groups (URL-based) | **-16** |
| LinkedIn | Education/Certification/Experience/Technical Contribution Records | (blank/NaN) | 1,082 / 685 / 2,164 / 571 | **not populated** |
| LinkedIn | Completion % | 1 (100%) | — | Consistent with a stale 500/500 snapshot only |
| Job Posting | Target Job Postings (Final) | 200 | 201 (actual) | **-1** |
| Job Posting | Job Postings Collected | 200 | 201 | **-1** |
| Job Posting | Included Postings | 200 | 201 | **-1** |
| Job Posting | Excluded Postings | 0 | 0 | Match |
| Job Posting | Duplicate Postings | 0 | 3 (URL-based) | **-3** |
| Job Posting | Requirements Extracted | 0 | 1,558 | **-1,558** |
| Job Posting | Companies Covered | 0 | not independently recomputed as a dashboard-comparable figure | **not populated** |
| Job Posting | Industries Covered | 0 | not independently recomputed as a dashboard-comparable figure | **not populated** |

**Finding DASH-01 [HIGH PRIORITY].** Both Dashboard sheets are stale and do not reflect the current state of their own workbook's data sheets. The LinkedIn Dashboard appears frozen at an early snapshot (500 profiles, before the 111 exclusions and additional collection to 611 total were recorded); several Job Posting Dashboard metrics (Requirements Extracted, Companies Covered, Industries Covered) show a literal `0` despite 1,558 requirement rows and 201 populated job records existing in the same workbook. Per instruction, the Dashboard sheets have not been modified. **Recommendation:** regenerate both Dashboards from the current data sheets before this dataset is used as a reference by anyone other than the primary collector, since a reviewer relying on the Dashboard alone would materially misjudge dataset size and exclusion rate.

---

## 4. Duplicate Audit

### 4.1 LinkedIn Profiles

| Check | Result |
|---|---|
| `Profile_ID` exact duplicates | 0 |
| `Profile_ID` format conformance (`LP####`) | 611/611 conform |
| `LinkedIn_URL` null/blank | 0 |
| `LinkedIn_URL` exact-string duplicates | 24 rows |
| `LinkedIn_URL` normalized duplicates (lowercased, query-stripped, trailing-slash-stripped) | 24 rows across 16 duplicate-value groups (group sizes: fourteen 2-row groups... see breakdown below) |
| Duplicate-group size distribution | 13 groups of 2, 2 groups of 3, 1 group of 8 |
| **Duplicate groups spanning both `Included = Yes` and `Included = No`** | **15 of 16 groups** |
| Duplicate group entirely within one population | 1 of 16 groups |
| URLs matching the standard `https://www.linkedin.com/in/<slug>` shape | 580 / 611 (95.0%) |
| URLs **not** matching that shape | 31 / 611 (5.1%) — of these, 23 still contain `linkedin.com` in some form; 8 do not appear to be URLs at all |
| Explicit non-URL placeholder values in the `LinkedIn_URL` column (e.g. a short textual marker rather than a link) | 8 rows — these account for the single largest duplicate-value group (the 8-row group above); the value is short (11 characters), contains a space, and contains none of `http`, `linkedin`, or `.com`, consistent with a textual missingness marker rather than a real URL entered eight times |
| Other placeholder-pattern matches (contains a token such as "example", "test", "placeholder", "n/a", "unknown") | 52 rows across 51 distinct values |

**Finding DUP-01 [CRITICAL BLOCKER].** Fifteen of sixteen duplicate-`LinkedIn_URL` groups contain at least one row marked `Included = Yes` and at least one row marked `Included = No` for what, by shared URL, is the same real individual. This means the same person is simultaneously represented as both a study participant and an excluded candidate. Until resolved, it is not possible to say with confidence that the 500-profile included sample and the 111-profile excluded set are disjoint populations of distinct individuals. **Nothing has been removed or resolved** — this is reported for manual review, per instruction.

**Finding DUP-02 [MEDIUM PRIORITY].** The `LinkedIn_URL` column mixes real URLs, non-standard-shape URL-like strings, and explicit non-URL placeholder text (e.g. "not visible"-style markers) within a single unnormalized text column, with no separate flag distinguishing "URL not observed" from "URL observed but malformed." This makes deterministic duplicate detection on this column inherently unreliable at its current level of normalization (see §10 for the recommended canonical form).

### 4.2 Child Sheets (LinkedIn)

| Sheet | Row count | Own-ID duplicates | Full-content duplicate rows (same content excluding the record's own ID) |
|---|---|---|---|
| Education | 1,082 | 0 | 0 |
| Certifications | 685 | 0 | 1 |
| Professional_Experience | 2,164 | 0 | 6 |
| Technical_Contributions | 571 | 0 | 0 |

**Finding DUP-03 [LOW PRIORITY].** Seven content-duplicate child rows found (1 Certification, 6 Professional_Experience) — the same `Profile_ID` with identical values across every other column, differing only in the row's own auto-generated ID. Plausibly double-entry during manual transcription. Not removed; listed here by count and sheet for manual review (record-level identifiers omitted from this report by design, per the read-only/no-export instruction and to avoid restating personal data — the researcher can locate them by re-running a full-row duplicate check on the two named sheets).

### 4.3 Job Postings

| Check | Result |
|---|---|
| `Job_ID` exact duplicates | 0 |
| `Posting_URL` null/blank | 0 |
| `Posting_URL` exact-string duplicates | 0 |
| `Posting_URL` normalized duplicates | 3 rows |
| `(Company_Name, Job_Title)` exact-combo duplicates | 0 |
| Likely reposts (same company + same normalized title, different collection dates) | 0 — no such pattern was found; the 0 combo-duplicates above means this check had no candidates to evaluate |

**Finding DUP-04 [LOW PRIORITY].** Three postings share a normalized `Posting_URL` with another posting. Given the overall low duplication rate on this side of the dataset, this is a minor finding relative to the LinkedIn duplicate picture.

---

## 5. Missingness Audit

Missingness is reported in two forms, kept distinct per instruction: **null/blank cells** (nothing recorded) and **explicit textual markers** (e.g. "Not Visible", "Unknown", "N/A", "None") — a positively recorded statement of unavailability, not a blank. No null cell was found anywhere in `Profile_Master`; every apparent "missing" value in that sheet is an explicit marker, which is the more defensible pattern of the two (it distinguishes "not collected" from "collector positively could not find this").

### 5.1 LinkedIn Profiles — All / Included / Excluded

| Field | All (n=611) marker rate | Included (n=500) marker rate | Excluded (n=111) marker rate |
|---|---|---|---|
| Federal_State | 5.2% | 4.0% | 10.8% |
| City | 6.2% | 5.0% | 11.7% |
| Current_Company | 1.5% | 0.2% | 7.2% |
| Industry | 0.5% | 0.2% | 1.8% |
| Company_Size | 4.9% | 2.6% | 15.3% |
| Current_Title | 1.0% | 0% | 5.4% |
| Current_Role_Start_Date | 3.8% | 2.4% | 9.9% |
| Current_Role_Duration_Months | 3.8% | 2.4% | 9.9% |
| Title_Category | 0.5% | 0% | 2.7% |
| LinkedIn_URL | 1.3% | 1.2% | 1.8% |

Excluded profiles show a consistently higher marker rate than included profiles across every field — directionally expected (a profile with more unobservable fields is more likely to have been excluded) and not itself a defect.

### 5.2 Child Sheets — Missing/Null Only

| Sheet | Field | Null count |
|---|---|---|
| Education | Start_Year | 1 |
| Professional_Experience | Duration_Months | 4 |

No other null values were found in any child sheet. **No date field of any kind exists in the Certifications sheet** — see Finding ALCSM-D2-01 in §7.

### 5.3 Job Postings

`Job_Master`: no null values found in any column examined. `Requirements`: `Requirement_Text` is 0% null and 0% empty-string across all 1,558 rows (min 14, max 187, mean 83.6 characters) — this field is fully and substantively populated.

### 5.4 Explicit statement on scoring

No missing value of any kind identified in this audit has been converted into a substantive zero or otherwise scored. No ALCSM dimension score of any kind was computed during this session.

---

## 6. Referential Integrity

| Check | Result |
|---|---|
| Every `Education.Profile_ID` exists in `Profile_Master` | ✅ 0 orphans |
| Every `Certifications.Profile_ID` exists in `Profile_Master` | ✅ 0 orphans |
| Every `Professional_Experience.Profile_ID` exists in `Profile_Master` | ✅ 0 orphans |
| Every `Technical_Contributions.Profile_ID` exists in `Profile_Master` | ✅ 0 orphans |
| Every `Requirements.Job_ID` exists in `Job_Master` | ✅ 0 orphans |
| Every included job has ≥1 requirement record | ✅ all 201 |
| No excluded profile referenced in a child sheet | ❌ **fails — see below** |

**Finding REF-01 [CRITICAL BLOCKER].** Child evidence sheets contain records belonging to profiles marked `Included = No`:

| Child sheet | Distinct excluded profiles referenced | Rows belonging to excluded profiles |
|---|---|---|
| Education | 31 | 70 |
| Certifications | 16 | 46 |
| Professional_Experience | 24 | 91 |
| Technical_Contributions | 8 | 38 |

None of this has been removed. Any downstream process that reads a child sheet directly — without first joining back to `Profile_Master` and filtering on `Included = Yes` — will silently draw on data from individuals who were excluded from the study population. This is the same structural risk this project's own `ALCSM_Relationships_v1.0.md` and frozen-schema design were built to prevent (`ON DELETE RESTRICT` foreign keys and provenance-linked tables in the actual database schema); the raw Excel workbook has no equivalent structural safeguard.

**Finding REF-02 [INFORMATIONAL].** `Profile_Master.Included = No` combined with `Collection_Status = "Complete"` or `"Completed"` for 96 of the 111 excluded rows (94 + 2); only 15 of the 111 excluded rows carry a `Collection_Status` that itself reflects exclusion (`"Excluded"`: 13, `"Duplicate"`: 2). The two columns are tracking different things and are not contradictory by definition, but a reader relying on `Collection_Status` alone (rather than `Included`) would undercount exclusions by 96 records — worth a one-line clarification in the data dictionary about which column is authoritative for inclusion status.

---

## 7. ALCSM Dimension Readiness

Assessed against the frozen six-dimension definitions in `ALCSM_Measurement_Specification_v1.0.md` and the evidence requirements in `ALCSM_Annotation_Handbook.md`. No dimension was redesigned, reinterpreted, or scored.

| Dimension | Available evidence in raw data | Unavailable / missing | Annotation-ready? |
|---|---|---|---|
| **D1 — Formal Education** | `Degree_Level`, `Field_of_Study`, `University`, `Country`, `Start_Year`/`End_Year`, `Verified` (Education sheet) | No verbatim profile education-section text | **No — see ALCSM-D1-01** |
| **D2 — Professional Certifications** | `Certification_Category`, `Certification_Name`, `Issuing_Organization`, `Verified` | **No date field of any kind** (no issue date, no expiry, no year); no verbatim text | **No — see ALCSM-D2-01** |
| **D3 — Practical AI Experience** | `Company`, `Job_Title`, `Industry`, dates, `Duration_Months`, `Leadership_Role` (Yes 1,684 / No 480), `AI_Related` (Yes 1,884 / No 280) | No verbatim experience-description text; `AI_Related`/`Leadership_Role` are pre-coded booleans, not raw evidence | **No — see ALCSM-D3-01** |
| **D4 — Technical Contributions** | `Contribution_Type`, `Title`, `Verified` (100% "Yes" except where noted) | No verification provenance (source/timestamp/outcome); no description/evidence text beyond a short `Title` field | **No — see ALCSM-D4-01** |
| **D5 — Leadership & Strategic Responsibility** | `Current_Title`, `Title_Category` (profile side); `Leadership_Role` flag (experience side) | No strategic-scope evidence text; on the job-requirement side, the `ALCSM_Dimension` controlled vocabulary has **no value corresponding to Leadership at all** (see §9) | **No — see ALCSM-D5-01** |
| **D6 — Professional Engagement & Continuous Development** | *(none identified)* | No activity, post-count, community-role, or continuing-education field exists anywhere in `Profile_Master` or any child sheet | **No — see ALCSM-D6-01** |

**Finding ALCSM-D1-01 [CRITICAL BLOCKER].** Education is captured as pre-coded categorical fields (`Degree_Level`, `Field_of_Study`) rather than the profile's own verbatim education-section text. The Annotation Handbook's decision tree requires a coder to read the source text and apply the rubric independently; a pre-coded `Degree_Level` value is already an interpretation, not raw evidence, and provides no evidence span for the database's evidence-required constraint.

**Finding ALCSM-D2-01 [CRITICAL BLOCKER].** No date/recency field exists for certifications. The frozen D2 rubric weights certifications partly by currency; currency cannot be assessed for any of the 685 certification records as currently structured.

**Finding ALCSM-D3-01 [HIGH PRIORITY].** `AI_Related` and `Leadership_Role` are already-coded booleans (1,884/2,164 and 1,684/2,164 "Yes" respectively) rather than raw experience-description text a coder could independently judge. Reusing these flags as if they were annotation output would bypass the coding rulebook's own decision process entirely.

**Finding ALCSM-D4-01 [HIGH PRIORITY].** `Verified` is "Yes" for 685/685 certifications, 571/571 technical contributions, and 1,081/1,082 education records — effectively no variance. The frozen D4 rule permits external verification only to confirm or lower a score, with the verification method/source/outcome recorded; a single near-constant boolean with no accompanying source, timestamp, or outcome does not meet that bar and cannot be distinguished from a default value applied uniformly at collection time.

**Finding ALCSM-D5-01 [CRITICAL BLOCKER].** No leadership/strategic-scope evidence text exists on the profile side beyond a title string. On the job-requirement side, §9 documents that the `ALCSM_Dimension` field used during collection has no category corresponding to Leadership at all.

**Finding ALCSM-D6-01 [CRITICAL BLOCKER].** No field of any kind — in `Profile_Master` or any child sheet — captures engagement, posting activity, community role, or continuing-education signal. D6 currently has zero evidentiary basis in the collected dataset.

**Overall Task 4 conclusion:** annotation cannot proceed on this dataset as currently structured for any of the six dimensions without either (a) recovering additional raw evidence from the original profiles, or (b) an explicit, author-approved decision about how to proceed with structured-field-only evidence — which would itself be a methodology question for the author, not a decision this audit makes.

---

## 8. Raw Evidence Availability

| Evidence type required by the Annotation Handbook | Present in this repository? | Location if present |
|---|---|---|
| Profile headline | **No** | Not found in `Profile_Master` or any child sheet |
| About section | **No** | Not found |
| Experience descriptions (verbatim) | **No** | `Professional_Experience` has structured fields only; no description column survives after removing fully-empty columns |
| Education details (verbatim) | **No** | `Education` has coded fields only (`Degree_Level`, `Field_of_Study`) |
| Certification details (verbatim) | **No** | `Certifications` has coded fields only |
| Technical contribution evidence (verbatim) | **Partial** | `Technical_Contributions.Title` is a short label field, not a description or link; insufficient as standalone evidence |
| Engagement/community evidence | **No** | Not found anywhere |
| Raw job requirement text | **Yes** | `Job_Posting/.../Requirements.Requirement_Text` — 1,558/1,558 rows populated, 14–187 characters, no nulls or empty strings |
| Full raw job posting text (as opposed to per-requirement excerpts) | **No** | `Job_Master` has no full-posting-text column; only the already-segmented `Requirements` rows exist |
| `Profile_Master.Notes` (a short free-text field, not itself Handbook-required evidence) | Present, 100% populated, 29–172 characters (mean 95.5) | Too short and not positioned as evidence text; likely a collector's operational annotation, not transcribed profile content |

**Finding EVID-01 [CRITICAL BLOCKER — DATA-COLLECTION GAP].** With the sole exception of job-requirement text, none of the raw, verbatim evidence categories the Annotation Handbook requires exist anywhere in the current data repository. This is classified, per instruction, as a data-collection gap requiring attention before P4, not a defect this audit can remediate. Every one of the ALCSM-D1 through ALCSM-D6 findings in §7 traces back to this single root cause on the profile side.

---

## 9. Job Requirement Mapping Audit

`Requirements.ALCSM_Dimension` distribution (n = 1,558):

| ALCSM_Dimension value | Count | % of total |
|---|---|---|
| Not Directly Mapped | 875 | 56.2% |
| Experience | 543 | 34.9% |
| Education | 116 | 7.4% |
| Certifications | 18 | 1.2% |
| Community Engagement | 5 | 0.3% |
| Technical Publications | 1 | 0.06% |

**Finding MAP-01 [CRITICAL BLOCKER].** The controlled vocabulary used for `ALCSM_Dimension` during collection does not correspond one-to-one with the six frozen dimensions. There is no value at all corresponding to **Leadership (D5)**. Cross-tabulating against `Requirement_Category` shows why: of 221 requirements categorized as `"Leadership Experience"`, 216 were mapped to `"Experience"` and only 5 to `"Not Directly Mapped"` — none to anything resembling Leadership. Similarly, `"Technical Publications"` (a `Technical_Contributions`/D4 proxy) has only 1 record, and `"Community Engagement"` (a D6 proxy) has only 5. The six frozen dimensions are not altered by this finding — only the collection-time mapping scheme is being reported as inconsistent with them.

**Finding MAP-02 [HIGH PRIORITY] — quantified potential impact of the "Not Directly Mapped" bucket.** Cross-tabulating the 875 unmapped requirements against `Requirement_Category`:

| Requirement_Category | Unmapped count | Plausible dimension relevance |
|---|---|---|
| Technical Skill | 174 | D3/D4 |
| Communication | 170 | D5/D6 (ambiguous) |
| Business Strategy | 91 | D5 |
| Stakeholder Management | 89 | D5 |
| Other | 75 | Unclear without manual review |
| Governance | 71 | D5 |
| GenAI | 60 | D3 |
| Cloud Technology | 41 | D3 |
| Programming | 30 | D3/D4 |
| Machine Learning | 29 | D3 |
| MLOps | 26 | D3 |
| Data Science | 11 | D3 |
| Leadership Experience | 5 | D5 |
| AI Experience | 3 | D3 |

At minimum, the `Business Strategy` (91), `Stakeholder Management` (89), `Governance` (71), and residual `Leadership Experience` (5) categories — **256 requirements, 16.4% of the full corpus** — appear on their face to be D5-relevant and are currently unmapped or (in the case of the 216 already discussed) mismapped to Experience. This is a quantified estimate of potential remapping impact, not a remapping decision; no record has been changed.

**Recommendation (not executed).** A manual review pass over the 875 "Not Directly Mapped" records, cross-referenced against `Requirement_Category`, focused first on the `Business Strategy`/`Stakeholder Management`/`Governance`/`Leadership Experience` subset, using the frozen six dimensions (not the current ad hoc vocabulary) as the target categories, with a `Leadership` (D5) option added to whatever tool performs the remapping. This is a data-preparation recommendation; it does not alter the frozen ALCSM dimensions themselves.

---

## 10. Controlled Vocabulary Audit

Raw values are unaltered; this section records canonical **processed-representation recommendations only**.

| Field | Issue found | Example |
|---|---|---|
| `Profile_Master.Company_Size` | Capitalization inconsistency | `"Large Enterprise"` (94) vs `"Large enterprise"` (3) — same semantic value |
| `Profile_Master.Company_Size` vs `Job_Master.Company_Size` | Cross-workbook vocabulary mismatch | Profile side has an extra value `"Unclear"` not present in the job-posting side's vocabulary (`"Unknown"` only) |
| `Profile_Master.Collection_Status` | Spelling/form inconsistency | `"Complete"` (450) vs `"Completed"` (146) — same semantic value, two literal strings |
| `Profile_Master.Title_Category` | Overlapping/redundant categories | `"VP"`, `"Vice President"`, `"Vice President / Head"` co-exist as distinct values; similarly `"Chief"` / `"Chief Officer"` / `"C-Suite"`, and `"Lead"` / `"Lead / Manager"` / `"Manager"` |
| `Profile_Master.Title_Category` | Duplicate missingness semantics | Both `"Not Applicable"` and `"Not Visible"` exist as separate values with unclear differentiation |
| `Education.Degree_Level` | High fragmentation (20 distinct values for what should be a small ordinal scale) | `"Bachelor's"`, `"BA/MA"`, `"Master's"`, `"Master's Equivalent"`, `"MBA"`, `"Magister"`, `"Diplom"`, `"Diploma"`, `"Postgraduate Diploma"`, `"Professional Diploma"` all co-exist; German legacy degree titles (`"Magister"`, `"Diplom"`) are not mapped to an international-scale equivalent |
| `Education.Degree_Level` | Duplicate missingness semantics | Both `"Unknown"` and `"Not Visible"` exist as separate values |
| `Certifications.Certification_Category` | **Invalid value, not present in the workbook's own `Validation_List` dropdown source** | The value `"a"` appears in the data — a single-character entry that does not correspond to any of the 28 legitimate dropdown options, almost certainly a data-entry error |
| `Technical_Contributions.Contribution_Type` | Near-duplicate categories | `"Open Source Contribution"` vs `"Open-source Project"` |
| `Job_Master.Job_Title_Category` | Overlapping categories | `"AI Architecture"`, `"AI Architecture Leadership"`, and `"AI Engineering / Architecture"` are three related but distinct values that a reviewer may intend as one category |

**Finding VOCAB-01 [LOW PRIORITY].** None of the above affects the underlying collected evidence; all are presentation/normalization candidates for a future processed (not raw) dataset layer, consistent with `16_Data/`'s stated role as the home for cleaned/derived data, distinct from this raw collection artifact.

**Finding VOCAB-02 [MEDIUM PRIORITY].** The single `"a"` value in `Certification_Category` is a clear data-entry error (not merely a style variant) and should be flagged for the collector to correct at source in a future collection pass — not corrected here, per the read-only instruction.

---

## 11. Critical Issues

| ID | Finding | Severity |
|---|---|---|
| GOV-01 | No documented ethics-committee approval, DPO sign-off, or resolution of the `Task5_Implementation_Readiness_Checklist.md` §3 blockers found anywhere in `DECISION_LOG.md`, `04_Ethics/`, or elsewhere in the repository | **CRITICAL BLOCKER** |
| GIT-01 | `.gitignore` does not cover `05_Data_Collection/LinkedIn_Profiles/` or `05_Data_Collection/Job_Postings/` (only `05_Data_Collection/Raw_Data/` and `05_Data_Collection/Logs/` are excluded) — the two raw workbooks, containing direct identifiers, are currently unprotected against accidental `git add` | **CRITICAL BLOCKER** |
| PII-01 | Raw workbook retains direct identifiers (`LinkedIn_URL` for all 611 profiles; `Posting_URL`) with no pseudonymization or migration into the frozen, identifier-free database schema performed yet | **CRITICAL BLOCKER** |
| DUP-01 | 15 of 16 duplicate-individual groups (by `LinkedIn_URL`) span both included and excluded populations | **CRITICAL BLOCKER** |
| REF-01 | Child evidence sheets contain 245 rows across 79 distinct excluded profiles, with no structural safeguard preventing their use downstream | **CRITICAL BLOCKER** |
| EVID-01 | No raw, verbatim evidence text exists for D1, D2, D3, D5, or D6 anywhere in the LinkedIn dataset | **CRITICAL BLOCKER** |
| ALCSM-D1-01 | Education captured as pre-coded fields only, not verbatim text | **CRITICAL BLOCKER** |
| ALCSM-D2-01 | No certification date/recency field exists | **CRITICAL BLOCKER** |
| ALCSM-D5-01 | No leadership evidence text; job-requirement side has no Leadership mapping category at all | **CRITICAL BLOCKER** |
| ALCSM-D6-01 | No engagement/community evidence field exists anywhere | **CRITICAL BLOCKER** |
| MAP-01 | Job-requirement dimension-mapping vocabulary omits Leadership entirely; 56.2% of requirements unmapped | **CRITICAL BLOCKER** |

## 12. Non-Critical Issues

| ID | Finding | Severity |
|---|---|---|
| DASH-01 | Both Dashboard sheets are stale relative to their own workbook's data | HIGH PRIORITY |
| ALCSM-D3-01 | Experience evidence is pre-coded (booleans), not raw text | HIGH PRIORITY |
| ALCSM-D4-01 | `Verified` flags show effectively no variance and carry no provenance | HIGH PRIORITY |
| MAP-02 | ~256 requirements (16.4%) plausibly D5-relevant sit in "Not Directly Mapped" or mismapped to "Experience" | HIGH PRIORITY |
| REF-02 | `Collection_Status` and `Included` are not fully consistent (96 rows) | INFORMATIONAL |
| DUP-02 | `LinkedIn_URL` column mixes real URLs, malformed URLs, and text placeholders with no distinguishing flag | MEDIUM PRIORITY |
| DUP-03 | 7 content-duplicate child rows (1 Certification, 6 Experience) | LOW PRIORITY |
| DUP-04 | 3 postings share a normalized URL | LOW PRIORITY |
| VOCAB-01 | Multiple controlled-vocabulary normalization candidates (casing, redundant categories, fragmentation) | LOW PRIORITY |
| VOCAB-02 | One clear data-entry error (`Certification_Category = "a"`) | MEDIUM PRIORITY |

## 13. Recommended Corrections

**None of the following have been applied. All require your explicit review and, where they touch the raw workbooks, must be applied to a new versioned copy — the raw workbooks themselves remain untouched per instruction.**

1. Confirm real ethics-committee approval and DPO sign-off status; if obtained, record it in `DECISION_LOG.md` and `04_Ethics/` with a reference number and date. If not yet obtained, treat all findings below as preparatory only.
2. Add `05_Data_Collection/LinkedIn_Profiles/` and `05_Data_Collection/Job_Postings/` (or their `01_Raw/` subpaths specifically) to `.gitignore` immediately, and confirm neither file has ever been staged or committed (`git log --all -- <path>` returns nothing for both as of this audit).
3. Decide and document a pseudonymization/migration plan moving this data into the frozen database schema (which structurally cannot hold `LinkedIn_URL`), consistent with `Task5_P3_Sampling_Framework_Design.md` and the existing `collection/helper.py` write path.
4. Manually review the 15 cross-population duplicate-individual groups (§4.1) and resolve which population each individual actually belongs to.
5. Regenerate both Dashboard sheets from current data.
6. Decide how to handle the 245 child-sheet rows belonging to excluded profiles (exclude from any derived/processed dataset, at minimum).
7. Resolve the raw-evidence gap (§8): either recover verbatim profile text for a representative subset, or make an explicit, author-level methodology decision about proceeding with structured-field-only evidence, before P4 annotation design proceeds further.
8. Add a certification date/recency field, or confirm its absence is a permanent, disclosed limitation.
9. Add a Leadership (D5) category to the job-requirement dimension-mapping vocabulary and manually review the 875 "Not Directly Mapped" and 216 "Experience"-mapped-but-Leadership-flavored records against it.
10. Correct the single `"a"` value in `Certification_Category` at source in a future data pass.
11. Normalize the controlled-vocabulary variants in §10 in any processed/derived copy of this data (never in the raw workbook).

## 14. P4 Readiness Assessment

P4 (annotation interface and pilot coding) requires, at minimum, a dataset with (a) confirmed ethics clearance, (b) a demonstrably disjoint included/excluded population, (c) raw evidence text an annotator can independently read and judge per the frozen Coding Rulebook and Annotation Handbook, and (d) a job-requirement corpus mapped to the six frozen dimensions with reasonable completeness. None of these four conditions is currently met. This dataset, as it stands, cannot support P4 annotation without further collection or an explicit, author-approved decision on how to proceed despite the gaps identified.

---

## Data Freeze Recommendation

### NOT READY FOR DATA FREEZE

**Every blocker below must be resolved, or explicitly and knowingly accepted by the author with a documented rationale, before this dataset is frozen for use in P4:**

1. **GOV-01** — Confirm and document real ethics/DPO clearance.
2. **GIT-01** — Close the `.gitignore` gap over the raw-data folders immediately; this is an active risk independent of every other finding.
3. **PII-01** — Decide and execute (or explicitly defer with rationale) the pseudonymization/migration path before any wider circulation of this workbook.
4. **DUP-01** — Resolve the 15 cross-population duplicate individuals.
5. **REF-01** — Decide how excluded-profile child records are handled in any derived dataset.
6. **EVID-01 / ALCSM-D1-01 / ALCSM-D2-01 / ALCSM-D5-01 / ALCSM-D6-01** — Resolve the raw-evidence and dimension-specific gaps; this is the largest body of work and the one most likely to require an author-level scoping decision rather than a data-cleaning fix.
7. **MAP-01** — Decide how Leadership-relevant job requirements will be represented before any RQ2 gap analysis depends on this mapping.

Once these are resolved, a future audit session can re-run this same procedure against the corrected data and, if clean, propose a concrete `DATA-v1.0` freeze specification (profile/posting/requirement counts, source workbook versions, schema version, framework version, collection window, QA status) at that time. That specification is not proposed now, because freezing a dataset with unresolved critical blockers would misrepresent its readiness.

---

*This report is an audit record. It modifies no raw data, no ALCSM methodology, no database schema, and no Git history.*
