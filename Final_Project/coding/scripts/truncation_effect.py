#!/usr/bin/env python3
"""What the 8,000-character cap would have left visible on each window it cuts, against labels. Writes results/truncation_effect.json; prints counts and code labels only, no window text.
Run after final labels exist. On a C2 window, 'matching run' means 30+ characters shared with this response in the text shown."""
import csv, json, os
import bet4
from bet4 import OUT
from overlap import matched
from truncation import cut_span
from views import CAP, _actions_text, load_windows


def short(v):
    return (v or "").split("_")[0]


def main():
    tr = json.load(open(os.path.join(OUT, "truncation.json")))["windows"]
    rows = list(csv.DictReader(open(os.path.join(OUT, "labels_ab.csv"))))
    A = {r["window_id"]: r for r in rows if r["coder"] == "A"}
    B = {r["window_id"]: r for r in rows if r["coder"] == "B"}
    Fin = {r["window_id"]: r for r in csv.DictReader(open(os.path.join(OUT, "final_labels.csv")))}
    ov = {r["window_id"]: r for r in csv.DictReader(open(os.path.join(OUT, "overlap_facts.csv")))}
    at = _actions_text()
    out = {}
    for w in load_windows():
        i = w["window_id"]
        if i not in tr or "next_actions_text" not in tr[i]["cuts"]:
            continue
        t = at(w)
        sp = cut_span(len(t), CAP)
        shown = t[:sp[0]] + "\n" + t[sp[1]:]
        out[i] = {"gold": tr[i]["gold"], "uptake_material": tr[i].get("uptake_material", False), "chars_cut": sp[1] - sp[0], "of": len(t),
                  "match_in_shown": matched(shown, w["response"])[0], "match_in_full": matched(t, w["response"])[0],
                  "overlap_class": ov[i]["class"], "A": short(A[i]["uptake"]), "B": short(B[i]["uptake"]), "final": short(Fin[i]["uptake"]), "final_decision": short(Fin[i]["decision"])}
    with open(os.path.join(OUT, "truncation_effect.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for i, v in sorted(out.items()):
        print(i, v)


if __name__ == "__main__":
    main()
