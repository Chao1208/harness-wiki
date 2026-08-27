# 分支 A 调研底稿：Agent 记忆（Memory for LLM Agents）

> openspec change-001 · 分支 A · 覆盖 2023-01 至 2026-08
> 本底稿是后续 wiki 与调研报告的唯一素材来源。所有已下载 PDF 见 `raw/papers/`，登记于 `raw/papers/index_fragments/A.yaml`。
> 注：文中标注"[库内: xxx.pdf]"表示 PDF 已归档在 `raw/papers/` 下；其中 4 篇（LoCoMo、LongMemEval、Zhang 综述、Generative Agents）由并行 agent 先行下载入库，本分支未重复登记。

---

## A1 记忆架构与系统论文

### 综述导航（读论文前先读这三篇）
- **A Survey on the Memory Mechanism of Large Language Model based Agents**（Zhang et al., 2024, arXiv 2404.13501, TOIS 2025）[库内: 2024-zhang-memory-survey.pdf]：2024 年的领域地图，定义记忆的来源（试内/跨试/外部知识）、形式（文本/参数）与操作（写入/管理/读取），并整理评测与应用。截至 2026 年仍是引用最广的记忆综述，但不覆盖 2025 后的爆发期。
- **Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers**（Du et al., 2026, arXiv 2603.07670）[库内: 2026-du-agent-memory-survey.pdf]：最新综述。把记忆形式化为 POMDP 循环内的"写-管-读"闭环，给出三维分类法；系统覆盖 2025-2026 的学习型记忆控制（RL/TTT）、agentic 基准（MemBench、MemoryAgentBench、MemoryArena）与工程现实（成本/延迟/污染）。本底稿的分类框架大量参考此文。
- **From Human Memory to AI Memory**（Wu et al., 2025, arXiv 2504.15965）：以人类记忆分类（感觉/工作/长期，情景/语义/程序）为镜子映射 AI 记忆的 3D-8Q 框架，适合作认知科学视角的补充读物（未下载，链接备查）。

### A1.0 奠基工作（2023）

#### Generative Agents: Interactive Simulacra of Human Behavior
- 作者/年份/venue：Park et al., 2023, UIST 2023
- 链接：https://arxiv.org/abs/2304.03442 [库内: 2023-park-generative-agents.pdf]
- 摘要：在 25 个 agent 组成的虚拟小镇中首次提出完整的 agent 记忆架构：**memory stream**（以自然语言记录全部经历的追加式日志）+ **检索函数**（按时近性 recency、重要性 importance、相关性 relevance 三因子加权）+ **反思 reflection**（周期性将低层观察综合为高层结论）+ 规划。消融实验证明观察、反思、规划三部件各自对行为可信度有独立贡献。该文定义了此后三年几乎所有 agent 记忆系统的基本词汇表（观察→检索→反思→行动闭环），是本分支一切工作的共同源头。

#### MemGPT: Towards LLMs as Operating Systems
- 作者/年份/venue：Packer et al., 2023, arXiv（后成为 Letta 公司产品）
- 链接：https://arxiv.org/abs/2310.08560 [库内: 2023-packer-memgpt.pdf]
- 摘要：将操作系统**虚拟内存**思想搬到 LLM：上下文窗口视为"主存"（main context），外部存储视为"磁盘"（external context），由 LLM 自身通过函数调用（自我编辑记忆块、分页换入换出、检索归档记忆）管理记忆层级，中断机制控制执行流。在文档分析与多会话对话（DMR 基准）上显著超过固定上下文基线。意义：确立"**LLM 自主管理记忆**"（agentic memory management）与"分层记忆"两大范式；其开源实现演化为 Letta（见 A3）。

#### MemoryBank: Enhancing LLMs with Long-Term Memory
- 作者/年份/venue：Zhong et al., 2023, AAAI 2024
- 链接：https://arxiv.org/abs/2305.10250
- 摘要：为陪伴型对话引入长期记忆库：记忆写入后按**艾宾浩斯遗忘曲线**动态调整保留强度，被检索命中的记忆得到强化，久未使用的自然衰减；同时维护事件摘要与不断更新的用户画像。在心理陪伴场景（SiliconFriend）验证。意义：最早把"遗忘"作为一等公民的设计，后续几乎所有系统的 decay/reinforcement 机制都可溯源于此。

### A1.1 图结构记忆

#### HippoRAG: Neurobiologically Inspired Long-Term Memory for LLMs
- 作者/年份/venue：Gutiérrez et al., 2024, NeurIPS 2024
- 链接：https://arxiv.org/abs/2405.14831 [库内: 2024-gutierrez-hipporag.pdf]
- 摘要：受海马体索引理论（hippocampal indexing theory）启发：离线用 LLM 做开放信息抽取构建知识图谱（皮层），在线检索时以查询实体为种子在图上跑 **Personalized PageRank**（海马体模式补全），单步完成多跳关联检索。多跳 QA 上超过当时最强检索器最高 20%，且比迭代式检索（IRCoT）便宜 10-30 倍。意义：证明图结构+图算法可以替代多轮 agentic 检索，是"结构化外部记忆"路线的代表。

