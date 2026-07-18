# 小说人物蒸馏项目

## 目标

不是生成"人物简介"，而是构建一个**可运行的人物认知模型**：

1. **SFT训练集** — 训练模型输出符合人物三观、气质、语言习惯的回答
2. **RAG知识库** — 查询人物事实、经历、关系
3. **RolePlay Agent** — 在新场景中生成符合人物逻辑的行为

核心理念：小说人物蒸馏不是提取"这个人物是什么样的人"，而是构建"这个人物面对未知情况时如何选择"的运行模型。

## 核心架构

```
CEU (Character Evidence Unit)
 ↓
Behavior Pattern
 ↓
Value Hierarchy   ← 人物在冲突中保护什么、牺牲什么
 ↓
Mental Model
 ↓
Decision Rules
 ↓
Character Runtime Model
 ↓
Generation
```

关键洞察：人物核心不是情绪标签，而是**情绪背后的价值排序**。现实人物问"他怎么看世界"，小说人物要问"当多个价值冲突时，他如何选择"。

## 工作方式：自我演进探索

这个项目采用**迭代验证**而非一次性提取：

1. 用已有的 Character OS（价值排序 + Mental Models + Decision Rules）作为**当前假设**
2. 逐章、逐 CEU 地过新章节，检验假设是否能预测/解释人物的选择
3. 遇到无法解释的行为 → **修正模型本身**，而不是硬凑一个解释
4. CEU 提取规范和脚本也随过程迭代增厚（如本次雅儿贝德测试中发现需要新增 `value_conflict` / `relationship_context` / `power_context` 字段）

失败即修改模型，不是修改答案。

## 目录结构

```
character/
├── README.md                          本文件
├── spec/
│   ├── CEU_schema.md                   CEU 数据结构规范（随迭代升级版本号）
│   └── character_os_template.md        Character OS 输出模板
├── characters/
│   └── 雅儿贝德/                        当前 Gold Character Case
│       ├── source/                     原文分卷文本（待上传）
│       ├── CEU/                        按卷/章拆分的 CEU 文件
│       ├── value_hierarchy.md
│       ├── mental_models.md
│       ├── decision_rules.md
│       ├── relationship_rules.md
│       ├── contradictions.md           模型解释不了的行为，待处理
│       └── fidelity_test.md            用后续卷盲测的记录
└── logs/
    └── revision_log.md                 模型每次修正的记录（含触发修正的 CEU 和修正原因）
```

## 当前状态

- Yaldabaoth（雅儿贝德）Value Hierarchy v0.2、Mental Models、Decision Heuristics 已有草稿（基于 Overlord 第一卷部分片段，非全文）
- 下一步：拿到《Overlord》全文 txt 后，从第一卷开始逐章跑 CEU 提取，验证/修正现有草稿模型，再用后续卷做盲测
