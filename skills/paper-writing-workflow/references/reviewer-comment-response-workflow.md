# Reviewer Comment Response Workflow

Use this reference when the user provides supervisor, reviewer, committee, or editor comments during ordinary writing or revision. For complete manuscript benchmark review, route to `$post-manuscript-benchmark-review`.

## Gate

Before editing the manuscript, turn comments into a revision plan and ask the user to confirm the plan when changes are substantial.

Do not mechanically accept every comment. Judge each one against manuscript goals, evidence, target venue, and available materials.

## Per-Comment Analysis

For each comment:

1. Restate the comment in concrete terms.
2. Separate the reasonable part from any questionable or unsupported part.
3. Assign status:
   - `accept`
   - `partly_accept`
   - `reject_with_reason`
   - `needs_user_decision`
   - `needs_new_evidence_or_analysis`
4. Identify the target section, paragraph, figure, table, or citation.
5. Propose the exact revision action.
6. State priority: P0, P1, or P2.
7. State the expected value for manuscript quality.
8. State possible new problems introduced by the change.

## Risk Checks

Check whether the proposed revision could introduce:

- logic break with surrounding paragraphs;
- duplicated content elsewhere;
- new evidence gap;
- terminology conflict;
- claim-strength inflation;
- formatting or citation side effects;
- requirement for new experiments, analysis, data, or literature.

If external material is needed, say exactly what the user must provide before execution.

## Revision Plan Output

Use this table:

| id | comment summary | status | target location | planned action | priority | value | new risk | external dependency |
|---|---|---|---|---|---|---|---|---|

End with:

```text
Plan needs user confirmation: yes/no
Can edit now:
Blocked until user provides:
Recommended execution order:
```

After user confirmation, apply accepted changes and keep a change report.
