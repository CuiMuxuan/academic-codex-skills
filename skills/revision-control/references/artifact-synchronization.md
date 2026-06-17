# Revision Artifact Synchronization

Use this reference whenever `manuscript_objects.json`, the canonical active manuscript, a latest bilingual review draft, pass/fail decisions, annotations, or shared UI resources may have changed.

The goal is to make revision state boring: after any object-library or official manuscript change, run one synchronization entry point and then check that all derived artifacts still agree with the object library.

## State Owner

`revision-control` is the only owner of synchronization for:

- `bilingual_revision/manuscript_objects.json`
- `bilingual_revision/manuscript_objects.md`
- `bilingual_revision/original_full_bilingual_review.md`
- `bilingual_revision/latest_full_bilingual_review.md`
- `bilingual_revision/partial_failed_sentence_review.md`
- `bilingual_revision/manifest.yaml`
- `bilingual_revision/id_mapping_history.yaml`
- `bilingual_revision/rounds/<round_id>/*`
- `shared/project_review_standards.*`
- `shared/terminology_glossary.*`
- `shared/problem_words.*`
- `shared/material_dependencies.*`

The annotation UI remains a collector. It writes `rounds/<round_id>/user_annotations.json` and `shared/terminology_glossary.*` only through the terminology-management page. It must not synchronize official manuscript state.

## Public Sync Entry Point

Use the bundled utility:

```bash
python skills/revision-control/scripts/sync_revision_artifacts.py --workbench <revision_workbench> --round <round_id>
```

Use `--check-only` to verify without writing.

Use `--overwrite-shared` only when the user intentionally wants to regenerate existing shared resources. Otherwise existing project standards and glossary edits must be preserved.

## Synchronization Order

1. Load `manuscript_objects.json` as the source of truth.
2. Normalize annotation status decisions from `user_annotations.json`; invalid, missing, or legacy values become `fail`.
3. Ensure shared UI resources exist with `ensure_revision_ui_resources.py`.
4. Upgrade existing terminology records to the current schema without deleting user edits.
5. Regenerate `manuscript_objects.md` from the object library summary.
6. Regenerate the complete latest bilingual review draft from all sentence objects.
7. Regenerate the partial failed/targeted review draft from explicit `fail` decisions, annotation targets, and existing requested/failed records.
8. Update `manifest.yaml` metadata if needed.
9. Validate counts and references:
   - all review-draft sentence ids exist in the object library;
   - latest full review sentence count equals object-library sentence count;
   - partial failed review contains only known sentence ids or explicitly marked chapter/section items;
   - annotation target ids either exist or are marked for relocation;
   - terminology entries include field/domain and source provenance.
   - bilingual paper/chapter/section title fields are present or reported as missing in the sync report.
10. Write a machine-readable sync report.

## Required Recheck

After synchronization, run the check mode or inspect the generated report before continuing official revision:

```bash
python skills/revision-control/scripts/sync_revision_artifacts.py --workbench <revision_workbench> --round <round_id> --check-only
```

Do not proceed to official sentence modification if the report shows:

- missing object library;
- full-review sentence count mismatch;
- unknown annotation target ids;
- malformed terminology records;
- formula or equation records marked `needs_manual_equation_check` when the requested task depends on them.

## Sync Report

The sync utility writes:

```text
revision_workbench/bilingual_revision/rounds/<round_id>/artifact_sync_report.json
```

The report should include:

```yaml
generated_at:
workbench:
round:
mode: write|check_only
object_counts:
annotation_counts:
  annotations:
  resolved_annotations:
  sentence_status_decisions:
written_files: []
issues: []
warnings: []
terminology_schema:
  total:
  missing_field:
  missing_source_provenance:
title_translation:
  total:
  confirmed_or_present:
  inferred:
  missing:
  missing_ids: []
review_drafts:
  full_sentence_count:
  partial_sentence_count:
  unknown_sentence_ids: []
```

## Boundary Rules

- Do not rebuild paragraph boundaries from a sentence-aligned review draft. Use `rebuild_manuscript_objects_from_main.py` first when paragraph objects do not come from the active main manuscript.
- Do not overwrite user-confirmed project standards during sync.
- Do not treat generated terminology candidates as confirmed standards.
- Do not silently delete annotations whose target text changed; mark them `needs_relocation` or list them in the sync report.
- Do not mutate official manuscript text from the UI.

## When To Extract Another Reference

If a synchronization rule is used by writing, parsing, formatting, or figures outside revision-control, move the field names and integrity checks to a shared reference. Keep this file focused on revision workbench artifacts and state ownership.
