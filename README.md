# jev2agent

Semantic Reflex Runtime：研究只读搜索结果的 ADMIT＋原文 recall，能否在保持任务质量与权限边界的同时降低实际执行成本。

当前完成架构设计，尚无生产运行时。宿主为 Codex CLI，下一阶段是 W1a 版本与原生能力核验；干预和语义后端默认关闭。

## 开发文档

- [当前状态](docs/STATUS.md)
- [架构合同](docs/architecture/ARCHITECTURE.md) · [Codex 宿主合同](docs/architecture/CODEX_HOST_CONTRACT.md)
- [实施路线](docs/plans/IMPLEMENTATION.md) · [E0 真机验收清单](docs/validation/E0_CODEX_ACCEPTANCE.md)
- [运行与回退](docs/OPERATIONS.md) · [决议记录](docs/decisions/DECISION_CLOSURE.md)
- [开发接续](docs/handoff/README.md) · [历史定义索引](docs/references/README.md)

交接资料已拆入 `docs/`。封包脚本、合成测试、旧检查报告、清单与重复 ZIP 已删除；尚无产品测试，E0 未执行。原件可从仓库外备份或 Git 历史恢复。

## 本地工作流

已安装 `dev-flow-GPT`，其 `AGENTS.md`、`Agent-init/`、`.agents/`、`.codex/` 与运行状态由 `.gitignore` 排除。新会话用 `/ms-start`，日常任务用 `/ms-loop`。项目文档与计划保留在 Git 中。

其他工作区可从自己的工作流母版执行 `bash skills/ms-init/init.sh <项目绝对路径> jev2agent`，根据上述资料填写项目 overlay。
