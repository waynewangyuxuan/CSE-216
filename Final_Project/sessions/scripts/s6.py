"""Shared paths and loaders for Bet 6 (sessions/) scripts. Reuses Bet 4 and codebook scripts by import; edits neither. Prints nothing."""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.abspath(os.path.join(HERE, ".."))
FP = os.path.abspath(os.path.join(SESS, ".."))
CODING = os.path.join(FP, "coding")
CODEBOOK = os.path.join(FP, "codebook")
sys.path.insert(0, os.path.join(CODEBOOK, "scripts"))
sys.path.insert(1, os.path.join(CODING, "scripts"))
csv.field_size_limit(10 ** 9)
BLIND = os.path.join(SESS, "blind")   # git-excluded: part files, coder and adjudicator files with free text
OUT = os.path.join(SESS, "results")   # labels-only and numbers-only, committed
PARTS = os.path.join(BLIND, "parts")
BET4 = os.path.join(CODING, "results")


def load_jsonl(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def meta():
    """window_id -> session, turn, coverage, from parts/index.json (built by build_parts.py)."""
    return json.load(open(os.path.join(BLIND, "index.json")))["windows"]


def bet4_final():
    return {r["window_id"]: r for r in csv.DictReader(open(os.path.join(BET4, "final_labels.csv"))) if r["dataset"] == "NIRVANA"}


def sensitivity_ids():
    return sorted(json.load(open(os.path.join(BET4, "older_turns.json")))["windows_with_unseen_older_turns"])
