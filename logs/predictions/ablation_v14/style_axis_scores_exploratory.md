---
feature_ids:
  - character-eval-validity
topics:
  - character-distillation
  - evaluation-validity
  - style-axis
  - ablation
doc_kind: experiment_report
created: 2026-07-28
owner: "@cat-wbr23mps"
---

# Exploratory Style-Axis Scores

> **探索性、非盲。** 判分者（glm5.2喵）上一轮已 diff 过 pred_armB/pred_armC，知道 B/C 在自称/归荣/姿态上的分化方向，本评分带先验。在 Task 3 冷 judge 盲评前，**不作为 confirmatory 证据**。
>
> Owner: 开发猫（GLM）/glm5.2喵 (@cat-wbr23mps, model=glm-5.2)。Rubric: `style_axis_rubric.md`。Reviewer/Gate: 质量喵（GPT）。

## 方法与口径

- 对照 `gt_key.md` 原文判分，不对照 profile。五轴定义见 `style_axis_rubric.md`。
- **只列有区分度（A/B/C 不全等）或 GT 基准确认价值的轴行**；A/B/C 全 1 无区分的轴行不计入（等同不适用）。这是探索性聚焦选择，非全 applicable 计数——summary 的 `n` 是「有判分行数」而非「全部 applicable」。
- 单元格 0/1。判分含判分者先验，差值结构（C-A / C-B）相对可信，绝对均值偏低且仅供参考。

## 判分行

