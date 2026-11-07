#!/usr/bin/env python3
"""Check one Bet 7 labels file against v1.1's code lists and coverage rules. Reads that file, windows_wildchat.csv and the batch list only.
Usage: check_labels.py <labels.jsonl> [batch_index]. Prints problems, no labels."""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "codebook", "scripts"))
import codes

HERE = os.path.dirname(os.path.abspath(__file__))
W7 = os.path.abspath(os.path.join(HERE, ".."))
KEYS = ["window_id", "domain", "prior_own_work", "operation", "function", "object", "decision", "verification", "uptake", "confidence", "u4_subtype", "evidence_note", "flag_field", "flag_note"]
SUB = ["", "RESTATE_OR_ELABORATE", "MORE_OUTPUTS", "QUESTION", "STYLE", "ADD_OR_REMOVE_CONTENT", "OTHER"]


def windows():
    return {r["window_id"]: r for r in csv.DictReader(open(os.path.join(W7, "results", "windows_wildchat.csv")))}


def problems(r, cov):
    """Rule problems of one label row (WildChat). Shared with finalize.py."""
    out = []
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
    if r["prior_own_work"] == "NONE_VISIBLE":
        out.append("NONE_VISIBLE is NIRVANA only")
    if r["domain"] == "ESSAY_TASK":
        out.append("ESSAY_TASK is NIRVANA only")
    return out


def main():
    W = windows()
    rows, bad = [], 0
    for n, l in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
        if not l.strip():
            continue
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
        if i not in W or W[i]["coded"] != "1":
            print(i, "is not a window to code")
            bad += 1
            continue
        ps = problems(r, W[i]["coverage"])
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
        sids = json.load(open(os.path.join(W7, "blind", "batches.json")))[int(sys.argv[2])]
        want = {i for i, w in W.items() if w["session_id"] in sids and w["coded"] == "1"}
        d = want ^ set(ids)
        if d:
            print("ids differ from batch list:", sorted(d))
            bad += 1
    print(f"rows {len(rows)}, problems {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
