---
name: workflow-delivery
description: Use when requirements are clear and changes need implementation or delivery; do not start the full workflow for simple questions.
---

# workflow-delivery

1. Derive observable acceptance outcomes from what the user has already confirmed. Ask only for missing decisions that change behavior.
2. Check repository rules, the working tree, and the target branch; preserve other work. Implement independently verifiable scope in dependency order.
3. Investigate verification failures instead of removing checks or weakening conditions to expedite delivery. Add only tests that expose real regressions.
4. Before delivery, check the complete task diff against acceptance outcomes, affected callers, failure paths, and verification evidence. Scale checks to risk; use [workflow-review](../workflow-review/SKILL.md) in author self-review mode when useful. Fix confirmed issues and rerun affected checks.
5. Use [workflow-commit](../workflow-commit/SKILL.md) when a commit is requested, followed by [workflow-create-pr](../workflow-create-pr/SKILL.md) when creating or updating a PR is requested. A ship-PR request connects implementation verification, commit, push, PR, and CI confirmation under existing authorization.
6. At delivery, distinguish code changes, local verification, remote CI, and actual user-interaction evidence. Complete authorized steps before reporting; clearly identify unfinished work.

## Handoff and resumption

Use [handoff.md](templates/handoff.md) when a handoff is requested or work must continue in another session. Update the existing task document's current state, or provide the handoff in conversation if none exists; do not create a history log. Use Traditional Chinese by default and omit irrelevant fields and secrets.

On resumption, verify the actual workspace, Git state, and relevant remote state. Prior results apply only to their recorded revision and environment. Preserve settled decisions and authorization without expanding their scope. Do not use a handoff to stop work that can still be completed.
