# Construction Log

train 阶段（卷一～十，事件提取 + `profile.yaml` 构建）的过程记录，字段定义见 `../spec/eval_protocol.md` 第8节。区别于 `eval_runs.md`（面向 dev/test 的预测力评分），本表回答"构建过程本身是否稳定、是否在收敛"。

## 历史记录归档说明

V0.1→V1.0（CEU格式）阶段的过程记录（run_id C001~C015，卷一~五全部处理批次）已归档到 `_history/construction_log.md`。本文件是albedo-round-v2.0开始后的活跃记录，字段名同步更新为事件模型术语。

| run_id | date | round | git_ref | scope | candidate_scenes | events_extracted | yield_rate | skipped_with_reason | schema_violations_caught | triggered_revisions | triggered_structure_updates | within_batch_accuracy | cross_validation | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C016 | 2026-07-19 | v2.0 | 7b98e74 | 卷六全卷（4 cluster） | 4 | 1 | 0.25 | B旁白提及/C二手转述无新信息/D纯提及，均无本人言行 | 1（profile.yaml普通标量内含冒号，写入时自查修复） | 6 | 2（双重人格转正+表演性得体范围限定） | 不适用（全卷仅1事件，无法预留自测场景） | 无 | 首个新Event schema处理卷；唯一事件7 turn/3处attribution，信息密度极高（效忠排他性为本卷最重要发现） |
| C017 | 2026-07-19 | v2.0 | 见commit | 卷七全卷（11 cluster） | 11 | 4 | 0.82（9/11 cluster入事件） | D安兹独白提及/F第三方言论，无本人言行 | 0 | 5 | 1（双重人格追加第3场景） | 不适用（未预留；定性回顾：秘密部队提案若用v0.2 profile可部分预测——效忠排他性+双重人格已具备，但"对安兹本人信息不对称"超出当时模型） | 无 | 规则12（折中执行）/规则13（推断性）为本卷新模式；竞技场慌乱道歉精确定位敏感轴 |
