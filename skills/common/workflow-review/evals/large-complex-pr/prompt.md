---
tags: [workflow-review]
max_turns: 40
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

I want a thorough, independent review of PR #8687 using the workflow-review skill. The diff is the local file pr8687.diff (test files and docs are omitted from it); do not run gh. Write the findings to review.md and stop there.
