# AI Trace Assessment

Use this reference when the user asks whether academic prose has obvious AI traces, AIGC risk, mechanical feel, or mass-generated style.

## Assessment Rules

- Give a qualitative reviewer-facing assessment.
- Separate human-reader style risk from detector speculation.
- Do not invent detector percentages or claim to predict a detector score.
- Identify exact paragraphs or sentence patterns that create residual risk.
- Flag argument or evidence problems before style problems when they affect credibility.

## Risk Categories

| level | signal | action |
|---|---|---|
| high | stacked connectors, mirrored sentence pairs, generic claim-contrast-conclusion rhythm, broad claims without mechanism | diagnose and rewrite |
| medium | smooth but generic transitions, repeated paragraph openers, vague academic nouns, weak authorial judgment | revise selectively |
| low | varied syntax, evidence-based judgment, implicit transitions, mechanism-bound claims | preserve |

## Output Template

```text
Overall assessment:
High-risk paragraphs:
Medium-risk paragraphs:
Main causes:
Recommended edit intensity:
Claims/evidence cautions:
Next step:
```

Do not polish over unsupported claims. If a paragraph overclaims, hides uncertainty, or uses a citation for a claim it may not support, soften the claim or ask for evidence before improving cadence.
