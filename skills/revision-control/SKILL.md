---
name: revision-control
description: "Manage sentence-level academic manuscript revision after or during drafting. Use when the user asks for formal revision,逐句修改,逐句审阅,修改轮次,句子通过/未通过确认,运行/打开/启动论文修改UI,运行/打开/启动批注UI,论文修改界面,批注界面,审稿批注界面, revision annotation UI, revision round control, object library maintenance, latest bilingual sentence review drafts, partial failed-sentence review drafts, project supplemental review standards, material dependency tracking, user confirmation logs, modification logs, or escalation plans for literature补充, structure重组, chapter rewriting, or large-scale rewriting. Coordinates language-style-review, post-manuscript-benchmark-review, academic-de-ai-polishing, paper-writing-workflow, and academic-research-verification results."
---

# Revision Control

Use this skill as the state owner for formal manuscript revision. It builds and maintains the object library, revision workbench, round folders, latest review drafts, pass/fail status, user confirmations, modification logs, shared project standards, and escalation plans.

## Boundaries

Do:

- Build or update the complete manuscript object library before local sentence edits.
- Maintain full original review drafts, full latest review drafts, and partial failed-sentence review drafts.
- Track revision rounds, sentence status, revision counts, id mappings, user confirmations, and modification logs.
- Coordinate reports from `$language-style-review`, `$post-manuscript-benchmark-review`, `$academic-de-ai-polishing`, and `$paper-writing-workflow`.
- Register supporting material paths, purpose, and changes without inserting support files into the sentence object library.
- Pause sentence editing and create an upgrade plan when the issue requires literature补充, evidence work, structural rewrite, chapter reorganization, or large-scale rewriting.

Do not:

- Provide official rewritten sentences when no `revision_workbench`, complete object library, or full-manuscript context is available.
- Rewrite unsupported superiority, novelty, contribution, or comparison claims into official manuscript text when required benchmark literature, baseline results, metrics, or evidence are missing.
- Treat a single paragraph as sufficient context when a project object library or full draft exists.
- Directly verify literature identity as final authority; route to `$academic-research-verification`.
- Silently confirm sentence pass/fail status without user confirmation.
- Update project supplemental standards without explicit user approval.
- Pollute the manuscript object library with support-paper notes, source PDFs, raw comments, or project-management files.

## Core Rules

1. Create or load `revision_workbench` before official revision.
2. Build a complete object library even when the requested edit scope is local.
3. Keep complete original and complete latest sentence-review drafts as whole-manuscript artifacts.
4. Keep partial failed-sentence review drafts limited to user-confirmed failed or requested target sentences.
5. Reset sentence attributes and renumber at each new round while preserving id mapping history.
6. Increment `revision_count` on every sentence modification.
7. Record deleted, merged, split, and derived sentence relationships; never let source sentence identity vanish.
8. Wait for user confirmation before final pass/fail decisions and before any upgrade work.
9. If the user provides only a local paragraph and asks for direct sentence edits, respond with `context_insufficient_for_formal_revision`, list required materials, and offer to create the workbench; do not present a polished replacement as the official modification.
10. If the requested sentence depends on missing benchmark literature, baseline experiments, metrics, data, or evidence, respond with `upgrade_required` and draft an upgrade plan instead of giving a formal replacement sentence.

## Sentence Pass/Fail Rules

- Sentence status has only two user states: `pass` and `fail`.
- Treat every sentence as `fail` by default until the user explicitly marks it `pass`.
- You may proactively suggest which sentence ids appear ready to pass, but the suggestion is not final status.
- Accept user confirmation from conversation, such as "S2.1.4 通过" or "接受你刚才建议的通过句子", and record those sentence ids as user-confirmed `pass`.
- In the annotation UI, the user may click the `通过 / Pass` or `未通过 / Fail` tag/button on a sentence row to change that sentence's user state.
- Do not use `pending`, `needs_user_decision`, or assistant suggestions as UI sentence states. Use upgrade or decision-needed wording only in analysis, comments, or task routing, not as the persisted sentence pass/fail state.

