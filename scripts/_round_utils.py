"""训练轮次目录解析的共用小工具。角色目录结构：
    characters/<角色>/source/          原文，各轮次共用，不重复存储
    characters/<角色>/V<版本号>/       每轮训练的 CEU + Character OS 文件
"""
import glob
import os
import re


def latest_round_dir(char_dir):
    """找 characters/<角色>/V* 里版本号最大的目录，按数字比较，不是字符串比较"""
    candidates = []
    for p in glob.glob(os.path.join(char_dir, "V*")):
        if not os.path.isdir(p):
            continue
        name = os.path.basename(p)
        m = re.match(r"^V(\d+)\.(\d+)$", name)
        if m:
            candidates.append((int(m.group(1)), int(m.group(2)), p))
    if not candidates:
        return None
    candidates.sort()
    return candidates[-1][2]


def resolve_round_dir(root, character, round_name=None):
    """round_name 形如 'V1.0'；不传则取最新轮次目录"""
    char_dir = os.path.join(root, "characters", character)
    if round_name:
        path = os.path.join(char_dir, round_name)
        if not os.path.isdir(path):
            raise FileNotFoundError(f"轮次目录不存在：{path}")
        return path
    path = latest_round_dir(char_dir)
    if path is None:
        raise FileNotFoundError(f"在 {char_dir} 下找不到任何 V<版本号> 轮次目录")
    return path
