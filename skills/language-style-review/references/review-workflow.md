# Language Style Review Workflow

## Modes

| mode | use when | output |
|---|---|---|
| independent_review | user asks only for language, wording, grammar, AI-like phrasing, translation, figure/table text, or citation-sentence style review | review report and candidate rewrites |
| orchestrated_review | orchestrator asks for language review after quality review or as one stage of a project | report plus risk notes for combined prioritization |
| revision_control_handoff | revision-control needs language diagnostics for selected objects or a whole draft | object-level issue table and modification queue |

## Sequence

1. Confirm scope: whole manuscript, chapter, section, paragraph, sentence, translation, figure/table text, or citation wording.
2. Identify available ids: chapter, section, paragraph, sentence, figure/table text object, or line numbers.
3. Read project supplemental standards, terminology list, and problem-word list when paths are provided.
4. Check operation-record residue, project-management traces, prompt traces, TODO markers, and internal workflow language.
5. Diagnose sentence function, ambiguity, terminology, citation expression, bilingual meaning drift, and mechanical cadence.
6. Produce a report using `scoring-and-output-schema.md`.
7. If official editing is requested, return a `$revision-control` queue instead of editing directly.

## Stop And Route

Route away when:

- the user asks whether a complete manuscript is publishable or SCI/Q1 ready: use `$post-manuscript-benchmark-review`;
- the user asks to update the draft, pass/fail sentence status, or round records: use `$revision-control`;
- the text is already approved for final polish and the user wants rewrite execution: use `$academic-de-ai-polishing`;
- a language problem depends on missing evidence, unverifiable references, or literature gaps: hand off to `$revision-control` for upgrade planning and `$academic-research-verification` as needed.

## Combined Review

When the user asks for "quality review plus language review":

1. Run or request full quality review first.
2. Run language-style review second.
3. Identify language suggestions that would undo quality-review priorities or weaken evidence support.
4. Return a unified queue ordered by blocker severity and user-confirmed scope.
