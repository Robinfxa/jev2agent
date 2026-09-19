# Semantic Reflex Runtime｜Codex 首发架构基线

**交付标识：codex-handoff-2026-09-18。作者侧设计已收束，进入实施交接；没有生成 v0.7。**

宿主由用户指定为 Codex；本包工程落点为 **Codex CLI、单任务非交互运行、本地 stdio MCP 搜索/召回工具**。MCP 是本包选择的适配路径，不是本轮已核验的 Codex 版本能力。当前环境无 Codex 命令、无可用网页搜索，故版本号、原生配置、出站模型请求和 E0 实测都不补造。

本稿以结项基线合并而来，采用 PATCH-01（批准与验证分开）、PATCH-02（仅 ADMIT＋recall 首发）、PATCH-03（弃权与失败分流），原文件不变。证据保存在 [结项副本](references/closeout/README.md)。本轮新增的 Codex/事务存储/单任务授权域等属于**工程裁定**，见 [变更及决议处置](docs/DECISION_CLOSURE.md)，不伪装成原材料已经指定。

所有真实干预默认关闭：`admission_mode=off`、`semantic_backend=disabled`。下文“允许 B/C”均以其相关验证和授权成立为前提；历史本地候选不是已验证生产基线。

## B0｜目标、范围与默认状态

在既有任务质量、权限和独立验收约束下，降低**单位独立验收成功任务的实际执行成本**；延迟、人工与维护另列并有明确口径。不得只以首次 token/字节或模型 agreement 宣布成功。

首发仅一种结构明确、完整捕获且生产方确认该查询完整的只读搜索返回：ADMIT＋原文 recall。只选择明确获准延后的 soft 内容；当前 diff、Required Reads、明确全文要求及其他授权硬保护不得降级。

先使用 Harness-native、Static instructions、Deterministic policies，再考虑 Semantic Reflex。C 默认不启用；只在明确授权的实验或已验证范围内使用。Codex 保留主 agent loop、原生工具权限与最终任务流程；我们不假设外部工具自动继承它的沙箱。自有工具另受可信 run manifest 与运行器隔离约束，独立验收不由选择器担任。

不在本期：生成摘要、subagent 报告筛选、DISCLOSE、完整 EXPAND、OBSERVE、review/repair/completion、每步语义审批、多宿主 bus、全 repo 索引、Registry、在线学习、通用控制平台。原生文件读取/新搜索仍可用，不能为了提升覆盖偷偷禁止。

依据：[MASTER，L71–161](references/closeout/evidence/MASTER.txt)；[M17，L5–38](references/closeout/evidence/M17.txt)；[CUR，L5–9](references/closeout/evidence/CUR.txt)。

## B1｜一个流程，六项逻辑责任，不是六个服务

```text
Codex 对自有 srr_search 的合法调用 → 产生已授权只读搜索返回（尚未返回 Codex）
    ↓ Host Adapter：调用/接收身份、返回状态与前置接缝
资格检查：支持范围、功能开关、当前授权、完整性、Hard/Soft、预算
    ├─ 不适用：保持原状态和权限，走原生或允许基线
    ↓ Source/State：保存可交付快照、分块与结构关联、当前任务状态
规则 B → 可选窄 Signal C → Policy：保护闭包、预算、候选 K/D
    ↓ 保存最低决策与恢复记录；渲染并核验完整信封
宿主提交 → confirmed 或 unknown（不盲重发）
    ↓ 接收方 view
Recall：当前鉴权 → 指定旧快照原文 → 显式分页 → 追加
    ↓
事件/源/状态/信号/策略/交付/召回记录 → 独立任务验收与费用
```

六项责任为 Host Adapter、Source/State、Predicate Backend、Policy/Executor、Recall、Telemetry/Evaluation。本包的在线责任由一个局部 stdio MCP provider 内的模块承载，数据为每 run 的本地事务存储；独立验收留在隔离的评测流程，不与在线输入共享答案。这不是六个服务。Codex 主循环不被复制。具体版本的 MCP 启动配置仍需从真实本机帮助/官方源码核验。

依据：[MASTER，L177–236](references/closeout/evidence/MASTER.txt)；[M03，L9–39](references/closeout/evidence/M03.txt)；[M15，L9–21](references/closeout/evidence/M15.txt)。

## B2｜对象、权威与生产消费关系

