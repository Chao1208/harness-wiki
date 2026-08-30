# 剪藏:Claude Code 记忆机制与跨项目限制(vectorize.io 两篇 + mem0 博客)

- 来源:
  - https://vectorize.io/articles/claude-code-cross-project-memory
  - https://vectorize.io/articles/claude-code-memory
  - https://mem0.ai/blog/claude-code-memory
- 剪藏时间:2026-08-28(survey-agent-A5,change-002)
- 相关方向:A5——为"harness 独有评测维度"提供机制事实(评测对象长什么样)

## Claude Code 原生记忆的硬限制(2026-08 时点)

1. **Auto Memory 按仓库隔离**:`MEMORY.md` per-repository,跨仓库/跨项目不可见;
2. **启动加载上限**:MEMORY.md 有 **200 行 / 25KB** 的 startup load 窗口,超出部分不进上下文;
3. **启动检索是索引式而非向量语义式**,词汇不匹配会漏掉 topic 文件;
4. **Dreams(Anthropic API 原语,驱动 Auto Dream)一次只固结一个记忆库**:做去重、最新值替换、洞见浮现,但**不跨 user_id/agent_id/session_id/org_id scope 融合**——单项目洞见不会织入跨项目心智模型。

## 原生跨项目的 4 种 workaround

- `~/.claude/CLAUDE.md`(用户级偏好,所有项目加载);
- symlink `.claude/rules/`(团队约定);
- 用户级 `~/.claude/rules/`;
- `--add-dir` + `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` 环境变量。

## 生态动向

- 外部记忆层(Mem0、Hindsight)以 MCP/插件形态补"跨项目、语义检索"缺口;Hindsight 自报 LongMemEval 94.6%;
- Mem0 插件在 Claude Code 生命周期挂钩:SessionStart 载入、UserPromptSubmit 检索、PreCompact 存会话摘要、PreToolUse **拦截 MEMORY.md 写入**。

## 对 A5 的意义

- 这些机制(200 行加载窗、per-repo scope、Dreams 单库固结、compaction 前摘要)构成 harness 记忆的**独有评测维度清单**,而当前没有任何学术基准把它们作为受控变量;
- "记忆放置决定压缩存活"(branch A 已记录)+ 本文的加载窗语义 = 新基准可直接操纵的实验旋钮。
