"""Codebook v1.2 inference layer: Q1-Q5 codes -> one window category, by an ordered rule table.

Categories are literature-grounded inferences from observed behavior, not probabilities and not
measurements of cognition. See CSE216_Writing_Codebook_v1.2.md section 9.

Usage:
  python3 apply_rules.py LABELS.csv OUT_DIR
LABELS.csv needs: window_id, session_id, coverage, prior_own_work, function, decision,
verification, uptake. A `turn` column is used for order if present; otherwise the -tNN suffix
of window_id. No model calls; no window text is read or written.
"""
import csv, json, os, re, sys
from collections import Counter, defaultdict

SURRENDER, OFFLOADING, AUGMENTING = "SURRENDER_LEANING", "OFFLOADING", "AUGMENTING"
NEUTRAL, INDET = "NEUTRAL_MECHANICAL", "INDETERMINATE"
CATEGORIES = [SURRENDER, OFFLOADING, AUGMENTING, NEUTRAL, INDET]

KNOWN = {
    "coverage": {"C0", "C1", "C2"},
    "prior_own_work": {"VISIBLE_DRAFT", "VISIBLE_PARTIAL", "NONE_VISIBLE", "UNOBSERVABLE"},
    "function": {"F1_EXPLAIN", "F2_OPTIONS", "F3_PLAN", "F4_GENERATE", "F5_TRANSFORM", "F6_CRITIQUE",
                 "F7_FIND_CHECK", "F8_PROCEDURAL", "FX_OTHER"},
    "decision": {"D0_NO_DECISION", "D1_HUMAN_GIVEN", "D2_AI_PROPOSED_OPEN", "D3_HUMAN_CHOSE_REVISED",
                 "D4_AI_PROPOSAL_TAKEN", "DX_INDETERMINATE"},
    "verification": {"V0_NONE_VISIBLE", "V1_SURFACE_ONLY", "V2_AI_SELF_CHECK", "V3_REASONED_CHALLENGE",
                     "V4_SOURCE_COMPARISON", "VX_UNOBSERVABLE"},
    "uptake": {"U1_EDITOR_DIRECT", "U2_EDITOR_SURFACE", "U3_EDITOR_SUBSTANTIVE", "U7_EDITOR_NEW_TEXT",
               "U4_CHAT_ITERATE", "U5_CHAT_ACCEPT", "U6_REJECT", "U8_MOVED_ON", "UX_NO_TRACE"},
}
FIELDS = list(KNOWN)

def s(code):
    """Short prefix: 'D4_AI_PROPOSAL_TAKEN' -> 'D4'."""
    return code.split("_")[0]

