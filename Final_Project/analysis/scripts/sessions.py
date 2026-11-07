"""Step 2: session measures (v1.2 s9.5) and the order questions, for whole sessions only
(NIRVANA 71 + WildChat Bet 7 35; the 30 Bet 4 WildChat windows are incomplete samples and excluded).
Windows from one session are clustered: counts are reported per session where possible.
Writes results/sessions/*.csv, results/sessions.json, results/sessions.md."""
import json, os, random
from collections import Counter
from common import (CATS, SL, OF, AU, NE, IN, SHORT, SUPPORT, RES, load_windows, sessions, md_table, pct,
                    write_csv, write_json, write_text)

SEED, PERMS = 216, 2000


def seq_of(ws):
    return [w["category"] for w in ws]


def transitions(seqs, drop=()):
    t = Counter()
    for s in seqs:
        s = [c for c in s if c not in drop]
        t.update(zip(s, s[1:]))
    return t


def matrix_rows(t, cats):
    rows = []
    for a in cats:
        tot = sum(t[(a, b)] for b in cats)
        rows.append([SHORT[a]] + [f"{t[(a, b)]}" + (f" ({100 * t[(a, b)] / tot:.0f}%)" if tot else "") for b in cats] + [tot])
    return rows


def perm_test(seqs, pairs, drop=(), seed=SEED, n=PERMS):
    """Shuffle categories within each session (keeps each session's composition); count each pair."""
    rng = random.Random(seed)
    obs = transitions(seqs, drop)
    ge = Counter()
    tot = {p: 0 for p in pairs}
    for _ in range(n):
        sh = []
        for s in seqs:
            s = list(s)
            rng.shuffle(s)
            sh.append(s)
        t = transitions(sh, drop)
        for p in pairs:
            tot[p] += t[p]
            ge[p] += t[p] >= obs[p]
    return {f"{SHORT[a]}->{SHORT[b]}": {"observed": obs[(a, b)], "expected": round(tot[(a, b)] / n, 1),
                                        "p_ge": round((ge[(a, b)] + 1) / (n + 1), 4)} for a, b in pairs}


def d1_then_d4(D):
    i = next((j for j, d in enumerate(D) if d == "D1"), None)
    return i is not None and "D4" in D[i + 1:]


def escalation_shuffle(S, seed=SEED, n=PERMS):
    """D1-then-D4 sessions observed vs with each session's decision codes shuffled; also the reverse order."""
    rng = random.Random(seed)
    Ds = [[w["D"] for w in v] for v in S.values()]
    obs = sum(d1_then_d4(D) for D in Ds)
    tot = ge = 0
    for _ in range(n):
        c = 0
        for D in Ds:
            D = list(D)
            rng.shuffle(D)
            c += d1_then_d4(D)
        tot += c
        ge += c >= obs
    rev = sum(1 for D in Ds if "D4" in D and "D1" in D[D.index("D4") + 1:])
    return {"observed": obs, "shuffled_mean": round(tot / n, 2), "p_ge": round((ge + 1) / (n + 1), 4), "reverse_observed": rev}


def drift_test(S, seed=SEED, n=PERMS):
    """Mean relative position i/(len-1) of selected windows vs within-session shuffles (sessions with 2+ windows)."""
    tests = {"SL": lambda w: w["category"] == SL,
             "SL not R16": lambda w: w["category"] == SL and w["rule"] != "R16",
             "SL by R16": lambda w: w["category"] == SL and w["rule"] == "R16",
             "Support (OFF+AUG)": lambda w: w["category"] in SUPPORT}
    seqs = [v for v in S.values() if len(v) >= 2]
    out = {}
    for name, t in tests.items():
        def mean(ss):
            xs = [i / (len(s) - 1) for s in ss for i, w in enumerate(s) if t(w)]
            return (sum(xs) / len(xs), len(xs)) if xs else (None, 0)
        obs, k = mean(seqs)
        if not k:
            continue
        rng = random.Random(seed)
        hi = lo = 0
        tot = 0.0
        for _ in range(n):
            e, _ = mean([rng.sample(s, len(s)) for s in seqs])
            tot += e
            hi += e >= obs
            lo += e <= obs
        out[name] = {"n": k, "observed": round(obs, 3), "expected": round(tot / n, 3),
                     "p_later": round((hi + 1) / (n + 1), 4), "p_earlier": round((lo + 1) / (n + 1), 4)}
    return out


def switches_sl_support(s):
    """1 if the session has an adjacent SL<->support pair once IND and NEU windows are removed."""
    k = [c for c in s if c not in (IN, NE)]
    return int(any((a == SL and b in SUPPORT) or (a in SUPPORT and b == SL) for a, b in zip(k, k[1:])))


