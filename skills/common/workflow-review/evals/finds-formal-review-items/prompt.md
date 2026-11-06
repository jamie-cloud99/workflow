---
tags: [workflow-review]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Take PR #561 through its review fixes with the workflow-review skill. Dry run: do not execute gh or git. The GitHub data is in local files stack.txt, reviews.json, inline.json, issue-comments.json. Write your plan to plan.md.
