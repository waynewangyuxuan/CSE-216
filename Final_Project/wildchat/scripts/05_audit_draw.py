#!/usr/bin/env python
"""Draw the audit sets and the Bet 4 re-judge list. No model. Run after 07_select.py.
 acc_random   ACC_N random screen-accepted unused conversations (key "audit_acc")      -> precision of the accepted pool
 selected     every conversation selected for coding                                     -> precision of the coded sample
 rej_confirm  REJ_N random top-K confirm records the screen did not accept (key "audit_rej") -> what the confirm pass threw away
 unlabeled    UNL_N random eligible unused records no screen label touched (key "audit_unl")  -> positives missed below the cut
 bet4         the WildChat conversations of Bet 4's sample                                -> re-judged against the new definition
The auditor gets one shuffled list and never sees which set a record came from. Writes blind/ids_audit.txt, blind/ids_rejudge.txt,
blind/extra_locations.json (Bet 4 conversations outside the eligible set) and results/audit_sets.tsv."""
import csv, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7
from importlib import import_module

ACC_N, REJ_N, UNL_N = 120, 100, 150


def bet4_conversations():
    sids = set(re.findall(r"WILDCHAT-([0-9a-f]{12})-t", open(os.path.join(w7.DATA, "sample.csv"), encoding="utf-8").read()))
    loc = {}
    with open(os.path.join(w7.DATA, "windows.jsonl"), encoding="utf-8") as f:
        for l in f:
            if '"WildChat"' not in l:
                continue
            w = json.loads(l)
            if w["session_id"] in sids:
                t = w["trace"]
                loc[t["conversation_hash"]] = (os.path.basename(t["file"]), t["row"])
    assert len({h[:12] for h in loc}) == len(sids), (len(loc), len(sids))
    return loc


def main():
    el = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    lab = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.OUT, "screen_labels.jsonl"))}
    acc = import_module("07_select").accepted(lab, el)
    sel = [r["hash"] for r in csv.DictReader(open(os.path.join(w7.OUT, "selected_conversations.tsv")), delimiter="\t")]
    top = [l.split("\t")[0] for l in open(os.path.join(w7.OUT, "rank_confirm.tsv")).read().split("\n")[1:] if l]
    sets = {}
    sets["acc_random"] = sorted((h for h in acc if not el[h]["used"]), key=lambda h: w7.key("audit_acc", h))[:ACC_N]
    sets["selected"] = sel
    sets["rej_confirm"] = sorted((h for h in top if h in lab and h not in acc), key=lambda h: w7.key("audit_rej", h))[:REJ_N]
    sets["unlabeled"] = sorted((h for h, r in el.items() if not r["used"] and h not in lab), key=lambda h: w7.key("audit_unl", h))[:UNL_N]
    b4 = bet4_conversations()
    sets["bet4"] = sorted(b4)
    json.dump({h: v for h, v in b4.items() if h not in el}, open(os.path.join(w7.BLIND, "extra_locations.json"), "w"), indent=1)
    allh = sorted({h for v in sets.values() for h in v}, key=lambda h: w7.key("audit_order", h))
    open(os.path.join(w7.BLIND, "ids_audit.txt"), "w").write("\n".join(allh) + "\n")
    open(os.path.join(w7.BLIND, "ids_rejudge.txt"), "w").write("\n".join(sets["bet4"]) + "\n")
    with open(os.path.join(w7.OUT, "audit_sets.tsv"), "w") as f:
        f.write("hash\tset\n")
        for s, v in sets.items():
            for h in v:
                f.write(f"{h}\t{s}\n")
    print({s: len(v) for s, v in sets.items()}, "distinct", len(allh), "bet4 outside eligible", sum(h not in el for h in b4))


if __name__ == "__main__":
    main()
