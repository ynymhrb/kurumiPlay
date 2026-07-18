# 雅儿贝德 — 训练轮次状态

**这是回答"当前训练阶段做了哪些事"的唯一入口。** 想知道细节再去查 `logs/construction_log.md`（过程指标）/ `logs/revision_log.md`（每条修正的原因）/ `logs/eval_runs.md`（正式dev/test评分）/ `logs/schema_gaps.md`（schema待复核信号），但"现在做到哪了"只看这一个文件就够。每处理完一个 batch 必须更新本文件。

## 当前轮次：albedo-round-v1.0（进行中）

- 上一轮 `albedo-round-v0.1` 已冻结（tag，对应 commit `c75ad0f`）：探索性阶段产出，卷二部分CEU、value_hierarchy v0.3等草稿
- V1.0 不是推倒重来：V0.1 内容作为起点/候选证据保留，冲突时以新规范为准。已完成的衔接工作：
  - `seed_fragments.yaml` 3条标记 `superseded`（无原文出处，不满足证据可溯源要求）
  - `vol2_ch01_early.yaml` 修复了一处 YAML 结构错误（导致 YLDB-V2-B-001 此前无法被机械读取，虽然人工阅读时能看到）
  - `python3 scripts/validate_ceu.py 雅儿贝德` 全库校验通过（0 error）

## 数据集切分（8:1:1，见 `spec/eval_protocol.md` 第2节）

- train（构建素材）：卷一～卷十
- dev（尚未开发）：卷十一、卷十二
- test/holdout：卷十三、卷十四验证集

## 卷处理进度

| 卷 | 状态 | 说明 |
|---|---|---|
| 卷一 | **已完成（19/19）+ schema复核已完成并commit** | 全部cluster处理完，约21条CEU。压轴S-001/S-002：她本人拒绝"起源决定真实性"，新增MM8候选"双重人格层次"。schema复核：3条信号中1条触发修改（value_conflict新增"已核实无冲突"写法，v0.5→v0.6），2条判断暂不需要改动。已commit（`61c333f`），下一步进入卷二复核 |
| 卷二 | **V0.1遗留，复核完成（确认兼容，无需调整）** | 9/11 cluster 有CEU（V0.1产出）。复核结论：raw_text/value_conflict/evidence_source均已合规，且MM3/MM5/MM6/MM7、relationship_rules均已实际引用vol2证据，不是"未整合的孤立数据"。cluster A(partial)确认无遗漏；cluster K（夏提雅造反伏笔）标记open_hook，留给卷三/四她本人反应场景时补CEU |
| 卷三～十 | 未开始，下一步是卷三 | |
| 卷十一～十二（dev） | 未启动 | 待train阶段收敛 |
| 卷十三～十四（test） | 未启动 | 仅里程碑触发 |

## 当前 Character OS 文件版本

- `value_hierarchy.md`：v0.3（第3/5层因移除seed引用暂列"待验证假设"）
- `mental_models.md`：v0.2（MM1已回填三重验证标注3/3已转正+"起源不重要"声明；MM5多轮验证基本稳定；新增MM8候选"双重人格层次"；MM2/MM4/MM6/MM7尚未逐条回填三重验证，是下一步）
- `decision_rules.md`：v0.2（新增候选规则7：命令逐字复诵；规则2新增第三层例外+对照组说明）
- `relationship_rules.md`：v0.1
- `expression_dna.md`：v0.4（首个正式转正口癖"最爱的人"，3个独立场景3种语境）
- `contradictions.md`：矛盾三分类 + 2条张力（含首次"本质性张力"分类）+ 2条观察项
- CEU schema：v0.6（卷一末尾schema复核触发：value_conflict新增"已核实无冲突"的显式写法）

## 待处理的 schema_gap 信号

**0条待复核** —— 卷一末尾累积的3条信号（A-001/C-002/S-002）已于2026-07-18全部复核完毕，详见 `logs/schema_gaps.md` 复核记录表。后续卷新出现的信号会继续累积到这里。

## 待处理的观察项（非schema_gap，是矛盾候选）

2条（见 `contradictions.md`）：
1. 语气词"喔"在公务/私密两种场合都出现，与MM5假设不完全吻合，n=2太小无法判断
2. 安兹在场但非竞争场合时（C-002）她也毫无克制地追求亲密——可能提示MM5的"看观众"框架该换成"看安兹是否明确表态"，目前只有1个场景，需要更多cluster验证

## Pipeline 基础设施（本轮新增）

流程是一个简单的 pipeline（见 `spec/eval_protocol.md` 第7节），不用 subagent：机械步骤（候选场景定位/schema校验/轮次汇总）用 `scripts/` 下的脚本，需要理解语义的步骤（CEU抽取/Character OS更新/schema复核）由我在对话里按文档记录的流程直接执行。

- 脚本：`scripts/locate_candidates.py`（候选场景定位）/ `scripts/validate_ceu.py`（机械校验）/ `scripts/reconcile_round.py`（轮次切换汇总），均已改为轮次感知（`--round` 参数，默认取最新 `V*` 目录）

## 下一步（用户要求处理到卷五；本session的TaskList#1-8对应这个顺序）

1. **卷三**——下一步，回来就先做这个（先跑`locate_candidates.py 雅儿贝德 3`生成`_index_vol3.yaml`，这是第一次处理卷三，无V0.1遗留数据）
2. 卷四
3. 卷五（本轮当前阶段的目标终点）
4. MM2/MM4/MM6/MM7 逐条回填三重验证标注（不必卡在卷一，可以和卷三~五并行积累证据后再做）

**跨会话恢复进度**：卷一（`_index_vol1.yaml`）已全部完成，`next_recommended: null`，schema复核已commit（`61c333f`）。卷二复核已完成（结论：兼容，无需调整CEU本身，仅revision_log记了一条确认记录，**这条revision_log改动尚未commit**）。下一步是卷三，本文件"下一步"列表第1项。

---
最后更新：2026-07-18（卷一完成 + schema复核完成 + 卷二复核完成，均已确认），对应 commit `61c333f`（**注意：卷二复核的revision_log条目本身尚未提交**）
