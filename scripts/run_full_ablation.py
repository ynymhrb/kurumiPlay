# -*- coding: utf-8 -*-
"""全量消融实验端到端编排器。

流程:
  1. validate   — 检查 12 个 pred_arm*_part*.md 完整性
  2. blind      — merge_blind → 生成 scoring_sheet.md（内容轴）
  3. unblind    — 读 scores_raw.md → unblind → scores.md（内容轴揭盲）
  4. style-blind — merge_style_blind → 生成 style_scoring_sheet.md（风格轴）
  5. style-unblind — 读 style_scores_raw.md → unblind_style → style_scores.md（风格轴揭盲）
  6. report     — 生成计数报告

步骤 3 和 5 需要人工打分的中间产物（scores_raw.md / style_scores_raw.md）。
分阶段运行，未完成前一步则中止并提示下一步。

用法:
    # 全流程（默认 ablation_v14_full）
    python scripts/run_full_ablation.py

    # 只验证
    python scripts/run_full_ablation.py --stage validate

    # 从 blind 开始（前提：预测已完成）
    python scripts/run_full_ablation.py --stage blind

    # n=79 小样本
    python scripts/run_full_ablation.py --dir ablation_v14
"""
import argparse
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED_DIR = os.path.join(BASE, "logs", "predictions")
DEFAULT_DIR = "ablation_v14_full"

STAGES = ["validate", "blind", "unblind", "style-blind", "style-unblind", "report"]


def run_script(script_name, args_list, cwd=BASE):
    """运行 Python 脚本，返回 (exit_code, stdout)。"""
    cmd = [sys.executable, f"scripts/{script_name}"] + args_list
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            encoding="utf-8", errors="replace"
        )
        return result.returncode, result.stdout
    except Exception as e:
        return 1, str(e)


def stage_validate(D):
    """阶段 1：验证 12 个预测文件。"""
    print("=" * 60)
    print("Stage 1/6: validate — 验证预测文件完整性")
    print("=" * 60)
    code, out = run_script("validate_predictions.py", ["--dir", os.path.basename(D)])
    print(out)
    return code == 0


def stage_blind(D):
    """阶段 2：内容轴盲合并。"""
    print("=" * 60)
    print("Stage 2/6: blind — 生成内容轴盲评分表")
    print("=" * 60)
    code, out = run_script("merge_blind.py", ["--dir", os.path.basename(D)])
    print(out)
    if code != 0:
        return False
    sheet = os.path.join(D, "scoring_sheet.md")
    if os.path.exists(sheet):
        print(f"✅ 已生成 {sheet}")
        print(f"\n⚠️  下一步：人工冷 judge 逐项给 X/Y/Z 打内容分，写入 scores_raw.md（格式见 sheet 头部）\n"
              f"   打分完后再运行: python scripts/run_full_ablation.py --stage unblind --dir {os.path.basename(D)}")
    return True


def stage_unblind(D):
    """阶段 3：内容轴揭盲。"""
    print("=" * 60)
    print("Stage 3/6: unblind — 内容轴揭盲")
    print("=" * 60)
    raw = os.path.join(D, "scores_raw.md")
    if not os.path.exists(raw):
        print(f"❌ 缺少 {raw}，先人工打分再运行本阶段。")
        return False
    code, out = run_script("unblind.py", ["--dir", os.path.basename(D)])
    print(out)
    return code == 0


def stage_style_blind(D):
    """阶段 4：风格轴盲合并。"""
    print("=" * 60)
    print("Stage 4/6: style-blind — 生成风格轴盲评分表")
    print("=" * 60)
    code, out = run_script("merge_style_blind.py", ["--dir", os.path.basename(D)])
    print(out)
    if code != 0:
        return False
    sheet = os.path.join(D, "style_scoring_sheet.md")
    if os.path.exists(sheet):
        print(f"✅ 已生成 {sheet}")
        print(f"\n⚠️  下一步：人工冷 judge 逐项给五轴打分，写入 style_scores_raw.md\n"
              f"   打分完后再运行: python scripts/run_full_ablation.py --stage style-unblind --dir {os.path.basename(D)}")
    return True


def stage_style_unblind(D):
    """阶段 5：风格轴揭盲。"""
    print("=" * 60)
    print("Stage 5/6: style-unblind — 风格轴揭盲")
    print("=" * 60)
    raw = os.path.join(D, "style_scores_raw.md")
    if not os.path.exists(raw):
        print(f"❌ 缺少 {raw}，先人工打分再运行本阶段。")
        return False
    code, out = run_script("unblind_style.py", [
        "--dir", os.path.basename(D),
        "--input", "style_scores_raw.md",
        "--output", "style_scores.md",
    ])
    print(out)
    return code == 0


