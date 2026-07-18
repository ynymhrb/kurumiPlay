# 心理结构记录方法论（取代 contradictions.md 的"矛盾记录"模式）

版本：v1.0（本轮新建，2026-07-19）

## 核心转变

旧版`contradictions.md`的原则是"矛盾是人格特征，记录下来但不调和"——这个原则本身是对的（防止选边站、编造调和解释、假装矛盾不存在），但客观效果是把"发现表象矛盾"当成了终点。

新原则：**表象矛盾不是要记录的东西，它只是信号。真正要记录的，是能同时解释看似矛盾的多个行为的那个更深层机制**。找到机制后，"矛盾"本身就消失了——不是被调和/和稀泥，是被真正理解了（比如F-001的"崩溃自裁"和平时"优雅得体"看似矛盾，但一旦理解为"依恋创伤：保护者部分vs流亡者部分"这个机制，两者是同一结构的不同表现，不再是矛盾）。

## 记录位置

`profile.yaml`的`psychological_structure`字段（见`character_static_profile_schema.md`），不再有独立的`contradictions.md`文件。

## 处理流程

```
观察到表象矛盾/行为不一致（触发信号，可能来自 attribution 分析或人工发现）
 ↓
按 attribution_framework.md 的心理学工具箱（依恋理论/IFS人格部分化/认知失调/
拟剧论/防御机制等）尝试寻找能同时解释多个行为的深层机制
 ↓
找到了？
 ├─ 是 → 记录机制本身（mechanism字段），引用曾经"看似矛盾"的行为作为支撑证据
 │        （surface_behaviors字段），status=confirmed（如果有≥2个独立场景支撑）
 │        或 status=open（如果只有1个场景，机制假设本身还需要更多验证）
 └─ 否 → **不强行编造一个机制**。如实记录为status=open，只写观察到的表象行为，
          明确标注"深层机制未确认，证据不足"。等后续有更多证据再回来判断。
```

## 禁止的处理方式（沿用旧版contradictions.md的核心禁令，适用对象改变）

- ~~记录矛盾但不调和~~ → 现在禁止的是：**为了让记录显得"解释完整"，编造一个似是而非的深层机制**，掩盖证据实际不足的事实。status=open这个状态存在的意义就是防止这种造假——允许"我们还不知道"这个诚实状态，不强迫每条观察都要有一个漂亮的心理学解释。
- 禁止选一边忽略另一边（沿用）：机制必须能同时解释被认为矛盾的所有行为，不能只解释一半、对另一半视而不见。
- 禁止把status=open的观察，仅仅因为"已经记录了"就当成confirmed结论使用——生成阶段引用psychological_structure时，必须区分confirmed和open两种置信度。

## 与 mental_models（若沿用）/ decision_rules 的关系

`psychological_structure`记录的是比"信念/决策规则"更底层的驱动机制——不是"她认为什么"（belief_system管这个）、不是"她会怎么选"（decision_rules管这个），而是"是什么心理结构在底层生成这些信念和选择模式"。一个confirmed的psychological_structure条目，可以作为多条decision_rules/belief_system条目共同的解释依据，但不直接替代它们。

## 示例（复用本轮对话已分析的案例）

```yaml
psychological_structure:
  - mechanism: >
      依恋创伤结构（IFS框架）：平时"优雅得体的守护者总管"是保护者部分（manager），
      底下压着携带"被抛弃即毁灭"核心恐惧的流亡者部分（exile）。任何可能被解读为
      "关系将终结"的信号（无论触发者是否有此意图），都可能意外触碰这个锚点，
      导致保护层瞬间失效，表现为迷走神经fawn型应激反应（讨好/自毁式言语）。
    surface_behaviors: [YLDB-EV-V3-xxx（F-001对应的新event_id）]
    status: open   # 目前只有1个场景直接支撑，需要更多卷验证这个机制是否稳定
    evidence: [YLDB-EV-V3-xxx]
```
