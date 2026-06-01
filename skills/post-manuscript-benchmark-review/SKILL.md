---
name: post-manuscript-benchmark-review
description: "Post-draft academic manuscript review against benchmark papers. Use only after an initial full manuscript draft, thesis chapter draft, or journal paper draft exists and the user asks for review, grading, gap analysis, target-paper comparison, SCI/Q1 readiness assessment, benchmark-literature comparison, reviewer-comment response planning, or next-version optimization planning. Do not use during outline planning, literature search, figure generation, citation verification, formatting, or de-AI polishing unless a complete draft already exists. Chinese triggers: 初版论文后评审, 论文生成后评审, 对标文献差距, SCI一区评审, 论文质量评判, 下一版优化方案, 与对标论文比较, 审稿意见处理."
---

# Post-Manuscript Benchmark Review

Use this skill as a post-draft quality gate. It reviews a complete or substantial academic draft against benchmark papers and produces the next-version revision plan.

## Activation Gate

Proceed only when a complete initial manuscript, integrated thesis chapter, or substantial full draft exists.

Do not run this skill for topic selection, outline design, literature discovery before drafting, PDF/DOCX parsing alone, figure/table generation alone, citation verification alone, formatting, or de-AI polishing before a full draft exists. Route those tasks upstream.

## Boundaries

Do:

- Judge a full draft against target standards and 3-10 benchmark papers.
- Identify manuscript gaps, claim risks, evidence needs, and next-version P0/P1/P2 actions.
- Analyze reviewer/editor/supervisor comments in the context of a complete draft.

Do not:

- Fabricate benchmark papers, DOI records, journal levels, acceptance probabilities, or benchmark-paper contents.
- Treat abstract-only or metadata-only benchmark information as full-paper evidence.
- Rewrite the manuscript as the primary task; route confirmed revisions to `$paper-writing-workflow`.
- Perform citation identity checks as final authority; route to `$academic-research-verification`.

## Intake

Collect draft path/content, target paper type, target journal/school/quality tier, reference list, evidence register, figures/tables, results/data, code or analysis scripts, benchmark papers, reviewer/supervisor comments, and missing-material constraints.

Before reviewing, ask for missing materials that would materially improve review quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

If key inputs are unavailable, produce a provisional review plan and materials request instead of a final readiness judgment.

## Workflow

1. Confirm the post-draft gate and review target.
2. Build or validate the 3-10 benchmark set with [benchmark-selection-and-extraction.md](references/benchmark-selection-and-extraction.md).
3. Apply the four-criterion review and claim triage in [review-rubric.md](references/review-rubric.md).
4. Use [benchmark-report-schema.md](references/benchmark-report-schema.md) to keep benchmark facts, access limits, manuscript claim records, gap severity, and next-version actions auditable.
5. Use [reviewer-comment-response-workflow.md](references/reviewer-comment-response-workflow.md) and [reviewer-comment-action-plan-gate.md](../../shared/reviewer-comment-action-plan-gate.md) when concrete reviewer, editor, committee, or supervisor comments are provided for a complete draft.
6. Use [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) before approving factual, boundary, subjective, contribution, limitation, or rebuttal judgments.
7. Use [review-output-template.md](references/review-output-template.md) for formal Chinese reports, readiness judgments, benchmark gap tables, and next-version plans.
8. Return readiness level, evidence limits, benchmark gaps, P0/P1/P2 actions, material requests, and handoff packets.

## Quality Gate

The review is high quality only if it:

- names exact draft sections, figures, tables, claims, data, code, or evidence-register keys behind each critique;
- separates benchmark facts from inference;
- distinguishes fatal blockers from optional polish;
- gives actions executable in the next manuscript iteration;
- marks missing evidence, benchmark access limits, and material dependencies explicitly.
- turns two or more review comments into a triaged action plan before manuscript rewriting.

## Reference

Read [benchmark-selection-and-extraction.md](references/benchmark-selection-and-extraction.md) when selecting or extracting benchmark papers.

Read [review-rubric.md](references/review-rubric.md) when scoring, gap-analyzing, judging readiness, or triaging claims.

Read [benchmark-report-schema.md](references/benchmark-report-schema.md) when producing benchmark material records, manuscript claim records, benchmark gap tables, or next-version action tables.

Read [reviewer-comment-response-workflow.md](references/reviewer-comment-response-workflow.md) when user-provided review comments must be accepted, partly accepted, rejected with reasons, prioritized, and turned into a next-stage plan.

Read [reviewer-comment-action-plan-gate.md](../../shared/reviewer-comment-action-plan-gate.md) when two or more review comments must become concrete modification actions.

Read [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) before treating benchmark, readiness, contribution, limitation, or rebuttal judgments as final prose.

Read [review-output-template.md](references/review-output-template.md) when producing a formal report, Chinese evaluation, SCI/Q1 readiness judgment, or benchmark gap table.
