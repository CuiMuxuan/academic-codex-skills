# Benchmark Report Schema

Use this reference when producing a post-draft benchmark review, readiness judgment, or next-version plan. The goal is to make benchmark comparison auditable and actionable.

Use the canonical benchmark-report field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md). This file adds post-draft review structure and reporting discipline.

## Report Header

```text
draft_version:
target_standard:
review_scope:
benchmark_count:
benchmark_access_limits:
readiness_judgment:
major_blockers:
next_revision_goal:
```

## Benchmark Material Record

| field | required | notes |
|---|---|---|
| `benchmark_id` | yes | B1, B2, B3 |
| `full_identity` | yes | authors, year, title, venue, DOI/link when available |
| `selection_reason` | yes | task, method, validation, target venue, or writing exemplar |
| `access_level` | yes | full_text, abstract_only, metadata_only, user_supplied_summary |
| `facts_used` | yes | only what was actually read or verified |
| `inferences_made` | no | reviewer-facing inference; keep separate from facts |
| `comparison_limit` | yes | what cannot be judged from the available material |

## Manuscript Claim Record

| field | required | notes |
|---|---|---|
| `claim_anchor_id` | recommended | use when the writing workflow provided anchors |
| `claim_summary` | yes | central claim, result claim, novelty claim, or method claim |
| `manuscript_location` | yes | section, paragraph, table, figure, or evidence-register key |
| `current_support` | yes | data, code, literature, figure, result, or none |
| `benchmark_pressure` | yes | which benchmark expectation affects this claim |
| `triage` | yes | promote, soften, move_to_supplement, hold_for_more_evidence, remove |
| `required_revision` | yes | concrete next action |

## Gap Table

| benchmark_id | gap_id | manuscript location | benchmark pressure | current manuscript state | required evidence or revision | severity | target impact |
|---|---|---|---|---|---|---|---|
| B1 | G1 | Results/Table 2 | stronger baseline set | current baseline lacks X | add baseline Y or soften claim | blocking | target not credible until resolved |

Severity must use `blocking`, `major`, `moderate`, or `minor`. Do not mark gaps about the main claim, baseline fairness, validation independence, data leakage, or evidence reproducibility as `minor`.

## Next-Version Action

| priority | action_id | objective | artifact to create or revise | required material | acceptance criterion | target location |
|---|---|---|---|---|---|---|
| P0 | A1 | close validation blocker | new experiment table | dataset split + script | result reproducible and claim narrowed | Methods/Results |

## Integrity Rules

- Separate benchmark facts from inference.
- Mark full text, abstract-only, metadata-only, and user-supplied summaries visibly.
- Tie each P0/P1 action to a manuscript location, claim anchor, benchmark pressure, or evidence gap.
- Do not give a final target-readiness judgment when the draft, benchmark set, or evidence base is too incomplete; use `cannot_judge_from_materials`.
- Route literature identity problems to `$academic-research-verification` and confirmed writing revisions to `$paper-writing-workflow`.
- Route final language polishing to `$academic-de-ai-polishing` only after claim triage, P0/P1 revisions, and evidence boundaries are stable.
