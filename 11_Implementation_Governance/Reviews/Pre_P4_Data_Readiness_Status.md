# Pre-P4 Data Readiness Status

**Version:** 1.0
**Status:** Final for this session. Consolidates Tasks 1–6 of the final pre-annotation data-preparation stage. Audit/planning only — no supplementary data collected, no raw file modified, no profile scored, P4 not started.
**Purpose:** give a single, current answer to "is this dataset ready for supplementary evidence collection" for an MSc thesis with an approximately three-week submission horizon, per the explicit scope framing: transparent, reproducible, methodologically defensible — not exhaustive.
**Last Updated:** 2026-08-17
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

---

## 1. Current Dataset Status

| Metric | Value | Source |
|---|---|---|
| LinkedIn profiles originally collected | 611 | `01_Raw/ALCSM_LinkedIn_DataCollection_v1.0.xlsx` (archival) |
| Included profiles (final analytical population) | 500 | `02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx` — confirmed as exactly 500 rows, 500 distinct `Profile_ID`, 0 duplicates |
| Job postings | 201 | `02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx` |
| Job requirement records | 1,558 | Same, `Requirements` sheet |
| Requirement-to-dimension mapping | Completed pass performed (see §6) | `Final_ALCSM_Dimension` column present in the processed Requirements sheet |

Independently re-verified: the processed LinkedIn `Profile_Master` no longer carries `LinkedIn_URL`, `Collection_Date`, `Collector`, `Included`, or free-text `Notes` — direct identifiers and collection-internal fields have been stripped at this layer, and the 111 excluded / cross-population-duplicate profiles previously flagged in `P3_Final_Data_QA_Report.md` (Findings DUP-01, REF-01) are no longer present. This is substantial, real remediation of two of that report's five CRITICAL BLOCKER findings.

## 2. Processed-Data Source-of-Truth

`02_Processed/` is now documented as the authoritative analytical working layer for both corpora (`05_Data_Collection/LinkedIn_Profiles/README.md`, `05_Data_Collection/Job_Postings/README.md`, both rewritten this session). `01_Raw/` is documented as permanent, read-only archival evidence — retained, never deleted, never used as an analytical source from this point forward.

**Git-safety verification performed:**

| Check | Result |
|---|---|
| Raw workbooks excluded from Git | ✅ `.gitignore` covers `05_Data_Collection/LinkedIn_Profiles/01_Raw/` and `05_Data_Collection/Job_Postings/01_Raw/` |
| Processed workbooks excluded from Git | ✅ `.gitignore` covers `05_Data_Collection/LinkedIn_Profiles/02_Processed/` and `05_Data_Collection/Job_Postings/02_Processed/` |
| Any raw or processed workbook ever tracked in Git history | ✅ Confirmed clean — `git log --all --diff-filter=A` for `*.xlsx` returns nothing; `git ls-files` for `*.xlsx` returns nothing |
| Temporary Excel lock files | ❌ **Two remain**: `05_Data_Collection/LinkedIn_Profiles/02_Processed/~$ALCSM_LinkedIn_Processed_v1.1.xlsx` and `05_Data_Collection/Job_Postings/02_Processed/~$ALCSM_JobPosting_Processed_v1.1.xlsx`. **Not deleted by this session** — a lock file normally indicates the workbook is (or recently was) open in Excel; removing it without confirming that is a decision for you, not something to do silently. Please close both workbooks in Excel (which removes the lock file automatically) or confirm it is safe to delete manually. |

No raw file was modified, renamed, or deleted in producing this report (confirmed via unchanged file modification timestamps, checked immediately before writing this section).

## 3. Ethics / Supervisor Status

Recorded factually in `04_Ethics/07_Institutional_Correspondence/ALCSM_Ethics_SupervisorReviewRecord_v0.1-DRAFT.md` and `DECISION_LOG.md` D-0036: the researcher reports the thesis supervisor reviewed the ethics/data-collection documentation in an in-person meeting and gave a positive indication to proceed. Meeting date, supervisor name, and exact wording are recorded as placeholders pending confirmation.

**This is not, and is not described as, formal ethics-committee approval or DPO sign-off.** Finding GOV-01 from `P3_Final_Data_QA_Report.md` remains open: no institutional approval reference, DPO sign-off, or Article 14 position is documented anywhere in this repository. This distinction is load-bearing for §7 and §9 below.

## 4. D6 Final Rule

Finalized and recorded in `DECISION_LOG.md` D-0037, confirmed as an operational clarification of the frozen D6 dimension (no rubric, taxonomy, or measurement-model change):

