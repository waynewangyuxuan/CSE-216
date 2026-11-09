#!/usr/bin/env python3
"""Draw every paper figure from analysis results in one palette, as vector PDFs; run with analysis/.venv/bin/python."""
import csv
import json
import math
import pathlib
import sys

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Patch, Rectangle
from matplotlib.text import Text
import numpy as np

PAPER = pathlib.Path(__file__).resolve().parents[1]
FP = PAPER.parent
sys.path.insert(0, str(FP / "analysis" / "scripts"))
import mine  # noqa: E402

OUT = PAPER / "figures"
WIDTH = 6.0  # inches; the figures are placed at \linewidth

# One color per category in every figure; lightness differs so the order survives greyscale print.
COL = {"SLb": "#D55E00", "SLr": "#F5B27A", "OFF": "#004E89", "AUG": "#56B4E9", "NEU": "#6E6E6E", "IND": "#E3E3E3"}
HATCH = {"SLr": "////"}
LABEL = {
    "SLb": "Surrender-leaning, behavior-based",
    "SLr": "Surrender-leaning, request-only",
    "OFF": "Offloading",
    "AUG": "Augmenting",
    "NEU": "Neutral-mechanical",
    "IND": "Indeterminate",
}
ON_DARK = {"SLb", "OFF", "NEU"}
INK, INK2, RULE = "#222222", "#555555", "#BBBBBB"
SCRIPT_FILL, AI_FILL = "#EEEEEE", "#FFFFFF"

plt.rcParams.update({
    "font.family": ["Arial", "DejaVu Sans"], "font.size": 8, "pdf.fonttype": 42, "axes.edgecolor": RULE,
    "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
    "axes.spines.right": False, "hatch.linewidth": 0.6, "hatch.color": "#B65A1E", "axes.titlesize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "axes.labelsize": 7.5, "axes.titleweight": "bold",
})

TEXTS = []


def save(fig, name):
    TEXTS.extend(t.get_text() for t in fig.findobj(Text) if t.get_text().strip())
    fig.savefig(OUT / f"{name}.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)


def canvas(height):
    fig = plt.figure(figsize=(WIDTH, height))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, WIDTH)
    ax.set_ylim(0, height)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc="white", ec=INK2, fs=7.5, color=INK, weight="normal", ls="-", hatch=None, lw=0.8, align="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", fc=fc, ec=ec, ls=ls, lw=lw, hatch=hatch))
    tx = x + w / 2 if align == "center" else x + 0.07
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=fs, color=color, weight=weight, linespacing=1.15)


def cat_box(ax, x, y, w, h, text, tok, fs=7.5, weight="normal"):
    box(ax, x, y, w, h, text, fc=COL[tok], ec=INK2, fs=fs, color="white" if tok in ON_DARK else INK, weight=weight, hatch=HATCH.get(tok))


def arrow(ax, p, q, color=INK2, lw=0.9, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=8, color=color, lw=lw, shrinkA=0, shrinkB=0))


