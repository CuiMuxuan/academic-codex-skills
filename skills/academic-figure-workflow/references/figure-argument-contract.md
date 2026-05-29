# Figure Argument Contract

Use this reference for complex, submission-bound, multi-panel, data-backed, code-backed, or evidence-sensitive figures.

Use the canonical `material_passport` and `claim_anchor` field names in [handoff-field-schema.md](../../../shared/handoff-field-schema.md) when figures consume shared project artifacts or support central manuscript claims.

## Contract

Before drawing, define:

```text
Main claim:
Claim anchor id:
Evidence hierarchy:
Material passports:
Panel roles:
Non-redundant message per panel:
Drawing method:
Editable source:
Export targets:
Open decisions:
```

## Rules

- Every panel, node, arrow, label, plotted value, annotation, or visual element must support a specific claim, method step, comparison, or design decision.
- If two panels communicate the same message, merge them or explain the distinction before drawing.
- For data-backed plots, record the data source, analysis status, statistics or uncertainty status, and whether values are provided or pending.
- For image-based figures, record permitted image processing, scale bars, annotations, and any manipulation or disclosure requirement.
- If the evidence hierarchy is incomplete, stop at a specification or storyboard instead of producing a final-looking figure.

## Quality Gate

| Gate | Pass condition |
|---|---|
| Claim clarity | The figure can be summarized in one defensible manuscript claim. |
| Panel necessity | Each panel has a non-redundant role. |
| Evidence trace | Every plotted value, label, node, arrow, or annotation traces to data, code, manuscript text, or user-approved facts. |
| Editability | Source files remain editable and text is not unnecessarily outlined. |
| Submission fit | Size, typography, colour, and annotation density fit the target journal or thesis context. |

## Package QA Hook

When maintaining this skills repository or checking a figure package, use:

```bash
python scripts/figure_package_check.py --package figures --captions captions.md --output-md figure_package_check.md
```

Treat missing editable sources, missing exports, and captions without claim anchors as issues to resolve or explicitly waive.

## Output Packet

```text
Figure source file:
Export file:
Caption draft:
Placement recommendation:
Evidence trace:
Related claim anchors:
Assumptions:
Manual checks:
Unresolved issues:
```
