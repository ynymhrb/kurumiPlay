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
| 卷七 | ⏳ 待处理 | | |
| 卷八 | ⏳ 待处理 | | |
| 卷九 | ⏳ 待处理 | | |
| 卷十 | ⏳ 待处理 | | 完成后做train阶段收尾（schema复核+机制状态复审+统一自测） |

## 下一步

1. 卷七起继续逐卷处理（locate_candidates.py → 两遍法 → events/volN.yaml → attribution → profile.yaml反馈）
2. `profile.yaml`里MM2/MM4/MM6/MM7对应的belief_system条目仍未做三重验证回填，`value_hierarchy`第3/5层仍无正式证据支撑
3. `psychological_structure`当前2条confirmed（表演性得体、双重人格层次）、2条open（依恋创伤、自我保护性合理化），open条目继续积累证据
4. 卷十完成后统一跑卷内自测（各卷预留场景不足时改用回顾式预测校验），补齐revision_log里"待卷十完成后统一自测"的eval_after

---
最后更新：2026-07-19（卷六处理完成，profile.yaml升至v0.2）
