#!/usr/bin/env python3
"""Seeded pilot draw. Excludes every session and participant holding a sample or gold window, because a neighbouring
window carries the next window's request in next_request and so would leak test text to pilot coders.
Prints counts only. Writes pilot/<round>/{ids.txt,view.jsonl}. Rerun gives the same draw."""
import collections, hashlib, json, os, random, re, sys
from views import CODEBOOK, load_ids, load_windows, make_views

SEED = 2164
QUOTA = {  # (dataset, coverage) -> n
    "r1": {("NIRVANA", "C2"): 16, ("NIRVANA", "C1"): 10, ("NIRVANA", "C0"): 2, ("WildChat", "C1"): 9, ("WildChat", "C0"): 3},
    "r2": {("NIRVANA", "C2"): 12, ("NIRVANA", "C1"): 6, ("NIRVANA", "C0"): 1, ("WildChat", "C1"): 9, ("WildChat", "C0"): 2},
}
# Targeted part of round 2: next user turn looks like a check or a co-construction. Enriched for rare labels, so it
# informs agreement on them and is left out of frequency estimates.
TARGET_N = 10
TARGET_RE = re.compile(r"\b(are you sure|that'?s (not|wrong)|is (that|this) (true|correct|right)|not (correct|accurate|true)|incorrect|you (said|wrote|claimed|mentioned)|"
                       r"according to|the (paper|article|source|study|author) says|where did you|citation|source for|I disagree|but I think|contradict)\b", re.I)


def pool(rows, blocked_sessions, blocked_parts):
    out = []
    for w in rows:
        if w["coverage"] == "CX":
            continue
        if (w["dataset"], w["session_id"]) in blocked_sessions or (w["dataset"], w["participant_id"]) in blocked_parts:
            continue
        # Same WildChat pool as the sample: conversations the screen marked clear. The label is used here, never shown.
        if w["dataset"] == "WildChat" and w["screen"]["llm_label"] != "CLEAR_RESEARCH_WRITING":
            continue
        out.append(w)
    return out


def draw(cands, n, rng, used_sessions):
    """Prefer sessions not yet used, so windows are as independent as the pool allows."""
    rng.shuffle(cands)
    picked = []
    for w in cands:
        if len(picked) == n:
            break
        k = (w["dataset"], w["session_id"])
        if k not in used_sessions:
            picked.append(w)
            used_sessions.add(k)
    if len(picked) < n:  # fall back: second window from a used session, never a window already taken
        for w in cands:
            if len(picked) == n:
                break
            if w not in picked:
                picked.append(w)
    return picked


def main(rounds):
    rows = load_windows()
    test = load_ids("sample.csv") | load_ids("gold.csv")
    held = [w for w in rows if w["window_id"] in test]
    blocked_s = {(w["dataset"], w["session_id"]) for w in held}
    blocked_p = {(w["dataset"], w["participant_id"]) for w in held}
    p = pool(rows, blocked_s, blocked_p)
    print("pool", len(p), dict(collections.Counter((w["dataset"], w["coverage"]) for w in p)))
    rng = random.Random(SEED)
    used, taken, sess = set(), set(), set()
    for r in ("r1", "r2"):
        picked = []
        for (ds, cov), n in QUOTA[r].items():
            c = sorted((w for w in p if w["dataset"] == ds and w["coverage"] == cov and w["window_id"] not in taken), key=lambda w: w["window_id"])
            picked += draw(c, n, rng, sess)
        target = []
        if r == "r2":
            c = sorted((w for w in p if w["window_id"] not in taken and w not in picked and w["coverage"] in ("C1", "C2")
                        and TARGET_RE.search(w.get("next_request") or "")), key=lambda w: w["window_id"])
            print("r2 targeted candidates", len(c))
            target = draw(c, TARGET_N, rng, sess)
        taken |= {w["window_id"] for w in picked + target}
        d = os.path.join(CODEBOOK, "pilot", r)
        os.makedirs(d, exist_ok=True)
        ids = sorted(w["window_id"] for w in picked) + sorted(w["window_id"] for w in target)
        with open(os.path.join(d, "ids.txt"), "w") as f:
            f.write("\n".join(ids) + "\n")
        with open(os.path.join(d, "targeted_ids.txt"), "w") as f:
            f.write("\n".join(sorted(w["window_id"] for w in target)) + ("\n" if target else ""))
        if r in rounds:
            views = make_views(set(ids))
            order = sorted(ids, key=lambda i: hashlib.sha256(f"{SEED}{i}".encode()).hexdigest())  # shuffled, so targeted ones are not marked by position
            with open(os.path.join(d, "view.jsonl"), "w", encoding="utf-8") as f:
                for i in order:
                    f.write(json.dumps(views[i], ensure_ascii=False) + "\n")
        all_w = picked + target
        print(r, len(all_w), "random", len(picked), "targeted", len(target), dict(collections.Counter((w["dataset"], w["coverage"]) for w in all_w)),
              "sessions", len({(w["dataset"], w["session_id"]) for w in all_w}))
    if test & taken:
        sys.exit("OVERLAP with sample/gold")
    print("overlap with sample/gold:", len(test & taken))


if __name__ == "__main__":
    main(sys.argv[1:] or ["r1", "r2"])
