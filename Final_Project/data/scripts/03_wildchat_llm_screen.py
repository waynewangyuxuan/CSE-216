#!/usr/bin/env python
"""Optional LLM second pass on WildChat. UNVERIFIED BY A HUMAN. Not deterministic, so results are cached.

Default run: reads the cache and summarizes it, and calls no model.
--call: fills missing cache entries by calling the Claude Code CLI with tools off.
Sets screened:
 draw2000   every record of the 2,000 draw, any language, to compare with the reported 42 + 40
 clear_mt   seeded 300 of rule-tier clear conversations with >=2 user turns
 possible_mt seeded 100 of rule-tier possible conversations with >=2 user turns
Excerpts: first 3 user turns, 600 characters each, emails and phone-like numbers masked.
"""
import collections, concurrent.futures, csv, glob, json, os, re, subprocess, sys, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = "claude-sonnet-5-5"
BATCH = 25
CACHE = os.path.join(common.DATA, "wildchat_llm_screen.jsonl")
LABELS = {"CLEAR_RESEARCH_WRITING", "POSSIBLE_RESEARCH_WRITING", "ACADEMIC_NOT_RESEARCH", "OTHER_WRITING", "NOT_WRITING", "UNKNOWN"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])")


def targets():
    with open(os.path.join(common.DATA, "wildchat_draw2000_log.tsv"), encoding="utf-8") as f:
        draw = list(csv.DictReader(f, delimiter="\t"))
    inc = common.read_jsonl(os.path.join(common.WORK, "wildchat_included.jsonl"))
    out = {r["conversation_hash"]: {"shard": r["shard"], "row": int(r["row"]), "sets": ["draw2000"]} for r in draw}
    for tier, n, tag in (("clear", 300, "clear_mt"), ("possible", 100, "possible_mt")):
        pool = sorted((h for h in inc if h["tier"] == tier and h["user_turns"] >= 2), key=lambda h: common.stable_key(tag, h["hash"]))
        for h in pool[:n]:
            out.setdefault(h["hash"], {"shard": h["shard"], "row": h["row"], "sets": []})["sets"].append(tag)
    return out


def load_excerpts(tg):
    by_shard = collections.defaultdict(dict)
    for h, t in tg.items():
        by_shard[t["shard"]][t["row"]] = h
    ex = {}
    for shard, rows in sorted(by_shard.items()):
        pf = pq.ParquetFile(os.path.join(common.RAW, "wildchat", shard))
        i = 0
        for batch in pf.iter_batches(batch_size=4096, columns=["conversation_hash", "conversation.list.element.content", "conversation.list.element.role"]):
            for rec in batch.to_pylist():
                if i in rows:
                    assert rec["conversation_hash"] == rows[i]
                    us = [t["content"] or "" for t in rec["conversation"] if t["role"] == "user"][:3]
                    ex[rows[i]] = [PHONE.sub("[masked]", EMAIL.sub("[masked]", u))[:600] for u in us]
                i += 1
    return ex


def call(batch, system, ver):
    body = "\n".join(f'<conv id="{h}">\n' + "\n---\n".join(us) + "\n</conv>" for h, us in batch)
    p = subprocess.run(["claude", "-p", "--model", MODEL, "--tools", "", "--system-prompt", system,
                        "--output-format", "json", "--no-session-persistence"],
                       input=body, capture_output=True, text=True, timeout=300, cwd=HERE)
    res = json.loads(p.stdout)
    got = {}
    for line in res.get("result", "").splitlines():
        line = line.strip().strip("`")
        if not line.startswith("{"):
            continue
        o = json.loads(line)
        if o.get("id") in {h for h, _ in batch} and o.get("label") in LABELS:
            got[o["id"]] = o["label"]
    return got, res.get("total_cost_usd", 0), sorted(res.get("modelUsage") or [])


def main():
    tg = targets()
    cache = {r["hash"]: r for r in common.read_jsonl(CACHE)} if os.path.exists(CACHE) else {}
    if "--call" in sys.argv:
        system = open(os.path.join(HERE, "wildchat_llm_prompt.txt"), encoding="utf-8").read()
        ver = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
        todo = sorted(h for h in tg if h not in cache)
        ex = load_excerpts({h: tg[h] for h in todo})
        items = [(h, ex[h]) for h in todo if ex.get(h)]
        batches = [items[i:i + BATCH] for i in range(0, len(items), BATCH)]
        lock, cost = threading.Lock(), [0.0]
        def work(b):
            try:
                got, c, served = call(b, system, ver)
            except Exception as e:
                print("batch failed", repr(e)[:200], flush=True)
                return
            with lock:
                cost[0] += c or 0
                for h, label in got.items():
                    cache[h] = {"hash": h, "label": label, "model": MODEL, "served": served, "cli": ver, "batch_size": BATCH}
                print(len(cache), "cached, cost so far", round(cost[0], 3), flush=True)
        with concurrent.futures.ThreadPoolExecutor(6) as ex_pool:
            list(ex_pool.map(work, batches))
        common.write_jsonl(CACHE, [cache[h] for h in sorted(cache)])
        print("total cost usd this run", round(cost[0], 3))
    elif len([h for h in tg if h not in cache]) > 1:
        sys.exit("LLM cache missing or partial: wildchat_llm_screen.jsonl must be kept to rebuild outputs. Rerun with --call to refill it (results will differ).")
    summary = {}
    for tag in ("draw2000", "clear_mt", "possible_mt"):  # sets as defined in the docstring
        hs = [h for h, t in tg.items() if tag in t["sets"]]
        c = collections.Counter(cache[h]["label"] if h in cache else "NOT_SCREENED" for h in hs)
        summary[tag] = {"n": len(hs), "labels": dict(sorted(c.items()))}
    with open(os.path.join(common.DATA, "wildchat_draw2000_log.tsv"), encoding="utf-8") as f:
        draw = list(csv.DictReader(f, delimiter="\t"))
    cross = collections.Counter()
    for r in draw:
        label = cache[r["conversation_hash"]]["label"] if r["conversation_hash"] in cache else "NOT_SCREENED"
        cross[label + " | rule=" + (r["tier"] if r["decision"] != "exclude" else r["exclude_reason"])] += 1
    summary["draw2000_llm_by_rule"] = dict(sorted(cross.items()))
    summary["draw2000_not_screened_hashes"] = sorted(r["conversation_hash"] for r in draw if r["conversation_hash"] not in cache)
    meta = {"model": MODEL, "batch_size": BATCH, "prompt_file": "scripts/wildchat_llm_prompt.txt",
            "excerpt": "first 3 user turns, 600 chars each, emails/phones masked",
            "settings": "claude -p, tools off, no session persistence; temperature and seed not settable through this CLI",
            "cli": sorted({r.get("cli") for r in cache.values()}), "human_verified": False}
    json.dump({"meta": meta, "summary": summary}, open(os.path.join(common.WORK, "wildchat_llm_stats.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
