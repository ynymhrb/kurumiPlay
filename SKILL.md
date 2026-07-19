---
name: character
description: 小说角色认知建模Skill，支持两种任务：①角色蒸馏——从小说原文逐卷构建可运行的角色认知模型（CSE架构：profile.yaml静态特质+events/动态时间线），产出存放在characters/<角色>/下；②言行预测——加载characters/下已蒸馏的角色模型，在新场景或盲测验证集中生成/预测该角色的言行（含强制三步推理协议）。
---

# 角色蒸馏与言行预测（Character Distillation & Prediction）

本项目本身就是这个 Skill：从小说原文提取**驱动角色言行的深层特征**（信念/价值排序/决策规则/心理机制/语言指纹），构建成认知模型（**蒸馏**）；再用该模型推理角色在新场景下会说什么、做什么（**预测**）。不是写人物简介，不是死记角色说过的话。

**任务路由**：
- 用户要建模/训练/处理某卷/开新角色 → 走【一、角色蒸馏】
- 用户要盲测/RolePlay/预测角色言行 → 走【二、言行预测】，角色模型从 `characters/<角色>/V<最新轮次>/` 加载

## 文件地图

| 路径 | 作用 |
|---|---|
| `spec/character_static_profile_schema.md` | profile.yaml 字段定义 |
| `spec/event_schema.md` | events/<卷>.yaml 字段定义 + 两遍法提取流程 |
| `spec/attribution_framework.md` | 双轴归因（心理轴四层→文学轴两层），触发条件见该文件 |
| `spec/psychological_structure_protocol.md` | 表象矛盾→深层机制的处理流程 |
| `spec/expression_dna_protocol.md` | speech_register语言指纹提取 + 特征频率概率模型 |
| `spec/eval_protocol.md` | 轮次版本化、train/dev/test切分、评分协议、日志字段定义 |
| `characters/<角色>/source/` | 原文分卷txt + 盲测验证集（各轮次共用） |
| `characters/<角色>/V<轮次>/` | 蒸馏产出：profile.yaml / profile_trace.yaml / events/ / literary_techniques.md / ROUND_STATUS.md |
| `logs/` | revision_log（字段级修正审计）/ construction_log（过程指标）/ eval_runs（正式评分）/ schema_gaps（schema信号池）/ predictions/（预测与评分报告） |
| `scripts/locate_candidates.py` | 候选场景定位（grep人名+聚类，产出events/_index_vol<N>.yaml） |

## 双文件纪律：profile.yaml 与 profile_trace.yaml

- **profile.yaml**：纯推理用行为逻辑，保持简洁（每条只带一词级status标注）。预测时只加载这个文件。
- **profile_trace.yaml**：证据链、置信度详情、逐卷来源、变更记录，键名与profile.yaml对应。
- 理由：追溯内容混进推理文件会稀释注意力。任何新增证据/修正都要**两边同步**：逻辑进profile，证据进trace。

---

# 一、角色蒸馏（训练侧）

## 开启新角色 / 新轮次

1. 建目录 `characters/<角色>/V<版本>/`（大版本=规范有实质变化的新一轮，小版本=同轮修正迭代，见eval_protocol §0）
2. 原文分卷放 `characters/<角色>/source/`，按卷数做 train/dev/test ≈ 8:1:1 切分并记入ROUND_STATUS
3. 建空的 `profile.yaml`（按schema骨架）、`profile_trace.yaml`、`events/`、`ROUND_STATUS.md`
4. 旧轮次冻结：打tag `<角色缩写>-round-v<版本>`，目录移入 `characters/<角色>/_history/`

## 逐卷训练流程（train阶段）

每处理一卷，按顺序：

1. **定位**：`python scripts/locate_candidates.py <角色> <卷号>` → 生成候选cluster索引
2. **事件提取**（两遍法，见event_schema.md）：一遍机械列全部言行节拍（宁滥勿缺）；二遍筛选"暴露价值选择/行为规律/心理机制"的节拍聚合为Event/Turn。skip的cluster记录原因。**铁律：raw_quote逐字引用先行，结构化字段从它派生；信息不足留空，不臆测。**
3. **归因分析**（仅触发时）：反应幅度异常或解释赤字 → 双轴分析写入turn的attribution。心理轴优先，文学轴是补丁不是默认。
4. **profile更新**：新事件挑战现有模型 → 修正模型而不是硬凑解释。**修正门槛（防过拟合）：只加通用属性、能简短描述的内在逻辑；禁止为单个场景加限定性补丁/白名单。** 表象矛盾走psychological_structure_protocol找深层机制，找不到就诚实标open。每条修正在revision_log.md落字段级记录（精确到具体条目），证据同步进profile_trace.yaml。
5. **speech_register更新**：本卷新台词补入语料池，n/p(n)按概率模型重算，必须分场合分桶。
6. **schema复核**（卷末或信号积累时）：schema_gaps.md的信号逐条处理，改不改都留复核记录。
7. **过程指标**：construction_log.md追加一行（字段见eval_protocol §8）
8. **收尾**：更新ROUND_STATUS.md → git commit → 用实际hash回填日志里的`git_ref: 待回填`（回填本身单独一个小commit）

## dev / test 阶段

- **dev卷**（倒数第3-4卷）：提取事件后跑 **derivability audit**——逐行为判断profile能否推导出它（带字段引用链），产出`logs/predictions/vol<N>.md`。允许根据失败案例改模型。注意：derivability是事后解释，分数偏高（pre-training contamination + 后见之明），真正价值是gap识别。
- **test卷**（最后1-2卷）：**占位符盲测**——把原文中该角色的言行挖成`{}`做成验证集（`<角色>_第N卷验证集.txt`），按【二、言行预测】流程先冻结预测，再对照原文评分。禁止调一次测一次。
- 经验教训（vol13，derivability 0.93/0.97 → blind 0.55）：**derivability是必要非充分条件**，模型解释得了不等于推理端用得对。盲测失败先归因到推理端（观众定位/存量调用/语域迁移）再考虑改模型。

