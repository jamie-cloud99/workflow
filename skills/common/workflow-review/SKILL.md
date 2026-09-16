---
name: workflow-review
description: Use when reviewing a PR or changes for requirement compliance and regressions.
---

# workflow-review

1. Obtain the exact head/base, requirements, and review scope. For stacked PRs, inspect both the incremental diff and final combined result.
2. Trace behavior through entry points, authorization, state, writes, and consumers. Each finding needs a triggering scenario, impact, and file evidence.
3. Distinguish confirmed defects, risks awaiting verification, and policy choices. Do not report style preferences or transitional intermediate-branch states as final defects.
4. Arrange independent passes when the user requests independent reviews by multiple roles; otherwise choose perspectives based on risk.
5. Explain policy decisions in plain language and resolve one open decision at a time. Keep comments as drafts unless publication is authorized.
