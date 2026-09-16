---
name: workflow-hexagonal
description: Design or review ports and adapters when isolating application logic from external dependencies.
---

# workflow-hexagonal

Use when a real dependency boundary needs isolation or the project already uses hexagonal architecture. Do not introduce layers solely to match a diagram.

- Identify the use case and its external interactions. Let application needs define ports; keep transport and storage details in adapters.
- Keep the core independent of concrete adapters. Place wiring at the application's composition boundary and follow the project's existing layout.
- Introduce abstractions where they express an actual boundary, not an interface for every class. DDD, CQRS, and microservices are separate choices.
- Preserve transaction, error, and authorization semantics across adapters. In-memory adapters can test core decisions; real adapter tests establish database and integration behavior.
- Finish with the affected ports, adapter responsibilities, dependency direction, and evidence that the boundary preserves behavior. Refactor incrementally within scope.

Reference when reasoning about boundaries: [Alistair Cockburn's Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture).
