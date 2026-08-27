# 分支 D 调研底稿：Agent Harness 本体的最新动态（2025–2026.8）

> openspec change-001 · 分支 D（D1 主流 harness 盘点 / D2 harness 设计论文 / D3 官方工程博客与趋势）
> 本底稿是后续 wiki 与调研报告的唯一素材来源。信息截至 2026-08-27，重点覆盖 2025 至 2026 年 8 月。

---

## D1 主流 harness 盘点及其记忆 / 学习机制

### D1.1 Claude Code（Anthropic）

- **定位**：终端优先的 coding agent CLI，业界事实标杆；2026 年中已支撑约 4% 的公开 GitHub commits（第三方估计）。闭源产品，但配套 Agent SDK 开放。
- **扩展原语（截至 2026-07 共七类）**：CLAUDE.md / rules、skills、hooks、subagents、agent teams、MCP、plugins。各原语在"加载时机、context 成本、advisory（模型可忽略）还是 deterministic（强制执行）"三个维度上互补。
- **记忆机制（双层）**：
  1. **CLAUDE.md（用户手写指令）**：分层加载——全局 `~/.claude/CLAUDE.md`、项目 `CLAUDE.md`、个人不入库的 `CLAUDE.local.md`、拆分式 `~/.claude/rules/`。全部在会话开始整体注入，属 advisory 性质；单文件上限 4 MiB，官方建议越短遵循度越高。
  2. **Auto memory（agent 自写笔记，2026 年新特性，v2.1.59+ 默认开启）**：目录 `~/.claude/projects/<项目>/memory/`，入口 `MEMORY.md` 作为索引，**仅前 200 行 / 25KB 在会话开始自动载入**；细节移入主题文件（`debugging.md` 等）按需读取。Claude 自主记录四类笔记（构建命令、调试洞见、架构决策、用户偏好/纠正），超限时 harness 会强制要求重写索引。`/memory` 命令管理。
- **Skills（经验沉淀单元）**：`.claude/skills/<name>/SKILL.md`（frontmatter + 正文 + 可选脚本）。**渐进式披露**：会话开始只见 name+description，正文在 `/name` 调用或模型自主匹配时才进入 context。2026 年起 slash commands 与 skills 统一，frontmatter 控制可否自动触发、是否在 subagent 中运行。
- **Subagents**：`.claude/agents/*.md`，独立 context window；2026 年新增 `memory` 字段（`user`/`project`/`local` 三种作用域的持久记忆目录，跨会话学习，属 auto memory 体系）、`isolation: worktree`（git worktree 隔离）、frontmatter 内嵌 hooks、`skills` 预载。
- **Hooks**：生命周期事件（PreToolUse、PostToolUse、SessionStart、Stop 等）触发脚本，deterministic，是唯一"模型无法忽略"的控制面；官方明确"要强制阻止某行为用 hook 而非 CLAUDE.md"。
- **API 侧 context/记忆工具**（对 harness 设计者开放）：memory tool `memory_20250818`（客户端文件式记忆，模型自主 create/read/update/delete `/memories` 目录）、context editing `clear_tool_uses_20250919` / `clear_thinking_20251015`、服务端 compaction `compact_20260112`（2026-01 上线，默认 150K token 触发）。官方内部评测：memory tool + context editing 相对 baseline 提升 39%。
- **2025–2026 关键更新**：2025-09 记忆工具与 context editing 公测；2025-10 Agent Skills 发布；2026 年 auto memory 默认开启、skills/commands 统一、subagent 持久记忆与 worktree 隔离、scheduled tasks（定时自主运行）。

### D1.2 OpenAI Codex CLI

