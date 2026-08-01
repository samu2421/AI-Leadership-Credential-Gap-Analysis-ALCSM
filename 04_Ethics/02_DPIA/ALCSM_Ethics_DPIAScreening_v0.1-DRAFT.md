# ALCSM DPIA Screening (Draft)

**Version:** 0.1-DRAFT
**Status:** Draft — analysis only. Final determination rests with the institutional Data Protection Officer, not with this document.
**Purpose:** determine, per GDPR Article 35 and the WP29/EDPB nine-criteria guidance, whether a full Data Protection Impact Assessment is required before the LinkedIn profile-audit strand of this study may proceed.
**Last Updated:** 2026-07-30
**Author:** Samiksha Dhere (researcher) — drafted with Claude Code assistance

---

## 1. Processing operation under review

Collection, pseudonymisation, storage, and structured scoring of ~500 LinkedIn profiles publicly presenting AI-leadership titles, plus comparison against ~200 job-posting requirements, producing per-dimension credential-signal scores for research and thesis purposes.

## 2. Screening against the recognised DPIA triggers

| # | Trigger (WP29/EDPB criteria) | Applies here? | Basis |
|---|---|---|---|
| 1 | Evaluation or scoring, including profiling | **Yes** | The core purpose of this study is a structured, six-dimension score assigned to each individual's presented credentials. |
| 2 | Automated decision-making with legal or similarly significant effect | No | Scores are descriptive research outputs, not used to make any decision about, or take any action affecting, the scored individuals. |
| 3 | Systematic monitoring | **Partially** | Profile content is captured at a point in time (not continuously monitored), but the *systematic* nature of scanning search results at scale is relevant context. |
| 4 | Sensitive data or data of a highly personal nature | No (by design) | Special-category data is explicitly excluded from collection (see the Ethics Application §4); no Article 9 data is sought or retained. |
| 5 | Data processed on a large scale | **Borderline** | ~500 individuals is modest by platform standards but is not trivial, and the underlying source (LinkedIn) is itself a large-scale platform; the *sample* is not large-scale, but the criterion is assessed cautiously here. |
| 6 | Matching or combining datasets | **Yes** | Profile-derived data is combined with independently collected job-posting data to compute a credential gap; RQ4 combines profile-derived observable indicators with the credential scores for correlation analysis (structurally kept separate to avoid circularity, but still a form of dataset combination for analysis purposes). |
| 7 | Data concerning vulnerable data subjects | No | Subjects are working professionals in senior/aspiring-senior roles, not a vulnerable population under the guidance's examples. |
| 8 | Innovative use or new technological solution | **Partially** | The NLP-automation strand (RQ5) is a novel application of local NLP models to this specific scoring task, though the underlying model families are established. |
| 9 | Data transfer outside the EU, or preventing data subjects from exercising a right | No (by design) | All storage/processing is confined to EEA-resident infrastructure; no international transfer is intended. |

**EDPB guidance:** a DPIA is generally considered necessary if a processing operation meets **two or more** of these criteria. This screening identifies criteria 1 and 6 as clearly met, with 3, 5, and 8 as reasonably arguable — **at least two, and plausibly more, criteria are met.**

## 3. Additional public-interest factor

Because the profiles are **publicly available data collected without direct contact with the data subject**, the Article 14 transparency question is engaged (see the LIA and the Privacy Notice), which the EDPB explicitly flags as a factor that should lower, not raise, the threshold for conducting a DPIA — transparency-limited processing of third-party data warrants closer scrutiny, not less.

## 4. Screening conclusion

**A full Data Protection Impact Assessment is warranted.** See `ALCSM_Ethics_DPIAFull_v0.1-DRAFT.md`.

This conclusion should be treated as provisional until confirmed in writing by the institutional Data Protection Officer. If the DPO's own assessment differs from this screening, the DPO's determination governs — record it here:

| Field | Value |
|---|---|
| DPO reviewed this screening | `[INSERT: yes/no, date]` |
| DPO conclusion | `[INSERT: DPIA required / not required, with reasoning if it differs from this screening]` |
| Reference | `[INSERT]` |

---

*Cross-reference: this screening operationalises the assessment already made in `05_Data_Collection/Documentation/Task5_PreCollection_Roadmap.md` §3.7 ("a DPIA is likely required, and you should assume it is until the DPO says otherwise"). No frozen ALCSM methodology or schema element is altered by this document.*
