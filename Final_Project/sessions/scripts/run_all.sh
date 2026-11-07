#!/bin/sh
# Rebuild Bet 6 numbers from saved labels. Calls no model. audit_access.py is not here: it needs local transcripts, and results/access_audit.json is its record.
# build_parts, merge, finalize and overlap_check need git-excluded data/ and sessions/blind/; stats.py needs only committed CSVs.
cd "$(dirname "$0")" || exit 1
PY=../../data/raw/_venv/bin/python
$PY coder_codebook.py > /dev/null && $PY build_parts.py > /dev/null && $PY merge.py && $PY finalize.py && $PY overlap_check.py > /dev/null && $PY stats.py > /dev/null || exit 1
for f in ../results/* ../coder_codebook_v1.1.md; do shasum "$f"; done