#### HippoRAG 2 / From RAG to Memory: Non-Parametric Continual Learning for LLMs
- 作者/年份/venue：Gutiérrez et al., 2025, ICML 2025
- 链接：https://arxiv.org/abs/2502.14802 [库内: 2025-gutierrez-hipporag2.pdf]
- 摘要：把连续知识积累明确表述为"**非参数持续学习**"问题，在 HippoRAG 基础上加入段落节点（phrase+passage 双层图）、查询到三元组的深度检索耦合、以及 LLM 在线识别记忆（recognition memory）过滤噪声。在事实记忆、常识和多跳关联任务上全面超过标准 RAG 与各类记忆系统，关联记忆任务较 RAG +7%。意义：给出"RAG→记忆"的演化论述——记忆 = 检索 + 结构 + 持续整合，直接挑战"长上下文可取代外部记忆"的观点。

#### Zep: A Temporal Knowledge Graph Architecture for Agent Memory
- 作者/年份/venue：Rasmussen et al., 2025, arXiv（Zep 公司，引擎开源为 Graphiti）
- 链接：https://arxiv.org/abs/2501.13956 [库内: 2025-rasmussen-zep.pdf]
- 摘要：核心是 **Graphiti 时间感知知识图谱**：每条边带双时间线（bi-temporal：事实有效时间 + 系统摄入时间），新信息与旧事实冲突时不删除而是**边失效（edge invalidation）**，保留完整历史可回溯查询；三层图结构（episode 子图→语义实体子图→社区子图）。DMR 上 94.8% 超过 MemGPT 的 93.4%；LongMemEval 上较全上下文基线准确率提升最高 18.5% 且延迟降低约 90%。意义：把"事实随时间演变"作为记忆系统的中心问题，是时间推理类查询目前的最强设计之一。

### A1.2 Agentic memory（记忆自组织）

#### A-MEM: Agentic Memory for LLM Agents
- 作者/年份/venue：Xu et al., 2025, arXiv（NeurIPS 2025 收录版本为更新稿）
- 链接：https://arxiv.org/abs/2502.12110 [库内: 2025-xu-amem.pdf]
- 摘要：借鉴 **Zettelkasten 卡片盒笔记法**：每条记忆是包含上下文描述、关键词、标签的原子笔记；新笔记写入时 LLM 主动建立与历史笔记的链接（link generation），并触发**记忆进化（memory evolution）**——被链接的旧笔记的描述/标签被更新以吸收新信息。在 LoCoMo 六个基座模型上超过静态记忆基线，多跳任务提升约 2 倍，且 token 成本更低。意义：代表"记忆结构不预先设计、由 agent 自组织涌现"的路线，与 MemGPT 的固定分层形成对照。

#### RMM: Reflective Memory Management（补充条目）
- 作者/年份/venue：Tan et al., 2025, ACL 2025（Google 合作）
- 链接：https://arxiv.org/abs/2503.08026
- 摘要：针对个性化长对话提出双向反思机制：**前瞻反思**（prospective reflection）在写入侧把对话动态摘要为不同粒度（话题/轮次/会话）的记忆条目；**回顾反思**（retrospective reflection）在读取侧用生成结果作为信号、以在线 RL 迭代改进检索器（引用归因作为奖励）。在 LongMemEval 上比无记忆管理基线提升 10%+。意义：把"检索粒度应该自适应"和"检索器可以从下游反馈持续学习"两个此前被忽略的问题摆上台面。

#### MemTree（补充条目）
- 作者/年份/venue：Rezazadeh et al., 2025（ICLR 2025 workshop → 正式版）
- 链接：https://arxiv.org/abs/2410.14052
- 摘要：把记忆组织为**动态层次树**：新信息到来时从根向下遍历，按语义相似度决定并入现有节点还是分裂新节点，各层维护不同抽象级别的摘要（越靠根越抽象）。在线增量维护，无需离线重建。对话与文档理解任务上超过扁平向量记忆。意义：树结构是介于"扁平向量库"与"知识图谱"之间的中间路线，读取时可按需选择抽象层级，与 harness 中"目录级/文件级/行级"天然的层次语义契合。

#### 经验/轨迹记忆（与持续学习交界，简记）
- **Reflexion**（Shinn et al., 2023, NeurIPS 2023, https://arxiv.org/abs/2303.11366）：失败轨迹→语言化自我反思→存入情景缓冲→下次尝试注入。"经验记忆"最小可行形态。
- **ExpeL**（Zhao et al., 2024, AAAI 2024）：跨任务收集成功/失败轨迹，离线归纳成自然语言 insights + 案例库，推理时检索注入，无需改权重。
- **Agent Workflow Memory / AWM**（Wang et al., 2024, ICML 2025, https://arxiv.org/abs/2409.07429）：从 agent 轨迹中归纳可复用**工作流**（子任务级动作模板）存入记忆，Mind2Web/WebArena 上相对基线成功率 +24.6%/+51.1%。对 coding harness 最具直接参考价值的记忆内容形态。
- 这些工作的完整展开归分支 B（持续学习），此处仅记录其作为"程序性记忆"的接口位置。

### A1.3 记忆操作系统（Memory OS）

#### MemOS: A Memory OS for AI System
- 作者/年份/venue：Li et al., 2025, arXiv（MemTensor 团队，开源）
- 链接：https://arxiv.org/abs/2507.03724 [库内: 2025-li-memos.pdf]
- 摘要：主张把记忆提升为与算力同级的**一等系统资源**：统一抽象 **MemCube**，覆盖三种记忆形态——明文记忆（可编辑文本/图）、激活记忆（KV cache 等运行时状态）、参数记忆（权重/LoRA），并支持三者之间转换（如热点明文记忆蒸馏进参数）；配备调度、生命周期管理、权限治理。LoCoMo 上较基线整体提升明显，时间推理类提升最大。意义：第一个认真讨论"明文↔激活↔参数"记忆形态转换通路的系统论文，也是"记忆即操作系统"叙事的代表。

