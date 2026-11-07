#!/usr/bin/env python
"""Build windows.jsonl, sample.csv, gold.csv and counts.json from the earlier steps. Fixed seed.

WildChat windows: built for conversations that pass the rule screen AND have a cached LLM label
of CLEAR or POSSIBLE. Eligible for the sample: LLM CLEAR, >=2 non-CX windows; WildChat runs start at the conversation opening. None verified by a human.
Coverage: C1 the next user turn exists and is not blank, C0 otherwise, CX blank request or response.
WildChat never reaches C2.

Sample: 70 NIRVANA + 30 WildChat. Each session gives one contiguous run of up to 3 windows, so
within-session transitions exist while no student dominates. Single-window sessions are skipped,
and a run never skips a turn. Up to 2 NIRVANA runs are reserved to end on a C0 window, so the
sample is not an estimate of the full distribution.
Gold: 20 from the sample, split in proportion to dataset and coverage (min 1 per present stratum),
at most one window per participant, skipping requests of <=2 words.
gold.csv holds the request, response, cleaned action text and required coverage code: no screen tiers, LLM labels, linkage flag
or interpretation.
"""
import collections, csv, hashlib, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import pyarrow.parquet as pq

csv.field_size_limit(10 ** 9)
RUN = 3
N_NIRVANA, N_WILD, N_GOLD = 70, 30, 20


def wildchat_windows():
    llm = {r["hash"]: r for r in common.read_jsonl(os.path.join(common.DATA, "wildchat_llm_screen.jsonl"))}
    inc = [h for h in common.read_jsonl(os.path.join(common.WORK, "wildchat_included.jsonl"))
           if llm.get(h["hash"], {}).get("label") in ("CLEAR_RESEARCH_WRITING", "POSSIBLE_RESEARCH_WRITING")]
    by_shard = collections.defaultdict(dict)
    for h in inc:
        by_shard[h["shard"]][h["row"]] = h
    out = []
    for shard in sorted(by_shard):
        pf, row = pq.ParquetFile(os.path.join(common.RAW, "wildchat", shard)), 0
        for batch in pf.iter_batches(batch_size=4096, columns=["conversation_hash", "hashed_ip", "conversation.list.element.content", "conversation.list.element.role"]):
            for rec in batch.to_pylist():
                if row in by_shard[shard]:
                    h = by_shard[shard][row]
                    assert rec["conversation_hash"] == h["hash"]
                    cluster = "ip" + hashlib.sha256(("cluster|" + (rec["hashed_ip"] or h["hash"])).encode()).hexdigest()[:10]
                    turns = rec["conversation"]
                    upos = [i for i, t in enumerate(turns) if t["role"] == "user"]
                    sid = h["hash"][:12]
                    for n, i in enumerate(upos, start=1):
                        req = turns[i]["content"] or ""
                        has_resp = i + 1 < len(turns) and turns[i + 1]["role"] == "assistant"
                        resp = (turns[i + 1]["content"] or "") if has_resp else ""
                        nxt = (turns[upos[n]]["content"] or "") if n < len(upos) else None
                        reasons = [r for r, bad in (("blank_request", not req.strip()), ("blank_response", not resp.strip())) if bad]
                        cov = "CX" if reasons else ("C1" if nxt is not None and nxt.strip() else "C0")
                        out.append({
                            "window_id": f"WILDCHAT-{sid}-t{n:02d}", "dataset": "WildChat", "session_id": sid,
                            "participant_id": cluster, "domain": None, "episode_id": None, "turn_order": n,
                            "previous_window_id": f"WILDCHAT-{sid}-t{n - 1:02d}" if n > 1 else None,
                            "coverage": cov, "cx_reasons": reasons, "linkage": None, "request": req, "response": resp,
                            "next_user_request_follows": nxt is not None, "next_request": nxt, "next_actions": [], "ops_during_wait": [],
                            "very_short_request": len(req.split()) <= 2,
                            "screen": {"rule_tier": h["tier"], "rule_terms": h["terms"], "llm_label": llm[h["hash"]]["label"],
                                       "llm_model": llm[h["hash"]]["model"], "human_verified": False},
                            "trace": {"file": f"raw/wildchat/{shard}", "row": row, "conversation_hash": h["hash"],
                                      "request_turn_index": i, "response_turn_index": i + 1 if has_resp else None},
                        })
                row += 1
    return out


