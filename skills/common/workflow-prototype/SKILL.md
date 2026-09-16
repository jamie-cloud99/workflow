---
name: workflow-prototype
description: Build a prototype or POC to resolve uncertain interaction, workflow, or state-model requirements.
---

# workflow-prototype

Use a prototype to answer a concrete unresolved question, not as a mandatory step for confirmed features or bug fixes.

- Carry forward settled requirements. Use grill-me if the question itself needs clarification; otherwise choose the smallest useful UI or logic prototype. Reuse existing product patterns and choose variants only when comparison helps the decision.
- Build a reviewable slice with a clear run command or preview URL and visible outcomes. Continue through running it and fixing obstacles to review; pause for user input when the next step depends on an unresolved product decision, not after every small edit.
- Clearly mark prototype-only behavior and mock data. Default to isolated mock or in-memory state; real persistence must be part of the authorized question. Do not connect exploratory UI to real destructive operations.
- Verify the behavior needed to answer the question. Add tests when they materially support that evidence; do not freeze speculative behavior or remove existing tests merely because the work is a prototype.
- Finish with a usable review path, observed results, confirmed requirements, open questions, and reuse/rewrite boundaries. Keep this concise in the existing task document or conversation; do not prescribe a new document for every prototype. User confirmation is distinct from a working demo.

Once the direction is confirmed, use to-spec when a written specification is useful, then [workflow-delivery](../workflow-delivery/SKILL.md) for authorized implementation. Reassess architecture, API contracts, permissions, data handling, and tests; prototype code and mock behavior are not production contracts or automatic approval to ship.
