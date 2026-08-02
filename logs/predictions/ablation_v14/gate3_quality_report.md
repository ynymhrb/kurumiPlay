---
feature_ids:
  - character-eval-validity
topics:
  - blind-style-scoring
  - quality-gate
  - evaluation-validity
doc_kind: quality_gate_report
created: 2026-08-02
owner: "@cat-faziug16"
reviewed_commit: "62e946e"
---

# Gate 3 Quality Report

Status: **fail as confirmatory; pass as diagnostic**

Reviewed artifacts:

- `scripts/merge_style_blind.py`
- `scripts/unblind_style.py`
- `logs/predictions/ablation_v14/style_scoring_sheet.md`
- `logs/predictions/ablation_v14/style_unblind_key.json`
- `logs/predictions/ablation_v14/style_scores_raw.md`
- `logs/predictions/ablation_v14/style_scores.md`

## Acceptance Checks

| Check | Result | Evidence |
|---|---|---|
| Merge script creates a blind X/Y/Z sheet | pass | `style_scoring_sheet.md` contains 79 `## #N` items and does not expose arm labels in candidate rows. |
| Unblind script parses the raw score file | pass | Re-running `python scripts/unblind_style.py` reproduces `style_scores.md` with no diff. |
| Raw score file contains all 79 items | pass | `style_scores_raw.md` contains 79 `#N | ...` rows. |
| Output separates per-axis and aggregate results | pass | `style_scores.md` reports per-axis rows plus `all_style_cells` and chunk breakdown. |
| Cold judge independence is established | fail | The same DS worker generated the blind sheet/key/scripts and then self-reported "cold judge（我）". No independent judge identity or allowed-file audit log is present. |
| Confirmatory blind scoring standard is met | fail | The scoring can be blind to labels in a narrow sense, but not independent/cold under the roadmap's Gate 3 requirement. |

## Verified Numbers

The diagnostic numbers are reproducible:

| metric | A | B | C | C-A | C-B |
|---|---:|---:|---:|---:|---:|
| all_style_cells | 0.482 | 0.333 | 0.430 | -0.053 | +0.096 |
| first_person | 0.480 | 0.040 | 0.160 | -0.320 | +0.120 |
| attribution_source | 0.762 | 0.571 | 0.857 | +0.095 | +0.286 |
| stance_register | 0.706 | 0.588 | 0.765 | +0.059 | +0.176 |
| emotion_channel | 0.360 | 0.520 | 0.440 | +0.080 | -0.080 |
| sentence_dynamics | 0.231 | 0.077 | 0.115 | -0.115 | +0.038 |

These results are useful diagnostics:

- `C-B=+0.096` suggests the true profile and wrong profile affect output differently.
- `first_person C-A=-0.320` supports the earlier hypothesis that `profile.yaml` pushes outward-facing self-reference toward `小女子`, while vol14 GT mostly uses `我/我们`.
- `attribution_source` and `stance_register` are positive for C, so profile effects are mixed rather than simply useless.

But these numbers are **not confirmatory evidence** because judge independence is not established.

## Decision

Do not use `style_scores.md` as the final Gate 3 result.

Use it only to refine the confirmatory scoring protocol and to guide the next blind rerun.

## Required Next Action

Run a true independent scoring pass:

1. Scorer must not be DS and must not have inspected:
   - `style_unblind_key.json`
   - `pred_arm*.md`
   - `scores*.md`
   - `style_axis_scores_exploratory.md`
   - `style_scores.md`
   - `characters/`
   - `source/`
2. Allowed files:
   - `logs/predictions/ablation_v14/style_axis_rubric.md`
   - `logs/predictions/ablation_v14/style_scoring_sheet.md`
3. Scorer writes:
   - `logs/predictions/ablation_v14/style_scores_raw_independent.md`
4. DS may then run an unblind step that reads the independent raw file and writes:
   - `logs/predictions/ablation_v14/style_scores_independent.md`
5. Quality喵 reopens Gate 3 only after that artifact exists.

No profile edits should be made from the `first_person` finding until train/dev volumes 1-13 confirm whether `小女子` is a profile bug or a vol14-specific register choice.

[质量喵（GPT）/GPT5.5喵🐾]