## Automatic Annotation UI Launch

When the user asks to run, open, start, or use the paper revision annotation UI, launch the bundled UI instead of only explaining it. Treat these as launch requests:

- Chinese examples: `运行论文修改UI`, `打开论文修改界面`, `启动批注UI`, `打开审稿批注界面`, `用界面做逐句修改`, `用鼠标批注论文`, `运行这个UI进行论文修改`, `打开 revision annotation UI`.
- English examples: `run the revision annotation UI`, `open the manuscript annotation UI`, `start the paper revision UI`, `use the UI for sentence revision annotations`.

Before launch, locate the active `revision_workbench` and round id. Ensure required UI support resources exist first. This includes `shared/project_review_standards.*`, `shared/terminology_glossary.*`, `shared/problem_words.*`, and `shared/material_dependencies.*`. If any are missing, create them before opening the UI; generate `terminology_glossary.yaml/md` as project-specific candidate terminology from the manuscript object library, with entries marked unconfirmed until the user edits or confirms them. For bilingual projects, each English term should include likely `chinese_translations` inferred from the aligned Chinese review text when possible, and Chinese terms/translations must also be available for shallow-green terminology highlighting in the UI. The project supplemental review standards template must state the paper's research field when known and include a candidate rule to avoid unnecessary artificial-intelligence, computer-science, or electronic-information jargon unless those terms genuinely belong to the paper's field or the user confirms them. Generic cross-field terms do not need special restriction.

If support resources are missing, run:

```bash
python skills/revision-control/scripts/ensure_revision_ui_resources.py --path <revision_workbench_path_or_round_path>
```

Then launch the UI:

```bash
python skills/revision-control/scripts/revision_annotation_ui.py --workbench <revision_workbench_path> --round <round_id> --open
```

If the workbench or round id is missing, ask one concise question for the missing path or round. If no object library exists at `revision_workbench/bilingual_revision/manuscript_objects.json`, do not launch; create or request the object library first. The UI remains an annotation collector only and must write only `revision_workbench/bilingual_revision/rounds/<round_id>/user_annotations.json`.

The bundled UI is Chinese-English bilingual for visible controls while preserving English JSON enum values. It uses a chapter stepper plus active-chapter virtual scrolling to keep large bilingual manuscripts responsive.

## Workflow

1. Use [revision-workbench-structure.md](references/revision-workbench-structure.md) to locate or create directories, shared project files, and round folders.
2. Use [object-model-and-state.md](references/object-model-and-state.md) and [manuscript-object-model.md](../../shared/manuscript-object-model.md) to build paper, chapter, section, paragraph, sentence, and figure/table text objects.
3. Use [round-workflow.md](references/round-workflow.md) for startup, each round start, sentence check, user confirmation, modification execution, and round close.
4. Use [project-standards-and-materials.md](references/project-standards-and-materials.md) and [project-review-standards-schema.md](../../shared/project-review-standards-schema.md) for supplemental standards, terminology, problem words, and material dependencies.
5. Use [upgrade-flow.md](references/upgrade-flow.md) and [revision-upgrade-plan-schema.md](../../shared/revision-upgrade-plan-schema.md) when sentence editing must pause for evidence, structure, or large rewrite work.
6. Use [templates-and-logs.md](references/templates-and-logs.md) and the `template-*` files when creating object libraries, review drafts, logs, and upgrade plans.
7. Use [artifact-synchronization.md](references/artifact-synchronization.md) after any object-library, latest-draft, annotation, pass/fail, or shared-resource change. Run the public sync utility and then check the sync report before continuing official revision.
8. Use [equation-and-formula-standard.md](../../shared/equation-and-formula-standard.md) whenever formulas, equations, inline math, chemical notation, unit notation, or equation references appear in manuscript objects, revision drafts, UI rendering, or formatting handoffs.

## Missing Context Response

When formal revision is requested but the workbench or complete object library is missing, return this shape instead of rewriting:

