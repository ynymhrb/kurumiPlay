---
feature_ids:
  - character-eval-validity
topics:
  - character-distillation
  - evaluation-validity
  - ablation
  - contamination-control
doc_kind: implementation_plan
created: 2026-07-28
owner: "@cat-faziug16"
---

# Character Eval Validity Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the current vol14 ablation from an inconclusive 79-slot diagnostic into a validated evaluation program that can separate profile contribution, protocol contribution, pretraining contamination, and scorer bias.

**Architecture:** Work proceeds through gates. First calibrate the measurement instrument on existing artifacts; then run confirmatory blind scoring; only after the metric can see profile-sensitive effects do we run full-size contamination ablation and profile/protocol 2x2. Quality喵 owns acceptance and merge gates, not prediction or judging.

**Tech Stack:** Markdown experiment records, Python parsing/statistics scripts, existing `logs/predictions/` artifacts, cold-context prediction/judge agents, Git commits on `main`.

---

## Current Evidence Baseline

Truth source: `logs/predictions/ablation_v14/scores.md`.

Current three-arm result:

| arm | condition | content | n | register | n |
|---|---|---:|---:|---:|---:|
| A | no profile | 0.373 | 79 | 0.760 | 25 |
| B | wrong profile | 0.424 | 79 | 0.800 | 25 |
| C | true profile v0.10 | 0.430 | 79 | 0.760 | 25 |

Pre-registered interpretation:

- `C - A = +0.057`: weak signal, below no-claim threshold.
- `B - C = -0.006`: wrong and true profile not separated by total content accuracy.
- Register axis has only 25 applicable items; one item is 0.04, so current register score has low power.

Operational conclusion for this roadmap:

- Do not tune `characters/雅儿贝德/V2.0/profile.yaml` from vol14/test evidence.
- Do not claim profile contribution is proven.
- Do not claim profile is useless. The current metric may be blind to expression-layer effects.

## Team Split

| Workstream | Owner | Reviewer / Gate |
|---|---|---|
| Style-axis rubric and exploratory profile-consumption diagnosis | 开发猫（GLM）/glm5.2喵 | 质量喵（GPT） |
| Paired statistical reanalysis and full-size ablation harness | 研究喵（DS）/DS-V4Pro喵 | 质量喵（GPT） |
| Confirmatory blind style scoring execution | 研究喵（DS） executes cold judges; GLM reviews rubric fit | 质量喵（GPT） |
| 2x2 profile/protocol intervention design | 开发猫（GLM） primary; DS checks statistical power | 质量喵（GPT） |
| N>1 generalization planning | 研究喵（DS） candidate/data audit; GLM method transfer critique | 质量喵（GPT） |
| Acceptance, merge, final verdicts | 质量喵（GPT） | co-creator decision gate |

Quality喵 acceptance rule: do not generate prediction arms, do not act as primary scorer, and do not edit profile content from test-set findings. Quality喵 may run parser/stat scripts, review diffs, verify counts, and write gate verdicts.

---

### Task 1: Exploratory Style-Axis Rescore of Existing Arms

**Owner:** 开发猫（GLM）/glm5.2喵  
**Purpose:** Determine whether B and C differ systematically on profile-sensitive expression axes even though total content scores are similar.

**Files:**
- Read: `logs/predictions/ablation_v14/pred_armA.md`
- Read: `logs/predictions/ablation_v14/pred_armB.md`
- Read: `logs/predictions/ablation_v14/pred_armC.md`
- Read: `logs/predictions/ablation_v14/gt_key.md`
- Read: `logs/predictions/ablation_v14/wrong_profile_counterfactual.yaml`
- Read: `characters/雅儿贝德/V2.0/profile.yaml`
- Create: `logs/predictions/ablation_v14/style_axis_rubric.md`
- Create: `logs/predictions/ablation_v14/style_axis_scores_exploratory.md`

- [ ] **Step 1: Write the style-axis rubric**

Create `style_axis_rubric.md` with these axes and scoring:

