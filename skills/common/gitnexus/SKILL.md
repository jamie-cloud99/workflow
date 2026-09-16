---
name: gitnexus
description: Use GitNexus to index a repository or inspect symbol relationships and change impact.
---

# gitnexus

Use when graph evidence helps the task. For a small local edit, direct source search may be sufficient.

- Resolve the intended repository and check index freshness with `gitnexus status` or the available MCP context. Use the installed CLI and its `--help`; tool names and supported arguments come from the active MCP schema.
- Use query/context to locate relevant flows and callers, impact for dependency reach, and change detection against the actual base for a review. Do not assume `main` for stacked branches. Graph reach is a candidate impact set, not proof that callers break.
- Verify conclusions against source and focused checks. If GitNexus is missing or stale, use direct search rather than presenting old graph results as current evidence.
- Run `gitnexus analyze` from the intended repository when indexing is needed and within task scope. Inspect Git state before and after: indexing can generate agent instructions and skills. Preserve existing project guidance and unrelated edits; follow the project's policy for generated files.
- Keep index cleanup, wiki generation, and external publication separate from read-only exploration. Do not clean all repositories or publish artifacts as a troubleshooting shortcut.

This supports [workflow-debug](../workflow-debug/SKILL.md), [workflow-review](../workflow-review/SKILL.md), and delivery; it does not replace their scope or authorization rules.
