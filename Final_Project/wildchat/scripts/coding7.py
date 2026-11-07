"""Bet 7 coding helpers: read coder files, merge, packet, finalize. Prints nothing on import. No model calls; no text written to results/."""
import collections, csv, glob, json, os, random, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "codebook", "scripts"))
import w7, codes
from agreement import FAMILY  # codebook/scripts/agreement.py, read-only reuse

CODED = ["domain", "prior_own_work", "operation", "function", "object", "decision", "verification", "uptake"]
PMAP = {f"O{i:02d}": ("P" if i <= 9 else "T" if i <= 11 else "R" if i <= 15 else "M") for i in range(1, 17)} | {"OX": "PX"}
ID_COLS = ["window_id", "session_id", "cluster", "turn_order", "coverage"]
UNSET = "UNSETTLED"
SEED = 2167


def meta():
    sel = {r["session_id"]: r for r in csv.DictReader(open(os.path.join(w7.OUT, "selected_conversations.tsv")), delimiter="\t")}
    out = {}
    for r in csv.DictReader(open(os.path.join(w7.OUT, "windows_wildchat.csv"))):
        if r["coded"] == "1":
            out[r["window_id"]] = {"window_id": r["window_id"], "session_id": r["session_id"], "cluster": sel[r["session_id"]]["cluster"],
                                   "turn_order": r["turn_order"], "coverage": r["coverage"]}
    return out


def read_coder(c):
    rows = {}
    for p in sorted(glob.glob(os.path.join(w7.BLIND, f"coder_{c}", "batch_*.jsonl"))):
        for r in w7.read_jsonl(p):
            assert r["window_id"] not in rows, r["window_id"]
            rows[r["window_id"]] = r
    return rows


def short(v):
    return (v or "").split("_")[0]
