# Construction Log

train 阶段（卷一～十，CEU 提取 + Character OS 构建）的过程记录，字段定义见 `../spec/eval_protocol.md` 第8节。区别于 `eval_runs.md`（面向 dev/test 的预测力评分），本表回答"构建过程本身是否稳定、是否在收敛"。

| run_id | date | round | git_ref | scope | candidate_scenes | ceu_extracted | yield_rate | skipped_with_reason | schema_violations_caught | triggered_revisions | triggered_contradictions | within_batch_accuracy | cross_validation | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| （尚无记录，卷二的处理早于本日志，属于 albedo-round-v0.1，未回填） | | | | | | | | | | | | | | |
| C001 | 2026-07-18 | v1.0 | 3696fc1 | 卷一 cluster A（第346-438行） | 7 | 1 | 0.14 | 6 | 0 | 1 | 0 |  | 无 | V1.0首个正式batch，端到端验证pipeline（locate_candidates→extractor流程→validate_ceu→character-os-updater流程→revision_log）；产出的CEU本身触发1个schema_gap信号（见schema_gaps.md），yield_rate偏低是因为这个cluster主要是场景描写而非独立选择场景，属正常 |
