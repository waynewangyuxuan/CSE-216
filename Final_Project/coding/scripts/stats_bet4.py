#!/usr/bin/env python3
"""Agreement from saved labels only: results/labels_ab.csv, and final_labels.csv if present. Calls no model, needs no window text. Fixed seed, so reruns give the same numbers.
Writes results/agreement.json and results/agreement_tables.md.
Every number is consistency between AI coders. Two models can share a bias. Nothing here validates claims about cognition."""
import collections, csv, json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")

FIELDS = ["family", "operation", "process", "function", "object", "prior_own_work", "decision", "verification", "uptake"]
ALL_FIELDS = ["domain"] + FIELDS
BOOT = 2000
SEED = 2164


def short(v):
    """D2_AI_PROPOSED_OPEN to D2. Leaves VISIBLE_DRAFT and FRAME_IDEA_PLAN whole."""
    return v.split("_")[0] if re.match(r"[DVUF](\d|X)_", v or "") else (v or "")


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def pct(a, b):
    return 100 * sum(x == y for x, y in zip(a, b)) / len(a) if a else None


def interval(vals):
    vals = sorted(v for v in vals if v is not None)
    return [round(vals[int(.025 * len(vals))], 2), round(vals[int(.975 * len(vals)) - 1], 2)] if vals else None


def boot(a, b, groups, rng):
    """Percentile intervals. groups: one list of positions per resampling unit. Unit = window, or session for clusters."""
    ks, ps = [], []
    for _ in range(BOOT):
        idx = []
        for _g in groups:
            idx += groups[rng.randrange(len(groups))]
        x, y = [a[i] for i in idx], [b[i] for i in idx]
        ks.append(kappa(x, y))
        ps.append(pct(x, y))
    return interval(ks), interval(ps)


def stats(ids, a, b, session):
    """a, b: {window_id: label}."""
    x, y = [a[i] for i in ids], [b[i] for i in ids]
    k = kappa(x, y)
    rng = random.Random(SEED)
    win = [[n] for n in range(len(ids))]
    by = collections.defaultdict(list)
    for n, i in enumerate(ids):
        by[session[i]].append(n)
    kw, pw = boot(x, y, win, rng)
    kc, pc = boot(x, y, list(by.values()), rng)
    return {"n": len(ids), "sessions": len(by), "pct": round(pct(x, y), 1), "kappa": None if k is None else round(k, 2), "kappa_ci_window": kw, "kappa_ci_cluster": kc, "pct_ci_window": pw, "pct_ci_cluster": pc}


def load():
    rows = list(csv.DictReader(open(os.path.join(OUT, "labels_ab.csv"))))
    meta = {r["window_id"]: r for r in rows if r["coder"] == "A"}
    A = {r["window_id"]: r for r in rows if r["coder"] == "A"}
    B = {r["window_id"]: r for r in rows if r["coder"] == "B"}
    return meta, A, B


def subsets(meta):
    ids = sorted(meta)
    return {"all": ids,
            "NIRVANA": [i for i in ids if meta[i]["dataset"] == "NIRVANA"], "WildChat": [i for i in ids if meta[i]["dataset"] == "WildChat"],
            "followup_C1C2": [i for i in ids if meta[i]["coverage"] != "C0"], "C2": [i for i in ids if meta[i]["coverage"] == "C2"], "C1": [i for i in ids if meta[i]["coverage"] == "C1"], "C0": [i for i in ids if meta[i]["coverage"] == "C0"],
            "NIRVANA_followup": [i for i in ids if meta[i]["coverage"] != "C0" and meta[i]["dataset"] == "NIRVANA"],
            "WildChat_followup": [i for i in ids if meta[i]["coverage"] != "C0" and meta[i]["dataset"] == "WildChat"]}


