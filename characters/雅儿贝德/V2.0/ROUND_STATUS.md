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

## ⚠️ 尚未完成、需要你决定优先级的部分

**`characters/雅儿贝德/V2.0/events/` 目录目前是空的。** 这是新架构和旧架构最大的差距所在：旧版CEU库（卷一~五，55条记录）里的**逐轮次时间线数据**（`progress_timeline`、`environmental_force_snapshot`等新字段）没有被自动迁移——旧CEU是"一个证据事件=一条扁平记录"，新Event是"一个事件=多个结构化turn的时间线"，两者结构不同，不能简单转换，需要重新回原文构建。

`profile.yaml`里保留的是**从这些证据推导出的分析结论**（信念、价值排序、决策规则、关系图谱），这部分没有丢失；丢失/待重建的是**支撑这些结论的原始时间线证据本身**（按新schema的细粒度）。

这意味着两个选择，需要你决定：

- **选项A**：把卷一~五的旧CEU语料重新过一遍，转换/重建成新Event格式的`events/vol1.yaml`~`events/vol5.yaml`（工作量接近重做一次卷一~五的抽取，但因为分析结论已经在profile.yaml里了，主要是把原文重新组织成turn时间线，不需要重新做归因分析）
- **选项B**：接受卷一~五只保留`profile.yaml`层面的分析结论，`events/`目录从卷六开始，用新schema处理新内容——旧证据的可追溯性依赖`_history/V1.0-CEU/`归档目录，而不是新格式的`events/`

## Character OS 文件版本（新命名）

- `profile.yaml`：v0.1（迁移+重整完成，MM2/MM4/MM6/MM7原有的"三重验证待回填"、value_hierarchy第3/5层"待坐实"等未完成事项原样保留，未因架构迁移而自动解决）
- `literary_techniques.md`：v0.1（迁移，1条手法，n=1）

## 下一步

1. **等待你对上面"选项A/B"的决定**，这个决定会影响接下来的工作量和顺序
2. 无论哪个选项，`profile.yaml`里MM2/MM4/MM6/MM7对应的belief_system条目仍未做三重验证回填，`value_hierarchy`第3/5层仍无正式证据支撑，这两项本身就值得继续推进，与events/怎么处理是独立的两件事
3. `psychological_structure`里4条机制全部标注`status: open`（样本量都只有1-2个场景），需要更多卷的证据来判断是否转正为`confirmed`

---
最后更新：2026-07-19（架构迁移到CSE，profile.yaml/literary_techniques.md迁移完成，events/待你决定处理方式）
