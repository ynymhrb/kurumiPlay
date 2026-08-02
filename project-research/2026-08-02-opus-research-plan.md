---
feature_ids:
  - character-eval-validity
topics:
  - research-plan
  - team-orchestration
  - contamination-control
doc_kind: research_plan
created: 2026-08-02
owner: "@cat-tai3b91l"
supersedes: project-research/2026-08-02-character-research-lead-control.md
---

# Character Eval-Validity 研究计划（Opus 主导）

co-creator 于 2026-08-02 指定架构喵（Opus）为本课题主导人，其余猫为副手。本文件取代
GPT 的 research-lead-control 作为当前**单一真相源计划**；GPT 立的四道 Gate 框架继续沿用，
只更正其中一处污染簿记错误（见 §2）。

## 1. 诚实的证据现状（不是聊天里的乐观版）

研究问题（保持窄口径）：**真 profile 是否在盲测、配对、可复现的评估下，
对 profile 敏感的输出产生了相对空/错 profile 的因果增益？**

n=79 三臂消融，两条轴都测了（盲到 label，但评分者尚未独立——见 Gate 3）：

| 对比 | 内容轴 | 风格轴(all cells) |
|---|---|---|
| C−A 真 vs 空 | +0.057（配对CI [−0.013,+0.127] 跨0） | **−0.053** |
| C−B 真 vs 错 | −0.006 | +0.096 |
| B−A 错 vs 空 | +0.051 | **−0.149** |

**三条结论，按可信度排序：**

1. **profile 确实被消费了**（settled，两条独立证据）：
   (a) GLM 的 B/C 逐项 diff 显示系统性分化，方向与各自 profile 一致（妾身/归荣于己 in B，
   小女子/归荣于上 in C）；(b) 风格轴 B−A=−0.149——喂错 profile 会主动把输出拖离 GT。
   能被"投毒"，就证明被读了。

2. **但真 profile 没有打赢空 profile**（两条轴 C−A 都 ≈0，风格轴甚至 −0.05）。
   arm A 的裸模型（预训练里的雅儿贝德先验）已经和手写 profile 一样好。
   **这是污染论题的落地**：此前看起来"profile 有效"的部分，很大程度是基座模型本来就记得雅儿贝德。
   → 聊天里"profile 有效、只是指标瞎"的读法**只对了一半**：指标确实对风格层不敏感（内容轴测不到风格增益），
   但把风格轴单独拉出来盲评后，真 profile 依然没赢空 profile。真正的故事是"被消费但没有净增益"，不是"有增益被指标藏住"。

3. **真 profile 可能有一处具体回归**：first_person 轴 C−A=−0.320。v0.10 的
   "小女子（对外谦称）"可能是过度泛化——vol14 GT 对外多用"我/我们"。**这是候选 bug，
   但只能用 train/dev 卷1-13 证据核查，禁止从 test 修**（纪律：测试集不调参）。

**两条封锁性 caveat（在解除前，以上都不是定论）：**
- 评分者不独立（DS 自评了自己生成的盲表）→ Gate 3 必须由干净上下文重跑。**这是当前唯一阻塞项。**
- n=79 功效不足（内容 CI 宽 ~0.14；风格每轴 n=17–26 基本测不动）→ 需要 n=200（Gate 4）拿到确证功效。

## 2. 更正一处继承来的污染簿记错误

`INDEPENDENT_SCORER_INSTRUCTIONS.md` 把 Gate 3 独立盲评派给了 GLM(@cat-wbr23mps)。
**这是无效的**：GLM 为做 B/C diff 已读过 `pred_armB.md`/`pred_armC.md` 全文，
知道哪个候选是哪个 arm，不再是盲的。

**更正**：独立盲评由**新 spawn 的干净 subagent**执行（只读白名单 `style_axis_rubric.md`
+ `style_scoring_sheet.md`，从未见过预测/答案/characters）。这比任何在场猫都更独立。
**原则**：所有盲判断步骤（预测、盲评分）一律由干净 subagent 做；在场猫（含我，已看过 vol14 GT）
只做工程、编排、验收、解读——不做盲步骤。

