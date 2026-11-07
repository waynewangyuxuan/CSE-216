#!/usr/bin/env python3
"""Audit what each Bet 6 coder and adjudicator did, from its session transcript, by path and order only. Writes results/access_audit.json; prints no window text.
Reads Claude Code transcripts in ~/.claude/projects/...; they are local and not in git, so the committed JSON is the record. Usage: audit_access.py <subagents_dir>
Checks: forbidden paths in any tool call (other coder, inference/, coding/, codebook/ incl. the frozen file with s9, data/, results/, .wayne, gold/Fable, pilot),
Write/Edit on a labels or rulings file, directory listing or search tools, the model served, every line of every assigned part returned to the agent,
and order: a window's label (or ruling) is written before any later part of its session is read."""
import collections, glob, json, os, re, sys
import s6

FORBID = {"inference": r"Final_Project/inference|/inference/", "coding_bet4": r"Final_Project/coding/", "codebook_dir": r"Final_Project/codebook/",
          "data": r"Final_Project/data/(?!raw/_venv)|windows\.jsonl|sample\.csv|gold\.csv", "results": r"sessions/results|labels_ab|final_labels|agreement|REPORT|decisions\.tsv",
          "wayne": r"\.wayne", "gold_fable": r"gold_agent|fable", "pilot": r"pilot", "wildchat": r"Final_Project/wildchat", "lit": r"Final_Project/lit"}
PART = re.compile(r"sessions/blind/parts/(\w+)/(NIRVANA-\w+-t\d+)\.txt")


def texts(c):
    if isinstance(c, str):
        return [c]
    out = []
    for x in c or []:
        if isinstance(x, dict) and x.get("type") == "text":
            out.append(x["text"])
        elif isinstance(x, dict) and x.get("type") == "tool_result":
            out += texts(x.get("content"))
    return out