def fig_flow():
    h = 3.85
    fig, ax = canvas(h)
    ax.text(1.5, h - 0.11, "NIRVANA", ha="center", weight="bold", fontsize=8.5, color=INK)
    ax.text(4.5, h - 0.11, "WildChat", ha="center", weight="bold", fontsize=8.5, color=INK)
    y = h - 0.68
    box(ax, 0.1, y, 2.8, 0.44, "77 university students wrote a timed essay\nwith ChatGPT; chat and editor were logged")
    box(ax, 3.1, y, 2.8, 0.44, "WildChat-1M: 837,989 conversations from\nusers of a free ChatGPT service")
    arrow(ax, (1.5, y), (1.5, y - 0.14))
    arrow(ax, (4.5, y), (4.5, y - 0.14))
    y -= 0.58
    box(ax, 0.1, y, 2.8, 0.44, "Script: 71 students used the chat,\n347 request windows", fc=SCRIPT_FILL)
    box(ax, 3.1, y, 2.8, 0.44, "Script: 139,736 eligible. AI screen of a\nrandom seed of 1,200: 114 accepted", fc=SCRIPT_FILL)
    arrow(ax, (1.5, y), (1.5, y - 0.14))
    arrow(ax, (4.5, y), (4.5, y - 0.14))
    y -= 0.58
    box(ax, 0.1, y, 2.8, 0.44, "71 whole sessions\nC0 7, C1 136, C2 204 windows", fc=SCRIPT_FILL)
    box(ax, 3.1, y, 2.8, 0.44, "35 whole conversations, 151 windows,\nplus 30 windows from an earlier sample", fc=SCRIPT_FILL)
    arrow(ax, (1.5, y), (2.6, y - 0.14))
    arrow(ax, (4.5, y), (3.4, y - 0.14))
    y -= 0.42
    box(ax, 1.9, y, 2.2, 0.28, "528 request windows", fc="white", weight="bold", ec=INK, lw=1.1)
    arrow(ax, (2.3, y), (1.3, y - 0.16))
    arrow(ax, (3.7, y), (4.7, y - 0.16))
    y -= 0.5
    box(ax, 0.1, y, 2.3, 0.34, "Coder A (Opus 5.5)\nlabels Q1 to Q5 alone", ls="--")
    box(ax, 3.6, y, 2.3, 0.34, "Coder B (Sonnet 5.5)\nlabels Q1 to Q5 alone", ls="--")
    box(ax, 2.55, y, 0.9, 0.34, "Adjudicator\n(Opus 5.5)", ls="--", fs=7)
    arrow(ax, (2.4, y + 0.17), (2.55, y + 0.17))
    arrow(ax, (3.6, y + 0.17), (3.45, y + 0.17))
    arrow(ax, (3.0, y), (3.0, y - 0.14))
    y -= 0.42
    box(ax, 2.4, y, 1.2, 0.28, "Final codes", fc="white")
    box(ax, 3.82, y, 0.98, 0.28, "Frozen v1.2 rules", fc=SCRIPT_FILL, fs=6.9)
    box(ax, 5.02, y, 0.88, 0.28, "Category,\nstrength", fc=COL["IND"], weight="bold", fs=6.9)
    arrow(ax, (3.6, y + 0.14), (3.82, y + 0.14))
    arrow(ax, (4.8, y + 0.14), (5.02, y + 0.14))
    box(ax, 0.1, y, 2.05, 0.28, "Log facts (NIRVANA): timing,\ntyping, essay outcomes", fc=SCRIPT_FILL, fs=6.9)
    arrow(ax, (1.1, y), (1.1, y - 0.14))
    arrow(ax, (5.46, y), (5.46, y - 0.14))
    y -= 0.42
    box(ax, 0.1, y, 5.8, 0.28, "106 whole sessions (498 windows), chained by turn: archetypes, order tests, theses T1 to T4", fc=SCRIPT_FILL)
    legend_y = 0.02
    ax.add_patch(Rectangle((0.1, legend_y + 0.02), 0.22, 0.13, fc="white", ec=INK2, lw=0.8))
    ax.text(0.36, legend_y + 0.085, "dataset authors", va="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle((1.32, legend_y + 0.02), 0.22, 0.13, fc=SCRIPT_FILL, ec=INK2, lw=0.8))
    ax.text(1.58, legend_y + 0.085, "script or screen", va="center", fontsize=7, color=INK2)
    ax.add_patch(Rectangle((2.52, legend_y + 0.02), 0.22, 0.13, fc="white", ec=INK2, lw=0.8, ls="--"))
    ax.text(2.78, legend_y + 0.085, "AI agent", va="center", fontsize=7, color=INK2)
    ax.text(5.9, legend_y + 0.085, "No human coded any window.", va="center", ha="right", fontsize=7.5, weight="bold", color=INK)
    save(fig, "flow")


def bracket(ax, x0, x1, y, text, fs=7.5, up=False):
    tick = 0.05 if not up else -0.05
    ax.plot([x0, x0, x1, x1], [y + tick, y, y, y + tick], color=INK2, lw=0.9)
    ax.text((x0 + x1) / 2, y - 0.04 if not up else y + 0.04, text, ha="center", va="top" if not up else "bottom", fontsize=fs, color=INK, linespacing=1.15)


def fig_anatomy():
    h = 2.75
    fig, ax = canvas(h)
    xs = [0.1, 1.55, 3.0, 4.45]
    w = 1.3
    y = 1.45
    labels = ["Editor and earlier\nturns before\nthe request", "Request\nthe writer sends", "AI response", "Next action, before\nthe next request:\neditor events or chat"]
    for i, (x, t) in enumerate(zip(xs, labels)):
        box(ax, x, y, w if i < 3 else 1.45, 0.62, t, weight="bold" if 0 < i else "normal", fc=SCRIPT_FILL if i == 0 else "white")
        if i < 3:
            arrow(ax, (x + w, y + 0.31), (xs[i + 1], y + 0.31))
    # coverage above
    top = 2.28
    for x1, label, yy in [(4.3, "C0: request and response only", top), (5.2, "C1: plus a later chat turn", top + 0.17), (5.9, "C2: plus editor or paste actions", top + 0.34)]:
        ax.plot([1.55, x1], [yy, yy], color=INK2, lw=1.2)
        ax.text(1.5, yy, label, ha="right", va="center", fontsize=7.2, color=INK2)
    # codes below
    bracket(ax, 0.1, 1.4, 1.36, "prior_own_work\nwriter's draft or\nnotes visible?")
    bracket(ax, 1.55, 2.85, 1.36, "Q1 operation\nQ2 function, object\nwhat is asked for")
    bracket(ax, 3.0, 5.9, 1.36, "Q3 decision: whose content is in the response,\nand what the next action shows")
    bracket(ax, 4.45, 5.14, 0.76, "Q4\nverification\nvisible check")
    bracket(ax, 5.2, 5.9, 0.76, "Q5 uptake\npaste, type,\niterate, leave")
    ax.text(0.1, 0.18, "Codes record behavior. Silent reading or thinking leaves no code.", fontsize=7.5, color=INK, style="italic")
    save(fig, "anatomy")


def fig_worked():
    h = 3.05
    fig, ax = canvas(h)
    cols = [(0.1, 2.35), (2.55, 0.85), (3.5, 1.15), (4.75, 1.15)]
    heads = ["Observed in the log (paraphrased)", "Codes (AI coders)", "Rule (script)", "Category (inference)"]
    top = h - 0.26
    for (x, w), t in zip(cols, heads):
        ax.text(x + w / 2, top + 0.13, t, ha="center", va="center", weight="bold", fontsize=7.5, color=INK)
    ax.add_patch(Rectangle((0.03, 0.03), 2.46, top - 0.03, fc="none", ec=RULE, lw=0.7, ls=":"))
    ax.text(0.09, 0.1, "observed", fontsize=7, color=INK2, va="center", style="italic")
    ax.add_patch(Rectangle((2.5, 0.03), 3.47, top - 0.03, fc="none", ec=RULE, lw=0.7, ls=":"))
    ax.text(2.56, 0.1, "assigned and inferred: nothing here measures thinking", fontsize=7, color=INK2, va="center", style="italic")
    rows = [
        (1.5, "NIRVANA-e41-t06: whole paste", "The editor is empty. The writer asks for\nthe essay in a form ready to copy, copies\nit 6.5 s after the response and pastes\n4,681 characters. Nothing is changed.",
         "F8  D4  V0  U1\nnone visible\nC2", "R09\nD4, no check, U1,\nno own work\nvisible, C2", "Surrender-leaning\nstrong", "SLb", "Alternative: silent\nevaluation first"),
        (0.28, "NIRVANA-e24-t01: partial take", "A short note is in the editor. The writer\ncopies one AI sentence, changes its ending\nand types a paragraph of their own:\n1,271 characters typed, 334 pasted, 577 s.",
         "F4  D3  V0  U3\nnone visible\nC2", "R08\nD3 or U3, after\nearlier rules\ndo not match", "Offloading\nmoderate", "OFF", "Alternative: the part\nkept may be AI's"),
    ]
    for y, title, obs, codes, rule, cat, tok, alt in rows:
        ax.text(0.14, y + 1.0, title, fontsize=7.5, weight="bold", color=INK, va="center")
        box(ax, 0.1, y, 2.35, 0.86, obs, align="left", fs=7.3)
        box(ax, 2.55, y, 0.85, 0.86, codes, ls="--", fs=7.3)
        box(ax, 3.5, y, 1.15, 0.86, rule, fc=SCRIPT_FILL, fs=7.3)
        cat_box(ax, 4.75, y + 0.34, 1.15, 0.52, cat, tok, weight="bold")
        ax.text(5.325, y + 0.16, alt, ha="center", va="center", fontsize=6.9, color=INK2, linespacing=1.1)
        arrow(ax, (2.45, y + 0.43), (2.55, y + 0.43))
        arrow(ax, (3.4, y + 0.43), (3.5, y + 0.43))
        arrow(ax, (4.65, y + 0.6), (4.75, y + 0.6))
    save(fig, "worked")


def fig_concept():
    h = 3.8
    fig, ax = canvas(h)
    x0, y0, W, H = 0.42, 0.42, 5.46, 3.28
    ax.add_patch(Rectangle((x0, y0), W, H, fc="white", ec=RULE, lw=0.8))
    ax.add_patch(Rectangle((x0 + W * 0.42, y0), W * 0.58, H * 0.47, fc="#FBE9DC", ec="none"))
    ax.add_patch(Rectangle((x0, y0 + H * 0.47), W, H * 0.53, fc="#E5F0F8", ec="none"))
    ax.add_patch(Rectangle((x0, y0), W * 0.42, H * 0.47, fc="#E5F0F8", ec="none"))
    ax.text(x0 + 0.07, y0 + H - 0.11, "Support side", fontsize=8, weight="bold", color=COL["OFF"], va="center")
    ax.text(x0 + W * 0.42 + 0.07, y0 + 0.12, "Surrender-leaning side", fontsize=8, weight="bold", color="#A84700", va="center")
    ax.annotate("", (x0 + W, 0.3), (x0, 0.3), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.9))
    ax.text(x0, 0.13, "the writer's own content", fontsize=7.5, color=INK2, va="center")
    ax.text(x0 + W / 2, 0.13, "Whose content is in play?", fontsize=7.5, weight="bold", color=INK, va="center", ha="center")
    ax.text(x0 + W, 0.13, "AI-originated content", fontsize=7.5, color=INK2, va="center", ha="right")
    ax.annotate("", (0.3, y0 + H), (0.3, y0), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.9))
    ax.text(0.14, y0 + H / 2, "Does the text pass through the writer's hands?", fontsize=7.5, weight="bold", color=INK, rotation=90, va="center", ha="center")
    items = [
        (0.62, 1.82, 1.55, 0.56, "Writer's text reworded\nfor language (D1 F5)\n68 windows, 46 offloading", "OFF"),
        (2.32, 2.97, 1.62, 0.56, "Ask, then write own text\n(D2 U7) 52 windows,\n37 augmenting", "AUG"),
        (4.08, 2.97, 1.62, 0.56, "Reasoned check (V3)\n13 windows,\nall offloading", "OFF"),
        (3.48, 2.18, 1.72, 0.56, "Partial take, AI text changed\n(D3) 46 windows,\n37 offloading", "OFF"),
        (2.72, 1.25, 1.5, 0.56, "Surface-only iteration\n(D2 V1 U4) 30 windows,\n21 surrender-leaning", "SLb"),
        (4.32, 1.33, 1.5, 0.56, "Whole paste (D4 V0 U1)\n32 windows,\n30 surrender-leaning", "SLb"),
        (4.08, 0.58, 1.72, 0.56, "Draft requested, kept in chat\n(D2 F4 U4/U5) 72 windows,\n69 surrender-leaning", "SLr"),
    ]
    for x, y, w, hh, text, tok in items:
        if tok == "SLr":
            ax.add_patch(FancyBboxPatch((x, y), w, hh, boxstyle="round,pad=0,rounding_size=0.05", fc=COL[tok], ec=INK2, lw=0.8, hatch="////"))
            ax.text(x + w / 2, y + hh / 2, text, ha="center", va="center", fontsize=7.1, color=INK, linespacing=1.15,
                    bbox=dict(fc=COL[tok], ec="none", pad=1.2))
        else:
            cat_box(ax, x, y, w, hh, text, tok, fs=7.1)
    box(ax, 0.62, 0.56, 1.72, 0.56, "No substantive decision\n(D0): neutral-mechanical,\noutside both axes, 53 windows", fc=COL["NEU"], fs=7.1, color="white")
    save(fig, "concept_map")


