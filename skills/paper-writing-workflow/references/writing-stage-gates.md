# Writing Stage Gates

Use this reference when diagnosing whether academic writing is ready for outlining, drafting, revision, integration, or polishing.

## Modes

Classify the task:

- `outline`: topic and structure are still forming.
- `section_draft`: one chapter or section needs drafting.
- `revision`: a draft exists and needs stronger logic, evidence, or style.
- `integration`: approved sections need a coherent full manuscript.
- `comment_response`: supervisor, reviewer, committee, or editor comments need analysis before editing.
- `polish`: content is stable and language quality is the main target.

## Stage Gate Report

```text
Mode:
Active gate: plan_only | draft_ready | revision_ready | needs_verification | needs_user_decision
Evidence status:
Allowed work now:
Blocked work:
Next confirmation:
```

Use `plan_only` when evidence, outline, or user decisions are insufficient for drafting. Use `needs_verification` when source authenticity or DOI/citation truth is unresolved and route that work to `$academic-research-verification`.

Stop for confirmation before drafting substantial body text from a new paper design document or chapter outline.

## Required Writing Gates

- Field/terminology gate: confirm the research field when it is inferred or unclear; if the user still does not set a field, proceed with `computer and electronic information` as a provisional fallback.
- Evidence precheck gate: before substantive drafting, classify core claims and identify unsupported claims that need `LIT_GAP`.
- Draft gate: stop after each major section or chapter draft for user confirmation.
- Detailed design gate: after material preparation and before formal drafting, confirm target venue, article type, chapter/section tasks, expected word counts, evidence needs, figure/table plan, risks, and missing materials.
- Comment-response gate: when comments are substantial, present the revision plan before editing.
- Revision-control gate: after an initial full draft, route formal sentence-level revision state, pass/fail confirmation, latest review drafts, and round logs to `$revision-control`.
- Final-polish gate: enter style polishing only after structure, evidence, and claim strength are stable; route heavy de-AI polishing to `$academic-de-ai-polishing`.