| 对象 | 生产方 → 消费方 | 固定语义／主定义 |
|---|---|---|
| Adapter Capability | 宿主核验 → 策略/实验 | 通知与前置替换分开；覆盖不能猜；§03 |
| Source Snapshot / Block | 授权捕获 → 判断/信封/Recall/评测 | 固定可交付表示与原文定位，不是实时文件全集；§04 |
| State Capsule | 宿主状态提取 → 判断/策略 | 当时真实可得的目标、约束、查询和覆盖；无隐藏思考或后见答案；§04 |
| Recipient View | 提交/回执 → 后续状态/评测 | 接收方实际交付事实，不是理解、可用全集或别人的视图；§04/§06 |
| Signal | 规则/语义后端 → Policy | 有限标签与引用；不拥有执行或授权权；§05 |
| Decision Record | Policy/Executor → 提交/审计 | 建议、保护覆写、实际划分、费用与交付状态分开；§06 |
| Disclosure Envelope | Renderer → 接收方 | 原文＋真实来源状态＋可枚举延后＋直接 Recall；§08 |
| Recall Request/Result | 授权调用方/读取器 → 接收方 | 当前权限下取旧版本原文，不隐式新搜索；§09 |
| Outcome / Cost | 独立验收／实际计量 → 实验评审 | success/failure/unknown、完整费用与缺失，不能由 selector 自证；§12–§13 |

字段族、生产/消费关系按 A5 主定义索引，不把本地 lab JSON 自动升级为生产 wire。历史 lab JSON、目录名和测试身份不是生产 wire 或认证。本包新增的首发工程选型见 Codex 合同；MCP SDK/协议版本与生产字段只能在版本绑定后锁定。

依据：[A5，L1–33](references/closeout/evidence/A5.txt)；[M04，L9–36](references/closeout/evidence/M04.txt)；[M14，L11–20](references/closeout/evidence/M14.txt)。

## B3｜数据和保护不变量

Source 保存既有权限和消毒之后本来允许交付的表示；记录调用、授权作用域、版本、编码/表示、hash、长度、完整性与保留状态。文本块区间为半开 `[start,end)`，UTF-8 不切断码点；独立来源的相似内容不自动去重。

至少区分五层：捕获是否完整、生产方是否声明完整、实际查询范围、当前展示全集/子集、任务证据是否充分。前三项不授予最后一项结论；取全快照也不等于读全文件或搜遍仓库。

任务/宿主授权方声明保护集合 H。对候选全集 U，K/D 互斥且穷尽，H 必须包含于 K；不可拆结构组求闭包。合法块级 abstain 是本次保留约束，不变成永久 Hard Context。未知关键性不被结构检查“证明安全”。

只有源与最低决策/恢复记录就绪后才承诺可延后；有效 run/handle 内不因普通容量淘汰删源。容量耗尽停新延后，原文/最低记录与普通 telemetry 轮转分离。本包固定为每 run 事务存储，活跃源不因普通配额淘汰，保留至可信启动器明确关闭/撤权；容量及有约束的运行期限是启动前必填部署参数。任务说 done 不自动关闭 run。详见 Codex 合同的生命周期条款。

依据：[M04，L18–64](references/closeout/evidence/M04.txt)；[M04，L66–98](references/closeout/evidence/M04.txt)；[M08，L23–37](references/closeout/evidence/M08.txt)。

## B4｜唯一选择与故障规则

语义后端仅输出 `prefer / defer_candidate / abstain`，绑定完整输入、块/组 ID、状态和版本。schema/引用/枚举/范围/覆盖校验失败是事件级不可用；分数没有校准不得解释为正确概率。输入过长、状态不足或不允许外发，不再调用强模型给本层兜底。

选择顺序服从保护、结构关联、合法弃权和完整表示预算。最终保留块按源序展示；排序优先级仅用于选入。B/C 共用已冻结的解析、结构组、渲染和读取机制；改变展示顺序是另一个干预。