```markdown
# Style-Axis Rubric for vol14 Ablation

This is exploratory because current predictions and GT have already been inspected by multiple agents. It is not confirmatory evidence until Task 3 reruns it blind.

Axes:

1. first_person
   - 1 = candidate uses the same self-reference class as GT (`我`, `小女子`, `妾身`, no self-reference).
   - 0 = candidate uses a conflicting self-reference class.
   - - = no self-reference decision exists.

2. attribution_source
   - 1 = agency/honor source matches GT (`安兹/陛下/至尊` as source vs speaker self as source).
   - 0 = agency/honor source conflicts with GT.
   - - = no agency/honor source decision exists.

3. stance_register
   - 1 = posture toward audience matches GT (deferential, hidden threat, open contempt, internal analysis, command).
   - 0 = posture conflicts with GT.
   - - = posture not judgeable.

4. emotion_channel
   - 1 = emotion channel matches GT (verbal outburst, bodily leakage, suppressed/analytic, no emotion).
   - 0 = emotion channel conflicts with GT.
   - - = no emotion-channel decision exists.

5. sentence_dynamics
   - 1 = high/low arousal length economy matches GT (short collapse, formal expansion, ordinary narration).
   - 0 = length economy conflicts with GT.
   - - = not judgeable.

Per-axis score = mean over applicable rows. Overall style score = mean of all applicable axis cells, not mean of items.
```

- [ ] **Step 2: Score A/B/C against GT on the five axes**

Append rows to `style_axis_scores_exploratory.md` in this exact format:

```markdown
# Exploratory Style-Axis Scores

| # | axis | GT cue | A | B | C | note |
|---|---|---|---:|---:|---:|---|
| 49 | first_person | 小女子 | 0 | 0 | 1 | C uses 小女子; A/B use 妾身 or omit. |
```

Use `-` for non-applicable cells. Do not collapse multiple axes into one row.

- [ ] **Step 3: Add summary table**

At the bottom of `style_axis_scores_exploratory.md`, add:

```markdown
## Summary

| axis | A | n | B | n | C | n | C-A | C-B |
|---|---:|---:|---:|---:|---:|---:|---:|
```

Rows required: `first_person`, `attribution_source`, `stance_register`, `emotion_channel`, `sentence_dynamics`, `all_style_cells`. For each row, compute `A`, `B`, and `C` as the mean of applicable 0/1 cells for that axis, compute each `n` as the count of applicable cells, compute `C-A` as `C minus A`, and compute `C-B` as `C minus B`.

- [ ] **Step 4: Commit exploratory rescore**

Run:

```powershell
git add logs/predictions/ablation_v14/style_axis_rubric.md logs/predictions/ablation_v14/style_axis_scores_exploratory.md
git commit -m "补充vol14消融风格轴探索评分" -m "Why: 内容准确率未能区分B/C，需要在profile敏感的自称、归荣、姿态、情绪通道、句长轴上做探索性诊断。`n`n[glm5.2喵/glm-5.2🐾]"
```

**Acceptance Gate 1:** Quality喵 verifies every scored row references an actual `#N`, summary arithmetic matches raw rows, and the report clearly labels itself exploratory.

---

### Task 2: Paired Statistical Reanalysis of Existing Scores

**Owner:** 研究喵（DS）/DS-V4Pro喵  
**Purpose:** Replace rough independent-SE reasoning with paired item-level estimates for existing 79-slot content and register scores.

**Files:**
- Read: `logs/predictions/ablation_v14/scores_raw.md`
- Read: `logs/predictions/ablation_v14/unblind_key.json`
- Read: `logs/predictions/ablation_v14/gt_key.md`
- Create: `scripts/analyze_ablation_pairs.py`
- Create: `logs/predictions/ablation_v14/paired_stats.md`

- [ ] **Step 1: Add parser/stat script**

Create `scripts/analyze_ablation_pairs.py` with these functions:

