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
| 卷一 | 进行中 | `_index_vol1.yaml` 已生成（19个候选cluster），cluster A 已处理完（YLDB-V1-A-001），其余18个cluster待处理 |
| 卷二 | V0.1遗留，待复核 | 9/11 cluster 有CEU（V0.1产出），尚未按V1.0流程重新审视是否需要调整；cluster A(partial)/K待处理 |
| 卷三～十 | 未开始 | |
| 卷十一～十二（dev） | 未启动 | 待train阶段收敛 |
| 卷十三～十四（test） | 未启动 | 仅里程碑触发 |

## 当前 Character OS 文件版本

- `value_hierarchy.md`：v0.3（第3/5层因移除seed引用暂列"待验证假设"）
- `mental_models.md`：v0.2（MM1背景脚注本轮已用YLDB-V1-A-001升级为第一手实锤）
- `decision_rules.md`：v0.2
- `relationship_rules.md`：v0.1
- `expression_dna.md`：v0.1（几乎空，仍是最大缺口）
- CEU schema：v0.5（本轮新增 `schema_gap` 字段）

## 待处理的 schema_gap 信号

1条未复核（见 `logs/schema_gaps.md`）：YLDB-V1-A-001 触发的"起源类证据不适配现有evidence_source三分类"问题，待 schema-reviewer 复核。

## Pipeline 基础设施（本轮新增）

- 脚本：`scripts/locate_candidates.py`（候选场景定位）/ `scripts/validate_ceu.py`（机械校验）/ `scripts/reconcile_round.py`（轮次切换汇总）
- Subagent：`.claude/agents/{ceu-extractor,character-os-updater,schema-reviewer,fidelity-evaluator}.md`
  - **已知限制**：本轮次创建的自定义subagent要到下次 Claude Code 会话启动时才会被识别为可调用的 subagent_type（当前会话里已通过手动模拟其角色指令的方式验证了 ceu-extractor + character-os-updater 两步的端到端流程，产出见 cluster A 处理记录）

## 下一步

- 用真正的 subagent（下次会话验证可调用后）继续处理卷一剩余18个cluster
- 处理到卷末时跑一次 schema-reviewer 复核 `logs/schema_gaps.md`
- 卷一处理完，回头审视卷二V0.1遗留CEU是否需要按当前schema/方法论调整

---
最后更新：2026-07-18（albedo-round-v1.0 首个batch：卷一 cluster A + 基础设施搭建），对应 commit（待本次提交后回填）
