# Agent 持续学习（Continual / Lifelong Learning for LLM Agents）

> **一句话结论**：agent 持续学习的主线是"从存储轨迹到反思轨迹再到抽象经验"（storage → reflection → experience）——朴素经验回放已被证伪为弱基线，失败经验蒸馏与成功同等重要；实现手段上**训练无关的非参数路线是 2023–2026 绝对主流**，但"灾难性遗忘"并未消失，只是换了形态（context collapse、检索退化、无关经验干扰）。

← 返回 [wiki 总览](index.md) · 相关页：[agent记忆](agent记忆.md)（存取基础设施）、[agent自进化](agent自进化.md)（进化机制）、[harness](harness.md)（学习闭环的天然载体）、[记忆与持续学习基准](记忆与持续学习基准.md)（lifelong 评测全景）、[harness遗忘与回归](harness遗忘与回归.md)（遗忘新形态的量化）

## 核心概念与分类法

**三条实现轴**：

1. **参数轴**（改权重）：持续预训练/微调、测试时训练 TTT。真正改变能力上限，但有训练成本、灾难性遗忘、对齐破坏三重代价，对 API 模型不可用；2026 年随开源强模型回潮。
2. **上下文轴**（维护一份持续编辑的 playbook）：Dynamic Cheatsheet → ACE 演进线。核心技术问题是**防坍缩的增量更新协议**（ACE 的 delta 条目 + helpful/harmful 计数是当前最佳答案）。
3. **外部记忆轴**（结构化库 + 检索），按**经验抽象层级**递增：原始轨迹（回放，弱基线）→ 案例（Memento）→ 因果模式（CLIN）→ 工作流（AWM）→ 策略记忆（ReasoningBank）→ 可执行技能（Voyager/SkillWeaver）→ 程序性脚本（Memp）→ **元技能：记忆操作本身**（MemSkill）。层级越高迁移性越强，但蒸馏难度与出错风险越大。

三轴正合流为**半参数**设计：外部库承担事实与程序知识，偶发参数更新承担能力内化——与人类"陈述性/程序性记忆 + 睡眠巩固"的类比在多篇 2026 文献反复出现。

**非参数系统的"遗忘"新形态**：context collapse（整体重写丢信息，ACE）、无关经验干扰（LifelongAgentBench）、context rot（Panini）——本质是稳定性-可塑性权衡在非参数系统的镜像。change-002 深挖确认该现象已在各组件层被独立撞见并被 HCL 正式命名为 harness-level forgetting，量化方法学与回归集是新空白，见 [harness遗忘与回归](harness遗忘与回归.md)。

**评测必测四件套**：流上累积成功率及其斜率、旧任务保持率（backward transfer）、新环境零样本迁移（技能资产保值度）、成本曲线（token/延迟随经验库增长的变化）。

## 代表工作

