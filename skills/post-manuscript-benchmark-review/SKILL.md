---
name: post-manuscript-benchmark-review
description: "Post-draft academic manuscript review against benchmark papers. Use only after an initial full manuscript draft, thesis chapter draft, or journal paper draft exists and the user asks for review, grading, gap analysis, target-paper comparison, SCI/Q1 readiness assessment, benchmark-literature comparison, or next-version optimization planning. Do not use during outline planning, literature search, figure generation, citation verification, formatting, or de-AI polishing unless a complete draft already exists. Chinese triggers: 初版论文后评审, 论文生成后评审, 对标文献差距, SCI一区评审, 论文质量评判, 下一版优化方案, 与对标论文比较."
---

# Post-Manuscript Benchmark Review

Use this skill as a **post-draft quality gate** for academic writing workflows. It complements `academic-paper-orchestrator`, `paper-writing-workflow`, `pdf-docx-parsing-workflow`, `academic-research-verification`, `academic-de-ai-polishing`, `academic-figure-workflow`, and `academic-formatting-workflow`.

## Activation Gate

Proceed only when a complete initial manuscript or substantial full draft exists. A complete draft may be a journal manuscript, thesis chapter, integrated paper draft, or manuscript markdown/DOCX with Abstract/Introduction/Methods/Results/Discussion or equivalent sections.

Do **not** run this skill for:

- topic selection;
- outline design;
- literature discovery before drafting;
- PDF/DOCX parsing alone;
- figure/table generation alone;
- citation verification alone;
- formatting or de-AI polishing before a full draft exists.

If the user asks for benchmark review before a draft exists, say that this gate belongs after the first complete draft and route to the appropriate upstream paper workflow.

## Required Inputs

Collect or infer these from local files and conversation:

- manuscript draft path or current draft content;
- target paper type and target standard, such as SCI Q1, STOTEN, Water Research, thesis, or supervisor standard;
- reference list, bibliography, or local PDF folder if available;
- user-provided benchmark papers, if any.

Before reviewing, ask for missing materials that would materially improve review quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for the complete draft, target journal/school/quality tier, 3-10 benchmark papers, reference list, local PDFs, data/results tables, figures, code or analysis scripts, supervisor comments, reviewer comments, and any claim-evidence register as relevant. If key inputs are unavailable, produce a provisional review plan and materials request instead of a final readiness judgment.

## Benchmark Paper Rule

Require **3-10 benchmark papers**.

1. If the user explicitly provides 3-10 benchmark papers, use them.
2. If the user provides more than 10, select the most similar and highest-quality 3-10 papers and explain the selection criteria.
3. If the user provides no explicit benchmark papers but references or PDFs exist, ask permission to parse existing references/PDFs, then identify the most similar and highest-quality 3-10 benchmark papers.
4. If fewer than 3 usable benchmark papers exist, ask the user for the manuscript target and quality requirement. Then search for suitable references if browsing/network is allowed or required by the environment.
5. If suitable papers can be downloaded automatically through approved tools, download or save them according to the active workflow. If not, provide a manual download list with title, DOI/link, journal, and why each paper is needed.

Use verified metadata where possible. Do not fabricate papers, DOIs, journal levels, metrics, or claims. When web search is required, follow browsing and citation rules from the active environment.

## Review Standard

Judge the manuscript as a reviewer would judge a submitted paper, not as a helper judging effort. Separate encouragement from readiness.

Use these readiness levels:

| Level | Meaning |
|---|---|
| `ready_with_minor_revision` | Core contribution, evidence, writing, figures, and citation discipline are close to the target standard. |
| `major_revision_required` | The manuscript has a plausible contribution but target-level evidence, structure, validation, or benchmark positioning is still incomplete. |
| `not_ready_for_target` | The current draft lacks the evidence, novelty, or manuscript norms needed for the stated target. |
| `cannot_judge_from_materials` | Missing draft, benchmarks, data, or source evidence prevents a defensible judgment. |

When a numerical score is useful, score each criterion from 1-5 and explain the evidence behind the score. Do not use scores as decoration; every low score must map to a concrete revision action.

## Review Workflow

1. Confirm the post-draft gate: identify the draft artifact and target standard.
2. Build the benchmark set using the 3-10 paper rule.
3. Read the manuscript evidence base: draft, results tables, claim gates, figures, methods scripts, evidence registers, and prior project notes as relevant.
4. Review by four criteria:
   - topic and literature review;
   - foundational knowledge and research capability;
   - innovation and paper value;
   - manuscript norms and writing quality.
5. Compare against each benchmark paper:
   - benchmark contribution and quality level;
   - what the current manuscript already matches or exceeds;
   - concrete remaining gap;
   - evidence needed to close the gap;
   - whether the gap blocks the target standard.
6. Identify current manuscript defects:
   - overclaiming;
   - missing evidence;
   - weak validation;
   - insufficient mechanism explanation;
   - missing baselines;
   - citation or source weakness;
   - narrative, figure, table, or formatting problems.
7. Produce the next-version optimization plan with P0/P1/P2 priorities.
8. List manual materials the user must provide.

## Benchmark Extraction Packet

For each benchmark paper, extract only what is relevant to comparison:

```text
Paper:
Why this is a benchmark:
Study design / data / task:
Method or argument strategy:
Validation or evidence standard:
Figures/tables that carry the main claim:
What reviewers would expect the current manuscript to match:
Gap pressure on current manuscript:
```

If the benchmark cannot be read directly, mark the comparison as metadata-only or abstract-only and avoid strong claims about its methods or results.

## Output Contract

Write in the user’s language. For Chinese requests, use Chinese.

For a full Chinese benchmark-review report, read [review-output-template.md](references/review-output-template.md) and adapt its report skeleton, benchmark gap table, P0/P1/P2 plan, and claim triage table to the user's manuscript. Use the template as structure, not filler; remove sections that are irrelevant and mark missing evidence explicitly.

Include these sections:

- `评审结论`
- `按评审标准逐项评价`
- `对标文献选择依据`
- `与对标文献的具体差距`
- `当前论文缺点和不足`
- `下一版优化方案与改进措施`
- `需要使用者提供或确认的资料清单`
- `是否达到目标档位的判定`

Make the review detailed and evidence-based. Use specific metrics, files, tables, figure names, manuscript sections, and benchmark-paper contrasts when available.

## Claim Discipline

Separate:

- what the manuscript can safely claim now;
- what requires additional evidence;
- what must not be claimed.

For high-stakes journal targeting, require direct evidence before allowing claims about external generalization, causal mechanisms, calibrated probabilities, universal model superiority, or solved rare-event warning.

## Quality Bar

The review is high quality only if it:

- names the exact draft sections, figures, tables, claims, or missing artifacts behind each critique;
- compares the manuscript against specific benchmark evidence rather than generic journal advice;
- distinguishes fatal blockers from optional polish;
- gives actions that can be executed in the next manuscript iteration;
- avoids unsupported claims about journal quartiles, acceptance probability, or benchmark-paper contents;
- preserves the user's target standard while being explicit when the target is unrealistic from current evidence.

## Reference Details

Read `references/review-rubric.md` when writing the full review, selecting benchmark papers, or producing the next-version plan.

Read `references/review-output-template.md` when the user asks for a formal report, Chinese evaluation, SCI/Q1 readiness judgment, or a benchmark gap table.
