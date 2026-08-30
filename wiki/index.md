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

**主题页**

| 页面 | 一句话结论 |
|---|---|
| [agent记忆](agent记忆.md) | coding harness 的记忆已收敛到明文文件 + 分层加载 + 离线固结，压倒向量库；评测重心从对话回忆转向 agent 经验 |
| [agent自进化](agent自进化.md) | 重心从"设计 agent"移到"进化 harness"；富文本反馈优于标量奖励；进化通路即攻击面 |
| [agent持续学习](agent持续学习.md) | 经验抽象取代轨迹存储；非参数路线是绝对主流，但"遗忘"只是换了形态（context collapse、检索退化） |
| [harness](harness.md) | harness 是第二学习载体；"三件套"（分层指令文件 + skills + auto memory）成为行业标准形态；harness-level forgetting 无人防护 |

**概念页**（change-002 五方向深挖沉淀，2026-08-30）

| 页面 | 一句话结论 |
|---|---|
| [记忆与持续学习基准](记忆与持续学习基准.md) | "无 coding harness 记忆/lifelong 基准"的宽表述已被 18 个月内 14+ 新基准填掉；真空白是"真实仓库跨会话演化 × harness 原生记忆为受控变量 × lifelong 三度量 × live 去污染"的合取，建议 A5+C6（+D1）合并立项 |
| [harness遗忘与回归](harness遗忘与回归.md) | harness-level forgetting 现象层空白已关闭（HCL 命名 + 各组件层独立撞见）；真空白是公开 retention 回归基准与回归集构建方法学（类比 RippleEdits 之于 MEMIT） |
| [进化信号构造](进化信号构造.md) | 弱评估器下的进化信号已形成五条路线且权重层已红海；真空白是 harness 层×真不可验证域、信号可靠性感知治理、延迟结果信号闭环三个交集 |
| [可编辑面](可编辑面.md) | 六类可编辑面的粒度谱系（单面→有界多面→组件全集→全代码库）已清晰，但消融证据碎片化且只测收益不测风险；真空白是跨面双轴预算受控的前瞻性消融与"最小充分集" |

## 素材来源

- 四份分支调研底稿（change-001）：`Project/survey/branch_A_agent记忆.md`、`branch_B_agent自进化.md`、`branch_C_agent持续学习.md`、`branch_D_harness动态.md`
- 五份方向深挖底稿（change-002）：`Project/survey/deep_A5_记忆基准.md`、`deep_B1_可编辑面消融.md`、`deep_B3_弱评估器自进化.md`、`deep_C6_lifelong_coding基准.md`、`deep_D1_harness遗忘量化.md`
- 综合调研报告：`Project/survey_reports/2026-08-27_change001_首轮全面调研报告.html`
- 论文 PDF：`raw/papers/`（change-001 索引 `raw/papers/index.yaml`；change-002 新增索引 `index_002_A5/B1/B3/C6/D1.yaml`）
- BFS search tree：change-001 `openspec/changes/001-survey-harness-memory-continual-learning/search_tree.yaml`（24 个下层候选问题）；change-002 `openspec/changes/002-paper-topic-deep-dive/search_tree.yaml`（5 方向深挖结论）

## 当前版本与更新记录

| 版本 | 日期 | 变更 | 负责 agent |
|---|---|---|---|
| 0.1 | 2026-08-27 | change-001 首轮全面调研落地：建立总览页 + 四大主题页，覆盖 2023-01 至 2026-08 文献 67 篇 | report-agent |
| 0.2 | 2026-08-30 | change-002 五方向深挖沉淀：新建 4 个概念页（基准/遗忘回归/进化信号/可编辑面），四大主题页开放问题更新为收窄后判定，五个空白点均由"空白"修正为"部分成立/收窄后成立" | survey-agent |

---
落款：report-agent · 2026-08-27 12:15
更新：survey-agent · 2026-08-30 10:15（v0.2：新增概念页目录、素材来源补 change-002 底稿与索引）
