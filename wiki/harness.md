# Harness（Agent 执行框架）

> **一句话结论**：harness 已成为继模型权重之后的**第二学习载体**——前沿模型在 SWE-bench Verified 上收敛到 1pp 以内而 harness 差异可摆动 20pp 以上；2025–2026 年所有主流 harness 收敛到"分层 markdown 指令文件 + 按需披露的 skills + 可选 auto memory"三件套，但记忆写入策略无理论、harness-level forgetting 无人防护、沉淀止步于文本，是三大设计空位。

← 返回 [wiki 总览](index.md) · 相关页：[agent记忆](agent记忆.md)（记忆机制）、[agent自进化](agent自进化.md)（harness 作为进化对象）、[agent持续学习](agent持续学习.md)（学习闭环）、[可编辑面](可编辑面.md)（harness 组件作为进化对象的谱系）、[harness遗忘与回归](harness遗忘与回归.md)（forgetting 的量化与回归集）

## 核心概念与分类法

**定义**（Lilian Weng, 2026）：harness = 包裹基座模型、编排"思考/规划、工具调用、上下文感知与管理、artifact 存储、结果评估"的系统。

**扩展原语的三维刻画**（以 Claude Code 七类原语为例：CLAUDE.md/rules、skills、hooks、subagents、agent teams、MCP、plugins）：加载时机 × context 成本 × advisory（模型可忽略）还是 deterministic（强制执行）。要强制阻止某行为用 hook 而非 CLAUDE.md。

**记忆机制的行业标准形态（"三件套"）**：

1. **分层指令文件**（advisory，手写）：CLAUDE.md / AGENTS.md（60,000+ 开源项目采用，跨工具事实标准）/ GEMINI.md / .cursor/rules
2. **skills**（程序性沉淀）：SKILL.md + 脚本，渐进式披露（会话开始只见 name+description，正文按需加载）
3. **auto memory**（agent 自写）：Claude Code 首个默认开启（MEMORY.md 索引仅前 200 行/25KB 自动载入，细节移主题文件）；OpenHands SDK 双层目录 opt-in；Gemini 实验特性。一年内完成从"手写指令"到"agent 自写记忆默认开"的范式切换

**沉淀强度光谱**：memory（事实）→ rule（约束）→ skill（流程）→ 编译 harness（SIGIL 的类型化编译）。"何种经验应沉淀到哪一层"没有任何理论。

**harness-level forgetting**（HCL, 2026）：更新任一 harness 组件（prompt/记忆/工具/技能）可能在模型完全不动的情况下破坏既有可靠行为——把持续学习的"遗忘"概念正式扩展到 harness 状态。change-002 深挖确认现象层证据已在各组件层密集出现（详见 [harness遗忘与回归](harness遗忘与回归.md)）。

## 代表工作

学术论文：

