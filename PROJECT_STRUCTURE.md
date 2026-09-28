# PROJECT_STRUCTURE.md
### AI Leadership Credential Gap Analysis (ALCSM) — Project Organization

This document explains the complete folder structure, the workflow it supports (Task 5 through final submission), and the naming/versioning conventions used throughout the project. See `VERSION.md` for current version status of frozen components.

---

## 1. Background

Tasks 1–4 produced two frozen deliverables:
- **ALCSM Framework v1.0** — the conceptual model (constructs, dimensions, taxonomy)
- **ALCSM Database Schema v1.0.1** — the implemented database

Both are locked and must not be edited in place. This structure organizes everything from **Task 5 onward** — ethics approval, data collection, annotation, reliability testing, NLP development, statistical analysis, and thesis writing — while keeping the frozen baseline safely preserved.

---

## 2. Folder Hierarchy

```
AI_Leadership_Credential_Gap_Analysis/
├── VERSION.md                      Root version-status record
├── PROJECT_STRUCTURE.md            This document
├── README.md, CLAUDE_CODE_RULES.md, CLAUDE_CODE_IMPLEMENTATION_GUIDE.md
│                                    Software-implementation governance (full copies live in
│                                    11_Implementation_Governance/)
├── pyproject.toml, src/alcsm/, tests/, .gitignore, requirements.txt
│                                    Software scaffolding (Phase P0) — the Python
│                                    implementation layer, additive to the thesis-task
│                                    folders below
│
├── 00_Project_Management/          Planning, timelines, meeting notes
├── 01_Literature_Review/           Sources, synthesis, review chapter drafts
├── 02_Framework_Development/       ALCSM framework — FROZEN v1.0
├── 03_Database_Design/             ALCSM database — FROZEN v1.0.1
│   ├── 01_Documentation/           Data dictionary, design rationale
│   ├── 02_Schema/                  DDL scripts, migrations
│   ├── 03_Validation/              QA/test/validation reports
│   └── 04_ER_Diagram/              Entity-relationship diagrams
├── 04_Ethics/                      IRB approvals, consent forms, DPIA, LIA, GDPR docs (draft — Phase P2)
│   ├── 01_Ethics_Approval/         Ethics application + LinkedIn collection protocol annex
│   ├── 02_DPIA/                    DPIA screening note + full Data Protection Impact Assessment
│   ├── 03_LIA/                     Legitimate Interests Assessment (Art 6(1)(f) basis)
│   ├── 04_Privacy_Notice/          Public Article 14 privacy notice
│   ├── 05_Consent_Materials/       Survey participant information sheet + consent form
│   ├── 06_GDPR_Documentation/      Data Management Plan + GDPR compliance checklist
│   ├── 07_Institutional_Correspondence/  Dated committee/DPO/supervisor correspondence log
│   ├── 08_Submission_Package/      Frozen, as-submitted snapshots (one per submission event)
│   └── 09_Review_Logs/             Governance consistency reviews of the 04_Ethics/ set
├── 05_Data_Collection/             Raw data acquisition (untouched originals)
├── 06_Annotation/                  Codebooks, annotated datasets
├── 07_Reliability/                 Inter-rater reliability analysis
├── 08_NLP_Development/             NLP/ML model artifacts and results
├── 09_Statistical_Analysis/        Statistical outputs and reports
├── 10_Thesis_Writing/              Manuscript chapters through final submission
├── 11_Implementation_Governance/   Claude Code governance package (PROJECT_CONTEXT.md,
│                                    Document_Version_Policy.md, roadmaps, consistency review)
├── 12_Figures/                     Thesis figures (source + exports)
├── 13_Tables/                      Thesis tables (source + exports)
├── 14_Appendix/                    Supplementary manuscript material
├── 15_Scripts/                     All executable code (data/NLP/stats)
├── 16_Data/                        Processed/working datasets
└── 16_Archive/                     Superseded versions of any artifact
    └── Superseded_Task1_Task4/     Superseded Task 1-4 files (see Document_Version_Policy.md)
```

Each folder listed above (the 18 top-level folders, `00` through `17`, plus the 4 `03_Database_Design` subfolders and the 9 `04_Ethics` subfolders) contains its own `README.md` describing that folder's purpose, contents, naming convention, and versioning rules in detail.

**Correction (P0 cleanup session, 2026-07-28):** this section previously numbered the folders `01`-`17` and did not list `11_Implementation_Governance` at all, which no longer matched the actual repository (numbered `00`-`17`, including `11_Implementation_Governance`). Numbering above is corrected to match disk; see `VERSION.md` for the corresponding log entry. This document describes navigation only — no thesis methodology content was touched.