```text
Status: context_insufficient_for_formal_revision
Cannot perform official sentence modification yet because:
- no complete manuscript object library is available;
- no full latest sentence-review draft is available;
- no round directory or user-confirmation log is active.

Required to proceed:
- manuscript path or full draft text;
- target scope;
- permission to create or locate revision_workbench;
- field, language, and target standard if available.

Allowed now:
- create a provisional issue list;
- prepare candidate checks for user review;
- create the revision workbench and object library if the user confirms.
```

When evidence is missing for the requested modification, use this instead:

```text
Status: upgrade_required
Cannot perform official sentence modification yet because the sentence depends on missing support:
- missing benchmark literature:
- missing baseline results:
- missing metric/data support:

Required upgrade plan:
- route literature or citation verification to $academic-research-verification;
- define required baseline/evidence materials;
- identify affected sentence/object ids;
- wait for user confirmation before changing the manuscript.

Allowed now:
- propose a conservative direction for later wording;
- mark the claim as hold_for_more_evidence or soften_after_upgrade;
- create an upgrade plan.
```

## Handoff Rules

- Receive language issue reports from `$language-style-review`; execute only user-confirmed modifications.
- Receive readiness and gap reports from `$post-manuscript-benchmark-review`; convert them into round priorities or upgrade plans.
- Use `$academic-de-ai-polishing` only as a rewrite tactic provider for confirmed local language issues after evidence and structure boundaries are stable.
- Call `$paper-writing-workflow` for confirmed chapter/section rewriting after an upgrade plan is approved.
- Call `$academic-research-verification` when new literature, DOI/title checks, citation authenticity, or `LIT_GAP` resolution is required.

## Reference

Read [revision-control-contract.md](../../shared/revision-control-contract.md) when coordinating this skill with orchestrator, language review, post-draft review, writing, research verification, or polishing.

Read [revision-workbench-structure.md](references/revision-workbench-structure.md) before creating or auditing a revision project directory.

Read [round-workflow.md](references/round-workflow.md) before starting or closing a revision round.

Read [object-model-and-state.md](references/object-model-and-state.md) before changing object ids, sentence status, split/merge records, or revision counts.

Read [project-standards-and-materials.md](references/project-standards-and-materials.md) before using project standards or modifying material dependency records.

Read [upgrade-flow.md](references/upgrade-flow.md) before pausing sentence-level work for evidence, structure, or large rewriting.

Read [templates-and-logs.md](references/templates-and-logs.md) before writing any revision artifact.

Read [annotation-ui-technical-plan.md](references/annotation-ui-technical-plan.md) before implementing, running, or modifying the lightweight local UI for collecting user annotations into `user_annotations.json`.

Read [artifact-synchronization.md](references/artifact-synchronization.md) before regenerating or validating derived revision artifacts from `manuscript_objects.json`.

Read [equation-and-formula-standard.md](../../shared/equation-and-formula-standard.md) before changing, displaying, or handing off formulas/equations.

## Bundled Utilities

- `scripts/revision_annotation_ui.py`: starts the lightweight local browser UI for collecting user annotations from `manuscript_objects.json` and writing only `rounds/<round_id>/user_annotations.json`.
- `scripts/ensure_revision_ui_resources.py`: creates required UI support resources under `revision_workbench/shared/`, including project supplemental review standards, terminology glossary candidates generated from `manuscript_objects.json`, problem-word records, and material-dependency records. Run this before launching the annotation UI.
- `scripts/rebuild_manuscript_objects_from_main.py`: rebuilds `manuscript_objects.json` from the canonical active main manuscript while preserving existing sentence ids and bilingual sentence text from a sentence-aligned review draft; use when paragraph objects were incorrectly created from sentence-aligned review items.
- `scripts/sync_revision_artifacts.py`: public synchronization entry point. Regenerates and validates object-library summary, latest full bilingual review, partial failed/targeted review, manifest metadata, shared UI resources, and terminology schema from `manuscript_objects.json` plus the active round annotations. Run after object-library or official revision changes, then re-run with `--check-only`.
