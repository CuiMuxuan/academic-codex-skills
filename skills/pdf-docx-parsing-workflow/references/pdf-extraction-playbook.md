# PDF Extraction Playbook

Use this reference for PDF text, table, bibliography, figure/table mention, and scanned-page recovery tasks.

## Inventory Fields

Record:

- file path;
- file type;
- size;
- page count when available;
- likely role: source paper, thesis draft, template, review file, appendix, or unknown.

## Extraction Fields

For each page or extracted unit, capture:

- page number;
- section-like heading if detectable;
- text snippet or evidence statement;
- table cells and table extraction method when table extraction is requested;
- table or figure mentions;
- reference entries when requested;
- extraction quality;
- notes about missing, scanned, garbled, or low-confidence areas.

## Quality Review

Check:

- empty or very short extraction;
- garbled encoding;
- missing pages or sections;
- tables flattened beyond usefulness;
- scanned pages requiring OCR approval;
- failed zones that need manual recovery.

Create `manual_recovery_list.md` when extraction is incomplete.
