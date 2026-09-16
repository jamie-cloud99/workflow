# Backend project rules template

Apply this document to an explicitly selected backend repository. Let the project supply its database versions, architecture, and policies.

- Inspect existing entry points, services, data access, and tests before editing. Support table names, columns, APIs, and state transitions with code or actual data evidence.
- Contracts cover successful outcomes, rejection reasons, authorization, error codes, and retry semantics. Verify consumer-affecting changes together with schemas/OpenAPI and consumers.
- Define strategies for write races, atomicity, lock ordering, and rollback. Application-level check-then-write logic is not a database guarantee.
- Generate migrations with the project's official command; preserve the identity of applied migrations. For large DDL, assess data volume, metadata locks, deployment order, and recovery.
- Use compatible database versions for integration checks and confirm tests execute rather than skip. In-memory mocks do not establish real transaction or locking behavior.
- Follow project domain contracts for money, dates, NULL, and time zones; do not invent business rules.
- Report primary writes, post-processing, and failures separately for batch jobs. Reject operations when permission checks fail; do not continue presenting fabricated data.
