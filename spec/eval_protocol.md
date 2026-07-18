# 评估协议（Eval Protocol）

版本：v0.2（新增训练轮次版本化规则、卷内自测层级）

目的：让每次对 Character OS（value_hierarchy / mental_models / decision_rules / relationship_rules / expression_dna / CEU schema）的修改，都能回答两个问题——**这次改动是变好了还是变坏了？哪类改动倾向于变好、哪类倾向于变坏？**——而不是停留在"感觉上更合理了"。

## 0. 训练轮次版本化

"重新训练一个角色"这件事会反复发生（规范/schema 迭代、发现方法论问题等都可能触发），因此需要一个比单个文件的版本号更高一层的"轮次"概念，**用真实目录体现，不是只靠 git 历史反查**：

- **轮次（round）**：形如 `V0.1`、`V1.0`、`V1.1`……小版本号（如 V1.0→V1.1）表示同一轮训练内部的修正迭代；大版本号进位（如 V0.x→V1.0）表示发起一次新训练轮次——通常意味着规范/schema/方法论有实质变化。
- **每次开启新轮次，在角色目录下新建一个版本子目录**：`characters/<角色>/V<版本号>/`，存放该轮次的 CEU/、value_hierarchy.md、mental_models.md、decision_rules.md、relationship_rules.md、expression_dna.md、contradictions.md、fidelity_test.md、ROUND_STATUS.md。旧版本目录冻结后不再修改，直接打开就能看到那一轮的完整状态，不需要 `git show` 或切分支。
- `source/`（原文分卷文本）放在 `characters/<角色>/` 下、**不按轮次重复存储**——原文不会变，重复存一份没有意义，只会增加体积。
- 每个角色每个轮次冻结时打 git tag：`<角色拼音缩写>-round-v<版本号>`，如 `albedo-round-v0.1`、`albedo-round-v1.0`，作为目录快照的辅助交叉引用（不是唯一凭证，目录本身才是主要的查阅方式）。
- `characters/<角色>/V<当前版本>/ROUND_STATUS.md` 是查询"当前轮次做了哪些事"的唯一入口，每处理完一批必须更新。

## 1. 版本管理约定

- 项目用 git 做版本控制。每次修改 Character OS 文件是一次 commit，commit message 引用 `logs/revision_log.md` 里对应条目的日期标题。
- 冻结一个模型版本时打 tag，命名规则：`<角色拼音缩写>-os-v<版本号>`，如 `albedo-os-v0.3`。
- **所有 eval 都必须记录自己针对的 git 引用（commit hash 或 tag）**，不能写"当前状态"——文件还会继续改，几个月后要能精确复现"评估的到底是哪个版本"。

## 2. 数据集切分：train / dev / test

按训练/开发/评测切分，比例约 8:1:1（14卷中 10:2:2）：

| | train（构建素材） | dev set | test / holdout set |
|---|---|---|---|
| 卷范围 | 卷一～卷十 | 卷十一、卷十二 | 卷十三、卷十四（`雅儿贝德_第十三卷验证集.txt` / `雅儿贝德_第十四卷验证集.txt`） |
| 阶段 | 当前所处阶段：CEU 提取 + Character OS 构建/加固 | **尚未开发**：待 train 阶段模型基本稳定后启动 | 最终验收 |
| 使用频率 | 持续处理 | dev 阶段启动后，每次修改模型都可以重跑 | 只在重大里程碑（如"阶段1收尾/是否进入阶段2"）跑一次 |
| 用途 | 产出 CEU、迭代 value_hierarchy/mental_models/decision_rules | 判断某次具体改动是否提升预测力，指导修订方向 | 确认模型没有过拟合到 dev 上的反复调参 |
| 注意事项 | 不用于评估评分 | 允许根据 dev 上的失败案例反过来改模型（这正是它存在的目的） | **禁止**根据 test 结果反复微调后马上重测；下一次正式重测 test 应间隔足够多的独立修订，不能"调一次测一次"变相把它也用成了 dev |

**当前所处阶段（v0.2 更新）**：train 阶段（卷一～十）现在有了第三层、比 dev/test 更高频的反馈——**卷内自测（within-batch holdout）**：处理一卷时，预留该卷最后 1-2 个 cluster 不喂给 Character OS 更新流程，处理完后用第3-4节的预测任务协议在这 1-2 个 cluster 上跑一次预测，立即知道这一批修改是否提升了预测力。这层反馈**用完即弃**（每卷用该卷自己预留的部分，不复用），不占用卷十一～十四的 dev/test 额度，结果记入 `logs/construction_log.md` 的 `within_batch_accuracy` 列（而非 `eval_runs.md`，那张表专属 dev/test 正式记录）。dev 阶段（卷十一～十二）的评估流程仍待 train 阶段收敛后启动。train 阶段的过程记录见 `logs/construction_log.md`（第8节）。

