# -*- coding: utf-8 -*-
"""揭盲风格轴评分：读 style_scores_raw.md（冷 judge 逐项对 X/Y/Z 打的五轴分）
+ style_unblind_key.json，换算出各 arm 的 per-axis 得分与 all_style_cells 汇总。

style_scores_raw.md 期望格式，每行一项：
    #49 | first_person X:1 Y:0 Z:- | attribution_source X:1 Y:- Z:0 | ...

每项必须包含全部五个轴。0/1/- 三档：- 不计分母。

用法:
    # 默认路径（原始评分）
    $env:PYTHONIOENCODING='utf-8'; python scripts/unblind_style.py

    # 独立评分路径（Gate 3 重跑）
    $env:PYTHONIOENCODING='utf-8'; python scripts/unblind_style.py --input style_scores_raw_independent.md --output style_scores_independent.md

    # n=200 全量消融
    $env:PYTHONIOENCODING='utf-8'; python scripts/unblind_style.py --dir ablation_v14_full
"""
import argparse
import json
import os
import re
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE, "logs", "predictions")
DEFAULT_DIR = "ablation_v14"
ARMS = ["A", "B", "C"]

AXES = [
    "first_person",
    "attribution_source",
    "stance_register",
    "emotion_channel",
    "sentence_dynamics",
]

ROW = re.compile(r"^\s*#?\s*(\d+)\s*\|(.*)$")
AXIS_CELL = re.compile(
    r"(\w+)\s+X:(-?\S+)\s+Y:(-?\S+)\s+Z:(-?\S+)"
)


def load_chunks(D):
    m = {}
    with open(os.path.join(D, "gt_key.md"), encoding="utf-8") as f:
        for raw in f:
            p = [x.strip() for x in raw.strip().strip("|").split("|")]
            if len(p) >= 3 and p[0].isdigit():
                m[int(p[0])] = p[1]
    return m


