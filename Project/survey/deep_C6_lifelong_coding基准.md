# 深挖底稿 C6：面向 coding harness 的 lifelong 基准设计

> openspec change-002 · 方向 C-6（源自分支 C"下一层待深挖问题"第 6 条）
> 三个子问题：C6-1 基准盘点与缺口；C6-2 与 A-5 的边界与合并建议；C6-3 任务序列构造可行性。
> 检索方法：websearch（重点 2025-06 至 2026-08 增量）+ Semantic Scholar API（venue/引用核验，2026-08-28）+ arXiv https 直连下载。新增论文登记于 `raw/papers/index_002_C6.yaml`。

---

## 1. 结论先行

**空白点是否成立：部分成立（原表述已过时，需重新定位）。**

上一轮（change-001，截至 2026-08-27 的底稿）判断"coding harness 场景（SWE 任务流）仍无专用 lifelong 基准"。本轮深挖发现该判断**在字面上已不成立**：从 2025-06 的 SWE-Bench-CL 开始，到 2026 上半年，"coding × 序列化/持续演化"交叉带在一年内密集出现了至少 8 个基准——SWE-Bench-CL（时序化 SWE-bench + CL 指标）、SWE-ContextBench（跨任务经验复用）、SWE-Milestone（ICML 2026，里程碑 DAG 连续演化）、SWE-CI（CI 循环长期维护）、SlopCodeBench（迭代质量退化）、EvoCode-Bench（多轮状态保持）、MemTrace-Bench（ICSE 2027 在审，持久记忆危害重放）、SkillFlow（真实 harness 上的 lifelong 技能演化）。"再做一个 lifelong coding 基准"作为独立选题的论文潜力应从 high 下调为 **medium**。

但**一个更精确的组合空白仍然存在且可辩护**：现有工作没有任何一个同时覆盖（i）**真实仓库的跨会话长期演化**（现有工作要么单会话连续跑、要么每任务重置）、（ii）**harness 原生记忆机制作为被测对象**（CLAUDE.md / auto memory / skills，现有工作评的是外挂记忆模块或根本无记忆）、（iii）**lifelong 三度量齐备**（遗忘/保持、前向迁移、经验复用率及其成本收益）、（iv）**活体污染控制**（SWE-Bench-CL 和 SWE-ContextBench 都建在 2023 年前的旧 SWE-bench 数据上，污染严重）。这四要素的合取无人占据。**建议不再单独立项 C-6，而是与 A-5（harness 记忆基准）合并为一个"演化仓库上的 harness 记忆与持续学习基准"**，理由见第 3.3 节。

---

## 2. 基准全景表

### 2.1 lifelong / continual agent 基准（非 coding 核心）

| 基准 | 年份 · venue | 任务形态 | 序列化 | coding | 记忆/学习被评 | 核心指标 |
|---|---|---|---|---|---|---|
| StreamBench | 2024 · NeurIPS D&B | 输入-反馈流（text-to-SQL、Python、医疗等） | ✅ 流式 | 部分（子任务） | ✅ 无梯度改进组件 | 流上累积准确率 |
| LifelongAgentBench | 2025 · arXiv | DB/OS/KG 三环境，技能锚定依赖任务流 | ✅ 依赖图 | ❌ | ✅ 经验回放/自一致 | 成功率、跨任务迁移 |
| MemoryAgentBench | 2025 · arXiv | 增量多轮交互 | ✅ 多轮 | ❌ | ✅ 四能力（含测试时学习） | AR/TTL/LRU/CR |
| MemoryArena | 2026 · arXiv | 相互依赖的多会话 agentic 任务 | ✅ 跨会话 | ❌ | ✅ 记忆→行动转化 | 任务耦合成功率 |
| EvoMemBench | 2026 · arXiv (2605.18421) | 记忆演化 2×2（in/cross-episode × 知识/执行） | ✅ | ❌ | ✅ 15 种记忆方法横评 | 各象限准确率 |
| SkillFlow | 2026 · arXiv (2604.17308) | 166 任务/20 工作流族，Agentic Lifelong Learning 协议，**直接在 Claude Code/Codex CLI 上跑** | ✅ 族内顺序 | 部分（含编码族） | ✅ 技能发现/修补/演化 | 有无技能库成功率差（Opus 4.6：62.65→71.08%） |
| SkillLearnBench | 2026（技能综述引） | 任务流上持续技能获取 | ✅ | 部分 | ✅ | 技能获取稳定性 |

