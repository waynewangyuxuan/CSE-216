#!/usr/bin/env python3
"""Check one labels file against v1.1's code lists and coverage rules. Reads only that file and view headers. Usage: check_labels.py <labels.jsonl> [batch_index]. Prints problems, no labels."""
import json, os, sys
import bet4
from bet4 import BLIND
import codes

KEYS = ["window_id", "domain", "prior_own_work", "operation", "function", "object", "decision", "verification", "uptake", "confidence", "u4_subtype", "evidence_note", "flag_field", "flag_note"]
SUB = ["", "RESTATE_OR_ELABORATE", "MORE_OUTPUTS", "QUESTION", "STYLE", "ADD_OR_REMOVE_CONTENT", "OTHER"]


def head(i):
    with open(os.path.join(BLIND, "views", i + ".txt"), encoding="utf-8") as f:
        ls = [f.readline().strip() for _ in range(3)]
    return ls[1].split(": ")[1], ls[2].split(": ")[1]


def problems(r):
    """Rule problems of one label row. Shared with the final-label check."""
    out = []
    ds, cov = head(r["window_id"])
    for k, vals in codes.CODE_COLS.items():
        if k in r and r[k] not in vals:
            out.append(f"{k} is not a valid code")
    if cov == "C0" and (r["verification"] != "VX_UNOBSERVABLE" or r["uptake"] != "UX_NO_TRACE"):
        out.append("C0 needs VX and UX")
    if cov != "C0" and r["verification"] == "VX_UNOBSERVABLE":
        out.append("VX is C0 only")
    if cov == "C1" and r["uptake"][:2] in ("U1", "U2", "U3", "U7"):
        out.append("C1 never takes U1, U2, U3, U7")
    if r["uptake"].startswith("U8") and not r["verification"].startswith("V0"):
        out.append("U8 needs V0")
    if ds == "NIRVANA" and r["prior_own_work"] == "UNOBSERVABLE":
        out.append("UNOBSERVABLE is for chat-only data")
    if ds == "WildChat" and r["prior_own_work"] == "NONE_VISIBLE":
        out.append("NONE_VISIBLE is NIRVANA only")
    if ds == "NIRVANA" and r["domain"] != "ESSAY_TASK":
        out.append("NIRVANA domain is ESSAY_TASK")
    return out


def main():
    path = sys.argv[1]
    bad = 0
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, l in enumerate(f, 1):
            try:
                rows.append(json.loads(l))
            except ValueError:
                print(f"line {n}: not JSON")
                bad += 1
    for r in rows:
        i = r.get("window_id", "?")
        miss = [k for k in KEYS if k not in r]
        if miss:
            print(i, "missing keys", miss)
            bad += 1
            continue
        ps = problems(r)
        if r["u4_subtype"] not in SUB:
            ps.append("u4_subtype not a listed value")
        if bool(r["u4_subtype"]) and not r["uptake"].startswith("U4"):
            ps.append("u4_subtype only with U4")
        if not r["evidence_note"]:
            ps.append("evidence_note empty")
        for p in ps:
            print(i, p)
        bad += len(ps)
    ids = [r.get("window_id") for r in rows]
    if len(ids) != len(set(ids)):
        print("duplicate window_id")
        bad += 1
    if len(sys.argv) > 2:
        want = json.load(open(os.path.join(BLIND, "batches.json")))[int(sys.argv[2])]
        d = set(want) ^ set(ids)
        if d:
            print("ids differ from batch list:", sorted(d))
            bad += 1
    print(f"rows {len(rows)}, problems {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
