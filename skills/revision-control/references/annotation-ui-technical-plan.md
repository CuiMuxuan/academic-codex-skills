# Revision Annotation UI Technical Plan

## Purpose

Build a lightweight local annotation UI for `revision-control`. The UI collects user feedback on manuscript sections, paragraphs, sentences, text spans, and sentence gaps, then writes a fixed JSON file that `revision-control` can read before formal modification.

The UI is an annotation collector only. It must not rewrite the manuscript, update official pass/fail state in `manuscript_objects.json` or round logs, update the latest full review draft, or create official modification logs by itself. It may collect user pass/fail decisions inside `user_annotations.json` for later `revision-control` processing.

## Minimal Technology Stack

Use the smallest distributable stack:

- Python 3 standard library only.
- Browser-native HTML, CSS, and JavaScript.
- No Node.js.
- No React, Vue, Electron, Tauri, npm, bundler, database, or third-party Python package.

Package as one script inside this skill:

```text
skills/revision-control/scripts/revision_annotation_ui.py
```

The Python script should embed the HTML, CSS, and JavaScript as strings and serve them through a local HTTP server.

Keep this stack unless profiling shows a single rendered chapter is still too large to scroll smoothly. The first performance lever is not a framework replacement; it is reducing live DOM size, rendering only the active chapter, and virtualizing that chapter's paragraph rows with measured dynamic row heights. Browser-native lazy layout can be considered for non-virtual static lists, but virtual paragraph rows must not rely on low fixed intrinsic heights that can clip long paragraphs. Consider a heavier frontend stack only after chapter-scoped rendering, virtual scrolling, and native browser optimizations are insufficient.

Run command:

```powershell
python skills/revision-control/scripts/revision_annotation_ui.py --workbench C:\path\to\revision_workbench --round round_001
```

Default local URL:

```text
http://127.0.0.1:8765
```

## Input Files

The canonical parse target is:

```text
revision_workbench/bilingual_revision/manuscript_objects.json
```

The UI must treat this file as the source of truth for the manuscript tree and object ids.

Optional input files:

```text
revision_workbench/bilingual_revision/figure_table_text_objects.json
revision_workbench/bilingual_revision/latest_full_bilingual_review.md
revision_workbench/bilingual_revision/partial_failed_sentence_review.md
revision_workbench/bilingual_revision/rounds/<round_id>/sentence_check_results.md
revision_workbench/shared/terminology_glossary.yaml
revision_workbench/shared/terminology_glossary.md
```

Before opening the UI, `revision-control` should create the shared project-support files if they are missing. At minimum this includes `project_review_standards.*`, `terminology_glossary.*`, `problem_words.*`, and `material_dependencies.*` under `revision_workbench/shared/`. Initialize `terminology_glossary.yaml/md` from the manuscript object library as project-specific, unconfirmed candidate terminology. In bilingual projects, each English term should carry likely `chinese_translations` inferred from the aligned Chinese review text when possible. If `shared/terminology_glossary.yaml` still does not exist, the manuscript view must not render terminology highlighting.

Each terminology entry must also carry `field`, `term_type`, and `source_provenance` so the UI can show why a term is treated as project-specific. The UI may highlight unconfirmed candidates, but the terminology-management page must let the user edit the field/domain and provenance before treating the entry as a durable project standard.

Initialize `project_review_standards.yaml/md` as a project supplemental standard template. The template should name the research field when known and include a candidate rule that warns against unnecessary artificial-intelligence, computer-science, or electronic-information jargon unless such terminology belongs to the paper's field or is user-confirmed. Generic terms broadly understood across academic fields do not need special restriction.

Do not parse DOCX, PDF, or free Markdown as the UI source. Those formats must first go through `revision-control` or upstream parsing to generate `manuscript_objects.json`.

## Fixed Output File

The UI writes annotations to:

```text
revision_workbench/bilingual_revision/rounds/<round_id>/user_annotations.json
```

