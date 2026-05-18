---
name: pdf-docx-parsing-workflow
description: "Parse, inspect, and structure academic PDF and DOCX files for papers, theses, dissertations, review articles, supervisor comments, formatting templates, and evidence extraction. Use when the user needs PDF text/table extraction, DOCX heading inventory, comments, tracked changes, style inspection, bibliography extraction, evidence CSVs, or conversion of documents into reusable structured notes. Chinese triggers: 解析PDF, 解析DOCX, 提取论文证据, Word批注, 修订痕迹, 文档结构化, PDF文献解析."
---

# PDF DOCX Parsing Workflow

Use this skill to turn PDFs and DOCX files into structured, traceable material for research verification, writing, formatting, and figure planning.

## Boundaries

Do:

- Extract document structure and reusable evidence.
- Preserve page, heading, paragraph, comment, and revision context when possible.
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
6. Do not install dependencies without user approval.
7. Do not overwrite source documents.

## Intake

Identify:

- Input file paths or folders.
- Purpose: evidence extraction, heading inventory, comments, tracked changes, formatting template inspection, bibliography extraction, or table extraction.
- Target examples: 3-10 approved target PDFs/DOCX files or templates when parsing is meant to infer structure, style, or evidence density.
- Output format: CSV, JSON, Markdown, or a compact report.
- Whether OCR is needed or allowed.
- Whether external dependencies can be installed if missing.

If target examples are missing, parse the provided files using the generic structured schema and mark inferred structure/style assumptions as provisional.

Before parsing files, ask for missing materials that would materially improve extraction quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for input PDFs/DOCX files, target examples, parsing purpose, expected output schema, OCR permission, dependency-install permission, password/access information, sensitivity constraints, and downstream target skill as relevant. If unavailable, run only safe local inventory or produce a manual recovery plan after user confirmation.

## Parsing Checkpoints

Stop and ask for confirmation before:

- Installing or upgrading parser dependencies.
- Running OCR, cloud OCR, or image-based extraction.
- Using Word automation or opening DOCX files in Word.
- Treating `low` or `failed` extraction zones as usable evidence.
- Passing parsed bibliography metadata to writing as verified literature.
- Parsing password-protected, restricted, sensitive, or third-party documents in a way that may violate access rules.

Use this checkpoint format:

```text
Decision needed:
Affected files:
Reason:
Options:
Risk if skipped:
Downstream impact:
```

## Workflow

### 1. Inventory

List:

- File path.
- File type.
- Size.
- Page count or document-part count when available.
- Likely role: source paper, thesis draft, template, review file, appendix, or unknown.

### 2. Choose Parser

PDF:

- Prefer PyMuPDF when available for text and page-level extraction.
- Use `scripts/pdf_table_ocr_inventory.py` when table extraction, scanned pages, or recovery reporting matter.
- Use pdfplumber as a table fallback when it is available.
- Use OCR only after user approval when the PDF is scanned or extraction is unusable.

DOCX:

- Prefer standard ZIP/XML inspection for headings, comments, styles, and tracked-change metadata.
- Use `python-docx` when available for paragraph and table content.
- Use Word automation only for Word-specific field behavior and only after user approval.

### 3. Extract

For PDFs, capture:

- Page number.
- Section-like heading if detectable.
- Text snippet or evidence statement.
- Table cells and table extraction method when table extraction is requested.
- Table or figure mentions.
- Reference entries when requested.
- Extraction quality.

For DOCX, capture:

- Heading hierarchy.
- Paragraph index.
- Paragraph style.
- Table count and rough location.
- Figure/table captions.
- Comments and authors when available.
- Tracked insertions/deletions when available.
- Section/page setup signals when inspecting templates.

### 4. Normalize Outputs

Use stable fields:

- `source_path`
- `source_type`
- `location`
- `heading`
- `content_type`
- `text`
- `metadata`
- `quality`
- `notes`

For evidence extraction, add:

- `claim_or_finding`
- `method_context`
- `limitation`
- `target_chapter`
- `citation_key`
- `verification_state`

### 5. Quality Review

Check:

- Empty or very short extraction.
- Garbled encoding.
- Missing pages or sections.
- Tables flattened beyond usefulness.
- DOCX comments not captured.
- Tracked changes hidden in XML but not summarized.

Create a manual recovery list for failed zones.

Before handing outputs to another skill, apply these gates:

| Target skill | Handoff gate |
|---|---|
| `$academic-research-verification` | Send extracted DOI strings, bibliography entries, and metadata with `quality` and `verification_state=candidate`; do not mark as verified |
| `$paper-writing-workflow` | Send only `high` or `medium` evidence by default; include `low` evidence only in an evidence-gap or manual-review list |
| `$academic-formatting-workflow` | Send template/style/page-setup signals with `quality` and `notes`; do not claim formatting compliance |
| `$academic-figure-workflow` | Send figure/table captions or extracted figure references as planning inputs, not as confirmed visual assets |

## Outputs

Use one or more:

- `document_inventory.md`.
- `pdf_evidence.csv`.
- `docx_structure.csv`.
- `docx_comments.csv`.
- `tracked_changes_report.md`.
- `format_template_inventory.md`.
- `manual_recovery_list.md`.

## Bundled Utilities

- `scripts/pdf_text_inventory.py`: PyMuPDF-based page-level PDF text inventory. Requires PyMuPDF and user approval before installing it.
- `scripts/pdf_table_ocr_inventory.py`: PyMuPDF-based page text plus table extraction and optional OCR recovery report; can fall back to pdfplumber for tables when installed. Requires user approval before OCR or dependency installation.
- `scripts/docx_inventory.py`: no-dependency DOCX heading, style, caption, comment, and tracked-change inventory helper.
- `scripts/make_evidence_register.py`: create an empty evidence register CSV with the standard fields.

Run scripts only when they fit the user's files and environment. Patch or replace them if the local project needs a more specific parser.

## Reference

Read [structured-output-schema.md](references/structured-output-schema.md) before creating CSV/JSON outputs or when coordinating parsed material with research and writing skills.
