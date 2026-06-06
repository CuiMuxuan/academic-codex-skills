# Cross-Disciplinary Academic Language Review Gate

Use this shared gate for formal manuscript body text, reviewer-response text, and final polished scholarly prose when wording may be abstract, mechanical, operation-record-like, internally defensive, self-invented, citation-unclear, or unsupported by concrete objects and conditions.

Do not apply this gate as a hard stop to titles, abstracts, highlights, graphical abstracts, outlines, brainstorming notes, or internal planning unless the user explicitly asks to review those parts.

When the user explicitly asks for language review, abstract-expression checking, terminology checking, operation-record cleanup, or similar wording audit, review the specified chapter or subsection sentence by sentence. Do not expand to later chapters, abstracts, or the full manuscript unless the user asks.

## 1. Confirm The Disciplinary Context First

Before judging wording, identify or confirm:

- research object: material, pollutant, patient, specimen, algorithm, text, organization, policy, market, learner, experimental system, artifact, archive, community, or other field object;
- method or technique: experiment, model, process, survey, interview, clinical study, simulation, algorithm, text analysis, field observation, archival analysis, theoretical argument, or mixed method;
- evaluation basis: performance, accuracy, risk, effect size, mechanism, stability, cost, reproducibility, ethical impact, explanatory power, interpretive boundary, validity, reliability, or transferability;
- paragraph task: define an object, explain a mechanism, introduce a method, compare studies, explain a result, state a limitation, define a metric, discuss application boundaries, or justify a classification.

If the field is unclear, infer it from the title, abstract, keywords, methods, target venue, source materials, and paragraph content, then ask the user to confirm. If the user also does not set the field, default to computer science and electronic information and mark that assumption.

## 2. Term Usability Test

Do not mechanically ban any word. Keep a term only when at least one condition is true:

- it is a standard term in the confirmed discipline;
- a cited paper, method standard, clinical guideline, policy document, handbook, or theoretical source supports it directly;
- the manuscript has already defined it clearly in body text;
- later use is consistent and maps to a specific object, variable, process, mechanism, metric, evidence item, or interpretive category.

If none of these conditions is met, replace the term with a more concrete disciplinary object or a testable expression. If the author needs a temporary concept, define it immediately at a stable location and state its scope, basis, and later use.

For each terminology judgment, be able to answer: is this a field-standard term, or a manuscript-local shorthand?

## 3. Object-Condition-Consequence Rule

Every judgment sentence must state the object, condition, and consequence. Do not rely on empty relations such as "related", "influences", "determines", "has significance", "supports", "controls", or "transforms into" without saying what changes under which condition.

The consequence must also answer at least one practical or argumentative question: so what, why it matters, what treatment or methodological consequence follows, or what boundary applies. If the sentence only says that a relation exists, rewrite it so the reader can see what comparison, mechanism, evaluation, interpretation, or application decision changes.

Bad pattern:

- "This factor is directly related to N2O."

Better pattern:

- "When nitrogen-containing components are abundant or nitrification/denitrification occurs, N2O generation or reduction needs to be included in the climate-impact discussion."

Required check:

```text
object:
condition:
consequence:
support or locator:
why_it_matters_or_boundary:
```

If any field is missing, rewrite, split, soften, or mark the sentence as needing support.

## 4. Replace Abstract Words With Concrete Disciplinary Objects

Do not use abstract summary words as substitutes for research objects, mechanisms, metrics, or consequences.

Use field-specific replacements:

| field | replace vague wording with |
|---|---|
| Engineering and environmental engineering | energy use, chemical consumption, waste liquid, maintenance frequency, secondary emissions, pressure drop, breakthrough time, bed life, regeneration cost, mass-transfer limitation, gas composition, device behavior |
| Medicine and public health | infection risk, bleeding risk, recurrence risk, mortality, complication rate, adverse events, exposure level, diagnostic sensitivity, treatment response, follow-up duration, confounders |
| Materials science and chemistry | capacity, selectivity, cycle stability, strength, conductivity, conversion rate, phase change, defect density, active site exposure, reaction pathway, degradation mode |
| Computer science and electronic information | accuracy, recall, latency, robustness, generalization, compute cost, memory use, false positive rate, model size, inference speed, ablation change, failure mode |
| Social sciences and management | effect direction, effect size, variable relation, sample scope, model setting, institutional condition, causal pathway, mediation or moderation relation, boundary condition |
| Education | learning outcome, assessment score, retention, participation, cognitive load, instructional intervention, learner group, classroom condition, validity of instrument |
| Humanities | textual function, narrative structure, conceptual genealogy, rhetorical position, interpretive boundary, source tradition, historical context, discourse relation |
| Law, policy, and governance | rule scope, enforcement condition, institutional actor, compliance burden, procedural consequence, rights limitation, accountability path, implementation boundary |

