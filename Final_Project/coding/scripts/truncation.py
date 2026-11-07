#!/usr/bin/env python3
"""Measure what the codebook's standard view cap (views.CAP, views.PRIOR_CAP) cuts across the sample, and what evidence the cut text holds.
Prints and writes counts only, never window text. Writes results/truncation.json.
A cut block is "uptake-material" if the text cut from next_actions_text holds any of:
  (a) an editor line (typed, deleted, pasted, cut, replaced) with 30+ characters of text, or any deletion or replacement, after a paste that matches this response;
  (b) a 30+ character run shared with this response.
Either can change U1/U2/U3/U7 (or a D4/D3 share)."""
import json, os, re, sys
import bet4
from bet4 import OUT, ids_of
from views import CAP, PRIOR_CAP, PRIOR_TURNS, _actions_text, editor_text, load_windows, norm
from overlap import facts, matched

LINE = re.compile(r"^\d+s after response, (editor|chatbot|other|\w+) (typed|deleted|pasted|copied|cut|replaced|undo|dragged)", re.M)
NEXT = "NEXT REQUEST TO AI: "


def cut_span(n, cap):
    """Same arithmetic as views.cap: head 75%, tail 25%."""
    return (int(cap * .75), n - int(cap * .25)) if n > cap else None


def hidden_events(text, span):
    """Editor events whose line intersects the cut."""
    marks = [m.start() for m in LINE.finditer(text)]
    ends = marks[1:] + [text.find(NEXT) if NEXT in text else len(text)]
    out = {"lines": 0, "typed": 0, "deleted": 0, "pasted": 0, "replaced": 0, "cut": 0, "copied": 0, "other": 0, "chars_del_or_rep": 0}
    for s, e in zip(marks, ends):
        if e <= span[0] or s >= span[1]:
            continue
        kind = LINE.match(text, s).group(2)
        out["lines"] += 1
        out[kind if kind in out else "other"] += 1
        if kind in ("deleted", "replaced", "cut"):
            out["chars_del_or_rep"] += e - s
    return out


def main():
    sample, gold = set(ids_of("sample.csv")), set(ids_of("gold.csv"))
    at = _actions_text()
    rows = load_windows()
    by = {}
    for w in rows:
        by.setdefault((w["dataset"], w["session_id"]), []).append(w)
    for v in by.values():
        v.sort(key=lambda x: x["turn_order"])
    res = {"cap_block": CAP, "cap_prior": PRIOR_CAP, "fields": {}, "windows": {}, "prior": {}}
    f_stat = {k: {"blocks_cut": 0, "chars_cut": 0, "max_cut": 0, "gold_blocks_cut": 0} for k in ("request", "response", "next_actions_text", "editor_before_request")}
    prior_cut = prior_cut_gold = prior_cut_chars = prior_blocks = 0
    prior_hides_request_run = []
    total_prior = {500: 0, 2000: 0, None: 0}
    for w in rows:
        i = w["window_id"]
        if i not in sample:
            continue
        text = {"request": w["request"], "response": w["response"], "next_actions_text": at(w),
                "editor_before_request": (editor_text(w) if w["dataset"] == "NIRVANA" else "") or ""}
        rec = {"dataset": w["dataset"], "coverage": w["coverage"], "gold": i in gold, "cuts": {}}
        for k, t in text.items():
            sp = cut_span(len(t or ""), CAP)
            if not sp:
                continue
            c = sp[1] - sp[0]
            s = f_stat[k]
            s["blocks_cut"] += 1
            s["chars_cut"] += c
            s["max_cut"] = max(s["max_cut"], c)
            s["gold_blocks_cut"] += i in gold
            rec["cuts"][k] = {"chars": c, "of": len(t)}
            if k == "next_actions_text":
                hid = t[sp[0]:sp[1]]
                ev = hidden_events(t, sp)
                pm, _ = matched(hid, w["response"])
                f = facts(w)
                rec["cuts"][k].update({"events_in_cut": ev, "cut_chars_matching_response": pm, "next_request_visible": (NEXT not in t) or t.rfind(NEXT) >= sp[1],
                                       "overlap_class": f["class"], "typed_after_paste": f["typed_after_paste"], "deleted_after_paste": f["deleted_after_paste"]})
                rec["uptake_material"] = bool(pm >= 30 or ((f["class"].startswith("PASTE_MATCH")) and (ev["deleted"] + ev["replaced"] + ev["cut"] or ev["typed"])) or ev["pasted"])
        # Earlier turns: cut at PRIOR_CAP. Can the cut hide that this request reuses earlier AI text (own work vs AI text)?
        earlier = [x for x in by[(w["dataset"], w["session_id"])] if x["turn_order"] < w["turn_order"]][-PRIOR_TURNS:]
        for x in earlier:
            for k in ("request", "response"):
                n = len(x[k] or "")
                prior_blocks += 1
                for cp in total_prior:
                    total_prior[cp] += min(n, cp) if cp else n
                sp = cut_span(n, PRIOR_CAP)
                if sp:
                    prior_cut += 1
                    prior_cut_gold += i in gold
                    prior_cut_chars += sp[1] - sp[0]
                    if k == "response" and matched(w["request"], x[k][sp[0]:sp[1]])[0] >= 30:
                        prior_hides_request_run.append(i)
        if rec["cuts"]:
            res["windows"][i] = rec
    res["fields"] = f_stat
    res["prior"] = {"blocks": prior_blocks, "blocks_cut": prior_cut, "gold_blocks_cut": prior_cut_gold, "chars_cut": prior_cut_chars,
                    "total_chars_by_cap": {str(k): v for k, v in total_prior.items()},
                    "windows_whose_request_reuses_cut_earlier_ai_text": sorted(set(prior_hides_request_run))}
    res["summary"] = {"windows_with_main_block_cut": len(res["windows"]), "gold_windows_with_main_block_cut": sum(v["gold"] for v in res["windows"].values()),
                      "uptake_material_windows": sorted(i for i, v in res["windows"].items() if v.get("uptake_material")),
                      "gold_uptake_material_windows": sorted(i for i, v in res["windows"].items() if v.get("uptake_material") and v["gold"]),
                      "gold_blocks_cut_on_page": sum(s["gold_blocks_cut"] for s in f_stat.values()) + prior_cut_gold}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "truncation.json"), "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    print(json.dumps({"fields": res["fields"], "prior": res["prior"], "summary": res["summary"]}, indent=1))
    for i, v in sorted(res["windows"].items()):
        print(i, "gold" if v["gold"] else "", v["coverage"], json.dumps(v["cuts"]), v.get("uptake_material"))


if __name__ == "__main__":
    main()