# Ordered rule table. First match wins, so every window gets exactly one category.
# (rule_id, category, strength, test, pattern in words). Sources and alternative readings for each
# rule are in the codebook's rule table, keyed by rule_id.
NOCHECK = {"V0", "V1", "V2"}  # V2: AI asked to check itself, no independent grounds (v1.1 s6)
RULES = [
    ("R00", INDET, "-", lambda w: w["_bad"],
     "A field is missing, unsettled or not a v1.1 code"),
    ("R01", INDET, "-",
     lambda w: w["D"] == "D0" and w["F"] == "F4",
     "D0 + F4: generation requested but no substantive content delivered (advice, refusal, missing input)"),
    ("R02", NEUTRAL, "moderate",
     lambda w: w["D"] == "D0",
     "D0: no substantive decision in play (formatting, look-up, term or task explanation, non-writing request)"),
    ("R03", INDET, "-",
     lambda w: w["C"] == "C0" or w["U"] == "UX" or w["D"] == "DX",
     "No next action (C0), no trace (UX), or origin indeterminate (DX)"),
    ("R04", OFFLOADING, "moderate",
     lambda w: w["V"] in {"V3", "V4"},
     "Reasoned challenge or source comparison against this output (V3/V4)"),
    ("R05", INDET, "-",
     lambda w: w["U"] == "U6",
     "Writer rejects the output in words (U6), no reasoned check"),
    ("R06", SURRENDER, "moderate",
     lambda w: w["D"] == "D3" and w["U"] in {"U1", "U2"} and w["V"] in NOCHECK,
     "Part of the AI text pasted verbatim or with surface edits only, no check (D3 + U1/U2 + V0/V1)"),
    ("R07", SURRENDER, "weak",
     lambda w: (w["D"] == "D3" or w["U"] == "U3") and w["U"] in {"U4", "U5"}
     and w["P"] in {"NONE_VISIBLE", "UNOBSERVABLE"},
     "Writer steers AI content in chat only, with no own work visible: substance stays AI's (D3/U3, chat uptake)"),
    ("R08", OFFLOADING, "moderate",
     lambda w: w["D"] == "D3" or w["U"] == "U3",
     "Writer selects or changes claims of AI content, or changes inserted AI text substantively (D3 or U3)"),
    ("R09", SURRENDER, "strong",
     lambda w: w["D"] == "D4" and w["V"] in NOCHECK and w["U"] in {"U1", "U2"} and w["P"] == "NONE_VISIBLE",
     "No visible own work + AI text reused about half or more, unchanged or surface-only, no check"),
    ("R10", AUGMENTING, "weak",
     lambda w: w["D"] == "D4" and w["V"] in NOCHECK and w["F"] in {"F1", "F6"},
     "AI explanation or evaluation of the writer's text accepted; no AI text enters the writing (D4 + F1/F6)"),
    ("R11", SURRENDER, "moderate",
     lambda w: w["D"] == "D4" and w["V"] in NOCHECK,
     "Other AI-origin content taken (D4) with no check beyond surface"),
    ("R12", AUGMENTING, "moderate",
     lambda w: w["D"] == "D1" and w["U"] == "U7",
     "AI renders the writer's text, writer types own changes instead of pasting (D1 + U7)"),
    ("R13", OFFLOADING, "moderate",
     lambda w: w["D"] == "D1" and w["F"] in {"F5", "F8"},
     "Writer-supplied content handed over for language, mechanics or format (D1 + F5/F8)"),
    ("R14", OFFLOADING, "weak",
     lambda w: w["D"] == "D1",
     "Writer-supplied content rendered by the AI under another request type (D1)"),
    ("R15", SURRENDER, "moderate",
     lambda w: w["D"] == "D2" and w["F"] == "F4" and w["V"] == "V1",
     "AI-originated substance kept; only length, tone or format of it asked for or edited (D2 + F4 + V1)"),
    ("R16", SURRENDER, "weak",
     lambda w: w["D"] == "D2" and w["F"] == "F4" and w["V"] in {"V0", "V2"} and w["U"] in {"U4", "U5", "U8"},
     "Substance requested from the AI; next action neither checks independently, changes nor composes (D2 + F4 + V0/V2, chat)"),
    ("R17", AUGMENTING, "weak",
     lambda w: w["D"] == "D2" and w["F"] == "F4" and w["U"] == "U7" and w["P"] in {"VISIBLE_DRAFT", "VISIBLE_PARTIAL"},
     "Writer with a visible own draft asks for content, then types own text with no verbatim AI run (D2 + F4 + U7)"),
    ("R18", AUGMENTING, "moderate",
     lambda w: w["D"] == "D2" and w["F"] in {"F1", "F6"} and w["U"] in {"U4", "U5", "U7", "U8"},
     "Explanation or critique requested; AI text not reused verbatim (D2 + F1/F6)"),
    ("R19", AUGMENTING, "weak",
     lambda w: w["D"] == "D2" and w["F"] in {"F2", "F3"} and w["U"] == "U7",
     "Options or plan requested, then the writer types own text with no verbatim AI run (F2/F3 + U7)"),
    ("R20", OFFLOADING, "weak",
     lambda w: w["D"] == "D2" and w["F"] == "F7" and w["U"] == "U7",
     "Fact or source look-up, then the writer keeps typing own text (D2 + F7 + U7)"),
    ("R99", INDET, "-", lambda w: True,
     "No rule's pattern fits (e.g. options worked on in chat, F4 + U7 with no own draft, AI rework of its own text)"),
]


