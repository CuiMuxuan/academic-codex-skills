---
name: academic-research-verification
description: "Discover, verify, and audit academic literature for papers, theses, dissertations, and review articles. Use when the user needs literature search, DOI verification, title-DOI matching, citation authenticity checks, bibliography cleanup, evidence register maintenance, or prevention of fabricated references. Chinese triggers: 文献检索, DOI核验, 引用真实性检查, 参考文献核对, 证据表, 文献可信度."
---

# Academic Research Verification

Use this skill to build and protect the evidence base behind academic writing. Its job is not to draft prose; its job is to make sure sources, citations, and claims can be traced.

## Boundaries

Do:

- Discover, normalize, verify, and audit literature records.
- Maintain explicit source trails and trust states.
- Produce evidence registers, mismatch lists, manual queues, and citation audit reports.

Do not:

- Treat unverified sources as trusted.
- Invent DOI strings, article titles, author lists, venues, page ranges, or citation metadata.
- Present `candidate` or `unresolved` sources as writing-ready without a user decision.
- Draft manuscript prose as the primary task; route writing to `$paper-writing-workflow`.

## Core Rules

1. Verify before trusting: title, venue, year, author identity, and DOI or stable source URL must match.
2. Separate discovery from verification.
3. Keep an evidence register with explicit trust states.
4. Use reliable external sources for current or uncertain bibliographic data when network access is available.
5. Record source links and verification trails when browsing or API access is used.
6. If verification cannot be completed, mark the item `unresolved`.

## Intake

Identify the paper type, subject area, target chapter or claim category, recency range, target examples, preferred source types, citation style, and available bibliography/PDF/export files.

Before search, DOI checks, or citation audits, ask for missing materials that would materially improve verification quality:

```text
Required or high-value materials:
Missing materials:
Can proceed without them: yes/no
Fallback if unavailable:
```

## Workflow

1. Define the evidence need and output a short search-and-verification plan.
2. Build or normalize the candidate list.
3. Apply [literature-search-and-identity-workflow.md](references/literature-search-and-identity-workflow.md) for discovery, DOI/title matching, and identity checks.
4. Apply [trust-state-decision-gates.md](references/trust-state-decision-gates.md) before changing trust state or marking a source writing-ready.
5. Apply [citation-authenticity-audit.md](references/citation-authenticity-audit.md) when auditing an existing manuscript or bibliography.
6. Return writing handoff evidence with claim/topic, source, finding, method context, limitation, target chapter, citation key, and verification state.

## Network And API Boundaries

Use browsing or APIs when the user requests current verification, DOI resolution, or source links. If network access is unavailable, create a manual verification queue with exact DOI/title/search strings and ask for BibTeX, RIS, DOI lists, PDFs, or exported metadata.

Do not claim that a source is verified from memory.

## Outputs

Use one or more:

- `literature_master.csv` or table;
- `doi_mismatch_list`;
- `missing_metadata_list`;
- `unverified_or_unresolved_list`;
- `evidence_register`;
- `citation_audit_report`;
- `search_strategy_note`.

Read [verification-output-templates.md](references/verification-output-templates.md) when preparing manual verification queues, DOI mismatch reports, or citation audit reports.

## Completion Criteria

- Each active source has a trust state.
- Verified sources include a stable source trail.
- Mismatches and unresolved items are explicit.
- The user can see which claims or chapters each source supports.
- No `candidate` or `unresolved` item is presented as writing-ready without an explicit user decision.

## Reference

Read [evidence-register-schema.md](references/evidence-register-schema.md) when creating or normalizing a literature master list, citation audit, or evidence register.

Read [trust-state-decision-gates.md](references/trust-state-decision-gates.md) when changing trust state or deciding writing readiness.

Read [literature-search-and-identity-workflow.md](references/literature-search-and-identity-workflow.md) for candidate discovery, DOI/title matching, and identity verification.

Read [citation-authenticity-audit.md](references/citation-authenticity-audit.md) when checking in-body citations, bibliography entries, or claim support.

## Bundled Utilities

- `scripts/doi_batch_check.py`: extract DOI strings from text/CSV/TSV and query Crossref metadata into a CSV. Requires network access.
- `scripts/multi_source_lit_check.py`: cross-check candidate records across Crossref, OpenAlex, Semantic Scholar, and PubMed; outputs proposed states, title similarity, DOI agreement, URLs, and manual next actions. Requires network access.
- `scripts/citation_bib_audit.py`: first-pass author-year in-body citation vs bibliography consistency audit for plain-text drafts.
