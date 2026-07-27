# -*- coding: utf-8 -*-
"""构建消融实验竞技场：从验证集切出连续段落，为占位符统一编号；
并用逐行正则回填从原文提取 ground truth，产出评分用答案键。

用法: python scripts/build_ablation_arena.py
输出: logs/predictions/ablation_v14/{arena_A.txt, arena_B.txt, gt_key.md}
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "characters", "雅儿贝德", "source")
VAL = os.path.join(SRC, "雅儿贝德_第十四卷验证集.txt")
ORIG = os.path.join(SRC, "雅儿贝德_第十四卷原文.txt")
OUT = os.path.join(BASE, "logs", "predictions", "ablation_v14")

# (段名, 起始行, 结束行, 场景标签)
CHUNKS = [
    ("A", 1, 100, "Prologue 独处办公 / 内心独白为主"),
    ("B", 500, 700, "对外公务：会议与谒见"),
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
            out = v
            k = v.count("{}")
            ids = []
            for j in range(k):
                counter += 1
                n_here += 1
                ids.append(counter)
                out = out.replace("{}", f"【#{counter}】", 1)
                gt = fills[j] if fills else "!!对齐失败,人工核对!!"
                if fills is None:
                    n_fail += 1
                gt_rows.append((counter, name, ln, gt))
            arena_lines.append(f"{ln:>5}| {out}")
        stats[name] = (n_here, n_fail)
        with open(os.path.join(OUT, f"arena_{name}.txt"), "w", encoding="utf-8") as f:
            f.write(f"# 竞技场 {name}：《第十四卷》验证集 L{lo}-{hi}（{label}）\n")
            f.write(f"# 待填占位符 {n_here} 个，编号 #{gt_rows[-n_here][0]}~#{counter}\n")
            f.write("# 行首数字为原文行号，仅供定位。\n\n")
            f.write("\n".join(arena_lines) + "\n")

    with open(os.path.join(OUT, "gt_key.md"), "w", encoding="utf-8") as f:
        f.write("# Ground Truth 答案键（评分用，禁止在预测阶段提供给任何 arm）\n\n")
        f.write("| # | chunk | line | 原文内容 |\n|---|---|---|---|\n")
        for cid, ch, ln, gt in gt_rows:
            g = gt.replace("|", "\\|").replace("\n", " ")
            f.write(f"| {cid} | {ch} | {ln} | {g} |\n")

    print("chunk stats (slots, align_failures):", stats)
    print("total slots:", counter)


if __name__ == "__main__":
    main()
