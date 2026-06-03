# Citation Authenticity Audit

Use this reference when auditing an existing manuscript, bibliography, reference list, or claim-evidence relationship.

## Audit Checks

- Match every in-body citation to a bibliography entry.
- Match every bibliography entry to at least one in-body citation unless the user intentionally keeps a reading list.
- Identify references with missing DOI, impossible year/venue combinations, broken links, or title-author mismatches.
- Flag claims that cite a source but are not supported by the source summary or extracted evidence.
- Flag citation-placement problems using [citation-proximity-and-style-gate.md](../../../shared/citation-proximity-and-style-gate.md).
- Do not use a citation as support for a claim until the source has been verified and the relevant evidence has been located.

## Manual Queue

When verification cannot be completed, create a manual queue:

| item | issue | exact search string | current evidence | needed decision |
|---|---|---|---|---|
| citation key or title | missing DOI/title mismatch/etc. | title + first author + year | local metadata/source trail | verify/reject/replace/user decision |

If network or API access is unavailable:

- separate confirmed local metadata from unconfirmed metadata;
- include exact DOI/title/search strings;
- ask the user for exported BibTeX, RIS, DOI list, or PDFs;
- mark records unresolved instead of treating them as verified.

## Writing Handoff

Return evidence in a form the writing skill can use:

- claim or topic;
- supporting source;
- specific finding;
- method or context;
- limitations;
- suggested target chapter;
- citation key or short label;
- verification state.

Avoid polished manuscript paragraphs unless explicitly requested. If prose is requested, keep citation uncertainty visible.
