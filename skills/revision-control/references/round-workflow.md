# Revision Round Workflow

## Startup

1. Confirm project path, canonical active manuscript path, optional sentence-aligned bilingual review path, target scope, language, and output format.
2. Locate or create `revision_workbench`.
3. Build the complete manuscript object library from the canonical active manuscript so paragraph objects preserve the manuscript's natural paragraph or structural-block boundaries.
4. Use any sentence-aligned bilingual review draft only as an alignment/review-text source, not as the paragraph-boundary source.
5. Generate the complete original bilingual sentence review draft.
6. Generate the complete latest bilingual sentence review draft.
7. Run the object-library source sanity check from [object-model-and-state.md](object-model-and-state.md).
8. Before launching or entering the annotation UI, ensure the project-level shared resources exist: `project_review_standards.*`, `terminology_glossary.*`, `problem_words.*`, and `material_dependencies.*`. If missing, generate them under `revision_workbench/shared/`; initialize terminology candidates from the current `manuscript_objects.json`, include likely `chinese_translations` for English terms from aligned Chinese review text when available, and mark them unconfirmed.
9. For bilingual projects, also ensure paper/chapter/section objects carry explicit bilingual title fields (`title_en`, `title_zh`, `bilingual_title`, `title_translation_status`, `title_translation_source`). If those fields are missing, add them during object-library initialization or run the title migration script with a title map before launching the UI.
10. Initialize terminology entries with field/domain, term type, and source provenance. If a term is a proper noun, named method, regulation, source-specific concept, or cited term, record the source sentence or cited paper where it appears.
11. Initialize the project supplemental review standards template with the research field when known and a candidate rule warning against unnecessary artificial-intelligence, computer-science, or electronic-information jargon unless the current paper's field requires it or the user confirms it. Do not restrict generic terms broadly understood across fields.
12. Run [artifact-synchronization.md](artifact-synchronization.md) before launching the UI or starting official modification so derived review drafts and shared resources agree with `manuscript_objects.json`.
13. Read project standards, terminology, problem-word list, and material dependency records.
14. If the user selected a local scope, still load the complete object library to check context fit and duplicate arguments.

## Object-Library Source Gate

Do not treat a sentence-aligned review draft as a natural paragraph object library. If the generated object library's source is a sentence-by-sentence review draft, or if most paragraph objects contain exactly one sentence because they were created from `S0001`, `S0002`, etc. items, mark the library as `paragraph_source_mode: sentence_aligned_review_only` and rebuild from the active main manuscript before paragraph-level or section-flow revision.

Allowed with a sentence-aligned-only object library:

- sentence-level annotation;
- sentence pass/fail collection;
- text-span comments within known sentence ids.

Blocked until rebuild from the active main manuscript:

- natural paragraph-level logic review;
- paragraph sequencing and section-flow judgments;
- UI claims that paragraph cards correspond to main-manuscript paragraphs.

## Missing Workbench Gate

If no `revision_workbench`, complete object library, or full latest sentence-review draft is available, do not provide official rewritten sentences. Return:

```text
Status: context_insufficient_for_formal_revision
Required materials:
- manuscript path or full draft text
- target scope
- permission to create or locate revision_workbench
- field, language, and target standard if available
Allowed now:
- provisional issue list
- candidate checks
- workbench/object-library creation after user confirmation
Blocked work:
- official sentence modification
- pass/fail state update
- latest full review draft update
- modification log update
```

Candidate wording may be shown only if clearly labelled `non-final diagnostic example`, and it must not be presented as the modified manuscript.

## Evidence Upgrade Gate

If a confirmed failed sentence contains an unsupported superiority, novelty, contribution, mechanism, or comparison claim, and the required literature, baseline, metrics, data, or evidence are missing, do not provide the formal replacement sentence. Return:

```text
Status: upgrade_required
Trigger reason:
- missing benchmark literature / baseline result / metric support / source evidence
Blocked work:
- official sentence modification
- latest full review draft update
Required upgrade plan:
- affected object ids
- needed evidence or materials
- skill route, such as academic-research-verification or paper-writing-workflow
- state that will reset after upgrade
- user decisions required
Allowed now:
- conservative wording direction labelled non-final
- claim triage such as hold_for_more_evidence or soften_after_upgrade
```

## Round Start

1. Create `rounds/round_NNN`.
2. If the user explicitly asks for benchmark or quality review, incorporate `$post-manuscript-benchmark-review` output; otherwise skip it.
3. Run sentence-level check for the target scope.
4. Produce suggested pass/fail status. Treat every sentence as `fail` by default until the user confirms `pass`.
5. You may proactively list sentence ids that appear ready to pass. These are suggestions only, not final state.
6. Wait for user confirmation, either in conversation or through the annotation UI pass/fail controls.

Accepted confirmation examples:

- `2.1 全部通过`
- `第 3 段未通过`
- `S2.1.4-S2.1.9 通过，S2.1.10 回退未通过`
- `接受你建议的通过句子`
- `Only revise failed sentences in Section 4.2`

## Modification Execution

1. Modify only user-confirmed failed or requested target sentences.
2. Use project standards, terminology, problem words, language-style review, quality review, and user sentence comments.
3. Use `$academic-de-ai-polishing` only for confirmed local mechanical-style or residue problems when evidence and structure are stable.
4. Send structure, evidence, chapter logic, literature, and large rewrite issues to the upgrade flow.
5. Increment `revision_count` for every modified sentence.
6. Update `manuscript_objects.json` first, preserving sentence ids, split/merge/delete mappings, revision counts, and formula LaTeX source when present.
7. Run `scripts/sync_revision_artifacts.py --workbench <revision_workbench> --round <round_id>` to regenerate the complete latest review draft, partial failed/targeted review draft, object-library summary, manifest, and project-resource schema.
8. Re-run the same utility with `--check-only`. Do not continue if the sync report contains count mismatches, unknown target ids, malformed terminology records, or unresolved formula/equation integrity issues.
9. Update modification log, user confirmation log, and id mapping.

## Round Close

1. Save object library snapshot.
2. Save full original review snapshot.
3. Save full latest review snapshot.
4. Save partial failed-sentence review snapshot.
5. Save modification log.
6. Save user confirmation log.
7. Generate next-round todo list.
8. Before the next round, renumber current ids and preserve history mapping.
9. Run artifact synchronization and inspect `artifact_sync_report.json` before treating the round artifacts as closed.
