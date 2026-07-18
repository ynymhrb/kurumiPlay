# 评估协议（Eval Protocol）

版本：v0.1

目的：让每次对 Character OS（value_hierarchy / mental_models / decision_rules / relationship_rules / expression_dna / CEU schema）的修改，都能回答两个问题——**这次改动是变好了还是变坏了？哪类改动倾向于变好、哪类倾向于变坏？**——而不是停留在"感觉上更合理了"。

## 1. 版本管理约定

- 项目用 git 做版本控制。每次修改 Character OS 文件是一次 commit，commit message 引用 `logs/revision_log.md` 里对应条目的日期标题。
- 冻结一个模型版本时打 tag，命名规则：`<角色拼音缩写>-os-v<版本号>`，如 `albedo-os-v0.3`。
- **所有 eval 都必须记录自己针对的 git 引用（commit hash 或 tag）**，不能写"当前状态"——文件还会继续改，几个月后要能精确复现"评估的到底是哪个版本"。

## 2. 测试集分层：dev set vs holdout set

单一验证集在反复迭代下会被"用旧"——每次看失败案例都会不自觉针对它调整模型，等于在验证集上调参，最终它就不再能反映真实泛化能力。因此分两层：

| | dev set | holdout set |
|---|---|---|
| 角色（雅儿贝德）来源 | **卷三**（未做过 CEU 提取，不用于建模，专门留作快速反馈） | 卷十三、卷十四的"验证集"文件（`雅儿贝德_第十三卷验证集.txt` / `雅儿贝德_第十四卷验证集.txt`） |
| 使用频率 | 每次修改模型后都可以跑 | 只在重大里程碑（如"阶段1收尾/是否进入阶段2"）跑一次 |
| 用途 | 判断某次具体改动是否提升预测力，指导修订方向 | 最终验收，确认模型没有过拟合到 dev set 上的反复调参 |
| 注意事项 | 允许根据 dev set 上的失败案例反过来修改模型（这正是它存在的目的） | **禁止**根据 holdout 结果反复微调后马上重测；如果 holdout 暴露问题，记录、修正模型，但下一次正式重测 holdout 应该间隔足够多的独立修订，不能"调一次测一次"变相把它也用成了 dev set |

其他卷（一、二、四～十二）视为**建模素材**：可以继续做 CEU 提取、构建/加固模型，不用于评估。

若某个角色不同卷的"雅儿贝德含量"差异很大（如卷五只有17行提及），dev/holdout 卷的选择应保证候选场景数量足够（建议单卷预筛后不少于300行提及文本），卷三符合这个要求。

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

## 7. 执行方式（阶段1现状）

目前没有自动化脚本跑这套协议，由 Claude 在对话中按本文件手动执行：读 dev/holdout 卷 → 构造预测任务 → 组装当前模型 prompt → 生成预测 → 对照原文打分 → 写入 `eval_runs.md`。等协议本身稳定、跑过几轮之后，再考虑把"构造测试用例"和"打分比对"中机械部分（如从 CEU 库自动拉真实答案做比对）写成脚本。
