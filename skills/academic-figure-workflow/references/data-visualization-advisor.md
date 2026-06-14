# Data Visualization Advisor

Use this reference when the user provides data and asks what chart to use, asks for a paper-ready plot, requests Matplotlib/Seaborn/Plotly work, or specifies a chart type that may not fit the data.

This reference is for data-backed plots only. Use the SVG/Draw.io references for mechanism diagrams, conceptual schematics, workflows, and architecture figures.

## Advisor Workflow

1. Identify the figure argument before plotting.
2. Inspect the data structure before choosing a chart.
3. Recommend one primary chart and one or two defensible alternatives.
4. Intercept chart choices that would misrepresent the data.
5. Draw at final physical size using publication defaults.
6. Render a preview and run the visual QA loop before final export.

If the user has not stated the figure argument, ask one concise question or infer a provisional argument from the manuscript context and label it as an assumption.

## Data Profiling Checklist

Before selecting a chart, inspect or summarize:

| item | why it matters |
|---|---|
| columns and units | axis labels, grouping, and caption wording |
| variable types | determines plot family |
| sample size overall and per group | controls whether aggregate charts are acceptable |
| missing values | may require filtering notes or missingness visualization |
| distribution shape | skew, heavy tails, bimodality, and log-scale needs |
| outliers | decide whether to show individual points, robust summaries, or axis treatment |
| group balance | affects comparisons and uncertainty display |
| repeated measures or pairing | requires paired lines, connected dots, or mixed-model/statistical notes |
| correlation structure | informs scatter, pair plot, correlation matrix, or dimensionality reduction |
| number of categories | determines whether to split panels rather than crowd a legend |

When source data are available, prefer a small profiling script or notebook cell that prints column dtypes, row counts, missingness, group counts, descriptive statistics, and candidate warnings. Do not silently coerce identifiers into continuous numeric variables.

## Argument To Chart Mapping

| user argument | default chart | avoid |
|---|---|---|
| show a single continuous distribution | histogram/KDE, rug, box, or violin | bar chart |
| compare groups with small n per group | dot/strip plot, optionally with box summary | mean-only bar |
| compare groups with moderate/large n | box/violin plus points or mean/CI when justified | hiding all raw points when n is small |
| show a trend over ordered x, time, dose, or iteration | line with points and uncertainty band | bars for dense ordered x |
| show relationship between two continuous variables | scatter with fit or confidence band when justified | line plot for unordered x |
| show matrix or correlation pattern | heatmap with labeled colorbar | 3D surface or rainbow heatmap |
| show many metrics or datasets | faceted/multi-panel layout | one overstuffed panel |
| show composition | stacked bar or small multiples | pie chart unless venue/user explicitly requires it |
| show benchmark or ablation comparison | ordered bar/dot plot, matrix, or line trend | colour-only emphasis of the proposed method |

## Intercept Rules

When a requested chart triggers one of these conditions, explain the risk and offer a better option before drawing:

- `n < 10` per group and the user asks for a mean-only bar chart.
- unrelated variables are requested on dual y-axes.
- categorical x-values are connected with a line that implies continuity.
- a pie, 3D pie, 3D bar, or decorative chart is requested for exact comparison.
- a proportional or count bar uses a truncated y-axis without explicit justification.
- a continuous color mapping lacks a colorbar with label and unit.
- rainbow/jet palettes are used for quantitative values.
- red/green is the only category distinction.
- statistical stars are requested without test, n, comparison, and correction plan.
- more than roughly 12 category combinations are packed into one legend or axis.
- the figure attempts to support more than one main claim.

Respect the user's final decision after warning them, but record the unresolved risk in the output packet.

## Publication Plot Defaults

- Set the figure size to the final manuscript size before plotting.
- Prefer editable SVG/PDF for plots; use PNG only as preview or when the destination requires raster.
- Use `svg.fonttype = "none"`, `pdf.fonttype = 42`, and `ps.fonttype = 42` for Matplotlib.
- Use color-blind-safe palettes and add line style, marker, hatch, direct label, or grayscale redundancy when categories matter.
- Make axis labels carry units when units exist.
- Keep titles out of the plotting area unless the venue or standalone figure format requires them.
- Put long interpretation in the caption, not inside the axes.
- State uncertainty type and sample size in the caption or figure note.

## Chinese And Bilingual Plots

For Chinese or bilingual figure text:

- check for an installed CJK-capable font before plotting;
- prefer Noto Sans CJK SC, Source Han Sans SC, Microsoft YaHei, SimHei, or SimSun according to the target style;
- set `axes.unicode_minus = False` in Matplotlib to prevent minus-sign boxes;
- verify rendered PNG previews for missing glyph boxes, mixed-language spacing, and clipped Chinese labels;
- for Chinese thesis/journal figures, use the target guide when it specifies Songti/SimSun, Heiti, Times New Roman, or mixed Chinese-English typography.

## Output Recommendation Format

Before plotting, report:

```text
Figure argument:
Data inspected:
Key data facts:
Recommended chart:
Why this chart:
Alternatives:
Rejected/unsafe chart types:
Source-data or evidence gaps:
```

After plotting, include the export packet from `export-and-editability-standards.md` plus the rendered QA result from `rendered-figure-qa.md`.
