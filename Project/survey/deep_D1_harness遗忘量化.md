# D-1 深挖底稿:harness-level forgetting 量化与 retention 回归集构建

> openspec change-002 · 方向 D-1(D1-1 相关工作全查 / D1-2 回归集构建方法 / D1-3 与 A5/C6 关系)
> 信息截至 2026-08-28。本轮新归档论文 17 篇(见 raw/papers/index_002_D1.yaml),网页剪藏 2 份(Clipping/)。

---

## 1. 结论先行

**空白点判断:部分成立。** "harness 更新导致既有行为回归"这一现象本身已不再是无人区——HCL(2026-08)正式命名并测量了 harness-level forgetting,且 2026 年上半年已有一批工作在各组件层独立撞见同一现象:HarnessFix 给 harness 补丁加了回归验收门、Adaptive Auto-Harness 实证"密集原地更新使准确率早期见顶后下滑"、SkillFlow 观察到"缺陷技能固化入库后把单次错误变成跨任务回归"、SkillLearnBench 发现纯自反馈技能迭代产生 recursive drift、ACE 记录了 context collapse(一步重写把 18,282 token 的积累压成 122 token,准确率 66.7→57.1)、Misevolution 量化了记忆积累导致的安全对齐衰减(Refusal Rate 99.4%→54.4%)。因此**"现象层"的空白已关闭**。但上一轮判断的核心仍然成立:**(a) 没有任何公开的、以"harness 更新"为被测变更单元的 retention 回归基准;(b) 回归集构建方法学(用例来源、统计效力、自动判定)是彻底空白**——HCL 自己承认其有限 anchor set 无法覆盖未观测回归、把 "efficient retention evaluation" 列为 open challenge;HarnessFix 的验收只用通用 held-out 集;工业界(AgentEval)只有事故驱动回归用例,不覆盖习得能力的保持。可立项,但定位必须从"发现现象"转为"评测方法学与公开回归集"(类比 model editing 领域中 RippleEdits/Gu et al. 相对 MEMIT 的位置)。

## 2. 相关工作全景表

### 2.1 直接触及"harness/明文层更新 → 行为回归"的工作

