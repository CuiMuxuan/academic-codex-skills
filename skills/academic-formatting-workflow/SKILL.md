---
name: academic-formatting-workflow
description: "Format, normalize, and quality-check academic manuscripts, theses, dissertations, reports, and journal submissions according to a provided school handbook, Word template, journal guide, or general bilingual academic formatting rules. Use for DOCX layout, headings, margins, fonts, abstracts, references, captions, table of contents, page numbering, final document packaging, and Markdown-to-DOCX conversion with LaTeX-readable formulas, superscript/subscript preservation, and citation or reference cross-references. Chinese triggers: 论文排版, 毕业论文格式, Word模板, 学校格式手册, 期刊格式, 目录页码, 参考文献格式, Markdown转Word, md转docx, LaTeX公式转换, 上标下标转换, 参考文献交叉引用."
---

# Academic Formatting Workflow

Use this skill after content is stable enough for formatting. Template and handbook requirements always outrank general rules.

## Priority Order

1. User-provided school handbook, thesis guide, journal instructions, or official template.
2. Formatting requirements stated by the user or supervisor.
3. Existing correct formatting in the target DOCX.
4. General academic formatting conventions.

If sources conflict, show the conflict and ask for confirmation before applying the rule.

## Boundaries

Do:

- Inspect document structure and formatting requirements.
- Normalize headings, body text, abstracts, captions, tables, references, margins, and page numbering.
- Normalize Markdown-to-DOCX conversions, including formulas, superscripts/subscripts, citations, cross-references, captions, and bibliography fields.
- Save a new formatted copy and report unresolved manual checks.

Do not:

- Rewrite academic content beyond formatting unless the user asks.
- Verify literature identity; route to `$academic-research-verification`.
- Draft chapters; route to `$paper-writing-workflow`.
- Generate diagrams; route to `$academic-figure-workflow`.
- Silently refresh Word-only fields if automation is unavailable.
- Overwrite or replace the target document in place without explicit confirmation.

## Intake

Identify the target document, official handbook/template/journal guide, target examples, language and bilingual front matter, citation style, Markdown-to-DOCX needs, Word automation permission, output naming preference, and overwrite permission.

Before inspecting or modifying any document, ask for missing materials that would materially improve formatting quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

If no official guide is provided, state that formatting will use a provisional general academic baseline. If target examples are provided, infer patterns from them but do not let them override official rules.

## Mandatory Checkpoints

Stop and ask before:

- applying a rule when handbook, template, journal guide, supervisor instruction, or existing DOCX style conflict;
- using Word COM automation, template attachment, macro-enabled files, or any workflow that opens Word;
- overwriting or replacing the target document in place;
- treating a provisional baseline as final;
- making broad formatting changes while content is still actively changing;
- converting Markdown formulas, citations, or cross-references into lossy DOCX output;
- claiming final readiness when TOC, fields, cross-references, captions, or page numbering still require Word refresh.

## Workflow

1. Inventory inputs and missing rule sources.
2. Extract the formatting baseline from the official guide, template, target examples, or provisional baseline.
3. Use [formatting-run-plan.md](references/formatting-run-plan.md) to create the rule table, pass plan, output naming, and report structure.
4. Use [markdown-to-docx-conversion.md](references/markdown-to-docx-conversion.md) when source Markdown formulas, superscripts/subscripts, citations, bibliography entries, or cross-references must survive DOCX conversion.
5. Apply formatting in separate passes and save a new output copy.
6. Use [formatting-validation.md](references/formatting-validation.md) before calling the output ready.

## Reference

Read [formatting-rule-checklist.md](references/formatting-rule-checklist.md) when applying a school handbook, Word template, or journal formatting guide.

Read [target-template-intake.md](references/target-template-intake.md) when the user lacks a strict handbook/template or wants formatting inferred from approved examples.

Read [markdown-to-docx-conversion.md](references/markdown-to-docx-conversion.md) when converting Markdown manuscripts to DOCX or validating converted formulas, superscripts/subscripts, citations, bibliography entries, and cross-references.

Read [formatting-run-plan.md](references/formatting-run-plan.md) when planning formatting passes, safe output naming, and the formatting report.

Read [formatting-validation.md](references/formatting-validation.md) for final QA, provisional baseline checks, and Word refresh rules.

## Bundled Utilities

- `scripts/docx_style_inventory.py`: no-dependency DOCX style and paragraph-style usage inventory.
- `scripts/docx_apply_basic_styles.py`: conservative `python-docx` baseline formatter for a new output copy; does not refresh Word-only fields.
- `scripts/refresh_word_fields.ps1`: optional Windows/Microsoft Word COM finalization script for TOC, fields, tables of figures, indexes, and repagination. Requires explicit user permission to open Word.
