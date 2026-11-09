#!/usr/bin/env python3
"""Fail if TODO_WAYNE.md section 1 lists a different number of items than main.tex has % TODO(Wayne): comments."""
import pathlib
import re
import sys

PAPER = pathlib.Path(__file__).resolve().parents[1]


def main():
    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    source = len(re.findall(r"^% TODO\(Wayne\):", tex, re.M))
    todo = (PAPER / "TODO_WAYNE.md").read_text(encoding="utf-8")
    section = todo.split("## 1.")[1].split("## 2.")[0]
    listed = len(re.findall(r"^\d+\. ", section, re.M))
    print(f"main.tex TODOs: {source}; listed in TODO_WAYNE.md: {listed}")
    sys.exit(0 if source == listed else 1)


main()