def audit(path, idx):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    meta = json.load(open(path.replace(".jsonl", ".meta.json")))
    prompt = texts(next(r for r in rows if r.get("type") == "user")["message"]["content"])[0]
    m = re.search(r"Coder ([AB]) for Bet 6, batch (\d+)", prompt)
    a = re.search(r"adjudicator for Bet 6, packet (\w+)\.", prompt)
    if not (m or a):
        return None
    role = f"coder_{m.group(1).lower()}" if m else "adjudicator"
    batch = int(m.group(2)) if m else a.group(1)
    uses, served, seen, result = [], collections.Counter(), [], {}
    for r in rows:
        msg = r.get("message") or {}
        if r.get("type") == "assistant":
            served[msg.get("model")] += 1
            for x in msg.get("content") or []:
                if isinstance(x, dict) and x.get("type") == "tool_use":
                    uses.append((x["name"], x["input"], x["id"]))
        if r.get("type") == "user":
            seen += texts(msg.get("content"))
            for x in msg.get("content") or [] if isinstance(msg.get("content"), list) else []:
                if isinstance(x, dict) and x.get("type") == "tool_result":
                    result[x.get("tool_use_id")] = "\n".join(texts(x.get("content")))
    viol, reads, writes_lab, listing = collections.Counter(), [], [], []
    other = {"coder_a": "coder_b", "coder_b": "coder_a"}.get(role)
    events = []  # (step, kind, window)
    for n, (name, inp, uid) in enumerate(uses):
        if name == "Read":
            target = inp.get("file_path", "")
            reads.append(target.replace("/Users/wang/CSE-216/", ""))
            mm = PART.search(target)
            if mm:
                events.append((n, "read", mm.group(2)))
        elif name == "Bash":
            cmd = inp.get("command", "")
            target = cmd.split("<<")[0]
            if re.search(r"add_label\.py|add_ruling\.py", cmd):
                # a label counts as written only when the gate printed ok for that window (failed calls write nothing)
                for w in re.findall(r"^ok (NIRVANA-\w+-t\d+)", result.get(uid, ""), re.M):
                    events.append((n, "label", w))
            for d in re.findall(r"(?:^|[;&|]\s*|\bcd\s+\S+\s*;\s*)((?:ls|find|tree|grep|rg)\b[^;&|]*)", target):
                listing.append(re.sub(r"\s+", " ", d).strip())
            for mm in PART.finditer(target):
                if re.search(r"\b(cat|head|tail|sed|awk|less|more)\b", target):
                    events.append((n, "read", mm.group(2)))
        elif name in ("Write", "Edit", "NotebookEdit"):
            target = inp.get("file_path", "")
            if re.search(r"coder_[ab]/|adjudication/", target):
                writes_lab.append(target.replace("/Users/wang/CSE-216/", ""))
        else:
            target = json.dumps(inp)
            if name in ("Glob", "Grep"):
                listing.append(name)
            if name == "Agent":
                viol["spawned agent"] += 1
        if other and re.search(rf"{other}\b", target):
            viol[f"{name}: other coder path"] += 1
        if role == "adjudicator" and re.search(r"coder_[ab]/|flips\.json", target):
            viol[f"{name}: coder files or flips"] += 1
        for k, pat in FORBID.items():
            if re.search(pat, target):
                viol[f"{name}: {k}"] += 1
    # order: label of window w must come before the first read of any later part of its session
    labeled, order_bad = {}, []
    for n, kind, w in events:
        if kind == "label" and w not in labeled:
            labeled[w] = n
    first_read = {}
    for n, kind, w in events:
        if kind == "read" and w not in first_read:
            first_read[w] = n
    if role == "adjudicator":
        pk = s6.load_jsonl(os.path.join(s6.BLIND, "adjudication", f"packet_{batch}.jsonl"))
        targets = [l["window_id"] for l in pk]
    else:
        targets = [w for s in json.load(open(os.path.join(s6.BLIND, "batches.json")))[batch] for w in idx["sessions"][s]]
    for w in targets:
        s, k = idx["windows"][w]["session"], idx["windows"][w]["part"]
        later = [first_read[x] for x in idx["sessions"][s][k:] if x in first_read]
        if w not in labeled:
            order_bad.append(f"{w}: no label call seen")
        elif later and min(later) < labeled[w]:
            order_bad.append(f"{w}: later part read before label")
    res = {"role": role, "batch": batch, "model_requested": meta.get("model"), "model_served": {k: v for k, v in served.items() if k and k != "<synthetic>"},
           "tool_uses": dict(collections.Counter(u[0] for u in uses)), "violations": dict(viol), "writes_to_label_files": writes_lab, "listing_or_search": listing,
           "other_reads": sorted(set(r for r in reads if not PART.search(r))), "order_problems": order_bad, "targets": len(targets), "labels_seen": len([w for w in targets if w in labeled])}
    want_parts = [w for w in targets] if role != "adjudicator" else sorted({p for l in pk for p in l["read_first"]})
    lines_seen = set()
    for t in seen:
        for l in t.split("\n"):
            lines_seen.add(re.sub(r"^\s*\d+[\t→]", "", l).strip())
    cov = {}
    for w in want_parts:
        p = w if w.endswith(".txt") else os.path.join(s6.PARTS, idx["windows"][w]["session"], w + ".txt")
        ls = [l.strip() for l in open(p, encoding="utf-8") if l.strip()]
        cov[os.path.basename(p)] = round(sum(l in lines_seen for l in ls) / len(ls), 4)
    res["part_line_coverage_min"] = min(cov.values()) if cov else None
    res["parts_under_full_coverage"] = {k: v for k, v in sorted(cov.items()) if v < 1}
    return res


def main():
    idx = json.load(open(os.path.join(s6.BLIND, "index.json")))
    out = [r for r in (audit(p, idx) for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.jsonl")))) if r]
    out.sort(key=lambda r: (r["role"], str(r["batch"]).zfill(3)))
    redone = {x["window_id"] for p in glob.glob(os.path.join(s6.BLIND, "adjudication", "rerun_*.jsonl")) for x in s6.load_jsonl(p)}
    for r in out:  # decisions.tsv S08: an adjudicator breach is redone by a fresh agent; a coder breach would need a recode
        r["order_problems_redone_S08"] = [o for o in r["order_problems"] if r["role"] == "adjudicator" and o.split(":")[0] in redone]
    json.dump(out, open(os.path.join(s6.OUT, "access_audit.json"), "w"), indent=1, sort_keys=True)
    for r in out:
        print(r["role"], r["batch"], "served", r["model_served"], "viol", r["violations"], "writes", len(r["writes_to_label_files"]), "list", len(r["listing_or_search"]),
              "other_reads", r["other_reads"], "order", len(r["order_problems"]), f"labels {r['labels_seen']}/{r['targets']}", "cov_min", r["part_line_coverage_min"])


if __name__ == "__main__":
    main()
