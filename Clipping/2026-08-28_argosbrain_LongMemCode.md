# 剪藏：LongMemCode（独立实验室基准，无 arXiv）

- 来源：https://argosbrain.com/papers/longmemcode-benchmark 与 https://github.com/CataDef/LongMemCode
- 剪藏日期：2026-08-28
- 剪藏人：survey-agent-C6（change-002 · C6 方向）
- 状态：独立作者（Aurelian Jibleanu, "Neurogenesis", 2026-04），MIT 许可，未见同行评审 venue；作为生态信号记录，引用时需标注非同行评审。

## 核心内容

- 定位："LongMemEval 之于会话记忆 = LongMemCode 之于代码记忆"——**隔离评测 coding agent 记忆系统的检索组件**（质量、延迟、压缩），不评端到端任务成功。
- 规模：20 个真实开源代码库（后扩至 31 个）、16 种语言、约 8,000 个场景、9 类任务（补全、修 bug、重构、测试生成、加功能、API 发现、控制流、配置面、safety-net）；ground truth 由语料确定性计算，**无 LLM judge**。
- 基线结果：grep 文本检索地板 6.3–54.4% 加权准确率；结构化参考系统 99.2–100%，P99 延迟 ≤0.82ms、近零成本。通用记忆系统（Mem0/Zep/Letta）读路径需 LLM 调用，每次查询 200–2000ms。
- 配套立场：结构查询（符号存在/调用者/覆写）应走确定性图遍历，语义查询走向量检索——单一机制路由两类查询会系统性掉分。

## C6 调研注记

- 该基准评的是"记忆读路径"的机械质量，与 lifelong 学习（写什么、学多快、忘多少）正交；说明"coding 记忆评测"已在组件层出现细分，进一步压缩单纯"记忆检索质量"型论文的空间。
