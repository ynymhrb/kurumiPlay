# 模型修正记录

每次因 Fidelity Test 或逐章验证发现模型无法解释的行为而做出修正时，在此记录。**这是回答"每个字段为什么加/删/改"的地方，`<修正对象>` 必须精确到具体子项**（如"value_hierarchy 第1层拆分"、"MM6 改名"、"decision_rule #2 补充例外"），不能只写"某文件改了"——写"某文件改了"等于没有回答"为什么"。

格式（v0.1 起新增 change_type / eval_before / eval_after / delta，v1.0 起新增 round，评估协议见 `../spec/eval_protocol.md`）：

```
## <日期> — <修正对象：精确到具体子项，如"MM6改名"/"value_hierarchy第1层拆分"/"decision_rule #2加例外">
触发: 哪个 CEU / 哪次盲测暴露的问题
修正前: ...
修正后: ...
原因: ...
change_type: 字段新增 / 层级拆分 / 候选模型新增 / 范围限定 / 重命名精确化 / 证据分级
round: 所属训练轮次（如 v1.0），见 eval_protocol.md 第0节
eval_before: <eval_runs.md 或 construction_log.md 的 id，改动前最近一次同测试集/同卷内自测分数>
eval_after: <改动后重跑同测试集的 id>
delta: <predictive_accuracy 变化，如 +0.08>
git_ref: <这次修正对应的 commit hash>
```

以下4条历史记录早于本评估协议（2026-07-18 引入）且属于 `albedo-round-v0.1`，无 eval 数据，标注 `predates eval harness`，不做补录。

## 2026-07-18 — seed_fragments标记superseded；value_hierarchy第3/5层移除无效引用

触发：用户要求正式开启 albedo-round-v1.0，需要对 V0.1 遗留内容做一次一致性核对。`seed_fragments.yaml` 3条（YLDB-SEED-001~003）全部 `confidence: low` 且 `evidence` 字段写的是"前期讨论摘要，未标注原文出处"，不满足 CEU_schema.md 的证据可溯源要求，此前 value_hierarchy.md 里已标注这3条"待定位或废弃"但一直没有正式处理。

修正前：`seed_fragments.yaml` 无 status 标记，仍被 `value_hierarchy.md` 第2/3/5层列为支撑证据（YLDB-SEED-001/002/003）。

修正后：`seed_fragments.yaml` 顶部标记 `status: superseded`，文件保留（可追溯）但今后不再作为 Character OS 推导依据；`value_hierarchy.md` 移除对这3条的引用，第2层保留 P-002/B-001 两条有效证据不受影响，第3、5层因唯一支撑证据被移除，改为标注"无正式CEU支撑，待卷一~十新证据重新坐实"。

原因：轮次切换（V0.1→V1.0）时不应该把无出处的种子数据继续当作既定结论使用；`raw_text`/`evidence` 字段存在的意义就是保证证据可溯源，seed_fragments 从建立时起就不满足这个要求，属于历史遗留的方法论漏洞，本轮切换是清理它的自然时机。

change_type: 证据分级
round: v1.0
eval_before: 无（train阶段尚未开始正式eval，本条修正不涉及预测力评分变化，纯粹是证据有效性清理）
eval_after: 不适用
delta: 不适用
git_ref: 3696fc1

## 2026-07-18 — mental_models.md MM1 背景脚注（爱的设定来源）

触发：albedo-round-v1.0 首个正式batch，处理卷一 cluster A（第346-438行）时定位到 YLDB-V1-A-001——游戏结束前飞鼠翻看雅儿贝德角色设定、删除"贱人"字样并新增"如今爱着飞鼠"的原始场景。此前 MM1 的背景脚注只引用卷二安兹事后回忆的转述（第166行），现在有了第一手原文实锤。

修正前：MM1 背景脚注仅引用卷二第166行的转述性描述，未提及原设定含"贱人"字样、也未提及这是即兴非深思熟虑的决定。

修正后：脚注更新为引用 YLDB-V1-A-001（卷一第383-418行）作为主要依据，补充"贬损字样被一并删除"和"事后感到害羞"两个细节，并注明该CEU本身触发了 schema_gap（她此时无自主意识，不是"她的选择"，evidence_source三分类都不完全贴切）。

