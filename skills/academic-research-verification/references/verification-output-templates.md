# Verification Output Templates

Use these templates when creating audit outputs or manual queues.

## Target Exemplar Intake

Ask whether the user can provide 3-10 target papers, approved theses, or accepted manuscripts from the intended field/outlet. Use them only to infer expected source types, recency range, citation style, and evidence density; do not treat their references as verified until checked.

## Manual Verification Queue

| id | raw citation | DOI | title | check needed | search string | expected source | status |
|---|---|---|---|---|---|---|
| local key | pasted entry | missing/provided | normalized | DOI/title/year/venue | exact query | Crossref/publisher/database | pending |

## DOI Mismatch Report

| id | supplied DOI | supplied title | resolved title | mismatch type | proposed action | user decision |
|---|---|---|---|---|---|
| local key | DOI | title | Crossref/publisher title | title/year/venue/author | reject/search/ask user | needed |

## Citation Audit Report

| issue | in-body key | bibliography key | location | action |
|---|---|---|---|---|
| missing bibliography | author-year | none | paragraph/section | add source or remove citation |
