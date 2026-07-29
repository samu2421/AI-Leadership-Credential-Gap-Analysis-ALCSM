# 07_Annotation

## Purpose
Manual/expert annotation of collected data against ALCSM framework constructs.

## What Belongs Here
- Annotation codebooks and annotator guidelines
- Annotated datasets and annotation-tool exports
- Annotator disagreement logs and resolution notes

## Naming Conventions
- `ALCSM_Annotation_<Description>_v<Major>.<Minor>.<ext>`
  - e.g., `ALCSM_Annotation_Codebook_v1.3.docx`
  - e.g., `ALCSM_Annotation_Round2_Dataset_v1.0.csv`

## Versioning Rules
- Codebook changes require a full version bump and must be cross-referenced in `08_Reliability`, since a codebook change invalidates any reliability calculations performed against the prior version.
- Never overwrite a completed annotation round's output; each round is a permanent, immutable record.
