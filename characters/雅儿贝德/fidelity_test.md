# Fidelity Test — 雅儿贝德

协议见 `../../spec/eval_protocol.md`。测试集分层：

- **dev set**：卷三（未用于建模，供每次模型修改后快速反馈）
- **holdout set**：卷十三、卷十四"验证集"文件（只在里程碑跑，不因日常改动频繁使用）
- 其余卷（一、二、四～十二）为建模素材

## 状态：协议已定稿，尚未跑第一轮

计划：

1. 当前模型（value_hierarchy v0.3 / mental_models v0.2 / decision_rules v0.2 / relationship_rules v0.1）作为 baseline，先在 dev set（卷三）上跑第一轮盲测，建立分数基线
2. 之后每次修改 Character OS 文件，重跑一次 dev set 同批测试用例，记录 `eval_before` / `eval_after` / `delta` 到 `../../logs/revision_log.md`，结果同步进 `../../logs/eval_runs.md`
3. 阶段1收尾（或其他里程碑）时跑一次 holdout set（卷十三/十四），验收是否过拟合到 dev set 上的反复调参
4. 预测失败 → 修改模型（value_hierarchy / mental_models / decision_rules），不是修改答案；修正记录同步写入 `../../logs/revision_log.md`，并打 `change_type` 标签

## 盲测记录

（待第一轮 dev set 基线跑完后开始记录，对应 `eval_runs.md` 中的 eval_id）
