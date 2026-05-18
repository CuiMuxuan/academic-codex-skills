---
name: academic-figure-workflow
description: "Plan, create, revise, and validate academic figures for papers, theses, dissertations, and technical reports. Use for SVG mechanism diagrams, conceptual models, Nature-grade multi-panel Matplotlib figures, data-driven plots, draw.io engineering diagrams, workflow charts, use-case diagrams, architecture diagrams, tables-as-figures, figure captions, and user-confirmed OpenAI image generation. Chinese triggers: 论文作图, 机理图, SVG绘图, Nature风格多面板图, matplotlib作图, drawio流程图, 用例图, 架构图, 大模型绘图API."
---

# Academic Figure Workflow

Use this skill for academic and thesis figures. Choose the drawing method by figure type, evidence needs, and reproducibility.

## Target Exemplar Intake

Before setting a figure style baseline, ask whether the user can provide 3-10 final target examples: accepted figures from the target journal, approved thesis figures, lab style guides, or supervisor-approved figures. Use them to infer panel density, typography, colour discipline, annotation style, and caption conventions. If none are available, use the generic academic baseline or the Nature-grade Matplotlib protocol when requested, and mark assumptions as provisional.

## Pre-Execution Material Request

Before drawing, plotting, generating, or exporting a figure, ask for missing materials that would materially improve figure quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for target examples, source data, statistics, code or repository facts, evidence table, rough sketch, journal/school figure guide, style constraints, existing figures, image-processing limits, output format, and AI-generation permission as relevant. If unavailable, stop at a figure spec, storyboard, or provisional template until the user confirms execution.

## Method Selection

Default choices:

| Figure type | Default method |
|---|---|
| Mechanism diagrams, conceptual models, moderately complex scholarly schematics | SVG |
| Workflow, use-case, module, architecture, ER/data-flow, software process diagrams | Draw.io |
| Data-driven plots or multi-panel quantitative figures | Matplotlib Nature-grade protocol with source data, editable SVG/PDF export, and final raster preview |
| Photorealistic, illustrative, texture-like, or hard-to-specify visual assets | OpenAI image generation after user confirmation |
| Simple numeric comparison | Native table or chart in manuscript tool |

Prefer reproducible vector outputs for academic submission.

## OpenAI Image Generation Gate

Before using OpenAI image generation:

1. Explain why SVG, Draw.io, or charting is insufficient.
2. Ask the user for explicit confirmation.
3. Confirm that the current environment can access the OpenAI image generation API or native image-generation tool.
4. Clarify output requirements: style, dimensions, transparency, labels, and whether text should be added afterward as vector text.
5. Record that the image is AI-generated if the target publication or school requires disclosure.

Do not call image generation silently.

## Core Rules

1. Draw only what the evidence, codebase, experiment, or user-approved concept supports.
2. Keep figure labels concise and consistent with manuscript terminology.
3. Prefer editable source files: `.svg` for SVG and `.drawio` for Draw.io.
4. Export publication formats only after the source figure is accepted.
5. Avoid decorative complexity that reduces academic readability.
6. Include captions or caption drafts when requested.
7. If a figure cannot be drawn faithfully, mark it as unresolved instead of inventing content.
8. Make every panel serve a scientific claim, method step, result contrast, or design decision. Remove elements that only make the figure look richer.

## Figure Argument Contract

For complex, submission-bound, multi-panel, or data-backed figures, define the figure's argument before drawing:

```text
Main claim:
Evidence hierarchy:
Panel roles:
Non-redundant message per panel:
Drawing method:
Editable source:
Export targets:
Open decisions:
```

Rules:

- Every panel or major element must support a specific claim, method step, comparison, or design decision.
- If two panels communicate the same message, merge them or explain the distinction before drawing.
- For data-backed plots, record the data source, analysis status, statistics/uncertainty status, and whether values are provided or still pending.
- For image-based figures, record permitted image processing, scale bars, annotations, and any manipulation or disclosure requirement.
- If the evidence hierarchy is incomplete, stop at a spec or storyboard instead of producing a final-looking figure.

Quality gate:

| Gate | Pass condition |
|---|---|
| Claim clarity | The figure can be summarized in one defensible manuscript claim. |
| Panel necessity | Each panel has a non-redundant role. |
| Evidence trace | Every plotted value, label, node, arrow, or annotation traces to data, code, manuscript text, or user-approved facts. |
| Editability | Source files remain editable and text is not unnecessarily outlined. |
| Submission fit | Size, typography, colour, and annotation density fit the target journal or thesis context. |

## Intake

Collect:

- Figure purpose and target chapter or section.
- Audience and language.
- Required method if the user has one.
- Source facts: text, evidence table, codebase facts, data columns, equations, or rough sketch.
- Source data, statistics, image-processing constraints, or codebase trace when the figure is evidence-backed.
- Output format: SVG, Draw.io, PNG, PDF, DOCX insertion, or source plus export.
- Style constraints: grayscale, journal style, school template, color restrictions, font, size.
- Whether AI image generation is allowed for this figure.

## Workflow

### 1. Define Figure Specification

Create a compact spec:

- Figure title.
- Claim or process the figure supports.
- Inputs and evidence sources.
- Elements and relationships.
- Drawing method.
- Output files.
- Validation checks.

For complex figures, stop for user confirmation before drawing.

### 2. SVG Mechanism Or Concept Figure

Use SVG when the figure needs precise academic shapes, arrows, layers, equations, labels, or mechanisms.

