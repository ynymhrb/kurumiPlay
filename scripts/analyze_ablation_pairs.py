# -*- coding: utf-8 -*-
"""Paired bootstrap reanalysis of vol14 three-arm ablation scores.

Replaces rough independent-proportion SE reasoning with paired item-level
bootstrap confidence intervals. Also computes a profile-sensitivity index:
for items where exploratory style-axis scores show B≠C, is |content_B - content_C|
larger than for items where style axes agree?

Usage: python scripts/analyze_ablation_pairs.py
Output: logs/predictions/ablation_v14/paired_stats.md
"""
import json
import os
import random
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(BASE, "logs", "predictions", "ablation_v14")
SEED = 20260728
N_BOOT = 10000

# ── Parsers ──────────────────────────────────────────────────────────────

def load_unblind_key():
    """Return dict: item_id(int) -> {X: arm, Y: arm, Z: arm}."""
    with open(os.path.join(D, "unblind_key.json"), encoding="utf-8") as f:
        raw = json.load(f)
    return {int(k): v for k, v in raw.items()}

def load_scores(key):
    """Return dict: item_id(int) -> {arm: {content: float|None, register: float|None}}."""
    ROW_RE = re.compile(r"^\s*#?\s*(\d+)\s*\|(.*)$")
    CELL_RE = re.compile(r"([XYZ])\s*:\s*([0-9.]+)\s*/\s*([0-9.]+|-)")
    rows = {}
    with open(os.path.join(D, "scores_raw.md"), encoding="utf-8") as f:
        for raw in f:
            m = ROW_RE.match(raw)
            if not m:
                continue
            cid = int(m.group(1))
            item_key = key.get(cid, {})
            values = {}
            for lab, content, register in CELL_RE.findall(m.group(2)):
                arm = item_key.get(lab)
                if arm is None:
                    continue
                values[arm] = {
                    "content": float(content),
                    "register": None if register == "-" else float(register),
                }
            rows[cid] = values
    return rows

def load_chunk_map():
    """Return dict: item_id(int) -> chunk_label(str)."""
    chunks = {}
    with open(os.path.join(D, "gt_key.md"), encoding="utf-8") as f:
        for raw in f:
            parts = [p.strip() for p in raw.strip().strip("|").split("|")]
            if len(parts) >= 3 and parts[0].isdigit():
                chunks[int(parts[0])] = parts[1]
    return chunks

def load_style_sensitivity():
    """Return dict: item_id(int) -> set of axis names where B≠C in exploratory scores.

    Reads style_axis_scores_exploratory.md rows, collects items where B != C
    on any axis. An item is 'style-sensitive' if at least one axis shows divergence.
    """
    AXIS_ROW_RE = re.compile(
        r"^\|\s*(\d+)\s*\|\s*(\w+)\s*\|.*\|\s*([01])\s*\|\s*([01])\s*\|\s*([01])\s*\|"
    )
    sensitive_ids = set()
    all_styled_ids = set()
    try:
        with open(os.path.join(D, "style_axis_scores_exploratory.md"), encoding="utf-8") as f:
            for raw in f:
                m = AXIS_ROW_RE.match(raw)
                if not m:
                    continue
                cid = int(m.group(1))
                ax = m.group(2)
                a_val = int(m.group(3))
                b_val = int(m.group(4))
                c_val = int(m.group(5))
                all_styled_ids.add(cid)
                if b_val != c_val:
                    sensitive_ids.add(cid)
    except FileNotFoundError:
        pass
    return sensitive_ids, all_styled_ids

# ── Bootstrap ────────────────────────────────────────────────────────────

def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0

def paired_diff(rows, left, right, field):
    """Return list of per-item paired differences."""
    ids = [
        cid for cid, vals in rows.items()
        if left in vals and right in vals
        and vals[left][field] is not None
        and vals[right][field] is not None
    ]
    return ids, [rows[cid][left][field] - rows[cid][right][field] for cid in ids]

def bootstrap_ci(diffs, n=N_BOOT, seed=SEED):
    """Return (mean_diff, ci95_low, ci95_high) from bootstrap of diffs list."""
    rng = random.Random(seed)
    n_items = len(diffs)
    boot_means = []
    for _ in range(n):
        sample = [rng.choice(diffs) for _ in range(n_items)]
        boot_means.append(mean(sample))
    boot_means.sort()
    lo = boot_means[int(0.025 * n)]
    hi = boot_means[int(0.975 * n)]
    return mean(diffs), lo, hi

# ── Sensitivity analysis ─────────────────────────────────────────────────

def sensitivity_report(rows, sensitive_ids, all_styled_ids):
    """For items with style-axis data, compare |B-C| content diffs in
    sensitive vs non-sensitive items."""
    sens_diffs = []
    nonsens_diffs = []
    for cid in all_styled_ids:
        if cid not in rows:
            continue
        vals = rows[cid]
        if "B" not in vals or "C" not in vals:
            continue
        b_c = abs(vals["B"]["content"] - vals["C"]["content"])
        if cid in sensitive_ids:
            sens_diffs.append(b_c)
        else:
            nonsens_diffs.append(b_c)
    return sens_diffs, nonsens_diffs

# ── Write report ─────────────────────────────────────────────────────────

def fmt_ci(est, lo, hi):
    return f"{est:+.3f}  [{lo:+.3f}, {hi:+.3f}]"

