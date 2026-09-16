---
name: workflow-create-pr
description: Use when the user requests creating or updating a GitHub pull request or completing an authorized ship-PR workflow; use workflow-review for PR reviews.
---

# workflow-create-pr

Deliver authorized changes as a reviewable PR and verify remote content, branch relationships, and actual CI status.

## Preparation and scope

1. Read repository PR conventions and templates. Confirm the task, Git status, head branch, base branch, remote, and GitHub identity. Select the base from user instructions, branch dependencies, or repository conventions. With multiple accounts, use the matching SSH/CLI identity without changing unrelated global settings.
2. Inspect commits and the diff from base to head to confirm delivery scope. Use [workflow-commit](../workflow-commit/SKILL.md) for task changes needing a commit. Inspect existing local commits too, not just working-tree changes.
3. Manage dependent PRs with gh-stack and verify the true incremental diff, each layer's base, and final combined behavior. Follow repository branch conventions for ordinary PRs.
4. Confirm relevant verification is complete. State unfinished work explicitly and choose draft status according to the user's request and readiness. If asked only to draft PR text, stop at the draft text.

## Create or update

5. When the user requests an actual PR, push the task branch to the verified remote as a required delivery step. If the remote has advanced, inspect differences; do not overwrite it with an unconditional force push.
6. Check for an existing open PR for this repository/head. Update it if present; otherwise create one with explicit base and head. Avoid duplicate PRs or modifying someone else's PR.
7. Base the title and description on the final change and use the ELI20 style below. Prefer the user's requested format, then repository conventions and PR templates, then the fallback. Preserve existing template fields while writing their content in ELI20 style.
8. Prefer structured APIs for content. With gh CLI, write complete Markdown to a temporary file and pass it through `gh pr create --body-file` or `gh pr edit --body-file`. Preserve actual newlines and code literals; do not interpolate the PR body into shell commands.

## Delivery verification

9. Read back the PR URL, base, head, head SHA, draft flag, and state. Confirm task content exists remotely. For stacks, also verify dependencies.
10. Wait for CI on that head SHA to reach a terminal state. You may use `gh pr checks --watch`; confirm the reported checks match the current head. Fix failures within authorized scope and verify again. Report cancellations, absent checks, external approval requirements, and service failures accurately. Provide brief progress updates while waiting.
11. Report the PR link, SHA, verification, and CI results. CI, review approval, merge, deployment, and user acceptance are separate states. Merging and additional external comments require corresponding authorization.

## ELI20 style

Write for an engineer with basic software knowledge who did not participate in this change. Explain why it is needed, what happens afterward, and the evidence that it works.

- Lead with a concrete scenario and its impact, then describe the change. For example: double-clicking Markdown fails because the script lacks execute permission; the installer now sets that permission so documents open successfully.
- Explain cause and effect in plain language. Briefly explain necessary terms on first use. Preserve exact APIs, fields, commands, and error text. Avoid childish analogies and lists consisting only of filenames or implementation terms.
- Include technical detail needed to assess correctness and risk. Explain consequential tradeoffs; scale length to the change.
- Distinguish local verification, CI, and unverified items. Do not present examples, expected outcomes, or planned tests as completed evidence.
- Describe the delivered result, not conversation history, development chronology, or abandoned approaches.

## Fallback format

Use [default-pr.md](templates/default-pr.md). Default the title to `type(scope): concrete improvement in one sentence`, with optional scope. Write prose in Traditional Chinese and preserve technical names.

The template instructions are in English. Render its headings, labels, and explanatory prose in Traditional Chinese unless the user or repository specifies another language. Replace placeholders with real content. Small changes may use short paragraphs but must still explain the problem, resulting behavior, and verification. Keep impact, deployment instructions, and references only when relevant; never invent content to fill the template.
