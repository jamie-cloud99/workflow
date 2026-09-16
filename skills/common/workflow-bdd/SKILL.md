---
name: workflow-bdd
description: Clarify acceptance behavior with concrete examples when BDD or example-based specification is needed.
---

# workflow-bdd

Use to resolve ambiguous business behavior with stakeholders, not to impose a new test framework on every task.

- Carry forward confirmed requirements. Identify the rule, concrete examples, meaningful counterexamples, and unresolved questions; do not restart an already settled interview.
- Express context, action, and observable outcome in domain language. Given/When/Then is useful when it clarifies the example; avoid implementation details and long click scripts.
- Separate agreed behavior from assumptions. Ask about unresolved policy instead of treating generated examples as stakeholder approval.
- When implementation is authorized, connect agreed examples to appropriate tests using the existing stack. BDD does not require Cucumber or a browser test for every scenario; use Gherkin when the project benefits from it.
- Finish with agreed examples, remaining questions, and any actual automation evidence. Keep scenarios in the existing specification or test location and avoid duplicate documents.

This complements grill-me for discovery, to-spec for synthesis, and TDD for implementation; it does not make all three mandatory.

Reference when deeper guidance is needed: [Cucumber's BDD guide](https://cucumber.io/docs/bdd/).
