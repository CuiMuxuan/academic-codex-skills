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
