# Formatting Validation

Use this reference before calling a DOCX or formatted manuscript ready.

## General Baseline Without Template

Use conservative defaults only after labeling them provisional:

- consistent heading hierarchy;
- readable body font and line spacing;
- first-line indent for body paragraphs when appropriate;
- separate Chinese and English abstract sections when required;
- consistent figure/table caption numbering;
- references formatted consistently in the requested citation style;
- stable page setup across sections.

State that these are provisional and should be checked against the real handbook before final submission.

## Final Checks

Before finishing, verify:

- output file exists and opens when validation is possible;
- page setup matches the chosen source;
- heading levels are consistent;
- captions and cross-references are not obviously broken;
- Markdown-origin formulas are readable, preferably editable, and traceable to their LaTeX source;
- superscripts and subscripts in formulas, units, chemical notation, and variables survived conversion;
- in-text citations, bibliography entries, and figure/table/equation cross-references remain linked or are explicitly listed for manual refresh;
- bibliography style is consistent;
- table of contents is refreshed or listed as requiring Word refresh;
- Word-only fields, TOC, tables of figures, indexes, and pagination are refreshed or explicitly listed as manual checks;
- no content was unintentionally removed.

## Word Refresh

When the user confirms Word automation and the document is ready for final field refresh, use:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/refresh_word_fields.ps1 -InputPath thesis_pre_final.docx -OutputPath thesis_pre_final_refreshed.docx
```

Do not run this silently. It opens Microsoft Word through COM automation, saves a new copy, and writes a `.word-refresh.json` report. Use `-AllowOverwrite` only after explicit overwrite confirmation.
