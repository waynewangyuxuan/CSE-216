#!/bin/sh
# Rerun every Bet 7 number from cached labels. Calls no model: llm_label.py without --call only checks the cache is complete.
# Needs the raw WildChat shards (data/raw, git-excluded) and blind/emb.npy (03_embed.py skips when present; recomputing it needs the
# pinned open model, no LLM). audit_access.py is not here: it needs local transcripts, and results/access_audit.json is its record.
set -e
cd "$(dirname "$0")"
PY=../blind/_venv/bin/python
$PY -I 01_eligible.py > /dev/null
$PY -I 02_seed.py
$PY -I llm_label.py screen ../blind/ids_seed.txt
$PY -I 03_embed.py
$PY -I 04_rank.py enrich
$PY -I llm_label.py screen ../blind/ids_enrich.txt
$PY -I 04_rank.py confirm
$PY -I llm_label.py screen ../blind/ids_confirm.txt
$PY -I 07_select.py
$PY -I 05_audit_draw.py
$PY -I llm_label.py screen ../blind/ids_rejudge.txt
$PY -I llm_label.py audit ../blind/ids_audit.txt
$PY -I 06_funnel.py > /dev/null
$PY -I 10_merge.py
$PY -I 12_finalize.py
$PY -I 13_stats.py > /dev/null
cd ../results && shasum -a 256 *.csv *.tsv *.json *.md | grep -v -e access_audit -e llm_cost_log
