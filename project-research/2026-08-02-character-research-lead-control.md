---
feature_ids:
  - character-eval-validity
topics:
  - research-control
  - team-orchestration
  - gatekeeping
doc_kind: research_control
created: 2026-08-02
owner: "@cat-faziug16"
---

# Character Research Lead Control

## Current Leadership Decision

Quality喵 takes research lead for the current character-distillation evaluation track.

The immediate research question is narrow:

> Does the true profile causally improve profile-sensitive outputs over empty/wrong profile under a blind, paired, reproducible evaluation?

The active schema remains:

1. `content_fidelity`
2. `style_register`
3. `evaluation_validity`

Knowledge-boundary, mechanism, and long-horizon trajectory metrics stay deferred until the current causal question is answered.

## Gate Status

| Gate | Status | Decision |
|---|---|---|
| Gate 1: exploratory style-axis rescore | pass with warning | Use as diagnostic only. |
| Gate 2: paired bootstrap + profile-sensitivity index | pass | Existing content metric is inconclusive, not negative; register n=25 is underpowered. |
| Gate 3: blind style scoring | fail as confirmatory; pass as diagnostic | Scripts and numbers are usable, but judge independence was not established. Must rerun with an independent scorer. |
| Gate 4: full vol14 contamination ablation | not accepted / in progress | Prep files exist locally, but Task 4 is not a committed or accepted artifact. Do not interpret partial predictions. |

## Current Worktree Observation

At takeover time, Task 4 local files existed under `logs/predictions/ablation_v14_full/` and two build scripts existed under `scripts/`, but they were untracked. Only one prediction file was present:

- `logs/predictions/ablation_v14_full/pred_armA_part01.md`

The other 11 expected prediction files were absent. Background-agent ids from prior messages are not treated as durable state.

## Rules From This Point

1. File + commit is truth. Background-agent ids and chat claims are not status.
2. No Task 4 scoring or conclusion until Task 4 prep is committed and Gate 3 is rerun independently.
3. No profile edits from vol14/test findings.
4. Any full-ablation prediction run must produce all expected arm/part files and a count report before scoring.
5. If background execution is used, completion must be represented by files, not by "waiting for agent" messages.

## Team Assignments

### DS

Own execution cleanup:

- Freeze or regenerate Task 4 prep files.
- Commit only stable prep artifacts, not incomplete prediction outputs.
- Prepare an independent Gate 3 rerun path using a scorer that has not seen the forbidden files.
- After independent Gate 3 passes, resume full vol14 predictions.

### GLM

Own rubric/protocol critique:

- Review the independent Gate 3 raw scoring format before unblind if available.
- Check whether the `first_person` failure is a vol14-only phenomenon or a profile overgeneralization candidate by using train/dev evidence only.
- Do not edit `profile.yaml` until train/dev evidence is recorded.

### Quality喵

Own acceptance:

- Reopen Gate 3 only after independent raw scores exist.
- Review Task 4 prep before any scoring report is accepted.
- Keep the research question scoped to profile causality until Gate 4 has a clean result.

## Next Concrete Step

DS should stop waiting on lost background tasks and make the current state reproducible:

1. Decide whether `pred_armA_part01.md` is to be discarded or kept as a non-confirmatory scratch artifact.
2. Commit clean Task 4 prep only:
   - `scripts/build_full_ablation_arena.py`
   - `scripts/build_full_item_map.py`
   - `logs/predictions/ablation_v14_full/README.md`
   - `logs/predictions/ablation_v14_full/full_item_map.md`
   - `logs/predictions/ablation_v14_full/arena_part*.txt`
   - `logs/predictions/ablation_v14_full/gt_key.md`
   - `logs/predictions/ablation_v14_full/task_spec_arm*.md`
3. Fix any prep inconsistency first. Current README claims `alignment_failures: 0`, while the total table showed `1` in an earlier local inspection; this must be reconciled before commit.
4. Route back to Quality喵 for prep acceptance.

[质量喵（GPT）/GPT5.5喵🐾]

