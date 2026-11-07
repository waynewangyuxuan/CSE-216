"""Bet 9 (0010): numeric-only facts from the git-excluded raw files, written to analysis/derived/ and committed,
so a fresh clone can rerun every analysis without the raw data. Ids, seconds, counts and percentages only:
no request, response, editor or essay text, and no demographics.

Runs under data/raw/_venv (openpyxl, pyarrow). run_all.sh calls it only when the raw files exist; otherwise the
committed derived/ files are used as they are.

Outputs
- derived/timing_nirvana.csv, one row per NIRVANA window (347):
  request_s, response_s       seconds from the essay's first log row (the log's own clock)
  first_action_s              response -> first logged action of any kind (editor, chat, prompt pane); blank if none
  first_edit_s                response -> first editor edit (same edit ops as Bet 1's coverage rule); blank if none
  first_copy_ai_s             response -> first copy from the chat pane; blank if none
  dwell_s                     response -> next request; blank for the last window (open-ended)
  typed_chars, pasted_chars   characters added to the editor by typing and by paste before the next request
  deleted_chars               characters deleted from the editor before the next request
  copies_from_ai              copy operations in the chat pane before the next request
  editor_chars_before         length of the editor text when the request was sent (the writer's draft so far)
  editor_chars_after          length of the editor text just before the next request (or at the log's end)
- derived/outcome_nirvana.csv, one row per essay: the dataset's own final-essay measures (User Final %, GPT Final %,
  GPT Paste, User Add, Total Words, Total Time, GPT Inquiry, Perceived Ownership, Self Efficacy Score).
- derived/timing_wildchat.csv, one row per WildChat window (151). The release stamps only AI turns, so the one
  interval available is ai_reply_to_next_ai_reply_s: this window's AI reply to the next window's AI reply (the writer's
  reading and composing time plus the next reply's generation time); blank for the last window. reply_s is the AI
  reply's time from the conversation's first AI reply.
Usage: data/raw/_venv/bin/python analysis/scripts/extract_raw.py"""
import csv, json, os, sys
from datetime import timezone

HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.normpath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(FP, "data", "raw")
OUT = os.path.join(FP, "analysis", "derived")
EDIT_OPS = {"i", "d", "d_i", "p", "x", "z", "r"}       # data/scripts/01_nirvana_windows.py
OUTCOME = ["User Final %", "GPT Final %", "GPT Paste", "User Add", "Total Words", "Total Time", "GPT Inquiry",
           "Perceived Ownership", "Self Efficacy Score"]