```python
# -*- coding: utf-8 -*-
import json
import os
import random
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "logs", "predictions", "ablation_v14")
ROW = re.compile(r"^\s*#?\s*(\d+)\s*\|(.*)$")
CELL = re.compile(r"([XYZ])\s*:\s*([0-9.]+)\s*/\s*([0-9.]+|-)")

def load_chunks():
    chunks = {}
    with open(os.path.join(D, "gt_key.md"), encoding="utf-8") as f:
        for raw in f:
            parts = [x.strip() for x in raw.strip().strip("|").split("|")]
            if len(parts) >= 3 and parts[0].isdigit():
                chunks[int(parts[0])] = parts[1]
    return chunks

def load_scores():
    key = json.load(open(os.path.join(D, "unblind_key.json"), encoding="utf-8"))
    rows = {}
    with open(os.path.join(D, "scores_raw.md"), encoding="utf-8") as f:
        for raw in f:
            m = ROW.match(raw)
            if not m:
                continue
            cid = int(m.group(1))
            values = {}
            for lab, content, register in CELL.findall(m.group(2)):
                arm = key[str(cid)][lab]
                values[arm] = {
                    "content": float(content),
                    "register": None if register == "-" else float(register),
                }
            rows[cid] = values
    return rows

def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def bootstrap_diff(rows, left, right, field, n=10000, seed=20260728):
    rng = random.Random(seed)
    ids = [cid for cid, vals in rows.items() if vals[left][field] is not None and vals[right][field] is not None]
    diffs = []
    for _ in range(n):
        sample = [rng.choice(ids) for _ in ids]
        diffs.append(mean([rows[cid][left][field] - rows[cid][right][field] for cid in sample]))
    diffs.sort()
    return ids, mean([rows[cid][left][field] - rows[cid][right][field] for cid in ids]), diffs[int(0.025*n)], diffs[int(0.975*n)]

def main():
    rows = load_scores()
    chunks = load_chunks()
    pairs = [("C", "A"), ("B", "C"), ("B", "A")]
    lines = ["# Paired Reanalysis of vol14 Ablation", ""]
    lines.append("| field | pair | mean_diff | ci95_low | ci95_high | n |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for field in ["content", "register"]:
        for left, right in pairs:
            ids, diff, lo, hi = bootstrap_diff(rows, left, right, field)
            lines.append(f"| {field} | {left}-{right} | {diff:+.3f} | {lo:+.3f} | {hi:+.3f} | {len(ids)} |")
    lines.append("")
    lines.append("## Chunk Content Diffs")
    lines.append("")
    lines.append("| chunk | pair | mean_diff | n |")
    lines.append("|---|---|---:|---:|")
    for chunk in sorted(set(chunks.values())):
        subset = {cid: vals for cid, vals in rows.items() if chunks.get(cid) == chunk}
        for left, right in pairs:
            ids = [cid for cid in subset if subset[cid][left]["content"] is not None and subset[cid][right]["content"] is not None]
            diff = mean([subset[cid][left]["content"] - subset[cid][right]["content"] for cid in ids])
            lines.append(f"| {chunk} | {left}-{right} | {diff:+.3f} | {len(ids)} |")
    with open(os.path.join(D, "paired_stats.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run script**

Run:

```powershell
$env:PYTHONIOENCODING='utf-8'; python scripts\analyze_ablation_pairs.py
```

Expected:

- Exit code 0.
- `logs/predictions/ablation_v14/paired_stats.md` exists.
- Table contains `content` and `register` rows for `C-A`, `B-C`, `B-A`.

- [ ] **Step 3: Commit paired reanalysis**

Run:

```powershell
git add scripts/analyze_ablation_pairs.py logs/predictions/ablation_v14/paired_stats.md
git commit -m "补充vol14消融配对统计分析" -m "Why: 三臂共享同一79项，需用配对bootstrap替代粗略独立比例SE，避免误判弱信号。`n`n[研究喵（DS）/deepseek-v4-pro🐾]"
```

**Acceptance Gate 2:** Quality喵 reruns the command and checks that confidence intervals are computed on paired item differences, not independent arm means.

---

### Task 3: Confirmatory Blind Style-Axis Scoring

**Owner:** 研究喵（DS） executes; 开发猫（GLM） reviews rubric fit  
**Purpose:** Turn Task 1 exploratory style-axis finding into a blind, reproducible score.

**Files:**
- Read: `logs/predictions/ablation_v14/style_axis_rubric.md`
- Read: `logs/predictions/ablation_v14/pred_armA.md`
- Read: `logs/predictions/ablation_v14/pred_armB.md`
- Read: `logs/predictions/ablation_v14/pred_armC.md`
- Read: `logs/predictions/ablation_v14/gt_key.md`
- Create: `scripts/merge_style_blind.py`
- Create: `scripts/unblind_style.py`
- Create: `logs/predictions/ablation_v14/style_scoring_sheet.md`
- Create: `logs/predictions/ablation_v14/style_unblind_key.json`
- Create after cold judge: `logs/predictions/ablation_v14/style_scores_raw.md`
- Create after unblind: `logs/predictions/ablation_v14/style_scores.md`

- [ ] **Step 1: Write blind style merge script**

`merge_style_blind.py` must mirror `merge_blind.py` but generate style scoring rows:

```markdown
## #49
- GT: 「好久不见了，兰布沙陛下。承蒙陛下在如此时局之中愿意拨冗接见小女子，心中不胜感激。」
- X: 「久违了，兰布沙陛下。承蒙陛下在如此仓促之下拨冗相见，妾身感激不尽。」
- Y: 「好久不见了，国王陛下。承蒙您在这样的时节拨冗接见小女子，不胜感激。」
- Z: 「承蒙陛下接见。」
- axes_to_score: first_person, attribution_source, stance_register, emotion_channel, sentence_dynamics
```

Use seed `20260728` so the output is reproducible.

- [ ] **Step 2: Write unblind style script**

`unblind_style.py` must parse this raw format:

```markdown
#49 | first_person X:1 Y:0 Z:1 | attribution_source X:- Y:1 Z:0 | stance_register X:1 Y:1 Z:0
```

It must output per-axis arm means and an `all_style_cells` aggregate.

- [ ] **Step 3: Generate blind sheet**

Run:

```powershell
$env:PYTHONIOENCODING='utf-8'; python scripts\merge_style_blind.py
```

Expected:

- `style_scoring_sheet.md` exists.
- `style_unblind_key.json` exists.
- Script reports A/B/C all have 79 predictions.

- [ ] **Step 4: Cold judge scores style sheet**

Dispatch a cold scoring agent with this allowed-file list only:

```text
logs/predictions/ablation_v14/style_axis_rubric.md
logs/predictions/ablation_v14/style_scoring_sheet.md
```

Forbidden:

```text
style_unblind_key.json
pred_armA.md
pred_armB.md
pred_armC.md
scores.md
scores_raw.md
characters/
source/
```

The cold judge writes only `style_scores_raw.md` and reports item count.

- [ ] **Step 5: Unblind style scores**

Run:

```powershell
$env:PYTHONIOENCODING='utf-8'; python scripts\unblind_style.py
```

Save stdout to `logs/predictions/ablation_v14/style_scores.md`.

- [ ] **Step 6: Commit blind style scoring**

Run:

```powershell
git add scripts/merge_style_blind.py scripts/unblind_style.py logs/predictions/ablation_v14/style_scoring_sheet.md logs/predictions/ablation_v14/style_unblind_key.json logs/predictions/ablation_v14/style_scores_raw.md logs/predictions/ablation_v14/style_scores.md
git commit -m "完成vol14消融风格轴盲评" -m "Why: 内容准确率无法区分profile表达层贡献，需用盲化风格轴评分验证profile-sensitive效果。`n`n[研究喵（DS）/deepseek-v4-pro🐾]"
```

**Acceptance Gate 3:** Quality喵 verifies cold judge did not read unblind key, all scripts parse 79 rows, and `style_scores.md` separates per-axis and aggregate results.

---

### Task 4: Full vol14 Contamination Ablation

**Owner:** 研究喵（DS）/DS-V4Pro喵  
**Purpose:** Increase sample size from 79 to the full vol14 scored target so profile/no-profile differences are not dominated by low power.

**Files:**
- Read: `characters/雅儿贝德/source/雅儿贝德_第十四卷验证集.txt`
- Read after prediction freeze only: `characters/雅儿贝德/source/雅儿贝德_第十四卷原文.txt`
- Read: `logs/predictions/vol14_scored.md`
- Create: `logs/predictions/ablation_v14_full/README.md`
- Create: `logs/predictions/ablation_v14_full/full_item_map.md`
- Create: `logs/predictions/ablation_v14_full/arena_part01.txt` through `arena_part04.txt`
- Create after alignment: `logs/predictions/ablation_v14_full/gt_key.md`
- Create after prediction: `pred_armA_part*.md`, `pred_armB_part*.md`, `pred_armC_part*.md`
- Create after scoring: `scores_raw.md`, `scores.md`

- [ ] **Step 1: Create full item map before any prediction**

Create `full_item_map.md` with exactly these columns:

```markdown
| full_id | vol14_id | source_line | chunk | include | reason |
|---|---|---:|---|---|---|
```

Rules:

- Include every independently scoreable item from `vol14_scored.md`.
- Target count is 200 because `vol14_scored.md` reports 200 scoring items.
- If a placeholder is excluded because it was merged/duplicate/non-character, mark `include=no` and write the reason.

- [ ] **Step 2: Build four approximately equal arenas**

Split included items into four parts of about 50 scoreable items each. The arena files must preserve local context but hide GT with `【#full_id】`.

