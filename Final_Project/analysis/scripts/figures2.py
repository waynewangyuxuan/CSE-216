"""Bet 9 (0010) figures for the theses, fig16-fig25, drawn from results/mining.json, results/mining/*.csv and the
same window loader as mine.py. Byte-identical reruns (no PNG metadata). SL is split into SLb (behavior basis,
full orange) and SLr (request-only basis, light orange with hatching, so the split never rests on color alone)."""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from common import RES, read_csv
from figures import save, INK, INK2, GRID
import mine

TCOL = {"SLb": "#eb6834", "SLr": "#f6b796", "OFF": "#2a78d6", "AUG": "#1baf7a", "NEU": "#8a8984", "IND": "#dcdbd6"}
THATCH = {"SLr": "////"}
TLAB = {"SLb": "Surrender-leaning, behavior basis (SLb)", "SLr": "Surrender-leaning, request only (R16, SLr)",
        "OFF": "Offloading", "AUG": "Augmenting", "NEU": "Neutral-mechanical", "IND": "Indeterminate"}
DCOL = {"NIRVANA": "#2a78d6", "WildChat": "#eb6834"}
ARCH_ORDER = ["Short support visit", "Long working session", "Paste into the draft", "One-shot paste", "Delegate in chat", "Unresolved"]


def tlegend(ax, toks=mine.TOK, **kw):
    ax.legend(handles=[Patch(facecolor=TCOL[t], hatch=THATCH.get(t, ""), edgecolor="white", label=TLAB[t]) for t in toks],
              frameon=False, **kw)


def J():
    with open(os.path.join(RES, "mining.json")) as f:
        return json.load(f)


def fig_sequence_index(arow):
    fig, axes = plt.subplots(2, 3, figsize=(11, 7.2), gridspec_kw={"hspace": 0.45, "wspace": 0.18})
    for ax, a in zip(axes.flat, ARCH_ORDER):
        rs = [r for r in arow if r["archetype"] == a]
        rs.sort(key=lambda r: (-int(r["n_windows"]), r["sequence"]))
        maxw = max(int(r["n_windows"]) for r in rs)
        for y, r in enumerate(rs):
            for x, t in enumerate(r["sequence"].split()):
                ax.add_patch(plt.Rectangle((x + 0.04, len(rs) - y - 1 + 0.06), 0.92, 0.88, facecolor=TCOL[t],
                                           hatch=THATCH.get(t, ""), edgecolor="white", linewidth=0.3))
        ax.set_xlim(0, max(maxw, 4)); ax.set_ylim(0, len(rs))
        ax.set_yticks([]); ax.set_xlabel("window in session", fontsize=8)
        nn = sum(r["dataset"] == "NIRVANA" for r in rs)
        ax.set_title(f"{a}\n{len(rs)} sessions (NIRVANA {nn}, WildChat {len(rs) - nn})", loc="left", fontsize=9.5)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
    fig.suptitle("Six session archetypes: every session as a row of windows, colored by its v1.2 category", x=0.06, ha="left",
                 fontweight="bold", y=0.99)
    tlegend(axes.flat[4], loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=8)
    save(fig, "fig16_archetype_sequences.png")


def fig_archetype_profiles(j):
    P = {p["name"]: p for p in j["archetypes"]["profiles"]}
    fig, ax = plt.subplots(figsize=(9, 3.6))
    y = np.arange(len(ARCH_ORDER))[::-1]
    for yi, a in zip(y, ARCH_ORDER):
        left = 0
        for t in mine.TOK:
            v = P[a][f"share_{t}"] * 100
            ax.barh(yi, max(v - 0.4, 0), left=left, color=TCOL[t], hatch=THATCH.get(t, ""), edgecolor="white", height=0.62, linewidth=0)
            if v >= 7:
                ax.text(left + v / 2, yi, f"{v:.0f}", ha="center", va="center", fontsize=7.5,
                        color="white" if t in ("SLb", "OFF", "AUG", "NEU") else INK)
            left += v
        ax.text(101, yi, f"{P[a]['sessions']} sessions, {P[a]['mean_windows']:.1f} windows", va="center", fontsize=8, color=INK2)
    ax.set_yticks(y, ARCH_ORDER); ax.set_xlim(0, 100); ax.set_xlabel("mean % of a session's windows")
    ax.set_title("Archetype profiles: what each kind of session is made of", loc="left")
    tlegend(ax, loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=8)
    save(fig, "fig17_archetype_profiles.png")


