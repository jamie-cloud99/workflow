---
name: bdd
description: Clarifies acceptance behavior with concrete Given/When/Then examples. Use when business behavior is ambiguous or BDD and example-based specification are requested.
---

# bdd

Use to resolve ambiguous business behavior with stakeholders, not to impose a new test framework on every task.

- Carry forward confirmed requirements. Identify the rule, concrete examples, meaningful counterexamples, and unresolved questions; do not restart an already settled interview.
- Express context, action, and observable outcome in domain language. Given/When/Then is useful when it clarifies the example; avoid implementation details and long click scripts.
- Separate agreed behavior from assumptions. Ask about unresolved policy instead of treating generated examples as stakeholder approval.
- When implementation is authorized, connect agreed examples to appropriate tests using the existing stack. Settle the check before the code. When a rule is an invariant (round-trip, idempotency, "must never happen"), a property-based test in the existing stack can add broad input coverage next to concrete examples. Assert structural invariants, round-trips, and boundaries, never a copy of the production formula, and skip it when no real property exists. BDD does not require Cucumber or a browser test for every scenario; use Gherkin when the project benefits from it.
- Finish with agreed examples, remaining questions, and any actual automation evidence. Keep scenarios in the existing specification or test location and avoid duplicate documents.

This complements grill-me for discovery, to-spec for synthesis, and TDD for implementation; it does not make all three mandatory.

Reference when deeper guidance is needed: [Cucumber's BDD guide](https://cucumber.io/docs/bdd/).
