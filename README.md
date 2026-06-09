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
| `post-manuscript-benchmark-review` | 完整初稿后的 benchmark review、质量评估、claim triage 和下一版 P0/P1/P2 计划。 |
| `language-style-review` | 对论文语言、用词、语法、AI 味、译文、图表文字和引用句式做审查，但不写入稿件状态。 |
| `revision-control` | 管理逐句 revision、对象库、轮次状态、通过/未通过确认、最新逐句稿、项目标准和升级计划。 |
| `academic-de-ai-polishing` | 在内容稳定后降低机械感和 AI 痕迹，同时保护 claim strength、引用和术语。 |
| `academic-formatting-workflow` | 学校/期刊模板、DOCX 排版、Markdown-to-DOCX、公式、上下标、交叉引用和参考文献格式。 |

## 共享协议层

跨 skill 的字段和边界放在 [shared](shared/)：

- `workflow-protocol-index.md`：跨 skill 协议索引。
- `trigger-conflict-matrix.md`：触发冲突与路由优先级。
- `handoff-field-schema.md`：`material_passport`、`claim_anchor`、`LIT_GAP`、benchmark report 等共享字段。
- `revision-control-contract.md`：逐句 revision 总控、对象库、轮次状态和升级流程边界。
- `language-style-review-schema.md`：语言风格审查报告和候选改写输出结构。
- `project-review-standards-schema.md`：项目补充审查标准、术语表和问题词表结构。
- `manuscript-object-model.md`：论文、章节、段落、句子和图表文字对象模型。
- `revision-upgrade-plan-schema.md`：补文献、结构重组或大规模改写前的升级计划结构。
- `validation-policy.md`：error/warning 与 strict 验证策略。

原则：总控 skill 负责跨阶段路由；`revision-control` 和 `language-style-review` 可直接读取各自需要的共享 schema，其它 skill 的 `SKILL.md` 尽量保持自包含，通过本地 references 与共享字段对齐。

## 安装

Windows:

```powershell
.\install.ps1
```

安装脚本只替换本仓库管理的同名 skill，并同步 `shared/` 到：

```text
C:\Users\<you>\.codex\skills
C:\Users\<you>\.codex\shared
```

不会删除 `.system` 或其它非本仓库 skill。

## 在 Claude Code 中使用(双端共存)

这套 skill 以 Codex 为主,同时兼容 Claude Code。两端共用同一份源:`SKILL.md` 的 frontmatter 只含 `name`/`description`,与 Claude Code 的 Agent Skills 格式一致,无需改动正文。

安装到 Claude Code 的 home(`~/.claude`):

Windows:

```powershell
.\install-claude.ps1
```

macOS / Linux:

```bash
bash install-claude.sh
```

安装脚本镜像 `install.ps1` 的逻辑,只把目标换成:

```text
~/.claude/skills
~/.claude/shared
```

`shared/` 同样装在 `skills/` 的上一级,保证各 `SKILL.md` 中 `../../shared/` 相对链接在 Claude Code 端正确解析。

触发方式:在 Claude Code 中直接描述任务(skill 的 `description` 会自动匹配),或用 `/skill-name` 调用。正文里的 `$skill`(如 `$academic-research-verification`)是 Codex 的路由语法;在 Claude Code 中它表示"切换到对应同名 skill",Claude 会按语义理解。

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
7. `language-style-review`
8. `revision-control`
9. `academic-de-ai-polishing`
10. `academic-formatting-workflow`

顺序可以根据项目状态调整，但正式写作前应优先完成证据核验；完整初稿后的语言审查只输出报告，正式逐句修改和通过/未通过状态由 `revision-control` 管理；最终润色和格式化应在内容、结构、证据和 claim strength 稳定后进行。

## 质量原则

- 不伪造文献、DOI、实验结果、图表内容或格式规则。
- 对无法判断的边界性选择先询问用户。
- 若用户不设定研究领域，默认领域为计算机与电子信息，并标记该假设。
- 写作 claim 通过 `claim_anchor` 与证据、代码、结果或用户决策连接。
- 图表 panel、caption、正文 claim 和 evidence register 应保持可追溯。
- 逐句 revision 修改、通过/未通过状态、项目补充标准和升级计划必须保留用户确认记录。
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
