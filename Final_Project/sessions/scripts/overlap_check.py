#!/usr/bin/env python3
"""Script audit (codebook/scripts/overlap.py, Bet 4's conflict rules) of uptake on all NIRVANA C2 windows, for A, B and final labels.
Needs git-excluded windows.jsonl. Writes results/overlap_facts.csv (numbers only) and results/overlap_audit.json. Prints counts only."""
import collections, csv, json, os
import s6
from overlap_audit import KEEP, conflict, short   # coding/scripts, Bet 4
from finalize import script_facts


def main():
    fx = script_facts()
    with open(os.path.join(s6.OUT, "overlap_facts.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["window_id"] + KEEP)
        for i in sorted(fx):
            w.writerow([i] + [fx[i][k] for k in KEEP])
    src = {"A": {}, "B": {}}
    for r in csv.DictReader(open(os.path.join(s6.OUT, "labels_ab.csv"))):
        src[r["coder"]][r["window_id"]] = r["uptake"]
    F = {r["window_id"]: r for r in csv.DictReader(open(os.path.join(s6.OUT, "final_labels_nirvana.csv")))}
    src["final"] = {i: r["uptake"] for i, r in F.items()}
    res = {"n_c2": len(fx), "class": dict(collections.Counter(v["class"] for v in fx.values())), "by_source": {}}
    for s, L in src.items():
        conf, u12, u7 = {}, {"both_present": 0, "agree": 0}, {"n": 0, "no_script_match": 0}
        for i, f in fx.items():
            lab = L[i]
            k = conflict(lab, f)
            if k:
                conf[i] = {"label": short(lab), "kind": k, "class": f["class"], "final_source": F[i]["source"]}
            if short(lab) in ("U1", "U2") and f["audit_u1_vs_u2"]:
                u12["both_present"] += 1
                u12["agree"] += f["audit_u1_vs_u2"] == short(lab)
            if short(lab) == "U7":
                u7["n"] += 1
                u7["no_script_match"] += not (f["class"].startswith("PASTE_MATCH") or f["class"] == "TYPED_MATCH")
        res["by_source"][s] = {"conflicts": conf, "conflict_kinds": dict(collections.Counter(c["kind"] for c in conf.values())), "u1_u2": u12, "u7": u7}
    json.dump(res, open(os.path.join(s6.OUT, "overlap_audit.json"), "w"), indent=1, sort_keys=True)
    print("C2 windows", res["n_c2"], res["class"])
    for s, v in res["by_source"].items():
        print(s, "U1/U2 agree", v["u1_u2"], "U7", v["u7"], "conflicts", v["conflict_kinds"])


if __name__ == "__main__":
    main()