**Update (P2 Session 4 governance cleanup, 2026-07-30):** `04_Ethics/` is expanded above into its 9 subfolders (created during P2 Sessions 1–2: `01_Ethics_Approval` through `09_Review_Logs`), which this diagram previously left as a single unexpanded line even after those subfolders existed. Navigation-only change; the ethics/GDPR documents themselves remain drafts pending supervisor/DPO/committee review — see `04_Ethics/09_Review_Logs/` and `11_Implementation_Governance/Reviews/P2_Governance_QA_Report.md`.

---

## 3. Workflow: Task 5 Through Submission

The numeric prefixes (00–17) reflect the natural order of thesis work, not a rigid sequence — several folders are used concurrently throughout the remaining tasks:

1. **Ethics (04)** — secure IRB approval before any human-subjects data work begins.
2. **Data Collection (05)** — gather raw source data per the approved protocol.
3. **Annotation (06)** — apply the ALCSM framework to label the collected data.
4. **Reliability (07)** — validate annotation quality before relying on the labels.
5. **NLP Development (08)** and **Statistical Analysis (09)** — build models and run analyses on the validated, annotated data (processed copies live in **Data, 16**; code lives in **Scripts, 15**).
6. **Thesis Writing (10)**, drawing on **Figures (12)**, **Tables (13)**, and **Appendix (14)**, is drafted and revised throughout, culminating in the final submitted manuscript.
7. **Project Management (00)** and **Literature Review (01)** run continuously alongside all of the above.
8. **Implementation Governance (11)** holds the Claude Code governance package guiding the software build (`src/alcsm/`), which proceeds alongside the thesis tasks per its own phase roadmap (P0–P9).
9. **Archive (17)** silently accumulates superseded versions from every folder as work progresses, under `16_Archive/Superseded_Task1_Task4/` for Tasks 1-4 artefacts specifically.

---

## 4. Naming Convention (Project-Wide)

All deliverables follow a consistent pattern:

```
ALCSM_<FolderTag>_<ShortDescription>_v<Major>.<Minor>[.<Patch>][-STATUS].<ext>
```

- `<FolderTag>` — short code identifying the folder/category (e.g., `PM`, `LitReview`, `Framework`, `DB`, `Ethics`, `DataCollection`, `Annotation`, `Reliability`, `NLP`, `Stats`, `Thesis`, `Fig`, `Tbl`, `Appendix`, `Data`).
- `<Major>.<Minor>` — standard two-part version (e.g., `v1.2`); the database uses three-part semantic versioning (`v1.0.1`) to match its schema versioning.
- `-STATUS` — optional suffix such as `-DRAFT` or `-FROZEN` where useful.
- Never use ambiguous labels like "final", "latest", "new", or "v2_really_final" — the version number is always the single source of truth.
- Executable scripts use snake_case instead (see `15_Scripts/README.md`), since they are also valid filenames/module names.

Each folder's own README.md specifies its exact `<FolderTag>` and any folder-specific naming detail.

---

## 5. Versioning Policy (Project-Wide)

1. **Never overwrite a finalized or reviewed file.** Save a new version instead.
2. **MAJOR** version bump — structural/conceptual changes, milestone freezes, or committee-approved changes.
3. **MINOR** version bump — edits, corrections, or incremental refinements within the same milestone.
4. **Frozen artifacts** (Framework v1.0, Database Schema v1.0.1) are locked: no in-place edits, ever. Changes require a new version number and a changelog entry in the relevant folder.
5. **Archiving** — when a file is superseded, move it (don't delete it) into `16_Archive/`, in a subfolder mirroring its original location (e.g., `16_Archive/10_Thesis_Writing/`), or into `16_Archive/Superseded_Task1_Task4/` for Tasks 1-4 artefacts (per `Document_Version_Policy.md`). Archived files keep their original name and version number.
6. **VERSION.md** at the project root is the authoritative log of version changes to major frozen components — append new rows there whenever Framework or Database versions change; never overwrite prior rows.

---

## 6. What This Structure Does Not Do

- It does not modify, move, or reorganize any existing thesis content, framework files, or database files — none existed in this directory prior to this setup, and this structure is purely additive scaffolding for Task 5 onward.
- It does not enforce version control (e.g., git) automatically — `15_Scripts/README.md` notes this as an optional recommendation for that folder specifically.
