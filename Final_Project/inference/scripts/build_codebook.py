"""Rebuild v1.2's section 9 from blind/section9_draft.md (no dataset text in it). Run before freezing."""
import os
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
p = os.path.join(ROOT, "CSE216_Writing_Codebook_v1.2.md")
t = open(p).read(); sec = open(os.path.join(ROOT, "blind", "section9_draft.md")).read().rstrip() + "\n\n"
s = t.index("## 9. "); e = t.index("## 10. Coding record")
open(p, "w").write(t[:s] + sec + t[e:])
