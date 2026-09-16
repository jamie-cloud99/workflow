---
name: workflow-review
description: Use for author self-review, reviewing another person's changes, or addressing PR review feedback.
---

# workflow-review

Choose the mode from the user's request; do not infer it solely from the PR author account.

| Mode | Action | Boundary |
| --- | --- | --- |
| Author self-review | Check the complete task diff against acceptance outcomes; fix confirmed issues and rerun relevant checks. | Continue within the authorized implementation scope. Self-review is not independent approval. |
| Act as a reviewer | Inspect the exact head/base and report findings with severity, triggering scenario, impact, and file/line evidence. | Read-only unless fixes are requested. Publish a review or approval only when authorized. |
| Address feedback | Read current feedback, verify each claim, then fix confirmed issues or explain disagreement with evidence. | Commit, push, reply, and resolve threads only within corresponding authorization. |

- Trace affected callers, authorization, state transitions, and failure paths as relevant. For stacks, inspect both the incremental diff and final combined behavior.
- Distinguish confirmed defects, unverified risks, and policy choices. Discuss unresolved policy decisions one at a time; do not treat style preferences as defects.
- Arrange independent review passes when requested; do not require separate agents for every review.
- For authorized delivery, use [workflow-commit](../workflow-commit/SKILL.md) and [workflow-create-pr](../workflow-create-pr/SKILL.md). Verify the resulting remote head and CI; read back published replies and resolved thread state.
- Report findings first, then coverage and remaining gaps. Keep fixes, CI, discussion resolution, approval, and merge status distinct; green CI alone does not justify resolving a finding.
