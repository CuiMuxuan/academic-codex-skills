# Final Polish Boundary

Use this reference when a user asks for polishing, de-AI rewriting, or style improvement and the manuscript may still have unresolved evidence, structure, or claim-strength problems.

Use the canonical `claim_anchor` field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md) when checking central claims during final polish.

## Enter Final Polish Only When

- the section purpose is known;
- the paragraph role is clear;
- core claims are fixed or explicitly marked for softening;
- claim anchors and allowed claim strength are available for central claims, or the rewrite stays conservative and marks verification needs;
- citations and citation boundaries are fixed;
- terminology is confirmed for the current field and target venue;
- unresolved `LIT_GAP` or `needs evidence` markers are not being hidden by rewrite;
- the user wants language refinement rather than new evidence, new structure, or new analysis.

If these conditions are not met, route back to `$paper-writing-workflow`, `$academic-research-verification`, `$post-manuscript-benchmark-review`, or `$revision-control`.

If the user asks for diagnosis without rewrite, route to `$language-style-review`.

If the user asks to manage sentence pass/fail status, round state, latest drafts, or object-library changes, route to `$revision-control`.

## What Polish May Do

- reduce repetitive cadence;
- remove formulaic transitions;
- replace generic filler with precise field-appropriate wording;
- improve paragraph flow while preserving logic;
- remove internal project notes, operation logs, prompt traces, and draft-management residue;
- soften overclaims when evidence boundaries are visible.

## What Polish Must Not Do

- add new facts, citations, results, methods, or conclusions;
- make the claim stronger than the evidence allows;
- exceed the allowed claim strength recorded in a claim anchor;
- erase uncertainty that the manuscript needs;
- hide literature gaps or missing data;
- import impressive but field-inappropriate terminology;
- turn a project log into a paper by inventing missing argument structure.

## Handoff From Writing

Expected handoff:

```text
Stable text:
Section role:
Paragraph role:
Fixed claims:
Claim anchors:
Fixed citations:
Do-not-change terms:
Unresolved evidence gaps:
Allowed edit intensity:
```

If the handoff is missing, keep edits conservative and list user-review items.

## Claim Strength Audit Hook

When polishing a claim-heavy section, run or emulate the claim-anchor audit before and after editing. In this repository, `scripts/audit_claim_anchors.py` can check that central claim anchors still have writing-ready evidence and allowed claim strength.
