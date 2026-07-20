# Eval Runs

结构化评估记录，协议见 `../spec/eval_protocol.md`。每次跑 dev/holdout 盲测追加一行。

| eval_id | date | type | model_ref | test_set | n_cases | predictive_accuracy | style_score | notes |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-07-19 | holdout（盲测） | profile v0.7（报告落盘于8b51cff） | 雅儿贝德-卷十三验证集（84占位符/116有效项） | 116 | 0.55 | 未单独评 | 首次真正盲测；复盘归因多数失败为推理端错误，催生prediction_protocol三步协议；contamination caveat适用（补登记录，原始报告见logs/predictions/vol13_scored.md） |
| E002 | 2026-07-20 | dev（盲测调试） | profile v0.8 @ e4c0268 | 雅儿贝德-卷十一验证集（BD特典drama段30项） | 30 | 0.57（机制0.80分开计） | 3/5 | **非干净盲测**（本卷已被train/audit消费过，分数仅供gap识别）；推理端调试轮：产出协议v1.1两条+profile v0.9四条通用修正；机制0.80vs总分0.57定位主要损失在文风渲染层 |
| E003 | 2026-07-20 | dev（盲测调试） | profile v0.9 @ 3a0cbbb | 雅儿贝德-卷十二验证集（使节接见29项，全对外场合） | 29 | 0.59（机制0.83分开计） | 3.5/5 | **非干净盲测**；与E002互补覆盖语域两极（内部私密/对外公务）；v1.1协议实测有效（状态继承+邻接反推）；产出协议v1.2一条+profile v0.10五条通用修正（归荣于上/隐威慑显体贴/躯体泄露通道/语体表演价值/小女子谦称）；损失稳定集中在话语模式层 |
| E004 | 2026-07-20 | holdout（干净盲测·test收官） | profile v0.10+协议v1.2 @ 1ca774e | 雅儿贝德-卷十四验证集（291占位符/200计分项，五场景全语域） | 200 | **0.63**（机制0.815分开计） | 3.5/5 | **项目级干净盲测**（本卷从未被消费；contamination条件与vol13基线相同故对比有效）；**0.55→0.63，dev调试闭环的真实增益确认**；残余损失定位于五个可命名层面（内心战略分析档/共谋筹划平语/支配游戏话术/私人势力实证/称谓补正），候选修正因来源为test仅记录待决，见logs/predictions/vol14_scored.md |

## 字段说明

- `eval_id`：如 `E001`，递增编号
- `type`：`dev` 或 `holdout`
- `model_ref`：跑这次评估时对应的 git commit hash 或 tag
- `test_set`：如 `雅儿贝德-卷三-batch1`
- `predictive_accuracy`：对/(对+部分对*0.5+错) 的总用例，部分对按 0.5 计
- `style_score`：1-5 分，LLM-judge 平均分（`profile.yaml` 的 `speech_register` 内容不足前该分数仅供参考）
