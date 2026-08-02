# -*- coding: utf-8 -*-
"""揭盲：读 scores_raw.md（主 agent 逐项对 X/Y/Z 打的分）+ unblind_key.json，
换算出各 arm 的两轴得分与分段得分。

scores_raw.md 期望格式，每行一项：
    #12 | X:1/1 | Y:0.5/0 | Z:1/-
即 内容分/语域分；语域不适用记 '-'。

用法:
    python scripts/unblind.py                          # 默认 ablation_v14
    python scripts/unblind.py --dir ablation_v14_full  # n=200 全量消融
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

ROW = re.compile(r"^\s*#?\s*(\d+)\s*\|(.*)$")
CELL = re.compile(r"([XYZ])\s*:\s*([0-9.]+)\s*/\s*([0-9.]+|-)")


def load_chunks(D):
    m = {}
    with open(os.path.join(D, "gt_key.md"), encoding="utf-8") as f:
        for raw in f:
            p = [x.strip() for x in raw.strip().strip("|").split("|")]
            if len(p) >= 3 and p[0].isdigit():
                m[int(p[0])] = p[1]
    return m


def main():
    parser = argparse.ArgumentParser(
        description="揭盲内容/语域评分"
    )
    parser.add_argument(
        "--dir", default=DEFAULT_DIR,
        help=f"消融目录名（相对于 logs/predictions/，默认 {DEFAULT_DIR}）"
    )
    args = parser.parse_args()

    D = os.path.join(PRED_DIR, args.dir)
    if not os.path.isdir(D):
        print(f"错误：目录不存在 {D}")
        return

    key_path = os.path.join(D, "unblind_key.json")
    if not os.path.exists(key_path):
        print(f"错误：{key_path} 不存在，先运行 merge_blind.py")
        return

    key = json.load(open(key_path, encoding="utf-8"))
    chunks = load_chunks(D)

    content = defaultdict(list)          # arm -> [score]
    register = defaultdict(list)         # arm -> [score]
    by_chunk = defaultdict(lambda: defaultdict(list))  # arm -> chunk -> [score]
    n_rows = 0

    with open(os.path.join(D, "scores_raw.md"), encoding="utf-8") as f:
        for raw in f:
            m = ROW.match(raw)
            if not m:
                continue
            cid = int(m.group(1))
            if str(cid) not in key:
                continue
            n_rows += 1
            for lab, c, r in CELL.findall(m.group(2)):
                arm = key[str(cid)][lab]
                content[arm].append(float(c))
                by_chunk[arm][chunks.get(cid, "?")].append(float(c))
                if r != "-":
                    register[arm].append(float(r))

    print(f"已解析 {n_rows} 项\n")
    print("| arm | 条件 | 内容准确率 | n | 语域正确率 | n |")
    print("|---|---|---|---|---|---|")
    names = {"A": "无 profile", "B": "错 profile", "C": "真 profile v0.10"}
    res = {}
    for a in ARMS:
        cs, rs = content[a], register[a]
        cm = sum(cs) / len(cs) if cs else 0
        rm = sum(rs) / len(rs) if rs else 0
        res[a] = cm
        print(f"| {a} | {names[a]} | {cm:.3f} | {len(cs)} | {rm:.3f} | {len(rs)} |")

    print("\n分段（内容准确率）：")
    print("| arm | chunk A 独处 | chunk B 对外公务 |")
    print("|---|---|---|")
    for a in ARMS:
        row = []
        for ch in ["A", "B"]:
            v = by_chunk[a][ch]
            row.append(f"{sum(v)/len(v):.3f} (n={len(v)})" if v else "-")
        print(f"| {a} | {row[0]} | {row[1]} |")

    print("\n对照差值：")
    print(f"  C − A (profile 边际贡献) = {res['C'] - res['A']:+.3f}")
    print(f"  B − C (喂错 profile 的代价) = {res['B'] - res['C']:+.3f}")
    print(f"  B − A (错 profile vs 无 profile) = {res['B'] - res['A']:+.3f}")
    n = len(content["A"]) or 1
    se = (0.25 / n) ** 0.5
    print(f"\n  单臂 SE 上界 ≈ {se:.3f}；差值 SE ≈ {se*1.41:.3f}；"
          f"按预注册口径，差值 <{se*2.83:.2f} 不宣称差异")


if __name__ == "__main__":
    main()