#### MIRIX: Multi-Agent Memory System for LLM-Based Agents
- 作者/年份/venue：Wang & Chen, 2025, arXiv
- 链接：https://arxiv.org/abs/2507.07957 [库内: 2025-wang-mirix.pdf]
- 摘要：按认知科学划分**六类记忆组件**：Core（核心画像）、Episodic（情景）、Semantic（语义）、Procedural（程序性）、Resource（资源文件）、Knowledge Vault（凭证等敏感库），由一个记忆管理多 agent 系统负责路由读写。在多模态 ScreenshotVQA 上比 RAG 基线准确率 +35% 且存储省 99.9%，LoCoMo 达 85.4%。意义：把"记忆类型学"做成显式工程分区，为多模态、屏幕级持续感知场景提供了参考架构。

#### MemoryOS（补充条目）
- 作者/年份/venue：Kang et al., 2025, arXiv 2506.06326（EMNLP 2025）
- 链接：https://arxiv.org/abs/2506.06326
- 摘要：同样借 OS 隐喻但更贴近传统存储层级：短期（对话页）/中期（分段主题）/长期（用户画像）三级存储，配分段分页调度与热度驱动的升降级。LoCoMo 上 F1 较此前最优提升约 49%。与 MemOS 名字相近但路线不同：MemoryOS 重在分层对话记忆管理，MemOS 重在记忆形态统一抽象。

### A1.4 参数化 / 隐式记忆

#### Titans: Learning to Memorize at Test Time
- 作者/年份/venue：Behrouz et al., 2025, arXiv（Google Research）
- 链接：https://arxiv.org/abs/2501.00663 [库内: 2025-behrouz-titans.pdf]
- 摘要：提出**神经长期记忆模块**：一个在推理时以梯度方式持续更新的小网络，按"惊讶度"（surprise，梯度大小）决定记多少、配权重衰减实现遗忘；attention 作为短期记忆，神经记忆作为长期记忆，另有任务级持久记忆参数。Titans 架构在语言建模、needle-in-haystack 上超过 Transformer 与现代线性 RNN，可扩展到 2M+ 上下文。意义：参数化记忆路线的旗舰工作；其后续 Nested Learning/HOPE（NeurIPS 2025）进一步把"模型即多层嵌套优化问题"作为持续学习框架。对本项目意义在于指出 harness 外部记忆之外还存在"改模型"的第二通路。

#### MemAgent: Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent
- 作者/年份/venue：Yu et al., 2025, arXiv 2507.02259（字节跳动）
- 链接：https://arxiv.org/abs/2507.02259
- 摘要：把长文本切块流式读取，模型维护一个固定长度的**可覆写明文记忆**，用 RL（DAPO）端到端训练"该记什么、该忘什么"；8K 上下文训练可外推到 3.5M token 输入且几乎无损，O(N) 线性复杂度。意义：证明"记忆策略可以被 RL 学出来"，代表学习型记忆管理（相对 MemGPT 的提示工程式管理）。同路线还有 MEM1（Zhou et al., 2025, arXiv 2506.15841：RL 训练 agent 在多轮工具使用中维护恒定大小的推理+记忆联合状态）。

#### 长上下文 vs 外部记忆之争（脉络梳理）
- 2024：LoCoMo 论文实测长上下文 LLM 与 RAG 在超长对话上都显著低于人类（时间推理差 41%），两条路线都不够。
- 2025：Mem0 论文实测全上下文（full-context）准确率上限高于多数记忆系统，但 token 成本与延迟不可接受（p95 延迟差 91%）；HippoRAG 2 论证结构化记忆在关联/时间任务上超过长上下文。
- 2025-2026：共识转向"**两者互补 + 效率是一等指标**"：新基准（BEAM、LongMemEval-V2）把 token 足迹和延迟与准确率一起纳入排行（LAFS 等指标）；架构上出现混合路由（上下文内 KV、外部明文、参数化三通路自适应选择，如 UniMem 方向）。2026 立场文《Contextual Agentic Memory is a Memo, Not True Memory》（arXiv 2604.27707）进一步论证：纯明文情景库只是"备忘录"，必须有**固结通道**（consolidation：周期性把经验蒸馏进参数，类比睡眠），且参数级记忆在可审计性（版本化、回滚）上反而优于无限增长的明文库；难点不在机制而在策略（何时固结、固结什么）。

### A1.5 2026 年新增系统与统一框架

- **Memory in the LLM Era: Modular Architectures and Strategies in a Unified Framework**（Wu et al., 2026, arXiv 2604.01707）：把记忆机制统一分解为四阶段——信息提取、记忆管理、存储结构、检索机制，在 LoCoMo/LongMemEval/MemoryArena 上系统复现对比 A-MEM、Mem0、MemGPT、MemoryOS、MemOS、MemTree 等十余系统，并给出上下文可扩展性与位置敏感性分析；据此设计的新方法在性能与成本效率上综合最优。是目前最好的"横评+框架"论文。
- **Are We Ready For An Agent-Native Memory System?**（2026, arXiv 2606.24775）：从数据管理视角把现有系统分四类：分层上下文管理（MemGPT/Letta）、知识图谱记忆（Mem0g/Zep）、复合混合系统（A-MEM）、以及运行态/长期存储分离架构；指出该领域碎片化严重、缺乏数据库级的一致性/事务/索引设计，呼吁"agent 原生记忆系统"。
- **LIGHT**（Tavakoli et al., ICLR 2026）：情景检索 + 草稿本（scratchpad）+ 工作记忆缓冲三通路组合，可扩展到 1000 万 token 交互历史。
- **Scaling Self-Evolving Agents via Parametric Memory**（2026, arXiv 2606.04536）：把 fast weights（Δ 参数）纳入 rollout 动态，只从蒸馏后的记忆中做选择性测试时训练，兼顾参数化记忆的泛化优势与 agent 决策过程的可控性。

