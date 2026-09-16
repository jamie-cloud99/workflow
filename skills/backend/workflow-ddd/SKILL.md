---
name: workflow-ddd
description: Design or review domain models, bounded contexts, and aggregate invariants when DDD is requested or already used.
---

# workflow-ddd

Use for a domain-modeling problem, not as a default architecture for ordinary CRUD.

- Consult relevant existing modules and architecture checks before proposing structure. Reconcile documentation with code and tests; do not copy legacy exceptions into new work.
- Start from the project's business language, concrete use cases, and disputed rules. Preserve established definitions; surface unknown policy rather than inventing it.
- Bound contexts by model meaning and ownership, not tables or deployment units. A bounded context does not automatically require a microservice.
- Choose entities, value objects, and aggregates around identity and consistency needs. State which invariants must hold atomically and how cross-boundary changes are coordinated.
- Preserve persistence and transaction guarantees during refactoring. A domain event is not automatically an integration event or a reason to add a broker.
- Finish with the relevant model, invariants, boundaries, and tradeoffs, or a scoped implementation when requested. Do not generate every DDD building block or impose a repository-wide redesign.

Reference when deeper modeling guidance is needed: [Eric Evans's DDD Reference](https://www.domainlanguage.com/ddd/reference/).
