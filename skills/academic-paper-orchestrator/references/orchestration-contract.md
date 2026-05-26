# Orchestration Contract

Use this reference when coordinating a substantial paper, thesis, dissertation, review paper, or journal manuscript project.

## Output Contract

For every substantial orchestration response, output these blocks in the user's language:

```text
Project state:
Route plan:
Handoff packets:
Current gate:
Risks:
Next step:
```

Use compact tables when the project has multiple materials or skills.

## Project State

Track:

- `paper_type`
- `language`
- `target_standard`
- `materials`
- `evidence_status`
- `draft_status`
- `figure_status`
- `format_status`
- `current_gate`

The route plan must map each stage to one focused skill or to the orchestrator itself.

## Handoff Packets

| Handoff | Required packet |
|---|---|
| Parsing -> research | extracted DOI strings, bibliography entries, source metadata, low-confidence flags |
| Research -> writing | verified evidence register, unresolved items, rejected or downgraded sources |
| Parsing -> writing | evidence CSV, headings, comments, tracked-change summaries, extracted notes |
| Writing -> figures | figure purpose, target section, factual content, caption intent |
| Writing -> formatting | stable manuscript version, target guide, figure/table list, bibliography status |
| Writing -> post-draft review | complete draft, target standard, benchmark set, evidence register, figures/tables, unresolved claims |
| Figures -> formatting | source figure files, exports, captions, placement notes, unresolved assumptions |
| Post-draft review -> writing | P0/P1/P2 revision plan, claim triage, benchmark gap table, missing evidence list |

## State File

For long-running projects, create or validate a machine-readable state file:

```bash
python scripts/project_state_check.py --init --output project_state.json
python scripts/project_state_check.py --state project_state.json --output project_state_validation.md
```

Use the state file as a durable handoff record. Do not let it override visible evidence. If JSON state conflicts with actual files or user instructions, show the conflict and ask for a decision.

Read [project-artifact-templates.md](project-artifact-templates.md) for project-state, handoff packet, and target-baseline templates.
