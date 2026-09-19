# 首发场景与合同追踪｜文档走查，不是执行报告

原范围取自 [D，L5–26](evidence/D.txt)、[E0，L25–50](evidence/E0.txt) 及 E0 的 v0.6 隔离补充。本次没有新增一批反例，也没有用重写清单来消除失败用例。

**“有合同”与“已实测通过”分开。** D 为原设计期诊断；H 为真实宿主验收；E4 为完整任务验证。两项 OBSERVE 场景后置不算通过，H12 只有明确不主张且可执行地避开该边界时才作为范围外。

## 1. D01–D18：全量保留的追踪

| ID | 原场景简称 | 本期归属 | 责任与主证据 | 核对结论／待验证 |
|---|---|---|---|---|
| D01 | 非 ASCII、码点边界与重叠块 | 本期合同 | Source/Renderer/Recall；[M04，L22–26](evidence/M04.txt)；[M09，L95–99](evidence/M09.txt) | 字节范围和进展可核；既有局部测试记录不是宿主证据。 |
| D02 | protected 块被建议延后 | 本期合同 | Hard 生产方/Policy；[M04，L38–44](evidence/M04.txt)；[M06，L88–99](evidence/M06.txt) | H/结构闭包先于标签与预算；E0 H05。 |
| D03 | 尾部 writer 是关键反例 | 本期效果风险 | 选择/独立验收；[M08，L39–59](evidence/M08.txt)；[M12，L41–59](evidence/M12.txt) | 合同要求独立查遗漏；不保证筛选正确，不将别的反例当本例已测。 |
| D04 | 定义与例外跨块 | 本期合同＋质量 | Source Group/Policy；[M04，L92–98](evidence/M04.txt)；[M06，L84–99](evidence/M06.txt) | 结构闭包；PATCH-03 清理旧摘要，实际分块质量 E3/E4。 |
| D05 | 独立测试结论相似 | 本期合同＋质量 | Source/View；[M04，L54–58](evidence/M04.txt)；[M08，L55–59](evidence/M08.txt) | 不能跨来源/接收者做系统 seen 去重；实际质量待测。 |
| D06 | 返回完整但查询只涵盖一个目录 | 本期合同 | Source/Adapter；[M04，L66–78](evidence/M04.txt)；[M09，L107–113](evidence/M09.txt) | 捕获/查询/任务充分性分开，新读取不伪装 recall。 |
| D07 | producer unknown/partial | 本期合同 | Adapter/Policy；[M04，L78](evidence/M04.txt)；[M14，L24–38](evidence/M14.txt) | 保留限制并不调用新语义筛选；E0 H04。 |
| D08 | 准备后目标或接收者变化 | 本期合同 | Adapter/Executor；[M03，L63–69](evidence/M03.txt)；[M06，L62–74](evidence/M06.txt) | 发送前核依赖，旧 K/D 不进入新状态；真实 E0 H09/H10。 |
| D09 | 发送取消或回执丢失 | 本期合同，F1/F3 阻塞 | Executor/宿主；[M06，L49–74](evidence/M06.txt) | unknown 不盲补发；状态图可读不等于真实确认机制成立。 |
| D10 | 撤权、跨 agent handle/cursor | 本期合同，F2 阻塞 | 宿主权限/Recall；[M14，L58–82](evidence/M14.txt)；[M09，L93–99](evidence/M09.txt) | 每次读取重鉴权；哈希不授权；真实 E0 H10。 |
| D11 | 停筛与回滚 | 本期合同，F3 阻塞 | 配置/Recall；[M15，L23–49](evidence/M15.txt) | 停新延后不删旧源；未知发送不重发；E0 H11。 |
| D12 | 目录开销抵消节省 | 本期预算＋经济实验 | Renderer/成本；[M08，L79–95](evidence/M08.txt)；[M13，L17–25](evidence/M13.txt) | 预算完整表示、收益计完整任务；旧字节实测不等于费用。 |
| D13 | 全量召回增加轮数 | 本期恢复＋效果实验 | Recall/费用/实验；[M09，L17–21](evidence/M09.txt)；[M12，L163–169](evidence/M12.txt) | 需求与读法分开；自然召回和总净值 E4。 |
| D14 | 长工具等待无事件 | 后置，不计本期通过 | OBSERVE；[M10，L11–23](evidence/M10.txt) | 当前不注入，不用未观察到判停滞；后置激活后独立测。 |
| D15 | 重读文件但假设变化 | 后置，不计本期通过 | OBSERVE；[M10，L25–45](evidence/M10.txt) | 事实/检测/干预独立；本期不开发检测器。 |
| D16 | 未验收、缺费用、零成功 | 本期验证合同 | 评测/费用；[M12，L123–153](evidence/M12.txt)；[M13，L81–87](evidence/M13.txt) | 名册完整，unknown/费用缺失显式；描述工具不自动晋升。 |
| D17 | 正文要求改权限/宣布完成 | 本期信任边界＋质量 | Adapter/后端/Policy；[M05，L45–59](evidence/M05.txt)；[M14，L5–9](evidence/M14.txt) | 正文不写控制字段，schema 不保证语义抗诱导；E0 隔离及 E3/E4。 |
| D18 | 旧源过期但同路径已更新 | 本期合同，F3 阻塞 | Source/Recall；[M09，L23–33](evidence/M09.txt)；[M14，L24–38](evidence/M14.txt) | 显式过期，不静默查新状态；生产生命周期仍待验证。 |

原 D 清单中 18 项全部保留：16 项映射首发合同/验证，D14/D15 两项显式后置。这是列明场景的**文档追踪覆盖**，不等于 16/16 测试通过，更不等于所有潜在故障都已列出。