### 2.2 coding 序列化 / 演化 / 记忆基准（C6 核心竞品）

| 基准 | 年份 · venue | 任务形态 | 序列化 | 跨会话记忆 | lifelong 指标 | 数据新鲜度/污染 |
|---|---|---|---|---|---|---|
| SWE-Bench-CL（Joshi et al.，2507.00014） | 2025-06 · 仅 arXiv，12 引 | SWE-bench Verified 按 issue 时间重排为 8 个仓库序列 + 课程分级 | ✅ 时序 | 外挂 FAISS 语义记忆（LangGraph 框架） | ✅ 最全：AA、遗忘、FWT/BWT、工具效率、CL-F1 | ❌ 全部 2023 前旧数据，污染重；偏 proposal，实验有限 |
| MemoryCode（Rakotonirina et al.，2502.13791） | 2025-02 · arXiv | 合成多会话对话中追踪/执行编码指令（插入+更新） | ✅ 多会话 | prompt 内历史 | 部分（指令保持） | 合成数据，无真仓库 |
| SWE-Exp（Silin Chen et al.，2507.23361） | 2025-07 · arXiv（方法非基准） | SWE-bench 上的经验蒸馏与复用框架 | —（协议：同仓库+时序后置轨迹排除） | ✅ 经验库 | 复用增益 | 沿用 SWE-bench 数据 |
| SWE-ContextBench（Zhu/Hu/Wu，2602.08316） | 2026-02 · arXiv，10 引 | SWE-bench Lite 300 经验任务 + 99 个真实 issue/PR 引用关系派生的相关任务 | ✅ 一跳关联对 | ✅ 轨迹/摘要经验池（Claude Code 收集） | 复用三维：准确率/时间/token 成本；**无遗忘度量** | ❌ 建于旧 SWE-bench Lite |
| SWE-Milestone（Deng et al.，2603.13428） | 2026-03 · **ICML 2026** | DeepCommit 管线从 commit 史重构里程碑 DAG；98 里程碑/7 仓库/5 语言，**单一连续会话**推进整个 DAG | ✅ DAG 流 | ❌（一次不间断 session，不测跨会话记忆） | 部分：P/R（F2P 完成+P2P 保持=回归惩罚） | 真实 release 区间；全量单跑 ≈$500；孤立>80% vs 连续 38.03% |
| SWE-CI（Jialong Chen et al.，2603.03823） | 2026-03 · arXiv，16 引 | 100 任务（v2 +126），每任务=真实仓库 base→target commit（均值 233 天/71 commits），Architect-Programmer 双 agent CI 循环 | ✅ commit 链 | ❌ | 部分：EvoScore（早期决策对后续演化的助益） | 真实演化史 |
| SlopCodeBench（Orlanski et al.，2603.24755） | 2026-03 · arXiv，16 引 | 20 题/93 检查点，agent 反复扩展自己的旧代码 | ✅ 检查点链 | ❌ | 质量轨迹：verbosity、结构侵蚀（非学习指标） | 手工构造 |
| EvoCode-Bench（Shen et al.，2605.24110） | 2026-05 · arXiv | 26 个有状态任务/227 轮，5-15 轮同一 workspace+同一 session，累积测试 | ✅ 轮内 | ❌（单 session 持续） | MT@4 vs SR（差 22-40 点，会重排名次） | 构造任务（Harbor/Terminus-2） |
| MemTrace-Bench v5（匿名，ICSE 2027 在审） | 2026 · 仅 GitHub（剪藏见 `Clipping/2026-08-28_github_MemTrace-Bench_README.md`） | 4,200 条 prelude-probe 序列/1,260 仓库：先导任务写记忆→探针任务测危害 | ✅ 两段式 | ✅ 15 种记忆配置 | **危害率**：朴素记忆 61.9→75.5% 有用率，但过期 API 记忆坏率 18.9%、过期安全策略 28.4%、跨仓库 22.6% | real/sanitized/synthetic-twin 三级 release |
| AGENTbench（Gloaguen et al.，2602.11988，ETH） | 2026-02 · arXiv | 138 个新仓库 issue 任务，比较无/LLM 生成/开发者手写 context 文件 | ❌ 静态 | 静态 CLAUDE.md/AGENTS.md | —（增益：人写 +4%，LLM 生成 -0.5~-2% 且成本 +20%） | 新/小众仓库，污染较轻 |
| LongMemCode（Jibleanu，独立实验室） | 2026-04 · 无 arXiv（剪藏见 `Clipping/2026-08-28_argosbrain_LongMemCode.md`） | 代码记忆**检索组件**隔离评测：20-31 仓库/16 语言/约 8000 结构查询场景 | ❌ | ✅ 只评读路径 | 检索加权准确率/P99 延迟/成本，无 LLM judge | 确定性 ground truth |

