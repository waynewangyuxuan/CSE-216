"""Stop unless inference/scripts/apply_rules.py and the v1.2 codebook match the hashes in inference/FROZEN.md."""
import hashlib, os, re, sys

INF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "inference")
frozen = open(os.path.join(INF, "FROZEN.md"), encoding="utf-8").read()
# Only the current-freeze bullets: "- `path` sha256 <64 hex>"
want = dict(re.findall(r"^- `([^`]+)` sha256 ([0-9a-f]{64})$", frozen, re.M))
assert set(want) == {"scripts/apply_rules.py", "CSE216_Writing_Codebook_v1.2.md"}, want
for rel, h in want.items():
    got = hashlib.sha256(open(os.path.join(INF, rel), "rb").read()).hexdigest()
    if got != h:
        sys.exit(f"FROZEN MISMATCH {rel}: {got} != {h}")
    print(f"frozen ok {rel} {h[:12]}")