- **定位**：OpenAI 官方 coding agent CLI，**开源**（openai/codex，Rust 实现），GPT-5.x-codex 系列模型专门针对该 harness 后训练。
- **记忆机制：AGENTS.md 指令链**：全局 `~/.codex/AGENTS.md`（**不占预算、整体加载**）+ 从 git root 到 cwd 沿途每个目录的 `AGENTS.md`（每层可用 `AGENTS.override.md` 覆盖），root-first 拼接、leaf 优先级更高；合并总量默认上限 32 KiB（`project_doc_max_bytes`），**超限从最深层（最具体）文件开始静默截断**——已成社区著名坑点（GitHub issue #13386/#37956）。每个文件以独立 user-role message 注入，模型经过训练"高度遵循"。
- **学习/沉淀机制**：无内置 auto memory；沉淀完全靠人工维护 AGENTS.md。2026-04 起新增 `--print-instructions` / `codex debug agents-md` 调试指令链。
- **生态意义**：AGENTS.md 已成**跨工具事实标准**（60,000+ 开源项目采用；Codex、Cursor、Copilot、Jules、Factory、Amp、OpenHands 等均读取）。
- **2025–2026 关键更新**：Rust 重写与开源、AGENTS.override.md、指令链调试工具、预算语义文档化争议。

### D1.3 Cursor

- **定位**：AI IDE（闭源商业产品），2026 年产品线含 IDE、CLI 与 Cloud Agents。
- **记忆机制（三层）**：
  1. **Rules**：`.cursor/rules/*.mdc`，版本化入库；frontmatter 控制四种触发（alwaysApply / globs 匹配自动附加 / description 语义相关时由 agent 拉取 / 仅 @ 手动引用）。优先级 Team Rules → Project Rules → User Rules。
  2. **Memories**：Cursor **自动从对话中提取**的句子级事实（"该 repo 用 pnpm""测试放在源文件旁"），按 git repo 作用域、存于个人 Cursor 配置（不入库、不共享），后续会话自动召回；设置页可审核/删除/关闭。
  3. **MCP 外接记忆**：`.cursor/mcp.json` 挂第三方 memory server，实现跨工具共享记忆（生态涌现出 MemoryLake、Mnemoverse、Basic Memory 等）。
- **学习/沉淀机制**：官方推荐"memory 先自动积累 → 人工审核后提升为 rule"的晋升路径；memories 与 rules 的"个人-临时 vs 团队-契约"分工已成社区共识。
- **2025–2026 关键更新**：Memories 功能逐步 GA（版本间行为有变动）、Team Rules（组织级强制）、AGENTS.md 兼容。

### D1.4 Gemini CLI（Google）

- **定位**：Google 官方开源 coding CLI（google-gemini/gemini-cli），设计明显对标 Claude Code。
- **记忆机制**：
  1. **GEMINI.md 层级加载**：全局 `~/.gemini/GEMINI.md` → 项目 → 子目录，`/init` 生成、`/memory show|refresh` 检查与重载。
  2. **save_memory 工具**：模型可调用的内置工具，把事实追加到 `~/.gemini/GEMINI.md` 的 `## Gemini Added Memories` 节；`/memory add` 为用户手动入口。社区反馈召回一致性一般。
- **学习/沉淀机制**：**实验性 Auto Memory**——从历史会话自动提取记忆更新与**可复用 skills**；skills 框架、hooks（提供从 Claude Code 迁移 hooks 的工具）、extensions（打包 MCP+命令+上下文+policies 的分发单元，`gemini extensions new` 有 skills/hooks/policies 等模板）。
- **2025–2026 关键更新**：skills 框架、auto memory 实验特性、extensions 生态、checkpointing、多目录 workspace。

### D1.5 OpenHands（原 OpenDevin，All Hands AI）

- **定位**：开源通用软件工程 agent 平台（60k+ stars 量级），2025 年发布重写的 **Agent SDK**（NeurIPS 系有配套论文，本库已存 2024 平台论文与 2025 SDK 论文）。
- **记忆机制**：
  1. **Microagents**：`.openhands/microagents/repo.md`（仓库级指令，等价 CLAUDE.md）+ 关键词/仓库名触发的 knowledge microagents（共享知识库，按 trigger 惰性注入——早期版本的"渐进披露"）。
  2. **Condenser 体系**：`LLMSummarizingCondenser`（超限用 LLM 摘要替换被丢弃事件）、`AmortizedForgettingCondenser`、`RecentEventsCondenser` 等可插拔 context 压缩策略。
  3. **SDK 持久记忆（2026，opt-in）**：双层目录——用户级 `~/.openhands/memory/` 与项目级 `<repo>/.openhands/memory/`；`MEMORY.md` 作为"精选耐久事实索引"注入 system prompt（`<MEMORY_CONTEXT>` 块），细节写每日 log；system prompt 指示 agent 任务尾声记录、去重合并、剔除可轻易重新发现的事实、不记密钥；**明确警告记忆文件可能含 prompt injection，须当作未验证提示**。
