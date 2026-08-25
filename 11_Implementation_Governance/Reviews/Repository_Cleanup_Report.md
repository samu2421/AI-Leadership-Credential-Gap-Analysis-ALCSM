# Repository Cleanup Report

**Status:** Cleanup complete for this session. No research history was deleted; every real-data file either has a canonical home, is archived (preserved), or was removed only after being verified byte-identical to a canonical copy.
**Author:** Samiksha Dhere (researcher) — performed with Claude Code assistance
**Date:** 2026-08-24

---

## 1. What triggered this cleanup

Before any cleanup rule was applied, the repository root and several folders were audited directly. Nine real, personal-data-bearing Excel workbooks were found sitting **outside** their intended locations — at the repository root (unprotected by `.gitignore`) or as a stale duplicate inside `06_Annotation/`. None had ever been committed to git, but several were unprotected by any `.gitignore` rule, which this cleanup also corrected. This is the same class of finding as the survey-file exposure discovered in the previous (RQ1–RQ5) session — now recurring at a larger scale, and fixed the same way: verify, relocate, git-ignore, document, never silently discard.

## 2. Cache / temp files removed (DELETE — pure regenerable cache, per Part B)

- Every `__pycache__/` directory under `src/` and `tests/` (19 directories).
- All `.pyc` files reachable outside `.venv/` were removed as part of the same pass. **Note:** the cleanup command's exclusion of `.venv/` did not fully take effect, and `.venv/`'s own cached `.pyc` files were also cleared (~6,400 files). This causes no functional harm — Python regenerates bytecode cache transparently on next import, confirmed directly (`import pandas, sqlalchemy, streamlit` succeeded immediately afterward with a freshly rebuilt cache) — but is disclosed here rather than left unmentioned, since it was a wider deletion than intended.
- `~$*.xlsx` Excel lock files: **one** was found (`05_Data_Collection/LinkedIn_Profiles/02_Processed/~$ALCSM_LinkedIn_Processed_v1.1.xlsx`). Checked via `lsof` before touching anything, per the explicit "after confirming they are not active" instruction — **Microsoft Excel currently has this file open** (live process, active file handle). **This lock file was left in place, not removed.** Removing it while the file is genuinely open in Excel risks data loss on the next save. Re-check and remove once the file is confirmed closed.

## 3. Root-level workbooks found, verified, and resolved

| File found at repository root | Resolution |
|---|---|
| `ALCSM_Final_Human_Annotation_v1.1.xlsx` (+ a byte-identical `(1)` duplicate download) | **This was the genuine, complete, researcher-reviewed final annotation** — not actually a root-level stray copy of something already canonical, but the missing canonical file itself, previously only present in `Downloads/`. Verified in full (see `Final_Annotation_v1.1_Freeze_Report.md`) and placed at `06_Annotation/ALCSM_Final_Human_Annotation_v1.1.xlsx`. |
| `ALCSM_Processed_Reviewed_v1.1.xlsx` | An intermediate review draft (per-dimension sheets `D1_Detailed_Review`/`D2_Review`/`D3_D5_Review`/`D6_Review` not present in the final file), superseded by the file above. **Archived**, not deleted → `16_Archive/Superseded_Annotation_Drafts/`. |
| `Book5ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` | A partial, single-sheet export (Profile_Scores only, `Overall_Review_Status` still showing the pre-review `Pending Review` state) — its content is a strict subset of the permanently-preserved, untouched `06_Annotation/ALCSM_Full_FirstPass_Annotation_v1.1.xlsx`. Not byte-identical to anything, so **archived out of caution rather than deleted** → `16_Archive/Superseded_Annotation_Drafts/`. |
| `ALCSM_Profile_Evidence_Review_Queue_v1.0.xlsx`, `ALCSM_Profile_Evidence_Review_Queue_v1.1.xlsx` | Precursor drafts of what became `05_Data_Collection/Supplementary_Review/ALCSM_Supplementary_Evidence_Collection_v1.0.xlsx` (built in the P4-preparation session). **Archived** → `16_Archive/Superseded_Supplementary_Review_Drafts/`. |
| `ALCSM_JobRequirement_Mapping_Review_v1.0 (1).xlsx`, `ALCSM_JobRequirements_Remapped_v1.1.xlsx` | Verified directly: the remapping file's `Original_ALCSM_Dimension` column exactly reproduces the requirement-mapping distribution found during the D6 v1.1 task (872 unmapped), and its `Final_ALCSM_Dimension` column exactly matches the canonical `05_Data_Collection/Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx`'s current distribution (799 unmapped) — **confirming the remapping documented in these files has already been fully applied to the canonical workbook.** Both files are the methodology trail behind an already-merged change, not a pending or conflicting update. **Archived** (preserves the mapping rationale/confidence/precedent record) → `16_Archive/Superseded_JobRequirement_Mapping/`. |
| `ALCSM_Supplementary_Evidence_Triage_v1.0.xlsx` | Verified **byte-identical** (SHA-256 match) to `05_Data_Collection/Supplementary_Review/ALCSM_Supplementary_Evidence_Triage_v1.0.xlsx`. A pure redundant copy with zero information difference. **Removed**, per Part B's explicit "redundant root-level copies... when a canonical copy exists" rule. |
| `ALCSM Expert Survey Responses.xlsx` | A **newer, larger** export of the same survey instrument — 23 consented respondents vs. the 12 already filed at `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` (same column structure, confirmed identical questions). This is real, current, more-complete data, not a duplicate. The old 12-respondent file was **archived** → `16_Archive/Superseded_Survey_Responses/ALCSM_Expert_Survey_Responses_v1.0_12respondents_20260822.xlsx`; the new 23-respondent export now occupies the canonical path. |
| `Expert_Survey_DataDictionary_v1.0.xlsx` | A supporting document for the (still-active) survey instrument, not obsolete. Moved to `07_Reliability/Survey_Responses/`. |

