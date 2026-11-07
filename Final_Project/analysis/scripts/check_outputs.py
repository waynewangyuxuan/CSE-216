"""Last step of run_all: every expected output exists, figures are non-empty PNGs, and no results file
holds anything but codes, ids and numbers (a crude guard: no line longer than 600 characters, no field
names that carry dataset text)."""
import os, sys
from common import RES, FIG

FIGS = [f"fig{i:02d}" for i in range(1, 15)]
need = ["out_of_sample.md", "out_of_sample.json", "sessions.md", "sessions.json", "sensitivity.md", "sensitivity.json",
        "patterns.md", "patterns/signatures.csv", "patterns/session_types.csv", "sessions/session_table.csv",
        "v12_final/window_categories.csv", "v12_coderA/window_categories.csv", "v12_coderB/window_categories.csv"]
bad = [p for p in need if not os.path.exists(os.path.join(RES, p))]
pngs = sorted(f for f in os.listdir(FIG) if f.endswith(".png"))
for f in FIGS:
    hits = [p for p in pngs if p.startswith(f)]
    if not hits or os.path.getsize(os.path.join(FIG, hits[0])) < 5000:
        bad.append(f"figure {f}")
TEXT_FIELDS = ("evidence_note", "user_text", "response", "prompt_text", "content")
for root, _, files in os.walk(RES):
    for fn in files:
        with open(os.path.join(root, fn), encoding="utf-8") as fh:
            head = fh.readline()
            if any(t in head for t in TEXT_FIELDS):
                bad.append(f"text field in {fn}")
            for line in [head] + fh.readlines():
                if len(line) > 600 and not fn.endswith(".json"):
                    bad.append(f"long line in {fn}")
                    break
if bad:
    sys.exit("check_outputs FAILED: " + "; ".join(bad))
print(f"check_outputs ok: {len(need)} result files, {len(pngs)} figures")
