---
name: academic-de-ai-polishing
description: "Use when polishing a paper, review, thesis, rebuttal, or other scholarly prose that reads mechanically, over-smoothed, or obviously AI-assisted. Best for section-by-section rewriting that preserves meaning, citations, and technical rigor while reducing templated transitions, repetitive cadence, and formulaic academic phrasing. Chinese triggers: 论文降AI痕迹, 去AI味, 去模板化润色, 降低机械感, 学术润色, AIGC痕迹评估."
---

# Academic De-AI Polishing

Use this skill when a user asks to reduce `AIGC` traces, remove `AI` smell, de-template academic English, or make scholarly prose sound more native, critical, and authorial without changing the core argument.

Typical triggers:

- journal manuscripts, review papers, theses, dissertations, rebuttals, and cover letters
- phrases such as "reduce AI traces", "remove mechanical feel", "make it less templated", "lower AIGC risk", or "make this sound like a senior scholar wrote it"
- drafts that are technically correct but rhythmically over-regular, transition-heavy, or built from repeated academic templates

Do not use this skill to fabricate evidence, change conclusions without support, or make false claims about detector scores. The goal is stronger academic prose, not deceptive metadata games.

If a paragraph feels high-risk but the exact failure mode is not obvious, read [references/high-risk-patterns.md](references/high-risk-patterns.md). Use that file when you need concrete pattern matching between a risky sentence shape and the most suitable rewrite strategy.

If you need concrete model examples before rewriting, read [references/before-after-examples.md](references/before-after-examples.md). Use that file when the user wants exemplar transformations or when you need to calibrate the difference between a templated sentence and a more native, authorial academic version.

If the main question is how to polish a specific chapter or manuscript section, read [references/section-playbooks.md](references/section-playbooks.md). Use that file when the rewrite problem is section-dependent rather than sentence-pattern-dependent.

If the user is working on a long review article and wants the practical lessons from a real end-to-end polishing project, read [references/project-notes-from-this-paper.md](references/project-notes-from-this-paper.md). Use that file when you need a field-tested sequence for lowering AI traces across a full manuscript rather than only fixing isolated paragraphs.

If the source text, target examples, section role, citation boundary, or allowed edit intensity is unclear, read [references/edit-contract-template.md](references/edit-contract-template.md) and ask for the missing edit contract fields before rewriting.

## Non-Negotiables

- Preserve technical meaning, evidence balance, citation logic, and section purpose.
- Do not reduce substantive content unless the user explicitly asks for compression.
- Prefer local paragraph-level rewrites over whole-section regeneration.
- Keep terminology exact and journal-appropriate.
- Retain or strengthen the author's critical judgment instead of flattening it into neutral summary.
- Fix argument, evidence scope, and claim precision before fixing cadence. A smoother unsupported claim is still a failed edit.

## Language And Bilingual Handling

- Reply in the user's requested language; if the request is Chinese, diagnose and revise in Chinese unless the user asks for English.
- For Chinese academic prose, reduce 套话, 连接词堆叠, and 机械对偶句式 while preserving disciplinary terminology, citation logic, evidence strength, and formal thesis tone.
- For bilingual work, keep Chinese and English terminology pairs stable. Do not translate, simplify, or Anglicize key terms unless the user asks.
- If a source paragraph mixes languages, preserve the manuscript's intended language mix and explain any terminology choices in the change note.

## Pre-Edit Gate

Before rewriting, confirm the minimum edit contract:

```text
Source text present:
Section type:
Paragraph role:
Fixed claims and citations:
Allowed edit intensity:
Do-not-change terms:
```

If the source text is missing, ask for it instead of producing a generic demonstration. If citations, data, or evidence boundaries are missing, keep the rewrite conservative and mark where author verification is needed.

Do not polish over a reasoning problem. When a paragraph overclaims, hides uncertainty, or uses a citation for a claim it may not support, flag the issue first and either soften the claim or ask for evidence before adding authorial judgment.

Ask for 3-10 target examples when the user wants a specific journal, school, supervisor, or authorial style. If none are provided, use the generic academic de-template baseline and label style assumptions.

Before assessment or rewriting, ask for missing materials that would materially improve polishing quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for the source text, target examples, section type, paragraph role, fixed claims, fixed citations, do-not-change terms, allowed edit intensity, and whether the user wants diagnosis only or rewrite. If unavailable, do not rewrite; provide a material request or a conservative qualitative assessment after the user confirms.

## Argument-First Gate

Before rewriting, classify each target paragraph:

| State | Action |
|---|---|
| `sound_argument_mechanical_style` | Rewrite for cadence, vocabulary, transitions, and authorial voice. |
| `overclaiming_or_missing_evidence` | Flag the claim problem first, then soften or request evidence before polishing. |
| `unclear_section_job` | Ask for section role or propose a local role before rewriting. |
| `citation_boundary_unclear` | Preserve citations conservatively and mark claims that need author verification. |

Do not make a paragraph sound more confident than the source evidence permits. For journal or thesis work, the best de-AI edit often makes the prose slightly less sweeping and more evaluative.

## Risk Signals

High-risk signs:

- stacked connector prose: "Moreover", "Furthermore", "However", "Therefore", repeated in close succession
- mirrored sentence pairs or repeated "X is effective, but Y remains challenging" structures
- overly even sentence length and paragraph rhythm
- broad summary language with weak mechanism, weak trade-off reasoning, or no evaluative stance
- numbered logic that reads like a checklist rather than an argument