Guidelines:

- Use semantic grouping.
- Keep dimensions stable with a viewBox.
- Use vector text when labels must remain editable.
- Keep color palette restrained and color-blind aware.
- Use line endings, arrowheads, and labels consistently.
- Place bilingual labels only when required and avoid crowded dual-language text.

Validate that the SVG opens, text fits, and labels do not overlap.

### 2.5. Nature-Grade Matplotlib Multi-Panel Figure

Use this module when the user asks for a Nature-style, Nature-grade, journal-ready, or multi-panel Matplotlib figure.

First create a panel architecture table:

| panel | claim | data source | plot type | semantic colour role | required annotation | redundancy check |
|---|---|---|---|---|---|---|
| a | one non-redundant message | file/table/column | scatter/line/bar/image/etc. | control/treatment/model/uncertainty/highlight | label, scale bar, statistic, or none | unique/merge/revise |

Execution rules:

1. Use `scripts/make_nature_multipanel.py` when the user provides a panel spec and source data; use `scripts/nature_mpl_style.py` when writing a custom plot script.
2. Size figures in millimetres: 89 mm single column, 183 mm double column, maximum 170 mm height unless the target journal guide says otherwise.
3. Use editable vector text: `svg.fonttype = "none"`, `pdf.fonttype = 42`, `ps.fonttype = 42`.
4. Use Arial or Helvetica-compatible sans-serif fonts; keep normal text between 5 pt and 7 pt, and panel labels as 8 pt bold lowercase letters.
5. Include axis lines and tick marks; label all axes with units in parentheses when units exist.
6. Avoid background gridlines, drop shadows, decorative icons, patterns, coloured text, overlapping text, and rainbow or red/green-dependent palettes.
7. Use a semantic colour map before plotting: assign each colour to a role such as `control`, `treatment`, `model`, `uncertainty`, `negative`, `positive`, or `highlight`; do not use colour merely for decoration.
8. Use the Wong/Nature colour-blind-safe palette by default unless the user or journal guide provides a stricter palette.
9. Export at minimum: editable `.svg`, editable `.pdf`, and a `.png` preview. Keep the plotting script and source data path with the outputs.
10. Inspect the exported SVG or PDF text when possible; if text is outlined, rerun export before claiming the figure is ready.
11. Check that every statistical annotation has a visible source: test name, n, uncertainty definition, and multiple-comparison handling when relevant.
12. When reproducing a benchmark-style figure, match its scientific function and density rather than copying its visual design.

For executable multi-panel plots, create a CSV or JSON panel spec with these fields before running the generator:

```text
panel,claim,data,plot_type,x,y,yerr,group,color_role,title,xlabel,ylabel,annotation
```

Run the generator only after source data and panel claims are available:

```bash
python scripts/make_nature_multipanel.py --spec panel_spec.csv --data-root data --output-dir figures --stem fig1 --column double
```

Treat a non-empty QA issue list as unresolved until inspected. The generated figure is not Nature-grade if the SVG lacks editable text, the panel claims are duplicated, source data are missing, or labels overlap.

Matplotlib output packet:

```text
Source data:
Plot script:
Panel architecture:
Figure size:
Palette roles:
Editable exports:
Raster preview:
QA checks:
Unresolved issues:
```

### 3. Draw.io Engineering Diagram

Use Draw.io for:

- System architecture.
- Runtime workflow.
- Use-case diagrams.
- Module design.
- Data-flow and storage diagrams.
- Code-backed thesis diagrams.

Rules:

- Base nodes and edges on real repository behavior or user-confirmed design.
- Use one page per diagram topic.
- Prefer uncompressed Draw.io XML when generating files for easier review.
- Keep page names close to manuscript subsection names.
- Avoid services, databases, or modules that do not exist.
- For code-backed diagrams, cite the files, modules, routes, tables, or functions that justify major nodes and edges in the final note.

### 4. AI-Generated Image

Use only after the gate above. Prefer AI generation for visual assets where strict factual geometry is not required. For academic diagrams with factual labels, generate the base image without text when possible, then add labels in SVG or another editable vector layer.

### 5. Caption And Manuscript Integration

For each figure, provide:

- Figure source file.
- Export file if generated.
- Caption draft.
- Placement recommendation.
- Notes on evidence, assumptions, or manual checks.

## Validation

Before finishing:

- Open or inspect generated source files when possible.
- Check label overlap and readability.
- Confirm the method matches the figure type.
- Confirm code-backed diagrams match actual implementation.
- Trace each panel, node, edge, label, plotted value, or annotation back to the approved source facts.
- Confirm exported files match the editable source and note any manual export or Word refresh still required.
- Confirm figure numbering or caption style is deferred to formatting if not known.
- For multi-panel figures, verify that panel labels, axes, legends, scale bars, uncertainty, and captions tell the same story and do not contradict the manuscript.
- List unresolved scientific, data, style, or export issues separately instead of calling the figure submission-ready.

## Reference

Read [figure-method-selection.md](references/figure-method-selection.md) for detailed method-choice rules and validation checks.

## Bundled Utilities

- `scripts/make_nature_multipanel.py`: execution script for Nature-style multi-panel Matplotlib figures from a panel spec and source CSV/image data. Exports editable SVG/PDF, PNG preview, and QA reports.
- `scripts/nature_mpl_style.py`: shared Nature-style Matplotlib defaults, semantic palette, panel labels, sizing helpers, and export helpers.
