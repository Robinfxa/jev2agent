# 交给实施 Codex 的任务说明

你负责实现本包定义的首个 **Codex CLI 单任务搜索/召回适配器**。这是实现任务，不是继续写架构书。请依次读取 `README.md`、`ARCHITECTURE.md`、`docs/CODEX_HOST_CONTRACT.md`、`docs/E0_CODEX_ACCEPTANCE.md` 和 `docs/IMPLEMENTATION.md`。

宿主已选定，不再横向选择其他 agent 平台；只处理 `srr_search` 的首次工具返回和 `srr_recall`，不碰其他原生通道、不增加动作审批和完成判定。MCP 是确定的适配路线，但其启动语法、SDK和具体能力要对本机 Codex 版本核验。

先在授权的本地环境运行 `tools/probe_host.py`；需要读取二进制帮助时显式加 `--inspect-local-binary`。不读登录凭据、不猜最新版、不把旧书的第三方配置直接当事实。当前包中的 host lock 为空，真实 admission 和 C 均为 off。

完成 W1a 后，在隔离 smoke 工作区实现最小 provider。该包没有现成 `srr-mcp` 命令；你需要实际提供并测试 transport、受保护 run manifest、literal search、SQLite事务、分页和失败处理。使用版本锁定的 SDK，不复制主 agent loop。需要外部资料时只核验本项目指定接口，不扩写通用平台。

把原搜索输出、信封、实际模型请求、实际 recall 和后续请求串成 E0 证据。provider 写出了响应不等于模型收到了。若没有合法观察点或隔离条件，记录 FAIL/NOT_RUN，不绕过授权、不启用真实筛选，也不制造模拟 trace 当作真机结果。

`archive/` 包含历史代码、oracle 和公开测试。可以用于开发回归；不要整个挂载到受测 agent 工作区，更不能将公开配对用作新留出任务。受测模型、selector、来源服务和 evaluator 分流。

回报格式固定为：实际版本与来源；本轮实现差异；真实通过/失败/未执行的 E0 项；费用与副作用；阻塞条款及最小修复。只在证据推翻某一条合同的情况下提局部变更。不要默认生成下一版架构书。
