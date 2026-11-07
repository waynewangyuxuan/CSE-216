#!/usr/bin/env python3
"""Audit what each Bet 4 subagent opened, from its session transcript, by path only. Writes results/access_audit.json; prints no window text.
Reads Claude Code transcripts in ~/.claude/projects/...; they are local and not in git, so the committed JSON is the record.
Usage: audit_access.py <subagents_dir>
Finds for coders: files read or searched, any other coder's path, Fable or pilot or data paths, whether each listed view was read to its end marker, and the model served."""
import collections, glob, json, os, re, sys
import bet4
from bet4 import BLIND, OUT

FORBID = {"gold_agent": r"gold_agent|fable", "pilot": r"codebook/pilot|pilot_results|coder_briefs|coder_final", "data": r"Final_Project/data/(?!raw/_venv)|sample\.csv|gold\.csv|windows\.jsonl",
          "other_outputs": r"(?<!tool-)results/|labels_ab|final_labels|agreement|REPORT|decisions\.tsv|c3_gold|\.wayne"}


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


def audit(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    first = next(r for r in rows if r.get("type") == "user")
    prompt = texts(first["message"]["content"])[0]
    meta = json.load(open(path.replace(".jsonl", ".meta.json")))
    m = re.search(r"blind/coder_([ab])/batch_(\d)\.jsonl", prompt)
    adj = "adjudicator_brief" in prompt
    who = {"role": f"coder_{m.group(1)}", "batch": int(m.group(2))} if m else {"role": "adjudicator" if adj else meta.get("description", "other"), "batch": None}
    uses, served = [], collections.Counter()
    ended = set()
    seen = []
    for r in rows:
        msg = r.get("message") or {}
        if r.get("type") == "assistant":
            served[msg.get("model")] += 1
            for x in msg.get("content") or []:
                if isinstance(x, dict) and x.get("type") == "tool_use":
                    uses.append((x["name"], json.dumps(x["input"])))
        if r.get("type") == "user":
            for t in texts(msg.get("content")):
                seen.append(t)
                ended |= set(re.findall(r"=== END OF WINDOW (\S+) ===", t))
    paths = collections.Counter()
    violations = []
    other = "b" if m and m.group(1) == "a" else "a"
    for name, inp in uses:
        if name in ("Read",):
            paths[json.loads(inp).get("file_path", "?").replace("/Users/wang/CSE-216/", "")] += 1
        if name == "Agent":
            violations.append("spawned agent")
        target = inp
        if name == "Write":  # file content is the agent's own output, so test only the path
            target = json.loads(inp).get("file_path", "")
        if adj and name == "Read":  # reading a persisted tool result of its own is fine
            target = target.replace("tool-results", "")
        if name == "Bash":  # same for heredocs that write labels
            target = json.loads(inp).get("command", "").split("<<")[0]
        if m and re.search(rf"coder_{other}/|coder_{other}\b(?!rief)", target):
            violations.append(f"{name}: other coder path")
        if adj and re.search(r"coder_[ab]/|results/labels", target):
            violations.append(f"{name}: coder files")
        if m or adj:
            for k, pat in FORBID.items():
                if re.search(pat, target):
                    violations.append(f"{name}: {k}")
    alltool = " ".join(json.loads(i).get("command", "").split("<<")[0] if n == "Bash" else (json.loads(i).get("file_path", "") + " " + json.loads(i).get("path", "") + " " + json.loads(i).get("pattern", "")) for n, i in uses)
    transcript_text = " ".join(seen)
    tr = sorted(set(re.findall(r"tool-results/[\w.-]+", " ".join(p for p in paths if "tool-results" in p))))
    res = {"file": os.path.basename(path), "scratch_files_touched": sorted(set(re.findall(r"scratchpad/([\w.-]+)", alltool))), "search_or_list_tools": dict(collections.Counter(n for n, _ in uses if n in ("Glob", "Grep"))),
           "dirs_listed": sorted(set(re.findall(r"\b(?:ls|find)\b[^;&|]*", alltool))), "tool_results_read": len(tr), "tool_results_not_own": sum(t.split("/")[1] not in transcript_text for t in tr), **who, "model_requested": meta.get("model"), "model_served": dict(served), "tool_uses": dict(collections.Counter(n for n, _ in uses)), "violations": dict(collections.Counter(violations)),
           "n_views_read": sum(p.startswith("Final_Project/coding/blind/views/") for p in paths), "other_reads": sorted(p for p in paths if not p.startswith("Final_Project/coding/blind/views/"))}
    if m:
        want = open(os.path.join(BLIND, "lists", f"batch_{who['batch']}.txt")).read().split()
        res["views_missing_end_marker"] = sorted(set(want) - ended)
        lines_seen = set()
        for t in seen:
            for l in t.split("\n"):
                lines_seen.add(re.sub(r"^\s*\d+\t", "", l).strip())  # Read prefixes line numbers
        cov = {}
        for i in want:
            ls = [l.strip() for l in open(os.path.join(BLIND, "views", i + ".txt"), encoding="utf-8") if l.strip()]
            cov[i] = round(sum(l in lines_seen for l in ls) / len(ls), 4)
        res["view_line_coverage_min"] = min(cov.values())
        res["views_under_full_line_coverage"] = {k: v for k, v in sorted(cov.items()) if v < 1}
        res["bash_commands"] = sorted({re.sub(r"\s+", " ", json.loads(i).get("command", ""))[:160] for n, i in uses if n == "Bash"})
    return res


def main():
    d = sys.argv[1]
    out = [audit(p) for p in sorted(glob.glob(os.path.join(d, "*.jsonl")))]
    out.sort(key=lambda r: (r["role"], r["batch"] if r["batch"] is not None else -1))
    for r in out:
        r["file"] = r["file"][:12] + "..."  # the id itself is of no use outside this machine
    keep = [r for r in out if r["role"].startswith("coder_") or r["role"] == "adjudicator"]
    with open(os.path.join(OUT, "access_audit.json"), "w") as f:
        json.dump(keep, f, indent=1, sort_keys=True)
    for r in keep:
        print(r["role"], r["batch"], "req", r["model_requested"], "served", r["model_served"], "views", r["n_views_read"], "viol", r["violations"], "missing_end", len(r.get("views_missing_end_marker", [])), "scratch", r["scratch_files_touched"], "ls", r["dirs_listed"], "glob", r["search_or_list_tools"], "tr_not_own", r["tool_results_not_own"], "min_line_cov", r.get("view_line_coverage_min"), "under", r.get("views_under_full_line_coverage"))


if __name__ == "__main__":
    main()
