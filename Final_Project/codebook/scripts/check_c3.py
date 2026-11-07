#!/usr/bin/env python3
"""Check the C3 sheet. `check_c3.py` checks a filled sheet; `check_c3.py --blank` checks the packet as issued.
Prints window ids and field names only, never window text. Exit 1 on any problem."""
import csv, io, os, re, sys
from codes import CODE_COLS, ID_COLS, SHEET_COLS
from views import CODEBOOK, DATA

csv.field_size_limit(10**9)
SHEET = os.path.join(CODEBOOK, "c3_gold_sheet.csv")
if "--sheet" in sys.argv:  # check a test copy; keep the real sheet's name, since only that name is git-excluded
    SHEET = sys.argv[sys.argv.index("--sheet") + 1]
PAGE = os.path.join(CODEBOOK, "c3_gold_windows.html")
FORBIDDEN = ["llm_label", "llm_model", "CLEAR_RESEARCH_WRITING", "POSSIBLE_RESEARCH_WRITING", "human_verified", "linkage", "verbatim_this_response", "verbatim_ambiguous", "temporal_only", "first_edit_latency"]
CODE_TOKEN = re.compile(r"\b(D[0-5X]_[A-Z_]+|V[0-5X]_[A-Z_]+|U[1-8X]_[A-Z_]+|F[1-8X]_[A-Z_]+)\b")


def rows():
    """A spreadsheet may save with a byte-order mark, another encoding, stray spaces or empty trailing columns."""
    with open(SHEET, "rb") as f:
        raw = f.read()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") and len(raw) % 2:
        sys.exit("PROBLEM the sheet looks like a damaged UTF-16 file; save it again as CSV")
    encs = ("utf-16",) if raw[:2] in (b"\xff\xfe", b"\xfe\xff") else ("utf-8-sig", "cp1252", "mac_roman")
    for enc in encs:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    first = text.splitlines()[0] if text else ""
    delim = max(",;\t", key=first.count)  # some spreadsheets save with semicolons or tabs
    out = []
    for r in csv.DictReader(io.StringIO(text, newline=""), delimiter=delim):
        stray = r.get(None)
        row = {(k or "").strip(): (v or "").strip() for k, v in r.items() if k is not None and k.strip()}
        if any((v or "").strip() for k, v in r.items() if k is not None and not k.strip()):
            row["_stray"] = "yes"  # text under a column with no name
        if not any(row.values()) and not any(s.strip() for s in (stray or [])):
            continue  # an empty trailing row
        if stray and any(s.strip() for s in stray):
            row["_stray"] = "yes"
        out.append(row)
    return out


def base(R):
    errs = []
    with open(os.path.join(DATA, "gold.csv"), encoding="utf-8", newline="") as f:
        gold = {r["window_id"]: r for r in csv.DictReader(f)}
    if R and [k for k in R[0] if k != "_stray"] != SHEET_COLS:
        missing = [c for c in SHEET_COLS if c not in R[0]]
        errs.append(f"columns differ from the v1.1 sheet; missing: {missing}")
        return errs
    for r in R:
        if r.get("_stray"):
            errs.append(f"{r.get('window_id')}: text in a column past the last one")
    if {r["window_id"] for r in R} != set(gold) or len(R) != len(gold):
        errs.append("window ids differ from gold.csv")
    for r in R:
        g = gold.get(r["window_id"])
        if g and any(r[k] != g[k] for k in ID_COLS):
            errs.append(f"{r['window_id']}: id columns changed")
    return errs


def blank(R):
    errs = base(R)
    for r in R:
        for c in list(CODE_COLS) + ["evidence_note", "flag_note"]:
            if r[c]:
                errs.append(f"{r['window_id']}: {c} is not blank")
        want = "" if r["dataset"] == "WildChat" else "NA"
        if r["is_research_writing"] != want:
            errs.append(f"{r['window_id']}: is_research_writing should start as {want!r}")
    for path in (SHEET, PAGE):
        t = open(path, "rb").read().decode("utf-8", errors="replace")
        for bad in FORBIDDEN:
            if bad in t:
                errs.append(f"{os.path.basename(path)} contains forbidden token {bad}")
        hits = CODE_TOKEN.findall(t)
        if hits:
            errs.append(f"{os.path.basename(path)} contains code-like tokens: {sorted(set(hits))}")
    return errs


def filled(R):
    errs = base(R)
    for r in R:
        i, cov, ds = r["window_id"], r["coverage"], r["dataset"]
        for c, vals in CODE_COLS.items():
            if r[c] not in vals:
                errs.append(f"{i}: {c}={r[c]!r} is not a valid code")
        if not r["evidence_note"].strip():
            errs.append(f"{i}: evidence_note is empty")
        if ds == "WildChat" and r["is_research_writing"].lower() not in ("yes", "no"):
            errs.append(f"{i}: is_research_writing must be yes or no")
        if ds == "NIRVANA" and r["is_research_writing"] != "NA":
            errs.append(f"{i}: is_research_writing must stay NA")
        if cov == "C0" and (r["verification"] != "VX_UNOBSERVABLE" or r["uptake"] != "UX_NO_TRACE"):
            errs.append(f"{i}: C0 needs VX and UX")
        if cov != "C0" and r["verification"] == "VX_UNOBSERVABLE":
            errs.append(f"{i}: VX is only for C0")
        if cov != "C2" and r["uptake"][:2] in ("U1", "U2", "U3", "U7"):
            errs.append(f"{i}: editor uptake needs C2")
        if r["uptake"].startswith("U8") and r["verification"] != "V0_NONE_VISIBLE":
            errs.append(f"{i}: U8 goes with V0")
        if ds == "NIRVANA" and r["domain"] != "ESSAY_TASK":
            errs.append(f"{i}: NIRVANA domain is ESSAY_TASK")
        if ds == "NIRVANA" and r["prior_own_work"] == "UNOBSERVABLE":
            errs.append(f"{i}: NIRVANA has an editor, so not UNOBSERVABLE")
        if ds == "WildChat" and r["prior_own_work"] == "NONE_VISIBLE":
            errs.append(f"{i}: WildChat has no editor, so not NONE_VISIBLE")
    return errs


def warnings(R):
    """Pairs v1.1's rules make unlikely. A prompt to reread the rule, not a failure, since a rare window may be odd."""
    out = []
    for r in R:
        i, d, u = r["window_id"], r["decision"][:2], r["uptake"][:2]
        if r["coverage"] == "C0" and d in ("D3", "D4"):
            out.append(f"{i}: {d} needs a next action, and C0 has none")
        if d == "D4" and u in ("U3", "U7"):
            out.append(f"{i}: D4 means reuse with no content change, which {u} contradicts")
        if u == "U2" and r["verification"] == "V0_NONE_VISIBLE":
            out.append(f"{i}: U2 means surface edits to AI text, which is V1")
        if d == "D2" and u in ("U1", "U2", "U5", "U6"):
            out.append(f"{i}: D2 means no acceptance or change shown, but {u} shows one (unless the content is not AI-origin)")
    return out


def main():
    R = rows()
    mode_blank = "--blank" in sys.argv
    errs = base(R)
    if not errs or not any("columns differ" in e for e in errs):
        errs = blank(R) if mode_blank else filled(R)
    for e in errs:
        print("PROBLEM", e)
    if not mode_blank and not errs:
        for w in warnings(R):
            print("REREAD", w)
    print(f"{'blank packet' if mode_blank else 'filled sheet'}: {len(R)} rows, {len(errs)} problems")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
