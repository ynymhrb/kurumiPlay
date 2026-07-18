# CEU (Character Evidence Unit) Schema

版本：v0.5（新增 schema_gap 字段）

**本schema不是定案，是持续检测中的假设。** 抽取时如果某条证据用现有字段表达不贴切/词不达意，不允许硬套现有字段掩盖问题——照实记录到 `schema_gap`，让流程能收集"schema哪里不够用"的信号，而不是丢弃或勉强塞进不合适的字段。修改规则见本文件"变更记录"约定：任何字段增/删/改都必须先在这里落一条"vX→vY变更记录"（写明改了什么、为什么），才能生效——这是回答"每个字段为什么加/删/改"的唯一权威来源。

## 定义

CEU 不是"人物出现的片段"，而是：**一个能够暴露人物价值选择、行为规律或心理机制的证据事件**。

判断标准：这一段是否回答了"人物在某个冲突/压力下做出了什么选择，保护了什么、放弃了什么" —— 而不只是"人物说了/做了什么"。

## 字段结构

```yaml
event_id:               # 唯一编号，如 YLDB-V1-C3-001（卷-章-序号）
raw_text:                # 原文逐字引用（完整段落，含行号），在任何结构化字段之前先固定下来
scene:                   # 场景描述（简述，非原文摘抄）
trigger:                 # 触发事件/刺激源
context:                 # 上下文背景

participants:            # 涉及人物
relationship_context:    # 人物之间关系（主仆/同僚/竞争者/至尊-下属等）
power_context:           # 权力位置（谁对谁有决定权/服从关系）

event_type:              # dialogue / action / decision / conflict / emotion

choice:                  # 人物做出的选择是什么
action:                  # 具体行动
speech:                  # 关键台词（原文引用需控制篇幅，避免整段照抄）
emotion:                 # 表现出的情绪

value_conflict:          # 本次事件中冲突的两个（或多个）价值是什么
chosen_value:            # 最终选择保护/优先的价值
sacrificed_value:        # 被放弃/牺牲的价值

underlying_belief:       # 支撑这个选择的深层信念（Mental Model 候选）
evidence:                # 原文出处（章节/位置，便于溯源核对）
evidence_source:         # self / others / narrator —— 这是人物本人的选择，还是他人对她的评价/观察，还是全知叙述者的评论
confidence:              # 该 CEU 对人物模型的置信度/重要性（high/medium/low）
schema_gap:              # 可选。这条证据如果用现有字段表达不贴切，写明"哪里不贴切、本来想表达什么"，不要硬套字段掩盖信息损失
```

## v0.4 → v0.5 变更记录

- 新增 `schema_gap`（可选字段）：v0.4 之前，抽取时如果某条证据不完全适配现有字段（比如既不是单纯的"选择"也不是单纯的"他人评价"，或者 value_conflict/chosen_value 硬套上去会失真），只能硬塞进现有字段或者干脆跳过，两种做法都会让"schema 本身可能有缺陷"这个信号消失、无法积累。现在改为：遇到这种情况照实记录 `schema_gap`，正常抽取流程不中断，信号汇总进 `logs/schema_gaps.md`，由定期的 schema 复核判断是否需要真正修改 schema。
  原因：用户明确要求"CEU的schema并没有确定，不能按当前schema为准，要检测并修正schema"——需要一个专门收集"schema不够用"信号的机制，而不是假设当前v0.4字段集已经完备。

## v0.3 → v0.4 变更记录

- 新增 `evidence_source`（self / others / narrator）：不是所有对人物有价值的证据都来自"她自己的选择"。他人对她的评价（如同僚点评她的能力）、全知叙述者的背景描述，都是有效证据，但证据强度和解读方式不同——不该用同一套"choice/value_conflict"硬套上去，也不该因为"不是她本人的选择"就直接丢弃（之前cluster A/E/I等的一些自身描述性内容因为没有独立选择场景被跳过，其实可以作为`evidence_source: others/narrator`的轻量证据保留，而不是完全不记录）。
  默认值为 `self`（人物本人的选择/行为），仅在证据来自他人观察或叙述者旁白时才需要显式标注为 `others` 或 `narrator`，此时 value_conflict/chosen_value 等字段可以从简或省略，改用更轻量的 `observation`/`context` 描述即可。

## v0.2 → v0.3 变更记录

- 新增 `raw_text`：结构化字段（scene/choice/value_conflict等）在CEU格式尚未固化前，过早把原文压缩成字段会丢信息，且外部审查者（如ChatGPT做交叉验证）只能看到我筛选后的结果，看不到原文，无法判断我是否漏判。现在要求：**先固定原文逐字引用，再派生结构化字段**，格式怎么改都不会丢失原始证据。
- 配套流程变更：提取一个候选场景时，先输出该场景的完整原文（含行号），而不是直接输出结构化CEU；结构化字段作为"从raw_text派生的解读"，可以随时重新推导。

## v0.1 → v0.2 变更记录

- 新增 `value_conflict` / `chosen_value` / `sacrificed_value`：仅记录 emotion/action/belief 不足以支撑 Value Hierarchy 推导。例如"雅儿贝德嫉妒夏提雅"本身信息量不够，需要拆解为"个人嫉妒 vs 守护者职责 → 选择战略竞争而非破坏组织 → 因为安兹认可优先"。
- 新增 `relationship_context`：同样的行为（如"攻击"）面对敌人/同僚/至尊时意义完全不同，缺少这个字段会导致行为解读错误。
- 新增 `power_context`：小说人物高度依赖主仆/上下级/阵营/身份等权力结构，脱离权力位置谈选择容易失真。

## 提取流程（每章/每卷）

```
原文章节
 ↓
筛选人物相关片段（不是任何提及都算，要含有"选择/冲突/决策/关系变化"）
 ↓
逐片段判断是否构成 CEU（用上面的判断标准）
 ↓
按 schema 填写字段
 ↓
标注 confidence，暂存 evidence 出处以便溯源
 ↓
汇总进 characters/<角色>/V<当前轮次>/CEU/<卷>_cluster_<ID>.yaml
```

## 待验证的开放问题（来自研究记录）

- CEU 是否需要升级为**事件图（Graph）**而非线性列表，以捕捉跨章节的因果链？
- 是否需要**时间阶段人格**（人物在不同阶段的价值排序是否会漂移）？
- 是否存在**多个人格状态**（如伪装/表演状态 vs 真实状态）需要分别建模？

这些问题在逐章验证过程中持续观察，一旦有证据支持就升级 schema 版本号并记录在 `logs/revision_log.md`。
