# Reviewer Comment Action Plan Gate

Use this shared gate when the user provides two or more reviewer, editor, committee, or supervisor comments for a complete draft or a substantial manuscript section.

## Trigger

Trigger this gate when:

- at least two review comments are provided; and
- the task is to revise, respond, plan changes, or decide what to accept; and
- the comments affect manuscript content, experiments, figures, citations, structure, formatting, or rebuttal language.

## Output Size Rule

Default rule:

- create an action plan with at least 20 concrete modification actions.

Exception:

- if the total number of review comments is below 25 and the manuscript quality is high enough that fewer concrete issues exist, the action plan may contain fewer than 20 actions;
- in that case, state that the action count follows the actual issue count.

## Required Comment Triage

Before writing the plan, classify each comment:

| state | meaning |
|---|---|
| accept | implement directly |
| partly_accept | implement the useful part and explain the boundary |
| reject_with_reason | do not implement; provide support-based reason |
| defer | not suitable for current version; record risk and future condition |
| needs_material | cannot decide until data, citation, code, figure, or user decision is supplied |

Do not blindly accept every comment. Every rejection, deferral, or partial acceptance needs a concrete reason.

## Concrete Action Plan Fields

Each action should be specific enough to execute later:

```text
action_id:
source_comment_id:
acceptance_state:
target_location:
modification_type:
specific_change:
required_material:
expected_effect:
verification_method:
owner_skill:
priority: P0/P1/P2
```

## Quality Bar

A useful action plan:

- maps comments to exact manuscript locations;
- separates content, experiment, figure, citation, rebuttal, and formatting actions;
- marks missing references, data, figures, or code as blockers;
- avoids vague actions such as "improve discussion" without a precise change;
- preserves the paper's main line instead of expanding every reviewer suggestion into main-text clutter.
