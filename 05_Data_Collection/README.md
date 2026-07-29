# 06_Data_Collection

## Purpose
Acquisition of the raw data that feeds the ALCSM analysis — e.g., job postings, credential/competency source documents, and any survey or scraping outputs — prior to cleaning or annotation.

## What Belongs Here
- Data collection protocols and source inventories
- Raw data exports (pre-cleaning, unmodified)
- Collection logs (what was collected, when, from where)

## Naming Conventions
- `ALCSM_DataCollection_<Source>_<Description>_v<Major>.<Minor>_<YYYYMMDD>.<ext>`
  - e.g., `ALCSM_DataCollection_JobPostings_Batch1_v1.0_20260410.csv`

## Versioning Rules
- Raw data snapshots are dated and **never overwritten**. Corrections or re-pulls create a new dated snapshot rather than replacing the original.
- Raw originals are preserved permanently as the source of truth; any cleaning/transformation happens downstream in `16_Data`, never here.
