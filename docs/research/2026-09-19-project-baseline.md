# 开发接续调查 · 2026-09-19

## 当前材料与结论

最初目录包含展开的 Codex 架构交接包、同名原始 ZIP、会话迁移 ZIP 和会话背景便笺；清理后保留展开架构包与 `docs/handoff/` 接续资料。交接标识为 `codex-handoff-2026-09-18`，设计收束状态为 SEALED_FOR_IMPLEMENTATION，不等于 HOST_VERIFIED 或 DEPLOYMENT_APPROVED。

已经阅读 README、会话背景、架构合同、Codex 宿主合同、有限实施任务、E0 清单与辅助检查说明。当前可执行代码只有三个封包工具及其单元测试；无生产 `srr_search`、`srr_recall`、MCP provider 或应用依赖清单。Jev 是可替换候选后端，不是首发必装依赖。

工程方向已定：Python 3.11+、标准库 SQLite、经实际版本核验的 MCP SDK；一个 run 一个授权域，可信 manifest、事务后发布引用、原文召回与显式分页。目标支持环境为受控 Linux；本机是 macOS，不能据此认定目标隔离通过。

## 后续开发次序

1. W1a：核验 Codex 二进制与分发身份、MCP 配置依据、实际模型请求观察点、隔离方案。历史“未找到 Codex”仅描述封包环境，不能外推到当前主机。
2. W1b：最小 literal UTF-8 搜索与原文 reader，核验真正工具调用与模型请求。
3. W1c：可信 run manifest、SQLite 事务、权限与 epoch、分页、撤权、重启、未知交付，完成 E0 H01–H14 和 ISOLATION。
4. 后续 W2–W6 依现有任务单评估成本、强 B、有限 C、自然任务与有限启用。真实证据前保持干预关闭。

原封包作为不可变基线保留，新增生产实现、测试与证据放包外。不复制第二套架构合同，不开始下一轮成书。历史 oracle/答案不能进入受测工作区。

## 本轮准备与验证

- 完整文件备份已存于仓库外 `../jev2agent-backups/jev2agent-before-workflow-20260919-092714.tar.gz`，对应 `.manifest.json` 保存文件与备份 SHA-256。备份内 78 个文件逐一核对成功。
- 两个根 ZIP 的 CRC 检查通过；原件保存在仓库外备份，工作目录的重复 ZIP 已按用户要求删除；封包内部两个历史 ZIP 保持跟踪以维持清单完整。
- Python 3.11.9；在交接包目录运行 `python3 -B -m unittest discover -s tests -v`：23 项通过，退出 0。
- `python3 -B tools/verify_package.py .`：PASS，73 个清单条目，退出 0。
- `python3 -B tools/check_e0_evidence.py --evidence config/e0-evidence.template.json --root .`：NOT_READY，退出 2，符合未填真机证据的预期；不代表 E0 通过。
- 全量 Git whitespace 检查发现原始历史证据中的行尾空白；为保留原包哈希不修改。新增文件单独通过 whitespace 检查。
- 工作流安装器返回 GATE: PASS；本机安装 9 个 skills、4 个角色及项目 overlay，hooks 仍为未启用示例。OpenSpec 未初始化，本次未改产品行为合同。
- GitHub API 与 `git ls-remote` 确认目标仓库为空。初始化本地 main、配置 origin 并保存初始提交；用户随后授权清理重复材料并推送。

本轮只完成研究留存、工作流与仓库准备，没有执行 W1a、模型调用、真实集成或部署。

## 交接版本比较与清理

会话迁移包是后生成的封装：ZIP 中 README/SESSION_CONTEXT/START_NEXT_SESSION 的时间为 2026-09-18 16:29:36，架构包 README 为同日 14:52:16（ZIP 时间未标时区，仅作顺序参考）。迁移 README 明确说明不是新架构版本。

逐字节确认：迁移包内的 handoff ZIP 与独立 handoff ZIP 完全相同；迁移包 SESSION_CONTEXT 与原根目录便笺完全相同；展开架构包全部文件与 ZIP 一致。迁移包 SHA256SUMS 全部通过。

- 唯一工程基线继续为 `semantic-reflex-runtime-codex-handoff/`，不删除其内部历史证据和清单依赖。
- 会话背景原字节迁移至 `docs/handoff/SESSION_CONTEXT.md`；保留迁移包独有的 `docs/handoff/START_NEXT_SESSION.md`，作为历史启动说明，当前本地入口使用根 README 和 `/ms-start`。
- 删除两个重复根 ZIP 及 `.DS_Store`；删除前核对仓库外备份 hash 与三个原文件字节一致。
- 本地工作流继续由 Git 忽略，项目资料和清理记录随 main 发布；此次不涉及产品合同变化，无需新增 OpenSpec change 或 Major Plan。
