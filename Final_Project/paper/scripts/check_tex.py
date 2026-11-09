#!/usr/bin/env python3
"""Lint main.tex without TeX: balanced braces and environments, cite keys, labels, figures, stray special characters, length estimate."""
import pathlib
import re
import sys

PAPER = pathlib.Path(__file__).resolve().parents[1]
TEX = (PAPER / "main.tex").read_text(encoding="utf-8")
BIB = (PAPER / "refs.bib").read_text(encoding="utf-8")


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def main():
    body = strip_comments(TEX)
    problems = []

    stack, line = [], 1
    escaped = False
    for ch in body:
        if ch == "\n":
            line += 1
        if escaped:
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == "{":
            stack.append(line)
        elif ch == "}":
            if not stack:
                problems.append(f"line {line}: unmatched closing brace")
            else:
                stack.pop()
    problems += [f"line {n}: unclosed brace" for n in stack]

    envs = []
    for match in re.finditer(r"\\(begin|end)\{([^}]+)\}", body):
        kind, name = match.groups()
        where = body[: match.start()].count("\n") + 1
        if kind == "begin":
            envs.append((name, where))
        elif not envs or envs[-1][0] != name:
            problems.append(f"line {where}: \\end{{{name}}} does not match {envs[-1] if envs else None}")
        else:
            envs.pop()
    problems += [f"line {n}: \\begin{{{e}}} never closed" for e, n in envs]

    bib_keys = set(re.findall(r"^@\w+\{([^,]+),", BIB, re.M))
    cited = set()
    for group in re.findall(r"\\cite[tp]?(?:author)?\{([^}]+)\}", body):
        cited |= {k.strip() for k in group.split(",")}
    problems += [f"cited but not in refs.bib: {k}" for k in sorted(cited - bib_keys)]
    problems += [f"in refs.bib but never cited: {k}" for k in sorted(bib_keys - cited)]

    labels = re.findall(r"\\label\{([^}]+)\}", body)
    refs = re.findall(r"\\ref\{([^}]+)\}", body)
    problems += [f"undefined reference: {k}" for k in sorted(set(refs) - set(labels))]
    problems += [f"duplicate label: {k}" for k in sorted(set(labels)) if labels.count(k) > 1]

    for name in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", body):
        if not (PAPER / "figures" / name).exists():
            problems.append(f"missing figure: {name}")

    for number, text in enumerate(body.splitlines(), 1):
        clean = re.sub(r"\\begin\{CCSXML\}.*", "", text)
        if "<" in clean and ("concept" in clean or "ccs2012" in clean):
            continue
        if re.search(r"(?<!\\)[#]", clean) and "\\newcommand" not in clean:
            problems.append(f"line {number}: unescaped #")
        if re.search(r"(?<!\\)_", clean) and not re.search(r"\\(label|ref|includegraphics|bibliography|graphicspath)|ccs|fig\d", clean):
            problems.append(f"line {number}: unescaped underscore")
        if re.search(r"[^\x00-\x7f]", clean):
            problems.append(f"line {number}: non-ASCII character")
        if re.search(r"(?<![\\\d])\d+(\.\d+)?%", clean):
            problems.append(f"line {number}: unescaped percent")

    body_part = body.split("\\begin{document}")[1].split("\\bibliographystyle")[0]
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]+", re.sub(r"\\[a-zA-Z]+\*?(\{[^}]*\}|\[[^]]*\])?", " ", body_part)))
    figures = body_part.count("\\begin{figure}")
    tables = body_part.count("\\begin{table}")
    pages = words / 520 + figures * 0.45 + tables * 0.2
    print(f"body words about {words}; figures {figures}; tables {tables}; estimated pages about {pages:.1f} (no TeX here, so this is an estimate)")

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("check_tex: ok")


main()
