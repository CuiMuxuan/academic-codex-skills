# Standards Review Agent

Use this reference when the user requests an editorial-style SCI/Q1 screening, desk-reject risk review, Applied Energy-level screening, or page/paragraph/sentence-level audit.

## Purpose

Delegate bounded review passes to a standards-review agent when the manuscript needs a strict editor-or-reviewer lens before the main readiness judgment.

The main skill remains responsible for the final synthesis. The standards-review agent returns findings only.

## Agent Passes

Run these passes independently when the draft is substantial enough:

1. Scope Fit pass
2. Novelty Assessment pass
3. Scientific Logic Audit pass

If the user asks for a broader multi-agent review, these passes may run in parallel with evidence, language, and citation checks.

## Scope Fit Pass

Check:

- whether the research question fits the target journal scope;
- whether the innovation direction matches the journal's typical concerns;
- whether the paper is a methods paper disguised as an application paper;
- whether the topic drifts away from the target venue;
- which desk-reject reason an editor is most likely to cite.

Return:

- `scope_fit_score_0_100`
- `direct_reject_risk`
- `likely_desk_reject_reasons`
- `revision_advice`
- `evidence_locations`

## Novelty Assessment Pass

Check:

- whether each claimed innovation point actually exists;
- whether it is only a small improvement over existing methods;
- whether it is merely incremental innovation;
- whether the novelty is exaggerated;
- whether the paper overlaps with prior literature.

For each innovation point, return:

- `innovation_point`
- `innovation_degree`
- `evidence_sufficiency`
- `applied_energy_level`
- `notes`
- `evidence_locations`

## Scientific Logic Audit Pass

Check:

- internal inconsistency;
- chapter conclusion conflict;
- logical jumps;
- broken inference chains;
- hidden assumptions;
- insufficient evidence;
- discussion beyond result support;
- exaggerated conclusions;
- causal misuse;
- violations of basic scientific/common-sense constraints.

For each issue, return:

- `quote_or_exact_locator`
- `issue_type`
- `why_problematic`
- `severity` with `Critical`, `Major`, or `Minor`
- `fix`

## Output Contract

Return findings in a structured block the main agent can merge:

```text
standards_review_report:
- scope_fit:
- novelty:
- scientific_logic:
- direct_reject_risk_summary:
- desk_reject_reasons:
- applied_energy_readiness_notes:
- page_paragraph_sentence_anchors:
```

## Merge Rule

The main review merges these findings into the final report, then decides:

- whether the draft is fit for the target venue;
- whether the paper is likely to face desk rejection;
- which claims should be softened, moved, or removed;
- which fixes are P0 blockers before submission.