Autosave after each annotation change. Also provide a manual "Save" button.

The manual save button is a fallback/flush control only. Normal text-span annotations, issue edits, deletes, and sentence pass/fail decisions should autosave immediately after the user action.

The terminology-management page writes only:

```text
revision_workbench/shared/terminology_glossary.yaml
revision_workbench/shared/terminology_glossary.md
```

Creating, editing, or deleting terminology entries in that page is a user-confirmed standards update. The manuscript annotation view must only read the glossary for highlighting and must not silently add terms.

If the round directory does not exist, the Python service may create it only after explicit user confirmation in the UI or a command-line flag:

```text
--create-round
```

## Full Draft vs Partial Failed Draft

Use one object library and two views.

### Full Manuscript View

Read every object from `manuscript_objects.json`, but do not render the complete manuscript into the DOM at once. Show a chapter stepper above the manuscript. Switching chapters replaces the active chapter model while preserving the shared annotation document. Within the active chapter, virtualize section/paragraph rows so that only the visible rows plus an overscan buffer are mounted in the DOM. Virtualized paragraph rows must not use a fixed clipping height: estimate initial height from text length, then measure the mounted DOM row and update subsequent offsets from the real rendered height so long paragraphs render completely.

```text
Paper
  Chapter
    Section
      Paragraph
        Sentence
        Sentence
```

### Failed/Targeted View

Still read the complete object library, but filter visible sentences using:

```text
partial_failed_sentence_review.md
rounds/<round_id>/sentence_check_results.md
user_annotations.json
```

The partial view must keep parent chapter, section, and paragraph nodes visible so context is not lost.

The partial view uses the same chapter stepper. Only chapters containing failed, targeted, or annotated sentences should contribute visible content in this view.

Do not treat the partial failed draft as a separate manuscript source. It is only a filtered view over the complete object library.

## Tree Rendering

Render the manuscript as a collapsible tree:

```text
Paper title
  Chapter 1
    Section 1.1
      Paragraph P1.1.1
        S1.1.1 sentence text
        [+ Insert comment here]
        S1.1.2 sentence text
```

Use browser-native elements where possible:

- `<details>` and `<summary>` for chapters and sections.
- `<article>` or `<section>` for major nodes.
- `<p>` for paragraphs.
- `<span>` for sentences and selectable text.
- Small inline button or gutter marker for sentence-gap insertion comments.

The UI chrome and controls should be Chinese-English bilingual. Keep saved JSON enum values in English, but display dropdown labels and status messages as Chinese label plus English enum/value.

For bilingual sentence text, preserve the source object text and render visible Chinese and English drafts on separate lines when the object text already contains explicit line breaks or an English/Chinese boundary. This display split must not overwrite `manuscript_objects.json` or change the annotation schema. Span annotations should continue to store character offsets against the normalized source sentence text.

Terminology highlighting is a visual layer only. Match terms, preferred forms, accepted variants, and `chinese_translations` from `shared/terminology_glossary.yaml` against the normalized source sentence text and render shallow green backgrounds for both English and Chinese occurrences without changing sentence text, character offsets, `manuscript_objects.json`, or `user_annotations.json` span schemas.

Formula rendering is also a visual layer. Apply [equation-and-formula-standard.md](../../../shared/equation-and-formula-standard.md): preserve LaTeX as the canonical source, keep short inline math inline, render substantive formulas/display equations as separate centered read-only formula blocks when the object text contains display math, and keep the raw LaTeX visible or copyable. The UI must not transform source text in a way that changes span annotation offsets, selected text, or text hashes. If no math-rendering dependency is bundled, render formulas as styled monospace LaTeX rather than adding a new frontend stack.

Span annotations must be rendered as local text-range highlights using `char_start` and `char_end`, not only as whole-sentence or whole-paragraph markers. When a span annotation is deleted, its text-range highlight must disappear immediately from the visible virtual rows.