def session_row(key, ws):
    ds, sid = key
    s = seq_of(ws)
    det = [c for c in s if c != IN]
    n = len(s)
    first_sl = next((i for i, c in enumerate(s) if c == SL), None)
    after = s[first_sl + 1:] if first_sl is not None else []
    runs, cur = [], 0
    for c in s:
        cur = cur + 1 if c == SL else 0
        runs.append(cur)
    Ds = [w["D"] for w in ws]
    first_d1 = next((i for i, d in enumerate(Ds) if d == "D1"), None)
    esc_d = first_d1 is not None and any(d == "D4" for d in Ds[first_d1 + 1:])
    first_sup = next((i for i, c in enumerate(s) if c in SUPPORT), None)
    return {
        "dataset": ds, "session_id": sid, "n_windows": n,
        "sequence": " ".join(SHORT[c] for c in s),
        "strengths": " ".join(w["strength"] for w in ws),
        "decisions": " ".join(Ds),
        "switches": sum(a != b for a, b in zip(s, s[1:])),
        "switches_excl_ind": sum(a != b for a, b in zip(det, det[1:])),
        **{f"n_{SHORT[c]}": s.count(c) for c in CATS},
        "first_category": SHORT[s[0]],
        "first_determinate": SHORT[det[0]] if det else "none",
        "first_sl_index": "" if first_sl is None else first_sl + 1,
        "first_sl_relative": "" if first_sl is None else (round(first_sl / (n - 1), 3) if n > 1 else 0.0),
        "has_sl": int(first_sl is not None),
        "has_support": int(first_sup is not None),
        "support_before_sl": int(first_sl is not None and first_sup is not None and first_sup < first_sl),
        "sl_before_support": int(first_sl is not None and first_sup is not None and first_sl < first_sup),
        "leaves_sl_to_support": "" if first_sl is None else int(any(c in SUPPORT for c in after)),
        "leaves_sl_any": "" if first_sl is None else int(any(c not in (SL, IN) for c in after)),
        "sl_has_later_window": "" if first_sl is None else int(bool(after)),
        "ends_in_sl": int(bool(det) and det[-1] == SL),
        "max_sl_run": max(runs) if runs else 0,
        "escalation_d1_to_d4": int(esc_d),
        "truncated_session": ws[0]["truncated_session"], "auditor_reject": ws[0]["auditor_reject"],
    }


