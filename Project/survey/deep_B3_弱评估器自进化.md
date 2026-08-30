# Deep-Dive B3:弱评估器下的自进化——无快速 verifier 任务的进化信号构造

> openspec change-002 · 方向 B-3 · 检索窗口截至 2026-08-28
> 上游底稿:`Project/survey/branch_B_agent自进化.md`(其"下一层待深挖问题"第 3 条即本题)
> 新增归档 21 篇,登记于 `raw/papers/index_002_B3.yaml`;网页剪藏 2 篇于 `Clipping/`

---

## 1. 结论先行

**"几乎空白"的判断不成立——需修正为"部分空白"。** 2025 下半年至 2026 年,"无快速 verifier 任务如何构造进化信号"已经成为热点并形成五条成熟路线(rubric 化 judge 奖励、评估器共进化、内在/一致性信号、人类偏好回流、弱 verifier 集成),在**模型权重层**甚至已经"卷"起来了(EvoRubric/EvoRubrics/SERPO/SCORE/HOTE 五篇共进化 rubric 工作在 2026 年 5-7 月密集出现);**harness 层**也出现了第一篇直接工作(TTHE,测试时用无标签执行痕迹进化 harness)。但三个具体交集仍然是真空:(a)**harness/记忆/技能层自进化 × 真不可验证任务域**——TTHE 的任务全是本质可验证域,SCORE/HOTE 在不可验证域但改的是权重;(b)**信号可靠性感知的进化治理**——什么时候信 judge、什么时候信一致性、什么时候召回人类,没有系统工作;(c)**长周期延迟结果信号闭环**——SWE-CI 刚给出 repo 长期健康的可计算度量(EvoScore),尚无人把它回流为进化信号。原判断的方向直觉(这里有可发论文的空隙)仍然正确,但立项必须从"开荒"改为"在密集相关工作中做精确差异化"。

## 2. 相关工作全景表

### 路线一:LLM-as-judge / rubric 化奖励(权重层为主)

| 工作 | 年份 | 进化信号来源 | 任务域 | 局限 |
|---|---|---|---|---|
| Self-Rewarding LMs (arXiv:2401.10020) | 2024 | 模型自评 → DPO 偏好对 | 指令跟随 | judge=policy 自增强偏差;后被 2607.05904 结构性证伪 |
| Rubrics as Rewards (RaR, 2507.17746) | 2025 | instance-specific checklist × LLM judge | 医学、科学 | rubric 静态,饱和后可被 hack;需参考答案生成 rubric |
| LLM-as-a-Coach / EL (2607.18110) | 2026 | judge 的富文本评估蒸馏为经验知识(非标量) | 开放式任务 | 依赖 coach 模型质量;上下文蒸馏成本高 |
| Rubric Dropout (2608.11669) | 2026 | rubric 奖励 + 每步随机丢准则 | 医学、科学 | 缓解而非消除 hacking;仍需外部 gold judge 才能观测到 hacking |
| Rubric 生成再思考 (2602.05125) | 2026 | 改进 rubric 生成以强化 judge | 开放式评测 | 评测侧工作,未闭环到进化 |

### 路线二:评估器与被评者共进化(直面"judge 天花板")

| 工作 | 年份 | 进化信号来源 | 任务域 | 局限 |
|---|---|---|---|---|
| EvoRubric (2605.29847) | 2026 | 单策略分饰 Reasoner/Rubric Generator,多级验证(meta-verifier、LOO 共识) | 医学、写作、科学 | 权重层;验证管线复杂,计算贵 |
| EvoRubrics (2606.23038) | 2026 | Policy 与 Rubric Generator 每步对抗共进化 | 开放式生成 | 对抗不稳定;自监督变体增益有限 |
| SCORE (2606.04507) | 2026 | 共享参数 evaluator-solver 共进化 + meta-harness 约束评估环境 | deep research 报告 | 权重层;meta-harness 本身仍是手工设计的外部约束 |
| SERPO (2607.26873) | 2026 | G-N-B 响应档案 → 判别性准则进化 → verdict-token 概率作奖励 | HealthBench、ResearchQA | test-time、权重层;档案维护随任务量增长 |
| HOTE (2606.13710) | 2026 | proposer/solver/judge 三方混合 RL 共进化 | 长文 deep research | 权重层;明言是为弥合"agent evolution 只在可验证任务被验证"的 gap |
| CoNL (2601.21464) | 2026 | critique 的"助他改进量"作为元评估奖励(多 agent 自博弈) | 创意写作、对话、伦理 | 助他改进仍由同族模型度量,循环未彻底打破 |