### 2.3 数据基础设施（任务序列构造与污染控制的可用底座）

| 工作 | 年份 · venue | 对 C6 的价值 |
|---|---|---|
| SWE-bench-Live（Linghao Zhang et al.，2505.23419） | NeurIPS 2025 D&B | RepoLaunch 全自动管线：issue 挖掘→容器环境→测试验证；每月 +50 题滚动更新；已扩多语言（743 题/6 语言）与 Windows。**live 序列数据的现成供给** |
| SWE-rebench（Badertdinov et al.，2505.20411） | NeurIPS 2025，94 引 | 21,000+ 任务自动采集；**逐 issue 记录创建日期 vs 模型发布日期**，榜单显式标记潜在污染——污染控制协议的参考实现 |
| GitChameleon 2.0（2507.12367） | ACL 2026 | 328 题版本条件生成：真实库版本断裂变化；"记忆随版本漂移"探针的构造方法参考 |
| CodeUpdateArena（2407.06249） | 2024 · arXiv | 合成 API 更新 + 知识编辑评测；漂移探针的合成路线 |

---

## 3. 空白点核实与 A-5 边界分析

### 3.1 核实过程

1. 以"lifelong/continual + coding agent + benchmark"、"SWE-bench 衍生 + sequential/evolution/memory"、"experience reuse + repository"等组合词全面检索（websearch 远程 + S2 API 核验 venue/引用），重点覆盖 2025-06 之后的增量（上一轮底稿检索止于 2025 年中的公开信息 + 部分 2026 条目）。
2. 对每个候选竞品读摘要或全文（SWE-ContextBench、SWE-Milestone、SWE-CI、SlopCodeBench、SkillFlow、EvoCode-Bench、MemTrace-Bench、AGENTbench 均读了正文关键节），确认任务形态、会话边界、记忆角色、指标族四要素。
3. 用 S2 API 核验发表状态：SWE-Milestone 已中 **ICML 2026**；SWE-bench-Live、SWE-rebench 已中 **NeurIPS 2025 D&B**；GitChameleon 2.0 已中 **ACL 2026**；其余竞品（SWE-Bench-CL 12 引、SWE-CI 16 引、SlopCodeBench 16 引、SWE-ContextBench 10 引、SkillFlow 15 引、EvoCode-Bench 3 引）截至 2026-08 均仅 arXiv。

### 3.2 逐竞品缺口矩阵（"完整组合空白"的证据）

