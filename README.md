# 小说人物蒸馏项目

## 目标

不是生成"人物简介"，而是构建一个**可运行的人物认知模型**：

1. **SFT训练集** — 训练模型输出符合人物三观、气质、语言习惯的回答
2. **RAG知识库** — 查询人物事实、经历、关系
3. **RolePlay Agent** — 在新场景中生成符合人物逻辑的行为

核心理念：小说人物蒸馏的目标不是写一份"这个人物是什么样的人"的简介，而是**提取决定人物言行的深层特征**——价值观、追求、所处环境、人物关系、年龄段、品格等——用这些特征去驱动、模拟人物在新场景下会说什么、会做什么，而不是死记她说过的话、做过的选择本身。

## 本项目即 Skill

整个项目本身就是一个 Claude Code Skill（根目录 `SKILL.md` 为入口），支持两种任务：

- **角色蒸馏**（训练侧）：开新角色/新轮次、逐卷提取事件、归因、更新profile、dev评估、日志与版本管理，产出存放在 `characters/<角色>/` 下
- **言行预测**（推理侧）：加载 `characters/<角色>/V<最新轮次>/profile.yaml`，走"定观众→存量优先→语域选档"强制三步协议，做盲测填充/新场景RolePlay生成/derivability audit

## 核心架构（V2.0，CSE认知仿真引擎设计）

```
原文
 ↓
静态特质模型（profile.yaml）              动态事件/时间线（events/<卷>.yaml）
 - 信念体系/价值排序/决策规则              - 事件初始动态快照（情绪/意图）
 - 依恋模式/关系图谱/语言风格指纹          - 逐轮次时间线（言行+环境情境快照）
 - 深层心理机制（psychological_structure）  - 归因分析（attribution，触发时才做）
       ↑__________________互相反馈__________________↓
              （事件驱动特质模型迭代，特质模型指导事件解读）
 ↓
Generation（两段式：先按心理内核生成写实反应，再判断是否套用已积累的文学化手法）
```

关键洞察：人物核心不是"她做过什么选择"的行为记录，而是**驱动这些言行的深层特征组合**。事件时间线里的具体言行只是这些特征的外显证据，不是特征本身——提取的目标是特征本身，事件记录只是用来反推特征的原材料。

**静态与动态分离**：长期固化的特质（信念、价值观、依恋模式）存在`profile.yaml`，随事件证据积累缓慢迭代；情绪、瞬时意图这类会在单次事件/对话内变化的状态，只存在事件的时间线结构里，不污染静态模型。

**推理/追溯双文件分离（v0.8起）**：`profile.yaml`只保留推理用的行为逻辑（简洁），证据链/置信度/来源史/变更记录全部放`profile_trace.yaml`——追溯内容混进推理文件会稀释注意力。

**心理轴优先于文学轴**：分析一段言行时，先假设这是一个真人，用心理学工具箱（依恋理论/认知失调/防御机制/代理人状态等，见`spec/attribution_framework.md`）走完四层归因；只有心理轴本身解释不了（行为超出真人物理极限、或动机逻辑跳跃过大）时，才认为是作者的文学化包装，这部分单独记录为可复用的"文学手法"（`literary_techniques.md`），不代表角色的字面行为倾向。

**矛盾即信号，不是终点**：观察到言行前后不一致时，不满足于"记录下来、不调和"，而是主动寻找能同时解释这些表现的深层心理机制（`psychological_structure_protocol.md`）。找不到机制就诚实标注"证据不足"，不强行编造解释凑数。

**derivability ≠ 可预测（vol13教训）**：模型能事后解释行为（derivability audit 0.93/0.97）不等于推理端能盲测生成对的行为（blind 0.55）。盲测失败先归因到推理端（观众定位/存量调用/语域迁移），再考虑改模型；由此确立`character-predict`的强制三步推理协议。

## 工作方式：自我演进探索

这个项目采用**迭代验证**而非一次性提取：

1. 用已有的静态特质模型（`profile.yaml`）作为**当前假设**
2. 逐卷、逐事件地过新章节，检验假设是否能预测/解释人物的言行
3. 遇到无法解释的行为 → **修正模型本身**，而不是硬凑一个解释（且修正只能是通用属性/简短逻辑，禁止场景级补丁）
4. Schema和方法论本身也随过程迭代（本项目已经历过一次大版本迁移：从CEU单条证据格式 → CSE静态/动态分离架构，见`characters/雅儿贝德/_history/`归档记录）

失败即修改模型，不是修改答案。

## 目录结构

```
character/
├── README.md                            本文件
├── SKILL.md                             Skill入口：角色蒸馏+言行预测两种任务的完整流程
├── spec/
│   ├── character_static_profile_schema.md  静态特质模型 schema（profile.yaml的结构定义）
│   ├── event_schema.md                     动态事件/时间线 schema（events/*.yaml的结构定义）
│   ├── attribution_framework.md            双轴归因分析法（心理轴四层+文学轴两层）
│   ├── psychological_structure_protocol.md 深层心理机制记录方法论（取代"矛盾记录"）
│   ├── expression_dna_protocol.md          语言风格提取方法论（产出speech_register字段）
│   ├── eval_protocol.md                    评估协议：训练轮次版本化、train/dev/test切分、pipeline
│   ├── prediction_protocol.md              言行预测协议：加载纪律、三步推理协议、盲测评分复盘
│   └── _history/                           归档：旧版CEU_schema.md、character_os_template.md
├── scripts/                              自动化脚本（候选场景定位），流程本身按skill文档执行
│   └── _history/                         归档：旧版validate_ceu.py、reconcile_round.py（CEU格式专用）
├── characters/
│   └── 雅儿贝德/                          当前 Gold Character Case
│       ├── source/                       原文分卷文本+盲测验证集（各轮次共用）
│       ├── _history/                     归档的历史训练轮次（V0.1-CEU、V1.0-CEU，已冻结不再修改）
│       └── V2.0/                         当前训练轮次（CSE架构）
│           ├── ROUND_STATUS.md           查询"当前训练阶段做了哪些事"的唯一入口
│           ├── profile.yaml              静态特质模型（推理简洁版，v0.8起）
│           ├── profile_trace.yaml        证据链/置信度/来源史/变更记录（追溯文件）
│           ├── events/                   按卷拆分的动态事件时间线
│           └── literary_techniques.md    文学化反应手法库
└── logs/
    ├── revision_log.md                   模型每次修正的记录（字段级精确到具体子项，含原因）
    ├── construction_log.md               train阶段过程指标（候选场景数/yield_rate/触发的修正数等）
    ├── eval_runs.md                      正式dev/test评分记录
    ├── schema_gaps.md                    schema 待复核信号池
    └── predictions/                      dev derivability audit报告 + test盲测预测/评分报告
```

**每次重新训练（规范/schema有实质变化）新建一个 `V<版本号>/` 目录**，旧版本冻结后归档到`_history/`，`source/` 原文不按轮次重复存储。

## 当前状态

雅儿贝德（Albedo）是当前唯一的 Gold Character Case，进度详见 `characters/雅儿贝德/V2.0/ROUND_STATUS.md`（**查询"做了哪些事"只看这一个文件**，本节只做顶层摘要）。

**albedo-round-v2.0** 已完成 train（卷六~十，16事件/57turn，profile v0.1→v0.6）、dev（卷十一~十二，derivability 0.93/0.97）、test 首轮盲测（卷十三，0.55，方法论级发现：derivability必要非充分）。当前 profile v0.8（推理简洁版+trace分离）。

下一步（可选）：卷十四盲测，检验 v0.8 + 三步推理协议的实际增益。