def analyse(S, tag):
    """All session measures for one session dict; returns (json, markdown, table rows)."""
    rows = [session_row(k, v) for k, v in S.items()]
    seqs = [seq_of(v) for v in S.values()]
    n_s, n_w = len(rows), sum(r["n_windows"] for r in rows)
    J = {"n_sessions": n_s, "n_windows": n_w}
    t_all, t_det = transitions(seqs), transitions(seqs, drop=(IN,))
    J["transitions"] = {f"{SHORT[a]}->{SHORT[b]}": t_all[(a, b)] for a in CATS for b in CATS}
    J["transitions_excl_ind"] = {f"{SHORT[a]}->{SHORT[b]}": t_det[(a, b)] for a in CATS[:4] for b in CATS[:4]}
    J["perm_test"] = perm_test(seqs, [(SL, SL), (OF, OF), (AU, AU), (SL, OF), (OF, SL), (SL, AU), (AU, SL)])
    J["shares_window_weighted"] = {SHORT[c]: round(sum(s.count(c) for s in seqs) / n_w, 3) for c in CATS}
    J["shares_session_weighted"] = {SHORT[c]: round(sum(s.count(c) / len(s) for s in seqs) / n_s, 3) for c in CATS}
    PAIRS = [(SL, SL), (OF, OF), (AU, AU), (SL, OF), (OF, SL), (SL, AU), (AU, SL)]
    J["perm_test_excl_ind"] = perm_test(seqs, PAIRS, drop=(IN,))
    # Where IND windows sit: the shuffle with IND kept moves closing-turn IND windows into SL runs.
    J["ind_windows"] = sum(s.count(IN) for s in seqs)
    J["ind_is_last_window"] = sum(1 for s in seqs if s[-1] == IN)
    J["sessions_with"] = {SHORT[c]: sum(r[f"n_{SHORT[c]}"] > 0 for r in rows) for c in CATS}
    J["first_window"] = dict(Counter(r["first_category"] for r in rows))
    J["first_determinate"] = dict(Counter(r["first_determinate"] for r in rows))
    sl_rows = [r for r in rows if r["has_sl"]]
    sl_later = [r for r in sl_rows if r["sl_has_later_window"]]
    both = [r for r in rows if r["has_sl"] and r["has_support"]]
    J.update({
        "sessions_with_sl": len(sl_rows),
        "sl_sessions_with_later_window": len(sl_later),
        "leaves_sl_to_support": sum(r["leaves_sl_to_support"] for r in sl_later),
        "leaves_sl_any": sum(r["leaves_sl_any"] for r in sl_later),
        "ends_in_sl": sum(r["ends_in_sl"] for r in rows),
        "sessions_with_sl_and_support": len(both),
        "support_first": sum(r["support_before_sl"] for r in both),
        "sl_first": sum(r["sl_before_support"] for r in both),
        "escalation_d1_to_d4": sum(r["escalation_d1_to_d4"] for r in rows),
        "switches_mean": round(sum(r["switches"] for r in rows) / n_s, 2),
        "switches_excl_ind_mean": round(sum(r["switches_excl_ind"] for r in rows) / n_s, 2),
        "first_sl_relative": sorted(r["first_sl_relative"] for r in sl_rows if r["n_windows"] > 1),
        "max_sl_run": dict(sorted(Counter(r["max_sl_run"] for r in rows).items())),
        "n_windows_dist": dict(sorted(Counter(r["n_windows"] for r in rows).items())),
    })
    # What follows / precedes a surrender-leaning window (adjacent, IND kept and dropped).
    J["after_sl"] = {SHORT[b]: t_all[(SL, b)] for b in CATS}
    J["before_sl"] = {SHORT[a]: t_all[(a, SL)] for a in CATS}
    J["after_sl_excl_ind"] = {SHORT[b]: t_det[(SL, b)] for b in CATS[:4]}
    # Category share by relative position (sessions with >= 3 windows), 5 centred bins, so the last
    # window of a short session lands in the last fifth. SL is also split into R16 and not-R16.
    pos = {k: [0] * 5 for k in [SHORT[c] for c in CATS] + ["SL_R16", "SL_not_R16"]}
    for v in S.values():
        if len(v) >= 3:
            for i, w in enumerate(v):
                b = min(4, int(5 * (i + 0.5) / len(v)))
                pos[SHORT[w["category"]]][b] += 1
                if w["category"] == SL:
                    pos["SL_R16" if w["rule"] == "R16" else "SL_not_R16"][b] += 1
    J["position_bins"] = pos
    J["drift"] = drift_test(S)
    J["first_sl_rule"] = dict(Counter(next(w["rule"] for w in v if w["category"] == SL) for v in S.values()
                                      if any(w["category"] == SL for w in v)))
    J["escalation_shuffle"] = escalation_shuffle(S)
    # O<->S switching, adjacent after dropping IND and NEU (support side vs SL only).
    so = transitions(seqs, drop=(IN, NE))
    J["support_sl_switch"] = {"SL->support": so[(SL, OF)] + so[(SL, AU)], "support->SL": so[(OF, SL)] + so[(AU, SL)],
                              "SL->SL": so[(SL, SL)], "support->support": sum(so[(a, b)] for a in SUPPORT for b in SUPPORT)}
    J["sessions_switching_sl_support"] = sum(switches_sl_support(s) for s in seqs)

    md = [f"\n### {tag}: {n_s} sessions, {n_w} windows\n\n",
          "**Transition counts, all categories** (row = from, column = to; row % in brackets)\n\n",
          md_table(["from \\ to"] + [SHORT[c] for c in CATS] + ["total"], matrix_rows(t_all, CATS)),
          "\n**Transition counts, `INDETERMINATE` windows removed first**\n\n",
          md_table(["from \\ to"] + [SHORT[c] for c in CATS[:4]] + ["total"], matrix_rows(t_det, CATS[:4])),
          "\n**Within-session shuffle test** (each session's categories shuffled 2,000 times, seed 216; p = share of shuffles with at least the observed count)\n\n",
          md_table(["Pair", "Observed", "Expected", "p"],
                   [[k, v["observed"], v["expected"], v["p_ge"]] for k, v in J["perm_test"].items()]),
          "\n**Same test with `INDETERMINATE` windows removed before shuffling** (IND windows are often the closing turn, "
          f"{J['ind_is_last_window']} of {n_s} sessions end on one; keeping them lets the shuffle break SL runs)\n\n",
          md_table(["Pair", "Observed", "Expected", "p"],
                   [[k, v["observed"], v["expected"], v["p_ge"]] for k, v in J["perm_test_excl_ind"].items()]),
          "\n**Position drift**: mean relative position (0 = first window, 1 = last) of each kind of window, against "
          "2,000 within-session shuffles (sessions with 2+ windows). p_later = share of shuffles with a mean at least as late\n\n",
          md_table(["Windows", "n", "Observed mean", "Shuffled mean", "p_later", "p_earlier"],
                   [[k, v["n"], v["observed"], v["expected"], v["p_later"], v["p_earlier"]] for k, v in J["drift"].items()]),
          "\n**Category share by position** (sessions with 3+ windows, centred fifths; counts)\n\n",
          md_table(["Category", "1st", "2nd", "3rd", "4th", "5th"], [[k] + v for k, v in J["position_bins"].items()]),
          "\n**Frequencies and order**\n\n",
          md_table(["Measure", "Value"], [
              ["Sessions containing each category", ", ".join(f"{k} {v}" for k, v in J["sessions_with"].items())],
              ["First window's category", ", ".join(f"{k} {v}" for k, v in sorted(J["first_window"].items()))],
              ["First non-indeterminate category", ", ".join(f"{k} {v}" for k, v in sorted(J["first_determinate"].items()))],
              ["Sessions with any SL window", f"{len(sl_rows)} of {n_s} ({pct(len(sl_rows), n_s)})"],
              ["…of which SL is not the last window", len(sl_later)],
              ["…which later reach a support window (OFF/AUG)", f"{J['leaves_sl_to_support']} of {len(sl_later)} ({pct(J['leaves_sl_to_support'], len(sl_later))})"],
              ["…which later reach any non-SL, non-IND window", f"{J['leaves_sl_any']} of {len(sl_later)}"],
              ["Sessions whose last non-IND window is SL", J["ends_in_sl"]],
              ["Sessions with both SL and support", len(both)],
              ["…support appears first / SL appears first", f"{J['support_first']} / {J['sl_first']}"],
              ["Adjacent SL→support / support→SL (IND, NEU removed)", f"{J['support_sl_switch']['SL->support']} / {J['support_sl_switch']['support->SL']}"],
              ["Sessions with at least one SL↔support switch (IND, NEU removed)", J["sessions_switching_sl_support"]],
              ["Escalation: a `D1` window later followed by a `D4` window", f"{J['escalation_d1_to_d4']} sessions"],
              ["…same, with each session's decision codes shuffled (mean, p ≥ observed)", f"{J['escalation_shuffle']['shuffled_mean']} (p {J['escalation_shuffle']['p_ge']})"],
              ["…reverse order: a `D4` window later followed by `D1`", f"{J['escalation_shuffle']['reverse_observed']} sessions"],
              ["Rule of each session's first SL window", ", ".join(f"{k} {v}" for k, v in sorted(J["first_sl_rule"].items()))],
              ["Shares, window-weighted", ", ".join(f"{k} {v}" for k, v in J["shares_window_weighted"].items())],
              ["Shares, each session weighted equally", ", ".join(f"{k} {v}" for k, v in J["shares_session_weighted"].items())],
              ["Mean switches per session (all / IND removed)", f"{J['switches_mean']} / {J['switches_excl_ind_mean']}"],
              ["Longest SL run per session (run length: sessions)", ", ".join(f"{k}: {v}" for k, v in J["max_sl_run"].items())],
              ["After an SL window comes", ", ".join(f"{k} {v}" for k, v in J["after_sl"].items())],
              ["Before an SL window comes", ", ".join(f"{k} {v}" for k, v in J["before_sl"].items())],
          ])]
    return J, "".join(md), rows


