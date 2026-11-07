"""Bet 9 (0010): session and temporal patterns for the theses. Whole sessions only (NIRVANA 71, WildChat 35).
Inputs: frozen-v1.2 categories (results/v12_final), v1.1 codes, the derived timing and outcome facts (derived/).
Every order claim is tested against a within-session shuffle (seed 216, 2,000 shuffles), which keeps each
session's make-up and moves only the order. Writes results/mining/*.csv, results/mining.json, results/mining.md.

Window tokens: SL is split by the rule that fired, because Bet 8 found the two kinds sit in different places:
  SLr  surrender-leaning by R16 (asked for generation, kept iterating or accepting in chat: a request-only basis)
  SLb  surrender-leaning by any other rule (a behavior basis: unchecked paste, surface-only work on AI text, ...)
  OFF, AUG, NEU, IND as in v1.2."""
import math, os, random
from collections import Counter, defaultdict
from common import (SL, OF, AU, NE, IN, SUPPORT, FP, RES, read_csv, load_windows, sessions, md_table, pct,
                    write_csv, write_json, write_text)

SEED, PERMS, BOOT = 216, 2000, 1000
TOK = ["SLr", "SLb", "OFF", "AUG", "NEU", "IND"]
SIDE = {"SLr": "S", "SLb": "S", "OFF": "P", "AUG": "P", "NEU": "X", "IND": "X"}
OUT = os.path.join(RES, "mining")


# ---------- loading ----------

def token(w):
    if w["category"] == SL:
        return "SLr" if w["rule"] == "R16" else "SLb"
    return {OF: "OFF", AU: "AUG", NE: "NEU", IN: "IND"}[w["category"]]


def load():
    ws = load_windows("final")
    src = {}
    for p in ("sessions/results/final_labels_nirvana.csv", "wildchat/results/final_labels_wildchat.csv"):
        for r in read_csv(os.path.join(FP, p)):
            src[r["window_id"]] = r
    tn = {r["window_id"]: r for r in read_csv(os.path.join(FP, "analysis", "derived", "timing_nirvana.csv"))}
    tw = {r["window_id"]: r for r in read_csv(os.path.join(FP, "analysis", "derived", "timing_wildchat.csv"))}
    S = sessions(ws)
    for v in S.values():
        n = len(v)
        for i, w in enumerate(v):
            w["tok"] = token(w)
            w["side"] = SIDE[w["tok"]]
            w["i"], w["n"] = i, n
            w["rel"] = (i + 0.5) / n
            s = src[w["window_id"]]
            w["process"], w["operation"] = s["process"], s["operation"]
            w["pow"] = w["prior_own_work"]
            w["t"] = tn.get(w["window_id"]) or tw.get(w["window_id"]) or {}
    out = {r["session_id"]: r for r in read_csv(os.path.join(FP, "analysis", "derived", "outcome_nirvana.csv"))}
    return S, out


def fnum(x):
    return float(x) if x not in ("", None) else None


def med(xs):
    xs = sorted(xs)
    if not xs:
        return None
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2


def q(xs, p):
    xs = sorted(xs)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    lo, hi = math.floor(k), math.ceil(k)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)


def r2(x):
    return None if x is None else round(x, 3)


