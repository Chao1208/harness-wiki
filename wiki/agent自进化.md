# Agent 自进化（Self-Evolving / Self-Improving Agents）

> **一句话结论**：自进化研究的重心已从"设计 agent"（2024 ADAS/AFlow）经"改整个 agent 代码库"（2025 DGM/SICA）移到"把 harness 组件化为显式可编辑面并配回归验证"（2026 Self-Harness/AHE/Meta-Harness）；**富文本反馈全面优于标量奖励**（GEPA 比 RL 高最多 +20% 且 rollout 少 35 倍），而**进化通路即攻击面**（Misevolution：记忆进化致拒绝率降 45–55%）是全领域必须内置的冷水。

← 返回 [wiki 总览](index.md) · 相关页：[harness](harness.md)（可编辑面清单）、[agent持续学习](agent持续学习.md)（经验固化通路）、[agent记忆](agent记忆.md)（记忆作为进化通路之一）、[可编辑面](可编辑面.md)（进化对象的谱系与消融证据）、[进化信号构造](进化信号构造.md)（弱评估器下的信号路线）

## 核心概念与分类法

三个正交轴可定位任何自进化工作（综合 Gao/Fang 两综述与 Tu/Liu 两博客）：

1. **进化对象（what）**：artifact（输出物，AlphaEvolve）→ harness（prompt/上下文/记忆/工具/技能/工作流/代码，DGM/AHE）→ 模型权重（R-Zero/Agent0 的零数据自博弈）
2. **进化时机（when）**：任务内（Self-Refine/Reflexion）→ 跨任务（DGM、技能库）→ 跨 agent/跨用户（档案与技能共享）
3. **进化信号（how）**：标量奖励（RL、基准分）vs 富文本反馈（GEPA 的完整轨迹反思、AHE 的根因报告）；单体自改（SICA/Gödel Agent）vs 群体进化（DGM/EvoAgent/HGM）

关键概念：**meta-agent search**（agent 设计空间 = 代码空间，用 LLM 搜索之，ADAS 确立）、**固化通路**（consolidation path：临时 artifact → 可复用 harness 逻辑 → 模型权重，Xinming Tu）、**CMP**（clade metaproductivity，用后代群体表现替代当前分数做选择信号，HGM）、**misevolution**（自进化朝非预期方向偏移）、**能力解耦**（harness 更新能力在 9B~Opus 级模型间近乎持平，收益能力才是瓶颈——"小模型进化、大模型执行"成为可能，Lin et al. 2026）。

## 代表工作

