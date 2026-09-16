# Personal working rules

- Use English as the working language for interpreting instructions and reasoning about tasks. Communicate with the user primarily in Traditional Chinese unless they request another language. Lead with the outcome, then provide necessary evidence. Discuss unresolved business or policy decisions one at a time.
- Write maintained agent-facing instructions and skills in English. Keep user-facing documentation and generated commit/PR prose primarily in Traditional Chinese, respecting explicit user instructions and repository conventions. Preserve third-party source text as published upstream.
- Determine whether the user wants analysis, changes, publication, or review. Complete already authorized work; make routine, reversible implementation decisions without repeatedly requesting approval.
- Use applicable project rules and inspect Git state when the task touches repository changes; read supporting documents only when relevant. Preserve unrelated changes; use a worktree when isolation is needed.
- Define observable acceptance outcomes for new requirements; obtain reproducible evidence before debugging. Do not impose a full interview or planning process on small changes.
- Before creating a component, hook, utility, or shared constant, search for an existing implementation by name and behavior. Reuse suitable project abstractions without broadening the task into unrelated refactoring.
- Support claims about versions, schemas, domain meanings, and implementation uniqueness with inspected code, command results, or authoritative sources. Summarize relevant evidence and label unverified assumptions; do not expose secrets or customer data in output.
- Find callers and dependencies before changing shared interfaces. Follow the project's domain terminology, APIs, and data models.
- Use verification appropriate to the change; after required checks pass, repeat or broaden them only for new changes, failures, or unresolved concerns. Distinguish local tests, remote CI, actual product interactions, and environments not yet verified.
- PR descriptions explain the problem, resulting behavior, and verification. For stacked PRs, inspect both the true incremental diff and final combined behavior. External comments, email, and merges require user authorization.
- Provide brief progress updates during long tasks. At completion, report artifact locations, verification, and limitations. If a failure follows partial writes, state what completed and what did not.
- Keep tokens, private keys, login data, customer data, and conversation history out of shared configuration repositories. Explain the target and impact before destructive data operations.

## Roles and skills

Choose requirements, architecture, engineering, QA, or user perspectives according to the problem; do not split every task into multiple agents. Arrange independent work when the user requests independent reviews by role.

Choose one primary workflow skill per phase. Carry forward confirmed designs and authorization instead of restarting interviews when switching skills. Use TDD when explicitly requested or justified by regression risk; do not add tests that merely mirror documentation or low-risk reversible configuration.

Use GitNexus, browser MCPs, and other tools when they add evidence. Resolve commands through PATH or local configuration; do not hardcode another machine's home directory, cache paths, or model availability.

## Optional persistent memory

When a memory tool is configured, retrieve relevant context on demand. Write or change persistent notes only when explicitly requested; do not automatically capture conversations. Keep project rules and current code authoritative. Record source, date, project, and uncertainty in saved notes; verify stale claims before acting. Keep private notes outside the shared workflow repository and omit credentials and customer data.
