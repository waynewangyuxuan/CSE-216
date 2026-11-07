#!/usr/bin/env python3
"""Third AI check: Fable 5.1 agent's labels on the 20 gold windows against A, B and final labels. Written after final labels were committed.
Reads saved CSVs only. Writes results/fable_comparison.json and .md. This is AI-to-AI consistency. Never human, expert or gold-standard validation."""
import collections, csv, json, math, os
from stats_bet4 import OUT, HERE, kappa, pct, stats, short
from merge_labels import PMAP
from agreement import FAMILY

def exact_ci(k, n, a=.05):
    """Clopper-Pearson by bisection. Standard library only."""
    cdf = lambda m, p: sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(m + 1))
    def bis(f):
        l, h = 0.0, 1.0
        for _ in range(60):
            m = (l + h) / 2
            l, h = (m, h) if f(m) else (l, m)
        return round(l, 2)
    return [bis(lambda p: 1 - cdf(k - 1, p) < a / 2), bis(lambda p: cdf(k, p) > a / 2)]


FABLE = os.path.join(HERE, "..", "..", "codebook", "gold_agent", "fable_labels.csv")
FIELDS = ["family", "operation", "process", "function", "object", "prior_own_work", "decision", "verification", "uptake"]
Q35 = ["decision", "verification", "uptake"]
# Decided in decisions.tsv T04 before the Fable labels were opened.
MARK_A = ["NIRVANA-e27-t02"]
MARK_B = ["NIRVANA-e26-t11", "NIRVANA-e70-t07", "WILDCHAT-0685972d7031-t03"]


def table(rows, ids, other, session):
    out = {}
    for f in FIELDS + ["domain"]:
        use = [i for i in ids if f != "domain" or rows[i]["dataset"] == "WildChat"]
        use = [i for i in use if other[i][f] != "UNSETTLED"]
        out[f] = stats(use, {i: rows[i][f] for i in use}, {i: other[i][f] for i in use}, session)
    return out


def main():
    F = {r["window_id"]: r for r in csv.DictReader(open(FABLE))}
    for r in F.values():
        r["process"], r["family"] = PMAP[r["operation"]], FAMILY[r["operation"]]
    rows = list(csv.DictReader(open(os.path.join(OUT, "labels_ab.csv"))))
    A = {r["window_id"]: r for r in rows if r["coder"] == "A"}
    B = {r["window_id"]: r for r in rows if r["coder"] == "B"}
    Fin = {r["window_id"]: r for r in csv.DictReader(open(os.path.join(OUT, "final_labels.csv")))}
    gold = sorted(i for i in A if A[i]["gold"] == "1")
    assert set(gold) == set(F) and len(gold) == 20
    assert all(F[i]["coverage"] == A[i]["coverage"] for i in gold)
    assert set(MARK_A + MARK_B) <= set(gold)
    session = {i: i for i in gold}  # gold has at most one window per participant
    follow = [i for i in gold if A[i]["coverage"] != "C0"]
    unmarked = [i for i in gold if i not in MARK_A + MARK_B]
    res = {"note": "AI-to-AI consistency on 20 windows. Not human, expert or gold-standard validation. Says nothing about cognition.", "n": 20,
           "marked_less_complete": {"main_block_cut": MARK_A, "reused_earlier_ai_text_cut": MARK_B}}
    for name, L in (("A", A), ("B", B), ("final", Fin)):
        res["fable_vs_" + name] = {"all": table(F, gold, L, session), "followup": table(F, follow, L, session), "unmarked": table(F, unmarked, L, session)}
    res["A_vs_B_on_gold"] = table(A, gold, B, session)
    dis = []
    for i in gold:
        for f in FIELDS[1:] + ["domain"]:
            if F[i][f] != Fin[i][f]:
                dis.append({"window_id": i, "field": f, "fable": short(F[i][f]), "A": short(A[i][f]), "B": short(B[i][f]), "final": short(Fin[i][f]), "marked": i in MARK_A + MARK_B, "dataset": A[i]["dataset"], "coverage": A[i]["coverage"]})
    res["disagreements_with_final"] = dis
    res["confusions_q3_q5"] = {f: dict(collections.Counter("|".join((short(F[i][f]), short(Fin[i][f]))) for i in gold if F[i][f] != Fin[i][f]).most_common()) for f in Q35}
    res["frequency"] = {f: {"fable": dict(sorted(collections.Counter(short(F[i][f]) for i in gold).items())), "final": dict(sorted(collections.Counter(short(Fin[i][f]) for i in gold).items()))} for f in Q35}
    res["marked_windows"] = {i: {f: {"fable": short(F[i][f]), "A": short(A[i][f]), "B": short(B[i][f]), "final": short(Fin[i][f])} for f in Q35} for i in MARK_A + MARK_B}
    wild = [i for i in gold if A[i]["dataset"] == "WildChat"]
    res["wildchat_is_research_writing"] = {"n": len(wild), "yes": sum(F[i]["is_research_writing"] == "yes" for i in wild), "no": sum(F[i]["is_research_writing"] == "no" for i in wild),
                                           "yes_exact_ci95": exact_ci(sum(F[i]["is_research_writing"] == "yes" for i in wild), len(wild)), "rows": {i: {"is_research_writing": F[i]["is_research_writing"], "fable_domain": F[i]["domain"], "final_domain": Fin[i]["domain"]} for i in wild},
                                           "fable_inconsistent": [i for i in wild if F[i]["domain"] == "RESEARCH_EXPLICIT" and F[i]["is_research_writing"] == "no"]}
    with open(os.path.join(OUT, "fable_comparison.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    L = ["# Fable comparison", "", "Written by `scripts/compare_fable.py`. A third AI check on 20 windows. **Not human, expert or gold-standard validation.**", "",
         f"| Field | Fable vs A % / κ | Fable vs B % / κ | Fable vs final % / κ [window CI] | Fable vs final, follow-up κ (n={len(follow)}) | Fable vs final, leaving out 4 marked windows, % / κ (n={len(unmarked)}) | A vs B on these 20, % / κ |", "|---|---|---|---|---|---|---|"]
    for f in ["domain"] + FIELDS:
        a, b, c, d, e, g = (res["fable_vs_A"]["all"][f], res["fable_vs_B"]["all"][f], res["fable_vs_final"]["all"][f], res["fable_vs_final"]["followup"][f], res["fable_vs_final"]["unmarked"][f], res["A_vs_B_on_gold"][f])
        L.append(f"| `{f}`{' (n=' + str(c['n']) + ')' if c['n'] != 20 else ''} | {a['pct']} / {a['kappa']} | {b['pct']} / {b['kappa']} | {c['pct']} / {c['kappa']} {c['kappa_ci_window']} | {d['kappa']} | {e['pct']} / {e['kappa']} | {g['pct']} / {g['kappa']} |")
    with open(os.path.join(OUT, "fable_comparison.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")
    print("\n".join(L))
    print(json.dumps({k: res[k] for k in ("confusions_q3_q5", "frequency", "marked_windows", "wildchat_is_research_writing")}, indent=0))
    for d in dis:
        print(d)


if __name__ == "__main__":
    main()
