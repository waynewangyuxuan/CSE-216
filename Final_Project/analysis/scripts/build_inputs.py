"""Build the label files Bet 8 feeds to the frozen v1.2 rules, plus per-window flags.

Reads committed v1.1 label files only (codes and ids, no dataset text). Writes:
  results/inputs/labels_final.csv   final labels, three sets: NIRVANA (347), WildChat (Bet 7, 151),
                                    WildChat-Bet4 (Bet 4's 30 sampled windows, incomplete sessions)
  results/inputs/labels_coderA.csv  coder A's labels for the same windows (adjudicator-lean check)
  results/inputs/labels_coderB.csv  coder B's labels
  results/inputs/flags.csv          per-window flags used to filter session measures and sensitivities
Usage: python3 build_inputs.py   (paths are relative to Final_Project/)
"""
import csv, json, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
OUT = os.path.join(ROOT, "analysis", "results", "inputs")
RULE_FIELDS = ["coverage", "prior_own_work", "function", "decision", "verification", "uptake"]
COLS = ["window_id", "dataset", "session_id", "turn"] + RULE_FIELDS


def read(rel, delim=","):
    with open(os.path.join(ROOT, rel), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def row(r, dataset, turn):
    out = {"window_id": r["window_id"], "dataset": dataset, "session_id": r["session_id"], "turn": str(turn)}
    out.update({k: r[k] for k in RULE_FIELDS})
    return out


def turn_of(wid):
    return int(wid.rsplit("-t", 1)[1])


def write(name, rows, cols):
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    os.makedirs(OUT, exist_ok=True)
    nir = read("sessions/results/final_labels_nirvana.csv")
    wc = read("wildchat/results/final_labels_wildchat.csv")
    b4 = [r for r in read("coding/results/final_labels.csv") if r["dataset"] == "WildChat"]
    calib_ids = {r["window_id"] for r in read("coding/results/final_labels.csv")}

    final = ([row(r, "NIRVANA", r["turn_order"]) for r in nir]
             + [row(r, "WildChat", r["turn_order"]) for r in wc]
             + [row(r, "WildChat-Bet4", turn_of(r["window_id"])) for r in b4])
    assert len(final) == 347 + 151 + 30, len(final)
    assert len({r["window_id"] for r in final}) == len(final), "duplicate window ids across sets"
    write("labels_final.csv", final, COLS)

    # Coder A / coder B labels for the same windows (rules applied to each coder alone).
    ab = {}
    for rel, ds in [("sessions/results/labels_ab.csv", "NIRVANA"),
                    ("wildchat/results/labels_ab_wildchat.csv", "WildChat")]:
        for r in read(rel):
            if ds == "NIRVANA" and r["set"] == "bet4_kept":
                continue  # these 52 keep Bet 4 labels; take their A/B from Bet 4 below
            ab[(r["window_id"], r["coder"])] = (r, ds)
    for r in read("coding/results/labels_ab.csv"):
        ds = "NIRVANA" if r["dataset"] == "NIRVANA" else "WildChat-Bet4"
        key = (r["window_id"], r["coder"])
        if ds == "NIRVANA" and key in ab:
            continue  # recoded in Bet 6 with full history; Bet 6's A/B labels are the final ones' source
        ab[key] = (r, ds)
    for coder in "AB":
        rows = []
        for fr in final:
            r, ds = ab[(fr["window_id"], coder)]
            rows.append(row(r, fr["dataset"], fr["turn"]))
        write(f"labels_coder{coder}.csv", rows, COLS)

    # Flags.
    sel = {r["session_id"]: r for r in read("wildchat/results/selected_conversations.tsv", "\t")}
    audit = {}
    with open(os.path.join(ROOT, "wildchat/results/audit_labels.jsonl"), encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            audit[d["hash"][:12]] = d["label"]
    nir_src = {r["window_id"]: r["source"] for r in nir}
    flags = []
    for fr in final:
        wid, ds, sid = fr["window_id"], fr["dataset"], fr["session_id"]
        unsettled = [k for k in ["prior_own_work", "function", "decision", "verification", "uptake", "coverage"]
                     if fr[k] == "UNSETTLED"]
        flags.append({
            "window_id": wid, "dataset": ds, "session_id": sid,
            "in_session_measures": "0" if ds == "WildChat-Bet4" else "1",
            "truncated_session": "1" if ds == "WildChat" and sel[sid]["turns_beyond_cap"] != "0" else "0",
            "auditor_reject": "1" if ds == "WildChat" and audit.get(sid) == "EXCLUDE" else "0",
            "nirvana_source": nir_src.get(wid, ""),
            "in_bet5_calibration": "1" if wid in calib_ids else "0",
            "unsettled_fields": ";".join(unsettled),
        })
    write("flags.csv", flags, list(flags[0]))
    print(f"final {len(final)}; coderA/B {len(final)} each; flags {len(flags)}")


if __name__ == "__main__":
    main()
