# Integrity Gate Patterns

Use this reference before drafting, benchmark review, final polishing, or delivery when the project depends on literature, data, code, experiments, figures, or user-provided claims.

## High-Risk Failure Modes

Watch for these patterns:

- source identity is assumed from title similarity or memory;
- a citation is real but does not support the exact claim;
- result, metric, dataset split, or code behavior is inferred without inspecting the artifact;
- a weak implementation or failed experiment is reframed as a novel contribution;
- benchmark facts are inferred from abstract or metadata as if full text had been read;
- generated prose keeps project-log residue, TODOs, operation records, or hidden assumptions in the manuscript body;
- the workflow stays locked to an early frame after new evidence contradicts it.

## Gate 1: Source And Claim Reality

Before writing or backfilling claims, require one of:

- verified literature with evidence location and allowed claim strength;
- user-provided data/result table with provenance;
- inspected code/script output with path, command, and result;
- explicit user approval to keep a provisional claim.

If none exists, write `LIT_GAP` or remove/soften the claim.

## Gate 2: Code, Data, And Experiment Reality

Use when the manuscript discusses implementation, datasets, experiments, baselines, or results.

Check:

- where the data came from and whether access restrictions exist;
- which script, notebook, command, or result file supports the statement;
- whether validation splits, baselines, metrics, and sample counts are visible;
- whether negative or failed results are being hidden by wording;
- whether the claim should be narrowed to what the artifact actually proves.

Ask the user before asserting experiment success, code behavior, or dataset properties when artifacts are missing or ambiguous.

## Gate 3: Benchmark Honesty

Before post-draft review:

- identify 3-10 benchmark papers or state why fewer are available;
- mark each benchmark access level: full text, abstract, metadata, or user-supplied;
- separate benchmark facts from reviewer-facing inference;
- do not score target readiness from metadata-only comparisons unless clearly provisional.

## Gate 4: Pre-Final Delivery

Before final polish, formatting, or delivery, check:

- all central claims have verified evidence, inspected artifacts, or accepted `LIT_GAP` status;
- citations and bibliography have been audited or queued for manual verification;
- figures and tables match the manuscript claims and captions;
- final polish did not change technical meaning, claim strength, citations, formulas, or terminology;
- DOCX/Markdown versions are semantically aligned if both exist.

## Integrity Gate Report

```text
Gate:
Checked artifacts:
Confirmed:
Unresolved:
User decision needed:
Allowed next step:
Blocked next step:
```