| 竞品 | 真实仓库演化 | 跨会话记忆持久 | 遗忘/保持度量 | 前向迁移/复用度量 | 污染控制 | harness 原生记忆 |
|---|---|---|---|---|---|---|
| SWE-Bench-CL | ✅（issue 时序） | ✅（外挂 FAISS） | ✅ | ✅ | ❌ 旧数据 | ❌ |
| SWE-ContextBench | ✅（issue 引用图） | ✅（经验池） | ❌ | ✅（准确/时/费） | ❌ 旧数据 | 部分（用 Claude Code 收集轨迹但不评其记忆） |
| SWE-Milestone | ✅（commit→DAG） | ❌ 单 session | 部分（P2P 回归） | ❌ | ✅（新 release 区间） | ❌ |
| SWE-CI | ✅（commit 链） | ❌ | ❌ | 部分（EvoScore） | 部分 | ❌ |
| EvoCode-Bench | ❌ 构造任务 | ❌ 单 session | 部分（累积测试） | ❌ | ✅ 全新构造 | ❌ |
| MemTrace-Bench | 部分（构造 prelude） | ✅ | ❌（只测危害不测学习） | ❌ | ✅ synthetic twin | 部分（memory store 通道） |
| SkillFlow | ❌ 工作流族非仓库 | ✅ 技能库前传 | 部分（regress 观察） | ✅（技能增益） | ✅ 新构造 | ✅（Claude Code skills！） |
| LifelongAgentBench | ❌ 非 coding | ✅ | ✅ | ✅ | 部分 | ❌ |

**读法**：每一列都有人做到，但没有一行全绿。最接近全绿的是 SkillFlow（缺真实仓库演化维）与 SWE-Bench-CL（缺污染控制与 harness 原生记忆，且工程完成度低）。这就是修正后的空白点。

另一个被全场忽略的维度：**记忆与仓库的协同演化**。MemTrace-Bench 证明了过期记忆有害（stale API 记忆坏率 18.9%），GitChameleon 证明了版本知识漂移是真实失败源，但没有基准把"仓库演化到版本 v+1 之后，v 时代沉淀的记忆/技能何时该失效"作为被测能力——这正是 harness 场景（记忆随 git 历史一起长）独有、通用 agent 基准天然缺失的问题。

### 3.3 与 A-5 的边界与合并建议

**边界的本质**：A-5（harness 记忆基准）评**机制层**——记没记住、固结对不对、跨会话/跨项目能不能召回、检索准不准（分支 A 的 A5-2 明确列了"跨会话、跨项目、固结正确性"三维）；C-6 评**结果层**——在任务流上是否越用越强（成功率斜率）、旧能力是否保持（遗忘）、经验是否被真正复用且省时省钱（复用率与成本曲线）。两者是同一现象的两个测量截面。

**明确建议：合并为一个基准工作**，理由三条：

1. **数据基座完全同构**。两者都需要"同一真实仓库上的时序任务序列 + 显式会话边界 + 持久记忆目录"。分开做意味着两套几乎相同的仓库策展、环境构建（RepoLaunch 级工程量）和标注管线，重复成本极高且互相竞争新颖性。
2. **指标天然分层而非冲突**。机制指标（记忆命中率、固结正确性、漂移后过期率）恰好是结果指标（成功率斜率、遗忘、复用收益）的**归因层**：结果差时靠机制层解释是"记忆没写对"还是"写对了没用上"。单一基准双 track（Memory track / Lifelong track）比两篇互引的独立论文强得多——这也是 2026 年评审趋势（Harness the Memory、EvoMemBench 都是"多截面统一协议"型工作）。
3. **竞品格局逼迫合并**。单做 C6：撞 SWE-Bench-CL + SWE-Milestone + SWE-ContextBench；单做 A5：撞 MemTrace-Bench + EvoMemBench + LongMemEval-V2。只有"演化仓库 × harness 原生记忆 × 学习+保持+漂移三合一协议"这个合取无人占据，而它必须同时携带 A5 与 C6 的要素才成立。
4. 风险与缓解：合并的代价是 scope 变大。缓解：分层发布——core 版（小规模序列 + 三个 harness 记忆配置）先行占位，full 版随滚动数据扩展；SWE-bench-Live 的"冻结 lite/verified split + 滚动 full split"模式可直接照抄。

（补充：D-1 的"harness-level forgetting / retention 回归集"是同一基准的第三个截面——harness 状态更新导致的行为回归。建议在 change-002 的 synthesis 阶段把 A5+C6+D1 统一为一个立项，分 track 设计。此判断留给主 agent 决策。）

