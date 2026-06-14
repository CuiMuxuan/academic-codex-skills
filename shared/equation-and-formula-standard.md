# Equation And Formula Standard

Use this shared reference whenever writing, revising, reviewing, converting, or formatting formulas, equations, inline math, chemical notation, unit expressions, or equation cross-references.

## Canonical Source

LaTeX is the canonical source for formulas and equation-like notation.

- Write new formulas in LaTeX syntax.
- Preserve the original LaTeX expression in the manuscript source, object library, conversion log, or handoff report.
- Do not replace an editable or reconstructable formula with an image unless the user explicitly approves a lossy fallback.
- If a formula is converted from DOCX, PDF, image, or plain text and the LaTeX cannot be recovered with confidence, mark it `needs_manual_equation_check`.

## Default Formula Standard

When no journal, school, or publisher rule is provided:

- Use LaTeX as the default formula source format.
- Treat inline math and display math as LaTeX layout wrappers, not as alternatives to LaTeX source.
- Use display math as the default layout for substantive formulas/equations. Display formulas must occupy a separate line or block and be centered unless the target journal, school, or template specifies another alignment.
- Keep inline math only for short variables, symbols, units, and simple relations that do not interrupt the sentence; do not keep a substantive formula inline merely because it is short.
- Use display math for definitions, derived expressions, multi-term equations, long fractions, aligned expressions, or equations that will be referenced later.
- Keep equation punctuation consistent with the surrounding sentence.
- Put equation labels on display equations that are referenced in text, using a stable label such as `{#eq:sulfur-energy}` or another project convention already in use.
- Number equations only when the target format or cross-reference workflow needs numbering; otherwise keep labels for traceability and defer final numbering to formatting.
- Define every symbol either immediately before or after the equation, unless it is already standard and unambiguous in the confirmed field.
- For chemical formulas and units, preserve semantic subscript/superscript structure: `CO_2`, `H_2S`, `10^{-3}`, `mg L^{-1}`, `E_{S,removed}`.
- Break long equations at logical operators or aligned terms; do not merge a long display equation into body prose.

## Journal Or Template Override

If the user provides a journal guide, school handbook, official template, or target example with explicit equation rules, those rules override the default standard.

Record the applied rule source in the output or formatting report:

```yaml
equation_rule_source:
  source_type: journal_guide|school_handbook|template|target_example|default
  source_path_or_url:
  applied_rules:
  unresolved_conflicts:
```

If the target rules conflict with the manuscript's current source format, show the conflict and ask before converting formulas in a way that could lose editability, labels, or cross-references.

## Cross-Skill Handoff Fields

When formulas move between skills, use these fields when applicable:

```yaml
formula_id:
owner_object_id:
formula_kind: inline|display|chemical_notation|unit_notation|table_formula|figure_label_formula
latex_source:
plain_text_fallback:
label:
numbering_state: unnumbered|source_numbered|needs_numbering|journal_template_numbered
symbol_definitions: []
source_path:
source_location:
conversion_state: source_latex|converted_to_omml|rendered_for_review|needs_manual_equation_check
notes:
```

## Writing And Revision Rules

- `$paper-writing-workflow` should write formulas in LaTeX and keep them traceable to the claim, data, or definition they support.
- `$revision-control` should preserve formula LaTeX source and object ids during object-library rebuilds and latest-draft synchronization.
- `$language-style-review` and `$post-manuscript-benchmark-review` may flag unclear symbol definitions, unsupported equations, or field-inappropriate notation, but formal state updates must go through `$revision-control`.
- `$academic-formatting-workflow` should convert LaTeX-derived formulas to editable Word equations or OMML when producing DOCX, and must report any formula that remains rasterized, flattened, or manually checked.

## UI Review Rule

The revision annotation UI should display formulas as visible, read-only formula content while preserving the LaTeX source for copying, annotation, and downstream conversion.

- Inline math stays inline in the sentence display.
- Display equations render as separate centered equation blocks in the manuscript row by default.
- The UI may use browser-native text rendering for LaTeX if no math renderer is bundled, but it must keep the raw LaTeX visible enough for review.
- Formula rendering must not change `char_start`, `char_end`, `selected_text`, or `text_hash` offsets for span annotations.
- If a sentence contains both prose and formula source, annotations remain anchored to the normalized source text.

## Acceptance Criteria

An equation/formula artifact is acceptable only when:

- the LaTeX source can be recovered;
- inline and display formula roles are preserved;
- labels and equation references are traceable or explicitly marked for manual refresh;
- symbols, units, subscripts, and superscripts remain semantically readable;
- DOCX outputs use editable equations where feasible;
- any lossy fallback is explicitly approved and logged.
