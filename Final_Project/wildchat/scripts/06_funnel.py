#!/usr/bin/env python
"""Funnel, precision and rough recall of the Bet 7 screen, from cached labels only. No model. AI judgment throughout: no human checked any label.
Precision = share of audited accepted records the auditor (claude-opus-5-5, own prompt, blind to screen labels) also calls INCLUDE.
Strict counts the auditor's UNSURE as a miss; lenient leaves UNSURE out.
Rough recall = estimated true positives found / (found + estimated positives among labelled rejects + among never-labelled records).
Writes results/funnel.json. Needs results/ only (blind/eligible.jsonl for the follow-up rule and pool sizes)."""
import collections, csv, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w7
from importlib import import_module


def wilson(x, n, z=1.96):
    if not n:
        return None
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def share(labs, want="INCLUDE"):
    c = collections.Counter(labs)
    n, x = len(labs), c[want]
    nl = n - c["UNSURE"]
    return {"n": n, "include": x, "unsure": c["UNSURE"], "exclude": c["EXCLUDE"], "strict": round(x / n, 3) if n else None, "strict_ci": wilson(x, n),
            "lenient": round(x / nl, 3) if nl else None, "lenient_ci": wilson(x, nl)}


def kappa(a, b):
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n ** 2
    return round((po - pe) / (1 - pe), 2) if pe < 1 else None


def ids(p):
    return [l.split("\t")[0] for l in open(p).read().split("\n")[1:] if l]


