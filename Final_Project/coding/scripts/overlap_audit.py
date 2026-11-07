#!/usr/bin/env python3
"""Script audit from codebook/scripts/overlap.py against saved labels. Needs windows.jsonl (git-excluded) and results/labels_ab.csv; final_labels.csv if present.
Writes results/overlap_facts.csv (numbers only) and results/overlap_audit.json. Prints counts only."""
import collections, csv, json, os
import bet4
from bet4 import OUT, ids_of
from overlap import facts
from views import load_windows

KEEP = ["class", "paste_chars", "paste_matched", "typed_chars", "typed_matched", "deleted_chars", "typed_after_paste", "deleted_after_paste", "share_paste_retained", "audit_u1_vs_u2", "share_response_pasted"]


def short(v):
    return (v or "").split("_")[0]


def script_facts():
    sample = set(ids_of("sample.csv"))
    return {w["window_id"]: facts(w) for w in load_windows() if w["window_id"] in sample and w["dataset"] == "NIRVANA" and w["coverage"] == "C2"}


def conflict(label, f):
    """Why a label disagrees with what the script measured, or None. Only U1/U2 is settled by script (v1.1 s7); the rest are flags for reading."""
    c, u = f["class"], short(label)
    if u in ("U1", "U2") and f["audit_u1_vs_u2"] and f["audit_u1_vs_u2"] != u:
        return "U1_U2_script_differs"
    if u in ("U1", "U2", "U3") and not c.startswith("PASTE_MATCH") and c != "TYPED_MATCH":
        return "insertion_label_no_script_match"
    if u == "U7" and (c.startswith("PASTE_MATCH") or c == "TYPED_MATCH"):
        return "U7_script_found_run"
    if u in ("U4", "U5", "U6", "U8", "UX") and c.startswith("PASTE_MATCH"):
        return "chat_or_no_trace_label_script_found_paste"
    return None


def main():
    fx = script_facts()
    with open(os.path.join(OUT, "overlap_facts.csv"), "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["window_id"] + KEEP)
        for i in sorted(fx):
            w.writerow([i] + [fx[i][k] for k in KEEP])
    res = {"n_c2": len(fx), "class": dict(collections.Counter(v["class"] for v in fx.values()))}
    sources = {"A": {}, "B": {}}
    for r in csv.DictReader(open(os.path.join(OUT, "labels_ab.csv"))):
        sources[r["coder"]][r["window_id"]] = r["uptake"]
    fp = os.path.join(OUT, "final_labels.csv")
    if os.path.exists(fp):
        sources["final"] = {r["window_id"]: r["uptake"] for r in csv.DictReader(open(fp))}
    res["by_source"] = {}
    for s, L in sources.items():
        t = collections.Counter()
        conf = {}
        u12 = {"both_present": 0, "agree": 0}
        u7 = {"n": 0, "no_script_match": 0}
        for i, f in fx.items():
            lab = L[i]
            t[f["class"] + "|" + short(lab)] += 1
            k = conflict(lab, f)
            if k:
                conf[i] = {"label": short(lab), "kind": k, "class": f["class"]}
            if short(lab) in ("U1", "U2") and f["audit_u1_vs_u2"]:
                u12["both_present"] += 1
                u12["agree"] += f["audit_u1_vs_u2"] == short(lab)
            if short(lab) == "U7":
                u7["n"] += 1
                u7["no_script_match"] += not (f["class"].startswith("PASTE_MATCH") or f["class"] == "TYPED_MATCH")
        res["by_source"][s] = {"class_by_label": dict(sorted(t.items())), "conflicts": conf, "u1_u2": u12, "u7": u7}
    with open(os.path.join(OUT, "overlap_audit.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print("C2 windows", res["n_c2"], res["class"])
    for s, v in res["by_source"].items():
        print(s, "U1/U2 agree", v["u1_u2"], "U7", v["u7"], "conflicts", dict(collections.Counter(x["kind"] for x in v["conflicts"].values())))


if __name__ == "__main__":
    main()