- **Window:** 12 months immediately preceding each profile's `collection_ts`.
- **Qualifies:** publicly visible original posts; publicly visible reshares/reposts; visible professional commentary; publicly stated community/professional roles; continuing-development signals where publicly stated and presented as engagement.
- **Excluded:** follower/connection counts, reach metrics, inferred engagement, private/connection-only content, non-LinkedIn activity not presented on LinkedIn.
- **Missingness:** an observable-but-empty activity surface → `present`/score 0 (an observed finding); an unavailable activity surface → `unavailable`/score 0 (a data gap) — never conflated.

No new schema field is required — `profile.activity_data_collected`, `profile.observation_window_days`, and the already-frozen `'activity'` value of `profile_raw_section.section_name` are sufficient, as established in `D6_Observation_Rule_Decision_Proposal.md` §6.

**The rule is finalized. Permission to apply it by collecting real supplementary evidence is a separate question — see §7.**

## 5. Supplementary Evidence Queue

Created at `05_Data_Collection/Supplementary_Review/ALCSM_Supplementary_Evidence_Queue_v1.0.xlsx` — **one combined queue, 500 rows (one per included profile), no per-dimension duplication**, with columns `Profile_ID`, `D1`–`D6_review_required` (boolean), `D1`–`D6_evidence_needed` (short rule-based reason string), `Review_Status` (initialized to "Not Started" for every row), `Reviewer_Notes` (blank, for the researcher to fill during actual review), and `Collection_Timestamp` (sourced by reference from the archival raw workbook, read-only join on `Profile_ID`).

**Flagging logic** (rule-based, computed from the processed dataset — not inferred, not fabricated; full rules documented here for transparency and reproducibility):

| Dimension | Rule | Profiles flagged | Rationale (Task 5 scoping principle applied) |
|---|---|---|---|
| D1 | Ambiguous/missing `Degree_Level` (`Not Visible`/`Unknown`/`Other`) on any education record, or no education record at all | 66 / 500 (13.2%) | "Only the small set already requiring targeted clarification" |
| D2 | ≥1 certification on file (no certification anywhere has a date; recency is relevant whenever a certification exists) | 234 / 500 (46.8%) | "Only where the scoring rule makes recency relevant" |
| D3 | No AI-related role recorded, OR AI-related role duration unrecorded, OR total AI-related experience duration falls in the 10–40-month band spanning the rubric's 1–2yr/3yr boundary | 93 / 500 (18.6%) | "Prioritize profiles where structured evidence cannot distinguish the band" |
| D4 | ≥1 technical contribution on file (verification status is absent from the processed layer entirely, for every record) | 175 / 500 (35.0%) | "Only where needed to resolve an actual verification requirement" |
| D5 | `Title_Category` is anything other than the two lowest-stakes values (`Manager`, `Lead`) — i.e. any title whose rubric band depends on confirming strategic/enterprise-strategy/augmentation-aware language | 474 / 500 (94.8%) | See flag below |
| D6 | Universal — no engagement evidence exists for any profile under any prior protocol | 500 / 500 (100%) | Applies the finalized rule consistently, per explicit instruction |

**Flag for your attention on D5.** 474 of 500 profiles (94.8%) are flagged, which is a materially higher proportion than D1–D4. This is not an error in the rule — it follows directly from the frozen D5 rubric itself, which requires confirming *language* ("strategic language," "explicit enterprise-strategy responsibility," "augmentation-aware framing") at every band above 2, and this study population is title-gated to leadership roles by design, so most titles genuinely do sit at Director/VP/Chief tier where that language confirmation is rubric-required, not optional. I have not narrowed this further myself, because doing so would mean deciding — rather than reporting — a scope trade-off that is yours to make. Two options, stated without a recommendation between them: (a) accept the 474-profile scope, given D5 is central to this thesis's core research question; or (b) adopt a further pragmatic simplification (e.g., treat title-tier alone as sufficient for a default-low score absent confirming language, reducing the review set) — which would itself be worth a one-line note in your Methods/Limitations text if adopted, since it is a real scoping choice, not a data artifact.

## 6. Taxonomy Status

Per instruction, **no taxonomy terms were generated this session.** Status of the eight frozen taxonomies (`ALCSM_Measurement_Specification_v1.0.md` §2):

