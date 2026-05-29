# Literature Gap And Evidence Precheck

Use this reference during outline planning, drafting, revision, and polishing whenever a claim needs more support than the current materials provide.

Use the canonical `lit_gap` and writing-ready handoff field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md).

## Evidence Precheck

Before drafting from an outline, inspect each core claim and mark whether it is:

- factual judgment;
- mechanism or causal judgment;
- engineering applicability judgment;
- route or method comparison;
- evidence-quality or reporting-standard judgment;
- conclusion-like synthesis;
- descriptive text that can be drafted without external support.

For every claim that needs support, record whether verified evidence, data, code output, or user-approved material is already available.

For central claims, contribution claims, result claims, benchmark comparisons, and code/data/experiment claims, also create or update a claim anchor using [claim-evidence-anchor-protocol.md](claim-evidence-anchor-protocol.md).

## Gap Marker

When support is missing, insert a marker rather than inventing citations:

```markdown
<!-- LIT_GAP:[field/evidence_type] brief description of required support -->
(This part should be completed after the needed literature or data is supplied.)
```

Use `field/evidence_type` values such as:

- `biomed/review`
- `materials/experiment`
- `cs/benchmark`
- `education/policy`
- `general/method-comparison`

## Drafting Behavior

- Skip the unsupported claim or paragraph after inserting the marker.
- Continue drafting adjacent sections that have enough support.
- Do not insert fake citation keys or placeholder DOIs.
- If a paragraph's main point is unsupported, draft only a neutral bridge or leave the marker.
- If the claim is optional, consider deleting it instead of marking it.

## Gap List

At the end of the draft or plan, list unresolved gaps:

| id | location | claim needing support | evidence type needed | suggested search/download target | blocks drafting? |
|---|---|---|---|---|---|

Recommend concrete material types, not fabricated references. Examples:

- recent review paper on the field-level trend;
- primary experimental study supporting a mechanism;
- benchmark paper using the target dataset;
- official reporting guideline or standard;
- user's own result table or analysis script output.

## Handoff To Research Verification

Route unresolved literature gaps to `$academic-research-verification` when the task is source discovery, DOI verification, or evidence-register update.

Handoff packet:

```text
claim_anchor_id:
LIT_GAP id:
Target claim:
Field and target venue:
Evidence type:
Candidate search terms:
Required recency or source type:
How the evidence will be used in the manuscript:
Minimum support needed:
Allowed claim strength if resolved:
```

Only after the new source is verified or user-approved should the gap be backfilled into prose.
