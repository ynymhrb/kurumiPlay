# 雅儿贝德 — 训练轮次状态（V2.0，CSE架构）

**这是回答"当前训练阶段做了哪些事"的唯一入口。** 想知道细节再去查 `logs/construction_log.md`（过程指标）/ `logs/revision_log.md`（每条修正的原因）/ `logs/schema_gaps.md`（schema待复核信号），但"现在做到哪了"只看这一个文件就够。

## 当前轮次：albedo-round-v2.0（架构迁移，刚开始）

**这是一次大版本进位**，不是同一方法论下的内容迭代——从旧版CEU+多文件Character OS结构，迁移到CSE（认知仿真引擎）设计：静态特质模型（`profile.yaml`）+ 动态事件序列（`events/`）分离，新增`attribution_framework.md`双轴归因法（沿用不变）、`psychological_structure_protocol.md`（取代contradictions.md，记录深层机制而非表象矛盾）。详见 `logs/revision_log.md` "架构迁移"条目、本次对话里的架构评审讨论。

- 上一轮 `albedo-round-v1.0` 已冻结并归档到 `characters/雅儿贝德/_history/V1.0-CEU/`（不再维护，仅供追溯）
- 旧版spec文档同步归档到 `spec/_history/`：`CEU_schema.md`、`character_os_template.md`
- 旧版脚本归档到 `scripts/_history/`：`validate_ceu.py`、`reconcile_round.py`（`locate_candidates.py`/`_round_utils.py`保留，与格式无关仍可用）

## 本轮已完成的工作

1. **`spec/character_static_profile_schema.md`**：新建，定义静态特质模型字段（合并了原CSE设计里6个边界模糊的信念类字段为`belief_system`，`relational_graph`从2个标量扩展为3维度）
2. **`spec/event_schema.md`**：新建，定义动态事件/时间线结构，取代CEU格式
3. **`spec/psychological_structure_protocol.md`**：新建，"发现深层机制、不记录表象矛盾"的方法论
4. **`spec/attribution_framework.md`** v0.1→v0.2：更新为对接新Event schema，方法论本身（双轴四层+两层）不变
5. **`spec/expression_dna_protocol.md`** v0.2→v0.3：更新产出目标为`profile.yaml`的`speech_register`字段
6. **`spec/eval_protocol.md`** v0.3→v1.0：全面重写，pipeline对接新文件结构，明确记录CSE设计里哪些部分（BLEU/交叉熵/Trunk-Sandbox自动化/decision_logic_tree严格DSL/数值阈值）暂不实现及原因
7. **`characters/雅儿贝德/V2.0/profile.yaml`**：新建，从旧版`value_hierarchy.md`/`mental_models.md`/`decision_rules.md`/`relationship_rules.md`/`expression_dna.md`/`contradictions.md`迁移+重整核心内容——**这是本轮最重要的产出，静态特质模型的分析结论基本完整保留**，只是组织方式变了（MM1-8→belief_system条目、contradictions.md→psychological_structure机制记录）
8. **`characters/雅儿贝德/V2.0/literary_techniques.md`**：迁移自`reaction_stylization.md`，内容不变

## 卷一~五处理方式：已定案（选项B）

`characters/雅儿贝德/V2.0/events/` 目录**有意保持为空**——用户已决定采用选项B：卷一~五不重新按新Event schema重建时间线数据，只保留`profile.yaml`层面已完成迁移的分析结论；`events/`目录从**卷六**开始正式启用，用新schema处理新内容。旧卷一~五的原始证据（含逐字原文引用）需要追溯时，去`characters/雅儿贝德/_history/V1.0-CEU/CEU/`查，不会有新格式的`events/vol1.yaml`~`vol5.yaml`。

## logs/ 归档整理（本次同步完成）

`logs/construction_log.md`、`logs/schema_gaps.md`、`logs/revision_log.md`（CEU时代累积内容）已归档到`logs/_history/`，三个文件重新建成干净的活跃版本（字段名同步为事件模型术语，如`events_extracted`/`triggered_structure_updates`），从架构迁移这条记录开始累积新内容。`logs/eval_runs.md`未归档（此前从未产生记录，格式本身与CEU/Event无关），只做了字段说明里的术语更新（expression_dna→speech_register）。

