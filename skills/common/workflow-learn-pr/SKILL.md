---
name: workflow-learn-pr
description: Use when walking someone through a PR or diff concept-by-concept to build understanding — a slower, teaching-first variant of reviewing that still surfaces real findings.
---

# workflow-learn-pr

A concept-first mode of [workflow-review](../workflow-review/SKILL.md)'s "act as a reviewer" path: reading is deeper and paced for understanding, not just for finding defects, but a genuine problem spotted along the way is still a finding — raise it as one, with the same file/line evidence and authorization boundary as workflow-review (read-only unless posting is authorized).

- Start where explanation density is highest: comments, docblocks, or PR description text that justify a non-obvious choice. That signal marks where a concept is worth extracting, not just the diff order.
- Split each concept in two: the transferable principle first (states independently of this codebase), then how this specific code embodies it. The principle is what should survive to the next unrelated codebase.
- For every design choice, trace the concrete failure: what breaks, who hits it, when, and what the symptom looks like — not a label like "uses fail-closed" left unexplained. This is also how a real defect surfaces here: tracing the concrete failure of a choice that turns out to have no good justification.
- Distinguish a documented, deliberate trade-off ("this is intentional, not an oversight") from a genuine gap. Engage the former as a trade-off to evaluate, not a defect; when scrutiny turns up a choice with no rationale and a real failure scenario, treat it as a finding, not a teaching aside — draft it and confirm before posting.
- Look for the same principle recurring at different call sites or layers (e.g., the same discipline applied at runtime and at compile time) — that repetition indicates a team convention worth naming, not a one-off. It also surfaces the same defect duplicated at every site it recurs.
- Verify any external claim (official behavior, "best practice," vendor docs) against the source before asserting it; correct explicitly and visibly if an earlier claim in the same walkthrough was wrong.
- One concept per turn. Stop after each and wait for confirmation before continuing; if the user needs a prerequisite explained, detour into it immediately rather than finishing the current concept first.
