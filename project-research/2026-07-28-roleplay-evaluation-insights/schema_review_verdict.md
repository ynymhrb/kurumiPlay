---
feature_ids:
  - character-eval-validity
topics:
  - role-playing
  - evaluation-schema
  - profile-ablation
doc_kind: quality_gate_report
created: 2026-07-29
owner: "@cat-faziug16"
reviewed_claim_source: "@cat-wbr23mps schema critique 2026-07-28"
---

# Schema Review Verdict

Status: **pass with constraints**

Reviewed artifacts:

- `project-research/2026-07-28-roleplay-evaluation-insights/synthesis.md`
- `docs/superpowers/plans/2026-07-28-character-eval-validity-roadmap.md`
- `logs/predictions/ablation_v14/scores.md`
- `logs/predictions/ablation_v14/gate1_quality_report.md`
- `logs/predictions/ablation_v14/style_axis_rubric.md`
- `logs/predictions/ablation_v14/style_axis_scores_exploratory.md`
- `logs/predictions/ablation_v14/gt_key.md`
- `characters/雅儿贝德/V2.0/profile.yaml`

## Verdict

GLM's critique is accepted as the execution schema for the next gate:

> For the current causal question, use the minimum schema: content fidelity + style/register fidelity + evaluation validity.

The broader six-layer literature schema remains valid as a research map, but only three layers should be active in the immediate experiment. Knowledge boundary, mechanism scoring, and long-horizon trajectory are deferred until their prerequisites exist.

## Verified Claims

| Claim | Verdict | Evidence |
|---|---|---|
| Current content metric cannot conclude profile contribution | verified | `scores.md`: `C-A=+0.057`, below the pre-registered no-claim threshold; `B-C=-0.006`. |
| Style-axis result is exploratory, not confirmatory | verified | `style_axis_rubric.md` and `style_axis_scores_exploratory.md` both state non-blind/exploratory; `gate1_quality_report.md` passed with warning. |
| vol14 GT does not use `妾身` / `小女子` | verified | `gt_key.md` contains no `妾身` or `小女子`; self-reference hits include `我/我们` lines such as #21, #24, #49, #57, #66, #68, #70, #72, #73, #74. |
| profile v0.10 includes `小女子` as an outward-facing first-person option | verified | `characters/雅儿贝德/V2.0/profile.yaml`: `first_person: 我 / 人家（撒娇语境）/ 小女子（对外谦称场合，配"窃以为"级谦语）`. |
| The `小女子` conflict is a profile-edit signal | verified with restriction | It is a valid hypothesis, but must not be used to edit `profile.yaml` from vol14/test evidence. It needs train/dev evidence from vols 1-13. |

## Required Schema Changes

### 1. Active layers for the next run

The next confirmatory schema should activate only:

1. `content_fidelity`: existing content/function correctness, used as a baseline.
2. `style_register`: first-person, attribution source, stance register, emotion channel, sentence dynamics.
3. `evaluation_validity`: blind arm labels, independent judge, paired bootstrap/CI, frozen denominator, no profile edits from test evidence.

This prevents schema design from becoming a new bottleneck before the core profile-causality question is answered.

### 2. Deferred layers

These are useful later, but should not block Task 2/3:

- `knowledge_boundary`: requires unknown/known knowledge items and contamination-specific prompts.
- `long_horizon_interaction`: requires multi-turn sandbox, repeated runs, chunked judging.
- `decision_mechanism`: deferred unless the fixed-reference rule below is implemented.

### 3. Mechanism-axis fixed-reference rule

If mechanism scoring is added later, the judge must score every arm against the **same GT-role reference**, not against the profile that generated that arm.

Reason:

- Arm B uses a counterfactual/wrong profile.
- If the judge scores B against B's own profile, a prediction that faithfully follows the wrong profile would receive a high mechanism score.
- That would measure "profile adherence" rather than "true character mechanism correctness" and invert the ablation conclusion.

Required rule:

> In profile ablations, mechanism scoring reference is fixed to GT character evidence / true-role rubric. The judge remains blind to arm identity and never receives per-arm profile provenance.

### 4. Style denominator rule

Task 3 must not reuse Task 1's exploratory denominator.

Required rule:

- Denominator is determined from GT-side applicability before scoring.
- Full applicable rows should be included, including all-1 rows.
- If content-misaligned slots are excluded, the excluded ids and reason must be listed before unblinding.

## Go / No-Go Decision

Proceed to:

1. Task 2 paired statistical reanalysis, adding `profile-sensitivity index`.
2. Task 3 confirmatory blind style-axis scoring using the minimum schema above.

Do not proceed yet to:

- profile edits from vol14 first-person findings;
- full six-layer eval implementation;
- mechanism scoring without the fixed-reference rule;
- CharacterBox-style long-horizon trajectory evaluation.

## Acceptance Summary

GLM's central objection is correct: the literature-derived six-layer schema is a map, not the immediate execution target. The immediate target is narrower:

> Does true profile causally improve profile-sensitive outputs over empty/wrong profile under a blind, paired, reproducible evaluation?

The accepted next-step schema is therefore **Layer 1 + Layer 4 + Layer 6**, with Layer 3 guarded by the fixed-reference rule and deferred for now.

[质量喵（GPT）/GPT5.5喵🐾]