def write(name, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def r1(x):
    return "" if x is None else f"{x:.1f}"


def nirvana():
    import openpyxl
    wins = [json.loads(l) for l in open(os.path.join(RAW, "_derived", "nirvana_windows.jsonl"), encoding="utf-8")]
    wb = openpyxl.load_workbook(os.path.join(RAW, "nirvana", "dataset.xlsx"), read_only=True)
    sheet = list(wb["Essay Data"].iter_rows(values_only=True))
    ix = {k: i for i, k in enumerate(sheet[0]) if k}
    time_of_row = {n: r[ix["time"]] for n, r in enumerate(sheet[1:], start=2) if len(r) > ix["time"]}
    start = {}
    for n, r in enumerate(sheet[1:], start=2):
        if len(r) > ix["time"] and isinstance(r[ix["time"]], (int, float)) and r[ix["essay_num"]] is not None:
            e = int(r[ix["essay_num"]])
            start[e] = min(start.get(e, r[ix["time"]]), r[ix["time"]])
    by = {}
    for w in wins:
        by.setdefault(w["session_id"], []).append(w)
    rows = []
    for sid in sorted(by):
        ws = sorted(by[sid], key=lambda w: w["turn_order"])
        t0 = start[ws[0]["trace"]["essay_num"]]
        for k, w in enumerate(ws):
            rt = w["response_time"]
            req = time_of_row[w["trace"]["request_row"]]
            nxt_req = time_of_row[ws[k + 1]["trace"]["request_row"]] if k + 1 < len(ws) else None
            acts = w["next_actions"]
            first = lambda pred: next((a["time"] - rt for a in acts if pred(a)), None) if rt is not None else None
            ed = [a for a in acts if a["op_loc"] == "editor"]
            rows.append({
                "window_id": w["window_id"], "session_id": sid, "turn_order": w["turn_order"],
                "request_s": r1(req - t0), "response_s": r1(rt - t0 if rt is not None else None),
                "first_action_s": r1(first(lambda a: a["op_type"] != "o")),
                "first_edit_s": r1(first(lambda a: a["op_loc"] == "editor" and a["op_type"] in EDIT_OPS)),
                "first_copy_ai_s": r1(first(lambda a: a["op_loc"] == "gpt" and a["op_type"] == "y")),
                "dwell_s": r1(nxt_req - rt if nxt_req is not None and rt is not None else None),
                "typed_chars": sum(len(a["add"]) for a in ed if a["op_type"] in ("i", "d_i")),
                "pasted_chars": sum(len(a["add"] or a["selected_text"]) for a in ed if a["op_type"] == "p"),
                "deleted_chars": sum(len(a["delete"]) for a in ed if a["op_type"] in ("d", "d_i", "x")),
                "copies_from_ai": sum(a["op_loc"] == "gpt" and a["op_type"] == "y" for a in acts),
                "editor_chars_before": len(w["editor_before_request"] or ""),
                "editor_chars_after": len(w["editor_after_next_actions"] or ""),
            })
    write("timing_nirvana.csv", rows)
    pr = list(wb["Participants"].iter_rows(values_only=True))
    pix = {k: i for i, k in enumerate(pr[0])}
    essays = {int(s[1:]) for s in by}
    out = []
    for r in pr[1:]:
        if r and r[0] is not None and int(r[0]) in essays:
            out.append({"session_id": f"e{int(r[0]):02d}", **{k: ("" if r[pix[k]] is None else round(float(r[pix[k]]), 4))
                                                               for k in OUTCOME}})
    write("outcome_nirvana.csv", sorted(out, key=lambda o: o["session_id"]))
    return len(rows), len(out)


def wildchat():
    import pyarrow.parquet as pq
    W = os.path.join(FP, "wildchat")
    wins = list(csv.DictReader(open(os.path.join(W, "results", "windows_wildchat.csv"), encoding="utf-8")))
    hashes = {w["conversation_hash"] for w in wins}
    loc = {}
    for l in open(os.path.join(W, "blind", "eligible.jsonl"), encoding="utf-8"):
        o = json.loads(l)
        if o["hash"] in hashes:
            loc.setdefault(o["shard"], {})[o["row"]] = o["hash"]
    turns = {}
    for s, rows in sorted(loc.items()):
        i = 0
        for b in pq.ParquetFile(os.path.join(RAW, "wildchat", s)).iter_batches(
                batch_size=1024, columns=["conversation_hash", "conversation"]):
            for rec in b.to_pylist():
                if i in rows:
                    assert rec["conversation_hash"] == rows[i]
                    turns[rows[i]] = [(t["role"], t["timestamp"]) for t in rec["conversation"]]
                i += 1
    assert set(turns) == hashes, len(hashes - set(turns))
    sec = lambda t: t.replace(tzinfo=timezone.utc).timestamp() if t is not None else None
    out = []
    for w in wins:
        tt = turns[w["conversation_hash"]]
        upos = [i for i, (r, _) in enumerate(tt) if r == "user"]
        n = int(w["turn_order"])
        i = upos[n - 1]
        reply = lambda j: sec(tt[j + 1][1]) if j + 1 < len(tt) and tt[j + 1][0] == "assistant" else None
        ai = reply(i)
        nxt = reply(upos[n]) if n < len(upos) else None
        t0 = next(sec(t) for r, t in tt if r == "assistant" and t is not None)
        out.append({"window_id": w["window_id"], "session_id": w["session_id"], "turn_order": n,
                    "reply_s": r1(ai - t0 if ai is not None else None),
                    "ai_reply_to_next_ai_reply_s": r1(nxt - ai if nxt is not None and ai is not None else None)})
    write("timing_wildchat.csv", out)
    return len(out)


def main():
    if not os.path.isdir(os.path.join(RAW, "nirvana")):
        print("extract_raw: skipped (raw data absent; committed derived/ files are used)")
        return
    a, b = nirvana()
    c = wildchat()
    print(f"extract_raw: NIRVANA windows {a}, essays {b}; WildChat windows {c}")


if __name__ == "__main__":
    main()