def fig_categories(S):
    rows = []
    for d in ("NIRVANA", "WildChat"):
        n = {t: 0 for t in mine.TOK}
        for (ds, _), v in S.items():
            if ds == d:
                for w in v:
                    n[w["tok"]] += 1
        rows.append((d, n))
    fig, ax = plt.subplots(figsize=(WIDTH, 1.55))
    for y, (d, n) in zip([1, 0], rows):
        total, left = sum(n.values()), 0
        for t in mine.TOK:
            v = 100 * n[t] / total
            ax.barh(y, v - 0.5, left=left, color=COL[t], hatch=HATCH.get(t), edgecolor="white", height=0.62, lw=0)
            if n[t] >= 5:
                t_obj = ax.text(left + v / 2, y, str(n[t]), ha="center", va="center", fontsize=7.5, color="white" if t in ON_DARK else INK)
                if t in HATCH:
                    t_obj.set_bbox(dict(fc=COL[t], ec="none", pad=0.8))
            left += v
    ax.set_yticks([1, 0], [f"{d}\n{sum(n.values())} windows" for d, n in rows])
    ax.set_xlim(0, 100)
    ax.set_xlabel("share of whole-session windows (%), with counts")
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False)
    ax.legend(handles=[Patch(facecolor=COL[t], hatch=HATCH.get(t, ""), edgecolor="white", label=LABEL[t]) for t in mine.TOK], frameon=False,
              fontsize=7, ncol=3, loc="lower center", bbox_to_anchor=(0.45, 1.0), handlelength=1.4, columnspacing=1.2)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.72, bottom=0.27)
    save(fig, "categories")


