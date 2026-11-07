#!/usr/bin/env python3
"""Stop dataset text from being committed. Run after `git add`, before `git commit`. Prints counts and paths only.
Fails if a staged file is outside Final_Project/wildchat/, is under blind/, has a free-text note column, or shares a 40-character run
(whitespace collapsed, lowercased) with: every turn of the selected and Bet 4 conversations, plus the masked user text of every
conversation any LLM labelled here. Usage: check_staged.py [--all-tracked]"""
import csv, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7

K = 40
BAN = ("evidence_note", "flag_note", "reason", "note")


def grams(t):
    t = re.sub(r"\s+", " ", t or "").strip().lower()
    return {hash(t[i:i + K]) for i in range(max(0, len(t) - K + 1))}


def main():
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    cmd = ["git", "ls-files", "--", "Final_Project/wildchat"] if "--all-tracked" in sys.argv else ["git", "diff", "--cached", "--name-only", "--diff-filter=d"]
    paths = [p for p in subprocess.check_output(cmd, text=True, cwd=root).split("\n") if p]
    el = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    full = {r["hash"] for r in csv.DictReader(open(os.path.join(w7.OUT, "selected_conversations.tsv")), delimiter="\t")}
    loc = {h: (el[h]["shard"], el[h]["row"]) for h in full}
    extra = os.path.join(w7.BLIND, "extra_locations.json")
    if os.path.exists(extra):
        loc.update({h: tuple(v) for h, v in json.load(open(extra)).items()})
    bank = set()
    for turns in w7.load_conversations(loc).values():
        for _, c in turns:
            bank |= grams(c)
    labelled = set()
    for f in ("screen_labels.jsonl", "audit_labels.jsonl"):
        p = os.path.join(w7.OUT, f)
        if os.path.exists(p):
            labelled |= {r["hash"] for r in w7.read_jsonl(p)}
    with open(os.path.join(w7.BLIND, "embed_text.jsonl"), encoding="utf-8") as fh:
        for l in fh:
            r = json.loads(l)
            if r["hash"] in labelled:
                bank |= grams(r["text"])
    bad = 0
    for p in paths:
        if not p.startswith("Final_Project/wildchat/") or "/blind/" in p:
            print("PROBLEM path not allowed:", p)
            bad += 1
            continue
        blob = subprocess.check_output(["git", "show", ":" + p] if "--all-tracked" not in sys.argv else ["git", "show", "HEAD:" + p], cwd=root).decode("utf-8", "replace")
        head = blob.split("\n", 1)[0].lower()
        hits = len(grams(blob) & bank)
        cols = [b for b in BAN if (p.endswith(".csv") or p.endswith(".tsv")) and re.search(rf"(^|[,\t]){b}([,\t]|$)", head)]
        print(f"{p}: chars {len(blob)}, 40-char runs shared with conversation text {hits}" + (f", banned columns {cols}" if cols else ""))
        bad += (hits > 0) + bool(cols)
    print(f"files {len(paths)}, conversations in bank {len(loc)} whole + {len(labelled)} user text, grams {len(bank)}, problems {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
