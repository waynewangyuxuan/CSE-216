#!/usr/bin/env python3
"""Final labels for all 347 NIRVANA windows by the rule fixed before coding (decisions.tsv S05). Writes results/final_labels_nirvana.csv
(labels and a source per field, no text) and results/adjudication_log.csv (no free text).
new and sensitivity windows: A=B keeps the label; a disputed field takes the adjudicator's ruling, or UNSETTLED; then v1.1 s7: if final uptake
is U1 or U2 and the script audit differs, the script decides (logged script_s7). bet4_kept windows: Bet 4 final labels as committed.
Bet 4 labels of all 70 Bet 4 windows are kept in bet4_ columns. Prints counts only."""
import collections, csv, glob, json, os, re, sys
import s6
import codes, check_labels
from merge_labels import CODED, PMAP
from agreement import FAMILY
from overlap import facts
from views import load_windows
from merge import read_coder, window_set
from add_label import head

check_labels.head = head
UNSET = "UNSETTLED"
SOURCE = {"new": "bet6", "sensitivity": "bet6_fullview_recode", "bet4_kept": "bet4"}


def short(v):
    return (v or "").split("_")[0]


def script_facts():
    return {w["window_id"]: facts(w) for w in load_windows() if w["dataset"] == "NIRVANA" and w["coverage"] == "C2"}


def rulings():
    adj = {}
    for p in sorted(glob.glob(os.path.join(s6.BLIND, "adjudication", "ruling_*.jsonl"))):
        for r in s6.load_jsonl(p):
            key = (r["window_id"], r["field"])
            assert key not in adj, key
            adj[key] = r
    return adj


def main():
    A, B, m, ws, b4 = read_coder("a"), read_coder("b"), s6.meta(), window_set(), s6.bet4_final()
    adj, fx = rulings(), script_facts()
    flips = json.load(open(os.path.join(s6.BLIND, "adjudication", "flips.json")))
    cols = ["window_id", "dataset", "session_id", "turn_order", "part", "coverage", "source"] + CODED + ["process", "family", "u4_subtype"] + [f + "_source" for f in CODED] + ["bet4_" + f for f in CODED]
    log, final, errs = [], {}, 0
    for i in sorted(m, key=lambda x: (m[x]["session"], m[x]["part"])):
        r = {"window_id": i, "dataset": "NIRVANA", "session_id": m[i]["session"], "turn_order": m[i]["turn_order"], "part": m[i]["part"], "coverage": m[i]["coverage"], "source": SOURCE[ws[i]]}
        r.update({"bet4_" + f: b4[i][f] if i in b4 else "" for f in CODED})
        if ws[i] == "bet4_kept":
            r.update({f: b4[i][f] for f in CODED + ["process", "family", "u4_subtype"]})
            r.update({f + "_source": "bet4:" + b4[i][f + "_source"] for f in CODED})
            final[i] = r
            continue
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
            log.append({"window_id": i, "set": ws[i], "field": f, "label_a": A[i][f], "label_b": B[i][f], "final": r[f], "source": src, "settled": int(settled),
                        "rule": re.sub(r"\s+", " ", a.get("rule", ""))[:60], "shown_order": flips[i]})
        f = fx.get(i)
        if f and short(r["uptake"]) in ("U1", "U2") and f["audit_u1_vs_u2"] and f["audit_u1_vs_u2"] != short(r["uptake"]):
            new = "U1_EDITOR_DIRECT" if f["audit_u1_vs_u2"] == "U1" else "U2_EDITOR_SURFACE"
            log.append({"window_id": i, "set": ws[i], "field": "uptake", "label_a": A[i]["uptake"], "label_b": B[i]["uptake"], "final": new, "source": "script_s7", "settled": 1, "rule": f"s7 script audit, kept {f['share_paste_retained']}", "shown_order": ""})
            r["uptake"], r["uptake_source"] = new, "script_s7"
        r["process"] = PMAP.get(r["operation"], UNSET)
        r["family"] = FAMILY.get(r["operation"], UNSET)
        same = short(A[i]["uptake"]) == short(B[i]["uptake"]) and A[i].get("u4_subtype", "") == B[i].get("u4_subtype", "")
        r["u4_subtype"] = A[i].get("u4_subtype", "") if same and short(r["uptake"]) == "U4" else ""
        final[i] = r
    for i, r in final.items():
        if UNSET not in [r[f] for f in CODED]:
            for p in check_labels.problems(r):
                print("PROBLEM final rule check", i, p)
                errs += 1
    extra = set(adj) - {(l["window_id"], l["field"]) for l in log if l["source"] != "script_s7"}
    if extra:
        print("PROBLEM rulings on fields not in dispute:", sorted(extra))
        errs += 1
    if len(final) != 347 or len({r["session_id"] for r in final.values()}) != 71:
        print("PROBLEM coverage", len(final))
        errs += 1
    with open(os.path.join(s6.OUT, "final_labels_nirvana.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, cols, lineterminator="\n")
        w.writeheader()
        w.writerows(final.values())
    with open(os.path.join(s6.OUT, "adjudication_log.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, ["window_id", "set", "field", "label_a", "label_b", "final", "source", "settled", "rule", "shown_order"], lineterminator="\n")
        w.writeheader()
        w.writerows(log)
    print("windows", len(final), "by source", dict(collections.Counter(r["source"] for r in final.values())), "log rows", len(log), dict(collections.Counter(l["source"] for l in log)), "problems", errs)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
