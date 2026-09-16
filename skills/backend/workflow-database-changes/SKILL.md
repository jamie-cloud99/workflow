---
name: workflow-database-changes
description: Use when creating migrations, backfilling data, synchronizing batches, or investigating database locks.
---

# workflow-database-changes

1. Confirm the target environment, version, table names, data volume, and recovery method. Names found in documentation are not verified schema evidence.
2. Use the project migration generator; preserve the identity of shared or applied migration files.
3. Assess metadata locks, long transactions, indexes, and deployment order. Before terminating connections or making destructive writes, verify the target and obtain authorization.
4. For backfills and synchronization, record actual writes and post-processing results for each scope. A final API failure does not imply that all writes rolled back.
5. Use a compatible real database to verify important NULL, precision, atomicity, and race behavior. Mocks cannot substitute for locking evidence.
