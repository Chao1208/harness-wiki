# Rubric-Based Rewards for RL(剪藏)

- 来源:Cameron R. Wolfe, Deep (Learning) Focus substack
- URL:https://cameronrwolfe.substack.com/p/rubric-rl
- 发布:2026-02-16 · 剪藏:2026-08-28 · 剪藏人:survey-agent-B3
- 用途:方向 B3(弱评估器下的自进化)——rubric-based RL 路线的最佳综述性博客

## 核心论点

> "Many important applications (e.g., creative writing or scientific reasoning) are not verifiable, making RLVR difficult to apply directly. To address this gap, we need reward signals that preserve RLVR's scalability and reliability while still working in non-verifiable settings."

Rubric-based rewards 把期望行为分解为结构化、可解释的准则清单,由 LLM judge 逐条评估后聚合为多维奖励;instance-specific rubric 显著提高 judge 可靠性,是把 RLVR 扩展到主观域的主流路径,已成为当前 RL 研究最热话题之一。

## 要点摘录

1. **LLM-as-a-Judge 的五类偏差**:position bias、verbosity bias、self-enhancement bias、capability bias(judge 评不了自己解不了的题)、distribution bias(分数分布偏斜)。缓解:in-context 校准、位置交换、参考答案、multi-judge jury。
2. **从 judge 到 rubric 的演化**:单一泛化 scoring prompt → per-criterion 分项 prompt → domain/task/instance 级 rubric。HealthBench 用医生手写的 conversation-specific rubric(带权重的自包含客观准则)是标志性实践;MultiChallenge 发现 rubric 提升专家与 judge 的一致性。
3. **与 RLHF 的对比**:偏好数据把多维质量压缩成单一标签,丧失准则级控制、易过拟合长度/格式 artifact;rubric 把评估维度显式化,是 "binary correctness 与 preference ranking 之间的中间地带"(RaR 论文语)。
4. **谱系溯源**:rubric-as-reward 思想可追溯到 Constitutional AI 与 Deliberative Alignment——直接从安全规范文本派生奖励,避免准则变化时重新收集偏好数据。
5. **代表工作**(文中综述):Rubrics-as-Rewards(RaR, Gunjal et al. 2025, arXiv:2507.17746,医学/科学域,HealthBench 相对提升至多 31%);RaR 的两种聚合(explicit 手工加权 vs implicit judge 整体评);Xu et al. 2026(arXiv:2602.01511)交替训练 rubric 奖励模型与策略。
6. **风险提示**:judge 偏差可被利用 → reward hacking 是 rubric-RL 的首要风险;细粒度 rubric 能降低但不能消除。

## 与 B3 的关联

该路线证明"弱评估器域的进化信号"在**模型权重层**已有成熟配方(rubric 化 + judge 化 + RL),但全部工作都在改权重、以单次回答为粒度;把同样的信号构造迁移到 harness/agent 进化层(以 harness 编辑为动作、以多任务轨迹为证据)仍是空隙——见 deep_B3 报告 §3。
