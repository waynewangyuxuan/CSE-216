#!/usr/bin/env python3
"""Build papers.csv and search_log.csv from run manifests, screener files and adjudication. Rerunnable."""
import csv, glob, json, os, re, sys
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(HERE,"scripts"))
from seed_match import is_seed, norm
S=os.path.join(HERE,"screening")
seeds=list(csv.DictReader(open(os.path.join(HERE,"scripts","seeds.csv"))))
def tsv(p):
    d={}
    for l in open(os.path.join(S,p)):
        x=l.rstrip("\n").split("\t")
        if len(x)>=3 and x[0] not in ("cid",) and not x[0].startswith("#"): d[x[0]]=x
    return d
def jl(p): return {json.loads(l)["cid"]:json.loads(l) for l in open(os.path.join(S,p))}
sets=[("frozen",jl("candidates.jsonl"),tsv("screener_A.tsv"),tsv("screener_B.tsv"),tsv("adjudication.tsv")),
      ("amendment",jl("candidates_amend.jsonl"),tsv("screener_A_amend.tsv"),tsv("screener_B_amend.tsv"),tsv("adjudication_amend.tsv"))]
READ=json.load(open(os.path.join(HERE,"scripts","read_levels.json")))
papers=[]; decided={}; stats={}
for name,c,A,B,D in sets:
    st=dict(n=len(c),both_inc=0,both_exc=0,disagree=0,inc=0,core=0)
    for k,r in c.items():
        a,b=A[k],B[k]
        if a[1]==b[1]=="INCLUDE": st["both_inc"]+=1; dec="INCLUDE"; tier="CORE" if a[2]==b[2]=="CORE" else "CONTEXT"; by="both screeners"
        elif a[1]==b[1]: st["both_exc"]+=1; dec="EXCLUDE"; tier=a[2]; by="both screeners"
        else:
            st["disagree"]+=1; d=D[k]; dec=d[1]; tier=d[2]; by="adjudicated ("+d[3]+")"
        decided[norm(r["title"])]=dec
        if dec!="INCLUDE": continue
        st["inc"]+=1; st["core"]+=tier=="CORE"
        sid=[s["seed_id"] for s in seeds if is_seed(r,s)]
        rid=r["doi"] and "doi:"+r["doi"] or (r.get("arxiv") and "arXiv:"+r["arxiv"]) or ""
        papers.append(dict(paper_id=k,title=r["title"],authors=r["authors"],year=r["year"],venue=r["venue"],identifier=rid,run=name,tier=tier,decided_by=by,seed_id=";".join(sid),found_by=";".join(sorted(set(r["sources"]))),read_level=READ.get(k,"title and abstract at screening only"),abstract_available="yes" if r["abstract"] else "no (title only)"))
    stats[name]=st
# seeds not found by the search stay as listed entries
KEEP={"S01":"Recovered, but both screeners excluded it as E2 (no human use data). Keep: Milestone 2 requires this comparison.","S14":"Recovered, but both screeners excluded it as E2 (a model study). Keep: it motivates source-checking codes, though it measures models, not people.","S03":"Missed: before date limit, and a book. Keep: foundational theory the codebook uses.","S04":"Missed: its record does not match the Q11 wording (no randomized or similar terms). Keep: context on idea-level use.",
"S05":"Missed: before date limit. Keep: the codebook's process field rests on it, and Jelson 2026 and Reza 2025 use it.","S13":"Missed: its abstract lacks the LLM terms Q9 requires, so Q9 cannot match it. Keep: closest measure of handed-over planning, execution and verification.",
"S15":"Missed: before date limit. Keep: required comparison framework.","S17":"Missed: before date limit. Keep only if cognitive load stays in the framing; van Merrienboer & Sweller already covers it for the codebook.",
"S20":"Missed: before date limit. Keep: basis for monitoring; not read, so cite carefully.","S21":"Missed: before date limit, and the wrong domain for these queries. Consider dropping: S17 or another general source would do, and it is on health education.",
"S22":"Missed: a web guide, not indexed as a paper. Keep only as a teaching resource for source roles; not research evidence."}
cc={r["id"]:r for r in csv.DictReader(open(os.path.join(HERE,"citation_check.csv")))}
found={x for p in papers for x in p["seed_id"].split(";") if x}
for s in seeds:
    if s["seed_id"] in found or s["seed_id"]=="S16": continue
    r=cc[s["seed_id"]]
    papers.append(dict(paper_id=s["seed_id"],title=r["confirmed_title"],authors=r["confirmed_authors"],year=re.search(r"(19|20)\d\d",r["citation_as_listed"]).group(0) if s["seed_id"]!="S22" else "",venue=r["confirmed_venue"],identifier=r["confirmed_id"],run="seed list only",tier=("SEED_EXCLUDED_BY_SCREEN" if s["seed_id"] in ("S01","S14") else "SEED_NOT_RECOVERED"),decided_by=KEEP[s["seed_id"]],seed_id=s["seed_id"],found_by="",read_level=READ.get(s["seed_id"],"not read"),abstract_available=""))
