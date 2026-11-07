#!/usr/bin/env python
"""Deterministic rule screen of WildChat-1M for research-writing conversations. No LLM here.

Criteria, written before the first scan and not changed after it (USER turns only, first match
wins, in this order). The funnel counts records; a conversation_hash can repeat across records:
 E1 non_english      conversation language field is not English
 E2 no_pair          no user turn followed by a non-empty assistant turn
 For each user turn, a HIT needs a topic term and a writing verb within 120 characters, and the
 turn must not match NEGATIVE (fiction, media, marketing, job documents, code).
 STRONG terms name a scholarly artifact -> tier clear. WEAK terms only suggest one -> tier possible.
 A conversation takes the best tier of any clean turn.
 E3 no_rule_hit      no topic term + verb pair in any turn
 E4 negative_context pairs exist but every such turn matched NEGATIVE
 E5 pii_regex        an included conversation has an email address or phone-like number in a user
                     turn; dropped so it never reaches sample files
 E6 duplicate_hash   conversation_hash already included (first occurrence kept)
    duplicate_request same normalized first user turn as an earlier included conversation
                     (shard, row order)
Two denominators:
 A every record in the corpus
 B a draw of 2,000 records by lowest sha256(seed|conversation_hash), to compare at the reported
   scale. The reported draw's method was lost, so this is not a replication of it.
Output holds hashes and rule hits, not conversation text.
"""
import collections, glob, heapq, json, multiprocessing, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import pyarrow.parquet as pq

STRONG = re.compile(r"\b(literature review|research (?:paper|article|proposal)|dissertation|thesis(?! statement)|"
                    r"journal (?:article|paper)|academic (?:paper|article)|scientific (?:paper|article)|scholarly (?:paper|article)|"
                    r"conference paper|manuscript|systematic review|peer[- ]review\w*|related work|methodology section|"
                    r"research gap|research questions?)\b", re.I)
WEAK = re.compile(r"\b(research|academic|essay|thesis statement|citations?|references|apa|mla|harvard style|"
                  r"methodology|hypothes[ie]s|abstract|scholarly|bibliography|peer[- ]reviewed)\b", re.I)
VERB = re.compile(r"\b(write|writing|rewrite|re-write|draft|paraphrase|revise|edit|proofread|polish|improve|summari[sz]e|"
                  r"expand|outline|reword|rephrase|shorten|structure|critique|cite|compose|formulate|continue)\b", re.I)
NEGATIVE = re.compile(r"midjourney|prompt generator|fan ?fic|fan fiction|role-?play|\bstory\b|screenplay|youtube|tiktok|"
                      r"blog post|\bseo\b|\bresume\b|cover letter|```|\bdef \w+\(|#include|\bgame\b|\bsql\b|\bpython\b|\bjavascript\b", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])")
WINDOW = 120
COLUMNS = ["conversation_hash", "language", "hashed_ip",
           "conversation.list.element.content", "conversation.list.element.role"]


def pair_near(term_re, text):
    hits = []
    for m in term_re.finditer(text):
        if VERB.search(text, max(0, m.start() - WINDOW), m.end() + WINDOW):
            hits.append(m.group(1).lower())
    return hits


def judge(language, turns):
    """Return (reason, tier, terms, user_turn_count). Reason is None for an included conversation."""
    users = [c for r, c in turns if r == "user"]
    n = len(users)
    if language != "English":
        return "non_english", None, [], n
    if not any(turns[i][0] == "user" and turns[i][1].strip() and turns[i + 1][0] == "assistant" and turns[i + 1][1].strip()
               for i in range(len(turns) - 1)):
        return "no_pair", None, [], n
    best, terms, negative_only = None, [], False
    for text in users:
        s, w = pair_near(STRONG, text), pair_near(WEAK, text)
        if not s and not w:
            continue
        if NEGATIVE.search(text):
            negative_only = True
            continue
        if s:
            best, terms = "clear", sorted(set(terms + s))
        elif best is None:
            best, terms = "possible", sorted(set(terms + w))
        elif best == "possible":
            terms = sorted(set(terms + w))
    if best is None:
        return ("negative_context" if negative_only else "no_rule_hit"), None, [], n
    if any(EMAIL.search(t) or PHONE.search(t) for t in users):
        return "pii_regex", best, terms, n
    return None, best, terms, n


