---
name: workflow-debug
description: Use when investigating errors, failed tests, or unexpected behavior.
---

# workflow-debug

1. Record inputs, actual and expected results, and a minimal reproduction. Verify the premises of the user report first.
2. Trace the data or call chain to the first deviation from expected behavior. Label database, API, and browser evidence with its source environment.
3. Test one causal hypothesis at a time. Rule out configuration or version differences before changing code.
4. After the fix, rerun the original reproduction and adjacent critical paths. Report successful primary writes separately from failed post-processing.

## Environment-sensitive failures

- For CI-only failures, inspect logs for the failing revision and compare runtime, dependencies, environment, database state, and test concurrency. Seek a minimal reproduction and evidence-backed hypothesis instead of speculative diagnostic pushes. If local reproduction is unavailable, state the limitation and use a bounded diagnostic step within authorization.
- Branch switches do not reset database migrations or exported environment variables. Check relevant state before changing code; redact secrets and do not automatically roll back shared data.
- Identify the owner of an occupied port before taking action. Do not stop unrelated user processes without authorization.
