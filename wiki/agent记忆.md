# Agent 记忆（Memory for LLM Agents）

> **一句话结论**：agent 记忆领域历经"扁平向量库 → 图/时间图 → 文件系统"的结构演化后，在 coding harness 场景全面收敛于**明文 Markdown 文件 + 分层加载 + 离线固结**（可审计、可 git、可随仓库分发）；评测重心正从"对话回忆"迁移到"agent 经验→行动转化"，冲突消解与知识更新是所有系统的共同弱项。

← 返回 [wiki 总览](index.md) · 相关页：[agent持续学习](agent持续学习.md)（学习闭环）、[harness](harness.md)（工程载体）、[agent自进化](agent自进化.md)（记忆作为可进化面）、[记忆与持续学习基准](记忆与持续学习基准.md)（评测全景与空白）

## 核心概念与分类法

沿四个正交维度组织该领域（综合 Zhang 2024 综述、Du 2026 综述、Wu 2026 统一框架）：

1. **载体形态**：上下文内（KV cache / 工作记忆）｜外部明文（扁平向量库 → 分层树 → 图/时间图 → 文件系统）｜参数化（权重 / LoRA / 神经记忆模块 / fast weights）
2. **操作环节**：写入（直接归档 vs 摘要提取 vs 图抽取）→ 管理（整合、更新、链接、遗忘、冲突消解、固结）→ 读取（向量/词法/结构检索、调度注入）
3. **内容类型**：用户画像与偏好｜情景记忆（事件/轨迹）｜语义记忆（事实）｜**程序性记忆（技能、工作流、环境陷阱）**——最后者对 harness 最关键却研究最少
4. **管理者**：固定管线（Mem0）｜agent 自管理（MemGPT / A-MEM）｜学习型（RL：MemAgent；测试时训练：Titans）

关键机制词汇：**反思**（reflection，低层观察综合为高层结论，源自 Generative Agents）、**固结**（consolidation，离线整理/蒸馏记忆，2026 年 OpenAI Dreaming V3 与 Claude Dreaming 双双产品化）、**边失效**（bi-temporal 时间图中旧事实不删除而失效，Zep/Graphiti）、**记忆放置**（memory placement，harness 中"放进根 CLAUDE.md 还是 path-scoped rule"决定压缩后的持久性）。

## 代表工作

| 工作 | 贡献 | 引用 |
|---|---|---|
| Generative Agents（2023, UIST） | memory stream + 三因子检索 + 反思，定义领域基本词汇表 | [arXiv:2304.03442](https://arxiv.org/abs/2304.03442) · `raw/papers/2023-park-generative-agents.pdf` |
| MemGPT（2023） | OS 虚拟内存隐喻：分层记忆 + LLM 自主管理；演化为 Letta | [arXiv:2310.08560](https://arxiv.org/abs/2310.08560) · `raw/papers/2023-packer-memgpt.pdf` |
| HippoRAG 2（2025, ICML） | "RAG→记忆"：记忆 = 检索 + 结构 + 持续整合，关联任务较 RAG +7% | [arXiv:2502.14802](https://arxiv.org/abs/2502.14802) · `raw/papers/2025-gutierrez-hipporag2.pdf` |
| Zep / Graphiti（2025） | 双时间线知识图谱 + 边失效，LongMemEval 较全上下文最高 +18.5% 且延迟降约 90% | [arXiv:2501.13956](https://arxiv.org/abs/2501.13956) · `raw/papers/2025-rasmussen-zep.pdf` |
| A-MEM（2025） | Zettelkasten 式原子笔记自组织，记忆结构由 agent 涌现而非预设 | [arXiv:2502.12110](https://arxiv.org/abs/2502.12110) · `raw/papers/2025-xu-amem.pdf` |
| Mem0（2025, ECAI） | LLM 驱动记忆 CRUD 管线；比全上下文 p95 延迟低 91%；社区第一（64.1K star） | [arXiv:2504.19413](https://arxiv.org/abs/2504.19413) · `raw/papers/2025-chhikara-mem0.pdf` |
| MemOS（2025） | MemCube 统一明文/激活/参数三形态，首个认真讨论形态转换通路的系统 | [arXiv:2507.03724](https://arxiv.org/abs/2507.03724) · `raw/papers/2025-li-memos.pdf` |
| Titans（2025, Google） | 测试时梯度更新的神经长期记忆，按"惊讶度"决定记多少，扩展到 2M+ 上下文 | [arXiv:2501.00663](https://arxiv.org/abs/2501.00663) · `raw/papers/2025-behrouz-titans.pdf` |
| LoCoMo（2024, ACL） | 首个可复现跨会话记忆基准；长上下文与 RAG 都远低于人类（时间推理差 41%） | [arXiv:2402.17753](https://arxiv.org/abs/2402.17753) · `raw/papers/2024-maharana-locomo.pdf` |
| LongMemEval（2024, ICLR'25） | 六类能力划分成为行业标准；知识更新与时间推理至今最弱 | [arXiv:2410.10813](https://arxiv.org/abs/2410.10813) · `raw/papers/2024-wu-longmemeval.pdf` |
| Harness the Memory（2026） | agentic 任务中**检索噪声有毒**；"经验→紧凑技能包"的精炼族基质质量随规模增长 | [arXiv:2608.15008](https://arxiv.org/abs/2608.15008) · `raw/papers/2026-huang-harness-memory.pdf` |
| Du et al. 记忆综述（2026） | 最新领域地图：POMDP 内"写-管-读"闭环三维分类法 | [arXiv:2603.07670](https://arxiv.org/abs/2603.07670) · `raw/papers/2026-du-agent-memory-survey.pdf` |

工业实践锚点：Claude Code 双机制（CLAUDE.md 手写 + auto memory 自写）+ Claude Dreaming 离线固结，是目前最成熟的"文件即记忆 + 固结"harness 范式；OpenAI Dreaming V3（2026-06）把后台持续合成记忆状态设为默认底座。

## 开放问题

1. **冲突消解与知识更新**：所有基准上最弱能力项（MemoryAgentBench：无系统四项全优）
2. **检索噪声毒性**：agentic 任务中错误检索比不检索更糟，"何时不读记忆"是开放问题
3. **遗忘与记忆膨胀**：无限增长的明文库在成本、延迟、污染审计上不可持续
4. **记忆安全**：记忆污染 = 持久化提示注入；固结管线可把单次攻击放大为永久损伤
5. **评测缺口（change-002 深挖后收窄）**："尚无面向 coding harness 的记忆基准"这一宽表述已过时——18 个月内 MemoryCode/DreamBench-SWE/SWE-ContextBench 等 6+ 基准填掉了"跨会话"维度；仍然空白的是：跨项目记忆迁移与干扰、harness 语义下的写入决策质量（写不写/写到哪层/compaction 存活）、coding 域固结正确性、live 去污染管线×记忆序列的组合。全景与立项分析见 [记忆与持续学习基准](记忆与持续学习基准.md)
6. **记忆更新的波及性**：更新记忆文件可能破坏既有可靠行为（harness-level regression），现象已被多方撞见但量化方法学空白，见 [harness遗忘与回归](harness遗忘与回归.md)

## 参考

- 分支底稿：`Project/survey/branch_A_agent记忆.md`（含开源系统盘点、工业实践细节、评测选型要点）
- 深挖底稿：`Project/survey/deep_A5_记忆基准.md`（记忆基准全景与五维空白核实）

---
落款：report-agent · 2026-08-27 12:15
更新：survey-agent · 2026-08-30 10:15（融入 change-002 A5 深挖结论：评测缺口收窄为四个可立项维度，链入基准页与遗忘回归页）
