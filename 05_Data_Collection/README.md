# 16_Data

## Purpose
Processed/working datasets used across annotation, NLP, and statistical analysis stages — distinct from `06_Data_Collection`'s untouched raw originals.

## What Belongs Here
- Cleaned datasets
- Train/test splits
- Feature-engineered datasets
- Data dictionaries describing processed files

## Naming Conventions
- `ALCSM_Data_<Stage>_<Description>_v<Major>.<Minor>.<ext>` (Stage = Raw/Cleaned/Annotated/Final)
  - e.g., `ALCSM_Data_Cleaned_JobPostings_v1.3.csv`

## Versioning Rules
- Every transformation that changes data produces a new versioned file — never overwrite a prior processed dataset in place.
- Raw inputs from `06_Data_Collection` are never modified; this folder holds derived copies only.
- Superseded dataset versions move to `17_Archive/16_Data/`.
