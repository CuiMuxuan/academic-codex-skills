# Language Style Review Schema

Use this schema for reports produced by `$language-style-review`.

```yaml
report_id:
source_skill: language-style-review
scope:
source_path:
object_ids: []
project_standards_used: []
source_limits:
scores:
  clarity_and_grammar:
  academic_expression:
  terminology_and_translation:
  residue_and_citation_style:
main_issues:
  - priority:
    issue_type:
    location:
    evidence:
    recommended_handling:
sentence_or_object_issues:
  - object_id:
    original_text_excerpt:
    issue_type:
    diagnosis:
    candidate_rewrite:
    handoff:
accepted_terms:
  - term:
    decision: keep
    reason:
revision_control_queue:
  - target_id:
    task:
    reason:
    required_confirmation: true
candidate_rules:
  - candidate_rule_id:
    source:
    proposed_rule:
    status: candidate_only
```

## Consumer Rules

- Candidate rewrites are not final manuscript text.
- `revision_control_queue` items require user confirmation before editing.
- `candidate_rules` cannot be written to project standards until `$revision-control` asks for and receives explicit user approval.
