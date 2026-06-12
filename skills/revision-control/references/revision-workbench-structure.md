# Revision Workbench Structure

Use `revision_workbench` at the project root unless the user specifies another name.

```text
revision_workbench/
  shared/
    project_review_standards.md
    project_review_standards.yaml
    terminology_glossary.md
    terminology_glossary.yaml
    problem_words.md
    problem_words.yaml
    material_dependencies.md
    material_dependencies.yaml
  bilingual_revision/
    manifest.yaml
    manuscript_objects.json
    manuscript_objects.md
    original_full_bilingual_review.md
    latest_full_bilingual_review.md
    partial_failed_sentence_review.md
    figure_table_text_objects.json
    figure_table_text_objects.md
    id_mapping_history.yaml
    rounds/
      round_001/
        benchmark_gap_report.md
        quality_review_report.md
        language_style_review_report.md
        sentence_check_results.md
        partial_failed_sentence_review.md
        modification_log.md
        user_confirmation_log.md
        latest_full_bilingual_review_snapshot.md
        manuscript_objects_snapshot.json
        original_full_bilingual_review_snapshot.md
        upgrade_plan.md
```

## Artifact Roles

| artifact | role |
|---|---|
| `project_review_standards.*` | user-confirmed supplemental review standards |
| `terminology_glossary.*` | professional terms, proper nouns, accepted variants, and Chinese translations used for terminology highlighting |
| `problem_words.*` | project-specific banned, risky, or user-disliked expressions |
| `material_dependencies.*` | support material paths, purpose, state, and change records |
| `manifest.yaml` | revision project metadata and current round pointer |
| `manuscript_objects.*` | complete object library for the whole manuscript |
| `original_full_bilingual_review.md` | complete original sentence review draft |
| `latest_full_bilingual_review.md` | complete latest sentence review draft |
| `partial_failed_sentence_review.md` | only failed or requested target sentences |
| `id_mapping_history.yaml` | old/new ids across rounds and split/merge operations |
| `rounds/round_NNN/*` | immutable round-level reports, snapshots, logs, and plans |

## Creation Rule

If the user provides only a local paragraph or section and no workbench exists, mark context as `context_insufficient_for_formal_revision`. Offer to create a workbench and complete object library before official sentence edits.

Do not return official rewritten sentences in this state. At most, return a provisional issue list or non-final diagnostic examples, clearly separated from formal manuscript modifications.
