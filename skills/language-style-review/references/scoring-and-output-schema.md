# Language Style Review Scoring And Output Schema

## Four Dimensions

Score each dimension from 0.0 to 10.0, one decimal place.

| dimension | checks |
|---|---|
| clarity_and_grammar | grammar, sentence completeness, ambiguity, referent clarity, word order, punctuation, readability |
| academic_expression | academic register, sentence value, argument function, repetition, templated phrasing, mechanical cadence |
| terminology_and_translation | field terminology, proper nouns, bilingual strength drift, translated term consistency, accepted technical phrases |
| residue_and_citation_style | prompt traces, operation records, project notes, TODOs, citation sentence style, citation proximity, figure/table wording |

## Report Template

```markdown
# Language Style Review Report

## Scope

- Source:
- Review scope:
- Object ids available:
- Project standards used:
- Source limits:

## Scores

| dimension | score | reason |
|---|---:|---|
| clarity_and_grammar | 0.0 |  |
| academic_expression | 0.0 |  |
| terminology_and_translation | 0.0 |  |
| residue_and_citation_style | 0.0 |  |

## Main Issues

| priority | issue | evidence | recommended handling |
|---|---|---|---|
| P0/P1/P2 |  |  |  |

## Sentence Or Object Issues

| object_id | original text excerpt | issue type | diagnosis | candidate rewrite | handoff |
|---|---|---|---|---|---|
|  |  |  |  | non-final suggestion | revision-control / none |

## Accepted Terms And Proper Nouns

| term | keep/change | reason |
|---|---|---|
|  | keep | accepted field term/proper noun |

## Revision-Control Queue

| target_id | task | reason | required confirmation |
|---|---|---|---|
|  |  |  | user confirmation needed |

## Candidate Rules

| candidate_rule_id | source | proposed rule | status |
|---|---|---|---|
|  | user/report |  | candidate_only |
```

## Issue Types

Use stable labels:

- `grammar`
- `ambiguity`
- `sentence_value_unclear`
- `terminology`
- `translation_drift`
- `ai_like_cadence`
- `templated_expression`
- `operation_record_residue`
- `citation_expression`
- `figure_table_text`
- `proper_noun_keep`
- `structure_or_evidence_handoff`
