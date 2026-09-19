# 本轮测试的含义

只测试封包辅助工具：本机探测、证据字段/文件核对、文件清单一致性。不测试 MCP、Codex、SQLite生产存储、权限系统或自然任务。

单元测试的正向结构样例故意使用写着 `SYNTHETIC UNIT TEST DATA` 的临时文件。即使字段宣称 `REAL_CODEX_CAPTURE`，检查器也只能返回“资料结构可进入人审”，从不宣布宿主通过。这是工具边界测试，不是将假文件当真机证据。

运行：`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`。在已封包目录中产生额外 `__pycache__` 或修改文件后，完整目录校验会提示差异；这是预期。
