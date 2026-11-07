#!/usr/bin/env python3
"""The only way a Bet 6 coder writes a label (decisions.tsv S02). Reads one JSON object on stdin and appends it to the labels file if it passes.
Refuses: bad format or codes, v1.1 coverage rules broken, a window not in the batch, a second label for a window, or a window whose earlier
windows in its session are not labeled yet. Usage: add_label.py <labels.jsonl> <batch_index> <<'EOF' {json} EOF. Prints problems, never labels."""
import json, os, sys
import s6
import check_labels                      # coding/scripts, Bet 4: KEYS, SUB, problems()
from check_labels import KEYS, SUB


def head(i):
    m = s6.meta()[i]
    return m["dataset"], m["coverage"]


check_labels.head = head                 # Bet 4's rule check, pointed at Bet 6's index instead of Bet 4 views


def problems(r, path, batch):
    idx = json.load(open(os.path.join(s6.BLIND, "index.json")))
    sessions = json.load(open(os.path.join(s6.BLIND, "batches.json")))[batch]
    want = [w for s in sessions for w in idx["sessions"][s]]
    miss = [k for k in KEYS if k not in r]
    if miss:
        return [f"missing keys {miss}"]
    extra = [k for k in r if k not in KEYS]
    i = r["window_id"]
    if i not in want:
        return [f"{i} is not in batch {batch}"]
    have = {x["window_id"] for x in s6.load_jsonl(path)}
    if i in have:
        return [f"{i} already has a label; labels are not revised"]
    s = idx["windows"][i]["session"]
    before = idx["sessions"][s][:idx["windows"][i]["part"] - 1]
    out = [f"label earlier window {w} first" for w in before if w not in have]
    out += check_labels.problems(r)
    if r["u4_subtype"] not in SUB:
        out.append("u4_subtype not a listed value")
    if bool(r["u4_subtype"]) and not r["uptake"].startswith("U4"):
        out.append("u4_subtype only with U4")
    if not r["evidence_note"]:
        out.append("evidence_note empty")
    if r["confidence"] not in ("HIGH", "MEDIUM", "LOW"):
        out.append("confidence is HIGH, MEDIUM or LOW")
    if extra:
        out.append(f"unknown keys {extra}")
    return out


def main():
    path, batch = sys.argv[1], int(sys.argv[2])
    try:
        r = json.loads(sys.stdin.read())
    except ValueError as e:
        print("PROBLEM not one JSON object:", e)
        sys.exit(1)
    ps = problems(r, path, batch)
    for p in ps:
        print("PROBLEM", p)
    if ps:
        sys.exit(1)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"ok {r['window_id']}: {len(s6.load_jsonl(path))} labels in file")


if __name__ == "__main__":
    main()
