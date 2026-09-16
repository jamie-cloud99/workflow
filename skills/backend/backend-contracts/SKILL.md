---
name: backend-contracts
description: Use when changing APIs, authorization, state transitions, or transactional writes.
---

# backend-contracts

1. Read entry points, authorization, services, and consumers; list success and rejection contracts.
2. Verify authorization separately from visibility. Presentation-only state must not determine write permissions.
3. Define outcomes for retries, duplicate submissions, and concurrent updates. Enforce relationships requiring atomicity through database guarantees.
4. Update OpenAPI/schemas and consumer verification. Confirm real database integration tests execute rather than skip.