- **学习/沉淀机制**：agent 自维护 MEMORY.md（"越用越懂项目"）；AGENTS.md 兼容；skills 合并机制（项目/用户级覆盖默认）。
- **2025–2026 关键更新**：SDK 重写、持久记忆特性、condenser 设置产品化（SaaS 组织级默认值）。

### D1.6 SWE-agent / mini-swe-agent（Princeton）

- **定位**：学术研究 harness。SWE-agent（2024）提出 **Agent-Computer Interface（ACI）** 概念——为 LLM 专门设计的接口层显著影响性能。**mini-swe-agent**（2025-06 创建，6.7k stars）反其道行之：约 100 行 Python、无任何专用工具、只用 bash subprocess、无状态线性历史。
- **记忆机制**：mini 刻意**零记忆、零 scaffold**——定位是"做 FT/RL 或跨模型对比时避免过拟合到特定 scaffold"的参考基线；Gemini 3 Pro 在其上达 SWE-bench Verified 74%，证明前沿模型已内化大部分 harness 功能。
- **学习/沉淀机制**：无；社区衍生 Exp-SWE-agent 等加装持久记忆模块的变体。
- **2025–2026 关键更新**：mini v2（更简的无状态架构）；被多方（HAL、第三方基准监测）推荐为 **locked-harness 跨模型评测协议**的参考实现；推出 ProgramBench。

### D1.7 Aider

- **定位**：最早的开源终端 coding agent 之一（35k+ stars，93 个 release），单人主导、2025 年后开发节奏放缓。
- **记忆机制**：**repo map**——用 PageRank 对代码依赖图排序、动态压缩进 context 的仓库地图（结构性 context 而非跨会话记忆）；`CONVENTIONS.md` 约定文件手动加载。
- **学习/沉淀机制**：每步修改自动 git commit（会话历史即 git 历史，可审计可回滚）；architect/editor 双模型分工。无 auto memory。
- **2025–2026 关键更新**：基本维持原架构；在 SWE-bench Verified 上约 32%（Claude 4.5），已明显落后于 OpenHands/Claude Code 等，反映"静态 repo map + 无记忆"路线的天花板。

### D1.8 Devin / Devin Desktop（Cognition）

- **定位**：闭源自主软件工程师产品；2025-07 收购 Windsurf，2026-06 将其改名为 Devin Desktop（IDE 形态）。
- **记忆机制**：
  1. **Knowledge（云端 Devin 核心）**：条目 = 内容 + **Trigger Description**（触发描述，检索键）；可 pin 到单 repo / 全部 repo / 不 pin（纯相关性召回）。**Devin 会根据用户在对话中的反馈自动建议新 Knowledge 或建议更新既有条目**，用户审核后入库；企业级 Knowledge 支持组织级规范下发。
  2. **Playbooks**：把成功 session 提炼成可复用的任务剧本（程序性记忆）。
  3. **Devin Desktop**：旧 Cascade agent 的 Memories（自动生成、存本地 `~/.codeium/windsurf/memories/`）已列为 legacy，官方建议迁移到 skills / rules / AGENTS.md；新 Devin Local agent 不持久化 memories，第三方（如 Hindsight）用"remote MCP + always-on rule"补跨会话记忆。
- **学习/沉淀机制**：Advanced Capabilities——session 结果分析（成败归因、模式提取）、playbook 创建与改进、知识库去重/合并/冲突消解，全部可经 **Devin MCP server** 编程访问。
- **2025–2026 关键更新**：知识建议自动化、MCP 化知识管理、Desktop 整合与 memories 退役（转向 rules/skills 这类显式可控载体）。

### D1.9 Manus

