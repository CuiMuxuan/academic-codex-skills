# Workflow Protocol Index

Use this shared index when coordinating multiple academic skills. Keep cross-skill protocol definitions here, and keep skill-local references focused on stage-specific execution.

## Shared Protocols

| protocol | read when | owner |
|---|---|---|
| Workflow mode | selecting or changing the current stage, resuming a project, or deciding the next user confirmation gate | orchestrator |
| Multi-agent academic workflow | planning default parallel review, verification, QA, or action-plan decomposition for substantial paper workflows | orchestrator + writing + post-manuscript benchmark review |
| Material passport | tracking artifacts that move across research, parsing, writing, figures, review, polishing, or formatting | orchestrator |
| Claim evidence anchor | drafting, verifying, reviewing, polishing, or captioning central claims | writing + research verification |
| Literature gap handoff | moving `LIT_GAP` items between writing and research verification | writing + research verification |
| Benchmark report | reviewing a complete draft against target papers | post-manuscript benchmark review |
| Language style review report | reviewing wording, grammar, AI-like phrasing, terminology, translation, figure/table text, or citation sentence style without editing state | language-style review |
| Revision control contract | managing formal sentence-level revision, object libraries, round state, latest drafts, project standards, material dependencies, and upgrade plans | revision control |
| Manuscript object model | building paper, section, paragraph, sentence, and figure/table text objects for revision rounds | revision control |
| Project review standards | maintaining user-confirmed supplemental language and review rules across rounds | revision control |
| Revision upgrade plan | pausing sentence-level editing for literature补充, structure reorganization, material changes, or large rewrites | revision control |
| Main text and rebuttal claim support | drafting, revising, polishing, or approving final main-text or rebuttal claims | writing + research verification |
| Citation proximity and style | drafting, reviewing, auditing, polishing, or converting cited manuscript text | writing + research verification + formatting |
| Cross-disciplinary language review | drafting, reviewing, or polishing formal body text or rebuttal prose for abstract wording, undefined terms, operation-record residue, unclear support, or sentence-level ambiguity | writing + post-manuscript benchmark review + polishing |
| Reviewer comment action plan | turning two or more review comments into accepted, partial, rejected, deferred, or material-blocked actions | writing + post-manuscript benchmark review |
| Notation and conversion integrity | converting formulas, superscripts/subscripts, citations, cross-references, figures, tables, or captions across output formats | formatting + figures |
| Trigger conflict matrix | deciding which skill owns an ambiguous user request | orchestrator |
| Validation policy | checking local or installed skills before use or release | repository validation script |

## Routing Rule

Use `academic-paper-orchestrator` as the broad entrypoint for repository-level routing protocols. Focused owner skills may read the shared protocol files they explicitly reference, especially `$revision-control` and `$language-style-review` for revision-state and review-report schemas.

## Required Gates

Ask for user confirmation before moving past:

- inferred or unclear research field or terminology baseline;
- multi-agent parallel checks before starting sub-agents, unless the user has already granted full permission or automatic-execution permission;
- user-requested strict sentence-by-sentence language review before expanding beyond the specified chapter, subsection, paragraph, or sentence;
- formal sentence-level revision before creating or changing pass/fail state, object-library state, latest review drafts, or project supplemental standards;
- language-style review candidate rules before writing them into project supplemental standards;
- project design document and chapter outline;
- initial verified evidence register or gap-resolution handoff;
- benchmark set before target-readiness judgment;
- combined quality and language review before sending a unified modification queue into revision control;
- unsupported main-text or rebuttal claims that require citations, data, standards, code, or user-supplied materials;
- reviewer-comment batches with two or more comments before drafting the revision or rebuttal;
- integrated draft before final polish or formatting;
- external image-generation use;
- lossy formula, superscript/subscript, citation, cross-reference, or figure/table conversion;
- formatting baseline before final DOCX normalization.

If sub-agent tools are unavailable or disallowed by the current environment, run planned parallel checks serially and state that limitation instead of silently dropping them.

When a field is unclear and the user also declines to set it, default to computer science and electronic information, then mark the assumption.

## Protocol Drift Rule

If a skill-local reference disagrees with this shared layer, prefer the shared protocol for field names, handoff states, and trigger conflict decisions. Then update the local reference in the repository before relying on it again.
