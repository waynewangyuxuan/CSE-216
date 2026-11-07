"""Gate check: no committed Bet 8 file (analysis/, report/) shares a run of 8+ consecutive words with any
window text in the git-excluded views (sessions/blind/parts, wildchat/blind/views, data/windows.jsonl).
Prints only file names and counts, never the matched text. Skips with a note when the views are absent
(a fresh clone has none). Usage: python3 check_no_text.py"""
import glob, os, re, sys
from common import FP

N = 8
WORD = re.compile(r"[a-z0-9']+")


def grams(text):
    w = WORD.findall(text.lower())
    return {" ".join(w[i:i + N]) for i in range(len(w) - N + 1)}


def main():
    sources = (glob.glob(os.path.join(FP, "sessions", "blind", "parts", "*", "*.txt"))
               + glob.glob(os.path.join(FP, "wildchat", "blind", "views", "*", "*.txt"))
               + glob.glob(os.path.join(FP, "data", "windows.jsonl")))
    if not sources:
        print("check_no_text: skipped (no git-excluded views on this machine)")
        return
    src = set()
    for p in sources:
        with open(p, encoding="utf-8", errors="ignore") as f:
            src |= grams(f.read())
    # Boilerplate shared by every view (field labels, codebook phrases) is not dataset text.
    targets = [p for d in ("analysis", "report") for p in glob.glob(os.path.join(FP, d, "**", "*"), recursive=True)
               if os.path.isfile(p) and p.endswith((".md", ".csv", ".json", ".tsv", ".txt", ".py", ".sh"))
               and "/blind/" not in p and "/.venv/" not in p]
    bad = {}
    for p in targets:
        with open(p, encoding="utf-8", errors="ignore") as f:
            hit = grams(f.read()) & src
        if hit:
            bad[os.path.relpath(p, FP)] = len(hit)
    if bad:
        sys.exit("check_no_text FAILED (8-word runs shared with window text): " +
                 "; ".join(f"{k} {v}" for k, v in sorted(bad.items())))
    print(f"check_no_text ok: {len(targets)} files, {len(sources)} source files, no shared {N}-word run")


if __name__ == "__main__":
    main()
