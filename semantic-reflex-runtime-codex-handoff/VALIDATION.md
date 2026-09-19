# 本次实际验证记录

**验证对象：codex-handoff-2026-09-18 封包材料与辅助脚本。不是 Codex 集成、生产权限或任务效果。** 本次为作者侧自检，非独立第三方评审。

## 已执行

| 检查 | 实际结果 | 证据 |
|---|---|---|
| 本机 Codex 可执行文件定位 | PATH 未找到 Codex；未运行任何 Codex 命令或模型任务 | [host-probe.json](evidence/host-probe.json) |
| 封包工具的有限单元测试 | 23 项通过；只测本机探测、资料字段/文件边界和清单核对 | [release-tools-tests.txt](evidence/release-tools-tests.txt) |
| 未填写真机证据的 E0 模板 | 如预期返回 NOT_READY，退出码2，`e0_verified=false` | [e0-preflight.json](evidence/e0-preflight.json) |
| 决议映射 | DEC01–DEC42、Q01–Q18、R01–R06 全量保留与分流 | [DECISION_REGISTER.json](DECISION_REGISTER.json) |
| 来源、JSON、相对链接 | 当前实际存在的文件核对；没有链接到假命令或未生成附件 | [build-checks.json](evidence/build-checks.json) |
| 最终包与清单 | SHA-256 覆盖所有非清单文件；ZIP 内容与解包重验 | 根目录 SHA256SUMS.txt；封包过程实际执行完整性检查 |

单元测试的“字段完整”用例使用明确写着 SYNTHETIC 的临时假文件；它只断言即使资料形式齐全，工具也不会产生集成PASS或开关授权。没有在正式 E0 目录中放置伪装真实的假trace。

## 没有执行

没有浏览官方站点/GitHub/社区，没有核验当前 Codex 版本接口或价格；没有安装/调用 Codex、MCP SDK或语义后端；没有实现本次选定的生产provider；没有真实请求观察、撤权、隔离、SQLite崩溃恢复或任务成功率/成本实验。

本轮未重跑 v0.6 的历史 32/37/40/42/71/11 等测试，不把档案中的数字加到本轮23项中。历史包按原字节保留，它们只能支持其自身记载的有限范围。

## 结论

**可以交付的是已收束的 Codex 架构实施包。不能宣布的是 F1–F3 真机验收、E0通过、部署批准或语义净收益。** 成书不再继续；外部事实的空白进入明确的实施验收，不靠换状态名消除。

文件校验是传输/内容一致性检查，不是作者身份签名，也不验证被引用事实。运行检查后若人为增加缓存文件，目录完整性会报告额外文件；建议使用 `python3 -B` 运行工具和测试。
