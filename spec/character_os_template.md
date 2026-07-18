# Character OS 输出模板

每个角色蒸馏完成后应产出以下文件集（对照 `characters/<角色名>/`）：

```
<角色>_Gold_Case/
├── CEU/                    CEU 全集（按卷/章拆分）
├── value_hierarchy.md      价值排序
├── mental_models.md        Mental Models
├── decision_rules.md       Decision Heuristics
├── relationship_rules.md   关系/权力规则
├── expression_dna.md       语言习惯、口癖、修辞特征（用于 SFT 语言风格）
├── contradictions.md       模型无法解释的行为记录
└── fidelity_test.md        用后续卷/盲测数据验证的记录
```

## value_hierarchy.md 结构

- 价值排序列表（从高到低），每条价值附上支撑它的 CEU 编号
- 排序应能解释：当两个价值冲突时，人物选哪个

## mental_models.md 结构

- 每个 Mental Model 一个小节：命名（如 MM1 至尊中心主义）+ 定义 + 支撑 CEU + 常见误读修正（如"爱导致失控"应修正为"爱成为战略行动驱动力"）

## decision_rules.md 结构

- 编号列表的行为启发式（如"先确认至尊意志，再行动"），每条可标注适用场景和例外

## fidelity_test.md 结构

- 冻结当前模型版本号
- 用新卷逐个 CEU 验证：预测是否正确
- 记录预测失败的 CEU、失败原因、触发的模型修正（并同步写入 `logs/revision_log.md`）
- **失败时修改模型，不修改答案**
