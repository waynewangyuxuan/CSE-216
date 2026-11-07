#!/usr/bin/env python3
"""Script facts for U1/U2/U7: how much editor text after the response matches this response. Needs no judgment.
A character of added text counts as matched when it lies in a run of 30+ characters shared with the response,
after whitespace is collapsed. Prints no text. Usage: overlap.py <round> or overlap.py --all (summary across NIRVANA C2)."""
import ast, collections, json, os, sys
from views import CODEBOOK, load_windows, norm

K = 30
EDIT_TOL = 5  # chars typed or deleted after a paste that still count as unedited (typos at a boundary)


def clean(v):
    v = v or ""
    if "\t{'t':" in v:
        v = v.split("\t", 1)[0]
    if v.endswith("'"):
        v = v[:-1]
        if v.endswith("\\"):
            v = v[:-1]
    return v.replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "'")


def matched(text, source):
    """Number of chars of text inside a K-run also present in source."""
    text, source = norm(text), norm(source)
    if len(text) < K or len(source) < K:
        return 0, len(text)
    grams = {source[i:i + K] for i in range(len(source) - K + 1)}
    cov = [False] * len(text)
    for i in range(len(text) - K + 1):
        if text[i:i + K] in grams:
            for j in range(i, i + K):
                cov[j] = True
    return sum(cov), len(text)


def editor_after(w):
    raw = w.get("editor_after_next_actions") or ""
    try:
        v = ast.literal_eval(raw)
        return "\n".join(str(x) for x in v) if isinstance(v, list) else str(v)
    except (ValueError, SyntaxError):
        return raw


def facts(w, earlier_responses=""):
    ops = [o for o in w["next_actions"] if o["op_loc"] == "editor"]
    pastes = [o for o in ops if o["op_type"] == "p"]
    paste_text = " ".join(clean(o["add"]) or clean(o["selected_text"]) for o in pastes)
    typed_text = "".join(clean(o["add"]) for o in ops if o["op_type"] in ("i", "d_i"))
    deleted = sum(len(clean(o["delete"])) for o in ops if o["op_type"] in ("d", "x", "d_i"))
    pm, pl = matched(paste_text, w["response"])
    if not pm and 0 < len(norm(paste_text)) < K and norm(paste_text) in norm(w["response"]):  # short paste, under the run length
        pm = pl
    tm, tl = matched(typed_text, w["response"])
    def is_match(o):
        t = clean(o["add"]) or clean(o["selected_text"])
        return matched(t, w["response"])[0] or (0 < len(norm(t)) < K and norm(t) in norm(w["response"]))
    first = next((n for n, o in enumerate(ops) if o["op_type"] == "p" and is_match(o)), None)
    after_t = after_d = 0
    if first is not None:
        for o in ops[first + 1:]:
            if o["op_type"] in ("i", "d_i"):
                after_t += len(clean(o["add"]))
            if o["op_type"] in ("d", "x", "d_i"):
                after_d += len(clean(o["delete"]))
    retained = None
    if pm:
        after = norm(editor_after(w))
        pieces = [clean(o["add"]) or clean(o["selected_text"]) for o in pastes]
        matched_text = " ".join(p for p in pieces if matched(p, w["response"])[0] or (0 < len(norm(p)) < K and norm(p) in norm(w["response"])))
        kept, tot = matched(matched_text, after)
        if tot < K:  # too short for the run test
            kept = tot if norm(matched_text) in after else 0
        retained = round(kept / max(1, tot), 3)
    if pm:
        cls = "PASTE_MATCH_UNEDITED" if after_t + after_d <= EDIT_TOL else "PASTE_MATCH_THEN_EDITS"
    elif tm:
        cls = "TYPED_MATCH"
    elif pl or tl >= K:
        cls = "ADDED_TEXT_NO_MATCH"
    elif tl or deleted:
        cls = "SMALL_EDITS_ONLY"
    else:
        cls = "NO_EDITOR_TEXT"
    return {"class": cls, "paste_chars": pl, "paste_matched": pm, "typed_chars": tl, "typed_matched": tm, "deleted_chars": deleted,
            "typed_after_paste": after_t, "deleted_after_paste": after_d,
            "share_paste_retained": retained, "audit_u1_vs_u2": ("U1" if (retained or 0) >= 0.995 else "U2") if pm else None, "share_response_pasted": round(pm / max(1, len(norm(w["response"]))), 2)}


def main():
    rows = load_windows()
    nir = [w for w in rows if w["dataset"] == "NIRVANA" and w["coverage"] == "C2"]
    if sys.argv[1:] == ["--all"]:
        print(collections.Counter(facts(w)["class"] for w in nir))
        print("vs linkage:", collections.Counter((facts(w)["class"], w["linkage"]) for w in nir).most_common())
        return
    rnd = sys.argv[1]
    d = os.path.join(CODEBOOK, "pilot", rnd)
    ids = {json.loads(l)["window_id"] for l in open(os.path.join(d, "view.jsonl"))}
    A = {json.loads(l)["window_id"]: json.loads(l) for l in open(os.path.join(d, "coder_a", "labels.jsonl"))}
    B = {json.loads(l)["window_id"]: json.loads(l) for l in open(os.path.join(d, "coder_b", "labels.jsonl"))}
    t = collections.Counter()
    out = {}
    for w in nir:
        if w["window_id"] in ids:
            f = facts(w)
            out[w["window_id"]] = f
            t[(f["class"], A[w["window_id"]]["uptake"].split("_")[0], B[w["window_id"]]["uptake"].split("_")[0])] += 1
    res = os.path.join(CODEBOOK, "pilot_results")
    os.makedirs(res, exist_ok=True)
    json.dump({"facts": out, "class_vs_coders": {"|".join(k): v for k, v in sorted(t.items())}}, open(os.path.join(res, f"{rnd}_overlap.json"), "w"), indent=1, sort_keys=True)
    for k, v in sorted(t.items()):
        print(v, k)


if __name__ == "__main__":
    main()
