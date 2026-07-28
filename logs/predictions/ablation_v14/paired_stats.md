# Paired Bootstrap Reanalysis of vol14 Ablation

Method: paired bootstrap, 10000 resamples, seed=20260728.
Items are paired across arms (same slot, three different profile conditions). This is the correct analysis because the three arms predict exactly the same 79 slots.

## Bootstrap Confidence Intervals

| field | pair | mean_diff | ci95 | n |
|---|---:|---:|---:|---:|
| content | C-A | +0.057 | [-0.013, +0.127] | 79 |
| content | B-C | -0.006 | [-0.057, +0.051] | 79 |
| content | B-A | +0.051 | [-0.006, +0.108] | 79 |
| register | C-A | +0.000 | [-0.160, +0.160] | 25 |
| register | B-C | +0.040 | [+0.000, +0.120] | 25 |
| register | B-A | +0.040 | [-0.120, +0.200] | 25 |

## Interpretation

The paired bootstrap CIs are narrower than the rough independent-SE estimate (SE ≈ 0.056 per arm, 2×SE ≈ 0.112 for difference) because paired analysis removes between-item variance. If the CI for C-A excludes 0, the profile effect is detectable above noise. If the CI for B-C straddles 0, wrong and true profile are not reliably separated.

## Chunk Breakdown (content accuracy)

| chunk | pair | mean_diff | n |
|---|---:|---:|---:|
| A | C-A | +0.062 | 48 |
| A | B-C | +0.010 | 48 |
| A | B-A | +0.073 | 48 |
| B | C-A | +0.048 | 31 |
| B | B-C | -0.032 | 31 |
| B | B-A | +0.016 | 31 |

## Profile-Sensitivity Index (exploratory)

Cross-reference with `style_axis_scores_exploratory.md`: for items where the exploratory style-axis B≠C (profile truly shifts expression), is the content-score |B-C| larger than for items where B=C on all style axes?

| group | n_items | mean_abs_B_minus_C_content |
|---|---:|---:|
| style-sensitive (B≠C on ≥1 axis) | 14 | 0.143 |
| style-insensitive (B=C on all axes) | 18 | 0.083 |

Items with style-axis divergence show larger content-score B-C gaps, suggesting profile consumption leaks into content scoring even on the current coarse metric.

## Arm Means (reference only)

| arm | content_mean | n | register_mean | n |
|---|---:|---:|---:|---:|
| A | 0.373 | 79 | 0.760 | 25 |
| B | 0.424 | 79 | 0.800 | 25 |
| C | 0.430 | 79 | 0.760 | 25 |

## Method Notes

- Bootstrap: 10 000 resamples with replacement, paired by item ID.
- Register axis n=25; CIs reflect the low sample size.
- Chunk breakdowns are descriptive (no bootstrap) due to small per-chunk n.
- Profile-sensitivity index uses exploratory (non-blind) style-axis data; 
  treat as diagnostic, not confirmatory.