- **定位**：闭源通用 agent 产品（Monica 团队），其 2025-07 博客《Context Engineering for AI Agents: Lessons from Building Manus》是 harness 设计领域引用最广的工程文章之一。
- **记忆机制**：**把文件系统当"终极 context"**——无限大、天然持久、agent 可自操作；压缩必须可恢复（如网页内容可丢但 URL 保留）。todo.md **复述机制**（不断重写任务清单把全局目标拉回注意力近端，对抗 lost-in-the-middle）。
- **学习/沉淀机制**：框架自身经历四次重写（自称 "Stochastic Graduate Descent"）；保留错误于 context 中让模型隐式更新信念（不擦除失败记录）；KV-cache 命中率作为最重要生产指标（前缀稳定、只追加、工具用 logits 掩码而非移除）。
- **2025–2026 关键更新**：wide research（大规模并行子 agent）等产品功能；博客六原则成为行业 context engineering 的公共词汇。

### D1.10 OpenClaw（开源现象级新秀）

- **定位**：2026 年爆发的开源个人 agent harness（Node.js，**250k+ stars，GitHub 史上 star 最多的 agent 项目**），24/7 自托管、经 Telegram/WhatsApp/Slack 等渠道对话，模型可插拔（"换脑不换记忆"）。
- **记忆机制**：**全 Markdown 文件式认知状态**——`SOUL.md`（人格与规则）、`IDENTITY.md`、`USER.md`（对用户的建模）、`AGENTS.md`（启动自检清单：先读 SOUL.md、USER.md、当日笔记）、`MEMORY.md`（精选长期记忆，仅主会话读）+ `memory/YYYY-MM-DD.md` 每日短期日志；接近 compaction 阈值时系统提示"把耐久记忆固化到文件"。每次启动**主动重读**这些文件——"重新学会自己"。
- **学习/沉淀机制**：SOUL.md 随使用持续被 agent 自我更新（LangChain 博客将其作为 agent 级 context learning 的代表案例）；ClawHub 生态 13k+ skills。
- **痛点与生态**：默认把全部 workspace 文件无条件注入每轮 system prompt，token 成本高昂；社区涌现 SoulClaw（三级分层加载，Tier3 记忆永不注入、只靠 `memory_search` 工具按需检索，省 60%）、MemClaw（L0/L1/L2 三层语义记忆 + 向量检索，声称省 95%）等记忆优化插件——**"文件全量注入 vs 分层按需检索"之争成为 2026 年记忆工程的活案例**。

### D1.11 其它值得记录

- **LangChain Deep Agents**：LangChain 的开源模型无关通用 base harness，原生支持用户级 memory、background learning；LangGraph 提供 checkpointing（线程内短期记忆）+ store（跨会话长期记忆），LangMem 提供记忆抽取/检索工具抽象。
- **GitHub Copilot**：custom instructions（`.github/copilot-instructions.md`）+ 2026 年对 AGENTS.md 的兼容；coding agent 形态跟进。
- **趋势注**：几乎所有 2025-2026 新 harness 都收敛到"分层 markdown 指令文件 + 按需披露的 skills + 可选 auto memory"三件套。

---

## D2 harness 设计相关论文与技术报告（2025–2026）

> 注：本分支新下载论文见文末索引；`raw/papers/` 中已有其它分支下载的 Mei et al. context engineering 综述、SWE-agent ACI、OpenHands 平台/SDK、ACE 等，此处不重复登记但列入分析。

1. **Stop Comparing LLM Agents Without Disclosing the Harness**（Zhang, Wang, Ge, Xu, Hamm, Reddy · arXiv:2605.23950 · 2026）
   链接：https://arxiv.org/abs/2605.23950（本库已存：2026-zhang-harness-disclosure.pdf）
   提出 **Binding Constraint Thesis**：长程任务上性能方差更多由 harness 配置而非模型决定，现行评测把 harness 收益错误归因给模型。控制论形式化：harness 是闭环系统的控制器、LLM 是其调度的随机策略。证据：SWE-bench Pro 上六个前沿模型在统一 SEAL scaffold 下仅差 4.9pp，而固定 Claude Opus 4.5 换 harness 差 9.5pp；HAL 报告跨 scaffold 差距 34–48pp；单加一个 WarpGrep 搜索 subagent 即 +2.1~2.2pp、足以翻转模型排名。提出 E/T/C/S/O/V 六层 harness 披露协议与 locked-harness 评测。