def scan_shard(path):
    pf = pq.ParquetFile(path)
    name = os.path.basename(path)
    counts, hits, draw, rownum, hashes = collections.Counter(), [], [], 0, set()
    for batch in pf.iter_batches(batch_size=4096, columns=COLUMNS):
        for rec in batch.to_pylist():
            row, rownum = rownum, rownum + 1
            turns = [(t["role"], t["content"] or "") for t in rec["conversation"]]
            reason, tier, terms, nuser = judge(rec["language"], turns)
            h = rec["conversation_hash"]
            hashes.add(h)
            first = next((c for r, c in turns if r == "user"), "")
            out = {"hash": h, "shard": name, "row": row, "language_is_english": rec["language"] == "English",
                   "reason": reason, "tier": tier, "terms": terms, "user_turns": nuser,
                   "first_key": common.stable_key(" ".join(first.lower().split()))}
            counts["records"] += 1
            if tier or reason == "pii_regex":
                hits.append(out)
            key = common.stable_key(h)
            item = (key, json.dumps(out, sort_keys=True))
            if len(draw) < 3000:  # margin above 2,000 for duplicate hashes
                heapq.heappush(draw, (_neg(key), item))
            elif _neg(key) > draw[0][0]:
                heapq.heapreplace(draw, (_neg(key), item))
            counts[reason or "included_" + tier] += 1
    return name, counts, hits, [i for _, i in draw], hashes


def _neg(hexkey):
    # heapq is a min-heap; keep smallest keys by storing the complement
    return -int(hexkey, 16)


def main():
    files = sorted(glob.glob(os.path.join(common.RAW, "wildchat", "*.parquet")))
    if len(files) != 14:
        sys.exit(f"expected 14 shards, found {len(files)}")
    with multiprocessing.get_context("spawn").Pool(min(8, os.cpu_count() or 4)) as pool:
        results = pool.map(scan_shard, files, chunksize=1)
    results.sort(key=lambda r: r[0])

    total = collections.Counter()
    seen_hash, seen_first, included, dup_hash = set(), set(), [], 0
    dup_first = collections.Counter()
    for name, counts, hits, _, _ in results:
        total.update(counts)
        for h in hits:
            if h["reason"] == "pii_regex":
                continue
            if h["hash"] in seen_hash:
                dup_hash += 1
                continue
            seen_hash.add(h["hash"])
            if h["first_key"] in seen_first:
                dup_first[h["tier"]] += 1
                continue
            seen_first.add(h["first_key"])
            included.append(h)
    distinct = len(set().union(*(r[4] for r in results)))
    denom_a = {"records": total["records"], "distinct_conversation_hashes": distinct, "non_english": total["non_english"], "no_pair": total["no_pair"],
               "no_rule_hit": total["no_rule_hit"], "negative_context": total["negative_context"],
               "pii_regex": total["pii_regex"],
               "rule_hits_before_dedup": {"clear": total["included_clear"], "possible": total["included_possible"]},
               "duplicate_hash_dropped": dup_hash, "duplicate_first_request_dropped": dict(sorted(dup_first.items())),
               "included_after_dedup": dict(sorted(collections.Counter(h["tier"] for h in included).items())),
               "included_multi_turn": dict(sorted(collections.Counter(h["tier"] for h in included if h["user_turns"] >= 2).items()))}

    # Denominator B
    pool_items = sorted({i for r in results for i in r[3]})
    draw, drawn = [], set()
    for key, raw in pool_items:
        rec = json.loads(raw)
        if rec["hash"] in drawn:
            continue
        drawn.add(rec["hash"])
        draw.append((key, rec))
        if len(draw) == 2000:
            break
    rows = []
    for key, rec in draw:
        decision = rec["tier"] if rec["reason"] is None else "exclude"
        rows.append([key[:16], rec["hash"], rec["shard"], rec["row"], decision, rec["reason"] or "", rec["tier"] or "",
                     ",".join(rec["terms"]), rec["user_turns"]])
    common.write_tsv(os.path.join(common.DATA, "wildchat_draw2000_log.tsv"),
                     ["draw_key", "conversation_hash", "shard", "row", "decision", "exclude_reason", "tier", "rule_terms", "user_turns"], rows)
    denom_b = collections.Counter(r[4] if r[4] != "exclude" else "exclude_" + r[5] for r in rows)
    denom_b["english"] = sum(1 for _, rec in draw if rec["language_is_english"])
    os.makedirs(common.WORK, exist_ok=True)
    common.write_jsonl(os.path.join(common.WORK, "wildchat_included.jsonl"), included)
    stats = {"denominator_A_full_corpus": denom_a, "denominator_B_draw_2000": dict(sorted(denom_b.items())),
             "shards": [r[0] for r in results]}
    json.dump(stats, open(os.path.join(common.WORK, "wildchat_screen_stats.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(stats, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
