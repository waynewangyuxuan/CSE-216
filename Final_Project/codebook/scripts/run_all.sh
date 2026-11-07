#!/bin/sh
# Rebuild every number and the C3 packet from cached coder labels. Calls no model. Coder labels live in pilot/ (git-excluded).
cd "$(dirname "$0")" || exit 1
PY=../../data/raw/_venv/bin/python
$PY draw_pilot.py r1 r2 && $PY draw_pilot_r3.py && $PY draw_pilot_r4.py && $PY draw_pilot_r5.py && $PY vignettes.py || exit 1
for r in r1 r2 r3 r4 r5; do $PY agreement.py $r && $PY overlap.py $r > /dev/null || exit 1; done
$PY summary.py && $PY make_c3.py || exit 1
# A filled sheet is not an error here: check_c3.py without --blank checks it.
$PY check_c3.py --blank || echo "NOTE: the lines above list why the sheet is not a blank packet. If it holds human labels, that is expected: run check_c3.py"
$PY check_blinding.py || exit 1
$PY scan_rare.py
$PY overlap.py --all
