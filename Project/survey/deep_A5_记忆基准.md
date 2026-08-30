# 深挖底稿 A5:评测方法学——为 harness 记忆设计新基准

> openspec change-002 · 方向 A-5 · 基于 branch_A(2026-08-27)的"评测切入"假设做空白点核实
> 新增论文登记于 `raw/papers/index_002_A5.yaml`;网页剪藏见 `Clipping/2026-08-28_*`
> 检索时点:2026-08-28/29;协议:arXiv(https)+ Semantic Scholar API + websearch + OpenReview API

---

## 1. 结论先行

**空白点判定:部分成立(原表述已过时,需收窄后才能立项)。**

branch_A(2026-08-27)记录的空白点是"尚无面向 coding harness 的记忆基准——跨会话修 bug 时是否记得上次的环境坑/用户编码偏好/仓库惯例无人评测"。本轮核实表明:**这个宽表述在 2026-08 已不成立**——过去 18 个月该空间被快速填充:MemoryCode(ACL 2025,跨会话编码约定)、SWE-Bench-CL(2025-07,coding agent 持续学习协议)、SWE-ContextBench(2026-02,编程经验复用)、DreamBench-SWE(2026-08,软件 agent 记忆卫生)以及社区级 codememo-benchmark(直接用 Claude Code 转录出题)都已出现;相邻空间(agent 轨迹记忆)还有 LongMemEval-V2、MemoryArena、AMA-Bench、EvoMemBench 等 2026 新基准密集落地。**但收窄后的空白仍然真实存在且可立项**:没有任何基准把 harness 原生记忆机制(CLAUDE.md/MEMORY.md/rules 分层、记忆放置、compaction 存活、加载窗上限、离线固结/Dreaming)当作**受控实验变量**;跨项目记忆迁移与干扰完全无基准;coding 域的记忆写入/固结正确性只有一个方法学上有争议的单作者工作(DreamBench-SWE);且**所有现存记忆基准都没有与去污染的 live 任务管线结合**。这四个收窄维度构成本方向真正的论文机会,但窗口紧迫(该子领域 8 个月内新增 6+ 基准)。

---

## 2. 相关工作全景表

### 2.1 对话/用户中心记忆基准(背景层,branch_A 已覆盖者从简)

| 基准 | 年份/venue | 任务形态 | 规模 | 指标 | 与 harness 场景差距 |
|---|---|---|---|---|---|
| DMR(MemGPT 内) | 2023 | 多会话对话 QA | ~500 题/5 会话 | 准确率 | 已饱和(94%+),无 agentic 成分 |
| LoCoMo | 2024, ACL | 超长多会话对话 QA/摘要 | ~600 轮/16K token,1,986 问 | 准确率/F1 | 合成对话、被刷榜、区分度饱和;纯回忆 |
| LongMemEval(V1) | 2024, ICLR'25 | 用户-助手对话六能力 QA | 500 问,115k-1.5M token | 准确率 | 能力划分成行业标准,但对话域、非执行 |
| PrefEval | 2025, ICLR'25 | 偏好遵循 | 3,000 对 | 遵循率 | "偏好主动应用"与 harness 用户纠偏同构,但对话域 |
| MemBench | 2025, ACL Findings | 事实+反思记忆 | — | 有效性/效率 | 对话域 |
| PersonaMem / v2 | 2025/2026 | 画像个性化 | 5,990/5,000 问 | 准确率 | 对话域 |
| **BEAM** | 2025-10, **ICLR 2026** | 128K-10M token 连贯对话,10 能力 | 100 对话/2,000 问 | 准确率(分能力) | 规模前沿(10M);域含 coding 话题但仍是对话回忆 [库内: 2025-tavakoli-beam.pdf] |
| **HaluMem** | 2025-11 | **操作级**:记忆提取/更新/QA 三阶段 | ~15k 记忆点/3.5k 问,>1M token | 各阶段幻觉率/omission/正确率 | 首个"写入质量"操作级基准;**对话域**,无 coding/harness [库内: 2025-chen-halumem.pdf] |
| **MemoryAgentBench** | 2025-07, **ICLR 2026** | 增量多轮喂入,四能力(AR/TTL/LRU/CR) | 2,071 问,~285k token | 准确率 | 增量协议是正确方向;仍以文本回忆为主 [库内: 2025-hu-memoryagentbench.pdf] |