Virtual scrolling must preserve annotation behavior. Rendered rows must still expose `data-chapter-id`, `data-section-id`, `data-paragraph-id`, and `data-sentence-id` attributes where applicable. Selecting an existing annotation should switch to the owning chapter and scroll the virtual list to the target row. Do not combine virtual rows with CSS that forces a fixed intrinsic paragraph height, such as a low `contain-intrinsic-size`; row measurement must allow long natural manuscript paragraphs to determine their own visible height.

If the object library contains sentence-aligned paragraph objects, the UI must not pretend these are natural manuscript paragraphs. Display the paragraph role/id from `manuscript_objects.json` and keep any regrouping work upstream in object-library creation from the main manuscript source.

Every rendered node must carry object id data attributes:

```html
<section data-section-id="SEC_2_1">
<p data-paragraph-id="P_2_1_03">
<span data-sentence-id="S2.1.4">...</span>
```

## User Interaction

### Text Span Annotation

The user selects text with the mouse. The UI resolves the selection to:

- `section_id`
- `paragraph_id`
- `sentence_id`
- `char_start`
- `char_end`
- `selected_text`
- `text_hash`

The same sentence may have any number of independent span annotations. Each newly selected word, phrase, or fragment should create a separate annotation object with its own `annotation_id`; do not collapse all issues in a sentence into one record. This lets one sentence carry separate comments such as terminology, grammar, and unsupported-claim issues at different offsets.

If the user selects the whole visible sentence text, store it as a `span_issue` with the normal `char_start`/`char_end` range and `selection_scope: "whole_sentence"`. Clicking a sentence without selecting text remains a `sentence_issue`; use this when the problem belongs to the whole sentence rather than to a highlighted text range.

For advanced cases where one single issue needs to point to several non-contiguous spans within the same sentence, the UI and downstream readers may use optional `target.ranges`. Each range item must contain `char_start`, `char_end`, `selected_text`, and optional `text_hash`. Keep the top-level `target.sentence_id`, `paragraph_id`, `section_id`, and `chapter_id` as the shared owner. Use this only when the multiple fragments are one logical issue; otherwise create multiple independent `span_issue` annotations.

If a selection crosses multiple sentences, split it into sentence-level annotations or ask the user to narrow the selection.

### Sentence Annotation

Clicking a sentence without selecting text should allow annotating the whole sentence.

Each sentence row should show only `pass` or `fail` status and allow the user to click `pass` / `fail` tags or buttons. Default every sentence to `fail` when no user decision exists. The UI must not mutate `manuscript_objects.json`; store user status decisions in `user_annotations.json` under a separate `sentence_status_decisions` object keyed by `sentence_id`.

### Paragraph Annotation

Each paragraph has a paragraph-level comment button. The right panel can attach feedback to the paragraph object.

### Section/Chapter Annotation

Each section and chapter summary row has a comment button. Use this for structural, positioning, or chapter-function feedback.

### Insert-Between-Sentences Annotation

Between every adjacent sentence pair, render an insertion marker:

```text
[+]
```

The marker creates an annotation with:

- `after_sentence_id`
- `before_sentence_id`
- `issue_type: needs_insert_sentence`
- optional comment

This records "insert a sentence here" or "add explanation here" without modifying text.

## Annotation Management Panels

Use a three-column desktop layout: manuscript content, current-annotation editor, and saved-annotations browser. The current-annotation editor edits the currently selected annotation. The saved-annotations browser must be a separate panel to the right of the editor, not a long card list inside the editor.

Required field:

- Problem type dropdown.

Optional fields:

- Free-text comment.
- Severity dropdown.
- Suggested action dropdown.
- Status display.

The text box is optional. The user may select only a problem type and save.

Provide a clear-selection control that deselects the current annotation in the editor without deleting the saved annotation. Deleting a saved annotation is a separate action and must update both the saved annotation list and the visible manuscript highlights.