def fig_stage(j):
    cross = {r["token"]: r for r in j["stage"]["cross"]}
    st = [("P", "Planning\n(frame, ideas, sources,\nclaims, argument)"), ("T", "Translating\n(drafting, citing)"),
          ("R", "Reviewing\n(revise, structure,\nlanguage, format)")]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    y = np.arange(len(st))[::-1]
    for yi, (s, lab) in zip(y, st):
        tot = sum(cross[t][s] for t in mine.TOK)
        left = 0
        for t in mine.TOK:
            v = 100 * cross[t][s] / tot
            ax.barh(yi, max(v - 0.4, 0), left=left, color=TCOL[t], hatch=THATCH.get(t, ""), edgecolor="white", height=0.62, linewidth=0)
            if v >= 6:
                ax.text(left + v / 2, yi, f"{cross[t][s]}", ha="center", va="center", fontsize=7.5,
                        color="white" if t in ("SLb", "OFF", "AUG", "NEU") else INK)
            left += v
        ax.text(101, yi, f"{tot} windows", va="center", fontsize=8, color=INK2)
    ax.set_yticks(y, [l for _, l in st]); ax.set_xlim(0, 100); ax.set_xlabel("% of windows at that stage (labels: counts)")
    ax.set_title("Surrender-leaning windows sit at the drafting stage; planning and reviewing are mostly support", loc="left")
    tlegend(ax, loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize=8)
    save(fig, "fig18_stage_by_category.png")


def fig_own_work(j, S):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8), gridspec_kw={"width_ratios": [1, 1.1], "wspace": 0.35})
    G = [g for g in j["own_work"]["first_window_groups"] if g["first_window_prior_own_work"] != "UNSETTLED"]
    order = ["NONE_VISIBLE", "UNOBSERVABLE", "VISIBLE_PARTIAL", "VISIBLE_DRAFT"]
    lab = {"NONE_VISIBLE": "none", "UNOBSERVABLE": "unseen\n(chat)", "VISIBLE_PARTIAL": "notes", "VISIBLE_DRAFT": "draft"}
    xs, i = [], 0
    for d in ("NIRVANA", "WildChat"):
        for p in order:
            g = next((g for g in G if g["dataset"] == d and g["first_window_prior_own_work"] == p), None)
            if not g:
                continue
            a1.bar(i, g["mean_support_share"] * 100, color=DCOL[d], width=0.7)
            a1.text(i, g["mean_support_share"] * 100 + 2, f"n={g['sessions']}", ha="center", fontsize=7.5, color=INK2)
            xs.append((i, lab[p]))
            i += 1
        i += 0.6
    a1.set_xticks([x for x, _ in xs], [l for _, l in xs], fontsize=7.5)
    a1.set_ylim(0, 110); a1.set_ylabel("support share of the session's\ndeterminate windows (%)")
    a1.set_title("Own work in the first window", loc="left")
    a1.legend(handles=[Patch(color=DCOL[d], label=d) for d in DCOL], frameon=False, fontsize=8, loc="upper left")
    pts = []
    for (d, sid), v in S.items():
        if d != "NIRVANA":
            continue
        det = [w for w in v if w["side"] != "X"]
        if det:
            pts.append((int(v[0]["t"]["editor_chars_before"]), 100 * sum(w["side"] == "P" for w in det) / len(det)))
    x = np.array([math.log10(p[0] + 10) for p in pts]); y = np.array([p[1] for p in pts])
    a2.scatter(x, y, s=22, color=DCOL["NIRVANA"], alpha=0.75, edgecolor="white", linewidth=0.6)
    c = j["own_work"]["nirvana_first_ask_correlations"]["editor_chars_first"]
    ticks = [0, 100, 1000, 3000]
    a2.set_xticks([math.log10(t + 10) for t in ticks], [str(t) for t in ticks])
    a2.set_xlabel("characters already in the editor at the first request (log scale)")
    a2.set_ylabel("support share (%)")
    a2.set_title(f"NIRVANA: draft before the first ask (Spearman {c['spearman_rho_with_support_share']}, p {c['p']})", loc="left", fontsize=9.5)
    save(fig, "fig19_own_work_first.png")


