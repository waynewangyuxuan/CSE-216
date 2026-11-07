#!/usr/bin/env python3
"""Fetch the public registry record for every seed citation and save it under raw/seed/. Safe to rerun."""
import json, os, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "raw", "seed"); os.makedirs(OUT, exist_ok=True)
UA = "CSE216-lit-check/1.0 (course project)"
ARXIV = ["2609.13155","2501.10551","2604.07344","2506.08872","2502.02904","2609.20143","2505.16023","2605.29392","2405.01470","2504.12488"]
DOIS = {"bastani":"10.1073/pnas.2422633122","doshi":"10.1126/sciadv.adn5290","flower":"10.2307/356600",
 "lee":"10.1145/3706598.3713778","peters":"10.1098/rsos.241776","risko":"10.1016/j.tics.2016.07.002",
 "sweller98":"10.1023/A:1022193728205","zimmerman":"10.1207/s15430421tip4102_2","vanmerrienboer":"10.1111/j.1365-2923.2009.03498.x",
 "jabareen":"10.1177/160940690900800406","hornbaek":"10.1145/3025453.3025765","mysore_emnlp":"10.18653/v1/2025.emnlp-main.852"}
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read()
ns={'a':'http://www.w3.org/2005/Atom','x':'http://arxiv.org/schemas/atom'}
rows=[]
for a in ARXIV:
    p=os.path.join(OUT,f"arxiv_{a}.xml")
    if not os.path.exists(p):
        try:
            open(p,"wb").write(get("https://export.arxiv.org/api/query?id_list="+a)); time.sleep(3.2)
        except Exception as e: print("ARXIV FAIL",a,e); continue
    root=ET.parse(p).getroot()
    for e in root.findall('a:entry',ns):
        t=lambda k:(e.find(k,ns).text if e.find(k,ns) is not None else "")
        print("ARXIV",a,"|"," ".join(t('a:title').split()),"|",[x.find('a:name',ns).text for x in e.findall('a:author',ns)],"|",t('a:published')[:10],"| updated",t('a:updated')[:10],"| ref:",t('x:journal_ref'),"| doi:",t('x:doi'),"| cmt:",t('x:comment')[:120])
for k,d in DOIS.items():
    p=os.path.join(OUT,f"crossref_{k}.json")
    if not os.path.exists(p):
        try:
            open(p,"wb").write(get("https://api.crossref.org/works/"+urllib.parse.quote(d)));time.sleep(0.5)
        except Exception as e: print("CROSSREF FAIL",k,d,e); continue
    m=json.load(open(p))["message"]
    print("CROSSREF",k,d,"|",(m.get("title") or [""])[0],"|",[f"{x.get('given','')} {x.get('family','')}" for x in m.get("author",[])][:8],"|",(m.get("container-title") or [""])[0],"|",m.get("volume"),m.get("issue"),m.get("page"),"|",(m.get("published") or {}).get("date-parts"))
