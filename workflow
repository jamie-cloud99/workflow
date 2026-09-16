#!/bin/bash
set -euo pipefail

repo_root="$(cd -- "$(/usr/bin/dirname "${BASH_SOURCE[0]}")" && pwd -P)"

supported() {
  [[ -x "$1" ]] && "$1" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' >/dev/null 2>&1
}

missing_python() {
  echo 'Workflow requires Python 3.11+. Install it with: brew install python' >&2
  echo 'Then rerun ./workflow. You can also set WORKFLOW_PYTHON to a compatible interpreter path.' >&2
  exit 1
}

if [[ -n "${WORKFLOW_PYTHON:-}" ]]; then
  candidate="$(command -v "$WORKFLOW_PYTHON" 2>/dev/null || true)"
  if supported "$candidate"; then
    exec "$candidate" "$repo_root/scripts/workflow.py" "$@"
  fi
  echo 'WORKFLOW_PYTHON does not point to a compatible executable.' >&2
  missing_python
fi

# Prefer the user's current environment when its default Python is new enough.
candidate="$(command -v python3 2>/dev/null || true)"
if supported "$candidate"; then
  exec "$candidate" "$repo_root/scripts/workflow.py" "$@"
fi

# macOS can keep an old system python3 even after a versioned Homebrew install.
IFS=: read -r -a directories <<< "${PATH:-}"
directories+=(/opt/homebrew/bin /usr/local/bin)
for directory in "${directories[@]}"; do
  directory="${directory:-.}"
  for candidate in "$directory"/python3 "$directory"/python3.*; do
    if [[ "${candidate##*/}" != python3 ]]; then
      minor="${candidate##*.}"
      case "$minor" in ''|*[!0-9]*) continue ;; esac
    fi
    if supported "$candidate"; then
      exec "$candidate" "$repo_root/scripts/workflow.py" "$@"
    fi
  done
done

missing_python
