# Academic Codex Skills

一套面向论文、学位论文、综述、投稿稿件和技术报告的 Codex academic workflow skills。目标是让 AI 协助写作时仍然保留证据纪律、引用可追溯、图表可验证、格式可检查、阶段可确认。

## 包含的 Skill

| Skill | 主要用途 |
|---|---|
| `academic-paper-orchestrator` | 论文全流程总控，路由到检索、解析、写作、图表、润色、后评审和格式化 skill。 |
| `academic-research-verification` | 文献检索、DOI/title 核验、引用真实性检查、证据表和 `LIT_GAP` 处理。 |
| `pdf-docx-parsing-workflow` | 解析 PDF/DOCX、批注、修订痕迹、样式、参考文献和结构化证据。 |
| `paper-writing-workflow` | 从已验证证据出发，规划、撰写、修订和整合论文章节。 |
| `academic-figure-workflow` | 论文图表、SVG、draw.io、Matplotlib 多面板图、caption 和投稿级图件 QA。 |
| `academic-de-ai-polishing` | 在内容稳定后降低机械感和 AI 痕迹，同时保护 claim strength、引用和术语。 |
| `academic-formatting-workflow` | 学校/期刊模板、DOCX 排版、Markdown-to-DOCX、公式、上下标、交叉引用和参考文献格式。 |
| `post-manuscript-benchmark-review` | 完整初稿后的 benchmark review、质量评估、claim triage 和下一版 P0/P1/P2 计划。 |

## 共享协议层

跨 skill 的字段和边界放在 [shared](shared/)：

- `workflow-protocol-index.md`：跨 skill 协议索引。
- `trigger-conflict-matrix.md`：触发冲突与路由优先级。
- `handoff-field-schema.md`：`material_passport`、`claim_anchor`、`LIT_GAP`、benchmark report 等共享字段。
- `validation-policy.md`：error/warning 与 strict 验证策略。

原则：总控 skill 直接读取 `shared/`；其它 skill 的 `SKILL.md` 尽量保持自包含，通过本地 references 与共享字段对齐。

## 安装

Windows:

```powershell
.\install.ps1
```

安装脚本只替换本仓库管理的 8 个同名 skill，并同步 `shared/` 到：

```text
C:\Users\<you>\.codex\skills
C:\Users\<you>\.codex\shared
```

不会删除 `.system` 或其它非本仓库 skill。

## 验证

本地严格验证：

```powershell
python scripts/validate_skills.py --strict
```

全局安装后验证：

```powershell
python scripts/validate_skills.py --root C:\Users\<you>\.codex --strict
```

仓库级 QA 脚本：

```powershell
python scripts/audit_claim_anchors.py --help
python scripts/validate_markdown_docx_package.py --help
python scripts/figure_package_check.py --help
```

这些 `scripts/` 是仓库维护工具，不复制到全局 `.codex`。

## 依赖与软件

不同阶段可能用到：

- 文献核验：网络、Crossref/OpenAlex/Semantic Scholar/PubMed。
- PDF/DOCX：PyMuPDF、pdfplumber、pypdf、python-docx、Microsoft Word COM。
- Markdown-to-DOCX：Pandoc、CSL、BibTeX/BibLaTeX、Word 字段刷新。
- 图表：Matplotlib、draw.io/diagrams.net、Inkscape、Graphviz、CairoSVG、Pillow。
- 数据/结果核验：项目代码、Python 科学计算栈、CSV/Parquet reader。

原则：skill 会明确指出可能需要的依赖，并引导用户确认安装或选择替代方案；不会静默安装或静默接受有损转换。

## 推荐流程

完整项目从总控开始：

```text
Use $academic-paper-orchestrator to plan an end-to-end workflow for my paper/thesis.
```

常见顺序：

1. `academic-paper-orchestrator`
2. `academic-research-verification`
3. `pdf-docx-parsing-workflow`
4. `paper-writing-workflow`
5. `academic-figure-workflow`
6. `post-manuscript-benchmark-review`
7. `academic-de-ai-polishing`
8. `academic-formatting-workflow`

顺序可以根据项目状态调整，但正式写作前应优先完成证据核验；最终润色和格式化应在内容、结构、证据和 claim strength 稳定后进行。

## 质量原则

- 不伪造文献、DOI、实验结果、图表内容或格式规则。
- 对无法判断的边界性选择先询问用户。
- 若用户不设定研究领域，默认领域为计算机与电子信息，并标记该假设。
- 写作 claim 通过 `claim_anchor` 与证据、代码、结果或用户决策连接。
- 图表 panel、caption、正文 claim 和 evidence register 应保持可追溯。
- Markdown-to-DOCX 时保护 LaTeX 公式、上下标、交叉引用和参考文献。

## 目录

```text
academic-codex-skills/
  install.ps1
  scripts/
  shared/
  skills/
  examples/
```

## License

MIT License. See [LICENSE](LICENSE).
