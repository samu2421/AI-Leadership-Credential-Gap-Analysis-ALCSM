# 04_Metadata

## Purpose

This folder is the governance layer for the ALCSM data collection process. It holds the research documentation that describes, independently of any implementation, **what** is collected, **how** it is collected, **how datasets relate to one another**, and **what quality standards govern the data** — sufficient for another researcher to understand and reproduce the collection process without reference to source code.

This is documentation, not software. The authoritative implementation of the collection tooling lives under `src/alcsm/collection/`; the authoritative database structure is defined in `schema/alcsm_schema_v1.0.1.sql`. This folder documents the research process those components implement — it does not redefine or supersede them.

## Contents

| Component | Location | Description |
|---|---|---|
| **Data Dictionary** | `Data_Dictionary/` *(to be added)* | Field-level definitions for every variable recorded across the LinkedIn profile and job posting datasets. **Placeholder — not yet populated.** |
| **Controlled Vocabularies** | `Controlled_Vocabularies/` *(to be added)* | Fixed value lists used during collection and coding (e.g. inclusion-reason codes, missing-data states). **Placeholder — not yet populated.** |
| **Collection Protocols** | `Protocols/` | Structured protocols governing LinkedIn profile collection and job posting collection, including sampling strategy, search strategy, and workflow. |
| **Dataset Relationships** | `Protocols/ALCSM_Relationships_v1.0.md` | The logical relationships between the datasets produced by collection, and the rationale for keeping the two corpora independent during collection. |
| **Data Quality Guidelines** | `Protocols/ALCSM_Data_Quality_Guidelines_v1.0.md` | Principles and rules governing data accuracy, consistency, duplicate handling, and audit trail requirements. |

## Versioning Approach

- Every substantive document in this folder carries an explicit version number (`v1.0`, `v1.1`, …) in its filename and in a **Revision History** section within the document itself.
- A version increment is required for any change to substantive content (criteria, workflow steps, quality rules). Formatting-only corrections do not require a version increment but are still noted in the revision history.
- Superseded versions are retained, not deleted, consistent with this repository's general archive policy (`Document_Version_Policy.md`).
- Where a decision has not yet been finalized, the document states this explicitly as a placeholder rather than presenting provisional content as final.

## Relationship to Other Governance Documentation

This folder complements, and does not duplicate, the following existing governance material:

- `05_Data_Collection/Documentation/` — operational collection workflow and pre-collection roadmap.
- `04_Ethics/` — ethics application, GDPR/DPIA documentation, and the LinkedIn Collection Protocol annex.
- `11_Implementation_Governance/` — software implementation governance, decision log, and phase roadmap.

Where content overlaps, this folder's documents are written at the level of a data-management/reproducibility record for the dataset itself, rather than an operational SOP or a software specification.
