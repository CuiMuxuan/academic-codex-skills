---
name: academic-figure-workflow
description: "Plan, create, revise, and validate academic figures for papers, theses, dissertations, and technical reports. Use for SVG mechanism diagrams, conceptual models, Nature-grade multi-panel Matplotlib figures, data-driven plots,正文 figure interpretation handoff, draw.io engineering diagrams, workflow charts, use-case diagrams, architecture diagrams, tables-as-figures, figure captions, publication visual standards, export/editability QA, accessibility/color checks, and user-confirmed OpenAI image generation. Chinese triggers: 论文作图, 机理图, SVG绘图, Nature风格多面板图, matplotlib作图, 数据图正文分析, 图的作用阐释, drawio流程图, 用例图, 架构图, 论文插图标准, 图片投稿标准, 大模型绘图API."
---

# Academic Figure Workflow

Use this skill for academic and thesis figures. Choose the method by figure type, evidence needs, editability, and reproducibility. For data-backed plots, also prepare the paragraph-level figure argument so正文 text can explain the plot's purpose, quantitative pattern, and implication.

## Boundaries

Do:

- Plan figure claims, panels, captions, source files, and exports.
- Create SVG mechanism figures, Draw.io engineering diagrams, and reproducible Matplotlib figures.
- Validate that every visual element traces to evidence, data, code, manuscript text, or user-approved facts.
- For data-backed plots, act as a visualization advisor first: inspect the data and figure argument before choosing or drawing a chart.

Do not:

- Invent data, mechanisms, system modules, experimental results, labels, or visual evidence.
- Use AI image generation without the explicit gate in `ai-image-generation-gate.md`.
- Call a figure submission-ready when labels overlap, source files are missing, or evidence trace is incomplete.

## Intake

Collect:

- figure purpose and target chapter or section;
- audience and manuscript language;
- source facts: text, evidence table, codebase facts, data columns, equations, or rough sketch;
- target examples, journal/school guide, or lab style guide when available;
- target venue stage: draft, thesis insertion, initial submission, final accepted artwork, or repository supplement;
- output format: SVG, Draw.io, PNG, PDF, DOCX insertion, or source plus export;
- style constraints: grayscale, journal style, school template, colour restrictions, font, size;
- AI image generation permission when relevant.

Before drawing, plotting, generating, or exporting, ask for missing materials that would materially improve figure quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

If key evidence is missing, stop at a figure specification, storyboard, or provisional template until the user confirms execution.

## Method Selection

| Figure type | Default method |
|---|---|
| Mechanism diagrams, conceptual models, moderately complex scholarly schematics | SVG |
| Workflow, use-case, module, architecture, ER/data-flow, software process diagrams | Draw.io |
| Data-driven plots or multi-panel quantitative figures | Data-visualization advisor flow plus Matplotlib Nature-grade protocol with source data, editable SVG/PDF export, and final raster preview |
| Photorealistic, illustrative, texture-like, or hard-to-specify visual assets | OpenAI image generation after user confirmation |
| Simple numeric comparison | Native table or chart in manuscript tool |

Read [figure-method-selection.md](references/figure-method-selection.md) when a figure could be created in more than one way.

## Core Rules

1. Draw only what the evidence, codebase, experiment, or user-approved concept supports.
2. Make every panel serve a scientific claim, method step, result contrast, or design decision.
3. Prefer editable source files: `.svg` for SVG and `.drawio` for Draw.io.
4. Export publication formats only after the editable source is accepted.
5. Keep labels concise and consistent with manuscript terminology.
6. Record assumptions and unresolved evidence instead of filling gaps visually.
7. Ensure figure text remains readable at final DOCX/PDF insertion size and remove text that should not appear inside the figure.
8. Prefer Draw.io for workflow and process diagrams; preserve user-edited `.drawio` styling unless a redraw is explicitly requested.
9. Preserve formulas, superscripts/subscripts, and notation in labels, captions, tables-as-figures, and exports.

## Workflow

1. Define the figure claim, target section, source facts, method, output files, and validation checks.
2. For complex, multi-panel, submission-bound, code-backed, or data-backed figures, apply [figure-argument-contract.md](references/figure-argument-contract.md).
3. For submission-quality or journal-facing figures, apply [publication-visual-standards.md](references/publication-visual-standards.md), [export-and-editability-standards.md](references/export-and-editability-standards.md), and [accessibility-and-color-standards.md](references/accessibility-and-color-standards.md).
4. For data-backed plots, chart-choice questions, user-provided CSV/Excel/DataFrame files, or risky user-specified chart types, apply [data-visualization-advisor.md](references/data-visualization-advisor.md) before plotting.
   - For正文 narration of a data-backed plot, also apply the writing-workflow reference for data-figure body analysis so the manuscript states the figure role, best/worst region, concentration or sparsity, and supported conclusion.
