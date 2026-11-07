#!/usr/bin/env python3
"""Bet 6 numbers from saved labels only: results/labels_ab.csv, final_labels_nirvana.csv, adjudication_log.csv, and Bet 4's committed labels.
Calls no model and reads no window text. Fixed seed (Bet 4's kappa and bootstrap code, imported), so reruns give the same numbers.
Writes results/agreement.json, results/sensitivity.json, results/tables.md. Every number is consistency between AI coders. u4_subtype is in no agreement claim."""
import collections, csv, json, os
import s6
from stats_bet4 import FIELDS, kappa, pct, short, stats   # coding/scripts, Bet 4

Q345 = ["decision", "verification", "uptake"]


def rd(p):
    return list(csv.DictReader(open(p)))


def r2(x):
    return None if x is None else round(x, 2)


def main():
    ab = rd(os.path.join(s6.OUT, "labels_ab.csv"))
    A = {r["window_id"]: r for r in ab if r["coder"] == "A"}
    B = {r["window_id"]: r for r in ab if r["coder"] == "B"}
    F = {r["window_id"]: r for r in rd(os.path.join(s6.OUT, "final_labels_nirvana.csv"))}
    log = rd(os.path.join(s6.OUT, "adjudication_log.csv"))
    b4ab = [r for r in rd(os.path.join(s6.BET4, "labels_ab.csv")) if r["dataset"] == "NIRVANA"]
    A4 = {r["window_id"]: r for r in b4ab if r["coder"] == "A"}
    B4 = {r["window_id"]: r for r in b4ab if r["coder"] == "B"}
    F4 = s6.bet4_final()
    older = json.load(open(os.path.join(s6.BET4, "older_turns.json")))
    reuse10 = sorted(older["windows_reusing_unseen_ai_text"])
    session = {i: A[i]["session_id"] for i in A}
    ids = sorted(A)
    adjd = [i for i in ids if A[i]["set"] != "bet4_kept"]
    sub = {"adjudicated": adjd, "followup": [i for i in adjd if A[i]["coverage"] != "C0"], "C1": [i for i in adjd if A[i]["coverage"] == "C1"],
           "C2": [i for i in adjd if A[i]["coverage"] == "C2"], "new": [i for i in adjd if A[i]["set"] == "new"], "sensitivity": [i for i in adjd if A[i]["set"] == "sensitivity"],
           "all_347": ids, "bet4_kept_52": [i for i in ids if A[i]["set"] == "bet4_kept"]}
    res = {"note": "Consistency between AI coders only. Not human, expert or gold-standard validation. Says nothing about cognition.",
           "n": {k: len(v) for k, v in sub.items()}, "sessions": {k: len({session[i] for i in v}) for k, v in sub.items()}, "agreement": {}}
    for f in FIELDS:
        res["agreement"][f] = {k: stats(v, {i: A[i][f] for i in v}, {i: B[i][f] for i in v}, session) for k, v in sub.items() if v}
    res["q345_min_kappa"] = {k: min((res["agreement"][f][k]["kappa"], f) for f in Q345 if res["agreement"][f][k]["kappa"] is not None) for k in ("adjudicated", "followup", "C1", "C2")}
    res["frequency_final"] = {f: dict(sorted(collections.Counter(short(F[i][f]) for i in F).items())) for f in FIELDS}
    res["frequency_final_by_source"] = {s: {f: dict(sorted(collections.Counter(short(F[i][f]) for i in F if F[i]["source"] == s).items())) for f in Q345 + ["prior_own_work"]} for s in ("bet6", "bet6_fullview_recode", "bet4")}
    res["frequency_coders"] = {f: {c: dict(sorted(collections.Counter(short(L[i][f]) for i in adjd).items())) for c, L in (("A", A), ("B", B))} for f in FIELDS}
    res["confusions"] = {f: dict(collections.Counter("|".join(sorted((short(A[i][f]), short(B[i][f])))) for i in adjd if A[i][f] != B[i][f]).most_common(5)) for f in FIELDS}
    # adjudication
    disp = [l for l in log if l["source"] != "script_s7"]
    flips = {l["window_id"]: l["shown_order"] for l in disp}
    won_pos = collections.Counter()
    for l in disp:
        if l["source"] in ("adj=A", "adj=B"):
            first = flips[l["window_id"]].split("=")[1]
            won_pos["first" if l["source"][-1] == first else "second"] += 1
    res["adjudication"] = {"windows_with_dispute": len({l["window_id"] for l in disp}), "windows_adjudicated": len(adjd), "disputed_fields": len(disp), "coded_fields": len(adjd) * 7,
                           "by_source": dict(collections.Counter(l["source"] for l in log)), "by_field": dict(collections.Counter(l["field"] for l in disp)),
                           "by_field_source": {f: dict(collections.Counter(l["source"] for l in disp if l["field"] == f)) for f in sorted({l["field"] for l in disp})},
                           "shown_position_won": dict(won_pos), "unsettled": sorted(f"{l['window_id']} {l['field']}" for l in disp if l["source"] == "UNSETTLED"),
                           "by_set": {s: dict(collections.Counter(l["source"] for l in disp if l["set"] == s)) for s in ("new", "sensitivity")}}
    res["final_source"] = {f: dict(collections.Counter(F[i][f + "_source"].split(":")[0] if F[i]["source"] != "bet4" else "bet4" for i in F)) for f in ["prior_own_work", "operation", "function", "object", "decision", "verification", "uptake"]}
    res["coverage"] = {"windows": len(F), "sessions": len({F[i]["session_id"] for i in F}), "by_source": dict(collections.Counter(F[i]["source"] for i in F)),
                       "unsettled_fields": sum(F[i][f] == "UNSETTLED" for i in F for f in FIELDS),
                       "sessions_complete": sum(1 for s in {F[i]["session_id"] for i in F})}
    json.dump(res, open(os.path.join(s6.OUT, "agreement.json"), "w"), indent=1, sort_keys=True)
    # sensitivity: full-history recode vs Bet 4's 3-turn view
    sens = sub["sensitivity"]
    S = {"note": "Bet 4 labels came from views showing the last 3 earlier turns; Bet 6 labels from full session history. Different agents, so a change can be view or coder noise.",
         "windows": sens, "reuse_unseen_ai_text": reuse10, "final_changes": [], "per_field": {}, "same_coder_role": {}}
    for i in sens:
        for f in FIELDS:
            if short(F[i][f]) != short(F4[i][f]) or F[i][f] != F4[i][f]:
                S["final_changes"].append({"window_id": i, "field": f, "bet4": F4[i][f], "bet6": F[i][f], "bet6_source": F[i][f + "_source"], "reuse_unseen": i in reuse10})
    for f in FIELDS:
        S["per_field"][f] = {"final_same": sum(F[i][f] == F4[i][f] for i in sens), "n": len(sens),
                             "final_same_reuse10": sum(F[i][f] == F4[i][f] for i in reuse10), "n_reuse10": len(reuse10)}
        for name, ws in (("sensitivity_18", sens), ("bet4_kept_52", sub["bet4_kept_52"])):
            S["same_coder_role"].setdefault(name, {})[f] = {"A6_vs_A4_pct": r2(pct([A[i][f] for i in ws], [A4[i][f] for i in ws])), "A6_vs_A4_kappa": r2(kappa([A[i][f] for i in ws], [A4[i][f] for i in ws])),
                                                         "B6_vs_B4_pct": r2(pct([B[i][f] for i in ws], [B4[i][f] for i in ws])), "B6_vs_B4_kappa": r2(kappa([B[i][f] for i in ws], [B4[i][f] for i in ws])),
                                                         "bet6_AB_pct": r2(pct([A[i][f] for i in ws], [B[i][f] for i in ws])), "bet4_AB_pct": r2(pct([A4[i][f] for i in ws], [B4[i][f] for i in ws]))}
    json.dump(S, open(os.path.join(s6.OUT, "sensitivity.json"), "w"), indent=1, sort_keys=True)
    # tables
    L = ["# Bet 6 tables", "", "Written by `scripts/stats.py` from saved labels. **AI-to-AI consistency only.** `u4_subtype` is in no agreement claim.", ""]
    for k in ("adjudicated", "followup", "C1", "C2", "new", "sensitivity", "all_347"):
        L += [f"## A vs B, {k} (n={res['n'][k]}, sessions {res['sessions'][k]})", "", "| Field | % | κ | κ CI, windows | κ CI, sessions |", "|---|---|---|---|---|"]
        for f in FIELDS:
            s = res["agreement"][f][k]
            L.append(f"| `{f}` | {s['pct']} | {s['kappa']} | {s['kappa_ci_window']} | {s['kappa_ci_cluster']} |")
        L.append("")
    L += ["## Final label use, 347 windows", "", "| Field | Labels |", "|---|---|"]
    L += [f"| `{f}` | " + ", ".join(f"{k} {v}" for k, v in res["frequency_final"][f].items()) + " |" for f in FIELDS]
    L += ["", "## Sensitivity: final label changes on the 18 windows (Bet 4 3-turn view to Bet 6 full history)", "", "| Window | Field | Bet 4 | Bet 6 | Bet 6 source | Reuses unseen AI text |", "|---|---|---|---|---|---|"]
    L += [f"| `{c['window_id']}` | `{c['field']}` | {short(c['bet4'])} | {short(c['bet6'])} | {c['bet6_source']} | {'yes' if c['reuse_unseen'] else ''} |" for c in S["final_changes"] if c["field"] not in ("process", "family")]
    open(os.path.join(s6.OUT, "tables.md"), "w").write("\n".join(L) + "\n")
    print("| Field | adj n | % | κ | session CI | follow-up κ [session CI] |")
    for f in FIELDS:
        a, fu = res["agreement"][f]["adjudicated"], res["agreement"][f]["followup"]
        print(f"| {f} | {a['n']} | {a['pct']} | {a['kappa']} | {a['kappa_ci_cluster']} | {fu['kappa']} {fu['kappa_ci_cluster']} |")
    print("Q3-Q5 min kappa", res["q345_min_kappa"])
    print("adjudication", {k: res["adjudication"][k] for k in ("windows_with_dispute", "disputed_fields", "by_source", "shown_position_won")})
    print("sensitivity final changes", len(S["final_changes"]), "coverage", res["coverage"])


if __name__ == "__main__":
    main()
