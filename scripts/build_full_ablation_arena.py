# -*- coding: utf-8 -*-
"""构建 vol14 全量消融实验竞技场（4 段，全 291 占位符）。

从验证集和原文逐行对齐，为所有 {} 统一编号，产出 4 个 arena part 文件 + gt_key.md。

用法: python scripts/build_full_ablation_arena.py
输出: logs/predictions/ablation_v14_full/{arena_part01.txt, ..., arena_part04.txt, gt_key.md}
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "characters", "雅儿贝德", "source")
VAL = os.path.join(SRC, "雅儿贝德_第十四卷验证集.txt")
ORIG = os.path.join(SRC, "雅儿贝德_第十四卷原文.txt")
OUT = os.path.join(BASE, "logs", "predictions", "ablation_v14_full")

CHUNKS = [
    ("part01", 1, 500, "Pro/序章 + 谒见会议"),
    ("part02", 501, 1000, "王座厅宣战 + 战时会议"),
    ("part03", 1001, 1500, "战场 + 战斗指挥"),
    ("part04", 1501, 1965, "复盘会 + 拉娜 + 菲利浦"),
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def recover_fills(val_line, orig_line):
    """val_line 形如 'A{}B{}C'，用非贪婪正则从 orig_line 还原每个 {} 的内容。"""
    parts = val_line.split("{}")
    pattern = "^" + "(.*?)".join(re.escape(p) for p in parts) + "$"
    m = re.match(pattern, orig_line, re.S)
    if not m:
        return None
    return list(m.groups())


def main():
    val = load(VAL)
    orig = load(ORIG)
    assert len(val) == len(orig), "行数不一致，无法逐行对齐"
    os.makedirs(OUT, exist_ok=True)

    gt_rows = []
    counter = 0
    stats = {}

    for name, lo, hi, label in CHUNKS:
        arena_lines = []
        n_here = 0
        n_fail = 0
        for ln in range(lo, hi + 1):
            v = val[ln - 1]
            if "{}" not in v:
                arena_lines.append(f"{ln:>5}| {v}")
                continue
            fills = recover_fills(v, orig[ln - 1])
            k = v.count("{}")
            out = v
            for j in range(k):
                counter += 1
                n_here += 1
                out = out.replace("{}", f"【#{counter}】", 1)
                gt = (fills[j] if fills and j < len(fills) else "!!对齐失败,人工核对!!")
                if fills is None:
                    n_fail += 1
                gt_rows.append((counter, name, ln, label, gt))
            arena_lines.append(f"{ln:>5}| {out}")
        stats[name] = (n_here, n_fail)

        # Arena header
        header = [
            f"# vol14 full ablation arena {name}：《第十四卷》验证集 L{lo}-{hi}（{label}）",
            f"# 待填占位符 {n_here} 个",
            "# 行首数字为原文行号，仅供定位。",
            "# Prediction phase forbidden files: gt_key.md, original vol14 source, pred_arm*, scores*",
            "",
        ]
        with open(os.path.join(OUT, f"arena_{name}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(header))
            f.write("\n".join(arena_lines) + "\n")

    # gt_key.md
    with open(os.path.join(OUT, "gt_key.md"), "w", encoding="utf-8") as f:
        f.write("# Ground Truth 答案键（评分用，禁止在预测阶段提供给任何 arm）\n\n")
        f.write("| # | chunk | line | context | 原文内容 |\n|---|---|---|---|---|\n")
        for cid, ch, ln, ctx, gt in gt_rows:
            g = gt.replace("|", "\\|").replace("\n", " ")
            f.write(f"| {cid} | {ch} | {ln} | {ctx} | {g} |\n")

    # README summary
    total_fail = sum(v[1] for v in stats.values())
    item_counts = {k: v[0] for k, v in stats.items()}
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("# vol14 Full Ablation README\n\n")
        f.write("## Arena stats\n\n")
        f.write("| part | slots | align_failures |\n|---|---|---|\n")
        for name, (slots, fails) in stats.items():
            f.write(f"| {name} | {slots} | {fails} |\n")
        f.write(f"| **total** | **{counter}** | **{total_fail}** |\n")
        f.write(f"\nalignment_failures: {total_fail}\n")
        f.write(f"total_placeholders: {counter}\n")

    print("chunk stats (slots, align_failures):", stats)
    print("total slots:", counter)


if __name__ == "__main__":
    main()
