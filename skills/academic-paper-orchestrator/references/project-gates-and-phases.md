# Project Gates And Phases

Use this reference for full paper, thesis, dissertation, or long-running manuscript coordination.

## Standard Project Phases

1. Intake and project-state setup.
2. Target and formatting baseline confirmation.
3. Existing material inventory.
4. Research verification plan.
5. PDF/DOCX parsing plan.
6. Paper design document and chapter outline.
7. Round-1 verified literature and evidence register.
8. Optional trial section.
9. Chapter-by-chapter drafting.
10. Round-2 gap-driven literature supplementation.
11. Figure and table plan.
12. Integrated manuscript.
13. Citation and bibliography validation.
14. Formatting normalization.
15. Dedicated quality review.
16. Pre-final delivery and version note.

Skip phases only when the user's request is explicitly narrower, and state the skipped scope.

## Required Gates

Stop and wait for confirmation after:

- project design document and chapter outline;
- initial verified literature/evidence register;
- each chapter draft;
- integrated full draft;
- benchmark-review plan and benchmark set before judging target readiness when the user asks for post-draft review;
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
- Writing: draft one chapter or section at a time after outline and evidence baseline are clear.
- Figures: use `$academic-figure-workflow` for nontrivial figures; AI image generation requires explicit confirmation.
- Formatting: use `$academic-formatting-workflow` only after content is reasonably stable.
- Post-draft review: use `$post-manuscript-benchmark-review` only after a complete first draft or integrated chapter exists.

Read [stage-map.md](stage-map.md) for compact stage handoffs and gate report templates.
