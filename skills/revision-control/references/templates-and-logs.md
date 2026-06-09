# Templates And Logs

Use these template files when creating revision artifacts:

- [template-manuscript-objects.json](template-manuscript-objects.json)
- [template-full-bilingual-review.md](template-full-bilingual-review.md)
- [template-partial-failed-review.md](template-partial-failed-review.md)
- [template-user-confirmation-log.md](template-user-confirmation-log.md)
- [template-modification-log.md](template-modification-log.md)
- [template-material-dependencies.yaml](template-material-dependencies.yaml)
- [template-upgrade-plan.md](template-upgrade-plan.md)

## Logging Rules

- Every user confirmation is logged with timestamp, round id, scope, affected ids, original user wording, normalized decision, and unresolved items.
- Every modification is logged with source id, old text, new text, operation, reason, evidence/standard used, reviewer input used, and `revision_count`.
- Every upgrade plan is saved before structural rewriting, evidence补充, or large-scale rewrite begins.
- Round snapshots are immutable after round close.