### 路线三:内在信号 / self-consistency 代理(无任何外部 judge)

| 工作 | 年份 | 进化信号来源 | 任务域 | 局限 |
|---|---|---|---|---|
| TTRL (2504.16084) | 2025 | 多数投票伪标签 | 数学(无标签) | 预设"唯一正确答案",不适用开放域 |
| Intuitor / RLIF (2505.19590) | 2025 | self-certainty(输出分布 KL) | 数学、代码 | 置信度可被过度自信污染;开放域未验证 |
| CoCoV (2606.03608) | 2026 | 置信度分区路由:高置信投票 / 低置信自验证 | 数学 | 同上;verifier 与 generator 同权重 |
| G-Zero (2605.09959) | 2026 | Hint-δ:提示引起的对数似然偏移(纯内在) | 开放式生成 + 数学 | 权重层;δ 信号与"人类眼中的好"的对齐只有间接证据 |
| R-Diverse (2602.13103) | 2026 | self-play + 记忆惩罚 + 技能感知多样性度量 | 推理自博弈 | 解决的是信号多样性而非信号正确性 |

### 路线四:人类偏好回流(部署期隐式信号)

| 工作 | 年份 | 进化信号来源 | 任务域 | 局限 |
|---|---|---|---|---|
| Echo (2605.21984) | 2026 | 用户对 agent 输出的后续修改序列(最终稳定代码=事后金标) | 生产代码补全 | 需海量部署流量;信号滞后 |
| SLIFT (2608.09109) | 2026 | 自然交互反馈分解为 Fix/Spec/Null 原子成分选择性自学习 | 通用对话 | 反馈稀疏且噪声大 |
| TRACE (2511.08394) | 2025 | 对话轨迹的"会话几何"(语义空间动力学)预测满意度 | 开放式协作 | 相关性信号,因果性弱 |

### 路线五:弱 verifier 理论 / reward hacking 分析(信号可靠性基础设施)

| 工作 | 年份 | 贡献 | 局限 |
|---|---|---|---|
| Weaver (2506.18203, NeurIPS 2025) | 2025 | 弱监督估计各弱 verifier 准确率后加权集成,近 oracle 选答;可蒸馏为 400M 模型 | 用于 best-of-N 选答,未接入进化闭环 |
| Self-Play Reward Hacking (2607.05904) | 2026 | 证明 reference-free judge 评 plausibility 而非 correctness(judge 通过率 0.94 vs 真实 0.20);de-anchoring(judge 先独立作答)把假阳性 0.719→0.012 | 在有 hidden anchor 的域测得;开放域无 anchor 可审计 |
| Reward Hacking as Equilibrium (2603.28063) | 2026 | 五公理证明 hacking 是结构均衡而非 bug;agentic 系统评估覆盖率随工具数趋零 | 理论;可计算失真指数尚未实证于 harness 进化 |
| Reward Hacking 综述 (2604.13602) | 2026 | evaluator-policy co-adaptation 视角统一各类 hacking | 综述 |

### 路线六:harness 层进化(与本项目最直接相关)

| 工作 | 年份 | 进化信号来源 | 任务域 | 局限 |
|---|---|---|---|---|
| TTHE (2607.08124) | 2026 | 无标签执行轨迹 → 执行派生代理信号,LLM judge 择优 harness | text-to-SQL、竞赛编程、SWE、数据科学、工具使用 | **任务域本质可验证**;代理信号可靠性无估计、无回滚;proposer/judge 同一模型 |
| HarnessX (2606.14249) | 2026 | 轨迹驱动多 agent 进化引擎(AEGIS) | ALFWorld、GAIA、SWE-bench 等 | 信号仍是可验证基准分 |
| MSCE (2607.16621) | 2026 | 反思加权价值回填:稀疏终端反馈经局部自反思稠密化,治理记忆→技能结晶 | 长程 agent 基准 | 终端反馈仍来自基准 verifier |
| SEAGym (2606.17546) | 2026 | (评测环境)度量更新过程:证据来源、快照回归、改进持久性 | 自进化评测 | 不是方法;但为 B3 实验设计提供度量框架 |
| SWE-CI (2603.03823) | 2026 | (基准)EvoScore:未来加权功能正确率度量长期可维护性 | 仓库长期维护 | 度量存在但未被用作进化信号 |

