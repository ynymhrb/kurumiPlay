# 事件/时间线 Schema（Event & Timeline Schema）

版本：v1.0（取代 `spec/_history/CEU_schema.md` 的CEU格式，是从原文提取证据的新单元）

## 定位

CSE架构模块一·动态部分：从原文直接提取的结构化事件序列，**替代原先的CEU**——不再有独立的"CEU抽取"步骤，原文分析直接产出这里定义的Event/Turn结构。角色的动态特征（情绪、意图）只在事件级存一份初始化快照，之后的变化由推理时动态演算，不在提取阶段逐轮固化存储成"标准答案"（除非该轮次本身就是要分析的Ground Truth，见下）。

物理存储：`characters/<角色>/V<版本>/events/<卷>.yaml`，按卷拆分。

## 字段结构

```yaml
event_id:                        # 唯一事件ID，如 YLDB-EV-V1-003（卷-序号）
time_stamp:                       # 故事内时间锚点（如小说没有精确时间，写"约XX之后"或留空）
location:                         # 地点
global_background:                # 宏观背景上下文（简述，非原文摘抄）
characters_present:                # 现场参与角色ID列表
source_reference:                  # 原文出处（卷/行号），可溯源核对——沿用原CEU_schema的raw_text精神，
                                  # 但不在这里整段照抄原文，原文引用放进每个turn的raw_quote字段

event_initial_dynamic_matrix:      # 事件开始时的初始化动态快照，按角色分别记录：
  <character_id>:
    mental_fatigue:                # 0.0~1.0，若原文无法判断则留空，不臆测
    initial_emotional_vector:      # {情绪类型: 强度}，如 {嫉妒: 0.6, 忠诚: 0.9}——只记录原文
                                  # 明确支撑的情绪，不要为了填满向量而编造数值
    hierarchical_intent_tree:
      root_strategic_goal:         # 长期目标在本次事件的投影（引用profile.yaml的ultimate_goal）
      current_event_subgoal:       # 本次事件的具体目标
      immediate_talk_intent:       # 本轮谈话的战术动机

progress_timeline:                 # 按时间线演进的言行序列
  - turn_id:                       # 递增序号
    elapsed_time:                  # 相对偏移（可选）
    actor_id:                      # 发言/行动者
    raw_quote:                     # 原文逐字引用（含行号）——对应旧CEU的raw_text，仍然是
                                  # "先固定原文再派生结构化字段"这条铁律的落地位置
    action_description:            # 动作神态客观描写（从raw_quote派生，非逐字照抄）
    speech_content:                # 台词（若有）
    environmental_force_snapshot:
      situational_pressure:        # 低/中/高
      spatial_proxemics:
        distance_meters:           # 数值或"未知"
        eye_contact:                # true/false/未知
    attribution:                   # 可选，仅在触发"解释赤字"或反应幅度明显异常时才填写，
                                  # 走 spec/attribution_framework.md 的双轴分析流程，产出：
      psychological_layers:        # 心理轴四层分析摘要（生物神经/个体心理/社会情境/文化演化，
                                  # 只写有实质发现的层，没有发现的层不强行凑字数）
      explanation_deficit:         # true/false——心理轴是否能完全覆盖原文表现形式
      literary_axis:               # 仅explanation_deficit=true时填写：叙事功能层+审美符号层分析
      judgment:                    # 心理完全闭环 / 心理燃料+文学外壳
      profile_updates_suggested:   # 这条分析建议对profile.yaml哪些字段做什么修改（触发审计记录，
                                  # 见 logs/revision_log.md）
```

## 与静态特质模型的关系

`progress_timeline`里的turn是"发生了什么"的记录（Ground Truth），`attribution`字段是"为什么"的分析，分析结果不直接改变这条turn记录本身，而是反馈去修改`profile.yaml`（静态特质，如新增一条`trauma`或调整`value_hierarchy`排序）——这保持了"证据"和"模型"的分离，证据本身不因为模型更新而改写，模型可以随着新证据推翻重来。

## 提取流程

沿用原CEU两遍法的精神，改造为直接产出Event/Turn结构：

```
原文章节
 ↓
用 scripts/locate_candidates.py 定位人物出场的候选行号区间（沿用，脚本本身与CEU/Event格式无关）
 ↓
一遍：机械列出候选区间内所有"说了/做了什么"的节拍（宁可过度收录）
 ↓
二遍：判断哪些节拍构成有意义的事件（标准同旧CEU：暴露价值选择/行为规律/心理机制，
      而不只是"发生了什么"），聚合进同一个event_id的progress_timeline（同一场景多个节拍
      是同一event的多个turn，不是分开的event）
 ↓
反应幅度明显异常或触发"解释赤字"信号的turn，补充attribution字段
 ↓
汇总进 characters/<角色>/V<版本>/events/<卷>.yaml
 ↓
根据attribution.profile_updates_suggested，更新profile.yaml，并在logs/revision_log.md记录
```

## 信息不足时的处理

留空，不臆测。`initial_emotional_vector`/`mental_fatigue`等字段如果原文没有明确支撑，直接不写这个字段或写空，不为了"看起来完整"而编造数值。

## 校验

沿用原validate_ceu.py的机械校验精神（必填字段齐全、event_id唯一、profile.yaml引用的event_id真实存在），脚本待重写（见 `scripts/_history/validate_ceu.py` 作为参考起点），当前阶段先人工核对。

## v1.0（本轮新建，2026-07-19）

初始版本，取代CEU_schema.md。核心变化：CEU是"一个证据事件=一条扁平记录"，Event/Turn结构把同一场景里的多个节拍显式组织成时间线（`progress_timeline`），并引入`environmental_force_snapshot`把此前只存在于`context`/`power_context`自由文本里的情境信息（是否有观众、空间距离）结构化，方便后续检索"哪些turn是高压场景"这类查询。`attribution`字段直接内嵌`psych_core`/`literary_technique`的分析产出（原CEU schema v0.7新增的字段），不再是CEU的独立字段，而是turn的可选子结构。