Medium-risk signs:

- smooth but generic transitions
- repeated paragraph openers across a section
- vague academic nouns such as "challenge", "issue", "important role", or "significance" where a sharper term is available
- conclusions that merely restate literature trends without weighing evidence quality or engineering consequences

Low-risk signs:

- variable syntax and paragraph rhythm
- selective, evidence-based critical judgment
- transitions driven by topic carry-over rather than explicit scaffolding
- claims anchored to mechanisms, operating boundaries, or study-quality differences

## Core Workflow

1. Read the section and identify only the medium- and high-risk paragraphs.
2. Diagnose the main failure mode for each paragraph:
   - connector overload
   - repetitive cadence
   - templated dialectic
   - vague vocabulary
   - missing authorial judgment
3. Rewrite in small blocks.
   - Default unit: one paragraph.
   - Expand to two adjacent paragraphs only when the transition between them is the problem.
   - Do not regenerate an entire section unless the user explicitly asks.
4. After each rewrite, verify:
   - meaning is unchanged
   - citations still support the claim they follow
   - technical scope has not been broadened
   - the paragraph no longer sounds mechanically balanced
5. Reassess the section and continue only where medium/high-risk traces remain.

## Rewrite Tactics

### 1. Replace Explicit Connector Scaffolding

- Remove stacked transition adverbs unless one is genuinely needed.
- Link sentences through topic continuation, pronouns, repeated key nouns, and cause-effect ordering.
- Let one sentence prepare the next through content, not signaling language.

### 2. Break Symmetrical Sentence Habits

- Alternate long and short sentences.
- Use subordinate clauses, appositives, and participial modifiers when natural.
- Avoid repeating the same subject-verb frame in adjacent sentences.
- Do not let every paragraph move in the same "claim -> contrast -> conclusion" rhythm.

### 3. De-Template the Vocabulary

- Replace generic academic filler with domain-specific distinctions.
- Prefer verbs that show mechanism or judgment: `narrows`, `redistributes`, `destabilizes`, `masks`, `overstates`, `depends on`, `shifts the burden`.
- Cut stock phrases such as "it is worth noting that", "plays an important role", and "in conclusion" unless they add real value.

### 4. Restore Authorial Judgment

Add disciplined evaluative sentences where the literature supports them, for example:

- why a comparison is misleading
- which metric overstates performance
- where headline removal hides instability
- why a route is credible only within a narrow operating role
- how a study design limits cross-study comparability

Judgment must remain evidence-grounded and formal.

### 5. Preserve Academic Rigor

- Do not paraphrase beyond the evidence.
- Keep abbreviations, units, and process names exact.
- Maintain citation density unless compression is clearly safe.
- When compressing long citation strings, do not hide disagreement or distinct evidence roles.

### 6. Calibrate Against Target Examples

When the user provides 3-10 target examples, infer:

- paragraph length and density;
- citation placement and evidence grouping;
- tolerance for first-person, cautious modal verbs, and evaluative language;
- section-specific rhythm for introduction, methods, results, discussion, rebuttal, or thesis chapters;
- how the target style handles limitations and negative findings.

Use target examples as calibration, not as text to imitate. Do not copy distinctive phrasing from the examples.

## Section-Specific Guidance

### Abstract and Highlights

- Avoid slogan-like balance and polished symmetry.
- Keep novelty and scope precise.
- In highlights, prefer concrete takeaways over elegant taglines.

### Introduction

- Reduce over-scripted critique.
- Let the motivation unfold with slight asymmetry rather than perfectly paired oppositions.
- Keep problem framing pointed, but not theatrically smooth.

### Technology Sections

- Watch for repeated advantage-versus-limitation templates.
- Tie evaluation to mechanism, operating window, failure route, or integration burden.
- Replace generic summary with selective engineering judgment.

### Hybrid Design and Future Directions

- These sections often look most AI-shaped because they invite list logic.
- Keep structure clear, but vary the prose inside each route or recommendation.
- Prefer trade-off reasoning over checklist phrasing.

## Output Pattern

When revising text with this skill, provide:

- the target section or paragraph opening
- the section job and edit boundary
- a short diagnosis of why it reads mechanically
- the revised paragraph or paragraph block
- a preservation check for meaning, citations, terminology, and technical scope
- a brief note on what changed in cadence, vocabulary, or judgment when helpful

For long passages, use a compact change log:

| paragraph | dominant risk | action | evidence/citation caution |
|---|---|---|---|
| P1 | connector stacking | rewritten | citation preserved |
| P2 | overclaiming | softened | author should verify claim scope |

Do not show a line-by-line diff unless the user asks; it often consumes space without improving the manuscript.

## If the User Asks for "AI Trace" Assessment

- Give a qualitative reviewer-facing assessment.
- Separate:
  - likelihood that a human reader notices obvious templating
  - likelihood that the passage feels under-edited or mass-generated
- Do not invent detector percentages.
- Point to the exact paragraphs where residual risk remains.

## Style Commitments

Use these as hard constraints during revision:

1. Minimize rigid textbook connectors and build transitions implicitly.
2. Vary sentence architecture and paragraph rhythm.
3. Remove boilerplate academic phrasing in favor of precise, native-level wording.
4. Preserve formal rigor, technical accuracy, and airtight logic at every step.
5. Keep the revision auditable: the user should be able to see what claim changed, what evidence boundary was preserved, and what remains risky.
