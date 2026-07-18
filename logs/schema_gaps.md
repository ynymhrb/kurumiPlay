# Schema Gaps

`spec/CEU_schema.md` 不是定案。每条 CEU 的 `schema_gap` 字段（如果填了）汇总到这里，作为"当前 schema 哪里不够用"的原始信号池，供卷末的 schema 复核步骤（见 `spec/eval_protocol.md` 第7节）处理。

不允许无声丢弃：每次复核后，无论是否触发 schema 修改，都要在下方"复核记录"里写一条结论（改了/没改+原因），不能只处理信号池里的条目却不留痕迹。

## 待复核信号

- **YLDB-V1-A-001**（`vol1_cluster_A.yaml`）：现有 schema 的核心字段（choice/value_conflict/chosen_value/power_context 里默认的"服从/反抗"框架）都预设"当事人是有自主意识的决策主体"，但这条证据（雅儿贝德"爱慕安兹"设定的起源场景）的关键价值恰恰在于"雅儿贝德此刻不是自主决策主体，是被单方面设定"。evidence_source 的 self/others/narrator 三分类里，"narrator"是最接近但不贴切的选择。建议评估是否需要专门的"起源/背景设定类"轻量分类（如 `origin_event`）。
- **YLDB-V1-C-002**（`vol1_cluster_C.yaml`）：这条CEU里"追求亲密"这一段她几乎没有表现出任何内在权衡/挣扎，是无保留的欣然配合——`value_conflict` 字段假设每条CEU都存在"冲突"，但这里的关键发现恰恰是"没有冲突"本身，用 value_conflict 字段名去装"没有冲突"这件事有点错位。建议评估：是否需要一个字段/约定来专门标注"经过检查确实没有内在冲突"（区别于"没检查/漏填"），避免这类有信息量的"无冲突"发现和单纯的字段缺失混在一起。

## 复核记录

| 日期 | 复核范围 | 结论 | 是否触发schema修改 | 对应revision_log条目 |
|---|---|---|---|---|
| （尚无记录） | | | | |