def choose_runs(sessions, quota, reserve=None):
    """sessions: {sid: [windows in order]}. One run per session and per participant until quota."""
    picked, used_part = [], set()
    order = sorted(sessions, key=lambda s: common.stable_key("order", s))
    if reserve:
        order = reserve + [s for s in order if s not in reserve]
    for sid in order:
        if len(picked) >= quota:
            break
        ws = sessions[sid]
        if ws[0]["participant_id"] in used_part:
            continue
        k = min(RUN, len(ws), quota - len(picked))
        if quota - len(picked) - k == 1 and k > 2:
            k -= 1  # never leave a remainder of one, which could not form a run
        if k < 2:
            continue
        if sid in (reserve or []):
            start = len(ws) - k
        elif ws[0]["dataset"] == "WildChat":
            start = 0  # conversation opening holds the screened goal more often than a later turn
        else:
            start = int(common.stable_key("start", sid), 16) % (len(ws) - k + 1)
        run = [ws[start]]
        for w in ws[start + 1:start + k]:
            if w["turn_order"] != run[-1]["turn_order"] + 1:
                break
            run.append(w)
        if len(run) < 2:
            continue
        picked.extend((w, sid) for w in run)
        used_part.add(ws[0]["participant_id"])
    return picked


def quotas(strata, total):
    """Largest remainder with a minimum of 1 per present stratum."""
    size = sum(strata.values())
    q = {k: max(1, int(v * total / size)) for k, v in strata.items()}
    rema = sorted(strata, key=lambda k: (-(strata[k] * total / size - int(strata[k] * total / size)), k))
    i = 0
    while sum(q.values()) < total:
        q[rema[i % len(rema)]] += 1
        i += 1
    while sum(q.values()) > total:
        big = max(q, key=lambda k: (q[k], k))
        q[big] -= 1
    return q


def actions_text(w):
    """Readable transcript of the trace: adjacent typing/deleting merged, log artifacts cleaned. windows.jsonl stays raw."""
    if w["dataset"] == "WildChat":
        return "NEXT USER TURN: " + w["next_request"] if w["next_request"] is not None else "(no later turn)"
    lines, buf = [], None
    t0, last_copy, repeats = w["response_time"], None, []
    for op in w["next_actions"]:
        kind = op["op_type"]
        if kind in ("i", "d") and op["op_loc"] == "editor":
            last_copy = None
            if buf and buf[0] == kind:
                buf[2] += common.clean_log_text(op["add"] if kind == "i" else op["delete"])
            else:
                if buf:
                    lines.append(f'{buf[1]:.0f}s after response, editor {"typed" if buf[0] == "i" else "deleted"}: {buf[2]}')
                buf = [kind, op["time"] - t0, common.clean_log_text(op["add"] if kind == "i" else op["delete"])]
            continue
        if buf:
            lines.append(f'{buf[1]:.0f}s after response, editor {"typed" if buf[0] == "i" else "deleted"}: {buf[2]}')
            buf = None
        if kind in ("o", "l"):
            continue
        cl = common.clean_log_text
        detail = {"p": f'pasted: {cl(op["add"]) or cl(op["selected_text"])}', "y": f'copied: {op["selected_text"]}', "x": f'cut: {cl(op["delete"])}',
                  "z": "undo", "r": "dragged text", "d_i": f'replaced "{cl(op["delete"])}" with "{cl(op["add"])}"'}.get(kind, kind)
        if kind == "y" and last_copy == op["selected_text"]:
            repeats[-1] += 1  # repeated identical copy events would swamp the cell
            lines[-1] = re.sub(r" copied(?: x\d+)?:", f" copied x{repeats[-1]}:", lines[-1], count=1)
            continue
        last_copy = op["selected_text"] if kind == "y" else None
        repeats.append(1)
        lines.append(f'{op["time"] - t0:.0f}s after response, {op["op_loc"]} {detail}')
    if buf:
        lines.append(f'{buf[1]:.0f}s after response, editor {"typed" if buf[0] == "i" else "deleted"}: {buf[2]}')
    if w.get("next_request") is not None:
        lines.append("NEXT REQUEST TO AI: " + w["next_request"])
    # Ops whose log cell holds no text would otherwise read as lost data.
    lines = [x for x in lines if not re.search(r"editor (typed|deleted): $", x)]
    return "\n".join(lines) if lines else "(no later action recorded)"


