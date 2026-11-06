---
type: llm
focus: trace
weight: 1
---

plan.md reuses PR #91 and uses a structured body argument or a temporary Markdown file with --body-file that preserves literal backticks and $(date). It does not interpolate the body as executable shell text.
