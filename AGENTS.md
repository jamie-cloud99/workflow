# Repository conventions

- Write agent-facing instructions, local skills, and their supporting guidance in English. Use English as the working language for interpreting instructions and reasoning about tasks; communicate with the user primarily in Traditional Chinese unless they request another language.
- Keep user-facing README and operating documentation in Traditional Chinese by default. Generated commit and PR prose also defaults to Traditional Chinese, subject to explicit user instructions and repository conventions.
- Every README describes only currently available functionality, configuration, and operations, consistent with the implementation.
- Use Git commits for change history and rationale. Do not add before/after timelines, migration histories, or completion logs to README files or create separate history documents.
- Documentation describes current design, operations, and verification, including the current guidance users need to update and restore their setup.
- Preserve third-party skills in their upstream language; do not translate or fork downloaded sources as part of synchronization.
