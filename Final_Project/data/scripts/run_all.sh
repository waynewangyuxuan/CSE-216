#!/bin/bash
# Rebuilds every output from raw data. Needs: uv. Calls no model: the LLM pass reads its cache.
# To fill the LLM cache instead: add --call to step 03 (not deterministic, costs money).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
VENV="${VENV:-$HERE/../raw/_venv}"
[ -x "$VENV/bin/python" ] || { uv venv -q --python 3.12 "$VENV"; uv pip install -q --python "$VENV/bin/python" -r "$HERE/requirements.txt"; }
cd "$HERE/.."          # never run from inside raw/
mkdir -p raw/_derived
"$HERE/00_fetch.sh"
for s in 01_nirvana_windows 02_wildchat_screen 03_wildchat_llm_screen 04_scholawrite_check 05_build_outputs; do
  echo "== $s"; "$VENV/bin/python" -I "$HERE/$s.py" > "$HERE/../raw/_derived/$s.out" ; tail -1 "$HERE/../raw/_derived/$s.out" >/dev/null
done
shasum -a 256 windows.jsonl sample.csv gold.csv counts.json wildchat_draw2000_log.tsv | tee raw/_derived/output_hashes.txt
