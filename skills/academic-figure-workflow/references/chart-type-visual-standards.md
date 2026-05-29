# Chart Type Visual Standards

Use this reference when choosing or polishing a data-backed plot, benchmark figure, ablation chart, heatmap, confusion matrix, or table-like figure.

## Universal Data Plot Rules

- State units in axis labels when units exist.
- State uncertainty meaning before plotting error bars or bands.
- Do not add statistical marks without test name, sample size or run count, and comparison meaning.
- Prefer source-data-driven scripts over manual chart editing.
- Use consistent category order across panels.
- Avoid chart junk: shadows, gradients, 3D bars, decorative icons, and heavy grid backgrounds.

## Bars

Use for discrete comparisons, not continuous trends.

- Keep a clear zero baseline unless a justified truncated axis is explicitly labelled.
- Prefer horizontal bars for long method names or ablation components.
- Use direct value labels sparingly; do not label every bar if axis reading is cleaner.
- For many methods, use one hue family plus alpha or lightness changes for related variants.
- Use hatch/line/marker redundancy when colour carries category meaning.

## Lines And Trends

Use for ordered x-values, time, training steps, or sample size trends.

- Keep line identities consistent across panels.
- Use uncertainty bands with low alpha when uncertainty is available.
- Use markers only when sample points matter or lines overlap.
- Use sparse tick marks and avoid dense grids.
- Place a shared legend above or beside the group when several panels reuse the same methods.

## Scatter And Embeddings

Use for point-level relationships or projected spaces.

- Avoid overplotting by using alpha, smaller markers, density contours, or hexbin summaries.
- State whether axes are meaningful dimensions, embeddings, or arbitrary projections.
- Do not imply clusters are real categories unless the analysis supports that claim.
- Label highlighted groups directly when there are only a few.

## Heatmaps And Matrices

Use for dense matrix-like relationships.

- Include a readable colour bar with units or score definition.
- Choose sequential, diverging, or categorical palettes according to the data type.
- Keep missing values visually distinct from low values.
- Use text inside cells only when the matrix is small enough at final size.
- For confusion matrices, state whether values are counts, row-normalized, column-normalized, or percentages.

## Ablation And Benchmark Figures

- Group baselines, variants, and the proposed method consistently.
- Encode improvement direction unambiguously.
- Keep the same metric direction across panels; if higher/lower changes, label it.
- Do not use colour to make a method look better than the data justify.
- Include run count, split, dataset, and metric definition in the caption or support note.

## Tables As Figures

Use only when visual comparison is stronger than a native table.

- Keep typography consistent with the manuscript.
- Use subtle rules, not heavy cell borders.
- Align numbers by decimal point when practical.
- Highlight only the values that support the figure's claim.
- Keep the source table or structured data available.

## Source Basis

This reference adapts high-impact figure design patterns, Nature/PLOS readability constraints, and common ML/engineering paper plotting standards into chart-specific checks.
