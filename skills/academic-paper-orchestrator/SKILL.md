---
name: academic-paper-orchestrator
description: "Coordinate an end-to-end academic paper, thesis, dissertation, review paper, or manuscript workflow by routing work across research verification, PDF/DOCX parsing, writing, academic figures, and formatting skills. Use when the user asks to manage a full paper project, plan a thesis from source materials to final DOCX, decide which academic skill should handle a task, or run gated human-AI paper production. Chinese triggers: 论文全流程, 毕业论文, 学位论文, 综述论文, 论文总控, 编排论文工作流."
---

# Academic Paper Orchestrator

Use this skill to coordinate a complete academic paper workflow. Do not do every specialized task inside this skill; route to the focused skill that owns the current stage.

## Routing Map

Use these skills when available:

| User need | Route to |
|---|---|
| Search literature, verify DOI/title match, check citation authenticity | `$academic-research-verification` |
| Parse PDFs or DOCX files into structured notes, evidence, headings, comments, or revision data | `$pdf-docx-parsing-workflow` |
| Plan sections, draft chapters, revise academic prose, integrate evidence into claims | `$paper-writing-workflow` |
| Create mechanism figures, SVG diagrams, draw.io engineering diagrams, or approved OpenAI generated images | `$academic-figure-workflow` |
| Apply school handbook, Word template, journal guide, or general academic formatting | `$academic-formatting-workflow` |
| Review a complete initial draft against 3-10 benchmark papers and plan the next revision | `$post-manuscript-benchmark-review` |

If a focused skill is unavailable, follow the same ownership boundaries in this file and tell the user which part was handled without the dedicated skill.

## Orchestration Output Contract

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

`Project state` must include:

- `paper_type`
- `language`
- `target_standard`
- `materials`
- `evidence_status`
- `draft_status`
- `figure_status`
- `format_status`
- `current_gate`

`Route plan` must map each stage to one focused skill or to the orchestrator itself.

`Handoff packets` must name the artifact that should move between skills:

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

For long-running projects, create or validate a machine-readable state file:

```bash
python scripts/project_state_check.py --init --output project_state.json
python scripts/project_state_check.py --state project_state.json --output project_state_validation.md
```

Use the state file as the durable handoff record. Do not let it override visible evidence; if the JSON state conflicts with actual files or user instructions, show the conflict and ask for a decision.

## Operating Rules

1. Ask only the minimum startup questions needed to choose the next stage.
2. Maintain a visible project state: goal, target outlet or school, available materials, missing materials, current stage, confirmed artifacts, and next gate.
3. Treat verified evidence as the source of truth for scholarly claims.
4. Treat the real codebase, dataset, or experiment artifacts as the source of truth for implementation or result claims.
5. Keep writing, parsing, figures, and formatting as separate passes.
6. Stop for user confirmation at required gates before moving to the next major stage.
7. Never fabricate citations, DOI records, experiment results, repository behavior, figure contents, or formatting rules.

## Startup Intake

Collect only what is missing:

- Paper type: review, experimental paper, undergraduate thesis, graduate thesis, dissertation, report, or journal manuscript.
- Language target: English, Chinese, or bilingual.
- Target standard: school handbook, Word template, journal guide, supervisor requirement, or provisional general standard.
- Target examples: ask for 3-10 accepted papers, approved theses, supervisor-approved chapters, Word/LaTeX templates, or author guidelines before setting the baseline. If none are available, proceed with a provisional general academic baseline and label assumptions.
- Current materials: topic, outline, draft, PDFs, DOCX files, data, codebase, figures, bibliography, and notes.
- Delivery target: outline, chapter draft, full manuscript, formatted DOCX, figures, verification report, or staged project plan.
- Constraints: deadline, citation style, word count, page count, required chapters, and tools the user permits.

If the user asks in Chinese, summarize the intake in Chinese. If the user asks in English, summarize in English.

## Pre-Execution Material Request

Before routing work into execution, ask the user for materials that would materially improve quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for target examples, source PDFs/DOCX files, verified or candidate bibliography, existing drafts, school/journal guides, Word/LaTeX templates, datasets, code repositories, figures, supervisor comments, and delivery constraints as relevant. If the user cannot provide them, ask whether to proceed with a provisional baseline and record the limitation in `Project state` and `Risks`.

## Standard Project Phases

