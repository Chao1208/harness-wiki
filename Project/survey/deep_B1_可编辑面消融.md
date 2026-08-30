# Deep-dive B1:harness 可编辑面的最小充分集——逐组件消融

> change-002 · 方向 B-1 · 深挖底稿
> 上游文档:`Project/survey/branch_B_agent自进化.md`(下一层待深挖问题第 1 条)

---

## 1. 结论先行

**空白点是否成立:部分成立(核心空白成立,但需重新定位)。**

"完全没有组件消融证据"这一强表述**不成立**:AHE 已给出单系统内的组件换入(swap-in)消融(工具/中间件/长期记忆增益显著、单独换 system prompt 反而回退),Yu & Desell 给出工具面 x 任务域 x agent 设计的交叉消融,CODESKILL 给出 skill 面内部生命周期消融,PAST-Bench 给出记忆/经验面的配对开/关受控对照,Ben Sghaier et al. 给出真实 harness 版本演化中组件敏感度的观察性证据。**但这些证据是碎片化的:各自只覆盖单一面、单一系统或观察性数据,且几乎全部只测收益不测风险。** 到 2026-08 为止,没有任何工作在同一 coding harness 上、固定进化算法与预算、对 system prompt / memory / skills / 工具定义 / workflow / 代码本体 六类面做"开放哪个面进化"的前瞻性交叉消融,并同时量化收益(任务成功率/效率)与风险(回归率、安全衰减、harness 膨胀)。综述《Self-Evolving Coding Agents》亦佐证:产品级进化能力普遍缺乏隔离消融,harness 膨胀与可逆性被列为开放问题。**因此,论文定位应从"首个组件消融"收窄为"首个跨面、收益/风险双轴、预算受控的可编辑面消融基准",该空白真实且可辩护。**

---

## 2. 可编辑面对照表(截至 2026-08)

| 工作 | 年份 | 开放哪些面 | 粒度 | 进化算法 | 安全机制 |
|---|---|---|---|---|---|
| **AHE**(Lin et al.) | 2026 | system prompt、tool description、tool implementation、middleware、skill、sub-agent 配置、长期记忆 | **7 组件,文件级暴露** | 可观测性驱动:trace 蒸馏为结构化证据 → 可验证预测 → 编辑 | 组件显式化 + 可回滚(revertible);编辑需附可验证预测 |
| **Self-Harness**(Zhang et al.) | 2026 | instructions、tools、verification guidance、memory sources、subagents、skills、runtime policies | **有界可编辑面**(harness 定义文件中声明的配置点) | 弱点挖掘 → harness 提案 → 提案验证 | 回归测试门禁;只能改声明过的面 |
| **Meta-Harness**(Lee et al.) | 2026 | 整个 harness 代码 | **全代码库**(外层循环) | coding agent 以文件系统访问历史候选(源码+分数+trace)并提出新候选 | 外层评分筛选;无组件级护栏 |
| **DGM**(Zhang et al.) | 2025 | 自身 agent 代码库 | 全代码库 | 基于 benchmark 表现的开放式进化 + archive | sandbox;archive 保留谱系可回溯 |
| **SICA**(Robeyns et al.) | 2025 | 自身代码库 | 全代码库 | 自我改进循环(基于基准得分选择) | 有限(实验环境隔离) |
| **Harness Updating ≠ Benefit**(Lin et al.) | 2026 | prompts、skills、memories、tools | 更新类型级(4 类) | 多模型对照的自更新 | 无(分析型工作) |
| **LLM-as-Code**(Qi et al.) | 2026 | harness 即代码,全部可编程 | 全代码(harness 表达为可执行程序) | agentic programming | 无显式 |
| **SIA**(Hebbar et al.) | 2026 | harness + 模型权重 | 两大面(harness 整体 / weights) | 自改进闭环 | 未详述 |
| **HarnessForge**(Chen et al.) | 2026 | harness 配置 + 策略(policy) | harness 整体 | harness 与 policy 联合进化 | 未详述 |
| **EvolveNet**(Nie et al.) | 2026 | harness 配置 | harness 整体 | 多 agent 协作进化 | 未详述 |
| **AutoSaddler**(Park et al.) | 2026 | harness(prompt/规则等持久更新) | 更新条目级 | trace 深度诊断 → 结构化干预 → 泛化感知选择 | 泛化感知选择(防过拟合) |
| **CODESKILL**(Li et al.) | 2026 | 仅 skills(skill bank) | 单面,skill 条目级(双粒度:event-driven / task-level) | 训练的 skill 管理模型:extraction → evolution → maintenance | maintenance 控制 bank 规模(add/merge/drop) |
| **SkillClaw**(Ma et al.) | 2026 | 仅 skills | 单面,跨 agent 集体演化 | agentic evolver | 未详述 |
| **ACE / GEPA / DSPy / TextGrad** | 2023-2025 | 仅 prompt/context | 单面(文本) | 程序化优化(反思梯度/进化搜索/编译) | 无(离线优化) |
| **AWM**(Wang et al.) | 2024 | 仅 workflow(记忆中的流程) | 单面 | 从 trace 归纳 workflow | 无 |
| **Claude Code(产品)** | 2025-2026 | CLAUDE.md、memory、skills、hooks、MCP 工具 | 配置面(核心循环闭源不可改) | 人在环 + auto-memory | 权限系统、hooks 审批 |
| **Misevolution**(Shao et al.) | 2025 | (分析对象)memory、tools、workflow | — | — | 提出风险分类:安全对齐衰减、有毒工具进化等 |

