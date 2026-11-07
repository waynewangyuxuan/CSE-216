#!/usr/bin/env python3
"""The only way the Bet 6 adjudicator writes a ruling. Reads one JSON object on stdin and appends it to the rulings file if it passes.
Refuses: a field not disputed in the packet, a second ruling on a field, a code not in v1.1, or a ruling while an earlier disputed window of the same session has no ruling yet.
Usage: add_ruling.py <packet.jsonl> <rulings.jsonl> <<'EOF' {json} EOF. Prints problems, never labels."""
import json, sys
import s6
import codes                               # codebook/scripts

KEYS = ["window_id", "field", "final", "settled", "rule", "reason"]


def main():
    packet, path = sys.argv[1], sys.argv[2]
    try:
        r = json.loads(sys.stdin.read())
    except ValueError as e:
        print("PROBLEM not one JSON object:", e)
        sys.exit(1)
    P = {l["window_id"]: l for l in s6.load_jsonl(packet)}
    have = {(x["window_id"], x["field"]) for x in s6.load_jsonl(path)}
    out = [f"missing key {k}" for k in KEYS if k not in r]
    if not out:
        i, f = r["window_id"], r["field"]
        if i not in P or f not in P[i]["fields"]:
            out.append("not a disputed field in this packet")
        elif (i, f) in have:
            out.append("already ruled; rulings are not revised")
        else:
            out += [f"rule on {w} first" for w, l in P.items() if l["session"] == P[i]["session"] and l["part"] < P[i]["part"]
                    and any((w, g) not in have for g in l["fields"])]
            if r["settled"] not in (True, False):
                out.append("settled is true or false")
            elif r["settled"] and r["final"] not in codes.CODE_COLS[f]:
                out.append("final is not a valid code for this field")
            elif not r["settled"] and r["final"]:
                out.append("final is empty when not settled")
            if not r["rule"] or not r["reason"]:
                out.append("rule and reason are needed")
    for p in out:
        print("PROBLEM", p)
    if out:
        sys.exit(1)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    left = sum(len(l["fields"]) for l in P.values()) - len(have) - 1
    print(f"ok {r['window_id']} {r['field']}; {left} disputed fields left in packet")


if __name__ == "__main__":
    main()
