---
name: workflow-eval
description: Evaluates and compares skill, agent, or review outputs and shows them in a review page. Use when asked to eval, benchmark, compare with/without a skill, or grade agent output.
---

# workflow-eval

Always finish an evaluation with the review page. Without it the user can only read your summary, not check your grading.

1. Lay out runs as `<workspace>/iteration-N/<case>/{with_skill,without_skill}/` with `outputs/`, `grading.json` (fields `text`, `passed`, `evidence`), and `timing.json`; put the prompt and assertions in `<case>/eval_metadata.json`. The skill-creator skill describes these formats and the baseline rules.
2. Grade each assertion against the actual outputs and cite evidence. Say plainly when you wrote the skill you are grading, and flag assertions both configurations pass, since they show nothing about the skill.
3. Run `scripts/eval-review.sh <iteration-dir> <name>`. It aggregates the benchmark, writes a standalone HTML page, and opens it.

Report the pass rates and the failures you are least sure of; the page carries the rest.