粒度谱系:**单面**(ACE/CODESKILL/SkillClaw/AWM)→ **有界多面**(Self-Harness / Harness Updating)→ **显式组件全集**(AHE 7 组件)→ **全代码库**(Meta-Harness / DGM / SICA / LLM-as-Code)。综述(Hu et al. 2026)将进化目标归为六类(framework / experience & repo memory / skill & tool / model / workflow & topology / environment & context),与上述谱系正交。

---

## 3. 已有消融证据盘点与空白点核实

### 3.1 已有证据(按组件)

| 组件 | 收益证据 | 风险证据 | 证据强度 |
|---|---|---|---|
| **工具定义/实现** | AHE Table 3(换入进化后工具面,增益显著);Yu & Desell(工具面选择 x 任务域 x agent 设计交叉消融,restricting 到 execute_code 的利弊由 regime 与设计共同决定) | Misevolution(工具进化可引入漏洞) | **较强**(唯一有双向证据的面) |
| **长期记忆/经验** | AHE Table 3(记忆面换入有增益);PAST-Bench(persistence 开/关配对对照,7 模型 x 4 框架,提升真实但按能力维度不均匀,且通路证据与表面增益分离) | Misevolution(记忆污染→安全对齐衰减);综述指出经验库会陈旧/冗余/被失败轨迹污染 | **较强** |
| **skills** | CODESKILL Table 2(生命周期逐级消融:双粒度互补,evolution +2.1 平均通过率,maintenance 牺牲 ~2% 换 bank 减半);SkillClaw(集体演化) | CODESKILL(无 maintenance 时 skill bank 从 676 膨胀到 1252——膨胀本身即风险信号) | **中等**(有面内消融,缺跨面对照) |
| **system prompt** | AHE Table 3:**单独换入进化后的 system prompt 反而回退**——目前唯一直接的"某面单独开放为负收益"证据;ACE/GEPA 等证明离线 prompt 优化有效(但非自进化闭环) | 综述:失败教训被无限追加为 prompt 规则 → harness 膨胀 | **中等偏弱**(单系统单基准) |
| **workflow/中间件** | AHE Table 3(middleware 换入有增益);AWM(workflow 归纳有效) | 综述:路由条件堆积、耦合上升 | **弱** |
| **代码本体** | DGM/SICA/Meta-Harness 证明全代码进化整体有效;但**无人对比"全代码 vs 受限面"在同预算下的差异** | DGM 已报告 reward hacking 式行为;Cordis 指出运行时组件修改缺乏时序可组合性 | **弱**(只有整体循环证据) |

### 3.2 相邻但不等价的消融

