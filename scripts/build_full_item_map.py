# -*- coding: utf-8 -*-
"""从 vol14_blind.md 生成 200-item V-number 视角的 full_item_map.md。

每行 = 一个 V-number (200 行)，映射到 arena slot(s)。
"""
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "logs", "predictions", "ablation_v14_full")

CHUNKS = [
    ("part01", 1, 500, "Pro/序章+谒见会议"),
    ("part02", 501, 1000, "王座厅宣战+战时会议"),
    ("part03", 1001, 1500, "战场+战斗指挥"),
    ("part04", 1501, 1965, "复盘会+拉娜+菲利浦"),
]


def get_chunk(line_num):
    for name, lo, hi, _ in CHUNKS:
        if lo <= line_num <= hi:
            return name
    return "???"


def get_chunk_label(line_num):
    for _, lo, hi, label in CHUNKS:
        if lo <= line_num <= hi:
            return label
    return "???"


def parse_v_entries(blind_path):
    """返回 [(v_num, [(line, slot_index), ...]), ...] 200 项。"""
    v_pat = re.compile(r"\*\*V(\d+)\.\s*L([^*]+)\*\*")
    entries = []

    with open(blind_path, encoding="utf-8") as f:
        for line in f:
            m = v_pat.search(line)
            if not m:
                continue
            v_num = int(m.group(1))
            line_ref = m.group(2).strip()
            targets = parse_line_ref(line_ref)
            entries.append((v_num, targets))
    return entries


def parse_line_ref(ref):
    """解析为 [(line_num, slot_index), ...]"""
    ref = ref.strip()
    segments = ref.split("+")
    results = []

    for seg in segments:
        seg = seg.strip()
        if "-" in seg and not any(c.isalpha() for c in seg.replace("-", "")):
            lo, hi = seg.split("-")
            for ln in range(int(lo), int(hi) + 1):
                results.append((ln, 0))
        elif re.match(r"^L?(\d+)([a-z])$", seg):
            m = re.match(r"^L?(\d+)([a-z])$", seg)
            results.append((int(m.group(1)), ord(m.group(2)) - ord('a')))
        elif re.match(r"^L?(\d+)([a-z])-([a-z])$", seg):
            m = re.match(r"^L?(\d+)([a-z])-([a-z])$", seg)
            ln = int(m.group(1))
            for si in range(ord(m.group(2)) - ord('a'), ord(m.group(3)) - ord('a') + 1):
                results.append((ln, si))
        elif re.match(r"^L?(\d+)$", seg):
            results.append((int(re.match(r"^L?(\d+)$", seg).group(1)), 0))
    return results


def build_arena_slot_map(arena_dir):
    """(line_num, slot_index) → arena_number"""
    mapping = {}
    for part_name, _, _, _ in CHUNKS:
        path = os.path.join(arena_dir, f"arena_{part_name}.txt")
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^\s*(\d+)\|", line)
                if not m:
                    continue
                line_num = int(m.group(1))
                arena_nums = re.findall(r"【#(\d+)】", line)
                for si, an in enumerate(arena_nums):
                    mapping[(line_num, si)] = int(an)
    return mapping


def main():
    blind_path = os.path.join(BASE, "logs", "predictions", "vol14_blind.md")
    v_entries = parse_v_entries(blind_path)
    print(f"Parsed {len(v_entries)} V-entries")

    arena_map = build_arena_slot_map(OUT)

    # 每一 V 条目: 查找其 arena slot(s)
    rows = []
    for v_num, targets in v_entries:
        arena_nums = []
        source_lines = []
        for (ln, si) in targets:
            an = arena_map.get((ln, si))
            if an is not None:
                arena_nums.append(an)
                if ln not in source_lines:
                    source_lines.append(ln)
            else:
                print(f"  WARN: V{v_num} target L{ln}[{si}] not in arena")

        if not arena_nums:
            print(f"  ERROR: V{v_num} has no arena slots!")
            continue

        chunk = get_chunk(targets[0][0])
        arena_str = ",".join(f"#{a}" for a in arena_nums)
        lines_str = "/".join(str(ln) for ln in source_lines)

        rows.append((v_num, lines_str, arena_str, chunk))

    # 写 full_item_map.md
    out_path = os.path.join(OUT, "full_item_map.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# Full Item Map: vol14 V-number → Arena Placeholder\n\n")
        f.write(f"- **Scoring items**: {len(rows)} (all V1-V200 from vol14_blind.md)\n")
        f.write("- Each row maps one V-number to its arena slot(s) in the full ablation arenas.\n")
        f.write("- Multi-slot V-numbers (e.g. V90 → #105,#106,#107) will be merged during scoring.\n\n")
        f.write("| vol14_id | source_lines | arena_slots | chunk |\n")
        f.write("|---|---|---|---|\n")
        for (v_num, lines_str, arena_str, chunk) in rows:
            f.write(f"| V{v_num} | {lines_str} | {arena_str} | {chunk} |\n")

    # 统计 per-chunk
    from collections import Counter
    chunk_counts = Counter(r[3] for r in rows)
    print(f"\nSummary: {len(rows)} V-numbers ({len(v_entries)} entries)")
    print(f"Per chunk:")
    for c in ["part01", "part02", "part03", "part04"]:
        print(f"  {c}: {chunk_counts.get(c, 0)}")


if __name__ == "__main__":
    main()
