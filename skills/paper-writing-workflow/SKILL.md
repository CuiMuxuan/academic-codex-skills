---
name: paper-writing-workflow
description: "Plan, draft, revise, and integrate academic papers, theses, dissertations, review papers, experimental papers, and manuscript chapters from verified evidence. Use when the user asks for chapter outlines, paper structure, academic prose, bilingual Chinese-English writing, literature-backed claims, section-by-section drafting, revision, polishing, or integrated manuscript assembly. Chinese triggers: 论文写作, 章节写作, 论文润色, 综述写作, 毕业论文正文, 学术表达."
---

# Paper Writing Workflow

Use this skill for academic writing after the writing goal and evidence baseline are clear. It owns structure, argument, chapter drafting, revision, and integration.

## Boundaries

Do:

- Plan paper structure.
- Draft and revise sections.
- Integrate verified evidence into claims.
- Improve academic style in English, Chinese, or bilingual manuscripts.
- Track claims that still need evidence.

Do not:

- Treat unverified literature as trusted.
- Perform DOI or citation authenticity checks as final authority; route to `$academic-research-verification`.
- Parse PDFs or DOCX comments as the primary task; route to `$pdf-docx-parsing-workflow`.
- Finalize layout or Word formatting; route to `$academic-formatting-workflow`.
- Create nontrivial figures as the primary task; route to `$academic-figure-workflow`.
- Judge a complete manuscript against benchmark papers as the primary task; route to `$post-manuscript-benchmark-review`.

## Core Rules

1. Write from an approved outline or propose one first.
2. Keep claims proportional to evidence.
3. Mark unsupported claims as `needs evidence`.
4. Draft in Markdown by default unless the user asks for another format.
5. Work chapter by chapter for long papers.
6. Preserve the user's required language and citation style.
7. Do not overwrite the only working draft.
8. Stop for confirmation after each major chapter or integrated manuscript.

## Intake

Collect paper type, audience, language, title/topic, required sections, verified evidence register, target examples, existing draft/notes, citation style, length target, deadline, and review priorities.

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
2. Normalize inputs and downstream handoffs with [writing-input-handoffs.md](references/writing-input-handoffs.md).
3. Build or confirm the design document: problem, scope, contribution, section map, evidence needed, figures/tables, and risks.
4. If target examples are available, use [target-benchmark-writing-alignment.md](references/target-benchmark-writing-alignment.md) and [writing-output-templates.md](references/writing-output-templates.md).
5. Draft with evidence discipline: section purpose, evidence used, evidence gaps, draft, citation placeholders only for verified sources, and user-review items.
6. Use [manuscript-type-playbooks.md](references/manuscript-type-playbooks.md) for review papers, experimental papers, theses, dissertations, and code-backed/system manuscripts.
7. Use [revision-and-quality-checks.md](references/revision-and-quality-checks.md) before calling writing complete.

## Reference

Read [writing-stage-gates.md](references/writing-stage-gates.md) to classify outline, draft, revision, integration, or polish readiness.

Read [writing-input-handoffs.md](references/writing-input-handoffs.md) before drafting from verified evidence, parsed notes, DOCX comments, figure plans, or post-draft review packets.

Read [chapter-drafting-checklist.md](references/chapter-drafting-checklist.md) when drafting long chapters, responding to supervisor comments, or integrating multiple sections.

Read [writing-output-templates.md](references/writing-output-templates.md) when creating a paper design document, evidence-to-section map, section draft packet, benchmark-calibrated section packet, or revision report.

Read [target-benchmark-writing-alignment.md](references/target-benchmark-writing-alignment.md) when using target examples or benchmark papers to shape a section.

Read [manuscript-type-playbooks.md](references/manuscript-type-playbooks.md) when writing review, experimental, thesis, dissertation, or code-backed/system manuscripts.

Read [revision-and-quality-checks.md](references/revision-and-quality-checks.md) for revision modes, output packets, supervisor-comment handling, and quality checks.

## Bundled Utilities

- `scripts/audit_evidence_alignment.py`: deterministic citation-key and evidence-register audit for Markdown/Pandoc or LaTeX-style drafts. Outputs CSV/Markdown issue reports and flags citations missing from the register, citations not writing-ready, unused verified evidence, and `needs evidence` markers.