def stage_report(D):
    """阶段 6：计数报告。"""
    print("=" * 60)
    print("Stage 6/6: report — 生成计数报告")
    print("=" * 60)

    # 重组 count_report.md
    lines = []
    lines.append("# 全量消融实验计数报告")
    lines.append("")
    lines.append(f"目录: {D}")
    lines.append("")

    # 预测数量
    lines.append("## 预测输出")
    lines.append("")
    parts = ["part01", "part02", "part03", "part04"]
    arms = ["A", "B", "C"]
    total_preds = 0
    for arm in arms:
        arm_total = 0
        for p in parts:
            fname = f"pred_arm{arm}_{p}.md"
            path = os.path.join(D, fname)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    count = sum(1 for line in f if line.strip() and not line.startswith("#"))
                arm_total += count
        lines.append(f"- Arm {arm}: {arm_total} 条预测")
        total_preds += arm_total
    lines.append(f"- **总计**: {total_preds} 条预测（12 文件）")
    lines.append("")

    # 评分结果
    lines.append("## 评分结果")
    lines.append("")

    scores_path = os.path.join(D, "scores.md")
    if os.path.exists(scores_path):
        lines.append(f"- 内容轴: `scores.md` ✅")
    else:
        lines.append(f"- 内容轴: 未完成")

    style_scores_path = os.path.join(D, "style_scores.md")
    if os.path.exists(style_scores_path):
        lines.append(f"- 风格轴: `style_scores.md` ✅")
    else:
        lines.append(f"- 风格轴: 未完成")

    lines.append("")

    # 文件清单
    lines.append("## 产物清单")
    lines.append("")
    lines.append("| 文件 | 用途 | 存在 |")
    lines.append("|---|---|---|")
    artifacts = [
        ("pred_arm*_part*.md", "12 文件原始预测", False),
        ("scoring_sheet.md", "内容轴盲评分表", False),
        ("unblind_key.json", "内容轴盲映射", False),
        ("scores_raw.md", "内容轴人工分", False),
        ("scores.md", "内容轴揭盲结果", False),
        ("style_scoring_sheet.md", "风格轴盲评分表", False),
        ("style_unblind_key.json", "风格轴盲映射", False),
        ("style_scores_raw.md", "风格轴人工分", False),
        ("style_scores.md", "风格轴揭盲结果", False),
    ]
    import glob as _glob
    for pattern, purpose, _ in artifacts:
        matches = _glob.glob(os.path.join(D, pattern))
        lines.append(f"| {pattern} | {purpose} | {'✅' if matches else '❌'} |")

    report = "\n".join(lines) + "\n"
    out_path = os.path.join(D, "count_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(report)
    print(f"\n报告已写入 {out_path}")
    return True


STAGE_FN = {
    "validate": stage_validate,
    "blind": stage_blind,
    "unblind": stage_unblind,
    "style-blind": stage_style_blind,
    "style-unblind": stage_style_unblind,
    "report": stage_report,
}


def main():
    parser = argparse.ArgumentParser(
        description="全量消融实验端到端编排器"
    )
    parser.add_argument(
        "--dir", default=DEFAULT_DIR,
        help=f"消融目录名（相对于 logs/predictions/，默认 {DEFAULT_DIR}）"
    )
    parser.add_argument(
        "--stage", default="auto", choices=["auto"] + STAGES,
        help="起始阶段。auto = 自动检测未完成步骤从断点继续；"
             "指定阶段名 = 从该阶段运行到 report"
    )
    args = parser.parse_args()

    D = os.path.join(PRED_DIR, args.dir)
    if not os.path.isdir(D):
        print(f"错误：目录不存在 {D}")
        sys.exit(1)

    print(f"消融目录: {D}")

    if args.stage == "auto":
        # 自动检测断点
        if not os.path.exists(os.path.join(D, "scoring_sheet.md")):
            # 无 scoring_sheet → 从 validate 开始
            start_idx = 0
        elif not os.path.exists(os.path.join(D, "scores.md")):
            # 有 blind 产物但没揭盲 → 从 unblind 开始
            start_idx = STAGES.index("unblind")
        elif not os.path.exists(os.path.join(D, "style_scoring_sheet.md")):
            # 内容轴完成但没风格轴 → 从 style-blind 开始
            start_idx = STAGES.index("style-blind")
        elif not os.path.exists(os.path.join(D, "style_scores.md")):
            # 风格盲评有但没揭盲 → 从 style-unblind 开始
            start_idx = STAGES.index("style-unblind")
        else:
            # 全部完成 → 生成 report
            start_idx = STAGES.index("report")
        print(f"自动检测: 从 {STAGES[start_idx]} 开始\n")
    else:
        start_idx = STAGES.index(args.stage)

    stages_to_run = STAGES[start_idx:]

    for stage in stages_to_run:
        if not STAGE_FN[stage](D):
            print(f"\n❌ {stage} 阶段未通过，停止。修复问题后重试。")
            sys.exit(1)
        print()

    print("✅ 全流程完成。")

    # 最终 artifact 检查
    final = [os.path.join(D, f) for f in ["scores.md", "style_scores.md", "count_report.md"]]
    missing = [f for f in final if not os.path.exists(f)]
    if missing:
        print(f"\n⚠️  以下产物缺失: {missing}")
    else:
        print(f"产物就绪: scores.md, style_scores.md, count_report.md")


if __name__ == "__main__":
    main()
