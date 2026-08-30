# 剪藏:两个自进化 agent 评测基准(B1 方向检索所得)

- 剪藏日期:2026-08-28
- 剪藏人:survey-agent-B1(change-002)
- 来源:arXiv 摘要页(经 websearch/webfetch 获取)

## 1. PAST-Bench (arXiv:2608.04003)

来源:https://arxiv.org/abs/2608.04003(PDF 已归档 raw/papers/2026-xue-past-bench.pdf)

**要点**(与 B1 相关):

- 性能归因(performance-attribution)基准:每个任务族跑两遍,一遍开放持久化经验、一遍剥离,**固定模型、prompt、工具、seed**——这正是"单面(记忆/经验面)受控消融"的范式。
- 26 scenarios / 204 episodes,覆盖 memory、procedural reuse、information gathering、update 四种能力维度;7 个基座模型 x 4 个 agent 框架。
- 结论:留存经验带来的提升真实但在能力维度上不均匀;相同表面增益的 agent 在"是否走了预期的 save-retrieve-update 通路"上差异巨大(outcome 与 mechanism 证据分离)。
- Hermes+ 对 agent loop 五阶段(Plan/Render/Route/Gate/Close)做**逐机制消融**:Update 维度上 closeout 单独 +0.16、retrieval gate 单独 +0.06,组合 +0.24(超可加)。
- 选择 Hermes 做逐机制消融的理由:它是唯一暴露 agent loop 且无预置持久化栈的框架——印证了"可干净消融的 harness 稀缺"这一 B1 立项动机。

## 2. ContinualSkillBench (arXiv 2026)

来源:arXiv 摘要页(标题:ContinualSkillBench: Can LLM Agents Truly Evolve Their Capabilities?)

**要点**:评测 LLM agent 能否在连续任务流中真正进化 skill 能力;关注 skill 累积的持续性与遗忘。与 B1 的 skills 单面证据互补(另见 CODESKILL、SkillClaw)。

## 与 B1 的关系

PAST-Bench 证明"配对开/关 + 固定其余变量 + 通路证据"的消融方法学可行,但其对象是**个人助理 agent 的经验持久化面**,不是 Claude Code 类 coding harness 的 7+ 组件;逐组件(system prompt/工具/记忆/skills/workflow/代码本体)交叉消融仍无人做。
