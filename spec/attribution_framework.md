# 归因分析框架（Attribution Framework）

版本：v0.2（架构迁移：CEU→Event/Turn，本框架现在是CSE架构"模块二·逆向归因引擎"的方法论依据，双轴模型本身不变）

目的：`event_schema.md`里一条`progress_timeline` turn记录了"发生了什么"，但不直接回答"这个turn触发的深层机制是什么，以及原文写出来的具体表现形式里，哪部分是可复用的心理真实、哪部分是作者为了叙事效果加的风格化包装"。这个框架就是用来回答后一个问题的，产出写入turn的`attribution`字段（见`event_schema.md`），分析结论进一步反馈更新`profile.yaml`（静态特质模型，见`character_static_profile_schema.md`）——尤其是`trauma`/`weaknesses`/`decision_rules`/`psychological_structure`这几个字段。

**不是每个turn都要走这个流程**——只在反应幅度看起来超出常理、或者需要判断是否触发`psychological_structure`（深层机制）更新时才启用。多数turn只需要`action_description`/`speech_content`已经足够，不需要这一层分析。

（本框架早期版本v0.1是在旧版CEU schema体系下设计的，产出对应`psych_core`/`literary_technique`字段；v0.2迁移到Event/Turn体系后，四层/两层轴的分析内容完全不变，只是产出的目标字段变了，见文末"输出格式"一节）

## 核心原则

**先假设这是一个真人，把心理轴走完，只有心理轴本身解释不了（"解释赤字"）时，才调用文学轴修正。** 文学轴不是默认的解释来源，是补丁。

**多层分析默认是互补关系，不是竞争关系**——正常情况下不需要用权重取舍。只有当不同层给出的结论方向相反时（不是"侧重点不同"，是"对行为是否反映真实内在状态"这件事本身判断相反），才需要判断取舍，此时按虚构角色默认"心理轴优先于文学轴"来裁决（因为项目目标是提取可用于模拟的深层特征，宁可先假设有心理真实、再确认是否需要打折扣，而不是先假设是噱头）。

## 第一轴：心理维度（先设想为真人，从微观到宏观走四层）

### Layer 1 生物与神经层（Biological & Neurological）
核心提问：行为发生那一秒，身体和神经的"通电状态"是怎样的？

- **杏仁核劫持模型**（Amygdala Hijack）：情绪中枢抢在理智前额叶反应之前接管身体，触发原始躯体化反应。
- **大脑奖励通路**（Dopaminergic Pathway）：特定刺激导致多巴胺（亢奋/期待）、催产素（依恋/归属）暴洪，引发行为失控。
- **多重迷走神经理论**（Polyvagal Theory，Porges）：危机应激顺序——社交沟通 → 战斗/逃跑（Fight/Flight）→ 瘫痪/讨好（Freeze/Fawn）。

### Layer 2 个体心理与认知层（Psychological & Cognitive）
核心提问：过往的"人生档案"给大脑刻下了怎样的"处理算法"？

- **认知失调理论**（Cognitive Dissonance，Festinger）：现实与核心信念冲突时，大脑启动合理化（Rationalization）防御机制，扭曲对现实的解释，而不是放弃信念。
- **精神分析的移情与向攻击者认同**（Transference / Identification with the Aggressor）：适合**单次、被特定情境触发**的即时反应分析（如某个语气/场景意外激活了某种深层反应模式）。
- **依恋理论**（Attachment Theory，Bowlby & Ainsworth）+ **人格部分化模型**（IFS，Richard Schwartz）：适合**贯穿多个CEU、反复出现的稳定人格结构**（如平时得体的"保护者"部分 vs 携带核心恐惧的"流亡者"部分）——一旦某个心理结构被确认跨CEU反复出现，统一用这套"部分"语言持久化记录，不要和移情框架的措辞混用。
- **认知ABC模型**（CBT，Beck）：A（诱发事件）→ B（信念/解读）→ C（行为和情绪结果）——决定行为结果的是B，不是A。

### Layer 3 社会与情境层（Social & Situational）
核心提问：当时当刻，周围的人和环境施加了什么"推拉力"？

- **勒温心理学场论**（Field Theory）：B = f(P, E)，行为是人格与环境场共同作用的结果。环境场引力足够大时，人格变量会被直接压制——这个公式对应`event_schema.md`的`environmental_force_snapshot`字段（situational_pressure/spatial_proxemics）：E变了导致P看起来不一致，但P本身没变，这类情况应该判定为不需要更新`psychological_structure`，只是环境驱动的正常变化。
- **米尔格拉姆代理人状态理论**（Agentic State）：身处严密层级体制、面对合法权威命令时，心智从"自主状态"切换为"权威的工具"，不再对自己的判断负全责——适合解释雅儿贝德"代入维护安兹权威角色"这类行为（对应`profile.yaml`的`decision_rules`）。
- **社会交换理论**（Social Exchange）：社会言行本质是心理收益-成本的计算。