---

## A2 记忆基准与评测

### 既有主力基准（2024-2025）

#### LoCoMo: Evaluating Very Long-Term Conversational Memory of LLM Agents
- 作者/年份/venue：Maharana et al., 2024, ACL 2024（Snap Research）
- 链接：https://arxiv.org/abs/2402.17753 [库内: 2024-maharana-locomo.pdf]
- 摘要：机器生成+人工校验的超长多会话对话数据集：平均约 600 轮、16K token、最多 32-35 个会话，基于人设与时间事件图保证长程一致性；任务含 QA（单跳/多跳/时间/开放域，约 1,986 问）、事件摘要、多模态对话生成。结论：长上下文 LLM 与 RAG 都远低于人类（总体差 36%，时间推理差 41%）。意义：第一个可复现的跨会话记忆基准，至今仍是所有记忆系统对比的默认战场；但因数据合成痕迹与被"刷榜"，2026 年其区分度已趋饱和。

#### LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
- 作者/年份/venue：Wu et al., 2024, ICLR 2025
- 链接：https://arxiv.org/abs/2410.10813 [库内: 2024-wu-longmemeval.pdf]
- 摘要：500 个人工筛选问题，系统覆盖六类能力：单会话用户信息回忆、单会话助手回忆、单会话偏好、**知识更新**、**时间推理**、多会话综合；可自由扩展干扰会话长度（S/M 版本）。实测商用助手在持续交互中准确率下降 30%。意义：能力维度划分成为行业标准；知识更新与时间推理两项至今仍是各系统最弱项，也是 Zep、Mem0 等主打卖点的评测依据。

#### DMR（Deep Memory Retrieval，背景条目）
- 来源：MemGPT 论文（2023）引入的多会话对话记忆检索测试，规模小（约 500 题、5 会话）。
- 现状：Zep（94.8%）与 MemGPT（93.4%）均已刷到 94%+，2025 年后被视为饱和基准，Zep 论文明确指出其无法反映企业真实场景，转向 LongMemEval。记录在此是因为大量 2023-2024 论文以它为主战场，读旧文献时需知其局限。

#### PrefEval（补充条目）
- 作者/年份/venue：Zhao et al., 2025, ICLR 2025
- 链接：https://arxiv.org/abs/2502.09597
- 摘要：专测**用户偏好遵循**：3,000 对偏好-查询，20 话题，考察助手能否在长对话后仍主动遵守用户此前显式/隐式表达的偏好。发现前沿 LLM 在 10 轮之后偏好遵循率骤降（零样本下 <10%），RAG 与提示技巧只能部分缓解。意义：把"个性化记忆"从"能否回忆"推进到"能否主动应用"，与 harness 中"用户纠正过的编码习惯应持续生效"（Claude Code auto memory 的动机）完全同构。

#### 其它 2025 基准
- **MemBench**（Tan et al., 2025, ACL 2025 Findings, arXiv 2506.21605）：超越事实回忆，纳入反思性记忆（participation/reflection 双视角）与效率维度，评 LLM agent 的记忆能力全谱。
- **MemoryAgentBench**（Hu et al., 2025, arXiv 2507.05257）：把记忆分解为四能力——精确检索（AR）、测试时学习（TTL）、长程理解（LRU）、**冲突消解（CR）**；结论是现有系统没有一个四项全优，冲突消解普遍最差。
- **PersonaMem**（2025）：以用户画像/个性化为中心，32k token 量级，考察助手能否随用户状态演化调整回应。

### 2026 新基准（重点：从"对话记忆"转向"agent 经验记忆"）

- **MemoryArena**（He et al., 2026, arXiv 2602.16313, UCSD/Stanford 等）：把记忆放进**相互依赖的多会话 agentic 任务**：后续任务的正确执行依赖此前会话中形成的记忆，直接度量"记忆→行动"转化率，而非问答式回忆。暴露出高分问答型记忆系统在任务耦合场景大幅退化。
- **LongMemEval-V2**（2026, arXiv 2605.12493）：451 个人工问题 + 多模态 web-agent 轨迹长历史（最大 115M token），五种能力：静态状态回忆、动态状态追踪、工作流知识、环境陷阱（gotchas）、前提感知；评测同时计分准确率与查询延迟（LAFS：延迟-准确率前沿增益）。**与本项目 harness 主题最相关的基准**——它评的正是"agent 能否通过记忆变成熟练老同事"。
- **BEAM**（2026）：100 段 10 万-1000 万 token 的超长对话，2,000 问、10 种记忆能力分类，专测极端规模；Mem0 自报 BEAM(10M) 仅 48.6，说明千万 token 级仍远未解决。
- **AgentMemBench**（2026, arXiv 2608.00009）：统一条件下对比五大策略族（in-context / 外部 KV / 图 / 压缩 / web 增强记忆），覆盖开放对话、任务规划、长程 QA 三任务型。
- **Harness the Memory: A Holistic Evaluation of Memory Substrates in Memory Agents**（Huang et al., 2026, arXiv 2608.15008）[库内: 2026-huang-harness-memory.pdf]：横跨用户中心（LoCoMo、MemoryAgentBench）与 **agent 中心**（ALFWorld 具身规划、BigCodeBench-Hard 代码）四个基准评测各类记忆基质（substrate）。核心发现：检索型/结构型基质在回忆型任务受益于规模，但在 agentic 任务中**检索噪声有毒**，把经验蒸馏成紧凑技能包（skill bundle）的"精炼族"基质质量随规模增长且读取成本恒定。对 coding harness 的记忆设计有直接指导意义。
- **独立评测平台**：AMB（agentmemorybenchmark.ai，开源中立复现，统一跑 BEAM/LoCoMo/LongMemEval/PersonaMem/lifebench）与 Bench'd 等出现，动因是**厂商自报成绩与独立复测差距巨大**（如某记忆产品自报 LongMemEval 93.4%，独立复测 OSS 版仅 32.4%，甚至低于无记忆基线 57.6%）。评测可信度本身已成为 2026 年的领域议题。

