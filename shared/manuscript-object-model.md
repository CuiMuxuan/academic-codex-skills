# Manuscript Object Model

Use this model when building or updating a manuscript object library for revision.

## Paper

```yaml
paper_id:
title:
language_mode:
target_journal_or_school:
manuscript_path:
current_round:
object_library_version:
```

## Section

```yaml
section_id:
parent_id:
title:
local_purpose:
evidence_scope:
target_problem:
position_in_argument:
status:
notes:
```

## Paragraph

```yaml
paragraph_id:
section_id:
paragraph_role:
main_claim:
evidence_ids: []
sentence_ids: []
context_fit:
duplicate_argument:
status:
notes:
```

## Sentence

```yaml
sentence_id:
round_sentence_id:
paragraph_id:
original_text:
latest_text:
suggested_status:
user_confirmed_status:
revision_count:
checks:
  grammar_correctness:
  sentence_value:
  context_fit:
  duplicate_argument:
  terminology:
  citation_expression:
  figure_table_reference:
source_sentence_ids: []
derived_sentence_ids: []
operation:
deleted_source_marker:
previous_round_sentence_ids: []
next_round_sentence_ids: []
history_mapping: []
notes:
```

## Figure/Table Text Object

```yaml
object_id:
type: figure_title/figure_caption/table_title/table_caption/figure_text/table_text
linked_sentence_ids: []
original_text:
latest_text:
terminology:
citation_expression:
status:
notes:
```

## Material Dependency

```yaml
material_id:
path:
type:
purpose:
access_state:
verification_state:
related_object_ids: []
change_state:
change_log: []
```
