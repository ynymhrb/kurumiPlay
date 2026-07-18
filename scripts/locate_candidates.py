#!/usr/bin/env python3
"""候选场景定位脚本（见 spec/eval_protocol.md 第7节步骤1）。

对指定卷的原文按人名 grep 命中行号，自动聚类成 cluster 草稿，写入/更新
characters/<角色>/V<轮次>/CEU/_index_vol<N>.yaml，供后续两遍法抽取时参考。
只做机械定位，不判断是否构成 CEU。

用法：
    python3 locate_candidates.py <角色名> <卷号数字> [--round V1.0] [--gap 40] [--pad 15]

例：
    python3 locate_candidates.py 雅儿贝德 1
    python3 locate_candidates.py 雅儿贝德 3 --round V1.0
"""
import argparse
import os
import sys
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from _round_utils import resolve_round_dir  # noqa: E402

CJK_NUM = "〇一二三四五六七八九十百"
DIGIT_TO_CJK = {
    1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七",
    8: "八", 9: "九", 10: "十", 11: "十一", 12: "十二", 13: "十三", 14: "十四",
}


def cluster_letter(i):
    """0 -> A, 1 -> B ... 25 -> Z, 26 -> AA ..."""
    s = ""
    i += 1
    while i > 0:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def find_mentions(lines, name):
    return [i + 1 for i, line in enumerate(lines) if name in line]  # 1-indexed


def cluster_mentions(mentions, gap):
    if not mentions:
        return []
    clusters = [[mentions[0]]]
    for m in mentions[1:]:
        if m - clusters[-1][-1] <= gap:
            clusters[-1].append(m)
        else:
            clusters.append([m])
    return clusters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("character", help="角色名，如 雅儿贝德")
    ap.add_argument("volume", type=int, help="卷号数字，如 1 表示第一卷")
    ap.add_argument("--round", default=None, help="轮次目录名，如 V1.0；不传则用最新轮次")
    ap.add_argument("--gap", type=int, default=40, help="同cluster内相邻命中行最大间隔")
    ap.add_argument("--pad", type=int, default=15, help="line_range 相对首尾命中行的前后留白")
    ap.add_argument("--root", default=None, help="项目根目录，默认按脚本位置向上找")
    args = ap.parse_args()

    root = args.root or os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    round_dir = resolve_round_dir(root, args.character, args.round)
    vol_cjk = DIGIT_TO_CJK.get(args.volume)
    if vol_cjk is None:
        print(f"暂不支持卷号 {args.volume}（未在 DIGIT_TO_CJK 里定义中文数字映射）", file=sys.stderr)
        sys.exit(1)

    source_path = os.path.join(root, "characters", args.character, "source", "全文", f"第{vol_cjk}卷.txt")
    if not os.path.exists(source_path):
        print(f"找不到原文文件：{source_path}", file=sys.stderr)
        sys.exit(1)

    with open(source_path, encoding="utf-8") as f:
        lines = f.readlines()
    total_lines = len(lines)

    mentions = find_mentions(lines, args.character)
    clusters_raw = cluster_mentions(mentions, args.gap)

    clusters = []
    for i, group in enumerate(clusters_raw):
        lo = max(1, group[0] - args.pad)
        hi = min(total_lines, group[-1] + args.pad)
        clusters.append({
            "cluster_id": cluster_letter(i),
            "line_range": [lo, hi],
            "mention_lines": group,
            "brief": "",  # 待抽取时填写场景简述
            "status": "pending",
            "ceu_ids": [],
            "priority": "high" if len(group) >= 3 else "low",
            "notes": "",
        })

    index = {
        "source": f"characters/{args.character}/source/全文/第{vol_cjk}卷.txt",
        "total_lines": total_lines,
        "total_mention_lines": len(mentions),
        "last_scanned": "由 locate_candidates.py 自动生成，未经人工复核",
        "clusters": clusters,
        "progress_summary": {
            "clusters_total": len(clusters),
            "clusters_done": 0,
            "clusters_partial": 0,
            "clusters_pending": len(clusters),
            "processing_order": "sequential",
            "next_recommended": clusters[0]["cluster_id"] if clusters else None,
        },
        "usage_note": (
            "本文件由 scripts/locate_candidates.py 机械生成（按人名grep聚类），"
            "brief/priority/status 需要处理该cluster时填写/更新，不代表已判断是否构成CEU。"
        ),
    }

    out_dir = os.path.join(round_dir, "CEU")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"_index_vol{args.volume}.yaml")

    if os.path.exists(out_path):
        print(f"警告：{out_path} 已存在，不会覆盖。如需重新生成请先手动移开旧文件。", file=sys.stderr)
        sys.exit(2)

    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(index, f, allow_unicode=True, sort_keys=False, width=100)

    print(f"已生成 {out_path}：{len(mentions)} 处命中，聚类为 {len(clusters)} 个候选场景")


if __name__ == "__main__":
    main()
