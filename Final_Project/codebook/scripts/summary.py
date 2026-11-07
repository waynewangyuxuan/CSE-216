#!/usr/bin/env python3
"""Tables for REPORT.md, from pilot_results/. Rerunnable; prints no window text. Writes pilot_results/summary.json."""
import collections, csv, json, os
from views import CODEBOOK

R = os.path.join(CODEBOOK, "pilot_results")
ROUNDS = ["r1", "r2", "r3", "r4"]
FIELDS = ["operation", "family", "function", "object", "prior_own_work", "decision", "verification", "uptake"]
ag = {r: json.load(open(os.path.join(R, f"{r}_agreement.json"))) for r in ROUNDS}
lab = {r: list(csv.DictReader(open(os.path.join(R, f"{r}_labels.csv")))) for r in ROUNDS}
out = {}

print("| Field | R1 n=40 % / k | R2 n=40 % / k [CI] | R3 n=30 % / k [CI] | R4 final text n=22 % / k [CI] |")
print("|---|---|---|---|---|")
for f in FIELDS:
    c = [ag[r]["agreement"][f]["all"] for r in ROUNDS]
    print(f"| `{f}` | {c[0]['pct_agree']} / {c[0]['kappa']} | " + " | ".join(f"{x['pct_agree']} / {x['kappa']} {x['kappa_ci95']}" for x in c[1:]) + " |")
for f in ["decision", "verification", "uptake"]:
    print(f"Follow-up windows k, {f}: " + " -> ".join(str(ag[r]["agreement"][f]["followup_C1C2"]["kappa"]) for r in ROUNDS))
    print(f"Random-only k, {f}: " + ", ".join(f"{r} n={ag[r]['agreement'][f]['random_only']['n']} {ag[r]['agreement'][f]['random_only']['kappa']}" for r in ROUNDS))
    print(f"R4 by dataset, {f}: NIRVANA {ag['r4']['agreement'][f]['NIRVANA']['kappa']}, WildChat {ag['r4']['agreement'][f].get('WildChat', {}).get('kappa')}")
wc = {r: ag[r]["agreement"]["domain"]["WildChat"] for r in ROUNDS}
print("domain, WildChat only:", {r: (v["n"], v["pct_agree"], v["kappa"]) for r, v in wc.items()})
print("u4_subtype:", {r: (ag[r]["agreement"]["u4_subtype"]["all"]["n"], ag[r]["agreement"]["u4_subtype"]["all"]["pct_agree"], ag[r]["agreement"]["u4_subtype"]["all"]["kappa"]) for r in ROUNDS})


def short(v):
    return (v or "").split("_")[0]


print("\nLabel use, two coders' labels pooled (each window counts twice)")
print("| Label | R1 | R2 | R3 | R4 | Total of 264 | Random windows only, of 210 |")
print("|---|---|---|---|---|---|---|")
rand = [x for r in ROUNDS for x in lab[r] if x["targeted"] == "0"]
assert len(rand) == 210
for f in ["decision", "verification", "uptake"]:
    labels = sorted({short(x[f]) for r in ROUNDS for x in lab[r]})
    for k in labels:
        n = [sum(short(x[f]) == k for x in lab[r]) for r in ROUNDS]
        rr = sum(short(x[f]) == k for x in rand)
        print(f"| `{k}` | {n[0]} | {n[1]} | {n[2]} | {n[3]} | {sum(n)} | {rr} |")
        out[k] = n
print("\nPer label, across rounds: windows where both coders chose it / windows where either did")
for f in ["decision", "verification", "uptake"]:
    labels = sorted({short(x[f]) for r in ROUNDS for x in lab[r]})
    row = []
    for k in labels:
        both = either = 0
        for r in ROUNDS:
            byw = collections.defaultdict(list)
            for x in lab[r]:
                byw[x["window_id"]].append(short(x[f]))
            both += sum(v[0] == k and v[1] == k for v in byw.values())
            either += sum(k in v for v in byw.values())
        row.append(f"{k} {both}/{either}")
    print(f, "; ".join(row))
