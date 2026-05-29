# Writing Input Handoffs

Use this reference before drafting substantial academic text or when consuming outputs from parsing, research verification, figures, formatting, or post-draft review.

Use the canonical cross-skill field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md), while keeping writing-stage decisions in this file.

## Input Handling

| Input | Required handling |
|---|---|
| Verified evidence register | Use only entries marked `verified`, `parsed`, or explicitly user-approved; keep `candidate` items in an evidence gap list |
| Material passport | Respect `data_access_level`, `verification_state`, `allowed_uses`, and restrictions before using an artifact in prose |
| Parsed PDF notes | Preserve source path, page/location, finding, method context, limitation, and citation key |
| Parsed DOCX comments | Convert comments into revision tasks with status, target section, and user-decision flags |
| Formatting guide or required headings | Use only to shape section structure; defer layout and style enforcement to `$academic-formatting-workflow` |
| Figure/table plan | Keep callouts and captions as placeholders until `$academic-figure-workflow` or the user confirms the artifact |
| Post-draft review request | Package complete draft, target standard, benchmark set, evidence register, figures/tables, and unresolved claims for `$post-manuscript-benchmark-review` |
| Literature gap list | Route discovery, DOI checks, and evidence-register updates to `$academic-research-verification`; backfill prose only after verification or user approval |
| Claim anchor list | Preserve support locator, allowed claim strength, and open risk; do not strengthen claims during revision |
| Final polish request | Route broad de-AI or style-polishing work to `$academic-de-ai-polishing` after content, structure, and evidence are stable |

## Evidence Alignment Audit

When a draft contains citation keys and an evidence register is available, run:

```bash
python scripts/audit_evidence_alignment.py --draft chapter_02.md --evidence-register evidence_register.csv --output-csv evidence_alignment_audit.csv --output-md evidence_alignment_audit.md
```

Treat `citation_missing_from_register`, `citation_not_writing_ready`, unresolved `needs evidence`, and unresolved `LIT_GAP` markers as blocking unless the user explicitly approves a provisional draft.

For claim-heavy sections, also check that central claims have anchors or appear in the unresolved claim list.
