# Publication Visual Standards

Use this reference for journal-facing, thesis-final, supervisor-facing, or submission-quality figures before drawing or revising the visual layer.

## Default Target

When no stricter journal or school guide is supplied, use a conservative high-impact-journal default:

| Element | Default |
|---|---|
| Page width | single-column 89 mm or double-column 183 mm when targeting Nature-like layouts |
| Maximum figure height | keep at or below 170 mm when imitating Nature-like final artwork |
| Typeface | Arial or Helvetica-compatible sans serif for figure labels |
| Final-size text | 5-7 pt for Nature-like dense figures; 8-12 pt when following PLOS-like requirements |
| Panel letters | lowercase bold, consistent position, no decorative boxes |
| Lines and strokes | visible at final size; do not use faint lines; keep line art at least 0.3 pt when no venue-specific value is known |
| Background | white for plots and diagrams; black only for image plates where the data convention requires it |
| Colour space | RGB unless the target journal explicitly says otherwise |

If the target venue gives a different rule, follow the venue and report the difference.

## Visual Hierarchy

1. Give the figure one main claim before styling.
2. Allocate the largest visual area to the panel that carries the main claim or the first reading step.
3. Make supporting panels smaller, quieter, and visually subordinate.
4. Prefer direct labels when the eye would otherwise travel repeatedly between a legend and fixed objects.
5. Use one shared legend for a row or figure when multiple panels use the same categories.
6. Avoid repeated legends, repeated axis labels, repeated colour keys, and duplicated panel messages.

## Readability At Final Size

Before calling a figure ready:

- inspect it at the intended print width, not only at full-screen zoom;
- inspect a DOCX/PDF insertion preview when the figure is meant for a manuscript or thesis;
- inspect a rendered PNG preview before final export for any submission-quality figure;
- ensure figure text does not look smaller than the surrounding body text after insertion, unless the target venue explicitly requires a smaller final-size font;
- ensure every label, tick, arrow label, legend entry, and panel letter remains legible;
- remove or rewrite labels that require shrinking below the selected standard;
- use shorter manuscript terminology rather than wrapping long prose inside the figure;
- avoid placing important text on saturated colours or busy image regions;
- keep text horizontal unless the axis or layout genuinely requires rotation.

## Figure-Internal Text Filter

Text inside the figure should be limited to what helps interpret the visual object:

- keep panel letters, axis labels, ticks, legends, node labels, short arrow labels, scale bars, and essential in-panel annotations;
- remove manuscript captions, figure titles, author notes, implementation TODOs, prompt traces, operation logs, file paths, draft comments, and explanatory paragraphs;
- move long explanations, limitations, source notes, and interpretation into the caption, main text, methods, appendix, or supplement;
- when a text label is needed but too long, shorten the label and define it in the caption or legend;
- for graphical abstracts, default to no formal reference citations inside the visual; if the target journal explicitly allows or requires a citation, or the abstract must directly identify specific prior work, follow the target style and keep the visual independently readable.

## Spacing And Alignment

- Align panels to a clear grid unless an asymmetric hero layout improves the scientific reading path.
- Keep gutters narrow but real; increase gutters between dark image plates and light plot panels.
- Use whitespace to group related panels; do not add decorative frames simply to show grouping.
- Keep arrow routes simple; prefer left-to-right or top-to-bottom reading for process figures.
- Avoid line crossings. If crossings are unavoidable, split the diagram or use lanes.

## Academic Anti-Patterns

Reject or revise figures that contain:

- decorative icons that do not encode information;
- colour gradients used only for style;
- rainbow palettes for categorical data;
- red/green distinctions without a non-colour cue;
- boxed panel letters;
- chart titles inside the figure when the caption/manuscript should provide the title;
- captions, figure numbers, author names, or article titles embedded inside the figure file;
- project notes, operation logs, TODOs, source-file comments, or revision instructions inside the figure;
- rasterized text in vector-style diagrams or plots;
- dense labels that make the figure unreadable after insertion into DOCX/PDF.
- missing CJK font support or minus-sign boxes in Chinese or bilingual figures.

## Source Basis

This standard is derived from publicly available guidance from the Nature Research Figure Guide, PLOS figure requirements, Springer Nature artwork guidance, Elsevier artwork instructions, IEEE Author Center graphics guidance, and design/QA patterns from the referenced `nature-figure` skill. Treat this as a default floor, not a substitute for the exact target journal guide.
