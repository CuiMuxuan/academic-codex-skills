# Trust State Decision Gates

Use this reference when changing a literature record's trust state or deciding whether a source is writing-ready.

## Trust States

| State | Meaning |
|---|---|
| `candidate` | Found or provided, not yet verified |
| `verified` | Bibliographic identity is confirmed |
| `downloaded` | Full text is available locally or lawfully accessible |
| `parsed` | Full text or key evidence has been extracted |
| `cited` | Used in the manuscript body |
| `rejected` | Duplicate, irrelevant, mismatched, retracted, or unreliable |
| `unresolved` | Cannot be confirmed with available access |

## Promotion Gates

| Decision | Required evidence |
|---|---|
| `candidate` -> `verified` | Title, year, venue, and author identity match an authoritative source; DOI resolves to the same work when a DOI exists |
| `verified` -> `downloaded` | Lawful full text or user-provided PDF is available locally or through a stable access path |
| `downloaded` -> `parsed` | Specific evidence locations or summaries have been extracted with source location and quality notes |
| any state -> `rejected` | Clear reason such as mismatch, duplicate, irrelevance, retraction, source unreliability, or user rejection |
| any state -> `unresolved` | Required metadata or source access is missing after reasonable checking |

Only change a record's trust state when the evidence for the change is visible in the register.

## Stop And Ask

Stop and ask before:

- accepting a source with no DOI when the venue or metadata is weak;
- repairing a DOI/title mismatch by choosing a replacement record;
- keeping a suspicious source because it appears important to the manuscript;
- using paywalled, manually supplied, or user-exported metadata as the only verification source;
- moving `candidate` or `unresolved` items into a writing-ready evidence set.

Use this checkpoint:

```text
Record:
Current state:
Proposed state:
Evidence for change:
Unresolved risk:
User decision needed:
```

Set `writing-ready` to `yes` only when the source is verified and the relevant evidence is located or explicitly approved for the target writing task.
