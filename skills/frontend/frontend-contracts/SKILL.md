---
name: frontend-contracts
description: Use when changing frontend API schemas, permission presentation, forms, or URL state.
---

# frontend-contracts

1. List fields actually used by the UI and the meanings of empty values, errors, permissions, and states. Compare them with the real backend contract.
2. Strictly validate fields affecting presentation, authorization, and calculations. Ignore unused fields and avoid coupling schemas across endpoints.
3. Handle stale tabs, duplicate submissions, back navigation, and URL reloads. Do not render normal actions when permission or role data is invalid.
4. At real entry points, verify success, rejection, retry after failure, and data refresh. Clearly separate mock checks from integration verification.
