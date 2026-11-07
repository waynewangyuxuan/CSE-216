#!/usr/bin/env python3
"""Stop dataset text from being committed (Bet 4's check, for sessions/). Run after `git add`, before `git commit`. Prints counts and paths only.
Fails if a staged file is outside Final_Project/sessions/, is under blind/, holds a free-text note column, or shares a 40-character run
(whitespace collapsed, lowercased) with any text of any NIRVANA window. Usage: check_staged.py [--all-tracked]"""
import subprocess, sys
import s6
from check_staged import BAN, grams      # coding/scripts, Bet 4
from views import _actions_text, editor_text, load_windows


def main():
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    if "--all-tracked" in sys.argv:
        paths = subprocess.check_output(["git", "ls-files", "--", "Final_Project/sessions"], text=True, cwd=root).split("\n")
    else:
        paths = subprocess.check_output(["git", "diff", "--cached", "--name-only", "--diff-filter=d"], text=True, cwd=root).split("\n")
    paths = [p for p in paths if p]
    at = _actions_text()
    bank = set()
    for w in load_windows():
        if w["dataset"] == "NIRVANA":
            for t in (w["request"], w["response"], at(w), editor_text(w)):
                bank |= grams(t)
    bad = 0
    for p in paths:
        if not p.startswith("Final_Project/sessions/") or "/blind/" in p:
            print("PROBLEM path not allowed:", p)
            bad += 1
            continue
        blob = subprocess.check_output(["git", "show", ":" + p], cwd=root).decode("utf-8", "replace")
        head = blob.split("\n", 1)[0].lower()
        hits = len(grams(blob) & bank)
        cols = [b for b in BAN if p.endswith(".csv") and b in head]
        print(f"{p}: chars {len(blob)}, 40-char runs shared with window text {hits}" + (f", banned columns {cols}" if cols else ""))
        bad += (hits > 0) + bool(cols)
    print(f"files {len(paths)}, grams in bank {len(bank)}, problems {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
