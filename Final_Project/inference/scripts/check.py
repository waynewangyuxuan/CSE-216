"""Checks for the inference layer. No model calls.
1. Every rule's category is a known category; R99 is last (total coverage).
2. Codebook v1.1 worked examples E1-E14 (constructed, not data) get the expected category.
3. Every window in calibration/final gets exactly one category, and categories match a fresh run.
4. If FROZEN.md exists, apply_rules.py matches its recorded sha256.
"""
import csv, hashlib, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_rules as A

ROOT = os.path.dirname(HERE)
fails = []

assert A.RULES[-1][0] == "R99" and A.RULES[-1][3]({}) is True
for rid, cat, *_ in A.RULES:
    if cat not in A.CATEGORIES:
        fails.append(f"{rid}: unknown category {cat}")

def ex(cov, prior, f, d, v, u):
    return {"window_id": "E", "coverage": cov, "prior_own_work": prior, "function": f, "decision": d,
            "verification": v, "uptake": u}

# Expected categories are what section 9 states for these constructed cases.
EXAMPLES = {
    "E1 format citation, pasted": (ex("C2", "VISIBLE_DRAFT", "F8_PROCEDURAL", "D0_NO_DECISION", "V0_NONE_VISIBLE", "U1_EDITOR_DIRECT"), A.NEUTRAL),
    "E2 grammar of own claim, wording edits": (ex("C2", "VISIBLE_DRAFT", "F5_TRANSFORM", "D1_HUMAN_GIVEN", "V1_SURFACE_ONLY", "U2_EDITOR_SURFACE"), A.OFFLOADING),
    "E3 polish, next paragraph": (ex("C1", "VISIBLE_DRAFT", "F5_TRANSFORM", "D1_HUMAN_GIVEN", "V0_NONE_VISIBLE", "U8_MOVED_ON"), A.OFFLOADING),
    "E4 thesis options, picks and limits": (ex("C1", "VISIBLE_PARTIAL", "F2_OPTIONS", "D3_HUMAN_CHOSE_REVISED", "V3_REASONED_CHALLENGE", "U5_CHAT_ACCEPT"), A.OFFLOADING),
    "E5 full essay pasted whole": (ex("C2", "NONE_VISIBLE", "F4_GENERATE", "D4_AI_PROPOSAL_TAKEN", "V0_NONE_VISIBLE", "U1_EDITOR_DIRECT"), A.SURRENDER),
    "E6 stance, essay, claims replaced": (ex("C2", "VISIBLE_PARTIAL", "F4_GENERATE", "D3_HUMAN_CHOSE_REVISED", "V0_NONE_VISIBLE", "U3_EDITOR_SUBSTANTIVE"), A.OFFLOADING),
    "E7 what is lost, own sentences": (ex("C2", "VISIBLE_DRAFT", "F2_OPTIONS", "D2_AI_PROPOSED_OPEN", "V0_NONE_VISIBLE", "U7_EDITOR_NEW_TEXT"), A.AUGMENTING),
    "E8 compare papers, C0": (ex("C0", "UNOBSERVABLE", "F4_GENERATE", "D2_AI_PROPOSED_OPEN", "VX_UNOBSERVABLE", "UX_NO_TRACE"), A.INDET),
    "E9 summary challenged from source": (ex("C1", "UNOBSERVABLE", "F1_EXPLAIN", "D3_HUMAN_CHOSE_REVISED", "V4_SOURCE_COMPARISON", "U4_CHAT_ITERATE"), A.OFFLOADING),
    "E11 outline, will use": (ex("C1", "UNOBSERVABLE", "F3_PLAN", "D4_AI_PROPOSAL_TAKEN", "V0_NONE_VISIBLE", "U5_CHAT_ACCEPT"), A.SURRENDER),
    "E12 template, AI invents, text sent": (ex("C1", "UNOBSERVABLE", "F5_TRANSFORM", "D2_AI_PROPOSED_OPEN", "V0_NONE_VISIBLE", "U4_CHAT_ITERATE"), A.INDET),
    "E14 advice only, writer rejects": (ex("C1", "UNOBSERVABLE", "F4_GENERATE", "D3_HUMAN_CHOSE_REVISED", "V0_NONE_VISIBLE", "U6_REJECT"), A.INDET),
    "E10-style prior window: generate, then AI asked to recheck itself": (ex("C1", "UNOBSERVABLE", "F4_GENERATE", "D2_AI_PROPOSED_OPEN", "V2_AI_SELF_CHECK", "U4_CHAT_ITERATE"), A.SURRENDER),
    "unsettled code": (ex("C1", "VISIBLE_DRAFT", "F5_TRANSFORM", "D2_AI_PROPOSED_OPEN", "UNSETTLED", "U4_CHAT_ITERATE"), A.INDET),
}
for name, (row, want) in EXAMPLES.items():
    rid, got, *_ = A.classify(row)
    if got != want:
        fails.append(f"{name}: got {got} via {rid}, want {want}")

final = os.path.join(ROOT, "calibration", "final", "window_categories.csv")
labels = os.path.join(os.path.dirname(ROOT), "coding", "results", "final_labels.csv")
if os.path.exists(final):
    got = {r["window_id"]: r for r in csv.DictReader(open(final, newline=""))}
    src = list(csv.DictReader(open(labels, newline="")))
    if len(got) != len(src):
        fails.append(f"window count {len(got)} != labels {len(src)}")
    for r in src:
        rid, cat, strength, _ = A.classify(r)
        g = got.get(r["window_id"])
        if not g or (g["rule"], g["category"], g["strength"]) != (rid, cat, strength):
            fails.append(f"{r['window_id']}: saved output differs from fresh run")

frozen = os.path.join(ROOT, "FROZEN.md")
if os.path.exists(frozen):
    m = re.search(r"apply_rules\.py[^\n]*?([0-9a-f]{64})", open(frozen).read())
    h = hashlib.sha256(open(os.path.join(HERE, "apply_rules.py"), "rb").read()).hexdigest()
    if not m or m.group(1) != h:
        fails.append(f"apply_rules.py sha256 {h} does not match FROZEN.md")

print("FAIL\n" + "\n".join(fails) if fails else "OK: rules total, worked examples, saved output, frozen hash")
sys.exit(1 if fails else 0)
