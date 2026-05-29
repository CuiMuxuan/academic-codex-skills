---
name: academic-de-ai-polishing
description: "Use when polishing stable paper, review, thesis, rebuttal, or other scholarly prose that reads mechanically, over-smoothed, obviously AI-assisted, or contaminated by internal project notes, operation logs, process records, TODOs, handoff language, or draft-management traces in the manuscript body. Best after content, structure, evidence, citations, and claim strength are stable, for section-by-section rewriting that preserves meaning, citations, and technical rigor while reducing templated transitions, repetitive cadence, formulaic academic phrasing, and non-manuscript operational residue. Chinese triggers: 论文降AI痕迹, 去AI味, 去模板化润色, 降低机械感, 学术润色, 最终润色, AIGC痕迹评估, 内部项目记录, 操作记录痕迹, 主文日志化."
---

# Academic De-AI Polishing

Use this skill to reduce mechanical or AI-like academic prose while preserving the core argument, evidence balance, citation logic, terminology, and technical scope.

## Boundaries

Do:

- Rewrite local paragraphs or adjacent paragraph blocks.
- Reduce templated transitions, repetitive cadence, vague academic filler, and over-smooth balance.
- Remove or recast internal project notes, operation logs, prompt traces, TODO markers, and draft-management residue.
- Preserve or strengthen evidence-grounded authorial judgment.
- Enforce final-polish boundaries after writing, evidence, and structure are stable.

Do not:

- Fabricate evidence, citations, results, or conclusions.
- Change claim strength beyond what the evidence supports.
- Claim detector percentages or guarantee AIGC-score outcomes.
- Regenerate whole sections unless the user explicitly asks.
- Use polish to bypass missing evidence, unresolved `LIT_GAP` markers, or unstable manuscript structure.

## Core Rules

1. Preserve technical meaning, evidence balance, citation logic, section purpose, and terminology.
2. Fix argument, evidence scope, and claim precision before fixing cadence.
3. Prefer paragraph-level rewrites over whole-section regeneration.
4. Do not make prose more confident than the evidence permits.
5. Keep Chinese, English, and bilingual terminology stable unless the user asks for translation.
6. Move unresolved author decisions to `User-review items` instead of hiding them in polished prose.
7. Treat accurate, direct, concise, understandable writing as the baseline; style elevation is optional and must stay evidence-safe.

## Pre-Edit Gate

Before rewriting, confirm or infer:

```text
Source text present:
Section type:
Paragraph role:
Fixed claims and citations:
Claim anchors, if available:
Allowed edit intensity:
Do-not-change terms:
```

If source text is missing, ask for it. If citation or evidence boundaries are unclear, keep the rewrite conservative and mark author verification needs.

## Argument-First Gate

Classify each target paragraph:

| State | Action |
|---|---|
| `sound_argument_mechanical_style` | Rewrite for cadence, vocabulary, transitions, and authorial voice. |
| `overclaiming_or_missing_evidence` | Flag the claim problem first, then soften or request evidence before polishing. |
| `unclear_section_job` | Ask for section role or propose a local role before rewriting. |
| `citation_boundary_unclear` | Preserve citations conservatively and mark claims that need author verification. |
| `internal_project_or_operation_trace` | Remove or recast workflow residue using `manuscript-residue-cleanup.md`. |

## Workflow

1. Identify medium- and high-risk paragraphs.
2. Diagnose the dominant risk: connector overload, repetitive cadence, templated dialectic, vague vocabulary, missing judgment, overclaiming, or workflow residue.
3. Use [final-polish-boundary.md](references/final-polish-boundary.md) before broad final polishing or when the request may hide evidence, structure, or claim-strength work.
4. Use [high-risk-patterns.md](references/high-risk-patterns.md) for pattern diagnosis and [rewrite-tactics.md](references/rewrite-tactics.md) for revision tactics.
5. Use [section-playbooks.md](references/section-playbooks.md) when the rewrite problem is section-dependent.
6. Use [manuscript-residue-cleanup.md](references/manuscript-residue-cleanup.md) when main text contains project, operation, prompt, or file-management traces.
7. After each rewrite, verify meaning, citations, terminology, claim anchors, and technical scope.

## Material Request

Before assessment or rewriting, ask for missing materials that would materially improve quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for source text, target examples, section type, paragraph role, fixed claims, fixed citations, do-not-change terms, allowed edit intensity, and whether the user wants diagnosis only or rewrite.

## Reference

Read [edit-contract-template.md](references/edit-contract-template.md) when the edit boundary is unclear.

Read [final-polish-boundary.md](references/final-polish-boundary.md) when deciding whether the manuscript is ready for final polish or whether the task should route back to writing, research verification, or post-draft review.

Read [high-risk-patterns.md](references/high-risk-patterns.md) when diagnosing mechanical or AI-shaped sentence patterns.

Read [rewrite-tactics.md](references/rewrite-tactics.md) for paragraph-level rewrite tactics, target-example calibration, and output patterns.

Read [before-after-examples.md](references/before-after-examples.md) when the user wants examples or when calibration is needed.

Read [section-playbooks.md](references/section-playbooks.md) for abstract, introduction, technology, discussion, review, or thesis-section handling.

Read [project-notes-from-this-paper.md](references/project-notes-from-this-paper.md) for long review-paper polishing sequences.

Read [manuscript-residue-cleanup.md](references/manuscript-residue-cleanup.md) for internal project notes, operation logs, prompt traces, file-management language, handoff language, TODO markers, or draft residue.

Read [ai-trace-assessment.md](references/ai-trace-assessment.md) when the user asks for AI-trace or AIGC-risk assessment.
