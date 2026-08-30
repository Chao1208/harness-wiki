# 剪藏:AHE 与 Self-Harness 代码发布核实

> 联网核实时间:2026-08-30 12:52 · main-agent
> 背景:HarnessAblate(B1 选题)的两个核心对照系统是否开源,直接影响实验基建复用与竞争风险评估
> 来源:websearch(GitHub 仓库页/README/arXiv HTML)+ GitHub API(仓库元数据与目录列表),检索词与关键页面见下文链接

## 结论:两篇均已放出官方代码

### 1. AHE(arXiv 2604.25850)——已开源,且是活跃的完整框架

- 官方仓库:https://github.com/china-qijizhifeng/agentic-harness-engineering
- MIT 协议,860 stars / 99 forks,创建于 2026-04-23,框架 2026-04 发布
- 团队:复旦 + 北大 + 上海奇绩智峰(Qiji Zhifeng / Nex AGI)
- 时间线:2026-04-28 论文上 arXiv;2026-05-14 AHE(GPT-5.5)以 84.7% 登 Terminal-Bench 2.0 榜第 3
- 内容:完整进化框架(`evolve.py` 主循环:workspace 管理、评估、归因、恢复、回滚),依赖 uv/E2B/Serper,论文附录声明附录 prompt 与公开仓库逐字一致
- **对 HarnessAblate 的含义**:(a) 六面文件级暴露的 seed harness 可直接复用,基建成本大降;(b) 竞争风险上调——该团队工程能力强、仓库活跃,做前瞻消融只差一步,4-6 周实验窗口的紧迫性得到证实

### 2. Self-Harness(arXiv 2606.09498)——已开源,代码真实但更新停滞

- 官方仓库:https://github.com/qzzqzzb/Self-Harness(README 含官方 citation,作者 Zhang et al., Shanghai AI Lab)
- Python,约 1.6MB,90 stars;目录:acceptance / diagnosis / eval / harnesses / proposer / workflow(三阶段循环齐全)
- 创建 2026-07-01,最后 push 2026-07-02——**此后未更新**;README 结果表只有 Terminal-Bench 2.0 三模型("More results are coming soon"),而论文 v3(2026-08-20)已扩到 9 个模型×基准对(含 AppWorld、SWE-bench Verified),代码落后于论文
- 另有第三方复现 NullLabTests/self-harness-starter(TypeScript,"inspired by",非官方)
- **对 HarnessAblate 的含义**:计划用作固定进化算法的 Self-Harness 循环有官方参考实现可对照,但需自行补齐 v3 的扩展;其"只能改声明过的面"的有界可编辑面机制正好是我们文件级 ACL 设计的现成范本

## 待办含义

- 实验基建方案更新:优先评估「AHE seed harness + Self-Harness 式循环」的组合复用,预计省 1 周基建时间
- 竞争监控:AHE 仓库(china-qijizhifeng)与 Self-Harness 仓库各设月度检查点

---
落款:main-agent · 2026-08-30 12:55
