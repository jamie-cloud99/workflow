---
name: workflow-task-breakdown
description: Split an agreed specification into independently verifiable tasks and dependencies.
---

# workflow-task-breakdown

Use when an agreed feature needs multiple implementation tasks. Small changes can go directly to [workflow-delivery](../workflow-delivery/SKILL.md).

- Reuse the confirmed spec and acceptance outcomes. Inspect relevant code to identify existing behavior, boundaries, and real dependencies; do not restart discovery or scan the entire repo by default.
- Split into vertical slices that produce an observable outcome. Each task should state its scope, acceptance evidence, dependencies, and relevant code locations when known. Separate necessary enabling work explicitly; avoid arbitrary size quotas or speculative file names.
- Order blockers before dependents and expose unresolved decisions that affect the split. If stacked PRs are appropriate, name the proposed branch/base relationships without creating them prematurely.
- Deliver the plan in the existing task location or conversation. Update an existing plan instead of creating duplicate planning documents. Continue to implementation when already authorized; ask only about consequential unresolved decisions.
- Create or update tracker issues only when requested. Follow project tracker conventions, reuse existing issues, and use real returned identifiers for parent/dependency links. Read back published content and relationships; report partial completion without duplicating successful writes on retry.

Completion means each task has a clear outcome and the dependency order is actionable, not that every task has become a separate issue or PR.
