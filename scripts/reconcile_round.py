#!/usr/bin/env python3
"""训练轮次切换核对脚本（一次性/按需运行）。

在开启新一轮训练（如 V0.1 → V1.0）时跑一次，做两件 validate_ceu.py 不做的事：
1. 汇总现有 CEU 库的概况（按卷/按 evidence_source/按 confidence 分布），
   给新一轮一个"起点快照"
2. 列出所有 status=superseded 的 CEU，提醒它们已不该被继续引用

不修改任何文件，只输出报告；实际的 schema 字段回填/证据重定位仍需人工或
ceu-extractor agent 处理。

用法：
    python3 reconcile_round.py <角色名>
"""
import argparse
import glob
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import yaml  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("character")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()

    root = args.root or os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    ceu_dir = os.path.join(root, "characters", args.character, "CEU")

    active = []
    superseded = []
    for path in sorted(glob.glob(os.path.join(ceu_dir, "*.yaml"))):
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, list):
            continue
        for rec in data:
            if not isinstance(rec, dict) or "event_id" not in rec:
                continue
            entry = (fname, rec)
            if rec.get("status") == "superseded":
                superseded.append(entry)
            else:
                active.append(entry)

    print(f"=== {args.character} CEU 库起点快照 ===\n")
    print(f"有效 CEU：{len(active)} 条 | 已废弃(superseded)：{len(superseded)} 条\n")

    by_source = Counter(rec.get("evidence_source", "self") for _, rec in active)
    by_conf = Counter(rec.get("confidence", "未标注") for _, rec in active)
    by_vol = Counter()
    for _, rec in active:
        eid = rec.get("event_id", "")
        parts = eid.split("-")
        vol = parts[1] if len(parts) > 1 else "未知"
        by_vol[vol] += 1

    print("按卷分布：", dict(by_vol))
    print("按 evidence_source 分布：", dict(by_source))
    print("按 confidence 分布：", dict(by_conf))

    if superseded:
        print(f"\n=== 已废弃（superseded），不应再被 Character OS 引用 ===")
        for fname, rec in superseded:
            print(f"  - {rec['event_id']} ({fname})")

    low_conf_active = [rec["event_id"] for _, rec in active if rec.get("confidence") == "low"]
    if low_conf_active:
        print(f"\n=== 有效但 confidence=low 的 CEU（新一轮可优先复核）===")
        for eid in low_conf_active:
            print(f"  - {eid}")

    print(f"\n提示：结构/引用完整性请另跑 `python3 validate_ceu.py {args.character}`，本脚本只做概况汇总。")


if __name__ == "__main__":
    main()
