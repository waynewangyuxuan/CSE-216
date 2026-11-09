#!/usr/bin/env python3
"""Spell-check the prose of main.tex with the macOS system dictionary (word lists as fallback); exit 1 on any finding."""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
PAPER = HERE.parent
ALLOW = HERE / "spell_allowlist.txt"
WORDLISTS = [pathlib.Path("/usr/share/dict/words"), pathlib.Path("/usr/share/dict/web2a")]
JXA = """
ObjC.import('AppKit');
function run(argv) {
  var words = JSON.parse(argv[0]);
  var checker = $.NSSpellChecker.sharedSpellChecker;
  checker.setLanguage('en_US');
  var bad = [];
  words.forEach(function (w) {
    var range = checker.checkSpellingOfStringStartingAt($(w), 0);
    if (range.length > 0) bad.push(w);
  });
  return JSON.stringify(bad);
}
"""


def prose_lines(tex):
    """Return (line number, text with commands, math, citations and code removed) for every line."""
    out = []
    xml = False
    for number, line in enumerate(tex.splitlines(), 1):
        if "\\begin{CCSXML}" in line:
            xml = True
        if xml:
            if "\\end{CCSXML}" in line:
                xml = False
            continue
        line = re.sub(r"(?<!\\)%.*$", "", line)
        line = re.sub(r"\$[^$]*\$", " ", line)
        line = re.sub(r"\\(begin|end)\{(tabular|longtable)\}.*$", " | ", line)
        line = re.sub(r"\\(code|citeauthor|citet|citep|cite|label|ref|includegraphics|bibliographystyle|bibliography|graphicspath|usepackage|documentclass|setcopyright|settopmatter|begin|end|ccsdesc|acmConference|acmYear|acmDOI|acmISBN)\b(\[[^]]*\])*(\{[^{}]*\})*", " | ", line)
        line = re.sub(r"\\[a-zA-Z]+\*?", " ", line)
        line = re.sub(r"\\.", " ", line)
        line = line.replace("&", " | ").replace("[tbp]", " ")
        line = re.sub(r"[{}\[\]~]", " ", line)
        out.append((number, line))
    return out


def tokens(text):
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)


def system_check(words):
    done = subprocess.run(["osascript", "-l", "JavaScript", "-e", JXA, json.dumps(words)], capture_output=True, text=True, timeout=120)
    if done.returncode != 0:
        raise RuntimeError(done.stderr)
    return set(json.loads(done.stdout))


def wordlist_check(words):
    known = set()
    for path in WORDLISTS:
        if path.exists():
            known |= {w.lower() for w in path.read_text().split()}
    def stems(w):
        w = w.lower().removesuffix("'s")
        yield w
        for suffix, repl in [("ies", "y"), ("es", ""), ("s", ""), ("ied", "y"), ("ed", ""), ("ed", "e"), ("ing", ""), ("ing", "e"), ("ly", ""), ("er", ""), ("er", "e")]:
            if w.endswith(suffix):
                yield w[: -len(suffix)] + repl
    return {w for w in words if not any(s in known for s in stems(w))}


def main():
    tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    allow = {w.strip().lower() for w in ALLOW.read_text().splitlines() if w.strip() and not w.startswith("#")} if ALLOW.exists() else set()
    lines = prose_lines(tex)
    figure_text = PAPER / "figures" / "figure_text.txt"
    if figure_text.exists():
        lines += [(f"figure text {n}", text) for n, text in enumerate(figure_text.read_text(encoding="utf-8").splitlines(), 1)]
    where = {}
    for number, text in lines:
        for word in tokens(text):
            where.setdefault(word, []).append(number)
    candidates = sorted(w for w in where if len(w) > 1 and w.lower() not in allow)
    try:
        bad, engine = system_check(candidates), "macOS NSSpellChecker"
    except Exception as err:
        print(f"system dictionary unavailable ({err}); using word lists", file=sys.stderr)
        bad, engine = wordlist_check(candidates), "word list"
    findings = []
    for word in sorted(bad):
        findings.append(f"spelling: {word} (line {where[word][0]}{' +' + str(len(where[word]) - 1) if len(where[word]) > 1 else ''})")
    for number, text in lines:
        for match in re.finditer(r"\b([A-Za-z]+)\s+\1\b", text):
            if match.group(1).lower() not in {"had", "that"}:
                findings.append(f"doubled word: {match.group(0)} (line {number})")
        for match in re.finditer(r"\b(behaviou?r\w*|analys(e|ed|es|ing)|colou?r\w*|organis\w*|centre\w*|labell\w*|modell\w*|programme\w*|whilst|towards)\b", text, re.I):
            if re.search("ou|analys|organis|centre|labell|modell|programme|whilst|towards", match.group(0), re.I) and not match.group(0).lower().startswith(("analysis", "behavior", "color")):
                findings.append(f"British form: {match.group(0)} (line {number})")
        for match in re.finditer(r"\ba\s+[aeio][a-z]+", text):
            if not re.match(r"a\s+(one|once|uni|use|eu)", match.group(0)):
                findings.append(f"a/an: {match.group(0)} (line {number})")
        for match in re.finditer(r"\ban\s+[bcdfgjklmnpqrstvwxyz][a-z]+", text):
            findings.append(f"a/an: {match.group(0)} (line {number})")
    print(f"checked {len(candidates)} distinct words with {engine}; {len(allow)} allowlisted")
    if findings:
        print("\n".join(findings))
        sys.exit(1)
    print("spellcheck: ok")


main()
