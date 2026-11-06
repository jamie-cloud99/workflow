---
tags: [workflow-review]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash, Agent]
---

Fix the review items on #561 and reply to the reviewer, using the workflow-review skill. Dry run: do not execute gh or git. The GitHub data is in local files stack.txt, reviews.json, inline.json, issue-comments.json. Write the reply text to reply.md and the commands you would run to plan.md.
