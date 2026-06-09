# Project Standards Handling

## Inputs

Use project-specific inputs only when they are provided, discoverable in the revision workbench, or passed by `$revision-control`:

- `project_review_standards.md`
- `project_review_standards.yaml`
- `terminology_glossary.md`
- `terminology_glossary.yaml`
- `problem_words.md`
- `problem_words.yaml`
- prior language-style review reports
- user-confirmed preference logs

## Rules

- User-confirmed project standards outrank general language preferences.
- Candidate standards are advisory only until the user explicitly confirms them.
- Never write standards files from this skill.
- If a user says "record this rule" or "remember this wording preference", output a candidate standard item and hand it to `$revision-control`.
- If a project standard conflicts with field terminology, report the conflict and ask for confirmation through `$revision-control`.

## Candidate Rule Format

```yaml
candidate_rule_id:
source:
trigger_text:
proposed_rule:
scope:
reason:
examples:
status: candidate_only
requires_user_confirmation: true
handoff_to: revision-control
```
