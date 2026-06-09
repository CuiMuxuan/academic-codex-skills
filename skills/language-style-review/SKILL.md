---
name: language-style-review
description: "Review academic language style without modifying manuscript state. Use when the user asks for language style review, wording checks, grammar, AI-like phrasing, templated expression, Chinese-English translation accuracy, figure/table text wording, citation sentence style, sentence-level ambiguity, terminology acceptability, or operation-record residue checks in a paper, thesis, dissertation, review, rebuttal, chapter, section, paragraph, or sentence. May run independently or as an upstream report for revision-control or academic-paper-orchestrator. Chinese triggers: 语言风格审查, 检查语言, 用词检查, 语法检查, AI味, 模板化表达, 中文译文准确性, 图表文字, 引用句式, 逐句语言审查."
---

# Language Style Review

Use this skill to audit scholarly wording and return scored findings, localized issues, candidate rewrites, and a handoff queue. It does not write the manuscript, update sentence status, or maintain revision state.

## Boundaries

Do:

- Review language at manuscript, chapter, section, paragraph, sentence, figure/table text, or citation-sentence level.
- Score clarity, academic expression, terminology, and residue/mechanical-pattern risk.
- Locate problems by object id or sentence when ids are available.
- Provide candidate rewrites as suggestions only.
- Explain why accepted professional terms or proper nouns should remain unchanged.
- Create candidate project-standard items when the user asks to record a preference.

Do not:

- Update the latest draft, object library, sentence pass/fail state, revision count, or round directory.
- Write to project supplemental review standards.
- Perform full manuscript quality or benchmark readiness review; route to `$post-manuscript-benchmark-review`.
- Perform formal sentence-level revision management; route to `$revision-control`.
- Final-polish stable text as the primary task; route accepted rewrite execution to `$academic-de-ai-polishing` when appropriate.
- Verify DOI, title, citation authenticity, or evidence sufficiency as final authority.

## Core Rules

1. Return review output, not official modifications.
2. Respect user-specified disliked words, phrases, sentence rhythm, and translation concerns as high-priority signals.
3. Keep field-specific terms if they are accepted professional terminology; explain the reason instead of rewriting them away.
4. Flag operation records, prompt traces, project-management traces, TODOs, and file workflow residue in manuscript prose.
5. Separate language problems from evidence, structure, citation-identity, or manuscript-readiness problems.
6. When a problem implies structural rewriting, missing literature, or object-state changes, create a handoff item for `$revision-control`.
7. Never add a project rule directly; produce `candidate_rules` for `$revision-control` to confirm with the user.

## Workflow

1. Identify scope, available object ids, manuscript language, field, target style, and any project standards path.
2. Use [review-workflow.md](references/review-workflow.md) to choose independent, orchestrated, or revision-control handoff mode.
3. Use [scoring-and-output-schema.md](references/scoring-and-output-schema.md) for four-dimension scoring, issue tables, accepted-term notes, candidate rewrites, and handoff queues.
4. Use [project-standards-handling.md](references/project-standards-handling.md) when project supplemental standards, terminology lists, problem-word lists, or user preferences are available.
5. If benchmark-quality judgment is requested, route the quality portion to `$post-manuscript-benchmark-review` before language review.
6. If official modification is requested, send the localized task queue to `$revision-control`.

## Output Contract

Return:

- review scope and source limits;
- project standards used, if any;
- four dimension scores to one decimal place;
- main issues;
- sentence/object-level issue table;
- accepted terms/proper nouns that should remain;
- candidate rewrites marked as non-final;
- suggested `$revision-control` task queue;
- `candidate_rules` when the user asks to record a preference.

## Reference

Read [review-workflow.md](references/review-workflow.md) for activation modes, sequencing with benchmark review, and handoff boundaries.

Read [scoring-and-output-schema.md](references/scoring-and-output-schema.md) before producing a formal report.

Read [project-standards-handling.md](references/project-standards-handling.md) before using or proposing project supplemental standards.

Read [language-style-review-schema.md](../../shared/language-style-review-schema.md) when another skill must consume the review report.