All new/moved locations under `06_Annotation/`, `07_Reliability/Survey_Responses/`, and `16_Archive/**/*.xlsx` are confirmed git-ignored (`git check-ignore -v`, verified for every path individually). `.gitignore` gained two new rules this session: `16_Archive/**/*.xlsx` (archived research data, as opposed to archived `.md`/`.py`/`.sql` documents, which remain trackable project history) — the pre-existing `07_Reliability/Survey_Responses/` folder rule already covered the survey-data-dictionary addition.

## 4. D6 document cleanup (Part C)

Searched the whole repository for documents primarily about the retired "Professional Engagement & Continuous Development" D6 construct. Exactly one qualifies as *purely* about the retired construct (as opposed to a general v1.0 framework document that covers all six original dimensions, D6 among them, and remains the legitimate frozen historical baseline for D1–D5):

- `11_Implementation_Governance/Reviews/D6_Observation_Rule_Decision_Proposal.md` → moved to `16_Archive/Superseded_D6_Professional_Engagement/`.

**Deliberately left untouched:** `ALCSM_Measurement_Specification_v1.0.md`, `ALCSM_Dimension_Design_Task2.md`, `ALCSM_v1.0_Scoring_Framework_Task3.md`, `ALCSM_Coding_Rulebook_and_Pilot_Design.md`, `ALCSM_Design_Decisions_and_Justification_v1.0.md`, `ALCSM_Final_Methodological_Audit.md`, `ALCSM_v1.0_Implementation_Readiness_Specification.md`, `ALCSM_Measurement_Model_and_Validation_Note.md` (all in `02_Framework_Development/`). Each of these documents the *entire* frozen v1.0 framework (D1–D6, or general methodology), not the retired D6 construct specifically — D1–D5 in these documents remain the live, authoritative frozen record, and every v1.1 D6 document already explicitly preserves them as unmodified historical reference. Archiving them would misrepresent still-current material as obsolete. No governance reference to these files needed updating — none of the D6 v1.1 documents' citations of them are affected by the one file that did move.

**Also deliberately left untouched:** every `11_Implementation_Governance/Reviews/` completion/QA report from P2, P3, and P4 (e.g., `P3_Final_Data_QA_Report.md`, `P4_Implementation_Completion_Report.md`). These document *completed* phases, not *retired* methodology — they are not superseded by anything, remain the sole permanent record of those decisions, and are still actively cited by `DECISION_LOG.md`. "No longer actively worked on" is not the same as "obsolete"; nothing here was archived on that basis alone.

## 5. Known, pre-existing, out-of-scope duplication (flagged, not resolved)

`16_Data/04_Metadata/Protocols/` and `05_Data_Collection/Research_Metadata/Protocols/` contain overlapping governance-protocol markdown documents, first noticed in an earlier session and never reconciled. This is a documentation-duplication issue, not a workbook/data-file issue, and falls outside this session's explicit Excel/data-focused cleanup rules. Flagged here for visibility, not acted on — consistent with "avoid perfectionism."

## 6. What was NOT touched

