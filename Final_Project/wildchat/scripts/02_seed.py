#!/usr/bin/env python
"""Random seed for the LLM screen. No model. Writes results/seed_ids.tsv and blind/ids_seed.txt.
Seed = every eligible record of Bet 1's random 2,000 draw (lowest-hash draw, so a random subset), topped up with eligible records
in order of key("seed", hash) to SEED_N. Used conversations are left out. Split: train if key("split", hash) is even in its last hex digit, else test.
Bet 1's cached labels (first 3 user turns, research-writing definition) are not reused as labels; they are cross-tabbed on the overlap."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7

SEED_N = 1200


def main():
    el = [r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl")) if not r["used"]]
    hs = {r["hash"] for r in el}
    with open(os.path.join(w7.DATA, "wildchat_draw2000_log.tsv"), encoding="utf-8") as f:
        draw = [r["conversation_hash"] for r in csv.DictReader(f, delimiter="\t") if r["conversation_hash"] in hs]
    seed = list(dict.fromkeys(draw))
    for h in sorted(hs - set(seed), key=lambda h: w7.key("seed", h)):
        if len(seed) >= SEED_N:
            break
        seed.append(h)
    d = set(draw)
    with open(os.path.join(w7.OUT, "seed_ids.tsv"), "w") as f:
        f.write("hash\tsplit\tfrom_draw2000\n")
        for h in seed:
            f.write(f"{h}\t{'train' if int(w7.key('split', h)[-1], 16) % 2 == 0 else 'test'}\t{int(h in d)}\n")
    open(os.path.join(w7.BLIND, "ids_seed.txt"), "w").write("\n".join(seed) + "\n")
    print(f"seed {len(seed)}, from draw2000 {len(d)}")


if __name__ == "__main__":
    main()