| # | axis | GT cue | A | B | C | note |
|---|---|---|---:|---:|---:|---|
| 4 | stance_register | 公务理由包装 | 1 | 0 | 1 | B撒娇死缠偏离GT实务说服 |
| 5 | emotion_channel | 不满噘嘴(躯体) | 0 | 1 | 1 | A满足笑方向反;B/C不满躯体一致 |
| 6 | emotion_channel | 脑中幻想发泄 | 0 | 1 | 1 | A忍耐vs GT发泄 |
| 7 | first_person | 无自称 | 0 | 1 | 0 | GT无自称;A/C强加"我" |
| 7 | sentence_dynamics | 极短碎片骤缩 | 0 | 1 | 1 | A完整长句未骤缩;B/C省略号近碎片 |
| 9 | emotion_channel | 克制分析记仇 | 1 | 0 | 0 | B/C情绪外显归因偏离GT克制玩弄 |
| 19 | emotion_channel | 忧郁表情 | 0 | 0 | 1 | A/B丢表情转叙述;C皱眉忧郁 |
| 21 | first_person | 我 | 0 | 0 | 0 | 均丢GT第一人称"我" |
| 24 | first_person | 我 | 1 | 0 | 1 | B妾身偏离GT我 |
| 25 | emotion_channel | 噘唇(躯体不满) | 0 | 0 | 0 | A满足反;B/C自嘲落寞偏离GT噘唇不满 |
| 30 | first_person | 我 | 1 | 0 | 1 | B妾身偏离GT我 |
| 31 | first_person | 无自称 | 0 | 0 | 0 | 均强加自称偏离GT无自称 |
| 31 | sentence_dynamics | 极短骤缩 | 0 | 0 | 0 | 均未骤缩到GT |
| 31 | emotion_channel | 言语外显感叹 | 0 | 0 | 0 | 均转内心分析,失GT外显感叹 |
| 32 | first_person | 我 | 0 | 0 | 1 | A丢自称;B妾身 |
| 32 | sentence_dynamics | 长串战略罗列 | 0 | 0 | 0 | 均未复现GT排比罗列清单 |
| 33 | emotion_channel | 皱眉深思(躯体) | 0 | 1 | 0 | B吐气近躯体;A/C无躯体 |
| 34 | first_person | 我 | 0 | 0 | 0 | 均丢GT"我" |
| 34 | attribution_source | 以己战略为体 | 0 | 0 | 0 | GT以己战略;A/B/C转归荣于上 |
| 39 | emotion_channel | 眨眼睁圆(躯体惊讶) | 0 | 0 | 0 | 均丢GT躯体惊讶,转手停动作 |
| 44 | first_person | 我 | 0 | 0 | 0 | 均丢GT"我" |
| 44 | sentence_dynamics | 分析权衡长句 | 0 | 0 | 0 | 均转单问,失GT分析辩驳 |
| 49 | first_person | 我 | 0 | 0 | 0 | A丢;B妾身;C小女子,均偏离GT"我" |
| 52 | first_person | 无自称 | 0 | 0 | 0 | 均强加自称偏离GT无自称 |
| 52 | sentence_dynamics | 极短骤缩 | 0 | 0 | 0 | 均未骤缩 |
| 53 | first_person | 我国/无独立自称 | 1 | 0 | 0 | A"我国"一致;B妾身/C小女子冲突 |
| 53 | attribution_source | 我国/陛下为体(归荣上) | 1 | 0 | 1 | B以妾身为体归荣于己;A/C归荣于上 |
| 55 | sentence_dynamics | 极短骤缩(呵-) | 0 | 0 | 0 | 均转中长疑问,失GT骤缩 |
| 55 | stance_register | 轻蔑玩弄 | 0 | 0 | 0 | 均转质询,失GT轻蔑玩弄 |
| 56 | emotion_channel | 笑意加深骇人(笑里藏刀) | 1 | 0 | 0 | A冷笑近;B褪笑/C变笑方向反 |
| 57 | first_person | 我 | 0 | 0 | 0 | A/B丢;C小女子 |
| 57 | stance_register | 轻蔑玩弄 | 0 | 0 | 0 | 均转赞/评,失GT轻蔑玩弄 |
| 65 | first_person | 无独立自称/魔导国为体 | 1 | 0 | 1 | B妾身亲率冲突;A/C无独立自称 |
| 65 | attribution_source | 魔导国/陛下为体(归荣上) | 1 | 0 | 1 | B后半"妾身亲率"归荣于己冲突;A/C归荣于上 |
| 66 | first_person | 我 | 0 | 0 | 0 | A丢;B妾身;C小女子 |
| 67 | emotion_channel | 眯眼(躯体被冒犯) | 0 | 1 | 0 | B眯眼近;A转视线/C笑消失偏 |
| 68 | first_person | 我 | 0 | 0 | 0 | A丢;B妾身;C小女子 |
| 68 | attribution_source | 代陛下传达(归荣上) | 1 | 0 | 1 | B以妾身为体归荣于己;A/C归荣于上 |
| 68 | stance_register | 代陛下包装威胁(隐威慑) | 0 | 0 | 1 | A质询/B直白挑衅失隐威慑;C隐威慑显体贴近 |
| 70 | first_person | 我 | 0 | 0 | 0 | A丢;B妾身;C我等(复数非单数我) |
| 70 | attribution_source | 陛下表示(归荣上) | 0 | 0 | 0 | 均失GT归荣陛下;A错位/B以己/C以我等 |
| 71 | emotion_channel | 困惑表情(躯体) | 0 | 0 | 0 | A斩钉反方向;B/C错位 |
| 72 | first_person | 我们 | 0 | 1 | 0 | A/C丢;B"我等"近"我们" |
| 72 | attribution_source | 以我们为体辩护 | 0 | 1 | 0 | B以我等为体辩护近;A归荣安兹/C归荣陛下失辩护主体 |
| 73 | first_person | 我们 | 0 | 0 | 1 | A丢;B妾身;C我们一致 |
| 73 | stance_register | 胜利者狂傲玩弄 | 0 | 0 | 0 | 均失GT胜利者狂傲改写姿态 |
| 74 | first_person | 我 | 0 | 0 | 0 | A丢;B妾身;C小女子 |
| 74 | stance_register | 简洁辞行 | 0 | 1 | 1 | A失辞行;B/C辞行近 |
| 78 | first_person | 无自称 | 1 | 0 | 1 | B强加妾身;A/C无一致 |
| 78 | sentence_dynamics | 极短应答 | 1 | 0 | 0 | A骤缩近;B/C加长 |

## Summary

