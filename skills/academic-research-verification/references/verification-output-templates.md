# Verification Output Templates

Use these templates when creating audit outputs or manual queues.

Use the canonical cross-skill field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md).

## Target Exemplar Intake

Ask whether the user can provide 3-10 target papers, approved theses, or accepted manuscripts from the intended field/outlet. Use them only to infer expected source types, recency range, citation style, and evidence density; do not treat their references as verified until checked.

## Manual Verification Queue

| id | raw citation | DOI | title | check needed | search string | expected source | status |
|---|---|---|---|---|---|---|
| local key | pasted entry | missing/provided | normalized | DOI/title/year/venue | exact query | Crossref/publisher/database | pending |

## DOI Mismatch Report

| id | supplied DOI | supplied title | resolved title | mismatch type | proposed action | user decision |
|---|---|---|---|---|---|
| local key | DOI | title | Crossref/publisher title | title/year/venue/author | reject/search/ask user | needed |

## Citation Audit Report

| issue | in-body key | bibliography key | location | action |
|---|---|---|---|---|
| missing bibliography | author-year | none | paragraph/section | add source or remove citation |

## Literature Gap Resolution Report

| gap id | claim anchor id | target claim | status | source/material | evidence use | limitation | allowed claim strength | next action |
|---|---|---|---|---|---|---|---|---|
| LIT_GAP-001 | C1 | claim needing support | resolved_verified/candidate_needs_download/requires_user_data_or_analysis/unresolved_search_more/delete_or_soften_claim | DOI/link/file needed | how it supports writing | scope limit | cautious/moderate/strong | backfill/search/ask user |

## Writing-Ready Evidence Handoff

```text
Claim anchor id:
LIT_GAP id:
Claim supported:
Recommended citation key:
Source identity:
Evidence location:
Finding to use:
Method/context:
Limitation:
Target manuscript location:
Allowed claim strength:
Verification state:
```

## Claim Anchor Audit Hook

When a writing workflow provides claim anchors, make the evidence register auditable by including `claim_anchor_id`, `verification_state`, and `allowed_claim_strength`. In this repository, `scripts/audit_claim_anchors.py` can be used as a maintenance smoke test for that handoff.