def main():
    key = load_unblind_key()
    rows = load_scores(key)
    chunks = load_chunk_map()
    sensitive_ids, all_styled_ids = load_style_sensitivity()

    lines = []
    lines.append("# Paired Bootstrap Reanalysis of vol14 Ablation")
    lines.append("")
    lines.append(f"Method: paired bootstrap, {N_BOOT} resamples, seed={SEED}.")
    lines.append(
        "Items are paired across arms (same slot, three different profile conditions). "
        "This is the correct analysis because the three arms predict exactly the same 79 slots."
    )
    lines.append("")

    # ── Main bootstrap table ──
    lines.append("## Bootstrap Confidence Intervals")
    lines.append("")
    lines.append("| field | pair | mean_diff | ci95 | n |")
    lines.append("|---|---:|---:|---:|")
    pairs = [("C", "A"), ("B", "C"), ("B", "A")]
    for field in ("content", "register"):
        for left, right in pairs:
            ids, diffs = paired_diff(rows, left, right, field)
            if not diffs:
                lines.append(f"| {field} | {left}-{right} | — | — | 0 |")
                continue
            est, lo, hi = bootstrap_ci(diffs)
            lines.append(
                f"| {field} | {left}-{right} | {est:+.3f} | [{lo:+.3f}, {hi:+.3f}] | {len(diffs)} |"
            )
    lines.append("")

    # ── Interpretation ──
    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "The paired bootstrap CIs are narrower than the rough independent-SE estimate "
        "(SE ≈ 0.056 per arm, 2×SE ≈ 0.112 for difference) because paired analysis "
        "removes between-item variance. If the CI for C-A excludes 0, the profile "
        "effect is detectable above noise. If the CI for B-C straddles 0, wrong and "
        "true profile are not reliably separated."
    )
    lines.append("")

    # ── Per-chunk breakdown ──
    lines.append("## Chunk Breakdown (content accuracy)")
    lines.append("")
    lines.append("| chunk | pair | mean_diff | n |")
    lines.append("|---|---:|---:|")
    for chunk_label in sorted(set(chunks.values())):
        subset = {
            cid: vals for cid, vals in rows.items()
            if chunks.get(cid) == chunk_label
        }
        for left, right in pairs:
            ids, diffs = paired_diff(subset, left, right, "content")
            if not diffs:
                lines.append(f"| {chunk_label} | {left}-{right} | — | 0 |")
                continue
            lines.append(
                f"| {chunk_label} | {left}-{right} | {mean(diffs):+.3f} | {len(diffs)} |"
            )
    lines.append("")

    # ── Profile-sensitivity index ──
    lines.append("## Profile-Sensitivity Index (exploratory)")
    lines.append("")
    lines.append(
        "Cross-reference with `style_axis_scores_exploratory.md`: for items where "
        "the exploratory style-axis B≠C (profile truly shifts expression), is the "
        "content-score |B-C| larger than for items where B=C on all style axes?"
    )
    lines.append("")
    sens, nonsens = sensitivity_report(rows, sensitive_ids, all_styled_ids)
    if sens or nonsens:
        lines.append("| group | n_items | mean |B-C| content |")
        lines.append("|---|---:|---:|")
        lines.append(
            f"| style-sensitive (B≠C on ≥1 axis) | {len(sens)} | {mean(sens):.3f} |"
        )
        lines.append(
            f"| style-insensitive (B=C on all axes) | {len(nonsens)} | {mean(nonsens):.3f} |"
        )
        lines.append("")
        if mean(sens) > mean(nonsens):
            lines.append(
                "Items with style-axis divergence show larger content-score B-C gaps, "
                "suggesting profile consumption leaks into content scoring even on the "
                "current coarse metric."
            )
        else:
            lines.append(
                "Style-axis divergence does not predict larger content-score gaps, "
                "consistent with the hypothesis that content accuracy is structurally "
                "blind to expression-layer effects."
            )
    else:
        lines.append("No style-axis sensitivity data available.")
    lines.append("")

    # ── Arm means (reference) ──
    lines.append("## Arm Means (reference only)")
    lines.append("")
    lines.append("| arm | content_mean | n | register_mean | n |")
    lines.append("|---|---:|---:|---:|---:|")
    for arm in ("A", "B", "C"):
        c_vals = [vals[arm]["content"] for vals in rows.values() if arm in vals and vals[arm]["content"] is not None]
        r_vals = [vals[arm]["register"] for vals in rows.values() if arm in vals and vals[arm]["register"] is not None]
        lines.append(
            f"| {arm} | {mean(c_vals):.3f} | {len(c_vals)} | {mean(r_vals):.3f} | {len(r_vals)} |"
        )
    lines.append("")

    # ── Method notes ──
    lines.append("## Method Notes")
    lines.append("")
    lines.append("- Bootstrap: 10 000 resamples with replacement, paired by item ID.")
    lines.append("- Register axis n=25; CIs reflect the low sample size.")
    lines.append("- Chunk breakdowns are descriptive (no bootstrap) due to small per-chunk n.")
    lines.append("- Profile-sensitivity index uses exploratory (non-blind) style-axis data; ")
    lines.append("  treat as diagnostic, not confirmatory.")

    out_path = os.path.join(D, "paired_stats.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path}")
    print(f"  Items parsed: {len(rows)}")
    print(f"  Chunks: {sorted(set(chunks.values()))}")
    print(f"  Style-sensitive items: {len(sensitive_ids)}")
    print(f"  All styled items: {len(all_styled_ids)}")


if __name__ == "__main__":
    main()
