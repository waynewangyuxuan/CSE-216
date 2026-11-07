#!/usr/bin/env python3
"""Merge coder batch files into results/labels_ab_wildchat.csv: labels only, no notes. Derives process and family by script. Prints counts."""
import csv, os
from coding7 import CODED, FAMILY, ID_COLS, PMAP, meta, read_coder, w7


def main():
    m = meta()
    A, B = read_coder("a"), read_coder("b")
    assert set(A) == set(B) == set(m), (len(A), len(B), len(m), sorted(set(m) ^ set(A))[:5], sorted(set(m) ^ set(B))[:5])
    cols = ID_COLS + ["coder"] + CODED + ["process", "family", "confidence", "u4_subtype", "flag_field"]
    with open(os.path.join(w7.OUT, "labels_ab_wildchat.csv"), "w", newline="") as f:
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