| 工作 | 贡献 | 引用 |
|---|---|---|
| SWE-agent / ACI（2024） | 首次系统论证接口层设计显著影响 agent 性能，harness 研究起点 | [arXiv:2405.15793](https://arxiv.org/abs/2405.15793) · `raw/papers/2024-yang-swe-agent-aci.pdf` |
| Stop Comparing…Harness（2026） | Binding Constraint Thesis：长程任务性能方差更多由 harness 决定；六层披露协议 + locked-harness 评测 | [arXiv:2605.23950](https://arxiv.org/abs/2605.23950) · `raw/papers/2026-zhang-harness-disclosure.pdf` |
| Harness-Bench（2026） | 5088 次 factorial 运行：最高最低 harness 差 23.8pp；模型越强对 harness 越不敏感 | [arXiv:2605.27922](https://arxiv.org/abs/2605.27922) · `raw/papers/2026-yao-harness-bench.pdf` |
| Claw-SWE-Bench（2026） | 同一底座极简 vs 完整适配器 19.1% vs 73.4%；harness 与成本应为评测一等公民 | [arXiv:2606.12344](https://arxiv.org/abs/2606.12344) · `raw/papers/2026-zheng-claw-swe-bench.pdf` |
| AHE（2026） | 可观测性驱动的 harness 自动进化，超人工设计 harness（详见 [agent自进化](agent自进化.md)） | [arXiv:2604.25850](https://arxiv.org/abs/2604.25850) · `raw/papers/2026-lin-agentic-harness-engineering.pdf` |
| HCL（2026） | 正式提出 harness-level forgetting 与 guarded harness evolution（Optimizer 起草 + Evaluator 验证后 commit） | [arXiv:2608.19013](https://arxiv.org/abs/2608.19013) · `raw/papers/2026-kang-harness-continual-learning.pdf` |
| SIGIL（2026） | prose skill 执行保真度仅 56%（产物却能过输出检查）；编译成类型化 harness 后稳定 86%、token 0.58 倍 | [arXiv:2607.27309](https://arxiv.org/abs/2607.27309) · `raw/papers/2026-dantanarayana-sigil.pdf` |
| Code Isn't Memory（2026） | 结构化代码库索引 ≠ 记忆，二者在 harness 内职责应分离；附 coding harness 谱系综述 | [arXiv:2606.22417](https://arxiv.org/abs/2606.22417) · `raw/papers/2026-bhola-code-isnt-memory.pdf` |
| Scaffold Effect（2026） | 300 次受控试验论证 harness 选择是评测隐藏变量 | [arXiv:2607.22585](https://arxiv.org/abs/2607.22585) · `raw/papers/2026-vats-scaffold-effect.pdf` |

主流 harness 速览（详表见底稿）：Claude Code（跨会话学习成熟度最高：auto memory 默认开 + skills + hooks + Dreaming 固结）、Devin（商业界最完整经验沉淀流水线：反馈→Knowledge 建议→人工审核；session→Playbook）、OpenHands（开源界最完整 auto memory 规范，含 prompt injection 警告）、Codex CLI（AGENTS.md 链，32KiB 超限静默截断为著名坑点，无 auto memory）、OpenClaw（250k+ star，全 Markdown 认知状态 SOUL.md/MEMORY.md，"全量注入 vs 分层按需检索"之争的活案例）、mini-swe-agent（刻意零记忆，locked-harness 评测参考基线）。

关键工程博客：Anthropic《Effective context engineering》（context 是有边际收益递减的有限资源；compaction/结构化笔记/subagent 隔离三策略）、Manus《Context Engineering for AI Agents》（文件系统即终极 context、KV-cache 命中率为最重要生产指标、保留错误、todo.md 复述）、Cognition《Don't Build Multi-Agents》（多 agent 是 workload 决策而非架构信仰）、LangChain《Continual learning for AI agents》（模型层/harness 层/context 层三层学习分类，本项目直接采用）。

## 开放问题

1. **记忆写入策略无理论**：何时记、记什么、如何合并去重全靠 prompt 纪律条款，无可度量的记忆价值函数（search tree D-2）；change-002 A5 深挖确认"写入决策质量"（写不写/写到哪层/compaction 存活）在评测侧也是空白，见 [记忆与持续学习基准](记忆与持续学习基准.md)
2. **harness-level forgetting（change-002 深挖后修正）**：现象层空白已关闭——HCL 命名并测量之外，HarnessFix/Adaptive Auto-Harness/SkillFlow/ACE/Misevolution 各自撞见同一现象；真空白转为"以 harness 更新为被测变更单元的公开 retention 回归基准 + 回归集构建方法学"，详见 [harness遗忘与回归](harness遗忘与回归.md)（仍是高潜论文方向）
3. **记忆安全**：持久记忆文件是新攻击面（OpenHands 官方已警告），防御手段几乎空白（search tree D-3）
4. **记忆的 token 经济学**：全量注入 vs 索引+按需 vs 向量检索，缺公开的召回/成本 tradeoff 实证（search tree D-4）
5. **跨工具记忆孤岛**：AGENTS.md/MCP/SKILL.md 三标准之外，记忆是唯一没有开放标准的一层
6. **模型-harness 协同设计**：模型针对 harness 后训练已开始（GPT-5-codex），harness 学习成果会否被下一代模型吸收而贬值（search tree D-6）

## 参考

- 分支底稿：`Project/survey/branch_D_harness动态.md`（含十大 harness 逐一盘点、记忆机制对比表、官方博客摘编）
- 深挖底稿：`Project/survey/deep_D1_harness遗忘量化.md`（retention 回归证据全查与构建方案）、`Project/survey/deep_B1_可编辑面消融.md`（harness 组件作为进化对象）

---
落款：report-agent · 2026-08-27 12:17
更新：survey-agent · 2026-08-30 10:15（融入 change-002 D1/B1/A5 深挖结论：开放问题 1、2 更新判定并链入新概念页）