### 2.2 agent 轨迹/经验记忆基准(2026 爆发带)

| 基准 | 年份/venue | 任务形态 | 规模 | 指标 | 与 harness 场景差距 |
|---|---|---|---|---|---|
| **MemoryArena** | 2026-02 | 任务间**显式依赖**的多会话 agentic 任务(web/规划/检索/形式推理) | 766 任务 | 端到端任务成功率 | 直接测"记忆→行动";无 coding 域、无 harness 机制变量 [库内: 2026-he-memoryarena.pdf] |
| **LongMemEval-V2** | 2026-05 | web-agent 轨迹史→环境知识 QA,5 能力(含 workflow knowledge、gotchas) | 451 问,25M-115M token | 准确率 + 查询延迟(**LAFS 前沿增益**) | 能力分类与 harness 需求高度同构,但 web 域、QA 形态、非执行验证 [库内: 2026-wu-longmemeval-v2.pdf] |
| **AMA-Bench** | 2026-02, **ICML 2026** | 真实 agentic 轨迹+专家 QA;合成轨迹(任意长)+规则 QA | 2,496 问 | 准确率 | "机器生成交互流"立论正确;单轨迹理解为主,非跨会话经验 [库内: 2026-zhao-ama-bench.pdf] |
| AgentLongBench | 2026-01 (arXiv 2601.20730) | 游戏 agent 环境 rollout 回忆 | 6,400 问,31k-4M token | 准确率 | 合成游戏域 |
| EMemBench / FileGramBench / RealMem / CloneMem / Mem-Gallery | 2026 | 游戏轨迹/文件系统行为/真实交互/AI 分身/多模态对话 | 各异 | 准确率 | 均非 coding harness |
| EvoMemBench | 2026-05 | 记忆二轴(in/cross-episode × 知识/执行),15 系统横评 | — | 任务成功率 | 统一协议横评;执行导向轴与本方向相关,但环境非 coding harness |
| MemTraceBench(MemTrace 内) | 2026-05 (arXiv 2605.28732) | **记忆失败归因**:操作图上定位故障操作 | 160 标注失败案例 | 归因准确率 | 诊断方法学可复用;语料是对话域基准×4 系统 |
| Evo-Memory / MemGym | 2025-11/2026-05 | 测试时学习/长程记忆环境 | — | 任务成功率 | 通用 agent 环境 |
| Harness the Memory | 2026-08 | 记忆基质横评(含 BigCodeBench-Hard 代码任务) | 4 基准复合 | 任务成功率+成本 | 是横评不是基准;已在库 [库内: 2026-huang-harness-memory.pdf] |

### 2.3 coding/SWE 域跨会话与经验基准(空白点的直接竞品)