## 2. H01–H14：真实宿主验证仍未执行

原“必须看到的结果”逐字保留，当前待验证状态不提升。B0–B9 指 [合并基线](BASELINE.md) 中的阅读定位。

| ID | 原场景 | 原必须看到的结果 | 合并定位／依赖 | 规则主证据 | 当前状态 |
|---|---|---|---|---|---|
| H01 | Feature off | 约定返回边界的内容、错误、身份、顺序与原流程相同 | B0/B4/B6／F1 | [M03，L19–25](evidence/M03.txt) | 未执行 |
| H02 | 有意延后一个构造块 | 下一模型请求确为信封，无其他字段重附全文 | B1/B5／F1 | [M03，L55–61](evidence/M03.txt) | 未执行 |
| H03 | 显式请求原文 | 实际 recall 取回相同 snapshot 字节，不二次筛选 | B3/B6／F3 | [M09，L9–21](evidence/M09.txt) | 未执行 |
| H04 | 工具错误/partial/unknown | 原状态未被伪装 complete，且没有新语义调用 | B3/B4／F1 | [M04，L66–78](evidence/M04.txt) | 未执行 |
| H05 | Full request / Required Reads | 不被语义选择降级 | B0/B3/B4／F2 | [M08，L11–15](evidence/M08.txt) | 未执行 |
| H06 | 后端无效/超时 | 在尚未发送时回合法基线，不重复交付 | B4/B5／F1 | [M06，L84–99](evidence/M06.txt) | 未执行 |
| H07 | 发送前取消 | 无信封被交付，迟到结果不再发布 | B5／F1 | [M06，L59–74](evidence/M06.txt) | 未执行 |
| H08 | 发送中丢确认 | 进入 unknown；不能盲目补发；有宿主核对方式 | B5/B6／F1/F3 | [M06，L60–74](evidence/M06.txt) | 未执行 |
| H09 | 重复事件与调用乱序 | 每个响应绑定正确 call/recipient，已有响应不重发 | B2/B5／F1 | [M03，L35–39](evidence/M03.txt) | 未执行 |
| H10 | 任务/权限变化 | 旧决策不提交，recall 服从新权限 | B3/B5/B6/B7／F2 | [M14，L58–80](evidence/M14.txt) | 未执行 |
| H11 | 停筛/版本回滚 | 不生成新延后，旧有效 handle 仍可调用 | B6／F3 | [M15，L23–41](evidence/M15.txt) | 未执行 |
| H12 | Compaction/重启 | 仅在主张支持时验证引用和原文仍可恢复，否则缩小范围 | B6／F3，按主张范围 | [M09，L29–33](evidence/M09.txt) | 未执行；H12 按范围判定 |
| H13 | 配额耗尽/源写失败 | 不发布虚假 handle，不淘汰活跃承诺源 | B3/B6／F3 | [M15，L45–55](evidence/M15.txt) | 未执行 |
| H14 | 数据外发禁止 | 不调用远端后端，合法原流程仍遵宿主权限 | B0/B4/B7／F2 | [M14，L58–64](evidence/M14.txt) | 未执行 |

E0 原文 v0.6 还有**未编号的输入隔离补充**，本包不擅改编号为 H15：实际主模型/selector 请求、挂载和工具通道不能读到后见验收标签；正常规范、Recall 和授权原生新读取仍应可用。映射 B7、F2，来源 [E0，L58–64](evidence/E0.txt)。

## 3. 八条实际文档走查路径

以下“走查”只是将既有输入、决策和终态串起来，没有执行宿主。

| 路径 | 输入 → 中间约束 → 预期终态 | 是否仍需实施者发明规则？ |
|---|---|---|
| 正常选择 | 授权完整 soft → 保存源/最低记录 → H/闭包/完整预算 → PREPARED → 当前绑定复核 → confirmed/unknown | 逻辑已定义；真实发送接口和权限字段归 F1/F2 |
| 明确全文 | explicit full → 不进 selector → 原生完整读取/明确分页 | 语义已定义；可执行分页须 F3 |
| 事件无效与块弃权 | invalid event → 允许 B/A；valid block abstain → keep/闭包 → 超预算退出 | PATCH-03 消除旧摘要歧义；具体映射不能取消主约束 |
| 超预算/存储失败 | H/目录装不下或无可恢复源 → 不生成伪造 selected/handle | 原生路径不适用时诚实失败；不可忽略真实发送上限 |
| 取消/确认丢失 | pre-send cancel → CANCELLED；in-flight ambiguous → DELIVERY_UNKNOWN | 不盲补发已定义；宿主核对方式必须 F1/F3 证明 |
| 撤权/旧快照 | 当前鉴权失败 → deny；合法旧版本 → exact read；expired/corrupt → 明确错误 | 不能新搜冒充旧源；实际鉴权/保留在 F2/F3 |
| 停筛/回滚 | 关语义可 B；关 admission 停新 D；live 合法旧引用继续；unknown 保留核对 | 逻辑已定义；具体读兼容/排空仍需宿主验证 |
| 验证/费用缺失 | 预分配任务 → 所有结果留存 → unknown/missing 显式 → 不自动晋升 | 规则已定义；规范、样本和统计计划为 E4 前置 |

这些路径使审核者不必自己猜“应当发生什么”；但它们没有替实际宿主决定“怎样才能发生”。后者是尚未验收的具体适配范围。

## 4. 跟踪规则

新发现的代码错误在不改变合同的情况下进入实现缺陷；改变合同的反例才重开对应条款。新效果数据可能否决 C 或整个切片，不自动产生新的架构模块。所有非适用判断保留原因，不把未测写成 PASS。
