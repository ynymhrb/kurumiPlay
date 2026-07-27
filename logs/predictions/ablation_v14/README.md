# vol14 三臂消融实验（ablation）

**⚠️ 本目录全部为实验对照件，不是蒸馏产物。`wrong_profile_counterfactual.yaml` 是故意写错的假模型（标签写雅儿贝德、行为内容系统性反转），仅供 arm B 使用，任何情况下都不得被引用为角色模型或复制进 `characters/`。**

## 要回答的问题

`0.55 → 0.63` 这个增益里，有多少来自 `profile.yaml`，有多少只是预训练里本来就记得《OVERLORD》？

## 设计

同一批 79 个占位符，三个 arm 唯一变量 = profile：

| arm | profile 输入 | 测什么 |
|---|---|---|
| A | 无（只有三步协议 + 角色名） | 裸预训练召回 + 协议脚手架的基线 |
| B | `wrong_profile_counterfactual.yaml`（假的，行为反转） | profile 到底有没有被消费 |
| C | `characters/雅儿贝德/V2.0/profile.yaml`（真 v0.10） | 冷上下文下的真实处理效果 |

**为什么 arm C 也要重跑**：既有的 0.63 是我在有完整会话上下文（写过协议、调过 vol11/12）的状态下产出的。若 A/B 冷跑而 C 用旧成绩，比较的就变成"冷 vs 热"而不是"有 profile vs 无 profile"。三臂同为冷上下文 subagent，旧的 0.63 只作外部参照点。

**为什么必须冷跑**：主 agent 已经看过 vol14 的 ground truth（上一轮打过分），不再是盲的。冷上下文 subagent 从未见过答案。

**为什么错 profile 是"反事实雅儿贝德"而不是"夏提雅"**：若文件头写着夏提雅，agent 一眼识破即丢弃它、回退到预训练记忆，arm B 会塌缩成 arm A，无法区分"没读 profile"和"读了但识破"。标签保持雅儿贝德、只反转行为内容，则唯一的识破通道就是预训练记忆本身——正是待测变量。

## 判读表

| 观察 | 结论 |
|---|---|
| A ≈ C | profile 边际贡献≈0，此前测的是预训练召回率 |
| A ≪ C | profile 在做真功 |
| B ≈ C | profile 没被真正消费，模型走预训练捷径 |
| B ≪ A | profile 被强消费（喂错就被带偏） |
| B ≈ A | 模型能识别并抵抗错误 profile |

## 文件

- `arena_A.txt` / `arena_B.txt`：竞技场（L1-100 独处 48 槽；L500-700 对外公务 31 槽）
- `gt_key.md`：答案键，**预测阶段禁止提供给任何 arm**
- `arm_task_spec.md`：三臂共用的任务说明
- `pred_arm{A,B,C}.md`：三臂冻结预测
- `scores.md`：评分与复盘
- `../../scripts/build_ablation_arena.py`：竞技场/答案键生成器（逐行正则回填，79/79 对齐成功）