ARCH = ["Short support visit", "Long working session", "Paste into the draft", "One-shot paste", "Delegate in chat", "Unresolved"]
ARCH_DESC = {
    "Short support visit": "mean 2.3 windows; offloading 46%,\naugmenting 28%; essay AI share 0.0",
    "Long working session": "mean 10.4 windows, mixed; offloading\n31%, augmenting 23%; essay AI share 0.18",
    "Paste into the draft": "mean 4.6 windows; behavior-based\nsurrender 65%; essay AI share 0.97",
    "One-shot paste": "a single window, behavior-based\nsurrender 71%; essay AI share 1.0",
    "Delegate in chat": "mean 7.9 windows; request-only\nsurrender 64%; essay AI share 0.32",
    "Unresolved": "mean 2.6 windows; indeterminate\n60%, request-only 30%; essay AI share 0.0",
}


def tile(ax, x, y, tok, w=0.92, h=0.88, lw=0.3):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=COL[tok], hatch=HATCH.get(tok), edgecolor="white", linewidth=lw))


def fig_archetypes(S):
    rows = list(csv.DictReader(open(FP / "analysis" / "results" / "mining" / "archetypes.csv")))
    fig = plt.figure(figsize=(WIDTH, 5.65))
    strip = fig.add_axes([0, 0.881, 1, 0.119])
    strip.set_xlim(0, WIDTH)
    strip.set_ylim(0, 0.671)
    strip.axis("off")
    seq = [w["tok"] for (d, sid), v in S.items() if d == "NIRVANA" and sid == "e70" for w in v]
    x0 = 1.15
    strip.text(0.08, 0.53, "One window", fontsize=7.5, weight="bold", color=INK, va="center")
    strip.text(0.08, 0.42, "request, response,\nnext action", fontsize=7, color=INK2, va="top", linespacing=1.1)
    for i, t in enumerate(seq):
        strip.add_patch(Rectangle((x0 + i * 0.36, 0.34), 0.33, 0.27, fc=COL[t], hatch=HATCH.get(t), ec="white", lw=0.6))
    arrow(strip, (0.9, 0.48), (x0 - 0.02, 0.48))
    strip.text(x0, 0.2, "One session (e70): windows in turn order. Polishing own text, then pasted AI text.", fontsize=7, color=INK2, va="center")
    arrow(strip, (3.75, 0.48), (4.1, 0.48))
    strip.text(4.15, 0.48, "Sessions with similar sequences\ncluster into archetypes (below)", fontsize=7.5, color=INK, va="center", linespacing=1.1)
    fig.legend(handles=[Patch(facecolor=COL[t], hatch=HATCH.get(t, ""), edgecolor="white", label=LABEL[t]) for t in mine.TOK], frameon=False,
               fontsize=7, ncol=3, loc="lower center", bbox_to_anchor=(0.5, 0.0), handlelength=1.3, columnspacing=1.2)
    g = fig.add_gridspec(2, 3, left=0.03, right=0.99, top=0.815, bottom=0.122, hspace=0.5, wspace=0.09)
    for k, a in enumerate(ARCH):
        ax = fig.add_subplot(g[k // 3, k % 3])
        rs = sorted([r for r in rows if r["archetype"] == a], key=lambda r: (-int(r["n_windows"]), r["sequence"]))
        maxw = max(int(r["n_windows"]) for r in rs)
        for y, r in enumerate(rs):
            for x, t in enumerate(r["sequence"].split()):
                tile(ax, x + 0.04, len(rs) - y - 1 + 0.06, t)
        ax.set_xlim(0, max(maxw, 4))
        ax.set_ylim(0, len(rs))
        ax.set_yticks([])
        ax.set_xlabel("window in session", fontsize=7, labelpad=1)
        ax.spines["left"].set_color(RULE)
        nn = sum(r["dataset"] == "NIRVANA" for r in rs)
        ax.set_title(f"{a}: {len(rs)} sessions\nNIRVANA {nn}, WildChat {len(rs) - nn}\n{ARCH_DESC[a]}", loc="left", fontsize=7, fontweight="normal", color=INK, linespacing=1.15, pad=3)
    save(fig, "archetypes")


def fig_after():
    h = 2.45
    rows = [
        ("AI proposal taken (D4)\n42 pasted windows,\n39 behavior-based", 15.3, 70.5, 6, "SLb"),
        ("Part taken or revised (D3)\n32 pasted windows,\n28 offloading", 17.2, 288.1, 304.5, "OFF"),
        ("Writer's own text reworked (D1)\n29 pasted windows,\n28 offloading", 8.75, 150.05, 25, "OFF"),
    ]
    fig, ax = canvas(h)
    x0, xw = 1.95, 3.3
    scale = xw / 300
    ys = [1.72, 1.08, 0.44]
    for (label, copy, dwell, typed, tok), y in zip(rows, ys):
        ax.text(0.1, y, label, fontsize=7.2, va="center", color=INK, linespacing=1.15)
        ax.add_patch(Rectangle((x0, y - 0.12), dwell * scale, 0.24, fc=COL[tok], ec="none"))
        px = x0 + copy * scale
        ax.plot([px, px], [y - 0.2, y + 0.2], color=INK, lw=1.3)
        end = x0 + dwell * scale
        ax.plot([end], [y], marker=">", color=INK, ms=6)
        ax.text(end + 0.1, y, f"{dwell:.1f} s", fontsize=7.5, va="center", color=INK, weight="bold")
        ax.text(x0 + 0.5 * (min(dwell, 300) * scale) if dwell > 100 else end + 0.65, y, f"typed {typed:g} chars", fontsize=7.5, va="center", ha="center" if dwell > 100 else "left", color="white" if dwell > 100 else INK)
    axis_y = 0.1
    ax.plot([x0, x0 + xw], [axis_y, axis_y], color=RULE, lw=0.8)
    for t in (0, 60, 120, 180, 240, 300):
        ax.plot([x0 + t * scale] * 2, [axis_y, axis_y + 0.04], color=RULE, lw=0.8)
        ax.text(x0 + t * scale, axis_y - 0.03, f"{t}", fontsize=7, ha="center", va="top", color=INK2)
    ax.text(x0 - 0.1, axis_y - 0.03, "seconds", fontsize=7, ha="right", va="top", color=INK2)
    ax.plot([x0, x0], [axis_y, 2.1], color=INK2, lw=0.9, ls=":")
    ax.text(x0, 2.26, "AI response\nfinishes", fontsize=7.2, color=INK, ha="center", va="center", linespacing=1.05)
    ax.plot([3.25, 3.25], [2.15, 2.37], color=INK, lw=1.3)
    ax.text(3.31, 2.26, "first copy from the chat", fontsize=7.2, va="center", color=INK)
    ax.plot([4.95], [2.26], marker=">", color=INK, ms=6)
    ax.text(5.03, 2.26, "next request", fontsize=7.2, va="center", color=INK)
    save(fig, "after_response")


def fig_outcome():
    j = json.load(open(FP / "analysis" / "results" / "mining.json"))
    C = {(r["session_measure"], r["outcome"]): r for r in j["outcome"]["correlations"]}
    rows = list(csv.DictReader(open(FP / "analysis" / "results" / "mining" / "outcome_sessions.csv")))
    pts = np.array([[float(r["SLb_share"]), float(r["SLr_share"]), float(r["gpt_final"]) * 100, float(r["ownership"])] for r in rows])
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH, 2.15))
    specs = [(0, 2, "SLb", "share behavior-based", "essay AI share (%)", "SLb_share", "gpt_final"),
             (1, 2, "SLr", "share request-only", "essay AI share (%)", "SLr_share", "gpt_final"),
             (0, 3, "SLb", "share behavior-based", "felt ownership (1 to 7)", "SLb_share", "ownership")]
    for ax, (xi, yi, tok, xl, yl, a, b) in zip(axes, specs):
        ax.scatter(pts[:, xi], pts[:, yi], s=14, color=COL[tok], edgecolor=INK2, linewidth=0.35, alpha=0.9)
        c = C[(a, b)]
        ax.set_title(f"rho {c['spearman_rho']:.2f} (n = {c['sessions']})".replace("-", "\u2212"), loc="left")
        ax.set_xlabel(xl, labelpad=2)
        ax.set_ylabel(yl, labelpad=2)
    fig.subplots_adjust(left=0.08, right=0.99, top=0.9, bottom=0.2, wspace=0.34)
    save(fig, "outcome")


