# Schema Gaps

`spec/CEU_schema.md` 不是定案。每条 CEU 的 `schema_gap` 字段（如果填了）汇总到这里，作为"当前 schema 哪里不够用"的原始信号池，供 `schema-reviewer` agent 定期复核。

不允许无声丢弃：`schema-reviewer` 每次复核后，无论是否触发 schema 修改，都要在下方"复核记录"里写一条结论（改了/没改+原因），不能只处理信号池里的条目却不留痕迹。

## 待复核信号

- **YLDB-V1-A-001**（`vol1_cluster_A.yaml`）：现有 schema 的核心字段（choice/value_conflict/chosen_value/power_context 里默认的"服从/反抗"框架）都预设"当事人是有自主意识的决策主体"，但这条证据（雅儿贝德"爱慕安兹"设定的起源场景）的关键价值恰恰在于"雅儿贝德此刻不是自主决策主体，是被单方面设定"。evidence_source 的 self/others/narrator 三分类里，"narrator"是最接近但不贴切的选择。建议评估是否需要专门的"起源/背景设定类"轻量分类（如 `origin_event`）。

## 复核记录

| 日期 | 复核范围 | 结论 | 是否触发schema修改 | 对应revision_log条目 |
|---|---|---|---|---|
| （尚无记录） | | | | |
