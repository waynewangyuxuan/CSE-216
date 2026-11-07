#!/usr/bin/env python
"""Build NIRVANA request -> response -> next-action windows (codebook 2.2, 2.3, 10).

Rules. R1 was written after inspecting the raw log's defects, and the reported 347 was known
throughout, so this is not a blind rebuild. The participant sheet's GPT Inquiry column is a separate check on 347, though it may derive from the same log.
 R1 A row is a replay duplicate if the same (essay_num, time, op_type) already appeared in
    that essay; drop it and log it. Then order each essay's rows by time (stable). Essay 69 logs
    the same stretch twice (op_index 82-109 and 82-110) with different numbering, so op_index cannot be the key.
 R2 One window per remaining gpt_inquiry. Its response is the next gpt_response before any
    other gpt_inquiry. No such response, or blank request/response text: coverage CX.
 R3 Next-action span: rows after the response, up to the next gpt_inquiry or the essay end.
    Rows between inquiry and response are kept as ops_during_wait and are never uptake.
 R4 Coverage: C2 if the span holds a text-changing editor op (i, d, d_i, p, x, z, r with
    op_loc=editor). Else C1 if another inquiry follows. Else C0. Cursor, selection and copy
    ops alone are not uptake evidence.
 R5 linkage records how strong C2 is. A text-adding editor op (p, i, d_i) in the span may share
    runs of >=30 characters with this response, on cleaned text, and all typed chunks in the span are
    also joined so typing in pieces can match. verbatim_this_response: some shared run is absent
    from this request, earlier responses and the prior editor text. verbatim_ambiguous: all shared
    runs also appear there. temporal_only: no shared run. A timestamp alone is not proof of cause.
 Usable = coverage in C0/C1/C2.
"""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
import openpyxl

EDIT_OPS = {"i", "d", "d_i", "p", "x", "z", "r"}
MIN_OVERLAP = 30
XLSX = os.path.join(common.RAW, "nirvana", "dataset.xlsx")
PREFIX_SHEET = "Essay Data"


def shingles(text):
    return {text[i:i + MIN_OVERLAP] for i in range(len(text) - MIN_OVERLAP + 1)}


def classify_linkage(added_texts, response, prior_texts):
    """prior_texts: this request, earlier responses, editor text before the request."""
    shared = set()
    target = shingles(response)
    for text in added_texts:
        shared |= shingles(text) & target
    if not shared:
        return "temporal_only"
    return "verbatim_ambiguous" if all(any(run in p for p in prior_texts) for run in shared) else "verbatim_this_response"


def s(v):
    return "" if v is None else str(v)


