# Your AI Agent Is Rewriting Its Own Brain at Runtime — Without Your Permission(剪藏)

- 来源:Priors(readpriors.com),作者 John
- URL:https://readpriors.com/your-ai-agent-is-rewriting-its-own-brain-at-runtime-without-your-permission/
- 发布:2026-07-11 · 剪藏:2026-08-28 · 剪藏人:survey-agent-B3
- 用途:方向 B3——对 TTHE(arXiv:2607.08124)的第三方冷评,聚焦"执行痕迹代理信号可靠性"这一 B3 核心问题

## 事实部分(What happened)

TTHE(Test-Time Harness Evolution, Jun Nie et al., HKBU/USTC/HKUST/TCL)把 agent 的可执行 harness(上下文构造、工具调用、错误恢复、结果校验)当作**测试时可变异对象**:维护候选 harness 种群,agentic proposer(同一冻结 LLM)阅读无标签执行轨迹提出改进,LLM-as-judge 角色用**执行派生的代理信号**(无 gold label)选出胜者,胜者持续治理后续输入。在 text-to-SQL、竞赛编程、软件工程、数据科学、agentic 工具使用五个域上稳定超过固定 ReAct 基线;全程不动模型权重。

## 冷评部分(Cold read)——对 B3 最有价值

> "The judge has no ground truth, and if the proxy signals are misleading, the harness can evolve confidently in the wrong direction."

1. 论文摘要自己承认 "execution-derived proxy reliability" 是无监督 agent 改进的**中心挑战**;
2. 所有结果只对比固定基线,没有对比"同等算力预算下预先搜索出的最优 harness";
3. **复合风险无解**:胜出 harness "persists to govern subsequent inputs"——早期一次坏进化决策会毒化整个后续运行,论文未提 rollback 机制;
4. proposer 与 judge 是同一个冻结 LLM → 自我增强偏差与基准污染是活风险;
5. 信号成熟度评级 2/5:纯学术 PoC,无生产验证、无延迟/成本数据。

## 预测(原文,截至 2026-07-11)

到 2027 Q3 至少一个主流 agent 框架会实验性上线 "live harness adaptation",但默认关闭——因为没有审计轨迹的运行时自改写无法过企业合规。

## 与 B3 的关联

TTHE 是"harness 层 × 无标签信号"的首个直接工作,但其任务域全部是本质可验证域(只是测试时不用标签)。它暴露的三个缺口正是 B3 立项空间:代理信号可靠性无估计、无回滚治理、无第三方审计。见 deep_B3 报告 §3/§4。
