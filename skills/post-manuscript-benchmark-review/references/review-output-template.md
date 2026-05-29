# Review Output Template

Use this template when producing a full Chinese post-draft benchmark review. Keep the report evidence-based and replace every bracketed placeholder with manuscript-specific information or mark it as `待补充`.

## 完整中文评审报告骨架

```text
# 初版论文后评审报告

## 1. 评审结论

目标档位：
当前判定：ready_with_minor_revision | major_revision_required | not_ready_for_target | cannot_judge_from_materials
总体评分：X/5 或 X/100
核心结论：
- 当前稿件最接近目标档位的方面：
- 当前稿件距离目标档位的主要阻塞：
- 下一版最优先解决的问题：

## 2. 评审材料与判断边界

已使用材料：
- 稿件版本：
- 目标期刊/学校/质量档位：
- 对标文献：
- 数据、结果表、图件、代码或证据表：

缺失材料：
- 缺失项：
- 对判断的影响：
- 可否继续评审：

判断边界：
- 本报告能可靠判断的内容：
- 只能做初步判断的内容：
- 不能判断或不得下结论的内容：

## 3. 按评审标准逐项评价

| 评审维度 | 分数 | 主要依据 | 关键问题 | 是否阻塞目标档位 |
|---|---:|---|---|---|
| 选题与文献综述 | X/5 | 具体章节/引用/benchmark | 问题链、研究空白、文献密度 | 是/否 |
| 基础知识与研究能力 | X/5 | 方法、数据、验证、代码、结果 | 数据来源、泄漏、基线、复现性 | 是/否 |
| 创新性与论文价值 | X/5 | 贡献、差异化、应用价值 | 创新类型是否成立 | 是/否 |
| 论文规范与写作质量 | X/5 | 结构、图表、语言、引用、限制 | 叙事、图表经济性、claim纪律 | 是/否 |

维度解释：
- 选题与文献综述：
- 基础知识与研究能力：
- 创新性与论文价值：
- 论文规范与写作质量：

## 4. 对标文献选择依据

| 编号 | 对标文献 | 选择理由 | 对标角色 | 可比性 | 访问级别 | 已使用事实 | 推断边界 |
|---|---|---|---|---|---|---|---|
| B1 | 作者-年份-题名-期刊-DOI | 任务/方法/验证/目标期刊相似 | 直接竞争/方法标杆/验证标杆/写作标杆 | 高/中/低 | full_text/abstract_only/metadata_only/user_supplied_summary | 已核验事实 | 不能判断的内容 |

选择逻辑：
- 为什么这些文献足以构成 benchmark set：
- 哪些关键 benchmark 仍缺失：

## 5. Benchmark Gap 表

| Benchmark | Benchmark 压力 | 当前稿件已达到 | 当前稿件差距 | 所需证据/修改 | 严重度 | 目标档位影响 |
|---|---|---|---|---|---|---|
| B1 | 该文献为何会成为审稿人参照 | 稿件已有结果/章节/图表 | 缺少的实验、论证、图表、验证或引用 | 具体新增数据、分析、文本或图表 | blocking/major/moderate/minor | 阻塞/削弱/可后置 |

逐篇说明：
- B1：
  - 对标压力：
  - 稿件优势：
  - 稿件差距：
  - 需要补充：
  - 是否阻塞：

## 6. 当前论文缺点和不足

### 6.1 P0 阻塞问题

| 问题 | 位置 | 为什么严重 | 需要怎么改 | 验收标准 |
|---|---|---|---|---|
| 问题1 | 章节/图/表/claim | 阻塞目标档位的原因 | 具体行动 | 完成后如何判断可通过 |

### 6.2 P1 重要改进

| 问题 | 位置 | 改进价值 | 建议动作 | 预期收益 |
|---|---|---|---|---|

### 6.3 P2 包装与表达

| 问题 | 位置 | 建议动作 |
|---|---|---|

## 7. Claim Triage

| claim anchor | 中心 claim | 当前证据 | benchmark 压力 | 建议状态 | 修改方式 | 对应位置 |
|---|---|---|---|---|---|---|
| C1/无 | claim 原文或摘要 | 图/表/数据/文献 | B1/B2 或无 | promote/soften/move_to_supplement/hold_for_more_evidence/remove | 保留、收窄、移至补充、暂缓或删除 | 摘要/引言/讨论 |

安全可声称：
- 

需要补证后才能声称：
- 

不得声称：
- 

## 8. 下一版优化方案与改进措施

| 优先级 | 目标 | 具体产物 | 所需材料 | 方法/实验/写作动作 | 验收标准 | 放置位置 |
|---|---|---|---|---|---|---|
| P0 | 关闭目标档位阻塞 | 新表/新图/新验证/改写章节 | 数据/文献/代码 | 具体步骤 | 达到什么证据强度 | 主文/补充 |

建议迭代顺序：
1. 先处理：
2. 再处理：
3. 最后处理：

## 9. 需要使用者提供或确认的资料清单

| 资料 | 用途 | 缺失影响 | 优先级 |
|---|---|---|---|
| 目标期刊或学校要求 | 判断档位 | 无法确定最终标准 | P0/P1/P2 |

## 10. 是否达到目标档位的判定

最终判定：
理由：
- 支持判定的证据：
- 阻碍判定的证据：
- 如果按当前版本投稿/提交，最大风险：
- 达到目标档位前必须完成的最小改动集合：
```

## Benchmark Gap 表字段说明

| 字段 | 写法要求 |
|---|---|
| `Benchmark` | 使用 B1/B2 编号，并在前文给出完整题名、年份、期刊和 DOI/链接。 |
| `Benchmark 压力` | 写清它为什么会成为审稿人的参照：任务相似、方法相似、验证更强、目标期刊示范、或领域机制关键。 |
| `当前稿件已达到` | 只写稿件中能定位的证据，如章节、图表、数据、方法、引用或代码。 |
| `当前稿件差距` | 写具体缺口，不写泛泛的“创新不足”“论证不充分”。 |
| `所需证据/修改` | 写下一版能执行的材料或动作：新增 baseline、外部验证、消融、机制解释、图表重构、讨论收窄等。 |
| `严重度` | 使用 `blocking`、`major`、`moderate`、`minor`。主 claim、基线公平性、验证独立性、证据复现性问题不能标为 minor。 |
| `目标档位影响` | 说明该 gap 是阻塞目标、显著削弱、还是可以放在补充材料或后续工作。 |

## Report Discipline

- Use manuscript locations whenever possible: section title, paragraph, table, figure, claim, result, code path, or evidence-register key.
- Separate benchmark facts from inference. If only metadata or abstract is available, mark the comparison as limited.
- Do not turn the report into generic journal advice. Every P0/P1 action must be tied to a benchmark pressure or manuscript defect.
- Keep the final judgment direct. A polite report can still say `not_ready_for_target` when evidence does not support the target.
