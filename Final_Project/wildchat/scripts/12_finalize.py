#!/usr/bin/env python3
"""Final labels from A, B and the adjudicator's rulings. A=B keeps the label; a disputed field takes the ruling, or UNSETTLED.
WildChat has no editor, so the s7 script rule never applies. Writes results/final_labels_wildchat.csv (labels and a source per field)
and results/adjudication_log_wildchat.csv (no free text). Prints counts and problems."""
import collections, csv, glob, json, os, re, sys
from coding7 import CODED, FAMILY, ID_COLS, PMAP, UNSET, codes, meta, read_coder, short, w7
from check_labels import problems


def main():
    A, B, m = read_coder("a"), read_coder("b"), meta()
    adj = {}
    for p in sorted(glob.glob(os.path.join(w7.BLIND, "adjudication", "ruling*.jsonl"))):
        for r in w7.read_jsonl(p):
            k = (r["window_id"], r["field"])
            assert k not in adj, k
            adj[k] = r
    flips = json.load(open(os.path.join(w7.BLIND, "adjudication", "flips.json")))
    cols = ID_COLS + CODED + ["process", "family", "u4_subtype"] + [f + "_source" for f in CODED]
    log, final, errs = [], {}, 0
    for i in sorted(m):
        r = dict(m[i])
        for f in CODED:
            if A[i][f] == B[i][f]:
                r[f], r[f + "_source"] = A[i][f], "A=B"
                continue
            a = adj.get((i, f))
            if not a:
                print("PROBLEM no ruling", i, f)
                errs += 1
                r[f], r[f + "_source"] = UNSET, "missing"
                continue
            ok = a["settled"] is True and bool(a["final"])
            if ok and a["final"] not in codes.CODE_COLS[f]:
                print("PROBLEM invalid ruling", i, f)
                errs += 1
            r[f] = a["final"] if ok else UNSET
            src = UNSET if not ok else "adj=A" if a["final"] == A[i][f] else "adj=B" if a["final"] == B[i][f] else "adj=other"
            r[f + "_source"] = src
            log.append({"window_id": i, "field": f, "label_a": A[i][f], "label_b": B[i][f], "final": r[f], "source": src, "settled": int(ok),
                        "rule": re.sub(r"\s+", " ", a.get("rule", ""))[:60], "shown_order": flips[i]})
        r["process"] = PMAP.get(r["operation"], UNSET)
        r["family"] = FAMILY.get(r["operation"], UNSET)
        same = short(A[i]["uptake"]) == short(B[i]["uptake"]) and A[i].get("u4_subtype", "") == B[i].get("u4_subtype", "")
        r["u4_subtype"] = A[i].get("u4_subtype", "") if same and short(r["uptake"]) == "U4" else ""
        final[i] = r
        if UNSET not in [r[f] for f in CODED]:
            for p in problems(r, r["coverage"]):
                print("PROBLEM final rule check", i, p)
                errs += 1
    extra = set(adj) - {(l["window_id"], l["field"]) for l in log}
    if extra:
        print("PROBLEM rulings on fields not in dispute:", sorted(extra))
        errs += 1
    with open(os.path.join(w7.OUT, "final_labels_wildchat.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, lineterminator="\n")
        w.writeheader()
        w.writerows(final[i] for i in sorted(final))
    with open(os.path.join(w7.OUT, "adjudication_log_wildchat.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, ["window_id", "field", "label_a", "label_b", "final", "source", "settled", "rule", "shown_order"], lineterminator="\n")
        w.writeheader()
        w.writerows(log)
    print("windows", len(final), "log rows", len(log), dict(collections.Counter(l["source"] for l in log)), "problems", errs)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
