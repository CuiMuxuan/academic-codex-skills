---
name: pdf-docx-parsing-workflow
description: "Parse, inspect, and structure academic PDF and DOCX files for papers, theses, dissertations, review articles, supervisor comments, formatting templates, and evidence extraction. Use when the user needs PDF text/table extraction, DOCX heading inventory, comments, tracked changes, style inspection, bibliography extraction, evidence CSVs, or conversion of documents into reusable structured notes. Chinese triggers: 解析PDF, 解析DOCX, 提取论文证据, Word批注, 修订痕迹, 文档结构化, PDF文献解析."
---

# PDF DOCX Parsing Workflow

Use this skill to turn PDFs and DOCX files into structured, traceable material for research verification, writing, formatting, and figure planning.

## Boundaries

Do:

- Extract document structure and reusable evidence.
- Preserve page, heading, paragraph, comment, style, and revision context when possible.
- Produce structured outputs for downstream skills.
- Identify failed or low-confidence extraction zones.

Do not:

- Treat extracted metadata as verified literature identity; route DOI/title checks to `$academic-research-verification`.
- Rewrite the manuscript as the primary task; route writing to `$paper-writing-workflow`.
- Apply final formatting; route to `$academic-formatting-workflow`.
- Generate figures; route to `$academic-figure-workflow`.

## Core Rules

1. Inventory files before parsing.
2. Keep extracted text tied to source path and page or document location.
3. Mark extraction quality and uncertainty.
4. Prefer structured outputs over long raw dumps.
5. Use the least fragile parser that works in the environment.
6. Do not install dependencies, run OCR, or use Word automation without user approval.
7. Do not overwrite source documents.

## Intake

Identify input paths, parsing purpose, target examples, output format, OCR needs, dependency constraints, password/access constraints, sensitivity constraints, and downstream target skill.

Before parsing files, ask for missing materials that would materially improve extraction quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

If materials are unavailable, run only safe local inventory or produce a manual recovery plan after user confirmation.

## Parsing Checkpoints

Stop and ask before installing dependencies, running OCR, using Word automation, treating `low` or `failed` extraction zones as usable evidence, passing bibliography metadata as verified literature, or parsing restricted/sensitive documents in a questionable way.

Use [parser-selection.md](references/parser-selection.md) for parser choice and checkpoint format.

## Workflow

1. Inventory files and their likely roles.
2. Choose the parser using [parser-selection.md](references/parser-selection.md).
3. For PDFs, apply [pdf-extraction-playbook.md](references/pdf-extraction-playbook.md).
4. For DOCX files, apply [docx-extraction-playbook.md](references/docx-extraction-playbook.md).
5. Normalize outputs with [structured-output-schema.md](references/structured-output-schema.md).
6. Apply [handoff-quality-gates.md](references/handoff-quality-gates.md) before routing outputs downstream.

## Outputs

Use one or more:

- `document_inventory.md`;
- `pdf_evidence.csv`;
- `docx_structure.csv`;
- `docx_comments.csv`;
- `tracked_changes_report.md`;
- `format_template_inventory.md`;
- `manual_recovery_list.md`.

## Reference

Read [structured-output-schema.md](references/structured-output-schema.md) before creating CSV/JSON outputs or coordinating parsed material with research and writing skills.

Read [parser-selection.md](references/parser-selection.md) when choosing PDF/DOCX parsers, OCR, dependencies, or Word automation.

Read [pdf-extraction-playbook.md](references/pdf-extraction-playbook.md) for PDF text, table, bibliography, and scanned-page recovery extraction.

Read [docx-extraction-playbook.md](references/docx-extraction-playbook.md) for DOCX headings, comments, tracked changes, styles, captions, and template inspection.

Read [handoff-quality-gates.md](references/handoff-quality-gates.md) before passing parsed outputs to research, writing, formatting, or figure workflows.

## Bundled Utilities

- `scripts/pdf_text_inventory.py`: PyMuPDF-based page-level PDF text inventory. Requires PyMuPDF and user approval before installing it.
- `scripts/pdf_table_ocr_inventory.py`: PyMuPDF-based page text plus table extraction and optional OCR recovery report; can fall back to pdfplumber for tables when installed. Requires user approval before OCR or dependency installation.
- `scripts/docx_inventory.py`: no-dependency DOCX heading, style, caption, comment, and tracked-change inventory helper.
- `scripts/make_evidence_register.py`: create an empty evidence register CSV with the standard fields.
