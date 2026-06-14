# Nature Matplotlib Protocol

Use this reference when the user asks for a Nature-style, Nature-grade, journal-ready, or multi-panel Matplotlib figure.

## Panel Architecture

Create this table before plotting:

| panel | claim | data source | plot type | semantic colour role | required annotation | redundancy check |
|---|---|---|---|---|---|---|
| a | one non-redundant message | file/table/column | scatter/line/bar/image/etc. | control/treatment/model/uncertainty/highlight | label, scale bar, statistic, or none | unique/merge/revise |

For executable multi-panel plots, create a CSV or JSON panel spec with:

```text
panel,claim,data,plot_type,x,y,yerr,group,color_role,title,xlabel,ylabel,annotation
```

## Execution Rules

1. Use `scripts/make_nature_multipanel.py` when the user provides a panel spec and source data; use `scripts/nature_mpl_style.py` when writing a custom plot script.
2. Size figures in millimetres: 89 mm single column, 183 mm double column, maximum 170 mm height unless the target journal guide says otherwise.
3. Use editable vector text: `svg.fonttype = "none"`, `pdf.fonttype = 42`, `ps.fonttype = 42`.
4. Use Arial or Helvetica-compatible sans-serif fonts for English figures; for Chinese or bilingual figures, select an installed CJK font and fix minus-sign rendering before export.
5. Keep normal text between 5 pt and 7 pt, and panel labels as 8 pt bold lowercase letters.
6. Include axis lines and tick marks; label all axes with units in parentheses when units exist.
7. Avoid background gridlines, drop shadows, decorative icons, patterns, coloured text, overlapping text, and rainbow or red/green-dependent palettes.
8. Use a semantic colour map before plotting: assign each colour to a role such as `control`, `treatment`, `model`, `uncertainty`, `negative`, `positive`, or `highlight`.
9. Use the Wong/Nature colour-blind-safe palette by default unless the user or journal guide provides a stricter palette.
10. Export at minimum: editable `.svg`, editable `.pdf`, a final-size `.png`, and a lower-DPI rendered preview for QA. Keep the plotting script and source data path with the outputs.
11. Inspect exported SVG or PDF text when possible; if text is outlined or clipped, rerun export before calling the figure ready.
12. Check that every statistical annotation has a visible source: test name, n, uncertainty definition, and multiple-comparison handling when relevant.
13. When reproducing a benchmark-style figure, match scientific function and density rather than copying visual design.

## Run Command

Run only after source data and panel claims are available:

```bash
python scripts/make_nature_multipanel.py --spec panel_spec.csv --data-root data --output-dir figures --stem fig1 --column double
```

Treat a non-empty QA issue list as unresolved until inspected. If the rendered preview fails, the figure is not Nature-grade yet.

## Output Packet

```text
Source data:
Plot script:
Panel architecture:
Figure size:
Palette roles:
Editable exports:
Raster preview:
Rendered preview:
QA checks:
Unresolved issues:
```

The generated figure is not Nature-grade if the SVG lacks editable text, the panel claims are duplicated, source data are missing, statistical annotations lack sources, or labels overlap.
