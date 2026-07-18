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
│   ├── CEU_schema.md                   CEU 数据结构规范（随迭代升级版本号，含 schema_gap 检测机制）
│   ├── character_os_template.md        Character OS 输出模板
│   └── eval_protocol.md                评估协议：训练轮次版本化、train/dev/test切分、打分标准、简单流程
├── scripts/                            自动化脚本（定位候选场景/校验CEU/轮次切换汇总），流程本身由我按文档手动执行，不用subagent
├── characters/
│   └── 雅儿贝德/                        当前 Gold Character Case
│       ├── source/                     原文分卷文本（各轮次共用，不按轮次重复存储）
│       ├── V0.1/                       历史轮次快照（已冻结，不再修改，对应 git tag albedo-round-v0.1）
│       │   ├── CEU/
│       │   ├── value_hierarchy.md ...  （与V1.0同名文件，是那个时间点的版本）
│       └── V1.0/                       当前训练轮次
│           ├── ROUND_STATUS.md         查询"当前训练阶段做了哪些事"的唯一入口
│           ├── CEU/                    按卷/cluster拆分的 CEU 文件 + 候选场景索引(_index_vol*.yaml)
│           ├── value_hierarchy.md
│           ├── mental_models.md
│           ├── decision_rules.md
│           ├── relationship_rules.md
│           ├── expression_dna.md       语言习惯/口癖，供SFT语言风格训练用（当前最薄弱环节）
│           ├── contradictions.md       模型解释不了的行为，待处理
│           └── fidelity_test.md        dev/test盲测记录
└── logs/
    ├── revision_log.md                 模型每次修正的记录（字段级精确到具体子项，含原因）
    ├── construction_log.md             train阶段过程指标（候选场景数/yield_rate/触发的修正数等）
    ├── eval_runs.md                    正式dev/test评分记录
    └── schema_gaps.md                  CEU schema 待复核信号池
```

**每次重新训练（规范/schema有实质变化）新建一个 `V<版本号>/` 目录**，旧版本冻结不再修改，`source/` 原文不按轮次重复存储（体积大且内容不变）。

## 当前状态

雅儿贝德（Albedo）是当前唯一的 Gold Character Case，进度详见 `characters/雅儿贝德/V1.0/ROUND_STATUS.md`（**查询"做了哪些事"只看这一个文件**，本节只做顶层摘要）。

正处于 **albedo-round-v1.0**：上一轮探索性阶段（`albedo-round-v0.1`，CEU schema v0.1→v0.4、卷二部分CEU、value_hierarchy草稿等）已冻结（快照见 `characters/雅儿贝德/V0.1/`），V1.0 在此基础上继续，不清空重来，冲突时以新规范为准。V1.0 新增了流程基础设施（见 `spec/eval_protocol.md`）：
- 训练轮次版本化（git tag + 按轮次新建目录 `characters/<角色>/V<版本>/` + `ROUND_STATUS.md`）
- 8:1:1 train/dev/test 数据切分（卷一~十 / 卷十一~十二 / 卷十三~十四）
- 字段级可追溯的修正记录（`logs/revision_log.md`）+ 过程指标日志（`logs/construction_log.md`）
- CEU schema 主动检测机制（`schema_gap` 字段 + `logs/schema_gaps.md`）
- 简单的机械脚本（`scripts/`）；判断类步骤（CEU抽取/模型更新/schema复核）由我按 `spec/eval_protocol.md` 记录的流程直接执行，不引入 subagent

下一步：继续跑卷一剩余 cluster 的 CEU 提取。
