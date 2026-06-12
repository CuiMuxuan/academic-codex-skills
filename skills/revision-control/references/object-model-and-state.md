# Object Model And State

Use the shared schema in [manuscript-object-model.md](../../../shared/manuscript-object-model.md) as the canonical object model.

## Object Types

- `Paper`
- `Chapter`
- `Section`
- `Paragraph`
- `Sentence`
- `FigureTableTextObject`

正文中的图表引用句进入 `Sentence` 对象。图题、图注、表题、表注、图中文字另建 `FigureTableTextObject`。

## Object Library Source Rules

Build the object library from the canonical active manuscript draft, not from a sentence-aligned bilingual review draft.

- `Chapter` and `Section` objects follow the active manuscript's heading structure.
- `Paragraph` objects follow the active manuscript's natural paragraphs or true structural blocks, such as list items, table rows, figure/table text references, or DOCX paragraphs.
- `Sentence` objects are segmented inside their parent paragraph. Multiple sentence objects may share one `paragraph_id` when the manuscript paragraph contains multiple sentences.
- A sentence-aligned bilingual review draft may supply `alignment_source_id`, English/Chinese paired sentence text, review notes, or latest review text, but it must not be the source of paragraph boundaries unless the original manuscript itself is already a sentence-aligned list.
- If only a sentence-aligned review draft is available, mark `paragraph_source_mode: sentence_aligned_review_only`, use `source_block_type: sentence_aligned_item_group`, and treat paragraph-level/section-flow review as context-limited until the object library is rebuilt from the main manuscript.

Before accepting a generated object library, run a source sanity check:

- compare the declared source file against the active main manuscript path;
- compare the number of paragraph objects with the main manuscript's natural paragraphs/blocks;
- flag the library for rebuild when most paragraph objects contain exactly one sentence and `paragraph_role` or `source_block_type` indicates sentence-aligned item groups.

## Sentence State

Each sentence object tracks:

- stable id and current-round id;
- original text and latest text;
- pass/fail suggestion and user-confirmed status;
- `revision_count`;
- grammar, sentence value, context fit, duplicate argument, terminology, citation expression, and figure/table reference checks;
- source and derived sentence ids;
- split, merge, delete, absorb, or rewrite operation;
- previous-round and next-round ids.

## Split, Merge, Delete

- If `S0020` splits into `S0020a` and `S0020b`, record both derived ids.
- If several old sentences merge into one new sentence, record every source id.
- If a source sentence is deleted or absorbed, keep a `deleted` or `merged` marker in history.
- At each new round, renumber current ids and preserve mapping in `id_mapping_history.yaml`.

## User Confirmation

The agent may suggest `pass`, `fail`, `needs_user_decision`, or `upgrade_required`. Only the user can finalize pass/fail status.