The saved-annotations browser should use an expandable/collapsible list. The collapsed row shows a short annotation id, problem type, and annotation type. Expanding a row reveals target details, suggested action, status, and comment. Selecting a saved annotation must load it into the current-annotation editor, scroll the manuscript to the target, and mark the selected saved-annotation row with a visible border. On narrow screens, move the saved-annotations panel below the current-annotation editor.

## Problem Type Dropdown

Use a fixed first-version list:

```text
language_style
grammar
ambiguity
terminology
citation_expression
unsupported_claim
unsupported_superiority_claim
duplicate_argument
context_fit
paragraph_logic
section_positioning
needs_insert_sentence
needs_delete
needs_merge
needs_split
operation_record_residue
figure_table_text
other
```

## Suggested Action Dropdown

Use:

```text
direct_revision_candidate
language_review_needed
upgrade_required
evidence_verification_needed
literature_verification_needed
structure_rewrite_needed
final_polish_later
keep_with_note
other
```

The UI may infer a default action from problem type, but the user can override it.

Suggested defaults:

| problem type | default action |
|---|---|
| `language_style` | `direct_revision_candidate` |
| `grammar` | `direct_revision_candidate` |
| `ambiguity` | `direct_revision_candidate` |
| `terminology` | `language_review_needed` |
| `citation_expression` | `evidence_verification_needed` |
| `unsupported_claim` | `upgrade_required` |
| `unsupported_superiority_claim` | `upgrade_required` |
| `paragraph_logic` | `structure_rewrite_needed` |
| `section_positioning` | `structure_rewrite_needed` |
| `needs_insert_sentence` | `direct_revision_candidate` |

## Annotation JSON Schema

Write one file:

```json
{
  "schema_version": "1.0",
  "paper_id": "P001",
  "round": "round_001",
  "source_object_library": "revision_workbench/bilingual_revision/manuscript_objects.json",
  "view_mode": "full_manuscript",
  "created_at": "2026-06-10T00:00:00+08:00",
  "updated_at": "2026-06-10T00:00:00+08:00",
  "annotations": [],
  "sentence_status_decisions": {}
}
```

### Sentence Status Decision

```json
{
  "sentence_status_decisions": {
    "S2.1.4": {
      "status": "fail",
      "updated_at": "2026-06-10T00:00:00+08:00"
    }
  }
}
```

Allowed user status values are:

```text
pass
fail
```

There is no `pending` sentence state. Missing, invalid, or legacy `pending` values must display and save as `fail`. Clicking the active status again keeps that same explicit status; it must not clear the sentence back to a third state.

### Span Issue

```json
{
  "annotation_id": "A001",
  "annotation_type": "span_issue",
  "target": {
    "paper_id": "P001",
    "chapter_id": "CH_2",
    "section_id": "SEC_2_1",
    "paragraph_id": "P_2_1_03",
    "sentence_id": "S2.1.4",
    "char_start": 12,
    "char_end": 28,
    "selection_scope": "text_span",
    "selected_text": "优于现有所有方法",
    "text_hash": "sha256..."
  },
  "issue_type": "unsupported_superiority_claim",
  "severity": "P0",
  "suggested_action": "upgrade_required",
  "comment": "",
  "status": "user_commented"
}
```

### Multi-Range Span Issue

Use this only when several non-contiguous fragments in the same sentence are one logical issue. Otherwise prefer separate `span_issue` objects.

```json
{
  "annotation_id": "A001B",
  "annotation_type": "span_issue",
  "target": {
    "chapter_id": "CH_2",
    "section_id": "SEC_2_1",
    "paragraph_id": "P_2_1_03",
    "sentence_id": "S2.1.4",
    "selection_scope": "multi_span",
    "ranges": [
      {
        "char_start": 12,
        "char_end": 18,
        "selected_text": "显著提高",
        "text_hash": "sha256..."
      },
      {
        "char_start": 42,
        "char_end": 51,
        "selected_text": "明显优于",
        "text_hash": "sha256..."
      }
    ]
  },
  "issue_type": "unsupported_superiority_claim",
  "severity": "P0",
  "suggested_action": "upgrade_required",
  "comment": "两个片段属于同一个过强比较问题。",
  "status": "user_commented"
}
```

