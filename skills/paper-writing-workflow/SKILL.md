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
- Perform DOI or citation authenticity checks as a final authority; route that work to `$academic-research-verification`.
- Parse source PDFs or DOCX comments as the primary task; route to `$pdf-docx-parsing-workflow`.
- Finalize layout or Word formatting; route to `$academic-formatting-workflow`.
- Create nontrivial figures as the primary task; route to `$academic-figure-workflow`.
- Judge a complete manuscript against benchmark papers as the primary task; route post-draft readiness review to `$post-manuscript-benchmark-review`.

## Core Rules

1. Write from an approved outline or propose one first.
2. Keep claims proportional to evidence.
3. Mark unsupported claims as `needs evidence` instead of presenting them as settled facts.
4. Draft in Markdown by default unless the user asks for another format.
5. Work chapter by chapter for long papers.
6. Preserve the user's required language and citation style.
7. Do not overwrite the only working draft.
8. Stop for confirmation after each major chapter or integrated manuscript.

## Intake

Collect the minimum needed:

- Paper type and target audience.
- Required language: English, Chinese, or bilingual.
- Working title or topic.
- Required chapters or journal sections.
- Verified evidence register or literature list.
- Target examples: 3-10 accepted papers, approved theses, or supervisor-approved chapters when available.
- Existing draft or notes.
- Citation style.
- Length target.
- Deadline and review priorities.

If evidence is missing, produce a writing plan with evidence gaps rather than fabricating citations.
If target examples are missing, use a provisional generic writing baseline and state that section depth, evidence density, and tone may need later adjustment.

Before drafting, revising, or integrating manuscript text, ask for missing materials that would materially improve writing quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for target examples, approved outline, verified evidence register, parsed PDF notes, existing drafts, supervisor comments, citation style, figure/table plan, and required section headings as relevant. If unavailable, produce only a plan, gap list, or clearly provisional draft after the user confirms they want to proceed.

## Workflow

### 1. Diagnose The Writing Stage

Classify the task:

- `outline`: topic and structure are still forming.
- `section_draft`: one chapter or section needs drafting.
- `revision`: a draft exists and needs stronger logic, evidence, or style.
- `integration`: approved sections need a coherent full manuscript.
- `polish`: content is stable and language quality is the main target.

State the selected mode, active gate, and expected output.

Stage gate report:

```text
Mode:
Active gate: plan_only | draft_ready | revision_ready | needs_verification | needs_user_decision
Evidence status:
Allowed work now:
Blocked work:
Next confirmation:
```

Use `plan_only` when evidence, outline, or user decisions are insufficient for drafting. Use `needs_verification` when source authenticity or DOI/citation truth is unresolved and route that work to `$academic-research-verification`.

### 1.5. Prepare Inputs And Handoffs

Before drafting any substantial text, normalize the material that writing will consume:

| Input | Required handling |
|---|---|
| Verified evidence register | Use only entries marked `verified`, `parsed`, or explicitly user-approved; keep `candidate` items in an evidence gap list |
| Parsed PDF notes | Preserve source path, page/location, finding, method context, limitation, and citation key |
| Parsed DOCX comments | Convert comments into revision tasks with status, target section, and user-decision flags |
| Formatting guide or required headings | Use only to shape section structure; defer layout and style enforcement to `$academic-formatting-workflow` |
| Figure/table plan | Keep callouts and captions as placeholders until `$academic-figure-workflow` or the user confirms the artifact |
| Post-draft review request | Package the complete draft, target standard, benchmark set, evidence register, figures/tables, and unresolved claims for `$post-manuscript-benchmark-review` |

Read [chapter-drafting-checklist.md](references/chapter-drafting-checklist.md) when the task involves a full chapter, supervisor comments, bilingual writing, or integration of multiple evidence sources.

Read [writing-output-templates.md](references/writing-output-templates.md) when creating a paper design document, evidence-to-section map, section draft packet, or revision report.

Read [writing-output-templates.md](references/writing-output-templates.md) when target papers, benchmark papers, approved theses, or supervisor-approved chapters are available and you need to build a writing-alignment brief before drafting.

### 2. Build Or Confirm The Design Document

For substantial papers, prepare:

- Research problem.
- Scope and exclusions.
- Central argument or contribution.
- Chapter/section map.
- Evidence required per section.
- Figures and tables needed.
- Known risks.

Stop for confirmation before drafting substantial body text.

### 2.5. Align With Target Or Benchmark Writing

Use this module before drafting or revising when the user provides 3-10 target papers, benchmark papers, accepted manuscripts, approved theses, or supervisor-approved chapters. The goal is to align manuscript writing with the target's rhetorical function and evidence standard, not to copy style.

Create a writing-alignment brief:

```text
Target set:
Section to draft:
Section job in benchmark papers:
Typical evidence density:
Claim style:
Citation pattern:
Figure/table callout pattern:
Limitation and uncertainty style:
Features to match:
Features to avoid:
Drafting implication:
```

