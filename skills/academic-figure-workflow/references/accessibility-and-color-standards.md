# Accessibility And Color Standards

Use this reference for all publication, thesis, and presentation figures that use colour, symbols, dense labels, or figures intended for PDF/HTML distribution.

## Colour Semantics

Before choosing a palette, define each colour role:

```text
Category or quantity:
Meaning:
Colour:
Non-colour cue:
Used in panels:
```

Rules:

- One meaning should keep the same colour across the whole figure.
- Use neutral colours for context and a small number of saturated colours for emphasis.
- Reserve red/green for signed changes only when there is also a non-colour cue.
- Do not use a rainbow palette for unordered categories.
- Avoid coloured text; use black or near-black labels unless text is part of a channel label on a dark image plate.

## Non-Colour Redundancy

Colour alone must not carry essential meaning. Add at least one redundant cue when distinctions matter:

- line style: solid, dashed, dotted;
- marker shape;
- direct label;
- hatch or texture for bars;
- position or grouping;
- annotation text;
- grayscale luminance difference.

## Grayscale And Colour-Blind Checks

Before final delivery:

- convert or preview the figure in grayscale when practical;
- confirm categories remain separable without hue;
- check that text and markers have enough luminance contrast against backgrounds;
- avoid red/green pairs as the only distinction;
- use a colour-blind-aware palette by default for categorical data.
- when colour encodes categories, pair it with line style, marker shape, hatch, direct labels, or grayscale contrast so the figure still works in monochrome.

## Figure Descriptions And Alt Text

For ACM-like, Springer Nature-like, accessible PDF/HTML, or user-requested accessibility outputs, provide a figure description separate from the caption.

Description rules:

- State the figure's function and key information, not every decorative detail.
- Use manuscript terminology.
- Go from overview to key details.
- Do not repeat the caption verbatim.
- Write out abbreviations when needed for accessibility.
- Mention colour only when colour itself carries meaning in the manuscript.

Output field:

```text
Figure description / alt text:
```

If the target workflow auto-generates alt text, treat it as a draft that must be checked by the author or agent against the actual figure.

## Visual Accessibility Anti-Patterns

Reject or revise:

- low-contrast labels on coloured fills;
- tiny labels that disappear at column width;
- colour-only legends;
- legends far from the marks they explain when direct labels would work;
- dense heatmaps without scale, units, or a readable colour bar;
- flowcharts where arrow direction is ambiguous;
- screenshots with unreadable UI text.

## Source Basis

This standard is based on Nature accessibility guidance, Springer Nature alt-text requirements, ACM figure-description guidance, SIGACCESS examples, and IEEE advice to pair colour with shape or other cues.