def safe(v):
    # Stop spreadsheet apps from evaluating dataset text as formulas when these CSVs are opened.
    v = "" if v is None else str(v)
    return "'" + v if v[:1] in ("=", "+", "-", "@") else v


def main():
    nir = common.read_jsonl(os.path.join(common.WORK, "nirvana_windows.jsonl"))
    for i, w in enumerate(nir):
        same = i + 1 < len(nir) and nir[i + 1]["session_id"] == w["session_id"]
        w["next_request"] = nir[i + 1]["request"] if same else None
    wild = wildchat_windows()
    windows = sorted(nir + wild, key=lambda w: (w["dataset"], w["window_id"]))
    common.write_jsonl(os.path.join(common.DATA, "windows.jsonl"), windows)

    def sessions_of(ws, cond=lambda w: True):
        d = collections.defaultdict(list)
        for w in ws:
            if w["coverage"] != "CX" and cond(w):
                d[w["session_id"]].append(w)
        for v in d.values():
            v.sort(key=lambda w: w["turn_order"])
        return {k: v for k, v in d.items() if len(v) >= 2}

    ns = sessions_of(nir)
    c0 = sorted((s for s, v in ns.items() if v[-1]["coverage"] == "C0"), key=lambda s: common.stable_key("c0", s))[:2]
    picked = choose_runs(ns, N_NIRVANA, reserve=c0)
    ws = sessions_of(wild, lambda w: w["screen"]["llm_label"] == "CLEAR_RESEARCH_WRITING")
    picked += choose_runs(ws, N_WILD)

    sample = [w for w, _ in picked]
    sample.sort(key=lambda w: (w["dataset"], w["window_id"]))
    H = ["window_id", "dataset", "session_id", "participant_id", "turn_order", "previous_window_id", "coverage", "request", "response", "next_actions_text"]
    def row(w, cols):
        vals = {"next_actions_text": actions_text(w), **w}
        return [safe(vals.get(c)) for c in cols]
    with open(os.path.join(common.DATA, "sample.csv"), "w", encoding="utf-8", newline="") as f:
        out = csv.writer(f, lineterminator="\n")
        out.writerow(H)
        out.writerows(row(w, H) for w in sample)

    gold, plan = [], {}
    for ds, n in quotas(collections.Counter(w["dataset"] for w in sample), N_GOLD).items():
        pool = [w for w in sample if w["dataset"] == ds and not w["very_short_request"]]
        q = quotas(collections.Counter(w["coverage"] for w in pool), n)
        plan[ds] = q
        used = set()
        for cov in sorted(q):
            cand = sorted((w for w in pool if w["coverage"] == cov), key=lambda w: common.stable_key("gold", w["window_id"]))
            for w in cand:
                if sum(1 for g in gold if g["dataset"] == ds and g["coverage"] == cov) >= q[cov]:
                    break
                if w["participant_id"] in used:
                    continue
                gold.append(w)
                used.add(w["participant_id"])
    gold.sort(key=lambda w: common.stable_key("gold-order", w["window_id"]))
    G = ["gold_order", "window_id", "dataset", "coverage", "request", "response", "next_actions_text"]
    with open(os.path.join(common.DATA, "gold.csv"), "w", encoding="utf-8", newline="") as f:
        out = csv.writer(f, lineterminator="\n")
        out.writerow(G)
        for i, w in enumerate(gold, 1):
            out.writerow([i] + row(w, G[1:]))

    def describe(ws):
        c = collections.Counter((w["dataset"], w["coverage"]) for w in ws)
        return {"windows": len(ws), "by_dataset_coverage": {f"{a}/{b}": v for (a, b), v in sorted(c.items())},
                "sessions": dict(sorted(collections.Counter(w["dataset"] for w in {w["session_id"]: w for w in ws}.values()).items())),
                "participants": dict(sorted(collections.Counter(w["dataset"] for w in {w["participant_id"]: w for w in ws}.values()).items()))}
    counts = {"windows_all": describe(windows), "sample": describe(sample), "gold": describe(gold), "gold_plan": plan}
    usable = [w for w in wild if w["coverage"] != "CX"]
    pii = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+|(?<![\w.])\+?\d[\d ()-]{8,}\d(?![\w.])")
    counts["contact_pattern_hits"] = {"sample": sorted(w["window_id"] for w in sample if pii.search(w["request"] + "\n" + w["response"] + "\n" + actions_text(w))),
                                      "gold": sorted(w["window_id"] for w in gold if pii.search(w["request"] + "\n" + w["response"] + "\n" + actions_text(w)))}
    counts["contact_pattern_hits"]["windows_jsonl_wildchat"] = sum(1 for w in wild if pii.search(w["request"] + "\n" + w["response"]))
    counts["response_without_terminal_punctuation"] = {
        ds: [sum(1 for w in ws_ if w["coverage"] != "CX" and not re.search(r"[.!?:)\"'\]`*]\s*$", w["response"])), sum(1 for w in ws_ if w["coverage"] != "CX")]
        for ds, ws_ in (("NIRVANA", nir), ("WildChat", wild))}
    def wilson(x, n, z=1.96):
        p, d = x / n, 1 + z * z / n
        c, h = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
        return [round(100 * p, 2), round(100 * (c - h), 2), round(100 * (c + h), 2)]
    with open(os.path.join(common.DATA, "wildchat_draw2000_log.tsv"), encoding="utf-8") as f:
        draw = list(csv.DictReader(f, delimiter="\t"))
    llm = {r["hash"]: r["label"] for r in common.read_jsonl(os.path.join(common.DATA, "wildchat_llm_screen.jsonl"))}
    screened = [r for r in draw if r["conversation_hash"] in llm]
    english = [r for r in screened if r["exclude_reason"] != "non_english"]
    def tally(rows, label):
        return sum(llm[r["conversation_hash"]] == label for r in rows)
    counts["draw_rates_percent_with_wilson95"] = {"clear_all": wilson(tally(screened, "CLEAR_RESEARCH_WRITING"), len(screened)),
                                                  "clear_english": wilson(tally(english, "CLEAR_RESEARCH_WRITING"), len(english))}
    counts["draw_english"] = {"screened": len(english), "clear": tally(english, "CLEAR_RESEARCH_WRITING"), "possible": tally(english, "POSSIBLE_RESEARCH_WRITING")}
    counts["wildchat_max_windows"] = {"per_conversation": max(collections.Counter(w["session_id"] for w in usable).values()),
                                      "per_ip_cluster": max(collections.Counter(w["participant_id"] for w in usable).values())}
    counts["wildchat_windows_llm_clear"] = sum(1 for w in usable if w["screen"]["llm_label"] == "CLEAR_RESEARCH_WRITING")
    counts["wildchat_windows_llm_possible"] = sum(1 for w in usable if w["screen"]["llm_label"] == "POSSIBLE_RESEARCH_WRITING")
    for n in ("nirvana_stats", "wildchat_screen_stats", "wildchat_llm_stats", "scholawrite_stats"):
        counts[n] = json.load(open(os.path.join(common.WORK, n + ".json")))
    bad = set(counts["nirvana_stats"]["windows_touching_malformed_rows"])
    counts["malformed_windows_in_sample"] = sorted(w["window_id"] for w in sample if w["window_id"] in bad)
    counts["malformed_windows_in_gold"] = sorted(w["window_id"] for w in gold if w["window_id"] in bad)
    json.dump(counts, open(os.path.join(common.DATA, "counts.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: counts[k] for k in ("windows_all", "sample", "gold", "gold_plan", "wildchat_windows_llm_clear", "wildchat_windows_llm_possible")}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
