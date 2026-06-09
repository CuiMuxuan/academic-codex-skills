# Revision Round Workflow

## Startup

1. Confirm project path, manuscript path, target scope, language, and output format.
2. Locate or create `revision_workbench`.
3. Build the complete manuscript object library.
4. Generate the complete original bilingual sentence review draft.
5. Generate the complete latest bilingual sentence review draft.
6. Read project standards, terminology, problem-word list, and material dependency records.
7. If the user selected a local scope, still load the complete object library to check context fit and duplicate arguments.

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
4. Produce suggested pass/fail status.
5. Wait for user confirmation.

Accepted confirmation examples:

- `2.1 全部通过`
- `第 3 段未通过`
- `S2.1.4-S2.1.9 通过，S2.1.10 回退未通过`
- `Only revise failed sentences in Section 4.2`

## Modification Execution

1. Modify only user-confirmed failed or requested target sentences.
2. Use project standards, terminology, problem words, language-style review, quality review, and user sentence comments.
3. Use `$academic-de-ai-polishing` only for confirmed local mechanical-style or residue problems when evidence and structure are stable.
4. Send structure, evidence, chapter logic, literature, and large rewrite issues to the upgrade flow.
5. Increment `revision_count` for every modified sentence.
6. Update complete latest review draft.
7. Update partial failed-sentence review draft.
8. Update object library, modification log, user confirmation log, and id mapping.

## Round Close

1. Save object library snapshot.
2. Save full original review snapshot.
3. Save full latest review snapshot.
4. Save partial failed-sentence review snapshot.
5. Save modification log.
6. Save user confirmation log.
7. Generate next-round todo list.
8. Before the next round, renumber current ids and preserve history mapping.