| 原因 | 当前合同 | 不允许的替代 |
|---|---|---|
| 语义关闭或事件级无效/超时 | 回允许的已验证 B，无 B 则 A；费用仍计原实验臂 | 把缺标签当 defer 或用迟到结果改历史 |
| 合法块级 abstain | 保留该块并求结构闭包，再测完整信封 | 直接回会延后该块的 B |
| 保护/弃权闭包或必要目录超预算 | 核验过的原生完整读取或明确分页；无合法路径则诚实失败/不适用 | 裁掉保护块、忽略发送上限或伪造 selected 成功 |
| 明确全文/全部匹配 | 不新增语义延后；允许原生可遍历分页 | 抽样冒充全文 |
| 源或最低记录不能保存 | 不发依赖恢复的延后信封 | 假 handle |
| 工具 partial/unknown/错误 | 保留状态并走原流程，不把它改成 complete | 删除警告与错误 |
| 权限拒绝/外发禁止 | 拒绝相应数据流；仅使用同权限允许路径 | 为恢复而直读底层文件或默认外发 |
| 结构关联无法可靠判定 | 不假定独立，不生成不守约的延后；按 §06.11 退出 | 普通 B 覆盖保护/结构要求 |
| COMMITTING/DELIVERY_UNKNOWN | 等宿主可核对证据决定恢复 | 盲发第二份全量响应 |

预算计头部、目录、原文、引用和必要协议表示，不只计 included 原文。更大 K 可能缩小目录，表示长度不保证单调。本地字节上限不是生产 token/发送上限。

依据：[M05，L15–35](references/closeout/evidence/M05.txt)；[M05，L55–61](references/closeout/evidence/M05.txt)；[M06，L84–105](references/closeout/evidence/M06.txt)；[M08，L79–105](references/closeout/evidence/M08.txt)。旧 §05 摘要按 PATCH-03 澄清，主规则仍归 §06.11。

## B5｜提交状态与接收事实

策略结果 `USE_BASELINE / DELIVER_ENVELOPE` 与交付状态分开。

```text
CAPTURED → PREPARED → COMMITTING → DELIVERED
   └──────────┘             └──→ DELIVERY_UNKNOWN
        ↓
     CANCELLED（仅发送前确定取消）
```

准备不等于发送，发送确认不等于理解。发送前核对 source、recipient、明确目标/任务合同、保护、授权和配置的相关版本；变化则旧选择失效。无关遥测计数不自动使所有事件失效。

已发送/取消后的迟到判断丢弃；发送中取消不自动判未交付。宿主可靠确认未交付才可按约定重试/基线；否则 unknown，不盲补发。可同进程保证有限去重，但不得承诺未经证明的跨崩溃严格一次。

本地 `READY`、`PREPARED_LOCAL_NOT_SENT` 和普通文件成功都不充当真实 receipt。不同接收方、source 或 call 不共用可变“当前结果”。

依据：[M03，L35–39](references/closeout/evidence/M03.txt)；[M03，L55–71](references/closeout/evidence/M03.txt)；[M06，L49–78](references/closeout/evidence/M06.txt)。

## B6｜召回、分页和停筛

稳定入口允许列目录、取明确块集合、取原始 D 或分页取全快照。`all_deferred` 是原视图最初的 D，不是当前未读、未理解或别人没看过的内容。`batch_ids` 不扩大请求范围，不顺便填入非相邻块之间的内容。

句柄/hash 不是权限凭证。每次实际读取按当前身份、作用域和保留状态鉴权；游标绑定 source/version、view、recipient、模式与规范化范围。分页必须有进展，不能返回永不前进的成功页；终点只代表请求范围遍历结束。

Recall 只取指定旧快照，不二次语义筛选。过期、损坏、缺失、拒绝或非法范围显式处理；错误可见性服从宿主防泄漏规则。要新数据就新工具事件（refresh/search/read），不得把它伪装成旧 recall，也不因此前移 EXPAND。

语义关闭可退 B；全部 admission 关闭停止所有新延后；两者都不自动关闭已有合法引用的读取器。升级需读兼容或拒绝破坏性升级直至旧 run 结束。权限撤回优先于保留，已交付内容不承诺可撤回。

首发要求同一 run 的恢复目录在 compaction 后仍能合法查询；provider 重启须可在同一授权 manifest 下重连并读旧源。H12 因而列为本配置的必测项。跨新任务/新授权域自动迁移不支持；未通过 H12 不得以“不支持压缩”绕开。批量重复 ID 明确拒绝，任一无效/越权项整体失败，不静默丢项；具体 wire 随已核验 SDK 锁定。

依据：[M09，L9–33](references/closeout/evidence/M09.txt)；[M09，L65–75](references/closeout/evidence/M09.txt)；[M09，L85–113](references/closeout/evidence/M09.txt)；[M15，L23–55](references/closeout/evidence/M15.txt)。

## B7｜信息安全、回放与证据等级

