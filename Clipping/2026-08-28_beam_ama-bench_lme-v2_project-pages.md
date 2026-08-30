# 剪藏:BEAM / AMA-Bench / LongMemEval-V2 项目页要点

- 来源:
  - https://mohammadtavakoli78.github.io/beam-light/(BEAM & LIGHT,ICLR 2026)
  - https://github.com/AMA-Bench/AMA-Hub(AMA-Bench,ICML 2026)
  - https://github.com/JJerryJi/LongMemEval-V2(LME-V2 官方评测 harness)
- 剪藏时间:2026-08-28(survey-agent-A5,change-002)

## BEAM(arXiv:2510.27246,ICLR 2026)

- 100 段连贯对话 × 4 个规模档(128K/500K/1M/10M token),2,000 个人工校验问题,10 种记忆能力;域含 coding、数学、健康、金融等;
- 自动生成管线 + 人工校验;1M 上下文窗口模型(含 RAG)随对话变长仍持续退化;LIGHT(情景+工作记忆+scratchpad)平均提升 3.50%-12.69%;
- 注意:GitHub fork(SemanticReach/BEAM)上出现厂商自报 96% 之类的复现声明,再次说明**排行榜治理**是记忆基准的现实问题。

## AMA-Bench(arXiv:2602.22769,ICML 2026;曾获 ICLR 2026 Memory Agent workshop oral)

- 立论:现有基准以人-agent 对话为中心,而真实 agent 记忆是**机器生成的 agent-环境交互流**;
- 双子集:真实 agentic 轨迹 + 专家 QA;合成轨迹可**任意拉长** + 规则 QA;
- 发现:现有记忆系统缺因果与客观信息、受相似度检索有损性所限;AMA-Agent(因果图+工具增强检索)57.22%,超最强基线 11.16%;
- HuggingFace 数据集与 leaderboard 已上线。

## LongMemEval-V2(arXiv:2605.12493;Di Wu 等,UCLA)

- 451 个人工问题,多模态 web-agent 轨迹长历史(25M-115M token,最多 500 条轨迹/haystack),web + enterprise 两域;
- 5 能力:static state recall / dynamic state tracking / workflow knowledge / gotchas(环境陷阱)/ premise awareness;
- 评测协议:记忆系统消费轨迹历史,返回紧凑证据供 QA;**同时计分准确率与查询延迟**,leaderboard 分数 = 相对固定参考前沿的 LAFS 增益,允许同一方法提交多个延迟工作点;
- 官方 repo 含 baselines(no_retrieval、AgentRunbook-C 等)与 small/medium 两个 tier。

## 对 A5 的意义

- LME-V2 的 LAFS(延迟-准确率前沿)协议是目前最成熟的"效率作为一等指标"的实现,任何新基准应兼容此报告格式;
- AMA-Bench 的"合成轨迹任意拉长 + 规则 QA"是控制规模与污染的可复用手法;
- 三者都不覆盖 coding harness:BEAM 是对话、AMA-Bench 是通用 agent 轨迹回忆、LME-V2 是 web-agent 环境知识。
