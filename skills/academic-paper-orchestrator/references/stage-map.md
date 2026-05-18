# Academic Paper Stage Map

Use this reference when coordinating a full paper project or resuming work after a pause.

## Project State Fields

Track these fields in a compact project-state note:

| Field | Meaning |
|---|---|
| `paper_type` | review, experimental paper, thesis, dissertation, report, manuscript |
| `language` | English, Chinese, bilingual |
| `target_standard` | school guide, Word template, journal guide, supervisor rule, provisional |
| `materials` | files, links, datasets, code repositories, notes |
| `evidence_status` | missing, candidate, verified, parsed, citation-audited |
| `draft_status` | none, outline, chapter drafts, integrated draft, pre-final |
| `figure_status` | none, planned, drafted, validated, inserted |
| `format_status` | none, baseline captured, normalized, final checked |
| `current_gate` | next user confirmation needed |

## Stage Handoffs

- Research to writing: pass verified evidence register and unresolved items.
- Parsing to research: pass extracted DOI strings, bibliography entries, and source metadata with low-confidence flags.
- Parsing to writing: pass evidence CSV, headings, comments, and extracted notes.
- Writing to figures: pass figure purpose, target section, factual content, and caption intent.
- Writing to formatting: pass stable manuscript version, target guide, figure/table list, and bibliography status.

## Gate Report Template

Use this structure at each human checkpoint:

```text
Completed:
Artifacts:
Needs confirmation:
Risks or missing materials:
Recommended next step:
```

## Narrow Task Shortcut

If the user asks for a narrow task, run only the relevant stage and state what was intentionally skipped. Example: for "format this DOCX", skip literature, parsing, and writing unless required by the formatting guide.
