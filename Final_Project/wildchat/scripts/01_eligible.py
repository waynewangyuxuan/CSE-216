#!/usr/bin/env python
"""Mechanical eligibility over every WildChat-1M record (DEFINITION.md, mechanical requirements). No model.
Funnel, first reason wins: toxic -> non_english -> fewer than 2 non-blank user turns -> no user turn followed by a
non-empty AI turn -> duplicate hash -> duplicate normalized first user turn. Records already used in Bet 4 or the
codebook pilot stay eligible but are flagged `used`, so they are kept out of selection and re-judged apart.
Writes blind/eligible.jsonl (locations), blind/embed_text.jsonl (masked user text for embedding), results/funnel_eligible.json."""
import collections, glob, hashlib, json, multiprocessing, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7
import pyarrow.parquet as pq

EMBED_CHARS = 2000


def used_sessions():
    """12-char session ids of WildChat conversations seen by Bet 4 (sample, gold) or the codebook pilot views."""
    ids = set()
    for p in [os.path.join(w7.DATA, "sample.csv"), os.path.join(w7.DATA, "gold.csv")] + glob.glob(os.path.join(w7.FP, "codebook", "pilot", "r*", "view.jsonl")):
        ids |= set(re.findall(r"WILDCHAT-([0-9a-f]{12})-t", open(p, encoding="utf-8").read()))
    return ids


def scan(path):
    name = os.path.basename(path)
    pf, row, out, c = pq.ParquetFile(path), 0, [], collections.Counter()
    for b in pf.iter_batches(batch_size=4096, columns=w7.COLS):
        for rec in b.to_pylist():
            r, row = row, row + 1
            c["records"] += 1
            turns = [(t["role"], t["content"] or "") for t in rec["conversation"]]
            users = [t for ro, t in turns if ro == "user"]
            if rec["toxic"]:
                c["toxic"] += 1
                continue
            if rec["language"] != "English":
                c["non_english"] += 1
                continue
            if sum(1 for u in users if u.strip()) < 2:
                c["under_2_user_turns"] += 1
                continue
            if not any(turns[i][0] == "user" and turns[i][1].strip() and turns[i + 1][0] == "assistant" and turns[i + 1][1].strip() for i in range(len(turns) - 1)):
                c["no_pair"] += 1
                continue
            first = next(u for u in users if u.strip())
            out.append({"hash": rec["conversation_hash"], "shard": name, "row": r, "user_turns": len(users),
                        "cluster": "ip" + hashlib.sha256(("cluster|" + (rec["hashed_ip"] or rec["conversation_hash"])).encode()).hexdigest()[:10],
                        "first_key": w7.key("first", " ".join(first.lower().split())),
                        "pii": bool(any(w7.EMAIL.search(u) or w7.PHONE.search(u) for u in users)),
                        "text": w7.mask(" || ".join(u.strip() for u in users if u.strip()))[:EMBED_CHARS]})
    return name, c, out


def main():
    with multiprocessing.get_context("spawn").Pool(8) as pool:
        res = sorted(pool.map(scan, w7.shards(), chunksize=1), key=lambda x: x[0])
    total, seen_h, seen_f, keep = collections.Counter(), set(), set(), []
    for _, c, out in res:
        total.update(c)
        for o in out:
            if o["hash"] in seen_h:
                total["duplicate_hash"] += 1
                continue
            seen_h.add(o["hash"])
            if o["first_key"] in seen_f:
                total["duplicate_first_turn"] += 1
                continue
            seen_f.add(o["first_key"])
            keep.append(o)
    used = used_sessions()
    for o in keep:
        o["used"] = o["hash"][:12] in used
    w7.write_jsonl(os.path.join(w7.BLIND, "embed_text.jsonl"), [{"hash": o["hash"], "text": o["text"]} for o in keep])
    w7.write_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"), [{k: v for k, v in o.items() if k != "text"} for o in keep])
    funnel = {"records": total["records"], "toxic": total["toxic"], "non_english": total["non_english"],
              "under_2_user_turns": total["under_2_user_turns"], "no_pair": total["no_pair"],
              "duplicate_hash": total["duplicate_hash"], "duplicate_first_turn": total["duplicate_first_turn"],
              "eligible": len(keep), "eligible_with_contact_pattern_masked": sum(o["pii"] for o in keep),
              "eligible_used_before": sum(o["used"] for o in keep), "used_session_ids_found": len(used),
              "used_session_ids_matched": len({o["hash"][:12] for o in keep if o["used"]})}
    os.makedirs(w7.OUT, exist_ok=True)
    json.dump(funnel, open(os.path.join(w7.OUT, "funnel_eligible.json"), "w"), indent=1)
    print(json.dumps(funnel, indent=1))


if __name__ == "__main__":
    main()