## 3. 预测任务构造

从 dev/holdout 卷文本中，按 `CEU_schema.md` 的判断标准挑场景，但**只给 trigger + context（选择发生前的信息），不给 choice/action/speech 之后的内容**。

被测对象：把当前冻结版本的 `value_hierarchy.md + mental_models.md + decision_rules.md + relationship_rules.md` 组装成一个"角色运行模型" prompt，输入 trigger+context，要求输出：

1. 预测的 choice 方向（她会做什么选择）
2. 预测的 `chosen_value` / `sacrificed_value`
3. （可选）一句符合她语言习惯的台词

## 4. 打分维度（两个独立分数，不合成一个总分）

### 4.1 预测准确率（客观）

对照原文真实 CEU 的 choice/chosen_value/sacrificed_value，逐条判定：
- **对**：choice 方向和 chosen_value 都命中
- **部分对**：choice 方向对，但 chosen_value/sacrificed_value 判断有偏差；或反之
- **错**：choice 方向判断错误

`predictive_accuracy = 对的数量 / 总测试用例数`（部分对按 0.5 计入，需在 notes 里注明有几条是部分对）。

### 4.2 风格保真度（主观，LLM-as-judge）

对照 `expression_dna.md` 里已积累的口癖/敬语/措辞特征，给预测台词打 1-5 分：
- 自称/敬语是否符合
- 情绪强度对应的语言变化是否符合场合（战略场合 vs 私密场合，见 MM5）
- 整体语感是否"像她"

`style_score` = 该批测试用例的平均分。**expression_dna.md 目前几乎是空的，这个分数在语料积累前意义有限，先跑起来但不要过度解读，等 expression_dna 有实质内容后再重视这个分数。**

## 5. 改动分类（change_type）

`logs/revision_log.md` 每条记录需要打一个标签，用于后续聚合"什么样的改动倾向于变好/变坏"：

- `字段新增`：CEU schema 新增字段
- `层级拆分`：value_hierarchy 某一层拆分为多层
- `候选模型新增`：新增 Mental Model 候选（MM5/MM6/MM7 这类）
- `范围限定`：给已有模型/规则加适用范围或例外
- `重命名精确化`：模型命名调整但核心机制不变
- `证据分级`：evidence_source 一类的证据强度/类型细分

样本量小的阶段，聚合表只能给方向性参考，不追求统计显著性。

## 6. 记录格式

- `logs/eval_runs.md`：结构化表格，每次 eval 一行（eval_id / date / type / model_ref / test_set / n_cases / predictive_accuracy / style_score / notes）。
- `logs/revision_log.md`：在原有"触发/修正前/修正后/原因"基础上，新增 `change_type` / `eval_before` / `eval_after` / `delta` 字段（引用 eval_runs.md 的 eval_id）。历史的4条修正记录早于本协议，不做补录，标注"predates eval harness"即可。

## 7. 流程（一个简单的 pipeline，不引入 subagent）

流程分两类步骤：能写成确定性脚本的（`scripts/`，机械判断，不需要理解语义），和需要读原文/理解语义的（由我在对话里按下面的步骤直接做，不拆分成独立的 subagent——独立 subagent 会带来上下文隔离和调用开销，对这种需要频繁交叉参考已有模型内容的任务没有必要）：

### 阶段A 训练（卷一～十，当前所处阶段）