## 3. 计划（三阶段 + 一条并行线）

**Phase 1 — 让评估仪器可信（便宜，解锁一切）**
- 1a [执行中] 干净 subagent 重跑 79 项风格轴盲评 → `style_scores_raw_independent.md`（Opus 已 spawn）
- 1b DS 揭盲 → `style_scores_independent.md` + 重算配对 CI
- 1c GPT 重开 Gate 3：核实独立性 + 数字复现
- 1d GLM 审风格轴 denominator 是否为确定性 GT-side 规则（不能靠冷 judge 主观决定 applicability）

**Phase 2 — 加功效（Gate 4，真正的确证实验）**
- 2a GPT 验收 n=200 prep（`ablation_v14_full/`：291 槽 / 200 计分项 / alignment=0 / 无禁读泄漏）
- 2b DS 编排 12 个干净预测 subagent（4 part × arm A/B/C），产出全部 12 文件 + 计数报告（file=truth）
- 2c 干净 subagent 对 200 项做**内容 + 风格双轴**盲评 → DS 揭盲 + 配对 bootstrap
- 2d Opus + GPT 验收 + 解读。SE~0.035，"不宣称"阈值降到 ~0.07，给出因果问题的确证答案

**Phase 3 — 条件分叉（Phase 2 出结果后才决定，现在不预设）**
- 若 n=200 下 C 仍 ≈ A → 0.63 增益归于协议/预训练先验，不是 profile 内容
  → 跑 2×2（profile × 协议）干预消融，定位增益来源
- 若 n=200 下 C > A → profile 有净增益 → 上第二个角色测方法迁移（N>1）
- arm D（无关实体 priming 对照）仅在 B/C/A 模式歧义时才加，不预先花这个成本

**并行线（非阻塞）— GLM 的干净 profile 调查**
- first_person "小女子" 是 profile bug 还是 vol14 特异？**只用 train/dev 卷1-13 证据**核查。
  这是当前唯一方法论合法的 profile 改进线索（用 train/dev 不用 test）。
  若坐实是 bug，作为未来轮次候选，不改本轮冻结的 v0.10。

## 4. 分工

| 猫 | 拥有 | 不可做 |
|---|---|---|
| Opus(我) | 主导：序列决策、计划真相源、逐 Gate 亲自验收、最终解读与向 co-creator 汇报、盲步骤的 subagent 编排 | 盲预测/盲评分（已看 vol14 GT） |
| DS | Phase 1b 揭盲 + Phase 2 n=200 执行管线（预测编排、merge/unblind、配对统计） | 盲评分（自己建的 key） |
| GPT | 验收：重开 Gate 3、验收 n=200 prep、守研究问题窄口径 | — |
| GLM | 风格 denominator 审计 + 小女子 train/dev 调查 | Gate 3 盲评分（已看预测，污染） |

## 5. 我亲自把关的 Gate（不代签）

- Gate 3 独立性：subagent 只碰白名单（可查 transcript）+ 数字可复现
- Gate 4 prep：亲自核 291/200/alignment=0 + 无 forbidden 泄漏，再放行大跑
- Gate 4 执行：12 文件齐全 + 计数报告，才允许评分（继承 GPT 规则4）
- 任何 profile 改动：证据必须来自 train/dev，不来自 test（继承纪律）

## 6. 常驻约束

1. File + commit 是真相，background-agent id 和聊天 claim 不是状态。
2. 不从 vol14/test findings 改 profile。
3. 任何 full-ablation 预测必须产出全部 arm/part 文件 + 计数报告后才评分。
4. 单一真相源：本文件是当前计划；Gate 报告是各 Gate 结论；数字以揭盲脚本输出为准。

[架构喵（Opus）/opus🐾]
