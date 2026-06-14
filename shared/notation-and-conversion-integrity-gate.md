# Notation And Conversion Integrity Gate

Use this shared gate whenever manuscript, figure, table, or caption content is converted between Markdown, DOCX, PDF, SVG, Draw.io, image exports, or other publication artifacts.

## Trigger

Apply this gate when converting or validating:

- LaTeX formulas;
- inline math and display math;
- superscripts and subscripts;
- chemical, mathematical, algorithmic, or model notation;
- citation links, bibliography entries, figure/table references, and cross-references;
- figure labels, axis labels, legends, captions, or table cells that contain notation.

## Non-Lossy Conversion Rule

Do not silently accept output that loses:

- superscript or subscript structure;
- formula readability;
- citation identity;
- cross-reference targets;
- figure/table numbering;
- editable source files needed for later correction.

If a tool cannot preserve these elements, report the limitation and ask before using a lossy fallback.

## Formula Standard

- Apply [equation-and-formula-standard.md](equation-and-formula-standard.md) before writing, revising, rendering, or converting formulas.
- Treat LaTeX as the canonical source for formulas.
- Preserve the original LaTeX expression in the Markdown source, object library, conversion log, or handoff report.
- Prefer editable Word equations for DOCX outputs.
- Use rasterized formulas only when the user approves the loss of editability.
- When no journal, school, or publisher rule is provided, use the default equation standard in the shared formula reference; when a target journal/template provides equation rules, those target rules override the default.

## Superscript And Subscript Checks

Check both source and rendered output for:

- exponents, indices, tensor notation, model names, and variable subscripts;
- units, statistical notation, and dataset/model version labels;
- chemical formulas and biological notation when relevant;
- citations or footnote markers that may be confused with superscripts.

## Cross-Reference Checks

Before calling an output ready, verify:

- citations point to the intended bibliography entries;
- figure, table, equation, and section references resolve after Word field refresh when applicable;
- captions and in-text references use the same numbering scheme;
- exported figures do not contain stale manual numbers that conflict with the manuscript.
