---
name: workflow-delivery
description: Runs requirements through implementation, verification, commit, and PR. Use when requirements are clear and changes need delivery or handoff; not for simple questions.
---

# workflow-delivery

For an explicitly requested prototype or unresolved behavior best explored interactively, use [workflow-prototype](../workflow-prototype/SKILL.md). Confirmed requirements do not need a prototype stage.

1. Derive observable acceptance outcomes from what the user has already confirmed. Ask only for missing decisions that change behavior.
2. Check repository rules, the working tree, and the target branch; preserve other work. Before coding, map each outcome to an existing test and read its actual assertion; a matching filename or an unrelated green suite is not coverage. For each gap, decide the check that will prove it (a real user flow, an invariant, or old-versus-new comparison for rewrites) and note the mock/real boundary. When proof needs real UI, CLI, or service behavior, use the project's verification or run skill; if none exists, report the gap and offer to create one rather than substituting unit or mock evidence. Then implement independently verifiable scope in dependency order.
3. Investigate verification failures instead of removing checks or weakening conditions to expedite delivery. Add only tests that expose real regressions and could fail for a plausible wrong implementation; do not pad test counts, and let an extra case stand only if the existing tests demonstrably miss it. To prove a new or kept test has value, plant a relevant defect in an isolated copy or pre-change snapshot, see it fail at the intended assertion, then restore and see it pass. Keep the loop fast and deterministic (seeded randomness, frozen clocks, isolated state); quarantine a flaky test and report it rather than retrying until green.
4. Before delivery, check the complete task diff against acceptance outcomes, affected callers, failure paths, and verification evidence. Scale checks to risk; use [workflow-review](../workflow-review/SKILL.md) in author self-review mode when useful. For high-risk or large changes, prefer a fresh-context reviewer that sees only the criteria and the evidence. Re-check the mapping from step 2 against the final diff. Zero tests run, skipped required scenarios, or an unavailable environment is a failure to report, not a pass; never offer mock evidence as proof of real backend, permission, or data behavior. Fix confirmed issues and rerun affected checks.
5. Use [workflow-commit](../workflow-commit/SKILL.md) when a commit is requested, followed by [workflow-create-pr](../workflow-create-pr/SKILL.md) when creating or updating a PR is requested. A ship-PR request connects implementation verification, commit, push, PR, and CI confirmation under existing authorization.
6. Report evidence the reader can check (commands run, failing step, output, screenshots or traces for UI) rather than asking them to re-read the diff. Keep raw runs, traces, and transcripts in ignored local paths or CI artifacts; commit only runnable tests and stable docs unless the user asks to version specific evidence. At delivery, distinguish code changes, local verification, remote CI, and actual user-interaction evidence. Complete authorized steps before reporting; clearly identify unfinished work.

## Handoff and resumption

Use [handoff.md](templates/handoff.md) when a handoff is requested or work must continue in another session. Update the existing task document's current state, or provide the handoff in conversation if none exists; do not create a history log. Use Traditional Chinese by default and omit irrelevant fields and secrets.

On resumption, verify the actual workspace, Git state, and relevant remote state. Prior results apply only to their recorded revision and environment. Preserve settled decisions and authorization without expanding their scope. Do not use a handoff to stop work that can still be completed.
