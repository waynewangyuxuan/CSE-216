#!/usr/bin/env python3
"""Merge Bet 6 coder files into results/labels_ab.csv: labels only, no notes, no window text. Derives process and family by script, as Bet 4.
`set` is new (no Bet 4 label), sensitivity (Bet 4 window with unseen older turns, recoded with full history) or bet4_kept (relabeled as a side check only). Prints counts only."""
import csv, glob, os
import s6
from merge_labels import CODED, PMAP      # coding/scripts, Bet 4
from agreement import FAMILY              # codebook/scripts

COLS = ["window_id", "session_id", "turn_order", "part", "coverage", "set", "coder"] + CODED + ["process", "family", "confidence", "u4_subtype", "flag_field"]


def window_set():
    b4, sens = s6.bet4_final(), set(s6.sensitivity_ids())
    return {i: ("sensitivity" if i in sens else "bet4_kept" if i in b4 else "new") for i in s6.meta()}


def read_coder(c):
    rows = {}
    for p in sorted(glob.glob(os.path.join(s6.BLIND, f"coder_{c}", "batch_*.jsonl"))):
        for r in s6.load_jsonl(p):
            assert r["window_id"] not in rows, r["window_id"]
            rows[r["window_id"]] = r
    return rows


def main():
    m, ws = s6.meta(), window_set()
    A, B = read_coder("a"), read_coder("b")
    assert set(A) == set(B) == set(m), (len(A), len(B), len(m))
    with open(os.path.join(s6.OUT, "labels_ab.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, COLS, lineterminator="\n")
        w.writeheader()
        for i in sorted(m):
            for name, L in (("A", A), ("B", B)):
                r = L[i]
                w.writerow({"window_id": i, "session_id": m[i]["session"], "turn_order": m[i]["turn_order"], "part": m[i]["part"], "coverage": m[i]["coverage"], "set": ws[i], "coder": name,
                            **{k: r[k] for k in CODED}, "process": PMAP[r["operation"]], "family": FAMILY[r["operation"]],
                            "confidence": r["confidence"], "u4_subtype": r.get("u4_subtype", ""), "flag_field": r.get("flag_field", "")})
    print(f"windows {len(m)}, coder rows {len(A)} + {len(B)}, sets", {k: list(ws.values()).count(k) for k in ("new", "sensitivity", "bet4_kept")})


if __name__ == "__main__":
    main()
