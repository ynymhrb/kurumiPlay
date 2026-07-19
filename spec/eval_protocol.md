# 评估协议（Eval Protocol）

版本：v1.1（v1.0→v1.1：§9生成pipeline的TODO占位已被`spec/prediction_protocol.md`正式承接，本节改为指向；其余不变。v1.0为架构迁移：CSE认知仿真引擎设计，取代旧版CEU+多文件Character OS的pipeline）

目的：让每次对角色模型（`profile.yaml` 静态特质 + `events/` 动态事件序列）的修改，都能回答两个问题——**这次改动是变好了还是变坏了？哪类改动倾向于变好、哪类倾向于变坏？**——而不是停留在"感觉上更合理了"。

**架构说明**：本轮（2026-07-19）对整个项目做了一次架构重设计，采纳CSE（认知仿真引擎）思路。旧版CEU+`value_hierarchy.md`/`mental_models.md`/`decision_rules.md`/`relationship_rules.md`/`expression_dna.md`/`contradictions.md`多文件结构已归档到`characters/<角色>/_history/`和`spec/_history/`，不再更新，仅供追溯参考。新架构下没有代码执行环境——所有"引擎""推理""归因"步骤仍由我在对话中人工/按方法论文档执行，不是真实运行的软件系统；量化指标（BLEU、交叉熵损失等）暂不采用，用现有的分类打分法代替，待后续有实际生成场景验证后再考虑升级。

## 0. 训练轮次版本化

"重新训练一个角色"这件事会反复发生（规范/schema 迭代、发现方法论问题等都可能触发），因此需要一个比单个文件的版本号更高一层的"轮次"概念，**用真实目录体现，不是只靠 git 历史反查**：

- **轮次（round）**：形如 `V1.0`、`V2.0`、`V2.1`……小版本号表示同一轮训练内部的修正迭代；大版本号进位表示发起一次新训练轮次——通常意味着规范/schema/方法论有实质变化（本次CEU→CSE架构迁移即为一次大版本进位，从`V1.0`到`V2.0`）。
- **每次开启新轮次，在角色目录下新建一个版本子目录**：`characters/<角色>/V<版本号>/`，存放：
  - `profile.yaml`（静态特质模型，见 `character_static_profile_schema.md`）
  - `events/<卷>.yaml`（动态事件序列，见 `event_schema.md`）
  - `literary_techniques.md`（文学化反应手法库）
  - `ROUND_STATUS.md`（查询"当前轮次做了哪些事"的唯一入口）
  - 旧版本目录冻结后不再修改，直接打开就能看到那一轮的完整状态，不需要 `git show` 或切分支。
- `source/`（原文分卷文本）放在 `characters/<角色>/` 下、**不按轮次重复存储**。
- 已归档的历史轮次（`V0.1-CEU`/`V1.0-CEU`）放在 `characters/<角色>/_history/`，是旧架构下的产出，不再维护，仅供追溯查阅原始分析内容。
- 每个角色每个轮次冻结时打 git tag：`<角色拼音缩写>-round-v<版本号>`，如 `albedo-round-v2.0`。
- `characters/<角色>/V<当前版本>/ROUND_STATUS.md` 是查询"当前轮次做了哪些事"的唯一入口，每处理完一批必须更新。

## 1. 版本管理约定

- 项目用 git 做版本控制。每次修改角色模型文件是一次 commit，commit message 引用 `logs/revision_log.md` 里对应条目的日期标题。
- **所有 eval 都必须记录自己针对的 git 引用（commit hash 或 tag）**，不能写"当前状态"。

## 2. 数据集切分：train / dev / test

按训练/开发/评测切分，比例约 8:1:1（14卷中 10:2:2）：

| | train（构建素材） | dev set | test / holdout set |
|---|---|---|---|
| 卷范围 | 卷一～卷十 | 卷十一、卷十二 | 卷十三、卷十四 |
| 阶段 | 事件提取 + 静态特质模型构建/加固 | 尚未开发 | 最终验收 |
| 用途 | 产出`events/`、迭代`profile.yaml` | 判断某次具体改动是否提升预测力 | 确认模型没有过拟合 |
| 注意事项 | 不用于评估评分 | 允许根据 dev 失败案例反过来改模型 | 禁止"调一次测一次" |

**卷内自测（within-batch holdout）**：处理一卷时，预留该卷最后1-2个场景不喂给静态特质模型更新流程，处理完后跑一次预测任务（第3-4节协议），立即知道这批修改是否提升了预测力。结果记入 `logs/construction_log.md` 的 `within_batch_accuracy` 列。

## 3. 预测任务构造

从 dev/holdout 卷文本中挑场景，但**只给`global_background` + `event_initial_dynamic_matrix` + 触发turn之前的`progress_timeline`**，不给待预测turn的`action_description`/`speech_content`。

被测对象：把当前冻结版本的 `profile.yaml` 组装成一个"角色运行模型" prompt，输入上述上下文，要求输出：

1. 预测的行为方向（她会做什么）
2. 预测这次行为对应`value_hierarchy`里的哪条价值排序
3. （可选）一句符合`speech_register`的台词

## 4. 打分维度（两个独立分数，不合成一个总分）

### 4.1 预测准确率（客观，分类判定）

对照原文真实turn的`action_description`/`speech_content`，逐条判定：**对** / **部分对**（方向对但细节偏差）/ **错**。

`predictive_accuracy = 对的数量 / 总测试用例数`（部分对按 0.5 计入）。

