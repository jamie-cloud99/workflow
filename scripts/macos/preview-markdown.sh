#!/bin/bash
set -euo pipefail

if [[ $# != 1 || ! -f "$1" || ! -r "$1" ]]; then
  echo 'Expected one readable Markdown file (.md or .markdown).' >&2
  exit 2
fi
case "$1" in
  *.[mM][dD]|*.[mM][aA][rR][kK][dD][oO][wW][nN]) ;;
  *) echo 'Expected one readable Markdown file (.md or .markdown).' >&2; exit 2 ;;
esac

# Finder applications do not inherit an interactive shell's Homebrew PATH.
export PATH="${PATH:-/usr/bin:/bin}:/opt/homebrew/bin:/usr/local/bin"
if ! command -v glow >/dev/null 2>&1; then
  echo 'Glow is missing. Install it with: brew install glow' >&2
  exit 127
fi

# Do not inherit a pager that launches an editor or exits on short documents.
export PAGER='/usr/bin/less -R'
export LESS='-R'
exec glow -p -w 100 -- "$1"
