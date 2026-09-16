---
name: workflow-delivery
description: Use when requirements are clear and changes need implementation or delivery; do not start the full workflow for simple questions.
---

# workflow-delivery

1. Derive observable acceptance outcomes from what the user has already confirmed. Ask only for missing decisions that change behavior.
2. Check repository rules, the working tree, and the target branch; preserve other work. Implement independently verifiable scope in dependency order.
3. Investigate verification failures instead of removing checks or weakening conditions to expedite delivery. Add only tests that expose real regressions.
4. Use [workflow-commit](../workflow-commit/SKILL.md) when a commit is requested, followed by [workflow-create-pr](../workflow-create-pr/SKILL.md) when creating or updating a PR is requested. A ship-PR request connects implementation verification, commit, push, PR, and CI confirmation under existing authorization.
5. At delivery, distinguish code changes, local verification, remote CI, and actual user-interaction evidence. Complete authorized steps before reporting; clearly identify unfinished work.
