# 剪藏:codememo-benchmark(HuggingFace 数据集页)

- 来源:https://huggingface.co/datasets/laynepro/codememo-benchmark
- 剪藏时间:2026-08-28(survey-agent-A5,change-002)
- 相关方向:A5(harness 记忆基准)——**目前最接近"coding harness 记忆基准"的社区工作,直接以 Claude Code 转录为语料**

## 要点

- 自称 "LoCoMo for coding sessions":系统摄入一系列 **Claude Code 转录(JSONL)**,回答需要跨会话记住决策、调试步骤、约定、时间顺序的问题。
- 规模:**158 个问题、3 个编码项目**(project_01 CLI 任务管理器 15 会话;project_02 Rust 多仓编排器 44 会话;project_03 会话记忆系统 7 会话)。
- 六类问题:Factual(35)/ Debug(31)/ Architecture(28)/ Temporal(22)/ Convention(20)/ Cross-session(22)。
- 指标:LLM-as-judge J-score(gpt-4o-mini)、token 级 F1、retrieval recall@k。
- 已发布结果(2026-03-14):synapt v0.6.2(本地 3B)总分 90.51 vs Mem0 v1.0.5(OpenAI 云)76.0;Convention 类差距最大(80.0 vs 42.86)。

## 对 A5 的判断意义

1. 证明"用真实 coding 会话转录出题"的路线可行,且社区已有人做;
2. 但它是**回忆型 QA**(不落到下游任务执行),规模小(158 题/3 项目)、无污染控制、judge 单一(gpt-4o-mini)、非同行评审;
3. "Convention 类得分最低"的现象与 MemoryCode(ACL 2025)结论一致——约定/偏好类记忆是 coding 场景最难的。
4. 空白点因此收窄但未关闭:**执行导向、带污染控制、可复现的 harness 记忆基准仍缺位**。