- **Meta-Harness** 的消融只针对提案者的信息接口(scores-only / +summary / full traces),不是 harness 组件。
- **AutoSaddler** 的消融针对方法阶段(诊断/干预/选择),不是可编辑面。
- **Harness Updating ≠ Benefit**(Lin et al. 2026)按更新类型分析,核心发现是"更新能力与受益能力解耦、受益随模型能力非单调"——提供了重要的模型能力协变量,但没有按面固定预算消融。
- **Ben Sghaier et al.** 是观察性纵向研究(固定模型、跨真实 harness 版本),定位出 LLM Provider 与 Context Management 组件回归风险最高,但无法区分组件效应与版本间混杂变更。
- **Raj et al.(Model or Harness?)** 提供失败归因到 harness 具体环节的分类法——是消融实验的测量工具,而非消融本身。

### 3.3 核实过程(方法与来源)

1. 深读库内三大代表(AHE / Self-Harness / Meta-Harness)全文,确认三者消融范围:AHE 有组件换入消融(Table 3),后两者无组件级消融。
2. Semantic Scholar API 检索("harness component ablation"、"editable surface self-evolving agent"、"scaffold ablation coding agent" 等)+ websearch 覆盖 2025-01 至 2026-08,新增 15 篇归档(见 `raw/papers/index_002_B1.yaml`)。
3. 交叉验证:综述《Self-Evolving Coding Agents》(2608.03392,2026-08-20 v2)的六类分类与开放问题章节明确指出:(a) 产品文档"describes the mechanism without reporting an ablation that isolates its effect";(b) harness 膨胀、可逆性、removal-as-first-class-operation 是开放问题——均支持本方向的立项动机,且该综述本身未做也未引用任何跨面消融。
4. 注意网络限制:arxiv.org 直连被重置,PDF 经 alphaxiv 镜像下载,已在 index_002_B1.yaml 中注明。

**核实结论**:单面消融与观察性证据存在(故"完全空白"不成立);**跨面 x 收益/风险双轴 x 固定进化预算的前瞻性消融不存在**(故核心空白成立)。

---

## 4. 立项方案

### 4.1 研究问题表述

> **RQ1**:对 Claude Code 类 coding harness,在固定进化算法与预算下,单独开放每一类可编辑面(system prompt / 长期记忆 / skills / 工具定义 / workflow / 代码本体)自我进化,各自的收益(任务成功率、步数/成本)与风险(held-out 回归率、安全衰减、harness 膨胀)是多少?
> **RQ2**:是否存在"最小充分集"——一个面的子集,其组合收益接近全开放,而风险显著低于全开放(尤其低于全代码库开放)?
> **RQ3**:各面的收益/风险比如何随基座模型能力与任务域(regime)变化?(接 Lin et al. 的非单调性与 Yu & Desell 的 regime 交互)

### 4.2 消融实验设计草案

**Harness 选择**(2 个,兼顾生态代表性与可控性):

1. **开源 Claude Code 类 harness**(OpenHands 或 AHE 式文件暴露组件的自建 harness):六面全部可编辑,支持"代码本体"条件;
2. **Claude Code 本体**(配置面子集:CLAUDE.md / memory / skills / hooks / MCP 工具描述):验证结论对闭源产品配置面的外推性(此臂不含代码本体条件)。

**进化算法(固定)**:采用 Self-Harness 式循环(弱点挖掘 → 提案 → 回归验证)统一驱动所有条件;提案 agent 只被授权写入当前条件开放的面(文件级 ACL 强制)。

**实验条件(主 harness 臂,共 9 条件)**:

| 条件 | 开放面 |
|---|---|
| C0 | 无(冻结基线) |
| C1-C6 | 单面:system prompt / 记忆 / skills / 工具定义 / workflow(hooks+循环策略)/ 代码本体 |
| C7 | 六面全开 |
| C8 | 最小充分集候选(由 C1-C6 结果选 top-2 组合,自适应加跑) |

(预算允许时补 leave-one-out 六条件,检测面间交互。)

**任务集**:SWE-bench Verified 抽样 100 题(60 train / 40 held-out,按 repo 切分防泄漏)+ Terminal-Bench 2 全量(held-out 域外泛化)。进化只见 train;held-out 与域外集全程冻结。

