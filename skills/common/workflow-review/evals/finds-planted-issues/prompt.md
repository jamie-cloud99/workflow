---
tags: [workflow-review]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Review PR #42 using the workflow-review skill. The PR is not on GitHub; the diff is the local file pr42.diff, so do not run gh. Write the final findings list to review.md and stop there.