def main():
    ws = load_windows("final")
    S = sessions(ws)
    # Consistency with the frozen script's own session measures.
    sm = json.load(open(os.path.join(RES, "v12_final", "session_measures.json"), encoding="utf-8"))
    for (d, sid), v in S.items():
        assert sm[f"{d}:{sid}"]["sequence"] == seq_of(v), (d, sid)
    assert len(S) == 106, len(S)

    out, md, all_rows = {}, ["# Session analysis\n\nGenerated by `scripts/sessions.py` from `results/v12_final/` "
                             "(frozen v1.2) and `results/inputs/flags.csv`. Whole sessions only: NIRVANA 71 and WildChat (Bet 7) 35, "
                             "reported together as one writing activity. WildChat cannot show editor behavior (R06, R09, R12, R17, R19, R20 "
                             "cannot fire there), so its sessions lean on chat-only rules; per-dataset rows are a coverage caveat, not a comparison. "
                             "Sequences per session: `sessions/session_table.csv`. The frozen script's `session_measures.json` gives the same "
                             "category sequences (asserted).\n"], []
    for tag, keep in [("All whole sessions", None), ("NIRVANA only (coverage caveat)", "NIRVANA"),
                      ("WildChat only (coverage caveat)", "WildChat")]:
        sub = {k: v for k, v in S.items() if keep is None or k[0] == keep}
        J, m, rows = analyse(sub, tag)
        out[tag] = J
        md.append(m)
        if keep is None:
            all_rows = rows
    write_csv(os.path.join(RES, "sessions", "session_table.csv"), all_rows)
    write_json(os.path.join(RES, "sessions.json"), out)
    write_text(os.path.join(RES, "sessions.md"), "".join(md))


if __name__ == "__main__":
    main()
