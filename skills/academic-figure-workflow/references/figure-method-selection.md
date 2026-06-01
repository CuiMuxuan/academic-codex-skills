# Figure Method Selection

Use this reference when a figure could be created in more than one way.

## SVG Is Preferred For

- Mechanism diagrams.
- Conceptual models.
- Layered theoretical frameworks.
- Equations plus arrows or process states.
- Diagrams that require precise labels and reproducible editing.

Validation:

- SVG opens.
- Text fits and does not overlap.
- Arrowheads and labels are consistent.
- The visual claim matches manuscript evidence.

## Draw.io Is Preferred For

- Flowcharts.
- Workflow and process diagrams.
- Use-case diagrams.
- System architecture.
- Module diagrams.
- Data-flow or storage diagrams.
- Code-backed engineering diagrams for theses.

Validation:

- Nodes represent real or user-confirmed entities.
- Edges represent real flow or dependency.
- Page names match target sections.
- No unsupported system layer appears.
- The `.drawio` source path is reported with any exported SVG/PDF/PNG preview.
- If the user manually edited the `.drawio` source, that edited style remains the baseline unless a redraw is explicitly requested.

## OpenAI Image Generation Is Reserved For

- Photorealistic or illustrative assets.
- Visual metaphors where exact geometry is not the scholarly claim.
- Texture, scene, or cutout assets used as supporting visuals.

Required gate:

- User confirmation.
- API availability confirmation.
- Disclosure check for school or publication rules.

## Method Decision Template

```text
Figure:
Purpose:
Evidence/source facts:
Recommended method:
Why:
Output source file:
Validation checks:
Needs user confirmation:
```

## Submission-Quality Checks

Use these checks before calling a figure final:

- The figure has one main scientific or technical claim.
- Every panel has a distinct job and no panel is decorative filler.
- Labels use manuscript terminology exactly.
- Colours have semantic roles and remain interpretable in grayscale or colour-blind-safe viewing when possible.
- Data-backed panels state units, uncertainty meaning, sample size, and statistical test when relevant.
- Code-backed diagrams name the source files or modules that justify the main structure.
- Editable source files are preserved alongside exported preview files.

If any check fails, report the figure as a draft/specification and name the unresolved issue.
