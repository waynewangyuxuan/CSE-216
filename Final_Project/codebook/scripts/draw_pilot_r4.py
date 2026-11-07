#!/usr/bin/env python3
"""Round 4 tests the final text: 19 fresh random windows, plus 3 typed-match and 2 partial-paste NIRVANA windows,
chosen by script facts so the retyped-run and partial-paste rules meet real cases. Prints counts only."""
import collections, hashlib, json, os, random
from draw_pilot import SEED, draw, pool
from overlap import facts
from views import CODEBOOK, load_ids, load_windows, make_views

RANDOM = {("NIRVANA", "C2"): 7, ("NIRVANA", "C1"): 4, ("WildChat", "C1"): 7, ("WildChat", "C0"): 1}


def main():
    rng = random.Random(SEED + 4)
    rows = load_windows()
    test = load_ids("sample.csv") | load_ids("gold.csv")
    held = [w for w in rows if w["window_id"] in test]
    p = pool(rows, {(w["dataset"], w["session_id"]) for w in held}, {(w["dataset"], w["participant_id"]) for w in held})
    by_id = {w["window_id"]: w for w in rows}
    used, used_s = set(), set()
    for r in ("r1", "r2", "r3"):
        for i in open(os.path.join(CODEBOOK, "pilot", r, "ids.txt")).read().split():
            used.add(i)
            used_s.add((by_id[i]["dataset"], by_id[i]["session_id"]))
    c2 = sorted((w for w in p if w["dataset"] == "NIRVANA" and w["coverage"] == "C2" and w["window_id"] not in used), key=lambda w: w["window_id"])
    typed = [w for w in c2 if facts(w)["class"] == "TYPED_MATCH"]
    partial = [w for w in c2 if facts(w)["paste_matched"] and facts(w)["share_response_pasted"] < 0.5 and w not in typed]
    rng.shuffle(typed)
    rng.shuffle(partial)
    target = typed[:3] + partial[:2]
    print("available: typed", len(typed), "partial", len(partial))
    taken = {w["window_id"] for w in target} | used
    picked = []
    for (ds, cov), n in RANDOM.items():
        c = sorted((w for w in p if w["dataset"] == ds and w["coverage"] == cov and w["window_id"] not in taken), key=lambda w: w["window_id"])
        picked += draw(c, n, rng, used_s)
    d = os.path.join(CODEBOOK, "pilot", "r4")
    os.makedirs(d, exist_ok=True)
    ids = sorted(w["window_id"] for w in picked) + sorted(w["window_id"] for w in target)
    open(os.path.join(d, "ids.txt"), "w").write("\n".join(ids) + "\n")
    open(os.path.join(d, "targeted_ids.txt"), "w").write("\n".join(sorted(w["window_id"] for w in target)) + "\n")
    v = make_views(set(ids))
    with open(os.path.join(d, "view.jsonl"), "w", encoding="utf-8") as f:
        for i in sorted(ids, key=lambda i: hashlib.sha256(f"{SEED}{i}".encode()).hexdigest()):
            f.write(json.dumps(v[i], ensure_ascii=False) + "\n")
    prior = sum((w["dataset"], w["session_id"]) in used_s - {(x["dataset"], x["session_id"]) for x in picked} for w in picked)
    print("r4", len(ids), "random", len(picked), "selected", len(target), dict(collections.Counter((w["dataset"], w["coverage"]) for w in picked + target)))


if __name__ == "__main__":
    main()
