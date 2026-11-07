"""Shared paths, seeds and readers for Bet 7 (WildChat formal long-form writing). Prints nothing.
Everything holding dataset text goes under blind/ (git-excluded). results/ holds ids, hashes, labels and counts only."""
import csv, glob, hashlib, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
W7 = os.path.abspath(os.path.join(HERE, ".."))
FP = os.path.abspath(os.path.join(W7, ".."))
DATA = os.path.join(FP, "data")
RAW = os.path.join(DATA, "raw", "wildchat")
BLIND = os.path.join(W7, "blind")
OUT = os.path.join(W7, "results")
SEED = 2167
csv.field_size_limit(10 ** 9)

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])")
COLS = ["conversation_hash", "language", "hashed_ip", "toxic", "conversation.list.element.content", "conversation.list.element.role"]


def key(*parts):
    """Deterministic pseudo-random sort key, independent of row order and Python hash seed."""
    return hashlib.sha256((str(SEED) + "|" + "|".join(map(str, parts))).encode()).hexdigest()


def mask(t):
    return PHONE.sub("[masked]", EMAIL.sub("[masked]", t or ""))


def shards():
    fs = sorted(glob.glob(os.path.join(RAW, "*.parquet")))
    assert len(fs) == 14, len(fs)
    return fs


def read_jsonl(p):
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def write_jsonl(p, rows):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def load_conversations(locs):
    """locs: {hash: (shard_name, row)}. Returns {hash: [(role, content), ...]} read from raw parquet."""
    import pyarrow.parquet as pq
    by = {}
    for h, (s, r) in locs.items():
        by.setdefault(s, {})[r] = h
    out = {}
    for s, rows in sorted(by.items()):
        pf, i = pq.ParquetFile(os.path.join(RAW, s)), 0
        for b in pf.iter_batches(batch_size=4096, columns=["conversation_hash", "conversation.list.element.content", "conversation.list.element.role"]):
            for rec in b.to_pylist():
                if i in rows:
                    assert rec["conversation_hash"] == rows[i]
                    out[rows[i]] = [(t["role"], t["content"] or "") for t in rec["conversation"]]
                i += 1
    return out


def clip(t, n):
    t = t or ""
    if len(t) <= n:
        return t
    h = int(n * 0.75)
    return t[:h] + f" [...{len(t) - n} chars cut...] " + t[-(n - h):]


def excerpt(turns, ucap=1500, acap=500, total=14000):
    """Whole conversation for a screening model: every turn, numbered, user turns and AI turns cut to caps, contact details masked.
    Caps shrink until the excerpt fits the total."""
    for uc, ac in ((ucap, acap), (1000, 300), (700, 200), (500, 120), (350, 80)):
        parts, n = [], 0
        for role, c in turns:
            if role == "user":
                n += 1
                parts.append(f"[USER {n}] " + clip(mask(c), uc))
            else:
                parts.append(f"[AI {n}] " + clip(mask(c), ac))
        s = "\n".join(parts)
        if len(s) <= total:
            return s
    return s[:total] + " [...rest of conversation cut...]"