def fig_lagged(j):
    rows = [r for r in j["lagged_model"]["coefficients"] if r["predictor"] != "intercept"]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    y = np.arange(len(rows))[::-1]
    for yi, r in zip(y, rows):
        col = "#eb6834" if r["ci95_low"] > 1 else ("#2a78d6" if r["ci95_high"] < 1 else "#8a8984")
        ax.plot([r["ci95_low"], r["ci95_high"]], [yi, yi], color=col, lw=2, solid_capstyle="round")
        ax.plot(r["odds_ratio"], yi, "o", color=col, ms=8, mec="white", mew=1.5)
        ax.text(r["ci95_high"] * 1.15, yi, f"{r['odds_ratio']:.2f}", va="center", fontsize=8, color=INK2)
    ax.axvline(1, color=GRID, lw=1.2, zorder=0)
    ax.set_xscale("log"); ax.set_yticks(y, [r["predictor"] for r in rows])
    ax.set_xlabel("odds ratio for the next substantive window being surrender-leaning (95% session bootstrap)")
    L = j["lagged_model"]
    ax.set_title(f"What the current window says about the next one ({L['n_pairs']} pairs, {L['n_sessions']} sessions)", loc="left")
    save(fig, "fig20_lagged_model.png")


def fig_triggers(j):
    T = j["triggers"]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), gridspec_kw={"wspace": 0.5})
    spec = [(axes[0], "from_SL", "U", "Leaving surrender-leaning,\nby uptake of the current window",
             {"U1": "pasted as is", "U2": "pasted, surface edits", "U4": "iterated in chat", "U8": "moved on"}),
            (axes[1], "from_SL", "prior_own_work", "Leaving surrender-leaning,\nby the writer's own work",
             {"UNOBSERVABLE": "not observable", "NONE_VISIBLE": "none visible", "VISIBLE_PARTIAL": "notes", "VISIBLE_DRAFT": "draft"}),
            (axes[2], "from_support", "prior_own_work", "Entering surrender-leaning from\nsupport, by the writer's own work",
             {"NONE_VISIBLE": "none visible", "VISIBLE_PARTIAL": "notes", "VISIBLE_DRAFT": "draft"})]
    for ax, frm, f, title, lab in spec:
        rs = [r for r in T[frm]["by_feature"][f] if r["value"] in lab]
        rs.sort(key=lambda r: list(lab).index(r["value"]))
        col = "#2a78d6" if frm == "from_SL" else "#eb6834"
        for i, r in enumerate(rs):
            ax.bar(i, r["switch_rate"] * 100, color=col, width=0.65)
            ax.text(i, r["switch_rate"] * 100 + 2, f"{r['switch']}/{r['stay'] + r['switch']}", ha="center", fontsize=7.5, color=INK2)
        ax.set_xticks(range(len(rs)), [lab[r["value"]] for r in rs], fontsize=7.5, rotation=20)
        ax.set_ylim(0, 75); ax.set_ylabel("% of pairs that switch side")
        ax.set_title(title, loc="left", fontsize=9.5)
    save(fig, "fig21_switch_triggers.png")


def fig_survival(j):
    V = j["survival"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.5), gridspec_kw={"wspace": 0.3})
    for d in ("NIRVANA", "WildChat"):
        for ax, key in ((a1, "to_first_SL"), (a2, "SL_to_support")):
            c = V[d][key]
            xs, ys = [0], [1.0]
            for p in c[1:]:
                xs += [p["t"], p["t"]]; ys += [ys[-1], p["surv"]]
            ax.plot(xs, [100 * y for y in ys], color=DCOL[d], lw=2, label=d)
    a1.set_title("Sessions not yet surrender-leaning", loc="left"); a1.set_xlabel("windows into the session")
    a2.set_title("Sessions not yet back to support after the first SL window", loc="left"); a2.set_xlabel("windows after the first SL window")
    for ax in (a1, a2):
        ax.set_ylim(0, 103); ax.set_ylabel("% of sessions (Kaplan-Meier)"); ax.legend(frameon=False, fontsize=8)
        ax.set_xlim(0, 12)
    save(fig, "fig22_time_to_event.png")


