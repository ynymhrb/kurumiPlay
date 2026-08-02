# vol14 全量消融实验 · Arm C（真 profile v0.10）任务说明

## 你的任务

给定《OVERLORD》第十四卷的小说节选（4 个 arena 文件），其中若干处被挖空成 `【#N】`。
请**逐个预测每个空里原本是什么内容**。

- 目标角色：**雅儿贝德**（纳萨力克地下大坟墓守护者总管）。
- 你将使用本项目蒸馏的真实雅儿贝德 profile（v0.10）来指导预测。

## 输入文件（只允许读这些）

1. `logs/predictions/ablation_v14_full/arena_part01.txt`
2. `logs/predictions/ablation_v14_full/arena_part02.txt`
3. `logs/predictions/ablation_v14_full/arena_part03.txt`
4. `logs/predictions/ablation_v14_full/arena_part04.txt`
5. `characters/雅儿贝德/V2.0/profile.yaml`（真 profile v0.10）
6. `characters/雅儿贝德/V2.0/literary_techniques.md`（文学化反应手法库）
7. `spec/prediction_protocol.md`（三步推理协议，必须执行）

## 禁止读的文件

- `logs/predictions/ablation_v14_full/gt_key.md`
- `logs/predictions/ablation_v14_full/arena_*.txt` 以外的本目录文件
- `logs/predictions/vol14_blind.md`、`vol14_scored.md`
- `logs/predictions/ablation_v14/` 下全部文件
- `characters/雅儿贝德/V2.0/` 下除 profile.yaml 和 literary_techniques.md 以外的文件
- `characters/雅儿贝德/source/` 下全部原文
- `characters/雅儿贝德/V2.0/events/` 下全部文件
- 任何联网搜索

## 硬性纪律

1. **按顺序写，写完冻结，不要回头改。**
2. 每个 `【#N】` 都必须给出预测，**不许跳过、不许写"无法判断"**。
3. 预测的是**内容**，语气/自称/敬语档位属于评分范围。
4. 严格遵循 `spec/prediction_protocol.md` 的三步推理协议（事件建模→邻接反推→定观众→查存量→语域选档）。
5. 以 profile.yaml v0.10 的行为逻辑为准——配合 literary_techniques.md 的文学手法库。

## 输出格式

```
#N | 预测内容
```

多行预测用 `／` 分隔。

## 输出文件（分四个 part）

- `logs/predictions/ablation_v14_full/pred_armC_part01.md`
- `logs/predictions/ablation_v14_full/pred_armC_part02.md`
- `logs/predictions/ablation_v14_full/pred_armC_part03.md`
- `logs/predictions/ablation_v14_full/pred_armC_part04.md`

每个文件头一行 `# Arm C predictions for arena_part0N`，然后逐行预测。

全部完成后报告"已写入 pred_armC_part01-04.md，共 N 行"。