def first_edit_summary(windows):
    lags = sorted(w["first_edit_latency_sec"] for w in windows if w["first_edit_latency_sec"] is not None)
    return {"median": lags[len(lags) // 2], "over_120": sum(x > 120 for x in lags), "over_300": sum(x > 300 for x in lags), "max": lags[-1]}


def main():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    sheet = list(wb[PREFIX_SHEET].iter_rows(values_only=True))
    head = sheet[0]
    ix = {k: i for i, k in enumerate(head) if k}
    pr = list(wb["Participants"].iter_rows(values_only=True))
    pix = {k: i for i, k in enumerate(pr[0])}
    roster = {int(r[0]): r[pix["GPT Inquiry"]] for r in pr[1:] if r and r[0] is not None}

    width = len(head)
    essays = collections.defaultdict(list)
    malformed = []
    for rownum, r in enumerate(sheet[1:], start=2):
        r = tuple(r) + (None,) * (width - len(r))
        merged = any(isinstance(v, str) and "\t{'t':" in v for v in r)
        if len(sheet[rownum - 1]) < width or any(v is not None for v in r[12:]) or merged:
            malformed.append(rownum)
        essays[int(r[ix["essay_num"]])].append((rownum, r))

    def g(r, k):
        return r[ix[k]]

    dropped, windows = [], []
    for essay in sorted(essays):
        seen, rows = set(), []
        for rownum, r in essays[essay]:
            key = (g(r, "time"), g(r, "op_type"))
            if key in seen:
                dropped.append((essay, rownum, g(r, "op_index"), g(r, "op_type")))
                continue
            seen.add(key)
            rows.append((rownum, r))
        rows.sort(key=lambda item: g(item[1], "time"))
        starts = [i for i, (_, r) in enumerate(rows) if g(r, "op_type") == "gpt_inquiry"]
        for turn, i in enumerate(starts, start=1):
            end = starts[turn] if turn < len(starts) else len(rows)
            resp_i = next((j for j in range(i + 1, end) if g(rows[j][1], "op_type") == "gpt_response"), None)
            rownum, r = rows[i]
            request, response = s(g(r, "selected_text")), ""
            cov, reasons = None, []
            if resp_i is None:
                reasons.append("no_paired_response")
            else:
                response = s(g(rows[resp_i][1], "selected_text"))
                if not response.strip():
                    reasons.append("blank_response")
            if not request.strip():
                reasons.append("blank_request")
            wait = rows[i + 1:resp_i] if resp_i is not None else []
            span = rows[resp_i + 1:end] if resp_i is not None else []
            edits = [(n, x) for n, x in span if g(x, "op_loc") == "editor" and g(x, "op_type") in EDIT_OPS]
            has_next = turn < len(starts)
            if reasons:
                cov = "CX"
            elif edits:
                cov = "C2"
            elif has_next:
                cov = "C1"
            else:
                cov = "C0"
            added = [common.clean_log_text(g(x, "add")) or common.clean_log_text(g(x, "selected_text"))
                     for _, x in edits if g(x, "op_type") in ("p", "i", "d_i")]
            added.append("".join(common.clean_log_text(g(x, "add")) for _, x in edits if g(x, "op_type") == "i"))
            prev_editor = next((s(g(x, "current_editor")) for n, x in reversed(rows[:i]) if g(x, "current_editor") is not None), "")
            earlier = [s(g(x, "selected_text")) for _, x in rows[:i] if g(x, "op_type") == "gpt_response"]
            linkage = classify_linkage(added, response, [request, prev_editor] + earlier) if cov == "C2" else None
            def op(n, x):
                return {"sheet_row": n, "op_index": g(x, "op_index"), "time": g(x, "time"), "op_loc": g(x, "op_loc"),
                        "op_type": g(x, "op_type"), "add": s(g(x, "add")), "delete": s(g(x, "delete")),
                        "selected_text": s(g(x, "selected_text")) if g(x, "op_type") in ("y", "l", "p") else "",
                        "malformed_row": n in set(malformed)}
            resp_row = rows[resp_i][0] if resp_i is not None else None
            last_editor = next((s(g(x, "current_editor")) for n, x in reversed(span) if g(x, "current_editor") is not None), prev_editor)
            words = len(request.split())
            windows.append({
                "window_id": f"NIRVANA-e{essay:02d}-t{turn:02d}",
                "dataset": "NIRVANA", "session_id": f"e{essay:02d}", "participant_id": f"e{essay:02d}",
                "domain": "ESSAY_TASK", "episode_id": None, "turn_order": turn,
                "previous_window_id": f"NIRVANA-e{essay:02d}-t{turn - 1:02d}" if turn > 1 else None,
                "coverage": cov, "cx_reasons": reasons, "linkage": linkage,
                "request": request, "response": response,
                "next_user_request_follows": has_next,
                "next_actions": [op(n, x) for n, x in span],
                "ops_during_wait": [op(n, x) for n, x in wait],
                "editor_before_request": prev_editor, "editor_after_next_actions": last_editor,
                "very_short_request": words <= 2,
                "response_time": g(rows[resp_i][1], "time") if resp_i is not None else None,
                "first_edit_latency_sec": round(g(edits[0][1], "time") - g(rows[resp_i][1], "time"), 3) if edits else None,
                "trace": {"file": "raw/nirvana/dataset.xlsx", "sheet": PREFIX_SHEET, "essay_num": essay,
                          "request_row": rownum, "response_row": resp_row, "request_op_index": g(r, "op_index")},
            })
    os.makedirs(common.WORK, exist_ok=True)
    common.write_jsonl(os.path.join(common.WORK, "nirvana_windows.jsonl"), windows)

    cov = collections.Counter(w["coverage"] for w in windows)
    per = collections.Counter(w["session_id"] for w in windows)
    in_log = collections.Counter(int(w["session_id"][1:]) for w in windows)
    stats = {
        "sheet_data_rows": len(sheet) - 1, "essays_in_log": len(essays), "roster_participants": len(roster),
        "raw_gpt_inquiry_rows": sum(1 for L in essays.values() for _, r in L if g(r, "op_type") == "gpt_inquiry"),
        "duplicate_rows_dropped": len(dropped),
        "duplicate_rows_by_essay": dict(collections.Counter(str(d[0]) for d in dropped)),
        "duplicate_gpt_inquiry_rows": sum(1 for d in dropped if d[3] == "gpt_inquiry"),
        "malformed_sheet_rows": malformed,
        "windows_total": len(windows), "coverage": dict(sorted(cov.items())),
        "windows_usable": sum(v for k, v in cov.items() if k != "CX"),
        "students_with_windows": len(per),
        "students_with_no_inquiry": sorted(e for e in essays if e not in in_log),
        "roster_inquiry_sum": sum(float(v or 0) for v in roster.values()),
        "roster_vs_log_mismatch_after_dedup": sorted(e for e in roster if float(roster[e] or 0) != in_log.get(e, 0)),
        "windows_per_student_sorted": sorted(per.values()),
        "linkage": dict(sorted(collections.Counter(w["linkage"] for w in windows if w["linkage"]).items())),
        "very_short_requests": sum(w["very_short_request"] for w in windows),
        "windows_with_ops_during_wait": sum(1 for w in windows if w["ops_during_wait"]),
        "repeat_request_text_same_student": len(windows) - len({(w["session_id"], w["request"]) for w in windows}),
        "windows_touching_malformed_rows": sorted(w["window_id"] for w in windows if any(o["malformed_row"] for o in w["next_actions"] + w["ops_during_wait"])),
        "first_edit_latency_sec": first_edit_summary(windows),
        "essays_past_30min_by_last_log_time": sum(1 for L in essays.values() if max(g(r, "time") for _, r in L) > 1800),
        "longest_last_log_time_sec": max(g(r, "time") for L in essays.values() for _, r in L),
        "essays_past_30min_by_sheet_total_time": sum(1 for r in pr[1:] if r and r[0] is not None and float(r[pix["Total Time"]] or 0) > 1800),
        "sha256": common.sha256_file(XLSX),
    }
    json.dump(stats, open(os.path.join(common.WORK, "nirvana_stats.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in stats.items() if k != "windows_per_student_sorted"}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
