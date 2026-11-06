#!/usr/bin/env bash
# Usage: eval-review.sh <iteration-dir> <name> [out.html]
# Aggregates a skill-creator style workspace and opens the review page.
set -eu
dir=${1:?iteration dir}; name=${2:?name}; out=${3:-$dir/../$name-review.html}
# ponytail: skill-creator lives under a hashed synced path, so glob for it
sc=$(ls -d "$HOME"/.claude/skills/synced/*/skill-creator 2>/dev/null | head -1)
[ -n "$sc" ] || { echo "skill-creator not found under ~/.claude/skills/synced" >&2; exit 1; }
find "$dir" -name grading.json | grep -q . || { echo "no grading.json under $dir; grade the runs first" >&2; exit 1; }
cd "$sc"
python3 -m scripts.aggregate_benchmark "$dir" --skill-name "$name"
python3 eval-viewer/generate_review.py "$dir" --skill-name "$name" --benchmark "$dir/benchmark.json" --static "$out"
open "$out"