1. **候选场景定位**（脚本）：`scripts/locate_candidates.py <角色> <卷号>` 按人名关键词 grep 命中行号，自动聚类成 cluster 草稿，写入 `CEU/_index_vol<N>.yaml`
2. **两遍法抽取**（我直接做）：一遍机械列出候选片段里所有"说了/做了什么"的节拍（宁可过度收录）；二遍逐条判断是否构成 CEU 并按 schema 填字段；字段套不上时写 `schema_gap` 而不是硬凑；产出写入 `CEU/vol<N>_cluster_<ID>.yaml`
3. **Schema 校验**（脚本）：`scripts/validate_ceu.py <角色>`——CEU 必填字段是否齐全、`event_id` 是否唯一、Character OS 文件里引用的 CEU 编号是否真实存在
4. **Character OS 更新**（我直接做）：新 CEU 是否挑战现有 value_hierarchy/mental_models/decision_rules，触发修正（**必须字段级精确**，见 `logs/revision_log.md` 顶部说明）或记入 `contradictions.md`（**必须分类**：时间性/领域性/本质性，见 `character_os_template.md`）；Mental Model 候选转正前过一遍三重验证（跨场景复现/有生成力/有排他性）
5. **expression_dna 更新**（我直接做，不是独立任务，跟着每批CEU走）：新CEU里如果有她本人的直接台词，按 `expression_dna_protocol.md` 补充进语料池，重新跑一遍句式指纹/风格标签统计，样本量不到阈值就明确标"初步观察"
6. **schema 复核**（我直接做，卷末或 `schema_gaps.md` 积累到一定量时）：判断 `schema_gaps.md` 里的信号是否需要真正修改 schema，无论改不改都要留复核记录
7. **卷内自测**（我直接做，可选）：对本卷预留的 1-2 个 cluster 跑预测任务（第3-4节协议），只根据 trigger+context 预测，再对照真实结果打分，记入 `construction_log.md` 的 `within_batch_accuracy`
8. **过程指标统计**：汇总写入 `logs/construction_log.md`（见第8节）
9. **收尾**：git commit（对应本批次改动，引用轮次 tag）+ 更新 `characters/<角色>/V<当前版本>/ROUND_STATUS.md`；冻结轮次时额外过一遍 `character_os_template.md` 的自检清单

### 阶段B 开发（卷十一～十二，尚未开发）

沿用第3-4节定义的预测任务/打分协议，语料换成卷十一、十二。启动条件：阶段A 在卷一～十上跑完、且连续若干卷不再触发 Character OS 的实质性修正（即触发的 revision 数量明显收敛，见 `construction_log.md` 的 `triggered_revisions` 趋势）。启动后由我在对话中手动执行：读 dev 卷 → 构造预测任务 → 组装当前模型 prompt → 生成预测 → 对照原文打分 → 写入 `eval_runs.md`。

### 阶段C 评测（卷十三～十四，holdout）

同阶段B的执行方式，但只在里程碑触发，且过程必须逐条记录进 `eval_runs.md`（type=holdout），不允许像 dev 一样频繁重跑。

## 8. 过程日志：logs/construction_log.md 记录哪些内容

`eval_runs.md` 是面向 dev/test 阶段的**预测力**指标，但当前项目还处在阶段A（构建/训练），需要一套独立的过程日志追踪"构建过程本身是否稳定、是否在收敛"，这是 git commit + revision_log.md 之外的第三类记录。每处理完一批（通常是一个 volume 或若干 cluster）记一条：

- `run_id`：如 `C001`，递增编号
- `date`
- `round`：所属训练轮次（如 `v1.0`），见第0节
- `git_ref`：这批处理对应的 commit hash
- `scope`：处理范围，如"卷三 cluster A-D"
- `candidate_scenes`：一遍法机械列出的候选节拍数（体现"过度收录"这一步是否真的做到位，而非凭印象跳过）
- `ceu_extracted`：二遍法最终构成 CEU 的数量
- `yield_rate`：`ceu_extracted / candidate_scenes`——筛选严格度，可跨卷比较是否漂移（比如后期突然暴涨/暴跌，可能说明判断标准不稳定）
- `skipped_with_reason`：明确记录跳过原因的候选数（防止"静默跳过"，呼应 schema v0.3 引入 raw_text 的初衷）
- `schema_violations_caught`：自动校验环节（第7节步骤3）抓到的字段缺失/引用错误数，修复前的原始计数
- `triggered_revisions`：本批次触发了几条 `revision_log.md` 修正——这个数字随卷数增加是否收敛，是判断"模型是否趋于稳定、能否进入阶段B"的核心信号
- `triggered_contradictions`：本批次新增几条 `contradictions.md` 记录
- `within_batch_accuracy`：本卷预留的 1-2 个 cluster 上跑出的预测准确率（见第2节"当前所处阶段"），格式同 `eval_runs.md` 的 `predictive_accuracy`（对/部分对0.5/错），没跑则留空
- `cross_validation`：是否用了外部交叉验证（如 ChatGPT），采纳了几条建议
- `notes`

**这套日志要回答的问题**：构建过程本身是否健康——`yield_rate` 是否稳定（说明抽取标准一致）、`triggered_revisions` 是否随卷数增加而下降（说明模型渐趋稳定，长期不收敛则可能是 schema 或方法论有系统性问题，需要停下来重新评估而不是继续堆卷）。这和 `eval_runs.md` 互补：一个看"构建过程是否稳定/收敛"，一个看"模型在未见数据上的预测力"，两者都需要但回答的是不同问题，不要混在一张表里。
