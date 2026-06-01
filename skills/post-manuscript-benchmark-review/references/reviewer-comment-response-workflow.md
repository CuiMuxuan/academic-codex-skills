# Reviewer Comment Response Workflow

Use this reference when reviewer, editor, committee, or supervisor comments are provided after a complete draft exists.

## Rule

Do not mechanically accept every comment. Judge each comment against:

- manuscript evidence;
- target standard;
- benchmark expectations;
- claim discipline;
- available data, literature, figures, and code;
- possible side effects on structure, terminology, and formatting.

Produce a next-stage revision plan and ask for user confirmation before executing substantial edits.

When two or more comments are provided, apply [reviewer-comment-action-plan-gate.md](../../../shared/reviewer-comment-action-plan-gate.md) before editing. The gate controls action-plan size, small-comment-set exceptions, triage states, and concrete action fields.

## Per-Comment Handling

For each comment:

1. Restate the comment.
2. Identify the reasonable part.
3. Identify any questionable, impossible, unsupported, or target-misaligned part.
4. Assign one status:
   - `accept`
   - `partly_accept`
   - `reject_with_reason`
   - `defer`
   - `needs_user_decision`
   - `needs_new_literature`
   - `needs_new_data_or_analysis`
5. Specify the exact manuscript location affected.
6. Specify the concrete revision action.
7. Set priority: P0, P1, or P2.
8. State the expected value for the manuscript.
9. State new risks introduced by the revision.

## New-Risk Assessment

Check whether the fix could cause:

- logic breaks before or after the edited section;
- content duplication;
- new evidence gaps;
- claim-strength inflation;
- terminology conflicts;
- benchmark-positioning conflicts;
- figure/table mismatch;
- formatting or citation side effects.

## Output Table

| id | comment | status | target location | action | priority | value | new risk | external dependency |
|---|---|---|---|---|---|---|---|---|

For executable next-version plans, preserve the shared action fields from [reviewer-comment-action-plan-gate.md](../../../shared/reviewer-comment-action-plan-gate.md): `source_comment_id`, `specific_change`, `required_material`, `expected_effect`, `verification_method`, `owner_skill`, and `priority`.

End with:

```text
Plan needs user confirmation: yes/no
Can execute now:
Blocked until user provides:
Recommended revision order:
Handoff to writing/research/figures/formatting:
```
