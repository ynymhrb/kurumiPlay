# -*- coding: utf-8 -*-
"""把三臂预测与 ground truth 合并成盲评分表。

每一项内部独立随机把三臂打乱成 X/Y/Z，映射写入 unblind_key.json。
主 agent 打分时只看 scoring_sheet.md，看不到 arm 身份。

用法:
    python scripts/merge_blind.py                          # 默认 ablation_v14
    python scripts/merge_blind.py --dir ablation_v14_full  # n=291 全量消融
"""
import argparse
import glob
import json
import os
import random
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE, "logs", "predictions")
DEFAULT_DIR = "ablation_v14"
ARMS = ["A", "B", "C"]
SEED = 20260728  # 固定种子，可复现

LINE = re.compile(r"^\s*#?\s*(\d+)\s*[|｜]\s*(.*?)\s*$")


def load_preds(arm, D):
    """加载某 arm 的所有预测。自动检测单文件 vs multi-part 结构。"""
    single = os.path.join(D, f"pred_arm{arm}.md")
    if os.path.exists(single):
        out = {}
        with open(single, encoding="utf-8") as f:
            for raw in f:
                m = LINE.match(raw)
                if m:
                    out[int(m.group(1))] = m.group(2)
        return out

    # n=200 multi-part: pred_arm{A,B,C}_part{01,02,03,04}.md
    parts = sorted(glob.glob(os.path.join(D, f"pred_arm{arm}_part*.md")))
    if not parts:
        raise FileNotFoundError(
            f"找不到 arm {arm} 的预测文件：{single} 或 pred_arm{arm}_part*.md 均不存在"
        )
    out = {}
    for path in parts:
        with open(path, encoding="utf-8") as f:
            for raw in f:
                m = LINE.match(raw)
                if m:
                    slot = int(m.group(1))
                    if slot in out:
                        print(f"警告：slot #{slot} 在多个 part 中出现，已覆盖")
                    out[slot] = m.group(2)
    return out


def load_gt(D):
    path = os.path.join(D, "gt_key.md")
    gt = {}
    with open(path, encoding="utf-8") as f:
        for raw in f:
            parts = [p.strip() for p in raw.strip().strip("|").split("|")]
            if len(parts) >= 5 and parts[0].isdigit():
                gt[int(parts[0])] = (parts[1], parts[2], parts[4])
            elif len(parts) >= 4 and parts[0].isdigit():
                gt[int(parts[0])] = (parts[1], parts[2], parts[3])
    return gt


def main():
    parser = argparse.ArgumentParser(
        description="合并三臂预测为盲评分表"
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

    rng = random.Random(SEED)
    gt = load_gt(D)
    preds = {a: load_preds(a, D) for a in ARMS}
    for a in ARMS:
        missing = sorted(set(gt) - set(preds[a]))
        print(f"arm {a}: {len(preds[a])} 条" + (f"，缺失 {missing}" if missing else "，无缺失"))

    key = {}
    rows = []
    for cid in sorted(gt):
        chunk, line, truth = gt[cid]
        order = ARMS[:]
        rng.shuffle(order)
        key[str(cid)] = dict(zip(["X", "Y", "Z"], order))
        rows.append((cid, chunk, line, truth, order))

    with open(os.path.join(D, "unblind_key.json"), "w", encoding="utf-8") as f:
        json.dump(key, f, ensure_ascii=False, indent=0)

    with open(os.path.join(D, "scoring_sheet.md"), "w", encoding="utf-8") as f:
        f.write("# 盲评分表（arm 身份已隐藏，逐项独立随机）\n\n")
        f.write("打分前禁止打开 unblind_key.json。规则见 rubric.md。\n\n")
        for cid, chunk, line, truth, order in rows:
            f.write(f"## #{cid}  [chunk {chunk} / L{line}]\n")
            f.write(f"- **GT**: {truth}\n")
            for lab, arm in zip(["X", "Y", "Z"], order):
                f.write(f"- {lab}: {preds[arm].get(cid, '(缺失)')}\n")
            f.write("\n")
    print("已生成 scoring_sheet.md 与 unblind_key.json")


if __name__ == "__main__":
    main()
