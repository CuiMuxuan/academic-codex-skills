# Rewrite Tactics

Use this reference when the paragraph argument is sound but the prose reads mechanically, overly templated, or too AI-smooth.

## Replace Explicit Connector Scaffolding

- Remove stacked transition adverbs unless one is genuinely needed.
- Link sentences through topic continuation, pronouns, repeated key nouns, and cause-effect ordering.
- Let one sentence prepare the next through content, not signaling language.
- Remove subsection bridges that exist only to announce the next subsection.
- If two subsections have no real relation, do not invent one; keep each subsection locally clear.

## Break Symmetrical Sentence Habits

- Alternate long and short sentences.
- Use subordinate clauses, appositives, and participial modifiers when natural.
- Avoid repeating the same subject-verb frame in adjacent sentences.
- Do not let every paragraph move in the same `claim -> contrast -> conclusion` rhythm.

## De-Template The Vocabulary

- Replace generic academic filler with domain-specific distinctions.
- Prefer verbs that show mechanism or judgment: `narrows`, `redistributes`, `destabilizes`, `masks`, `overstates`, `depends on`, `shifts the burden`.
- Cut stock phrases such as "it is worth noting that", "plays an important role", and "in conclusion" unless they add real value.
- Replace vague abstractions with the exact referent when the prior text has not established the concept.
- Avoid using "framework", "mechanism", "strategy", "feature", "factor", or "performance" without naming what it refers to.

## Repair Ambiguity And Premature References

- When a sentence points to later-only content, either move it later, add the needed setup, or reduce it to concise structure navigation.
- Split sentences that combine multiple claims with different support sources.
- Replace unclear pronouns and generic nouns with the actual method, dataset, variable, result, section, or claim.
- Remove repeated explanations across subsections unless they serve a deliberate contrast, summary, or methodological distinction.

## Restore Authorial Judgment

Add disciplined evaluative sentences where the literature supports them, for example:

- why a comparison is misleading;
- which metric overstates performance;
- where headline removal hides instability;
- why a route is credible only within a narrow operating role;
- how a study design limits cross-study comparability.

Judgment must remain evidence-grounded and formal.

## Preserve Academic Rigor

- Do not paraphrase beyond the evidence.
- Do not hide unresolved `LIT_GAP` or `needs evidence` markers by smoothing the surrounding prose.
- Keep abbreviations, units, and process names exact.
- Maintain citation density unless compression is clearly safe.
- When compressing long citation strings, do not hide disagreement or distinct evidence roles.

## Calibrate Against Target Examples

When the user provides 3-10 target examples, infer:

- paragraph length and density;
- citation placement and evidence grouping;
- tolerance for first-person, cautious modal verbs, and evaluative language;
- section-specific rhythm for introduction, methods, results, discussion, rebuttal, or thesis chapters;
- how the target style handles limitations and negative findings.

Use target examples as calibration, not as text to imitate. Do not copy distinctive phrasing from examples.

## Output Pattern

When revising text, provide:

- target section or paragraph opening;
- section job and edit boundary;
- short diagnosis of why it reads mechanically;
- revised paragraph or paragraph block;
- preservation check for meaning, citations, terminology, and technical scope;
- brief note on cadence, vocabulary, or judgment changes when helpful.

For long passages, use:

| paragraph | dominant risk | action | evidence/citation caution |
|---|---|---|---|
| P1 | connector stacking | rewritten | citation preserved |
| P2 | overclaiming | softened | author should verify claim scope |

Do not show a line-by-line diff unless the user asks.
