#!/usr/bin/env python3
"""A vs B agreement on Bet 7 labels, from results/labels_ab_wildchat.csv only. Calls no model, needs no text. Fixed seed.
Reuses kappa and the window/session bootstrap of coding/scripts/stats_bet4.py (imported, not edited). Session = conversation (one per IP cluster).
Writes results/agreement_wildchat.json and results/agreement_tables_wildchat.md. AI-to-AI consistency only."""
import collections, csv, importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")
spec = importlib.util.spec_from_file_location("stats_bet4", os.path.join(HERE, "..", "..", "coding", "scripts", "stats_bet4.py"))
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)
FIELDS = ["domain"] + S.FIELDS


def main():
    rows = list(csv.DictReader(open(os.path.join(OUT, "labels_ab_wildchat.csv"))))
    A = {r["window_id"]: r for r in rows if r["coder"] == "A"}
    B = {r["window_id"]: r for r in rows if r["coder"] == "B"}
    ids = sorted(A)
    session = {i: A[i]["session_id"] for i in ids}
    sub = {"all": ids, "followup_C1": [i for i in ids if A[i]["coverage"] == "C1"], "C0": [i for i in ids if A[i]["coverage"] == "C0"],
           "turn1": [i for i in ids if A[i]["turn_order"] == "1"], "later_turns": [i for i in ids if A[i]["turn_order"] != "1"]}
    res = {"note": "Consistency between AI coders only. Not human, expert or gold-standard validation. Says nothing about cognition.",
           "n": len(ids), "sessions": len(set(session.values())), "agreement": {}, "frequency": {}, "confusions": {}, "flags": {}, "confidence": {}}
    for f in FIELDS:
        res["agreement"][f] = {n: S.stats(s, {i: A[i][f] for i in s}, {i: B[i][f] for i in s}, session) for n, s in sub.items() if s}
        res["confusions"][f] = dict(collections.Counter("|".join(sorted((S.short(A[i][f]), S.short(B[i][f])))) for i in ids if A[i][f] != B[i][f]).most_common())
    fp = os.path.join(OUT, "final_labels_wildchat.csv")
    final = {r["window_id"]: r for r in csv.DictReader(open(fp))} if os.path.exists(fp) else None
    for f in FIELDS:
        res["frequency"][f] = {n: dict(sorted(collections.Counter(S.short(L[i][f]) for i in ids).items())) for n, L in (("A", A), ("B", B)) + ((("final", final),) if final else ())}
    for n, L in (("A", A), ("B", B)):
        res["flags"][n] = dict(collections.Counter(L[i]["flag_field"] or "none" for i in ids))
        res["confidence"][n] = dict(collections.Counter(L[i]["confidence"] for i in ids))
    if final:
        res["final_source"] = {f: dict(collections.Counter(final[i][f + "_source"] for i in ids)) for f in FIELDS if f + "_source" in final[ids[0]]}
    json.dump(res, open(os.path.join(OUT, "agreement_wildchat.json"), "w"), indent=1, sort_keys=True)
    L = ["# Agreement tables, Bet 7 WildChat", "", "Written by `scripts/13_stats.py` from saved labels. A vs B. **AI-to-AI consistency only.**", ""]
    for n, s in sub.items():
        if not s:
            continue
        L += [f"## {n} (n={len(s)}, conversations {len({session[i] for i in s})})", "", "| Field | % [window CI] | κ | κ CI, windows | κ CI, conversations |", "|---|---|---|---|---|"]
        for f in FIELDS:
            x = res["agreement"][f][n]
            L.append(f"| `{f}` | {x['pct']} {x['pct_ci_window']} | {x['kappa']} | {x['kappa_ci_window']} | {x['kappa_ci_cluster']} |")
        L.append("")
    L += ["## Label use (windows)", ""]
    for f in FIELDS:
        labs = sorted(set().union(*[set(v) for v in res["frequency"][f].values()]))
        L += [f"**{f}**", "", "| Label | " + " | ".join(res["frequency"][f]) + " |", "|---|" + "---|" * len(res["frequency"][f])]
        L += [f"| `{k}` | " + " | ".join(str(res["frequency"][f][c].get(k, 0)) for c in res["frequency"][f]) + " |" for k in labs]
        L.append("")
    open(os.path.join(OUT, "agreement_tables_wildchat.md"), "w").write("\n".join(L) + "\n")
    print("| Field | n | % | κ | window CI | conversation CI | follow-up κ [conv CI] |")
    for f in FIELDS:
        a, c = res["agreement"][f]["all"], res["agreement"][f].get("followup_C1", {})
        print(f"| {f} | {a['n']} | {a['pct']} | {a['kappa']} | {a['kappa_ci_window']} | {a['kappa_ci_cluster']} | {c.get('kappa')} {c.get('kappa_ci_cluster')} |")


if __name__ == "__main__":
    main()
