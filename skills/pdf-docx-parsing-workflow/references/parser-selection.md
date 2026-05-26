# Parser Selection

Use this reference when choosing how to parse PDF or DOCX files and whether to request dependency, OCR, or Word automation approval.

## PDF

Prefer:

- PyMuPDF for text and page-level extraction when available.
- `scripts/pdf_table_ocr_inventory.py` when table extraction, scanned pages, or recovery reporting matter.
- `pdfplumber` as a table fallback when available.
- OCR only after user approval when the PDF is scanned or extraction is unusable.

## DOCX

Prefer:

- standard ZIP/XML inspection for headings, comments, styles, captions, and tracked-change metadata;
- `python-docx` when paragraph and table content are needed and the dependency is available;
- Word automation only for Word-specific field behavior and only after user approval.

## Approval Gates

Ask before:

- installing or upgrading parser dependencies;
- running OCR, cloud OCR, or image-based extraction;
- using Word automation or opening DOCX files in Word;
- parsing password-protected, restricted, sensitive, or third-party documents in a way that may violate access rules.

Use:

```text
Decision needed:
Affected files:
Reason:
Options:
Risk if skipped:
Downstream impact:
```
