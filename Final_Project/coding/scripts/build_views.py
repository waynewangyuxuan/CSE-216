#!/usr/bin/env python3
"""Build Bet 4 coder views for the 100 sampled windows: one text file per window under blind/views/, plus batch lists and the sidecar of which earlier blocks were expanded.
Uses the whitelist of keys from views.py. Differs from views.build_view on purpose (see coding/decisions.tsv T01, T02):
main blocks are never cut; earlier blocks stay cut to 500 chars unless the request or editor reuses a 30+ char run from the cut part of an earlier AI response.
Lines are wrapped so reading tools cannot drop the end of a long line. Prints counts only."""
import json, os, random, textwrap
import bet4
from bet4 import BLIND, ids_of
from overlap import matched
from truncation import cut_span
from views import PRIOR_CAP, PRIOR_TURNS, VIEW_KEYS, _actions_text, cap, editor_text, load_windows

WRAP = 200
BATCH_CHARS = 135000  # about the view size Bet 3 gave a coder per round (r4: 145 KB)
SEED = 2164


def wrap(text):
    out = []
    for line in (text or "").split("\n"):
        out.extend(textwrap.wrap(line, WRAP, break_long_words=True, break_on_hyphens=False, replace_whitespace=False, drop_whitespace=False) or [""])
    return "\n".join(out)


def expand_prior(w, x, editor):
    """Show an earlier AI response whole if this request or editor reuses text from its cut part."""
    sp = cut_span(len(x["response"] or ""), PRIOR_CAP)
    if not sp:
        return False
    hid = x["response"][sp[0]:sp[1]]
    return matched(w["request"], hid)[0] >= 30 or matched(editor or "", hid)[0] >= 30


def build(w, by, at):
    earlier = [x for x in by[(w["dataset"], w["session_id"])] if x["turn_order"] < w["turn_order"]][-PRIOR_TURNS:]
    ed = editor_text(w) if w["dataset"] == "NIRVANA" else None
    prior, expanded = [], []
    for x in earlier:
        full = expand_prior(w, x, ed)
        if full:
            expanded.append(x["turn_order"])
        prior.append({"turn": x["turn_order"], "request": cap(x["request"], PRIOR_CAP), "response": x["response"] if full else cap(x["response"], PRIOR_CAP)})
    v = {"window_id": w["window_id"], "dataset": w["dataset"], "coverage": w["coverage"], "turn_order": w["turn_order"], "prior_turns": prior,
         "editor_before_request": ed, "request": w["request"], "response": w["response"], "next_actions_text": at(w)}
    assert set(v) == set(VIEW_KEYS)
    return v, expanded


def render(v):
    p = [f"WINDOW {v['window_id']}", f"dataset: {v['dataset']}", f"coverage: {v['coverage']}", f"turn_order: {v['turn_order']}", ""]
    for t in v["prior_turns"]:
        p += [f"--- EARLIER TURN {t['turn']}, WRITER ---", wrap(t["request"]), f"--- EARLIER TURN {t['turn']}, AI ---", wrap(t["response"]), ""]
    if v["dataset"] == "NIRVANA":
        p += ["--- EDITOR JUST BEFORE THIS REQUEST ---", wrap(v["editor_before_request"]) or "(empty)", ""]
    p += ["--- REQUEST ---", wrap(v["request"]), "", "--- AI RESPONSE ---", wrap(v["response"]), "",
          "--- WHAT HAPPENED NEXT ---", wrap(v["next_actions_text"]), "", f"=== END OF WINDOW {v['window_id']} ==="]
    return "\n".join(p) + "\n"


def main():
    sample = set(ids_of("sample.csv"))
    rows = load_windows()
    by = {}
    for w in rows:
        by.setdefault((w["dataset"], w["session_id"]), []).append(w)
    for v in by.values():
        v.sort(key=lambda x: x["turn_order"])
    at = _actions_text()
    d = os.path.join(BLIND, "views")
    os.makedirs(d, exist_ok=True)
    sizes, sess, exp = {}, {}, {}
    for w in rows:
        if w["window_id"] not in sample:
            continue
        v, expanded = build(w, by, at)
        t = render(v)
        with open(os.path.join(d, w["window_id"] + ".txt"), "w", encoding="utf-8") as f:
            f.write(t)
        sizes[w["window_id"]] = len(t)
        sess.setdefault((w["dataset"], w["session_id"]), []).append(w["window_id"])
        if expanded:
            exp[w["window_id"]] = expanded
    assert len(sizes) == 100
    # Whole sessions in shuffled order, so a coder meets a run together and batches mix datasets.
    keys = sorted(sess)
    random.Random(SEED).shuffle(keys)
    keys.sort(key=lambda k: -sum(sizes[i] for i in sess[k]))  # largest first, into the lightest batch
    n = max(1, round(sum(sizes.values()) / BATCH_CHARS))
    batches = [[] for _ in range(n)]
    load = [0] * n
    for k in keys:
        b = load.index(min(load))
        batches[b] += sorted(sess[k])
        load[b] += sum(sizes[i] for i in sess[k])
    with open(os.path.join(BLIND, "batches.json"), "w") as f:
        json.dump(batches, f, indent=1)
    with open(os.path.join(bet4.OUT, "views_expanded_prior.json"), "w") as f:
        json.dump(exp, f, indent=1, sort_keys=True)
    print(f"views {len(sizes)}, chars {sum(sizes.values())}, largest {max(sizes.values())}; batches {n}: windows {[len(b) for b in batches]}, chars {load}")
    print(f"windows with an earlier AI response shown whole: {len(exp)}")


if __name__ == "__main__":
    main()