Each arena header must include:

```markdown
# vol14 full ablation arena part NN
# Scoreable items: 50
# Prediction phase forbidden files: gt_key.md, original vol14 source, pred_arm*, scores*
```

- [ ] **Step 3: Verify GT alignment**

Create `gt_key.md` only after all arena files are frozen. It must contain:

```markdown
| # | vol14_id | chunk | line | 原文内容 |
|---|---|---|---|---|
```

Run an alignment check and record:

```markdown
alignment_failures: 0
scoreable_items: 200
```

in `README.md`.

- [ ] **Step 4: Generate all three arms cold**

Use cold-context agents. Do not reuse hot `vol14_blind.md` for C and do not reuse the 79-slot ablation predictions for confirmatory full-size scoring.

Allowed inputs per arm:

- A: `arm_task_spec.md`, full arenas, `spec/prediction_protocol.md`.
- B: same plus `wrong_profile_counterfactual.yaml`.
- C: same plus `characters/雅儿贝德/V2.0/profile.yaml` and `characters/雅儿贝德/V2.0/literary_techniques.md`.

Each arm writes one file per part:

```text
logs/predictions/ablation_v14_full/pred_armA_part01.md
logs/predictions/ablation_v14_full/pred_armB_part01.md
logs/predictions/ablation_v14_full/pred_armC_part01.md
```

