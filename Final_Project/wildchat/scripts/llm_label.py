#!/usr/bin/env python
"""Cached LLM labels for the Bet 7 screen and its audit. NOT VERIFIED BY A HUMAN. Not deterministic, so every label is cached.
Usage: llm_label.py <role> <ids_file> [--call]
 role screen: model claude-sonnet-5-5, prompt screen_prompt.txt, cache results/screen_labels.jsonl
 role audit:  model claude-opus-5-5,   prompt audit_prompt.txt,  cache results/audit_labels.jsonl (separate calls, never sees screen labels)
ids_file: one conversation hash per line (written by the rank or audit scripts). Without --call, reports what is missing and calls nothing.
Each call is a fresh `claude -p` process: tools off, no session persistence. Excerpts are built by w7.excerpt (whole conversation, caps, contact details masked).
The cache holds hashes, labels and run metadata only, no conversation text."""
import concurrent.futures, json, os, subprocess, sys, threading, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7

ROLES = {"screen": ("claude-sonnet-5-5", "screen_prompt.txt", "screen_labels.jsonl"),
         "audit": ("claude-opus-5-5", "audit_prompt.txt", "audit_labels.jsonl")}
LABELS = {"INCLUDE", "EXCLUDE", "UNSURE"}
BATCH_CHARS = 90000
WORKERS = 6


def cache_path(role):
    return os.path.join(w7.OUT, ROLES[role][2])


def load_cache(role):
    p = cache_path(role)
    return {r["hash"]: r for r in w7.read_jsonl(p)} if os.path.exists(p) else {}


def call(model, system, batch):
    body = "\n".join(f'<conv id="{h}">\n{t}\n</conv>' for h, t in batch)
    p = subprocess.run(["claude", "-p", "--model", model, "--tools", "", "--system-prompt", system, "--output-format", "json", "--no-session-persistence"],
                       input=body, capture_output=True, text=True, timeout=900, cwd=w7.HERE)
    res = json.loads(p.stdout)
    want, got = {h for h, _ in batch}, {}
    for line in (res.get("result") or "").splitlines():
        line = line.strip().strip("`")
        if not line.startswith("{"):
            continue
        try:
            o = json.loads(line)
        except ValueError:
            continue
        if o.get("id") in want and o.get("label") in LABELS:
            got[o["id"]] = o
    return got, res.get("total_cost_usd") or 0, sorted(res.get("modelUsage") or [])


def main():
    role, ids_file = sys.argv[1], sys.argv[2]
    model, prompt, _ = ROLES[role]
    ids = [l.strip() for l in open(ids_file) if l.strip()]
    cache = load_cache(role)
    todo = [h for h in ids if h not in cache]
    print(f"{role}: {len(ids)} ids, {len(ids) - len(todo)} cached, {len(todo)} missing")
    if not todo:
        return
    if "--call" not in sys.argv:
        sys.exit(f"{len(todo)} labels missing from the cache; rerun with --call to fill them (results will differ)")
    system = open(os.path.join(w7.HERE, prompt), encoding="utf-8").read()
    ver = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    loc = {r["hash"]: (r["shard"], r["row"]) for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    extra = os.path.join(w7.BLIND, "extra_locations.json")  # Bet 4 conversations outside the eligible set
    if os.path.exists(extra):
        loc.update({h: tuple(v) for h, v in json.load(open(extra)).items()})
    for attempt in range(3):
        todo = [h for h in ids if h not in cache]
        if not todo:
            break
        conv = w7.load_conversations({h: loc[h] for h in todo})
        items = sorted(((h, w7.excerpt(conv[h])) for h in todo), key=lambda x: w7.key("batch", attempt, x[0]))
        batches, cur, n = [], [], 0
        for it in items:
            if cur and n + len(it[1]) > BATCH_CHARS:
                batches.append(cur)
                cur, n = [], 0
            cur.append(it)
            n += len(it[1])
        if cur:
            batches.append(cur)
        lock, cost = threading.Lock(), [0.0]

        def work(b):
            try:
                got, c, served = call(model, system, b)
            except Exception as e:
                print("batch failed", repr(e)[:200], flush=True)
                return
            with lock:
                cost[0] += c
                for h, o in got.items():
                    cache[h] = {"hash": h, "label": o["label"], "genre": str(o.get("genre", "")), "first_writing_turn": int(o.get("first_writing_turn") or 0),
                                "model": model, "served": served, "cli": ver, "batch_n": len(b), "attempt": attempt}
                w7.write_jsonl(cache_path(role), [cache[h] for h in sorted(cache)])
                print(f"{len(cache)} cached, batch {len(b)} got {len(got)}, cost so far {cost[0]:.2f}", flush=True)
        print(f"attempt {attempt}: {len(todo)} to label in {len(batches)} batches", flush=True)
        with concurrent.futures.ThreadPoolExecutor(WORKERS) as ex:
            list(ex.map(work, batches))
        with open(os.path.join(w7.OUT, "llm_cost_log.tsv"), "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{role}\t{os.path.basename(ids_file)}\tattempt {attempt}\t{cost[0]:.3f}\n")
    print("missing after calls:", len([h for h in ids if h not in cache]))


if __name__ == "__main__":
    main()
