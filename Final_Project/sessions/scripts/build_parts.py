#!/usr/bin/env python3
"""Build Bet 6 part files: one text file per NIRVANA window, blind/parts/<session>/<window_id>.txt, read in turn order (decisions.tsv S01, S02).
Part k holds window k whole: editor before the request, request, AI response, what happened next. No block is cut. Reading parts 1..k gives
the full session history up to window k. Also writes blind/index.json and blind/batches.json (whole sessions, about Bet 4's batch size).
Uses Bet 4's wrap and the whitelist of view keys. Prints counts only."""
import json, os, random
import s6
from build_views import wrap            # coding/scripts, Bet 4
from views import VIEW_KEYS, _actions_text, editor_text, load_windows

BATCH_CHARS = 145000  # Bet 4 batches were 145 to 148 KB
SEED = 2164


def render(w, k, n, at):
    v = {"window_id": w["window_id"], "dataset": w["dataset"], "coverage": w["coverage"], "turn_order": w["turn_order"], "prior_turns": [],
         "editor_before_request": editor_text(w), "request": w["request"], "response": w["response"], "next_actions_text": at(w)}
    assert set(v) == set(VIEW_KEYS)
    s = w["session_id"]
    p = [f"WINDOW {v['window_id']}", f"dataset: {v['dataset']}", f"coverage: {v['coverage']}", f"turn_order: {v['turn_order']}",
         f"session: {s}, part {k} of {n}", "",
         "--- EDITOR JUST BEFORE THIS REQUEST ---", wrap(v["editor_before_request"]) or "(empty)", "",
         "--- REQUEST ---", wrap(v["request"]), "", "--- AI RESPONSE ---", wrap(v["response"]), "",
         "--- WHAT HAPPENED NEXT ---", wrap(v["next_actions_text"]), "", f"=== END OF WINDOW {v['window_id']} (session {s}, part {k} of {n}) ==="]
    return "\n".join(p) + "\n"


def main():
    rows = [w for w in load_windows() if w["dataset"] == "NIRVANA"]
    by = {}
    for w in rows:
        by.setdefault(w["session_id"], []).append(w)
    at = _actions_text()
    index, size = {}, {}
    for s, ws in by.items():
        ws.sort(key=lambda x: x["turn_order"])
        assert len({w["turn_order"] for w in ws}) == len(ws)
        d = os.path.join(s6.PARTS, s)
        os.makedirs(d, exist_ok=True)
        for k, w in enumerate(ws, 1):
            t = render(w, k, len(ws), at)
            open(os.path.join(d, w["window_id"] + ".txt"), "w", encoding="utf-8").write(t)
            index[w["window_id"]] = {"session": s, "part": k, "parts": len(ws), "turn_order": w["turn_order"], "coverage": w["coverage"], "dataset": "NIRVANA"}
            size[s] = size.get(s, 0) + len(t)
    assert len(index) == 347 and len(by) == 71, (len(index), len(by))
    keys = sorted(by)
    random.Random(SEED).shuffle(keys)
    keys.sort(key=lambda k: -size[k])  # largest first, into the lightest batch
    n = max(1, round(sum(size.values()) / BATCH_CHARS))
    batches, load = [[] for _ in range(n)], [0] * n
    for k in keys:
        b = load.index(min(load))
        batches[b].append(k)
        load[b] += size[k]
    for b in batches:
        b.sort()
    order = {s: [w["window_id"] for w in by[s]] for s in by}
    json.dump({"windows": index, "sessions": order}, open(os.path.join(s6.BLIND, "index.json"), "w"), indent=1, sort_keys=True)
    json.dump(batches, open(os.path.join(s6.BLIND, "batches.json"), "w"), indent=1)
    os.makedirs(os.path.join(s6.BLIND, "lists"), exist_ok=True)
    for i, b in enumerate(batches):
        with open(os.path.join(s6.BLIND, "lists", f"batch_{i}.txt"), "w") as f:
            for s in b:
                for wid in order[s]:
                    f.write(os.path.join(s6.PARTS, s, wid + ".txt") + "\n")
    print(f"parts {len(index)}, sessions {len(by)}, chars {sum(size.values())}, largest session {max(size.values())}; batches {n}: sessions {[len(b) for b in batches]}, windows {[sum(len(order[s]) for s in b) for b in batches]}, chars {load}")


if __name__ == "__main__":
    main()
