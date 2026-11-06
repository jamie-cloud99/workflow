---
type: llm
focus: trace
weight: 1
---

Evaluate draft.md, not the agent's assurances about it. Before implementation details or evaluation jargon, its opening explains who asks an agent to ship a PR and one concrete failure with its consequence, such as including another person's staged edits or reporting old code's successful CI as success for new code. A generic claim about testing "authorization, staging, SHA, CI" fails even if all those topics appear later. The reader must be able to picture the mistake without knowing the evaluation framework.
