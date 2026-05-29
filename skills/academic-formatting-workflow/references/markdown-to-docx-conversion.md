# Markdown To DOCX Conversion

Use this reference when a Markdown manuscript must become a DOCX while preserving formulas, superscripts/subscripts, citations, bibliography entries, and figure/table/equation cross-references.

## Conversion Contract

Before converting, identify:

- source Markdown file and target DOCX path;
- target handbook, Word template, reference DOCX, or journal guide;
- bibliography source: `.bib`, `.ris`, `.json`, pasted reference list, or none;
- citation style: CSL, numeric, author-year, school style, or provisional;
- cross-reference mechanism: Pandoc labels, Markdown links, Word fields, manual labels, or none;
- formula expectation: editable Word equations preferred, LaTeX review notes acceptable, raster fallback only by user approval.

Do not install or upgrade converters silently. If Pandoc, a citation processor, a DOCX reference file, or Word automation is missing, report the limitation and ask before using a fallback that loses editability or links.

## Formula Standard

- Treat LaTeX as the canonical source for formulas. Preserve the original LaTeX expression in the Markdown source or a conversion log.
- Prefer editable Word equations or Office Math Markup Language (OMML). Do not accept rasterized, flattened, or garbled formulas as final unless the user explicitly approves that fallback.
- Keep inline math inline and display math as separate equation blocks.
- Preserve equation labels and numbering when present. If automatic numbering is unavailable, mark equations that need Word refresh or manual numbering.
- Check long equations for readable line breaks; do not let conversion merge them into body text.
- If a converter cannot handle a formula, keep the LaTeX source visible in the QA note and mark it `needs manual equation check`.

## Superscripts And Subscripts

Check both formulas and non-formula text:

- LaTeX forms: `x_i`, `x_i^2`, `x_{i,j}`, `E^{(t)}`, `10^{-3}`, `R^2`.
- Chemical and unit notation: `CO_2`, `H_2S`, `m^2`, `s^{-1}`, `mg L^{-1}`.
- Markdown or HTML forms: `<sup>`, `<sub>`, `^text^`, `~text~`.

Preserve semantic grouping. Do not let grouped indices, exponents, chemical formulas, or units degrade into baseline plain text. Inspect nested indices, primes, Greek letters, vectors, matrices, fractions, summations, integrals, and equation labels after conversion.

## Citations And Cross-References

- Prefer a structured citation processor such as Pandoc with CSL and BibTeX/BibLaTeX metadata when available.
- Preserve citation keys until the final render; do not flatten references into untraceable plain text before citation audit unless the user confirms this is acceptable.
- Validate that every in-text citation has a bibliography entry and every required bibliography item is intentionally used or retained.
- Check figure, table, and equation references separately from bibliographic citations.
- Confirm that captions, labels, numbering, and reference text survive conversion or are listed as requiring Word refresh/manual repair.
- When Word fields, TOC, tables of figures, or automatic cross-references are required, mark the DOCX as `needs Word refresh` unless Word automation has been explicitly run and verified.

## Run Plan

| pass | purpose | output |
|---|---|---|
| source inventory | detect math, citations, labels, captions, bibliography inputs | conversion risk list |
| formula conversion | preserve LaTeX-derived formulas as readable DOCX equations | formula QA list |
| superscript/subscript check | inspect formulas, units, chemical notation, and inline symbols | notation issue list |
| citation processing | render or preserve citations according to target style | citation audit list |
| cross-reference validation | check figure/table/equation labels and targets | cross-reference issue list |
| final formatting | apply template, styles, captions, page setup, and Word refresh plan | formatted DOCX and report |

## Package QA Hook

When maintaining this skills repository or validating a conversion package, use:

```bash
python scripts/validate_markdown_docx_package.py --markdown manuscript.md --docx manuscript.docx --output-md markdown_docx_validation.md
```

If Pandoc or Word is unavailable, report the missing dependency and keep the output provisional rather than silently accepting lossy conversion.

## QA Packet

```text
Source Markdown:
Conversion toolchain:
Reference DOCX/template:
Formula handling:
Superscript/subscript checks:
Citation processor:
Cross-reference status:
Bibliography status:
Manual Word checks:
Unresolved conversion risks:
```

## Acceptance Criteria

The converted DOCX is acceptable only when:

- formulas are readable and preferably editable;
- original LaTeX can be recovered from the source or conversion note;
- superscripts and subscripts survive in formulas, variables, units, and chemical notation;
- in-text citations and bibliography entries are consistent;
- figure, table, and equation cross-references have valid targets or are explicitly flagged;
- Word-only fields, TOC, tables of figures, and pagination are refreshed or listed for manual refresh.
