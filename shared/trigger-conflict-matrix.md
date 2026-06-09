# Trigger Conflict Matrix

Use this matrix when a user request could trigger more than one academic skill. Prefer the owner skill for execution and use the other skill only as an upstream or downstream handoff.

## Conflict Rules

| user request | owner skill | route away when |
|---|---|---|
| "write", "draft", "revise section", "outline", "introduction logic" | `paper-writing-workflow` | evidence identity is missing, then route gaps to `academic-research-verification` |
| "polish", "de-AI", "remove project-log traces" | `academic-de-ai-polishing` | content, citations, structure, or claim strength are unstable, then route to writing or verification |
| "language review", "wording check", "grammar", "AI-like phrasing", "translation accuracy", "figure/table wording", "citation sentence style" | `language-style-review` | user asks to write official changes or maintain sentence state, then route to `revision-control` |
| "sentence-level revision", "逐句修改", "pass/fail sentence confirmation", "revision round", "object library", "latest full review draft" | `revision-control` | the task is only diagnosis with no state updates, then route to `language-style-review`; literature evidence gaps route through research verification |
| "review against benchmarks", "SCI/Q1 readiness", "next-version plan" | `post-manuscript-benchmark-review` | no complete draft exists, then route to writing or orchestrator |
| "multiple reviewer/supervisor comments", "revision action plan", "rebuttal plan" | `paper-writing-workflow` or `post-manuscript-benchmark-review` | use post-review when a complete draft must be judged against benchmarks; otherwise use writing |
| "find papers", "verify DOI", "citation authenticity", "resolve LIT_GAP" | `academic-research-verification` | task asks to write prose from verified sources, then route to writing |
| "parse PDF/DOCX", "extract comments", "structured notes" | `pdf-docx-parsing-workflow` | user asks for scholarly interpretation or writing, then hand off parsed output |
| "format DOCX", "Word template", "Markdown to DOCX" | `academic-formatting-workflow` | content is still changing, then route to writing before final formatting |
| "formula, superscript/subscript, citation, cross-reference conversion" | `academic-formatting-workflow` | the issue is inside figure source/export, then hand off to figure workflow |
| "draw figure", "draw.io", "SVG", "Nature-style Matplotlib" | `academic-figure-workflow` | figure factual content is unclear, then route to writing or verification for figure argument |
| "full thesis workflow", "paper project management", "which skill should handle this" | `academic-paper-orchestrator` | the user asks for a narrow single-stage task with clear inputs |

## Tie Breakers

- If the request spans three or more stages, use `academic-paper-orchestrator`.
- If the request modifies manuscript wording, but evidence status is unclear, start with writing diagnosis and route evidence gaps to research verification.
- If the request asks for final polish and also asks for new content, treat it as writing first, polish later.
- If the request asks for language diagnosis and official modification, diagnose with `language-style-review` and execute confirmed changes through `revision-control`.
- If the request asks for quality review and language review together, run `post-manuscript-benchmark-review` first, then `language-style-review`, then hand the unified queue to `revision-control`.
- If the request asks for benchmark review but only has an outline, treat it as writing/target alignment, not post-manuscript review.
- If the request asks for a DOCX output from unstable Markdown, ask whether the user accepts rework risk before formatting.
- If a workflow/process diagram is requested and no tool is specified, prefer Draw.io through `academic-figure-workflow`.

## Confirmation Points

Stop for user confirmation when:

- the field or terminology baseline is inferred;
- a candidate or unresolved source would be used in writing;
- benchmark access is abstract-only or metadata-only but the user wants a readiness judgment;
- language-style review proposes candidate project standards;
- revision control would change sentence pass/fail state, latest draft text, round records, or project standards;
- final polishing may soften or remove claims;
- formatting may overwrite or normalize the only working draft;
- conversion may flatten formulas, superscripts/subscripts, citations, cross-references, or figure/table notation;
- figure generation requires external image generation or unverifiable visual content.