## Character OS 文件版本（新命名）

- `profile.yaml`：v0.1（迁移+重整完成，MM2/MM4/MM6/MM7原有的"三重验证待回填"、value_hierarchy第3/5层"待坐实"等未完成事项原样保留，未因架构迁移而自动解决）
- `literary_techniques.md`：v0.1（迁移，1条手法，n=1）

## 卷六~卷十 训练进度（用户指令：连续处理，自主裁决）

| 卷 | 状态 | 事件数 | 要点 |
|---|---|---|---|
| 卷六 | ✅ 完成 | 1（YLDB-EV-V6-001，7 turn） | 效忠排他性（只忠于安兹个人，私下敌视公会名号）为最重要发现；"双重人格层次"机制转正confirmed；"表演性得体"机制加范围限定（不覆盖对安兹的恭敬仪态）；preferences首次非空 |
| 卷七 | ✅ 完成 | 4（EV-V7-001~004，13 turn） | 折中执行模式（规则12）；秘密部队提案→"对安兹本人也保有信息不对称"（规则13，推断性标注）；秩序观双向扩展（主权红线）；关键词击穿第三类触发器（无意中冒犯安兹）；"神圣化升格解读"口癖（n=2） |
| 卷八 | ✅ 完成 | 3（EV-V8-001~003，12 turn） | 日常卷，同僚/私下模式语料最丰富；第四类击穿触发器（安兹珍爱表达→情欲失控，扑倒事件）；效忠排他性第2实例（痛骂路西法）+保密三级梯度；合理化机制双向扩展转正confirmed；失控态责任外化（与自我归责状态绑定反向）；新增aura节点；literary_techniques手法2 |
| 卷九 | ✅ 完成 | 1（EV-V9-001，5 turn） | 生产性共构（与迪米乌哥斯共同构建安兹从未提出的战略叙事并使之成为实际政策——认知机制升级为组织行为发生器）；效忠排他性第2推断关联（"至高王"提案）；"更懂安兹"地位货币竞争（胜利者笑容）；demiurge共构同盟/得体性冲突分维度 |
| 卷十 | ✅ 完成 | 7（EV-V10-001~007，20 turn） | 她戏份最重的一卷；效忠排他性**转正**（"飞鼠大人"峰值流露为第3直接证据）；未来投射**转正**（夫君/新娘修行/婚戒指位/下腹部习惯四实例）；对外行动首个完整样本（外交层级宣示/寂寞侧脸钓鱼/八指恐惧管理/拉娜handler）；规则14战略耐心；情感通道终止谏言；语域四分档；renner节点 |

## 🏁 train阶段（卷一~十）完成——里程碑总结

**用户目标"卷六到卷十训练"已达成**（2026-07-19，卷一~五为CEU时代已完成的沉淀）。

- `events/`：卷六~十共16个事件、57个turn、17处attribution双轴分析，全部通过YAML校验
- `profile.yaml` v0.1→v0.6：本阶段新增/修正累计26条revision_log记录，全部字段级精确+git_ref可溯
- **已转正（三重验证）的信念**：至尊中心主义、秩序观（双向）、对人类态度、至尊象征崇拜（带范围限定）、**效忠排他性**（本阶段最重要发现——只忠于安兹个人，敌视至尊集体，含推断性暗线3条）、**未来投射**（配偶级自我定位体系）
- **psychological_structure**：3条confirmed（表演性得体·语域四分档／双重人格层次·对安兹也有信息不对称／认知加工·生产性共构随时在线），1条open（依恋创伤——直接危机场景仍只有1个，attachment_style候选偏强但不强行转正）
- **literary_techniques**：2条手法（n=1/n=3）+初步规律（文学外壳仅限"对安兹的欲望表达"主题+内部场合，对外一律写实）
- **回顾式自测**（C020）：15个关键行为按处理前profile判断可预测性，accuracy≈0.53（回顾式非盲测，仅供量级参考）；4个"不可预测"项全部转化为修正条目
- **schema复核**：3个信号记录并复核，均判定暂不改schema（见logs/schema_gaps.md首条复核记录）

## dev阶段（卷十一~十二，开发调测）进度

