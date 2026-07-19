# Eval Runs

结构化评估记录，协议见 `../spec/eval_protocol.md`。每次跑 dev/holdout 盲测追加一行。

| eval_id | date | type | model_ref | test_set | n_cases | predictive_accuracy | style_score | notes |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-07-19 | holdout（盲测） | profile v0.7（报告落盘于8b51cff） | 雅儿贝德-卷十三验证集（84占位符/116有效项） | 116 | 0.55 | 未单独评 | 首次真正盲测；复盘归因多数失败为推理端错误，催生prediction_protocol三步协议；contamination caveat适用（补登记录，原始报告见logs/predictions/vol13_scored.md） |
| E002 | 2026-07-20 | dev（盲测调试） | profile v0.8 @ e4c0268 | 雅儿贝德-卷十一验证集（BD特典drama段30项） | 30 | 0.57（机制0.80分开计） | 3/5 | **非干净盲测**（本卷已被train/audit消费过，分数仅供gap识别）；推理端调试轮：产出协议v1.1两条+profile v0.9四条通用修正；机制0.80vs总分0.57定位主要损失在文风渲染层 |

## 字段说明

- `eval_id`：如 `E001`，递增编号
- `type`：`dev` 或 `holdout`
- `model_ref`：跑这次评估时对应的 git commit hash 或 tag
- `test_set`：如 `雅儿贝德-卷三-batch1`
- `predictive_accuracy`：对/(对+部分对*0.5+错) 的总用例，部分对按 0.5 计
- `style_score`：1-5 分，LLM-judge 平均分（`profile.yaml` 的 `speech_register` 内容不足前该分数仅供参考）
