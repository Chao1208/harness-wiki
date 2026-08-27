# Change 001：Harness 记忆与持续学习 · 首轮全面调研

## 为什么（Why）

wiki 刚建立，知识库为空。在开展任何研究与工程之前，必须先全面掌握该领域截至 2026-08 的最新进展（论文、GitHub 项目、工业界博客），否则后续方向选择与论文选题缺乏依据。

## 做什么（What）

一次广度优先的全景调研，覆盖四个分支（详见 `search_tree.yaml`）：

- **A. Agent 记忆**：记忆架构与系统、记忆基准、开源实现、工业实践
- **B. Agent 自进化**：自我改进方法、自动化 agent 设计、prompt/工作流优化
- **C. Agent 持续学习**：经验积累与技能库、在线/测试时学习、灾难性遗忘、评测
- **D. Harness 最新动态**：主流 coding/general agent harness 的记忆与学习机制、工程博客

## 交付物（Deliverables）

1. 4 份分支调研底稿（markdown）→ `Project/survey/`
2. 关键论文 PDF 归档 → `raw/papers/` + `index.yaml` 登记（远端只存链接）
3. 综合调研报告（html，中文）→ `Project/survey_reports/`
4. wiki 首批条目（总览页 + 三大主题页）→ `wiki/`
5. 工作日志（html）→ `Project/notebooks/`

## 非目标（Non-goals）

- 不做深度复现或代码实验（后续 change）
- 不确定论文选题（依据本调研在后续 change 中决策）
- 不追求文献全覆盖，聚焦 2023–2026 高影响力与最新工作

## 执行方式

主 session 只做派发与验收；4 个 survey subagent 按分支并行执行（BFS 第一层），
汇总报告由独立 report subagent 撰写。

---
撰写者：main-agent · 2026-08-27 11:12
