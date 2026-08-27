# Harness 的记忆与持续学习 · Wiki 总览

> **一句话定义**：本 wiki 汇集"agent harness（Claude Code / Codex 类执行框架）如何拥有记忆、如何从经验中持续学习"这一领域截至 2026-08 的最先进研究与工程实践，目标是指导现实设计并孕育顶会论文。

## 主题定义

**Harness** 是包裹基座模型、编排"思考/规划、工具调用、上下文管理、artifact 存储、结果评估"的执行系统（Lilian Weng 2026 定义）。2025–2026 年的关键事实是：前沿模型在 SWE-bench Verified 上已收敛到 1pp 以内，而 harness 差异可摆动 20pp 以上——**竞争主战场从模型转向 harness**，harness 状态（prompt、记忆、技能、工具、工作流）成为继模型权重之后的第二学习载体。

本 wiki 围绕四个互相咬合的概念展开：

- **记忆**：harness 把什么信息以什么形态存下来（[agent记忆](agent记忆.md)）
- **自进化**：harness 的各组件如何被自动优化（[agent自进化](agent自进化.md)）
- **持续学习**：经验如何被抽象、复用而不遗忘（[agent持续学习](agent持续学习.md)）
- **harness 本体**：主流 harness 的机制现状与设计空位（[harness](harness.md)）

## 知识地图

```
                    ┌─────────────────────────────┐
                    │       harness（载体）        │
                    │  指令文件 · skills · hooks   │
                    └──────┬───────────────┬──────┘
                           │               │
              ┌────────────▼───┐   ┌───────▼──────────┐
              │  agent记忆      │   │  agent自进化      │
              │  存什么、怎么存  │   │  谁来改、怎么改   │
              └────────────┬───┘   └───────┬──────────┘
                           │               │
                    ┌──────▼───────────────▼──────┐
                    │      agent持续学习           │
                    │  经验抽象 · 遗忘 · 学习闭环   │
                    └─────────────────────────────┘
```

| 页面 | 一句话结论 |
|---|---|
| [agent记忆](agent记忆.md) | coding harness 的记忆已收敛到明文文件 + 分层加载 + 离线固结，压倒向量库；评测重心从对话回忆转向 agent 经验 |
| [agent自进化](agent自进化.md) | 重心从"设计 agent"移到"进化 harness"；富文本反馈优于标量奖励；进化通路即攻击面 |
| [agent持续学习](agent持续学习.md) | 经验抽象取代轨迹存储；非参数路线是绝对主流，但"遗忘"只是换了形态（context collapse、检索退化） |
| [harness](harness.md) | harness 是第二学习载体；"三件套"（分层指令文件 + skills + auto memory）成为行业标准形态；harness-level forgetting 无人防护 |

## 素材来源

- 四份分支调研底稿：`Project/survey/branch_A_agent记忆.md`、`branch_B_agent自进化.md`、`branch_C_agent持续学习.md`、`branch_D_harness动态.md`
- 综合调研报告：`Project/survey_reports/2026-08-27_change001_首轮全面调研报告.html`
- 论文 PDF（67 篇）：`raw/papers/`（索引 `raw/papers/index.yaml`）
- BFS search tree（含 24 个下层候选问题）：`openspec/changes/001-survey-harness-memory-continual-learning/search_tree.yaml`

## 当前版本与更新记录

| 版本 | 日期 | 变更 | 负责 agent |
|---|---|---|---|
| 0.1 | 2026-08-27 | change-001 首轮全面调研落地：建立总览页 + 四大主题页，覆盖 2023-01 至 2026-08 文献 67 篇 | report-agent |

---
落款：report-agent · 2026-08-27 12:15