def fig_own_work(S):
    j = json.load(open(FP / "analysis" / "results" / "mining.json"))
    G = j["own_work"]["first_window_groups"]
    order = ["NONE_VISIBLE", "UNOBSERVABLE", "VISIBLE_PARTIAL", "VISIBLE_DRAFT"]
    lab = {"NONE_VISIBLE": "none", "UNOBSERVABLE": "unseen", "VISIBLE_PARTIAL": "notes", "VISIBLE_DRAFT": "draft"}
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(WIDTH, 2.25), gridspec_kw={"width_ratios": [1, 1.1]})
    xs, i = [], 0
    for d, fc, hatch in (("NIRVANA", "#444444", None), ("WildChat", "#FFFFFF", "....")):
        start = i
        for p in order:
            g = next((g for g in G if g["dataset"] == d and g["first_window_prior_own_work"] == p), None)
            if not g:
                continue
            a1.bar(i, g["mean_support_share"] * 100, color=fc, width=0.72, hatch=hatch, edgecolor="#444444", lw=0.7)
            a1.text(i, g["mean_support_share"] * 100 + 2, f"n={g['sessions']}", ha="center", fontsize=7, color=INK2)
            xs.append((i, lab[p]))
            i += 1
        a1.text((start + i - 1) / 2, 118, d, ha="center", fontsize=7.5, weight="bold", color=INK)
        i += 0.6
    a1.set_xticks([x for x, _ in xs], [l for _, l in xs])
    a1.set_ylim(0, 112)
    a1.set_ylabel("mean support share (%)", labelpad=2)
    a1.set_xlabel("own work visible in the first window", labelpad=2)
    pts = []
    for (d, sid), v in S.items():
        if d != "NIRVANA":
            continue
        det = [w for w in v if w["side"] != "X"]
        if det:
            pts.append((int(v[0]["t"]["editor_chars_before"]), 100 * sum(w["side"] == "P" for w in det) / len(det)))
    x = [math.log10(p[0] + 10) for p in pts]
    y = [p[1] for p in pts]
    a2.scatter(x, y, s=14, color="#444444", alpha=0.75, edgecolor="white", linewidth=0.4)
    c = j["own_work"]["nirvana_first_ask_correlations"]["editor_chars_first"]
    ticks = [0, 100, 1000, 3000]
    a2.set_xticks([math.log10(t + 10) for t in ticks], [str(t) for t in ticks])
    a2.set_xlabel("characters in the editor at the first request (log scale)", labelpad=2)
    a2.set_ylabel("support share (%)", labelpad=2)
    a2.set_title(f"NIRVANA sessions: rho {c['spearman_rho_with_support_share']:.2f}, n = {c['sessions'] if 'sessions' in c else 65}", loc="left")
    fig.subplots_adjust(left=0.08, right=0.99, top=0.86, bottom=0.19, wspace=0.24)
    save(fig, "own_work")