1. Intake and project-state setup.
2. Target and formatting baseline confirmation.
3. Existing material inventory.
4. Research verification plan.
5. PDF/DOCX parsing plan.
6. Paper design document and chapter outline.
7. Round-1 verified literature and evidence register.
8. Optional trial section.
9. Chapter-by-chapter drafting.
10. Round-2 gap-driven literature supplementation.
11. Figure and table plan.
12. Integrated manuscript.
13. Citation and bibliography validation.
14. Formatting normalization.
15. Dedicated quality review.
16. Pre-final delivery and version note.

Skip phases only when the user's request is explicitly narrower, and state the skipped scope.

## Required Gates

Stop and wait for confirmation after:

- Project design document and chapter outline.
- Initial verified literature/evidence register.
- Each chapter draft.
- Integrated full draft.
- Benchmark-review plan and benchmark set before judging target readiness when the user asks for post-draft review.
- Figure plan when figures are substantial or use an external image-generation API.
- Formatting baseline before applying final DOCX normalization.
- Pre-final draft after quality review.

At every gate, report:

- Completed work.
- Artifacts produced.
- Decisions needing confirmation.
- Risks, missing materials, or unverified claims.
- Recommended next step.

## Stage Execution

### 1. Inventory

Create a short working inventory:

- `materials`: files, links, datasets, code repositories, notes.
- `trusted_evidence`: verified sources only.
- `unverified_items`: sources, claims, figures, or formatting rules needing confirmation.
- `outputs`: draft files, registers, diagrams, DOCX versions, reports.
- `decisions`: user confirmations and rejected options.

When resuming a project, rebuild the `Project state` block first and mark stale, unknown, or unverified items instead of assuming continuity.

### 2. Research

Use `$academic-research-verification` before writing claims that depend on external literature. Require DOI/title matching or another explicit source trail before treating a source as trusted.

### 3. Parsing

Use `$pdf-docx-parsing-workflow` when the project includes PDFs, DOCX drafts, review comments, tracked changes, or formatting templates. Ask it to produce structured outputs that writing and formatting can reuse.

### 4. Writing

Use `$paper-writing-workflow` after the outline and evidence baseline are clear. Draft one chapter or section at a time unless the user explicitly asks for a compact deliverable.

### 5. Figures

Use `$academic-figure-workflow` for all figures that are not trivial tables. Default to:

- SVG for mechanism, concept, and moderately complex academic diagrams.
- Draw.io for workflows, use cases, system architecture, module, and data-flow diagrams.
- OpenAI image generation only after user confirmation and API availability confirmation.

### 6. Formatting

Use `$academic-formatting-workflow` only after content is reasonably stable. Prefer user-provided handbook, template, or journal guide over general rules.

### 7. Post-Draft Benchmark Review

Use `$post-manuscript-benchmark-review` after a complete first draft or integrated chapter exists and the user asks for readiness, SCI/Q1 evaluation, benchmark-paper comparison, or next-version optimization. Provide the draft, target standard, benchmark papers, evidence register, figures/tables, and unresolved claim list. Do not use the post-draft review gate for topic planning, early literature search, isolated polishing, or formatting-only work.

## Evidence And Version Discipline

- Keep a single evidence register or literature master list for the project.
- Mark items as `candidate`, `verified`, `downloaded`, `parsed`, `cited`, or `rejected`.
- Keep paired Markdown and DOCX outputs at the same semantic version when both exist.
- Create a version note for major changes.
- Save new outputs with explicit suffixes; do not overwrite the only working draft unless the user explicitly requests it.
- Validate `project_state.json` before moving from research/parsing into drafting, and before moving from writing into formatting.

## Fallbacks

- If literature verification requires network access and network is unavailable, create a manual verification queue with exact DOI/title/search strings.
- If PDF parsing fails, list failed pages and recommended manual recovery.
- If a DOCX needs Word-only features such as TOC refresh or field updates, explain what can be automated and what requires Word.
- If a requested figure cannot be drawn faithfully from evidence or code, decline the specific figure or mark it as a user-provided/manual asset.
- If the user wants to skip a gate, comply only after stating the risk.

## Reference

Read [stage-map.md](references/stage-map.md) when a full project needs a compact stage checklist or when resuming a long-running thesis workflow.

Read [project-artifact-templates.md](references/project-artifact-templates.md) when creating a project state file, handoff packet, or target-baseline note.

## Bundled Utilities

- `scripts/project_state_check.py`: create a JSON project-state template or validate project state, required handoff packets, gate consistency, evidence readiness, and formatting readiness.
