# Project Artifact Templates

Use these templates when coordinating a full paper, thesis, or manuscript project. If the user provides 3-10 final target examples, use them to set the project baseline before routing work to focused skills. If no examples are provided, mark the baseline as provisional.

## Target Exemplar Request

Ask once at project start:

```text
Please provide 3-10 target examples if available:
- accepted papers from the target journal or conference
- approved theses from the same school or department
- supervisor-approved chapters or reports
- Word templates, LaTeX templates, author guidelines, or formatting handbooks

If none are available, I will proceed with a provisional general academic baseline and mark assumptions explicitly.
```

## Project State File

```text
current_mode:
paper_type:
language:
target_standard:
current_field:
target_venue_field:
target_examples:
material_passports:
materials:
evidence_status:
draft_status:
figure_status:
format_status:
current_gate:
open_risks:
next_step:
```

## Material Passport Block

Use this block for any artifact that will be consumed by more than one stage. For field definitions, read [material-passport-schema.md](material-passport-schema.md).

```text
material_id:
artifact_type:
path_or_source:
stage_owner:
data_access_level:
task_type:
verification_state:
allowed_uses:
restrictions:
source_trail:
handoff_status:
user_decisions:
```

## Handoff Packet Template

| from | to | artifact | required fields | status | gate |
|---|---|---|---|---|---|
| parsing | research | extracted bibliography | DOI/title/authors/year/source path/quality | ready/unresolved | verify before writing |

## Claim Anchor Template

Use this compact format when a claim must survive writing, review, polishing, and formatting without drifting.

```text
claim_anchor_id:
claim_summary:
manuscript_location:
support_type: literature | data | code | result | figure | user_decision
support_locator:
allowed_claim_strength:
verification_state:
owner_skill:
open_risk:
```

## Target Baseline Note

```text
Source:
What to match:
What not to copy:
Known assumptions:
Applies to:
```
