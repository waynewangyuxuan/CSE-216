#!/usr/bin/env python3
"""Run the frozen queries against OpenAlex, arXiv and Semantic Scholar; save raw responses and merge into candidates.
Usage: run_search.py <run_label> [--only Q3] [--sources openalex,arxiv,s2]. Raw files go to raw/search/<label>/."""
import json, os, re, sys, time, hashlib, csv, urllib.parse, urllib.request, urllib.error, xml.etree.ElementTree as ET, datetime
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cfgname = sys.argv[sys.argv.index("--config")+1] if "--config" in sys.argv else "queries.json"
cfg = json.load(open(os.path.join(HERE, "scripts", cfgname)))
label = sys.argv[1]
only = sys.argv[sys.argv.index("--only")+1] if "--only" in sys.argv else None
srcs = sys.argv[sys.argv.index("--sources")+1].split(",") if "--sources" in sys.argv else ["openalex","arxiv","s2"]
OUT = os.path.join(HERE, "raw", "search", label); os.makedirs(OUT, exist_ok=True)
UA = "CSE216-lit-search/1.0 (course project)"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()
def get_retry(url, waits=(5,20,45)):
    for i, w in enumerate((0,)+tuple(waits)):
        if w: time.sleep(w)
        try: return get(url), 200
        except urllib.error.HTTPError as e:
            code = e.code
            if code not in (429,500,502,503): return None, code
        except Exception: code = -1
    return None, code
ns={'a':'http://www.w3.org/2005/Atom','o':'http://a9.com/-/spec/opensearch/1.1/'}
def arxiv_q(t):
    # convert the boolean string to arXiv field syntax: each term or phrase becomes all:term
    out = re.sub(r'"[^"]+"|\b(?!AND\b|OR\b)[A-Za-z][\w-]*', lambda m: 'all:'+m.group(0), t)
    return out
def inv(ab):
    if not ab: return ""
    pos=[(i,w) for w,ps in ab.items() for i in ps]
    return " ".join(w for i,w in sorted(pos))
def run_openalex(q):
    f=[f"title_and_abstract.search:{q['text']}", f"from_publication_date:{cfg['from_date']}"]
    if 'openalex_cites_doi' in q:
        w=json.loads(get("https://api.openalex.org/works/doi:"+q['openalex_cites_doi']+"?select=id"))["id"].split("/")[-1]
        f.append("cites:"+w)
    url="https://api.openalex.org/works?"+urllib.parse.urlencode({"filter":",".join(f),"per_page":cfg["openalex_per_query"],"sort":"relevance_score:desc","select":"id,doi,title,publication_year,publication_date,authorships,primary_location,abstract_inverted_index,type,ids,referenced_works"})
    b,code=get_retry(url)
    if b is None: return None,code,url
    d=json.loads(b); recs=[]
    for r in d["results"]:
        pl=r.get("primary_location") or {}; so=pl.get("source") or {}
        ax=None
        for s in [(r.get("ids") or {}).get("doi") or "", pl.get("landing_page_url") or ""]:
            m=re.search(r"(?:arxiv\.org/abs/|10\.48550/arxiv\.)(\d{4}\.\d{4,5})",s,re.I)
            if m: ax=m.group(1)
        recs.append(dict(title=r.get("title") or "",authors="; ".join(a["author"]["display_name"] for a in (r.get("authorships") or [])[:6]),year=r.get("publication_year"),venue=so.get("display_name") or "",doi=(r.get("doi") or "").replace("https://doi.org/","").lower(),arxiv=ax,abstract=inv(r.get("abstract_inverted_index")),openalex=r["id"],type=r.get("type")))
    return dict(hits=d["meta"]["count"],recs=recs),200,url
def run_arxiv(q):
    url="https://export.arxiv.org/api/query?"+urllib.parse.urlencode({"search_query":arxiv_q(q["text"]),"start":0,"max_results":cfg["arxiv_per_query"],"sortBy":"relevance"})
    b,code=get_retry(url)
    time.sleep(3.2)
    if b is None: return None,code,url
    root=ET.fromstring(b); recs=[]
    for e in root.findall('a:entry',ns):
        t=lambda k:(e.find(k,ns).text if e.find(k,ns) is not None else "") or ""
        aid=re.search(r"abs/(\d{4}\.\d{4,5})",t('a:id'))
        pub=t('a:published')[:10]
        if pub<cfg["from_date"]: continue
        recs.append(dict(title=" ".join(t('a:title').split()),authors="; ".join(a.find('a:name',ns).text for a in e.findall('a:author',ns)[:6]),year=int(pub[:4]) if pub else None,venue="arXiv",doi="",arxiv=aid.group(1) if aid else None,abstract=" ".join(t('a:summary').split()),openalex="",type="preprint"))
    return dict(hits=int(root.find('o:totalResults',ns).text),recs=recs),200,url
def run_s2(q):
    url="https://api.semanticscholar.org/graph/v1/paper/search?"+urllib.parse.urlencode({"query":re.sub(r'\bAND\b|\bOR\b|[()]',' ',q["text"]),"limit":cfg["s2_per_query"],"year":"2022-","fields":"title,year,authors,venue,abstract,externalIds"})
    b,code=get_retry(url,waits=(10,30))
    if b is None: return None,code,url
    d=json.loads(b); recs=[]
    for r in d.get("data",[]):
        x=r.get("externalIds") or {}
        recs.append(dict(title=r.get("title") or "",authors="; ".join(a["name"] for a in (r.get("authors") or [])[:6]),year=r.get("year"),venue=r.get("venue") or "",doi=(x.get("DOI") or "").lower(),arxiv=x.get("ArXiv"),abstract=r.get("abstract") or "",openalex="",type=""))
    return dict(hits=d.get("total",0),recs=recs),200,url
runners={"openalex":run_openalex,"arxiv":run_arxiv,"s2":run_s2}
now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"); manifest=[]
for q in cfg["queries"]+cfg["citation_queries"]:
    if only and q["id"]!=only: continue
    for s in srcs:
        if "openalex_cites_doi" in q and s!="openalex": continue
        res,code,url=runners[s](q)
        row=dict(run=label,utc=now,qid=q["id"],source=s,text=q["text"],url=url,http=code,hits=None,retrieved=0)
        if res:
            row.update(hits=res["hits"],retrieved=len(res["recs"]))
            json.dump(res["recs"],open(os.path.join(OUT,f"{q['id']}_{s}.json"),"w"),ensure_ascii=False)
        manifest.append(row); print(q["id"],s,code,row["hits"],row["retrieved"],flush=True)
        time.sleep(0.3)
json.dump(manifest,open(os.path.join(OUT,"manifest.json" if not only else f"manifest_{only}.json"),"w"),indent=1,ensure_ascii=False)
print("queries sha256:",hashlib.sha256(open(os.path.join(HERE,"scripts",cfgname),"rb").read()).hexdigest())
