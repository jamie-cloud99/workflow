---
name: cqrs
description: Design or review command/query model separation when CQRS is requested or already used.
---

# cqrs

Use when read and write responsibilities need distinct models; slow queries alone do not establish that need.

- Identify the concrete benefit over the existing model and limit adoption to the affected area. Preserve simpler CRUD where it fits.
- Keep write authorization and invariants on the command side. Commands may read authoritative state to validate a write; read-side presentation must not become write authority.
- Follow existing handler and controller organization; CQRS does not require one controller per use case. Read models may return purpose-built DTOs without reconstituting aggregates, while still enforcing access rules.
- Choose consistency deliberately. CQRS can share one database and does not require event sourcing, a broker, separate services, or eventual consistency.
- When projections are asynchronous, define acceptable lag, user-visible stale states, duplicate handling, ordering, recovery, and rebuilding as relevant to the task.
- Finish with clear read/write ownership, consistency expectations, and verification of affected behavior. Explain additional operational cost before extending the architecture.

Reference when evaluating the pattern: [Martin Fowler on CQRS](https://martinfowler.com/bliki/CQRS.html).
