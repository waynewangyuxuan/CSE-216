#!/bin/sh
# Rebuild every Bet 4 number from saved labels. Calls no model. Needs git-excluded data/ and blind/ for all but stats_bet4.py and compare_fable.py.
cd "$(dirname "$0")" || exit 1
PY=../../data/raw/_venv/bin/python
$PY truncation.py > /dev/null && $PY build_views.py && $PY merge_labels.py && $PY finalize.py && $PY overlap_audit.py && $PY truncation_effect.py > /dev/null && $PY stats_bet4.py && $PY compare_fable.py > /dev/null || exit 1
for f in ../results/*; do shasum "$f"; done