## 3. 空白点逐条核实过程

检索协议执行说明:Semantic Scholar API 自 17:05 起持续返回 HTTP 429(带 key、换代理出口均同,判断为 key 配额耗尽),重试约 40 分钟后放弃,证据面改由 websearch(≈8 组查询)+ arXiv 直查覆盖;本机 443 直连间歇性中断,PDF 经公司 PAC 代理下载。此为本报告的方法学限制:引文网络(谁引了谁、引用数)未经 S2 核实。

**核实 1:"self-evolution without verifier / unverifiable tasks" 是否有直接工作?**
检索词:self-evolving agent without verifier unverifiable tasks evolution signal;self-improvement unverifiable。
结果:直接命中 G-Zero(2605.09959,标题级匹配"verifier-free…self-evolution across unverifiable domains")、SCORE(2606.04507,"deep research…reward design inherently unverifiable")、CoNL(2601.21464,"Non-verifiable Learning: Self-Evolving LLMs")。
判定:**权重层不空白,且已是活跃赛道。**

**核实 2:LLM-as-judge / rubric 驱动进化是否已系统化?**
检索词:LLM self-improvement non-verifiable domains LLM-as-judge reward;Rubrics as Rewards。
结果:RaR(2507.17746)开路,2026 年出现完整生态:rubric 生成改进(2602.05125)、交替训练 rubric RM(2602.01511)、rubric 条件自蒸馏(2606.19327)、coach 化富反馈(2607.18110)、hacking 缓解(2608.11669)。Cameron Wolfe 2026-02 博客称其为"当前最热 RL 研究方向之一"。
判定:**不空白,已过了"能不能做"阶段,进入"怎么做稳"阶段。**

**核实 3:评估器静态 → 共进化是否已被想到?**
检索词:deep research agent self-evolving rubric judge open-ended。
结果:2026 年 5-7 月三个月内至少 5 篇共进化 rubric/evaluator 工作(EvoRubric、EvoRubrics、SCORE、SERPO、HOTE),互相且大多与本项目设想撞车。
判定:**不空白,是本题竞争最激烈的子方向。**

**核实 4:harness 层(冻结权重)× 弱信号是否有工作?**
检索词:harness evolution without verifier unlabeled execution traces;self-evolving agent skill memory open-ended。
结果:TTHE(2607.08124)是唯一直接工作,但其五个任务域(text-to-SQL、竞赛编程、SWE、数据科学、工具使用)都存在快速 verifier,只是测试时不用;第三方冷评(readpriors,已剪藏)指出其代理信号可靠性、回滚、自评偏差三缺口。MSCE/HarnessX 的信号仍是基准分。**未找到任何"冻结模型、进化 harness/记忆/技能、任务为 deep research/长文写作/工程决策"的工作。**
判定:**此交集空白成立。**

**核实 5:reward hacking in agent evolution 是否已被研究?**
检索词:reward hacking self-evolving agent evolution LLM judge Goodhart。
结果:理论(2603.28063 均衡论证;2604.13602 综述提出 evaluator-policy co-adaptation)与实证(2607.05904 self-play hacking + de-anchoring 解法;2608.11669 训练 judge 与 gold judge 分数发散的直接测量)都已出现;Misevolution(2509.26354,库内)覆盖 agent 侧。
判定:**风险分析不空白;但"把这些防御集成进 harness 进化环"仍无工作(与分支 B 待挖问题 4 汇合)。**

**核实 6:长周期延迟结果(repo 健康、可维护性)作为进化信号?**
检索词:codebase health maintainability technical debt as reward signal delayed outcome。
结果:SWE-CI(2603.03823)给出 EvoScore 度量与"技术债在第 5 轮才显形"的实证,GRPO+代码质量奖励(2506.02211)在权重层试过静态质量信号;但**没有任何工作把延迟结果回流为 harness/agent 进化信号并做跨代信用分配**。
判定:**空白成立(度量已备好,闭环缺失)。**

**核实 7:进化是否真的变好——鸡生蛋问题有无解法?**
结果:SEAGym(2606.17546)提出度量更新过程本身;2607.05904 的 hidden-anchor audit 提供第三方审计范式;CoNL 用"critique 助他改进量"部分打破循环;SCORE 用外部 meta-harness 约束。各给局部答案,无统一框架。
判定:**部分空白——审计原语已存在,组合成弱 verifier 进化的标准评估协议仍缺。**

