#!/bin/bash
# Commit only the given paths: text-check them on a private copy of the index, wait out index.lock, then commit with a pathspec.
# Usage (from repo root): Final_Project/wildchat/scripts/commit_paths.sh "message" path...
set -euo pipefail
msg="$1"; shift
W="$(cd "$(dirname "$0")/.." && pwd)"
T=$(mktemp); cp .git/index "$T"
GIT_INDEX_FILE="$T" git add -- "$@"
GIT_INDEX_FILE="$T" "$W/blind/_venv/bin/python" -I "$W/scripts/check_staged.py" | tail -1
rm -f "$T"
while [ -f .git/index.lock ]; do sleep 2; done
git add -- "$@"
git commit -q -m "$msg

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -- "$@"
git log --oneline -1
