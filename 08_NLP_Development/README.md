# 09_NLP_Development

## Purpose
NLP/ML model development for automated credential-gap extraction and classification, built on top of the frozen ALCSM framework (v1.0) and database (v1.0.1).

## What Belongs Here
- Model configurations and hyperparameter records
- Embeddings and intermediate artifacts
- Evaluation metrics and experiment logs
- Model cards / summaries per experiment
(Executable training/inference code lives in `15_Scripts`; this folder holds the artifacts and results those scripts produce.)

## Naming Conventions
- `ALCSM_NLP_<ModelName>_<Description>_v<Major>.<Minor>.<ext>`
  - e.g., `ALCSM_NLP_BERTClassifier_EvalResults_v1.2.json`

## Versioning Rules
- Each trained model checkpoint or experiment gets its own version and experiment ID.
- Never overwrite prior experiment results — reproducibility and result comparison depend on retaining every run's output.
