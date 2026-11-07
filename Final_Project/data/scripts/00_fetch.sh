#!/bin/bash
# Downloads raw data into ../raw/<dataset>/. Rerunnable: skips files already complete,
# verifies sha256 against values published by the host. Needs no account.
# ScholaWrite data is gated on Hugging Face. Accept its terms and log in yourself, then:
#   hf download minnesotanlp/scholawrite --repo-type dataset --revision e880b2401080de356d0eb29163e8824fd608de5d --local-dir raw/scholawrite/hf
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; RAW="$HERE/../raw"
OSF_KEY=1f1af82b22384961b682d9cba5d1661f   # view-only key printed in arXiv:2604.07344 section 3.5
fetch() { # url dest sha256
  if [ -f "$2" ] && [ "$(shasum -a 256 "$2" | cut -d' ' -f1)" = "$3" ]; then echo "ok   $2"; return; fi
  curl -sSL --retry 5 --retry-delay 5 -C - -o "$2" "$1" || curl -sSL --retry 5 -o "$2" "$1"
  [ "$(shasum -a 256 "$2" | cut -d' ' -f1)" = "$3" ] && echo "got  $2" || { echo "BAD SHA $2"; exit 1; }
}
fetch "https://osf.io/download/tmq6v/?view_only=$OSF_KEY" "$RAW/nirvana/dataset.xlsx" e63e6c47d1eb17c7bb3d081ec2dc7ec81059031bb58488a41272e6e20a2ea734
# WildChat-1M, pinned revision; shard list and hashes in wildchat_manifest.tsv
while IFS=$'\t' read -r name sha rev; do
  fetch "https://huggingface.co/datasets/allenai/WildChat-1M/resolve/$rev/data/$name" "$RAW/wildchat/$name" "$sha"
done < "$HERE/wildchat_manifest.tsv"
# ScholaWrite: public sources only (no login). Pinned commit of the authors' repo, and the paper HTML.
SW="$RAW/scholawrite/public"; mkdir -p "$SW"
COMMIT=1ee32c45bfed9df8806536c9dd821438305c5161
[ -f "$SW/labels.py.txt" ] || curl -sSL -o "$SW/labels.py.txt" "https://raw.githubusercontent.com/minnesotanlp/scholawrite/$COMMIT/augmented/scholawrite/labels.py"
[ -f "$SW/small_model_classifier.py.txt" ] || curl -sSL -o "$SW/small_model_classifier.py.txt" "https://raw.githubusercontent.com/minnesotanlp/scholawrite/$COMMIT/scholawrite_finetune/bert_finetune/small_model_classifier.py"
[ -f "$SW/paper_v4.html" ] || curl -sSL -o "$SW/paper_v4.html" "https://arxiv.org/html/2502.02904v4"
