---
feature_ids:
  - character-eval-validity
topics:
  - full-ablation
  - prep-gate
  - alignment
doc_kind: quality_gate_report
created: 2026-08-02
owner: "@cat-faziug16"
reviewed_commit: "4a65e03"
lead_plan: "project-research/2026-08-02-opus-research-plan.md"
---

# Gate 4 Prep Quality Report

Status: **fail**

Reviewed artifacts:

- `scripts/build_full_ablation_arena.py`
- `scripts/build_full_item_map.py`
- `logs/predictions/ablation_v14_full/README.md`
- `logs/predictions/ablation_v14_full/arena_part01.txt`
- `logs/predictions/ablation_v14_full/arena_part02.txt`
- `logs/predictions/ablation_v14_full/arena_part03.txt`
- `logs/predictions/ablation_v14_full/arena_part04.txt`
- `logs/predictions/ablation_v14_full/gt_key.md`
- `logs/predictions/ablation_v14_full/full_item_map.md`
- `logs/predictions/ablation_v14_full/task_spec_armA.md`
- `logs/predictions/ablation_v14_full/task_spec_armB.md`
- `logs/predictions/ablation_v14_full/task_spec_armC.md`

## Checks

| Check | Result | Evidence |
|---|---|---|
| Prep commit exists and is scoped to prep files | pass | `4a65e03` contains arena files, `gt_key.md`, `full_item_map.md`, three task specs, and two build scripts. |
| No prediction outputs committed | pass | `logs/predictions/ablation_v14_full/` contains no `pred_arm*.md` files. |
| Arena placeholder counts match README | pass | part01=94, part02=43, part03=94, part04=60, total=291. |
| `gt_key.md` row count matches arena slots | pass | `gt_key.md` contains 291 numbered rows. |
| `full_item_map.md` row count matches planned scoring items | pass | `full_item_map.md` contains 200 `V` rows. |
| Task specs include allowed/forbidden file boundaries | pass | Arm A/B/C specs list allowed arena/protocol/profile files and forbid `gt_key.md`, source files, prior scored artifacts, and web search. |
| Build scripts reproduce committed prep | **fail** | Re-running `build_full_ablation_arena.py` changes `README.md` and `gt_key.md`, reintroducing one alignment failure at #226. |

## Blocking Finding

`build_full_ablation_arena.py` is not currently reproducible against the committed prep.

Fresh command:

```powershell
$env:PYTHONIOENCODING='utf-8'; python scripts\build_full_ablation_arena.py; python scripts\build_full_item_map.py
```

Observed script output:

```text
chunk stats (slots, align_failures): {'part01': (94, 0), 'part02': (43, 0), 'part03': (94, 1), 'part04': (60, 0)}
total slots: 291
```

Generated diff:

```diff
-| part03 | 94 | 0 |
+| part03 | 94 | 1 |
-| **total** | **291** | **0** |
+| **total** | **291** | **1** |
-alignment_failures: 0
+alignment_failures: 1
-| 226 | part03 | 1413 | 战场 + 战斗指挥 | 想继续冲去的雅儿贝德 |
+| 226 | part03 | 1413 | 战场 + 战斗指挥 | !!对齐失败,人工核对!! |
```

Root cause evidence:

```text
validation L1413: 安兹阻止了{}。
original   L1413: 安兹阻止想继续冲去的雅儿贝德。
```

The committed `gt_key.md` manually resolves #226 as `想继续冲去的雅儿贝德`, which appears semantically correct. The problem is that this manual override is not encoded in the build script or documented in README. Therefore the prep claims `alignment_failures: 0`, but a fresh rebuild produces `alignment_failures: 1`.

## Decision

Gate 4 prep does **not** pass yet.

Do not run the 12 full-ablation prediction jobs until the prep is reproducible.

## Required Fix

DS should make one of these fixes:

1. Add an explicit manual override for slot #226 / L1413 in `build_full_ablation_arena.py`, then report both:
   - `auto_alignment_failures: 1`
   - `manual_overrides: 1`
   - `unresolved_alignment_failures: 0`
2. Or change the build process so L1413 aligns automatically and a fresh rebuild has no diff.

After the fix:

```powershell
$env:PYTHONIOENCODING='utf-8'; python scripts\build_full_ablation_arena.py; python scripts\build_full_item_map.py
git diff --exit-code -- logs/predictions/ablation_v14_full scripts/build_full_ablation_arena.py scripts/build_full_item_map.py
```

must exit 0.

Then route back to Quality喵 for prep gate recheck.

[质量喵（GPT5.5）/gpt-5.5🐾]