print("domain, WildChat, pooled n and agreement per round:", {r: (ag[r]["agreement"]["domain"]["WildChat"]["n"], ag[r]["agreement"]["domain"]["WildChat"]["kappa"]) for r in ROUNDS})
seen_s = set()
for r in ROUNDS:
    ids = [x["window_id"] for x in lab[r] if x["coder"] == "A" and x["targeted"] == "0"]
    sess = ["-".join(i.split("-")[:2]) for i in ids]
    print(f"{r}: random windows {len(ids)}, from a session used in an earlier round {sum(s in seen_s for s in sess)}")
    seen_s |= {"-".join(x["window_id"].split("-")[:2]) for x in lab[r]}
ops = collections.Counter(x["operation"] for r in ROUNDS for x in lab[r])
print("\noperation pooled:", dict(sorted(ops.items())))
print("family pooled:", dict(sorted(collections.Counter(x["family"] for r in ROUNDS for x in lab[r]).items())))
print("prior_own_work pooled:", dict(sorted(collections.Counter(x["prior_own_work"] for r in ROUNDS for x in lab[r]).items())))
print("function pooled:", dict(sorted(collections.Counter(short(x["function"]) for r in ROUNDS for x in lab[r]).items())))
print("object pooled:", dict(sorted(collections.Counter(x["object"] for r in ROUNDS for x in lab[r]).items())))

PMAP = {f"O{i:02d}": ("P" if i <= 9 else "T" if i <= 11 else "R" if i <= 15 else "M") for i in range(1, 17)} | {"OX": "PX"}
pr = [x for r in ("r1", "r2") for x in lab[r]]
print(f"\nprocess equals the map from operation: {sum(PMAP[x['operation']] == x['process'] for x in pr)} of {len(pr)}")

# Audit: coder editor-uptake labels vs script overlap
t = collections.Counter()
aud = {"both": 0, "agree": 0}
u7 = {"n": 0, "script_no_match": 0}
for r in ROUNDS:
    fx = json.load(open(os.path.join(R, f"{r}_overlap.json")))["facts"]
    for x in lab[r]:
        f = fx.get(x["window_id"])
        if not f:
            continue
        s = short(x["uptake"])
        t[(f["class"], s)] += 1
        if s in ("U1", "U2") and f["audit_u1_vs_u2"]:
            aud["both"] += 1
            aud["agree"] += f["audit_u1_vs_u2"] == s
        if s == "U7":
            u7["n"] += 1
            u7["script_no_match"] += f["class"] in ("ADDED_TEXT_NO_MATCH", "SMALL_EDITS_ONLY", "NO_EDITOR_TEXT")
print("\nScript class by coder label (labels, both coders):")
for k, v in sorted(t.items()):
    print(" ", k, v)
print("U1/U2 labels where script audit agrees:", aud, " U7 labels with no script match:", u7)

key = {x["window_id"]: x for x in csv.DictReader(open(os.path.join(R, "vignette_key.csv")))}
VA = {json.loads(l)["window_id"]: json.loads(l) for l in open(os.path.join(CODEBOOK, "pilot", "r3", "coder_a", "vignette_labels.jsonl"))}
VB = {json.loads(l)["window_id"]: json.loads(l) for l in open(os.path.join(CODEBOOK, "pilot", "r3", "coder_b", "vignette_labels.jsonl"))}
print("\nConstructed cases (n=12): coders agree / both match the author's key")
for f in ("verification", "uptake", "decision"):
    print(f, sum(VA[i][f] == VB[i][f] for i in key), "/", sum(VA[i][f] == VB[i][f] == key[i][f] for i in key))
json.dump({"label_use": out, "ops": ops}, open(os.path.join(R, "summary.json"), "w"), indent=1, sort_keys=True)
