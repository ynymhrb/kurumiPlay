# 模型修正记录

每次因 Fidelity Test 或逐卷验证发现模型无法解释的行为而做出修正时，在此记录。**这是回答"每个字段为什么加/删/改"的地方，`<修正对象>` 必须精确到具体子项**（如"belief_system新增一条""value_hierarchy第1层拆分""decision_rules第2条加例外""psychological_structure新增机制"），不能只写"某文件改了"——写"某文件改了"等于没有回答"为什么"。

格式（评估协议见 `../spec/eval_protocol.md`）：

```
## <日期> — <修正对象：精确到具体子项>
触发: 哪个事件/哪次盲测暴露的问题
修正前: ...
修正后: ...
原因: ...
change_type: 字段新增 / 层级拆分 / 候选机制新增 / 范围限定 / 重命名精确化 / 证据分级 / 架构迁移
round: 所属训练轮次（如 v2.0），见 eval_protocol.md 第0节
eval_before: <eval_runs.md 或 construction_log.md 的 id，改动前最近一次同测试集/同卷内自测分数>
eval_after: <改动后重跑同测试集的 id>
delta: <predictive_accuracy 变化，如 +0.08>
git_ref: <这次修正对应的 commit hash>
```

## 历史记录归档说明

本文件是**albedo-round-v2.0（CSE架构）**开始后的活跃记录。V0.1→V1.0（CEU单条证据格式）阶段的全部修正历史（含seed_fragments清理、MM1三重验证转正、卷一~五全部CEU抽取过程、CEU schema v0.1→v0.7的历次变更、以及V1.0→V2.0本次架构迁移的完整决策记录）已归档到 `_history/revision_log.md`，不再更新，需要追溯旧决策依据时去那里查。

**下一条新记录将从这里开始。**

## 2026-07-19 — logs/ 归档整理 + 卷一~五处理方式定案（选项B）

触发：完成CEU→CSE架构迁移（`profile.yaml`/`events/`分离）后，用户对"卷一~五的events/怎么处理"给出决定：选项B——卷一~五只保留`profile.yaml`层面已迁移的分析结论，不重新按新Event schema重建这两卷的原始时间线数据；`events/`目录从卷六开始，用新schema处理新内容。同时要求把`logs/`也按照`characters/`/`spec/`/`scripts/`的先例做归档整理。

修正前：`logs/revision_log.md`/`construction_log.md`/`schema_gaps.md`三个文件从项目最初一直累积到本次架构迁移，内容几乎全部是CEU时代的记录（构建过程指标用`ceu_extracted`等CEU专属字段名、schema_gaps记录的信号全部指向已废弃的CEU schema字段），与当前CSE架构脱节。

修正后：
1. `logs/construction_log.md`、`logs/schema_gaps.md`、`logs/revision_log.md` 全部归档到 `logs/_history/`（git mv，完整保留）
2. 新建干净的 `logs/revision_log.md`（本文件）、`logs/construction_log.md`，字段名同步更新为事件模型术语（`events_extracted`/`triggered_structure_updates`等，见`spec/eval_protocol.md`第8节）
3. `logs/schema_gaps.md` 同样重建为空白模板，等待卷六起新schema下产生的新信号
4. `characters/雅儿贝德/V2.0/ROUND_STATUS.md` 更新记录选项B决定：卷一~五仅`profile.yaml`层面沉淀，不追溯重建`events/`；`events/`从卷六起启用

原因：延续本次架构迁移一贯的原则——旧格式的过程记录（构建过程指标、schema信号）绑定的是已经退役的CEU字段，继续留在活跃文件里既无法直接使用（字段名对不上新schema），又会让"当前状态"和"历史存档"混在一起，不利于`ROUND_STATUS.md`"只看一个文件就知道现状"的设计目标。卷一~五不重建`events/`的决定（选项B）本身权衡是：`profile.yaml`已经承载了这两卷贡献的全部分析结论（belief_system/decision_rules/relational_graph/speech_register/psychological_structure），重建时间线数据的边际价值（主要是未来可能需要的"卷内自测"回归测试语料）不足以覆盖重做一次提取的成本，且旧CEU语料完整归档在`_history/V1.0-CEU/`，需要时仍可查阅原文出处。

change_type: 架构迁移
round: v2.0
eval_before: 无
eval_after: 不适用
delta: 不适用
git_ref: a329bd1
