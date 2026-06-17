---
name: paper-writing-workflow
description: "Plan, draft, revise, and integrate academic papers, theses, dissertations, review papers, experimental papers, and manuscript chapters from verified evidence. Use when the user asks for chapter outlines, paper structure, academic prose, bilingual Chinese-English writing, literature-backed claims, section-by-section drafting, revision, supervisor or reviewer comment response planning, introduction logic, abbreviation-first-use checks, evidence-gap marking, field terminology control, integrated manuscript assembly, data-figure body narration, rhetorical-depth calibration for正文 vs summary transitions, or multi-agent/sub-agent parallel checks for writing evidence support, subsection language audit, citation-distance audit, or reviewer-comment action decomposition. Chinese triggers: 论文写作, 章节写作, 论文润色, 综述写作, 毕业论文正文, 学术表达, 引言逻辑, 文献缺口, 待补证据, 评审意见修改, 术语规范, 数据图解读, 正文图表分析, 深度改写, 多agent写作审查, 子agent证据检查, 并行语言审查."
---

# Paper Writing Workflow

Use this skill for academic writing after the writing goal and evidence baseline are clear. It owns structure, argument, detailed design documents, chapter drafting, ordinary prose revision, section-level figure narration, and integration.

## Boundaries

Do:

- Plan paper structure.
- Draft and revise sections.
- Integrate verified evidence into claims.
- Improve academic clarity in English, Chinese, or bilingual manuscripts.
- Track claims that still need evidence.
- Prepare comment-response revision plans before editing.
- Execute approved structure, section, or chapter rewrites when `$revision-control` escalates beyond sentence-level editing.

Do not:

- Treat unverified literature as trusted.
- Perform DOI or citation authenticity checks as final authority; route to `$academic-research-verification`.
- Parse PDFs or DOCX comments as the primary task; route to `$pdf-docx-parsing-workflow`.
- Finalize layout or Word formatting; route to `$academic-formatting-workflow`.
- Create nontrivial figures as the primary task; route to `$academic-figure-workflow`.
- Perform final de-AI style polishing as the primary task after content is stable; route to `$academic-de-ai-polishing`.
- Judge a complete manuscript against benchmark papers as the primary task; route to `$post-manuscript-benchmark-review`.
- Perform language-style review as the primary task; route to `$language-style-review`.
- Maintain formal sentence-level revision state, pass/fail status, round numbers, complete latest review drafts, or object libraries; route to `$revision-control`.

## Core Rules

1. Write from an approved outline or propose one first.
2. Insert a detailed paper or chapter design document between material preparation and formal drafting.
3. Keep claims proportional to evidence.
4. Mark unsupported claims with `LIT_GAP` or `needs evidence`; do not fabricate citations.
5. Draft in Markdown by default unless the user asks for another format.
6. Work chapter by chapter for long papers.
7. Preserve the user's required language and citation style.
8. Do not overwrite the only working draft.
9. Stop for confirmation after each major chapter or integrated manuscript.
10. During drafting and ordinary revision, prioritize accurate, direct, concise, understandable prose; reserve style elevation for the final polishing pass unless the target section is a正文机理段、数据图解读段、摘要、引言、结论, or other section that needs a calibrated rhetorical mode.
11. From the first body-text section onward, write the full term followed by the abbreviation in parentheses on first use unless the target style guide says otherwise; title, abstract, and highlights are exempt by default.
12. Judge manuscript quality by whether the problem is clear, the method is reasonable, the experiments support the conclusion, and the contribution is explicit.
13. For body text and rebuttal text, stop when factual, boundary, subjective, novelty, contribution, or limitation claims lack concrete support; title, abstract, highlights, and graphical abstract are exempt unless the target rules require otherwise.
14. Give each chapter, major section, and subsection a clear local purpose without forcing artificial transitions.
15. For正文 data-figure commentary, describe the figure's role, quantitative pattern, best/worst region, concentration or sparsity, and implication before polishing the prose.
16. After an initial full draft, hand complex sentence-by-sentence revision, pass/fail confirmation, and latest-draft state management to `$revision-control`.
17. Apply the shared citation-proximity gate when placing or revising citations.
18. Route strict language-style diagnosis to `$language-style-review`; use local language checks only as part of drafting or ordinary revision.
19. Apply [academic-rhetorical-depth-modes.md](references/academic-rhetorical-depth-modes.md) when the user wants a denser正文机理版 or a紧凑摘要/引言/过渡版.
20. Apply [data-figure-body-analysis.md](references/data-figure-body-analysis.md) when writing正文 about a data figure and the paragraph must explain the figure's purpose, quantitative pattern, and implication.
21. Apply the shared equation/formula standard when writing or revising formulas, equations, inline math, chemical notation, unit notation, or equation cross-references. Use LaTeX as the canonical source. If no journal or school rule is supplied, use the default formula standard; if a target journal/template rule exists, follow it.
22. For substantial writing reviews, evidence checks, strict language audits, or reviewer-comment decomposition, plan multi-agent parallel checks by default; start sub-agents only after user confirmation unless prior full or automatic-execution permission exists.

