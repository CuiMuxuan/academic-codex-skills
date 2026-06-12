# Project Standards And Materials

## Project Standards

`revision-control` owns creation and updates for:

- `project_review_standards.md`
- `project_review_standards.yaml`
- `terminology_glossary.md`
- `terminology_glossary.yaml`
- `problem_words.md`
- `problem_words.yaml`

Before launching the annotation UI, these project-level shared resources must exist. If they are missing, create them under `revision_workbench/shared/` before opening the UI. Use `scripts/ensure_revision_ui_resources.py` when available.

`terminology_glossary.yaml/md` should be initialized from the current manuscript object library so each paper project has its own professional-term and proper-noun candidate list. For bilingual projects, each English entry should include likely `chinese_translations` from the aligned Chinese review text when possible; both the English term/variants and the Chinese translations are used by the annotation UI for shallow-green terminology highlighting. Generated entries are candidates only and must use `confirmed: false` until the user edits or confirms them in the UI. Do not reuse another paper project's glossary.

`project_review_standards.yaml/md` should be initialized as a project supplemental review-standard template. It should identify the research field when known and include a candidate reminder to preserve discipline-appropriate terminology while avoiding unnecessary artificial-intelligence, computer-science, or electronic-information jargon unless such terms genuinely belong to the current paper's field or the user confirms them. Generic professional terms broadly known across fields do not require special restriction.

Inputs may come from:

- user sentence-level opinions;
- `$language-style-review` reports;
- `$post-manuscript-benchmark-review` reports;
- stable language preferences found during `$academic-de-ai-polishing`;
- project-specific rules found during `$paper-writing-workflow` rewrites.

## Confirmation Rule

New or modified project supplemental standards require explicit user confirmation. Unconfirmed items stay in `candidate_rules` or `user_confirmation_log.md`.

Auto-generated terminology and project-standard entries are unconfirmed candidates. They may guide UI highlighting and user review, but they must not be treated as final revision rules until confirmed by the user.

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
