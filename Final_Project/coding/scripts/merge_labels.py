#!/usr/bin/env python3
"""Merge coder batch files into results/labels_ab.csv: labels only, no notes, no window text. Derives process and family by script. Prints counts only."""
import csv, glob, json, os, sys
import bet4
from bet4 import BLIND, DATA, OUT, ids_of, load_jsonl
from agreement import FAMILY  # codebook/scripts/agreement.py

CODED = ["domain", "prior_own_work", "operation", "function", "object", "decision", "verification", "uptake"]
PMAP = {f"O{i:02d}": ("P" if i <= 9 else "T" if i <= 11 else "R" if i <= 15 else "M") for i in range(1, 17)} | {"OX": "PX"}
ID_COLS = ["window_id", "dataset", "session_id", "coverage", "gold"]


def meta():
    gold = set(ids_of("gold.csv"))
    with open(os.path.join(DATA, "sample.csv"), encoding="utf-8", newline="") as f:
        return {r["window_id"]: {"window_id": r["window_id"], "dataset": r["dataset"], "session_id": r["session_id"], "coverage": r["coverage"], "gold": int(r["window_id"] in gold)} for r in csv.DictReader(f)}


def read_coder(c):
    rows = {}
    for p in sorted(glob.glob(os.path.join(BLIND, f"coder_{c}", "batch_*.jsonl"))):
        for r in load_jsonl(p):
            assert r["window_id"] not in rows, r["window_id"]
            rows[r["window_id"]] = r
    return rows


def main():
    m = meta()
    A, B = read_coder("a"), read_coder("b")
    assert set(A) == set(B) == set(m), (len(A), len(B), len(m))
    cols = ID_COLS + ["coder"] + CODED + ["process", "family", "confidence", "u4_subtype", "flag_field"]
    with open(os.path.join(OUT, "labels_ab.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, cols, lineterminator="\n")
        w.writeheader()
        for i in sorted(m):
            for name, L in (("A", A), ("B", B)):
                r = L[i]
                w.writerow({**m[i], "coder": name, **{k: r[k] for k in CODED}, "process": PMAP[r["operation"]], "family": FAMILY[r["operation"]],
                            "confidence": r["confidence"], "u4_subtype": r.get("u4_subtype", ""), "flag_field": r.get("flag_field", "")})
    print(f"windows {len(m)}, coder rows {len(A)} + {len(B)}")


if __name__ == "__main__":
    main()
