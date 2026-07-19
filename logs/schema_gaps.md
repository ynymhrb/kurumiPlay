# Schema Gaps

`spec/event_schema.md` 和 `spec/character_static_profile_schema.md` 不是定案。提取事件时如果某条证据用现有字段表达不贴切，照实记录到这里，作为"当前schema哪里不够用"的信号池，供定期的schema复核处理。

不允许无声丢弃：每次复核后，无论是否触发schema修改，都要在下方"复核记录"里写一条结论（改了/没改+原因），不能只处理信号池里的条目却不留痕迹。

## 历史记录归档说明

V0.1→V1.0（CEU schema）阶段积累的全部信号及复核记录（含CEU schema v0.1→v0.7历次变更依据）已归档到 `_history/schema_gaps.md`。本文件是albedo-round-v2.0开始后的活跃记录。

## 待复核信号

（卷六~十处理期间积累，2026-07-19卷末复核已处理，见下方复核记录；新信号继续记录到这里）

## 复核记录

| 日期 | 复核范围 | 结论 | 是否触发schema修改 | 对应revision_log条目 |
|---|---|---|---|---|
| 2026-07-19 | 卷六~十全部events文件（event_schema.md v1.0与character_static_profile_schema.md v0.1的首次实战检验） | 三个信号，均判定暂不改schema，继续观察：(1) `event_initial_dynamic_matrix.mental_fatigue`在5卷16事件中从未有原文依据可填（全部留空）——符合"无证据留空"设计，但若到卷末（dev阶段）仍零使用，考虑降为可选注释或删除；(2) 长对白turn的`speech_content`与`raw_quote`高度重复（多处写"见raw_quote"），信号：两字段的分工（逐字引用vs台词提取）在长对白场景退化——暂用"见raw_quote"惯例解决，不改字段；(3) `characters_present`需要标注状态（如"仅远程通话，人不在场"），当前用括号注记的非正式方案够用。另：attribution的"推断性标注"实践（规则13/效忠排他性暗线）运转良好，psychological_structure_protocol的open/confirmed分级在本轮完成3次转正，门槛（≥2独立场景）未见误判，不调整 | 否 | 无（未触发修改，本条即复核留痕） |
