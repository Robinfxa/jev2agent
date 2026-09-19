# 项目整理记录 · 2026-09-19

## 版本判断

较新的 session-transfer 包增加会话背景与启动说明，没有更新工程合同。已核对内嵌 handoff ZIP、独立 ZIP、展开文件和便笺字节一致；ZIP 清单通过。

## 项目结构

按用户要求拆除交接包外层，现行架构与宿主合同归入 `docs/architecture/`，实施路线归入 `docs/plans/`，E0 要求归入 `docs/validation/`，决议归入 `docs/decisions/`，接续背景归入 `docs/handoff/`。当前合同引用或定义索引依赖的历史章节保留在 `docs/references/`。

删除纯封包工具、合成测试、证据空模板、旧状态/清单/报告、重复基线和评审产物、内部 ZIP。设计意图 JSON 放在架构目录，明确不是可运行配置。原交接文件夹完整移除。

当前无生产源码或产品测试。旧 23 项辅助测试不作为产品验收依据；真正的 E0 义务保留。当前状态见 [STATUS](../STATUS.md)，后续路线见 [IMPLEMENTATION](../plans/IMPLEMENTATION.md)。

## 恢复与验证

- 首次原件备份：仓库外 `../jev2agent-backups/jev2agent-before-workflow-20260919-092714.tar.gz`，78 个原文件核对通过。
- 拆分前完整备份（不含 `.git`）：`../jev2agent-backups/jev2agent-before-docs-layout-20260919-095308.tar.gz`，123 个文件逐字节核对通过，含本地工作流。
- 整理前提交 `5852988` 保留旧布局，可逐文件恢复；未重写 Git 历史。
- 仅调整文档组织与封包资产，不改变架构行为合同；验证采用内容迁移、JSON、本地 Markdown 链接、陈旧路径和 Git diff 检查，不运行已删除的工具测试。
- 实际验证通过：74 处本地 Markdown 链接、全部保留 JSON 解析、活跃文档无旧路径/旧命令；28 份历史定义及操作合同/决议 JSON/设计意图 JSON 与备份一致；Git diff whitespace 通过。
- 本地工作流与 overlay 同步目录及验证入口，继续不纳入 Git。