---

## 4. 立项草案（以合并后形态给出）

### 4.1 研究问题表述

> **RQ：配备持久记忆的 coding harness，在同一真实仓库的长期演化任务流上，能否"越用越强"而不退化？**
> 分解为：RQ1（学习）经验积累带来的成功率/效率增益曲线是什么形状？RQ2（保持）harness 记忆状态更新后，旧任务成功率是否回归（遗忘/harness-level forgetting）？RQ3（漂移）仓库演化（API 变更、依赖升级、约定变化）后，过期记忆造成多大危害、多久被纠正？RQ4（机制归因）上述结果差异可归因到记忆写入/固结/检索哪一环？

### 4.2 基准设计草案

- **任务序列构造（三源混合）**：
  1. *issue 流*：SWE-bench-Live/SWE-rebench 管线取 cutoff 后新 issue，按仓库分组、按创建时间排序（SWE-Bench-CL 的时序化协议，换到 live 数据上）；
  2. *里程碑流*：DeepCommit 式从 release 区间重构里程碑 DAG（SWE-Milestone 协议），提供"仓库状态真实前进"的骨架；
  3. *关联对增强*：issue/PR 引用图挖掘相关任务对（SWE-ContextBench 六类关系），保证序列内存在可复用结构；
  4. *漂移探针注入*：在序列中部选取真实版本断裂点（GitChameleon 式 documented breaking changes），构造"此前沉淀的记忆现已过期"的探针任务。
- **会话与记忆协议**：每任务一个新会话（fresh context），仓库 checkout 到该任务对应的真实历史状态；唯一跨任务通道是 harness 持久记忆目录（CLAUDE.md/MEMORY.md/skills/ 或外挂记忆系统），git 版本化记录每次记忆变更——记忆变更历史本身成为评测产物（可 diff、可归因）。
- **被测配置（横轴）**：no-memory 基线 / 朴素轨迹回放 / ExpeL-ReasoningBank 式蒸馏 / AWM 工作流归纳 / ACE playbook / Claude Code auto memory（产品原生） / Mem0 类外挂记忆 / SkillFlow 式技能库。
- **指标（纵轴，三 track）**：
  - Lifelong track：流上成功率斜率、AA、回访旧任务保持率（BWT）、前向迁移（FWT）、**复用率**（记忆条目被检索且被采纳进解题动作的比例，可从轨迹自动判定）、成本曲线（token/延迟随记忆库增长）；
  - Memory track（A5）：跨会话召回、固结正确性（记忆条目 vs 轨迹事实的一致性标注）、检索精度；
  - Drift track：漂移探针后的过期记忆危害率（MemTrace 式 bad rate）与自我纠正延迟（多少任务后记忆被更新）。
- **污染控制**：只用各被测模型 cutoff 之后创建的 issue（SWE-rebench 的日期标记协议）；滚动月度扩充；敏感/不可复现仓库用 synthetic-twin（MemTrace 方案）；序列多顺序随机化对照（防单一顺序过拟合，分支 C C4.6 已识别此坑）。

### 4.3 数据与标注需求估算

- 规模目标：core 版 10-15 个活跃仓库 × 每仓库 20-40 任务序列（含 3-5 个漂移探针）≈ 300-500 任务；full 版随月度滚动。
- 工程：环境构建可复用 RepoLaunch（开源），主要新工程量是"会话边界 + 记忆目录持久化 + 记忆变更 git 留痕"的评测 harness 层，以及漂移探针的断裂点标注。
- 标注（项目有本科级标注员资源）：① 序列质量人工校验（每序列约 0.5-1 人时，参考 SWE-Milestone 98 里程碑全人工核验）；② 固结正确性标注（记忆条目对照轨迹，MemTrace 的 annotation audits 有现成协议）；③ 漂移探针的过期记忆判定。估算 core 版总标注量 400-700 人时，可承受。
- 算力成本：SWE-Milestone 单全量跑 ≈$500（Opus 级）；本基准是"配置×模型×序列"三维矩阵，core 版若 8 配置 × 4 模型 × 全序列，粗估 $2-5 万/完整榜单——必须设计 lite split（2-3 仓库）供社区低成本复现。

