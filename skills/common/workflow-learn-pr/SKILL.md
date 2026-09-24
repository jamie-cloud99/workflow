---
name: workflow-learn-pr
description: Use when walking someone through a PR or diff to teach the underlying concepts, not to review or approve it.
---

# workflow-learn-pr

Read-only. This is teaching, not [workflow-review](../workflow-review/SKILL.md); do not post review comments or findings unless separately authorized.

- Start where explanation density is highest: comments, docblocks, or PR description text that justify a non-obvious choice. That signal marks where a concept is worth extracting, not just the diff order.
- Split each concept in two: the transferable principle first (states independently of this codebase), then how this specific code embodies it. The principle is what should survive to the next unrelated codebase.
- For every design choice, trace the concrete failure: what breaks, who hits it, when, and what the symptom looks like — not a label like "uses fail-closed" left unexplained.
- Distinguish a documented, deliberate trade-off ("this is intentional, not an oversight") from a genuine gap. Engage the former as a trade-off to evaluate, not a defect; reserve scrutiny for choices with no rationale at all.
- Look for the same principle recurring at different call sites or layers (e.g., the same discipline applied at runtime and at compile time) — that repetition indicates a team convention worth naming, not a one-off.
- Verify any external claim (official behavior, "best practice," vendor docs) against the source before asserting it; correct explicitly and visibly if an earlier claim in the same walkthrough was wrong.
- One concept per turn. Stop after each and wait for confirmation before continuing; if the user needs a prerequisite explained, detour into it immediately rather than finishing the current concept first.
