#!/usr/bin/env python3
"""Write screening/adjudication.tsv: the third-judge decision and rule for each screener disagreement."""
import json, os
R={
"R1":"Review of human-use studies: prompt was silent on reviews. Keep if on writing, offloading, agency or metacognition; drop general education reviews as E4.",
"R2":"System paper: keep only if the abstract shows human use data. Adjudicator read the full abstract.",
"R3":"No usable abstract: keep only if the title alone clearly meets I1 and I2; marked title-only.",
"R4":"Other domains: keep only if it proposes a framework or measure of offloading or reliance.",
"R5":"Perception or acceptance survey with no behavior, reliance, checking or ownership measure: E6.",
"R6":"Abstract not in English: fails I3.",
"R7":"Earlier version of a paper already in the set: drop as superseded.",
"R8":"Direct application of I1 to I3.",
}
inc=lambda t,r,n="":(("INCLUDE",t,r,n))
exc=lambda c,r,n="":(("EXCLUDE",c,r,n))
D={
"C0009":exc("E4","R8","argues for redesign; no data or framework visible"),"C0011":exc("E4","R1","general education review"),
"C0017":inc("CONTEXT","R3","title states measured reliance in large sample"),"C0025":exc("E6","R5"),"C0033":exc("E3","R4","programming course, no framework"),
"C0043":exc("R7","R7","superseded by Jelson 2026"),"C0068":inc("CORE","R2","14-day field deployment on authorship"),"C0077":inc("CONTEXT","R1"),
"C0088":inc("CONTEXT","R8","professional writers edit LLM text"),"C0116":exc("E4","R1"),"C0132":inc("CORE","R3","title names ChatGPT interaction in writing"),
"C0133":inc("CORE","R8","seed Reza 2025; PRISMA review plus 15 interviews"),"C0141":inc("CONTEXT","R4","proposes a model of generative atrophy"),"C0143":inc("CONTEXT","R1"),
"C0148":inc("CONTEXT","R1"),"C0151":inc("CONTEXT","R2","technical evaluation with small pilot"),"C0176":exc("R6","R6"),"C0179":inc("CONTEXT","R3","dependence scale"),
"C0193":exc("E3","R4"),"C0198":inc("CONTEXT","R1"),"C0202":exc("E6","R5"),"C0231":exc("E6","R5"),"C0259":exc("E3","R4"),"C0260":inc("CONTEXT","R8","predictors of delegating writing"),
"C0261":exc("E4","R8"),"C0266":inc("CONTEXT","R3","systematic review of overreliance"),"C0275":inc("CONTEXT","R1"),"C0277":exc("E4","R1","record too thin to judge"),
"C0281":exc("E4","R1"),"C0283":inc("CONTEXT","R1"),"C0285":exc("E4","R1","feedback and rating focus"),"C0286":inc("CONTEXT","R4","epistemic responsibility framework"),
"C0288":inc("CONTEXT","R4","scaffold pathways framework"),"C0294":inc("CONTEXT","R1"),"C0296":inc("CONTEXT","R3","dependence scale"),"C0305":exc("E4","R1"),"C0308":inc("CONTEXT","R1"),
"C0312":exc("E4","R1"),"C0328":inc("CONTEXT","R1"),"C0329":inc("CONTEXT","R1","scientific writing"),"C0332":inc("CORE","R2","18 participants on writing agency"),"C0342":exc("E3","R4"),
"C0344":inc("CONTEXT","R1"),"C0345":exc("E3","R4"),"C0350":inc("CONTEXT","R3"),"C0354":exc("E3","R4"),"C0371":exc("E6","R5"),"C0377":inc("CONTEXT","R4","offloading to orchestration framework"),
"C0381":exc("E4","R8"),"C0383":exc("E2","R2","no human data in abstract"),"C0385":inc("CONTEXT","R3","randomized vignette on co-writing"),"C0387":inc("CONTEXT","R8","survey measures ownership concern"),
"C0390":exc("E3","R4"),"C0391":inc("CORE","R8","interviews and chat logs on delegation"),"C0408":inc("CONTEXT","R3","graduate research writing"),"C0427":inc("CORE","R8","ownership survey"),
"C0432":exc("E4","R1","bibliometric"),"C0439":inc("CONTEXT","R1"),"C0443":inc("CONTEXT","R2","N=146 online study"),"C0444":inc("CONTEXT","R2","writers' utilization measured"),
"C0456":exc("E3","R4"),"C0468":exc("E3","R4"),"C0471":inc("CORE","R8","misattribution of contribution"),"C0478":inc("CONTEXT","R2","RCT N=64 on scaffolded use"),"C0484":exc("E2","R8"),
"C0488":exc("E6","R5","simulated survey data"),"C0489":inc("CONTEXT","R3"),"C0491":inc("CORE","R8","planning/waiting/reviewing claim"),"C0493":exc("E3","R4"),"C0502":exc("E4","R1"),
"C0507":inc("CONTEXT","R4"),"C0512":exc("E3","R4"),"C0529":exc("E6","R5"),"C0531":exc("E6","R5"),"C0549":exc("E3","R4"),"C0555":exc("E3","R4"),"C0557":inc("CONTEXT","R8","think-first vs general AI plan"),
"C0560":exc("E3","R4"),"C0563":inc("CORE","R2","13 writers; provenance tool"),"C0567":inc("CONTEXT","R1"),"C0569":inc("CONTEXT","R1"),"C0571":exc("R6","R6"),"C0575":exc("E3","R4"),
"C0577":inc("CONTEXT","R4","misattribution concept"),"C0579":inc("CONTEXT","R4"),"C0595":inc("CORE","R4","measure of offloading, programming"),"C0598":inc("CONTEXT","R1"),"C0599":exc("E5","R8"),
"C0618":exc("E6","R5"),"C0633":inc("CONTEXT","R8","writers' disclosure decisions"),"C0637":exc("E3","R4"),"C0644":exc("R7","R7","workshop version of Jelson 2026"),"C0650":exc("E4","R8"),
}
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(HERE,"screening","adjudication.tsv"),"w") as o:
    o.write("cid\tdecision\tcode_or_tier\trule\tnote\n")
    for k,v in sorted(D.items()): o.write("\t".join((k,)+v)+"\n")
    o.write("\n# rules\n"); [o.write(f"# {k}: {v}\n") for k,v in R.items()]
print(len(D), sum(v[0]=="INCLUDE" for v in D.values()))
# Amendment-run disagreements (added after A1)
AM={"A013":("INCLUDE","CONTEXT","R4","conceptual account of resisting surrender"),"A038":("EXCLUDE","E3","R4","persuasion on societal issues"),"A049":("EXCLUDE","E7","R3","no abstract; enterprise task")}
with open(os.path.join(HERE,"screening","adjudication_amend.tsv"),"w") as o:
    o.write("cid\tdecision\tcode_or_tier\trule\tnote\n")
    for k,v in sorted(AM.items()): o.write("\t".join((k,)+v)+"\n")
