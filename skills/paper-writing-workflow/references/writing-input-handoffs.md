# Writing Input Handoffs

Use this reference before drafting substantial academic text or when consuming outputs from parsing, research verification, figures, formatting, or post-draft review.

## Input Handling

| Input | Required handling |
|---|---|
| Verified evidence register | Use only entries marked `verified`, `parsed`, or explicitly user-approved; keep `candidate` items in an evidence gap list |
| Parsed PDF notes | Preserve source path, page/location, finding, method context, limitation, and citation key |
| Parsed DOCX comments | Convert comments into revision tasks with status, target section, and user-decision flags |
| Formatting guide or required headings | Use only to shape section structure; defer layout and style enforcement to `$academic-formatting-workflow` |
| Figure/table plan | Keep callouts and captions as placeholders until `$academic-figure-workflow` or the user confirms the artifact |
| Post-draft review request | Package complete draft, target standard, benchmark set, evidence register, figures/tables, and unresolved claims for `$post-manuscript-benchmark-review` |

## Evidence Alignment Audit

When a draft contains citation keys and an evidence register is available, run:

```bash
python scripts/audit_evidence_alignment.py --draft chapter_02.md --evidence-register evidence_register.csv --output-csv evidence_alignment_audit.csv --output-md evidence_alignment_audit.md
```

Treat `citation_missing_from_register`, `citation_not_writing_ready`, and unresolved `needs evidence` markers as blocking unless the user explicitly approves a provisional draft.
