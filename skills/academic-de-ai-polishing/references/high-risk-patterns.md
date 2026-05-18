# High-Risk Patterns

Use this reference when diagnosing why a paragraph sounds obviously AI-assisted, over-smoothed, or mechanically academic. These are pattern examples, not text to copy directly. Match the user's paragraph to a pattern, then apply the corresponding rewrite strategy.

## How To Use

1. Identify the dominant problem in the paragraph, not every minor issue at once.
2. Choose the closest pattern family below.
3. Rewrite locally.
4. Re-check whether the meaning, citation logic, and technical scope still match the source paragraph.

## Pattern Table

| High-risk pattern | Example shape | Why it reads as AI-shaped | Preferred rewrite strategy |
|---|---|---|---|
| Connector stacking | "Moreover, ... Furthermore, ... However, ... Therefore, ..." | The logic is signposted too explicitly and rhythm becomes schematic. | Remove most connectors. Rebuild transitions through topic carry-over, causality, and noun continuity. Keep at most one explicit connector if the logic genuinely needs it. |
| Mirror-balanced contrast | "X is effective, but Y remains challenging." repeated across paragraphs | The prose sounds generated from a reusable dialectical template. | Break the symmetry. Convert one sentence into mechanism, another into operating consequence, and a third into evaluative judgment. |
| Checklist logic in prose | "The first issue is... The second is... The third is..." | Reads like prompted outline expansion rather than authored argument. | Preserve the sequence only if necessary. Otherwise recast as burden redistribution, constraint hierarchy, or design logic. |
| Over-even sentence rhythm | Five to seven medium-length declarative sentences in a row | The paragraph sounds polished but machine-regular. | Vary sentence length and architecture. Introduce one shorter judgment sentence and one longer mechanism-driven sentence. |
| Generic evaluative nouns | "important role", "significant challenge", "key issue", "crucial factor" | Signals low-specificity academic filler. | Replace with precise nouns or verbs: `mass-transfer bottleneck`, `liquid-handling burden`, `stability window`, `overstates performance`, `narrows usability`. |
| Abstract totalization | "The resulting picture is..." / "Taken together, these studies show..." without narrowing conditions | Sounds globally summarizing and over-controlled. | Add scope limits: under what feed, operating window, or evidence base the statement holds. Replace broad synthesis with selective judgment. |
| Over-scripted critique | "That structure is useful for orientation. It is less helpful when..." | Elegant, but too perfectly staged. | Keep the critique, but make the turn less theatrical. Let the second sentence emerge from the first through a concrete deficiency. |
| Repetitive paragraph openers | Multiple paragraphs beginning with "For X...", "In Y...", "Regarding Z..." | Section cadence becomes visibly templated. | Vary openings: start with a result, a constraint, a mechanism, or a caveat instead of repeating framing formulas. |
| Safe summary without stake | "These studies provide useful insights..." | Technically harmless, but bland and non-authorial. | Replace with a sentence that states what the evidence actually settles, what remains uncertain, or what would be misleading to conclude. |
| Headline-metric inflation | "Removal efficiency remained high..." with no mention of instability, loading, or duration | Sounds like uncritical literature digestion. | Add the hidden qualifier: duration, breakthrough, real-gas complexity, pressure drop, pH drift, by-products, or regeneration cost. |
| Review-section repetition | Each technology section repeats "mechanism -> advantage -> limitation -> future work" in the same rhythm | Cross-section regularity itself becomes an AI cue. | Change the organizing pressure in each section. One can pivot on mechanism, another on failure route, another on integration role. |
| Citation pile-up without structure | A long run of studies attached to one broad claim | Looks assembled rather than interpreted. | Split citations by evidence function: representative mechanism, performance benchmark, contradiction, or long-term validation. |
| Future-work boilerplate | "More studies are needed..." / "Standardization is required..." | Common in real papers too, but high density makes it feel generated. | Specify what exactly is missing: real-gas duration, minimum reporting variables, cost-normalized comparisons, or by-product mass balance. |
| Mechanical confidence in the introduction | Smooth, assertive prose with no local asymmetry or nuance | Feels polished by model-level style control. | Keep confidence, but insert sharper scope control, one concrete asymmetry, or one sentence that distinguishes orientation from decision-usefulness. |
| Hybrid-route over-formatting | Route I / Route II / Route III each explained with the same sentence skeleton | Strong signal of templated generation in engineering reviews. | Keep route labels if needed, but vary internal prose. Emphasize different burdens: shock capture, bulk stabilization, polishing credibility, regeneration economics. |

## Pattern Families By Section

### Abstract

Common risk:

- slogan-like synthesis
- perfect sentence symmetry
- novelty claims that sound pre-packaged

Best move:

- tighten scope
- replace broad claims with conditional claims
- keep one sentence more concrete than elegant

### Introduction

Common risk:

- polished critique delivered in evenly paired contrasts
- too many "existing reviews ... however ..." structures

Best move:

- anchor the critique in one practical decision failure
- vary paragraph rhythm
- let the novelty claim emerge from constraint mismatch rather than sales language

### Technology Review Sections

Common risk:

- recurring "good at X but poor at Y" template
- descriptive balance without mechanism

Best move:

- tie evaluation to control step, humidity penalty, failure route, or integration burden
- add one authorial selection sentence showing what should not be overinterpreted

### Hybrid Design / Future Perspectives

Common risk:

- list-heavy route catalogues
- procedural wording
- generic research-gap sentences

Best move:

- convert lists into trade-off logic
- state why one route is credible only under a narrow role allocation
- distinguish unresolved science from unresolved reporting practice

## Rewrite Prompts You Can Apply Internally

Use these as silent working prompts, not as visible output:

- "What is the single most mechanical sentence in this paragraph?"
- "Which claim sounds globally true but is only conditionally true?"
- "Where does the paragraph summarize instead of judge?"
- "Which repeated sentence shape can be broken without changing meaning?"
- "What hidden engineering burden is missing from the current wording?"

## Final Check

Before finishing a rewrite, verify:

- the paragraph no longer depends on stacked connectors
- at least one sentence carries concrete mechanism or consequence
- the author's judgment is visible but evidence-bound
- the cadence is no longer overly even
- citations still align with the claims they follow
