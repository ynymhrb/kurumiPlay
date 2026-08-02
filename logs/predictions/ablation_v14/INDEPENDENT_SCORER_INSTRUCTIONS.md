# Gate 3 Independent Blind Style-Axis Scoring

> **Scorer**: 开发猫（GLM）/glm5.2喵 (@cat-wbr23mps)
> **Gate owner**: 质量喵（GPT）(@cat-faziug16)
> **Unblind executor**: 研究喵（DS）(@deepseek)

## What You're Doing

Score 79 blind items on 5 style axes. Each item has 3 anonymous candidates (X/Y/Z) and a GT reference. You don't know which arm each candidate comes from — that's the point.

## Allowed Files (ONLY these two)

1. `style_axis_rubric.md` — 5-axis definitions, scoring rules, GT style benchmarks
2. `style_scoring_sheet.md` — 79 blind items with X/Y/Z candidates + GT + axes_to_score

## FORBIDDEN Files (DO NOT OPEN)

- `style_unblind_key.json`
- `pred_arm*.md`
- `scores*.md`
- `style_axis_scores_exploratory.md`
- `style_scores.md` / `style_scores_raw.md`
- `gt_key.md`
- `unblind_key.json`
- Any file in `characters/` or `source/`

## Output

Write to: `logs/predictions/ablation_v14/style_scores_raw_independent.md`

**Format** — one line per item, all 5 axes required even if all `-`:

```
#N | first_person X:0 X:1 Y:0 Z:- | attribution_source X:1 Y:- Z:0 | stance_register X:- Y:1 Z:0 | emotion_channel X:0 Y:0 Z:1 | sentence_dynamics X:1 Y:- Z:1
```

**Rules**:
- `1` = candidate matches GT style on this axis
- `0` = candidate conflicts with GT style on this axis
- `-` = GT has no decision on this axis for this slot (don't count in denominator)
- Score against GT, NOT against profile
- Must produce exactly 79 lines (items #1 through #79)
- Even if all 3 candidates are `-` on an axis, include it

## Scoring Criteria Summary

| Axis | What to compare | 1 (match) | 0 (conflict) |
|---|---|---|---|
| `first_person` | Self-reference form | GT「我」→ candidate「我」 | GT「我」→ candidate「妾身/小女子」 |
| `attribution_source` | Agency/honor source direction | Same direction as GT | Opposite direction |
| `stance_register` | Audience posture | Same register as GT | Different register |
| `emotion_channel` | Emotion expression channel + valence | Same channel AND same valence | Different channel OR opposite valence |
| `sentence_dynamics` | Arousal-sentence length economy | Same pattern | Opposite pattern |

See `style_axis_rubric.md` for full definitions, GT style benchmarks, and edge cases.

## After Scoring

DS will run unblind:
```
$env:PYTHONIOENCODING='utf-8'; python scripts/unblind_style.py --input style_scores_raw_independent.md --output style_scores_independent.md
```

Quality喵 will reopen Gate 3 after `style_scores_independent.md` exists.
