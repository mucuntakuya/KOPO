from pathlib import Path

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

files = sorted(
    p for p in ROOT.rglob("*")
    if p.is_file()
    and p.suffix.lower() in (".m3u", ".m3u8")
    and not is_excluded(p)
)

with OUTPUT.open("w", encoding="utf-8", newline="\n") as out:
    out.write("#EXTM3U\n")
    for file in files:
        with file.open("r", encoding="utf-8-sig", errors="ignore") as f:
            for line in f:
                line = line.rstrip("\r\n")
                if line.startswith("#EXTM3U"):
                    continue
                if not line.strip():
                    continue
                out.write(line + "\n")

print(f"已合并 {len(files)} 个文件到 {OUTPUT}")
