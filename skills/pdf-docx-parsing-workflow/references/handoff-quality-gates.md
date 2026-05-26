# Handoff Quality Gates

Use this reference before passing parsed material to research verification, writing, formatting, or figure planning.

## Normalized Output Fields

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

## Downstream Gates

| Target skill | Handoff gate |
|---|---|
| `$academic-research-verification` | Send extracted DOI strings, bibliography entries, and metadata with `quality` and `verification_state=candidate`; do not mark as verified |
| `$paper-writing-workflow` | Send only `high` or `medium` evidence by default; include `low` evidence only in an evidence-gap or manual-review list |
| `$academic-formatting-workflow` | Send template/style/page-setup signals with `quality` and `notes`; do not claim formatting compliance |
| `$academic-figure-workflow` | Send figure/table captions or extracted figure references as planning inputs, not as confirmed visual assets |

Do not treat parsed bibliography metadata as verified literature identity. Route DOI/title checks to `$academic-research-verification`.