| 基准 | 年份/venue | 任务形态 | 规模 | 指标 | 关键短板(=差异化空间) |
|---|---|---|---|---|---|
| **MemoryCode** | 2025-02, **ACL 2025** | 合成 mentor-mentee 多会话对话,跨会话追踪编码指令并在最终任务执行 | 会话数 3-100 可扩 | 代码执行正确率 | 合成对话、指令为简单编码约定;**无真实仓库、无 harness**;GPT-4o 全历史跌 67% [库内: 2025-rakotonirina-memorycode.pdf] |
| **SWE-Bench-CL** | 2025-07 (arXiv 2507.00014) | SWE-Bench Verified 重组为按时间排序的 issue 序列 | 基于 SWE-Bench Verified | ACC/Forgetting/FT/BWT/TUE/CL-F1 | **只有协议无完整结果**;底层数据已污染;记忆模块=外挂 FAISS,与 harness 原生机制无关 |
| **SWE-ContextBench** | 2026-02 (arXiv 2602.08316) | SWE-Bench Lite + 99 个按真实 issue/PR 依赖派生的关联任务序列,测经验复用 | 300+99 任务 | 解决率/时间/成本 | 单仓库内序列;oracle 检索为主;仍是外部经验注入,非 harness 记忆闭环 |
| **DreamBench-SWE** | 2026-08 (arXiv 2608.20664) | 多会话 SWE"记忆陷阱":后续任务依赖前期会话不可推断信息,**可执行隐藏 oracle** 计分 | 180 cell × 4 条件(v2.1) | 通过率(预注册统计) | 最接近的竞品;但**单作者**、报告以审计免责为主、主对比 null、覆盖仅"记忆卫生"一维、无 harness 机制变量 |
| **SWE-chat / SWE-Together** | 2026, COLM 2026 / arXiv 2606.29957 | 真实用户-agent 编码会话重建(11,260 会话→109 任务)+ 用户模拟器 | 109 任务 | 最终仓库正确性+纠偏轮数 | 测交互协作不测记忆;但其**数据管线是新基准的数据来源范本** [库内: 2026-baumann-swe-chat.pdf] |
| **codememo-benchmark** | 2026-03(社区,HuggingFace) | 摄入 Claude Code JSONL 转录,跨会话 QA(6 类) | 158 问/3 项目 | LLM-judge/F1/recall@k | 非同行评审、规模小、QA 型;证明语料路线可行 [剪藏: Clipping/2026-08-28_huggingface_codememo-benchmark.md] |
| **Evaluating AGENTS.md**(附 AGENTbench) | 2026-02 (arXiv 2602.11988) | 上下文文件(AGENTS.md/CLAUDE.md)对 SWE 任务的因果效应 | SWE-bench Lite + 138 新任务 | 解决率/步数/成本 | 只测**静态、单会话**的 context file;不测 agent 自写记忆与跨会话累积 [库内: 2026-gloaguen-evaluating-agents-md.pdf] |
| Why Does CLAUDE.md Keep Growing | 2026-08 (arXiv 2608.11095) | 指令文件维护策略评测("灾难性记住") | 51 步维护序列等 | 超额增长率/指令遵循率 | 首个把"记忆文件维护质量"做成可测量对象的工作;非任务级基准 |
| LifelongAgentBench / StreamBench | 2025 | lifelong/流式学习(含 DB/OS 环境) | — | 持续学习指标 | 已在库;环境非 coding harness(与 C-6 方向交界)[库内: 2025-zheng-lifelongagentbench.pdf, 2024-wu-streambench.pdf] |

### 2.4 评测基础设施(A5-3 复用件)

- **SWE-bench-Live**(NeurIPS 2025 D&B):REPOLAUNCH 自动环境构建 + 月度刷新,1,319 任务/93 仓库;静态基准 vs live 基准分差证明污染真实存在。
- **SWE-rebench**(arXiv 2505.20411):21,000+ 交互式 SWE 任务自动采集;**按 issue 创建日 vs 模型发布日标记污染**的排行榜协议。
- **AMB / Bench'd**(独立复测平台):厂商自报 vs 独立复测差距(某产品自报 93.4% vs OSS 复测 32.4%)——排行榜治理是必答题(branch_A 已记录)。
- **LME-V2 的 LAFS 协议**:延迟-准确率前沿增益计分,允许一方法多延迟工作点,是效率一等指标的最成熟实现。

---

## 3. 空白点逐条核实过程

### A5-2-a 跨会话(cross-session)记忆 → **已被覆盖,不再是空白**

- 检索词:`coding agent cross-session memory benchmark`、`SWE-bench multi-session repository memory evaluation`、`MemoryCode multi-session coding`(websearch + S2 API `agent memory benchmark coding`)。
- 查到:MemoryCode(ACL 2025)、DreamBench-SWE、SWE-ContextBench、SWE-Bench-CL、codememo-benchmark、SWE-Together/SWE-chat。
- 判定:**不空白**。跨会话编码记忆的"存在性"问题已被回答(MemoryCode 证明模型级缺陷,DreamBench-SWE 证明记忆系统级差异)。新工作若仍以"第一个跨会话 coding 记忆基准"立论会被直接拒稿。

### A5-2-b 跨项目(cross-project)记忆迁移与干扰 → **空白成立**

