from pathlib import Path
import re

ROOT = Path(".")
OUTPUT = ROOT / "all.m3u"

print("=== 开始合并 ===")

# 找出所有 m3u 文件
files = []
for p in sorted(ROOT.rglob("*")):
    if not p.is_file():
        continue
    if p.suffix.lower() not in (".m3u", ".m3u8"):
        continue
    if p.name == "all.m3u":
        continue
    if ".git" in p.parts:
        continue
    files.append(p)

print(f"找到 {len(files)} 个文件：")
for f in files:
    print("  ", f, "-> 分组:", f.stem)

def add_group(line, group):
    # 去掉已有的 group-title
    line = re.sub(r'\s*group-title="[^"]*"', '', line)
    # 找到第一个不在引号内的逗号
    in_quote = False
    pos = -1
    for i, ch in enumerate(line):
        if ch == '"':
            in_quote = not in_quote
        elif ch == ',' and not in_quote:
            pos = i
            break
    if pos == -1:
        return line + ' group-title="' + group + '"'
    return line[:pos] + ' group-title="' + group + '"' + line[pos:]

with OUTPUT.open("w", encoding="utf-8", newline="\n") as out:
    out.write("#EXTM3U\n")
    for file in files:
        group = file.stem
        print(f"处理 {file}，分组 = {group}")
        with file.open("r", encoding="utf-8-sig", errors="ignore") as f:
            for raw in f:
                line = raw.rstrip("\r\n")
                if not line.strip():
                    continue
                if line.startswith("#EXTM3U"):
                    continue
                if line.startswith("#EXTINF"):
                    line = add_group(line, group)
                    out.write(line + "\n")
                    out.write("#EXTGRP:" + group + "\n")
                else:
                    out.write(line + "\n")

print(f"完成，输出到 {OUTPUT}")
