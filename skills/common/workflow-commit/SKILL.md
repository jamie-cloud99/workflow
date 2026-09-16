---
name: workflow-commit
description: Create scoped commits when requested or required by an authorized delivery.
---

# workflow-commit

- Confirm the intended branch immediately before committing. Include only task-owned files or hunks; preserve unrelated work and its staging state. Split by independently understandable purpose.
- Use checks appropriate to the change and repository requirements; keep hooks enabled. Fix failures caused by the task and rerun affected checks without seeking repeated approval. Avoid empty commits or unrelated cleanup.
- Follow the user's message format, then repository conventions. Otherwise use [default-commit.txt](templates/default-commit.txt): Conventional Commits with optional scope and Traditional Chinese prose. Translate template labels, replace placeholders, and omit unnecessary body fields.
- An authorized commit does not require another message approval. History rewrites must fit the authorized scope and branch circumstances. A request for message wording alone does not authorize committing.
- Finish by verifying the commit SHA, committed scope, and remaining working-tree state. Report actual verification and excluded task changes.

A commit-only request ends locally. Continue an already authorized push or PR workflow using [workflow-create-pr](../workflow-create-pr/SKILL.md); do not ask again for authorization already given.
