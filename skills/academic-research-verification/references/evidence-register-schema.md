# Evidence Register Schema

Use this schema for literature master lists, citation audits, and evidence registers.

## Core Literature Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | Stable local key such as `smith2024battery` |
| `title` | yes | Normalized title |
| `authors` | yes | Short author list or full list if needed |
| `year` | yes | Publication year |
| `venue` | yes | Journal, conference, book, repository, standard body |
| `doi` | no | Required when available |
| `url` | no | Stable source link |
| `source_path` | no | Local PDF or DOCX path |
| `trust_state` | yes | candidate, verified, downloaded, parsed, cited, rejected, unresolved |
| `verification_source` | no | Link or database used to verify identity |
| `intended_use` | no | Claim, section, or chapter |
| `notes` | no | Gaps, doubts, or user decisions |

## Evidence Fields

| Field | Required | Notes |
|---|---|---|
| `evidence_id` | yes | Stable local key |
| `source_id` | yes | Link to core literature field `id` |
| `location` | no | Page, section, table, figure, paragraph |
| `claim_or_finding` | yes | Short paraphrase |
| `method_context` | no | Conditions, sample, method, dataset |
| `limitation` | no | Scope limits or uncertainty |
| `target_chapter` | no | Where this evidence may be used |
| `quote` | no | Keep short and copyright-compliant |
| `verification_state` | yes | verified, unresolved, rejected |

## Audit Lists

Create separate lists when useful:

- DOI mismatch list.
- Duplicate records.
- Uncited bibliography items.
- In-body citations missing bibliography entries.
- Claims with weak or missing support.

## Rules

- Do not move `candidate` sources into writing without a visible warning.
- Keep rejected records with a reason when they were previously considered.
- Do not store long copyrighted passages in the register.
