#!/usr/bin/env python3
"""Round 5 tests one rule R4 never met: a summary or analysis of supplied material is AI-origin. 10 pool windows whose
request asks for a summary or explanation, seeded. Not random, so left out of frequency estimates. Prints counts only."""
import collections, hashlib, json, os, random, re
from draw_pilot import SEED, pool
from views import CODEBOOK, load_ids, load_windows, make_views

RX = re.compile(r"\b(summar(y|ize|ise)|explain|what does (this|the) .{0,40}(say|mean)|main (points|findings))\b", re.I)


def main():
    rng = random.Random(SEED + 5)
    rows = load_windows()
    test = load_ids("sample.csv") | load_ids("gold.csv")
    held = [w for w in rows if w["window_id"] in test]
    p = pool(rows, {(w["dataset"], w["session_id"]) for w in held}, {(w["dataset"], w["participant_id"]) for w in held})
    used = set()
    for r in ("r1", "r2", "r3", "r4"):
        used |= set(open(os.path.join(CODEBOOK, "pilot", r, "ids.txt")).read().split())
    c = sorted((w for w in p if w["window_id"] not in used and RX.search(w["request"][:400])), key=lambda w: w["window_id"])
    print("candidates", len(c), dict(collections.Counter(w["dataset"] for w in c)))
    rng.shuffle(c)
    pick, sess = [], set()
    for w in c:
        k = (w["dataset"], w["session_id"])
        if k not in sess and len(pick) < 10:
            pick.append(w)
            sess.add(k)
    d = os.path.join(CODEBOOK, "pilot", "r5")
    os.makedirs(d, exist_ok=True)
    ids = sorted(w["window_id"] for w in pick)
    open(os.path.join(d, "ids.txt"), "w").write("\n".join(ids) + "\n")
    open(os.path.join(d, "targeted_ids.txt"), "w").write("\n".join(ids) + "\n")
    v = make_views(set(ids))
    with open(os.path.join(d, "view.jsonl"), "w", encoding="utf-8") as f:
        for i in sorted(ids, key=lambda i: hashlib.sha256(f"{SEED}{i}".encode()).hexdigest()):
            f.write(json.dumps(v[i], ensure_ascii=False) + "\n")
    print("r5", len(ids), dict(collections.Counter((w["dataset"], w["coverage"]) for w in pick)))


if __name__ == "__main__":
    main()
