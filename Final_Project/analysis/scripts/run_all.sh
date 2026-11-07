#!/bin/sh
# Bet 8: rebuilds every analysis number, table and figure from committed v1.1 labels. No model calls.
# Usage: sh Final_Project/analysis/scripts/run_all.sh   (from anywhere)
set -e
cd "$(dirname "$0")/.."            # Final_Project/analysis
PY=${PY:-.venv/bin/python}
if ! "$PY" -c "import matplotlib, numpy" 2>/dev/null; then
  echo "Creating .venv with requirements.txt (git-excluded)" >&2
  python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
  PY=.venv/bin/python
fi
export MPLBACKEND=Agg PYTHONHASHSEED=0 SOURCE_DATE_EPOCH=0

# 1. Frozen v1.2 must be byte-identical to inference/FROZEN.md before it runs.
"$PY" scripts/check_frozen.py

# 2. Inputs, then the frozen rules, unchanged, on final labels and on each coder alone.
"$PY" scripts/build_inputs.py
for set in final coderA coderB; do
  "$PY" ../inference/scripts/apply_rules.py results/inputs/labels_$set.csv results/v12_$set > /dev/null
done

# 3. Analysis, tables and figures.
"$PY" scripts/out_of_sample.py
"$PY" scripts/sessions.py
"$PY" scripts/patterns.py
"$PY" scripts/sensitivity.py
"$PY" scripts/figures.py
"$PY" scripts/check_outputs.py
echo "run_all: ok"