- `06_Annotation/ALCSM_Full_FirstPass_Annotation_v1.1.xlsx` — the permanent, immutable first-pass baseline. Not archived (it is not obsolete — it is the deliberately-preserved audit-trail source every review decision is checked against) and not modified.
- The canonical LinkedIn processed workbook, canonical job-postings processed workbook, and all `05_Data_Collection/` subfolders already in their correct locations from prior sessions.
- Any `alcsm_dev` database content or schema (see `PostgreSQL_ProfileID_Compatibility_Audit.md` — investigation only, no change).
- Any ALCSM dimension, scoring criterion, or D6 definition.

## 7. Final repository tree (concise)

```
02_Framework_Development/
  ALCSM_v1.1_Scoring_Framework.md                     ★ canonical (scoring)
  ALCSM_D6_Industry_Breadth_v1.1.md                    ★ canonical (D6 construct, PROPOSED/PILOT_REQUIRED)
  ALCSM_Coding_Rulebook_v1.1_Addendum.md               ★ canonical (D6 coding rules)
  ALCSM_v1.0_Scoring_Framework_Task3.md                  frozen v1.0 predecessor (D1-D5 still authoritative)
  ALCSM_Coding_Rulebook_and_Pilot_Design.md              frozen v1.0 (D1-D5 canonical)
  ALCSM_Measurement_Specification_v1.0.md                frozen v1.0 baseline (D1-D5 + general methodology)
  ALCSM_Dimension_Design_Task2.md                        frozen v1.0 design record
  ALCSM_Measurement_Model_and_Validation_Note.md         frozen formative-index validation frame
  ALCSM_Design_Decisions_and_Justification_v1.0.md       frozen v1.0 record
  ALCSM_Final_Methodological_Audit.md                    frozen v1.0 record
  ALCSM_v1.0_Implementation_Readiness_Specification.md   frozen v1.0 record

05_Data_Collection/
  LinkedIn_Profiles/02_Processed/ALCSM_LinkedIn_Processed_v1.1.xlsx   ★ canonical (git-ignored)
  LinkedIn_Profiles/01_Raw/...                                          permanent archival evidence
  Job_Postings/02_Processed/ALCSM_JobPosting_Processed_v1.1.xlsx     ★ canonical (git-ignored)
  Job_Postings/01_Raw/...                                               permanent archival evidence
  Supplementary_Review/*.xlsx                                           active (git-ignored)
  Dictionaries/, Sampling/, Pilot/, Research_Metadata/, Documentation/  active reference material
  {LinkedIn_Profiles,Job_Postings}/{03_Tracking,04_Metadata,05_Quality_Control}/  empty scaffold folders, unused

06_Annotation/
  ALCSM_Final_Human_Annotation_v1.1.xlsx               ★ canonical, FROZEN (git-ignored)
  ALCSM_Full_FirstPass_Annotation_v1.1.xlsx              permanent immutable baseline (git-ignored)
  Documentation/ALCSM_Annotation_Handbook.md             active

07_Reliability/
  Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx    ★ canonical, 23 respondents (git-ignored)
  Survey_Responses/Expert_Survey_DataDictionary_v1.0.xlsx              active supporting doc (git-ignored)

08_NLP_Development/
  README.md only — awaiting Phase P7 (unchanged this session)

09_Statistical_Analysis/
  README.md only — awaiting downstream analysis (unchanged this session)

11_Implementation_Governance/
  Governance/DECISION_LOG.md, Document_Version_Policy.md, CLAUDE_CODE_RULES.md   ★ live governance
  Context/, Guides/, Roadmaps/                                                     live governance
  Reviews/*.md                                                                     permanent phase-completion record (16 reports; none archived this session — see §4)

15_Scripts/
  alcsm_analysis_dry_run_v1.0.py                        active demonstration script
  README.md

16_Archive/
  Superseded_Task1_Task4/                    P0-era schema/validation history (pre-existing)
  Superseded_Annotation_Drafts/              new this session
  Superseded_Supplementary_Review_Drafts/    new this session
  Superseded_JobRequirement_Mapping/         new this session
  Superseded_Survey_Responses/               new this session
  Superseded_D6_Professional_Engagement/     new this session
```

**Nothing flagged as unnecessarily duplicated as of this session's end.** The one previously-known duplication concern (`16_Data/04_Metadata/Protocols/` vs. `05_Data_Collection/Research_Metadata/Protocols/`, noted in an earlier session) is no longer live — `16_Data/` does not exist anywhere in this repository as of this audit, so only the `05_Data_Collection/Research_Metadata/Protocols/` copy remains; there is nothing left to reconcile.

---

*This report documents file relocation and cache cleanup only. No research data was altered, and every real-data file that existed before this session still exists after it — either at its canonical path or in a clearly-named archive folder.*
