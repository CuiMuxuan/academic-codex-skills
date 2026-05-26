# Literature Search And Identity Workflow

Use this reference for literature discovery, DOI/title matching, bibliography cleanup, and identity verification.

## Define The Evidence Need

Identify:

- paper type and subject area;
- target chapter or claim category;
- required recency range if any;
- target examples: 3-10 accepted papers, approved theses, or target-journal examples when available;
- preferred source types: journal articles, conference papers, standards, books, patents, datasets, or policy documents;
- citation style or bibliography format if already known.

Before doing large searches or DOI checks, ask for missing materials:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

Ask for DOI lists, pasted bibliography, BibTeX/RIS/EndNote exports, draft text with in-body citations, PDFs, target examples, target recency range, preferred databases, and permission to browse or call APIs.

## Candidate List

For each candidate, capture:

- title;
- authors;
- year;
- venue;
- DOI;
- URL;
- source database or search path;
- intended use or target chapter;
- priority;
- notes.

Prefer authoritative sources such as publisher pages, Crossref, PubMed, Semantic Scholar, arXiv, IEEE, ACM, Springer, Elsevier, Wiley, official standards bodies, or university repositories. Use general search only as a fallback discovery surface.

## Verification Worklist

Use this table before and after checking:

| id | title or citation | current state | check needed | source trail | next action | writing-ready |
|---|---|---|---|---|---|---|
| local key | normalized title or raw citation | candidate/verified/unresolved/etc. | DOI/title/citation/evidence/manual | URL, database, file path, or pending | verify/reject/ask user/queue manual check | yes/no/user decision |

## Identity Verification

For each candidate:

1. Normalize the title.
2. Resolve the DOI when present.
3. Confirm the DOI landing page describes the same paper.
4. Cross-check year, venue, and first author across at least two authoritative sources when available.
5. Check for duplicates or translated-title duplicates.
6. Apply [trust-state-decision-gates.md](trust-state-decision-gates.md) before changing trust state.
7. Mark the state and record the verification source.

If DOI and title conflict, do not repair silently. Put the record in a mismatch list and search again.

## Multi-Source Script

When a bibliography has many candidate entries, prefer:

```bash
python scripts/multi_source_lit_check.py --input literature.csv --output literature_identity_audit.csv --mailto user@example.com
```

Use script output as an audit queue, not final truth. Promote a record only after reviewing proposed state, title similarity, DOI agreement, source URLs, and errors. For biomedical sources, PubMed evidence is high-value, but absence from PubMed is not evidence that a non-biomedical source is invalid.
