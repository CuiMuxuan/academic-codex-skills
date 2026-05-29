# Academic Prose And Claim Standards

Use this reference for drafting, revising, and integrating academic prose. It is the baseline before any final style polishing.

## Language Priority

1. Drafting and revision: be accurate, direct, concise, and easy to understand.
   Chinese baseline: 准确、直接、简洁、易懂.
2. Avoid rare, ornate, or over-complex wording unless it is a standard term in the current field.
3. Final polish may improve rhythm, emphasis, and academic voice only after accuracy, evidence, and logic are stable.
4. Never trade precision for elegant phrasing.

## Abbreviations

- On first use, write `full term (abbreviation)`.
- Use the abbreviation alone only after the first-use definition.
- If a journal, school, or discipline has a fixed convention, follow that convention and record the exception.
- In bilingual work, keep Chinese and English term pairs stable.

## Section And Paragraph Logic

- Each section or subsection should have a clear purpose before drafting.
- The opening of a section should tell the reader what the section is trying to establish.
- Each paragraph should have a paragraph job: problem framing, concept definition, evidence synthesis, route comparison, method justification, result interpretation, limitation, or transition.
- A paragraph that cannot be assigned a job is likely filler and should be removed, merged, or rewritten.
- Sentences must connect by explicit logic: cause, contrast, sequence, scope narrowing, evidence, implication, or transition.
- Avoid citation dumping. Explain why the cited evidence matters for the paper's argument.

## Contribution And Limitation Framing

- When describing the manuscript's own contribution, emphasize completed work, evidence, analysis, and defensible conclusions.
- Reduce defensive language such as broad claims that the work is still incomplete unless the target genre requires a limitation statement.
- State limitations only when useful to interpretation, reproducibility, or future work.
- When possible, recast self-limitations as future optimization directions without hiding real uncertainty.
- When describing weaknesses in prior work, use citations or evidence and keep the critique proportional.

## Claims That Require Evidence

Do not make these claims without verified literature, data, analysis output, code evidence, or a user-approved source:

- factual judgments about a field, method, dataset, standard, or practice;
- mechanism or causal judgments;
- engineering applicability judgments;
- route, method, model, or technology comparisons;
- evidence-quality or reporting-standard judgments;
- conclusion-like statements that summarize what is known or proven.

If the required support is missing, mark the location with `LIT_GAP` and continue with other draftable sections.

For central claims, maintain a claim anchor with support locator and allowed claim strength. Do not phrase the claim more strongly than the anchor permits.

## Code, Data, And Result Claims

When the manuscript describes implementation details, datasets, experiments, baselines, or metrics, the support must be traceable to a user-provided artifact, inspected code, a result table, a script/notebook output, or verified literature. If the artifact is unavailable or ambiguous, ask the user before asserting the claim or mark it as `LIT_GAP`.

## Writing Completion Check

Before calling prose complete:

- section purpose is visible;
- paragraph jobs are visible;
- abbreviations are defined on first use;
- major claims have verified evidence or `LIT_GAP` markers;
- central claims have evidence anchors or are explicitly unresolved;
- terminology matches the confirmed field;
- contribution claims emphasize completed work rather than unsupported promise;
- final style polish has not changed claim strength.