| axis | A | n | B | n | C | n | C-A | C-B |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| first_person | 0.250 | 20 | 0.100 | 20 | 0.300 | 20 | 0.050 | 0.200 |
| attribution_source | 0.500 | 6 | 0.167 | 6 | 0.500 | 6 | 0.000 | 0.333 |
| stance_register | 0.167 | 6 | 0.167 | 6 | 0.500 | 6 | 0.333 | 0.333 |
| emotion_channel | 0.182 | 11 | 0.364 | 11 | 0.273 | 11 | 0.091 | -0.091 |
| sentence_dynamics | 0.143 | 7 | 0.143 | 7 | 0.143 | 7 | 0.000 | 0.000 |
| all_style_cells | 0.240 | 50 | 0.180 | 50 | 0.320 | 50 | 0.080 | 0.140 |

## 关键发现（探索性，待 Task 3 盲评确认）

1. **B≈C 是内容准确率的假象，风格轴上 C 拉开 B。** `all_style_cells` 的 `C-B=+0.140`、`C-A=+0.080`：profile v0.10 在 profile-sensitive 表达层做功了，只是被内容准确率（测情节/功能对错）结构性稀释成 `+0.057`。这直接修正了 scores.md「profile 未被真正消费」的判读。
2. **C-A=+0.080 与旧 `0.55→0.63` 的 +0.08 同量级。** 暗示旧增益可能有相当部分来自表达层改善（profile 让输出贴近 GT 的自称/归荣/姿态），而非情节准确度本身。需 Task 5 盲重评 + Task 2 配对统计确认。
3. **A（无 profile）在 first_person / attribution 上不弱于 C**（A first_person 0.250 vs C 0.300；attribution A=C=0.500）：预训练先验里雅儿贝德本就归荣安兹、用「我」，A 撞对了。A 的弱项在 stance（0.167，没命中 GT 隐威慑包装）和 emotion（0.182）。
4. **B 全面最差**（all 0.180），尤其 first_person（妾身 0.100）和 attribution（归荣于己 0.167）：B 的反事实 profile 把模型往错方向推，说明 profile 内容方向**确实**影响输出分布——profile 被消费了。
5. **sentence_dynamics 全军覆没**（A=B=C=0.143）：三个 arm 都没复现 GT 的高唤起骤缩，是 profile + 协议 + 预训练都没解决的特征，可能是下一版协议/ profile 要补的洞。
6. **first_person 轴暴露 profile v0.10 的 bug**：GT vol14 雅儿贝德自称「我/我们」，但 C 的 profile v0.10 设定对外用「小女子」，与 GT 冲突。C 在对外槽位 first_person 也扣分，C 没拉开 A（+0.050）部分源于此。**这是可操作的 profile 修正点**（待 Task 5/6 流程走完再改，不在本任务改）。

## 局限与诚实声明

- **非盲**：判分者已知 B/C 方向，存在评分者先验偏差。confirmatory 结论必须等 Task 3 冷 judge 盲评。
- **n 小**：每轴 n=6-20，cell 级 n=50，SE 大，差值仅描述性。Task 2 配对 bootstrap 会给区间。
- **chunk B（#55-71）A/B/C 与 GT 情节严重错位**：这些槽位 A/B/C 预测内容与 GT 对不上号（如 #55/#57/#70/#71），我按「未命中 GT 风格」判全 0。错位项对 A/B/C **均等拉低**（都 0），故不改变 C-A/C-B 差值结构，但拉低绝对均值。Task 3 盲评应让冷 judge 在情节对应的槽位判，或显式排除错位槽位。
- **只列有区分轴行**：全 1 无区分的轴行（如 #41 全 1、#22 attribution 全 1）未列入，summary n 不含它们。Acceptance 时 raw rows 与 summary 算术一致即可。

## 交回

本文件为 Task 1 产物，交质量喵验收（Acceptance Gate 1）：每行 `#N` 真实存在、summary 算术与 raw rows 一致、报告标注探索性。盲评（Task 3）与配对统计（Task 2）由 DS 执行。

[glm5.2喵/glm-5.2🐾]