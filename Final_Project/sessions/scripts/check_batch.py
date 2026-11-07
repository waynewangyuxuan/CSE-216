#!/usr/bin/env python3
"""End-of-batch check for a Bet 6 coder: every window of the batch labeled once, in session order. Usage: check_batch.py <labels.jsonl> <batch_index>. Prints counts and missing ids, no labels."""
import json, os, sys
import s6


def main():
    path, batch = sys.argv[1], int(sys.argv[2])
    idx = json.load(open(os.path.join(s6.BLIND, "index.json")))
    want = [w for s in json.load(open(os.path.join(s6.BLIND, "batches.json")))[batch] for w in idx["sessions"][s]]
    got = [r["window_id"] for r in s6.load_jsonl(path)]
    bad = sorted(set(want) - set(got)) + sorted(set(got) - set(want))
    dup = len(got) - len(set(got))
    order = [w for w in got if w in want]
    sess_ok = all([x for x in order if idx["windows"][x]["session"] == s] == idx["sessions"][s] for s in {idx["windows"][x]["session"] for x in order}) if not bad else False
    print(f"labels {len(got)} of {len(want)}, missing or extra {bad}, duplicates {dup}, session order kept {sess_ok}")
    sys.exit(0 if not bad and not dup and sess_ok else 1)


if __name__ == "__main__":
    main()
