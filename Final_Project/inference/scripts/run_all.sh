#!/bin/sh
# Reruns every number in inference/ from saved labels. No model calls.
set -e
cd "$(dirname "$0")/.."
python3 scripts/apply_rules.py ../coding/results/final_labels.csv calibration/final > /dev/null
python3 calibration/apply_rules_draft0.py ../coding/results/final_labels.csv calibration/draft0 > /dev/null
python3 scripts/check.py