## 蒸馏铁律

1. 失败即改模型，不是改答案/硬凑解释
2. raw_quote先行，留空不臆测
3. 心理轴优先于文学轴；文学外壳单独沉淀进literary_techniques.md，不当字面行为
4. 矛盾是信号不是终点：找能同时解释所有表现的机制，找不到标open，禁止编造
5. 修正只能是通用简短逻辑，禁止场景级补丁（过拟合）
6. profile简洁/trace分离，两边同步
7. 所有修正字段级可追溯（revision_log），所有评估记录git_ref

---

# 二、言行预测（推理侧）

三种模式：**盲测填充**（验证集`{}`占位符）、**新场景RolePlay生成**、**derivability audit**（事后解释，仅dev阶段用）。

## 加载纪律

- **只加载 `characters/<角色>/V<最新轮次>/profile.yaml` + `literary_techniques.md`**。
- 不加载 `profile_trace.yaml`（证据链会稀释推理注意力）；不默认加载 `events/`（仅当场景是已有事件的延续、需要时间线上下文时按需查询）。
- 盲测模式下**严禁**读取该卷原文（`characters/<角色>/source/`下对应卷）——评分之前预测必须冻结。

## 第0步：事件建模（先于任何台词生成）

对目标场景建一份简易动态快照（对齐event_schema的思路，不必写成YAML）：

- 时间/地点/**在场者清单**（谁在场、谁缺席，这直接决定后续机制作用域）
- 事件性质与压力等级（日常/公务/危机；situational_pressure 低/中/高）
- 角色的目标层级：长期目标在本事件的投影 → 本事件子目标 → 当前轮的战术动机
- 与在场各对象的关系定位（查profile的relational_graph：affinity/professional_trust/tension）

## 强制三步推理协议（每一条言行预测都要走完）

vol13盲测复盘（0.55）确立：多数失败是推理端错误而非模型缺口。以下三步按序执行，各堵一类已知失败模式。

### 第1步：定观众，再选机制（堵"面具用错观众"）

- 显式回答："这句话/这个动作，观众是谁？"
- 把profile里的心理机制当**带作用域的函数**调用，不当泛化的人格形容词：每个候选机制先查其适用场合/对象是否包含当前观众，不匹配则拒绝套用。
- 涉及欺骗类预测的专项检查："该角色对这个对象的忠诚/关系结构允许这种谎吗？"——区分**隐瞒**（信息不对称，可能允许）与**虚饰**（谎报能力/立场保面子，对最高忠诚对象通常禁止）。

### 第2步：先检索存量，再考虑发明（堵"发明字段外行为"）

- 把profile当**行为库存**用：先枚举能匹配当前情境的存量条目——catchphrases（带n/p_n）、decision_rules、psychological_structure的默认反应路径。
- 存量中有 p≥0.5 的匹配项 → 直接消费它。
- 只有库存穷尽仍无匹配时才允许发明新行为，且必须在推理链中标注"[发明·低置信]"。
- 闭世界优先：默认答案在模型里，模型外的答案要额外举证。

### 第3步：语域选档，写完自检（堵"文风迁移不足"）

- 写台词前从 speech_register 的场合分桶里**显式选档**（对外/对同僚/对下位者/对最高忠诚对象等，以该角色profile实际分档为准）。
- 语气强度按第0步的关系定位二次缩放：同一种情绪对不同对象的表达形态不同。
- 写完**回读自检**："这句是书面腔还是口语？符合所选档位吗？"不符合就重写，不要保留初稿。
- 文学化加工（两段式）：先出写实版，再查literary_techniques.md是否有基调匹配的手法，按p(n)加权决定是否套用；对外场合默认写实。

## 输出格式

每个预测项给出：

```
### <编号>. Line <行号>（<场景简述>）
推理链: 观众=X → 机制=Y（作用域检查✓）→ 存量=Z（n=?, p=?）/[发明·低置信] → 语域档=W
预测: <台词或行为描述>
```

盲测模式产出 `logs/predictions/vol<N>_blind.md`，预测完成后才允许打开原文。

## 盲测评分与复盘

1. 逐项对照原文判定：**对**(1) / **部分对**(0.5，方向对细节偏) / **错**(0)，加权均分。产出 `logs/predictions/vol<N>_scored.md`。
2. 失败逐项归因，先问推理端再问模型端：
   - 推理端：三步协议哪一步没执行到位？（观众定位错/没查存量/语域没选档）
   - 模型端：profile确实缺一条**通用**逻辑？——修正必须过蒸馏侧的防过拟合门槛（通用属性+简短逻辑，禁场景补丁）。
3. 机制选择准确性与文风保真度**分开计分**，便于定位错误层。
4. 结果登记：eval_runs.md一行 + construction_log.md一行 + ROUND_STATUS.md更新 + commit（git_ref回填）。
5. 透明声明：若原著可能在预训练语料中，准确率数字偏高，须在报告中注明contamination caveat。

## 新场景RolePlay生成（无ground truth）

同样走第0步+三步协议，区别：

- 无原文可对照，推理链照常输出（供人工review角色"为什么"这么说）
- 状态连续性：多轮对话中情绪/意图在轮间演算更新，但**不回写**profile（动态状态不污染静态模型）
- 空字段=该维度无已知约束，不臆测补全
