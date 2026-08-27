# 分支 C 调研底稿：Agent 持续学习（Continual / Lifelong Learning for LLM Agents）

> openspec change-001 · 分支 C · 覆盖 2023-01 ～ 2026-08
> 定位：为 wiki 主题"Harness 的记忆与持续学习"提供 agent 持续学习方向的唯一素材底稿。
> 检索方法：arXiv（https）+ Semantic Scholar API（venue/引用数交叉验证）+ web 搜索（重点补齐 2025-2026）+ GitHub API（star/活跃度，取数日期 2026-08-27）。
> 论文 PDF 均归档于 `raw/papers/`，索引片段见 `raw/papers/index_fragments/C.yaml`。

---

## C0 范围界定与总览

本分支回答一个问题：**LLM agent 如何在不断执行任务的过程中变得更强，同时不忘掉已会的东西**。与分支 A/B（记忆系统本体）的边界是：这里关注"学习闭环"——经验如何被提取、抽象、复用、评测，而非记忆的存取架构本身。

四个子方向：
- **C1 经验积累与技能库**：从执行轨迹中蒸馏可复用的技能/工作流/策略；
- **C2 在线学习与测试时适应**：部署后持续适应，包括基于记忆的在线学习与参数化的 test-time training；
- **C3 灾难性遗忘与知识保持**：LLM 持续学习（参数化）与 agent 场景（非参数化为主）的交叉对比；
- **C4 基准评测与开源实现**：lifelong agent benchmark、评测协议与代码生态。

