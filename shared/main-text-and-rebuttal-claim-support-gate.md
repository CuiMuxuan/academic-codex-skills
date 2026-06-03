# Main Text And Rebuttal Claim Support Gate

Use this shared gate only for manuscript main text and reviewer, editor, committee, or supervisor rebuttal text. Do not apply it as a hard stop to titles, abstracts, highlights, graphical abstracts, notes, brainstorming, outlines, or internal planning unless the output will be used as final manuscript main-text or rebuttal prose.

## Trigger

Apply this gate before drafting, revising, polishing, or approving:

- factual judgments;
- boundary statements;
- benchmark or comparison statements;
- subjective quality judgments;
- novelty, contribution, limitation, or generalization claims;
- rebuttal statements that accept, reject, or qualify a reviewer comment.

Do not require citations or claim-support locators inside the title, abstract, highlights, or graphical abstract unless the user, target journal, school template, or supervisor explicitly requires them. Start this gate from the first body-text section, such as Introduction or Chapter 1.

## Required Support

Every triggered sentence must be tied to at least one concrete support item:

| support type | acceptable locator |
|---|---|
| Literature | verified citation key, DOI, title, page, section, table, figure, or quoted claim locator |
| Experimental result | dataset, metric, table, figure, script, run id, or result file |
| Code or implementation | repository path, function/module, commit, configuration, or reproducible command |
| User-supplied material | document path, page, paragraph, comment id, or explicit user decision |
| Standard or guideline | official guide name, URL/path, section, version/date if available |

Do not treat a convenient source as adequate if it does not support the exact sentence being written.

## Missing Support Stop Rule

If support is missing for main text or rebuttal text:

1. Do not draft the unsupported sentence as final prose.
2. Output a material request or reference download list.
3. Mark the affected claim as blocked or unresolved.
4. Wait for the user to provide the material or explicitly narrow the claim.

## Download Or Material Request

Use this compact format when stopping:

```text
missing_support_request:
- claim_or_sentence:
  needed_support_type:
  suggested_reference_or_material:
  why_needed:
  target_manuscript_location:
  blocks_next_step: yes/no
```

## Wording Discipline

Prefer precise support nouns over the generic word "evidence" when the support type is known:

- use "literature support" for verified papers;
- use "experimental result" or "result table" for measured outcomes;
- use "data support" for datasets or measurements;
- use "implementation basis" for code-backed statements;
- use "theoretical basis" for derivations, definitions, or formal arguments;
- use "reviewer comment" or "editor concern" for rebuttal inputs.

Use "evidence" only when it is the most accurate umbrella term.
