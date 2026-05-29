# Material Passport Schema

Use this reference when coordinating long-running projects or passing materials between parsing, research, writing, figures, review, polishing, and formatting.

This file is a skill-local execution guide. The canonical shared field names live in [handoff-field-schema.md](../../../shared/handoff-field-schema.md).

A material passport is a compact record of what an artifact is, how trustworthy it is, how it may be used, and which workflow stage owns it.

## Required Fields

```text
material_id:
artifact_type: draft | pdf | bibliography | evidence_register | dataset | code | result_table | figure | template | comment_set | benchmark | other
path_or_source:
stage_owner:
data_access_level: raw | redacted | verified_only
task_type: open_ended | outcome_gradable
verification_state: unknown | candidate | verified | parsed | writing_ready | rejected | unresolved
allowed_uses:
restrictions:
source_trail:
related_lit_gap_ids:
related_claim_anchor_ids:
handoff_status: missing | candidate | ready | blocked | complete
user_decisions:
notes:
```

## Access Levels

| level | meaning | allowed use |
|---|---|---|
| `raw` | Original draft, PDF text, dataset, code output, comments, or other unfiltered material | Use only in the owning stage or with explicit user permission; keep limitations visible |
| `redacted` | Sensitive, answer-bearing, or irrelevant parts removed | Use for review, planning, or external-style comparison when raw access could bias judgment |
| `verified_only` | Only identity-checked sources, extracted findings, confirmed results, or approved claims | Preferred input for writing, final review, polishing, and formatting |

Use `verified_only` for writing-ready evidence whenever possible. If only `raw` or `redacted` material is available, show what is not yet verified.

## Task Types

| task_type | use when | discipline |
|---|---|---|
| `open_ended` | drafting, synthesis, conceptual figure design, review judgment | Record assumptions and evidence limits |
| `outcome_gradable` | DOI checks, citation audits, formatting checks, code/result consistency, conversion validation | Keep the expected output, checker, or acceptance criterion explicit |

## Handoff Rules

- Every handoff packet should cite one or more material passports.
- Writing may use a source as evidence only when `verification_state` is `verified`, `parsed`, `writing_ready`, or explicitly approved by the user.
- Benchmark review must state whether benchmark material is full text, abstract-only, metadata-only, or user-supplied.
- Formatting must know which manuscript version, figure files, bibliography, and template are current.
- If a material passport conflicts with visible files or user instructions, stop and ask which source is authoritative.

## Minimal Passport Table

| material_id | artifact_type | path_or_source | access | verification_state | allowed_uses | owner | status |
|---|---|---|---|---|---|---|---|
| M1 | evidence_register | `evidence_register.csv` | verified_only | writing_ready | draft/review/citation audit | research | ready |
