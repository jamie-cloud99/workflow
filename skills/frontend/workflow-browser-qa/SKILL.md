---
name: workflow-browser-qa
description: Use after frontend implementation when browser verification of user flows and presentation is needed.
---

# workflow-browser-qa

1. Confirm the startup command, URL, login method, test data, and tool availability. Do not assume an existing session has sufficient permissions.
2. Use observable actions to verify loading, input, submission, errors, retry, and completion. Inspect console and network evidence when needed.
3. Check keyboard focus, labels, narrow screens, and long text. A screenshot proves only the visible state at that moment, not that data was written correctly.
4. Report environment, actions, results, and uncovered scope. Creating a page or passing tests does not by itself establish acceptance of the actual flow.
