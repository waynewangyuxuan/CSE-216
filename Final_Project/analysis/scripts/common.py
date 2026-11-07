"""Shared paths, loaders and constants for Bet 8 analysis scripts. Codes and ids only; no dataset text."""
import csv, importlib.util, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.normpath(os.path.join(HERE, "..", ".."))          # Final_Project/
AN = os.path.join(FP, "analysis")
RES = os.path.join(AN, "results")
FIG = os.path.join(AN, "figures")

SL, OF, AU, NE, IN = "SURRENDER_LEANING", "OFFLOADING", "AUGMENTING", "NEUTRAL_MECHANICAL", "INDETERMINATE"
CATS = [SL, OF, AU, NE, IN]
SHORT = {SL: "SL", OF: "OFF", AU: "AUG", NE: "NEU", IN: "IND"}
LABEL = {SL: "Surrender-leaning", OF: "Offloading", AU: "Augmenting", NE: "Neutral-mechanical", IN: "Indeterminate"}
SUPPORT = {OF, AU}                     # RQ1 "supports thinking" side (v1.2 s9.1)
SESSION_SETS = ("NIRVANA", "WildChat")  # WildChat-Bet4 sessions are incomplete samples: excluded
EDITOR_ONLY_RULES = ["R06", "R09", "R12", "R17", "R19", "R20"]  # cannot fire without an editor (v1.2 s9.4)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, cols=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cols = cols or list(rows[0])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def frozen_rules():
    """Import the frozen apply_rules.py as a module, unchanged (check_frozen.py runs first)."""
    p = os.path.join(FP, "inference", "scripts", "apply_rules.py")
    spec = importlib.util.spec_from_file_location("apply_rules_frozen", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_windows(which="final"):
    """Window rows: frozen-rule output joined with v1.1 codes and flags, sorted by set, session, turn."""
    cats = {r["window_id"]: r for r in read_csv(os.path.join(RES, f"v12_{which}", "window_categories.csv"))}
    labels = {r["window_id"]: r for r in read_csv(os.path.join(RES, "inputs", f"labels_{which}.csv"))}
    flags = {r["window_id"]: r for r in read_csv(os.path.join(RES, "inputs", "flags.csv"))}
    out = []
    for wid, c in cats.items():
        r = dict(c)
        r.update({k: v for k, v in labels[wid].items() if k not in r})
        r.update({k: v for k, v in flags[wid].items() if k not in r})
        r["order"] = int(r["order"])
        r["D"], r["V"], r["U"], r["F"] = (r[k].split("_")[0] for k in ("decision", "verification", "uptake", "function"))
        out.append(r)
    out.sort(key=lambda r: (r["dataset"], r["session_id"], r["order"]))
    return out


def sessions(windows, sets=SESSION_SETS, keep=lambda w: True):
    """{(dataset, session_id): [windows in turn order]} for whole-session sets only."""
    s = {}
    for w in windows:
        if w["dataset"] in sets and keep(w):
            s.setdefault((w["dataset"], w["session_id"]), []).append(w)
    return dict(sorted(s.items()))


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "–"


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(x) for x in r) + " |" for r in rows]
    return "\n".join(out) + "\n"