def main():
    el = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.BLIND, "eligible.jsonl"))}
    lab = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.OUT, "screen_labels.jsonl"))}
    aud = {r["hash"]: r for r in w7.read_jsonl(os.path.join(w7.OUT, "audit_labels.jsonl"))}
    acc = import_module("07_select").accepted(lab, el)
    seed = list(csv.DictReader(open(os.path.join(w7.OUT, "seed_ids.tsv")), delimiter="\t"))
    enrich = ids(os.path.join(w7.OUT, "rank_enrich.tsv"))
    top = ids(os.path.join(w7.OUT, "rank_confirm.tsv"))
    sets = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(w7.OUT, "audit_sets.tsv")), delimiter="\t"):
        sets[r["set"]].append(r["hash"])
    f = json.load(open(os.path.join(w7.OUT, "funnel_eligible.json")))
    unused = [h for h, r in el.items() if not r["used"]]
    labelled_unused = [h for h in unused if h in lab]
    out = {"note": "AI judgment only. No human checked any label.", "eligibility": f}
    sl = [lab[r["hash"]]["label"] for r in seed]
    out["seed"] = {"n": len(seed), "labels": dict(collections.Counter(sl)), "include_share": round(sl.count("INCLUDE") / len(sl), 3), "include_ci": wilson(sl.count("INCLUDE"), len(sl)),
                   "accepted_followup_rule": sum(r["hash"] in acc for r in seed),
                   "genre_of_include": dict(collections.Counter(lab[r["hash"]]["genre"] for r in seed if lab[r["hash"]]["label"] == "INCLUDE").most_common())}
    out["enrich"] = {"n": len(enrich), "labels": dict(collections.Counter(lab[h]["label"] for h in enrich if h in lab))}
    out["confirm"] = {"k": len(top), "already_labelled_in_seed_or_enrich": sum(1 for h in top if h in {r["hash"] for r in seed} or h in set(enrich)),
                      "labels": dict(collections.Counter(lab[h]["label"] for h in top if h in lab)), "accepted": sum(h in acc for h in top),
                      "rank_meta": json.load(open(os.path.join(w7.OUT, "rank_confirm_meta.json")))}
    out["confirm"]["rank_meta"].pop("test_include_ranks", None)
    out["pool"] = {"labelled_unused": len(labelled_unused), "accepted_unused": sum(1 for h in acc if not el[h]["used"]),
                   "accepted_unused_by_source": {"seed": sum(1 for r in seed if r["hash"] in acc), "enrich_only": sum(1 for h in enrich if h in acc),
                                                 "confirm_only": sum(1 for h in top if h in acc and h not in set(enrich) and h not in {r["hash"] for r in seed})},
                   "accepted_genre": dict(collections.Counter(lab[h]["genre"] for h in acc if not el[h]["used"]).most_common()),
                   "never_labelled_unused": len(unused) - len(labelled_unused)}
    sel = list(csv.DictReader(open(os.path.join(w7.OUT, "selected_conversations.tsv")), delimiter="\t"))
    win = list(csv.DictReader(open(os.path.join(w7.OUT, "windows_wildchat.csv"))))
    out["sample"] = {"conversations": len(sel), "windows": len(win), "coded": sum(w["coded"] == "1" for w in win),
                     "coverage": dict(collections.Counter(w["coverage"] for w in win)), "turns_beyond_cap": sum(int(c["turns_beyond_cap"]) for c in sel),
                     "user_turns_median": sorted(int(c["user_turns"]) for c in sel)[len(sel) // 2], "genre": dict(collections.Counter(c["genre"] for c in sel).most_common())}
    au = {s: share([aud[h]["label"] for h in v if h in aud]) | {"missing": sum(h not in aud for h in v)} for s, v in sets.items()}
    out["audit"] = au
    p = au["acc_random"]
    tp = p["strict"] * out["pool"]["accepted_unused"]
    rej = len(labelled_unused) - out["pool"]["accepted_unused"]
    miss_rej = au["rej_confirm"]["strict"] * rej
    miss_unl = au["unlabeled"]["strict"] * out["pool"]["never_labelled_unused"]
    out["recall_rough"] = {"true_found_est": round(tp), "labelled_rejects": rej, "missed_in_rejects_est": round(miss_rej),
                           "never_labelled": out["pool"]["never_labelled_unused"], "missed_unlabelled_est": round(miss_unl),
                           "recall_est": round(tp / (tp + miss_rej + miss_unl), 3),
                           "caveat": "Reject rate measured on top-K rejects is applied to all labelled rejects; unlabelled rate rests on a small sample. Rough only.",
                           "seed_test_half_in_top_k": f'{out["confirm"]["rank_meta"]["test_include_in_top_k"]} of {out["confirm"]["rank_meta"]["test_include"]}'}
    both = [h for h in aud if h in lab]
    out["screen_vs_audit"] = {"n": len(both), "agree_pct": round(100 * sum(lab[h]["label"] == aud[h]["label"] for h in both) / len(both), 1),
                              "kappa_3way": kappa([lab[h]["label"] for h in both], [aud[h]["label"] for h in both]),
                              "table": dict(collections.Counter(f'{lab[h]["label"]}|{aud[h]["label"]}' for h in both))}
    # Bet 1 cached labels vs new screen labels, on the random draw overlap (W04)
    old = {r["hash"]: r["label"] for r in w7.read_jsonl(os.path.join(w7.DATA, "wildchat_llm_screen.jsonl"))}
    ov = [r["hash"] for r in seed if r["from_draw2000"] == "1" and r["hash"] in old]
    out["bet1_vs_new_on_draw"] = {"n": len(ov), "table": dict(collections.Counter(f'{old[h]}|{lab[h]["label"]}' for h in ov).most_common())}
    # Bet 4 re-judge (labels not changed)
    b4 = sets["bet4"]
    out["bet4_rejudge"] = {"conversations": len(b4), "screen": dict(collections.Counter(lab[h]["label"] for h in b4 if h in lab)),
                           "audit": dict(collections.Counter(aud[h]["label"] for h in b4 if h in aud)),
                           "per_conversation": {h[:12]: {"screen": lab.get(h, {}).get("label"), "screen_genre": lab.get(h, {}).get("genre"),
                                                         "audit": aud.get(h, {}).get("label"), "audit_genre": aud.get(h, {}).get("genre")} for h in sorted(b4)}}
    json.dump(out, open(os.path.join(w7.OUT, "funnel.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("seed", "pool", "audit", "recall_rough", "screen_vs_audit", "bet4_rejudge")}, indent=1)[:6000])


if __name__ == "__main__":
    main()
