# Field And Terminology Control

Use this reference before drafting or revising when the manuscript field, target venue field, or terminology boundary is not already explicit.

## Field Setup Gate

Determine the current field in this order:

1. If the user explicitly names the manuscript field, adopt it.
2. If the user provides title, abstract, keywords, topic, methods, or target venue, infer the likely field and ask the user to confirm.
3. If the field cannot be inferred, ask the user to specify it.
4. If the user does not specify after being asked, use `computer and electronic information` as the fallback default and mark it as provisional.

Use this prompt shape when confirmation is needed:

```text
Detected research field:
Target venue/school field:
Terminology baseline:
Please confirm or correct this field before I draft terminology-sensitive prose.
```

## Venue Field vs Manuscript Field

- If the manuscript field and target venue field differ, use the target venue's terminology norms for framing, section emphasis, and reviewer-facing claims.
- Keep method names and domain-specific technical terms accurate to the manuscript field.
- Explain cross-domain terms briefly on first use when the target audience may not share the source field.

## Avoiding Domain Drift

- Do not import mechanical, computer-science, or electronic-information jargon into unrelated fields unless that field commonly uses the term.
- Terms such as robustness, bandwidth, feature engineering, pipeline, deployment, architecture, module, and optimization should be checked against the confirmed field before use.
- If a cross-domain term is necessary, define it in plain language and connect it to the field's accepted vocabulary.
- Prefer field-native words over impressive but foreign technical vocabulary.

## Output Field

When field setup affects writing, include:

```text
Current field:
Target venue/school field:
Terms to use:
Terms to avoid or explain:
User confirmation needed:
```
