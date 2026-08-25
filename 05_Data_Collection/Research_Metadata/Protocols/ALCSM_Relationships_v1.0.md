# ALCSM Dataset Relationships

**Version:** 1.0
**Status:** Draft — governance-layer research documentation.
**Document type:** Research protocol (data governance layer, `16_Data/04_Metadata/Protocols/`)
**Last Updated:** 2026-08-02

---

## 1. Purpose

This document describes the logical relationships between the datasets produced by ALCSM data collection, at a conceptual level suitable for a researcher reviewing the dataset's structure without reference to any specific database implementation. It records which datasets relate to which, how they relate, and — most importantly — clarifies that the two source corpora are collected and stored independently of one another.

**Relationship to the implemented database schema.** This document describes the *logical* dataset structure for research-documentation purposes. The authoritative *physical* database structure is defined exclusively in `schema/alcsm_schema_v1.0.1.sql`, which is frozen and governs the actual implementation. Where this document and the physical schema differ in naming or grouping, the physical schema governs implementation; this document governs conceptual understanding of the data for reproducibility and research documentation purposes.

## 2. Overview of the Relational Data Model

The ALCSM dataset is organized around two independent master entities — one representing collected LinkedIn profiles, one representing collected job postings — each with associated child entities capturing specific categories of information linked back to that master record.

## 3. Independence of the Two Corpora

The LinkedIn profile dataset and the job posting dataset are collected, stored, and maintained as **entirely independent datasets** throughout the collection process. No record in one dataset references or is linked to any record in the other at the point of collection or storage.

The two datasets are brought together **only later, and only analytically** — during statistical analysis and ALCSM evaluation, where credentials held (from the profile dataset) are compared against credentials required (from the job posting dataset) at the level of aggregate patterns per dimension, not at the level of any individual record-to-record linkage.

## 4. Dataset Overview

| Dataset | Description | Corpus |
|---|---|---|
| `LinkedIn_Profile_Master` | One record per collected LinkedIn profile, holding profile-level provenance and identifying metadata (pseudonymous). | LinkedIn |
| `Education` | Education entries associated with a profile. | LinkedIn |
| `Certifications` | Certification entries associated with a profile. | LinkedIn |
| `Professional_Experience` | Professional experience entries associated with a profile. | LinkedIn |
| `Technical_Contributions` | Technical contribution entries (e.g. publications, open-source work) associated with a profile. | LinkedIn |
| `Job_Posting_Master` | One record per collected job posting, holding posting-level provenance and metadata. | Job Posting |
| `Job_Requirements` | Requirement entries associated with a job posting. | Job Posting |

## 5. Relationship Table

| Parent | Child | Primary Key | Relationship Type |
|---|---|---|---|
| `LinkedIn_Profile_Master` | `Education` | Profile_ID | One-to-Many |
| `LinkedIn_Profile_Master` | `Certifications` | Profile_ID | One-to-Many |
| `LinkedIn_Profile_Master` | `Professional_Experience` | Profile_ID | One-to-Many |
| `LinkedIn_Profile_Master` | `Technical_Contributions` | Profile_ID | One-to-Many |
| `Job_Posting_Master` | `Job_Requirements` | Posting_ID | One-to-Many |

No relationship exists between `LinkedIn_Profile_Master` and `Job_Posting_Master`, or between any LinkedIn-corpus entity and any job-posting-corpus entity. This absence is deliberate and is the subject of §6.

## 6. Methodology Note: Why Independent Datasets Improve Reproducibility and Reduce Analytical Bias

Keeping the two corpora independent during collection, rather than linking them at the point of capture, serves the study's reproducibility and validity in several concrete ways:

- **No circularity between required and held credentials.** If a profile record were linked to a specific posting at collection time, a collector's judgement about what a posting requires could unconsciously shape what is transcribed from a profile (or vice versa). Collecting each corpus without reference to the other removes this channel of contamination.
- **Independent error surfaces.** A transcription or coding error in one corpus cannot propagate into the other through a shared record, since no shared record exists. Each corpus can be quality-checked and corrected on its own terms.
- **Reproducibility of each corpus in isolation.** A future researcher can reproduce, audit, or extend either corpus independently, without needing to reconstruct or preserve a cross-corpus linkage scheme.
- **Analytical comparison remains a deliberate, documented step.** Because the two corpora are never linked at the record level, any comparison between required and held credentials is necessarily a later, explicit, aggregate-level analytical procedure — visible and auditable in the analysis methodology, rather than an implicit consequence of how the data happened to be stored.

## 7. Version History

| Version | Date | Summary of Change | Author |
|---|---|---|---|
| 1.0 | 2026-08-02 | Initial documentation of the logical dataset relationships and the rationale for corpus independence. | Samiksha Dhere |

---

*This document describes the logical relationships between datasets for research documentation purposes. It does not define or alter the frozen physical database schema (`schema/alcsm_schema_v1.0.1.sql`) or any ALCSM scoring methodology.*