- 检索词:`cross-project memory transfer coding agent benchmark`、`user preference persistence across repositories evaluation`、S2 检索 `cross-repository agent memory`。
- 查到:只有工程博客(vectorize.io、mem0.ai)在讨论 Claude Code Auto Memory per-repo 隔离与跨项目 workaround(4 种原生模式);Mem0/Hindsight 以 scope 标签宣传跨项目能力但**无基准背书**;SWE-Bench-CL 的序列按仓库组织,不测跨仓迁移;SWE-ContextBench 的关联任务在同仓库内。
- 判定:**空白**。"用户级偏好应跨项目生效、项目级惯例不应泄漏到别的项目(干扰/污染)"这一对偶命题无任何基准。且该维度有天然的 harness 语义(user-scope vs repo-scope 文件层级),外部记忆层厂商有强需求(评测背书)。

### A5-2-c 记忆固结正确性(consolidation correctness) → **对话域已覆盖,coding/harness 域基本空白**

- 检索词:`memory consolidation correctness evaluation benchmark 2026`、`sleep-time compute dreaming evaluation`、`HaluMem`、`TrustMem`。
- 查到:HaluMem(操作级幻觉:提取/更新/QA,发现更新阶段正确率 <26%)、TrustMem(固结可信度的 verifier+RL 方法,评测用 HaluMem/Mem-α)、MemTrace(操作图错误归因,160 案例)、DreamBench-SWE(SWE 域记忆卫生:陈旧/矛盾/冗余,可执行 oracle)。
- 判定:**部分空白**。对话域的固结正确性已有 HaluMem 一系;coding 域只有 DreamBench-SWE,而它:(1) 单作者、v2 主对比为 null 结果、自述"不建立机制结论";(2) 只测"卫生"(hygiene)不测"固结收益 vs 固结损伤"的权衡;(3) 不覆盖 Claude Dreaming/Anthropic Dreams 这类**产品级固结原语**的正确性(Dreams 单库固结、不跨 scope——机制事实见剪藏)。"固结不应伤害下游任务 + 可审计可回滚"在 coding 域无标准评测。

### A5-2-d 记忆写入策略质量(write policy quality) → **对话域已覆盖,harness 域空白成立**

- 检索词:`memory write policy quality evaluation`、`Mem-alpha memory construction reward`、`memory placement CLAUDE.md evaluation`、`context compaction survival benchmark`。
- 查到:对话域有 HaluMem(提取遗漏/虚构)、Mem-α(写入策略 RL 的 reward 设计)、TrustMem;harness 域有 Evaluating AGENTS.md(静态文件因果效应:手写 +4%、LLM 生成 -3%/成本 +20%)和 Catastrophic Remembering(指令文件膨胀 +226%、prompt comments 修复)。
- 判定:**收窄后空白成立**。现有 harness 域工作只测"静态文件存在与否/如何维护",没有测 **agent 在会话中的写入决策质量**:该不该写(vs 噪声)、写到哪一层(根 CLAUDE.md / path-scoped rule / MEMORY.md / 丢弃)、能否在 compaction 后存活并继续起作用。"记忆放置决定持久性"是 harness 独有语义(branch_A A4 已记录 compaction 语义),没有任何基准操纵它。

### A5-2-e 效率与污染控制协议 → **部件齐全,组合空白**

- 检索词:`benchmark contamination agentic coding SWE-bench-Live SWE-rebench`、`memory benchmark contamination control`。
- 查到:效率一等指标已成共识(LAFS/MemScore);污染控制在 SWE 域有成熟管线(SWE-bench-Live 月度刷新、SWE-rebench 日期标记),但**没有任何记忆基准使用 live 任务源**——LoCoMo/BEAM 合成、SWE-Bench-CL/SWE-ContextBench 基于已污染的 SWE-Bench 家族、DreamBench-SWE 手工陷阱。记忆基准的污染问题更尖锐:跨会话设计要求任务序列**长期稳定可复现**,与 live 刷新存在张力,这个矛盾本身没有人正面解决。
- 判定:**组合空白成立**(live 数据源 × 记忆序列 × 效率前沿计分,三者从未同框)。

### 小结

| 原假设维度 | 判定 | 依据 |
|---|---|---|
| 跨会话 | 不空白 | MemoryCode/DreamBench-SWE/SWE-ContextBench 等 6+ 工作 |
| 跨项目 | **空白** | 仅工程博客,无基准 |
| 固结正确性 | 部分空白(coding 域) | 对话域 HaluMem;coding 域仅 DreamBench-SWE(方法学存疑) |
| 写入策略质量 | **空白(harness 语义下)** | 静态文件评测≠写入决策评测;放置/压缩存活无人测 |
| live 污染控制 × 记忆 | **组合空白** | 部件成熟,无人组合 |