2. **Harness-Bench**（Yao et al. · 2026）
   链接：见 raw/papers/index 其它分支条目（本库已存：2026-yao-harness-bench.pdf）
   固定任务环境、系统改变 scaffold 的诊断基准：6 个可配置 harness × 8 个模型 × 106 任务、5088 次 factorial 运行。最高与最低 harness 聚合差 23.8pp；**模型越强对 harness 越不敏感，弱模型对执行层高度敏感**——harness 是"模型能力的放大器/瓶颈"。

3. **Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks**（Zheng et al.（华为诺亚等）· arXiv:2606.12344 · 2026）
   链接：https://arxiv.org/abs/2606.12344
   为异构通用 harness（"claws"）建立公平可比的 SWE-bench 式协议（固定 prompt、预算、workspace 契约、patch 提取、评测器），350 题 8 语言。同一 GLM 5.1 底座：极简 direct-diff 适配器 19.1% vs 完整适配器 73.4%；扫描实验中模型选择影响 29.4pp、harness 选择影响 27.4pp——**harness 与成本应作为评测一等公民**。

4. **Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses（AHE）**（Lin, Liu, Pan et al.（复旦等）· arXiv:2604.25850 · 2026）
   链接：https://arxiv.org/abs/2604.25850
   让 agent 自动进化自己的 harness：三大可观测性支柱——组件可观测（每个可编辑组件文件化、动作空间显式可回滚）、经验可观测（把百万级轨迹 token 蒸馏成分层证据库）、决策可观测（每次编辑绑定自declared 预测、下一轮结果证伪）。10 轮迭代把 Terminal-Bench 2 pass@1 从 69.7% 提到 77.0%，超过人工设计的 Codex harness（71.9%）与 ACE 等自进化基线；冻结后跨模型家族迁移 +5.1~10.1pp。**消融定位收益主要来自 tools、middleware 与 long-term memory，而非 system prompt**。

5. **Harness Continual Learning: Continual Adaptation Beyond Model Parameters（HCL）**（Kang, Gu, Lv, Li, Wang, Gao（南大等）· arXiv:2608.19013 · 2026）
   链接：https://arxiv.org/abs/2608.19013
   **与本项目主题最直接相关的论文**。把整个可变 harness 状态（prompts、memories、tools、skills、路由策略）当作统一的持续学习对象，正式提出 **harness-level forgetting**：更新任一 harness 组件可能在模型完全不动的情况下破坏既有可靠行为。提出 guarded harness evolution：Continual Optimizer 从执行反馈起草候选更新，Continual Evaluator 检查"当前改进 + 历史保持 + 有效性"后才 commit。把持续学习研究从权重扩展到 harness 状态。

6. **SIGIL: Compiling Agent Skills into Typed Harnesses**（Dantanarayana, Kashmira, Tang, Mars（密歇根大学）· arXiv:2607.27309 · 2026）
   链接：https://arxiv.org/abs/2607.27309
   量化"prose skill 的脆弱性"：30 个 skills、两代模型上，纯 prose agent 只执行了自己 skill 规定步骤的 56%（产物却能过输出检查）。提出 Skill Compilation：经 AG-IR（类型化 agentic 中间表示，分离模型拥有的认知与代码拥有的机制）把 prose skill 编译成可执行 harness——规定步骤执行率 86%、完整走完流程 2.3 倍、token 0.58 倍，且**保证与模型无关**（prose 在 56%→68% 间摆动，编译后稳定 86%）。指出"指令式沉淀"与"程序式沉淀"的根本差异。

7. **The Scaffold Effect in Coding Agents: Harness Choice as a Hidden Variable in Coding-Agent Evaluation**（Vats, Golev · arXiv:2607.22585 · 2026）
   链接：https://arxiv.org/abs/2607.22585
   300 次受控试验比较不同 harness 下同一模型的通过率、每解决任务 token 数、空转轮次与失败模式，论证 harness 选择是 coding-agent 评测中的隐藏变量，呼应 #1 的披露主张。

