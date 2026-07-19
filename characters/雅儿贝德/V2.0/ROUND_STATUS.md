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
| 卷十二 | ⏳ 待处理 | — | — | — |

**dev阶段方法说明**：因为连续叙事文本中trigger与response交织（无法先冻结预测再读答案），dev阶段采用"derivability audit"替代盲测——逐行为判断profile现有字段能否推导出该行为，带引用链。透明声明：pre-training contamination使准确率偏高，关注点在"引用链能否建立"（gap识别）而非绝对数字。详见 `logs/dev_predictions/vol11.md`。

## 下一步

1. **卷十二 dev评估**：同卷十一流程（derivability audit + gap修正 + profile更新）
2. 遗留：value_hierarchy第3/5层仍无正式证据；MM2/MM4/MM6/MM7三重验证回填；依恋创伤机制需更多危机场景
3. `event_initial_dynamic_matrix.mental_fatigue`若dev阶段仍零使用，考虑schema调整

---
最后更新：2026-07-19（卷十一dev评估完成，profile.yaml升至v0.7——認知加工+効忠排他性两处修正）
