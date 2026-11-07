#!/usr/bin/env python3
"""Report which seed papers appear in a search run. Usage: seed_match.py <run_label>."""
import csv, glob, json, os, re, sys
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
norm=lambda s:" ".join(re.sub(r"[^a-z0-9]+"," ",(s or "").lower()).split())
def is_seed(r,s):
    if s["doi"] and r.get("doi","")==s["doi"]: return True
    if s["arxiv"] and r.get("arxiv")==s["arxiv"]: return True
    t=norm(r.get("title"))
    return t==s["title_key"] or (len(s["title_key"])>20 and t.startswith(s["title_key"]))
if __name__=="__main__":
    seeds=list(csv.DictReader(open(os.path.join(HERE,"scripts","seeds.csv"))))
    hit={s["seed_id"]:[] for s in seeds}
    for f in glob.glob(os.path.join(HERE,"raw","search",sys.argv[1],"*_*.json")):
        q=os.path.basename(f)[:-5]
        for r in json.load(open(f)):
            for s in seeds:
                if is_seed(r,s): hit[s["seed_id"]].append(q)
    for s in seeds: print(s["seed_id"],s["short"],sorted(set(hit[s["seed_id"]])))
