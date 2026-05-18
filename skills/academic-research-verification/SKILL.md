---
name: academic-research-verification
description: "Discover, verify, and audit academic literature for papers, theses, dissertations, and review articles. Use when the user needs literature search, DOI verification, title-DOI matching, citation authenticity checks, bibliography cleanup, evidence register maintenance, or prevention of fabricated references. Chinese triggers: 文献检索, DOI核验, 引用真实性检查, 参考文献核对, 证据表, 文献可信度."
---

# Academic Research Verification

Use this skill to build and protect the evidence base behind academic writing. Its job is not to draft prose; its job is to make sure sources, citations, and claims can be traced.

## Core Rules

1. Verify before trusting: never mark a source as trusted until the title, venue, year, and DOI or stable source URL match.
2. Separate discovery from verification.
3. Keep an evidence register with explicit trust states.
4. Do not invent DOI strings, article titles, author lists, venues, page ranges, or citation metadata.
5. For current or uncertain bibliographic data, use reliable external sources when network access is available.
6. When browsing or API access is needed, tell the user what will be checked and record source links in the result.
7. If verification cannot be completed, mark the item as unresolved instead of quietly accepting it.

## Trust States

Use these states consistently:

| State | Meaning |
|---|---|
| `candidate` | Found or provided, not yet verified |
| `verified` | Bibliographic identity is confirmed |
| `downloaded` | Full text is available locally or lawfully accessible |
| `parsed` | Full text or key evidence has been extracted |
| `cited` | Used in the manuscript body |
| `rejected` | Duplicate, irrelevant, mismatched, retracted, or unreliable |
| `unresolved` | Cannot be confirmed with available access |

## Verification Decision Gates

Only change a record's trust state when the evidence for the change is visible in the register.

Use these gates:

| Decision | Required evidence |
|---|---|
| `candidate` -> `verified` | Title, year, venue, and author identity match an authoritative source; DOI resolves to the same work when a DOI exists |
| `verified` -> `downloaded` | Lawful full text or user-provided PDF is available locally or through a stable access path |
| `downloaded` -> `parsed` | Specific evidence locations or summaries have been extracted with source location and quality notes |
| any state -> `rejected` | Clear reason such as mismatch, duplicate, irrelevance, retraction, source unreliability, or user rejection |
| any state -> `unresolved` | Required metadata or source access is missing after reasonable checking |

Stop and ask the user before:

- Accepting a source with no DOI when the venue or metadata is weak.
- Repairing a DOI/title mismatch by choosing a replacement record.
- Keeping a suspicious source because it appears important to the manuscript.
- Using paywalled, manually supplied, or user-exported metadata as the only verification source.
- Moving `candidate` or `unresolved` items into a writing-ready evidence set.

Use this checkpoint format:

```text
Record:
Current state:
Proposed state:
Evidence for change:
Unresolved risk:
User decision needed:
```

## Workflow

### 1. Define The Evidence Need

Identify:

- Paper type and subject area.
- Target chapter or claim category.
- Required recency range if any.
- Target examples: 3-10 accepted papers, approved theses, or target-journal examples when available. Use them to infer source types, recency, and citation density; still verify every source independently.
- Preferred source types: journal articles, conference papers, standards, books, patents, datasets, or policy documents.
- Citation style or bibliography format if already known.

Output a short search-and-verification plan before doing large searches.

Before starting search, DOI checks, or citation audits, ask for missing materials that would materially improve verification quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for DOI lists, pasted bibliography, BibTeX/RIS/EndNote exports, draft text with in-body citations, PDFs, target examples, target recency range, preferred databases, and permission to browse or call APIs. If unavailable, create a manual verification queue and mark all identity checks that remain pending.

Use this verification worklist before and after checking:

| id | title or citation | current state | check needed | source trail | next action | writing-ready |
|---|---|---|---|---|---|---|
| local key | normalized title or raw citation | candidate/verified/unresolved/etc. | DOI/title/citation/evidence/manual | URL, database, file path, or pending | verify/reject/ask user/queue manual check | yes/no/user decision |