### 4.4 最像的竞品与差异化（一句话版）

- vs **SWE-Bench-CL**：同为 CL 指标 + 时序 SWE 任务，但我们用 live 无污染数据、真实 harness 记忆机制（非外挂 FAISS demo）、且有漂移 track；对方仅 arXiv proposal（12 引），工程完成度低。
- vs **SWE-Milestone**（最强已发表竞品）：对方是单一连续 session 内的演化能力，我们是**跨会话**、以持久记忆为唯一通道的学习能力——正交且互补，可直接复用其 DeepCommit 管线。
- vs **SWE-ContextBench**：对方是一跳经验复用对 + 旧数据 + 无遗忘度量，我们是长序列 + live 数据 + 全 lifelong 指标族。
- vs **MemTrace-Bench**：对方只测记忆的危害面（构造 prelude），我们测学习-保持-漂移全曲线（真实演化序列）；其危害标注协议可直接借用。
- vs **SkillFlow**：对方证明了"harness 上 lifelong 协议可行"，但任务是合成工作流族；我们把同一协议落到真实仓库演化上——这是 harness 用户的真实工作负载。

### 4.5 顺带的实证卖点（基准之外的科学发现机会）

分支 C/D 已有信号表明本基准可能产出反直觉结论，这对 D&B track 论文是加分项：AGENTbench 显示 LLM 生成的 context 文件是负收益；SWE-ContextBench 显示自由检索经验≈零增益、只有正确挑选的摘要有用；LifelongAgentBench 显示朴素回放有害；MemTrace 显示朴素持久记忆 +13.6 点有用率但伴随 ~20% 坏率。"harness 记忆在真实演化仓库上的净收益何时为正"目前没有答案——本基准就是给出答案的仪器。

---

## 5. 风险与不确定性

1. **赛道拥挤且移动极快**（最大风险）：2026 上半年该交叉带新增 8 个基准，SWE-Milestone 已占住 ICML 2026、SWE-rebench/SWE-bench-Live 占住 NeurIPS 2025。从立项到投稿的 6-9 个月窗口内，"跨会话 + harness 记忆 + live 数据"组合被他人（尤其 OpenHands 系，Xingyao Wang 同时是 SWE-Milestone 作者且其 SDK 已有持久记忆特性）抢先的概率不低。缓解：尽快以 lite 版 + 立场论文占位；与 A5/D1 合并提高护城河。
2. **评测成本**：三维矩阵全跑 $2-5 万/榜单；若模型方不赞助，社区复现性受限。缓解：lite split + 冻结 split 策略。
3. **harness 混杂变量**：Scaffold Effect / harness disclosure 文献（分支 D）证明 harness 差异可造成 20+pp 摆动，会淹没记忆效应。必须 locked-harness 协议（mini-swe-agent 式参考实现 + 每 harness 独立榜单），这增加设计复杂度。
4. **净效应可能太小或全阴性**：若所有记忆配置在严格协议下增益 <2pp（AGENTbench 式结论），基准的"排行榜价值"受损——但作为负结果仍可发表，需在论文定位时预留两手。
5. **自判与归因噪声**：复用率指标依赖"记忆条目被采纳"的轨迹判定，LLM-judge 误差会传导；需抽样人工校准（分支 C 未解决问题 #3 的已知坑）。
6. **命名与认知撞车**：SWE-Bench-CL、SWE-ContextBench 名称已占据心智；新工作需明确差异化命名与对比实验（把两者作为 baseline 协议复现）。
7. **不确定性声明**：MemTrace-Bench 为 ICSE 2027 在审匿名工作，细节以 README 为准，可能变动；LongMemCode 为非同行评审独立工作，仅作生态信号；本轮未能穷尽 NeurIPS 2026 D&B 在投未公开工作，撞车风险评估存在盲区。

---

## 6. 参考文献（含归档路径）

**本轮新归档（登记于 `raw/papers/index_002_C6.yaml`）**

