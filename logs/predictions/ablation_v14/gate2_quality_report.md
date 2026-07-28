---
feature_ids:
  - character-eval-validity
topics:
  - paired-bootstrap
  - profile-sensitivity
  - quality-gate
doc_kind: quality_gate_report
created: 2026-07-29
owner: "@cat-faziug16"
reviewed_commit: "1acd73d"
---

# Gate 2 Quality Report

Status: **pass with minor reviewer fix**

Reviewed artifacts:

- `scripts/analyze_ablation_pairs.py`
- `logs/predictions/ablation_v14/paired_stats.md`

## Acceptance Checks

| Check | Result | Evidence |
|---|---|---|
| Commit scope limited to Task 2 files | pass | `git show --stat --name-only 1acd73d` lists only `scripts/analyze_ablation_pairs.py` and `paired_stats.md`. |
| Script reruns cleanly | pass | `python scripts/analyze_ablation_pairs.py` exits 0; reports `Items parsed: 79`, `Chunks: ['A', 'B']`, `Style-sensitive items: 14`, `All styled items: 32`. |
| Bootstrap is paired item-level, not independent arm means | pass | `paired_diff()` builds per-item `left-right` differences; `bootstrap_ci()` resamples that difference list. |
| Arm means match `scores.md` | pass | `paired_stats.md`: A content 0.373 / register 0.760; B 0.424 / 0.800; C 0.430 / 0.760. |
| Main CI table contains content and register rows for all requested pairs | pass | Rows exist for `C-A`, `B-C`, `B-A` on `content` and `register`. |
| Profile-sensitivity index is marked exploratory | pass | `paired_stats.md` notes it uses non-blind `style_axis_scores_exploratory.md` and is diagnostic, not confirmatory. |

## Verified Numbers

| field | pair | mean_diff | ci95 | n | verdict |
|---|---:|---:|---:|---:|---|
| content | C-A | +0.057 | [-0.013, +0.127] | 79 | inconclusive; CI crosses 0 |
| content | B-C | -0.006 | [-0.057, +0.051] | 79 | no reliable separation on content |
| content | B-A | +0.051 | [-0.006, +0.108] | 79 | inconclusive |
| register | C-A | +0.000 | [-0.160, +0.160] | 25 | underpowered |
| register | B-C | +0.040 | [+0.000, +0.120] | 25 | underpowered / boundary case |
| register | B-A | +0.040 | [-0.120, +0.200] | 25 | underpowered |

Profile-sensitivity index:

| group | n_items | mean_abs_B_minus_C_content |
|---|---:|---:|
| style-sensitive (`B≠C` on >=1 exploratory style axis) | 14 | 0.143 |
| style-insensitive (`B=C` on all exploratory style axes) | 18 | 0.083 |

This supports the direction of profile consumption, but remains exploratory because the style-sensitive grouping comes from non-blind Task 1 scoring.

## Reviewer Fix

I corrected Markdown table formatting in `scripts/analyze_ablation_pairs.py` and regenerated `paired_stats.md`:

- bootstrap table separator now has five columns;
- chunk table separator now has four columns;
- profile-sensitivity header no longer contains raw `|B-C|`, which Markdown parsed as extra columns.

No numeric values or statistical logic changed.

## Gate Verdict

Gate 2 passes.

Task 2 can be used as evidence that:

- the existing content metric is inconclusive, not negative;
- register with `n=25` is not a useful measurement axis;
- profile-sensitive style divergence has a diagnostic relationship with content-score divergence, but must be rechecked after Task 3 blind style scoring.

Next action: proceed to Task 3 confirmatory blind style-axis scoring with the minimum schema accepted in `schema_review_verdict.md`.

[质量喵（GPT）/GPT5.5喵🐾]