def main():
    meta, A, B = load()
    session = {i: meta[i]["dataset"] + "/" + meta[i]["session_id"] for i in meta}
    res = {"note": "Consistency between AI coders only. Not human, expert or gold-standard validation. Says nothing about cognition.", "n": len(meta), "agreement": {}, "frequency": {}, "per_label": {}, "confusions": {}, "flags": {}, "confidence": {}}
    sub = subsets(meta)
    for f in ALL_FIELDS:
        res["agreement"][f] = {}
        for name, ids in sub.items():
            if f == "domain" and "WildChat" not in name:
                continue
            if ids:
                res["agreement"][f][name] = stats(ids, {i: A[i][f] for i in ids}, {i: B[i][f] for i in ids}, session)
    fp = os.path.join(OUT, "final_labels.csv")
    final = {r["window_id"]: r for r in csv.DictReader(open(fp))} if os.path.exists(fp) else None
    for f in ALL_FIELDS:
        res["frequency"][f] = {}
        for name, L in (("A", A), ("B", B)) + ((("final", final),) if final else ()):
            for ds, ids in (("all", sub["all"]), ("NIRVANA", sub["NIRVANA"]), ("WildChat", sub["WildChat"])):
                res["frequency"][f].setdefault(name, {})[ds] = dict(sorted(collections.Counter(short(L[i][f]) for i in ids).items()))
        lab = sorted({short(A[i][f]) for i in A} | {short(B[i][f]) for i in B})
        res["per_label"][f] = {k: [sum(short(A[i][f]) == k == short(B[i][f]) for i in A), sum(k in (short(A[i][f]), short(B[i][f])) for i in A)] for k in lab}
        res["confusions"][f] = dict(collections.Counter("|".join(sorted((short(A[i][f]), short(B[i][f])))) for i in A if A[i][f] != B[i][f]).most_common())
    for name, L in (("A", A), ("B", B)):
        res["flags"][name] = dict(collections.Counter(L[i]["flag_field"] or "none" for i in L))
        res["confidence"][name] = dict(collections.Counter(L[i]["confidence"] for i in L))
    if final:
        res["final_source"] = {f: dict(collections.Counter(final[i].get(f + "_source", "") for i in final)) for f in ALL_FIELDS if final[next(iter(final))].get(f + "_source") is not None}
        res["final_vs_coder"] = {}
        for f in FIELDS:
            res["final_vs_coder"][f] = {c: stats(sub["all"], {i: L[i][f] for i in L}, {i: final[i][f] for i in final}, session) for c, L in (("A", A), ("B", B))}
    with open(os.path.join(OUT, "agreement.json"), "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    L = ["# Agreement tables", "", "Written by `scripts/stats_bet4.py` from saved labels. A vs B. **AI-to-AI consistency only.**", ""]
    for name in sub:
        ids = sub[name]
        if not ids:
            continue
        L += [f"## {name} (n={len(ids)}, sessions {len({session[i] for i in ids})})", "", "| Field | % [window CI] | κ | κ CI, windows | κ CI, sessions |", "|---|---|---|---|---|"]
        for f in ALL_FIELDS:
            s = res["agreement"][f].get(name)
            if s:
                L.append(f"| `{f}` | {s['pct']} {s['pct_ci_window']} | {s['kappa']} | {s['kappa_ci_window']} | {s['kappa_ci_cluster']} |")
        L.append("")
    L += ["## Label use (windows)", ""]
    for f in ALL_FIELDS:
        L.append(f"**{f}**")
        L.append("")
        L.append("| Label | A | B |" + (" final |" if final else "") + " both / either |")
        L.append("|---|---|---|" + ("---|" if final else "") + "---|")
        labs = sorted(set(res["frequency"][f]["A"]["all"]) | set(res["frequency"][f]["B"]["all"]) | (set(res["frequency"][f]["final"]["all"]) if final else set()))
        for k in labs:
            pl = res["per_label"][f].get(k, [0, 0])
            L.append(f"| `{k}` | {res['frequency'][f]['A']['all'].get(k, 0)} | {res['frequency'][f]['B']['all'].get(k, 0)} |" + (f" {res['frequency'][f]['final']['all'].get(k, 0)} |" if final else "") + f" {pl[0]}/{pl[1]} |")
        L.append("")
    with open(os.path.join(OUT, "agreement_tables.md"), "w") as fh:
        fh.write("\n".join(L))
    print("| Field | n | % | κ | window CI | session CI | follow-up κ | NIRVANA κ | WildChat κ |")
    for f in ALL_FIELDS:
        g = res["agreement"][f]
        a = g.get("all") or g.get("WildChat")
        print(f"| {f} | {a['n']} | {a['pct']} | {a['kappa']} | {a['kappa_ci_window']} | {a['kappa_ci_cluster']} | {(g.get('followup_C1C2') or g.get('WildChat_followup'))['kappa']} | {(g.get('NIRVANA') or {}).get('kappa')} | {g['WildChat']['kappa']} |")


if __name__ == "__main__":
    main()