6. For Nature-style or multi-panel Matplotlib figures, apply [nature-matplotlib-protocol.md](references/nature-matplotlib-protocol.md), [multi-panel-layout-patterns.md](references/multi-panel-layout-patterns.md), and [chart-type-visual-standards.md](references/chart-type-visual-standards.md).
7. For SVG mechanism diagrams or Draw.io engineering diagrams, apply [svg-and-drawio-diagrams.md](references/svg-and-drawio-diagrams.md); for Draw.io code-backed or engineering diagrams, also apply [drawio-engineering-diagram-standards.md](references/drawio-engineering-diagram-standards.md).
8. For image plates, photographs, microscopy, heatmaps over images, or mixed raster/vector panels, apply [image-panel-integrity.md](references/image-panel-integrity.md).
9. For AI-generated bitmap assets, apply [ai-image-generation-gate.md](references/ai-image-generation-gate.md) before generation.
10. When a venue-specific requirement, external visual example, or numeric artwork standard matters, apply [publisher-visual-source-map.md](references/publisher-visual-source-map.md) and verify the current official guide when possible.
11. Apply [notation-and-conversion-integrity-gate.md](../../shared/notation-and-conversion-integrity-gate.md) when figure labels, formulas, superscripts/subscripts, citations, or cross-references may be converted.
12. For any submission-quality generated or revised figure, apply [rendered-figure-qa.md](references/rendered-figure-qa.md) before calling it ready.
13. Provide the editable source, exports if generated, caption draft, placement recommendation, evidence/code trace, rendered QA result, and unresolved issues.

## Validation

Before finishing:

- confirm the method matches the figure type;
- inspect generated source files when possible;
- check label overlap, readability, export integrity, and editability;
- inspect a rendered PNG preview at intended final size for submission-quality figures;
- verify final-size readability, font consistency, line weight, colour meaning, grayscale or colour-blind-safe interpretation, and caption/description handoff when relevant;
- report the editable source path, especially `.drawio` paths for workflow diagrams;
- trace each panel, node, edge, label, plotted value, or annotation back to approved source facts;
- confirm code-backed diagrams match actual implementation;
- defer figure numbering or final caption style to formatting when the target format is not known;
- list unresolved scientific, data, style, or export issues separately.

## Reference

Read [figure-method-selection.md](references/figure-method-selection.md) for method-choice rules.

Read [figure-argument-contract.md](references/figure-argument-contract.md) for complex, evidence-backed, multi-panel, or submission-bound figures.

Read [publication-visual-standards.md](references/publication-visual-standards.md) for journal-facing typography, sizing, line weight, spacing, and visual hierarchy.

Read [export-and-editability-standards.md](references/export-and-editability-standards.md) for SVG/PDF/EPS/TIFF/PNG choice, editable text, embedded fonts, RGB, DPI, and file packaging.

Read [accessibility-and-color-standards.md](references/accessibility-and-color-standards.md) for colour-blind-safe design, grayscale checks, direct labels, contrast, and figure descriptions or alt text.

Read [data-visualization-advisor.md](references/data-visualization-advisor.md) before choosing or drawing data-backed plots from CSV/Excel/DataFrame files, when the user asks what chart to use, or when a requested chart type may be misleading.

Read [nature-matplotlib-protocol.md](references/nature-matplotlib-protocol.md) for Nature-grade Matplotlib figures.

Read [multi-panel-layout-patterns.md](references/multi-panel-layout-patterns.md) for hero panels, asymmetric layouts, shared legends, panel order, and anti-redundancy layout rules.

Read [chart-type-visual-standards.md](references/chart-type-visual-standards.md) for bars, lines, scatter, heatmaps, matrices, ablations, comparisons, and tables-as-figures.

Read [svg-and-drawio-diagrams.md](references/svg-and-drawio-diagrams.md) for mechanism diagrams, conceptual SVGs, architecture diagrams, and code-backed Draw.io diagrams.

Read [drawio-engineering-diagram-standards.md](references/drawio-engineering-diagram-standards.md) for Draw.io architecture, workflow, module, use-case, data-flow, and code-backed diagram conventions.

Read [notation-and-conversion-integrity-gate.md](../../shared/notation-and-conversion-integrity-gate.md) when figure text, notation, formulas, superscripts/subscripts, citations, or cross-references are converted across figure, manuscript, DOCX, PDF, SVG, or Draw.io outputs.

Read [image-panel-integrity.md](references/image-panel-integrity.md) for photographs, microscopy, image plates, raster panels, scale bars, crop/manipulation notes, and mixed raster/vector figures.

Read [ai-image-generation-gate.md](references/ai-image-generation-gate.md) before using AI image generation.

Read [publisher-visual-source-map.md](references/publisher-visual-source-map.md) when mapping standards to a specific publisher, journal family, venue, or external figure-standard source.

Read [rendered-figure-qa.md](references/rendered-figure-qa.md) after generating or revising a submission-quality figure to run the rendered-preview QA loop before final export or delivery.

## Bundled Utilities

- `scripts/make_nature_multipanel.py`: generate Nature-style multi-panel Matplotlib figures from a panel spec and source data; exports editable SVG/PDF, PNG preview, and QA reports.
- `scripts/nature_mpl_style.py`: shared Nature-style Matplotlib defaults, semantic palette, panel labels, sizing helpers, and export helpers.