### 评测选型要点（为本项目后续实验备查）
- **按场景选基准**：对话助手回忆 → LongMemEval；跨会话持久性 → LoCoMo；记忆是否改善任务结果 → MemoryArena；agent 经验/环境知识（最贴合 harness）→ LongMemEval-V2；极端规模 → BEAM；偏好主动应用 → PrefEval。
- **必报指标**：准确率之外必须报每查询 token 数、p50/p95 延迟、存储增长率；2026 年评审已默认要求（LAFS/MemScore 类联合指标）。
- **防坑清单**：(1) LoCoMo 存在标注噪声与合成痕迹，多篇论文报告其上限失真；(2) 厂商自报成绩一律标注"self-reported"，采信 AMB/Bench'd 独立复测值；(3) 评测记忆系统时必须固定基座模型与检索预算，否则不可比；(4) 问答型基准高分不预示 agentic 任务表现（Harness the Memory 的教训）。
- **本项目缺口**：尚无面向 coding harness 的记忆基准——"跨会话修 bug 时是否记得上次的环境坑/用户编码偏好/仓库惯例"无人评测，是明确的论文机会（详见综合分析）。

---

## A3 开源记忆系统（GitHub）

> star 数与活跃度为 2026-08 检索值，来源为 GitHub 页面与第三方横评，标注"约"者为二手来源。

#### Mem0（mem0ai/mem0）
- ⭐ 64.1K（fork 7.5K，创建于 2023-06），Apache 2.0，Python/TS
- 论文：Chhikara et al., ECAI 2025, https://arxiv.org/abs/2504.19413 [库内: 2025-chhikara-mem0.pdf]
- 设计：两阶段管线——提取阶段用 LLM 从对话增量提取候选"记忆单元"，更新阶段由 LLM 决策 ADD/UPDATE/DELETE/NOOP（LLM 驱动的记忆 CRUD）；默认向量存储，Mem0g 变体加图存储记实体关系。论文在 LoCoMo 上首次十系统横评：比 OpenAI 内置 memory 高 26%，比全上下文 p95 延迟低 91%、token 省 90%。
- 活跃度/动向：领域第一大社区，21 框架 20 向量库集成，OpenMemory MCP 本地记忆服务器；2026-04 发布新算法（单遍分层提取+多信号检索），自报 LoCoMo 92.5 / LongMemEval 94.4 / BEAM(1M) 64.1。注意：高分属**托管平台**（含专有优化），OSS 版明确"方向一致但数值不同"，独立复测差距大（见 A2）。
- 取舍：易集成、生态最大；但记忆抽取有损、召回依赖提取质量，托管/OSS 双轨引发信任争议。

#### Letta（letta-ai/letta，前身 MemGPT）
- ⭐ 24.5K（fork 2.6K，创建于 2023-10），Apache 2.0
- 设计：不是"记忆层库"而是**有状态 agent 运行时**：记忆块（persona/human/task 等 memory blocks）驻留上下文由 agent 自编辑，归档记忆走向量库；agent 状态整体可导出（.af agent file 格式）；配 sleep-time compute（空闲期离线整理记忆）。
- 活跃度/动向：2026 年重大转向——主仓库归档为 landing page，开发转移到 **letta-ai/letta-code**（含 agent harness、终端 UI、App Server、runtime）。这一转向本身是重要信号：记忆公司结论是"记忆必须长在 harness 里"，与本项目命题高度一致。
- 取舍：记忆-行为一体、控制力最强；但框架锁定重（必须用 Letta 运行时），做纯记忆层不如 Mem0 轻。

#### Zep / Graphiti（getzep/graphiti）
- ⭐ 约 30K（2026-08；2026 年初约 27K），Apache 2.0（Graphiti 引擎开源，Zep 平台商业）
- 设计：时间感知知识图谱（bi-temporal 双时间线、边失效不删除、episode→实体→社区三层图）；增量实时更新，无需整图重算。自报 DMR 94.8%、LoCoMo 94.7%、LongMemEval 90.2%（平台版）；独立评测中时间类查询表现最强，但图谱异步构建导致新事实入图有延迟。
- 取舍：时间推理与事实演变场景最强、可溯源；代价是图构建成本高、写入路径延迟、部署依赖图数据库。

