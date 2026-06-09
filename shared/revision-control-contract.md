# Revision Control Contract

Use this shared contract when a skill hands manuscript problems to `$revision-control` or consumes its state.

## Ownership

`revision-control` owns:

- complete manuscript object library;
- round state and current round id;
- full original and full latest sentence review drafts;
- partial failed-sentence review drafts;
- sentence pass/fail confirmation state;
- sentence revision counts and id mapping history;
- project supplemental review standards;
- terminology and problem-word lists;
- material dependency records;
- modification and user-confirmation logs;
- upgrade plans.

Other skills may produce reports, suggestions, rewrites, evidence updates, or review findings, but they do not update revision state unless operating through `revision-control`.

## Handoff Packet

```yaml
handoff_id:
from_skill:
to_skill: revision-control
manuscript_path:
workbench_path:
scope:
object_ids: []
report_paths: []
task_queue:
  - target_id:
    task:
    reason:
    source_report:
    requires_user_confirmation: true
state_constraints:
  latest_draft_write_allowed: false
  pass_fail_update_allowed: false
  standards_update_allowed: false
material_dependencies: []
```

## Confirmation Gates

Stop for user confirmation before:

- creating a new workbench when it may become the project source of revision truth;
- finalizing sentence pass/fail states;
- modifying any sentence;
- applying candidate project standards;
- starting evidence补充, chapter rewrite, structure reorganization, or large-scale rewriting;
- overwriting a latest draft or replacing the only manuscript copy.

## State Discipline

- Complete original and latest sentence review drafts always represent the whole manuscript.
- Partial failed-sentence drafts represent only failed or explicitly requested target sentences.
- Support materials are registered as dependencies, not embedded as sentence objects.
- Round snapshots become immutable after round close.