---

## 4. 立项论证(若做)

### 4.1 研究问题表述

**RQ:coding harness 的原生记忆机制(分层记忆文件、agent 自写笔记、放置决策、compaction、离线固结)在多会话、多项目的真实软件工程工作流中,是否、何时、以多大代价改善 agent 表现?**

拆解:
- RQ1(收益):跨会话前向迁移(第 k 次相关任务的解决率/成本曲线)有多大?哪类记忆内容(环境坑/用户偏好/仓库惯例/工作流)贡献最大?
- RQ2(写入):agent 自写记忆的操作级质量(precision/recall vs 事后标注的"值得记住集合")与放置正确率(user/repo/path scope)如何?
- RQ3(固结):离线固结(dreaming)前后,记忆库的卫生指标与下游任务表现如何变化?固结引入的损伤(丢关键项/合并错误)频率?
- RQ4(干扰):项目 A 的记忆对项目 B 的任务是助益还是污染(跨项目 backward interference)?
- RQ5(效率):以上全部在 token/延迟预算约束下报告(LAFS 式前沿)。

### 4.2 基准设计草案(工作名:HarnessMemBench)

- **任务单元**:"episode 序列"= 同一仓库(或仓库对)上 5-15 个按真实时间排序的任务(issue 修复/特性/重构),序列内后续任务显式或隐式依赖前期会话可获得的信息(环境坑、构建脚本怪癖、用户纠偏、API 演变)。
- **三种序列来源**(对应三档污染控制):
  1. **Live 层**:SWE-rebench/SWE-bench-Live 式管线抓取新鲜 issue,按 issue/PR 引用关系(SWE-ContextBench 方法)自动成链,月度刷新,日期标记;
  2. **注入层**:在真实仓库上合成"不可推断事实"注入早期会话(MemoryCode/DreamBench-SWE 方法),用可执行 oracle 验证后期任务是否用到——天然免污染(事实是新造的);
  3. **回放层**:真实 harness 会话转录(SWE-chat 管线先例:11,260→109,转化率 0.97%;codememo 先例)重建为可复现任务,用户模拟器回放纠偏。
- **受控变量(本基准独有)**:harness 记忆条件矩阵——无记忆 / 只读 CLAUDE.md / auto-memory 开 / auto-memory+定期固结 / 外部 MCP 记忆层;放置扰动(同一记忆内容强制放 user/repo/path 层)× 强制 compaction 事件。多 harness 执行(Claude Code、OpenHands、Codex CLI)以回应 scaffold-effect 批评(库内 2026-vats-scaffold-effect.pdf、2026-zhang-harness-disclosure.pdf)。
- **指标栈**:任务解决率曲线(FT/BWT,沿 SWE-Bench-CL 定义)+ 操作级写入/固结质量(沿 HaluMem 三阶段)+ 记忆卫生 oracle 探针(沿 DreamBench-SWE)+ token/延迟前沿(沿 LME-V2 LAFS)。

### 4.3 数据与标注需求估算

| 项 | 估算 | 依据 |
|---|---|---|
| Live 序列 | 60-100 序列(≈500-800 任务),月刷 10-20 | SWE-rebench 21k 任务池 + 依赖成链筛选率按 SWE-ContextBench(300→99)≈1/3 折算 |
| 注入层 | 40-60 序列,每序列 3-5 个 oracle 探针 | DreamBench-SWE 180 cell 规模即可出统计;oracle 编写≈2-4 人时/探针 → 500-1,000 人时 |
| 回放层 | 30-50 任务 | SWE-chat 0.97% 转化率意味着需要 3k-5k 原始会话;若无一手转录渠道则此层降级为 codememo 式 QA |
| 人工标注 | "值得记住集合"标注(RQ2 gold):每序列 2-3 人时 × 150 序列 ≈ 400 人时;QA 校验参照 LME-V2(451 问人工)| LME-V2/BEAM 均为"自动生成+人工校验"配比 |
| 环境工程 | REPOLAUNCH 复用可大幅压缩;预算大头是 agentic 评测算力(每条件全序列跑一遍,粗估 $3k-8k/系统) | SWE-bench-Live 报告的自动化率 |