#### LangMem（langchain-ai/langmem）
- ⭐ 约 1.3-1.6K，MIT
- 设计：LangGraph 原生长期记忆 SDK：核心 memory API（存储后端无关）+ 热路径记忆工具（对话中即时读写）+ 后台 memory manager（会话后异步提取）；显式支持 semantic/episodic/procedural 三型记忆模板。
- 取舍：与 LangGraph checkpointer/store 深度绑定，生态内体验好、生态外锁定强；star 数与投入明显小于前三者。

#### Memobase（memodb-io/memobase）
- ⭐ 约 5-6K（2026-08 检索，二手来源）
- 设计：**画像优先（profile-based）**路线：不存对话流水，而是维护结构化用户画像（预定义 schema 的槽位：基本信息、兴趣、状态等）+ 时间线事件；适合个性化陪伴/消费级应用。
- 取舍：读取成本极低（画像直接注入 prompt）、可控性强；但丢弃细节多，不适合需要精确回溯的 agent 任务。

#### 其它值得记录
- **Cognee**（⭐ 约 12-30K，区间差异来自不同时点）：文档→知识图谱管线（ECL：extract-cognify-load），面向组织知识而非会话记忆。
- **Hindsight**（⭐ 约 4K，增长快）：面向"机构知识"的多策略混合记忆，AMB 独立榜上综合成绩领先（LoCoMo 92.0 / LongMemEval 94.6 / BEAM(10M) 64.1）。
- **SuperMemory**（⭐ 约 29K）：记忆 API + 消费级应用，闭源核心。
- **MemU、ReMe、EverOS** 等 2025-2026 新入场者：分别主打文件式透明记忆、多模态自进化记忆 OS 等叙事。
- 生态观察：MCP 已成记忆互通的事实通道（OpenMemory MCP、agentmemory 等以 MCP server 形态接入任意 harness）；"记忆层"赛道从 2023 年的 2-3 家膨胀到 2026 年的 40+ 架构，且开始与 harness/runtime 融合（Letta 转向、Claude Code auto memory）。

---

## A4 工业界实践

### OpenAI / ChatGPT
- 演进：2024-02 上线 saved memories（显式"记住 X"）；2025 年扩展 chat history reference（隐式引用全部历史）；逆向研究表明记忆以"Model Set Context"等文本块**注入 system prompt**，非推理时检索。2025-11 公开的架构说明：合成记忆状态存于独立数据层、推理时注入。
- **Dreaming V3**（2026-06-04 官宣）：后台进程持续从全部对话历史**合成**记忆状态——新对话被吸收进既有记忆表示、过时信息被重写、随情境变化自适应更新；成为默认记忆底座（saved memories 降为回退），并首次开放免费层。
- 安全面：Tenable 等研究把注入式记忆定性为推理时的 system prompt injection 面；记忆污染（persistent prompt injection via memory）是已被验证的攻击路径。
- 参考实现：社区文档化的 "OpenMemory 模式"（LangGraph + Redis Streams + Qdrant + 异步 worker 做嵌入/去重/信任评分）成为自建 ChatGPT 式记忆的通用蓝图。

### Anthropic / Claude（与本项目 harness 最相关）
- **API memory tool**（2025-10 beta）：客户端文件式记忆——模型通过工具在开发者管理的记忆目录读写文件，跨会话保留；与 context editing（自动清理旧工具结果）配合，官方评测 agentic 搜索任务 +39%。"记忆=文件+工具"的极简设计哲学。
- **Claude.ai Chat Memory**：2025-09 起企业/团队版逐步开放，2026-03-02 全量（含免费层）；每约 24 小时把对话合成进 `userMemories` 文本块注入系统提示，Settings 中可查看/编辑/删除，支持 incognito；较 ChatGPT 更保守——偏"稳定事实抽取"而非持续重写。2026 年还推出 ChatGPT/Gemini 历史导入工具（把记忆作为迁移成本武器）。
- **Claude Dreaming**（2026-05-06，Managed Agents）：agent 空闲时的**离线记忆固结**进程：扫描记忆目录+近期会话转录，删过时、消矛盾、并重复、归一化时间引用、把模式抽取成主题文件；不改权重、全程产出可审计的明文文件。这是"睡眠固结"理念第一次成为正式产品。
- **Claude Code（coding harness 的记忆实践）**：双机制——`CLAUDE.md`（用户手写的持久指令，项目根/用户级/子目录嵌套）+ **auto memory**（`~/.claude/projects/.../MEMORY.md`，agent 根据用户纠正与偏好自写笔记）；两者每会话启动即加载。**Compaction 语义**：上下文将满时自动压缩——从磁盘加载的内容（根 CLAUDE.md、unscoped rules、MEMORY.md）压缩后重新注入，对话内内容只留摘要；嵌套 CLAUDE.md 与 path-scoped rules 懒加载回补。实践准则："必须存活的指令放进根 CLAUDE.md"，即**记忆放置（memory placement）决定持久性**。这是目前最成熟的"文件即记忆 + 固结"harness 范式。

### Google
- **Gemini Personal Intelligence**：路线独特——不重对话记忆而重**生态数据接入**（Gmail/Drive/Calendar/搜索历史即记忆），辅以 Gemini 内的对话记忆开关。
- **Vertex AI Memory Bank**（2025 GA）：面向开发者的托管记忆服务：从会话中按 topic 提取、整合（冲突消解）、按 scope 隔离，与 Agent Engine/ADK 集成——工业界第一个云原生"记忆即服务"。