The point is not to make every sentence longer. The point is to replace abstract praise or vague relation with a concrete object and a verifiable change.

## 5. Avoid Self-Invented Labels Without Definition

When the manuscript uses broad labels such as "path", "role", "framework", "mechanism", "function", "dimension", "burden", "contribution", "support level", "maturity", "capacity", "proxy value", "protection", "load", or "breakthrough", first decide whether the label is a recognized term in the field.

If it is not a recognized term:

- define its concrete meaning immediately;
- map it to an object, process, metric, or interpretive category;
- state the scope where the label is valid;
- use the same meaning consistently later.

Do not treat manuscript-local labels as terms the reader is expected to understand. For example, labels like "dynamic capacity proxy", "outlet protection", "main load", or "wet-state breakthrough" must either be defined in engineering terms or rewritten into measurable adsorption behavior, protection target, mass load, humidity condition, or breakthrough criterion.

## 6. Do Not Stack Parallel Nouns Without A Shared Level

Parallel nouns must belong to the same conceptual level and each item must have a clear disciplinary meaning.

Weak pattern:

- "water competitive adsorption, pore condensation, and coexisting-component displacement"

Clearer pattern:

- "After water enters the bed, it may occupy adsorption sites or condense inside pores; coexisting pollutants may also displace the target compound from adsorption sites."

If parallel items mix mechanism, result, metric, and application, split the sentence or reorganize by level.

## 7. Avoid Operation-Record, Internal-Review, And Self-Proving Prose

Formal manuscript body text should not sound like an internal writing log, reviewer guide, or author self-defense.

Avoid patterns such as:

- "This section organizes ... into ..."
- "The main significance that can be read from Table 1 is ..."
- "This paper is not ..., but ..."
- "Here, ... does not mean ..."
- "This result shows that the present study is important."
- "To better display ..."
- "The study should report/provide ..."

Rewrite toward the research object, method, result, mechanism, limitation, or application condition.

For review-paper body text, avoid writing as if instructing other papers how to report. Instead of "studies should report operating parameters", write why the parameter matters:

- "Whether these results can support comparison across combined processes depends on whether inlet concentration, residence time, humidity, and bed configuration are explicit."

## 8. Explain Why A Proxy Or Methodological Substitution Is Valid

When a figure, table, comparison, or method description uses one value as a proxy for another, explain:

- the relation between the proxy and the target value;
- the condition under which the proxy is informative;
- what the proxy cannot replace;
- what uncertainty or limitation remains.

Weak pattern:

- "When A is unavailable, B is used as a proxy."

Better pattern:

- "In flow-bed experiments, dynamic adsorption capacity can supplement trend comparison when complete breakthrough time is unavailable, but it cannot replace the true breakthrough curve or bed-life estimate."

This applies across disciplines: surrogate endpoints in medicine, benchmark subsets in computer science, survey proxies in social science, textual indicators in humanities, and implementation indicators in policy research all need a validity boundary.

## 9. Check The Function Of Each Sentence

For each reviewed sentence, identify its job:

- define object;
- describe method;
- explain mechanism;
- report result;
- compare difference;
- explain cause;
- limit boundary;
- state evaluation metric;
- state application condition;
- connect a local subsection to its immediate question.

If a sentence only piles up terminology, repeats prior content, or does not advance the argument, delete, split, or rewrite it. For Chinese review, judge by whether the sentence itself can be understood on first reading, not whether a specialized reader can infer the missing meaning from context.

## 10. Logic Connectors, Literature Roles, And Table/Figure Wording

Use connectors only when they match the actual relation:

- contrast;
- cause;
- consequence;
- progression;
- temporal, mechanistic, or analytical sequence;
- parallel relation;
- clarification.

Avoid "therefore", "thus", "thereby", "then", "subsequently", "随后", "因此", or "由此" when the preceding sentence only says that literature exists, a table is provided, or a topic has been introduced. A source, table, or review does not by itself prove a conclusion; the sentence must name what it shows and why that matters.