| 卷 | 状态 | 事件数 | derivability audit | 要点 |
|---|---|---|---|---|
| 卷十一 | ✅ 完成 | 4（EV-V11-001~004，14 turn） | 加权均分 0.93 | 矮人国远征卷她留守（yield仅0.18）；Epilogue独处场景为効忠排他性**迄今最强直接证据**（踩踏公会旗帜+消灭守护者宣言）；4处gap中2处修入profile（deflect guilt形态+即時重構→認知加工surface_behaviors追加；排他性evidence+confidence措辞微调）；profile升至v0.7 |
| 卷十二 | ✅ 完成 | 1（EV-V12-001，3 turn） | 加权均分 0.97 | 圣王国使节卷（外部POV限制信息）；她以宰相身份主导外交接见——外部视角完美验证"表演性得体"机制（outsider完全无法读穿面具）；唯一gap是安兹权威→轻微身体回应的连续谱中间点，不修正；profile维持v0.7 |

**dev阶段方法说明**：因为连续叙事文本中trigger与response交织（无法先冻结预测再读答案），dev阶段采用"derivability audit"替代盲测——逐行为判断profile现有字段能否推导出该行为，带引用链。透明声明：pre-training contamination使准确率偏高，关注点在"引用链能否建立"（gap识别）而非绝对数字。详见 `logs/predictions/vol11.md`。

## dev阶段（卷十一~十二）完成——里程碑总结

**两卷合计**：5事件、17 turn、derivability audit均分0.93/0.97。

- profile v0.7覆盖两卷所有行为极好：卷十一仅4处gap（2处已修正），卷十二仅1处gap（连续谱中间点，不需修正）
- **关键发现**：卷十一Epilogue踩旗场景将効忠排他性的"意愿层面"正式确认；卷十二外交接见从外部POV完美验证"表演性得体"机制的有效性
- **profile v0.7是当前最终版本**（dev阶段无需进一步修正）
- 两卷的低yield（0.18/0.33）反映故事结构：矮人国远征+圣王国POV限制卷对她的展示空间极少
- **dev阶段方法透明声明**：因pre-training contamination，0.93/0.97数字偏高是确定的；但derivability audit的真正价值——gap识别+引用链验证——仍有效完成

## test阶段：卷十三盲测（2026-07-19）

**方法升级**：用户提供占位符格式验证集（`雅儿贝德_第十三卷验证集.txt`，84个`{}`），实现**真正的盲测**——先推理填充、后对照原文评分，切断derivability audit的"事后解释"通道。

| 项目 | 结果 |
|---|---|
| 盲测均分 | **0.55**（116有效项，5场景：木屋0.63/独白0.90/团战0.53/拍卖0.50/休假0.69） |
| 对比dev | derivability 0.93/0.97 → blind 0.55，**方法论级发现：derivability是必要非充分条件** |
| 报告 | `logs/predictions/vol13_blind.md`（预测）+ `vol13_scored.md`（评分+复盘） |

**复盘结论（用户指导后修订）**：多数失败归属**推理端错误**而非profile缺口——(1) 把面具机制用到了安兹身上（A9让她对安兹虚饰能力，违背忠诚逻辑）；(2) 发明字段外新行为而不调用已建模的高概率行为；(3) 语域生成文风迁移不足（书面行政腔覆盖了口语直白档）。初版10条逐字段修正建议判定为**过拟合，全部撤回**。修正原则确立：**只加通用属性、能简短描述的内在逻辑，不加场景限定补丁**。

## profile结构重构（v0.7→v0.8）

用户指示：profile保持简洁，过程/追溯字段分文件承载（避免推理时注意力分散）。已执行：

- **`profile.yaml` v0.8**：纯行为逻辑简洁版（~230行，原607行），每条仅保留status一词级标注
- **`profile_trace.yaml`**（新建）：证据链/置信度详情/逐卷来源史/变更记录，键名与profile对应
- 内容变更仅1条逻辑新增："对安兹零虚饰"（表演性得体的corollary，vol13 A9/A10复盘产物）+1处语体标注补全（对下位者口语直白）

## dev回归调试：卷十一验证集盲测（2026-07-20）

vol13复盘确立三步推理协议（`spec/prediction_protocol.md` v1.0）后，用户指令回到dev集做推理端调试：卷十一验证集（BD特典drama段30占位符）盲测→对照原文评分→只修通用逻辑。

