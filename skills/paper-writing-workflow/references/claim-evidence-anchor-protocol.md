# Claim Evidence Anchor Protocol

Use this reference when drafting, revising, integrating, reviewing, or polishing claims that must remain traceable to evidence.

Use the canonical field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md). This file adds writing-stage behavior and claim-strength rules.

## When To Create Anchors

Create a claim anchor for:

- abstract, introduction, conclusion, and contribution claims;
- method comparison or benchmark claims;
- results, performance, data, code, or experiment claims;
- mechanism, causality, or applicability claims;
- claims that are likely to be reused by figures, review reports, rebuttals, or final polishing.

Do not anchor purely descriptive transitions unless they carry a factual judgment.

## Anchor Fields

```text
claim_anchor_id:
claim_summary:
manuscript_location:
support_type: literature | data | code | result | figure | user_decision
support_locator:
evidence_register_key:
allowed_claim_strength: strong | moderate | cautious | descriptive_only | unresolved
verification_state: verified | parsed | writing_ready | user_approved | unresolved
owner_skill:
open_risk:
```

`support_locator` should be concrete: DOI and page/table/figure, local file path, table ID, script path plus command, result file, figure panel, or explicit user decision.

## Claim Strength Rules

| strength | allowed wording |
|---|---|
| `strong` | Direct conclusion, only when evidence is direct and robust. |
| `moderate` | Supported but bounded by method, sample, dataset, or benchmark scope. |
| `cautious` | Use "suggests", "indicates", "is consistent with", or equivalent cautious wording. |
| `descriptive_only` | State what was observed or reported; do not infer mechanism or superiority. |
| `unresolved` | Do not present as a manuscript claim; mark `LIT_GAP` or remove. |

Never let final polish strengthen a claim beyond its anchor.

## Drafting Use

Before drafting a claim-heavy section:

1. List the central claims.
2. Attach existing anchors or create provisional anchors.
3. Draft only claims with `verified`, `parsed`, `writing_ready`, or `user_approved` support.
4. Mark unsupported claims with `LIT_GAP` and route them to research verification.

## Handoff To Research Verification

When a claim lacks support, pass:

```text
claim_anchor_id:
claim_summary:
manuscript_location:
current_field:
evidence_type_needed:
candidate_search_terms:
minimum_support_needed:
allowed_claim_strength_if_resolved:
```

## Completion Check

Before calling a section complete:

- every central claim has an anchor, verified support, or visible `LIT_GAP`;
- support locations are precise enough for another agent to inspect;
- wording does not exceed `allowed_claim_strength`;
- unresolved anchors are listed in the user-review items.