8. **Code Isn't Memory: A Structural Codebase Index Inside a Coding Agent**（Bhola, Krishnan, Kurmala, Mukunda（SuperAGI）· arXiv:2606.22417 · 2026）
   链接：https://arxiv.org/abs/2606.22417
   在固定模型下改变开源 harness 配置：把结构化代码库索引（符号级）作为一等工具内置于 SuperCoder harness，与 Aider 的 PageRank repo map、语义/图检索路线对比，论证"代码结构索引 ≠ 记忆"、二者在 harness 内的职责应分离。含一份很好的 coding-agent harness 谱系综述（SWE-agent ACI → OpenHands → Aider → AutoCodeRover → OpenCode）。

9. **（背景，本库已存）SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**（Yang et al. · 2024）：首次系统论证接口层设计（ACI）本身显著影响 agent 性能，是 harness 研究的起点文献。
10. **（背景，本库已存）A Survey of Context Engineering for Large Language Models**（Mei et al. · 2025）：context engineering 的系统化综述，为 D 分支提供分类框架。

---

## D3 官方工程博客与 changelog（2025–2026 重点）

1. **Anthropic《Effective context engineering for AI agents》**（anthropic.com/engineering · 2025-09）
   把 context 定义为"有边际收益递减的有限资源"（attention budget），提出从 prompt engineering 到 context engineering 的范式转移；系统化三大策略：compaction、结构化笔记（note-taking / agentic memory）、subagent 隔离；"寻找最小的高信号 token 集"。该文成为 2025-2026 各家 harness 文档反复引用的锚点。

2. **Anthropic《Managing context on the Claude Developer Platform》**（claude.com/blog · 2025-09-29，随 Sonnet 4.5 发布）
   正式推出 **memory tool**（`memory_20250818`，客户端文件式跨会话记忆）与 **context editing**（自动清理旧 tool results）。内部 agentic search 评测：两者合用 +39%，仅 context editing +29%。2026-01 追加服务端 **compaction API**（`compact_20260112`）。三件套（compaction / 清理 / 记忆）自此有一等 API 支持。

3. **Anthropic：Claude Code auto memory 与 Agent Skills**（code.claude.com docs/changelog · 2025-10 至 2026）
   Agent Skills（2025-10）确立 SKILL.md + 渐进披露格式，随后被 Gemini CLI、OpenHands 等借鉴，走向跨工具标准；auto memory（2026，v2.1.59+）让 harness 默认自动积累跨会话经验——**首个在旗舰产品中默认开启 agent 自写记忆的主流 harness**。

4. **Manus《Context Engineering for AI Agents: Lessons from Building Manus》**（manus.im/blog · 2025-07）
   六条工程原则：围绕 KV-cache 设计（前缀稳定、只追加）、mask 而非移除工具、文件系统作为终极 context、用复述操纵注意力（todo.md）、保留错误、打破 few-shot 定式。“我们把 agent 框架重写了四次”——harness 设计是实验科学的最佳注脚。

5. **Cognition《Don't Build Multi-Agents》（2025-06）与《Multi-Agents: What's Actually Working》（2026）**
   前者：共享完整轨迹而非消息、行动携带隐式决策——并行子 agent 的假设冲突使多 agent 系统脆弱，主张单线程线性 agent + 专门压缩模型（Cognition 训练了专用模型识别并保留关键上下文信息）。后者（2026 更新）：有效的多 agent 模式收敛为"读 only subagents + 写单线程"与 map-reduce-and-manage；无结构 swarm 是干扰项。与 Anthropic《How we built our multi-agent research system》（2025-06）对照阅读：研究型可并行、编码型需共享上下文——**多 agent 是 workload 决策而非架构信仰**。

6. **LangChain《Context Engineering for Agents》（2025）与《Continual learning for AI agents》（2026）**
   前者提出 write / select / compress / isolate 四象限。后者给出**本项目应直接采用的三层学习分类**：模型层（权重）、harness 层（驱动代码 + 常驻指令与工具）、context 层（可配置的指令/skills/memory）；context 学习又分 agent 级（如 OpenClaw 自更新 SOUL.md）与租户级（Hex Context Studio、Decagon Duet、Sierra Explorer 等每客户独立 context）；并展示用 LangSmith trace + coding agent 改进自家 Deep Agents harness 的闭环。