def fig_dwell(S):
    toks = ["SLr", "SLb", "OFF", "AUG"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.6), gridspec_kw={"wspace": 0.3})
    rng = np.random.default_rng(216)
    for ax, f, title in ((a1, "dwell_s", "Response to the next request (dwell)"),
                         (a2, "first_copy_ai_s", "Response to the first copy from the chat")):
        for i, t in enumerate(toks):
            xs = [mine.fnum(w["t"].get(f)) for (d, _), v in S.items() if d == "NIRVANA" for w in v if w["tok"] == t]
            xs = np.array([x for x in xs if x is not None])
            if not len(xs):
                continue
            jit = rng.uniform(-0.18, 0.18, len(xs))
            ax.scatter(i + jit, np.log10(xs + 1), s=10, color=TCOL[t], alpha=0.7, edgecolor="none")
            m = np.median(xs)
            ax.plot([i - 0.3, i + 0.3], [math.log10(m + 1)] * 2, color=INK, lw=2)
            ax.text(i + 0.33, math.log10(m + 1), f"{m:.0f}s", va="center", fontsize=8)
        ticks = [1, 10, 60, 300, 1200]
        ax.set_yticks([math.log10(t + 1) for t in ticks], [f"{t}s" for t in ticks])
        ax.set_xticks(range(len(toks)), ["SL\nrequest only", "SL\nbehavior", "Offloading", "Augmenting"], fontsize=8)
        ax.set_title(title, loc="left")
    a1.set_ylabel("seconds (log scale; bar = median)")
    fig.suptitle("NIRVANA: surrender-leaning windows end fast; the copy itself is not slower or faster", x=0.06, ha="left",
                 fontweight="bold", y=1.02)
    save(fig, "fig23_dwell_latency.png")


def fig_outcome(orow, j):
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5), gridspec_kw={"wspace": 0.35})
    C = {(r["session_measure"], r["outcome"]): r for r in j["outcome"]["correlations"]}
    for ax, (x, y, xl, yl) in zip(axes, [("SLb_share", "gpt_final", "share of windows SL by behavior", "GPT Final % of the essay"),
                                         ("SLr_share", "gpt_final", "share of windows SL by request only", "GPT Final % of the essay"),
                                         ("SLb_share", "ownership", "share of windows SL by behavior", "perceived ownership (1-7)")]):
        xs = [float(r[x]) for r in orow if r[y] != ""]
        ys = [float(r[y]) * (100 if y == "gpt_final" else 1) for r in orow if r[y] != ""]
        ax.scatter(xs, ys, s=22, color=TCOL["SLb" if x == "SLb_share" else "SLr"], edgecolor=INK2, linewidth=0.4, alpha=0.85)
        c = C[(x, y)]
        ax.set_title(f"rho {c['spearman_rho']}, p {c['p']} (n={c['sessions']})", loc="left", fontsize=9.5)
        ax.set_xlabel(xl, fontsize=8.5); ax.set_ylabel(yl, fontsize=8.5)
    fig.suptitle("NIRVANA essays: behavior-based surrender tracks AI share and lower ownership; request-only does not track AI share",
                 x=0.06, ha="left", fontweight="bold", y=1.03)
    save(fig, "fig24_outcome.png")


def fig_log_triggers(j):
    rows = j["log_triggers"]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    y = np.arange(len(rows))[::-1]
    base = rows[0]["SL_base_rate_determinate"] * 100
    for yi, r in zip(y, rows):
        ax.barh(yi + 0.17, r["SL_among_fired_determinate"] * 100, height=0.32, color="#eb6834")
        ax.barh(yi - 0.17, r["SL_windows_caught"] * 100, height=0.32, color="#2a78d6")
        ax.text(r["SL_among_fired_determinate"] * 100 + 1, yi + 0.17, f"{r['SL_among_fired_determinate'] * 100:.0f}%", va="center", fontsize=7.5)
        ax.text(r["SL_windows_caught"] * 100 + 1, yi - 0.17, f"{r['SL_windows_caught'] * 100:.0f}%", va="center", fontsize=7.5)
    ax.axvline(base, color=INK2, lw=1, ls="--")
    ax.text(base + 1, y[-1] - 0.5, f"SL base rate {base:.0f}%", fontsize=7.5, color=INK2)
    ax.set_yticks(y, [r["trigger"] for r in rows]); ax.set_xlim(0, 100); ax.set_xlabel("%")
    ax.legend(handles=[Patch(color="#eb6834", label="SL among windows where it fires (precision)"),
                       Patch(color="#2a78d6", label="SL windows it catches (recall)")], frameon=False, fontsize=8,
              loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    ax.set_title("NIRVANA: four triggers computed from the keystroke log alone", loc="left")
    save(fig, "fig25_log_triggers.png")


def main():
    j = J()
    S, _ = mine.load()
    arow = read_csv(os.path.join(RES, "mining", "archetypes.csv"))
    orow = read_csv(os.path.join(RES, "mining", "outcome_sessions.csv"))
    fig_sequence_index(arow)
    fig_archetype_profiles(j)
    fig_stage(j)
    fig_own_work(j, S)
    fig_lagged(j)
    fig_triggers(j)
    fig_survival(j)
    fig_dwell(S)
    fig_outcome(orow, j)
    fig_log_triggers(j)


if __name__ == "__main__":
    main()
