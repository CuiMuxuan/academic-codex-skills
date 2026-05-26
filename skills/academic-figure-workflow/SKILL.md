---
name: academic-figure-workflow
description: "Plan, create, revise, and validate academic figures for papers, theses, dissertations, and technical reports. Use for SVG mechanism diagrams, conceptual models, Nature-grade multi-panel Matplotlib figures, data-driven plots, draw.io engineering diagrams, workflow charts, use-case diagrams, architecture diagrams, tables-as-figures, figure captions, and user-confirmed OpenAI image generation. Chinese triggers: 论文作图, 机理图, SVG绘图, Nature风格多面板图, matplotlib作图, drawio流程图, 用例图, 架构图, 大模型绘图API."
---

# Academic Figure Workflow

Use this skill for academic and thesis figures. Choose the method by figure type, evidence needs, editability, and reproducibility.

## Boundaries

Do:

- Plan figure claims, panels, captions, source files, and exports.
- Create SVG mechanism figures, Draw.io engineering diagrams, and reproducible Matplotlib figures.
- Validate that every visual element traces to evidence, data, code, manuscript text, or user-approved facts.

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
| Data-driven plots or multi-panel quantitative figures | Matplotlib Nature-grade protocol with source data, editable SVG/PDF export, and final raster preview |
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

## Workflow

1. Define the figure claim, target section, source facts, method, output files, and validation checks.
2. For complex, multi-panel, submission-bound, code-backed, or data-backed figures, apply [figure-argument-contract.md](references/figure-argument-contract.md).
3. For Nature-style or multi-panel Matplotlib figures, apply [nature-matplotlib-protocol.md](references/nature-matplotlib-protocol.md).
4. For SVG mechanism diagrams or Draw.io engineering diagrams, apply [svg-and-drawio-diagrams.md](references/svg-and-drawio-diagrams.md).
5. For AI-generated bitmap assets, apply [ai-image-generation-gate.md](references/ai-image-generation-gate.md) before generation.
6. Provide the editable source, exports if generated, caption draft, placement recommendation, evidence/code trace, and unresolved issues.

## Validation

Before finishing:

- confirm the method matches the figure type;
- inspect generated source files when possible;
- check label overlap, readability, export integrity, and editability;
- trace each panel, node, edge, label, plotted value, or annotation back to approved source facts;
- confirm code-backed diagrams match actual implementation;
- defer figure numbering or final caption style to formatting when the target format is not known;
- list unresolved scientific, data, style, or export issues separately.

## Reference

Read [figure-method-selection.md](references/figure-method-selection.md) for method-choice rules.

Read [figure-argument-contract.md](references/figure-argument-contract.md) for complex, evidence-backed, multi-panel, or submission-bound figures.

Read [nature-matplotlib-protocol.md](references/nature-matplotlib-protocol.md) for Nature-grade Matplotlib figures.

Read [svg-and-drawio-diagrams.md](references/svg-and-drawio-diagrams.md) for mechanism diagrams, conceptual SVGs, architecture diagrams, and code-backed Draw.io diagrams.

Read [ai-image-generation-gate.md](references/ai-image-generation-gate.md) before using AI image generation.

## Bundled Utilities

- `scripts/make_nature_multipanel.py`: generate Nature-style multi-panel Matplotlib figures from a panel spec and source data; exports editable SVG/PDF, PNG preview, and QA reports.
- `scripts/nature_mpl_style.py`: shared Nature-style Matplotlib defaults, semantic palette, panel labels, sizing helpers, and export helpers.