| 工作 | 贡献 | 引用 |
|---|---|---|
| Voyager（2023, TMLR） | "技能 = 经验证代码 + 可检索描述"范式确立，Claude Code Skills 的学术原型 | [arXiv:2305.16291](https://arxiv.org/abs/2305.16291) · `raw/papers/2023-wang-voyager.pdf` |
| ExpeL（2023, AAAI'24） | 成败轨迹对比归纳自然语言 insights，无梯度经验学习成立 | [arXiv:2308.10144](https://arxiv.org/abs/2308.10144) · `raw/papers/2023-zhao-expel.pdf` |
| CLIN（2023, AI2） | 因果抽象记忆；证明记忆的**表示形式**决定迁移能力 | [arXiv:2310.10134](https://arxiv.org/abs/2310.10134) · `raw/papers/2023-majumder-clin.pdf` |
| AWM（2024, ICML'25） | 工作流归纳，离线+在线双模式；Mind2Web +24.6%、WebArena +51.1%（相对） | [arXiv:2409.07429](https://arxiv.org/abs/2409.07429) · `raw/papers/2024-wang-agent-workflow-memory.pdf` |
| Dynamic Cheatsheet（2025） | 自编辑"小抄"即可带来测试时持续学习，GPT-4o 在 AIME 上翻倍 | [arXiv:2504.07952](https://arxiv.org/abs/2504.07952) · `raw/papers/2025-suzgun-dynamic-cheatsheet.pdf` |
| ACE（2025, ICLR'26） | 增量 delta playbook 防坍缩；与 harness 工程形态最接近的持续学习方案 | [arXiv:2510.04618](https://arxiv.org/abs/2510.04618) · `raw/papers/2025-zhang-ace.pdf` |
| SkillWeaver（2025, OSU） | 探索→练习→测试→蒸馏 API 技能；强 agent 技能给弱 agent 用提升最高 +54.3% | [arXiv:2504.07079](https://arxiv.org/abs/2504.07079) · `raw/papers/2025-zheng-skillweaver.pdf` |
| Memp（2025, 浙大/阿里） | 程序性记忆构建/检索/更新三元设计空间的首个受控实验 | [arXiv:2508.06433](https://arxiv.org/abs/2508.06433) · `raw/papers/2025-fang-memp.pdf` |
| Memento（2025, UCL） | 记忆增广 MDP + 案例推理：梯度只流经案例选择器，基座冻结；GAIA 验证集 87.88% Pass@3 | [arXiv:2508.16153](https://arxiv.org/abs/2508.16153) · `raw/papers/2025-zhou-memento.pdf` |
| ReasoningBank + MaTTS（2025, Google） | 成败双向蒸馏策略级记忆；"记忆×测试算力"确立为新扩展维度 | [arXiv:2509.25140](https://arxiv.org/abs/2509.25140) · `raw/papers/2025-ouyang-reasoningbank.pdf` |
| MemSkill（2026） | 元技能：不仅学"记什么"还学"**如何记**" | [arXiv:2602.02474](https://arxiv.org/abs/2602.02474) · `raw/papers/2026-zhang-memskill.pdf` |
| LifelongAgentBench（2025） | 首个 lifelong agent 统一基准；**朴素经验回放收益有限甚至有害**的负结果 | [arXiv:2505.11942](https://arxiv.org/abs/2505.11942) · `raw/papers/2025-zheng-lifelongagentbench.pdf` |
| StreamBench（2024, NeurIPS） | 首个流式在线改进基准；"只回放自我生成且被证实正确的例子"是极强廉价基线 | [arXiv:2406.08747](https://arxiv.org/abs/2406.08747) · `raw/papers/2024-wu-streambench.pdf` |
| LLM 持续学习综述（2024, CSUR） | 参数化路线完整地图：纵向/横向连续性双维框架 | [arXiv:2404.16789](https://arxiv.org/abs/2404.16789) · `raw/papers/2024-shi-llm-continual-learning-survey.pdf` |

## 开放问题

1. **经验质量与污染**：自判成败引入错误经验且会自我强化；缺可靠的验证、置信标注与溯源机制
2. **非参数遗忘/容量管理**：库无限增长后的检索退化；何时删、删什么（Memp 初步触及，无定论）
3. **冲突消解**：新经验与旧规则矛盾时的仲裁（MemoryAgentBench 显示为普遍短板）
4. **参数 vs 非参数的边界条件**：什么时候值得把经验"蒸进"权重，缺成本-收益定量刻画
5. **面向 coding harness 的 lifelong 基准（change-002 深挖后修正）**：字面空白已被一年内 8 个基准填掉（SWE-Bench-CL、SWE-Milestone〔ICML 2026〕、SWE-CI、SWE-ContextBench、SkillFlow 等）；剩余可辩护组合是"真实仓库跨会话演化 × harness 原生记忆 × lifelong 三度量 × live 污染控制"的合取，底稿建议与 A5 记忆基准合并立项，详见 [记忆与持续学习基准](记忆与持续学习基准.md)

**本项目的关键判断**：harness 相对学术系统有两大天然优势——(a) 执行环境提供客观成败信号（编译、测试、退出码），绕开 LLM 自判这一最大质量风险；(b) git 免费提供版本化、审查与回滚，正是学术界呼吁的治理层。底稿中给出了可落地的最小学习闭环设计草图（轨迹判定→双向蒸馏→验证准入→增量合入→维护修剪）。

## 参考

- 分支底稿：`Project/survey/branch_C_agent持续学习.md`（含时间线、参数/非参数对比表、评测协议要点、最小闭环草图）
- 深挖底稿：`Project/survey/deep_C6_lifelong_coding基准.md`（coding 序列化基准缺口矩阵与合并立项论证）

---
落款：report-agent · 2026-08-27 12:16
更新：survey-agent · 2026-08-30 10:15（融入 change-002 C6/D1 深挖结论：lifelong 基准空白收窄并指向合并立项，遗忘新形态链入 harness遗忘与回归页）
