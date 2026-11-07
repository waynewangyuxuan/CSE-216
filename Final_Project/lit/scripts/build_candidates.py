#!/usr/bin/env python3
"""Merge a search run into deduplicated candidates for screening. Usage: build_candidates.py <run_label>. Writes screening/candidates.jsonl and screening/batch_NN.txt."""
import glob, json, os, re, sys
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
norm=lambda s:" ".join(re.sub(r"[^a-z0-9]+"," ",(s or "").lower()).split())
merged={}; dropped_auto=[]
for f in sorted(glob.glob(os.path.join(HERE,"raw","search",sys.argv[1],"*_*.json"))):
    if "manifest" in f: continue
    qs=os.path.basename(f)[:-5]
    for r in json.load(open(f)):
        k=norm(r["title"])
        if not k: continue
        # peer-review reports and front matter are not papers
        if re.match(r"(review for|reply to|peer review|decision letter|author response)",k):
            dropped_auto.append(r["title"]); continue
        m=merged.setdefault(k,dict(r,sources=[]))
        m["sources"].append(qs)
        for a in ("doi","arxiv","abstract","venue","openalex"):
            if not m.get(a) and r.get(a): m[a]=r[a]
cands=sorted(merged.values(),key=lambda r:norm(r["title"]))
os.makedirs(os.path.join(HERE,"screening"),exist_ok=True)
with open(os.path.join(HERE,"screening","candidates.jsonl"),"w") as o:
    for i,c in enumerate(cands):
        c["cid"]=f"C{i+1:04d}"; o.write(json.dumps(c,ensure_ascii=False)+"\n")
with open(os.path.join(HERE,"screening","input.txt"),"w") as o:
    for c in cands:
        o.write(f"{c['cid']} | {c['title']} | {c['year']} | {c['venue']}\nABSTRACT: {(c['abstract'] or '[none]')[:500]}\n\n")
print(len(cands),"candidates; dropped non-paper records",len(dropped_auto),"; no abstract",sum(1 for c in cands if not c['abstract']))