def support_bar(ax, x, value, width):
    ax.bar(x, value, width, color=COL["AUG"], hatch="\\\\\\\\", edgecolor=COL["OFF"], lw=0.5)


def fig_dwell(S):
    toks = ["SLr", "SLb", "OFF", "AUG"]
    names = {"SLr": "request-\nonly", "SLb": "behavior-\nbased", "OFF": "offload-\ning", "AUG": "augment-\ning"}
    fig, axes = plt.subplots(1, 3, figsize=(WIDTH, 2.5), gridspec_kw={"width_ratios": [1.15, 1.15, 0.85]})
    rng = np.random.default_rng(216)
    for ax, field, title in ((axes[0], "dwell_s", "Response to next request (dwell)"), (axes[1], "first_copy_ai_s", "Response to first copy")):
        for i, t in enumerate(toks):
            vals = [mine.fnum(w["t"].get(field)) for (d, _), v in S.items() if d == "NIRVANA" for w in v if w["tok"] == t]
            vals = np.array([x for x in vals if x is not None])
            ax.scatter(i + rng.uniform(-0.2, 0.2, len(vals)), np.log10(vals + 1), s=6, color=COL[t], edgecolor=INK2, linewidth=0.2, alpha=0.9)
            m = float(np.median(vals))
            ax.plot([i - 0.32, i + 0.32], [math.log10(m + 1)] * 2, color=INK, lw=1.8)
            ax.text(i + 0.34, math.log10(m + 1) + 0.07, f"{m:.0f}", fontsize=7, color=INK, weight="bold", ha="right", va="bottom", bbox=dict(fc="white", ec="none", pad=0.4, alpha=0.8))
        ticks = [1, 10, 60, 300, 1200]
        ax.set_yticks([math.log10(t + 1) for t in ticks], [str(t) for t in ticks])
        ax.set_xticks(range(4), [names[t] for t in toks], fontsize=6.9)
        ax.set_title(title, loc="left")
    axes[0].set_ylabel("seconds (log scale; bar = median)", labelpad=2)
    ax = axes[2]
    x = np.array([0, 1])
    ax.bar(x - 0.18, [44.1, 156.1], 0.34, color=COL["SLb"])
    support_bar(ax, x + 0.18, [43.5, 308.25], 0.34)
    for xi, a, b in zip(x, [44.1, 156.1], [43.5, 308.25]):
        ax.text(xi - 0.18, a + 6, f"{a:.0f}", ha="center", fontsize=7, color=INK)
        ax.text(xi + 0.18, b + 6, f"{b:.0f}", ha="center", fontsize=7, color=INK)
    ax.set_xticks(x, ["under 50\ntyped", "50+\ntyped"], fontsize=7)
    ax.set_ylabel("median dwell (s)", labelpad=2)
    ax.set_title("The gap is typing", loc="left")
    ax.legend(handles=[Patch(facecolor=COL["SLb"], label="behavior-based"), Patch(facecolor=COL["AUG"], hatch="\\\\\\\\", edgecolor=COL["OFF"], label="support")],
              frameon=False, fontsize=6.8, loc="upper left", handlelength=1.3)
    fig.subplots_adjust(left=0.085, right=0.99, top=0.91, bottom=0.19, wspace=0.3)
    save(fig, "dwell")


