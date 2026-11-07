#!/usr/bin/env python3
"""Build the C3 packet: a blank sheet and a reading page for the 20 gold windows. Never prints window text.
No LLM label, linkage, or coder label reaches either file: views are whitelisted in views.py."""
import csv, html, json, os, shutil
from codes import ID_COLS, SHEET_COLS
from views import CODEBOOK, DATA, make_views

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>C3 gold windows</title><style>
body{{font:15px/1.5 -apple-system,sans-serif;max-width:900px;margin:24px auto;padding:0 16px;color:#222;background:#fff}}
h2{{margin-top:40px;border-top:3px solid #333;padding-top:12px}}h3{{margin:18px 0 4px;font-size:14px;color:#555;text-transform:uppercase;letter-spacing:.04em}}
pre{{white-space:pre-wrap;word-wrap:break-word;background:#f6f6f4;padding:10px;border-radius:4px;font:13px/1.45 ui-monospace,monospace;max-height:420px;overflow:auto}}
details{{margin:12px 0}}summary{{cursor:pointer;color:#333;font-weight:600}}.m{{color:#555}}nav a{{margin-right:8px}}</style></head><body><h1>C3 gold windows</h1>
<p>Code each window in <code>c3_gold_sheet.csv</code>. No AI label appears here or in the sheet.</p><nav>{nav}</nav>{body}</body></html>"""


def block(title, text):
    return f"<h3>{html.escape(title)}</h3><pre>{html.escape(text or '(none)')}</pre>"


def fold(title, text):
    """Context stays one click away, so it does not cost reading time unless it is needed."""
    return f"<details><summary>{html.escape(title)}</summary><pre>{html.escape(text or '(none)')}</pre></details>"


def has_human_labels(path):
    if not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ("utf-8-sig", "cp1252", "mac_roman"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    keep = set(ID_COLS) | {"is_research_writing"}
    for r in csv.DictReader(text.splitlines()):
        if any((v or "").strip() for k, v in r.items() if k not in keep):
            return True
        if (r.get("is_research_writing") or "").strip().lower() in ("yes", "no"):
            return True
    return False


def main():
    with open(os.path.join(DATA, "gold.csv"), encoding="utf-8", newline="") as f:
        gold = list(csv.DictReader(f))
    assert len(gold) == 20
    views = make_views({g["window_id"] for g in gold})
    sheet = os.path.join(CODEBOOK, "c3_gold_sheet.csv")
    if has_human_labels(sheet):  # the sheet is git-excluded with no backup, so never overwrite a filled one
        os.makedirs(os.path.join(CODEBOOK, "pilot"), exist_ok=True)
        shutil.copyfile(sheet, os.path.join(CODEBOOK, "pilot", "c3_sheet_backup.csv"))
        print("sheet already holds human labels: left untouched, copy in pilot/c3_sheet_backup.csv")
    else:
        with open(sheet, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, SHEET_COLS, lineterminator="\n")
            w.writeheader()
            for g in gold:
                w.writerow({**{k: g[k] for k in ID_COLS}, "is_research_writing": "" if g["dataset"] == "WildChat" else "NA"})
    body, nav, cut, same = [], [], 0, 0
    for g in gold:
        v = views[g["window_id"]]
        same += (v["request"] == g["request"] or "characters cut" in v["request"]) and (v["next_actions_text"] == g["next_actions_text"] or "characters cut" in v["next_actions_text"])
        cut += any("characters cut from this view" in (v[k] or "") for k in ("request", "response", "next_actions_text", "editor_before_request"))
        prior = "\n\n".join(f"[turn {p['turn']}] WRITER: {p['request']}\n[turn {p['turn']}] AI: {p['response']}" for p in v["prior_turns"])
        parts = [f'<h2 id="w{g["gold_order"]}">Window {g["gold_order"]} of 20</h2><p class="m">{html.escape(g["window_id"])} · {html.escape(g["dataset"])} · coverage {html.escape(g["coverage"])} · turn {v["turn_order"]}</p>']
        if prior:
            parts.append(fold("Earlier turns: open for context (each cut to 500 characters)", prior))
        if g["dataset"] == "NIRVANA":
            parts.append(fold("Editor just before this request: open for prior_own_work", v["editor_before_request"]))
        parts += [block("Request", v["request"]), block("AI response", v["response"]), block("What happened next", v["next_actions_text"])]
        body.append("".join(parts))
        nav.append(f'<a href="#w{g["gold_order"]}">{g["gold_order"]}</a>')
    with open(os.path.join(CODEBOOK, "c3_gold_windows.html"), "w", encoding="utf-8") as f:
        f.write(PAGE.format(nav="".join(nav), body="".join(body)))
    words = {k: sum(len((views[g["window_id"]][k] or "").split()) for g in gold) for k in ("request", "response", "next_actions_text", "editor_before_request")}
    words["prior_turns"] = sum(len(json.dumps(views[g["window_id"]]["prior_turns"]).split()) for g in gold)
    print("words by block:", words)
    print(f"sheet 20 rows, page 20 windows; views match gold.csv: {same}/20; windows with a cut block: {cut}")


if __name__ == "__main__":
    main()
