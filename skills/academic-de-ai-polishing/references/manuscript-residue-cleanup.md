# Manuscript Residue Cleanup

Use this reference when academic prose still contains internal project notes, operation logs, task handoffs, prompt traces, file-management language, TODO markers, or draft-management residue in the manuscript body.

## Triage

Classify each suspicious phrase before rewriting:

| residue type | typical signal | action |
|---|---|---|
| project progress | "本阶段完成", "当前状态", "下一步将" | remove or move to a progress note |
| file operation | "生成了 `xxx.md`", "保存到目录", "运行脚本后" | keep only the research method or result |
| workflow handoff | "交接给下一阶段", "交给 formatting skill", "gate" | remove from body text |
| prompt or AI trace | "根据提示词", "模型输出", "本助手", "AI 生成" | remove unless disclosure is required |
| unresolved author note | TODO, issue id, private project code, "待确认" | move to `User-review items` |
| legitimate method detail | software version, parameter, dataset split, model training step | rewrite as formal methods prose |

## Rewrite Rules

- Delete residue that only describes the writing process, project management, or file movement.
- Recast legitimate research operations as methods: tool, version, data, parameter, procedure, and output.
- Preserve uncertainty when the residue marks an unresolved decision; do not polish it into a settled claim.
- Remove local paths, private project codes, temporary file names, prompt IDs, and internal checklist labels from the body.
- Keep required disclosure notes outside the main argument unless the target format explicitly asks for them in the manuscript body.

## Common Conversions

| source trace | manuscript-safe handling |
|---|---|
| `运行脚本后得到结果` | Describe the computational procedure, software environment, parameters, and result. |
| `本阶段完成文献筛选` | Describe inclusion criteria, screening process, retained studies, and exclusion reasons. |
| `交给下一阶段进行分析` | Delete, or recast as a scientifically relevant workflow only when the workflow itself is studied. |
| `根据任务计划，本节将...` | Replace with the section's scholarly purpose or delete the meta-commentary. |
| `已生成图 3 文件` | Refer to the figure's scientific content, not file generation. |

## Output Handling

When residue is found, report it separately from style polishing:

```text
Residue found:
Body-text action:
Moved to user-review note:
Research-method content preserved:
Unresolved author decision:
```

Do not hide project residue by making it sound academic. Either remove it, convert it into a defensible method statement, or keep it visible as an author decision outside the manuscript body.