原因：一手原始场景比事后转述信息量更大、更可靠，且这条证据本身暴露了 schema 的一个盲区（起源类证据不完全适配当前分类），值得在脚注里显式记录，方便以后 schema 复核时能追溯到具体案例。

change_type: 证据分级
round: v1.0
eval_before: 无（train阶段卷一首个batch，尚无卷内自测基线）
eval_after: 不适用（本条不是对预测力的修正，是补充/精化已有背景注脚，不改变模型的预测性结论）
delta: 不适用
git_ref: 3696fc1

## 2026-07-18 — expression_dna.md v0.1→v0.2；mental_models/contradictions方法论新增三重验证与矛盾三分类

触发：用户提供外部参考`nuwa-skill`项目的`extraction-framework.md`，要求参考其方法论补充expression_dna.md并把规则并入当前流程。

修正前：
1. `expression_dna.md` 是纯占位（v0.1，无实际内容，四个维度全部"待提取"）
2. `mental_models.md` 的候选模型转正没有明确标准，MM5/MM7当前是"候选"但缺少可检验的判断依据
3. `contradictions.md` 只有一条记录（张力1），没有分类体系，矛盾类型全部混在一起处理

修正后：
1. 新增 `spec/expression_dna_protocol.md`（句式指纹/风格标签/禁忌词口癖的量化方法，按场合拆分统计，样本不足显式标注），`expression_dna.md` 升级到 v0.2，用现有CEU库里的5条真实台词做了首次实际分析（按公务/私密场合对比职衔自我援引、句式结构、语气词），产出候选口癖2条（反问句式化解质疑；援引官方职衔为行动背书）
2. `character_os_template.md` 新增 Mental Model 三重验证标准（跨场景复现/有生成力/有排他性），只过1重的降级为候选不写入正式结论
3. `contradictions.md` 记录格式新增"类型"字段（时间性/领域性/本质性），张力1回溯分类为"领域性矛盾"；新增"观察项1"记录expression_dna分析中发现的"喔"语气词场合区分度不明显的现象，暂不升级为矛盾
4. `character_os_template.md` 新增"信息不足时的处理"通用规则和"轮次冻结前自检清单"
5. `eval_protocol.md` 第7节pipeline新增独立的"expression_dna更新"步骤（此前完全没有这一步，是明显的流程缺口）

原因：expression_dna.md此前是全项目最薄弱的文件，且没有可执行的提取方法——只写"待提取"不会自动变成有内容，需要像CEU抽取一样有明确的、可重复执行的流程。三重验证和矛盾分类同样是采纳外部方法论后发现能直接补上当前流程里"候选模型什么时候能转正"和"矛盾要不要调和"这两个此前一直靠主观判断的空白。

change_type: 字段新增
round: v1.0
eval_before: 不适用（方法论/文档新增，非预测力相关修正）
eval_after: 不适用
delta: 不适用
git_ref: 1edb72f

## 2026-07-18 — mental_models.md MM1三重验证转正；value_hierarchy第1层、relationship_rules"安兹"行新增证据

触发：正式开始训练（用户批准），处理卷一cluster B（第492-522行，有效内容492-507行）——世界转移瞬间，服务器未如期关闭，雅儿贝德以自主意识第一次出声关切飞鼠，产出 YLDB-V1-B-001。这是继cluster A（她被设定"爱安兹"）之后的直接续篇：她自主意识觉醒的第一个动作就是关切飞鼠。

修正前：
1. `mental_models.md` MM1 没有三重验证标注，最早支撑证据是卷二的CEU
2. `value_hierarchy.md` 第1层只有卷二的G-001/G-002两条证据
3. `relationship_rules.md` "安兹"行的支撑CEU列表没有卷一的证据

修正后：
1. MM1 标注"三重验证：3/3，已转正"，新增"起源实锤"小节引用YLDB-V1-B-001，说明这是目前最早、最直接的证据（她有意识存在的第一个动作就体现MM1，不是"学会"的）
2. value_hierarchy第1层新增YLDB-V1-B-001为第一条列出的证据（比G-001/G-002更直接：关切安兹本人的状态，而非空间/气味等象征物）
3. relationship_rules"安兹"行新增YLDB-V1-A-001、YLDB-V1-B-001，标注为"关系起源"/"关系起点"

