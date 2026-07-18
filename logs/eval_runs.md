# Eval Runs

结构化评估记录，协议见 `../spec/eval_protocol.md`。每次跑 dev/holdout 盲测追加一行。

| eval_id | date | type | model_ref | test_set | n_cases | predictive_accuracy | style_score | notes |
|---|---|---|---|---|---|---|---|---|
| （尚无记录） | | | | | | | | |

## 字段说明

- `eval_id`：如 `E001`，递增编号
- `type`：`dev` 或 `holdout`
- `model_ref`：跑这次评估时对应的 git commit hash 或 tag
- `test_set`：如 `雅儿贝德-卷三-batch1`
- `predictive_accuracy`：对/(对+部分对*0.5+错) 的总用例，部分对按 0.5 计
- `style_score`：1-5 分，LLM-judge 平均分（expression_dna 内容不足前该分数仅供参考）
