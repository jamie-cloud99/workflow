---
name: frontend-contracts
description: Verifies frontend API schemas, permission presentation, forms, and URL state against the real backend contract. Use when changing any of these.
---

# frontend-contracts

1. List fields actually used by the UI and the meanings of empty values, errors, permissions, and states. Compare them with the real backend contract.
2. Strictly validate fields affecting presentation, authorization, and calculations. Ignore unused fields and avoid coupling schemas across endpoints.
3. Handle stale tabs, duplicate submissions, back navigation, and URL reloads. Do not render normal actions when permission or role data is invalid.
4. At real entry points, verify success, rejection, retry after failure, and data refresh. Clearly separate mock checks from integration verification.