cols=["paper_id","title","authors","year","venue","identifier","run","tier","decided_by","seed_id","found_by","read_level","abstract_available"]
with open(os.path.join(HERE,"papers.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,cols); w.writeheader(); w.writerows(papers)
# search log
rows=[]
def counts(run,qid_src):
    p=os.path.join(HERE,"raw","search",run,qid_src+".json")
    if not os.path.exists(p): return 0,0,""
    rs=json.load(open(p)); scr=inc=0; rec=set()
    for r in rs:
        k=norm(r["title"])
        if k in decided:
            scr+=1; inc+=decided[k]=="INCLUDE"
        for s in seeds:
            if is_seed(r,s): rec.add(s["seed_id"])
    return scr,inc,";".join(sorted(rec))
for run,stage in [("dev1","development"),("dev2","development"),("forward","frozen forward run"),("amend1","post-freeze amendment")]:
    for m in json.load(open(os.path.join(HERE,"raw","search",run,"manifest.json"))):
        q=f"{m['qid']}_{m['source']}"; scr,inc,rec=counts(run,q)
        if stage=="development": scr,inc="",""
        note=("" if m["http"]==200 else f"HTTP {m['http']}: rate limited with no key after retries; no records") or ("6 peer-review records on Peters & Chin-Yee dropped automatically before screening" if (run,q)==("forward","Q7_openalex") else "")
        rows.append(dict(date=m["utc"],run=run,stage=stage,query_id=m["qid"],source=m["source"],query=m["text"],hit_count=m["hits"] if m["hits"] is not None else "",retrieved=m["retrieved"],screened=scr,included=inc,n_seed_recovered=len(rec.split(";")) if rec else 0,seeds_recovered=rec,note=note))
sch=[l for l in open(os.path.join(HERE,"protocol.md")) if re.match(r"\d+\. `",l)]
for i,l in enumerate(sch):
    rows.append(dict(date="",run="scholar-hand",stage="not_run_by_hand",query_id=f"H{i+1}",source="google_scholar",query=l.split("`")[1],hit_count="",retrieved="",screened="",included="",n_seed_recovered="",seeds_recovered="",note="robots.txt disallows /scholar; for the user to run by hand"))
with open(os.path.join(HERE,"search_log.csv"),"w",newline="") as f:
    w=csv.DictWriter(f,list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(stats); print("papers",len(papers), "core",sum(p['tier']=='CORE' for p in papers))
for run in ("frozen","amendment"):pass
all_seed=set()
for p in papers:
    if p["run"] in ("frozen",): all_seed|=set(x for x in p["seed_id"].split(";") if x)
print("seeds included from frozen",sorted(all_seed))
print("seeds included from amendment",sorted({x for p in papers if p['run']=='amendment' for x in p['seed_id'].split(';') if x}))
for p in papers:
    if p["seed_id"] and p["run"]!="seed list only": print(p["seed_id"],p["paper_id"],p["tier"],p["decided_by"],p["found_by"][:50],p["title"][:50])