def ranks(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else 0.0


def spearman_p(x, y, seed=SEED, n=PERMS):
    """Two-sided permutation p for Spearman's rho (sessions are independent units)."""
    rng, obs, ge = random.Random(seed), abs(spearman(x, y)), 0
    y = list(y)
    for _ in range(n):
        rng.shuffle(y)
        ge += abs(spearman(x, y)) >= obs - 1e-12
    return (ge + 1) / (n + 1)


def shuffles(S, seed=SEED, n=PERMS):
    """Yield n within-session shuffles of the token sequences (same rng stream for every caller)."""
    rng = random.Random(seed)
    seqs = [[w["tok"] for w in v] for v in S.values()]
    for _ in range(n):
        out = []
        for s in seqs:
            s = s[:]
            rng.shuffle(s)
            out.append(s)
        yield out


# ---------- 1. archetypes ----------

def sub_cost(a, b):
    if a == b:
        return 0.0
    if SIDE[a] == SIDE[b] or "X" in (SIDE[a], SIDE[b]):
        return 1.0
    return 2.0


def om(a, b):
    """Optimal-matching distance (indel 1, substitution 1 within a side or to NEU/IND, 2 across SL/support),
    normalised by len(a)+len(b), so 0 is identical and 1 is nothing shared."""
    la, lb = len(a), len(b)
    d = [[0.0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + sub_cost(a[i - 1], b[j - 1]))
    return d[la][lb] / (la + lb)


def upgma(D, k):
    """Average-linkage agglomerative clustering to k clusters; ties broken by lowest index (deterministic)."""
    cl = {i: [i] for i in range(len(D))}
    while len(cl) > k:
        best = None
        keys = sorted(cl)
        for x in range(len(keys)):
            for y in range(x + 1, len(keys)):
                a, b = cl[keys[x]], cl[keys[y]]
                d = sum(D[i][j] for i in a for j in b) / (len(a) * len(b))
                if best is None or d < best[0] - 1e-12:
                    best = (d, keys[x], keys[y])
        _, a, b = best
        cl[a] = cl[a] + cl.pop(b)
    lab = [0] * len(D)
    for c, (_, mem) in enumerate(sorted(cl.items(), key=lambda kv: min(kv[1]))):
        for i in mem:
            lab[i] = c
    return lab


def silhouette(D, lab):
    n, s = len(D), []
    for i in range(n):
        own = [D[i][j] for j in range(n) if lab[j] == lab[i] and j != i]
        if not own:
            s.append(0.0)
            continue
        a = sum(own) / len(own)
        b = min(sum(D[i][j] for j in range(n) if lab[j] == c) / sum(1 for j in range(n) if lab[j] == c)
                for c in set(lab) if c != lab[i])
        s.append((b - a) / max(a, b) if max(a, b) else 0.0)
    return sum(s) / n


def name_archetype(p):
    """Names from the cluster profile by fixed thresholds (shares are mean shares of a session's windows)."""
    sl, sup = p["share_SLr"] + p["share_SLb"], p["share_OFF"] + p["share_AUG"]
    if p["share_IND"] + p["share_NEU"] >= 0.5:
        return "Unresolved"
    if sl >= 0.5 and p["share_SLr"] >= p["share_SLb"]:
        return "Delegate in chat"
    if sl >= 0.5:
        return "One-shot paste" if p["mean_windows"] <= 1.5 else "Paste into the draft"
    if sup >= 0.5:
        return "Long working session" if p["mean_windows"] >= 6 else "Short support visit"
    return "Mixed"


def archetypes(S):
    keys = list(S)
    seqs = [[w["tok"] for w in S[k]] for k in keys]
    D = [[om(a, b) for b in seqs] for a in seqs]
    sil = {k: silhouette(D, upgma(D, k)) for k in range(3, 8)}
    k = max(sil, key=lambda x: (round(sil[x], 6), -x))
    lab = upgma(D, k)
    rows, prof = [], []
    for c in range(k):
        mem = [i for i in range(len(keys)) if lab[i] == c]
        p = {"cluster": c, "sessions": len(mem),
             "NIRVANA": sum(keys[i][0] == "NIRVANA" for i in mem), "WildChat": sum(keys[i][0] == "WildChat" for i in mem),
             "mean_windows": round(sum(len(seqs[i]) for i in mem) / len(mem), 2)}
        for t in TOK:
            p[f"share_{t}"] = round(sum(seqs[i].count(t) / len(seqs[i]) for i in mem) / len(mem), 3)
        p["mean_switches"] = round(sum(switches(seqs[i]) for i in mem) / len(mem), 2)
        p["first_SL"] = sum(seqs[i][0] in ("SLr", "SLb") for i in mem)
        p["first_support"] = sum(seqs[i][0] in ("OFF", "AUG") for i in mem)
        p["name"] = name_archetype(p)
        prof.append(p)
    # Two clusters can earn one name; keep them apart by cluster number.
    seen = Counter(p["name"] for p in prof)
    for p in prof:
        if seen[p["name"]] > 1:
            p["name"] += f" ({p['cluster']})"
    for i, kk in enumerate(keys):
        rows.append({"dataset": kk[0], "session_id": kk[1], "cluster": lab[i], "archetype": prof[lab[i]]["name"],
                     "n_windows": len(seqs[i]), "sequence": " ".join(seqs[i])})
    return {"k": k, "silhouette": {str(a): round(b, 4) for a, b in sil.items()}, "profiles": prof}, rows


def switches(s):
    k = [SIDE[t] for t in s if SIDE[t] != "X"]
    return sum(a != b for a, b in zip(k, k[1:]))


# ---------- 2. over-represented n-grams ----------

def grams(seqs, n):
    c = Counter()
    for s in seqs:
        for i in range(len(s) - n + 1):
            c[tuple(s[i:i + n])] += 1
    return c


def ngram_test(S, seq_fn, nmin=2, nmax=4, min_obs=5):
    seqs = [seq_fn(v) for v in S.values()]
    obs = {n: grams(seqs, n) for n in range(nmin, nmax + 1)}
    cand = {(n, g) for n in obs for g, c in obs[n].items() if c >= min_obs}
    tot, ge = Counter(), Counter()
    rng = random.Random(SEED)
    for _ in range(PERMS):
        sh = []
        for s in seqs:
            s = s[:]
            rng.shuffle(s)
            sh.append(s)
        gs = {n: grams(sh, n) for n in range(nmin, nmax + 1)}
        for n, g in cand:
            tot[(n, g)] += gs[n][g]
            ge[(n, g)] += gs[n][g] >= obs[n][g]
    rows = []
    for n, g in sorted(cand, key=lambda x: (x[0], x[1])):
        e = tot[(n, g)] / PERMS
        rows.append({"n": n, "gram": " > ".join(g), "observed": obs[n][g], "expected": round(e, 2),
                     "ratio": round(obs[n][g] / e, 2) if e else None, "p_over": round((ge[(n, g)] + 1) / (PERMS + 1), 4)})
    rows.sort(key=lambda r: (r["p_over"], -r["observed"]))
    return rows, len(cand)


def sig(w):
    """Code signature: decision and uptake codes, the two that say what happened to the output."""
    return f"{w['D']}{w['U']}"


# ---------- 3. triggers and the lagged model ----------

FEATS = [("tok", lambda w: w["tok"]), ("D", lambda w: w["D"]), ("U", lambda w: w["U"]), ("V", lambda w: w["V"]),
         ("F", lambda w: w["F"]), ("prior_own_work", lambda w: w["pow"]), ("process", lambda w: w["process"])]


def pairs(S, drop_x=True):
    """Adjacent (current, next) pairs. drop_x removes NEU/IND first, so a pair is the next substantive window."""
    out = []
    for (d, sid), v in S.items():
        k = [w for w in v if not (drop_x and w["side"] == "X")]
        out += [(a, b, d) for a, b in zip(k, k[1:])]
    return out


def triggers(S):
    P = pairs(S)
    res = {}
    for frm, label in (("S", "from_SL"), ("P", "from_support")):
        sub = [(a, b) for a, b, _ in P if a["side"] == frm]
        stay = [a for a, b in sub if b["side"] == frm]
        move = [a for a, b in sub if b["side"] != frm]
        tab = {}
        for name, f in FEATS:
            vals = sorted({f(a) for a, _ in sub})
            tab[name] = [{"value": v, "stay": sum(f(a) == v for a in stay), "switch": sum(f(a) == v for a in move),
                          "switch_rate": r2(sum(f(a) == v for a in move) / max(1, sum(f(a) == v for a, _ in sub)))}
                         for v in vals]
        # Where does the switch window land (next window's codes)?
        tab["next_D_U_when_switch"] = Counter(f"{b['D']}/{b['U']}" for a, b in sub if b["side"] != frm).most_common(8)
        tab["next_D_U_when_switch"] = [list(x) for x in tab["next_D_U_when_switch"]]
        res[label] = {"pairs": len(sub), "stay": len(stay), "switch": len(move), "by_feature": tab}
    return res


def logit_fit(X, y, iters=50, ridge=1e-6):
    """Logistic regression by Newton-Raphson (tiny ridge for stability). Pure Python; few predictors."""
    p = len(X[0])
    b = [0.0] * p
    for _ in range(iters):
        g = [0.0] * p
        H = [[ridge * (i == j) for j in range(p)] for i in range(p)]
        for x, t in zip(X, y):
            z = sum(bi * xi for bi, xi in zip(b, x))
            m = 1 / (1 + math.exp(-max(-30, min(30, z))))
            for i in range(p):
                g[i] += (t - m) * x[i]
                for j in range(p):
                    H[i][j] += m * (1 - m) * x[i] * x[j]
        step = solve(H, g)
        b = [bi + si for bi, si in zip(b, step)]
        if max(abs(s) for s in step) < 1e-9:
            break
    return b


def solve(A, v):
    n = len(v)
    M = [row[:] + [v[i]] for i, row in enumerate(A)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[c][c]:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] if M[i][i] else 0.0 for i in range(n)]


PRED = [("intercept", lambda a, d: 1.0),
        ("current SL by request only (SLr)", lambda a, d: float(a["tok"] == "SLr")),
        ("current SL by behavior (SLb)", lambda a, d: float(a["tok"] == "SLb")),
        ("current output stayed in chat (U4/U5/U8)", lambda a, d: float(a["U"] in ("U4", "U5", "U8"))),
        ("writer's own draft visible (VISIBLE_DRAFT)", lambda a, d: float(a["pow"] == "VISIBLE_DRAFT")),
        ("WildChat (no editor)", lambda a, d: float(d == "WildChat")),
        ("relative position (0-1)", lambda a, d: a["rel"])]


def lagged_model(S):
    """P(next substantive window is SL) from the current substantive window. Session-cluster bootstrap CIs."""
    P = pairs(S)
    by = defaultdict(list)
    for a, b, d in P:
        by[(d, a["session_id"])].append(([f(a, d) for _, f in PRED], float(b["side"] == "S")))
    keys = sorted(by)
    X = [x for k in keys for x, _ in by[k]]
    y = [t for k in keys for _, t in by[k]]
    b = logit_fit(X, y)
    rng = random.Random(SEED)
    boots = []
    for _ in range(BOOT):
        ks = [keys[rng.randrange(len(keys))] for _ in keys]
        Xb = [x for k in ks for x, _ in by[k]]
        yb = [t for k in ks for _, t in by[k]]
        if len(set(yb)) < 2:
            continue
        boots.append(logit_fit(Xb, yb, iters=25))
    rows = []
    for i, (name, _) in enumerate(PRED):
        bs = sorted(x[i] for x in boots)
        lo, hi = q(bs, 0.025), q(bs, 0.975)
        rows.append({"predictor": name, "odds_ratio": r2(math.exp(b[i])),
                     "ci95_low": r2(math.exp(max(-20, lo))), "ci95_high": r2(math.exp(min(20, hi)))})
    # Simple conditional rates for the reader.
    cond = []
    for name, f in PRED[1:6]:
        on = [(a, bb) for a, bb, d in P if f(a, d) == 1.0]
        off = [(a, bb) for a, bb, d in P if f(a, d) == 0.0]
        cond.append({"feature": name, "n_on": len(on), "next_SL_if_on": r2(sum(bb["side"] == "S" for _, bb in on) / max(1, len(on))),
                     "n_off": len(off), "next_SL_if_off": r2(sum(bb["side"] == "S" for _, bb in off) / max(1, len(off)))})
    return {"n_pairs": len(y), "n_sessions": len(keys), "next_SL_rate": r2(sum(y) / len(y)), "bootstraps": len(boots),
            "coefficients": rows, "conditional": cond}


# ---------- 4. process stage ----------

def stage(S, arch_of):
    W = [w for v in S.values() for w in v]
    st = ["P", "T", "R", "M", "PX", "UNSETTLED"]
    cross = []
    for t in TOK:
        row = {"token": t}
        for s in st:
            row[s] = sum(w["tok"] == t and w["process"] == s for w in W)
        cross.append(row)
    by_stage = []
    for s in ("P", "T", "R"):
        ws = [w for w in W if w["process"] == s]
        by_stage.append({"stage": s, "windows": len(ws), "SL": sum(w["side"] == "S" for w in ws),
                         "SLr": sum(w["tok"] == "SLr" for w in ws), "SLb": sum(w["tok"] == "SLb" for w in ws),
                         "support": sum(w["side"] == "P" for w in ws),
                         "SL_share_of_determinate": r2(sum(w["side"] == "S" for w in ws) / max(1, sum(w["side"] != "X" for w in ws))),
                         "mean_rel_position": r2(sum(w["rel"] for w in ws) / len(ws)) if ws else None})
    # Stage order: mean position of P, T, R windows against the shuffle (multi-window sessions only).
    order = {}
    multi = {k: v for k, v in S.items() if len(v) > 1}
    for s in ("P", "T", "R"):
        obs = [w["rel"] for v in multi.values() for w in v if w["process"] == s]
        if not obs:
            continue
        rng, ge_l, ge_e, tot = random.Random(SEED), 0, 0, 0.0
        o = sum(obs) / len(obs)
        for _ in range(PERMS):
            vals = []
            for v in multi.values():
                ps = [w["process"] for w in v]
                rng.shuffle(ps)
                vals += [(i + 0.5) / len(v) for i, p in enumerate(ps) if p == s]
            m = sum(vals) / len(vals)
            tot += m
            ge_l += m >= o - 1e-12
            ge_e += m <= o + 1e-12
        order[s] = {"windows": len(obs), "mean_rel": r2(o), "shuffled_mean": r2(tot / PERMS),
                    "p_later": round((ge_l + 1) / (PERMS + 1), 4), "p_earlier": round((ge_e + 1) / (PERMS + 1), 4)}
    arch = []
    for a in sorted(set(arch_of.values())):
        ws = [w for k, v in S.items() if arch_of[k] == a for w in v]
        arch.append({"archetype": a, "windows": len(ws), **{s: sum(w["process"] == s for w in ws) for s in ("P", "T", "R", "M")}})
    return {"cross": cross, "by_stage": by_stage, "order": order, "by_archetype": arch}


# ---------- 5. own work ----------

def own_work(S, arch_of):
    W = [w for v in S.values() for w in v]
    bins = defaultdict(Counter)
    for w in W:
        if w["n"] > 1:
            bins[min(4, int(5 * w["rel"]))][w["pow"]] += 1
    traj = [{"bin": b, **dict(bins[b])} for b in range(5)]
    # NIRVANA editor length at each request, by relative position (chars of the writer's document so far).
    ed = defaultdict(list)
    for w in W:
        if w["dataset"] == "NIRVANA" and w["n"] > 1 and w["t"]:
            ed[min(4, int(5 * w["rel"]))].append(int(w["t"]["editor_chars_before"]))
    ed_rows = [{"bin": b, "windows": len(ed[b]), "median_editor_chars": med(ed[b])} for b in range(5)]
    # Typed and pasted characters after the response, by token (NIRVANA).
    tp = []
    for t in TOK:
        ws = [w for w in W if w["dataset"] == "NIRVANA" and w["tok"] == t and w["t"]]
        tp.append({"token": t, "windows": len(ws),
                   "median_typed": med([int(w["t"]["typed_chars"]) for w in ws]),
                   "median_pasted": med([int(w["t"]["pasted_chars"]) for w in ws]),
                   "share_any_paste": r2(sum(int(w["t"]["pasted_chars"]) > 0 for w in ws) / max(1, len(ws))),
                   "share_any_copy_from_ai": r2(sum(int(w["t"]["copies_from_ai"]) > 0 for w in ws) / max(1, len(ws)))})
    # Does own work before the first request predict the session's support share?
    first = []
    for (d, sid), v in S.items():
        det = [w for w in v if w["side"] != "X"]
        first.append({"dataset": d, "session_id": sid, "first_pow": v[0]["pow"],
                      "editor_chars_first": int(v[0]["t"]["editor_chars_before"]) if d == "NIRVANA" else None,
                      "minutes_before_first_ask": round(float(v[0]["t"]["request_s"]) / 60, 2) if d == "NIRVANA" else None,
                      "support_share": (sum(w["side"] == "P" for w in det) / len(det)) if det else None,
                      "SL_share": (sum(w["side"] == "S" for w in det) / len(det)) if det else None})
    grp = []
    for d in ("NIRVANA", "WildChat"):
        for p in sorted({r["first_pow"] for r in first if r["dataset"] == d}):
            rs = [r for r in first if r["dataset"] == d and r["first_pow"] == p and r["support_share"] is not None]
            grp.append({"dataset": d, "first_window_prior_own_work": p, "sessions": len(rs),
                        "mean_support_share": r2(sum(r["support_share"] for r in rs) / len(rs)) if rs else None,
                        "sessions_any_SL": sum(r["SL_share"] > 0 for r in rs)})
    nv = [r for r in first if r["dataset"] == "NIRVANA" and r["support_share"] is not None]
    corr = {}
    for f in ("editor_chars_first", "minutes_before_first_ask"):
        x, y = [r[f] for r in nv], [r["support_share"] for r in nv]
        corr[f] = {"sessions": len(nv), "spearman_rho_with_support_share": r2(spearman(x, y)), "p": round(spearman_p(x, y), 4)}
    # Pasting is common on both sides; what differs is whose content was pasted and what the writer did next.
    paste = []
    for dcode in ("D0", "D1", "D2", "D3", "D4"):
        ws = [w for w in W if w["dataset"] == "NIRVANA" and w["t"] and int(w["t"]["pasted_chars"]) > 0 and w["D"] == dcode]
        if ws:
            paste.append({"decision": dcode, "windows_with_paste": len(ws), **{t: sum(w["tok"] == t for w in ws) for t in TOK},
                          "median_typed_after": med([int(w["t"]["typed_chars"]) for w in ws]),
                          "median_dwell": r2(med([float(w["t"]["dwell_s"]) for w in ws if w["t"]["dwell_s"] != ""]))})
    return {"paste_by_decision": paste, "trajectory_prior_own_work": traj, "editor_chars_by_position": ed_rows, "typed_pasted_by_token": tp,
            "first_window_groups": grp, "nirvana_first_ask_correlations": corr}


# ---------- 6. time to event ----------

def km(times):
    """Kaplan-Meier: times = [(t, event)], t = windows elapsed (1-based index of the event, or length if censored)."""
    ts = sorted({t for t, _ in times})
    s, out, at = 1.0, [{"t": 0, "surv": 1.0, "at_risk": len(times)}], len(times)
    for t in ts:
        d = sum(1 for tt, e in times if tt == t and e)
        n = sum(1 for tt, _ in times if tt >= t)
        if n:
            s *= 1 - d / n
        out.append({"t": t, "surv": round(s, 4), "at_risk": n, "events": d})
    return out


def survival(S):
    res = {}
    for d in ("NIRVANA", "WildChat", "both"):
        V = [v for (dd, _), v in S.items() if d in ("both", dd)]
        t_first = []
        for v in V:
            i = next((k for k, w in enumerate(v) if w["side"] == "S"), None)
            t_first.append((i + 1, True) if i is not None else (len(v), False))
        t_b = []
        for v in V:
            i = next((k for k, w in enumerate(v) if w["tok"] == "SLb"), None)
            t_b.append((i + 1, True) if i is not None else (len(v), False))
        back = []
        for v in V:
            i = next((k for k, w in enumerate(v) if w["side"] == "S"), None)
            if i is None:
                continue
            j = next((k for k in range(i + 1, len(v)) if v[k]["side"] == "P"), None)
            back.append((j - i, True) if j is not None else (len(v) - 1 - i, False))
        res[d] = {"to_first_SL": km(t_first), "to_first_SLb": km(t_b), "SL_to_support": km(back),
                  "n_sessions": len(V), "first_SL_events": sum(e for _, e in t_first),
                  "SL_sessions_with_window_after": sum(1 for t, _ in back if t > 0 or _),
                  "returned_to_support": sum(e for _, e in back)}
    # Return to support by which kind of SL came first, and by editor presence.
    by_kind = []
    for kind in ("SLr", "SLb"):
        for d in ("NIRVANA", "WildChat"):
            n = ret = after = 0
            for (dd, _), v in S.items():
                if dd != d:
                    continue
                i = next((k for k, w in enumerate(v) if w["side"] == "S"), None)
                if i is None or v[i]["tok"] != kind:
                    continue
                n += 1
                after += i + 1 < len(v)
                ret += any(w["side"] == "P" for w in v[i + 1:])
            by_kind.append({"first_SL_kind": kind, "dataset": d, "sessions": n, "with_a_later_window": after, "returned_to_support": ret})
    res["return_by_first_kind"] = by_kind
    return res


# ---------- 7. latency ----------

def strat_perm_median(S, val, grp_a, grp_b, seed=SEED, n=PERMS):
    """Difference in median of val between windows in group a and b; null shuffles tokens within each session."""
    rng = random.Random(seed)
    items = [[(w, val(w)) for w in v] for v in S.values()]

    def stat(assign):
        a = [x for s, toks in assign for (w, x), t in zip(s, toks) if x is not None and t in grp_a]
        b = [x for s, toks in assign for (w, x), t in zip(s, toks) if x is not None and t in grp_b]
        if not a or not b:
            return None, len(a), len(b)
        return med(a) - med(b), len(a), len(b)

    base = [(s, [w["tok"] for w, _ in s]) for s in items]
    obs, na, nb = stat(base)
    if obs is None:
        return {"n_a": na, "n_b": nb}
    ge = 0
    for _ in range(n):
        sh = []
        for s, toks in base:
            t = toks[:]
            rng.shuffle(t)
            sh.append((s, t))
        v, _, _ = stat(sh)
        ge += v is not None and abs(v) >= abs(obs) - 1e-12
    return {"n_a": na, "n_b": nb, "median_diff": r2(obs), "p_two_sided": round((ge + 1) / (n + 1), 4)}


def latency(S):
    SN = {k: v for k, v in S.items() if k[0] == "NIRVANA"}
    SW = {k: v for k, v in S.items() if k[0] == "WildChat"}
    fields = [("first_action_s", "NIRVANA"), ("first_copy_ai_s", "NIRVANA"), ("first_edit_s", "NIRVANA"),
              ("dwell_s", "NIRVANA"), ("ai_reply_to_next_ai_reply_s", "WildChat")]
    desc = []
    for f, d in fields:
        Sd = SN if d == "NIRVANA" else SW
        for t in TOK + ["SL", "support"]:
            xs = [fnum(w["t"].get(f)) for v in Sd.values() for w in v
                  if (w["tok"] == t or (t == "SL" and w["side"] == "S") or (t == "support" and w["side"] == "P"))]
            xs = [x for x in xs if x is not None]
            desc.append({"measure": f, "dataset": d, "group": t, "windows": len(xs), "median": r2(med(xs)),
                         "q25": r2(q(xs, .25)), "q75": r2(q(xs, .75))})
    tests = []
    for f, d in fields:
        Sd = SN if d == "NIRVANA" else SW
        val = lambda w, f=f: fnum(w["t"].get(f))
        for a, b, lab in ((("SLr", "SLb"), ("OFF", "AUG"), "SL vs support"), (("SLb",), ("OFF", "AUG"), "SLb vs support"),
                          (("SLr",), ("OFF", "AUG"), "SLr vs support"), (("SLb",), ("SLr",), "SLb vs SLr")):
            tests.append({"measure": f, "dataset": d, "contrast": lab, **strat_perm_median(Sd, val, a, b)})
    # Fast pastes: copy from chat within 10 s of the response, by token (NIRVANA).
    fast = []
    for t in TOK:
        ws = [w for v in SN.values() for w in v if w["tok"] == t]
        c = [fnum(w["t"].get("first_copy_ai_s")) for w in ws]
        fast.append({"token": t, "windows": len(ws), "copied_at_all": sum(x is not None for x in c),
                     "copied_within_10s": sum(x is not None and x <= 10 for x in c),
                     "copied_within_30s": sum(x is not None and x <= 30 for x in c)})
    # Same contrasts on code signatures that matter for the theses.
    sigs = []
    for name, test in (("D4 + U1 (whole paste, no change)", lambda w: w["D"] == "D4" and w["U"] == "U1"),
                       ("D3 (partial take or revision)", lambda w: w["D"] == "D3"),
                       ("U7 (own new text)", lambda w: w["U"] == "U7"),
                       ("U4 (iterate in chat)", lambda w: w["U"] == "U4"),
                       ("D1 (writer's content)", lambda w: w["D"] == "D1")):
        ws = [w for v in SN.values() for w in v if test(w)]
        row = {"signature": name, "windows": len(ws)}
        for f in ("first_action_s", "first_copy_ai_s", "dwell_s"):
            xs = [fnum(w["t"].get(f)) for w in ws]
            xs = [x for x in xs if x is not None]
            row[f"{f}_n"] = len(xs)
            row[f"{f}_median"] = r2(med(xs))
        sigs.append(row)
    return {"describe": desc, "tests": tests, "fast_copy": fast, "signatures": sigs}


# ---------- 8. essay outcome ----------

def outcome(S, out, arch_of):
    rows = []
    for (d, sid), v in S.items():
        if d != "NIRVANA" or sid not in out:
            continue
        n = len(v)
        o = out[sid]
        rows.append({"session_id": sid, "archetype": arch_of[(d, sid)], "windows": n,
                     "SL_share": sum(w["side"] == "S" for w in v) / n,
                     "SLb_share": sum(w["tok"] == "SLb" for w in v) / n,
                     "SLr_share": sum(w["tok"] == "SLr" for w in v) / n,
                     "support_share": sum(w["side"] == "P" for w in v) / n,
                     "any_SLb": any(w["tok"] == "SLb" for w in v),
                     "gpt_final": fnum(o["GPT Final %"]), "ownership": fnum(o["Perceived Ownership"]),
                     "self_efficacy": fnum(o["Self Efficacy Score"]), "total_words": fnum(o["Total Words"])})
    cor = []
    for x in ("SL_share", "SLb_share", "SLr_share", "support_share"):
        for y in ("gpt_final", "ownership", "self_efficacy"):
            rs = [r for r in rows if r[y] is not None]
            xs, ys = [r[x] for r in rs], [r[y] for r in rs]
            cor.append({"session_measure": x, "outcome": y, "sessions": len(rs), "spearman_rho": r2(spearman(xs, ys)),
                        "p": round(spearman_p(xs, ys), 4)})
    arch = []
    for a in sorted({r["archetype"] for r in rows}):
        rs = [r for r in rows if r["archetype"] == a]
        g = [r["gpt_final"] for r in rs if r["gpt_final"] is not None]
        ow = [r["ownership"] for r in rs if r["ownership"] is not None]
        arch.append({"archetype": a, "sessions": len(rs), "median_gpt_final": r2(med(g)), "q25": r2(q(g, .25)), "q75": r2(q(g, .75)),
                     "median_ownership": r2(med(ow))})
    split = []
    for flag in (True, False):
        rs = [r for r in rows if r["any_SLb"] == flag and r["gpt_final"] is not None]
        g = [r["gpt_final"] for r in rs]
        split.append({"any_behavior_SL": flag, "sessions": len(rs), "median_gpt_final": r2(med(g)),
                      "median_ownership": r2(med([r["ownership"] for r in rs if r["ownership"] is not None]))})
    return {"correlations": cor, "by_archetype": arch, "by_any_SLb": split}, rows


# ---------- 9. log-only triggers (NIRVANA) ----------

LOG_TRIGGERS = [
    # (name, test on the derived timing row, when it would fire). Thresholds fixed before counting.
    ("Large paste, little typing", lambda t: int(t["pasted_chars"]) >= 200 and int(t["typed_chars"]) < 50,
     "after a response, 200+ characters pasted into the editor and under 50 typed before the next request"),
    ("Quick return to chat", lambda t: t["dwell_s"] != "" and float(t["dwell_s"]) < 60 and int(t["typed_chars"]) < 50,
     "the next request comes within 60 s of the response, with under 50 characters typed"),
    ("Ask on a near-empty page", lambda t: int(t["editor_chars_before"]) < 200,
     "the request is sent while the editor holds under 200 characters"),
    ("Paste, then straight back", lambda t: int(t["pasted_chars"]) >= 200 and t["dwell_s"] != "" and float(t["dwell_s"]) < 90,
     "200+ characters pasted and the next request within 90 s"),
]


def log_triggers(S, out):
    W = [w for (d, _), v in S.items() if d == "NIRVANA" for w in v]
    rows = []
    for name, test, when in LOG_TRIGGERS:
        fired = [w for w in W if test(w["t"])]
        det = [w for w in fired if w["side"] != "X"]
        sl_all = [w for w in W if w["side"] == "S"]
        slb_all = [w for w in W if w["tok"] == "SLb"]
        sess = defaultdict(int)
        for w in fired:
            sess[w["session_id"]] += 1
        n_sess = len(sess)
        sids = sorted({w["session_id"] for w in W if w["session_id"] in out})
        x = [sess.get(s, 0) / sum(1 for w in W if w["session_id"] == s) for s in sids]
        y = [fnum(out[s]["GPT Final %"]) for s in sids]
        yo = [fnum(out[s]["Perceived Ownership"]) for s in sids]
        rows.append({"trigger": name, "fires_when": when, "windows_fired": len(fired), "of_windows": len(W),
                     "SL_among_fired_determinate": r2(sum(w["side"] == "S" for w in det) / len(det)) if det else None,
                     "SL_base_rate_determinate": r2(len(sl_all) / sum(1 for w in W if w["side"] != "X")),
                     "SL_windows_caught": r2(sum(w["side"] == "S" for w in fired) / len(sl_all)),
                     "SLb_windows_caught": r2(sum(w["tok"] == "SLb" for w in fired) / len(slb_all)),
                     "sessions_fired": n_sess,
                     "session_fire_rate_vs_gpt_final_rho": r2(spearman(x, y)), "p": round(spearman_p(x, y), 4),
                     "session_fire_rate_vs_ownership_rho": r2(spearman(x, yo)), "p_ownership": round(spearman_p(x, yo), 4)})
    return rows


# ---------- 10. robustness (checks the skeptic asked for) ----------

def robustness(S, out, arch_rows):
    W = [w for v in S.values() for w in v]
    R = {}
    # Stage within generation requests (F4) and outside them: is the stage result more than "asked for prose"?
    st = []
    for f4 in (True, False):
        for s_ in ("P", "T", "R"):
            ws = [w for w in W if (w["F"] == "F4") == f4 and w["process"] == s_ and w["side"] != "X"]
            st.append({"F4_request": f4, "stage": s_, "determinate": len(ws),
                       "SL_share": r2(sum(w["side"] == "S" for w in ws) / len(ws)) if ws else None})
    R["stage_by_F4"] = st
    R["T_windows_that_are_F4"] = [sum(w["process"] == "T" and w["F"] == "F4" for w in W), sum(w["process"] == "T" for w in W)]
    # Dwell with typing held low or high (NIRVANA): is the dwell gap anything more than typing time?
    SN = [w for (d, _), v in S.items() if d == "NIRVANA" for w in v if w["t"].get("dwell_s")]
    dt = []
    for lab, test in (("under 50 typed", lambda w: int(w["t"]["typed_chars"]) < 50), ("50+ typed", lambda w: int(w["t"]["typed_chars"]) >= 50)):
        for g, gt in (("SLb", lambda w: w["tok"] == "SLb"), ("support", lambda w: w["side"] == "P")):
            xs = [float(w["t"]["dwell_s"]) for w in SN if test(w) and gt(w)]
            dt.append({"typing": lab, "group": g, "windows": len(xs), "median_dwell": r2(med(xs))})
    R["dwell_by_typing"] = dt
    both = shorter = 0
    for (d, _), v in S.items():
        if d != "NIRVANA":
            continue
        a = [float(w["t"]["dwell_s"]) for w in v if w["side"] == "S" and w["t"].get("dwell_s")]
        b = [float(w["t"]["dwell_s"]) for w in v if w["side"] == "P" and w["t"].get("dwell_s")]
        if a and b:
            both += 1
            shorter += med(a) < med(b)
    R["dwell_within_session"] = {"sessions_with_both": both, "SL_median_shorter": shorter}
    # Editor text at first ask: multi-window sessions only.
    nv = []
    for (d, sid), v in S.items():
        det = [w for w in v if w["side"] != "X"]
        if d == "NIRVANA" and det and len(v) > 1:
            nv.append((int(v[0]["t"]["editor_chars_before"]), sum(w["side"] == "P" for w in det) / len(det)))
    R["editor_first_multi_window"] = {"sessions": len(nv), "rho": r2(spearman([a for a, _ in nv], [b for _, b in nv])),
                                      "p": round(spearman_p([a for a, _ in nv], [b for _, b in nv]), 4)}
    # Outcome links without one-window sessions, and ownership among sessions that have any SLb.
    rows = []
    for (d, sid), v in S.items():
        if d == "NIRVANA":
            rows.append((len(v), sum(w["tok"] == "SLb" for w in v) / len(v), fnum(out[sid]["GPT Final %"]), fnum(out[sid]["Perceived Ownership"])))
    mw = [r for r in rows if r[0] > 1]
    R["outcome_multi_window"] = {"sessions": len(mw), "SLb_vs_gpt_final_rho": r2(spearman([r[1] for r in mw], [r[2] for r in mw])),
                                 "SLb_vs_ownership_rho": r2(spearman([r[1] for r in mw], [r[3] for r in mw]))}
    any_b = [r for r in rows if r[1] > 0]
    R["ownership_among_any_SLb"] = {"sessions": len(any_b), "rho": r2(spearman([r[1] for r in any_b], [r[3] for r in any_b])),
                                    "p": round(spearman_p([r[1] for r in any_b], [r[3] for r in any_b]), 4)}
    # The two working log triggers together.
    Wn = [w for (d, _), v in S.items() if d == "NIRVANA" for w in v]
    fire = [w for w in Wn if LOG_TRIGGERS[0][1](w["t"]) or LOG_TRIGGERS[2][1](w["t"])]
    det = [w for w in fire if w["side"] != "X"]
    R["two_triggers_combined"] = {"windows_fired": len(fire), "of_windows": len(Wn),
                                  "SL_among_fired_determinate": r2(sum(w["side"] == "S" for w in det) / len(det)),
                                  "SL_caught": r2(sum(w["side"] == "S" for w in fire) / sum(w["side"] == "S" for w in Wn)),
                                  "SLb_caught": r2(sum(w["tok"] == "SLb" for w in fire) / sum(w["tok"] == "SLb" for w in Wn))}
    # Archetype stability over k.
    keys = list(S)
    seqs = [[w["tok"] for w in S[k]] for k in keys]
    D = [[om(a, b) for b in seqs] for a in seqs]
    base = {(r["dataset"], r["session_id"]): r["cluster"] for r in arch_rows}
    stab = []
    for k in (4, 5, 7):
        lab = upgma(D, k)
        same = 0
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                same += (lab[i] == lab[j]) == (base[keys[i]] == base[keys[j]])
        n = len(keys) * (len(keys) - 1) // 2
        stab.append({"k": k, "pair_agreement_with_k6": r2(same / n)})
    R["archetype_stability"] = stab
    return R


# ---------- report ----------

def main():
    S, out = load()
    assert len(S) == 106
    J = {}
    J["archetypes"], arow = archetypes(S)
    write_csv(os.path.join(OUT, "archetypes.csv"), arow)
    arch_of = {(r["dataset"], r["session_id"]): r["archetype"] for r in arow}
    J["ngrams_category"], ncat = ngram_test(S, lambda v: [w["tok"] for w in v])
    J["ngrams_signature"], nsig = ngram_test(S, lambda v: [sig(w) for w in v], nmin=2, nmax=3, min_obs=4)
    J["ngram_tests"] = {"category": ncat, "signature": nsig}
    write_csv(os.path.join(OUT, "ngrams_category.csv"), J["ngrams_category"])
    write_csv(os.path.join(OUT, "ngrams_signature.csv"), J["ngrams_signature"])
    J["triggers"] = triggers(S)
    J["lagged_model"] = lagged_model(S)
    J["stage"] = stage(S, arch_of)
    J["own_work"] = own_work(S, arch_of)
    J["survival"] = survival(S)
    J["latency"] = latency(S)
    J["outcome"], orow = outcome(S, out, arch_of)
    write_csv(os.path.join(OUT, "outcome_sessions.csv"),
              [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in orow])
    J["log_triggers"] = log_triggers(S, out)
    J["robustness"] = robustness(S, out, arow)
    write_json(os.path.join(RES, "mining.json"), J)
    write_text(os.path.join(RES, "mining.md"), report(J))


def report(J):
    A = J["archetypes"]
    md = ["# Session and temporal patterns (Bet 9)\n\nGenerated by `scripts/mine.py` from frozen-v1.2 categories, v1.1 codes and "
          "`derived/` timing and outcome facts. Whole sessions only (NIRVANA 71, WildChat 35). Order tests shuffle tokens within "
          f"each session ({PERMS} shuffles, seed {SEED}). Tokens: SLr = surrender-leaning by R16 (request-only basis), SLb = "
          "surrender-leaning by any other rule (behavior basis), OFF, AUG, NEU, IND.\n"]
    md.append(f"\n## 1. Archetypes\n\nOptimal-matching distance, average linkage; k chosen by the best mean silhouette over 3–7: "
              f"k = {A['k']} (silhouettes {A['silhouette']}). Names follow fixed thresholds in `name_archetype`.\n\n")
    md.append(md_table(["Cluster", "Name", "Sessions", "NIRVANA", "WildChat", "Mean windows", "SLr", "SLb", "OFF", "AUG", "NEU", "IND",
                        "Mean switches", "Starts SL", "Starts support"],
                       [[p["cluster"], p["name"], p["sessions"], p["NIRVANA"], p["WildChat"], p["mean_windows"], p["share_SLr"],
                         p["share_SLb"], p["share_OFF"], p["share_AUG"], p["share_NEU"], p["share_IND"], p["mean_switches"],
                         p["first_SL"], p["first_support"]] for p in A["profiles"]]))
    md.append(f"\n## 2. Over-represented n-grams\n\nCategory tokens, n = 2–4, observed ≥ 5: {J['ngram_tests']['category']} tested. "
              "Top 15 by p:\n\n")
    md.append(md_table(["n", "Sequence", "Observed", "Shuffled mean", "Ratio", "p (over)"],
                       [[r["n"], r["gram"], r["observed"], r["expected"], r["ratio"], r["p_over"]] for r in J["ngrams_category"][:15]]))
    md.append(f"\nCode signatures (decision + uptake), n = 2–3, observed ≥ 4: {J['ngram_tests']['signature']} tested. Top 15 by p:\n\n")
    md.append(md_table(["n", "Sequence", "Observed", "Shuffled mean", "Ratio", "p (over)"],
                       [[r["n"], r["gram"], r["observed"], r["expected"], r["ratio"], r["p_over"]] for r in J["ngrams_signature"][:15]]))
    T = J["triggers"]
    md.append("\n## 3. Triggers (NEU and IND removed; a pair is a window and the next substantive window)\n\n")
    for lab in ("from_SL", "from_support"):
        t = T[lab]
        md.append(f"**{lab}**: {t['pairs']} pairs, {t['stay']} stay, {t['switch']} switch.\n\n")
        for f in ("tok", "U", "D", "prior_own_work", "process"):
            md.append(f"By current window's `{f}`:\n\n" + md_table(["Value", "Stay", "Switch", "Switch rate"],
                      [[r["value"], r["stay"], r["switch"], r["switch_rate"]] for r in t["by_feature"][f]]) + "\n")
        md.append("Next window's decision/uptake when it switches:\n\n" + md_table(["D/U", "Count"], t["by_feature"]["next_D_U_when_switch"]) + "\n")
    L = J["lagged_model"]
    md.append(f"\n### Lagged model: next substantive window is SL\n\n{L['n_pairs']} pairs in {L['n_sessions']} sessions; base rate "
              f"{L['next_SL_rate']}. Logistic regression, 95% intervals from {L['bootstraps']} session-cluster bootstraps.\n\n")
    md.append(md_table(["Predictor", "Odds ratio", "95% low", "95% high"],
                       [[r["predictor"], r["odds_ratio"], r["ci95_low"], r["ci95_high"]] for r in L["coefficients"]]))
    md.append("\n" + md_table(["Current window feature", "n on", "Next SL if on", "n off", "Next SL if off"],
                              [[r["feature"], r["n_on"], r["next_SL_if_on"], r["n_off"], r["next_SL_if_off"]] for r in L["conditional"]]))
    G = J["stage"]
    md.append("\n## 4. Process stage (derived from operation: P planning, T translating, R reviewing, M monitoring)\n\n")
    md.append(md_table(["Stage", "Windows", "SL", "SLr", "SLb", "Support", "SL share of determinate", "Mean position"],
                       [[r["stage"], r["windows"], r["SL"], r["SLr"], r["SLb"], r["support"], r["SL_share_of_determinate"],
                         r["mean_rel_position"]] for r in G["by_stage"]]))
    md.append("\nStage order against the shuffle (multi-window sessions):\n\n" +
              md_table(["Stage", "Windows", "Mean position", "Shuffled", "p later", "p earlier"],
                       [[s, o["windows"], o["mean_rel"], o["shuffled_mean"], o["p_later"], o["p_earlier"]] for s, o in G["order"].items()]))
    md.append("\nStage by archetype (windows):\n\n" + md_table(["Archetype", "Windows", "P", "T", "R", "M"],
              [[r["archetype"], r["windows"], r["P"], r["T"], r["R"], r["M"]] for r in G["by_archetype"]]))
    O = J["own_work"]
    md.append("\n## 5. Own work\n\nprior_own_work by centred position bin (multi-window sessions):\n\n")
    pk = sorted({k for r in O["trajectory_prior_own_work"] for k in r if k != "bin"})
    md.append(md_table(["Bin"] + pk, [[r["bin"]] + [r.get(k, 0) for k in pk] for r in O["trajectory_prior_own_work"]]))
    md.append("\nNIRVANA editor length when each request is sent (median characters), by position bin:\n\n" +
              md_table(["Bin", "Windows", "Median chars"], [[r["bin"], r["windows"], r["median_editor_chars"]] for r in O["editor_chars_by_position"]]))
    md.append("\nNIRVANA typing and pasting after the response, by token:\n\n" +
              md_table(["Token", "Windows", "Median typed", "Median pasted", "Any paste", "Any copy from chat"],
                       [[r["token"], r["windows"], r["median_typed"], r["median_pasted"], r["share_any_paste"], r["share_any_copy_from_ai"]]
                        for r in O["typed_pasted_by_token"]]))
    md.append("\nNIRVANA windows with any paste into the editor, by decision code:\n\n" +
              md_table(["Decision", "Windows with paste"] + TOK + ["Median typed after", "Median dwell (s)"],
                       [[r["decision"], r["windows_with_paste"]] + [r[t] for t in TOK] + [r["median_typed_after"], r["median_dwell"]]
                        for r in O["paste_by_decision"]]))
    md.append("\nFirst window's prior_own_work and the session's support share (of determinate windows):\n\n" +
              md_table(["Dataset", "First window prior_own_work", "Sessions", "Mean support share", "Sessions with any SL"],
                       [[r["dataset"], r["first_window_prior_own_work"], r["sessions"], r["mean_support_share"], r["sessions_any_SL"]]
                        for r in O["first_window_groups"]]))
    md.append("\n" + md_table(["NIRVANA measure before first ask", "Sessions", "Spearman with support share", "p"],
                              [[k, v["sessions"], v["spearman_rho_with_support_share"], v["p"]] for k, v in O["nirvana_first_ask_correlations"].items()]))
    V = J["survival"]
    md.append("\n## 6. Time to event (windows)\n\n")
    rows = []
    for d in ("NIRVANA", "WildChat", "both"):
        s = V[d]
        f = lambda curve, t: next((c["surv"] for c in reversed(curve) if c["t"] <= t), 1.0)
        rows.append([d, s["n_sessions"], s["first_SL_events"], f(s["to_first_SL"], 1), f(s["to_first_SL"], 3),
                     f(s["to_first_SLb"], 3), s["returned_to_support"]])
    md.append(md_table(["Dataset", "Sessions", "Sessions with SL", "No SL after window 1", "No SL after window 3",
                        "No SLb after window 3", "SL sessions that return to support"], rows))
    md.append("\nReturn to support by the kind of the first SL window:\n\n" +
              md_table(["First SL kind", "Dataset", "Sessions", "With a later window", "Returned to support"],
                       [[r["first_SL_kind"], r["dataset"], r["sessions"], r["with_a_later_window"], r["returned_to_support"]]
                        for r in V["return_by_first_kind"]]))
    Lt = J["latency"]
    md.append("\n## 7. Latency (seconds)\n\nNIRVANA: response to first action, to first copy from chat, to first editor edit, and to the "
              "next request (dwell). WildChat: AI reply to the next AI reply.\n\n")
    md.append(md_table(["Measure", "Dataset", "Group", "Windows", "Median", "Q25", "Q75"],
                       [[r["measure"], r["dataset"], r["group"], r["windows"], r["median"], r["q25"], r["q75"]]
                        for r in Lt["describe"] if r["windows"]]))
    md.append("\nMedian differences, tokens shuffled within session:\n\n" +
              md_table(["Measure", "Dataset", "Contrast", "n a", "n b", "Median diff", "p"],
                       [[r["measure"], r["dataset"], r["contrast"], r["n_a"], r["n_b"], r.get("median_diff"), r.get("p_two_sided")]
                        for r in Lt["tests"]]))
    md.append("\nNIRVANA copies from chat, by token:\n\n" +
              md_table(["Token", "Windows", "Copied", "Within 10 s", "Within 30 s"],
                       [[r["token"], r["windows"], r["copied_at_all"], r["copied_within_10s"], r["copied_within_30s"]] for r in Lt["fast_copy"]]))
    md.append("\nNIRVANA latency by code signature (medians, s):\n\n" +
              md_table(["Signature", "Windows", "First action (n)", "First copy (n)", "Dwell (n)"],
                       [[r["signature"], r["windows"], f"{r['first_action_s_median']} ({r['first_action_s_n']})",
                         f"{r['first_copy_ai_s_median']} ({r['first_copy_ai_s_n']})", f"{r['dwell_s_median']} ({r['dwell_s_n']})"]
                        for r in Lt["signatures"]]))
    Oc = J["outcome"]
    md.append("\n## 8. NIRVANA essay outcome (the dataset's own final-essay measures)\n\n" +
              md_table(["Session measure", "Outcome", "Sessions", "Spearman", "p"],
                       [[r["session_measure"], r["outcome"], r["sessions"], r["spearman_rho"], r["p"]] for r in Oc["correlations"]]))
    md.append("\n" + md_table(["Archetype", "Sessions", "Median GPT Final %", "Q25", "Q75", "Median ownership"],
                              [[r["archetype"], r["sessions"], r["median_gpt_final"], r["q25"], r["q75"], r["median_ownership"]]
                               for r in Oc["by_archetype"]]))
    md.append("\n" + md_table(["Any behavior-based SL window", "Sessions", "Median GPT Final %", "Median ownership"],
                              [[r["any_behavior_SL"], r["sessions"], r["median_gpt_final"], r["median_ownership"]] for r in Oc["by_any_SLb"]]))
    md.append("\n## 9. Log-only triggers (NIRVANA; computed from the keystroke log alone, no codes)\n\n" +
              md_table(["Trigger", "Fires when", "Windows fired", "SL among fired (determinate)", "SL base rate", "SL caught",
                        "SLb caught", "Sessions", "Fire rate vs GPT Final % (rho, p)", "Fire rate vs ownership (rho, p)"],
                       [[r["trigger"], r["fires_when"], f"{r['windows_fired']}/{r['of_windows']}", r["SL_among_fired_determinate"],
                         r["SL_base_rate_determinate"], r["SL_windows_caught"], r["SLb_windows_caught"], r["sessions_fired"],
                         f"{r['session_fire_rate_vs_gpt_final_rho']} ({r['p']})",
                         f"{r['session_fire_rate_vs_ownership_rho']} ({r['p_ownership']})"] for r in J["log_triggers"]]))
    Rb = J["robustness"]
    md.append("\n## 10. Robustness\n\nStage within generation requests (F4) and outside them; "
              f"{Rb['T_windows_that_are_F4'][0]} of {Rb['T_windows_that_are_F4'][1]} translating windows are F4:\n\n" +
              md_table(["F4 request", "Stage", "Determinate", "SL share"],
                       [[r["F4_request"], r["stage"], r["determinate"], r["SL_share"]] for r in Rb["stage_by_F4"]]))
    md.append("\nNIRVANA dwell with typing held low or high:\n\n" + md_table(["Typing after response", "Group", "Windows", "Median dwell (s)"],
              [[r["typing"], r["group"], r["windows"], r["median_dwell"]] for r in Rb["dwell_by_typing"]]))
    dw = Rb["dwell_within_session"]
    md.append(f"\nWithin NIRVANA sessions that have both sides: SL median dwell shorter in {dw['SL_median_shorter']} of {dw['sessions_with_both']}.\n")
    e = Rb["editor_first_multi_window"]
    md.append(f"\nEditor characters at first ask vs support share, multi-window NIRVANA sessions: rho {e['rho']}, p {e['p']} ({e['sessions']} sessions).\n")
    o = Rb["outcome_multi_window"]
    md.append(f"\nOutcome links, multi-window NIRVANA sessions ({o['sessions']}): SLb share vs GPT Final % rho {o['SLb_vs_gpt_final_rho']}; "
              f"vs ownership {o['SLb_vs_ownership_rho']}.\n")
    a = Rb["ownership_among_any_SLb"]
    md.append(f"\nAmong the {a['sessions']} sessions with any SLb window, SLb share vs ownership: rho {a['rho']}, p {a['p']}.\n")
    c = Rb["two_triggers_combined"]
    md.append(f"\nLarge paste with little typing OR ask on a near-empty page: fires on {c['windows_fired']} of {c['of_windows']} windows; "
              f"SL among fired {c['SL_among_fired_determinate']}; catches {c['SL_caught']} of SL and {c['SLb_caught']} of SLb windows.\n")
    md.append("\nArchetype stability (share of session pairs placed together or apart as at k = 6): " +
              ", ".join(f"k={r['k']} {r['pair_agreement_with_k6']}" for r in Rb["archetype_stability"]) + ".\n")
    return "".join(md)


if __name__ == "__main__":
    main()
