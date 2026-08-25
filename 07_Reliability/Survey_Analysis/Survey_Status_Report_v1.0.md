# Expert Survey Status Report v1.0

**Status:** A newer raw response-level export was found and promoted to canonical this session. Survey analysis is not blocked.
**Author:** Samiksha Dhere (researcher) — investigated with Claude Code assistance

---

## What was searched

Per this session's Part G, searched for a raw Google Forms response-level export (as opposed to a pre-aggregated summary) in: `07_Reliability/Survey_Responses/`, `~/Downloads`, `~/Desktop`, `~/Documents` (shallow).

## What was found

The canonical file at `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx` was, and remains, genuinely **response-level** — 27 columns, one row per respondent, individual Likert-scale answers per dimension per question, not a pre-aggregated summary table. It was never the pre-aggregated file; that description fits `07_Reliability/Survey_Analysis/ALCSM_Survey_Analysis_Processed_v1.0.xlsx` instead, which is a *derived* summary this project's own scripts produce from the raw file, not a separate source.

**A newer raw export was found** at `~/Downloads/ALCSM Expert Survey Responses.xlsx` — same 27-column structure, but **24 consented responses instead of 23**. Every one of the 23 canonical rows (matched by `Timestamp`) is present in the Downloads copy; the Downloads copy has exactly one additional row, timestamped `2026-08-24 21:37:20.404` — after the canonical file was last synced into the repository. This is a legitimate newer export of the same Google Form, not a different survey or a corrupted file.

## Action taken

Following this project's established version-update procedure (same procedure used for the 12→23 respondent update in a prior session):

1. Archived the 23-respondent file to `16_Archive/Superseded_Survey_Responses/ALCSM_Expert_Survey_Responses_v1.0_23respondents_20260824.xlsx`.
2. Promoted the 24-respondent Downloads file to the canonical path, `07_Reliability/Survey_Responses/01_Raw/ALCSM_Expert_Survey_Responses_v1.0.xlsx`.
3. Updated `Document_Version_Policy.md`'s canonical register and archive-folder description.
4. Re-ran `15_Scripts/alcsm_survey_analysis_v1.0.py` and `Survey_Analysis_Plan_v1.0.md`'s headline table against the new file — no code change was required; the existing `alcsm.analysis.survey`/`rq3_validation.content_validity_summary` modules read it correctly as-is.

Nothing was fabricated: every number now in `Survey_Analysis_Plan_v1.0.md` §4 and `ALCSM_Survey_Analysis_Processed_v1.0.xlsx` comes directly from this real, found file.

## What can and cannot currently be calculated

| Item | Status |
|---|---|
| Participant background (role, years experience, AI experience, leadership experience) | **Available** — 24/24 respondents, real counts. |
| Dimension relevance (mean/median, 1–5) | **Available** — 24/24 answered every dimension. |
| Dimension clarity (mean/median, 1–5) | **Available** — 24/24 answered every dimension. |
| Dimension distinctiveness | **Not calculable** — 0 of 24 respondents answered any distinctiveness item, for any dimension. This is a property of the real, current data (nobody has answered this section, in either the 23- or 24-respondent export), not something withheld or fabricatable. Reported as a stated limitation, not silently omitted. |
| Overall framework appropriateness | **Available** — mean 3.42 (24/24 answered). |
| Most-important-dimension counts | **Available** — D3 leads with 9 of 24 picks. Not converted into a weight (§3 of the Plan). |
| Open-comment themes | **Comment COUNT available** (8 of 24 left a missing-signal comment); **theme content is not calculated by any script** — thematic coding of what respondents actually wrote is a manual qualitative step for the researcher, deliberately kept out of the automated pipeline (`alcsm.analysis.survey` structurally carries only a boolean presence flag, never the comment text). |
| Standard deviation of ratings | **Not currently reported** — the existing `content_validity_summary` reports mean/median/n, not SD. This is addable (a one-line change to `_ratings_summary_table` in `rq3_validation.py`) but was not added in this session since it was not explicitly requested by name in the deliverable list, and adding statistics beyond what's asked risks scope creep this close to a deadline. Flagged here rather than silently added or silently omitted — tell me if you want SD added and I will add it in under a minute. |

**This does not block RQ1, RQ2, or reliability work** — none of that work depends on the survey in any way; all three are already complete and reported independently (`09_Statistical_Analysis/RQ1/`, `09_Statistical_Analysis/RQ2/`, `07_Reliability/Reliability_Report_v1.1.md`).

---

*Source file unmodified beyond the version promotion described above (a file replacement at the canonical path, per established policy, not an in-place edit) — no cell was hand-edited.*