**进化预算(固定)**:每条件 15 轮迭代,每轮在 train 上跑 20 题并允许 ≤3 次编辑提案;3 个随机种子。

**评估协议**:

- 收益:held-out resolve rate Δ、平均步数/token 成本 Δ(相对 C0);
- 风险:(a) held-out 回归率(C0 能解而该条件不能解的题占比);(b) 安全探针:进化后 harness 面对 Misevolution 式诱导(污染反馈、诱导性任务)的失败率;(c) 膨胀度:各面字节数/条目数增长曲线;(d) 可逆性:随机回滚最后 k 次编辑后性能恢复度;
- 通路证据(借鉴 PAST-Bench):trace 级验证增益是否真经过被开放面(而非 prompt 泄漏等旁路)。

**安全护栏**:全程容器沙箱;每次编辑 git 提交(可回滚);编辑 diff 经规则审计(禁网络外呼、禁改评估代码);评估 key 与 train 环境物理隔离;代码本体条件额外加静态扫描 + 资源限额。

### 4.3 成本估算

- 运行量:主臂 9 条件 x 3 seeds x(15 轮 x 20 train 题 + 3 次全量评估 x 140 题)≈ 9 x 3 x 720 ≈ **19,500 次 agent 运行**;Claude Code 臂(5 条件)≈ 7,500 次;合计 ~27,000 次。
- 单次运行成本(Sonnet 级模型,SWE-bench 均值)≈ $0.5-1.5 → **API 成本约 $15k-40k**;取中值预算 **$25k**。
- 降本选项:train 题降至 12/轮、种子降为 2、Claude Code 臂砍半 → 可压至 ~$10k;或用开源模型(GLM/Qwen coder 级)先跑全矩阵、闭源模型只复现关键条件。
- 时间:并行度 20 下约 3-4 周(含 1 周基建)。

### 4.4 最像的竞品与差异化

| 竞品 | 它做了什么 | 我们的差异 |
|---|---|---|
| **AHE Table 3**(最像) | 把进化终态的单组件**换入** seed harness,事后归因增益 | 我们做**前瞻性开放消融**(限制进化只能碰某面,而非事后换入)——回答"开放什么"而非"哪部分变了";且加风险轴、多 harness、固定预算、交互条件 |
| Harness Updating ≠ Benefit | 更新能力 vs 受益能力,按模型能力轴 | 我们按**面**做轴,模型能力作为协变量(RQ3 直接对话其非单调性发现) |
| Yu & Desell | 工具面 x regime 交叉消融(静态配置,无进化) | 我们是进化闭环下的六面矩阵,工具面结论可与其对表 |
| PAST-Bench | 记忆/经验单面开关 + 逐机制消融(个人助理域) | 借鉴其配对对照与通路证据方法学,搬到 coding harness 六面 |
| Ben Sghaier et al. | 观察性组件敏感度(真实版本演化) | 我们是受控实验,可做因果归因;其发现(context management 高风险)可作先验假设 |

---

## 5. 风险与不确定性

1. **结果可能"无聊"**:若六面收益排序与 AHE Table 3 完全一致(工具/记忆/中间件 > prompt),增量贡献仅剩风险轴与预算控制——对策:把风险/安全轴和最小充分集(RQ2)做成一等公民,而非附属。
2. **进化循环高方差**:自进化实验 run-to-run 方差大(PAST-Bench 已报告 Δ 差异小于 run 间波动),3 seeds 可能不够——需预实验估方差,必要时增 seed 或用配对检验。
3. **面间交互被单面消融低估**:AHE 已示组件组合效应非线性;C8/leave-one-out 只能部分覆盖,全因子(2^6)不可负担。
4. **Claude Code 闭源**:核心循环与代码本体不可改,该臂结论只覆盖配置面;开源臂与 Claude Code 行为差异可能被审稿人质疑外推性(可引 Dive into Claude Code 论证组件同构)。
5. **基准污染与过拟合**:进化系统对公开基准的泄漏敏感(综述已列为首要开放问题);repo 级切分 + 域外 Terminal-Bench 只能缓解,不能根除。
6. **领域时效风险**:该方向 2026 年产出密度极高(半年内 ≥15 篇 harness 进化论文),存在被抢发可能;AHE 团队做前瞻版消融是最可能的竞争者,宜快速立项。
7. 模型版本漂移:实验周期内 API 模型静默更新会破坏可比性——需锁定 snapshot 版本。

