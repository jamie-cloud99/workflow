---
name: workflow-review
description: Handles author self-review, reviewing another person's changes, and addressing PR review feedback. Use when the user asks to review code, a PR, or respond to review comments.
---

# workflow-review

Choose the mode from the user's request; do not infer it solely from the PR author account.

| Mode | Action | Boundary |
| --- | --- | --- |
| Author self-review | Check the complete task diff against acceptance outcomes; fix confirmed issues and rerun relevant checks. | Continue within the authorized implementation scope. Self-review is not independent approval. |
| Act as a reviewer | Inspect the exact head/base and report findings with severity, triggering scenario, impact, and file/line evidence. | Read-only unless fixes are requested. Publish a review or approval only when authorized. |
| Address feedback | Read current feedback, verify each claim, then fix confirmed issues or explain disagreement with evidence. | Commit, push, reply, and resolve threads only within corresponding authorization. |

- State the PR number, title, and author before reviewing, and review only the PR named. Treat a newly added TODO/FIXME/"verify" in the diff, docs included, as blocking.
- For a thorough or independent review of a non-trivial diff, run read-only subagents in parallel, one concern each (architecture, deploy/ops safety, data robustness, test gaps), then re-read the cited code yourself and drop what you cannot verify. A small diff may be reviewed in one pass; say so.
- Fetch formal reviews (`gh api repos/{owner}/{repo}/pulls/N/reviews`) as well as inline and issue comments; the Critical items often appear only there.
- Write every review comment and reply in ELI20 style, as [workflow-create-pr](../workflow-create-pr/SKILL.md) does for PR bodies: the concrete problem, the triggering scenario, the impact, and the evidence, for an engineer unfamiliar with the change. Traditional Chinese by default.
- Reply once per PR, mapping every item to its commit, without conflict-resolution details, and request re-review. Stop after 3 failed CI iterations and report.
- Trace affected callers, authorization, state transitions, and failure paths as relevant. For stacks, inspect both the incremental diff and final combined behavior.
- Distinguish confirmed defects, unverified risks, and policy choices. Discuss unresolved policy decisions one at a time; do not treat style preferences as defects.
- Arrange independent review passes when requested; do not require separate agents for every review.
- For authorized delivery, use [workflow-commit](../workflow-commit/SKILL.md) and [workflow-create-pr](../workflow-create-pr/SKILL.md). Verify the resulting remote head and CI; read back published replies and resolved thread state.
- Report findings first, then coverage and remaining gaps. Keep fixes, CI, discussion resolution, approval, and merge status distinct; green CI alone does not justify resolving a finding.

Use open-code-review-delegate when explicit file coverage or file-specific rule matching would help. It requires the optional `ocr` CLI; check availability before invoking it and keep the review moving with normal tools if unavailable. Preserve the actual base/head (including stack ancestry), account for excluded or skipped files, and validate findings against requirements. Delegation uses the current agent, not an independent reviewer; it does not authorize fixes or publication beyond the selected mode.

## Test quality when relevant

Check whether changed tests can fail for the regression they claim to cover and can tell a correct implementation from a plausible wrong one (for rewrites, whether old and new behavior is compared on the same inputs, with intentional differences listed), whether mocks bypass the behavior under review, and whether important failure paths remain exercised. Inspect deleted/skipped tests and changed expected values against requirements; passing output alone is not the oracle. Text assertions and mocks can be valid when they express the actual contract. Treat zero executed tests, skipped required scenarios, and mock-only evidence offered for real-backend behavior as unverified. Report demonstrated gaps with a concrete missed scenario, not blanket demands for more tests; fixes follow the selected review mode.
