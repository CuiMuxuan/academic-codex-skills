# Draw.io Engineering Diagram Standards

Use this reference for Draw.io workflow, architecture, use-case, module, data-flow, deployment, and code-backed diagrams.

## When Draw.io Is The Right Tool

Use Draw.io when the figure's value is an editable engineering diagram rather than quantitative plotting or freeform illustration:

- system architecture;
- runtime workflow;
- module relationship;
- use-case diagram;
- data-flow or storage diagram;
- experiment or thesis implementation pipeline;
- code-backed process extracted from a repository.

Use SVG instead when the figure is a mechanism illustration or concept diagram that needs precise custom shapes. Use Matplotlib when the figure is data-driven.

## Source Contract

Before generating:

```text
Diagram type:
Target manuscript section:
Real/source-backed entities:
User-confirmed entities:
Edges and flow meanings:
Unsupported or unknown entities:
Output pages:
```

Do not invent services, databases, models, APIs, datasets, or modules just to make the diagram look complete.

## Shape Semantics

Keep a small and consistent shape vocabulary:

| Meaning | Shape |
|---|---|
| process or module | rounded rectangle or rectangle |
| external actor/user/system | actor icon or plain labeled rectangle |
| data store | cylinder or storage rectangle |
| document/artifact | document shape |
| decision | diamond, only for real branching logic |
| boundary/layer | container or swimlane |
| note/assumption | small callout, visually quiet |

If a shape meaning changes between diagrams, state the legend or change the design.

## Edges

- Use arrows only for direction, dependency, or data/control flow that exists.
- Label edges when the relationship would be ambiguous.
- Avoid crossing lines; use lanes, grouping, or separate pages instead.
- Do not mix temporal sequence and static dependency in the same arrow style.
- Use dashed lines for optional, asynchronous, or inferred relationships only when defined.

## Layout Patterns

| Diagram type | Preferred layout |
|---|---|
| Architecture | layered top-to-bottom or left-to-right; external systems outside the boundary |
| Workflow | left-to-right or top-to-bottom sequence with clear start/end |
| Use case | actors outside, use cases inside system boundary |
| Data flow | sources on left, transformations center, stores/outputs right |
| Module design | containers for packages/layers; dependencies flow one direction where possible |

## Visual Style

- Use restrained colours with semantic roles: external, core, data, model, interface, risk/exception.
- Keep labels short and manuscript-consistent.
- Use one font family and one or two text sizes.
- Avoid shadows, gradients, clipart, and decorative icons.
- Prefer uncompressed Draw.io XML for review and version control.
- Use one Draw.io page per figure or subfigure topic; name pages after manuscript sections or figure panels.

## Output Packet

```text
Draw.io source:
Exported SVG/PDF/PNG:
Page names:
Diagram legend:
Evidence/code trace:
Unsupported assumptions:
Manual checks:
```

## Source Basis

This standard turns the general academic figure rules into a Draw.io-specific convention so generated diagrams remain editable, evidence-backed, and clear at thesis or paper column width.
