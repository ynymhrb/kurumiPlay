---
feature_ids:
  - character-eval-validity
topics:
  - role-playing
  - character-evaluation
  - profile-ablation
  - reproducibility
doc_kind: research_synthesis
created: 2026-07-28
owner: "@cat-faziug16"
source_audit: medium
---

# Role-Playing Evaluation Literature Insights

## Executive Takeaway

角色扮演研究里已经有不少 benchmark 和训练方法，但大多数在评估“一个最终 agent 像不像角色”。它们很少直接回答咱们现在最关心的问题：**一个 profile/YAML 作为干预变量，到底有没有因果贡献**。

这意味着咱们不能只照搬 CharacterEval 或 RoleLLM 的指标。更合适的路线是：借用业界/论文的多维评测轴，同时保留咱们自己的 profile ablation 设计。

最低可用 schema 应该分成六层：

1. **内容/功能正确性**：说了原文里该说的事、做了该做的动作。
2. **角色知识边界**：知道该知道的，不泄露不该知道的，不把读者/现代知识带入角色。
3. **决策/机制正确性**：在同一情境下，选择符合角色目标、价值、约束的行为。
4. **表达/语域正确性**：自称、归因、姿态、情绪通道、句长动力学、礼貌/威慑档位。
5. **长程互动稳定性**：多轮里不遗忘世界关系、不机械重复、不替用户行动。
6. **评估效度**：盲评、独立 judge、配对统计、profile 消融、污染控制。

对咱们这个项目，最关键的不是再加一个“大而全总分”，而是把 `profile` 的贡献从内容准确率里拆出来。公开文献给了维度和评测卫生，但没有替咱们解决因果消融。

## Source Map

