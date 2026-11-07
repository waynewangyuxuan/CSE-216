#!/usr/bin/env python3
"""Per-field agreement and label frequencies for a pilot round. Rerunnable; prints no window text.
Usage: agreement.py <round> [--families]   writes codebook/pilot_results/<round>_agreement.json and a labels-only CSV.
Agreement here is a consistency check between two models, never validation."""
import collections, csv, json, os, random, sys
from views import CODEBOOK

FIELDS = ["domain", "process", "operation", "family", "function", "object", "decision", "verification", "uptake", "prior_own_work", "u4_subtype"]
# Operation families (Chen 2026 layers informed this grouping; the grouping itself is the project's). See v1.1 section 3.
FAMILY = {"O01": "FRAME_IDEA_PLAN", "O02": "FRAME_IDEA_PLAN", "O03": "FRAME_IDEA_PLAN", "O04": "SOURCE_WORK", "O05": "SOURCE_WORK", "O06": "SOURCE_WORK", "O07": "SOURCE_WORK",
          "O08": "CLAIM_ARGUMENT", "O09": "CLAIM_ARGUMENT", "O10": "PROSE_CITATION", "O11": "PROSE_CITATION", "O12": "REVIEW_SUBSTANCE", "O13": "REVIEW_SUBSTANCE",
          "O14": "SURFACE", "O15": "SURFACE", "O16": "MONITOR", "OX": "OX",
          # v1.1 labels are family names already
          "FRAME_IDEA_PLAN": "FRAME_IDEA_PLAN", "SOURCE_WORK": "SOURCE_WORK", "CLAIM_ARGUMENT": "CLAIM_ARGUMENT", "PROSE_CITATION": "PROSE_CITATION",
          "REVIEW_SUBSTANCE": "REVIEW_SUBSTANCE", "SURFACE": "SURFACE", "MONITOR": "MONITOR"}
BOOT = 2000
SEED = 2164


def load(path):
    with open(path, encoding="utf-8") as f:
        return {r["window_id"]: r for r in map(json.loads, f)}


def short(v):
    return (v or "").split("_")[0] if (v or "")[:1] in "DVUF" and "_" in (v or "") else (v or "")


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def stats(a, b):
    k = kappa(a, b)
    rng = random.Random(SEED)
    idx = range(len(a))
    bs = []
    for _ in range(BOOT):
        s = [rng.choice(idx) for _ in idx] if a else []
        v = kappa([a[i] for i in s], [b[i] for i in s])
        if v is not None:
            bs.append(v)
    bs.sort()
    ci = [round(bs[int(.025 * len(bs))], 2), round(bs[int(.975 * len(bs)) - 1], 2)] if bs else None
    return {"n": len(a), "pct_agree": round(100 * sum(x == y for x, y in zip(a, b)) / len(a), 1) if a else None,
            "kappa": None if k is None else round(k, 2), "kappa_ci95": ci}


def main(rnd):
    d = os.path.join(CODEBOOK, "pilot", rnd)
    A, B = load(os.path.join(d, "coder_a", "labels.jsonl")), load(os.path.join(d, "coder_b", "labels.jsonl"))
    views = load(os.path.join(d, "view.jsonl"))
    targeted = set(open(os.path.join(d, "targeted_ids.txt")).read().split())
    assert set(A) == set(B) == set(views), "coders and view differ"
    ids = sorted(views)
    for L in (A, B):
        for r in L.values():
            op = r.get("operation", "")
            r["family"] = FAMILY.get(op, "?" + op)
    subsets = {"all": ids, "random_only": [i for i in ids if i not in targeted],
               "followup_C1C2": [i for i in ids if views[i]["coverage"] != "C0"],
               "NIRVANA": [i for i in ids if views[i]["dataset"] == "NIRVANA"], "WildChat": [i for i in ids if views[i]["dataset"] == "WildChat"],
               "C2": [i for i in ids if views[i]["coverage"] == "C2"], "C1": [i for i in ids if views[i]["coverage"] == "C1"]}
    res = {"round": rnd, "n": len(ids), "agreement": {}, "frequency_random_only": {}, "confusions": {}, "flags": {}, "note": "consistency check between two models, not validation"}
    fields = [f for f in FIELDS if any(f in r for r in A.values())]
    for f in fields:
        res["agreement"][f] = {}
        for name, sub in subsets.items():
            if f == "u4_subtype":  # only where both coders called it U4
                sub = [i for i in sub if short(A[i].get("uptake")) == "U4" and short(B[i].get("uptake")) == "U4"]
            if f == "domain" and name != "WildChat":
                continue
            if not sub:
                continue
            res["agreement"][f][name] = stats([str(A[i].get(f, "")) for i in sub], [str(B[i].get(f, "")) for i in sub])
    rand = subsets["random_only"]
    for f in fields:
        cnt = collections.Counter(str(A[i].get(f, "")) for i in rand) + collections.Counter(str(B[i].get(f, "")) for i in rand)
        res["frequency_random_only"][f] = dict(sorted(cnt.items()))
        res["confusions"][f] = dict(collections.Counter("|".join(sorted((short(str(A[i].get(f, ""))), short(str(B[i].get(f, ""))))))
                                                        for i in ids if A[i].get(f) != B[i].get(f)).most_common(15))
    res["flags"] = dict(collections.Counter(r.get("flag_field") or "" for L in (A, B) for r in L.values()))
    res["confidence"] = dict(collections.Counter(r.get("confidence") for L in (A, B) for r in L.values()))
    out = os.path.join(CODEBOOK, "pilot_results")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, f"{rnd}_agreement.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    with open(os.path.join(out, f"{rnd}_labels.csv"), "w", newline="") as f:  # labels only, no window text, safe for git
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["window_id", "dataset", "coverage", "targeted", "coder"] + fields + ["confidence"])
        for i in ids:
            for name, L in (("A", A), ("B", B)):
                w.writerow([i, views[i]["dataset"], views[i]["coverage"], int(i in targeted), name] + [L[i].get(k, "") for k in fields] + [L[i].get("confidence", "")])
    print(f"{rnd}: n={len(ids)}")
    print(f"{'field':16}{'all %':>7}{'k':>6}  {'CI95':14}{'C1/C2 %':>8}{'k':>6}")
    for f in fields:
        r = res["agreement"][f]
        a, c = r.get("all") or r.get("WildChat") or {}, r.get("followup_C1C2") or {}
        print(f"{f:16}{a.get('pct_agree')!s:>7}{a.get('kappa')!s:>6}  {a.get('kappa_ci95')!s:14}{c.get('pct_agree')!s:>8}{c.get('kappa')!s:>6}")


if __name__ == "__main__":
    main(sys.argv[1])