原因：跨轮次/跨卷的独立证据是三重验证里"跨场景复现"这一条的核心要求，卷一这两条证据（A+B）不仅数量上增强了MM1，且时间线上比所有卷二证据都更早、更根本——这正是`character_os_template.md`要求的"每个MM标注满足几重验证"的第一次实际应用。

change_type: 证据分级
round: v1.0
eval_before: 无（尚未开始卷内自测/正式eval，卷一才处理2个cluster）
eval_after: 不适用
delta: 不适用
git_ref: a112726

## 2026-07-18 — mental_models MM1自我归责细化+MM5潜在细化；contradictions观察项2；decision_rules规则7候选；expression_dna三分类重构

触发：处理卷一cluster C（第592-833行），产出 YLDB-V1-C-001（反复关切+对无关自己的问题主动请罪）、YLDB-V1-C-002（安兹以"测试"名义请求身体接触，她欣然应允并主动升级，安兹喊停后瞬间切回职责模式）。

修正前：
1. `mental_models.md` MM1 只到"关切"层次，没有"默认归责自己"这一层；MM5没有考虑"安兹在场但非竞争场合"这类情况
2. `contradictions.md` 只有1条张力+1条观察项
3. `decision_rules.md` 只有6条规则，没有命令复诵相关的规则
4. `expression_dna.md` 只有"公务/私密"二分类，n=5

修正后：
1. MM1新增"自我归责细化"小节（C-001支撑）：安兹的任何负面状态默认是自己的责任，即使客观无关；MM5新增"潜在细化"小节（C-002支撑）：安兹在场但非竞争场合时她并不表现出克制，提示"是否有观众"可能不如"安兹是否明确表态"更根本，暂不改动MM5正式表述
2. contradictions.md新增"观察项2"，指出C-002正是此前张力1"待观察"部分预警的反例类型，与观察项1并列跟踪
3. decision_rules.md新增候选规则7"接到命令逐字复诵确认"（C-002支撑，1个场景）
4. expression_dna.md v0.2→v0.3：语料从5条增至15条，发现原有"公务/私密"二分类不够用，拆出第三类"安兹在场一对一场合"（n=10，目前语料最多的一类），重新做了三分类的句式指纹对比；同时发现候选口癖"主动自我归责"（C-001+C-002两个场景，接近转正门槛）

原因：这一批CEU信息量很大，同时触动了mental_models、contradictions、decision_rules、expression_dna四个文件——没有拆成4条零散记录，是因为它们都源自同一批新证据、且互相引用（C-002既是MM5细化的证据，也是contradictions观察项2的证据，也是expression_dna新场合分类的证据），拆开记录反而会掩盖这些发现是同一批数据的不同侧面这件事。C-002本身还触发了一个schema_gap（"无冲突"本身值得记录，但value_conflict字段名装不下这个发现），已记入schema_gaps.md。

change_type: 候选模型新增
round: v1.0
eval_before: 无（卷一才处理到cluster C，尚无卷内自测基线）
eval_after: 不适用
delta: 不适用
git_ref: （待commit回填）

## 2026-07-17 — CEU schema v0.1 → v0.2

触发：雅儿贝德测试中发现仅用 emotion/action/belief 字段不足以支撑 Value Hierarchy 推导（"雅儿贝德嫉妒夏提雅"信息量不够）。

修正前：CEU 只含 emotion / action / belief。

修正后：新增 value_conflict / chosen_value / sacrificed_value 字段，并补充 relationship_context / power_context。

原因：人物核心不是情绪，而是情绪背后的价值排序；同样行为面对不同权力关系对象时意义不同。

## 2026-07-17 — CEU schema v0.2 → v0.3，且提取流程改为"两遍法"

触发：用户发现我提取的CEU有明显遗漏，且认为应该先给ChatGPT原文而非格式化后的结构化内容，避免过早格式化丢失信息。

修正前：直接读场景→凭印象挑1-2个"戏剧化"冲突时刻→直接写成结构化CEU，跳过的行不留痕迹；对外展示时只给格式化后的CEU，不给原文。