| 工作 | 年份 | 触及哪种明文层回归 | 量化/防护方法 | 局限 |
|---|---|---|---|---|
| **HCL**(Kang et al., 2608.19013) | 2026 | 统一四组件(Task Interface / Experience Memory / Capability Map / Adaptive Router)更新的回归,正式命名 harness-level forgetting | anchor set(每旧任务 80 条,存原始输入+成功判据),提交门槛 Dn≤Bn(Dn=原本通过、候选下失败的 anchor 数);Avg. Fgt. 指标;b∈{0,1,3,∞} 的 stability–plasticity 扫描 | anchor 是**内部机制而非公开基准**;无统计功效分析;b=0 仍有残余遗忘(anchor 有限覆盖);自建任务流,非真实 coding harness |
| **HarnessFix**(Chen et al., 2606.06324) | 2026 | harness 代码/prompt 补丁引入的回归(ETCLOVG 七层) | regression-aware acceptance:TargetImprovement(ΔD≥δmin)+ RegressionBound(Rnew≤rmax,Rnew=原 harness 通过而补丁失败的验证任务数);消融证明去掉该门在全部四基准掉分 | 验证集是通用 held-out(50 任务量级),非 retention 专用;阈值 δmin/rmax 启发式;不研究回归集本身该怎么建 |
| **Adaptive Auto-Harness**(Liu et al., 2606.01770) | 2026 | 单一 harness 被反复密集更新的脆化:所有 stopping budget 都"peak and decline";技能跨任务误触发(news_from_future.md 在 sports 任务有用、在 politics 任务误击) | 不做守护,改架构回避:harness 树(历史分支保留不覆写)+ solve-time 路由;分解 evolution loss / adaptation loss | 回避而非量化回归;预测市场/CTF 等流,非 coding;无 retention 指标 |
| **Harness Updating ≠ Harness Benefit**(Lin et al., 2605.30621) | 2026 | 更新收益的模型依赖性:同一 harness 更新在弱模型上因"不激活工件/不忠实执行"而失效 | 拆分 harness-updating 与 harness-benefit 两能力;7 模型×3 基准 | 测收益不测回归;但含关键含义:**retention 判定必须绑定执行模型**,换模型后回归集结论不可迁移 |
| **SkillFlow**(Zhang et al., 2604.17308) | 2026 | 技能库演化冲突:弱模型把缺陷技能固化入库(skill enshrinement)反复复用,单错变跨任务回归;多模型技能演化后净退步(GPT-5.3-Codex −6.02pp) | 166 任务/20 工作流族的 lifelong 协议,轨迹+rubric 驱动 patch;测 discovery/repair/transfer 失败模式 | forgetting 只是观察不是协议核心;无更新级归因;技能单组件 |
| **SkillLearnBench**(Zhong et al., 2604.20087, COLM'26) | 2026 | 纯 self-feedback 技能迭代产生 recursive drift(递归漂移) | 技能质量/执行轨迹/任务结果三级评测 | 20 任务规模小;drift 定性为主;不测跨任务回归 |
| **ContinualSkillBench**(Guan et al., 2608.03874) | 2026 | 真实 coding harness(Codex CLI/Claude Code 改造)上技能库膨胀、质量参差 | 顺序执行 vs 独立执行 vs 纯 ICL 对照(0.605 vs 0.602:ICL 与显式技能维护平均相当) | 不测 retention;聚焦"演化有没有用"而非"演化破坏了什么" |
| **PAST-Bench**(Xue et al., 2608.04003) | 2026 | 持久状态的 update 正确性(过时状态必须被替换,7 场景/51 episode) | 开关持久化的配对对照 + save/retrieve/update 通路归因 | 测"更新是否生效",不测"更新是否破坏无关行为"(与 retention 恰好互补) |
| **ACE**(Zhang et al., 2510.04618, ICLR'26) | 2025 | context collapse:LLM 整体重写积累 context 时突然坍缩(18,282→122 token,acc 66.7→57.1<无适配基线 63.7);brevity bias | 以增量结构化更新替代整体重写来预防 | 预防设计,无回归度量;单 context 组件 |
| **Misevolution**(Shao et al., 2509.26354) | 2025 | 记忆积累的副作用:SE-Agent 三轮记忆蒸馏后 RedCode RR 99.4%→54.4%;记忆导致部署期 reward hacking(退款-好评错误启发式) | 演化前后安全基准对照;100 轮纵向 Unsafe Rate 追踪 | 只测安全维度回归,不测能力回归;无守护机制 |
| **Slipstream**(Chen et al., 2605.08580) | 2026 | compaction(harness 触发的明文重写)静默丢失后续所需信息且错误无声传播 | 轨迹接地验证:用 agent 在未压缩 context 上的后续行为作独立验证信号,判定候选摘要是否可接受 | 只覆盖 compaction 一种更新;在线验证而非回归集 |
| **MemRL / MemP**(2601.03192 / 2508.06433,经 HCL 复现) | 2026 | 记忆演化方法在 ALFWorld 任务流上 Avg. Fgt. 5.64 / 5.18(对照 RAG 1.74) | 被 HCL 用作基线,首次给出记忆方法的遗忘数值 | 数字出自 HCL 复现,方法本身无 retention 意识 |

### 2.2 方法论迁移源(非 harness 场景)

| 工作 | 年份 | 可迁移的方法论 |
|---|---|---|
| **Conversation Regression Testing**(Zamfirescu-Pereira et al., 2302.03154) | 2023 | 最早的"prompt 改动需在固定对话集上回归检查"概念(HCI 工具层雏形) |
| **(Why) Is My Prompt Getting Worse?**(Ma et al., 2311.11123) | 2023 | LLM API 演化下的回归测试重思:58.8% 场景存在回归;**单点回归率 10.9% 意味着逐用例判定信噪比极低,必须 slice 级统计**;回归集中于特定切片(90% 在 toxic 讨论)。注意方向相反:模型变、prompt 不变;D1 是模型冻结、明文变 |
| **RETAIN**(Dixit et al., 2409.03928, Adobe) | 2024 | 工业界 prompt 回归测试交互工具:行为差异可视化、错误发现辅助——回归"诊断 UX"参考 |
| **CASPER**(Muse, Briand et al., 2608.00378) | 2026 | LLM 系统回归测试的成本控制:单实例失败信息量不足→以语义切片为单位;变更感知的切片优先级排序(应对全量回归太贵) |
| **RippleEdits**(Cohen et al., 2307.12976) | 2023 | model editing 的涟漪效应评测:从每个编辑**系统生成波及探针**(逻辑关联事实须更新、无关事实不得动)——"从更新反推回归探针"的直接模板 |
| **Model Editing Can Hurt General Abilities**(Gu et al., 2401.04700) | 2024 | 编辑方法×通用任务矩阵的副作用量化范式;确立"编辑收益必须与保持性一起报告";另有 Butterfly Effect(2402.09656)证明少量编辑可致模型崩溃 |
| **MINJA**(Dong et al., 2503.03704)及 AgentPoison/MemoryGraft | 2025 | 对抗版记忆更新副作用:仅凭 query 即可注入恶意记忆(≈98% 成功),证明**记忆写入路径完全缺乏行为级验收**——D1 守护机制的安全动机 |
| **Adding Error Bars to Evals**(Miller, 2411.00640, Anthropic) | 2024 | 评测统计学:CLT 标准误、题目成组时的 clustered SE、**成对差检验**(大幅缩减所需样本)、功效分析——回归集规模计算的直接依据 |
| **Context rot 系**(Chroma 报告 Hong et al. 2025;Xia et al. 2606.29718;Classifier Context Rot 2605.12366) | 2025-26 | 概念区分:context rot 是**长度增长**导致的退化,不涉及更新;但其"行为机理诊断"手法(compaction/trimming/isolation 如何重塑行为)可借用 |
| **AgentEval**(开源工具,见 Clipping) | 2026 | 工业界已出现 agent 回归 CI 门禁:生产事故→脱敏→聚类→回放→最小化→人工审批→版本化 golden 用例;但**只有事故驱动用例,无习得能力 retention 用例** |

## 3. 空白点核实过程

1. **检索面**:Semantic Scholar API(prompt regression testing、memory editing side effects、skill library interference、agent retention benchmark 等 10+ 组关键词;期间多次 429 限流,部分改走 web 检索)+ web 检索("harness-level forgetting"、context rot、memory poisoning、retention suite 等)+ 反向滚雪球(精读 HCL 全文参考文献,由此挖出 Harness Updating≠Benefit、Adaptive Auto-Harness、HarnessFix、SkillFlow、SkillLearnBench、MemRL 等本轮最相关的一批 2026 工作)。
2. **深读核实 HCL 的真实边界**(全文 PDF,重点第 3-4 节):其 anchor set 每旧任务仅 80 条、按预设成功/失败比例抽样、仅供 Evaluator 评估;论文明确写道 "Preserving all anchors currently solved by Hn cannot guarantee unchanged behavior on historical cases not represented by An"(b=0 时仍有 0.39 Avg. Fgt.),结论处把 "efficient retention evaluation" 列为未解挑战。→ HCL 提供了**问题定义与机制原型**,没有提供**回归集方法学与公开基准**。
3. **核实 HarnessFix 的验收门**(全文 PDF §III-D):RegressionBound 用的是 2:1:2 切分出的通用验证集(如 SWE-bench Verified 50 题),不是 retention 专用集;消融(w/o regression-aware acceptance)在四基准全部掉分(57→53、9→8、37→33、38→35),证明回归门有实际价值——但论文不研究"验证集该怎么构成、多大、判定是否可靠"。
4. **专项检索"retention suite/benchmark for harness updates"**:未发现任何公开基准以 harness diff 为被测单元;最接近的是 PAST-Bench(测 update 生效性,不测波及)与 AgentEval(事故驱动 CI 门禁)。ContinualSkillBench/SkillFlow/LifelongAgentBench 把 forgetting 当聚合曲线报告,均不做更新级归因。
5. **结论**:现象已被命名、机制已有原型、痛点已被多方独立撞见(这反而证明时机成熟),但"量化方法学 + 公开 retention 回归集"仍无人做。空白以修正后的形式成立。

## 4. 立项论证

### 4.1 研究问题表述

> **RQ:当一个冻结模型的 agent harness 发生明文更新(memory 追加/改写、skill 增删改、指令文件编辑、compaction)时,如何以可控成本、可复现地量化该更新对既有可靠行为的破坏(harness-level regression),并据此构建首个公开的 retention 回归基准与守护协议?**

子问题:(1) 回归用例从哪来、如何带上可执行的验收判据;(2) 非确定性下回归判定的信噪比与所需规模(统计效力);(3) 不同更新算子(append vs rewrite vs delete vs compact)与不同组件(memory/skill/指令)的回归率是否有系统差异;(4) 回归是否局域(波及任务与更新内容的语义距离关系,类比 RippleEdits 的 locality);(5) 守护机制(HCL 门槛、HarnessFix 验收、切片优先级)在同一回归集上的横向比较。

### 4.2 retention 回归集构建方案草案

**用例来源(三路互补)**:
1. **历史成功轨迹回放**(主体):从 agent 运行日志抽取曾成功的 (任务输入, 环境快照, 验收判据) 三元组,判据必须可执行(coding 场景=测试通过;HCL anchor 的做法,AgentEval 证明工程可行)。冷启动可用基准任务流(SWE-bench 子集)先跑出成功集。
2. **更新反推探针**(创新点,借 RippleEdits):对每条被更新的 harness 工件,自动生成"该工件应支配的行为"探针(这条 memory 被引用时应产生什么行为、这个 skill 的触发条件与规定步骤)——使回归集能随 harness 内容增长而增长,并支持 locality 分析。
3. **语义等价扰动**(稳健性):对同一用例生成改写变体,区分"真回归"与"prompt 敏感性噪声"。

**规模与统计效力**(依 Miller 2411.00640):
- 逐用例判定不可靠(Ma et al.:单点回归率 10.9% 属噪声量级)→ 每用例 k=3–5 次重复取多数票,把单用例翻转噪声压到低位;回归判定在集合级做成对差检验(同一用例在 H_n 与 H_{n+1} 下配对,McNemar/paired-t)。
- 量级估算:二值结果 σ²=p(1−p)≈0.24,检出净回归 δ=5pp、80% power、α=0.05,独立设计需 n≈2(z_{0.975}+z_{0.8})²σ²/δ² ≈ 300–400 用例;成对设计在用例间相关 ρ≈0.5 时约减半(~150–200);检出 10pp 约 50–100。→ **HCL 的 80 anchors/task 恰在"只能检出 ~10pp 级回归"的边缘,这本身就是可发表的功效分析结论**。任务按族分组时用 clustered SE 防低估。
- 成本控制:全量回归每次提交都跑不现实 → 变更感知的切片优先级(CASPER):按更新工件与用例的语义关联度排序,预算内优先跑高风险切片。

**自动判定行为回归(三层)**:结果级(可执行 verifier,金标准)→ 轨迹级(关键不变量:必须/禁止的工具调用、文件触碰,借 HarnessFix 的 failure attribution 与 SkillFlow 的 rubric)→ LLM-judge(兜底,须报告与人工标注的对齐率并抽样审计)。回归 = 配对多数票结果从通过翻转为失败,或连续指标成对差超阈。

### 4.3 实验设计雏形

- **环境**:开源 coding harness(OpenHands SDK 或 mini-swe-agent 加装 memory/skill 层,保证可控可复现;与 C6 共享 SWE 任务流),组件=指令文件/MEMORY.md/skills 目录。
- **操作变量**:受控更新算子矩阵——{append, rewrite, merge, delete, compact} × {memory, skill, 指令};算子由真实 auto-memory 流水线产生(跑任务流让 harness 自然演化)+ 注入式合成更新(控制强度)。
- **指标**:URR(update regression rate:单次更新导致的回归用例比例)、Retention@t(任务流第 t 步对历史成功集的保持率)、locality 曲线(回归用例与更新内容的语义距离分布)、净学习收益(new-task gain − retention loss,呼应 HCL 的 stability–plasticity)、守护成本(门禁的额外 token/时间)。
- **基线与对照**:no-guard(每更新直接提交)、HCL Evaluator(b=0/1/3/∞)、HarnessFix 式验收(δmin/rmax)、CASPER 式预算受限门禁;跨 2-3 个模型验证 Lin et al. 的"retention 结论绑定执行模型"预言。
- **预期主张**:(1) 首个公开 harness retention 回归基准 + 构建工具链;(2) 各更新算子/组件的回归率排序(工程指导:哪类自动更新最危险);(3) 回归集规模-功效曲线;(4) 现有守护机制的首次横向比较。

### 4.4 最像的竞品与差异化

| 竞品 | 它做什么 | 我们的差异 |
|---|---|---|
| **HCL**(最像) | 问题定义 + 守护机制,anchor 为内部私有组件 | 我们做**评测方法学与公开基准**:回归集构建协议、功效分析、更新级归因、守护机制横评;HCL 变成我们的被测方法之一。类比:HCL 之于我们 ≈ MEMIT 之于 RippleEdits/Gu et al. |
| **HarnessFix** | 修复流水线内嵌回归验收 | 同上;且它以 harness 代码补丁为对象,我们以明文工件(memory/skill/指令)的日常演化为对象 |
| **SkillFlow / ContinualSkillBench / LifelongAgentBench** | lifelong 协议下报告聚合 forgetting/演化曲线 | 它们的变更单元是"任务流推进",我们的是"单次 harness diff";它们无归因、无回归集协议、无守护比较 |
| **PAST-Bench** | 更新生效性(该改的有没有改) | 我们测更新波及性(不该变的有没有变)——正反两面,可互引 |

## 5. 与 A-5 / C-6 的关系判断

**明确判断:与 A-5 互补,与 C-6 近邻且有合并选项;D1 可独立成篇,条件是把重心放在"量化方法学 + 回归集协议 + 守护机制横评",而不是再造一个 lifelong 基准。**

- **vs A-5(harness 记忆基准)**:互补,竞争风险低。A5 谱系(LongMemEval、Harness the Memory 的 26 项指标等)测的是"固定 harness 下记忆基质的读写/召回/效率",没有任何 update-regression 维度(核实过 Harness the Memory 全文,retention 仅作为"raw history 参照基质"出现)。retention 可以作为 A5 新基准的一个指标维度被吸收,但 D1 的核心贡献(以 harness diff 为变更单元、回归集构建协议、守护横评)不依赖也不包含于 A5。若 A5 立项,建议 A5 引用 D1 的 retention 协议作为其一个 track。
- **vs C-6(coding harness lifelong 基准)**:关系最近,需主 agent 协调边界。lifelong 基准天然包含 forgetting 指标(LifelongAgentBench 已有、SkillFlow/ContinualSkillBench 已报),若 C6 落地为"SWE 任务流 lifelong 基准",D1 的 retention 回归协议是其最自然的核心组件(任务流中周期性重评历史成功集)。两个选择:**(a) 合并成一篇**"lifelong coding-harness 基准,以 retention 回归协议为核心创新"——更强、更完整,推荐;**(b) D1 独立成篇**,聚焦方法学(功效分析、更新级归因、守护横评),用现成小任务流即可,不必自建完整 lifelong 基准——风险更低、更快,但单独可能被审稿人问"为什么不做成完整基准"。倾向 (a),由 synthesis 阶段定夺。

## 6. 风险与不确定性

1. **竞速风险(最高)**:HCL 团队在结论里把 efficient retention evaluation 点名为 open challenge,大概率在做后续;HarnessFix/AAH 团队(Amazon 系)也在同一水域。窗口估计 6-12 个月,需快。
2. **回归判定信噪比**:agent 任务非确定性大(Ma et al. 单点 10.9% 翻转),k 次重复×数百用例×每次更新都要评 → 算力/费用是主要成本项;切片优先级只能缓解。若信噪比压不下来,"回归率排序"类结论可能不显著。
3. **闭源 harness 不可控**:Claude Code 的 auto memory 等真实场景无法直接插桩,只能在开源复刻(OpenHands/mini-swe-agent 改装)上做,外推有效性会被质疑;需引 branch D 的机制盘点论证复刻忠实度。
4. **操作空间爆炸**:更新算子×组件×模型×守护机制的矩阵大,须提前砍到可负担子集(建议先 memory+skill 两组件、3 算子、2 模型)。
5. **与 C6/A5 的选题重叠**由主 agent 在 synthesis 收敛,本稿仅给出边界建议。
6. **检索局限**:S2 API 本轮多次限流,引文网络(如 HCL 的被引)未能穷尽;export.arxiv.org/arxiv.org 直连被网络重置,PDF 经 alphaXiv 资产站镜像下载(已核对首页与 arXiv 版本一致)。

## 7. 参考文献(本轮新归档 → raw/papers/)

1. Kang et al., 2026, Harness Continual Learning, arXiv:2608.19013 → raw/papers/2026-kang-harness-continual-learning.pdf(change-001 已归档,本轮深读)
2. Chen et al., 2026, HarnessFix: Diagnosing and Repairing Harness Flaws, arXiv:2606.06324 → raw/papers/2026-chen-harnessfix.pdf
3. Liu et al., 2026, Adaptive Auto-Harness, arXiv:2606.01770 → raw/papers/2026-liu-adaptive-auto-harness.pdf
4. Lin et al., 2026, Harness Updating Is Not Harness Benefit, arXiv:2605.30621 → raw/papers/2026-lin-harness-updating-not-benefit.pdf
5. Zhang et al., 2026, SkillFlow, arXiv:2604.17308 → raw/papers/2026-zhang-skillflow.pdf
6. Zhong et al., 2026, SkillLearnBench, arXiv:2604.20087 → raw/papers/2026-zhong-skilllearnbench.pdf
7. Guan et al., 2026, ContinualSkillBench, arXiv:2608.03874 → raw/papers/2026-guan-continualskillbench.pdf
8. Xue et al., 2026, PAST-Bench, arXiv:2608.04003 → raw/papers/2026-xue-past-bench.pdf
9. Chen et al., 2026, Slipstream, arXiv:2605.08580 → raw/papers/2026-chen-slipstream.pdf
10. Xia et al., 2026, Diagnosing and Mitigating Context Rot in Long-horizon Search, arXiv:2606.29718 → raw/papers/2026-xia-context-rot-search.pdf
11. Muse, Briand et al., 2026, CASPER, arXiv:2608.00378 → raw/papers/2026-muse-casper.pdf
12. Ma, Yang & Kästner, 2023, (Why) Is My Prompt Getting Worse?, arXiv:2311.11123 → raw/papers/2023-ma-prompt-regression-llm-apis.pdf
13. Dixit et al., 2024, RETAIN, arXiv:2409.03928 → raw/papers/2024-dixit-retain.pdf
14. Zamfirescu-Pereira et al., 2023, Conversation Regression Testing, arXiv:2302.03154 → raw/papers/2023-zamfirescu-conversation-regression-testing.pdf
15. Cohen et al., 2023, Ripple Effects of Knowledge Editing, arXiv:2307.12976 → raw/papers/2023-cohen-ripple-effects.pdf
16. Gu et al., 2024, Model Editing Can Hurt General Abilities, arXiv:2401.04700 → raw/papers/2024-gu-model-editing-hurts.pdf
17. Dong et al., 2025, MINJA, arXiv:2503.03704 → raw/papers/2025-dong-minja.pdf
18. Miller, 2024, Adding Error Bars to Evals, arXiv:2411.00640 → raw/papers/2024-miller-error-bars-evals.pdf

已归档旧文(本轮深读引用):2025-zhang-ace.pdf、2025-shao-misevolution.pdf、2026-huang-harness-memory.pdf、2025-zheng-lifelongagentbench.pdf、2026-lin-agentic-harness-engineering.pdf。
网页剪藏:Clipping/2026-08-28_chroma_context-rot.md(context rot 出处报告)、Clipping/2026-08-28_github_AgentEval_README.md(工业界回归门禁)。
仅引用未归档:Butterfly Effect of Model Editing(2402.09656)、MemRL(2601.03192)、Classifier Context Rot(2605.12366)、AgentPoison(2407.12784)、MemoryGraft(2025-12)。

---

落款:survey-agent-D1 · 2026-08-28 17:52(UTC)
