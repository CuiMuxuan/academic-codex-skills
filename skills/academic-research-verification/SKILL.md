---
name: academic-research-verification
description: "Discover, verify, and audit academic literature for papers, theses, dissertations, and review articles. Use when the user needs literature search, DOI verification, title-DOI matching, citation authenticity checks, bibliography cleanup, evidence register maintenance, LIT_GAP or 待补证据 resolution, writing-ready source handoffs, or prevention of fabricated references. Chinese triggers: 文献检索, DOI核验, 引用真实性检查, 参考文献核对, 证据表, 文献可信度, 待补证据, 文献缺口, LIT_GAP."
---

# Academic Research Verification

Use this skill to build and protect the evidence base behind academic writing. Its job is not to draft prose; its job is to make sure sources, citations, and claims can be traced.

## Boundaries

Do:

- Discover, normalize, verify, and audit literature records.
- Maintain explicit source trails and trust states.
- Produce evidence registers, mismatch lists, manual queues, and citation audit reports.
- Convert writing `LIT_GAP` items into verified evidence or manual download/search queues.

Do not:

- Treat unverified sources as trusted.
- Invent DOI strings, article titles, author lists, venues, page ranges, or citation metadata.
- Present `candidate` or `unresolved` sources as writing-ready without a user decision.
- Draft manuscript prose as the primary task; route writing to `$paper-writing-workflow`.
- Backfill unsupported prose before the source is verified or explicitly approved.

## Core Rules

1. Verify before trusting: title, venue, year, author identity, and DOI or stable source URL must match.
2. Separate discovery from verification.
3. Keep an evidence register with explicit trust states.
4. Use reliable external sources for current or uncertain bibliographic data when network access is available.
5. Record source links and verification trails when browsing or API access is used.
6. If verification cannot be completed, mark the item `unresolved`.
7. For main-text or rebuttal support gaps, return a concrete reference download or material request list instead of backfilling prose.

## Intake

Identify the paper type, subject area, target chapter or claim category, `LIT_GAP` id or evidence need, recency range, target examples, preferred source types, citation style, and available bibliography/PDF/export files.

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
3. Apply [literature-gap-verification-workflow.md](references/literature-gap-verification-workflow.md) when resolving `LIT_GAP`, 待补证据, or writing evidence-gap lists.
4. Apply [literature-search-and-identity-workflow.md](references/literature-search-and-identity-workflow.md) for discovery, DOI/title matching, and identity checks.
5. Apply [trust-state-decision-gates.md](references/trust-state-decision-gates.md) before changing trust state or marking a source writing-ready.
6. Apply [citation-authenticity-audit.md](references/citation-authenticity-audit.md) when auditing an existing manuscript or bibliography.
7. Apply [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) when a writing or rebuttal handoff is blocked by missing support.
8. Return writing handoff evidence with claim/topic, claim-anchor id when provided, source, finding, method context, limitation, target chapter, citation key, verification state, support locator, and allowed claim strength.

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
- `lit_gap_resolution_report`;
- `writing_ready_evidence_handoff`;
- `citation_audit_report`;
- `search_strategy_note`.

Read [verification-output-templates.md](references/verification-output-templates.md) when preparing manual verification queues, DOI mismatch reports, or citation audit reports.

## Completion Criteria

- Each active source has a trust state.
- Verified sources include a stable source trail.
- Mismatches and unresolved items are explicit.
- The user can see which claims or chapters each source supports.
- Writing handoffs include evidence locations and allowed claim strength for central claims.
- No `candidate` or `unresolved` item is presented as writing-ready without an explicit user decision.

## Reference

Read [evidence-register-schema.md](references/evidence-register-schema.md) when creating or normalizing a literature master list, citation audit, or evidence register.

Read [trust-state-decision-gates.md](references/trust-state-decision-gates.md) when changing trust state or deciding writing readiness.

Read [literature-search-and-identity-workflow.md](references/literature-search-and-identity-workflow.md) for candidate discovery, DOI/title matching, and identity verification.

Read [literature-gap-verification-workflow.md](references/literature-gap-verification-workflow.md) when a writing workflow passes `LIT_GAP` markers, evidence-gap lists, or requests for new support before drafting.

Read [citation-authenticity-audit.md](references/citation-authenticity-audit.md) when checking in-body citations, bibliography entries, or claim support.

Read [main-text-and-rebuttal-claim-support-gate.md](../../shared/main-text-and-rebuttal-claim-support-gate.md) when missing support blocks main-text drafting or rebuttal response writing.

## Bundled Utilities

- `scripts/doi_batch_check.py`: extract DOI strings from text/CSV/TSV and query Crossref metadata into a CSV. Requires network access.
- `scripts/multi_source_lit_check.py`: cross-check candidate records across Crossref, OpenAlex, Semantic Scholar, and PubMed; outputs proposed states, title similarity, DOI agreement, URLs, and manual next actions. Requires network access.
- `scripts/citation_bib_audit.py`: first-pass author-year in-body citation vs bibliography consistency audit for plain-text drafts.
