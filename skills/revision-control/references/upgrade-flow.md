# Revision Upgrade Flow

## Upgrade Triggers

Pause sentence-level editing when:

- new literature is needed;
- a superiority, novelty, contribution, or comparison claim lacks benchmark literature, baseline results, metric support, data, or source evidence;
- support materials are insufficient;
- chapter or section structure must be reorganized;
- a sentence problem comes from paragraph or section function failure;
- large-scale duplicate argumentation exists;
- figure, evidence, or conclusion relationships are invalid;
- editing would change supporting material files;
- the user asks for large-scale rewriting.

## Required Behavior

1. Stop sentence modification.
2. Create an upgrade plan with [revision-upgrade-plan-schema.md](../../../shared/revision-upgrade-plan-schema.md).
3. Identify affected object range, needed skills, missing materials, expected rewrite level, state reset impact, and user decision points.
4. Wait for user confirmation.
5. After approved evidence or structure work completes, rebuild the object library, regenerate latest full review draft, renumber, preserve id mapping, and re-enter sentence checking.

## Routing

| trigger | route |
|---|---|
| DOI/title/citation authenticity, new literature, `LIT_GAP` | `$academic-research-verification` |
| section/chapter rewrite, new draft content | `$paper-writing-workflow` |
| complete draft readiness or benchmark gap | `$post-manuscript-benchmark-review` |
| local stable language rewrite after confirmation | `$academic-de-ai-polishing` |
| language diagnosis without writing | `$language-style-review` |
