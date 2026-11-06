---
type: llm
focus: trace
weight: 1
---

Read ALL of draft.md, including verification, operational notes, references, and collapsed details. Each paragraph must explain its action, result, or evidence in language an engineer unfamiliar with this change can follow on the first reading. Fail if any substantive paragraph relies on a cluster of unexplained evaluation or project-specific terms, abbreviations, or internal symbols instead of explaining what happens. A good opening, Chinese translation, glossary elsewhere, or moving jargon into details does not rescue a dense body. Necessary precise names may remain when their purpose is locally understandable; ordinary Git/PR terminology alone is not a failure. Quote the hardest passage and explain what the reader must decode or why it is understandable. Do not pass merely because the text is accurate or mentions all required topics.
