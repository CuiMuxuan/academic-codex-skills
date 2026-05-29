# Dependency And Software Guide

Use this reference during project intake, before file conversion, before figure generation, and whenever a stage needs tools that may not exist on the user's machine.

## Principle

Do not install dependencies silently. Detect what is available, explain what is missing, ask for confirmation before installation, and offer a lower-risk fallback when possible.

## Common Tools

| stage | useful tools | use | fallback when missing |
|---|---|---|---|
| Literature verification | browser/network access, Crossref/OpenAlex/Semantic Scholar/PubMed APIs | DOI/title/source identity checks | manual verification queue with exact search strings |
| PDF parsing | PyMuPDF, pdfplumber, pypdf, Poppler, OCR tools | page inventory, table extraction, scanned-page recovery | low-confidence manual recovery list |
| DOCX parsing/formatting | python-docx, zipfile/OOXML inspection, Microsoft Word COM on Windows | style inventory, comments, field refresh, TOC/caption updates | save unrefreshed copy and list Word-only checks |
| Markdown to DOCX | Pandoc, citeproc, CSL/BibTeX/BibLaTeX, MathML/OMML support | LaTeX-readable formulas, citations, references, cross-references | validate Markdown risks and ask user to install Pandoc |
| Figures | Matplotlib, draw.io/diagrams.net CLI, Inkscape, Graphviz, CairoSVG, Pillow | SVG/PNG/PDF export, draw.io rendering, diagram conversion | provide editable source/specification only |
| Data/result claims | Python scientific stack, project scripts, notebooks, CSV/Parquet readers | inspect result provenance and reproducibility | mark claim as unresolved or ask for result tables |
| Final packaging | Word, PDF export tools, image metadata tools | final DOCX/PDF checks, figure package QA | manual packaging checklist |

## Intake Prompt

When a stage may need unavailable software, report:

```text
Likely tools needed:
Already available:
Missing or unknown:
Why they matter:
Can proceed without them: yes/no
Fallback:
User confirmation needed:
```

## Installation Guidance

- Ask before installing Python packages, system packages, OCR tools, Pandoc, draw.io CLI, Inkscape, or Word automation helpers.
- Prefer project-local or user-approved environments over global installs.
- If the user declines installation, continue only with a clearly marked fallback.
- Never claim a DOCX, PDF, figure package, citation audit, or generated image is final when the required tool-specific check was skipped.

## Verification Hooks

Use repository-level maintenance scripts when working inside this skills repository:

```powershell
python scripts/validate_markdown_docx_package.py --help
python scripts/figure_package_check.py --help
python scripts/audit_claim_anchors.py --help
```

These scripts are not installed into global `.codex`; they are development and QA tools for this repository.
