#!/usr/bin/env bash
# N-8(a) inventory check (rc10). Fails if any file in the tree is not listed in SHA256SUMS.txt
# (e.g. a stray .gitkeep) or any listed file is missing. SHA256SUMS.txt itself and .git/ are excluded.
# Usage: bash tools/ci_inventory_check.sh [TREE_DIR]   (default: .)
set -euo pipefail
cd "${1:-.}"
export LC_ALL=C
tree=$(mktemp); listed=$(mktemp)
find . -type f -not -path './.git/*' -not -name SHA256SUMS.txt | sed 's|^\./||' | sort > "$tree"
cut -c67- SHA256SUMS.txt | sort > "$listed"
if ! diff -u "$listed" "$tree"; then
  echo "INVENTORY_FAIL: tree and SHA256SUMS.txt differ ('+' = unlisted file in tree, '-' = listed but missing)"
  exit 1
fi
echo "INVENTORY_OK: $(wc -l < "$tree") files, all listed, none missing"
