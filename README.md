# jev2agent

Semantic Reflex Runtime 的开发仓库。当前是已封包的架构与实施交接材料，尚无生产 MCP provider。

首发范围：Codex CLI 单任务运行中的只读搜索 ADMIT＋原文 recall。默认关闭干预与语义后端；先完成 W1a 宿主能力核验，再推进最小实现和 E0 真机验收。

## 开发入口

- [开发接续调查](docs/research/2026-09-19-project-baseline.md)
- [交接包说明](semantic-reflex-runtime-codex-handoff/README.md)
- [架构合同](semantic-reflex-runtime-codex-handoff/ARCHITECTURE.md)
- [有限实施任务](semantic-reflex-runtime-codex-handoff/docs/IMPLEMENTATION.md)
- [前序会话背景](semantic-reflex-runtime-session-context.md)

原封包保持字节不变；后续生产代码与新增测试放包外。`references/` 和 `archive/` 含历史验收材料，不应整体提供给受测 agent。

## 本地检查

需要 Python 3.11+，在交接包目录运行：

```sh
cd semantic-reflex-runtime-codex-handoff
python3 -B -m unittest discover -s tests -v
python3 -B tools/verify_package.py .
python3 -B tools/check_e0_evidence.py --evidence config/e0-evidence.template.json --root .
```

未填 E0 模板预期返回退出码 2、`NOT_READY`；辅助检查通过不代表 Codex 集成已验收。

## 本地开发工作流

本机安装 `dev-flow-GPT`，其入口与配置由 `.gitignore` 排除，不随仓库发布。项目研究与开发计划保留在 Git 中。

其他工作区可从自己的工作流母版目录执行 `bash skills/ms-init/init.sh <项目绝对路径> jev2agent`，根据上述项目资料填写 `Agent-init/PROJECT_OVERLAY.md`，新会话使用 `/ms-start`。
