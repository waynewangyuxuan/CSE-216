#!/usr/bin/env python
"""Coder views for the selected conversations, one part file per window, read in order: blind/views/<session_id>/part_NN.txt.
Part NN holds turn NN's request, the AI response and the next user turn, uncut, with contact patterns masked and lines wrapped at 200 characters.
Together, parts 01..NN are the full history up to and including window NN; nothing after the next user turn is in them.
Holds no screen label, genre, audit result or inference content. Writes blind/batches.json (whole conversations per batch). Prints counts only."""
import csv, json, os, random, sys, textwrap
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7

WRAP, BATCH_CHARS, SEED = 200, 135000, 2167


def wrap(t):
    out = []
    for line in (t or "").split("\n"):
        out.extend(textwrap.wrap(line, WRAP, break_long_words=True, break_on_hyphens=False, replace_whitespace=False, drop_whitespace=False) or [""])
    return "\n".join(out)


def render(wid, sid, n, nparts, cov, req, resp, nxt):
    p = [f"WINDOW {wid}", "dataset: WildChat", f"coverage: {cov}" + ("  (not coded: blank request or response; context only)" if cov == "CX" else ""),
         f"turn_order: {n}", f"conversation: {sid}, part {n} of {nparts}",
         f"(Earlier turns of this conversation are parts 1 to {n - 1}.)" if n > 1 else "(This is the first turn of the conversation.)", "",
         "--- REQUEST (writer) ---", wrap(w7.mask(req)), "", "--- AI RESPONSE ---", wrap(w7.mask(resp)), "",
         "--- WHAT HAPPENED NEXT ---", ("NEXT USER TURN: " + wrap(w7.mask(nxt))) if nxt is not None else "(no later turn)", "", f"=== END OF WINDOW {wid} ==="]
    return "\n".join(p) + "\n"


def main():
    sel = list(csv.DictReader(open(os.path.join(w7.OUT, "selected_conversations.tsv")), delimiter="\t"))
    el = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    conv = w7.load_conversations({c["hash"]: (el[c["hash"]]["shard"], el[c["hash"]]["row"]) for c in sel})
    wins = list(csv.DictReader(open(os.path.join(w7.OUT, "windows_wildchat.csv"))))
    size, sess = {}, {}
    for c in sel:
        h, sid = c["hash"], c["session_id"]
        turns = conv[h]
        upos = [i for i, (r, _) in enumerate(turns) if r == "user"]
        mine = [w for w in wins if w["session_id"] == sid]
        d = os.path.join(w7.BLIND, "views", sid)
        os.makedirs(d, exist_ok=True)
        for w in mine:
            n = int(w["turn_order"])
            i = upos[n - 1]
            resp = turns[i + 1][1] if i + 1 < len(turns) and turns[i + 1][0] == "assistant" else ""
            nxt = turns[upos[n]][1] if n < len(upos) else None
            t = render(w["window_id"], sid, n, len(mine), w["coverage"], turns[i][1], resp, nxt)
            open(os.path.join(d, f"part_{n:02d}.txt"), "w", encoding="utf-8").write(t)
            size[w["window_id"]] = len(t)
        sess[sid] = [w["window_id"] for w in mine]
    keys = sorted(sess)
    random.Random(SEED).shuffle(keys)
    keys.sort(key=lambda k: -sum(size[i] for i in sess[k]))
    nb = max(1, round(sum(size.values()) / BATCH_CHARS))
    batches, load = [[] for _ in range(nb)], [0] * nb
    for k in keys:
        b = load.index(min(load))
        batches[b].append(k)
        load[b] += sum(size[i] for i in sess[k])
    json.dump(batches, open(os.path.join(w7.BLIND, "batches.json"), "w"), indent=1)
    os.makedirs(os.path.join(w7.BLIND, "lists"), exist_ok=True)
    coded = {w["window_id"] for w in wins if w["coded"] == "1"}
    for k, b in enumerate(batches):
        L = [f"Batch {k}: {len(b)} conversations. Read each conversation's parts in order; code each listed window before opening the next part.", ""]
        for sid in b:
            L.append(f"conversation {sid}: parts 1 to {len(sess[sid])} in {os.path.join(w7.BLIND, 'views', sid)}/")
            L.append("  code: " + " ".join(i for i in sess[sid] if i in coded))
        open(os.path.join(w7.BLIND, "lists", f"batch_{k}.txt"), "w").write("\n".join(L) + "\n")
    print(f"parts {len(size)}, chars {sum(size.values())}, largest part {max(size.values())}, largest conversation {max(sum(size[i] for i in v) for v in sess.values())}; "
          f"batches {nb}: conversations {[len(b) for b in batches]}, chars {load}")


if __name__ == "__main__":
    main()
