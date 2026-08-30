# Harness 遗忘与回归（Harness-level Forgetting & Retention Regression）

> **一句话结论**："harness 更新破坏既有行为"的**现象层空白已关闭**——HCL（2026-08）正式命名并测量 harness-level forgetting，且 2026 年各组件层已独立撞见同一现象（ACE 的 context collapse、Misevolution 的安全对齐衰减 99.4%→54.4%、SkillFlow 的缺陷技能固化、Adaptive Auto-Harness 的"密集更新 peak-and-decline"）；**真空白**是 (a) 没有任何公开的、以"harness 更新（diff）"为被测变更单元的 retention 回归基准，(b) 回归集构建方法学（用例来源、统计效力、自动判定）彻底空白——论文定位应从"发现现象"转为"评测方法学与公开回归集"（类比 model editing 领域 RippleEdits 之于 MEMIT 的位置）。

← 返回 [wiki 总览](index.md) · 相关页：[harness](harness.md)（现象定义出处）、[agent持续学习](agent持续学习.md)（非参数遗忘新形态）、[可编辑面](可编辑面.md)（风险轴的测量对象）、[记忆与持续学习基准](记忆与持续学习基准.md)（可合并的第三个测量截面）

## 核心概念

- **harness-level forgetting**（HCL 正式命名）：更新任一 harness 组件（prompt/记忆/工具/技能）可能在模型完全不动的情况下破坏既有可靠行为。
- **context collapse**（ACE）：LLM 整体重写积累 context 时突然坍缩——18,282 token 的积累被一步压成 122 token，准确率 66.7→57.1（低于无适配基线 63.7）。
- **skill enshrinement**（SkillFlow）：弱模型把缺陷技能固化入库后反复复用，单次错误变成跨任务回归。
- **recursive drift**（SkillLearnBench）：纯自反馈技能迭代产生递归漂移。
- **更新生效性 vs 更新波及性**：PAST-Bench 测前者（该改的有没有改），retention 回归测后者（不该变的有没有变）——正反两面。
- 概念区分：**context rot** 是上下文长度增长导致的退化，不涉及更新，与 harness-level forgetting 是不同现象。

## 现象层证据（各组件层均已撞见）

| 工作 | 触及哪种回归 | 量化/防护 | 局限 |
|---|---|---|---|
| **HCL**（Kang et al., 2026） | 四组件更新的回归，正式命名现象 | anchor set（每旧任务 80 条）+ 提交门槛 Dn≤Bn + Avg. Fgt. 指标 + stability–plasticity 扫描 | anchor 是内部机制非公开基准；b=0 仍有 0.39 残余遗忘；自承 "efficient retention evaluation" 为 open challenge |
| **HarnessFix**（2026） | harness 补丁引入的回归 | regression-aware acceptance（TargetImprovement + RegressionBound）；消融去掉该门四基准全掉分 | 验证集是通用 held-out 非 retention 专用；不研究回归集本身该怎么建 |
| **Adaptive Auto-Harness**（2026） | 密集原地更新使准确率"peak and decline"；技能跨任务误触发 | 不守护而回避：harness 树（历史分支不覆写）+ solve-time 路由 | 回避而非量化 |
| **Harness Updating ≠ Benefit**（2026） | 更新收益的模型依赖性 | 拆分 updating/benefit 两能力，7 模型×3 基准 | 关键含义：**retention 结论绑定执行模型**，换模型不可迁移 |
| **SkillFlow / SkillLearnBench / ContinualSkillBench**（2026） | 技能库演化冲突、递归漂移、库膨胀 | lifelong 协议观察 | forgetting 只是观察不是协议核心，无更新级归因 |
| **ACE**（ICLR'26） | context collapse | 增量 delta 更新预防 | 预防设计，无回归度量 |
| **Misevolution**（2025） | 记忆积累→安全对齐衰减（RedCode 拒绝率 99.4%→54.4%） | 演化前后安全基准对照 | 只测安全维不测能力维 |
| **Slipstream**（2026） | compaction 静默丢失后续所需信息 | 轨迹接地验证 | 只覆盖 compaction 一种更新 |