### Sentence Issue

```json
{
  "annotation_id": "A002",
  "annotation_type": "sentence_issue",
  "target": {
    "sentence_id": "S2.1.4"
  },
  "issue_type": "ambiguity",
  "severity": "P1",
  "suggested_action": "direct_revision_candidate",
  "comment": "主语不清楚。",
  "status": "user_commented"
}
```

### Paragraph Comment

```json
{
  "annotation_id": "A003",
  "annotation_type": "paragraph_comment",
  "target": {
    "paragraph_id": "P_2_1_03"
  },
  "issue_type": "paragraph_logic",
  "severity": "P1",
  "suggested_action": "structure_rewrite_needed",
  "comment": "这一段应先说明指标，再讨论方法价值。",
  "status": "user_commented"
}
```

### Insert Between Sentences

```json
{
  "annotation_id": "A004",
  "annotation_type": "insert_between_sentences",
  "target": {
    "after_sentence_id": "S2.1.4",
    "before_sentence_id": "S2.1.5"
  },
  "issue_type": "needs_insert_sentence",
  "severity": "P1",
  "suggested_action": "direct_revision_candidate",
  "comment": "这里应插入一句解释 baseline 设置。",
  "status": "user_commented"
}
```

## Text Hash

Use a stable hash for selected text and sentence text:

```text
sha256(normalized_text)
```

Normalization:

- Convert CRLF to LF.
- Trim leading and trailing whitespace for selected spans.
- Preserve internal spaces and punctuation.

During later revision, `revision-control` should compare stored hash with the current object text. If it differs, mark the annotation as:

```text
needs_relocation
```

## Python Local Service

Use standard library modules:

- `argparse`
- `json`
- `hashlib`
- `datetime`
- `pathlib`
- `http.server`
- `socketserver`
- `urllib.parse`

No external dependency.

## HTTP Endpoints

```text
GET  /
GET  /api/manuscript
GET  /api/annotations
POST /api/annotations
POST /api/annotations/delete
POST /api/save
```

### GET /api/manuscript

Returns:

```json
{
  "paper": {},
  "tree": [],
  "round": "round_001",
  "available_views": ["full_manuscript", "failed_or_targeted"]
}
```

### GET /api/annotations

Returns existing `user_annotations.json` if present; otherwise returns an empty annotation document.

### POST /api/annotations

Creates or updates one annotation, then writes the full JSON file.

### POST /api/annotations/delete

Deletes an annotation by `annotation_id`.

### POST /api/save

Writes the current annotation document to the fixed output file.

## Rendering From manuscript_objects.json

Expected object library shape may vary slightly, so the service should normalize it into a UI tree:

```json
{
  "node_type": "section",
  "id": "SEC_2_1",
  "title": "2.1 ...",
  "children": []
}
```

Normalized node types:

```text
paper
chapter
section
paragraph
sentence
figure_table_text
```

Each sentence node should include:

```json
{
  "node_type": "sentence",
  "sentence_id": "S2.1.4",
  "text": "...",
  "status": "fail",
  "revision_count": 0,
  "hash": "sha256..."
}
```

## Visual States

Use CSS classes:

```text
annotation-p0
annotation-p1
annotation-p2
annotation-upgrade-required
annotation-language
annotation-structure
annotation-evidence
annotation-selected
```

Suggested colors:

- P0: red border/background.
- P1: orange.
- P2: yellow.
- language: blue underline.
- structure: purple side marker.
- evidence/upgrade: red side marker.

Keep visual styling simple and readable. The UI should feel like an editor review surface, not a dashboard or landing page.

## revision-control Integration

At the beginning of a revision round, `revision-control` should check:

