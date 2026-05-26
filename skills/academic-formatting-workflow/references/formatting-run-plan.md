# Formatting Run Plan

Use this reference when planning or reporting a manuscript formatting pass.

## Rule Table

When the guide or template is long, create a compact rule table before editing:

| area | rule | source | priority | automation | status |
|---|---|---|---|---|---|
| heading | Heading 1 font and numbering | handbook p.X or template style | official/template/provisional | python-docx/Word COM/manual | pending/applied/needs Word refresh/unresolved |

## Pass Table

Before editing, map rules to formatting passes:

| pass | scope | rule sources | tool | output copy | manual check |
|---|---|---|---|---|---|
| page setup | sections, margins, headers, page numbering | handbook/template/provisional | python-docx/Word COM/manual | `_pre_final` or planned suffix | Word refresh needed? |

Use one row per pass from page setup through final validation. Mark any pass as `manual` when it depends on Word-only behavior, template attachment, TOC refresh, field updates, or visual page inspection.

For Markdown-to-DOCX work, add explicit passes for formula conversion, superscript/subscript normalization, citation processing, cross-reference validation, and bibliography rendering before final Word refresh.

## Pass Order

1. Page setup and sections.
2. Front matter.
3. Heading hierarchy.
4. Body paragraphs.
5. Figures, tables, formulas, and captions.
6. References and appendices.
7. Final validation.

## Safe Output Naming

Default output suffixes:

- `_formatted`
- `_normalized`
- `_template_applied`
- `_pre_final`

Do not overwrite the only working document unless the user explicitly asks.

## Output Report

Return:

- source rules used;
- output file path;
- formatting changes applied;
- rule-table items still marked `unresolved` or `needs Word refresh`;
- items requiring manual Word check;
- remaining conflicts or missing rule sources.