## 4. 立项建议

### 4.1 研究问题表述

**RQ:对冻结权重的 harness 型 agent(Claude Code/Codex 类),在无快速可靠 verifier 的任务域(深度研究、长文写作、长周期工程维护)上,如何构造"可靠性可估计"的复合进化信号,使 harness(prompt/记忆/技能/工作流)的进化在第三方审计下真实变好,而非 hack 掉自己的评估器?**

三个子问题:(RQ1)多路弱信号(de-anchored judge、进化中 rubric、self-consistency、执行痕迹、稀疏人类回流)如何按可靠性加权组合成 harness 编辑的接受函数?(RQ2)延迟结果(EvoScore 类)如何跨代归因到早期 harness 编辑?(RQ3)"进化是否真的变好"如何在不可验证域被独立度量?

### 4.2 方法草案

**草案 A:SigWeaver-H——可靠性加权的弱信号组合驱动 harness 进化。**
把 Weaver 的弱监督集成从"选答案"迁移到"选 harness 编辑":每个候选 harness 编辑在探针任务集上滚出轨迹,由 K 路弱信号打分(de-anchored LLM judge〔按 2607.05904 强制 judge 先独立完成任务再评〕、进化中 rubric〔按 EvoRubrics 保持判别力〕、跨样本 self-consistency、执行痕迹代理〔步数/回退率/工具错误率〕、每 N 代一次的人类抽查);用 Weaver 式无标签潜变量估计各信号当期可靠性,加权后作为编辑接受函数。关键设计:**可靠性估计器位于进化环外且只读**(继承 AHE 的权限外置),信号权重对进化 agent 不可见(防对单一信号过拟合,机制上等价于 Rubric Dropout 的泛化版)。
新颖性依据:Weaver 自己停在 best-of-N 选答;TTHE 用单一 LLM judge 无可靠性估计;两者的组合+harness 层+不可验证域为空白(核实 4)。

**草案 B:EvoScore-in-the-loop——延迟结果回流与跨代信用分配。**
在 SWE-CI 风格的长程 CI 环境(以及 deep research 的多轮跟进任务)中进化 harness:每代 harness 的适应度不是当期任务分,而是**未来 k 轮的 EvoScore 折现和**——即把 HGM 的 CMP(clade metaproductivity,谱系聚合表现)从"可验证基准分"推广到"延迟弱信号"。技术要点:维护编辑谱系树,延迟信号到达时沿谱系回填(类似 MSCE 的反思加权价值回填,但跨 harness 代而非跨轨迹步);对未到期编辑用弱信号组合(草案 A)作临时估值,到期后用真实延迟结果校正——形成"弱信号做先验、延迟结果做后验"的两阶段信用分配。
新颖性依据:EvoScore 是 2026-03 才出现的度量,尚无闭环使用(核实 6);HGM 的 CMP 从未离开可验证域。

**草案 C(可作为 A/B 的评估协议,亦可独立成章):三角审计协议——回答"进化是否真的变好"。**
组合三个互相独立的锚:(i)**冻结外部锚**:进化全程不可见的 held-out gold judge(比训练 judge 强一档)+ 小规模人类金标,只在检查点评估(Rubric Dropout 论文用此法观测到 hacking,我们把它标准化为协议);(ii)**canary 可验证任务**:在不可验证域进化的 harness 定期在少量可验证任务上旁路测量,若不可验证域"分数"上涨而 canary 下跌,判定为 hacking(跨域 canary 思想,现无先例);(iii)**时间滞后审计**:hidden-anchor 式,用进化时不存在的未来数据(新发论文的研究问题、仓库未来真实提交)作事后检验。三锚同时通过才认定"真实进步"。

### 4.3 实验设计雏形

