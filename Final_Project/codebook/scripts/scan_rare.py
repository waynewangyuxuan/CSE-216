#!/usr/bin/env python3
"""Find pilot-pool windows whose next user turn may show a check, an acceptance or a rejection. Uses only windows outside
sample/gold sessions and outside rounds 1-2. Prints counts by default; --show N prints short next-turn snippets (pool only)."""
import collections, re, sys, random
from draw_pilot import pool, SEED
from views import load_ids, load_windows, CODEBOOK
import os

GROUPS = {
    "self_check": r"\b(are you sure|is (that|this|it) (true|correct|right|accurate|real)|double.?check|can you (verify|confirm)|provide (the )?(source|reference|citation)s? for|where did you (get|find)|what is the source|do these (references|sources)|real (references|sources|paper))\b",
    "reasoned": r"\b(that'?s (not|wrong|incorrect)|you('re| are) wrong|this is (wrong|incorrect|not (correct|true|accurate))|not (correct|accurate|true)\b|incorrect|i disagree|but i think|contradict|doesn'?t (exist|make sense|match)|does not (exist|make sense|match)|you (said|wrote|claimed|mentioned)|fake|made up|hallucinat)\b",
    "source": r"\b(the (paper|article|study|author|authors|source|abstract|text) (says|said|states|stated|shows|found|reports|does not)|according to (the|this|my) (paper|article|study|source|data|table)|in the (paper|article|original)|my data|the original (text|paper|article))\b",
    "accept": r"^\W*(thanks?|thank you|great|perfect|good|nice|ok(ay)?|awesome)\b.{0,60}$|\b(i('ll| will) use|i('ll| will) take|i like (this|that|it|the)|that works|looks good|this is (good|great|perfect))\b",
    "reject": r"^\W*(no\b|nope|not what|wrong)|\b(not what i (asked|wanted|meant)|i don'?t like|try again|you did(n'?t| not))\b",
}
RX = {k: re.compile(v, re.I) for k, v in GROUPS.items()}


def candidates():
    rows = load_windows()
    test = load_ids("sample.csv") | load_ids("gold.csv")
    held = [w for w in rows if w["window_id"] in test]
    p = pool(rows, {(w["dataset"], w["session_id"]) for w in held}, {(w["dataset"], w["participant_id"]) for w in held})
    used = set()
    for r in ("r1", "r2"):
        used |= set(open(os.path.join(CODEBOOK, "pilot", r, "ids.txt")).read().split())
    out = collections.defaultdict(list)
    for w in p:
        nr = w.get("next_request") or ""
        if w["window_id"] in used or not nr or len(nr) > 1500:  # long turns are mostly pasted text
            continue
        for k, rx in RX.items():
            if rx.search(nr):
                out[k].append(w)
    return p, out


if __name__ == "__main__":
    p, out = candidates()
    print("pool", len(p), {k: len(v) for k, v in out.items()})
    print("by dataset", {k: dict(collections.Counter(w["dataset"] for w in v)) for k, v in out.items()})
    if "--show" in sys.argv:
        n = int(sys.argv[sys.argv.index("--show") + 1])
        rng = random.Random(SEED)
        for k, v in out.items():
            s = sorted(v, key=lambda w: w["window_id"])
            rng.shuffle(s)
            print("==", k)
            for w in s[:n]:
                print(w["window_id"], "|", re.sub(r"\s+", " ", w["next_request"])[:150])
