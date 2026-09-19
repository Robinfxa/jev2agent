# Semantic Reflex Runtime｜Codex 首发架构交接包

**交付标识：codex-handoff-2026-09-18。这是成书收束后的实施交接包，不是 v0.7。**

宿主指定为 **Codex**；本包将首个支持形态确定为 **Codex CLI、单任务非交互运行、一个授权域、本地只读搜索工具**。首发仅 ADMIT＋原文 recall。设计方案在本包落定，不再默认继续丰满通用架构。

**交付边界：架构与实施任务已封包，Codex 集成未验收，B/C 均不得在真实工作流默认启用。** 当前环境未找到 `codex` 可执行文件，网页搜索不可用。本次没有安装 Codex、读取账户凭据、联网查文档、调用模型或生成真实 Codex trace。本包不是可直接安装的插件，也没有一个虚构的 `srr-mcp` 可执行程序。

## 从这里开始

| 入口 | 用途 |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | 已合并、采用三处修订的首发逻辑合同；不用沿历史版本寻找现行规则 |
| [CODEX_HOST_CONTRACT.md](docs/CODEX_HOST_CONTRACT.md) | Codex 具体适配方案，F1–F3 的设计解法、支持范围和责任 |
| [DECISION_CLOSURE.md](docs/DECISION_CLOSURE.md) | 42 项建议、18 项问题、6 项研究事项的结项处置 |
| [IMPLEMENTATION.md](docs/IMPLEMENTATION.md) | 有限实施工作包与停止线；不用重开成书 |
| [E0_CODEX_ACCEPTANCE.md](docs/E0_CODEX_ACCEPTANCE.md) | 14 项真机接入检查，版本锁和证据要求 |
| [CODEX_HANDOFF.md](CODEX_HANDOFF.md) | 可以交给实施 Codex 的任务说明；不代表 Codex 已加载本包 |
| [VALIDATION.md](VALIDATION.md) | 本次真正执行了什么、没有执行什么 |

## 四项已明确的决定

1. **不寻找全局后置拦截器。** 我们提供 `srr_search`，先产生原结果，再在该工具自己的返回边界生成披露信封。只覆盖实际调用这个工具的结果，其他 Codex 原生通道保持原样。
2. **不靠模型参数获得权限。** 由可信启动器建立不可由仓库内容覆盖的 run manifest；MCP 通道绑定整个单任务授权域，不把模型传入的 `agent_id` 当认证。
3. **不把 JSON 文件当持久性承诺。** 首发设计采用每 run 的本地 SQLite 事务保存源、视图及最低恢复记录；只有提交成功才发布引用。OS 隔离、撤权和崩溃恢复仍须实际验证。
4. **不把工具发送当模型收件。** 服务端只记录准备/发送事实。真实下一次模型请求才是 E0 的关键证据；未知交付不主动补发，无法核对时停止该受影响运行。

## 本地可执行检查

要求 Python 3.11 或更新版本；以下命令不访问网络、不启动 Codex 会话、不修改用户 Codex 配置，也不读取登录文件。

```sh
python3 -B tools/probe_host.py --output /tmp/srr-codex-host-probe.json
python3 -B tools/check_e0_evidence.py --evidence config/e0-evidence.template.json --root .
python3 -B -m unittest discover -s tests -v
python3 -B tools/verify_package.py .
```

第二条在本包未填写真机证据的状态下应以非零码退出，报告缺失；这不是包损坏。第一条默认只定位可执行文件；只有显式加 `--inspect-local-binary` 才运行本机 `codex --version` 和 `codex --help`，不发起任务。

## 什么已结束，什么没有结束

**已结束：** 本轮作者侧设计收束、Codex 首发形态选择、责任与失败路径裁定、实施材料封装。用户明确指定 Codex 并要求解决问题封包；具体工程裁定由本包给出，不冒充逐条用户签字或独立第三方批准。

**未结束：** 指定 Codex 二进制版本上的 F1–F3 真机证据，以及 E1–E5 的分布、强基线、语义质量、完整任务和实际经济性。它们进入实施/实验待办，不再驱动整册加版本。

`config/deployment.intent.json` 是**本项目的设计配置**，不是 Codex 原生配置。包中不提供未经核验的 Codex 参数、hook 名或可直接粘贴的安装命令。

`references/` 与 `archive/` 是不可作为现行规范的历史证据。不要把完整历史实验包挂载给受测 agent：其中包含公开反例和验收材料。只有合法任务资料进入受测工作区。
