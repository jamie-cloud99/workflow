---
name: workflow-create-pr
description: Create or update a GitHub PR and verify its remote head and CI.
---

# workflow-create-pr

- Confirm the intended head, base, remote, and account before pushing. Inspect the complete base-to-head change, including existing commits; preserve unrelated work and global account settings. For dependent PRs, use gh-stack and verify each layer's actual increment.
- An actual PR request includes the necessary branch push; a text-only request stops at draft wording. Use [workflow-commit](../workflow-commit/SKILL.md) for task changes needing a commit. Inspect remote divergence before reconciling it; do not overwrite it blindly.
- Update the existing PR for the intended head when present. Choose draft status from readiness and the user's request. Follow the user's format, then the repository template; otherwise use [default-pr.md](templates/default-pr.md), with an optional-scope Conventional Commits title.
- Write in ELI20 style: explain the concrete problem, resulting behavior, necessary tradeoffs, and evidence to an engineer unfamiliar with the change. Use Traditional Chinese by default, including template headings. Scale detail to the change; omit empty fields and development chronology.
- Use structured content arguments or a temporary Markdown file with `--body-file`; do not interpolate PR prose into shell commands.
- Complete delivery by reading back the PR URL, base/head, SHA, and draft state, and checking CI for that exact head through a terminal result. Fix task-caused failures within scope. Report absent checks, external blockers, or unverified environments accurately instead of claiming success.

Report the PR link, SHA, and verification. CI, review approval, merge, deployment, and acceptance remain distinct; merge and additional external comments require corresponding authorization. Continue already authorized steps without requesting permission again.
