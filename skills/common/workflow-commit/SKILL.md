---
name: workflow-commit
description: Use when the user requests a commit or organized commits, or an authorized shipping workflow requires commits; provide wording only when asked solely for a suggested message.
---

# workflow-commit

Create scoped, verified, independently understandable commits while preserving other work in the working tree.

## Commit workflow

1. Read repository commit conventions and recent commit style. Check the current branch, `git status --short`, staged and unstaged diffs, and new files to identify task-owned changes.
2. Split commits by purpose. Each commit should represent an understandable change; stage explicit files or selected hunks. If a file mixes unrelated changes, commit only clearly separable portions.
3. Preserve unrelated staged content and its staging state; use an isolated worktree when needed. If ownership is unclear, identify the specific files and diffs before asking. Do not clear the index, stash, or discard changes unilaterally.
4. Run repository-required checks and verification appropriate to the change, then inspect `git diff --cached --check` and the complete staged diff. Exclude credentials, temporary artifacts, and unrelated files. Stage files before running lint-staged for it to check them.
5. Prefer the user's requested message format, then repository conventions, then the fallback below. Describe the concrete change in the subject; add rationale, behavior, and limitations in the body when useful. Put change history in commits; README files describe current state only.
6. When the user has requested a commit, create it without asking for message approval again. Keep normal hooks enabled; diagnose failures, fix them, and rerun relevant checks. Amend, rebase, and other history rewrites must fit existing authorization and branch circumstances.
7. Read back the commit SHA, content, and file scope. Recheck the working tree and index to confirm other work remains intact. Report the SHA, verification, and any task changes excluded from the commit.

## Delivery integration

A commit-only request ends with the local commit. Continue to push, PR, or shipping steps when separately authorized; use [workflow-create-pr](../workflow-create-pr/SKILL.md) to create or update a PR. If there are no task changes, report the state instead of creating an empty commit.

## Fallback format

Use [default-commit.txt](templates/default-commit.txt). Follow the Conventional Commits shape, writing prose in Traditional Chinese by default and preserving technical names:

- Use `type(scope): concrete change` for the subject; scope is optional.
- Choose feat, fix, refactor, docs, test, or chore according to the main change; do not misclassify it to exaggerate impact.
- A small change needs only a subject. Keep rationale, changes, verification, and references in the body as needed; remove unused fields and replace every placeholder.
- Report only checks actually performed. Include issue references only when known; do not invent numbers or links.
- The template instructions are in English. Render its labels and explanatory prose in Traditional Chinese unless the user or repository specifies another language.
