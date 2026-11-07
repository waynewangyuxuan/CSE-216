#!/usr/bin/env python3
"""Check pilot blinding by script. Prints counts and file names only.
1. Pilot windows share no window, session or participant with sample or gold.
2. No pilot view holds a long stretch of gold or sample text. Essay prompts and templates recur across sessions, so a
   40-character run seen in 3+ sessions counts as common text, and a view fails at 60+ remaining runs shared with one held-out window (about 100 characters).
3. Pilot views carry only whitelisted keys, so no LLM label or linkage.
4. Written documents hold no 40-character run of gold, sample or pilot window text."""
import collections, itertools, json, os, re, sys
import codes
from views import CODEBOOK, DATA, VIEW_KEYS, load_ids, load_windows, norm

K = 40
DOCS = ["CSE216_Research_Writing_Codebook_v1.1.md", "REPORT.md", "REPORT_AFTER_C3.md", "decisions.tsv", "C3_INSTRUCTIONS.md", "coder_briefs/coder_final_messages.md"]
SEP = re.compile(r"\s+")


def grams(text):
    t = norm(text).lower()
    return {t[i:i + K] for i in range(0, max(0, len(t) - K + 1))}


def main():
    errs = 0
    rows = load_windows()
    by_id = {w["window_id"]: w for w in rows}
    test = load_ids("sample.csv") | load_ids("gold.csv")
    held = [by_id[i] for i in test]
    blocked_s = {(w["dataset"], w["session_id"]) for w in held}
    blocked_p = {(w["dataset"], w["participant_id"]) for w in held}
    pilot = []
    rounds = sorted(d for d in os.listdir(os.path.join(CODEBOOK, "pilot")) if re.fullmatch(r"r\d+", d))
    for r in rounds:
        ids = open(os.path.join(CODEBOOK, "pilot", r, "ids.txt")).read().split()
        pilot += ids
        with open(os.path.join(CODEBOOK, "pilot", r, "view.jsonl"), encoding="utf-8") as f:
            for l in f:
                v = json.loads(l)
                if set(v) != set(VIEW_KEYS):
                    errs += 1
                    print("PROBLEM extra keys in view", r)
    ps = set(pilot)
    w_ov = len(ps & test)
    s_ov = len({(by_id[i]["dataset"], by_id[i]["session_id"]) for i in ps} & blocked_s)
    p_ov = len({(by_id[i]["dataset"], by_id[i]["participant_id"]) for i in ps} & blocked_p)
    dup = len(pilot) - len(ps)
    print(f"pilot windows {len(pilot)} in rounds {rounds}; overlap with sample/gold: windows {w_ov}, sessions {s_ov}, participants {p_ov}; drawn twice {dup}")
    errs += w_ov + s_ov + p_ov + dup
    # Essay prompts and pasted templates recur across many students. A run seen in 3+ sessions is common text, not a leak.
    seen = collections.Counter()
    for k, ws in itertools.groupby(sorted(rows, key=lambda w: (w["dataset"], w["session_id"])), key=lambda w: (w["dataset"], w["session_id"])):
        sg = set()
        for w in ws:
            sg |= grams(w["request"]) | grams(w["response"])
        seen.update(sg)
    held_g = set()
    for w in held:
        held_g |= grams(w["request"]) | grams(w["response"])
    rare = {g for g in held_g if seen[g] < 3}
    held_rare = {w["window_id"]: (grams(w["request"]) | grams(w["response"])) & rare for w in held}
    leak, worst, any_views = 0, 0, 0
    for r in rounds:
        with open(os.path.join(CODEBOOK, "pilot", r, "view.jsonl"), encoding="utf-8") as f:
            for l in f:
                v = json.loads(l)
                vg = set()
                for k in ("request", "response", "next_actions_text", "editor_before_request"):
                    vg |= grams(v[k])
                any_views += bool(vg & held_g)
                n = max((len(vg & h) for h in held_rare.values()), default=0)  # a leak is a stretch from ONE held-out window
                worst = max(worst, n)
                leak += n >= 60
    print(f"pilot views sharing any 40-char run with held-out text: {any_views}; rare runs shared with one held-out window, worst view {worst}; views at 60+ (about 100 characters): {leak}")
    errs += leak
    def full(w):
        return grams(w["request"]) | grams(w["response"]) | grams(w.get("next_request")) | grams(w.get("editor_before_request"))

    held_all = set().union(*(full(w) for w in held))
    pilot_g = set().union(*(full(by_id[i]) for i in ps))
    for d in DOCS:
        p = os.path.join(CODEBOOK, d)
        if not os.path.exists(p):
            print(f"{d}: not written yet")
            continue
        g = grams(open(p, encoding="utf-8").read())
        a, b = len(g & held_all), len(g & pilot_g)
        print(f"{d}: 40-char runs shared with gold/sample {a}, with pilot {b}")
        errs += (a > 0) + (b > 0)
    doc = open(os.path.join(CODEBOOK, DOCS[0]), encoding="utf-8").read()
    missing = [c for vals in codes.CODE_COLS.values() for c in vals if c not in ("HIGH", "MEDIUM", "LOW") and c not in doc]
    print("sheet codes missing from v1.1:", missing)
    errs += len(missing)
    print("problems:", errs)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
