# vol14 全量消融实验 · Arm A（无 profile）任务说明

## 你的任务

给定《OVERLORD》第十四卷的小说节选（4 个 arena 文件），其中若干处被挖空成 `【#N】`。
请**逐个预测每个空里原本是什么内容**。

- 目标角色：**雅儿贝德**（纳萨力克地下大坟墓守护者总管）。
- 挖空的绝大多数是她的言行、心理活动、表情动作；少数是与她直接相关的叙述。
- 你**看不到**原文答案，这是盲测。

## 输入文件（只允许读这些）

1. `logs/predictions/ablation_v14_full/arena_part01.txt`
2. `logs/predictions/ablation_v14_full/arena_part02.txt`
3. `logs/predictions/ablation_v14_full/arena_part03.txt`
4. `logs/predictions/ablation_v14_full/arena_part04.txt`
5. `spec/prediction_protocol.md`（三步推理协议，必须执行）

## 禁止读的文件

- `logs/predictions/ablation_v14_full/gt_key.md`
- `logs/predictions/ablation_v14_full/arena_*.txt` 以外的本目录文件
- `logs/predictions/vol14_blind.md`
- `logs/predictions/vol14_scored.md`
- `logs/predictions/ablation_v14/` 下全部文件
- `characters/雅儿贝德/` 下全部文件（profile.yaml、literary_techniques.md 等）
- `characters/雅儿贝德/source/` 下全部原文
- 任何联网搜索

## 硬性纪律

1. **按顺序写，写完冻结，不要回头改。**
2. 每个 `【#N】` 都必须给出预测，**不许跳过、不许写"无法判断"**。
3. 预测的是**内容**，语气/自称/敬语档位属于评分范围。
4. 严格遵循 `spec/prediction_protocol.md` 的三步推理协议（事件建模→邻接反推→定观众→查存量→语域选档）。

## 输出格式（每行一条，评分脚本要解析）

```
#N | 预测内容
```

- 括注 `（内心）`/`（动作）`/`（台词）` 可选
- 对话行里的空，直接写她说的话
- 多行预测放在同一行内，用 `／` 分隔（如 `#168 | 第一句／第二句`）

## 输出文件

按 part 分四个文件，每个文件只写对应 arena 的预测：

- `logs/predictions/ablation_v14_full/pred_armA_part01.md`（对应 arena_part01）
- `logs/predictions/ablation_v14_full/pred_armA_part02.md`（对应 arena_part02）
- `logs/predictions/ablation_v14_full/pred_armA_part03.md`（对应 arena_part03）
- `logs/predictions/ablation_v14_full/pred_armA_part04.md`（对应 arena_part04）

每个文件头一行写 `# Arm A predictions for arena_part0N`，然后逐行预测。

全部完成后报告"已写入 pred_armA_part01-04.md，共 N 行"。