1. SWE-Bench-CL: Continual Learning for Coding Agents · Joshi, Chowdhury & Uysal · 2025 · arXiv:2507.00014 · `raw/papers/2025-joshi-swe-bench-cl.pdf`
2. SWE-Milestone: Evaluating AI Agents on Continuous Software Evolution · Deng et al.（含 Xiangru Tang、Xingyao Wang）· ICML 2026 · arXiv:2603.13428 · `raw/papers/2026-deng-swe-milestone.pdf`
3. SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration · Jialong Chen et al. · 2026 · arXiv:2603.03823 · `raw/papers/2026-chen-swe-ci.pdf`
4. SlopCodeBench: Benchmarking How Coding Agents Degrade Over Long-Horizon Iterative Tasks · Orlanski et al. · 2026 · arXiv:2603.24755 · `raw/papers/2026-orlanski-slopcodebench.pdf`
5. SWE Context Bench: A Benchmark for Context Learning in Coding · Zhu, Hu & Wu · 2026 · arXiv:2602.08316 · `raw/papers/2026-zhu-swe-contextbench.pdf`
6. SWE-bench Goes Live! · Linghao Zhang et al. · NeurIPS 2025 D&B · arXiv:2505.23419 · `raw/papers/2025-zhang-swe-bench-live.pdf`
7. SWE-rebench · Badertdinov et al. · NeurIPS 2025 · arXiv:2505.20411 · `raw/papers/2025-badertdinov-swe-rebench.pdf`
8. SWE-Exp: Experience-Driven Software Issue Resolution · Silin Chen et al. · 2025 · arXiv:2507.23361 · `raw/papers/2025-chen-swe-exp.pdf`
9. MemoryCode（From Tools to Teammates）· Rakotonirina et al. · 2025 · arXiv:2502.13791 · `raw/papers/2025-rakotonirina-memorycode.pdf`
10. SkillFlow: Benchmarking Lifelong Skill Discovery and Evolution · Zhang et al. · 2026 · arXiv:2604.17308 · `raw/papers/2026-zhang-skillflow.pdf`
11. EvoCode-Bench: Evaluating Coding Agents in Multi-Turn Iterative Interactions · Shen et al. · 2026 · arXiv:2605.24110 · `raw/papers/2026-shen-evocode-bench.pdf`
12. Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? · Gloaguen et al.（ETH）· 2026 · arXiv:2602.11988 · `raw/papers/2026-gloaguen-agentbench-contextfiles.pdf`

**剪藏（`Clipping/`）**

- MemTrace-Bench v5（ICSE 2027 在审，无 arXiv）：`Clipping/2026-08-28_github_MemTrace-Bench_README.md`
- LongMemCode（独立实验室，无 arXiv）：`Clipping/2026-08-28_argosbrain_LongMemCode.md`

**库内已有（不重复下载）**

- LifelongAgentBench · `raw/papers/2025-zheng-lifelongagentbench.pdf`；StreamBench · `raw/papers/2024-wu-streambench.pdf`；ReasoningBank · `raw/papers/2025-ouyang-reasoningbank.pdf`；Harness the Memory · `raw/papers/2026-huang-harness-memory.pdf`；Harness Continual Learning（HCL）· `raw/papers/2026-kang-harness-continual-learning.pdf`；Claw-SWE-Bench · `raw/papers/2026-zheng-claw-swe-bench.pdf`；Harness-Bench · `raw/papers/2026-yao-harness-bench.pdf`；SWE-agent ACI · `raw/papers/2024-yang-swe-agent-aci.pdf`

**仅链接（未深读，不入库）**

- EvoMemBench · arXiv:2605.18421；GitChameleon 2.0 · arXiv:2507.12367（ACL 2026）；CodeUpdateArena · arXiv:2407.06249；MemoryAgentBench · arXiv:2507.05257（分支 B/C 已登记）；MemoryArena · arXiv:2602.16313（A-5 范围）

---

**落款**：survey-agent-C6 · 2026-08-29 01:48（12/12 篇 PDF 已核实归档）
