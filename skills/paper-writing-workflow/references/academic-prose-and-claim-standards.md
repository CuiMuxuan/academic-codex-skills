# Academic Prose And Claim Standards

Use this reference for drafting, revising, and integrating academic prose. It is the baseline before any final style polishing.

## Language Priority

1. Drafting and revision: be accurate, direct, concise, and easy to understand.
   Chinese baseline: 准确、直接、简洁、易懂.
2. Avoid rare, ornate, or over-complex wording unless it is a standard term in the current field.
3. Final polish may improve rhythm, emphasis, and academic voice only after accuracy, evidence, and logic are stable.
4. Never trade precision for elegant phrasing.

## Abbreviations

- From the first body-text section onward, write `full term (abbreviation)` on first use.
- Titles, abstracts, and highlights are exempt from the first-use abbreviation expansion rule unless the target journal, school template, supervisor, or user explicitly requires expansion there.
- Use the abbreviation alone only after the first-use definition.
- If a journal, school, or discipline has a fixed convention, follow that convention and record the exception.
- In bilingual work, keep Chinese and English term pairs stable.

## Section And Paragraph Logic

- Each section or subsection should have a clear purpose before drafting.
- The opening of a section should tell the reader what the section is trying to establish.
- Each paragraph should have a paragraph job: problem framing, concept definition, evidence synthesis, route comparison, method justification, result interpretation, limitation, or transition.
- A paragraph that cannot be assigned a job is likely filler and should be removed, merged, or rewritten.
- Sentences must connect by explicit logic: cause, contrast, sequence, scope narrowing, evidence, implication, or transition.
- Avoid citation dumping. Apply [citation-proximity-and-style-gate.md](../../../shared/citation-proximity-and-style-gate.md) when placing, moving, or reviewing citations.

## Chapter And Subsection Independence

- A chapter or major section may have its own local purpose and does not need to mechanically echo the full-paper theme in every paragraph.
- Local independence is bounded: the chapter or section must still stay within the paper's research object, evidence scope, target problem, and accepted terminology.
- Each subsection should explain its own content clearly before being used by later subsections.
- Do not force bridges, transition paragraphs, or connective phrases between subsections when no real relationship exists.
- If subsections do have a real relationship, state the relationship specifically: dependency, contrast, sequence, shared evidence, different scope, or different method role.

## Information Order And Forward Reference Discipline

- Earlier text should not abruptly mention concepts, experiments, conclusions, methods, or terms that only become meaningful later.
- Necessary structure navigation is allowed, especially in introductions, long review sections, theses, or result roadmaps.
- Do not use "the next section will..." or similar previews as a substitute for argument, evidence, or concept setup.
- Later text may refer back to established concepts, definitions, claims, figures, tables, and results.
- When forward navigation is needed, keep it brief and tied to the current section's purpose.

## Sentence Ambiguity And Abstract Wording

For formal review or revision, check each sentence for ambiguity:

- unclear subject or object;
- undefined "this", "it", "they", "the method", "the model", or "the system";
- vague scope words such as "certain", "some", "many", "various", "related", "effective", or "significant" without measurable or contextual meaning;
- abstract nouns such as "mechanism", "framework", "strategy", "process", "feature", or "performance" when the exact referent has not been introduced;
- compressed sentences that combine multiple claims and make citation support unclear.

Fix ambiguity by naming the referent, narrowing the scope, adding the missing setup, splitting the sentence, or removing the unsupported abstraction.

## Paper Mainline Standard

Use these four questions as the core writing-quality gate:

1. Is the problem clear?
2. Is the method reasonable for that problem?
3. Do the experiments or analysis support the conclusion?
4. Is the contribution explicit and tied to the manuscript's central idea?

Keep the main manuscript focused on the central problem, method, experiment, and contribution. Remove material that does not support the main line, or move it to methods detail, appendix, supplement, limitation, or future work when it is still useful.

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

For final body text and rebuttal text, apply [main-text-and-rebuttal-claim-support-gate.md](../../../shared/main-text-and-rebuttal-claim-support-gate.md). Title, abstract, highlights, and graphical abstract do not need citation/support locators by default. If required support is missing in body text or rebuttal text, stop and output a reference download or material request list instead of drafting final prose.

For outlines, planning notes, or non-final draft areas that are not main-text or rebuttal final prose, mark the location with `LIT_GAP` and continue with other draftable sections.

For central claims, maintain a claim anchor with support locator and allowed claim strength. Do not phrase the claim more strongly than the anchor permits.

## Citation Placement

Use [citation-proximity-and-style-gate.md](../../../shared/citation-proximity-and-style-gate.md) for citation proximity, paragraph-end citation piles, multi-claim sentences, and punctuation placement under different citation styles.

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
