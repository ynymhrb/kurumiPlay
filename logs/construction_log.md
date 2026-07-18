# Construction Log

train 阶段（卷一～十，CEU 提取 + Character OS 构建）的过程记录，字段定义见 `../spec/eval_protocol.md` 第8节。区别于 `eval_runs.md`（面向 dev/test 的预测力评分），本表回答"构建过程本身是否稳定、是否在收敛"。

| run_id | date | round | git_ref | scope | candidate_scenes | ceu_extracted | yield_rate | skipped_with_reason | schema_violations_caught | triggered_revisions | triggered_contradictions | within_batch_accuracy | cross_validation | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| （尚无记录，卷二的处理早于本日志，属于 albedo-round-v0.1，未回填） | | | | | | | | | | | | | | |
| C001 | 2026-07-18 | v1.0 | 3696fc1 | 卷一 cluster A（第346-438行） | 7 | 1 | 0.14 | 6 | 0 | 1 | 0 |  | 无 | V1.0首个正式batch，端到端验证pipeline（locate_candidates.py定位→两遍法抽取→validate_ceu.py校验→Character OS更新→revision_log）；产出的CEU本身触发1个schema_gap信号（见schema_gaps.md），yield_rate偏低是因为这个cluster主要是场景描写而非独立选择场景，属正常 |
| C002 | 2026-07-18 | v1.0 | （待commit回填） | 卷一 cluster B（第492-507行有效内容） | 4 | 1 | 0.25 | 3 | 1 | 1 | 0 |  | 无 | 正式开始训练后第一个batch。用户批准前先跑了全文vs预筛文件的交叉核对（1502/1502行匹配，仅1行未覆盖且与她无关），确认locate_candidates.py的grep+聚类方法召回率可信。CEU本身是世界转移瞬间/自主意识觉醒场景，触发MM1三重验证转正。schema_violations_caught=1是抽取时手误留了ASCII引号导致YAML解析失败，当场发现修复（第三次遇到这个模式，应考虑写进CEU抽取的检查清单） |
