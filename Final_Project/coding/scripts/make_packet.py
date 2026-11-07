#!/usr/bin/env python3
"""Build the adjudication packet: only disputed fields, coders shown as first and second with a seeded flip per window. Fable labels are not read. Goes to blind/. Prints counts only."""
import collections, json, os, random
import bet4
from bet4 import BLIND
from merge_labels import CODED, read_coder

SEED = 2164
MAX_CHARS = 300000  # one adjudicator reads all disputed windows


def main():
    A, B = read_coder("a"), read_coder("b")
    rng = random.Random(SEED)
    d = os.path.join(BLIND, "adjudication")
    os.makedirs(d, exist_ok=True)
    lines, flips, by_field = [], {}, collections.Counter()
    for i in sorted(A):
        flip = rng.random() < .5
        one, two = (B[i], A[i]) if flip else (A[i], B[i])
        flips[i] = "first=B" if flip else "first=A"
        fs = {f: {"first": one[f], "second": two[f]} for f in CODED if A[i][f] != B[i][f]}
        if fs:
            by_field.update(fs.keys())
            lines.append({"window_id": i, "fields": fs, "notes": {"first": {k: one.get(k, "") for k in ("evidence_note", "flag_field", "flag_note")},
                                                                  "second": {k: two.get(k, "") for k in ("evidence_note", "flag_field", "flag_note")}}})
    size = {l["window_id"]: os.path.getsize(os.path.join(BLIND, "views", l["window_id"] + ".txt")) for l in lines}
    parts, cur, n = [], [], 0
    for l in lines:
        if cur and n + size[l["window_id"]] > MAX_CHARS:
            parts.append(cur)
            cur, n = [], 0
        cur.append(l)
        n += size[l["window_id"]]
    parts.append(cur)
    for k, p in enumerate(parts):
        with open(os.path.join(d, f"packet_{k}.jsonl"), "w", encoding="utf-8") as f:
            for l in p:
                f.write(json.dumps(l, ensure_ascii=False) + "\n")
    json.dump(flips, open(os.path.join(d, "flips.json"), "w"), indent=1)
    print(f"windows with a dispute {len(lines)}, disputed fields {sum(by_field.values())}, by field {dict(by_field)}, parts {[len(p) for p in parts]}, chars {sum(size.values())}")


if __name__ == "__main__":
    main()