## Intake

Collect paper type, audience, language, title/topic, research field, target venue or school field, required sections, verified evidence register, target examples, existing draft/notes, citation style, length target, deadline, and review priorities.

Before drafting, revising, or integrating manuscript text, ask for missing materials that would materially improve writing quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

If evidence is missing, produce a writing plan with evidence gaps rather than fabricating citations.

## Workflow

1. Diagnose the writing mode and active gate with [writing-stage-gates.md](references/writing-stage-gates.md).
2. Set or confirm the current research field and terminology boundary with [field-and-terminology-control.md](references/field-and-terminology-control.md).
3. Normalize inputs and downstream handoffs with [writing-input-handoffs.md](references/writing-input-handoffs.md).
4. Build or confirm the detailed design document before drafting: target venue, article type, chapter structure, each chapter's goal, each section's task, expected word counts, evidence needs, figure/table plan, risks, and missing materials.
5. Run outline-level evidence precheck with [literature-gap-and-evidence-precheck.md](references/literature-gap-and-evidence-precheck.md) before drafting substantive claims.
6. Apply [claim-evidence-anchor-protocol.md](references/claim-evidence-anchor-protocol.md) for central claims, contribution statements, result claims, benchmark comparisons, and code/data/experiment statements.
7. Apply [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) before final main-text or rebuttal claim wording.
8. Apply [citation-proximity-and-style-gate.md](../../shared/citation-proximity-and-style-gate.md) when placing, moving, or auditing citations.
9. Apply [equation-and-formula-standard.md](../../shared/equation-and-formula-standard.md) whenever formulas, equations, math notation, chemical notation, unit notation, or equation references are written or revised.
10. Apply [cross-disciplinary-language-review-gate.md](../../shared/cross-disciplinary-language-review-gate.md) only when the user asks for language or terminology review, strict sentence-by-sentence checking, or when formal body text or rebuttal prose clearly shows abstract terms, undefined local labels, operation-record residue, unclear sentence purpose, unsupported proxy wording, citation-distance problems, or bilingual strength drift.
11. Apply [multi-agent-academic-workflow-gate.md](../../shared/multi-agent-academic-workflow-gate.md) before launching independent writing-related checks such as evidence support review, subsection language audit, citation-distance audit, or reviewer-comment action decomposition.
12. If target examples are available, use [target-benchmark-writing-alignment.md](references/target-benchmark-writing-alignment.md) and [writing-output-templates.md](references/writing-output-templates.md).
13. Draft with [academic-prose-and-claim-standards.md](references/academic-prose-and-claim-standards.md): section purpose, subsection independence, evidence used, evidence gaps, draft, citation placeholders only for verified sources, and user-review items.
14. Use [introduction-logic-playbook.md](references/introduction-logic-playbook.md) for Introduction, background, problem statement, or thesis-opening sections.
15. Use [manuscript-type-playbooks.md](references/manuscript-type-playbooks.md) for review papers, experimental papers, theses, dissertations, and code-backed/system manuscripts.
16. Use [revision-and-quality-checks.md](references/revision-and-quality-checks.md) before calling writing complete.
17. Use [reviewer-comment-response-workflow.md](references/reviewer-comment-response-workflow.md) and [reviewer-comment-action-plan-gate.md](../../shared/reviewer-comment-action-plan-gate.md) when the user provides two or more supervisor, reviewer, or committee comments during normal writing/revision.
18. When `$revision-control` escalates a confirmed issue to chapter/section rewrite, execute only the approved rewrite scope and return outputs to `$revision-control` for object-library rebuild and renumbering.

