# Project Review Standards Schema

Use paired Markdown and YAML files for project-specific review standards, terminology, and problem-word rules.

## YAML Shape

```yaml
project_review_standards:
  version:
  confirmed_rules:
    - rule_id:
      source:
      confirmed_by:
      confirmed_at:
      scope:
      rule:
      examples: []
      related_object_ids: []
  candidate_rules:
    - candidate_rule_id:
      source:
      proposed_rule:
      reason:
      status: candidate_only
      requires_user_confirmation: true

terminology_glossary:
  - term:
    language:
    preferred_form:
    accepted_variants: []
    chinese_translations: []
    forbidden_variants: []
    field:
    term_type:
    source_provenance: []
    reason:
    confirmed: false

problem_words:
  - expression:
    scope:
    risk:
    replacement_guidance:
    confirmed: false
```

## Rules

- Confirmed user standards outrank general style guidance.
- Candidate rules remain advisory until user confirmation.
- For bilingual projects, `chinese_translations` records likely Chinese renderings of English terms; both source English terms and Chinese translations may be used by the annotation UI for visual terminology highlighting before confirmation, but they are not final terminology standards until confirmed.
- Every terminology entry must record `field` and `source_provenance`. For professional terms, `field` states the discipline or subfield where the term is valid. For proper nouns, named methods, named datasets, software, regulations, or cited concepts, `source_provenance` should identify the cited paper, source material, or manuscript sentence where the name appears.
- Use `term_type` values such as `professional_term`, `proper_noun_or_named_method`, `abbreviation`, `chemical_species`, `instrument_or_method`, `regulation_or_standard`, or `project_local_label`.
- Keep Markdown readable for human review and YAML structured for automation.
- Record source and confirmation history for every confirmed rule.
