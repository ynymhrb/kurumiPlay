---
name: character-distill
description: 角色蒸馏——从小说原文逐卷构建可运行的角色认知模型（CSE架构：profile.yaml静态特质+events/动态时间线）。用于开启新角色/新轮次、逐卷训练、dev评估、日志与版本管理。
---

# 角色蒸馏（Character Distillation）

从小说原文提取**驱动角色言行的深层特征**（信念/价值排序/决策规则/心理机制/语言指纹），构建成可用于言行预测的认知模型。不是写人物简介，不是死记她说过的话。

言行预测（用建好的模型生成/预测）是另一个skill：`character-predict`。

## 文件地图

| 路径 | 作用 |
|---|---|
| `spec/character_static_profile_schema.md` | profile.yaml 字段定义 |
| `spec/event_schema.md` | events/<卷>.yaml 字段定义 + 两遍法提取流程 |
| `spec/attribution_framework.md` | 双轴归因（心理轴四层→文学轴两层），触发条件见该文件 |
| `spec/psychological_structure_protocol.md` | 表象矛盾→深层机制的处理流程 |
| `spec/expression_dna_protocol.md` | speech_register语言指纹提取 + 特征频率概率模型 |
| `spec/eval_protocol.md` | 轮次版本化、train/dev/test切分、评分协议、日志字段定义 |
| `characters/<角色>/source/` | 原文分卷txt（各轮次共用） |
| `characters/<角色>/V<轮次>/` | 本轮产出：profile.yaml / profile_trace.yaml / events/ / literary_techniques.md / ROUND_STATUS.md |
| `logs/` | revision_log（字段级修正审计）/ construction_log（过程指标）/ eval_runs（正式评分）/ schema_gaps（schema信号池）/ predictions/（预测与评分报告） |
| `scripts/locate_candidates.py` | 候选场景定位（grep人名+聚类，产出events/_index_vol<N>.yaml） |

## 双文件纪律：profile.yaml 与 profile_trace.yaml

- **profile.yaml**：纯推理用行为逻辑，保持简洁（每条只带一词级status标注）。预测时只加载这个文件。
- **profile_trace.yaml**：证据链、置信度详情、逐卷来源、变更记录，键名与profile.yaml对应。
- 理由：追溯内容混进推理文件会稀释注意力。任何新增证据/修正都要**两边同步**：逻辑进profile，证据进trace。

## 开启新角色 / 新轮次

1. 建目录 `characters/<角色>/V<版本>/`（大版本=规范有实质变化的新一轮，小版本=同轮修正迭代，见eval_protocol §0）
2. 原文分卷放 `characters/<角色>/source/`，按卷数做 train/dev/test ≈ 8:1:1 切分并记入ROUND_STATUS
3. 建空的 `profile.yaml`（按schema骨架）、`profile_trace.yaml`、`events/`、`ROUND_STATUS.md`
4. 旧轮次冻结：打tag `<角色缩写>-round-v<版本>`，目录移入 `characters/<角色>/_history/`

## 逐卷训练流程（train阶段）

每处理一卷，按顺序：

1. **定位**：`python scripts/locate_candidates.py <角色> <卷号>` → 生成候选cluster索引
2. **事件提取**（两遍法，见event_schema.md）：一遍机械列全部言行节拍（宁滥勿缺）；二遍筛选"暴露价值选择/行为规律/心理机制"的节拍聚合为Event/Turn。skip的cluster记录原因。**铁律：raw_quote逐字引用先行，结构化字段从它派生；信息不足留空，不臆测。**
3. **归因分析**（仅触发时）：反应幅度异常或解释赤字 → 双轴分析写入turn的attribution。心理轴优先，文学轴是补丁不是默认。
4. **profile更新**：新事件挑战现有模型 → 修正模型而不是硬凑解释。**修正门槛（防过拟合）：只加通用属性、能简短描述的内在逻辑；禁止为单个场景加限定性补丁/白名单。** 表象矛盾走psychological_structure_protocol找深层机制，找不到就诚实标open。每条修正在revision_log.md落字段级记录（精确到具体条目），证据同步进profile_trace.yaml。
5. **speech_register更新**：本卷她的新台词补入语料池，n/p(n)按概率模型重算，必须分场合分桶。
6. **schema复核**（卷末或信号积累时）：schema_gaps.md的信号逐条处理，改不改都留复核记录。
7. **过程指标**：construction_log.md追加一行（字段见eval_protocol §8）
8. **收尾**：更新ROUND_STATUS.md → git commit → 用实际hash回填日志里的`git_ref: 待回填`（回填本身单独一个小commit）

## dev / test 阶段

- **dev卷**（倒数第3-4卷）：提取事件后跑 **derivability audit**——逐行为判断profile能否推导出它（带字段引用链），产出`logs/predictions/vol<N>.md`。允许根据失败案例改模型。注意：derivability是事后解释，分数偏高（pre-training contamination + 后见之明），真正价值是gap识别。
- **test卷**（最后1-2卷）：**占位符盲测**——把原文中该角色的言行挖成`{}`做成验证集（`<角色>_第N卷验证集.txt`），用`character-predict` skill先冻结预测，再对照原文评分。禁止调一次测一次。
- 经验教训（vol13，derivability 0.93/0.97 → blind 0.55）：**derivability是必要非充分条件**，模型解释得了不等于推理端用得对。盲测失败先归因到推理端（观众定位/存量调用/语域迁移）再考虑改模型。

## 铁律汇总

1. 失败即改模型，不是改答案/硬凑解释
2. raw_quote先行，留空不臆测
3. 心理轴优先于文学轴；文学外壳单独沉淀进literary_techniques.md，不当字面行为
4. 矛盾是信号不是终点：找能同时解释所有表现的机制，找不到标open，禁止编造
5. 修正只能是通用简短逻辑，禁止场景级补丁（过拟合）
6. profile简洁/trace分离，两边同步
7. 所有修正字段级可追溯（revision_log），所有评估记录git_ref
