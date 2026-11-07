#!/usr/bin/env python
"""Seeded draw of conversations to code, from the screen-accepted pool. No model.
Accepted = screen label INCLUDE and a user turn after the first writing turn (W02); an INCLUDE with first_writing_turn 0 is read as turn 1.
Rules (decisions.tsv W10): drawn only from the RANDOM SEED's accepted conversations, so ranking by keywords or embeddings cannot bias
the coded sample; unused conversations only; at most one per IP cluster; order by key("select", hash); a conversation is coded from
turn 1 to turn CAP at most, and needs its first writing turn inside that run; add conversations until MIN_CONV and MIN_WINDOWS are both met.
Windows: one per user turn. CX (blank request or response) is shown but not coded; C0 = no later user turn or a blank one; else C1.
Writes results/selected_conversations.tsv and results/windows_wildchat.csv (ids, coverage, no text)."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7

CAP, MIN_CONV, MIN_WINDOWS = 10, 30, 150


def accepted(lab, el):
    out = {}
    for h, l in lab.items():
        if h in el and l["label"] == "INCLUDE":
            fwt = l["first_writing_turn"] or 1
            if fwt < el[h]["user_turns"]:
                out[h] = fwt
    return out


def windows_of(turns, cap):
    upos = [i for i, (r, _) in enumerate(turns) if r == "user"]
    ws = []
    for n, i in enumerate(upos[:cap], start=1):
        req = turns[i][1]
        resp = turns[i + 1][1] if i + 1 < len(turns) and turns[i + 1][0] == "assistant" else ""
        nxt = turns[upos[n]][1] if n < len(upos) else None
        cov = "CX" if not req.strip() or not resp.strip() else ("C1" if nxt is not None and nxt.strip() else "C0")
        ws.append({"turn": n, "coverage": cov, "req_i": i})
    return ws, len(upos)


def main():
    el = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    lab = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.OUT, "screen_labels.jsonl"))}
    acc = accepted(lab, el)
    seed = {l.split("\t")[0] for l in open(os.path.join(w7.OUT, "seed_ids.tsv")).read().split("\n")[1:] if l}
    pool = sorted((h for h in acc if h in seed and not el[h]["used"] and acc[h] <= CAP), key=lambda h: w7.key("select", h))
    conv = w7.load_conversations({h: (el[h]["shard"], el[h]["row"]) for h in pool[:400]})
    chosen, clusters, rows, skipped = [], set(), [], {"cluster_taken": 0}
    for h in pool[:400]:
        if len(chosen) >= MIN_CONV and sum(1 for r in rows if r["coverage"] != "CX") >= MIN_WINDOWS:
            break
        if el[h]["cluster"] in clusters:
            skipped["cluster_taken"] += 1
            continue
        clusters.add(el[h]["cluster"])
        ws, nu = windows_of(conv[h], CAP)
        chosen.append({"hash": h, "session_id": h[:12], "cluster": el[h]["cluster"], "user_turns": nu, "coded_turns": len(ws),
                       "turns_beyond_cap": max(0, nu - CAP), "first_writing_turn": acc[h], "genre": lab[h]["genre"], "select_order": pool.index(h) + 1})
        for w in ws:
            rows.append({"window_id": f"WILDCHAT-{h[:12]}-t{w['turn']:02d}", "session_id": h[:12], "conversation_hash": h, "turn_order": w["turn"],
                         "coverage": w["coverage"], "coded": int(w["coverage"] != "CX")})
    with open(os.path.join(w7.OUT, "selected_conversations.tsv"), "w") as f:
        k = list(chosen[0])
        f.write("\t".join(k) + "\n")
        for c in chosen:
            f.write("\t".join(str(c[x]) for x in k) + "\n")
    with open(os.path.join(w7.OUT, "windows_wildchat.csv"), "w", newline="") as f:
        wr = csv.DictWriter(f, list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    coded = [r for r in rows if r["coded"]]
    print(json.dumps({"accepted": len(acc), "seed_pool_unused_fwt_le_cap": len(pool), "conversations": len(chosen), "windows_all": len(rows),
                      "windows_coded": len(coded), "by_coverage": {c: sum(r["coverage"] == c for r in rows) for c in ("C0", "C1", "CX")},
                      "turns_beyond_cap": sum(c["turns_beyond_cap"] for c in chosen), "skipped": skipped}))


if __name__ == "__main__":
    main()
