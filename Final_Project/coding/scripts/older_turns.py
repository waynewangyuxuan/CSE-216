#!/usr/bin/env python3
"""Measure the 3-turn limit of coder views: which sampled windows have earlier turns no coder saw, and whose request or editor reuses a 30+ character run from an AI response in those unseen turns.
Writes results/older_turns.json. Prints ids, shares and code labels only, no window text."""
import csv, json, os
import bet4
from bet4 import OUT, ids_of
from overlap import matched
from views import PRIOR_TURNS, editor_text, load_windows, norm


def short(v):
    return (v or "").split("_")[0]


def main():
    sample, gold = set(ids_of("sample.csv")), set(ids_of("gold.csv"))
    rows = load_windows()
    by = {}
    for w in rows:
        by.setdefault((w["dataset"], w["session_id"]), []).append(w)
    Fin = {r["window_id"]: r for r in csv.DictReader(open(os.path.join(OUT, "final_labels.csv")))}
    has_older, reuse = [], {}
    for w in rows:
        i = w["window_id"]
        if i not in sample:
            continue
        s = sorted(by[(w["dataset"], w["session_id"])], key=lambda x: x["turn_order"])
        earlier = [x for x in s if x["turn_order"] < w["turn_order"]]
        older = earlier[:-PRIOR_TURNS] if len(earlier) > PRIOR_TURNS else []
        if not older:
            continue
        has_older.append(i)
        src = "\n".join(x["response"] or "" for x in older)
        ed = editor_text(w) if w["dataset"] == "NIRVANA" else ""
        rm, rl = matched(w["request"], src)
        em, el = matched(ed or "", src)
        if rm >= 30 or em >= 30:
            reuse[i] = {"older_turns": len(older), "share_request_from_unseen_ai": round(rm / max(1, rl), 2), "share_editor_from_unseen_ai": round(em / max(1, el), 2), "gold": i in gold,
                        "decision": short(Fin[i]["decision"]), "prior_own_work": Fin[i]["prior_own_work"], "decision_source": Fin[i]["decision_source"], "prior_source": Fin[i]["prior_own_work_source"]}
    res = {"windows_with_unseen_older_turns": sorted(has_older), "windows_reusing_unseen_ai_text": reuse}
    with open(os.path.join(OUT, "older_turns.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print(len(has_older), "windows with unseen older turns;", len(reuse), "reuse unseen AI text;", sum(i in gold for i in has_older), "gold with older turns")
    for i, v in sorted(reuse.items()):
        print(i, v)


if __name__ == "__main__":
    main()