源保存、外发给语义后端、向接收者披露、给独立验收者完整源、任务后保留是不同数据流。元数据、路径、数量、hash 同样受授权约束。代码/注释/日志是数据，不能写入可信控制字段；schema 校验不是语义抗注入证明。

接收方、selector、来源服务、evaluator 输入分别授权；实际挂载和工具通道须核验。hidden 测试可以保密，但任务有效规范应在授权范围内可获知，不能以秘密规范惩罚 agent。后见答案不能补进在线 Hard Context。

串联 event/source/state/signal/decision/delivery/recall/outcome。原建议、保护覆写、实际交付与后续行为分开。未读/未引用不自动等于无用；可访问/已交付不等于理解。

固定前缀重算、轨迹重演、完整闭环重跑三者分开。动作分岔后不能继续喂原轨迹未来结果。最低记录失败不延后；详细日志缺失记录 gap，相关任务/费用不从分母消失。

依据：[M14，L58–90](references/closeout/evidence/M14.txt)；[M11，L11–61](references/closeout/evidence/M11.txt)；[M11，L65–79](references/closeout/evidence/M11.txt)。

## B8｜验证与成本合同

A 为合理配置后的原生流程；B 为确定性整理/来源/恢复；C 在相同基础上只增加语义选择。B 必须经原生核验与先导比较，不把能跑的局部规则自动当强 B。

B/A 检验包装和恢复是否值得；C/B 检验选择增量；C/A 检验整包净值。固定需求读法实验不证明自然需求发现，捕获覆盖不等于候选内选择，原文保真不等于任务结果可靠。

主分析按预分配完整任务单位，失败、旁路、弃权、内部重试和 unknown 保留。内部重试增加费用、不增加成功单位；名册/结果/费用对账。费用缺失不填零，零成功的单位成功成本无定义；unknown 两臂都计失败并不能证明非劣，需缺失识别与抽样不确定性分析。

计量执行、研究、维护三类账；互斥的实际 usage/缓存/费用映射，人工与延迟未有单价时不和金额混加。append-only 是变更纪律，不是缓存或省钱保证。

E0 接入 → E1 分布 → E2 强 B → E3 语义 shadow → E4 自然任务闭环 → E5 有限启用。每步可停止。δq/ηc/Lmax、样本/分析/成本门槛在留出前冻结；真实 E4 空表不得晋升。公开反例只能开发回归；本地测试不代替宿主或效果证据。

依据：[M12，L21–77](references/closeout/evidence/M12.txt)；[M12，L117–153](references/closeout/evidence/M12.txt)；[M13，L9–15](references/closeout/evidence/M13.txt)；[M13，L71–87](references/closeout/evidence/M13.txt)；[M16，L15–26](references/closeout/evidence/M16.txt)；[E4，L11–36](references/closeout/evidence/E4.txt)。

## B9｜本次收束、适配优先级与状态

逻辑基线及三处文档修订纳入本次实施交接；Codex 首发形态和适配裁定见 [Codex 合同](docs/CODEX_HOST_CONTRACT.md)。这不是对旧历史材料的全部事实背书。

本包的状态是 `SEALED_FOR_IMPLEMENTATION`，表示作者侧不再开放式续写，并形成明确实现合同；它不等于 `HOST_VERIFIED` 或 `DEPLOYMENT_APPROVED`。用户已指定 Codex 并授权封包；没有虚构独立评审、用户逐条技术签字或真实运行通过。

F1–F3 已从“未选方案”转成具体 Codex 实施/验收任务，**运行事实尚未关闭**。F1 前置边界与交付、F2 可信任务/权限、F3 来源恢复都须按 [E0](docs/E0_CODEX_ACCEPTANCE.md) 验证。不拿状态改名消除未核验条件。

允许四种结果：C 在已验证范围有效；B 有效而删除 C；只留窄场景；停止整个切片。不能为补 C/A 的坏账自动加 OBSERVE，也不因已写代码必须保留它。

现行规范为本文 B0–B9 的逻辑语义、Codex 合同的具体映射和 E0 的验证义务；引用的旧稿只作依据。出现冲突时登记受影响条款，不从历史中挑更宽松解释。版本化宿主事实可以重开具体映射，不自动重开整书。

下一步是完成真实版本绑定与 E0 最小链路，而不是另造 Runtime 版图。基线批准、实现、运行验收和价值证明分别记录。
