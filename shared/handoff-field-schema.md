# Handoff Field Schema

Use these field names across academic skills. Skill-local references may add stage-specific fields, but should not rename these shared fields.

## Workflow Mode

```text
current_mode:
mode_id:
mode_owner:
task_type: open_ended | outcome_gradable
input_materials:
expected_output:
quality_gate:
user_confirmation_required: yes/no
next_allowed_modes:
```

## Material Passport

```text
material_id:
artifact_type: draft | pdf | bibliography | evidence_register | dataset | code | result_table | figure | template | comment_set | benchmark | other
path_or_source:
stage_owner:
data_access_level: raw | redacted | verified_only
task_type: open_ended | outcome_gradable
verification_state: unknown | candidate | verified | parsed | writing_ready | rejected | unresolved
allowed_uses:
restrictions:
source_trail:
related_lit_gap_ids:
related_claim_anchor_ids:
handoff_status: missing | candidate | ready | blocked | complete
user_decisions:
notes:
```

## Claim Evidence Anchor

```text
claim_anchor_id:
claim_summary:
manuscript_location:
support_type: literature | data | code | result | figure | user_decision
support_locator:
evidence_register_key:
allowed_claim_strength: strong | moderate | cautious | descriptive_only | unresolved
verification_state: verified | parsed | writing_ready | user_approved | unresolved
owner_skill:
open_risk:
```

## Literature Gap

```text
lit_gap_id:
claim_anchor_id:
target_claim:
field_and_target_venue:
evidence_type:
candidate_search_terms:
required_recency_or_source_type:
minimum_support_needed:
allowed_claim_strength_if_resolved:
intended_manuscript_use:
blocks_drafting: yes/no
```

## Writing-Ready Evidence Handoff

```text
claim_anchor_id:
lit_gap_id:
claim_supported:
recommended_citation_key:
source_identity:
evidence_location:
finding_to_use:
method_context:
limitation:
target_manuscript_location:
allowed_claim_strength:
verification_state:
```

## Benchmark Report

```text
benchmark_id:
full_identity:
selection_reason:
access_level: full_text | abstract_only | metadata_only | user_supplied_summary
facts_used:
inferences_made:
comparison_limit:
claim_anchor_id:
claim_summary:
benchmark_pressure:
gap_severity: blocking | major | moderate | minor
next_version_action:
```

## Reviewer Comment Action

```text
action_id:
source_comment_id:
acceptance_state: accept | partly_accept | reject_with_reason | defer | needs_material
target_location:
modification_type:
specific_change:
required_material:
expected_effect:
verification_method:
owner_skill:
priority: P0 | P1 | P2
```
