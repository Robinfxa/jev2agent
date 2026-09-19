# 项目状态

设计基线：`codex-handoff-2026-09-18`，作者侧架构已收束（SEALED_FOR_IMPLEMENTATION）。现行工程合同见 [架构](architecture/ARCHITECTURE.md) 和 [Codex 宿主合同](architecture/CODEX_HOST_CONTRACT.md)。

- 生产 provider：未实现，尚无可运行应用或产品测试套件。
- 下一阶段：W1a 版本与原生能力核验，见 [实施路线](plans/IMPLEMENTATION.md)。
- F1 前置边界与交付、F2 权限与隔离、F3 原文恢复：方案已定，真机证据开放。
- E0：NOT_RUN；E1–E5：NOT_VERIFIED；部署：未批准。
- 默认 `admission_mode=off`、`semantic_backend=disabled`。

原封包辅助工具的 23 项测试仅验证探测、资料格式和清单，不能证明生产功能或 E0。相关工具及报告已删除，原件保存在仓库外备份与 Git 历史。

原封包环境观察不代表当前本机能力。真实版本、MCP SDK、模型请求观察点和隔离方案均待 W1a 核验。
