# Skills Pack

这里是可安装到 Codex 的 8 个 academic workflow skills。跨 skill 的共享字段和触发冲突规则在仓库根目录 `shared/` 中维护。

## 推荐触发顺序

1. `academic-paper-orchestrator`
2. `academic-research-verification`
3. `pdf-docx-parsing-workflow`
4. `paper-writing-workflow`
5. `academic-figure-workflow`
6. `post-manuscript-benchmark-review`
7. `academic-de-ai-polishing`
8. `academic-formatting-workflow`

## 边界

- 完整项目、阶段判断、触发冲突：用 `academic-paper-orchestrator`。
- 写作前的文献真实性和证据表：用 `academic-research-verification`。
- 完整初稿后的质量判断：用 `post-manuscript-benchmark-review`。
- 内容稳定后的语言去机械感：用 `academic-de-ai-polishing`。
- 最终 DOCX/模板/公式/交叉引用：用 `academic-formatting-workflow`。

安装后建议运行：

```powershell
python scripts/validate_skills.py --root C:\Users\<you>\.codex --strict
```
