#!/usr/bin/env python3
"""Check that every repository path named in SUPPLEMENT.md exists, and report which ones git tracks."""
import pathlib
import re
import subprocess
import sys

PAPER = pathlib.Path(__file__).resolve().parents[1]
ROOT = PAPER.parents[1]


def main():
    text = (PAPER / "SUPPLEMENT.md").read_text(encoding="utf-8")
    paths = sorted(set(re.findall(r"`((?:Final_Project|\.wayne)/[^`*]+)`", text)))
    missing, tracked, local = [], [], []
    for path in paths:
        if not (ROOT / path).exists():
            missing.append(path)
            continue
        out = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--", path], capture_output=True, text=True).stdout
        (tracked if out.strip() else local).append(path)
    print(f"{len(paths)} paths: {len(tracked)} tracked, {len(local)} local only, {len(missing)} missing")
    for path in local:
        print("local:", path)
    for path in missing:
        print("MISSING:", path)
    sys.exit(1 if missing else 0)


main()