## Reference

Read [writing-stage-gates.md](references/writing-stage-gates.md) to classify outline, draft, revision, integration, or polish readiness.

Read [field-and-terminology-control.md](references/field-and-terminology-control.md) before drafting or revising when the research field, target venue field, or cross-domain terminology is unclear.

Read [writing-input-handoffs.md](references/writing-input-handoffs.md) before drafting from verified evidence, parsed notes, DOCX comments, figure plans, or post-draft review packets.

Read [literature-gap-and-evidence-precheck.md](references/literature-gap-and-evidence-precheck.md) before drafting from an outline or when a claim needs more literature/data than currently available.

Read [claim-evidence-anchor-protocol.md](references/claim-evidence-anchor-protocol.md) when central claims, contribution statements, method comparisons, result claims, code/data/experiment claims, or figure-caption claims must remain traceable across writing, review, polish, and formatting.

Read [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) before writing final main-text or rebuttal sentences that make factual judgments, boundary statements, subjective evaluations, novelty claims, contribution claims, or limitation claims.

Read [citation-proximity-and-style-gate.md](../../shared/citation-proximity-and-style-gate.md) when placing, moving, reviewing, or auditing citations in manuscript text.

Read [equation-and-formula-standard.md](../../shared/equation-and-formula-standard.md) before writing, revising, or handing off formulas, equations, inline math, chemical notation, unit notation, or equation cross-references.

Read [cross-disciplinary-language-review-gate.md](../../shared/cross-disciplinary-language-review-gate.md) when the user asks for language review, terminology review, abstract-expression cleanup, operation-record cleanup, or strict sentence-by-sentence review of formal body text or rebuttal prose.

Read [multi-agent-academic-workflow-gate.md](../../shared/multi-agent-academic-workflow-gate.md) before planning parallel writing-related checks. Use it to decide when to propose sub-agents, when to skip them for simple local tasks, what output format to require, and how the main agent should merge results.

Read [academic-prose-and-claim-standards.md](references/academic-prose-and-claim-standards.md) for language baseline, abbreviation-first-use, paragraph logic, contribution framing, and claim evidence rules.

Read [introduction-logic-playbook.md](references/introduction-logic-playbook.md) when drafting or revising an Introduction, background, problem statement, or thesis-opening chapter.

Read [chapter-drafting-checklist.md](references/chapter-drafting-checklist.md) when drafting long chapters, responding to supervisor comments, or integrating multiple sections.

Read [academic-rhetorical-depth-modes.md](references/academic-rhetorical-depth-modes.md) when the user needs two writing outputs: a dense正文机理版 and a compact摘要/引言/过渡版.

Read [data-figure-body-analysis.md](references/data-figure-body-analysis.md) when the user asks for正文 text that interprets a data figure by pattern, extremum, concentration, sparsity, or implication.

Read [writing-output-templates.md](references/writing-output-templates.md) when creating a paper design document, evidence-to-section map, section draft packet, benchmark-calibrated section packet, or revision report.

Read [revision-control-contract.md](../../shared/revision-control-contract.md) when receiving an approved structure, section, chapter, or large-rewrite handoff from `$revision-control`.

Read [target-benchmark-writing-alignment.md](references/target-benchmark-writing-alignment.md) when using target examples or benchmark papers to shape a section.

Read [manuscript-type-playbooks.md](references/manuscript-type-playbooks.md) when writing review, experimental, thesis, dissertation, or code-backed/system manuscripts.

Read [revision-and-quality-checks.md](references/revision-and-quality-checks.md) for revision modes, output packets, supervisor-comment handling, and quality checks.

Read [reviewer-comment-response-workflow.md](references/reviewer-comment-response-workflow.md) when comments must be accepted, partly accepted, rejected with reasons, prioritized, and turned into a user-confirmed revision plan.

Read [reviewer-comment-action-plan-gate.md](../../shared/reviewer-comment-action-plan-gate.md) when two or more comments must be turned into concrete revision actions before editing.

## Bundled Utilities

- `scripts/audit_evidence_alignment.py`: deterministic citation-key and evidence-register audit for Markdown/Pandoc or LaTeX-style drafts. Outputs CSV/Markdown issue reports and flags citations missing from the register, citations not writing-ready, unused verified evidence, and `needs evidence` or `LIT_GAP` markers.
