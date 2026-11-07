#!/usr/bin/env python3
"""Coder and adjudicator separation from local transcripts. Prints counts and paths only, writes results/access_audit.json.
For every agent: (1) each path its tool calls touch (Read file_path, Glob/Grep paths, any absolute path or part file in a Bash command),
flagged when outside its allowed set; (2) the served model; (3) for coders, read order: for each coded window N, the highest part number of
the same conversation read before window N's label was first written (lookahead = that minus N; 1 is only the next window, whose request
the window's own next user turn already shows).
Needs the transcripts under ~/.claude, so run_all.sh does not rerun it; the JSON is the record. Usage: audit_access.py"""
import collections, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
W7 = os.path.abspath(os.path.join(HERE, ".."))
TX = os.path.expanduser("~/.claude/projects/-Users-wang-CSE-216/d63d6bd7-deff-4b3e-a8bd-ddad98114572/subagents")
AGENTS = [l.split("\t") for l in open(os.path.join(W7, "results", "agents.tsv")).read().split("\n")[1:] if l]
PART = re.compile(r"views/([0-9a-f]{12})/part_(\d\d)\.txt|part_(\d\d)\.txt")
CD = re.compile(r"views/([0-9a-f]{12})/?")
ABS = re.compile(r"/Users/wang/[^\s'\"<>|;&)]+")
WID = re.compile(r"WILDCHAT-([0-9a-f]{12})-t(\d\d)")


def allowed(role, batch, p):
    ok = ["codebook/CSE216_Research_Writing_Codebook_v1.1.md", "/blind/views/", "/blind/_venv/bin/python", "/scripts/check_labels.py"]
    if role == "adjudicator":
        ok += ["adjudicator_brief.md", "/blind/adjudication/packet_0.jsonl", "/blind/adjudication/ruling_0.jsonl", "/blind/adjudication"]
    else:
        ok += ["coder_brief.md", f"/blind/lists/batch_{batch}.txt", f"/blind/coder_{role[-1].lower()}/batch_{batch}.jsonl", f"/blind/coder_{role[-1].lower()}"]
    if "/.claude/projects/" in p and "/tool-results/" in p:  # the harness's saved copy of the agent's own large tool output
        return True
    return any(o in p for o in ok) or p.rstrip("/") in ("/Users/wang/CSE-216/Final_Project/wildchat/blind",)


def main():
    out = {}
    for aid, role, batch, model in AGENTS:
        events, served, viol, paths = [], set(), [], collections.Counter()
        for l in open(os.path.join(TX, f"agent-{aid}.jsonl")):
            o = json.loads(l)
            m = o.get("message") or {}
            if m.get("model"):
                served.add(m["model"])
            if not isinstance(m.get("content"), list):
                continue
            for c in m["content"]:
                if c.get("type") != "tool_use":
                    continue
                inp = c["input"]
                text = json.dumps(inp)
                ps = set(ABS.findall(text.replace("\\n", " ")))
                if c["name"] in ("Read", "Glob", "Grep"):
                    ps |= {inp.get("file_path") or inp.get("path") or ""}
                for p in ps:
                    if p and not allowed(role, batch, p):
                        viol.append(p)
                    paths[p] += 1
                cmd = inp.get("command", "") if c["name"] == "Bash" else ""
                # A heredoc append runs before whatever follows its terminator line, so split the command there.
                wpart, rpart = "", cmd
                mh = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", cmd)
                if mh:
                    end = re.search(r"\n" + mh.group(1) + r"\s*(\n|$)", cmd[mh.end():])
                    cut = mh.end() + (end.end() if end else len(cmd) - mh.end())
                    wpart, rpart = cmd[:cut], cmd[cut:]
                if c["name"] in ("Write", "Edit"):
                    wpart, rpart = text, ""
                writes = [(s_, int(n)) for s_, n in WID.findall(wpart)]
                # Loop-generated ids such as WILDCHAT-<sid>-t0$n inside "for n in 3 4 5"
                for var, vals in re.findall(r"for (\w+) in ([\d ]+);", cmd):
                    for s_ in re.findall(r"WILDCHAT-([0-9a-f]{12})-t0?\$\{?" + var + r"\}?", cmd):
                        writes += [(s_, int(v)) for v in vals.split()]
                sid_cd = (CD.findall(cmd) or [None])[0]
                reads = []
                if c["name"] == "Read":
                    mm = PART.search(inp.get("file_path", ""))
                    if mm and mm.group(1):
                        reads.append((mm.group(1), int(mm.group(2))))
                for mm in PART.finditer(rpart):
                    sid = mm.group(1) or sid_cd
                    if sid:
                        reads.append((sid, int(mm.group(2) or mm.group(3))))
                for sid, a, b in re.findall(r"views/([0-9a-f]{12})/part_\{?(\d+)\.\.(\d+)\}?", rpart):
                    reads += [(sid, n) for n in range(int(a), int(b) + 1)]
                if re.search(r"part_\*|part_\?\?|\*\.txt", rpart):
                    reads.append(((CD.findall(rpart) or [sid_cd or "?"])[0], 99))
                events.append((writes, reads))
        res = {"role": role, "batch": batch, "requested": model, "served": sorted(served), "disallowed_paths": sorted(set(viol)), "distinct_paths": len(paths)}
        if role.startswith("coder"):
            maxread, first_write = collections.defaultdict(int), {}
            for writes, reads in events:  # writes in a call happen before its reads
                for s, n in writes:
                    first_write.setdefault((s, n), maxread[s])
                for s, n in reads:
                    maxread[s] = max(maxread[s], n)
            look = {f"{s}-t{n:02d}": seen - n for (s, n), seen in first_write.items()}
            res["windows_written"] = len(look)
            res["lookahead_counts"] = dict(sorted(collections.Counter(min(v, 5) if v >= 0 else -1 for v in look.values()).items()))
            res["windows_lookahead_ge2"] = sorted(k for k, v in look.items() if v >= 2)
        out[aid] = res
        print(aid, role, batch, "served", res["served"], "disallowed", len(res["disallowed_paths"]), res.get("lookahead_counts", ""))
    json.dump(out, open(os.path.join(W7, "results", "access_audit.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