### Layer 4 文化与演化层（Cultural & Evolutionary）
核心提问：物种的"出厂设置"和文化规训是什么？

- **文化维度理论**（Hofstede）：权力距离、集体/个人主义——高权力距离文化下对权威的神化/盲从是被内化的"合理言行"。
- **性选择与亲缘选择理论**（Darwin）：嫉妒、占有欲、向强者低头等日常行为的演化基础，容易过度套用（"just-so story"风险），需要克制使用，只在确实提供背景合理性时引用，不强行牵连。

## 第二轴：文学维度（仅在心理轴出现"解释赤字"时调用）

**触发条件**：心理轴四层走完后，发现行为**超出真人物理极限**，或**动机逻辑跳跃过大**，心理轴无法完整覆盖——这才调用文学轴。

### Layer 5 叙事功能层（Narrative Function）
核心提问：作者是不是为了"推进剧情"或"高效反差"故意而为之？
- 冲突推动：该言行是否为了快速制造误会/激化矛盾？
- 效率原则：篇幅限制下，创作者是否用"降智脑补"跳过了漫长的心理铺垫？

### Layer 6 审美符号层（Aesthetic Semiotics）
核心提问：这是不是某种特定的艺术表达手法或市场标签？
- 角色标签：该言行是否为了强化某个人设标签（如"病娇""狂信徒"）？
- 表现主义视觉夸张：把无形的内心状态外化为极端的躯体动作，是动漫/轻小说常见的视觉化放大技法。

## 输出格式：三段式归因报告

```
1. 判定结论：心理完全闭环 / 心理燃料+文学外壳
2. 主线解码（心理轴）：层层递进说明内部精神动力
3. 修正解码（文学轴，仅"心理燃料+文学外壳"时需要）：指出外在夸张表现的艺术根源，
   并明确切分——哪部分是可迁移的心理内核，哪部分是不可字面复用的风格化外壳
```

对应Event/Turn的`attribution`子结构（见`event_schema.md`）：
- `psychological_layers` ← 心理轴四层的分析记录
- `explanation_deficit` + `literary_axis` ← 是否触发文学轴+文学轴分析（仅触发时填写）
- `judgment` ← 心理完全闭环 / 心理燃料+文学外壳
- `profile_updates_suggested` ← 这次分析对`profile.yaml`哪些字段（`trauma`/`weaknesses`/`decision_rules`/
  `psychological_structure`等）建议做什么修改，实际修改需要走`logs/revision_log.md`的审计记录

如果判定命中"心理燃料+文学外壳"，风格化的部分（文学轴内容）应沉淀进`profile.yaml`的`speech_register`
或专门的`literary_techniques.md`手法库（沿用原`reaction_stylization.md`的设计，改名迁移），可复用的
频率标注用`character_static_profile_schema.md`的"特征频率概率模型"。

如果这次分析揭示了一个能同时解释多条turn的深层机制（而不只是单条turn的解读），应该走
`psychological_structure_protocol.md`的流程，判断是否新增/更新`profile.yaml`的`psychological_structure`条目。

## 生成阶段如何使用（详见 `eval_protocol.md` 生成pipeline章节）

文学手法不是提取阶段就该丢弃的噪音，是可复用的风格化手法。生成新场景反应时：
1. 先用心理轴分析结论生成写实反应
2. 再判断是否要套用已积累的文学手法做风格化加工（判断标准见 `eval_protocol.md`，目前是TODO占位）
3. 套用与否按该手法的场合概率抽样决定，不是非黑即白（概率模型见 `character_static_profile_schema.md` "特征频率概率模型"）

## 示例（本轮对话实际分析结果，产出于旧CEU体系，方法论不变，仅供参考四层/两层分析怎么写）

| 案例 | 判定 | 心理轴主线 | 文学轴（如适用） |
|---|---|---|---|
| "爱"字触发失控撞天花板 | 心理燃料+文学外壳 | 情感锚点（"爱"）被击中→杏仁核劫持式狂喜→短暂失神呢喃 | 表现主义外化（撞天花板），强化"病娇"标签 |
| 发现安兹失误后自我说服 | 心理完全闭环 | 认知失调+合理化防御，保护"安兹绝对英明"这一核心信念 | 不适用 |
| 起源话题表态vs私下嫉妒 | 心理完全闭环 | 身份建构/自我说服，主动树立的信念尚未完全覆盖底层情绪 | 不适用 |
| 被抛弃恐惧崩溃自裁提议 | 心理完全闭环 | 依恋创伤结构（IFS：保护者/流亡者）+fawn型应激反应，四层从演化到神经完整闭环 | 不适用 |
