# Project Standards And Materials

## Project Standards

`revision-control` owns creation and updates for:

- `project_review_standards.md`
- `project_review_standards.yaml`
- `terminology_glossary.md`
- `terminology_glossary.yaml`
- `problem_words.md`
- `problem_words.yaml`

Inputs may come from:

- user sentence-level opinions;
- `$language-style-review` reports;
- `$post-manuscript-benchmark-review` reports;
- stable language preferences found during `$academic-de-ai-polishing`;
- project-specific rules found during `$paper-writing-workflow` rewrites.

## Confirmation Rule

New or modified project supplemental standards require explicit user confirmation. Unconfirmed items stay in `candidate_rules` or `user_confirmation_log.md`.

## Material Dependency Rule

Supporting materials are not manuscript objects. Register them by path, purpose, access state, change state, and affected manuscript objects.

Examples:

- source PDF used for evidence;
- supervisor comment DOCX;
- data table;
- code repository output;
- figure source file;
- benchmark paper;
- literature verification register.

Use [template-material-dependencies.yaml](template-material-dependencies.yaml) for YAML records.
