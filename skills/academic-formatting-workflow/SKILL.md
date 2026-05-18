---
name: academic-formatting-workflow
description: "Format, normalize, and quality-check academic manuscripts, theses, dissertations, reports, and journal submissions according to a provided school handbook, Word template, journal guide, or general bilingual academic formatting rules. Use for DOCX layout, headings, margins, fonts, abstracts, references, captions, table of contents, page numbering, and final document packaging. Chinese triggers: 论文排版, 毕业论文格式, Word模板, 学校格式手册, 期刊格式, 目录页码, 参考文献格式."
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
- Produce a formatting checklist and change report.
- Save a new formatted copy.

Do not:

- Rewrite academic content beyond formatting unless the user asks.
- Verify literature identity; route to `$academic-research-verification`.
- Draft chapters; route to `$paper-writing-workflow`.
- Generate diagrams; route to `$academic-figure-workflow`.
- Silently refresh Word-only fields if automation is unavailable.

## Intake

Identify:

- Target document: latest DOCX or manuscript file.
- Official handbook, template, or journal guide.
- Target examples: 3-10 approved theses, accepted articles, official templates, or supervisor-approved files when available.
- Required language and bilingual front matter.
- Citation and bibliography style.
- Whether Word automation is available or permitted.
- Whether in-place replacement is allowed. Default: no.

If no official guide is provided, state that formatting will use a provisional general academic baseline.
If target examples are provided, inspect them only to infer formatting patterns; do not treat them as official rules when they conflict with a handbook, template, journal guide, or user instruction.

Before inspecting or modifying any document, ask for missing materials that would materially improve formatting quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for the latest DOCX, official handbook, Word template, journal guide, target examples, supervisor rules, citation style, output naming preference, Word automation permission, and overwrite permission as relevant. If unavailable, proceed only with a provisional baseline after the user confirms the limitation.

## Mandatory Checkpoints

Stop and ask for confirmation before:

- Applying a rule when handbook, template, journal guide, supervisor instruction, or existing DOCX style conflict.
- Using Word COM automation, template attachment, macro-enabled files, or any workflow that requires opening Word.
- Overwriting or replacing the target document in place.
- Treating a provisional baseline as final when no official guide is available.
- Making broad formatting changes after content is still actively changing.
- Claiming final readiness when TOC, fields, cross-references, captions, or page numbering still require Word refresh.

At each checkpoint, show:

```text
Decision needed:
Options:
Recommended choice:
Risk if skipped:
Output file that will be affected:
```

## Workflow

### 1. Inventory Inputs

List:

- Target manuscript.
- Formatting source documents.
- Existing templates.
- Required output format.
- Missing rule sources.

### 2. Extract Formatting Baseline

From the guide or template, capture:

- Page size and margins.
- Section breaks and page numbering.
- Header and footer requirements.
- Cover and front matter.
- Chinese and English abstracts.
- Heading levels and numbering.
- Body font, line spacing, paragraph spacing, and indentation.
- Captions, tables, formulas, references, appendices.

When the guide is long, create a compact rule table before editing.

Use this rule-table format:

| area | rule | source | priority | automation | status |
|---|---|---|---|---|---|
| heading | Heading 1 font and numbering | handbook p.X or template style | official/template/provisional | python-docx/Word COM/manual | pending/applied/needs Word refresh/unresolved |

Read [formatting-rule-checklist.md](references/formatting-rule-checklist.md) when building the rule table or when high-risk areas such as page numbering, TOC refresh, captions, or East Asian font mapping are involved.

Read [target-template-intake.md](references/target-template-intake.md) when the user lacks a strict handbook/template or wants formatting inferred from approved examples.

### 2.5. Create Formatting Run Plan

Before editing or giving a detailed plan, map rules to formatting passes:

| pass | scope | rule sources | tool | output copy | manual check |
|---|---|---|---|---|---|
| page setup | sections, margins, headers, page numbering | handbook/template/provisional | python-docx/Word COM/manual | `_pre_final` or planned suffix | Word refresh needed? |

Use one row per pass from page setup through final validation. Mark any pass as `manual` when it depends on Word-only behavior, template attachment, TOC refresh, field updates, or visual page inspection. If no official guide exists, label every provisional rule source as `provisional` and state what evidence would replace it.

### 3. Inspect The Document

Check:

- Heading hierarchy.
- Abstract and keywords.
- Table of contents.
- Figure and table captions.
- Reference section.
- Mixed Chinese-English font handling.
- Tables, formulas, appendices, and page breaks.

Use a DOCX inventory script when available before writing custom code.

### 4. Normalize In Passes

Apply formatting in separate passes:

1. Page setup and sections.
2. Front matter.
3. Heading hierarchy.
4. Body paragraphs.
5. Figures, tables, formulas, and captions.
6. References and appendices.
7. Final validation.

Use `python-docx` for stable paragraph, run, table, and section edits when available. Use Word COM automation only for Word-specific tasks such as TOC refresh, field updates, complex page numbering, or template attachment when explicitly permitted.

When the user confirms Word automation and the document is ready for final field refresh, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/refresh_word_fields.ps1 -InputPath thesis_pre_final.docx -OutputPath thesis_pre_final_refreshed.docx
```

Do not run this silently. It opens Microsoft Word through COM automation, saves a new copy, and writes a `.word-refresh.json` report. Use `-AllowOverwrite` only after explicit overwrite confirmation.

### 5. Save Safely

Default output naming:

- `_formatted`
- `_normalized`
- `_template_applied`
- `_pre_final`

Do not overwrite the only working document unless the user explicitly asks.

## General Baseline When No Template Exists

Use conservative defaults:

- Consistent heading hierarchy.
- Readable body font and line spacing.
- First-line indent for body paragraphs when appropriate.
- Separate Chinese and English abstract sections when required.
- Consistent figure/table caption numbering.
- References formatted consistently in the requested citation style.
- Stable page setup across sections.

State that these are provisional and should be checked against the real handbook before final submission.

## Validation

Before finishing, verify:

- The output file exists and opens when validation is possible.
- Page setup matches the chosen source.
- Heading levels are consistent.
- Captions and cross-references are not obviously broken.
- Bibliography style is consistent.
- The table of contents either is refreshed or is listed as requiring Word refresh.
- Word-only fields, TOC, tables of figures, indexes, and pagination are refreshed or explicitly listed as manual checks.
- No content was unintentionally removed.

## Output Report

Return:

- Source rules used.
- Output file path.
- Formatting changes applied.
- Rule-table items still marked `unresolved` or `needs Word refresh`.
- Items requiring manual Word check.
- Remaining conflicts or missing rule sources.

## Bundled Utilities

- `scripts/docx_style_inventory.py`: no-dependency DOCX style and paragraph-style usage inventory.
- `scripts/docx_apply_basic_styles.py`: conservative `python-docx` baseline formatter for a new output copy; does not refresh Word-only fields.
- `scripts/refresh_word_fields.ps1`: optional Windows/Microsoft Word COM finalization script for TOC, fields, tables of figures, indexes, and repagination. Requires explicit user permission to open Word.

Run scripts only after confirming the target file and output copy. Ask before installing `python-docx`.

## Reference

Read [formatting-rule-checklist.md](references/formatting-rule-checklist.md) when applying a school handbook, Word template, or journal formatting guide.
