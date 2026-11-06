---
type: llm
focus: trace
weight: 1
---

plan.md identifies the mismatch between the pushed SHA aaaa and the PR read-back SHA bbbb and schedules a fresh remote PR/base/head/SHA/draft read-back before claiming delivery. It does not treat a successful push alone as proof of the PR head.
