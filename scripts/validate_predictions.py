# -*- coding: utf-8 -*-
"""验证全量消融预测输出：检查 12 个 pred 文件存在性、行数、格式，输出计数报告。

用法:
    python scripts/validate_predictions.py                        # 验证 ablation_v14
    python scripts/validate_predictions.py --dir ablation_v14_full  # 验证 n=291 全量
"""
import argparse
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE, "logs", "predictions")
DEFAULT_DIR = "ablation_v14"
ARMS = ["A", "B", "C"]
PARTS = ["part01", "part02", "part03", "part04"]

LINE = re.compile(r"^\s*#?\s*(\d+)\s*[|｜]\s*(.+?)\s*$")


def count_arena_slots(arena_path):
    """从 arena 文件统计 【#N】 数量。"""
    if not os.path.exists(arena_path):
        return 0
    with open(arena_path, encoding="utf-8") as f:
        text = f.read()
    return len(re.findall(r"【#\d+】", text))


def validate_predictions(D):
    """验证所有 12 个预测文件，返回 (ok, report_lines, errors)。"""
    errors = []
    lines = []
    lines.append("# 预测文件验证报告")
    lines.append("")
    lines.append(f"目录: {D}")
    lines.append("")

    # 各 part 的 arena slot 数
    expected_per_part = {}
    for p in PARTS:
        arena_path = os.path.join(D, f"arena_{p}.txt")
        expected_per_part[p] = count_arena_slots(arena_path)
    total_expected = sum(expected_per_part.values())

    lines.append("## Arena slot 分布")
    lines.append("")
    lines.append("| part | expected slots |")
    lines.append("|---|---:|")
    for p in PARTS:
        lines.append(f"| {p} | {expected_per_part[p]} |")
    lines.append(f"| **total** | **{total_expected}** |")
    lines.append("")

    # 逐一检查
    all_files = []
    for arm in ARMS:
        for part in PARTS:
            all_files.append((arm, part, f"pred_arm{arm}_{part}.md"))

    lines.append("## 逐文件检查")
    lines.append("")
    lines.append("| arm | part | 文件 | 存在 | 行数 | 期望 | 状态 |")
    lines.append("|---|---|---|---:|---:|---:|")

    total_lines = 0
    ok_count = 0
    for arm, part, fname in all_files:
        path = os.path.join(D, fname)
        exists = os.path.exists(path)
        if not exists:
            lines.append(f"| {arm} | {part} | {fname} | ❌ | - | {expected_per_part[part]} | 缺失 |")
            errors.append(f"缺失: {fname}")
            continue

        with open(path, encoding="utf-8") as f:
            content = f.read()

        raw_lines = content.strip().splitlines()
        pred_count = sum(1 for line in raw_lines if LINE.match(line.strip()))

        expected = expected_per_part[part]
        total_lines += pred_count

        if pred_count == expected:
            lines.append(
                f"| {arm} | {part} | {fname} | ✅ | {pred_count} | {expected} | 通过 |"
            )
            ok_count += 1
        else:
            delta = pred_count - expected
            lines.append(
                f"| {arm} | {part} | {fname} | ✅ | {pred_count} | {expected} | 偏差 {delta:+d} |"
            )
            errors.append(
                f"行数不符: {fname} ({pred_count} != {expected})"
            )

    lines.append(f"| **汇总** | | **{ok_count}/12** | | **{total_lines}** | **{total_expected}** | |")

    lines.append("")
    lines.append("## 判定")
    lines.append("")
    if ok_count == 12 and not errors:
        lines.append("✅ **全部通过** — 可进入 merge_blind / merge_style_blind。")
    else:
        lines.append(f"❌ **{len(errors)} 项问题**:")
        for e in errors:
            lines.append(f"  - {e}")
        lines.append("")
        lines.append("修复后重新运行本脚本。")

    report = "\n".join(lines) + "\n"
    all_ok = (ok_count == 12 and not errors)
    return all_ok, report, errors


def main():
    parser = argparse.ArgumentParser(
        description="验证消融预测文件完整性"
    )
    parser.add_argument(
        "--dir", default=DEFAULT_DIR,
        help=f"消融目录名（相对于 logs/predictions/，默认 {DEFAULT_DIR}）"
    )
    parser.add_argument(
        "--output", default=None,
        help="输出报告文件（相对于消融目录，默认 stdout）"
    )
    args = parser.parse_args()

    D = os.path.join(PRED_DIR, args.dir)
    if not os.path.isdir(D):
        print(f"错误：目录不存在 {D}")
        sys.exit(1)

    ok, report, errors = validate_predictions(D)

    if args.output:
        out_path = os.path.join(D, args.output)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已写入 {out_path}")

    print(report)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
