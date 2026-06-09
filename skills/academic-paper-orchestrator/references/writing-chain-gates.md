# Writing Chain Gates

Use this reference when the full project moves through writing, evidence-gap handling, review response, benchmark review, final polishing, or formatting.

## Gate Sequence

| Gate | Owner skill | Must wait for user confirmation before moving on? |
|---|---|---|
| Field and terminology confirmation | `$paper-writing-workflow` | Yes when inferred or unclear |
| Outline and paper design approval | `$paper-writing-workflow` | Yes before substantial drafting |
| Evidence precheck and `LIT_GAP` list | `$paper-writing-workflow` | Yes before drafting unsupported claim areas |
| New literature search/verification for gaps | `$academic-research-verification` | Yes before treating new sources as writing-ready unless user explicitly approves |
| Main-text or rebuttal claim support | `$paper-writing-workflow` + `$academic-research-verification` | Yes when required support is missing |
| Chapter or major section draft | `$paper-writing-workflow` | Yes before integrating or moving to the next major chapter |
| Reviewer/supervisor-comment revision plan | `$paper-writing-workflow` | Yes before substantial edits |
| Multi-comment action plan | `$paper-writing-workflow` or `$post-manuscript-benchmark-review` | Yes before editing when two or more comments are provided |
| Complete first draft benchmark review | `$post-manuscript-benchmark-review` | Yes on benchmark set and review plan before readiness judgment |
| Language-style review | `$language-style-review` | Yes before expanding beyond the requested manuscript scope |
| Formal sentence-level revision control | `$revision-control` | Yes before modifying sentences, finalizing pass/fail status, or starting upgrade work |
| Final de-AI/style polishing | `$academic-de-ai-polishing` | Yes after content, evidence, and structure are stable |
| Notation-sensitive conversion | `$academic-formatting-workflow` + `$academic-figure-workflow` | Yes before lossy formula, superscript/subscript, citation, or cross-reference conversion |
| Formatting baseline | `$academic-formatting-workflow` | Yes before final DOCX normalization |

If the user asks to skip a gate, state the risk and record the skip as a user decision.

## Route Distinctions

- Ordinary chapter drafting, introduction logic, abbreviation checks, terminology control, and comment-response planning go to `$paper-writing-workflow`.
- Literature gaps and source discovery go to `$academic-research-verification`.
- Complete first-draft readiness review against benchmark papers goes to `$post-manuscript-benchmark-review`.
- Language diagnosis without manuscript writing goes to `$language-style-review`.
- Sentence-level revision state, object libraries, and modification rounds go to `$revision-control`.
- Final polish, de-AI cadence reduction, and removal of internal project residue go to `$academic-de-ai-polishing`.
- Formatting and Markdown/DOCX conversion go to `$academic-formatting-workflow`.

## Gate Report Additions

For writing-chain gates, include:

```text
Current field:
Target venue/school field:
Evidence or LIT_GAP status:
Main-text/rebuttal support status:
Reviewer-comment action-plan status:
Language-style review status:
Revision-control status:
Notation/conversion risk:
User confirmation required:
Allowed next work:
Blocked work:
Recommended route:
```
