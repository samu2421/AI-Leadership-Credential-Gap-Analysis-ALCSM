# 15_Scripts

## Purpose
All executable code supporting the thesis — data processing, the NLP pipeline, and statistical analysis — kept separate from the database implementation code in `04_Database_Design`.

## What Belongs Here
- Python/R scripts and Jupyter notebooks
- Environment/requirements files (`requirements.txt`, `environment.yml`)
- Shared utility functions/modules

## Naming Conventions
- Snake_case, since these are executable filenames: `alcsm_<module>_<description>_v<Major>.<Minor>.py`
  - e.g., `alcsm_nlp_train_classifier_v1.2.py`

## Versioning Rules
- Maintain a `CHANGELOG.md` in this folder documenting notable script revisions alongside in-file docstring headers noting version and date.
- Never silently overwrite a script used to produce results already reported elsewhere (e.g., in `09_NLP_Development` or `10_Statistical_Analysis`) — bump its version so past results remain reproducible.
- For fine-grained line-by-line history, consider placing this folder under its own lightweight version control (e.g., a local git repo) — recommended, not automatically configured.
