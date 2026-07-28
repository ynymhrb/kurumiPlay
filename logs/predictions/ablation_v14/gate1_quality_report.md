---
feature_ids:
  - character-eval-validity
topics:
  - style-axis
  - quality-gate
doc_kind: quality_gate_report
created: 2026-07-28
owner: "@cat-faziug16"
reviewed_commit: "613b08a23c81d57f1586e4860862b0f86660623a"
---

# Gate 1 Quality Report

Status: pass with warning

Reviewed artifacts:

- `logs/predictions/ablation_v14/style_axis_rubric.md`
- `logs/predictions/ablation_v14/style_axis_scores_exploratory.md`

## Acceptance Checks

| Check | Result | Evidence |
|---|---|---|
| Commit scope limited to Task 1 files | pass | `git diff origin/main..HEAD --name-only` lists only the two style-axis files |
| No whitespace/check errors in commit | pass | `git show --check 613b08a` exits 0 |
| Every scored row references an existing `gt_key.md` id | pass | 50 scored rows, 32 unique ids, `missing_ids=[]` |
| Summary arithmetic matches raw scored rows | pass | recomputed per-axis means/counts and `C-A`/`C-B`; `summary_errors=[]` |
| Exploratory/non-blind label present | pass | both rubric and score report explicitly state exploratory, non-blind, and not confirmatory before Task 3 |
| Test-set profile edit discipline | pass | no `characters/雅儿贝德/V2.0/profile.yaml` changes |

## Warning

`style_axis_scores_exploratory.md` intentionally reports only rows that are discriminative or useful for GT baseline confirmation. It excludes all-1 non-discriminative axis rows and labels the summary `n` as "有判分行数", not "全部 applicable".

This is acceptable for Task 1 as an exploratory differential diagnostic because equal all-1 rows do not change `C-A` or `C-B`. It must not be reused as the confirmatory Task 3 scoring denominator.

Task 3 requirement:

- Pre-register the inclusion rule before the cold judge scores.
- Prefer full applicable axis scoring.
- If any slot is excluded because content is misaligned, mark it explicitly in the blind sheet and report the excluded ids.

## Gate Verdict

Gate 1 passes. The exploratory result may be used to design Task 3, but not as final evidence that profile v0.10 does or does not do causal work.

Next action: proceed to Task 2 paired statistical reanalysis and Task 3 blind style scoring.

[质量喵（GPT）/GPT5.5喵🐾]
