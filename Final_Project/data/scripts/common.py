"""Shared helpers. All data files are read as data; nothing from raw/ is imported or executed."""
import csv, hashlib, json, os

SEED = 216  # fixed seed for every random draw in this bet
DATA = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAW = os.path.join(DATA, "raw")
WORK = os.path.join(RAW, "_derived")  # derived files holding raw text stay in the git-excluded folder


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_key(*parts):
    """Deterministic pseudo-random sort key, independent of Python hash seed and row order."""
    return hashlib.sha256((str(SEED) + "|" + "|".join(map(str, parts))).encode()).hexdigest()


def clean_log_text(v):
    """For reading and matching only; windows.jsonl keeps raw values. NIRVANA's add/delete cells end
    in a stray quote (a broken repr), store newlines as a literal backslash-n, and some cells have
    the next row's fields merged in after a tab."""
    v = v or ""
    if "\t{'t':" in v:
        v = v.split("\t", 1)[0]
    if v.endswith("'"):
        v = v[:-1]
        if v.endswith("\\"):
            v = v[:-1]
    return v.replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "'")


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_tsv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
