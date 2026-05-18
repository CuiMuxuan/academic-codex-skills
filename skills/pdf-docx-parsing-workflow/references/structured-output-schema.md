# Structured Output Schema

Use this schema when exporting parsed PDF or DOCX content.

## Document Inventory

| Field | Notes |
|---|---|
| `source_path` | Original file path |
| `source_type` | pdf, docx, template, unknown |
| `role` | source paper, thesis draft, review file, template, appendix |
| `size_bytes` | File size |
| `page_or_part_count` | PDF pages or DOCX body/table/comment counts |
| `parse_status` | pending, parsed, partial, failed |
| `notes` | Warnings or next actions |

## Parsed Content

| Field | Notes |
|---|---|
| `source_path` | Original file path |
| `source_type` | pdf or docx |
| `location` | Page, paragraph index, heading path, table index, comment id |
| `heading` | Nearest heading if known |
| `content_type` | paragraph, heading, table, caption, comment, revision, reference |
| `text` | Extracted text or concise summary |
| `metadata` | JSON-like compact metadata if needed |
| `quality` | high, medium, low, failed |
| `notes` | Recovery notes or uncertainty |

## Evidence Extension

Add these fields when the output feeds academic writing:

| Field | Notes |
|---|---|
| `claim_or_finding` | Paraphrased evidence |
| `method_context` | Conditions, dataset, method, population |
| `limitation` | Scope and uncertainty |
| `target_chapter` | Suggested destination |
| `citation_key` | Local source key |
| `verification_state` | candidate, verified, unresolved |

## Quality Labels

- `high`: clean extraction and source location preserved.
- `medium`: readable but layout or metadata may be imperfect.
- `low`: usable only for manual review.
- `failed`: extraction did not produce reliable content.
