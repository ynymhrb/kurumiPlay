# 角色静态特质模型 Schema（Character Static Profile）

版本：v1.0（取代 `spec/_history/CEU_schema.md` 和 `spec/_history/character_os_template.md` 描述的旧版CEU+多文件Character OS结构）

## 定位

这是"认知仿真引擎（CSE）"架构里的模块一·静态部分：存储角色长期固化的本质属性，全局只读/受控更新。与之相对的是"动态状态"（情绪、瞬时意图），只存在于`event_schema.md`定义的事件/轮次结构里，不在这里固化。

物理存储：`characters/<角色>/V<版本>/profile.yaml`，单文件，人工/LLM直接编辑。

## 字段结构

```yaml
entity_id:               # 角色标识符，如 albedo
gender:                  # 性别定位
age_group:                # 年龄段：少年/青年/中年/老年

belief_system:            # 【合并字段】世界观+信仰+人生观。回答"她如何理解世界运行的规则、
                          # 不可动摇的崇拜核心、生存意义的定义"。三者合并是因为对雅儿贝德这类
                          # 角色，"至尊中心主义"这个信念同时是她的世界观、信仰对象和人生意义来源，
                          # 强行拆成三个字段会重复记录同一条证据三次。每条记录标注类型倾向
                          # （偏世界观/偏信仰/偏人生观），但不强制唯一归类。
value_hierarchy:          # 保持独立字段，不合并进belief_system——这是有明确用途的排序结构
                          # （价值冲突时选哪个），不是笼统的信念陈述，结构：从高到低的价值列表，
                          # 每条附支撑证据（event_id）
decision_rules:            # 决策逻辑，叙事化规则列表（不是严格DSL）：编号规则+适用场景+例外，
                          # 延续原decision_rules.md的写法。每条规则可以引用value_hierarchy和
                          # belief_system里的具体条目作为其依据
ultimate_goal:             # 终极目标/驱动力，凌驾于短期利益之上的那一条

attachment_style:          # 依恋模式：安全型/焦虑型/回避型/紊乱型，或"证据不足，暂缺"
culture:                   # 所属文化圈层
customs:                   # 内化的风俗习惯/行为禁忌
preferences:               # 喜好列表
dislikes:                  # 厌恶/排斥列表
birthplace:                # 出生地/原生环境底色

talents:                   # 特长/优势技能/心智长板
weaknesses:                # 弱点/生理或认知短板/应激脆弱点
traits:                    # 【合并字段】性格+品质。回答"稳定的人格侧面是什么"，不区分
                          # "性格维度"和"美德标签"这种边界模糊的二分——两者在实际标注时
                          # 经常无法客观判定该归哪类
trauma:                    # 创伤档案：历史核心应激事件，直接决定特定刺激下的防御激活。
                          # 没有证据支撑就留空，不脑补

relational_graph:          # 关系矩阵，数组，每条：
                          #   target_id: 关系对象
                          #   role_relation: 固化社会关系名称（如"至尊-守护者总管"）
                          #   affinity: 私人亲密度 0.0~1.0（启发式估计，非精确统计）
                          #   professional_trust: 专业信任度 0.0~1.0（新增，拆开private/professional
                          #     两个维度，避免单一affinity数字压扁"同僚+情敌+竞争对手"这类多维关系）
                          #   tension: 竞争/张力度 0.0~1.0（新增，同上原因）
                          #   notes: 自由文本，记录数字表达不了的关系细节（矛盾、演变、开放问题）

speech_register:           # 话语风格指纹，对象：
                          #   first_person: 自称
                          #   honorific_level: 敬语/语体等级，按场合分桶（沿用原expression_dna.md
                          #     的场合三分类方法论）
                          #   catchphrases: 口癖/高频句式数组，每条标注 n（独立出现次数）+
                          #     p_n（采样权重，公式见下方"特征频率概率模型"）+场合分桶

psychological_structure:   # 【新增，取代旧版contradictions.md】记录表象矛盾背后的深层机制
                          # （见 spec/psychological_structure_protocol.md），不是记录矛盾本身。
                          # 每条：
                          #   mechanism: 机制描述（如"依恋创伤：保护者部分vs流亡者部分"）
                          #   surface_behaviors: 曾经表现为矛盾的具体行为（引用event_id），
                          #     现在被这个机制统一解释，不再是"未调和的矛盾"
                          #   status: confirmed（机制已被多条证据支撑）/ open（证据不足，
                          #     暂未确认深层机制，只记录了表象观察，不强行编造解释）
                          #   evidence: 支撑该机制的event_id列表
```

## 特征频率概率模型（沿用自 `expression_dna_protocol.md`，适用于catchphrases和literary_techniques）

```
p(n) = min(0.3 + 0.1 × (n-1), 0.8)
```

按场合分桶计算，n=1也记录（p(1)=30%），不再有"未到门槛不算数"的二元判定。

## 信息不足时的处理

留空即可，不填默认值/先验。生成阶段读到空字段时，应视为"该维度暂无已知偏好，不施加特定约束"，不臆测。

## 修改规则

任何字段的增/删/改都必须先在此文件的"变更记录"落一条说明，才能生效。变更记录格式沿用旧版CEU_schema.md的约定（写明改了什么、为什么），具体触发/修正前/修正后/原因的详细记录写入 `logs/revision_log.md`（保持现有审计纪律，见该文件顶部说明）。

## v0.1（本轮新建，2026-07-19）

初始版本，从旧版CEU_schema.md+character_os_template.md迁移而来，采纳CSE设计文档的静态特质模型思路，但合并了`worldview/values/outlook_on_life/beliefs/qualities/personality`六个边界模糊的字段为`belief_system`+`traits`两个用途更明确的字段（保留`value_hierarchy`独立，因其有明确的冲突排序用途）；`decision_logic_tree`改用叙事化规则列表而非严格DSL（原设计的DSL语法未定义，且当前无代码执行环境，结构化DSL的意义有限）；`relational_graph`从单一affinity/compatibility两个标量扩展为affinity/professional_trust/tension三维度，避免压扁多维关系。