7. **OpenAI：Codex 提示指南与 AGENTS.md 生态**（developers.openai.com cookbook · 2025-2026）
   官方文档化 AGENTS.md 注入机制（逐文件 user-role message、root→leaf）与"模型已被训练遵循这些指令"；2026 年社区量化研究《The State of AGENTS.md》扫描 36 个头部 agent 仓库：均分 70/中位 C，**连 agent 厂商自己都写不好指令文件**——说明人工维护指令的天花板。

8. **OpenHands 文档/博客：SDK 持久记忆与 condenser**（docs.openhands.dev · 2026）
   persistent memory 指南明确了开源界最完整的 auto memory 设计规范（双层 tier、MEMORY.md 索引、写入纪律、prompt injection 警告），可作为本项目 develop 分支的直接参考实现。

9. **Devin 文档：Knowledge / Playbooks / Advanced Capabilities**（docs.devin.ai · 2025-2026）
   商业产品中最完整的"经验沉淀流水线"：反馈→自动 Knowledge 建议→人工审核→trigger 检索；成功 session→playbook；知识库自动去重/冲突消解，全套开放 MCP 接口。

10. **2026 趋势速记（综合第三方分析）**
    - 前沿模型在 SWE-bench Verified 上已收敛到 1pp 以内，而 scaffold 变动可摆动 22+pp（particula.tech、Weave Research 等监测）——**竞争主战场从模型转向 harness**；
    - 模型开始**针对特定 harness 后训练**（GPT-5-codex 对 Codex CLI、MiniMax 对 OpenClaw scaffold 的自进化训练），模型与 harness 走向协同设计；
    - AGENTS.md（指令）、MCP（工具）、Agent Skills（技能）形成三大开放标准栈；
    - "文件式 markdown 记忆"压倒向量库成为主流（可审计、可 git、可迁移），但 token 成本问题催生分层加载/按需检索的第二代方案。

---

## 综合分析

### harness 记忆 / 学习机制对比表

| Harness | 手写指令（advisory） | 自动记忆（agent 自写） | 技能/程序性沉淀 | 强制控制面 | 跨会话学习成熟度 |
|---|---|---|---|---|---|
| Claude Code | CLAUDE.md 分层 + rules | **auto memory 默认开**（MEMORY.md 索引 + 主题文件，200 行/25KB 限载） | skills（渐进披露）+ subagent 持久记忆 | hooks（deterministic） | ★★★★★ |
| Codex CLI | AGENTS.md 链（32KiB 预算） | 无 | 无内置 | 无 | ★★ |
| Cursor | rules（.mdc，四种触发） | Memories（自动提取、个人、不入库） | 规则晋升路径；skills 兴起 | 无 | ★★★ |
| Gemini CLI | GEMINI.md 层级 | save_memory 工具 + 实验性 auto memory（可提取 skills） | skills + extensions | hooks | ★★★ |
| OpenHands | repo.md + 触发式 microagents | SDK 持久记忆（双 tier MEMORY.md，opt-in） | skills 合并；condenser 可插拔 | 事件流架构 | ★★★★ |
| SWE-agent/mini | 无（刻意） | 无（刻意） | 无 | 无 | ★（评测基线） |
| Aider | CONVENTIONS.md | 无（repo map 是结构 context 非记忆） | 无 | git 逐步提交 | ★ |
| Devin | Knowledge（trigger 检索）| 自动 Knowledge 建议（人工审核入库） | **Playbooks**（session→剧本） | 产品内控 | ★★★★★ |
| Manus | 系统内置 | 文件系统即记忆 + todo.md 复述 | 框架层迭代 | logits 掩码 | ★★★★（产品内隐） |
| OpenClaw | SOUL/AGENTS/USER.md | MEMORY.md + 每日日志（启动重读） | ClawHub skills | 无 | ★★★★（成本高） |

### 共性缺口