| # | Taxonomy | Structure | Current version status | Terms present |
|---|---|---|---|---|
| 1 | Degree (D1) | Frozen | Not yet anchored/stamped | 0 |
| 2 | Certification (D2) | Frozen | Not yet anchored/stamped | 0 |
| 3 | AI role (D3) | Frozen | Not yet anchored/stamped | 0 |
| 4 | Leadership-level (D5) | Frozen | Not yet anchored/stamped | 0 |
| 5 | Technical contribution (D4) | Frozen | Not yet anchored/stamped | 0 |
| 6 | Professional engagement (D6) | Frozen | Not yet anchored/stamped | 0 |
| 7 | AI keyword ontology | Frozen | Not yet anchored/stamped | 0 |
| 8 | Automation vs. augmentation | Frozen | Not yet anchored/stamped | 0 |

No `taxonomy_version` row has ever been written against real data in this project (confirmed by the full P3 session history — only throwaway test clusters have ever exercised `create_taxonomy_version`/`insert_taxonomy_terms`). This is unchanged by anything in this session.

**Source posting corpus is now real and usable:** 201 processed job postings, 1,558 requirement records, `Requirement_Text` 100% populated with verbatim, non-empty text (14–187 characters). The requirement-to-dimension mapping pass is substantially complete — `Final_ALCSM_Dimension` now includes a proper D5 (Leadership) category (397 records, resolving the prior audit's MAP-01 CRITICAL finding of zero Leadership-mapped requirements) — but 872 of 1,558 requirements (56.0%) remain `"Not Directly Mapped"`, essentially unchanged in volume from the prior audit's 875, concentrated in Technical Skill, Communication, Business Strategy residual, Cloud Technology, and similar categories.

**Can anchoring now proceed?** From a **data-availability** standpoint, yes — the raw material (a real, verbatim, non-trivial posting-requirement corpus) now exists where it did not before. From a **software** standpoint, no — `anchor_taxonomy_from_postings()` remains an intentionally unimplemented stub (deferred since P3 Session 2), and the extraction method/threshold has never been decided. Per instruction, this session does not build it or decide that method; it only confirms the corpus is now ready to be anchored against, once that separate build step happens.

## 7. Remaining Blockers

| # | Blocker | Status |
|---|---|---|
| 1 | Formal ethics-committee approval / DPO sign-off | **Open.** Only a supervisor's informal, in-person review is documented (§3); this is explicitly not equivalent. |
| 2 | Activity-specific ethics justification (DPIA/LIA addendum for D6 observation) | **Open.** The draft protocol requires it; it has not been drafted. |
| 3 | Two Excel lock files in `02_Processed/` | **Open**, low severity — see §2. |
| 4 | D5 supplementary-review scope (474/500) | **Open** — a scoping decision for you, not a defect (§5). |
| 5 | Taxonomy-anchoring extraction algorithm | **Open**, not in scope for this session (§6) — the corpus is ready; the software and method decision are not. |
| 6 | 56% of job requirements remain "Not Directly Mapped" | **Open**, carried forward from the prior audit's MAP-02 finding — largely unchanged despite the D5 remapping improvement. |

## 8. Recommended Next Action

In order: (1) resolve or explicitly accept blocker #1/#2 with your supervisor/institution before any real supplementary collection occurs, since that gate is independent of everything else in this report and cannot be worked around by data-quality improvements; (2) close the two Excel lock files; (3) decide the D5 scope question in §5; (4) only then, with those resolved, supplementary evidence collection against the queue in §5 becomes executable — still as its own, separate, explicitly-authorized session, not automatically triggered by this report.

## 9. P4 Readiness Criteria

Unchanged from `P3_Final_Data_QA_Report.md` §14: P4 requires (a) confirmed ethics clearance, (b) a demonstrably disjoint included/excluded population, (c) raw evidence text an annotator can independently judge, and (d) a job-requirement corpus reasonably mapped to the six frozen dimensions. (b) is now substantially satisfied by the processed layer (§1). (c) remains unmet for D1–D5's verbatim-text gap and D6's total absence, pending the supplementary review this report prepares for. (d) has improved materially (D5 mapping resolved) but the 56% unmapped residual (§6) is still a real gap. (a) is unchanged and remains the hardest blocker.

---

## Recommendation

### NOT READY

*(for supplementary evidence collection — as distinct from readiness to plan and specify it, which this session and the prior D6 proposal both advance.)*

Not ready because blockers #1 and #2 in §7 are unresolved and are, by this project's own standing rule, absolute: no real personal data collection proceeds without ethics clearance, regardless of how well-specified the collection plan is. Everything else in this report — the queue, the finalized D6 rule, the processed-data documentation — is genuinely ready and waiting on that one gate, not on further data-preparation work.

---

*This report is a planning and status document. It modifies no ALCSM methodology, no database schema, no raw data, and collects no supplementary evidence. Supplementary collection and P4 remain unauthorized pending your review.*
