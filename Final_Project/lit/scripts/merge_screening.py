#!/usr/bin/env python3
"""Compare the two screeners, report agreement, and list disagreements. Usage: merge_screening.py."""
import csv, json, os
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=os.path.join(HERE,"screening")
c={json.loads(l)["cid"]:json.loads(l) for l in open(os.path.join(S,"candidates.jsonl"))}
def load(p):
    d={}
    for l in open(p):
        x=l.rstrip("\n").split("\t")
        if len(x)>=3 and x[0] in c: d[x[0]]=x
    return d
A=load(os.path.join(S,"screener_A.tsv")); B=load(os.path.join(S,"screener_B.tsv"))
print("records",len(c),"A",len(A),"B",len(B))
both=[k for k in c if k in A and k in B]
a=[A[k][1] for k in both]; b=[B[k][1] for k in both]
agree=sum(x==y for x,y in zip(a,b))/len(both)
pa=a.count("INCLUDE")/len(a); pb=b.count("INCLUDE")/len(b)
pe=pa*pb+(1-pa)*(1-pb); kappa=(agree-pe)/(1-pe)
print(f"agreement {agree:.3f} kappa {kappa:.3f}  A include {a.count('INCLUDE')}  B include {b.count('INCLUDE')}")
both_inc=[k for k in both if A[k][1]=="INCLUDE" and B[k][1]=="INCLUDE"]
either=[k for k in both if (A[k][1]=="INCLUDE")!=(B[k][1]=="INCLUDE")]
core=[k for k in both_inc if A[k][2]=="CORE" and B[k][2]=="CORE"]
print("both include",len(both_inc),"disagree",len(either),"both core",len(core))
with open(os.path.join(S,"disagreements.txt"),"w") as o:
    for k in either:
        o.write(f"{k} | {c[k]['title']} | {c[k]['year']} | A:{A[k][1]}/{A[k][2]} B:{B[k][1]}/{B[k][2]}\nABSTRACT: {(c[k]['abstract'] or '[none]')[:500]}\n\n")
