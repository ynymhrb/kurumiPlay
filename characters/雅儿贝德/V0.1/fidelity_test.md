# Fidelity Test

## 状态：未开始

计划：

1. 用第一卷全文逐章提取 CEU，修正/夯实 value_hierarchy / mental_models / decision_rules 到稳定版本
2. 冻结该版本模型
3. 用第二卷（未见数据）逐 CEU 盲测：
   - 模型能否正确预测雅儿贝德在给定 trigger + context 下的 choice？
   - 哪些行为无法解释？记录到 `contradictions.md`
4. 预测失败 → 修改模型（value_hierarchy / mental_models / decision_rules），不是修改答案
5. 修正记录同步写入 `../../logs/revision_log.md`

## 盲测记录

（待第一卷模型稳定后开始）
