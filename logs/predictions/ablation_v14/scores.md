# vol14 三臂消融实验评分报告

生成日期：2026-07-28

## 流程

- arm A（无 profile）由冷上下文 agent 生成，仅允许读取 `arm_task_spec.md`、`arena_A.txt`、`arena_B.txt`、`spec/prediction_protocol.md`。
- arm B（错 profile）与 arm C（真 profile v0.10）沿用已冻结预测文件。
- `merge_blind.py` 将三臂逐项随机打乱为 X/Y/Z，生成 `scoring_sheet.md` 与 `unblind_key.json`。
- 盲评分由独立冷上下文 agent 完成，仅允许读取 `rubric.md` 与 `scoring_sheet.md`，输出 `scores_raw.md`。
- 主 agent 在 `scores_raw.md` 完成后才运行 `unblind.py` 揭盲。

## 揭盲结果

| arm | 条件 | 内容准确率 | n | 语域正确率 | n |
|---|---|---:|---:|---:|---:|
| A | 无 profile | 0.373 | 79 | 0.760 | 25 |
| B | 错 profile | 0.424 | 79 | 0.800 | 25 |
| C | 真 profile v0.10 | 0.430 | 79 | 0.760 | 25 |

## 分段结果（内容准确率）

| arm | chunk A 独处 | chunk B 对外公务 |
|---|---:|---:|
| A | 0.354 (n=48) | 0.403 (n=31) |
| B | 0.427 (n=48) | 0.419 (n=31) |
| C | 0.417 (n=48) | 0.452 (n=31) |

## 对照差值

| 对照 | 差值 | 含义 |
|---|---:|---|
| C - A | +0.057 | 真 profile 相对无 profile 的边际贡献 |
| B - C | -0.006 | 喂错 profile 相对真 profile 的代价 |
| B - A | +0.051 | 错 profile 相对无 profile 的变化 |

## 判读

按 `rubric.md` 的预注册口径，`C - A = +0.057` 落在 `+0.05 ~ +0.15` 的中间带：有弱信号，但 n=79 不足以定论。并且该差值低于预注册的“不宣称差异”阈值 0.11；若按两独立比例差的更保守标准，`unblind.py` 给出的阈值约为 0.16，同样不宣称差异。

`B - C = -0.006`，绝对值远小于 0.05，符合预注册判读表中的 `B ≈ C`：在这轮冷上下文设置里，错 profile 与真 profile 几乎没有拉开。这说明模型输出没有稳定体现 profile 内容被强消费；更像主要由预训练召回、竞技场邻接上下文和通用推理协议驱动。

结论：这轮 79 槽消融不能支持“profile v0.10 在冷上下文中带来稳定、可检出的增益”。此前 `0.55 → 0.63` 的解释需要下调 profile 贡献权重，并保留“可能主要来自预训练召回/推理协议/热上下文”的替代解释。

## 注意事项

- 本实验是描述性消融，不宣称显著性。
- 本轮样本是 vol14 的 79 槽子集，且评分者/上下文设置不同；结果不应直接等同于旧 `vol14_scored.md` 的 200 项全量分数。
- 《OVERLORD》原著很可能进入预训练语料，contamination caveat 仍适用。