总量级:2-3 人 × 4-5 个月 + 评测算力预算;对照 LME-V2(UCLA 7 人)与 AMA-Bench(UCSD 12 人)属可行区间,但明显不是单人项目。

### 4.4 最像的竞品与差异化

| 竞品 | 像在哪 | 差异化 |
|---|---|---|
| **DreamBench-SWE** | 多会话 SWE + 记忆依赖 + 可执行 oracle | 我们:多维(收益/写入/固结/干扰 vs 只有卫生)、harness 原生机制为变量(vs 外挂记忆条件)、live 污染控制、多 harness、规范统计但以效应量为主(vs 预注册审计式 null 报告) |
| **SWE-ContextBench** | issue 依赖成链、经验复用三维指标 | 我们:链上跑真实 harness 记忆闭环(vs oracle 注入经验)、新鲜任务(vs SWE-Bench Lite)、加入写入/固结质量维 |
| **SWE-Bench-CL** | CL 指标栈(FT/BWT/CL-F1) | 我们:有完整实验(它只有协议)、去污染数据、harness 原生记忆 |
| **LongMemEval-V2** | 能力分类(workflow/gotchas)、LAFS | 我们:coding 域、执行验证(vs QA)、写入侧评测(它只评读取侧) |
| **Evaluating AGENTS.md** | harness 上下文文件的因果评测 | 我们:动态自写记忆与多会话累积(它是静态单会话);其效应量小(±3-4%)的教训直接决定我们的统计功效设计 |

新颖性核心一句话:**第一个把"harness 记忆机制本身"(放置、压缩存活、固结)作为受控变量、并在去污染 live 任务流上度量记忆四维质量(收益/写入/固结/干扰)的可执行基准**。

### 4.5 目标 venue

NeurIPS 2027 Datasets & Benchmarks(SWE-bench-Live 先例)或 ICLR 2027(BEAM/MemoryAgentBench 先例);ACL 系统 track 备选(MemoryCode 先例)。

---

## 5. 风险与不确定性

1. **抢跑风险(最高)**:该子领域 8 个月新增 6+ 基准;DreamBench-SWE 已在迭代(v2.1),LME-V2 团队(UCLA)顺势做 coding 版的概率不低;AMA-Bench 团队已宣布扩展计划。缓解:以"harness 机制为变量"这一别人没有的角度切入,并尽快占位(workshop 短文/预注册)。
2. **效应量风险**:Evaluating AGENTS.md 显示 context file 效应仅 ±3-4%,chatcode 复现指出检出 10pp 效应需 120-200 任务;若记忆收益本身小,基准会退化为"证明记忆没用"的负结果(仍可发表,但叙事变化)。缓解:注入层保证存在"必须靠记忆才能解"的任务(DreamBench-SWE 的 non-inferable 设计),把"记忆可有可无"与"记忆必要"两种 regime 分开报告。
3. **harness 不稳定性**:Claude Code auto memory/Dreams 语义随版本变化(200 行加载窗、per-repo scope 均为 2026 时点事实),闭源机制不可控;OpenHands 可控但生态代表性弱。缓解:版本 pin + 机制抽象层(把"分层文件记忆"定义为规范接口,具体 harness 只是实现)。
4. **live 刷新与可复现的张力**:记忆序列要求长程稳定,live 源要求月度换血。缓解:双轨制——冻结版(注入层为主,用于论文可复现)+ live 排行榜(SWE-rebench 式日期标记)。
5. **评测成本**:全条件矩阵 × 多 harness × 序列长任务,算力成本可能是 LoCoMo 类基准的 10-50 倍;需要在设计期就做条件裁剪(fractional factorial)。
6. **排行榜治理**:厂商自报与独立复测的信任危机(AMB 教训);若无维护承诺,基准发布后一年即腐化。
7. **信息来源不确定性**:SWE-ContextBench、TrustMem、MemTrace、AgentMemBench、SWE-Together 五篇因检索当日 arXiv 全域连接被重置未能入库深读(细节判断基于 arXiv HTML/摘要/第三方分析);PDF 补档任务在进行中,登记状态见 index_002_A5.yaml 的 pdf_status 字段。DreamBench-SWE(GitHub release)与 SWE-Bench-CL(OpenReview)已补档核验。

