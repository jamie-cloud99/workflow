# Grader calibration

`rejected-description.md` is the actual PR #3 body the user rejected as insufficiently plain. Keep it outside `files/` so generation runs do not see the negative control.

Before trusting these graders, score that unchanged description as `draft.md` with the same grader files in an isolated calibration run. The first two graders must fail: its opening lists technical concepts without a concrete scenario, and its change summary lists evaluation machinery without explaining the simulated task comparison. The accuracy grader may pass. A grader that passes the rejected opening needs correction before its generation scores are used as evidence. Also inspect a generated revision for factual accuracy; a negative control alone does not prove good writing will pass.

Run the generation case with and without `workflow-create-pr` available. Report whether the skill was actually invoked. Keep the prompt, raw notes, model, and tools equal. A shared pass is contract coverage, not evidence of an incremental skill benefit. The author of this case also wrote the rejected PR; disclose that evaluation bias.