def main():
    parser = argparse.ArgumentParser(description="揭盲风格轴评分")
    parser.add_argument(
        "--dir", default=DEFAULT_DIR,
        help=f"消融目录名（相对于 logs/predictions/，默认 {DEFAULT_DIR}）"
    )
    parser.add_argument(
        "--input", default="style_scores_raw.md",
        help="输入原始评分文件（相对于消融目录，默认 style_scores_raw.md）"
    )
    parser.add_argument(
        "--output", default="style_scores.md",
        help="输出揭盲结果文件（相对于 消融目录，默认 style_scores.md）"
    )
    args = parser.parse_args()

    D = os.path.join(PRED_DIR, args.dir)
    if not os.path.isdir(D):
        print(f"错误：目录不存在 {D}")
        return

    key_path = os.path.join(D, "style_unblind_key.json")
    raw_path = os.path.join(D, args.input)
    out_path = os.path.join(D, args.output)

    if not os.path.exists(key_path):
        print(f"错误：{key_path} 不存在，先运行 merge_style_blind.py")
        return
    if not os.path.exists(raw_path):
        print(f"错误：{raw_path} 不存在，冷 judge 还没打分")
        return

    key = json.load(open(key_path, encoding="utf-8"))
    chunks = load_chunks(D)

    # arm -> axis -> [0/1 scores]
    axis_scores = {a: {ax: [] for ax in AXES} for a in ARMS}
    # arm -> [all 0/1 scores across axes]
    all_cells = {a: [] for a in ARMS}
    n_rows = 0
    missing_arms_rows = 0

    with open(raw_path, encoding="utf-8") as f:
        for raw in f:
            m = ROW.match(raw)
            if not m:
                continue
            cid = int(m.group(1))
            if str(cid) not in key:
                continue
            n_rows += 1
            rest = m.group(2)

            found_axes = set()
            for ax_name, xv, yv, zv in AXIS_CELL.findall(rest):
                if ax_name not in AXES:
                    continue
                found_axes.add(ax_name)
                for lab, val in [("X", xv), ("Y", yv), ("Z", zv)]:
                    arm = key[str(cid)][lab]
                    if val != "-":
                        try:
                            score = int(val)
                            axis_scores[arm][ax_name].append(score)
                            all_cells[arm].append(score)
                        except ValueError:
                            pass

            if len(found_axes) < 5:
                missing_arms_rows += 1

    print(f"已解析 {n_rows} 项")
    if missing_arms_rows:
        print(f"警告：{missing_arms_rows} 项未包含全部五个轴")

    # 逐臂汇总
    names = {"A": "无 profile", "B": "错 profile", "C": "真 profile v0.10"}

    lines = []
    lines.append("# 风格轴盲评揭盲结果")
    lines.append("")
    lines.append(f"解析项数：{n_rows}")
    lines.append("")
    lines.append("## Per-Axis 汇总")
    lines.append("")
    lines.append("| axis | A | n_A | B | n_B | C | n_C | C-A | C-B |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")

    per_axis_means = {}
    for ax in AXES:
        ms = {}
        ns = {}
        for a in ARMS:
            vs = axis_scores[a][ax]
            ms[a] = sum(vs) / len(vs) if vs else 0.0
            ns[a] = len(vs)
        per_axis_means[ax] = ms
        ca = ms["C"] - ms["A"]
        cb = ms["C"] - ms["B"]
        lines.append(
            f"| {ax} | {ms['A']:.3f} | {ns['A']} | {ms['B']:.3f} | {ns['B']} | {ms['C']:.3f} | {ns['C']} | {ca:+.3f} | {cb:+.3f} |"
        )

    # all_style_cells
    ac = {}
    an = {}
    for a in ARMS:
        vs = all_cells[a]
        ac[a] = sum(vs) / len(vs) if vs else 0.0
        an[a] = len(vs)

    lines.append("")
    lines.append("## All Style Cells 汇总")
    lines.append("")
    lines.append(
        f"| all_style_cells | {ac['A']:.3f} | {an['A']} | {ac['B']:.3f} | {an['B']} | {ac['C']:.3f} | {an['C']} | {ac['C']-ac['A']:+.3f} | {ac['C']-ac['B']:+.3f} |"
    )

    # 对照
    lines.append("")
    lines.append("## 对照")
    lines.append("")
    lines.append(f"- **C − A** (true profile 边际贡献) = {ac['C']-ac['A']:+.3f}")
    lines.append(f"- **C − B** (true vs wrong profile) = {ac['C']-ac['B']:+.3f}")
    lines.append(f"- **B − A** (wrong profile vs none) = {ac['B']-ac['A']:+.3f}")

    # 与探索性评分对照
    lines.append("")
    lines.append("## 与探索性（非盲）评分对照")
    lines.append("")
    lines.append("| axis | 探索-C | 盲评-C | 探索-C-A | 盲评-C-A | 探索-C-B | 盲评-C-B |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")

    # Task 1 exploratory values from style_axis_scores_exploratory.md
    exploratory = {
        "first_person": {"A": 0.250, "B": 0.100, "C": 0.300},
        "attribution_source": {"A": 0.500, "B": 0.167, "C": 0.500},
        "stance_register": {"A": 0.167, "B": 0.167, "C": 0.500},
        "emotion_channel": {"A": 0.182, "B": 0.364, "C": 0.273},
        "sentence_dynamics": {"A": 0.143, "B": 0.143, "C": 0.143},
        "all_style_cells": {"A": 0.240, "B": 0.180, "C": 0.320},
    }

    for ax in AXES + ["all_style_cells"]:
        if ax == "all_style_cells":
            e = exploratory[ax]
            bC = ac["C"]
            bA = ac["A"]
            bB = ac["B"]
            eCA = e["C"] - e["A"]
            eCB = e["C"] - e["B"]
            bCA = bC - bA
            bCB = bC - bB
        else:
            e = exploratory[ax]
            bC = per_axis_means[ax]["C"]
            bA = per_axis_means[ax]["A"]
            bB = per_axis_means[ax]["B"]
            eCA = e["C"] - e["A"]
            eCB = e["C"] - e["B"]
            bCA = bC - bA
            bCB = bC - bB
        lines.append(
            f"| {ax} | {e['C']:.3f} | {bC:.3f} | {eCA:+.3f} | {bCA:+.3f} | {eCB:+.3f} | {bCB:+.3f} |"
        )

    # 分段（chunk A 独处 / chunk B 对外公务）
    lines.append("")
    lines.append("## 分段（all_style_cells）")
    lines.append("")
    lines.append("| arm | chunk A 独处 | chunk B 对外公务 |")
    lines.append("|---|---|---|")
    by_chunk = {a: {ch: [] for ch in ["A", "B"]} for a in ARMS}
    for a in ARMS:
        for ch in ["A", "B"]:
            pass  # populated below

    # Re-scan raw to get per-chunk breakdown
    with open(raw_path, encoding="utf-8") as f:
        for raw in f:
            m = ROW.match(raw)
            if not m:
                continue
            cid = int(m.group(1))
            if str(cid) not in key:
                continue
            ch = chunks.get(cid, "?")
            if ch not in ["A", "B"]:
                continue
            rest = m.group(2)
            for ax_name, xv, yv, zv in AXIS_CELL.findall(rest):
                if ax_name not in AXES:
                    continue
                for lab, val in [("X", xv), ("Y", yv), ("Z", zv)]:
                    arm = key[str(cid)][lab]
                    if val != "-":
                        try:
                            by_chunk[arm][ch].append(int(val))
                        except ValueError:
                            pass

    for a in ARMS:
        row_parts = []
        for ch in ["A", "B"]:
            vs = by_chunk[a][ch]
            row_parts.append(
                f"{sum(vs)/len(vs):.3f} (n={len(vs)})" if vs else "-"
            )
        lines.append(f"| {a} | {row_parts[0]} | {row_parts[1]} |")

    result = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result)

    # 同时输出到 stdout
    print(result)


if __name__ == "__main__":
    main()
