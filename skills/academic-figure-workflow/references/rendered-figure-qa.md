# Rendered Figure QA

Use this reference after creating or revising any submission-quality plot, diagram, multi-panel figure, table-as-figure, or image plate. The goal is to inspect the rendered artifact, not only the source code.

## QA Loop

1. Export or render a PNG preview at the intended final size.
2. Inspect the preview visually with `view_image` or an equivalent image viewer.
3. Check vector/editable exports separately when SVG/PDF/DRAWIO outputs are required.
4. Fix layout, fonts, labels, colour, and export settings in the source.
5. Re-render and inspect again.
6. Stop after the figure passes or after three failed loops; if three loops fail, reconsider chart type, panel density, or figure scope.

Do this loop before calling the figure final. For data plots, run this after applying `data-visualization-advisor.md`.

## Programmatic Checks

When Matplotlib or another script generated the figure, inspect what can be checked deterministically:

- missing source files, empty data, or failed plot panels;
- text overlap using bounding boxes when available;
- warnings about missing glyphs, font fallback, or layout failure;
- SVG text editability (`<text>` exists when editable text is expected);
- PDF font embedding when tooling is available;
- raster preview dimensions and DPI metadata;
- final physical size compared with target width/height;
- colorbar existence for continuous color encodings;
- duplicate panel labels or missing panel labels;
- non-empty QA issue lists from bundled scripts.

Treat programmatic warnings as unresolved until inspected, not as harmless console noise.

## Visual Inspection Checklist

Inspect the rendered preview at the intended final width, then answer:

- Are all labels, ticks, legends, arrows, scale bars, panel letters, and in-panel annotations readable?
- Are any labels clipped, wrapped badly, hidden behind axes, or outside the figure boundary?
- Are Chinese characters, minus signs, Greek symbols, superscripts, subscripts, and units rendered correctly?
- Does any legend, colorbar, inset, annotation, or panel label cover data?
- Are panel labels aligned consistently and placed at the visual start of each panel?
- Are axes, baselines, and comparable panels aligned?
- Is the reading order obvious within five seconds?
- Does the figure still work in grayscale or for common color-vision deficiencies?
- Are category colors consistent across panels?
- Are continuous color scales perceptually appropriate and labeled with units/meaning?
- Are image panels free from distorted aspect ratios, missing scale bars, or unexplained crops?
- Does any panel look like decorative filler rather than evidence for the figure argument?

## Common Fixes

| problem | preferred fix |
|---|---|
| missing CJK glyphs or square boxes | choose an installed CJK font, refresh font cache if needed, set Matplotlib `axes.unicode_minus = False` |
| clipped text | increase margins, shorten labels, rotate only when necessary, or export with tight bounding box |
| legend covers data | move legend outside axes, use a shared legend, or direct-label lines/regions |
| dense tick labels | reduce tick count, abbreviate labels, split panels, or use horizontal bars |
| panel labels drift | place labels with a shared helper or figure-level coordinates |
| colorbar crowds plot | allocate a dedicated colorbar axis or use a shared colorbar |
| color-only encoding fails grayscale | add marker shape, line style, hatch, direct labels, or faceting |
| too many categories | split into panels or choose a summary figure plus supplementary detail |
| small-n aggregate hides data | show individual points and use robust summaries |
| one figure carries multiple claims | split figures or remove panels that serve a different argument |

## Vector And Raster Verification

For SVG/PDF outputs:

- open or inspect the file when possible;
- confirm text remains editable unless the venue requires outlines;
- confirm strokes, arrows, markers, symbols, and labels survive export;
- confirm hidden/off-canvas objects are not present;
- confirm the figure does not include captions, author names, operation notes, file paths, or prompt traces.

For raster outputs:

- confirm source resolution is sufficient at final size;
- avoid JPEG for line art, plots, and text-heavy figures unless a portal explicitly requires it;
- confirm no compression artifacts damage axes, text, or data marks.

## QA Result Format

Report:

```text
Rendered preview:
Preview inspected: yes/no
Visual QA result: pass/fail
Programmatic checks:
Vector/editability checks:
Issues fixed:
Remaining issues:
Next action:
```

If visual QA is not possible in the environment, say so and leave the figure as draft or unverified rather than submission-ready.