### 其它 coding harness 的记忆实践
- **OpenAI Codex / AGENTS.md**：OpenAI 主推 `AGENTS.md` 作为跨工具的 agent 指令文件开放标准（2025 起，Codex、Cursor、Gemini CLI 等均支持），角色等同 CLAUDE.md——"给 agent 的 README"。Codex 云端任务另有环境级配置与会话恢复，但截至检索时点未提供 Claude Code auto memory 式的 agent 自写笔记，记忆责任主要留给用户维护 AGENTS.md。
- **Cursor Memories**（2025）：从对话中自动生成记忆条目（规则化的用户偏好/项目约定），入库前经后台"评审"筛选，用户可在设置中管理；本质是"对话→规则文件"的自动固结，与 Claude Code auto memory 同类。
- **Gemini CLI**：`GEMINI.md` 分层指令文件 + `/memory add` 显式记忆命令，跟随 AGENTS.md 生态。
- 共性观察：coding harness 的记忆几乎全部收敛到**明文 Markdown 文件 + 分层加载 + （可选）自动固结**，没有一家采用向量库作为主记忆——与通用助手产品形成鲜明分化。原因：代码场景要求记忆可审计、可版本控制、可随仓库分发。

### 框架与横向观察
- **LangChain/LangGraph**：2024-10 上线跨线程 long-term memory store（JSON 文档 + 命名空间）；2025-02 发布 LangMem SDK；LangGraph checkpointer 负责线程内状态、store 负责跨线程记忆的两层设计被广泛效仿。
- **LlamaIndex**：2025 年重构 Memory 组件为可组合 blocks：static block（固定信息）、fact extraction block（事实抽取）、vector memory block（向量检索），短期+长期统一 API。
- 横向趋势：(1) 记忆成为助手产品的**护城河/切换成本**，各家互不互通，反向催生 MCP 记忆服务器与导入工具；(2) 产品形态收敛为"注入式合成画像（低成本、默认开）+ 工具式检索记忆（agent 场景）"双轨；(3) 2026 年 OpenAI/Anthropic 双双落地"dreaming/离线固结"，工业界与学术界（sleep-time compute、consolidation 立场文）罕见地同步。

---

## 综合分析

### 分类法（taxonomy）
沿四个正交维度组织该领域（综合 Zhang et al. 2024 综述、Du 2026 综述、Wu et al. 2026 统一框架）：
1. **载体形态**：上下文内（KV cache/工作记忆）｜外部明文（扁平向量库 → 分层/树 → 图/时间图 → 文件系统）｜参数化（权重/LoRA/神经记忆模块/fast weights）。
2. **操作环节**：写入（直接归档 vs 摘要提取 vs 图抽取）→ 管理（整合、更新、链接、遗忘、冲突消解、固结）→ 读取（向量/词法/结构检索、调度注入）。四阶段框架（提取/管理/存储/检索）是目前最好用的分解。
3. **内容类型**：用户画像与偏好（个性化）｜情景记忆（事件/轨迹）｜语义记忆（事实/知识）｜**程序性记忆（技能、工作流、环境陷阱）**——最后者对 harness 最关键却研究最少。
4. **管理者**：固定管线（Mem0）｜agent 自管理（MemGPT/A-MEM/Letta）｜学习型（RL：MemAgent/MEM1；测试时训练：Titans/TTT）。

### 主要系统一览（速查表）

| 系统 | 年份 | 存储结构 | 管理方式 | 突出能力 | 主要短板 |
|---|---|---|---|---|---|
| MemGPT/Letta | 2023 | 分层（上下文块+向量归档） | agent 自编辑 | 记忆-行为一体 | 框架锁定、评测饱和 |
| HippoRAG 1/2 | 2024/25 | 知识图谱+PPR | 离线构图+在线过滤 | 多跳关联、单步检索 | 构图成本、对话场景弱 |
| Zep/Graphiti | 2025 | 双时间线知识图谱 | 增量入图+边失效 | 时间推理、事实演变 | 入图延迟、部署重 |
| A-MEM | 2025 | 原子笔记+动态链接 | LLM 链接+记忆进化 | 自组织、低成本 | 链接质量依赖模型 |
| Mem0/Mem0g | 2025 | 扁平向量（+图） | LLM CRUD 管线 | 易集成、token 效率 | 抽取有损、OSS/托管差距 |
| MemOS | 2025 | MemCube（文本/激活/参数） | 调度+生命周期 | 形态转换通路 | 系统复杂、生态早期 |
| MIRIX | 2025 | 六类分区 | 多 agent 路由 | 多模态、类型化 | 组件多、开销大 |
| MemoryOS | 2025 | STM/MTM/LTM 三级 | 分段分页+热度升降 | 对话场景 F1 高 | 面向对话、非 agentic |
| Titans | 2025 | 神经记忆模块（参数） | 测试时梯度更新 | 超长序列、泛化 | 需训练、不可解释 |
| MemAgent/MEM1 | 2025 | 固定长明文（覆写） | RL 学习策略 | 线性复杂度、外推 | 任务特化、需训练 |
| Claude Code | 2025-26 | 明文 Markdown 文件 | 用户手写+agent 自写+离线固结 | 可审计、随仓库分发 | 无检索、规模受限 |