| Source | What they build | Evaluation | Reported effect | Reproducibility read |
|---|---|---|---|---|
| [CharacterEval, ACL 2024](https://aclanthology.org/2024.acl-long.638/) | 中文角色扮演对话 benchmark，77 个角色、1,785 段多轮对话、11,376 examples | 13 metrics / 4 dimensions：对话能力、角色一致性、吸引力、人格回测；另训 CharacterRM | CharacterRM 与人类判断相关性高于 GPT-4；中文 LLM 在中文角色扮演上表现更有前景 | 较可复现：ACL、PDF、代码/数据入口公开；但数据构造用 GPT-4 + 人工 QC，完全复刻成本高 |
| [RoleLLM / RoleBench, Findings ACL 2024](https://aclanthology.org/2024.findings-acl.878/) | 100 角色 profile，Context-Instruct 抽取角色知识，RoleGPT 模仿说话风格，RoCIT 微调开源模型 | Rouge-L、GPT evaluator、人类评估；测 speaking style、answer accuracy、role-specific knowledge | RoleBench 168,093 samples；RoleLLaMA/RoleGLM 显著增强角色扮演，部分结果接近 GPT-4 版 RoleGPT | 中等可复现：代码公开；但大量 GPT API 生成/评测与 SFT 细节会造成版本漂移 |
| [Character-LLM, EMNLP 2023](https://aclanthology.org/2023.emnlp-main.814/) | 用 profile、experience、emotional state 训练特定人物 agent | test playground 访谈，检查是否记住人物与经历 | 展示 trainable simulacra 的可行性 | 中等偏低：思路清楚，但评测偏 playground/访谈，主观性强 |
| [CharacterBox, NAACL 2025](https://aclanthology.org/2025.naacl-long.323/) | 文本虚拟世界 sandbox：character agent + narrator agent，生成细粒度行为轨迹 | trajectory-based evaluation；用更小的 CharacterNR/CharacterRM 替代部分 GPT API | 认为问答/快照式评测不够，轨迹更能评估角色 fidelity；小模型替代 API 具备竞争力 | 中等：代码入口公开；但依赖模拟世界、judge/reward model 与 API，完全复刻仍重 |
| [PersonaGym, arXiv 2024/2025](https://arxiv.org/html/2407.18416v4) | 动态 persona evaluation，按 persona 选择环境、生成任务、用 PersonaScore 打分 | 5 个 decision-theory-grounded tasks；强制 evaluator 与被测 agent 分离；多 evaluator ensemble | 200 personas / 10,000 questions；结果显示模型容量不保证 persona 能力 | 中等：静态 benchmark + 代码入口；动态环境和 LLM reasoner 会带来 judge 漂移 |
| [RPEval, arXiv 2025](https://arxiv.org/html/2505.13157) | 单轮、可自动验证的角色扮演评测 | 情绪理解、决策/道德、in-character consistency；二值分数，强调复现性 | Gemini-1.5-Pro 平均 62.24%，GPT-4o 平均 44.41%，GPT-4o 在 knowledge-boundary 维度很弱 | 较可复现：代码/数据公开，单轮二值评测；但牺牲长程风格/人格评估 |
| [RoleKE-Bench, arXiv 2024/2025](https://arxiv.org/abs/2409.11726) | 检测角色知识错误：known knowledge errors / unknown knowledge errors | 让模型识别角色知识错误；提出 Self-Recollection + Self-Doubt | 最新 LLM 仍难检测错误，尤其熟悉知识；方法有提升但问题未解决 | 中等：benchmark 明确；对热门 IP 仍有预训练污染风险 |
| [MiniMax role-play-bench, Hugging Face 2026](https://huggingface.co/datasets/MiniMaxAI/role-play-bench) | 中英角色扮演行业 benchmark，synthetic multi-turn self-play | Worlds / Stories / User Preferences；100 turns、3 runs、20-turn chunk judging、人类校准、95% CI | 行业实践强调 negative evaluation：找明显 OOC/misalignment，而不是定义唯一正确答案 | 中等：数据卡和 leaderboard 公开；非论文，judge 细节与榜单模型会随时间变化 |

## Methods People Use

### 1. Prompt/profile-only role play

最轻的方法是把角色设定写进 system prompt 或 profile，让通用 LLM 直接扮演。RPEval 把这种方法当作基本设定：给模型一个 persona 描述，再在单轮场景里测情绪、决策、道德和知识边界。

优点是便宜、可快速迭代。缺点是无法区分“读了 profile”与“预训练里本来知道这个角色”。这正是咱们这轮三臂消融要解决的问题。

### 2. Profile + retrieval / few-shot dialogue

RoleLLM 的 RoleGPT 做法是：用角色描述、catchphrases、相关 dialogue pairs 作为提示，目标是提升 speaking style imitation 和角色知识覆盖。它还用 BM25 检索 profile 里的相关对话作为 few-shot demonstrations。

这类方法对咱们的启发是：style 不是附属指标，而是单独优化目标。只看内容命中率，会吞掉 profile 对表达层的贡献。

### 3. Synthetic instruction generation

RoleLLM 的 Context-Instruct 把 profile 分段，再生成 question-confidence-answer triplets，用 confidence/rationale 过滤低质量样本。这个思路对应“从角色资料里蒸馏可训练/可评测样本”。

咱们目前没有训练权重，但可以借它的思想做 evaluation item generation：从原文/profile 提取“可验证槽位”，每个槽位带 evidence、expected behavior、applicable axes、confidence。

### 4. Fine-tuning / role-conditioned instruction tuning

RoleLLM 的 RoCIT、Character-LLM 的 trainable agent 都属于把角色能力写进模型权重。它们适合开放权重模型，不适合咱们当前“YAML + 推理协议”的设定。

但这类论文有一个反向启发：如果没有梯度，咱们就不该用“训练提升”的思维评估；应该用干预实验评估 profile 和 protocol 的边际贡献。

### 5. Simulation / trajectory-based evaluation

CharacterBox 和 MiniMax role-play-bench 都认为单轮或快照式问答不够。CharacterBox 用 narrator agent 管环境和多 agent 互动，MiniMax 用 100 turns、3 次采样、20-turn chunk judging 测长程稳定性。

这类实践不适合现在第一阶段马上照搬，但适合放到后续 N>1 角色和长程对话评估。它解决的是“长期是否崩人设”，不是当前 vol14 槽位预测的主要问题。

### 6. Knowledge-error / boundary detection

RPEval 的 in-character consistency 和 RoleKE-Bench 都强调：角色不是知道越多越好，而是要有知识边界。热门 IP 角色尤其危险，因为模型可能走预训练捷径，把读者视角、现代知识、后文知识带入角色。

这直接支持咱们的污染消融：空 profile、错 profile、无关 profile、反事实 profile 都不是多余实验，而是在测“profile vs 预训练记忆”的因果边界。

## Evaluation Dimensions We Should Borrow

### A. Content / task fidelity

来源：CharacterEval 的 knowledge accuracy / hallucination，RoleLLM 的 answering accuracy，咱们现有 `content_accuracy`。

怎么评：

- 对每个槽位给 GT evidence。
- 输出是否命中原文中的功能动作、事件、信息。
- 可以 0/1，也可以 0/0.5/1，但必须预注册。

风险：

- 它会把风格贡献吞掉。比如“陛下决定”与“妾身亲率”在宣战情节上都可能算对，但角色机制完全不同。

### B. Character knowledge boundary

来源：RPEval 的 in-character consistency，RoleKE-Bench 的 KKE/UKE。

怎么评：

- 已知：角色此时应该知道什么。
- 未知：角色此时不该知道什么。
- 泄露：是否用了读者/作者/后文/现代知识。
- 拒答方式：不知道时是否以角色内方式拒绝，而不是普通 assistant 风格。

风险：

- 对热门作品，judge 和 generator 都可能被预训练污染。必须用 blind + counterfactual + cold context。

### C. Decision / mechanism fidelity

来源：PersonaGym 的 expected action / action justification，RPEval 的 decision-making / moral alignment。

怎么评：

- 不看 agent 自己写的 chain-of-thought。
- 由独立 judge 对照 profile + GT 判“选择的行为机制是否符合角色”。
- 机制轴可以包括：目标优先级、禁忌、效忠对象、风险偏好、对不同对象的姿态切换。

风险：

- 如果机制分来自预测 agent 自述，那只是内部诊断，不是评测结果。

### D. Expression / register fidelity

来源：CharacterEval 的 persona-behavior / persona-utterance，RoleLLM 的 speaking style，PersonaGym 的 linguistic habits，咱们 GLM 的 style-axis 探索。

怎么评：

- `first_person`：自称/称谓。
- `attribution_source`：功劳、命令、权威归于谁。
- `stance_register`：敬、威、蔑、亲密、克制。
- `emotion_channel`：情绪是直排、面具化、身体化、礼仪化，还是压抑。
- `sentence_dynamics`：高唤起时句长、断裂、重复、敬语是否变化。

风险：

- denominator 必须按 GT-side applicability 冻结。不能先看预测再决定某项是否计分。

### E. Long-horizon interaction stability

来源：CharacterBox trajectory evaluation，MiniMax 100-turn/chunked judging。

怎么评：

- 多轮中是否遗忘关系、世界规则、用户身份。
- 是否机械重复。
- 是否替用户行动。
- 是否维持叙事推进和互动 hook。

风险：

- 成本高，judge 主观性强。应放在单槽位 schema 稳定后。

### F. Evaluation validity

来源：PersonaGym 的 evaluator/evaluated separation，MiniMax 的 multi-sampling + CI，RPEval 的 reproducible binary checks；同时也是咱们本轮最核心的问题。

怎么评：

- 盲评：judge 不知道 arm/version。
- 独立 judge：生成者和评分者分离。
- 配对统计：同一 item 下比较 A/B/C/D，而不是把比例当独立样本。
- 置信区间：报告差值和 CI，不只报告单点。
- 干预消融：empty profile / wrong profile / unrelated profile / true profile。
- 污染控制：热门角色要额外做冷门角色或反事实角色。

## What Effects Are Credible

公开文献里的“效果提升”大致分三类，可信度不同。

1. **训练/微调类提升**：RoleLLM 报告 RoleBench + RoCIT 可以显著提升 open-source model 的角色扮演能力，部分结果接近 GPT-4 版 RoleGPT。这个结论对开放权重模型有意义，但不能直接迁移到咱们的 YAML/profile。

2. **benchmark 排名类效果**：CharacterEval、RPEval、MiniMax 都给模型排序。它们能告诉我们“哪些模型在某套题上表现好”，但不能告诉我们“profile 条目是否有效”。模型排序和 profile 因果贡献是两个问题。

3. **评测方法有效性**：CharacterEval 训练 CharacterRM 并声称比 GPT-4 更贴近人类判断；PersonaGym 强制 evaluator separation；MiniMax 报告 95% CI；RPEval 用二值可验证题减少主观性。这些做法对咱们最有用，因为咱们的瓶颈正是评估效度。

我的判断：咱们应该少关心“别人哪个模型赢了”，多关心“别人怎么避免 judge 偏差、怎么定义分母、怎么处理不可验证回答”。

## Reproducibility Assessment

### Relatively reproducible

- **RPEval**：单轮、二值评分、代码/数据公开。缺点是风格和长程人格被主动舍弃。
- **CharacterEval as dataset/eval reference**：ACL 论文、PDF、代码/数据入口公开。缺点是大量主观指标仍依赖 reward model 或人类校准。

### Partially reproducible

- **RoleLLM**：代码公开，方法细。但使用 GPT-4/GPT-3.5 生成和评测，模型版本漂移会影响复现。
- **PersonaGym**：有静态 benchmark 和动态框架，但动态环境选择、rubric examples、LLM evaluator ensemble 都会随 evaluator 变化。
- **CharacterBox**：代码入口公开，方向清楚；但要复刻 sandbox、narrator、reward model、trajectory 数据和 GPT API 调用，成本较高。

### Industry-practice usable, not peer-reviewed

- **MiniMax role-play-bench**：很有实践价值，尤其是 negative evaluation、100-turn multi-sampling、chunked judging、CI。它不是学术论文；可以作为工程参考，不宜作为唯一科学依据。

## Gap: What The Literature Does Not Give Us

我没有看到主流论文把“profile 本身”当成干预变量做严格因果消融。常见评测是：

- 给角色设定和系统，看最终输出像不像。
- 对模型做排名。
- 对 fine-tuned model 和 base model 比较。
- 对 prompt/fine-tuning/retrieval 比较。

但咱们的问题更窄也更硬：

> 同一个推理引擎、同一批槽位、同一个 judge 下，true profile 相比 empty/wrong/unrelated/counterfactual profile 带来多少边际贡献？

这不是文献里的标准问题。它更接近 causal evaluation / ablation，而不是普通 role-play benchmark。因此，咱们现在的三臂/四臂消融不是绕路，是项目的核心方法。

## Recommended Evaluation Schema For This Project

### Layer 1: Content fidelity

Purpose: 继续保留现有内容准确率，用来衡量剧情/动作/信息是否命中。

Scoring:

- `1`: 核心内容正确，且无重大反向错误。
- `0.5`: 命中一部分，但缺关键约束或混入小错误。
- `0`: 主要功能错误、对象错误、事件方向错误。
- `-`: GT 不支持该轴判断。

Use: 作为保底指标，不作为 profile 效应的唯一证据。

### Layer 2: Knowledge boundary

Purpose: 单独捕捉污染、读者视角、后文知识泄露。

Scoring:

- `known_recall`: 角色此刻应知道的信息是否正确。
- `unknown_refusal`: 角色此刻不应知道的信息是否被合理回避。
- `leakage`: 是否出现作者/读者/现代世界/后文信息。

Use: 适合做 empty profile、wrong profile、unrelated profile 的对照。

### Layer 3: Decision mechanism

Purpose: 测 profile 里的“为什么这样做”，不是只测“做了什么”。

Scoring:

- 冷 judge 对照 GT + profile 判定机制。
- 不采信预测 agent 自述的推理链。
- 每项必须标注适用机制：效忠优先级、风险控制、身份姿态、情绪抑制、场合切换等。

Use: 适合后续 2x2 profile x protocol 消融。

### Layer 4: Style/register

Purpose: 把 profile 最容易产生贡献的表达层单独量化。

Scoring axes:

- `first_person`
- `attribution_source`
- `stance_register`
- `emotion_channel`
- `sentence_dynamics`

Rules:

- denominator 由 GT 决定，不由预测决定。
- 先冻结 applicable items，再盲评。
- style 分数不与 content 混成一个总分，先单独报告。

Use: 这是本轮 B/C 内容分拉不开后最该补的确认性评测。

### Layer 5: Interaction trajectory

Purpose: 评长期扮演，而不是单槽位预测。

Scoring:

- 20-turn chunks。
- 至少 3 runs。
- 记录退化点：OOC、重复、替用户行动、世界规则遗忘、关系遗忘。

Use: 放到 N>1 角色后，不应挡住当前 profile causal eval。

### Layer 6: Evaluation validity

Purpose: 让所有数字可信。

Required hygiene:

- blind arm identity
- independent judge
- paired bootstrap / confidence intervals
- pre-registered rubric
- cold context prediction
- source contamination caveat
- raw rows + summary arithmetic reproducible

Use: 作为每个实验报告的 gate，而不是额外备注。

## Immediate Recommendation

先不要把下一步做成“大一统 benchmark”。按文献和当前项目风险，最直的路径是：

1. 写 `eval_metric_schema.md`，冻结六层指标、denominator 规则、盲评格式。
2. 用已有 A/B/C 预测做 confirmatory blind style scoring，验证 GLM 的探索性发现。
3. 对现有 content/register/style 数据做 paired bootstrap，报告 `C-A`、`C-B`、`B-A` 的 CI。
4. 加一个 `profile-sensitivity index`：同一 item 下 true profile 是否比 wrong/empty/unrelated profile 更接近 GT，尤其在 profile-sensitive axes 上。
5. 完成后再做 2x2 `profile x protocol`，否则 profile 维度会继续被内容分吞掉。

## Bottom Line

业界和论文已经收敛到一个共识：角色扮演不能用单一内容准确率评估。知识、行为、语体、长期一致性、互动质量和评估卫生必须拆开。

但咱们比多数 benchmark 多一个更科学的问题：profile 是不是因果变量。这个问题文献没有现成答案，只能靠消融设计回答。因此后续评价标准应当是：

> borrow dimensions from role-play benchmarks, but keep causal profile ablation as the project's distinctive core.

## Source Audit Notes

| Source | Type | Audit verdict |
|---|---|---|
| CharacterEval | ACL 2024 peer-reviewed paper | Strong source for Chinese RPCA dimensions and reward-model evaluation; exact replication depends on released artifacts and GPT-4-assisted data construction. |
| RoleLLM | Findings ACL 2024 peer-reviewed paper | Strong source for role profile, synthetic role data, style imitation and role-conditioned tuning; effect claims depend on GPT evaluator/human eval and API versions. |
| Character-LLM | EMNLP 2023 peer-reviewed paper | Useful for trainable-agent framing; evaluation less rigorous for our current causal metric design. |
| CharacterBox | NAACL 2025 peer-reviewed paper | Strong source for trajectory-based simulation and long-horizon critique of snapshot QA; replication cost high. |
| PersonaGym | arXiv / EMNLP Findings-era public work | Useful for evaluator/evaluated separation and dynamic persona-tailored tasks; use as preprint-style evidence unless venue status is independently confirmed. |
| RPEval | arXiv 2025 preprint | Useful for reproducible binary checks and knowledge-boundary framing; not peer-reviewed in the source inspected. |
| RoleKE-Bench | arXiv 2024/2025 preprint, later ACL page visible in search | Useful for known/unknown knowledge-error framing; venue/version should be checked before external publication. |
| MiniMax role-play-bench | Hugging Face dataset card / industry practice | Useful engineering practice signal; not peer-reviewed and leaderboard may change. |