1. **写入策略无理论**：何时记、记什么、如何合并去重，各家全靠 prompt 里的"纪律条款"（OpenHands 的写入规范、Claude 的 200 行索引约束），没有可度量的记忆价值函数。
2. **harness-level forgetting 无人防护**：除 HCL（2026-08）外，没有任何生产 harness 对"更新记忆/skills 导致既有行为回归"做保持性检查；没有 retention 回归集。
3. **记忆安全**：持久记忆文件是新攻击面（OpenHands 官方已警告 memory 文件可携带 prompt injection；memory poisoning 在 Anthropic cookbook 中也被点名），防御手段几乎空白。
4. **记忆的 token 经济学**：全量注入（OpenClaw）与索引+按需（Claude auto memory、SoulClaw Tier3）两条路线并存，缺乏公开的召回率/成本 tradeoff 实证。
5. **跨工具记忆孤岛**：Cursor Memories、Claude auto memory、Devin Knowledge 互不相通；MCP memory server 是唯一在野的互通方案，无标准。
6. **沉淀止步于文本**：多数"学习"= 追加 markdown。SIGIL 证明 prose 沉淀执行保真度仅 56%，程序化/编译式沉淀刚刚起步。

### 2026 趋势

- **harness 成为持续学习的载体**：LangChain 三层分类（model/harness/context）、HCL 的正式问题定义、AHE 的自动进化闭环，共同把"harness 状态"确立为继权重之后的第二学习对象——这正是本项目选题的时代背景。
- **评测改革**：harness 披露协议、locked-harness（mini-swe-agent 参考实现）、Claw-SWE-Bench 的 adapter 契约、Harness-Bench 的 factorial 设计——"报告成绩必须报告 harness"正在成为规范。
- **auto memory 默认化**：从 2025 的"手写指令文件"到 2026 的"agent 自写记忆默认开启"（Claude Code → OpenHands → Gemini 实验特性），一年内完成范式切换。
- **标准栈成型**：AGENTS.md + MCP + SKILL.md 三标准让指令/工具/技能可移植，记忆是唯一还没有开放标准的一层。
- **模型-harness 协同设计**：模型针对 harness 后训练，harness 针对模型进化（AHE），二者边界开始溶解。

### 对本项目研究方向的启示

1. **最有价值的研究空位是 D+C 交叉**：HCL 刚提出 harness-level forgetting，但其 Continual Evaluator 依赖的"历史正确行为集"在实践中几乎无人维护——**构建 harness 记忆/技能更新的 retention 基准与守护机制**是可发表且可落地的方向。
2. **记忆写入策略可实验化**：各 harness 的写入纪律是纯 prompt 工程，用"多做实验多标注"的项目资源优势，可以对写入时机/粒度/合并策略做受控研究（何种记忆条目在未来会话中真正被用到并改善结果）。
3. **prose→程序的沉淀谱系**：memory（事实）→ rule（约束）→ skill（流程）→ 编译 harness（SIGIL）构成沉淀强度光谱，"何种经验应沉淀到哪一层"没有任何理论——适合形成 wiki 的核心概念页并展开研究。
4. **评测先行**：跨会话学习收益目前只有厂商内部数字（Anthropic +39% 等），缺公开基准；结合分支 C 的 StreamBench/LongMemEval 等，可设计"同 harness 连续任务序列"的学习曲线评测。

---

## 下一层待深挖问题（供下一轮 BFS）

1. **harness-level forgetting 的量化**：HCL 之外还有哪些工作触及"更新 prompt/memory/skill 导致行为回归"？retention 回归集如何构建、多大规模才有统计效力？
2. **auto memory 写入策略逐字对比**：抓取 Claude Code、OpenHands SDK、Gemini auto memory 的实际 system prompt/源码，对比写入时机、格式约束、合并规则，并实测记忆命中率。
3. **记忆安全与 memory poisoning**：持久记忆文件的攻击面分类（injection、投毒、跨项目泄漏）、现有防御（OpenHands 的"未验证提示"框架、路径校验）与评测方法。
4. **记忆分层加载的成本-召回实证**：全量注入 vs 索引+按需（200 行阈值）vs 向量检索（MemClaw 类）三路线在真实长程任务上的对照实验设计。
5. **skills 的可移植性与编译路线**：SKILL.md 跨 harness（Claude/Gemini/OpenHands）行为差异；SIGIL 式编译在多大技能范围内可行、faithfulness 如何保证。
6. **模型-harness 协同训练**：针对特定 harness 后训练模型（GPT-5-codex、MiniMax/OpenClaw）的公开细节与对"harness 可迁移性"的影响——harness 学习的成果会否被下一代模型吸收而贬值？

---

落款：survey-agent-D · 2026-08-27 11:37
