# Revision And Quality Checks

Use this reference for revision modes, output packets, and final quality checks for academic writing.

## Revision Modes

| Mode | Action |
|---|---|
| `logic` | Strengthen argument sequence, transitions, and section roles |
| `logic_depth` | Upgrade a paragraph into a deeper mechanism, boundary, or engineering-consequence argument while keeping evidence scope fixed |
| `data_figure_analysis` | Interpret a data figure in正文 by role, quantitative pattern, best/worst region, concentration/sparsity, and supported implication |
| `evidence` | Add, remove, or flag claims based on verified evidence |
| `style` | Improve academic tone, precision, concision, and bilingual consistency |
| `structure` | Reorganize headings, paragraph order, and chapter balance |
| `ambiguity` | Review each sentence for unclear referents, vague abstractions, unsupported concepts, and cross-disciplinary language-gate issues |
| `supervisor_response` | Address review comments one by one and preserve a change log |
| `reviewer_response_plan` | Analyze comments, decide accept/partly accept/reject, assess risks, and wait for user confirmation before editing |

## Typical Outputs

- `paper_design.md`
- `chapter_01_vX.Y.md`
- `section_<name>_draft.md`
- `integrated_manuscript_vX.Y.md`
- `revision_report.md`
- `evidence_gap_list.md`
- `reviewer_comment_revision_plan.md`

When producing a draft, include:

- active gate and allowed work;
- what was drafted or revised;
- evidence used;
- unsupported or uncertain claims;
- next recommended step.

For supervisor-comment or DOCX-derived revisions, include:

- comment or revision id;
- target section;
- action taken;
- status: `done`, `partly_done`, `rejected_with_reason`, `needs_user_decision`, or `needs_new_evidence_or_analysis`;
- follow-up evidence or formatting handoff.

Before editing from substantial comments, use `reviewer-comment-response-workflow.md` to produce a user-confirmed plan.

## Quality Checklist

Before claiming a writing task is complete, check:

- section answers its stated purpose;
- every subsection and paragraph has a clear job;
- each chapter, major section, and subsection has a local purpose within the paper's research scope;
- independent subsections are not forced together with artificial transitions;
- necessary structure navigation is brief and does not introduce later-only concepts abruptly;
- section follows target/benchmark alignment when examples were available;
- major claims have verified evidence or are flagged;
- citations are present where needed;
- citations follow [citation-proximity-and-style-gate.md](../../../shared/citation-proximity-and-style-gate.md);
- draft citation keys have been audited against the evidence register when a register exists;
- grouped citations state a clear evidence role or grouping basis when sources differ;
- first-use abbreviations follow `full term (abbreviation)` unless the target style says otherwise;
- field-specific terminology matches the confirmed field and target venue;
- data-backed figure paragraphs state the figure's role, quantitative pattern, best/worst region, concentration or sparsity, and implication instead of only restating that the figure exists;
- repeated expressions across subsections have been removed, merged, or justified;
- each sentence has been checked for ambiguity, vague abstraction, undefined referents, concepts introduced without setup, and the object-condition-consequence rule in [cross-disciplinary-language-review-gate.md](../../../shared/cross-disciplinary-language-review-gate.md);
- logic connectors, source-role wording, table/figure sentences, and bilingual sentence structure follow [cross-disciplinary-language-review-gate.md](../../../shared/cross-disciplinary-language-review-gate.md);
- no bibliography-only source is implied as cited;
- terminology is consistent;
- Chinese and English terms are paired consistently in bilingual work;
- figure and table references match planned or existing artifacts.

For user-requested strict language review, apply [cross-disciplinary-language-review-gate.md](../../../shared/cross-disciplinary-language-review-gate.md) to the specified chapter, subsection, paragraph, or sentence only, and include every sentence in the review table.