| 工作 | 贡献 | 引用 |
|---|---|---|
| Reflexion（2023, NeurIPS） | "以文本代替梯度"的最小自改进范式，HumanEval pass@1 91% | [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) · `raw/papers/2023-shinn-reflexion.pdf` |
| STOP（2023, COLM'24） | 最早"改进改进器"实验；警示：弱模型上递归改进反而退化 | [arXiv:2310.02304](https://arxiv.org/abs/2310.02304) · `raw/papers/2023-zelikman-stop.pdf` |
| ADAS（2024, ICLR'25） | meta-agent search 确立"agent 设计空间=代码空间"范式 | [arXiv:2408.08435](https://arxiv.org/abs/2408.08435) · `raw/papers/2024-hu-adas.pdf` |
| AFlow（2024, ICLR'25 oral） | 工作流代码上的 MCTS 搜索，比 ADAS +19.5% | [arXiv:2410.10762](https://arxiv.org/abs/2410.10762) · `raw/papers/2024-zhang-aflow.pdf` |
| Darwin Gödel Machine（2025, ICLR'26） | 冻结模型 + 进化 harness 代码，SWE-bench Verified 20.0%→50.0% | [arXiv:2505.22954](https://arxiv.org/abs/2505.22954) · `raw/papers/2025-zhang-darwin-godel-machine.pdf` |
| Huxley-Gödel Machine（2025） | 指出 Metaproductivity–Performance Mismatch，CMP 谱系搜索超 DGM/SICA | [arXiv:2510.21614](https://arxiv.org/abs/2510.21614) · `raw/papers/2025-wang-huxley-godel-machine.pdf` |
| AlphaEvolve（2025, DeepMind） | artifact 层进化天花板：56 年来首次改进 Strassen 4×4 复矩阵乘法、回收全球 0.7% 算力 | [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) · `raw/papers/2025-novikov-alphaevolve.pdf` |
| ShinkaEvolve（2025, Sakana） | 样本效率降一个数量级（约 150 样本达 SOTA），个人跑 harness 进化成为现实 | [arXiv:2509.19349](https://arxiv.org/abs/2509.19349) · `raw/papers/2025-lange-shinkaevolve.pdf` |
| GEPA（2025, ICLR'26 oral） | 遗传-Pareto 进化 + 轨迹反思，比 GRPO 高最多 +20% 且 rollout 少 35 倍；prompt 优化当前 SOTA | [arXiv:2507.19457](https://arxiv.org/abs/2507.19457) · `raw/papers/2025-agrawal-gepa.pdf` |
| Self-Harness（2026） | 弱点挖掘→提案→双重回归验证；学到的 harness 机制是**模型特异的** | [arXiv:2606.09498](https://arxiv.org/abs/2606.09498) · `raw/papers/2026-zhang-self-harness.pdf` |
| AHE（2026） | 可观测性三支柱驱动 harness 自动进化，Terminal-Bench 2 达 77.0% 超人工 Codex harness；消融定位收益主要来自 tools/middleware/长期记忆 | [arXiv:2604.25850](https://arxiv.org/abs/2604.25850) · `raw/papers/2026-lin-agentic-harness-engineering.pdf` |
| MCE（2026） | 双层优化：进化的不是上下文内容而是**管理上下文的机制**；技能=文件目录，与 Claude Code Skills 同构 | [arXiv:2601.21557](https://arxiv.org/abs/2601.21557) · `raw/papers/2026-ye-meta-context-engineering.pdf` |
| Misevolution（2025, 上海 AI Lab） | 首次系统定义自进化风险：四条进化通路条条是攻击面，顶级模型无一幸免 | [arXiv:2509.26354](https://arxiv.org/abs/2509.26354) · `raw/papers/2025-shao-misevolution.pdf` |

综述与骨架：Gao et al. what/when/how 三问综述（[arXiv:2507.21046](https://arxiv.org/abs/2507.21046) · `raw/papers/2025-gao-self-evolving-agents-survey.pdf`）、Fang et al. 四组件反馈环综述（[arXiv:2508.07407](https://arxiv.org/abs/2508.07407) · `raw/papers/2025-fang-self-evolving-ai-agents-survey.pdf`）、Lilian Weng《Harness Engineering for Self-Improvement》（2026-07 博客，本主题最重要的单篇综述性文章，提出优化对象递进链与七大挑战）。

## 开放问题

1. **弱评估器下的自进化（change-002 深挖后修正）**："几乎空白"不成立——权重层五条信号路线已成形且共进化 rubric 子方向已红海，harness 层有首篇 TTHE；剩余真空是 harness 层×真不可验证域、信号可靠性感知治理、延迟结果信号闭环三个交集，详见 [进化信号构造](进化信号构造.md)
2. **可编辑面的最小充分集（change-002 深挖后修正）**："完全无消融证据"不成立（AHE 换入消融、Yu & Desell 工具面交叉消融等已存在），但证据碎片化且只测收益不测风险；真空白是跨面×收益/风险双轴×固定预算的前瞻性消融，详见 [可编辑面](可编辑面.md)
3. **进化环安全审计协议**：Misevolution 四通路检测做成标准回归门，无任何开源实现（search tree B-4）
4. **scaffolding 自改进的天花板之争**：SICA 明言有上限，DGM 认为开放式探索可持续
5. **harness 进化与权重更新的联合优化**：SIA/Continual Harness 证据尚弱（与[持续学习](agent持续学习.md)交汇）

## 参考

- 分支底稿：`Project/survey/branch_B_agent自进化.md`（含开源项目 star 盘点、工程博客、防御设计汇总）
- 深挖底稿：`Project/survey/deep_B1_可编辑面消融.md`、`Project/survey/deep_B3_弱评估器自进化.md`

---
落款：report-agent · 2026-08-27 12:16
更新：survey-agent · 2026-08-30 10:15（融入 change-002 B1/B3 深挖结论：开放问题 1、2 由"空白"修正为"部分空白"，链入可编辑面页与进化信号构造页）
