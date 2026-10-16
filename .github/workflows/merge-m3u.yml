from pathlib import Path
import re

ROOT = Path(".")
OUTPUT = ROOT / "all.m3u"

EXCLUDE_DIRS = {".git"}

def is_excluded(path: Path) -> bool:
    if path.resolve() == OUTPUT.resolve():
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False

def escape_group(s: str) -> str:
    # 去掉引号，避免破坏 group-title 的格式
    return s.replace('"', "'").strip()

def set_group_title(line: str, group: str) -> str:
    """
    在 #EXTINF 行里插入或替换 group-title="..."
    """
    group = escape_group(group)

    # 如果已经有 group-title，替换它
    if re.search(r'group-title\s*=\s*"[^"]*"', line):
        return re.sub(
            r'group-title\s*=\s*"[^"]*"',
            f'group-title="{group}"',
            line
        )

    # 否则，在第一个不在引号内的逗号前插入 group-title
    in_quote = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_quote = not in_quote
        elif ch == ',' and not in_quote:
            return line[:i] + f' group-title="{group}"' + line[i:]
    # 没有逗号，直接追加
    return line + f' group-title="{group}"'

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file()
    and p.suffix.lower() in (".m3u", ".m3u8")
    and not is_excluded(p)
)

with OUTPUT.open("w", encoding="utf-8", newline="\n") as out:
    out.write("#EXTM3U\n")
    for file in files:
        group = file.stem  # 用文件名（不含扩展名）作为分组名
        with file.open("r", encoding="utf-8-sig", errors="ignore") as f:
            for line in f:
                line = line.rstrip("\r\n")
                if line.startswith("#EXTM3U"):
                    continue
                if not line.strip():
                    continue

                if line.startswith("#EXTINF"):
                    # 给 #EXTINF 加上 group-title
                    line = set_group_title(line, group)
                    out.write(line + "\n")
                    # 再加一个 #EXTGRP，兼容更多播放器
                    out.write(f"#EXTGRP:{group}\n")
                else:
                    out.write(line + "\n")

print(f"已合并 {len(files)} 个文件到 {OUTPUT}")
