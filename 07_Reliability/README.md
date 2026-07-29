# 08_Reliability

## Purpose
Inter-rater / inter-annotator reliability analysis validating the quality of the annotation process.

## What Belongs Here
- Reliability calculations (e.g., Cohen's kappa, Krippendorff's alpha) per annotation round
- Reliability reports and interpretation notes
- Discrepancy resolution documentation tied to specific rounds

## Naming Conventions
- `ALCSM_Reliability_Round<N>_<Description>_v<Major>.<Minor>.<ext>`
  - e.g., `ALCSM_Reliability_Round2_KappaReport_v1.0.pdf`

## Versioning Rules
- Each reliability round is tied to a specific `07_Annotation` codebook version — record which codebook version was in effect.
- Never overwrite a completed round's results; it is a permanent record. New rounds get new round numbers, not overwritten files.
