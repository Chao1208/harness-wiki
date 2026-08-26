# harness-wiki · CLAUDE.md

> 版本见 `version.yaml`（当前 0.1）。本文件是所有 agent 的最高行为准则。
> 红线：本文件永远不得超过 200 行。新增内容前先删减，细则外移到 `openspec/` 或 `wiki/`。

## 1. 项目使命

建设 LLM-wiki，主题：**Harness 的记忆与持续学习**（memory & continual learning for agent harness）。
三个目标，优先级相同：

1. 汇集该领域人类当前最先进的研究与工程实践；
2. 指导解决现实问题（可落地的设计与代码）；
3. 指明研究方向，产出可发表于 ML 顶会（NeurIPS / ICML / ICLR 等）的论文。

## 2. 目录结构（顶层固定，不得擅自增删）

```
Clipping/            # 网页剪藏、临时收集的原始素材
raw/                 # 一切下载材料的归档（只进不改）
  papers/            #   论文 PDF（下载即归档，不许只留链接）
  dataset/           #   数据集
wiki/                # 知识沉淀主体（Karpathy LLM-wiki 风格）
Project/             # 软件工程区，按 agent 分目录
  survey/            #   survey agent 工作区
  survey_reports/    #   调研报告（html）
  qa/                #   qa agent 工作区
  qa_reports/        #   测试报告（html）
  review/            #   review agent 工作区
  review_reports/    #   评审意见（html）
  notebooks/         #   全体 agent 的工作日志（html）
  develop/           #   develop agent 工作区（代码实现）
openspec/            # 工程管理：spec、change、任务分解、search tree
research/            # 论文撰写（草稿 html，投稿前转 LaTeX）
```

## 3. 多 Agent 架构

- 至少四个独立 agent：**develop、qa、review、survey**，各自只在自己的 `Project/<name>/` 工作区内工作，产出写入对应 `_reports/` 或 `wiki/`。
- 主 session 只做：任务分解、派发 subagent、验收结果、与用户确认业务问题。**具体子任务一律用 subagent + workflow 完成**，保持主 session 历史清晰。
- 后台长任务必须用 harness 后台机制（工具自带 `run_in_background: true`），禁止 `nohup ... &` 裸后台。
- 完成判定看真实产出（结果文件有内容、退出码正常），不轻信"任务完成"信号，须用 Read/ls 核实。

## 4. 执行决策原则

1. **业务逻辑**的澄清与判断 → 找用户确认；**技术选型与技术方案** → 参考行业先进经验独立决定，不必请示。
2. 多分支探索采用**广度优先（BFS）**：先在 `openspec/` 建好 search tree（yaml 或 markdown），列出全部分支后再逐层展开，禁止未建树就深入单一分支。
3. 资源假设：大模型 token 近乎无限；有大量本科毕业的专业标注人员可供调度。据此优先选择"多做实验、多标注、多验证"的方案。

## 5. 工程管理（openspec）

- 用 openspec 框架管理需求与变更：新能力先写 spec / change proposal，评审通过再实现。
- 所有跨 agent 的任务分解、里程碑、search tree 都落在 `openspec/` 中，作为唯一事实来源。

## 6. 搜索与资料获取协议

| 来源 | 协议 |
|---|---|
| arXiv | 必须走 https（`https://arxiv.org/...`） |
| 期刊/引文 | Crossref / OpenAlex / Semantic Scholar API |
| 其余 | websearch |

- Semantic Scholar API key 存放于项目根 `.env`（`S2_API_KEY`），**已 gitignore，严禁写入任何会提交的文件**。
- 凡下载/阅读过的材料一律归档：论文 → `raw/papers/`，数据集 → `raw/dataset/`，网页剪藏 → `Clipping/`。
- 调研**结论**写入 `wiki/`，调研**过程报告**写入 `Project/survey_reports/`，原始数据留在 `raw/`。

## 7. 文档规范

1. 与用户交互、所有文件内容一律用**中文**（代码、术语、引文除外）。
2. 每份文档落款：时间**具体到分钟**（如 `2026-08-26 12:20`）+ 撰写者（具体 agent 名，如 `survey-agent`）。
3. 格式约定：
   - 工作日志 → `Project/notebooks/`，html；
   - qa 测试报告 → `Project/qa_reports/`，html；
   - review 评审意见 → `Project/review_reports/`，html；
   - survey 调研报告 → `Project/survey_reports/`，html；
   - 论文草稿 → `research/`，html；投稿前用 LaTeX 重写一遍。
4. wiki 条目遵循 Karpathy LLM-wiki 理念：一个概念一页、层层链接、结论先行、附引文与 raw 材料路径。

## 8. 版本与配置管理

- 全局配置与版本号统一用 yaml 管理，入口为根目录 `version.yaml`；当前版本 **0.1**。
- 版本升级须在 `version.yaml` 中登记：版本号、日期、变更摘要、负责 agent。

## 9. Git 规范

- 代码仓库托管 GitHub，账号 **Chao1208**；克隆/远程一律用 **SSH**（`git@github.com:...`），不用 HTTPS。
- **commit 不需用户批准**：有进展随时 commit；消息用中文，格式 `[agent] 动作：摘要`（如 `[survey] 新增：MemGPT 论文调研`）。
- 大文件（`raw/` 下 PDF、数据集）按需用 Git LFS 或在 `.gitignore` 中排除超大数据集，但目录结构与索引文件必须入库。
- `.env` 及一切密钥永不入库。

## 10. 红线（违反即为事故）

1. `CLAUDE.md` ≤ 200 行，永久有效。
2. 密钥不入库、不写入可提交文件。
3. 下载过的材料必须归档到 `raw/` 或 `Clipping/`，不允许"读完即弃"。
4. 报告类文件只能落在各自规定目录，格式为 html。
5. 顶层目录结构不得擅自变更；确需变更走 openspec 流程并经用户确认。

---
撰写者：main-agent · 2026-08-26 12:20
