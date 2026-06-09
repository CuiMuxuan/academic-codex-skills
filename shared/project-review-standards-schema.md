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
    forbidden_variants: []
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
- Keep Markdown readable for human review and YAML structured for automation.
- Record source and confirmation history for every confirmed rule.