Do not turn source existence into a causal relation. A study or review may provide measurements, definitions, property context, comparison data, methodological precedent, or interpretive framing, but it is not the reason why the phenomenon exists. State the disciplinary role first, then name the source role.

When several sources are grouped, name the grouping basis or evidence role. Do not combine experimental results, mechanism studies, review papers, theoretical arguments, clinical guidelines, policy documents, and benchmark reports as if they provide the same kind of support. If the sources play different roles, split the sentence or cite each role separately.

Table and figure sentences should not stop at "Table 1 shows", "Figure 2 presents", or similar display verbs. State the comparison, boundary, trend, limitation, method implication, or decision supported by the table or figure. If the sentence only locates information, keep it in the caption, table note, or a concise parenthetical reference.

## 11. Citation Proximity And Support

Use [citation-proximity-and-style-gate.md](citation-proximity-and-style-gate.md) for citation placement.

Citation must support the nearest concrete judgment. If one sentence contains several mechanisms, results, or conclusions, split it and place each citation near the claim it supports. Do not place a citation pile at the end of a paragraph after broad description.

If the claim lacks support, use [main-text-and-rebuttal-claim-support-gate.md](main-text-and-rebuttal-claim-support-gate.md) and stop before final wording.

## 12. Use "Report" Carefully

When the intended meaning is that a study or manuscript should provide parameters, variables, data, or method details:

- in Chinese, prefer "给出", "说明", "提供", "列明", "记录", or "呈现";
- in English, prefer "provide", "specify", "include", "document", or "present".

Prefer "报告/report" only for formal research reports, regulatory reports, case reports, technical reports, and other report-genre contexts.

In review-paper body text, often prefer a relation-based sentence over an instruction-based sentence:

- not "studies should report humidity";
- but "humidity affects site occupation and pore condensation, so comparisons across adsorbents are difficult when humidity is not specified."

## 13. Cross-Language Consistency

For bilingual manuscripts, do not require word-by-word correspondence. Require consistency in:

- research object;
- variables and metrics;
- mechanism or causal relation;
- support source;
- limitation and boundary condition;
- conclusion strength.

Chinese must not be stronger than English, and English must not add unsupported claims that are absent from Chinese.

Do not mechanically mirror long modifier chains from one language into the other. If the Chinese becomes clearer by splitting a sentence or naming the object directly, simplify or split the English as well so the research object, condition, support, boundary, and conclusion strength still match.

If a term is changed from an abstract label to a concrete object in one language, update the other language's object too. Preserve stable sentence IDs when needed, but do not preserve awkward wording only to keep one-to-one syntax.

## 14. Required Output When Reviewing A User-Flagged Passage

When the user points to a language problem:

1. judge whether the user's concern is valid;
2. if valid, name the problem type: abstract term, unclear object, undefined field term, operation-record prose, citation too far, unclear sentence function, overstrong conclusion, unsupported proxy, noun pile-up, self-invented label, or cross-language inconsistency;
3. if invalid, explain why the term or wording is acceptable in the confirmed field;
4. revise only the specified chapter, subsection, paragraph, or sentence unless the user explicitly requests broader checking.

Use this compact output shape unless the user asks for a different format:

```text
field_context:
- field:
- paragraph_task:
- terminology_boundary:

sentence_review:
| location | original issue | problem type | judgment | revision | support/check needed |
|---|---|---|---|---|---|

unchanged_terms:
| term | why acceptable | scope |
|---|---|---|

remaining_questions:
- ...
```

For strict subsection review, include every sentence in `sentence_review`, including sentences that are acceptable.

## 15. Quality Gate

Do not approve formal body text, rebuttal text, or final polished prose unless:

- the field and paragraph task are explicit or the field assumption is marked;
- key terms are field-standard, cited, defined, or concretely mapped;
- judgment sentences state object, condition, and consequence;
- abstract labels have been replaced or defined;
- noun lists are same-level or split;
- operation-record and internal-review wording has been removed or recast;
- proxies and substitutions state relation, scope, and limits;
- logical connectors match real contrast, cause, consequence, sequence, parallel relation, or clarification;
- source mentions state the source's evidence role instead of turning source existence into a causal claim;
- table and figure sentences state the comparison, boundary, trend, limitation, or method implication they support;
- citations sit near concrete supported claims;
- unsupported claims are blocked, softened, or turned into material requests;
- bilingual versions preserve the same object, condition, support, boundary, and conclusion strength.