### 2025-2026 趋势
1. **评测重心从"对话回忆"迁到"agent 经验"**：LongMemEval-V2、MemoryArena、Harness the Memory 全部转向 agent 轨迹与"记忆→行动"转化；LoCoMo 类问答基准已近饱和且被刷榜。
2. **效率成为一等指标**：token 足迹、延迟与准确率共同构成前沿（LAFS、MemScore）；"高分但每查询烧 5 万 token"的系统不再被接受。
3. **固结通道成为共识议题**：学术（consolidation 立场文、sleep-time compute、parametric memory 蒸馏）与工业（OpenAI Dreaming V3、Claude Dreaming）同步落地"离线整理/固结"进程；分歧只在固结目标是明文文件（Anthropic）还是持续重写的合成状态（OpenAI）还是参数（研究前沿）。
4. **评测信任危机与中立化**：厂商自报 vs 独立复测差距悬殊，催生 AMB、Bench'd 等第三方平台；复现性成为记忆论文的默认要求。
5. **记忆层与 harness 融合**：Letta 整体转向 harness（letta-code）；Claude Code auto memory 把记忆内建进 coding agent；"独立记忆中间件"与"harness 原生记忆"两条路线开始正面竞争。
6. **图记忆时间化**：bi-temporal、边失效、事实演变追踪从 Zep 特性变成图记忆标配。

### 未解决问题
- **冲突消解与知识更新**：所有基准上最弱的能力项；跨会话身份一致性（同一实体多次出现的对齐）尚无好解。
- **时间抽象**：大规模历史上的相对时间推理（"上上周说的那个方案"）与时间粒度压缩。
- **检索噪声毒性**：agentic 任务中错误检索比不检索更糟（Harness the Memory 的核心发现），何时不读记忆是开放问题。
- **遗忘与记忆膨胀**：无限增长的明文库在成本、延迟、污染审计上均不可持续；主动遗忘策略仍靠启发式。
- **记忆安全**：记忆污染=持久化提示注入；固结管线可能把单次攻击放大为永久损伤；溯源、版本化、回滚机制刚起步。
- **多 agent 共享记忆**：并发读写一致性、权限、租约——数据库共同体刚开始介入（"agent-native memory system"之问）。

### 与 harness（Claude Code/Codex 类执行框架）结合的机会
1. **程序性记忆优先**：Harness the Memory 证明对 coding/具身任务，"经验→紧凑技能包"胜过事实检索；harness 应内建"任务后蒸馏"步骤（类似 Agent Workflow Memory 的工作流归纳），产出可读的 skill/规则文件而非向量库。
2. **文件即记忆 + dream loop**：Claude Code 的 CLAUDE.md/MEMORY.md + Claude Dreaming 的离线固结可组合成完整闭环：会话内自写笔记 → 空闲期整理（去重、消矛盾、模式抽取）→ 下会话注入。全明文、可审计，与 git 天然兼容（记忆可 diff、可 review、可回滚）——这是 harness 场景相对通用记忆中间件的独特优势。
3. **compaction 感知的记忆放置**：harness 掌握"什么会在压缩中幸存"的完整语义，可以做自动记忆放置决策（该进根 CLAUDE.md 还是 path-scoped rule 还是丢弃），这是外部记忆层做不到的。
4. **仓库级时间记忆**：把 Graphiti 式 bi-temporal 思想用于代码库事实（"这个 API 在 v2 后废弃"），解决 coding agent 最常见的过时知识错误。
5. **评测切入**：LongMemEval-V2（环境 gotchas、工作流知识、前提感知五能力）几乎就是为 harness 记忆定制的评测框架，可直接作为本项目实验基准；MemoryArena 的任务间依赖设计可迁移到多次 coding 会话场景。
6. **安全差异化**：harness 内记忆全部落盘为项目文件，可用 hooks/review 门禁审计记忆写入，天然缓解记忆污染——值得作为论文点深挖。

### 与其它分支的接口（供主 session 汇总时对齐）
- **→ 持续学习分支**：Reflexion/ExpeL/AWM/Voyager 等"经验→能力"工作在本分支只记录记忆接口，其学习机制归对方展开；固结通道（明文→参数）是两分支的天然交汇点。
- **→ 上下文工程/harness 机制分支**（如有）：compaction、context editing、渐进披露与记忆放置策略在 A4 已记录事实，设计权衡宜与该分支合并论述。
- **重叠文献提醒**：`raw/papers/` 中 2023-shinn-reflexion、2023-wang-voyager、2024-wang-agent-workflow-memory、2025-fang-memp-procedural-memory 等由并行分支下载，本分支引用时用同一份 PDF，不重复登记。

## 下一层待深挖问题（供 BFS 展开）
1. **程序性/技能记忆专题**：Agent Workflow Memory、Voyager 技能库、skill bundle、Memp 等在 coding harness 的可移植性与评测方案（与分支 B 持续学习交界）。
2. **记忆固结算法**：sleep-time compute、明文→参数蒸馏（Doc-to-LoRA、SSR、MEMIT、TTT layers）、固结时机与安全护栏（provenance、回滚、回归门禁）的具体设计空间。
3. **时间知识图谱机制细节**：Graphiti 的边失效/双时间线实现、增量图更新成本、与轻量文件式记忆的成本-收益边界。
4. **记忆安全与污染**：memory poisoning 攻击面综述（Tenable ChatGPT 研究等）、固结管线的放大风险、审计与隔离机制。
5. **评测方法学**：LAFS/MemScore 类效率-准确率联合指标、AMB 复现协议，以及为"harness 记忆"设计新基准的可行性（本项目潜在论文方向）。
6. **多 agent 共享记忆**：并发一致性、命名空间与权限模型、团队级记忆枢纽（TencentDB Agent Memory、MemPalace 等工业方案）的设计取舍。

---
落款：survey-agent-A · 2026-08-27 11:43
