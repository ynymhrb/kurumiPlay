# Fidelity Test — 雅儿贝德

协议见 `../../../spec/eval_protocol.md`。数据集切分（约 8:1:1）：

- **train（构建素材，当前所处阶段）**：卷一～卷十
- **dev set（尚未开发）**：卷十一、卷十二
- **test / holdout set**：卷十三、卷十四"验证集"文件

## 状态：仍在 train 阶段（卷二已处理，卷一及卷三～十未开始）

当前顺序：先把 train 阶段（卷一～十）的 CEU 提取和 Character OS 构建做到收敛（`triggered_revisions` 趋于稳定，见 `../../../logs/construction_log.md`），再启动 dev 阶段。

计划：

1. train 阶段（卷一～十）：逐卷跑 CEU 提取，过程指标写入 `../../../logs/construction_log.md`；触发模型修正时更新 `../../../logs/revision_log.md` 并打 `change_type` 标签
2. train 阶段收敛信号：连续多卷 `triggered_revisions` 明显下降，视为模型基本稳定，可以冻结一个版本（打 git tag）
3. 启动 dev 阶段（卷十一、十二）：按 `eval_protocol.md` 第3-4节构造预测任务、跑盲测，记录 `predictive_accuracy` / `style_score` 到 `../../../logs/eval_runs.md`（type=dev）；允许根据 dev 失败案例反过来修改模型，同步记 `eval_before`/`eval_after`/`delta` 到 `revision_log.md`
4. 阶段1收尾（或其他里程碑）时跑一次 test/holdout（卷十三/十四），记录进 `eval_runs.md`（type=holdout），验收是否过拟合到 dev 上的反复调参
5. 预测失败 → 修改模型（value_hierarchy / mental_models / decision_rules），不是修改答案

## 盲测记录

（待 train 阶段收敛、dev 阶段启动后开始记录，对应 `eval_runs.md` 中的 eval_id）
