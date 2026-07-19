---
name: character
description: 小说角色认知建模Skill，支持两种任务：①角色蒸馏——从小说原文逐卷构建可运行的角色认知模型（CSE架构：profile.yaml静态特质+events/动态时间线），产出存放在characters/<角色>/下；②言行预测——加载characters/下已蒸馏的角色模型，在新场景或盲测验证集中生成/预测该角色的言行（含强制三步推理协议）。
---

# 角色蒸馏与言行预测

从小说原文提取**驱动角色言行的深层特征**（信念/价值排序/决策规则/心理机制/语言指纹），构建成认知模型（**蒸馏**）；再用该模型推理角色在新场景下会说什么、做什么（**预测**）。不是写人物简介，不是死记角色说过的话。

**本文件只是流程骨架和路由；每一步的权威定义在 `spec/` 对应文件里，执行到该步时必须先通读它，不凭本文件的一句话概括开工。**

**任务路由**：
- 建模/训练/处理某卷/开新角色 → 【一、角色蒸馏】
- 盲测/RolePlay/预测角色言行 → 【二、言行预测】，模型从 `characters/<角色>/V<最新轮次>/` 加载

## 目录速查

| 路径 | 作用 |
|---|---|
| `spec/` | 全部方法论正本（schema、归因、心理机制、语言指纹、评估、预测），见下方各步引用 |
| `characters/<角色>/source/` | 原文分卷txt + 盲测验证集（各轮次共用） |
| `characters/<角色>/V<轮次>/` | 蒸馏产出：profile.yaml / profile_trace.yaml / events/ / literary_techniques.md / ROUND_STATUS.md |
| `logs/` | revision_log（字段级修正审计）/ construction_log（过程指标）/ eval_runs（正式评分）/ schema_gaps（schema信号池）/ predictions/（预测与评分报告） |
| `scripts/locate_candidates.py` | 候选场景定位（grep人名+聚类） |

# 一、角色蒸馏（训练侧）

**开新角色/新轮次**：目录规划、大小版本规则、train/dev/test切分、轮次冻结打tag —— 全按 `spec/eval_protocol.md` §0-§2 执行。

**逐卷训练**（每卷按序8步；流程定义=`eval_protocol.md` §7）：

| 步骤 | 权威spec |
|---|---|
| 1. 定位：`python scripts/locate_candidates.py <角色> <卷号>` | — |
| 2. 事件提取（两遍法；raw_quote先行，留空不臆测） | `spec/event_schema.md`（先通读） |
| 3. 归因分析（仅触发时；心理轴优先） | `spec/attribution_framework.md`（触发条件也在此） |
| 4. profile更新（修正模型而非硬凑解释；防过拟合门槛；矛盾找深层机制；trace同步） | `spec/character_static_profile_schema.md`（含双文件纪律）+ `spec/psychological_structure_protocol.md` |
| 5. speech_register更新（分场合分桶，n/p(n)重算） | `spec/expression_dna_protocol.md` |
| 6. schema复核（改不改都留复核记录） | `logs/schema_gaps.md` 顶部说明 |
| 7. 过程指标一行 | `spec/eval_protocol.md` §8 |
| 8. 收尾：更新ROUND_STATUS → commit → 回填`git_ref: 待回填`（回填单独小commit） | `spec/eval_protocol.md` §1 |

**dev / test 阶段**：dev卷跑derivability audit（事后解释，价值在gap识别），test卷做占位符盲测（走【二】的流程，先冻结预测再评分）——切分、评分两维度（预测准确率+风格保真度）、change_type、日志格式全按 `spec/eval_protocol.md` §2-§6。

# 二、言行预测（推理侧）

**执行前必须通读 `spec/prediction_protocol.md`（正本）**，要点索引：

- 三种模式：盲测填充 / 新场景RolePlay生成 / derivability audit（仅dev）
- 加载纪律：只加载 `profile.yaml` + `literary_techniques.md`；不加载trace；盲测严禁读原文
- 第0步事件建模 → **强制三步推理协议**：①定观众再选机制 ②先检索存量再发明 ③语域选档写完自检
- 输出格式（带推理链）、盲测评分与复盘（先归因推理端再归因模型端）、RolePlay状态连续性规则

# 铁律（跨两侧，spec细节以spec为准）

1. 失败即改模型，不是改答案/硬凑解释
2. raw_quote先行，留空不臆测
3. 心理轴优先于文学轴；文学外壳单独沉淀进literary_techniques.md，不当字面行为
4. 矛盾是信号不是终点：找不到统一机制就标open，禁止编造
5. 修正只能是通用简短逻辑，禁止场景级补丁（过拟合）
6. profile简洁/trace分离，两边同步
7. 所有修正字段级可追溯（revision_log），所有评估记录git_ref
8. derivability是必要非充分条件：盲测失败先查推理端三步，再考虑改模型
