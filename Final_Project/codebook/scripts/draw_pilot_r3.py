#!/usr/bin/env python3
"""Round 3: 16 fresh random windows plus 14 enriched windows from scan_rare.py groups. Prints counts only."""
import collections, hashlib, json, os, random
from draw_pilot import SEED, draw, pool
from scan_rare import candidates
from views import CODEBOOK, make_views

RANDOM = {("NIRVANA", "C2"): 8, ("NIRVANA", "C1"): 3, ("WildChat", "C1"): 4, ("WildChat", "C0"): 1}
ENRICH = {"reasoned": 5, "reject": 3, "source": 2, "accept": 4}


def main():
    rng = random.Random(SEED + 3)
    p, cands = candidates()
    used = set()
    used_s = set()
    by_id = {w["window_id"]: w for w in p}
    for r in ("r1", "r2"):
        for i in open(os.path.join(CODEBOOK, "pilot", r, "ids.txt")).read().split():
            used.add(i)
            if i in by_id:
                used_s.add((by_id[i]["dataset"], by_id[i]["session_id"]))
    target = []
    for g, n in ENRICH.items():
        c = sorted((w for w in cands[g] if w not in target), key=lambda w: w["window_id"])
        rng.shuffle(c)
        target += c[:n]
    taken = {w["window_id"] for w in target} | used
    picked = []
    for (ds, cov), n in RANDOM.items():
        c = sorted((w for w in p if w["dataset"] == ds and w["coverage"] == cov and w["window_id"] not in taken), key=lambda w: w["window_id"])
        picked += draw(c, n, rng, used_s)
    d = os.path.join(CODEBOOK, "pilot", "r3")
    os.makedirs(d, exist_ok=True)
    ids = sorted(w["window_id"] for w in picked) + sorted(w["window_id"] for w in target)
    open(os.path.join(d, "ids.txt"), "w").write("\n".join(ids) + "\n")
    open(os.path.join(d, "targeted_ids.txt"), "w").write("\n".join(sorted(w["window_id"] for w in target)) + "\n")
    v = make_views(set(ids))
    order = sorted(ids, key=lambda i: hashlib.sha256(f"{SEED}{i}".encode()).hexdigest())
    with open(os.path.join(d, "view.jsonl"), "w", encoding="utf-8") as f:
        for i in order:
            f.write(json.dumps(v[i], ensure_ascii=False) + "\n")
    print("r3", len(ids), "random", len(picked), "enriched", len(target), dict(collections.Counter((w["dataset"], w["coverage"]) for w in picked + target)))


if __name__ == "__main__":
    main()
