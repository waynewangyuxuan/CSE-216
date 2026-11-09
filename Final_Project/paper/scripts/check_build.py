#!/usr/bin/env python3
"""Compile main.tex with the committed ACM class in a temp folder; fail on errors, undefined references, overfull lines or too many body pages."""
import pathlib
import re
import subprocess
import sys
import tempfile

PAPER = pathlib.Path(__file__).resolve().parents[1]
MAX_BODY_PAGES = 20
OVERFULL_LIMIT_PT = 2.0


def main():
    with tempfile.TemporaryDirectory() as out:
        done = subprocess.run(
            ["tectonic", "-Z", "search-path=template", "-o", out, "--keep-logs", "--keep-intermediates", "main.tex"],
            cwd=PAPER, capture_output=True, text=True,
        )
        log = pathlib.Path(out, "main.log").read_text(errors="ignore") if pathlib.Path(out, "main.log").exists() else ""
        aux = pathlib.Path(out, "main.aux").read_text(errors="ignore") if pathlib.Path(out, "main.aux").exists() else ""
        blg = pathlib.Path(out, "main.blg").read_text(errors="ignore") if pathlib.Path(out, "main.blg").exists() else ""
    problems = []
    if done.returncode != 0:
        problems.append("compile failed:\n" + done.stdout[-1500:] + done.stderr[-1500:])
    problems += [line for line in log.splitlines() if line.startswith("!")]
    problems += sorted({line for line in log.splitlines() if re.search(r"(Citation|Reference) .* undefined|There were undefined", line)})
    problems += [line for line in blg.splitlines() if line.startswith(("I couldn't", "I found no"))]
    missing_fields = sum(line.startswith("Warning--") for line in blg.splitlines())
    over = [m for m in re.finditer(r"Overfull \\hbox \((\d+\.\d+)pt too wide\)[^\n]*", log) if float(m.group(1)) > OVERFULL_LIMIT_PT]
    problems += [m.group(0) for m in over]
    match = re.search(r"\\newlabel\{end:body\}\{\{[^{}]*\}\{(\d+)\}", aux)
    pages = re.search(r"Output written on .*\((\d+) pages?", log)
    body = int(match.group(1)) if match else None
    print(f"body pages (excluding references and appendix): {body}; total pages: {pages.group(1) if pages else '?'}; overfull lines over {OVERFULL_LIMIT_PT}pt: {len(over)}; bib entries' missing-field warnings (not in the registry, so not invented): {missing_fields}")
    if body is None:
        problems.append("could not read the end:body label from main.aux")
    elif body > MAX_BODY_PAGES:
        problems.append(f"body is {body} pages, over the {MAX_BODY_PAGES}-page guideline")
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print("check_build: ok")


main()