Set `writing-ready` to `yes` only when the source is verified and the relevant evidence is located or explicitly approved for the target writing task.

### 2. Build Candidate List

For each candidate, capture:

- Title.
- Authors.
- Year.
- Venue.
- DOI.
- URL.
- Source database or search path.
- Intended use or target chapter.
- Priority.
- Notes.

Prefer authoritative sources such as publisher pages, Crossref, PubMed, Semantic Scholar, arXiv, IEEE, ACM, Springer, Elsevier, Wiley, official standards bodies, or university repositories. Use general search only as a fallback discovery surface.

### 3. Verify Identity

For each candidate:

1. Normalize the title.
2. Resolve the DOI when present.
3. Confirm the DOI landing page describes the same paper.
4. Cross-check year, venue, and first author across at least two authoritative sources when available.
5. Check for obvious duplicates or translated-title duplicates.
6. Apply the verification decision gates before changing trust state.
7. Mark the state and record the verification source.

If the DOI and title conflict, do not repair silently. Put the record in a mismatch list and search again.

When a bibliography has many candidate entries, prefer the multi-source script before manual checking:

```bash
python scripts/multi_source_lit_check.py --input literature.csv --output literature_identity_audit.csv --mailto user@example.com
```

Use the script output as an audit queue, not as final truth. Promote a record only after reviewing the proposed state, title similarity, DOI agreement, source URLs, and errors. For biomedical sources, PubMed evidence is high-value but absence from PubMed is not evidence that a non-biomedical source is invalid.

### 4. Check Citation Authenticity

When auditing an existing manuscript or bibliography:

- Match every in-body citation to a bibliography entry.
- Match every bibliography entry to at least one in-body citation unless the user is intentionally keeping a reading list.
- Identify references with missing DOI, impossible year/venue combinations, broken links, or title-author mismatches.
- Flag claims that cite a source but are not actually supported by the source summary or extracted evidence.

Do not use a citation as support for a claim until the source has been verified and the relevant evidence has been located.

### 5. Support Writing Without Writing For It

Return evidence in a form the writing skill can use:

- Claim or topic.
- Supporting source.
- Specific finding.
- Method or context.
- Limitations.
- Suggested target chapter.
- Citation key or short label.
- Verification state.

Avoid producing polished manuscript paragraphs unless the user explicitly asks. If they do, keep citation uncertainty visible.

## Network And API Boundaries

Use browsing or APIs when the user requests current verification, DOI resolution, or source links. If network access is unavailable:

- Create a manual verification queue.
- Include exact search strings.
- Separate confirmed local metadata from unconfirmed metadata.
- Ask the user to provide exported BibTeX, RIS, DOI list, or PDFs when needed.

Do not claim that a source is verified from memory.

## Outputs

Use one or more of these outputs:

- `literature_master.csv` or table.
- `doi_mismatch_list`.
- `missing_metadata_list`.
- `unverified_or_unresolved_list`.
- `evidence_register`.
- `citation_audit_report`.
- `search_strategy_note`.

## Bundled Utilities

- `scripts/doi_batch_check.py`: extract DOI strings from text/CSV/TSV and query Crossref metadata into a CSV. Requires network access.
- `scripts/multi_source_lit_check.py`: cross-check candidate records across Crossref, OpenAlex, Semantic Scholar, and PubMed; outputs proposed states, title similarity, DOI agreement, URLs, and manual next actions. Requires network access.
- `scripts/citation_bib_audit.py`: first-pass author-year in-body citation vs bibliography consistency audit for plain-text drafts.

Read [verification-output-templates.md](references/verification-output-templates.md) when preparing manual verification queues, DOI mismatch reports, or citation audit reports.

## Completion Criteria

A verification task is complete when:

- Each active source has a trust state.
- Verified sources include a stable source trail.
- Mismatches and unresolved items are explicit.
- The user can see which claims or chapters each source supports.
- No `candidate` or `unresolved` item is presented as writing-ready without an explicit user decision.

## Reference

Read [evidence-register-schema.md](references/evidence-register-schema.md) when creating or normalizing a literature master list, citation audit, or evidence register.
