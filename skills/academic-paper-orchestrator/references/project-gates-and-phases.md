# Project Gates And Phases

Use this reference for full paper, thesis, dissertation, or long-running manuscript coordination.

## Standard Project Phases

1. Intake and project-state setup.
2. Target and formatting baseline confirmation.
3. Existing material inventory.
4. Research verification plan.
5. PDF/DOCX parsing plan.
6. Research field and terminology baseline confirmation.
7. Paper design document and chapter outline.
8. Outline-level evidence precheck and `LIT_GAP` list.
9. Round-1 verified literature and evidence register.
10. Optional trial section.
11. Chapter-by-chapter drafting.
12. Round-2 gap-driven literature supplementation.
13. Figure and table plan.
14. Integrated manuscript.
15. Citation and bibliography validation.
16. Dedicated quality review or reviewer-comment plan.
17. Final de-AI/style polishing when content is stable.
18. Formatting normalization.
19. Pre-final delivery and version note.

Skip phases only when the user's request is explicitly narrower, and state the skipped scope.

## Required Gates

Stop and wait for confirmation after:

- project design document and chapter outline;
- inferred or unclear research field/terminology baseline;
- outline-level evidence precheck and `LIT_GAP` list;
- initial verified literature/evidence register;
- gap-driven literature supplementation before writing-ready use;
- each chapter draft;
- integrated full draft;
- reviewer/supervisor-comment revision plan before substantial edits;
- benchmark-review plan and benchmark set before judging target readiness when the user asks for post-draft review;
- final de-AI/style polish entry after content, evidence, and structure are stable;
- figure plan when figures are substantial or use an external image-generation API;
- formatting baseline before applying final DOCX normalization;
- pre-final draft after quality review.

At every gate, report:

```text
Completed work:
Artifacts produced:
Decisions needing confirmation:
Risks, missing materials, or unverified claims:
Recommended next step:
```

## Stage Execution Notes

- Inventory: track materials, trusted evidence, unverified items, outputs, and decisions.
- Research: require DOI/title matching or another explicit source trail before trusting a source.
- Parsing: ask `$pdf-docx-parsing-workflow` for structured outputs that writing and formatting can reuse.
- Writing: confirm field/terminology, draft one chapter or section at a time after outline and evidence baseline are clear, and mark unsupported required claims with `LIT_GAP`.
- Evidence gaps: route search, DOI checks, and trust-state changes to `$academic-research-verification`.
- Comment response: use `$paper-writing-workflow` for ordinary revision planning; use `$post-manuscript-benchmark-review` for full-draft benchmark review.
- Final polish: use `$academic-de-ai-polishing` only after content, evidence, and structure are stable.
- Figures: use `$academic-figure-workflow` for nontrivial figures; AI image generation requires explicit confirmation.
- Formatting: use `$academic-formatting-workflow` only after content is reasonably stable.
- Post-draft review: use `$post-manuscript-benchmark-review` only after a complete first draft or integrated chapter exists.

Read [stage-map.md](stage-map.md) for compact stage handoffs and gate report templates.