Rules:

1. Extract section function before wording: how the target papers open the problem, introduce the gap, report methods, interpret results, and state limitations.
2. Match evidence density and claim discipline before matching prose tone.
3. Use benchmark papers to calibrate length, paragraph roles, citation grouping, figure/table callouts, and how much mechanism or validation detail belongs in the main text.
4. Do not imitate distinctive phrasing, sentence rhythm, or proprietary text from target papers.
5. If target examples conflict with the user's data strength, follow the evidence. A high-impact writing pattern does not justify a stronger claim than the manuscript can support.
6. If no target examples exist, state that the writing uses a provisional general academic baseline and list what may need recalibration later.

Use the alignment brief to constrain drafting. Each generated section should show how the draft follows the intended section job and where it deliberately diverges because evidence, audience, or target format differs.

### 3. Draft With Evidence Discipline

For each section:

1. State the section purpose.
2. List evidence items to use.
3. List evidence gaps and unresolved user decisions.
4. Draft the section.
5. Add citation placeholders or citation keys only for verified sources.
6. Mark weak or missing support.
7. Summarize what changed and what needs user review.

Use topic sentences, transitions, and explicit links between evidence and claims.

When a draft contains citation keys and an evidence register is available, run the deterministic alignment audit before calling the draft evidence-clean:

```bash
python scripts/audit_evidence_alignment.py --draft chapter_02.md --evidence-register evidence_register.csv --output-csv evidence_alignment_audit.csv --output-md evidence_alignment_audit.md
```

Treat `citation_missing_from_register`, `citation_not_writing_ready`, and unresolved `needs evidence` markers as blocking unless the user explicitly approves a provisional draft.

Default section-output template:

```text
Mode:
Section purpose:
Target/benchmark alignment:
Evidence used:
Evidence gaps:
Draft:
User-review items:
Next step:
```

### 4. Handle Review Papers

Emphasize:

- Search scope and inclusion criteria.
- Taxonomy or comparison framework.
- Synthesis across studies.
- Agreement, conflict, and gaps.
- Limitations of the review.

Avoid turning the paper into an annotated bibliography.

### 5. Handle Experimental Papers

Emphasize:

- Methods that match actual data and procedures.
- Results that match provided analysis.
- Discussion that distinguishes observation, interpretation, and speculation.
- Limitations and reproducibility.

Do not analyze data or invent results unless the user provides data and authorizes analysis.

### 6. Handle Theses And Dissertations

Emphasize:

- Chapter continuity.
- School-required sections.
- Literature review depth.
- Method or system design consistency.
- Figure and table callouts.
- Formal bilingual abstract when required.

When a thesis describes software or experiments, verify implementation claims against the codebase or provided artifacts before drafting as fact.

## Revision Modes

Use the mode that matches the user's request:

| Mode | Action |
|---|---|
| `logic` | Strengthen argument sequence, transitions, and section roles |
| `evidence` | Add, remove, or flag claims based on verified evidence |
| `style` | Improve academic tone, precision, concision, and bilingual consistency |
| `structure` | Reorganize headings, paragraph order, and chapter balance |
| `supervisor_response` | Address review comments one by one and preserve a change log |

## Outputs

Typical outputs:

- `paper_design.md`.
- `chapter_01_vX.Y.md`.
- `section_<name>_draft.md`.
- `integrated_manuscript_vX.Y.md`.
- `revision_report.md`.
- `evidence_gap_list.md`.

When producing a draft, include a compact stage report with:

- Active gate and allowed work.
- What was drafted or revised.
- Evidence used.
- Unsupported or uncertain claims.
- Next recommended step.

For supervisor-comment or DOCX-derived revisions, include:

- Comment or revision id.
- Target section.
- Action taken.
- Status: `done`, `partly_done`, `rejected_with_reason`, or `needs_user_decision`.
- Follow-up evidence or formatting handoff.

## Quality Checklist

Before claiming a writing task is complete, check:

- The section answers its stated purpose.
- The section follows the target/benchmark alignment brief when target examples were available.
- Major claims have verified evidence or are flagged.
- Citations are present where needed.
- Draft citation keys have been audited against the evidence register when a register exists.
- No bibliography-only source is implied as cited.
- Terminology is consistent.
- Chinese and English terms are paired consistently in bilingual work.
- Figure and table references match planned or existing artifacts.

## Bundled Utilities

- `scripts/audit_evidence_alignment.py`: deterministic citation-key and evidence-register audit for Markdown/Pandoc or LaTeX-style drafts. Outputs CSV/Markdown issue reports and flags citations missing from the register, citations not writing-ready, unused verified evidence, and `needs evidence` markers.

## Reference

Read [chapter-drafting-checklist.md](references/chapter-drafting-checklist.md) when drafting long chapters, responding to supervisor comments, or integrating multiple sections.