---

## 6. 参考文献(均在 raw/papers/)

**核心对照系统**

1. Lin et al., 2026. Agentic Harness Engineering (AHE). `raw/papers/2026-lin-agentic-harness-engineering.pdf`
2. Zhang et al., 2026. Self-Harness. `raw/papers/2026-zhang-self-harness.pdf`
3. Lee et al., 2026. Meta-Harness. `raw/papers/2026-lee-meta-harness.pdf`
4. Zhang et al., 2025. Darwin Gödel Machine. `raw/papers/2025-zhang-darwin-godel-machine.pdf`
5. Robeyns et al., 2025. SICA. `raw/papers/2025-robeyns-sica.pdf`

**消融/对照证据(本轮新增)**

6. Yu & Desell, 2026. When Does Restricting a Coding Agent to execute_code Help? arXiv:2607.10569. `raw/papers/2026-yu-execute-code-ablation.pdf`
7. Li et al., 2026. CODESKILL. arXiv:2605.25430. `raw/papers/2026-li-codeskill.pdf`
8. Xue et al., 2026. PAST-Bench. arXiv:2608.04003. `raw/papers/2026-xue-past-bench.pdf`
9. Ben Sghaier et al., 2026. How Agent Harness Evolution Shapes Coding Agent Quality. arXiv:2607.03691. `raw/papers/2026-bensghaier-harness-evolution-quality.pdf`
10. Lin et al., 2026. Harness Updating Is Not Harness Benefit. arXiv:2605.30621. `raw/papers/2026-lin-harness-updating-not-benefit.pdf`

**可编辑面谱系(本轮新增)**

11. Hu et al., 2026. Self-Evolving Coding Agents (Survey). arXiv:2608.03392. `raw/papers/2026-hu-self-evolving-coding-agents-survey.pdf`
12. Qi et al., 2026. LLM-as-Code. arXiv:2606.15874. `raw/papers/2026-qi-llm-as-code.pdf`
13. Hebbar et al., 2026. SIA. arXiv:2605.27276. `raw/papers/2026-hebbar-sia.pdf`
14. Chen et al., 2026. HarnessForge. arXiv:2606.01779. `raw/papers/2026-chen-harnessforge.pdf`
15. Nie et al., 2026. EvolveNet. arXiv:2608.04968. `raw/papers/2026-nie-evolvenet.pdf`
16. Park et al., 2026. AutoSaddler. arXiv:2608.23041. `raw/papers/2026-park-autosaddler.pdf`
17. Ma et al., 2026. SkillClaw. arXiv:2604.08377. `raw/papers/2026-ma-skillclaw.pdf`
18. Liu et al., 2026. Dive into Claude Code. arXiv:2604.14228. `raw/papers/2026-liu-dive-into-claude-code.pdf`
19. Macedo, 2026. What makes a harness a harness. arXiv:2606.10106. `raw/papers/2026-macedo-what-makes-a-harness.pdf`
20. Raj et al., 2026. Model or Harness? arXiv:2607.28802. `raw/papers/2026-raj-model-or-harness.pdf`

**风险与优化基线(库内既有)**

21. Shao et al., 2025. Misevolution. `raw/papers/2025-shao-misevolution.pdf`
22. Zhang et al., 2025. ACE. `raw/papers/2025-zhang-ace.pdf`
23. Agrawal et al., 2025. GEPA. `raw/papers/2025-agrawal-gepa.pdf`
24. Khattab et al., 2023. DSPy. `raw/papers/2023-khattab-dspy.pdf`
25. Yuksekgonul et al., 2024. TextGrad. `raw/papers/2024-yuksekgonul-textgrad.pdf`
26. Wang et al., 2024. Agent Workflow Memory. `raw/papers/2024-wang-agent-workflow-memory.pdf`

**剪藏**:`Clipping/2026-08-28_arxiv_past-bench-continualskillbench-abstracts.md`

---

*survey-agent-B1 · 完成于 2026-08-29 01:28*