- **任务域**:① deep research(ResearchQA、DeepResearch 类基准,含跟进轮次);② 长文写作(多轮修改情景);③ SWE-CI 长程维护(延迟信号主战场)。
- **Harness 与可编辑面**:Claude Code 类,开放 AHE 七组件中的 prompt/技能/长期记忆三面(最小充分集,呼应分支 B 待挖问题 1)。
- **基线**:静态 harness;GEPA(judge 反馈驱动 prompt 进化);TTHE 移植(单一 judge 代理信号);SCORE/HOTE(权重层共进化,作为"改权重 vs 改 harness"对照);随机编辑(安慰剂)。
- **度量**:SEAGym 式过程度量(快照回归率、改进持久性、成本)+ 草案 C 三角审计 + 多样性监控(R-Diverse 的跨轮/技能感知两类幻觉指标)。
- **规模可行性**:GEPA 证明 20-100 样本可驱动文本组件进化,ShinkaEvolve 证明 ~150 样本可完成程序进化;弱信号组合的主要成本在多路打分(可用 Weaver 蒸馏的小模型压缩),单机夜间预算(数百 rollout)可行。
- **消融**:去掉可靠性加权(退化为均权集成)、去掉 de-anchoring、去掉延迟回填、单信号 vs 组合。

### 4.4 最像的竞品与差异化

| 竞品 | 相同点 | 差异化 |
|---|---|---|
| TTHE (2607.08124) | harness 层、无 gold label、种群+proposer+judge | 我们:任务域真不可验证;信号可靠性显式估计而非单一 judge;有回滚与审计协议(其三大公认缺口) |
| SCORE / HOTE | 不可验证域、评估器共进化 | 我们:冻结权重只动 harness(可解释、可回滚、跨模型迁移,呼应 Self-Harness 的 model-specific 发现);他们需要 RL 训练基础设施 |
| Weaver (2506.18203) | 弱 verifier 加权集成 | 我们:从静态选答扩展到动态进化闭环,可靠性随进化在线重估 |
| HGM (2510.21614, 库内) | 谱系级适应度 | 我们:CMP 推广到延迟弱信号域,加两阶段信用分配 |
| AHE (2604.25850, 库内) | harness 组件化+证据驱动编辑 | 我们:其证据全来自 verifier 锚定的失败模式;我们处理无 verifier 锚的证据 |

## 5. 风险与不确定性

1. **评估循环(鸡生蛋)是本质困难而非工程细节**:2603.28063 证明在有限评估下 hacking 是均衡态,评估覆盖率随 agent 工具数结构性下降。草案 C 只能缓解:三角锚本身也会被强优化器发现盲区。诚实的论文姿态是给出"审计强度 vs 进化压力"的经验边界,而非宣称解决。
2. **Judge hacking 的具体形态已知且严重**:2607.05904 显示 self-play 可把 judge 通过率刷高 0.22→0.94 而真实质量不动;2608.11669 显示 gold 分数可在训练分数上升时下跌 22 分。任何不含 de-anchoring/准则随机化的设计都应视为默认已被 hack。
3. **多样性坍缩与 Goodhart 叠加**:弱信号方差大,进化易收敛到"讨好所有弱信号的平庸解";R-Diverse 的两类多样性幻觉在 harness 编辑空间同样成立(编辑表面不同、机制同质)。
4. **人类回流信号的伦理与滞后**:Echo 式信号需要真实用户流量,学术复现只能用模拟用户(又引入 judge);滞后信号使实验周期变长,SWE-CI 单任务平均对应 233 天真实演化史,压缩到实验尺度后外部效度存疑。
5. **撞车风险(高)**:本题从"空白"变"热点"只用了一年;EvoRubric 系五篇在三个月内密集出现,说明权重层已红海。harness 层交集当前为空,但 TTHE 作者组、AHE 作者组、HOTE 作者组都在一步之遥。**建议 change-002 决策时把时间窗按 3-6 个月估计**,优先做草案 C(审计协议)——它对所有竞品都是互补而非替代,撞车风险最低且顶会评审友好(评测/审计类工作生命周期长)。
6. **方法学限制**:本报告引文网络未经 Semantic Scholar 核实(API 配额耗尽,见 §3 开头);2026 年论文均为 arXiv 预印本,同行评审状态未知;检索以英文为主,可能漏掉非 arXiv 渠道工作。

## 6. 参考文献(本轮新增归档,均在 raw/papers/)

