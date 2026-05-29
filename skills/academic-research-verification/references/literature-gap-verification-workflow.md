# Literature Gap Verification Workflow

Use this reference when `$paper-writing-workflow` or `$academic-paper-orchestrator` passes `LIT_GAP`, 待补证据, or an evidence-gap list.

Use the canonical `lit_gap` and writing-ready handoff field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md).

## Intake

For each gap, capture:

```text
Claim anchor id:
LIT_GAP id:
Target claim:
Current field:
Target venue/school field:
Evidence type needed:
Manuscript location:
Preferred recency/source type:
Existing candidate sources:
How the evidence will be used:
Minimum support needed:
Allowed claim strength if resolved:
```

If the target claim is too broad, split it into smaller verifiable claims before searching.

## Search And Verification

1. Translate the target claim into 2-4 search strings.
2. Identify candidate source types: review, primary study, benchmark paper, dataset paper, standard/guideline, method paper, or user data.
3. Search or inspect provided sources.
4. Verify identity with DOI/title/author/year/venue agreement when possible.
5. Apply trust-state gates before marking a source writing-ready.
6. Extract only the finding needed for the manuscript, with location and limitation.

Do not treat a convenient source as adequate if it does not support the exact claim.

## Download Or User Material Gate

If a source is useful but inaccessible:

- provide title, DOI or stable link, venue, year, and why it is needed;
- ask the user to download, attach, or provide the relevant pages;
- mark the source `candidate` or `unresolved`, not writing-ready.

If the evidence requires user data or a new analysis, state the needed table, figure, script output, or experiment instead of searching literature.

## Output: Gap Resolution Report

| gap id | target claim | status | verified source or needed material | evidence use | limitation | next action |
|---|---|---|---|---|---|---|

Status values:

- `resolved_verified`
- `candidate_needs_download`
- `candidate_needs_user_decision`
- `requires_user_data_or_analysis`
- `unresolved_search_more`
- `delete_or_soften_claim`

## Writing-Ready Handoff

Only for verified or explicitly user-approved evidence:

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

Route back to `$paper-writing-workflow` for prose backfill after this handoff is complete.
