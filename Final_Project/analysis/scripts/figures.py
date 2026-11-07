"""Step 2 figures: every chart for the M2 draft, drawn from results/ only. PNGs are written with no
timestamp metadata so reruns are byte-identical. Colors: three categorical slots of the reference palette
(orange, blue, aqua: validated all-pairs) for SL, OFF, AUG; grays for NEU and IND."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import numpy as np
from common import CATS, SL, OF, AU, NE, IN, SHORT, LABEL, SUPPORT, RES, FIG, load_windows, sessions, read_csv

COL = {SL: "#eb6834", OF: "#2a78d6", AU: "#1baf7a", NE: "#8a8984", IN: "#dcdbd6"}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "font.size": 9, "axes.titlesize": 10.5, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "svg.hashsalt": "bet8", "path.simplify": True,
})
STR_ALPHA = {"strong": 1.0, "moderate": 0.75, "weak": 0.42, "-": 1.0}


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, name), dpi=150, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)


def legend(ax, cats=CATS, **kw):
    ax.legend(handles=[Patch(color=COL[c], label=LABEL[c]) for c in cats], frameon=False, **kw)


def fig_category_strength(ws):
    sets = [("NIRVANA", "NIRVANA (347)"), ("WildChat", "WildChat Bet 7 (151)"), ("WildChat-Bet4", "WildChat Bet 4 sample (30)")]
    fig, ax = plt.subplots(figsize=(8, 3.2))
    y = np.arange(len(sets))[::-1]
    for yi, (d, lab) in zip(y, sets):
        g = [w for w in ws if w["dataset"] == d]
        left = 0
        for c in CATS:
            for s in ["strong", "moderate", "weak", "-"]:
                k = sum(w["category"] == c and w["strength"] == s for w in g)
                if not k:
                    continue
                v = 100 * k / len(g)
                ax.barh(yi, v - 0.4, left=left, color=COL[c], alpha=STR_ALPHA[s], height=0.6, edgecolor="none")
                if v >= 4:
                    ax.text(left + v / 2, yi, f"{k}", ha="center", va="center", fontsize=7.5,
                            color="white" if c in (SL, OF, NE) and s != "weak" else INK)
                left += v
    ax.set_yticks(y, [s[1] for s in sets])
    ax.set_xlim(0, 100); ax.set_xlabel("% of windows")
    ax.set_title("Window categories under frozen v1.2, by set (shade: strong > moderate > weak)", loc="left")
    legend(ax, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=5, fontsize=8)
    save(fig, "fig01_category_strength_by_set.png")


def fig_rules(ws):
    rules = sorted({w["rule"] for w in ws})
    cat_of = {w["rule"]: w["category"] for w in ws}
    nir = [sum(w["rule"] == r and w["dataset"] == "NIRVANA" for w in ws) for r in rules]
    wc = [sum(w["rule"] == r and w["dataset"] != "NIRVANA" for w in ws) for r in rules]
    fig, ax = plt.subplots(figsize=(8, 3.4))
    x = np.arange(len(rules))
    ax.bar(x, nir, color=[COL[cat_of[r]] for r in rules], width=0.7, edgecolor="none", label="NIRVANA")
    ax.bar(x, wc, bottom=nir, color=[COL[cat_of[r]] for r in rules], width=0.7, alpha=0.45, edgecolor="none",
           hatch="////", label="WildChat (both sets)")
    for xi, a, b in zip(x, nir, wc):
        ax.text(xi, a + b + 1.5, str(a + b), ha="center", fontsize=7, color=INK2)
    ax.set_xticks(x, rules, rotation=90, fontsize=7.5)
    ax.set_ylabel("windows")
    ax.set_title("Which frozen rule fired (528 windows). Solid = NIRVANA, hatched = WildChat", loc="left")
    legend(ax, loc="upper left", fontsize=7.5, ncol=1)
    ax.yaxis.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    save(fig, "fig02_rules_fired.png")


def fig_timelines(S):
    """One row per session, one cell per window, colored by category; sorted by SL share then length."""
    idx = {c: i for i, c in enumerate(CATS)}
    cmap = ListedColormap([COL[c] for c in CATS] + [SURF])
    norm = BoundaryNorm(np.arange(-0.5, len(CATS) + 1.5), cmap.N)
    groups = [("NIRVANA", "NIRVANA sessions (71)"), ("WildChat", "WildChat sessions (35)")]
    heights = [sum(1 for k in S if k[0] == d) for d, _ in groups]
    fig, axes = plt.subplots(2, 1, figsize=(8, 0.11 * sum(heights) + 2.2), gridspec_kw={"height_ratios": heights})
    for ax, (d, title) in zip(axes, groups):
        keys = [k for k in S if k[0] == d]
        keys.sort(key=lambda k: (-sum(w["category"] == SL for w in S[k]) / len(S[k]),
                                 -sum(w["category"] in SUPPORT for w in S[k]) / len(S[k]), -len(S[k]), k[1]))
        width = max(len(S[k]) for k in keys)
        M = np.full((len(keys), width), len(CATS))
        for i, k in enumerate(keys):
            for j, w in enumerate(S[k]):
                M[i, j] = idx[w["category"]]
        ax.imshow(M, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
        ax.set_xticks(np.arange(width), [str(i + 1) for i in range(width)], fontsize=6.5)
        ax.set_yticks(np.arange(len(keys)), [k[1][:6] for k in keys], fontsize=5)
        ax.set_xticks(np.arange(-0.5, width), minor=True); ax.set_yticks(np.arange(-0.5, len(keys)), minor=True)
        ax.grid(which="minor", color=SURF, lw=1.2); ax.tick_params(which="minor", length=0)
        ax.set_title(title + ": rows sorted by surrender-leaning share", loc="left")
        for sp in ax.spines.values():
            sp.set_visible(False)
    axes[-1].set_xlabel("window (turn order)")
    legend(axes[0], loc="lower right", bbox_to_anchor=(1.0, 1.02), ncol=5, fontsize=7)
    save(fig, "fig03_session_timelines.png")


def fig_transitions(J):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.9))
    for ax, key, cats, title in [(axes[0], "transitions", CATS, "All windows"),
                                 (axes[1], "transitions_excl_ind", CATS[:4], "Indeterminate removed first")]:
        M = np.array([[J[key][f"{SHORT[a]}->{SHORT[b]}"] for b in cats] for a in cats], float)
        R = M / np.maximum(M.sum(1, keepdims=True), 1)
        ax.imshow(R, cmap="Blues", vmin=0, vmax=1)
        for i in range(len(cats)):
            for j in range(len(cats)):
                ax.text(j, i, f"{int(M[i, j])}\n{100 * R[i, j]:.0f}%", ha="center", va="center", fontsize=7,
                        color="white" if R[i, j] > 0.5 else INK)
        ax.set_xticks(range(len(cats)), [SHORT[c] for c in cats]); ax.set_yticks(range(len(cats)), [SHORT[c] for c in cats])
        ax.set_xlabel("next window"); ax.set_ylabel("this window")
        ax.set_title(f"{title} (row %)", loc="left")
        for sp in ax.spines.values():
            sp.set_visible(False)
    fig.suptitle("Transitions between adjacent windows, 106 whole sessions", x=0.02, y=1.03, ha="left", fontweight="bold")
    save(fig, "fig04_transition_matrices.png")


def fig_perm(SJ):
    """Observed vs within-session shuffle, with IND kept (top) and removed before shuffling (bottom)."""
    tags = [("All whole sessions", "All"), ("NIRVANA only (coverage caveat)", "NIRVANA"), ("WildChat only (coverage caveat)", "WildChat")]
    pairs = ["SL->SL", "OFF->OFF", "AUG->AUG", "SL->OFF", "OFF->SL"]
    fig, axes = plt.subplots(2, 3, figsize=(11, 5.6))
    fig.subplots_adjust(wspace=0.5, hspace=0.55)
    for r, (key, rowlab) in enumerate([("perm_test", "IND kept"), ("perm_test_excl_ind", "IND removed first")]):
        for ax, (t, lab) in zip(axes[r], tags):
            pt = SJ[t][key]
            y = np.arange(len(pairs))[::-1]
            ax.hlines(y, [pt[p]["expected"] for p in pairs], [pt[p]["observed"] for p in pairs], color=GRID, lw=2)
            ax.plot([pt[p]["expected"] for p in pairs], y, "o", ms=7, mfc=SURF, mec=INK2, label="shuffled within session")
            ax.plot([pt[p]["observed"] for p in pairs], y, "o", ms=8, color=COL[SL], label="observed")
            top = max(max(pt[p]["observed"], pt[p]["expected"]) for p in pairs)
            for yi, p in zip(y, pairs):
                ax.text(max(pt[p]["observed"], pt[p]["expected"]) + top * 0.04, yi, f"p {pt[p]['p_ge']:.2f}", va="center", fontsize=7, color=INK2)
            ax.set_yticks(y, pairs); ax.set_title(f"{lab}, {rowlab}", loc="left", fontsize=9.5); ax.set_xlabel("adjacent pairs")
            ax.set_xlim(0, top * 1.35)
    axes[0][0].legend(frameon=False, fontsize=7, loc="lower right")
    fig.suptitle("SL->SL is no stickier than session make-up once closing-turn IND windows are set aside (2,000 shuffles each)",
                 x=0.02, y=0.99, ha="left", fontweight="bold")
    save(fig, "fig05_persistence_vs_shuffle.png")


def fig_position(SJ):
    """Category share by centred fifth of the session, per dataset; SL split into request-only (R16) and other."""
    parts = [("SL_not_R16", "Surrender-leaning, behavior seen", COL[SL], 1.0), ("SL_R16", "Surrender-leaning, request only (R16)", COL[SL], 0.4),
             ("OFF", LABEL[OF], COL[OF], 1.0), ("AUG", LABEL[AU], COL[AU], 1.0), ("NEU", LABEL[NE], COL[NE], 1.0), ("IND", LABEL[IN], COL[IN], 1.0)]
    tags = [("NIRVANA only (coverage caveat)", "NIRVANA"), ("WildChat only (coverage caveat)", "WildChat")]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
    x = np.arange(5)
    for ax, (t, lab) in zip(axes, tags):
        bins = SJ[t]["position_bins"]
        tot = np.array([sum(bins[k][i] for k in ("SL", "OFF", "AUG", "NEU", "IND")) for i in range(5)], float)
        bottom = np.zeros(5)
        for key, name, col, al in parts:
            v = 100 * np.array(bins[key]) / tot
            ax.bar(x, v, bottom=bottom, color=col, alpha=al, width=0.75, edgecolor=SURF, linewidth=1, label=name,
                   hatch="////" if key == "SL_R16" else None)
            for xi, vi, b in zip(x, v, bottom):
                if vi > 7:
                    ax.text(xi, b + vi / 2, f"{vi:.0f}%", ha="center", va="center", fontsize=7,
                            color="white" if key in ("SL_not_R16", "OFF", "NEU") else INK)
            bottom += v
        ax.set_xticks(x, ["first fifth", "2nd", "3rd", "4th", "last fifth"])
        ax.set_title(f"{lab} (sessions with 3+ windows)", loc="left")
    axes[0].set_ylabel("% of windows in that part of the session")
    axes[0].legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(1.05, -0.12), ncol=3)
    fig.suptitle("Request-only surrender-leaning opens sessions; behavior-based surrender-leaning sits later",
                 x=0.02, y=1.02, ha="left", fontweight="bold")
    save(fig, "fig06_category_by_position.png")


def fig_drift(SJ):
    tags = [("All whole sessions", "All"), ("NIRVANA only (coverage caveat)", "NIRVANA"), ("WildChat only (coverage caveat)", "WildChat")]
    kinds = ["SL by R16", "SL not R16", "Support (OFF+AUG)"]
    cols = {"SL by R16": COL[SL], "SL not R16": COL[SL], "Support (OFF+AUG)": COL[OF]}
    fig, ax = plt.subplots(figsize=(8, 3.4))
    rows = [(t, lab, k) for t, lab in tags for k in kinds if k in SJ[t]["drift"]]
    y = np.arange(len(rows))[::-1]
    for yi, (t, lab, k) in zip(y, rows):
        d = SJ[t]["drift"][k]
        ax.hlines(yi, d["expected"], d["observed"], color=GRID, lw=2)
        ax.plot(d["expected"], yi, "o", ms=6, mfc=SURF, mec=INK2)
        ax.plot(d["observed"], yi, "o", ms=7, color=cols[k], alpha=0.45 if k == "SL by R16" else 1)
        ax.text(0.87, yi, f"n {d['n']}, p_later {d['p_later']:.3f}", va="center", fontsize=7, color=INK2)
    ax.axvline(0.5, color=GRID, lw=1)
    ax.set_yticks(y, [f"{lab}: {k}" for t, lab, k in rows], fontsize=7.5)
    ax.set_xlim(0.25, 1.1); ax.set_xlabel("mean relative position in session (0 = first window, 1 = last); hollow = shuffled")
    ax.set_title("Where in a session each kind of window sits, vs within-session shuffle", loc="left")
    save(fig, "fig15_position_drift.png")


def fig_first_sl(rows):
    fig, axes = plt.subplots(1, 2, figsize=(9, 3))
    for ax, d in zip(axes, ["NIRVANA", "WildChat"]):
        v = [float(r["first_sl_relative"]) for r in rows if r["dataset"] == d and r["first_sl_relative"] != "" and int(r["n_windows"]) > 1]
        ax.hist(v, bins=np.linspace(0, 1, 11), color=COL[SL], edgecolor=SURF, linewidth=2)
        ax.set_xlabel("relative position of first surrender-leaning window (0 = first, 1 = last)")
        ax.set_title(f"{d}: {len(v)} sessions", loc="left"); ax.set_ylabel("sessions")
    fig.suptitle("When does the first surrender-leaning window appear?", x=0.02, ha="left", fontweight="bold")
    save(fig, "fig07_first_surrender_position.png")


def fig_leave(SJ):
    tags = [("All whole sessions", "All 106"), ("NIRVANA only (coverage caveat)", "NIRVANA 71"), ("WildChat only (coverage caveat)", "WildChat 35")]
    fig, ax = plt.subplots(figsize=(8, 2.8))
    y = np.arange(len(tags))[::-1]
    for yi, (t, lab) in zip(y, tags):
        J = SJ[t]
        n = J["sl_sessions_with_later_window"]
        a = J["leaves_sl_to_support"]
        b = J["leaves_sl_any"] - a
        c = n - a - b
        left = 0
        for k, col, name in [(a, COL[OF], "later reaches offloading/augmenting"), (b, COL[NE], "later reaches neutral only"),
                             (c, COL[SL], "never leaves surrender-leaning (IND aside)")]:
            ax.barh(yi, 100 * k / n - 0.4, left=left, color=col, height=0.55, label=name if yi == y[0] else None)
            if k:
                ax.text(left + 50 * k / n, yi, str(k), ha="center", va="center", fontsize=8, color="white")
            left += 100 * k / n
        ax.text(101, yi, f"n={n}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(y, [t[1] for t in tags]); ax.set_xlim(0, 108); ax.set_xlabel("% of sessions whose first SL window is not their last window")
    ax.set_title("After the first surrender-leaning window, does the session leave it?", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.45, -0.3), ncol=3)
    save(fig, "fig08_leaving_surrender.png")


def fig_composition(rows):
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    for d, m, col in [("NIRVANA", "o", COL[OF]), ("WildChat", "s", COL[SL])]:
        r = [x for x in rows if x["dataset"] == d]
        sx = [int(x["n_OFF"]) + int(x["n_AUG"]) for x in r]
        sy = [int(x["n_SL"]) for x in r]
        n = [int(x["n_windows"]) for x in r]
        xs = [a / b for a, b in zip(sx, n)]; ys = [a / b for a, b in zip(sy, n)]
        ax.scatter(xs, ys, s=[12 + 6 * k for k in n], marker=m, facecolor="none" if d == "WildChat" else col,
                   edgecolor=col, alpha=0.7, linewidth=1.3, label=f"{d} (size = windows)")
    ax.plot([0, 1], [1, 0], color=GRID, lw=1)
    ax.set_xlabel("share of windows: offloading + augmenting"); ax.set_ylabel("share of windows: surrender-leaning")
    ax.set_xlim(-0.03, 1.03); ax.set_ylim(-0.03, 1.03)
    ax.set_title("Session make-up: support vs surrender share", loc="left")
    ax.legend(frameon=False, fontsize=7.5)
    save(fig, "fig09_session_composition.png")


def fig_decisions(S):
    """Decision-code timelines (D0..D4) per NIRVANA session, to see escalation such as D1 -> D4."""
    order = ["D0", "D1", "D2", "D3", "D4", "DX", "?"]
    cols = ["#dcdbd6", "#9ec5f0", "#f5b48f", "#2a78d6", "#c2410c", "#8a8984", "#ffffff"]
    cmap = ListedColormap(cols + [SURF]); norm = BoundaryNorm(np.arange(-0.5, len(order) + 1.5), cmap.N)
    keys = [k for k in S if k[0] == "NIRVANA"]
    keys.sort(key=lambda k: ([w["D"] for w in S[k]].count("D4") * -1, k[1]))
    width = max(len(S[k]) for k in keys)
    M = np.full((len(keys), width), len(order))
    for i, k in enumerate(keys):
        for j, w in enumerate(S[k]):
            M[i, j] = order.index(w["D"]) if w["D"] in order else order.index("?")
    fig, ax = plt.subplots(figsize=(7, 0.11 * len(keys) + 1.6))
    ax.imshow(M, cmap=cmap, norm=norm, aspect="auto", interpolation="nearest")
    ax.set_xticks(np.arange(width), [str(i + 1) for i in range(width)], fontsize=6.5)
    ax.set_yticks(np.arange(len(keys)), [k[1] for k in keys], fontsize=5)
    ax.set_xticks(np.arange(-0.5, width), minor=True); ax.set_yticks(np.arange(-0.5, len(keys)), minor=True)
    ax.grid(which="minor", color=SURF, lw=1.2); ax.tick_params(which="minor", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    names = {"D0": "D0 no decision", "D1": "D1 writer gave content", "D2": "D2 AI proposed, open",
             "D3": "D3 writer chose/revised", "D4": "D4 AI proposal taken", "DX": "DX indeterminate", "?": "unsettled"}
    ax.legend(handles=[Patch(color=c, label=names[o]) for o, c in zip(order, cols) if o != "?"], frameon=False,
              fontsize=6.5, ncol=3, loc="lower left", bbox_to_anchor=(0, 1.01))
    ax.set_xlabel("window (turn order)")
    ax.set_title("NIRVANA decision codes (Q3) per session, sorted by number of D4 windows", loc="left", pad=34)
    save(fig, "fig10_decision_timelines_nirvana.png")


def fig_sensitivity():
    raw = json.load(open(os.path.join(RES, "sensitivity.json"), encoding="utf-8"))
    J, names = raw["variants"], raw["order"]
    fig, axes = plt.subplots(1, 3, figsize=(11, 4.2), sharey=True)
    y = np.arange(len(names))[::-1]
    metrics = [("SL share of windows (%)", lambda h: 100 * h["sl_windows"] / h["windows"], COL[SL]),
               ("Support share of windows (%)", lambda h: 100 * h["support_windows"] / h["windows"], COL[OF]),
               ("SL sessions later reaching support (%)", lambda h: 100 * h["leaves_to_support"] / max(h["sl_with_later"], 1), COL[AU])]
    for ax, (title, f, col) in zip(axes, metrics):
        v = [f(J[n]) for n in names]
        ax.hlines(y, 0, v, color=GRID, lw=2)
        ax.plot(v, y, "o", color=col, ms=6)
        ax.axvline(v[0], color=INK2, lw=0.8, ls=":")
        for yi, vi in zip(y, v):
            ax.text(vi + 1.5, yi, f"{vi:.0f}", va="center", fontsize=7, color=INK2)
        ax.set_title(title, loc="left", fontsize=9); ax.set_xlim(0, 100)
    axes[0].set_yticks(y, [n if len(n) <= 62 else n[:60] + "…" for n in names], fontsize=7)
    fig.suptitle("Headline measures under skeptic variants (dotted = base)", x=0.02, ha="left", fontweight="bold")
    save(fig, "fig11_sensitivity.png")


def fig_coverage(ws):
    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    groups = [("C0", "C0: no next action seen"), ("C1", "C1: chat only"), ("C2", "C2: chat + editor")]
    y = np.arange(3)[::-1]
    for yi, (c, lab) in zip(y, groups):
        g = [w for w in ws if w["coverage"] == c]
        left = 0
        for cat in CATS:
            k = sum(w["category"] == cat for w in g)
            ax.barh(yi, 100 * k / len(g) - 0.3, left=left, color=COL[cat], height=0.55)
            left += 100 * k / len(g)
        ax.text(101, yi, f"n={len(g)}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(y, [g[1] for g in groups]); ax.set_xlim(0, 110); ax.set_xlabel("% of windows")
    ax.set_title("What the log can see decides how much can be inferred", loc="left")
    legend(ax, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=5, fontsize=7)
    save(fig, "fig12_category_by_coverage.png")


def fig_coder_ab(ws):
    A = {w["window_id"]: w["category"] for w in load_windows("coderA")}
    B = {w["window_id"]: w["category"] for w in load_windows("coderB")}
    M = np.array([[sum(A[w["window_id"]] == a and B[w["window_id"]] == b for w in ws) for b in CATS] for a in CATS])
    fig, ax = plt.subplots(figsize=(4.6, 4))
    ax.imshow(M, cmap="Greys", vmin=0, vmax=M.max() * 1.6)
    for i in range(5):
        for j in range(5):
            ax.text(j, i, str(M[i, j]), ha="center", va="center", fontsize=8, color=INK)
    ax.set_xticks(range(5), [SHORT[c] for c in CATS]); ax.set_yticks(range(5), [SHORT[c] for c in CATS])
    ax.set_xlabel("category from coder B's labels"); ax.set_ylabel("category from coder A's labels")
    agree = np.trace(M)
    ax.set_title(f"Coder A vs B categories: {agree}/{M.sum()} agree", loc="left")
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, "fig13_coder_ab_categories.png")


def fig_signatures():
    rows = read_csv(os.path.join(RES, "patterns", "signatures.csv"))
    fig, ax = plt.subplots(figsize=(8, 3.2))
    y = np.arange(len(rows))[::-1]
    nir = [int(r["windows_NIRVANA"]) for r in rows]; wc = [int(r["windows_WildChat"]) for r in rows]
    ax.barh(y, nir, color=COL[OF], height=0.55, label="NIRVANA windows")
    ax.barh(y, wc, left=nir, color=COL[OF], alpha=0.4, hatch="////", height=0.55, label="WildChat windows")
    for yi, a, b, r in zip(y, nir, wc, rows):
        ax.text(a + b + 1, yi, f"{a + b} windows, {r['sessions']} sessions", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(y, [r["signature"] for r in rows], fontsize=8)
    ax.set_xlim(0, max(a + b for a, b in zip(nir, wc)) * 1.45)
    ax.set_title("Recurring behavior signatures (from v1.1 codes)", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="lower right")
    save(fig, "fig14_signatures.png")


def main():
    ws = load_windows("final")
    S = sessions(ws)
    SJ = json.load(open(os.path.join(RES, "sessions.json"), encoding="utf-8"))
    rows = read_csv(os.path.join(RES, "sessions", "session_table.csv"))
    fig_category_strength(ws)
    fig_rules(ws)
    fig_timelines(S)
    fig_transitions(SJ["All whole sessions"])
    fig_perm(SJ)
    fig_position(SJ)
    fig_first_sl(rows)
    fig_leave(SJ)
    fig_composition(rows)
    fig_decisions(S)
    fig_sensitivity()
    fig_coverage(ws)
    fig_coder_ab(ws)
    fig_signatures()
    fig_drift(SJ)


if __name__ == "__main__":
    main()
