# Change 002 · 高论文潜力方向深挖与选题收敛

## 背景

change-001 完成首轮全景调研(版本 0.2),在 search tree 中登记 24 个下层候选问题,其中 5 个标记 `paper_potential: high`:

| ID | 问题 | 来源分支 |
|---|---|---|
| A-5 | 评测方法学:为 harness 记忆设计新基准 | A(记忆) |
| B-1 | harness 可编辑面的最小充分集:逐组件消融 | B(自进化) |
| B-3 | 弱评估器下的自进化:无快速 verifier 任务的进化信号构造(几乎空白) | B(自进化) |
| C-6 | 面向 coding harness 的 lifelong 基准设计 | C(持续学习) |
| D-1 | harness-level forgetting 量化与 retention 回归集构建 | D(harness 动态) |

## 目标

1. 对 5 个方向逐一深挖:相关工作全覆盖(截至 2026-08)、空白点核实、可行性评估(数据/评测/算力/新颖性);
2. 收敛出 **1-2 个可立项的论文选题**,给出研究问题、方法草案、实验设计雏形、目标会议;
3. 产出沉淀:调研报告(html)、wiki 条目更新、论文归档与索引登记。

## 非目标

- 不在本 change 内动手做实验或写论文初稿(留给 change-003);
- 其余 19 个候选问题不展开(留在 search tree 待下轮)。

## 判定标准

- 每个方向有独立深挖底稿(Project/survey/deep_*.md),含"空白点是否成立"的明确结论;
- 新下载论文全部归档 raw/papers/ 并登记 index.yaml;
- 选题收敛报告落 Project/survey_reports/,含 1-2 个选题的完整立项论证。

撰写者:main-agent · 2026-08-28 16:58
