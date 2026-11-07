#!/usr/bin/env python3
"""Final labels from A, B, the adjudication file and the script rule of v1.1 s7. Writes results/final_labels.csv (labels and source per field) and results/adjudication_log.csv (no free text).
Rules: A=B keeps the label. A disputed field takes the adjudicator's ruling, or UNSETTLED when the rules do not settle it. Then, if final uptake is U1 or U2 and the script audit differs, the script decides (v1.1 s7), logged as script_s7. Prints counts only."""
import collections, csv, glob, json, os, re, sys
import bet4
from bet4 import BLIND, OUT, load_jsonl
import codes
from check_labels import problems
from merge_labels import CODED, ID_COLS, PMAP, meta, read_coder
from agreement import FAMILY
from overlap_audit import script_facts

UNSET = "UNSETTLED"


def short(v):
    return (v or "").split("_")[0]


def main():
    A, B, m = read_coder("a"), read_coder("b"), meta()
    adj = {}
    for p in sorted(glob.glob(os.path.join(BLIND, "adjudication", "ruling*.jsonl"))):
        for r in load_jsonl(p):
            key = (r["window_id"], r["field"])
            assert key not in adj, key
            adj[key] = r
    flips = json.load(open(os.path.join(BLIND, "adjudication", "flips.json")))
    fx = script_facts()
    cols = ID_COLS + CODED + ["process", "family", "u4_subtype"] + [f + "_source" for f in CODED]
    log = []
    final, errs = {}, 0
    for i in sorted(m):
        r = {**m[i]}
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
            settled = a["settled"] is True and bool(a["final"])
            if settled and a["final"] not in codes.CODE_COLS[f]:
                print("PROBLEM invalid ruling", i, f)
                errs += 1
            r[f] = a["final"] if settled else UNSET
            src = UNSET if not settled else "adj=A" if a["final"] == A[i][f] else "adj=B" if a["final"] == B[i][f] else "adj=other"
            r[f + "_source"] = src
            log.append({"window_id": i, "field": f, "label_a": A[i][f], "label_b": B[i][f], "final": r[f], "source": src, "settled": int(settled), "rule": re.sub(r"\s+", " ", a.get("rule", ""))[:60], "shown_order": flips[i]})
        for key in adj:
            pass
        f = fx.get(i)
        if f and short(r["uptake"]) in ("U1", "U2") and f["audit_u1_vs_u2"] and f["audit_u1_vs_u2"] != short(r["uptake"]):
            new = "U1_EDITOR_DIRECT" if f["audit_u1_vs_u2"] == "U1" else "U2_EDITOR_SURFACE"
            log.append({"window_id": i, "field": "uptake", "label_a": A[i]["uptake"], "label_b": B[i]["uptake"], "final": new, "source": "script_s7", "settled": 1, "rule": f"s7 script audit, kept {f['share_paste_retained']}", "shown_order": ""})
            r["uptake"], r["uptake_source"] = new, "script_s7"
        r["process"] = PMAP.get(r["operation"], UNSET)
        r["family"] = FAMILY.get(r["operation"], UNSET)
        same = short(A[i]["uptake"]) == short(B[i]["uptake"]) and A[i].get("u4_subtype", "") == B[i].get("u4_subtype", "")
        r["u4_subtype"] = A[i].get("u4_subtype", "") if same and short(r["uptake"]) == "U4" else ""
        final[i] = r
        if UNSET not in (r["decision"], r["verification"], r["uptake"], r["domain"], r["prior_own_work"]):
            for p in problems(r):
                print("PROBLEM final rule check", i, p)
                errs += 1
    extra = set(adj) - {(l["window_id"], l["field"]) for l in log if l["source"] != "script_s7"}
    if extra:
        print("PROBLEM rulings on fields not in dispute:", sorted(extra))
        errs += 1
    with open(os.path.join(OUT, "final_labels.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, lineterminator="\n")
        w.writeheader()
        w.writerows(final[i] for i in sorted(final))
    with open(os.path.join(OUT, "adjudication_log.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, ["window_id", "field", "label_a", "label_b", "final", "source", "settled", "rule", "shown_order"], lineterminator="\n")
        w.writeheader()
        w.writerows(log)
    print("windows", len(final), "log rows", len(log), collections.Counter(l["source"] for l in log), "problems", errs)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
