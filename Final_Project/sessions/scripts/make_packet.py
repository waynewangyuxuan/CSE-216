#!/usr/bin/env python3
"""Build Bet 6 adjudication packets: disputed fields of the new and sensitivity windows only, coders shown as first and second with a seeded flip per window (as Bet 4).
Sessions stay whole in one packet. Each line lists the part files to read before ruling, in order. Goes to blind/adjudication/. Prints counts only."""
import collections, json, os, random
import s6
from merge_labels import CODED
from merge import read_coder, window_set

SEED = 2164
MAX_CHARS = 260000   # parts an adjudicator reads, near Bet 4's single packet


def main():
    A, B, ws, m = read_coder("a"), read_coder("b"), window_set(), s6.meta()
    idx = json.load(open(os.path.join(s6.BLIND, "index.json")))
    rng = random.Random(SEED)
    d = os.path.join(s6.BLIND, "adjudication")
    os.makedirs(d, exist_ok=True)
    by_s, flips, by_field = collections.defaultdict(list), {}, collections.Counter()
    for i in sorted(m, key=lambda x: (m[x]["session"], m[x]["part"])):
        flip = rng.random() < .5
        flips[i] = "first=B" if flip else "first=A"
        if ws[i] == "bet4_kept":
            continue
        one, two = (B[i], A[i]) if flip else (A[i], B[i])
        fs = {f: {"first": one[f], "second": two[f]} for f in CODED if A[i][f] != B[i][f]}
        if fs:
            by_field.update(fs.keys())
            by_s[m[i]["session"]].append({"window_id": i, "session": m[i]["session"], "part": m[i]["part"], "fields": fs,
                                          "notes": {"first": {k: one.get(k, "") for k in ("evidence_note", "flag_field", "flag_note")},
                                                    "second": {k: two.get(k, "") for k in ("evidence_note", "flag_field", "flag_note")}}})
    def path(w):
        return os.path.join(s6.PARTS, m[w]["session"], w + ".txt")
    need = {s: idx["sessions"][s][:max(l["part"] for l in ls)] for s, ls in by_s.items()}
    size = {s: sum(os.path.getsize(path(w)) for w in ws_) for s, ws_ in need.items()}
    parts, cur, n = [], [], 0
    for s in sorted(by_s, key=lambda s: -size[s]):
        if cur and n + size[s] > MAX_CHARS:
            parts.append(cur)
            cur, n = [], 0
        cur.append(s)
        n += size[s]
    parts.append(cur)
    for k, ss in enumerate(parts):
        with open(os.path.join(d, f"packet_{k}.jsonl"), "w", encoding="utf-8") as f:
            for s in sorted(ss):
                for l in by_s[s]:
                    l["read_first"] = [path(w) for w in need[s][:l["part"]]]
                    f.write(json.dumps(l, ensure_ascii=False) + "\n")
    json.dump(flips, open(os.path.join(d, "flips.json"), "w"), indent=1)
    print(f"windows with a dispute {sum(map(len, by_s.values()))}, disputed fields {sum(by_field.values())}, by field {dict(by_field)}, packets {len(parts)}: sessions {[len(p) for p in parts]}, chars {[sum(size[s] for s in p) for p in parts]}")


if __name__ == "__main__":
    main()