一条贯穿 2023-2026 的主线：**从"存储轨迹"到"反思轨迹"再到"抽象经验"**（Storage → Reflection → Experience，见 ACL 2026 Findings 综述 [From Storage to Experience](https://aclanthology.org/2026.findings-acl.2069.pdf)）；实现手段上从参数更新全面转向**训练无关（training-free）的上下文与外部记忆演化**，2026 年参数化 test-time training 有回潮迹象，形成三足鼎立格局。

**关键工作时间线（本分支视角）**：

| 时间 | 工作 | 里程碑意义 |
|---|---|---|
| 2023-03 | Reflexion | 言语强化学习：失败→文本教训，episode 内自我改进 |
| 2023-05 | Voyager | 技能=经验证代码，终身技能库范式确立 |
| 2023-08 | ExpeL | 跨任务经验蒸馏（insights+成功轨迹），无梯度学习成立 |
| 2023-10 | CLIN | 因果抽象记忆，记忆表示形式决定迁移能力 |
| 2024-04 | CL-of-LLMs 综述 | 参数化持续学习地图定型（CSUR） |
| 2024-06 | StreamBench | 首个流式在线改进基准（NeurIPS 2024） |
| 2024-09 | AWM | 工作流归纳，离线+在线双模式（ICML 2025） |
| 2024-11 | TTT for ARC | 参数化测试时训练回潮的信号弹 |
| 2025-04 | Dynamic Cheatsheet / SkillWeaver | 自编辑记忆；技能 API 化+验证流程 |
| 2025-05 | LifelongAgentBench | 首个 lifelong agent 统一基准；经验回放负结果 |
| 2025-08 | Memp / Memento / 自进化综述×2 | 程序性记忆设计空间；M-MDP 在线学习；领域成型 |
| 2025-09 | ReasoningBank+MaTTS | 失败入库；"记忆×测试算力"新扩展维度 |
| 2025-10 | ACE | 防坍缩增量 playbook，上下文轴当前最佳实践 |
| 2026 上半年 | MemSkill / MUSE / 三篇技能综述 / Panini | 元技能；生命周期工程化；NPCL 理论化；SKILL.md 入学术议程 |

---

## C1 经验积累与技能库

### C1.1 Voyager: An Open-Ended Embodied Agent with Large Language Models
- **作者/年份/venue**：Guanzhi Wang et al. · 2023 · TMLR（arXiv 2023-05）
- **链接**：https://arxiv.org/abs/2305.16291 · [GitHub MineDojo/Voyager](https://github.com/MineDojo/Voyager)（7160 stars，最近推送 2024-04，已停止维护但影响深远）
- **PDF**：`raw/papers/2023-wang-voyager.pdf`
- **摘要**：首个在 Minecraft 中进行终身学习的 LLM agent，三大组件：自动课程（automatic curriculum）、**以可执行代码为载体的技能库**（skill library，用描述的 embedding 做检索）、迭代提示机制（环境反馈+执行错误+自我验证三路信号迭代改进程序）。获得独特物品数量为此前 SOTA 的 3.3 倍，且技能库可迁移到新世界。它确立了"**技能=经过验证的代码+自然语言描述索引**"这一范式——这正是后来 Claude Code Skills（SKILL.md + 脚本）的学术原型，对 harness 的意义是：agent 的持续学习产物可以直接落盘为代码资产，而非模型权重。（引用数 2186，为本分支被引最高工作。）

### C1.2 ExpeL: LLM Agents Are Experiential Learners
- **作者/年份/venue**：Andrew Zhao et al. · 2023 · AAAI 2024
- **链接**：https://arxiv.org/abs/2308.10144 · [GitHub LeapLabTHU/ExpeL](https://github.com/LeapLabTHU/ExpeL)（237 stars，最近推送 2024-12）
- **PDF**：`raw/papers/2023-zhao-expel.pdf`
- **摘要**：提出"经验蒸馏"两阶段范式：训练期让 agent 用 Reflexion 式重试收集成败轨迹，然后**用 LLM 从轨迹对比中归纳自然语言 insights**（可增、可改、可投票强化、可删），推理期同时检索"成功轨迹作为 few-shot 示例"+"insights 作为规则"注入 prompt。在 HotpotQA、ALFWorld、WebShop 上超过 ReAct/Reflexion，且展示了跨任务正迁移。意义：证明**无梯度的经验学习可行**，其"insight 提取+计数器投票"机制被 ACE 等 2025 年工作直接继承；对 harness 而言，这是"从会话日志自动生成 CLAUDE.md 规则"的理论依据。（引用 836。）

### C1.3 Agent Workflow Memory（AWM）
- **作者/年份/venue**：Zora Zhiruo Wang, Jiayuan Mao, Daniel Fried, Graham Neubig · 2024 · ICML 2025
- **链接**：https://arxiv.org/abs/2409.07429 · [GitHub zorazrw/agent-workflow-memory](https://github.com/zorazrw/agent-workflow-memory)（461 stars，最近推送 2025-12）
- **PDF**：`raw/papers/2024-wang-agent-workflow-memory.pdf`
- **摘要**：从 agent 轨迹中归纳**工作流（workflow）**——一段带目标描述的常用子例程（比 Voyager 的代码技能更抽象、比 ExpeL 的规则更结构化），并支持离线（从训练集归纳）与**在线（从自身测试时轨迹持续归纳）**两种模式。Mind2Web 相对提升 24.6%、WebArena 相对提升 51.1%，且在线模式无需标注即可随任务流持续变强。意义：workflow 是"技能"的轻量文本形态，在线归纳模式就是 harness 场景下"边干活边沉淀 SOP"的直接蓝本。（引用 245。）

### C1.4 Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory
- **作者/年份/venue**：Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, James Zou · 2025 · arXiv 2025-04（后收录于 EACL）
- **链接**：https://arxiv.org/abs/2504.07952 · [GitHub suzgunmirac/dynamic-cheatsheet](https://github.com/suzgunmirac/dynamic-cheatsheet)（276 stars，最近推送 2026-03）
- **PDF**：`raw/papers/2025-suzgun-dynamic-cheatsheet.pdf`
- **摘要**：给黑盒 LLM 挂一个**自编辑的"小抄"外部记忆**：推理时不断把可复用的策略、代码片段、教训写入/改写 cheatsheet，供后续查询复用；提供累积式（DC-Cu）与检索式（DC-RS）两种变体。GPT-4o 在 AIME 上翻倍，Claude 3.5 Sonnet 在 24 点游戏上提升超 2 倍，均不更新任何参数。意义：证明**单个不断改写的文本记忆就能带来测试时持续学习**，是 ACE 的直接前身（ACE 论文明言 building on Dynamic Cheatsheet）；也暴露了整体改写会丢信息的问题（见 C1.5）。（引用 106。）

### C1.5 ACE: Agentic Context Engineering
- **作者/年份/venue**：Qizheng Zhang et al.（Stanford + SambaNova + UC Berkeley）· 2025 · arXiv 2025-10
- **链接**：https://arxiv.org/abs/2510.04618 · [GitHub ace-agent/ace](https://github.com/ace-agent/ace)（1275 stars，最近推送 2026-08-24，**高度活跃**）
- **PDF**：`raw/papers/2025-zhang-ace.pdf`
- **摘要**：指出上下文自适应两大失败模式——**brevity bias**（迭代摘要丢领域细节）与 **context collapse**（整体重写导致记忆坍缩退化），提出把上下文当作"**演化中的 playbook**"：Generator 产生轨迹、Reflector 提炼成败教训、Curator 生成**增量 delta 条目**（带 helpful/harmful 计数器）做确定性合并、去重、修剪，只增改不重写。Agent 任务 +10.6%（AppWorld 上以小开源模型追平 GPT-4.1 生产级 agent）、金融推理 +8.6%，适应延迟降 86.9%，可仅凭执行反馈无监督运行。意义：这是目前**与 harness 工程形态最接近的持续学习方案**——playbook 即 CLAUDE.md/规则文件，delta 更新即受控的配置修改，直接可移植。（引用 269，发布不到一年。）

### C1.6 SkillWeaver: Web Agents can Self-Improve by Discovering and Honing Skills
- **作者/年份/venue**：Boyuan Zheng et al.（OSU）· 2025 · arXiv 2025-04
- **链接**：https://arxiv.org/abs/2504.07079 · [GitHub OSU-NLP-Group/SkillWeaver](https://github.com/OSU-NLP-Group/SkillWeaver)（154 stars，最近推送 2025-04）
- **PDF**：`raw/papers/2025-zheng-skillweaver.pdf`
- **摘要**：web agent 在新网站上**自主探索→提出技能→反复练习→蒸馏为经过测试的 API**（含合成测试与调试），迭代扩张即插即用的 API 库。WebArena 相对提升 31.8%、真实网站 39.8%；**强 agent 合成的 API 给弱 agent 用可提升至多 54.3%**，证明技能资产可跨模型迁移。意义：把 Voyager 的代码技能范式落到实用 web 场景，并给出"练习+测试+调试"的技能质量保障流程——对应 harness 中"skill 必须带验证脚本"的工程要求。（引用 118。）

### C1.7 Memp: Exploring Agent Procedural Memory
- **作者/年份/venue**：Runnan Fang et al.（浙大 + 阿里通义）· 2025 · arXiv 2025-08（后收录于 ACL）
- **链接**：https://arxiv.org/abs/2508.06433 · [GitHub zjunlp/Memp](https://github.com/zjunlp/Memp)（35 stars，最近推送 2026-01）
- **PDF**：`raw/papers/2025-fang-memp.pdf`（另有兄弟分支归档的同文件 `2025-fang-memp-procedural-memory.pdf`）
- **摘要**：系统研究 agent **程序性记忆（procedural memory）**的构建、检索与更新三元设计空间：把历史轨迹蒸馏成细粒度步骤脚本与更高层的脚本式抽象，并比较增/删/改等多种记忆更新策略对任务流性能的影响。在 TravelPlanner、ALFWorld 上，随记忆库演化成功率与效率同步上升；强模型构建的程序性记忆迁移给弱模型仍显著涨点。意义：给"该存什么粒度、何时更新、何时废弃"这一 harness 记忆设计核心问题提供了首个受控实验。（引用 62。）

### C1.8 MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents
- **作者/年份/venue**：Haozhen Zhang, Quanyu Long, Jianzhu Bao, Tao Feng et al. · 2026 · arXiv 2026-02
- **链接**：https://arxiv.org/abs/2602.02474 · [GitHub ViktorAxelsen/MemSkill](https://github.com/ViktorAxelsen/MemSkill)（565 stars，最近推送 2026-05，活跃）
- **PDF**：`raw/papers/2026-zhang-memskill.pdf`
- **摘要**：把**记忆操作本身**重构为可演化的技能库（meta-memory）：controller 学习为每个上下文片段挑选少量相关"记忆技能"，条件化地构建记忆；designer 周期性从困难样例中**改进既有技能并提出新技能**，形成闭环训练。在 LoCoMo、LongMemEval、HotpotQA、ALFWorld 上稳定超过强基线。意义：代表 2026 年新方向——不仅学"记住什么"，还学"**如何记**"；harness 可类比为让 agent 自动演化自己的记忆写入策略（如何时写 memory 文件、写什么摘要）。

### C1.9 本节其他值得记录的工作（未下载 PDF，仅登记链接）
- **Reflexion**（Shinn et al. 2023, NeurIPS 2023, https://arxiv.org/abs/2303.11366）：episode 内的言语强化学习，是 ExpeL/ACE 等一切"从失败中提炼文本教训"的方法论源头。PDF 已由兄弟分支归档：`raw/papers/2023-shinn-reflexion.pdf`。
- **MUSE-Autoskill**（2026, https://arxiv.org/abs/2605.27366）：提出技能五阶段统一生命周期——创建、记忆、管理、评估、精炼，把技能从一次性产物升级为"被管理、可测试、可迁移的基础设施"，在 Skills Bench 上验证。
- **A Comprehensive Survey on Agent Skills**（2026, https://arxiv.org/abs/2605.07358）：按表示/获取/检索/演化四阶段组织技能文献，明确指出技能区别于工具与 MCP server 之处在于**编码了情境化程序知识（触发条件、步骤顺序、坑）**，并盘点 SkillNet、ClawHub、SkillsMP 等技能分发平台——直接对应 Claude Code Skills 生态。
- **Dynamic Agent Skills: A Lifecycle Survey**（2026, https://arxiv.org/abs/2607.10113）：对 2023-2026 共 124 篇文献的审计式综述，给出八阶段生命周期（证据获取→提议→验证/准入→存储→检索/组合→维护→蒸馏/移植→治理）与十算子词表；明确把 SKILL.md 包列为技能载体之一。是 C1 方向最新、最工程化的地图。

---

## C2 在线学习与测试时适应

### C2.1 Memento: Fine-tuning LLM Agents without Fine-tuning LLMs
- **作者/年份/venue**：Huichi Zhou, Yihang Chen, Siyuan Guo, Xue Yan et al.（UCL + 华为等）· 2025 · arXiv 2025-08
- **链接**：https://arxiv.org/abs/2508.16153 · [GitHub Agent-on-the-Fly/Memento](https://github.com/Agent-on-the-Fly/Memento)（2569 stars，最近推送 2025-10）
- **PDF**：`raw/papers/2025-zhou-memento.pdf`
- **摘要**：把持续适应形式化为**记忆增广 MDP（M-MDP）+ 基于案例推理（CBR）**：情节记忆存过往轨迹（case bank），一个轻量神经案例选择策略通过环境反馈在线更新（记忆重写=策略更新，记忆读取=策略改进），底座 LLM 完全冻结。深研场景下 GAIA 验证集 87.88% Pass@3（当时 top-1）、测试集 79.40%；案例记忆在分布外任务上带来 4.7-9.6 个绝对点。意义：给"基于记忆的在线强化学习"提供了干净的形式化——**梯度只流经记忆选择器，不碰基座**，是 harness 可直接借用的低成本在线学习架构。（引用 95。）

### C2.2 ReasoningBank + MaTTS: Scaling Agent Self-Evolving with Reasoning Memory
- **作者/年份/venue**：Siru Ouyang, Jun Yan, I-Hung Hsu, Yanfei Chen et al.（UIUC + Google Cloud AI Research）· 2025 · arXiv 2025-09
- **链接**：https://arxiv.org/abs/2509.25140
- **PDF**：`raw/papers/2025-ouyang-reasoningbank.pdf`
- **摘要**：从 agent **自判的成功与失败**轨迹中同时蒸馏"策略级推理记忆"（而非存原始轨迹或仅存成功例程），测试时检索注入、用后回写；进一步提出**记忆感知的测试时扩展 MaTTS**——并行（多轨迹自对比）与串行（迭代精炼）两种方式放大经验多样性，为记忆萃取提供对比信号，记忆又反过来让扩展更有效，形成"记忆×算力"协同。在 WebArena、Mind2Web、SWE-Bench-Verified 上一致超过轨迹存储与成功例程基线，且减少冗余探索步数。意义：提出"**经验驱动的扩展是继模型/数据/测试算力之后的新扩展维度**"，failure-aware 蒸馏与 SWE 场景验证对 coding harness 尤其相关。（引用 180，发布一年内。）

### C2.3 CLIN: A Continually Learning Language Agent
- **作者/年份/venue**：Bodhisattwa Prasad Majumder et al.（AI2）· 2023 · arXiv 2023-10
- **链接**：https://arxiv.org/abs/2310.10134 · [GitHub allenai/clin](https://github.com/allenai/clin)（89 stars，最近推送 2023-12）
- **PDF**：`raw/papers/2023-majumder-clin.pdf`
- **摘要**：首批明确以"持续学习"为题的语言 agent：维护一个**因果抽象记忆**（"X may be necessary for Y"形式的模式），每次 trial 后重写，无需参数更新即可跨 trial、跨环境、跨任务快速适应，在 ScienceWorld 上超过 Reflexion。意义：证明记忆内容的**表示形式**（因果关系 vs 原始轨迹）决定迁移能力，是"经验抽象层级"研究的早期锚点。（引用 96。）

### C2.4 参数化路线：Test-Time Training / 测试时微调
- **The Surprising Effectiveness of Test-Time Training for Abstract Reasoning**（Akyürek et al. 2024, https://arxiv.org/abs/2411.07279）：推理时用目标任务的少量示例做 LoRA 微调，ARC 公开集达 61.9%（接近人类平均），证明**临时参数更新**可解锁 ICL 做不到的抽象推理。
- **Learning to (Learn at Test Time): RNNs with Expressive Hidden States**（Sun et al. 2024, https://arxiv.org/abs/2407.04620）：TTT 层把隐状态本身变成一个在测试序列上持续做自监督更新的小模型，把"测试时学习"下沉到架构层。
- 与 C2.1/C2.2 的非参数路线相比：TTT 收益集中在"任务分布内的快速特化"，但带来单实例训练成本、多阶段后训练对齐被破坏、以及遗忘风险（见 C3）；agent 场景 2025-2026 主流仍是非参数记忆，但 **Panini（C3.3）等 2026 工作已开始论证两者互补**。

### C2.5 经验回放在 agent 场景的实证结论
- LifelongAgentBench（C4.1）的系统实验给出重要负结果：**朴素经验回放（把历史成功轨迹塞回上下文）收益有限甚至有害**——无关信息干扰与上下文长度约束是主因；其 group self-consistency（把历史经验分组、各组独立生成再投票）显著改善。
- StreamBench（C4.2）从另一侧印证：只回放**自我生成且被证实正确**的例子，就是极强的廉价基线——回放的关键不在"量"而在"筛选"。
- 对 harness 的启示：直接"回放会话历史"不是有效的持续学习；必须有抽象/筛选层（正呼应 C1 的经验蒸馏路线）。

### C2.6 自进化 agent 综述（领域成型的标志，2025-08 两篇同期）
- **A Comprehensive Survey of Self-Evolving AI Agents: A New Paradigm Bridging Foundation Models and Lifelong Agentic Systems**（Jinyuan Fang et al. · 2025 · https://arxiv.org/abs/2508.07407 · PDF：`raw/papers/2025-fang-self-evolving-ai-agents-survey.pdf`，由兄弟分支归档）：提出"系统输入-Agent 系统-环境-优化器"四组件反馈环统一框架，按被优化对象（基座模型/prompt/记忆/工具/工作流/多 agent 通信）系统分类自进化技术，划分 MOP→MOA→MAO→MASE 四代范式，并提出 Endure/Excel/Evolve 三定律（安全、保性能、自主进化）。其"测试时行为优化"一节把外部反馈引导与多候选+验证器两条路线统一起来，是 C2 方向的理论骨架。（引用 172。）
- **A Survey of Self-Evolving Agents: On Path to Artificial Super Intelligence**（Huan-ang Gao et al. · 2025 · https://arxiv.org/abs/2507.21046 · PDF：`raw/papers/2025-gao-self-evolving-agents-survey.pdf`，由兄弟分支归档）：按"进化什么（模型/上下文/工具/架构）、何时进化（测试时/测试间）、如何进化（奖励/模仿/群体）"三问组织文献，与 Fang 综述互补，明确把 lifelong learning 列为自进化的目标状态。
- 两篇综述共同结论：当前系统只能优化 prompt/记忆等外围组件，距"真正自主进化"尚远；**缺少衡量"进化成功"的稳健基准**（呼应 C4）；进化必须受控，否则漂移与退化不可避免。

---

## C3 灾难性遗忘与知识保持

### C3.1 Continual Learning of Large Language Models: A Comprehensive Survey
- **作者/年份/venue**：Haizhou Shi et al.（Rutgers）· 2024 · ACM Computing Surveys（arXiv 2404.16789，持续更新至 v4）
- **链接**：https://arxiv.org/abs/2404.16789 · [GitHub Wang-ML-Lab/llm-continual-learning-survey](https://github.com/Wang-ML-Lab/llm-continual-learning-survey)
- **PDF**：`raw/papers/2024-shi-llm-continual-learning-survey.pdf`
- **摘要**：LLM 持续学习最系统的综述：提出**纵向连续性**（通用→领域→任务的能力下沉）与**横向连续性**（时间/分布漂移）双维框架，按持续预训练（CPT）、领域适应（DAP）、持续微调（CFT）三阶段组织方法，覆盖 replay/正则化/架构三大遗忘缓解家族及其在 LLM 尺度上的适配。意义：为 C 分支提供参数化路线的完整地图与术语基线（stability-plasticity 权衡、forward/backward transfer 度量），是对比非参数 agent 方法时的参照系。（引用 329。）

### C3.2 Continual Learning in LLMs: Methods, Challenges, and Opportunities（2026 综述）
- **作者/年份/venue**：2026 · arXiv 2026-03
- **链接**：https://arxiv.org/abs/2603.12658
- **摘要**：按持续预训练/持续微调/**持续对齐**三训练阶段重组 CL 方法学，并单列**半参数（semi-parametric）方法**为新兴类别——参数更新与非参数记忆结合，用外部记忆模块、检索增强或 agent 架构选择性召回旧知识而不覆写参数。明确指出灾难性遗忘、跨任务知识迁移不足仍是根本挑战。意义：官方确认了"agent 外部记忆"已被 CL 社区收编为遗忘缓解的一等公民路线。

### C3.3 Panini: Continual Learning in Token Space via Structured Memory
- **作者/年份/venue**：2026 · arXiv 2026-02
- **链接**：https://arxiv.org/abs/2602.15156
- **摘要**：针对参数化持续学习（PCL）三大痛点——反复训练开销、灾难性遗忘、破坏多阶段后训练对齐（且无可靠方法在持续训练后恢复指令遵循），提出**非参数持续学习（NPCL）**：基座冻结，新知识以结构化记忆存于 token 空间，同时对抗长上下文的 lost-in-the-middle 与 context rot。意义：给出了"为什么 agent 场景选非参数"的最完整论证清单，可直接引用于 wiki 的路线对比页。

### C3.4 半参数折中：MoNIM（Learn to Memorize）
- **作者/年份/venue**：ACL 2025 长文
- **链接**：https://aclanthology.org/2025.acl-long.1385/
- **摘要**：混合近邻归纳记忆（Mixture-of-Neighbors Induction Memory）把可学习的 replay 记忆挂在冻结 LM 外侧，在流式新闻数据上持续学习：新知识 PPL 大幅下降的同时，旧测试集 PPL 几乎不退化（因为从不擦除旧记忆），优于 RecAdam、Mix-Review 等经典 CL 基线。意义：半参数路线的代表实证——**把"遗忘"问题转化为"记忆容量与检索"问题**。

### C3.5 参数化 vs 非参数化：本分支的对比结论
| 维度 | 参数化（CPT/CFT/TTT） | 非参数化（上下文/外部记忆） | 半参数 |
|---|---|---|---|
| 遗忘 | 灾难性遗忘核心风险；对齐能力也会被冲掉 | 无参数遗忘，但有**检索退化/上下文干扰**（"检索时代的遗忘"变体） | 记忆不擦除，遗忘转为容量管理 |
| 成本 | 每次更新需训练；API 模型不可行 | 近零训练成本；推理时上下文变长 | 中等 |
| 即时性 | 批量、滞后 | 单任务级即时生效（test-time） | 即时写入 |
| 可解释/可回滚 | 差 | **好（文本/代码资产，可 diff、可版本化）** | 中 |
| 能力上限 | 可改变模型内在能力 | 受限于基座 ICL 能力与上下文预算 | 取决于耦合设计 |
| agent 场景现状 | 少数（TTT 回潮中） | **2023-2026 绝对主流** | 2026 起上升 |

关键交叉发现：agent 的非参数记忆同样面临"遗忘"的镜像问题——ACE 指出的 **context collapse**（重写丢失）、LifelongAgentBench 的**无关经验干扰**、Panini 引的 **context rot**，本质都是非参数系统的稳定性-可塑性权衡。"灾难性遗忘"没有消失，而是换了形态。

### C3.6 与 agent 场景直接相关的两个衍生议题
- **对齐/安全能力的遗忘**：2025-2026 的一支文献把"微调后安全护栏退化"显式建模为灾难性遗忘的特例，并用 CL 工具箱（正则化、replay、模型合并）做缓解实验。对计划做参数化巩固的 harness 而言，这意味着每轮持续训练后都需重跑安全评测，成本不可忽略——又一个支持非参数路线的论据。
- **知识编辑（knowledge editing）与 CL 的合流**：定点改权重（ROME/MEMIT 系）曾被视为轻量替代，但连续多次编辑会累积损伤模型通用能力，2025 年后共识是编辑不适合作为持续学习的主机制，仅适合少量事实修正；程序性知识（怎么做）几乎无法用编辑注入，只能走 C1 的技能/经验路线。

---

## C4 基准评测与开源实现

### C4.1 LifelongAgentBench: Evaluating LLM Agents as Lifelong Learners
- **作者/年份/venue**：Junhao Zheng, Xidi Cai et al.（华南理工等）· 2025 · arXiv 2025-05
- **链接**：https://arxiv.org/abs/2505.11942 · 项目页 https://caixd-220529.github.io/LifelongAgentBench/ · [GitHub caixd-220529/LifelongAgentBench](https://github.com/caixd-220529/LifelongAgentBench)（97 stars，最近推送 2025-05）
- **PDF**：`raw/papers/2025-zheng-lifelongagentbench.pdf`
- **摘要**：首个统一的 LLM agent 终身学习基准：Database / OS / Knowledge Graph 三个交互环境，任务**技能锚定且相互依赖**（前序技能是后序任务的组件），带自动标签校验、可复现性与模块化扩展。核心实证：常规经验回放受无关信息与上下文长度限制、收益不稳；提出 group self-consistency（历史轨迹分组+投票）显著提升各基座的终身学习表现。意义：C 分支评测协议的事实起点；其"技能依赖任务流"设计正是 harness 真实工作负载（后续任务依赖此前沉淀）的抽象。（引用 47。）

### C4.2 StreamBench: Towards Benchmarking Continuous Improvement of Language Agents
- **作者/年份/venue**：Cheng-Kuang Wu, Zhi Rui Tam, Chieh-Yen Lin, Yun-Nung Chen 等（台大 + Appier）· 2024 · NeurIPS 2024 Datasets & Benchmarks
- **链接**：https://arxiv.org/abs/2406.08747 · [GitHub stream-bench/stream-bench](https://github.com/stream-bench/stream-bench)（85 stars，最近推送 2024-10）
- **PDF**：`raw/papers/2024-wu-streambench.pdf`
- **摘要**：首个评测"部署后在**输入-反馈流**上持续改进"的基准：覆盖 text-to-SQL、Python 编程、医疗诊断等多任务序列，反馈仅为正误信号，考察 agent 在流上的累积提升；系统比较记忆增长、检索、自我反思等无梯度改进组件。重要发现：**简单而廉价的组合（如仅回放自我生成的正确例）常胜过复杂方法**。意义：确立了"在线流式评测"协议（区别于静态基准），其"编程任务流"设定与 harness 的日常使用模式同构。（引用 44。）

### C4.3 MemoryAgentBench: Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions
- **作者/年份/venue**：Yuanzhe Hu, Yu Wang, Julian McAuley（UCSD）· 2025 · arXiv 2025-07
- **链接**：https://arxiv.org/abs/2507.05257 · [GitHub HUST-AI-HYZ/MemoryAgentBench](https://github.com/HUST-AI-HYZ/MemoryAgentBench)
- **摘要**：把记忆 agent 的能力拆成四项——精确检索、**测试时学习**、长程理解、冲突消解，用增量多轮交互喂入语料评测商用与开源记忆系统（Mem0、MemGPT 类、RAG 组合等）。结论：**没有任何现有方法四项全优**，测试时学习与冲突消解是普遍短板。意义：其中"测试时学习"子项是 C2 方向的专用量尺；冲突消解对应 harness 中"新经验与旧规则打架"的真实痛点。（PDF 未入库，为分支 B 相交条目，此处只登记链接。）

### C4.4 其他基准与协议（简条目）
- **Skills Bench / SkillLearnBench / SkillRet**（2026，见 MUSE-Autoskill 与技能生命周期综述引用）：分别测"带技能库的端到端任务成功率"（Docker 评测的真实任务）、"任务流上的持续技能获取"、"从 1.8 万社区技能中检索"的能力。值得注意的结论：**单一强方法在持续技能获取上并不稳定占优**，系统级设计（生命周期管理）更重要。
- **评测度量迁移**：经典 CL 的 forward/backward transfer 与遗忘率度量正在被改造为 agent 版本——任务流上的成功率斜率（学习速度）、旧技能保持率、跨环境迁移增益（如 SkillWeaver 的强→弱迁移 +54.3%）。协议尚未统一，属开放问题。

### C4.6 评测协议要点归纳（为本项目后续 qa/评测设计备用）
1. **任务组织**：静态集合（传统）→ 有序任务流（StreamBench）→ 带技能依赖图的任务流（LifelongAgentBench）。依赖图设计决定了"复用旧技能"是否真的被考到。
2. **反馈信号**：全监督标签 → 仅正误反馈（StreamBench）→ 无监督自判（ReasoningBank/ACE 的部署设定）。信号越弱越接近 harness 真实环境，也越考验经验质量控制。
3. **必测四件套**（综合各基准）：a) 流上累积成功率及其斜率；b) 回访旧任务的保持率（backward transfer）；c) 新环境零样本迁移（技能资产保值度）；d) 成本曲线（token/延迟随经验库增长的变化）——d 项目前只有 ACE 与 ReasoningBank 认真报告。
4. **常见坑**：任务顺序单一（应做多序随机化）；自判成功率与真实成功率的偏差未报告；记忆库初始化不公平（有的方法暗带人工种子经验）。

### C4.5 开源实现速览（star 数与活跃度截至 2026-08-27）
| 项目 | 方向 | stars | 最近推送 | 备注 |
|---|---|---|---|---|
| [MineDojo/Voyager](https://github.com/MineDojo/Voyager) | 代码技能库 | 7160 | 2024-04 | 范式源头，已停更 |
| [Agent-on-the-Fly/Memento](https://github.com/Agent-on-the-Fly/Memento) | 案例库在线 RL | 2569 | 2025-10 | 深研 agent，社区热 |
| [ace-agent/ace](https://github.com/ace-agent/ace) | playbook 增量演化 | 1275 | 2026-08 | **当前最活跃** |
| [ViktorAxelsen/MemSkill](https://github.com/ViktorAxelsen/MemSkill) | 记忆技能演化 | 565 | 2026-05 | 2026 新范式 |
| [zorazrw/agent-workflow-memory](https://github.com/zorazrw/agent-workflow-memory) | 工作流归纳 | 461 | 2025-12 | 轻量易移植 |
| [suzgunmirac/dynamic-cheatsheet](https://github.com/suzgunmirac/dynamic-cheatsheet) | 自编辑小抄 | 276 | 2026-03 | 单文件记忆 |
| [LeapLabTHU/ExpeL](https://github.com/LeapLabTHU/ExpeL) | 经验蒸馏 | 237 | 2024-12 | 教科书实现 |
| [OSU-NLP-Group/SkillWeaver](https://github.com/OSU-NLP-Group/SkillWeaver) | web 技能 API | 154 | 2025-04 | 带技能验证流程 |
| [caixd-220529/LifelongAgentBench](https://github.com/caixd-220529/LifelongAgentBench) | 基准 | 97 | 2025-05 | C4 首选基准 |
| [allenai/clin](https://github.com/allenai/clin) | 因果记忆 | 89 | 2023-12 | 历史参考 |
| [stream-bench/stream-bench](https://github.com/stream-bench/stream-bench) | 流式基准 | 85 | 2024-10 | 在线协议 |
| [zjunlp/Memp](https://github.com/zjunlp/Memp) | 程序性记忆 | 35 | 2026-01 | 设计空间实验 |

---

## 综合分析

### 1. 分类法：agent 持续学习的三条实现轴
1. **参数轴**（改权重）：CPT/CFT/PEFT、TTT（Akyürek 2024）、TTT 层（Sun 2024）。优点是真正改变能力上限；代价是训练成本、遗忘、对齐破坏，且对 API 模型不可用。agent 场景中 2023-2025 几乎缺席，2026 随开源强模型与低成本 LoRA 出现回潮。
2. **上下文轴**（改 prompt/playbook，单一活跃文本）：Dynamic Cheatsheet → ACE 的演进线，加上 AWM 在线模式。本质是把"策略"维护成一份持续编辑的文档，核心技术问题是**防坍缩的增量更新协议**（ACE 的 delta + 计数器是当前最佳答案）。
3. **外部记忆轴**（结构化库+检索）：按抽象层级递增——原始轨迹（回放，已被证伪为弱基线）→ 案例（Memento）→ 因果模式（CLIN）→ 工作流（AWM）→ 策略记忆（ReasoningBank）→ 可执行技能（Voyager/SkillWeaver）→ 程序性脚本（Memp）→ **元技能：记忆操作本身**（MemSkill）。抽象层级越高，迁移性越强、但蒸馏难度与出错风险越大。

三轴正在合流为"**半参数**"设计（C3.2/C3.4）：外部库承担事实与程序知识，偶发的参数更新承担能力内化——这与人类"陈述性/程序性记忆 + 睡眠巩固"的类比在多篇 2026 文献中反复出现。

### 2. 2025-2026 趋势
- **从存储到经验**：社区共识已从"更大的记忆"转向"更高信息密度的抽象"（storage → reflection → experience 三段论）。
- **失败经验入库**：ReasoningBank/ACE 证明从失败中蒸馏与成功同等重要，纯"成功例程库"已过时。
- **记忆×测试时算力协同**：MaTTS 把经验积累确立为新的 scaling 维度，"多花推理算力→更好经验→更省算力"的正循环是 2026 热点。
- **技能生命周期工程化**：2026 出现三篇技能综述 + Skills Bench 系基准，验证/准入/修剪/治理成为标准阶段；SKILL.md 等 harness 原生格式被学术界正式收编为研究对象——**工业实践（Claude Code Skills、ClawHub）正在反哺学术议程**。
- **评测从静态转向流式**：StreamBench → LifelongAgentBench → SkillLearnBench，任务依赖与在线协议成为标配；但 coding harness 场景（SWE 任务流）仍无专用 lifelong 基准。
- **非参数系统的"遗忘"被重新定义**：context collapse、无关经验干扰、context rot 构成新的稳定性-可塑性研究议程。

### 3. 未解决问题
1. **经验质量与污染**：自判成败会引入错误经验，错误一旦入库会自我强化；缺少可靠的经验验证、置信度标注与溯源机制。
2. **非参数遗忘/容量管理**：库无限增长后的检索退化、冗余与冲突；何时删、删什么（Memp 初步触及，无定论）。
3. **冲突消解**：新经验与旧规则矛盾时的仲裁（MemoryAgentBench 显示为普遍短板）。
4. **跨模型/跨环境可迁移性**：技能资产随基座升级是否保值（SkillWeaver 给出正面证据但仅限 web）。
5. **参数 vs 非参数的边界条件**：什么时候值得把经验"蒸进"权重，缺乏成本-收益的定量刻画。
6. **评测碎片化**：forward/backward transfer 等 CL 度量尚未在 agent 基准间统一；自判成功率与真实成功率的偏差未被系统度量。

### 4. 与 harness（Claude Code / Codex 类执行框架）结合的机会
- **现成对应物**：CLAUDE.md/AGENTS.md ≈ ACE 的 playbook；Skills（SKILL.md+脚本）≈ Voyager/SkillWeaver 的验证技能库；会话轨迹/终端日志 ≈ ExpeL 的经验原料。harness 已具备全部"器官"，缺的是**自动化学习闭环**。
- **机会 1：轨迹→经验的离线蒸馏管线**。夜间批处理会话日志，ExpeL/ReasoningBank 式双向（成败）蒸馏出 delta 规则，经 ACE 式计数器与人工抽检准入后合入 CLAUDE.md——git 提供天然的版本化、diff 审查与回滚，正好补齐学术工作缺失的治理层。
- **机会 2：技能自动铸造**。对重复出现的工作流（AWM 归纳）自动生成 SKILL.md+验证脚本（SkillWeaver 的练习-测试-调试流程），入库前跑 qa agent 验证——与本项目多 agent 架构（develop/qa/review）天然契合。
- **机会 3：面向 coding harness 的 lifelong 基准**。SWE 任务流 + 技能依赖 + 流式协议（LifelongAgentBench × SWE-Bench 杂交）目前是空白，可发表。
- **机会 4：记忆策略的元学习**。MemSkill 思路移植：让 harness 学习"何时写记忆文件、写什么粒度"，而非硬编码规则。
- **风险提示**：经验污染与 context collapse 在长期运行的 harness 中必然发生；任何自动写入 CLAUDE.md/Skills 的机制必须带 helpful/harmful 计数、留痕与回滚。

一个可落地的最小闭环设计草图（综合本分支证据，供 develop 分支参考）：

```
会话轨迹（终端日志/工具调用流）
  → ① 轨迹判定：结合退出码/测试结果做成败标注（弱化 LLM 自判偏差，harness 有真实信号！）
  → ② 双向蒸馏：成功→候选 workflow/skill（AWM/SkillWeaver 式）；失败→候选教训条目（ReasoningBank 式）
  → ③ 验证准入：skill 附带验证脚本并由 qa agent 实测；教训条目进入 candidate 区带 helpful/harmful 计数（ACE 式）
  → ④ 增量合入：delta 方式写入 CLAUDE.md / skills/ 目录，git commit 留痕
  → ⑤ 维护：定期修剪计数为负/长期未命中的条目；冲突条目走 review agent 仲裁
```

关键判断：**harness 相对学术系统有两大天然优势**——(a) 执行环境提供客观成败信号（编译、测试、退出码），可绕开"LLM 自判"这一最大质量风险；(b) git 免费提供版本化、审查与回滚，正是学术界呼吁的治理层。因此"harness 原生持续学习"具备超越现有论文系统的条件，这是本项目的研究缝隙。

### 5. 与其他分支的接口备注
- 与分支 A/B（记忆系统）的分工：本分支的"经验/技能库"可视为记忆系统之上的**学习层**；A/B 负责存取基础设施（向量库、分层记忆、遗忘策略的机制实现），C 负责"存什么抽象、何时更新、如何评测学习效果"。
- ACE、Memp、MemSkill 等条目同时涉及两侧，wiki 化时建议：机制页归 A/B，学习闭环页归 C，互相链接。
- 本分支下载的 PDF 与兄弟分支存在两处有意的重叠归档（ACE、Memp 各有一份异名副本），合并 index 时按 arXiv id 去重即可。

---

## 下一层待深挖问题（供下轮 BFS 展开）
1. **经验条目的验证与淘汰机制**：ACE 的 helpful/harmful 计数、技能生命周期综述的"验证/准入/修剪"阶段，有哪些可直接实现的算法与阈值策略？（关联 C1.5、2607.10113）
2. **非参数记忆的容量-检索退化曲线**：经验库规模增长时性能如何变化？有无实证 scaling 研究？（关联 LifelongAgentBench 负结果、SkillRet 1.8 万技能检索）
3. **自判成败的可靠性**：ReasoningBank/Memento 依赖 LLM-as-judge 判定轨迹成败，其错误率对经验库质量的长期影响是否被量化过？
4. **参数化 TTT 在 agent 的落地实验**：2026 年是否已有"harness + 夜间 LoRA 巩固"式系统？成本-收益边界何在？（关联 Panini、TTT 回潮）
5. **多 agent / 多用户共享经验库的治理**：出处（provenance）、权限、冲突合并与安全（提示注入经由经验库传播）——技能分发平台（ClawHub 等）已有何种实践？
6. **面向 coding harness 的 lifelong 基准设计**：SWE 任务流的技能依赖图如何构造、如何自动验证——作为本项目潜在论文选题的可行性。

---

## 附录：本分支引用但未入库 PDF 的文献清单（仅链接，供下轮按需归档）

| 文献 | 年份 | 链接 | 所属小节 |
|---|---|---|---|
| Reflexion: Language Agents with Verbal Reinforcement Learning | 2023 | https://arxiv.org/abs/2303.11366 | C1.9（PDF 已由兄弟分支归档） |
| The Surprising Effectiveness of Test-Time Training for Abstract Reasoning | 2024 | https://arxiv.org/abs/2411.07279 | C2.4 |
| Learning to (Learn at Test Time): RNNs with Expressive Hidden States | 2024 | https://arxiv.org/abs/2407.04620 | C2.4 |
| A Survey of Self-Evolving Agents: On Path to ASI | 2025 | https://arxiv.org/abs/2507.21046 | C2.6（PDF 已由兄弟分支归档） |
| MemoryAgentBench: Evaluating Memory in LLM Agents | 2025 | https://arxiv.org/abs/2507.05257 | C4.3 |
| MUSE-Autoskill: Self-Evolving Agents via Skill Lifecycle | 2026 | https://arxiv.org/abs/2605.27366 | C1.9 |
| A Comprehensive Survey on Agent Skills | 2026 | https://arxiv.org/abs/2605.07358 | C1.9 |
| Dynamic Agent Skills: A Lifecycle Survey | 2026 | https://arxiv.org/abs/2607.10113 | C1.9 |
| Self-Evolving Agents as Dynamic Graph Transformation: A Survey | 2026 | https://arxiv.org/abs/2608.18104 | C1/C2 交叉 |
| Continual Learning in LLMs: Methods, Challenges, and Opportunities | 2026 | https://arxiv.org/abs/2603.12658 | C3.2 |
| Panini: Continual Learning in Token Space via Structured Memory | 2026 | https://arxiv.org/abs/2602.15156 | C3.3 |
| Learn to Memorize (MoNIM), ACL 2025 | 2025 | https://aclanthology.org/2025.acl-long.1385/ | C3.4 |
| From Storage to Experience: LLM Agent Memory 综述, ACL 2026 Findings | 2026 | https://aclanthology.org/2026.findings-acl.2069.pdf | C0 |

检索与选材说明：候选池约 40 项，按"对本项目主题的直接相关度 × 影响力（引用/star）× 时间覆盖均衡（2023-2026 各期均有锚点）"三准则筛出 14 篇入库；凡与分支 A/B 主题重叠且已被归档的不重复下载。venue 与引用数经 Semantic Scholar API 批量核验（2026-08-27），star 数经 GitHub API 核验（同日）。

---

**落款**：survey-agent-C · 2026-08-27 11:44