**暂不采用CSE设计文档里的交叉熵损失方案**——该方案要求穷举"该节点所有可能行为分支"并让模型输出校准概率分布，穷举本身是主观判断、LLM输出的概率也不可靠，属于虚假精确度。继续用现有的分类判定法，更诚实地反映当前的评估能力上限。

### 4.2 风格保真度（主观，LLM-as-judge）

对照 `profile.yaml` 的 `speech_register` 已积累的口癖/敬语/措辞特征，给预测台词打 1-5 分。

**暂不采用CSE设计文档里的BLEU_Style方案**——BLEU衡量的是n-gram用词重合度，不是风格保真度，两者不等价，容易产生误导性的高分/低分。继续用LLM-as-judge主观打分。

`style_score` = 该批测试用例的平均分。

## 5. 改动分类（change_type）

`logs/revision_log.md` 每条记录需要打一个标签：

- `字段新增`：schema 新增字段
- `层级拆分`：value_hierarchy 某一层拆分为多层
- `候选机制新增`：新增 psychological_structure 候选（status=open）
- `范围限定`：给已有规则加适用范围或例外
- `重命名精确化`：命名调整但核心机制不变
- `证据分级`：证据强度/类型细分
- `架构迁移`：本次CEU→CSE这类大范围结构调整专用标签

## 6. 记录格式

- `logs/eval_runs.md`：结构化表格，每次 eval 一行（eval_id / date / type / model_ref / test_set / n_cases / predictive_accuracy / style_score / notes）。
- `logs/revision_log.md`：**这是新架构下唯一的字段级可追溯审计入口**，格式不变（触发/修正前/修正后/原因/change_type/round/eval_before/eval_after/delta/git_ref），继续要求精确到具体子项，不能只写"某文件改了"。

## 7. 流程（一个简单的 pipeline，不引入 subagent，不写代码，我在对话中直接执行）

### 阶段A 训练（卷一～十）

1. **候选场景定位**（脚本）：`scripts/locate_candidates.py <角色> <卷号>`，沿用不变（与CEU/Event格式无关，只是grep聚类）
2. **事件提取**（我直接做）：按`event_schema.md`的两遍法，产出`events/<卷>.yaml`；字段套不上时如实留空或走归因分析（第3步），不硬凑
3. **归因分析**（我直接做，可选，仅触发条件满足时）：按`attribution_framework.md`的双轴分析法，产出turn的`attribution`子结构
4. **静态特质模型更新**（我直接做）：新事件是否挑战现有`profile.yaml`（**必须字段级精确**，见`logs/revision_log.md`）；表象矛盾按`psychological_structure_protocol.md`判断是否揭示了深层机制（status=confirmed/open）
5. **speech_register 更新**（我直接做，跟着每卷事件走）：按`expression_dna_protocol.md`补充语料池，更新概率模型的n/p(n)
6. **schema 复核**（我直接做，卷末或信号积累到一定量时）：判断是否需要修改`event_schema.md`/`character_static_profile_schema.md`，无论改不改都要留复核记录（`logs/schema_gaps.md`）
7. **卷内自测**（我直接做，可选）：见第2节
8. **过程指标统计**：汇总写入 `logs/construction_log.md`（见第8节，字段名同步调整，`ceu_extracted`→`events_extracted`等）
9. **收尾**：git commit + 更新 `ROUND_STATUS.md`

### 阶段B 开发（卷十一～十二，尚未开发）/ 阶段C 评测（卷十三～十四，holdout）

同旧协议，不变，只是被测对象换成`profile.yaml`。

## 8. 过程日志：logs/construction_log.md 记录哪些内容

字段基本不变，命名同步调整为事件模型术语：`run_id`/`date`/`round`/`git_ref`/`scope`/`candidate_scenes`/`events_extracted`（原`ceu_extracted`）/`yield_rate`/`skipped_with_reason`/`schema_violations_caught`/`triggered_revisions`/`triggered_structure_updates`（原`triggered_contradictions`，对应psychological_structure的新增/更新）/`within_batch_accuracy`/`cross_validation`/`notes`。

## 9. 生成/预测阶段 pipeline → 见 `spec/prediction_protocol.md`

推理侧正本已独立成文（v1.1起）：加载纪律、第0步事件建模、强制三步推理协议（定观众→存量优先→语域选档）、输出格式、盲测评分与复盘、RolePlay模式，全部见`prediction_protocol.md`。原TODO中的两段式文学加工（写实draft→按p(n)判断是否套用literary_techniques手法）已并入其三步协议的第3步；`attribution_framework.md`"生成阶段如何使用"一节仍是文学化判断的方法论依据。

## 10. 关于CSE设计文档中"暂不实现"的部分（记录以便追溯决策依据）

以下模块保留在CSE原始设计里，但本轮判断为暂不实现，原因见此前的架构评审讨论（`logs/revision_log.md`"架构迁移"条目）：

- **量化评分公式**（BLEU_Style / 交叉熵损失）：虚假精确度问题，继续用分类判定+LLM-as-judge
- **Trunk/Sandbox双轨A/B验证 + ΔScore自动化合并门控**：需要真实可执行的推理引擎和评分系统，当前无代码环境，continue用`logs/schema_gaps.md`的人工复核记录代替
- **decision_logic_tree严格DSL**：改用叙事化规则列表（见`character_static_profile_schema.md`）
- **数值阈值硬编码**（如0.90杏仁核劫持判定线）：没有校准依据，改用归因分析中的定性判断