and so on through part04.

- [ ] **Step 5: Blind merge and score**

Reuse the blind scoring pattern from `scripts/merge_blind.py` and `scripts/unblind.py`; create full-specific copies only if needed to avoid altering the 79-slot experiment.

Expected output:

```markdown
| arm | condition | content | n | register | n |
```

with content `n=200`.

- [ ] **Step 6: Commit full ablation**

Run:

```powershell
git add logs/predictions/ablation_v14_full
git commit -m "完成vol14全量三臂污染消融" -m "Why: 79槽消融功效不足，需扩展到vol14全量计分项以估计profile边际贡献。`n`n[研究喵（DS）/deepseek-v4-pro🐾]"
```

**Acceptance Gate 4:** Quality喵 verifies `scoreable_items=200`, all arms have exactly 200 predictions, no prediction agent saw `gt_key.md`, and final report includes paired or bootstrap intervals.

---

### Task 5: Blind Rejudge of the Original 0.55 -> 0.63 Claim

**Owner:** 开发猫（GLM）/glm5.2喵  
**Purpose:** Test scorer independence for the original vol13 vs vol14 improvement.

**Files:**
- Read: `logs/predictions/vol13_blind.md`
- Read: `logs/predictions/vol14_blind.md`
- Read: `logs/predictions/vol13_scored.md`
- Read: `logs/predictions/vol14_scored.md`
- Create: `logs/predictions/rejudge_13_14/README.md`
- Create: `logs/predictions/rejudge_13_14/scoring_sheet.md`
- Create: `logs/predictions/rejudge_13_14/unblind_key.json`
- Create after cold judge: `logs/predictions/rejudge_13_14/scores_raw.md`
- Create after unblind: `logs/predictions/rejudge_13_14/scores.md`