```text
revision_workbench/bilingual_revision/rounds/<round_id>/user_annotations.json
```

If present:

1. Validate `schema_version`, `paper_id`, `round`, and `source_object_library`.
2. Validate target ids against `manuscript_objects.json`.
3. Validate text hashes when span annotations are present.
4. Convert annotations into a revision task queue.
5. Apply gates:
   - `unsupported_claim` and `unsupported_superiority_claim` trigger `upgrade_required`.
   - `paragraph_logic` and `section_positioning` may trigger structure rewrite planning.
   - `needs_insert_sentence` becomes an insertion task, but still needs user confirmation.
   - `language_style`, `grammar`, and `ambiguity` may become direct revision candidates if context is sufficient.
6. Ask for user confirmation before official modification.

If absent:

```text
No user_annotations.json found. Continue from user-provided conversational instructions.
```

## Safety Rules

- The UI must not overwrite `manuscript_objects.json`.
- The UI must not write `latest_full_bilingual_review.md`.
- The UI must not write `modification_log.md`.
- The UI must not finalize pass/fail status in `manuscript_objects.json` or official round logs. It may autosave user pass/fail decisions to `user_annotations.json`.
- The UI must treat all sentences without an explicit user `pass` decision as `fail`, including the failed/targeted filtered view.
- The UI must not add project standards directly.
- The UI only writes `user_annotations.json`.

## Failure Handling

| condition | behavior |
|---|---|
| `manuscript_objects.json` missing | show setup error and command hint to run `revision-control` object-library creation |
| invalid JSON | show parse error and do not start annotation |
| round directory missing | ask whether to create, or require `--create-round` |
| annotation target id not found | mark annotation `needs_relocation` |
| text hash mismatch | mark annotation `needs_relocation` |
| save fails | show local path and error message; keep browser copy in memory |

## Implementation Steps

1. Add `skills/revision-control/scripts/revision_annotation_ui.py`.
2. Implement CLI args:
   - `--workbench`
   - `--round`
   - `--host`, default `127.0.0.1`
   - `--port`, default `8765`
   - `--create-round`
3. Implement object-library loader and normalizer.
4. Implement annotation file loader/writer.
5. Implement embedded HTML/CSS/JS.
6. Implement chapter-scoped tree rendering with a chapter stepper; do not render the full manuscript DOM at once.
7. Implement virtual scrolling for active-chapter section and paragraph rows, including dynamic row height correction.
8. Implement bilingual visible labels and bilingual sentence line display without changing source objects or schema values.
9. Implement selection capture and sentence-id resolution against normalized source sentence text.
10. Implement right-panel annotation editor.
11. Implement autosave and manual save.
12. Add `revision-control` reference note telling agents to read this plan before implementing or running the UI.

## Acceptance Criteria

- Runs with Python 3 and no third-party dependencies.
- Renders a tree from `manuscript_objects.json`.
- Shows Chinese-English UI labels while preserving English schema enum values.
- Shows Chinese and English drafts on separate visible lines when sentence text is bilingual.
- Highlights project terminology with shallow green backgrounds for English terms, accepted variants, preferred forms, and Chinese translations from `terminology_glossary.yaml`.
- Shows terminology field/domain and source provenance in the terminology-management page.
- Shows formulas and equation-like LaTeX in readable read-only blocks or inline spans while preserving raw source text and annotation offsets.
- Provides a chapter stepper and virtualizes the selected chapter so only visible rows plus overscan are mounted in the DOM.
- Shows sentence pass/fail status only, defaults missing decisions to fail, and autosaves user pass/fail decisions to `user_annotations.json`.
- Supports full manuscript view and failed/targeted filtered view.
- Supports span, sentence, paragraph, section/chapter, and sentence-gap annotations.
- Requires problem type; comment is optional.
- Autosaves `user_annotations.json` to the fixed round path.
- Does not modify manuscript text or revision state files.
- `revision-control` can detect the annotation file and route tasks through existing gates.
