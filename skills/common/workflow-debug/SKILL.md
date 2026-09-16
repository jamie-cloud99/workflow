---
name: workflow-debug
description: Use when investigating errors, failed tests, or unexpected behavior.
---

# workflow-debug

1. Record inputs, actual and expected results, and a minimal reproduction. Verify the premises of the user report first.
2. Trace the data or call chain to the first deviation from expected behavior. Label database, API, and browser evidence with its source environment.
3. Test one causal hypothesis at a time. Rule out configuration or version differences before changing code.
4. After the fix, rerun the original reproduction and adjacent critical paths. Report successful primary writes separately from failed post-processing.
