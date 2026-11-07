"""Shared paths and loaders for Bet 4 scripts. Prints nothing."""
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODING = os.path.abspath(os.path.join(HERE, ".."))
FP = os.path.abspath(os.path.join(CODING, ".."))
DATA = os.path.join(FP, "data")
CODEBOOK = os.path.join(FP, "codebook")
sys.path.insert(0, os.path.join(CODEBOOK, "scripts"))
csv.field_size_limit(10 ** 9)
BLIND = os.path.join(CODING, "blind")     # git-excluded: views and coder files with free text
OUT = os.path.join(CODING, "results")     # labels-only and numbers-only, committed


def ids_of(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return [r["window_id"] for r in csv.DictReader(f)]


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]
