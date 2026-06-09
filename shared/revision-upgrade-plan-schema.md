# Revision Upgrade Plan Schema

Create an upgrade plan when sentence-level revision must pause for evidence, structure, material, or large-scale rewriting work.

```yaml
upgrade_plan_id:
created_at:
round:
trigger_reason:
affected_scope:
affected_object_ids: []
required_skills:
  - skill:
    task:
    input:
    expected_output:
missing_materials_or_evidence:
  - item:
    why_needed:
    owner:
    status:
rewrite_level:
state_reset:
  object_library_rebuild: false
  latest_review_regeneration: false
  renumbering_required: false
  preserve_id_mapping: true
user_decisions_required:
  - decision:
    options: []
    recommendation:
pre_upgrade_version:
supporting_material_paths: []
possibly_modified_materials:
  - path:
    before_state:
    planned_change:
    after_state:
```

## Required Gate

Do not begin the upgrade work until the user approves the plan or explicitly narrows the task back to sentence-level revision.
