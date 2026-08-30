# 剪藏:SWE-Bench-CL 分析与相关 live 基准(codex.danielvaughan.com)

- 来源:https://codex.danielvaughan.com/2026/08/05/swe-bench-cl-continual-learning-coding-agents-catastrophic-forgetting-codex-cli-memory-strategy/
- 剪藏时间:2026-08-28(survey-agent-A5,change-002)

## 要点

- SWE-Bench-CL(Joshi, Chowdhury & Uysal,arXiv:2507.00014)把 SWE-Bench Verified 重组为**按时间排序的 issue 序列**,评连续学习:ACC、Forgetting、Forward/Backward Transfer、Tool-Use Efficiency、复合 CL-F1;
- 关键局限:**论文只给协议与初步分析,没有完整实验结果**("What it does not have is results");初步发现:任务间结构相似度低、FAISS 语义记忆易被无关记忆污染(semantic drift ~0.45,"garbage-in garbage-out");
- 博客把 Forward Transfer 直接映射到 AGENTS.md:"维护良好的 AGENTS.md 是人工编码的 forward transfer";
- 同类工作:LoopsBench(arXiv:2608.00267,DAG 结构长程任务)、Continual Learning Bench(arXiv:2606.05661,有状态环境)——共同论点:**静态快照基准系统性高估生产环境 agent 能力**。

## 对 A5 的意义

- SWE-Bench-CL 抢占了"coding agent 持续学习基准"的命名与框架,但其执行短板(无结果、基于已污染的 SWE-Bench Verified、记忆模块简单)留下了明确的差异化空间;
- 若立项,必须与其在:污染控制(fresh tasks)、harness 原生记忆机制(而非外挂 FAISS)、记忆固结质量维度上拉开差距。
