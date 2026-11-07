#!/usr/bin/env python3
"""Convert downloaded PDFs/HTML in a folder to .txt next to them. Usage: extract_text.py <folder>. Needs pypdf and bs4."""
import os, sys
from pypdf import PdfReader
from bs4 import BeautifulSoup
d = sys.argv[1]
for f in sorted(os.listdir(d)):
    p = os.path.join(d, f); out = os.path.splitext(p)[0] + ".txt"
    if f.endswith(".txt") or os.path.exists(out): continue
    if f.endswith(".pdf"):
        r = PdfReader(p)
        pages = []
        for i, pg in enumerate(r.pages):
            try: t = pg.extract_text() or ""
            except Exception as e: t = f"[extract error {e}]"
            pages.append(f"\n[[page {i+1}]]\n{t}")
        open(out, "w").write("".join(pages))
    elif f.endswith(".html"):
        s = BeautifulSoup(open(p, errors="ignore").read(), "html.parser")
        for x in s(["script", "style", "annotation", "nav"]): x.decompose()
        open(out, "w").write("\n".join(l.strip() for l in s.get_text("\n").splitlines() if l.strip()))
    print(f, os.path.getsize(out))