| 项目 | 结果 |
|---|---|
| 预测准确率 | 0.57（对10/部分对14/错6）；**机制选择分开计0.80** |
| 文风保真度 | 3/5（系统性偏长偏雅，原文高唤起时全为短爆发句） |
| 效度 | **非干净盲测**（本卷已被train/audit消费），分数仅供gap识别；contamination下仍0.57≈vol13干净盲测0.55，佐证损失主因在推理端生成习惯 |
| 报告 | `logs/predictions/vol11_blind.md`（冻结预测）+ `vol11_scored.md`（评分+复盘） |

**产出（全部通用修正，无场景补丁）**：
- `prediction_protocol.md` v1.1：第0步补状态继承（延续场景禁止重置情绪）；新增第0.5步邻接上下文反推功能类型
- `profile.yaml` v0.9：speech_register新增**语体动力学**（情绪峰值句长骤缩——本轮最大发现）；deflect guilt作用域限定（限统治/职责级自责）；规则9作用域（政务可坚持vs私愿被拒零坚持）；翅膀情绪通道（候选）
- eval_runs.md启用：E001（vol13补登）/E002（本次）

## dev回归调试第二轮：卷十二验证集盲测（2026-07-20）

对外公务语域（使节接见，29占位符），与卷十一（内部私密）互补覆盖语域两极。

| 项目 | 结果 |
|---|---|
| 预测准确率 | 0.59（对10/部分对14/错5）；机制选择0.83 |
| 文风保真度 | 3.5/5（较vol11改善：语体动力学在#24命中短句） |
| 协议实测 | v1.1两条新规则有效：状态继承使语域全程稳定；邻接反推24/29功能正确；5错中3个为衬垫/滑档→催生v1.2 |
| 报告 | `logs/predictions/vol12_blind.md` + `vol12_scored.md` |

**产出**：协议v1.2（衬垫与滑档警觉）；profile v0.10五项通用修正——**归荣于上**（对外恩典/许可皆以陛下为源，5实例）、**隐威慑显体贴**（威慑零出口由对方自行推断）、**躯体泄露通道**（翅膀+肩颤+红晕，言语纪律/躯体泄露分离，2卷支持）、语体动力学补表演价值维度、"小女子"对外谦称。

**结构性结论**：两轮dev调试稳定复现"机制≈0.8、总分≈0.58"——模型核心机制正确率高，损失集中在**话语模式层**，两轮修正全部指向该层。

## 🏁 test阶段收官：卷十四干净盲测（2026-07-20）

项目级干净盲测（本卷从未被消费），291占位符/200计分项，覆盖全部语域（独处/内部会议/对外宣战/战场/handler/处刑）。

| 指标 | 结果 |
|---|---|
| **预测准确率** | **0.63**（vol13基线0.55 → **+0.08**，同contamination条件对比有效） |
| 机制选择 | 0.815（与dev两轮0.80/0.83一致，稳定） |
| 文风保真度 | 3.5/5（语体经济多处逐字命中） |
| 分段 | 独处0.545／会议0.686／宣战0.50／战场0.667／收尾0.75 |
| 报告 | `logs/predictions/vol14_blind.md` + `vol14_scored.md` |

**里程碑结论：dev调试闭环（v0.9/v0.10+协议v1.1/v1.2）在干净数据上产生真实增益。** 残余损失定位于五个可命名层面（F1内心默认档=战略分析／F2对安兹共谋筹划平语档／F3支配游戏话术／F4私人势力实证／F5称谓补正），不再是弥散性错误。**五条候选修正因来源为test集，按纪律仅记录待决**（见vol14_scored.md），未修入profile。

## 下一步（等用户指示）

1. **决定F1-F5五条test来源候选修正是否修入profile v0.11**（无更多干净数据可验证，修入即用于RolePlay生成场景）
2. 本轮（albedo-round-v2.0）train/dev/test全部完成，可考虑打tag冻结；或开启新角色复用skill流程
3. 遗留：value_hierarchy第3/5层；MM2/MM4/MM6/MM7三重验证回填；依恋创伤机制需更多危机场景

---
最后更新：2026-07-20（卷十四干净盲测0.63/机制0.815——test收官，dev闭环增益确认）
