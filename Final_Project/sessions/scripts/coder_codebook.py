#!/usr/bin/env python3
"""Write sessions/coder_codebook_v1.1.md: the frozen v1.1 codebook with section 9 (Q3-Q5 risk indicators) removed, for coders (decisions.tsv S03).
The frozen file is only read. Records its SHA-256 and checks every other line is kept word for word. Prints the hash and line counts."""
import hashlib, os
import s6

SRC = os.path.join(s6.CODEBOOK, "CSE216_Research_Writing_Codebook_v1.1.md")
DST = os.path.join(s6.SESS, "coder_codebook_v1.1.md")


def main():
    raw = open(SRC, encoding="utf-8").read()
    h = hashlib.sha256(raw.encode()).hexdigest()
    lines = raw.split("\n")
    a = next(n for n, l in enumerate(lines) if l.startswith("## 9."))
    b = next(n for n, l in enumerate(lines) if l.startswith("## 10."))
    keep = lines[:a] + ["## 9. (Removed from this coder copy. It is reporting guidance for later analysis, not a coding rule.)", ""] + lines[b:]
    note = f"<!-- Coder copy made by sessions/scripts/coder_codebook.py from codebook/CSE216_Research_Writing_Codebook_v1.1.md, sha256 {h}. Section 9 removed; all else unchanged. -->"
    out = note + "\n" + "\n".join(keep)
    assert keep[:a] == lines[:a] and keep[a + 2:] == lines[b:]
    assert "| Candidate indicator |" not in "\n".join(keep)
    open(DST, "w", encoding="utf-8").write(out)
    print("source sha256", h, "lines kept", len(lines) - (b - a), "of", len(lines), "removed", b - a)


if __name__ == "__main__":
    main()
