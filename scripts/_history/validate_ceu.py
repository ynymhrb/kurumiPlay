#!/usr/bin/env python3
"""CEU 机械校验脚本（可自动化步骤，见 spec/eval_protocol.md 第7节步骤3）。

不判断内容是否合理，只做机械检查：
1. 必填字段是否齐全（self 来源的 CEU 要求更严格，others/narrator 走轻量schema）
2. event_id 在整个角色的 CEU 库里是否唯一
3. Character OS 文件（value_hierarchy/mental_models/decision_rules/relationship_rules/
   contradictions）里引用的 CEU 编号，是否都能在 CEU 库里找到；引用了 status=superseded
   文件（如 seed_fragments.yaml）里的 id 会单独警告

用法：
    python3 validate_ceu.py <角色名>

退出码：0=无错误（可能有警告），1=有错误
"""
import argparse
import glob
import os
import re
import sys
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from _round_utils import resolve_round_dir  # noqa: E402

ALWAYS_REQUIRED = ["event_id", "raw_text", "scene", "context", "participants", "evidence", "confidence"]
REQUIRED_IF_SELF = ["choice", "value_conflict", "chosen_value", "underlying_belief"]


def load_ceu_files(ceu_dir):
    """返回 {event_id: (file, record)}，以及按文件分组的记录列表"""
    records = {}
    duplicates = []
    by_file = {}
    for path in sorted(glob.glob(os.path.join(ceu_dir, "*.yaml"))):
        fname = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as e:
                print(f"[ERROR] {fname}: YAML 解析失败: {e}")
                continue
        if not data:
            continue
        # 只处理顶层是 list of CEU 的文件（_index_*.yaml 等索引文件顶层是dict，跳过）
        if not isinstance(data, list):
            continue
        items = data
        by_file[fname] = items
        for rec in items:
            if not isinstance(rec, dict) or "event_id" not in rec:
                continue
            eid = rec["event_id"]
            superseded = rec.get("status") == "superseded"  # 逐条判断，不是整文件级别
            if eid in records:
                duplicates.append((eid, records[eid][0], fname))
            else:
                records[eid] = (fname, rec, superseded)
    return records, duplicates, by_file


def validate_fields(eid, rec, fname):
    errors = []
    if rec.get("status") == "superseded":
        return [f"[INFO] {fname} {eid}: status=superseded，跳过字段完整性检查（历史遗留，不再作为有效证据）"]
    for field in ALWAYS_REQUIRED:
        if field not in rec or rec[field] in (None, ""):
            errors.append(f"[ERROR] {fname} {eid}: 缺少必填字段 `{field}`")
    source = rec.get("evidence_source", "self")
    if source == "self":
        for field in REQUIRED_IF_SELF:
            if field not in rec or rec[field] in (None, ""):
                errors.append(f"[ERROR] {fname} {eid}: evidence_source=self 但缺少 `{field}`")
    elif source in ("others", "narrator"):
        if "observation" not in rec and "limitation" not in rec:
            errors.append(f"[WARN] {fname} {eid}: evidence_source={source} 建议填 `observation`（轻量schema）")
    else:
        errors.append(f"[ERROR] {fname} {eid}: evidence_source 值非法: {source!r}（应为 self/others/narrator）")
    return errors


def find_ceu_references(character_dir):
    """扫描 Character OS 的 .md 文件，找形如 XXXX-Vn-... 的CEU编号引用"""
    pattern = re.compile(r"\b[A-Z]{2,6}-[A-Z0-9]+-[A-Z0-9]+-\d{3}\b")
    refs = {}
    for path in glob.glob(os.path.join(character_dir, "*.md")):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        found = set(pattern.findall(text))
        if found:
            refs[os.path.basename(path)] = found
    return refs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("character", help="角色名，如 雅儿贝德")
    ap.add_argument("--round", default=None, help="轮次目录名，如 V1.0；不传则用最新轮次")
    ap.add_argument("--root", default=None)
    args = ap.parse_args()

    root = args.root or os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    character_dir = resolve_round_dir(root, args.character, args.round)
    ceu_dir = os.path.join(character_dir, "CEU")

    if not os.path.isdir(ceu_dir):
        print(f"找不到 CEU 目录：{ceu_dir}", file=sys.stderr)
        sys.exit(1)

    records, duplicates, by_file = load_ceu_files(ceu_dir)

    all_msgs = []
    for eid, (fname, rec, superseded) in records.items():
        all_msgs.extend(validate_fields(eid, rec, fname))

    for eid, first_file, dup_file in duplicates:
        all_msgs.append(f"[ERROR] event_id 重复: {eid} 同时出现在 {first_file} 和 {dup_file}")

    superseded_ids = {eid for eid, (fname, rec, sup) in records.items() if sup}

    refs = find_ceu_references(character_dir)
    known_ids = set(records.keys())
    for md_file, ids in refs.items():
        for eid in ids:
            if eid not in known_ids:
                all_msgs.append(f"[ERROR] {md_file} 引用了不存在的 CEU 编号: {eid}")
            elif eid in superseded_ids:
                all_msgs.append(f"[WARN] {md_file} 引用了已标记 superseded 的 CEU 编号: {eid}")

    errors = [m for m in all_msgs if m.startswith("[ERROR]")]
    warnings = [m for m in all_msgs if m.startswith("[WARN]")]

    for m in all_msgs:
        print(m)

    gaps = [(eid, fname) for eid, (fname, rec, sup) in records.items() if rec.get("schema_gap")]
    if gaps:
        print(f"\n=== schema_gap 信号（{len(gaps)}条，应汇总进 logs/schema_gaps.md 供下次schema复核处理）===")
        for eid, fname in gaps:
            print(f"  - {eid} ({fname})")

    print(f"\n共检查 {len(records)} 条 CEU（{len(by_file)} 个文件）。"
          f"{len(errors)} 个错误，{len(warnings)} 个警告，{len(gaps)} 个未处理的 schema_gap 信号。")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
