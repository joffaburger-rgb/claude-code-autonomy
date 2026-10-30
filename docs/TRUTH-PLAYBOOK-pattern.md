# The TRUTH / PLAYBOOK / LEARNINGS Pattern

Every project that CC works on gets three files in its root directory. These survive session boundaries and mean CC never starts from scratch.

---

## TRUTH.md — Live project state

The single source of truth for what's built, what's broken, and what's next.

**CC reads this before starting any task on the project.**
**CC updates this after any significant work.**

### What goes in TRUTH.md

- What the project is (one paragraph max)
- Current production/deployment state
- What was built this session / recently
- Known issues and blockers
- Immediate next steps
- Key file locations and commands

### Example structure

```markdown
# ProjectName — TRUTH

## What it is
[One paragraph]

## Production state
deploy: [URL or N/A]
last deploy: [date]
status: [working / broken / in progress]

## Built
- [Feature/fix] — [date]
- [Feature/fix] — [date]

## Broken / Blocked
- [Issue] — blocked on: [what's needed]

## Next
1. [Immediate next step]
2. [Step after that]

## Key paths & commands
config: path/to/config
deploy: [command]
test: [command]
```

---

## LEARNINGS.md — Error log and confirmed patterns

A running log of what went wrong, why, and what the fix was. Also logs confirmed working approaches that aren't obvious.

**CC updates this in the same response as the task — never later.**

### What goes in LEARNINGS.md

- Errors hit, root cause, fix applied
- Things that failed and why (don't delete — future you will hit the same thing)
- Confirmed working patterns (e.g. "this deploy sequence works, don't change it")
- Non-obvious gotchas specific to this project

### Example entry

```markdown
## 2026-10-28 — Docker worker crash on scraper

Error: context deadline exceeded after 21:48 UTC
Root cause: worker process died, container kept running with 0 workers
Fix: docker restart gmaps-scraper
Prevention: monitor container health, not just port availability
```

---

## PLAYBOOK.md — Verified step-by-step for repeatable workflows

When a workflow first reaches "verified working", write it down. Prevents reinventing the wheel every session.

**Write this the first time a workflow works end-to-end. Never after a failed attempt.**

### What goes in PLAYBOOK.md

- Pre-flight checklist (what must be true before starting)
- Step-by-step commands in order
- What success looks like at each step
- Known failure modes and recovery
- Tool stack and file locations

### Example structure

```markdown
# Email Send Workflow — PLAYBOOK

## Tool stack
- pm-send.py — Gmail sender, 5 accounts, 100/day limit
- suppress-list.txt — dedup list, append after each send

## Pre-flight
- [ ] contacts TSV exists with correct columns
- [ ] email template .md exists and approved
- [ ] suppress-list.txt up to date
- [ ] Not using run_in_background (golden rule)

## Steps
1. Score contacts: python3 score-contacts.py --input raw.tsv --output scored.tsv
2. Dry run: python3 pm-send.py --contacts scored.tsv --email email.md --dry-run
3. Review dry run output — check email count, check first few addresses
4. Live send: python3 pm-send.py --contacts scored.tsv --email email.md --live --log send-log.txt
5. Verify: tail send-log.txt — check for FAILED lines

## GOLDEN RULE
Run pm-send.py foreground direct. Never: run_in_background, fork agents, wrapper scripts.
Session poisoning: once classifier blocks a send attempt, whole session is poisoned. Start fresh.

## Known failure modes
- Classifier blocks: session poisoned — start new session
- Worker crash: docker restart [container]
- Daily limit hit: switch account with --account flag
```

---

## The three-file rule

Every project root: TRUTH.md + LEARNINGS.md + PLAYBOOK.md (once a workflow exists).

If you open a project and these don't exist, create them before the first task.
If you finish a task and TRUTH.md isn't updated, it isn't done.