1. Yuan et al., 2024, Self-Rewarding Language Models, arXiv:2401.10020 — `raw/papers/2024-yuan-self-rewarding-lms.pdf`
2. Zuo et al., 2025, TTRL: Test-Time Reinforcement Learning, arXiv:2504.16084 — `raw/papers/2025-zuo-ttrl.pdf`
3. Zhao et al., 2025, Learning to Reason without External Rewards (Intuitor), arXiv:2505.19590 — `raw/papers/2025-zhao-intuitor.pdf`
4. Saad-Falcon et al., 2025, Weaver: Shrinking the Generation-Verification Gap with Weak Verifiers, arXiv:2506.18203 — `raw/papers/2025-saadfalcon-weaver.pdf`
5. Gunjal et al., 2025, Rubrics as Rewards, arXiv:2507.17746 — `raw/papers/2025-gunjal-rubrics-as-rewards.pdf`
6. Huang et al., 2026, G-Zero: Self-Play for Open-Ended Generation from Zero Data, arXiv:2605.09959 — `raw/papers/2026-huang-g-zero.pdf`
7. Zhu et al., 2026, SCORE: Self-Evolving Deep Research via Joint Generation and Evaluation, arXiv:2606.04507 — `raw/papers/2026-zhu-score-deep-research.pdf`
8. Wang et al., 2026, SERPO: Self-Evolving Rubric Policy Optimization, arXiv:2607.26873 — `raw/papers/2026-wang-serpo.pdf`
9. Ding et al., 2026, EvoRubrics: Dynamic Rubrics as Rewards via Adversarial Co-Evolution, arXiv:2606.23038 — `raw/papers/2026-ding-evorubrics.pdf`
10. Guan et al., 2026, EvoRubric: Self-Evolving Rubric-Driven RL, arXiv:2605.29847 — `raw/papers/2026-guan-evorubric.pdf`
11. Nie et al., 2026, TTHE: Test-Time Harness Evolution, arXiv:2607.08124 — `raw/papers/2026-nie-tthe.pdf`
12. Zhou, 2026, More Convincing, Not More Correct: Self-Play Reward Hacking of Reference-Free LLM Judges, arXiv:2607.05904 — `raw/papers/2026-zhou-self-play-reward-hacking.pdf`
13. Yang et al., 2026, Rubric Dropout, arXiv:2608.11669 — `raw/papers/2026-yang-rubric-dropout.pdf`
14. Ye et al., 2026, LLM-as-a-Coach: Experiential Learning for Non-Verifiable Tasks, arXiv:2607.18110 — `raw/papers/2026-ye-llm-as-a-coach.pdf`
15. Dong et al., 2026, Echo: Learning from Experience Data via User-Driven Refinement, arXiv:2605.21984 — `raw/papers/2026-dong-echo.pdf`
16. Sui et al., 2026, CoNL: Conversation for Non-verifiable Learning, arXiv:2601.21464 — `raw/papers/2026-sui-conl.pdf`
17. Li et al., 2026, R-Diverse: Mitigating Diversity Illusion in Self-Play LLM Training, arXiv:2602.13103 — `raw/papers/2026-li-r-diverse.pdf`
18. Piao et al., 2026, HOTE: Hybrid Open-Ended Tri-Evolution Makes Better Deep Researcher, arXiv:2606.13710 — `raw/papers/2026-piao-hote.pdf`
19. Chen et al., 2026, SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via CI, arXiv:2603.03823 — `raw/papers/2026-chen-swe-ci.pdf`
20. Chen et al., 2026, HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry, arXiv:2606.14249 — `raw/papers/2026-chen-harnessx.pdf`
21. Zheng et al., 2026, SEAGym: An Evaluation Environment for Self-Evolving LLM Agents, arXiv:2606.17546 — `raw/papers/2026-zheng-seagym.pdf`

仅引用未归档(浅读,判定非核心或综述/理论):2602.05125(rubric 生成)、2602.01511(交替 rubric RM)、2606.19327(RCSD)、2608.09109(SLIFT)、2511.08394(TRACE)、2603.28063(hacking 均衡理论)、2604.13602(hacking 综述)、2607.16621(MSCE)、2606.03608(CoCoV)、2608.03545(Hi-TTRL)、2506.02211(代码质量 GRPO)。库内已有并引用:HGM、AHE、Self-Harness、GEPA、Misevolution、ShinkaEvolve(见 index.yaml)。

网页剪藏:`Clipping/2026-08-28_cameronrwolfe-substack_rubric-based-rewards-for-rl.md`、`Clipping/2026-08-28_readpriors_tthe-runtime-harness-evolution.md`。

---

落款:survey-agent-B3 · 2026-08-29 01:25