- [ ] **Step 1: Pre-register rejudge protocol**

`README.md` must say:

```markdown
# vol13 vs vol14 Blind Rejudge

Question: Does the old 0.55 -> 0.63 improvement survive arm-label blinding and an independent scorer?

Prediction files are frozen before this experiment. The judge sees GT and candidate predictions but not version labels.

Primary metric: content accuracy using the existing 1/0.5/0 rubric.
Secondary metric: mechanism/style if directly recoverable from scored files.
No profile edits are allowed from this result.
```

- [ ] **Step 2: Generate mixed scoring sheet**

Randomize item order and version labels. Use labels `X` and `Y`, not `vol13`/`vol14`.

- [ ] **Step 3: Cold judge scores**

Cold judge may read only:

```text
logs/predictions/rejudge_13_14/README.md
logs/predictions/rejudge_13_14/scoring_sheet.md
```

The judge writes `scores_raw.md`.

- [ ] **Step 4: Unblind and report**

`scores.md` must include:

```markdown
| source | blinded_accuracy | old_accuracy | delta |
|---|---:|---:|---:|
```

- [ ] **Step 5: Commit rejudge**

Run:

```powershell
git add logs/predictions/rejudge_13_14
git commit -m "完成vol13-vol14独立盲重评" -m "Why: 原0.55到0.63增益由非盲评分产生，需独立盲评确认评分者偏差是否影响结论。`n`n[glm5.2喵/glm-5.2🐾]"
```

**Acceptance Gate 5:** Quality喵 verifies the judge could not infer version labels from file headers and the final report compares old vs blinded scores.

---

### Task 6: Profile x Protocol 2x2 Intervention Design

**Owner:** 开发猫（GLM）/glm5.2喵  
**Blocked Until:** Acceptance Gates 1, 2, 3, and either Gate 4 or Gate 5 have a written verdict.

**Files:**
- Create: `docs/discussions/profile_protocol_2x2_design.md`
- Create after approval: `logs/predictions/profile_protocol_2x2_v14/README.md`

- [ ] **Step 1: Write design document**

Create `docs/discussions/profile_protocol_2x2_design.md`:

```markdown
---
feature_ids:
  - character-eval-validity
topics:
  - profile-protocol-2x2
doc_kind: design
created: 2026-07-28
---

# Profile x Protocol 2x2 Design

Question: Does the observed improvement come from profile contents, prediction protocol, or their interaction?

Cells:

| cell | profile | protocol |
|---|---|---|
| P07-R10 | profile v0.7 | prediction_protocol v1.0 |
| P07-R12 | profile v0.7 | prediction_protocol v1.2 |
| P10-R10 | profile v0.10 | prediction_protocol v1.0 |
| P10-R12 | profile v0.10 | prediction_protocol v1.2 |

Primary metric: use the metric validated by Gates 1-5.
Secondary metric: original content accuracy.

Do not run this experiment if prior gates say the metric cannot detect profile-sensitive differences.
```