def fig_signals():
    h = 3.95
    fig, ax = canvas(h)
    x0, x1 = 0.55, 5.85
    base = 2.3
    ax.annotate("", (x1, base), (x0, base), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.9))
    ax.annotate("", (x0, h - 0.1), (x0, base), arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.9))
    ax.text(x1, base - 0.13, "time in the session (schematic)", fontsize=7, ha="right", color=INK2, va="center")
    ax.text(0.34, base + 0.42, "characters in the editor", fontsize=7, rotation=90, color=INK2, va="center", ha="center")
    path = [(x0, base + 0.06), (1.65, base + 0.08), (2.25, base + 0.2), (2.75, base + 0.3), (2.75, base + 0.92), (4.05, base + 0.95), (5.5, base + 1.26)]
    ax.plot([p[0] for p in path], [p[1] for p in path], color=INK, lw=1.4)
    # signal 1
    s1 = 1.1
    ax.plot([s1, s1], [base + 0.04, base + 0.42], color=COL["SLb"], lw=1.2)
    ax.plot([s1], [base + 0.07], marker="o", color=COL["SLb"], ms=6)
    box(ax, 0.68, base + 0.45, 2.0, 0.98, "Signal 1: ask on a near-empty page\nRequest sent with under 200 characters\nin the editor.\nFeedback before showing generated\nprose: ask for the claim the writer\nwants to make.", fs=7.2, ec=COL["SLb"], lw=1.0, align="left")
    # signal 2
    s2 = 3.2
    ax.plot([2.75, s2], [base + 0.62, base + 1.0], color=COL["SLb"], lw=1.0, alpha=0)
    ax.annotate("", (2.76, base + 0.62), (s2, base + 0.62), arrowprops=dict(arrowstyle="-", color=COL["SLb"], lw=1.2))
    ax.plot([2.76], [base + 0.62], marker="o", color=COL["SLb"], ms=6)
    box(ax, s2, base + 0.1, 2.5, 0.72, "Signal 2: large paste, little typing\n200+ characters pasted, under 50 typed before\nthe next request. Feedback: ask which sentence\nof it the writer would defend or change.", fs=7.2, ec=COL["SLb"], lw=1.0, align="left")
    # chart
    rows = [("Large paste, little typing", 55, 64.0, 32.7, "\u22120.41"), ("Ask on a near-empty page", 101, 58.7, 44.9, "\u22120.28"), ("Either of the two (proposed)", 140, 55.9, 63.3, "not computed"),
            ("Quick return to chat", 122, 54.8, 40.8, "\u22120.11"), ("Paste, then straight back", 23, 66.7, 14.3, "\u22120.23")]
    chart = fig.add_axes([0.32, 0.095, 0.46, 0.42])
    y = np.arange(len(rows))[::-1]
    for yi, (name, fired, prec, rec, rho) in zip(y, rows):
        chart.barh(yi + 0.18, prec, 0.33, color="#444444")
        chart.barh(yi - 0.18, rec, 0.33, color="#FFFFFF", hatch="....", edgecolor="#444444", lw=0.6)
        chart.text(prec + 1, yi + 0.18, f"{prec:.0f}", va="center", fontsize=7, color=INK)
        chart.text(rec + 1, yi - 0.18, f"{rec:.0f}", va="center", fontsize=7, color=INK)
        chart.text(-2, yi, name, ha="right", va="center", fontsize=7.3, color=INK, weight="bold" if "two" in name else "normal")
        chart.text(101, yi, f"fired {fired}; rho {rho}" if rho != "not computed" else f"fired {fired}", va="center", fontsize=7, color=INK2)
    chart.axvline(39.5, color=INK2, lw=0.9, ls="--")
    chart.text(39.5, len(rows) - 0.42, "base rate 39.5", fontsize=7, color=INK2, ha="center", va="bottom")
    chart.set_xlim(0, 100)
    chart.set_ylim(-0.6, len(rows) - 0.4)
    chart.set_yticks([])
    chart.spines["left"].set_color(RULE)
    chart.set_xlabel("% of surrender-leaning, by AI-coded labels", labelpad=1)
    chart.legend(handles=[Patch(facecolor="#444444", label="precision"), Patch(facecolor="white", hatch="....", edgecolor="#444444", label="recall")],
                 frameon=False, fontsize=7, loc="lower right", bbox_to_anchor=(1.0, 0.02), handlelength=1.4)
    save(fig, "signals")


def main():
    OUT.mkdir(exist_ok=True)
    S, out = mine.load()
    fig_flow()
    fig_anatomy()
    fig_worked()
    fig_concept()
    fig_categories(S)
    fig_archetypes(S)
    fig_after()
    fig_outcome()
    fig_own_work(S)
    fig_dwell(S)
    fig_signals()
    (OUT / "figure_text.txt").write_text("\n".join(TEXTS) + "\n", encoding="utf-8")
    print("figures written:", len(list(OUT.glob("*.pdf"))))


main()
