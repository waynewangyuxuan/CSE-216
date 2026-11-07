"""Coder-facing views of windows. Removes LLM labels and linkage; adds only text the window already has.
Used for the pilot, the C3 packet, and (should Bet 4 want the same view) the sample."""
import ast, csv, importlib.util, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FP = os.path.abspath(os.path.join(HERE, "..", ".."))
DATA = os.path.join(FP, "data")
CODEBOOK = os.path.join(FP, "codebook")
CAP = 8000          # chars per text block in a view; head+tail kept, cut is marked
PRIOR_TURNS = 3     # earlier request/response pairs shown for context
PRIOR_CAP = 500
csv.field_size_limit(10**9)

# Whatever windows.jsonl adds, a view holds only these keys. A whitelist, so new label fields cannot leak.
VIEW_KEYS = ["window_id", "dataset", "coverage", "turn_order", "prior_turns", "editor_before_request",
             "request", "response", "next_actions_text"]


def _actions_text():
    sys.path.insert(0, os.path.join(DATA, "scripts"))
    spec = importlib.util.spec_from_file_location("build_outputs", os.path.join(DATA, "scripts", "05_build_outputs.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.actions_text


def load_windows():
    with open(os.path.join(DATA, "windows.jsonl"), encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def load_ids(name):
    with open(os.path.join(DATA, name), encoding="utf-8", newline="") as f:
        return {r["window_id"] for r in csv.DictReader(f)}


def cap(text, n=CAP):
    text = text or ""
    if len(text) <= n:
        return text
    head, tail = int(n * 0.75), int(n * 0.25)
    return f"{text[:head]}\n[... {len(text) - head - tail} characters cut from this view ...]\n{text[-tail:]}"


def editor_text(w):
    """NIRVANA stores the editor as the repr of a list of lines."""
    raw = w.get("editor_before_request")
    if raw is None:
        return None
    try:
        v = ast.literal_eval(raw)
        return "\n".join(str(x) for x in v) if isinstance(v, list) else str(v)
    except (ValueError, SyntaxError):
        return str(raw)


def build_view(w, by_session, actions_text):
    earlier = [x for x in by_session[(w["dataset"], w["session_id"])] if x["turn_order"] < w["turn_order"]][-PRIOR_TURNS:]
    return {
        "window_id": w["window_id"], "dataset": w["dataset"], "coverage": w["coverage"], "turn_order": w["turn_order"],
        "prior_turns": [{"turn": x["turn_order"], "request": cap(x["request"], PRIOR_CAP), "response": cap(x["response"], PRIOR_CAP)} for x in earlier],
        "editor_before_request": cap(editor_text(w)) if w["dataset"] == "NIRVANA" else None,
        "request": cap(w["request"]), "response": cap(w["response"]), "next_actions_text": cap(actions_text(w)),
    }


def make_views(ids=None):
    rows = load_windows()
    by_session = {}
    for w in rows:
        by_session.setdefault((w["dataset"], w["session_id"]), []).append(w)
    for v in by_session.values():
        v.sort(key=lambda x: x["turn_order"])
    at = _actions_text()
    out = {}
    for w in rows:
        if ids is None or w["window_id"] in ids:
            out[w["window_id"]] = build_view(w, by_session, at)
    assert all(set(v) == set(VIEW_KEYS) for v in out.values())
    return out


def norm(t):
    return re.sub(r"\s+", " ", t or "").strip()
