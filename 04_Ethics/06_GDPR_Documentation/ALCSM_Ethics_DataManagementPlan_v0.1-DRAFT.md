# ALCSM Data Management Plan (Draft)

**Version:** 0.1-DRAFT
**Status:** Draft — living document during collection planning; not yet finalised or approved.
**Purpose:** describe how research data (profiles, postings, survey responses, derived annotation/analysis data) will be stored, protected, retained, and destroyed throughout and after this project.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance
**Template basis:** standard funder/university DMP structure (Horizon Europe / Science Europe style), adapted to this project. `[INSERT: replace with SRH's own DMP template if one exists]`.

---

## 1. Data description

Two independently collected corpora plus derived research data:

- **~500 pseudonymised LinkedIn profiles** — section text (headline, about, experience, education, certifications, contributions, activity), provenance fields, and RQ4 observable-impact indicators.
- **~200 job postings** — full verbatim posting text plus provenance.
- **Expert survey responses** — a small number of pseudonymous responses to the validation survey (separate legal basis, separate population — see the LIA and the consent materials).
- **Derived data:** human annotation scores and evidence, reliability statistics, NLP predictions, and analysis outputs — all generated from the above, governed by the frozen `alcsm_schema_v1.0.1.sql`.

**Formats:** PostgreSQL relational data (primary); text exports (CSV) for analysis where needed. No proprietary or hard-to-open formats are used.

## 2. Volume

Small by any standard — low gigabytes at most, dominated by profile/posting text rather than any binary media (no photos, no video, no audio are ever collected).

## 3. Personal data

Yes — the LinkedIn profile corpus and the survey responses both contain personal data (pseudonymised). The job-posting corpus is organisation-authored and is not treated as personal data, except that individual recruiter names, if they appear in a posting, are never recorded (see the collection protocols).

**Pseudonymisation:** applied at the moment of capture for profiles (`PRF-#####`) and for survey respondents. No direct identifier (name, URL, photo, email, phone) is ever stored in the research database — this is enforced by the collection tooling, not left to procedural discipline alone.

## 4. Storage

- **Location:** university-approved, access-controlled, **EEA-resident** storage. Host: `[INSERT: specific approved host/environment]`.
- **Hard rule:** no profile or survey-response data is ever stored on a personal laptop, in consumer cloud storage (e.g. a personal Dropbox/Google Drive), or in the project's Git repository. The repository (`AI_Leadership_Credential_Gap_Analysis`) holds only code, schema, and non-personal documentation — `data/` is git-ignored and never populated with real records.
- **Local development** (schema/software testing, already completed for Phases P0–P1) uses only constructed, non-personal fixture data on the researcher's own development machine — never real profile or survey content.

### 4.1 The re-identification mapping decision

The frozen schema deliberately contains **no** built-in pseudonym-to-real-person mapping table. Three options exist, in ascending order of risk:

1. **No mapping at all** — once pseudonymised, the link to the real individual is not retained anywhere. Lowest risk; makes honouring a specific rectification/erasure request difficult if a subject does come forward, which is disclosed as an honest limitation rather than concealed.
2. **Temporary mapping** — retained only during active collection/quality-review, then destroyed on a documented date before analysis begins.
3. **Retained mapping** — kept outside the research database, under separate and stricter access control, justified by a specific, named need.

**Recommended default: option 1 (no mapping), or option 2 if a short-lived, documented temporary mapping proves operationally necessary for deduplication during collection.** Option 3 is not recommended without a specific justification reviewed by the DPO, since it would constitute the single most sensitive artefact in the entire project.

| Field | Value |
|---|---|
| Option selected | `[INSERT: 1 / 2 / 3, decided with DPO]` |
| If option 2: destruction date/trigger | `[INSERT]` |
| If option 3: justification and access control | `[INSERT]` |

## 5. Access control

Access limited to the researcher (Samiksha Dhere) and the supervisor (`[INSERT: name]`). Any additional coder (for double-coding, Phase P4) is granted access only under the same confidentiality expectations, and only to the extent needed to perform annotation — not to any re-identification mapping, should one exist.

## 6. Backup

Regular encrypted backups to the approved storage environment, using `scripts/backup_alcsm.sh` (a `pg_dump`-based, integrity-verified backup already implemented and tested — see `P1_Completion_Summary.md`). Restore has been verified in a throwaway-environment round-trip during software development (Phase P1); a **real-data restore rehearsal** on the production environment should be performed once real collection begins, before it is needed in earnest.

## 7. Security

Encryption at rest and in transit; pseudonymous keys throughout; principle of least privilege for access; no personal data ever logged (enforced by the application's logging design — see `PROJECT_CONTEXT.md` §31).

## 8. Retention

Data is retained only as long as needed for the thesis and its examination, plus any required post-examination retention period under institutional policy. **[INSERT: concrete retention period/trigger, confirmed with the institution — e.g. "N years after final degree conferral," or a specific calendar date]**.

## 9. Destruction

On reaching the retention trigger: secure deletion of the production database's personal-data tables (`profile`, `profile_raw_section`, `survey_respondent`, `survey_response_item`, and any re-identification mapping if one exists), all backups containing that data, and any local exports. A destruction log entry is made in `07_Institutional_Correspondence/` or an equivalent record, confirming what was destroyed and when. **[INSERT: name of person responsible for executing destruction]**.

## 10. Sharing and openness

- **Shareable without restriction:** the ALCSM framework, the database schema, the taxonomies, the rulebook, and the application source code — none of these contain personal data.
- **Not shared:** raw profile-level or survey-response-level personal data, in any form, at any time, to any third party — including other researchers, unless a new, separately reviewed data-sharing agreement and legal basis is put in place.
- **Aggregate results** (the credential-gap statistics, reliability results, NLP evaluation results) may be published as part of the thesis and any subsequent academic work.

## 11. Roles and responsibilities

| Role | Name |
|---|---|
| Controller | `[INSERT: typically the university, to be confirmed]` |
| Researcher | Samiksha Dhere |
| Supervisor | `[INSERT]` |
| Data Protection Officer | `[INSERT]` |

---

*This DMP formalises the structure and content already reasoned through in `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §4, including its §4.1 re-identification discussion. No frozen ALCSM methodology or database schema element is altered by this document.*
