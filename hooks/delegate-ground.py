#!/usr/bin/env python3
"""delegate-ground.py — delegation protocol grounding hook (UserPromptSubmit).

Injects delegation reminder before every turn. Same design as search-ground.py:
  - Context injection ONLY — never blocks
  - Fail-open: any error → exit 0 silently
  - Kill switch: ~/.claude/hooks/DISABLED sentinel → skip
"""
import json
import os
import sys

DISABLED_SENTINEL = os.path.expanduser("~/.claude/hooks/DISABLED")

def main() -> None:
    try:
        if os.path.exists(DISABLED_SENTINEL):
            sys.exit(0)
    except Exception:
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "Delegation protocol (HARDEST RULE — no exceptions): "
                    "ANY task estimated >30s → fork BEFORE starting. "
                    "Two options: Agent(subagent_type:'fork') for code/reasoning; "
                    "Hermes (delegate-hermes skill) for mechanical tasks (scraping, CSV, file processing, long polls, email sends, dashboard rebuilds). "
                    "Main thread stays conversational while fork works in background. "
                    "Summarise result on return — never dump raw output. "
                    "Inline only: single Bash reads, quick searches, single file edits, direct answers under 30s."
                )
            }
        }))
    except Exception:
        pass

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
