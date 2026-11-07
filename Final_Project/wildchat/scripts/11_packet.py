#!/usr/bin/env python3
"""Adjudication packet: disputed fields only, coders shown as first and second with a seeded flip per window. Goes to blind/adjudication/. Prints counts."""
import collections, json, os, random
from coding7 import CODED, SEED, read_coder, w7


def main():
    A, B = read_coder("a"), read_coder("b")
    rng = random.Random(SEED)
    d = os.path.join(w7.BLIND, "adjudication")
    os.makedirs(d, exist_ok=True)
    lines, flips, by = [], {}, collections.Counter()
    for i in sorted(A):
        flip = rng.random() < .5
        one, two = (B[i], A[i]) if flip else (A[i], B[i])
        flips[i] = "first=B" if flip else "first=A"
        fs = {f: {"first": one[f], "second": two[f]} for f in CODED if A[i][f] != B[i][f]}
        if fs:
            by.update(fs)
            lines.append({"window_id": i, "conversation": i.split("-")[1], "turn": int(i.rsplit("t", 1)[1]), "fields": fs,
                          "notes": {k: {x: o.get(x, "") for x in ("evidence_note", "flag_field", "flag_note")} for k, o in (("first", one), ("second", two))}})
    with open(os.path.join(d, "packet_0.jsonl"), "w", encoding="utf-8") as f:
        for l in lines:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    json.dump(flips, open(os.path.join(d, "flips.json"), "w"), indent=1)
    print(f"windows with a dispute {len(lines)}, disputed fields {sum(by.values())}, by field {dict(by)}")


if __name__ == "__main__":
    main()