def window_order(row):
    if row.get("turn"):
        return int(row["turn"])
    m = re.search(r"-t(\d+)$", row["window_id"])
    return int(m.group(1)) if m else 0


def prep(row):
    bad = [f for f in FIELDS if row.get(f, "") not in KNOWN[f]]
    get = lambda f: s(row[f]) if f not in bad else "?"
    return {"_bad": bool(bad), "_badfields": bad, "C": row.get("coverage", "?"), "P": row.get("prior_own_work", "?"),
            "F": get("function"), "D": get("decision"), "V": get("verification"), "U": get("uptake")}


def classify(row):
    w = prep(row)
    for rid, cat, strength, test, _ in RULES:
        if test(w):
            return rid, cat, strength, w["_badfields"]
    raise AssertionError("R99 always matches")


def session_measures(rows):
    """rows: one session's classified windows. Order by turn."""
    rows = sorted(rows, key=lambda r: r["order"])
    seq = [r["category"] for r in rows]
    n = len(seq)
    trans = Counter(zip(seq, seq[1:]))
    det = [c for c in seq if c != INDET]
    first = next((i for i, c in enumerate(seq) if c == SURRENDER), None)
    return {
        "n_windows": n,
        "sequence": seq,
        "switches": sum(a != b for a, b in zip(seq, seq[1:])),
        "switches_excluding_indeterminate": sum(a != b for a, b in zip(det, det[1:])),
        "transitions": {f"{a}->{b}": k for (a, b), k in sorted(trans.items())},
        "proportions": {c: round(seq.count(c) / n, 3) for c in CATEGORIES},
        "first_surrender_index": None if first is None else first + 1,
        "first_surrender_relative": None if first is None else (round(first / (n - 1), 3) if n > 1 else 0.0),
        "turns_observed": [r["order"] for r in rows],
    }


def main(labels, out_dir):
    with open(labels, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        rid, cat, strength, bad = classify(r)
        out.append({"window_id": r["window_id"], "dataset": r.get("dataset", ""), "session_id": r.get("session_id", ""),
                    "order": window_order(r), "coverage": r.get("coverage", ""), "rule": rid, "category": cat,
                    "strength": strength, "unrecognized_fields": ";".join(bad)})
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "window_categories.csv"), "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(out[0]))
        wr.writeheader(); wr.writerows(out)
    by_sess = defaultdict(list)
    for o in out:
        by_sess[(o["dataset"], o["session_id"])].append(o)
    sessions = {f"{d}:{sid}": session_measures(v) for (d, sid), v in sorted(by_sess.items())}
    n = len(out)
    summary = {"n_windows": n,
               "coverage_not_indeterminate": round(sum(o["category"] != INDET for o in out) / n, 3),
               "by_category": dict(Counter(o["category"] for o in out).most_common()),
               "by_category_strength": dict(sorted(Counter(f'{o["category"]}/{o["strength"]}' for o in out).items())),
               "by_rule": dict(sorted(Counter(o["rule"] for o in out).items())),
               "by_dataset": {d: {"n": len(v), "coverage_not_indeterminate": round(sum(o["category"] != INDET for o in v) / len(v), 3),
                                  "by_category": dict(Counter(o["category"] for o in v).most_common())}
                              for d in sorted({o["dataset"] for o in out}) for v in [[o for o in out if o["dataset"] == d]]},
               "by_coverage": {c: {"n": len(v), "coverage_not_indeterminate": round(sum(o["category"] != INDET for o in v) / len(v), 3)}
                               for c in sorted({o["coverage"] for o in out}) for v in [[o for o in out if o["coverage"] == c]]},
               "unrecognized": [o["window_id"] for o in out if o["unrecognized_fields"]]}
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=1)
    with open(os.path.join(out_dir, "session_measures.json"), "w", encoding="utf-8") as f:
        json.dump(sessions, f, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