---

## 6. 参考文献(核心;库内路径)

**本轮新增归档(raw/papers/,登记于 index_002_A5.yaml):**
1. Rakotonirina et al., 2025, MemoryCode / From Tools to Teammates, ACL 2025, arXiv:2502.13791 — `raw/papers/2025-rakotonirina-memorycode.pdf`
2. Hu, Wang & McAuley, 2025, MemoryAgentBench, ICLR 2026, arXiv:2507.05257 — `raw/papers/2025-hu-memoryagentbench.pdf`
3. Tavakoli et al., 2025, BEAM/LIGHT, ICLR 2026, arXiv:2510.27246 — `raw/papers/2025-tavakoli-beam.pdf`
4. Chen et al., 2025, HaluMem, arXiv:2511.03506 — `raw/papers/2025-chen-halumem.pdf`
5. He et al., 2026, MemoryArena, arXiv:2602.16313 — `raw/papers/2026-he-memoryarena.pdf`
6. Wu, Ji et al., 2026, LongMemEval-V2, arXiv:2605.12493 — `raw/papers/2026-wu-longmemeval-v2.pdf`
7. Zhao et al., 2026, AMA-Bench, ICML 2026, arXiv:2602.22769 — `raw/papers/2026-zhao-ama-bench.pdf`
8. Gloaguen et al., 2026, Evaluating AGENTS.md, arXiv:2602.11988 — `raw/papers/2026-gloaguen-evaluating-agents-md.pdf`
9. Baumann et al., 2026, SWE-chat, COLM 2026 — `raw/papers/2026-baumann-swe-chat.pdf`
10. Singh, 2026, DreamBench-SWE, arXiv:2608.20664(经 GitHub release v2.1.0 获取)— `raw/papers/2026-singh-dreambench-swe.pdf`
11. Joshi et al., 2025, SWE-Bench-CL, arXiv:2507.00014(经 OpenReview 获取)— `raw/papers/2025-joshi-swe-bench-cl.pdf`

**PDF 待补(arXiv 当日不可达,pdf_status=pending,后台补档任务运行中):**
12. (作者待补), 2026, SWE-ContextBench, arXiv:2602.08316
13. (作者待补), 2026, Why Does CLAUDE.md Keep Growing, arXiv:2608.11095
14. (作者待补), 2026, TrustMem, arXiv:2606.25161
15. Deng et al., 2026, MemTrace, arXiv:2605.28732

**既有库内(branch_A/其它分支已登记,不重复):**
- `raw/papers/2024-maharana-locomo.pdf`、`raw/papers/2024-wu-longmemeval.pdf`、`raw/papers/2026-huang-harness-memory.pdf`、`raw/papers/2026-du-agent-memory-survey.pdf`、`raw/papers/2025-zheng-lifelongagentbench.pdf`、`raw/papers/2024-wu-streambench.pdf`、`raw/papers/2026-zheng-claw-swe-bench.pdf`、`raw/papers/2026-vats-scaffold-effect.pdf`、`raw/papers/2026-zhang-harness-disclosure.pdf`

**其它(未入库,链接备查):**
- SWE-bench-Live, NeurIPS 2025 D&B, arXiv:2505.23419;SWE-rebench, arXiv:2505.20411;Mem-α, arXiv:2509.25911;AgentLongBench, arXiv:2601.20730;RealMem, arXiv:2601.06966;AgentMemBench, arXiv:2608.00009;SWE-Together, arXiv:2606.29957;LoopsBench, arXiv:2608.00267
- 网页剪藏:`Clipping/2026-08-28_huggingface_codememo-benchmark.md`、`Clipping/2026-08-28_vectorize_claude-code-memory-limits.md`、`Clipping/2026-08-28_swe-bench-cl_codex-kb-analysis.md`、`Clipping/2026-08-28_beam_ama-bench_lme-v2_project-pages.md`

---

落款:survey-agent-A5 · 2026-08-29 01:45
