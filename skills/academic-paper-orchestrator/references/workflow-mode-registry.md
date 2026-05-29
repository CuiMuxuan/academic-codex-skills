# Workflow Mode Registry

Use this reference at project startup, resume, or any time the user asks which stage the academic workflow is in.

This file is a skill-local execution guide. The canonical shared field names live in [handoff-field-schema.md](../../../shared/handoff-field-schema.md), and the cross-skill protocol index lives in [workflow-protocol-index.md](../../../shared/workflow-protocol-index.md).

## Mode Record

Each active stage should be expressible as:

```text
mode_id:
mode_owner:
task_type: open_ended | outcome_gradable
input_materials:
expected_output:
quality_gate:
user_confirmation_required: yes/no
next_allowed_modes:
```

`task_type` is a workflow label, not skill frontmatter. Use `outcome_gradable` when there is a known correct artifact, such as DOI matching, citation consistency, formatting checks, or script output validation. Use `open_ended` for drafting, synthesis, figure concept design, and review judgment.

## Standard Modes

| mode_id | owner | use when | expected output | confirmation gate |
|---|---|---|---|---|
| `intake_inventory` | orchestrator | project starts or resumes | material list, missing inputs, provisional route | yes, if materials or field are unclear |
| `target_baseline` | orchestrator + formatting | venue, school, journal, or examples define the target | target-baseline note | yes |
| `research_verify` | research verification | literature, DOI, citation, or `LIT_GAP` needs trust decisions | verified register or unresolved queue | yes, before writing use |
| `parse_materials` | PDF/DOCX parsing | PDFs, DOCX drafts, comments, or templates need extraction | structured notes, comments, evidence inventory | no unless extraction quality is low |
| `field_terms` | writing | field or terminology boundary affects prose | field and terminology baseline | yes when inferred |
| `design_outline` | writing | paper structure or chapter plan is being made | design document and outline | yes |
| `draft_section` | writing | one section or chapter is drafted from verified evidence | section draft packet | yes after each major section |
| `gap_resolution` | research verification | writing produced `LIT_GAP` items | gap resolution report and writing-ready handoff | yes before backfill |
| `figure_plan_build` | figure workflow | substantial academic figures are planned or created | figure plan, source files, exports, captions | yes for major figures or AI image generation |
| `integrated_draft` | writing | sections are merged into a full manuscript | integrated draft and unresolved claim list | yes |
| `benchmark_review` | post-manuscript review | complete draft is judged against target papers | benchmark review report and next-version plan | yes on benchmark set before judging |
| `final_polish` | de-AI polishing | content, evidence, and structure are stable | polished manuscript and edit contract | yes before entry |
| `format_delivery` | formatting | final DOCX/layout/submission package is needed | formatted files and validation report | yes on formatting baseline |

## Transition Rules

- State the current mode before substantial work.
- Move forward only through a handoff packet or user-confirmed shortcut.
- If the research field is unclear, ask the user. If the user still does not set it, default to computer science and electronic information and mark the assumption.
- Do not enter `draft_section`, `integrated_draft`, `benchmark_review`, `final_polish`, or `format_delivery` with unresolved source, data, code, or target-standard ambiguity unless the user explicitly accepts the risk.
- Keep mode changes visible in the project state and in the response's `Current gate` block.

## Compact Mode Report

```text
Current mode:
Why this mode:
Inputs used:
Output expected:
Gate before next mode:
User decision needed:
```