修正后：
1. schema新增 `raw_text` 字段，结构化字段一律从原文派生，原文本身先于任何格式判断被固定下来；
2. 提取流程改为两遍：第一遍机械列出候选场景里所有"她说了/做了什么"的节拍（宁可过度收录），第二遍才逐条判断是否构成CEU，跳过的要写跳过原因；
3. 对外交叉验证（如给ChatGPT核对）时，先给原文让对方独立提取，再比较双方结果，而不是只给我筛选后的结论。

原因：检索方式（按人名grep定位候选区域）和筛选方式（一遍读完就下判断、门槛偏高、跳过不留痕）两方面都可能导致漏判；格式化过早会让丢失的信息无法被追溯，也让外部审查者只能审查我的结论而非我的取舍过程。

## 2026-07-17 — 新增候选模型 MM5（表演性得体）、MM6（幻想化的爱）

触发：处理完cluster D（娜贝拉尔通讯）和cluster G（迪米乌哥斯找她）后，发现两个独立场景都显示——
安兹不在场/不知情、且无政治对手观众时，雅儿贝德会情绪失控（YLDB-V2-D-003）或沉溺于不考虑现实
可行性的幻想行为（YLDB-V2-G-002：为不可能存在的孩子做婴儿服）。这与MM3"战略化的爱=不失控"字面
表述矛盾。

修正前：MM3表述为"爱成为战略行动驱动力，情绪不会压过理性行动"，未限定场合。

修正后：MM3补充范围限定——只在有竞争/政治意义的场合成立；新增MM5候选（得体是看观众的表演，
不是恒定人格）、MM6候选（部分行为是无关战略目的的幻想沉溺，与MM3并存而非取代）。

原因：目前只有D、G两个独立场景支持"看场合切换"这个假设，强度中等，暂不视为对MM3的推翻，
而是加范围限定+提出候选模型，记入contradictions.md持续观察，卷2剩余章节和未来卷若出现
反例（如安兹在场时仍失控，或私密场合仍严格克制）会削弱这个假设，需要重新评估。

## 2026-07-18 — 与ChatGPT交叉分析cluster G后的模型调整

触发：用户让ChatGPT独立分析cluster G原文（只给了G，未给D），对比双方结果。ChatGPT只看到G，
所以没有提到我方基于D+G两个场景连起来发现的"看场合切换"（MM5候选）——这不算它漏判，
是比较条件不对等，暂不认领为"双方独立验证"。但ChatGPT在其他地方给出了更深的分析，值得采纳：

1. 新增CEU schema字段 `evidence_source`（self/others/narrator）：采纳自ChatGPT把"他人对雅儿贝德的
   评价"（如迪米乌哥斯评价她的管理能力）也正式作为一种证据类型的做法。之前这类信息只能靠
   `supplementary_notes`零散处理，现在有了正式字段和"轻量schema"（不强制value_conflict等字段）。
   新增CEU：YLDB-V2-G-004（迪米乌哥斯对她管理能力/军事能力的评价）。

2. Value Hierarchy 第1层拆分：ChatGPT追问"守护安兹卧室这个行为是否真的提升了组织效率"，
   发现答案是否定的，从而推出她真正优先保护的不是"组织利益"而是"安兹本人及其存在的象征物"，
   这两者需要拆开。原第1层"安兹的认可与意志"拆分为新的第1层（安兹本人/象征）和第2层（安兹的意志/真正利益）。

3. MM6改名：原"幻想化的爱"改名为"至尊象征崇拜"（ChatGPT的提法更精确，能同时解释守房间、
   留香、做抱枕三件事，而不只是"婴儿服"这一件事的幻想性质）。

4. 新增MM7"未来投射模型"（完全采纳自ChatGPT）：她会主动构建围绕安兹的未来叙事并让当下行动
   向其靠拢，这对RolePlay生成"你未来想做什么"这类问题有直接指导意义。

原因：独立的第二个分析视角（哪怕只看同一段原文）能发现我自己方法论下没深挖到的角度
（这次是"这个行为是否真的服务于它声称的价值"这层追问），值得建立成常规的交叉验证习惯，
而不是自己关起门来验证自己的模型。