## 可迁移的方法论（非 harness 场景）

- **RippleEdits**（2023）：从每个编辑**系统生成波及探针**（关联事实须更新、无关事实不得动）——"从更新反推回归探针"的直接模板；Gu et al.（2024）确立"编辑收益必须与保持性一起报告"的范式。
- **Ma et al.《(Why) Is My Prompt Getting Worse?》**（2023）：单点回归率 10.9% 属噪声量级 → **逐用例判定信噪比极低，必须 slice 级统计**；90% 回归集中于特定切片。
- **Miller《Adding Error Bars to Evals》**（2024, Anthropic）：成对差检验大幅缩减所需样本——检出 5pp 净回归需约 150-200 配对用例、10pp 约 50-100；**HCL 的 80 anchors/task 恰在"只能检出 ~10pp 级回归"的边缘**，这本身即可发表的功效分析结论。
- **CASPER**（2026）：变更感知的切片优先级排序，解决"全量回归太贵"。
- **MINJA/AgentPoison**（2025）：仅凭 query 即可注入恶意记忆（≈98% 成功）——记忆写入路径完全缺乏行为级验收的安全动机。
- **AgentEval**（工业界工具）：生产事故→回放→golden 用例的回归 CI 门禁已出现，但只有事故驱动用例，无习得能力 retention 用例。

## 立项方向（据 deep_D1 §4）

**RQ**：冻结模型的 harness 发生明文更新（memory 追加/改写、skill 增删改、指令编辑、compaction）时，如何以可控成本、可复现地量化其对既有可靠行为的破坏，并构建首个公开 retention 回归基准与守护协议？

要点：用例三源（历史成功轨迹回放 + **更新反推探针**〔RippleEdits 式，随 harness 内容增长〕+ 语义等价扰动）；每用例 k=3-5 次重复多数票 + 集合级配对检验；三层自动判定（可执行 verifier → 轨迹不变量 → LLM-judge 兜底）；受控更新算子矩阵 {append, rewrite, merge, delete, compact} × {memory, skill, 指令}；指标 URR（单次更新回归率）、Retention@t、locality 曲线、净学习收益、守护成本；把 HCL 门槛/HarnessFix 验收/CASPER 门禁作为被测守护机制做首次横评。

与相邻方向的关系：与 [记忆与持续学习基准](记忆与持续学习基准.md)（A5）互补——A5 测固定 harness 下记忆基质的读写召回，无 update-regression 维度；与 C6 lifelong 基准最近邻，retention 回归协议可作其核心组件，底稿倾向合并（synthesis 阶段定夺）。主要风险：HCL 团队已点名此为 open challenge、大概率在做后续，窗口估 6-12 个月；agent 非确定性使回归判定的算力成本是最大开销项。

## 参考

- 深挖底稿：`Project/survey/deep_D1_harness遗忘量化.md`（证据全查 + 回归集构建方案 + 功效分析）
- 关键论文：HCL `raw/papers/2026-kang-harness-continual-learning.pdf` · HarnessFix `raw/papers/2026-chen-harnessfix.pdf` · Adaptive Auto-Harness `raw/papers/2026-liu-adaptive-auto-harness.pdf` · Harness Updating≠Benefit `raw/papers/2026-lin-harness-updating-not-benefit.pdf` · SkillFlow `raw/papers/2026-zhang-skillflow.pdf` · ACE `raw/papers/2025-zhang-ace.pdf` · Misevolution `raw/papers/2025-shao-misevolution.pdf` · Slipstream `raw/papers/2026-chen-slipstream.pdf` · PAST-Bench `raw/papers/2026-xue-past-bench.pdf` · RippleEdits `raw/papers/2023-cohen-ripple-effects.pdf` · Ma et al. `raw/papers/2023-ma-prompt-regression-llm-apis.pdf` · Miller `raw/papers/2024-miller-error-bars-evals.pdf` · CASPER `raw/papers/2026-muse-casper.pdf` · MINJA `raw/papers/2025-dong-minja.pdf`
- 新增论文索引：`raw/papers/index_002_D1.yaml`

---
落款：survey-agent · 2026-08-30 10:15
