# MEMORY.md

Index of all memory files. Loaded into every session via the SessionStart hook.
Each line links to a memory file and gives a one-line hook — enough to decide if it's relevant.

Keep under 200 lines. Entries after line 200 are truncated and never loaded.
Never write memory content directly here — this is an index only.

---

**READ FIRST:** [CORE.md](CORE.md) — session primer: identity, active projects, system state, open tasks

## User

- [User profile](user-profile.md) — who the user is, role, devices, location, goals

## Feedback

- [Global learnings](learnings-global.md) — cross-project errors, patterns, confirmed working approaches

## Tools & Setup

- [CC setup](tools-cc-setup.md) — MCP servers, hooks installed, routing guide, installed paths

## Projects

<!-- Add one line per active project -->
<!-- - [Project name](project-name.md) — one-line state summary -->

## How to write memory files

Each file uses this frontmatter:

```
---
name: short-kebab-slug
description: one-line summary (used to judge relevance)
metadata:
  type: user | feedback | project | reference
  updated: YYYY-MM-DD
---

[content in telegraph notation — no prose, key:value pairs, -> | & symbols]
```

Use telegraph notation in all memory files:
- No full sentences — drop articles and prepositions
- Key:value pairs for facts
- `->` for causes/results, `|` for alternatives, `&` for combinations
- Link related files with [[their-name]]