- [ ] **Step 2: Add power and cost estimate**

Include:

```markdown
Minimum expected detectable main effect:
- n=79: descriptive only.
- n=200: main effects around 0.08 may be detectable; interaction effects likely underpowered.

Execution rule:
- If full ablation C-A remains below 0.05 and style-axis C-B also fails, do not run 2x2.
- If style-axis C-B succeeds but content C-A fails, run 2x2 on style metrics first.
```

- [ ] **Step 3: Commit design**

Run:

```powershell
git add docs/discussions/profile_protocol_2x2_design.md
git commit -m "设计profile与协议2x2干预实验" -m "Why: 在评估效度通过门控后，需要拆分profile内容与推理协议对增益的贡献。`n`n[glm5.2喵/glm-5.2🐾]"
```

**Acceptance Gate 6:** Quality喵 checks that the design has explicit go/no-go conditions and does not assume the current content metric is valid.

---

### Task 7: N>1 Generalization Candidate Audit

**Owner:** 研究喵（DS）/DS-V4Pro喵  
**Blocked Until:** Gates 1-6 identify a valid metric and at least one reliable effect.

**Files:**
- Create: `docs/discussions/second_character_candidate_audit.md`

- [ ] **Step 1: Define candidate criteria**

The audit must rank candidates by:

```markdown
| criterion | reason |
|---|---|
| lower pretraining popularity than Overlord/Albedo | better contamination contrast |
| enough source text with recurring decisions | profile can be distilled |
| clear held-out scenes | can evaluate prediction |
| distinct speech/register markers | style metric can transfer |
| manageable source access | pipeline cost stays bounded |
```

- [ ] **Step 2: Score at least three candidates**

Use this table:

```markdown
| candidate | contamination risk | source volume | decision density | style separability | heldout feasibility | total | notes |
|---|---:|---:|---:|---:|---:|---:|---|
```

Each dimension is 1-5. Total is the sum.

- [ ] **Step 3: Recommend one candidate and one backup**

The recommendation must include:

```markdown
Primary:
Backup:
Why not the other candidates:
First train/dev/test split:
Expected biggest risk:
```

- [ ] **Step 4: Commit candidate audit**

Run:

```powershell
git add docs/discussions/second_character_candidate_audit.md
git commit -m "评估第二角色泛化候选" -m "Why: N=1无法支持方法论泛化，需要在指标可信后选择低污染且可验证的第二角色。`n`n[研究喵（DS）/deepseek-v4-pro🐾]"
```

**Acceptance Gate 7:** Quality喵 checks that the recommendation is based on contamination and evaluation feasibility, not character preference.

---

## Quality喵 Acceptance Checklist

For every task:

- [ ] `git status --short --branch` is clean except known governance files.
- [ ] New artifacts have YAML frontmatter when placed under `docs/`.
- [ ] Prediction agents and judge agents list allowed and forbidden files.
- [ ] Any blind key is not read before raw scores are completed.
- [ ] Every result report states whether it is exploratory or confirmatory.
- [ ] No profile changes are made from vol14/test evidence.
- [ ] Commit body contains `Why:` and the worker signature.
- [ ] After acceptance, push `main`.

## Gate Order

1. Gate 1 + Gate 2: existing experiment diagnostics are internally consistent.
2. Gate 3: style-axis metric can be scored blind.
3. Gate 4 and Gate 5: full-size contamination and old-score independence are checked.
4. Gate 6: only then run or reject 2x2.
5. Gate 7: only after metric/effect is reliable, start N>1 generalization.

If a gate fails, Quality喵 writes a `verdict.md` in the relevant experiment directory, for example `logs/predictions/ablation_v14/verdict.md` or `logs/predictions/ablation_v14_full/verdict.md`, with:

```markdown
# Verdict

Status: pass | fail | inconclusive

Evidence:

Decision:

Required next action:
```

No failed gate should be papered over by moving to a more expensive downstream experiment.
