---
name: academic-paper-orchestrator
description: "Coordinate an end-to-end academic paper, thesis, dissertation, review paper, or manuscript workflow by routing work across research verification, PDF/DOCX parsing, writing, academic figures, de-AI polishing, post-draft review, and formatting skills. Use when the user asks to manage a full paper project, plan a thesis from source materials to final DOCX, decide which academic skill should handle a task, run gated human-AI paper production, coordinate evidence gaps, field confirmation, reviewer-comment revision planning, or final polish handoffs. Chinese triggers: 论文全流程, 毕业论文, 学位论文, 综述论文, 论文总控, 编排论文工作流, 待补证据流程, 评审意见流程, 最终润色流程."
---

# Academic Paper Orchestrator

Use this skill to coordinate a complete academic paper workflow. Do not do every specialized task inside this skill; route to the focused skill that owns the current stage.

## Routing Map

| User need | Route to |
|---|---|
| Search literature, verify DOI/title match, check citation authenticity | `$academic-research-verification` |
| Parse PDFs or DOCX files into structured notes, evidence, headings, comments, or revision data | `$pdf-docx-parsing-workflow` |
| Plan sections, draft chapters, revise academic prose, integrate evidence into claims | `$paper-writing-workflow` |
| Confirm research field, handle terminology gates, mark writing evidence gaps, or plan ordinary reviewer/supervisor-comment revisions | `$paper-writing-workflow` |
| Resolve `LIT_GAP` items, find needed literature, verify new evidence, or update the evidence register | `$academic-research-verification` |
| Create mechanism figures, SVG diagrams, draw.io engineering diagrams, or approved OpenAI generated images | `$academic-figure-workflow` |
| Apply school handbook, Word template, journal guide, or general academic formatting | `$academic-formatting-workflow` |
| Review a complete initial draft against 3-10 benchmark papers and plan the next revision | `$post-manuscript-benchmark-review` |
| Polish stable manuscript prose, reduce AI-like cadence, or remove internal project/operation traces | `$academic-de-ai-polishing` |

If a focused skill is unavailable, follow the same ownership boundaries and tell the user which part was handled without the dedicated skill.

## Core Rules

1. Ask only the minimum startup questions needed to choose the next stage.
2. Maintain visible project state, current gate, confirmed artifacts, missing materials, risks, and next step.
3. Treat verified evidence as the source of truth for scholarly claims.
4. Treat real codebase, dataset, or experiment artifacts as the source of truth for implementation or result claims.
5. Keep research, parsing, writing, figures, formatting, and post-draft review as separate passes.
6. Stop for user confirmation at required gates before moving to the next major stage.
7. Never fabricate citations, DOI records, experiment results, repository behavior, figure contents, or formatting rules.

## Intake

Collect only what is missing:

- paper type, language target, and delivery target;
- research field and target venue/school field when terminology may matter;
- target standard: school handbook, Word template, journal guide, supervisor requirement, or provisional baseline;
- target examples: 3-10 accepted papers, approved theses, templates, author guidelines, or supervisor-approved chapters when available;
- current materials: topic, outline, draft, PDFs, DOCX files, data, codebase, figures, bibliography, and notes;
- constraints: deadline, citation style, word/page count, required chapters, and permitted tools.

Before routing work into execution, ask for materials that would materially improve quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

## Workflow

1. Rebuild or create the project state.
2. Decide the current mode and route using the routing map.
3. Apply [workflow-protocol-index.md](../../shared/workflow-protocol-index.md) and [trigger-conflict-matrix.md](../../shared/trigger-conflict-matrix.md) when a request spans stages or the owner skill is ambiguous.
4. Apply [orchestration-contract.md](references/orchestration-contract.md) for substantial projects, state files, material passports, and handoff packets.
5. Apply [project-gates-and-phases.md](references/project-gates-and-phases.md) for full-project phase sequencing and required gates.
6. Apply [integrity-gate-patterns.md](references/integrity-gate-patterns.md) before drafting, benchmark review, final polish, formatting, or any claim about code/data/results.
7. Apply [writing-chain-gates.md](references/writing-chain-gates.md) when the project is entering field confirmation, evidence-gap handling, reviewer-comment response, post-draft review, or final polish.
8. Route execution to the focused skill that owns the current stage.
9. At each gate, report completed work, artifacts, decisions, risks, missing materials, and recommended next step.

For narrow requests, run only the relevant stage and state what was intentionally skipped.

## Evidence And Version Discipline

- Keep a single evidence register or literature master list for the project.
- Mark items as `candidate`, `verified`, `downloaded`, `parsed`, `cited`, `rejected`, or `unresolved`.
- Track major project inputs with material passports when multiple stages depend on them.
- Keep paired Markdown and DOCX outputs at the same semantic version when both exist.
- Save new outputs with explicit suffixes; do not overwrite the only working draft unless the user explicitly requests it.
- Validate `project_state.json` before moving from research/parsing into drafting, and before moving from writing into formatting.

## Fallbacks

- If literature verification requires network access and network is unavailable, create a manual verification queue with exact DOI/title/search strings.
- If PDF parsing fails, list failed pages and recommended manual recovery.
- If a DOCX needs Word-only features, explain what can be automated and what requires Word.
- If a requested figure cannot be drawn faithfully from evidence or code, decline the specific figure or mark it unresolved.
- If the user wants to skip a gate, comply only after stating the risk.

## Reference

Read [stage-map.md](references/stage-map.md) when a full project needs a compact stage checklist or when resuming a long-running thesis workflow.

Read [workflow-protocol-index.md](../../shared/workflow-protocol-index.md) before selecting shared protocol references for cross-skill coordination.

Read [trigger-conflict-matrix.md](../../shared/trigger-conflict-matrix.md) when a request could trigger multiple academic skills or when deciding whether the orchestrator should own the task.

Read [handoff-field-schema.md](../../shared/handoff-field-schema.md) when checking field names for workflow modes, material passports, claim anchors, literature gaps, writing-ready handoffs, or benchmark reports.

Read [project-artifact-templates.md](references/project-artifact-templates.md) when creating a project state file, handoff packet, or target-baseline note.

Read [orchestration-contract.md](references/orchestration-contract.md) for project-state output, route plan, handoff packets, and state-file use.

Read [project-gates-and-phases.md](references/project-gates-and-phases.md) for standard phases, required gates, and stage execution notes.

Read [integrity-gate-patterns.md](references/integrity-gate-patterns.md) before accepting claims about sources, code, data, experiments, benchmarks, figures, or final deliverables.

Read [writing-chain-gates.md](references/writing-chain-gates.md) for field confirmation, `LIT_GAP` handling, reviewer-comment revision planning, post-draft review routing, and final de-AI polishing gates.

## Bundled Utilities

- `scripts/project_state_check.py`: create a JSON project-state template or validate project state, required handoff packets, gate consistency, evidence readiness, and formatting readiness.
