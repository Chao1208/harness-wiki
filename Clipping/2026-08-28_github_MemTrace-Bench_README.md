# 剪藏：MemTrace-Bench v5（GitHub README）

- 来源：https://github.com/huyuelin/MemTrace-Bench
- 剪藏日期：2026-08-28
- 剪藏人：survey-agent-C6（change-002 · C6 方向）
- 状态：ICSE 2027 在审（匿名），**无 arXiv 版本**，仅 GitHub 发布。论文题为 "Memory Is a Hidden Dependency: A Benchmark for Replay-Defined Harm in Stateful Coding Agents"。

## 核心内容（摘自 README）

Persistent memory is becoming part of the infrastructure of coding agents. It improves long-horizon software work by preserving project conventions, debugging evidence, API choices, and developer preferences across tasks, but the same mechanism creates a **hidden dependency**: a later repair may be shaped by memory written for another repository, dependency version, tool trace, or security policy.

MemTrace-Bench v5 是通过**可审计重放（auditable replay）**评测 coding agent 持久记忆依赖的基准：

- 定义 prelude-probe 序列（先导任务写入记忆 → 探针任务检验记忆影响）、release tiers、sequence cards、官方重放条件、run manifests、标注审计与打分脚本；不要求被测系统采用任何特定记忆策略。
- 规模：**4,200 条序列，来自 1,260 个仓库**；90.5% 可本地运行（公开真实 / 脱敏 / synthetic-twin 三类 release）。
- 核心实证（15 种记忆配置 × 6 agent 家族 × 多模型家族）：
  - 朴素持久记忆把 in-scope 有用通过率从 61.9% 提到 75.5%；
  - 但坏率（bad rate）显著上升：**跨仓库记忆 22.6%、过期 API 记忆 18.9%、过期安全策略记忆 28.4%、隐通道记忆 23.1%**。
- 序列分类维度：Release（real/synthetic twin/remote-only）、Memory（in-scope useful / cross-repo / stale dep-API / stale security / sensitive-license / prompt injection）、Channel（memory store / conversation / tool log / terminal-cache / wrapper-patch / scratchpad-planner）、Oracle（hidden tests / semantic-security / static-license）。

## C6 调研注记

- 该工作直接覆盖 C6 关注的"**记忆随仓库/版本漂移的危害**"维度，但其序列是构造的 prelude-probe 对，不评"学习收益曲线/遗忘/前向迁移"，与 lifelong 学习基准互补而非替代。
- 引用格式（README 提供）：`@inproceedings{memtrace2027, title={Memory Is a Hidden Dependency: ...}, booktitle={ICSE}, year={2027}}`
