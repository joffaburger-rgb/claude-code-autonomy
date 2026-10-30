#!/usr/bin/env python3
"""search-ground.py — search protocol grounding hook (UserPromptSubmit).

Injects a one-line search protocol reminder before every LLM turn.
Design principles:
  - Context injection ONLY — never blocks, never gates tools
  - Fail-open: any error -> exit 0 silently (broken hook must not disrupt work)
  - Kill switch: ~/.claude/hooks/DISABLED sentinel -> skip immediately
  - No state tracking — nothing to get stuck
  - SIGTERM -> exit 0 (fail-open; this is nudge-only, not a security boundary)

Customise the additionalContext string to match your own research protocol.
"""
import json
import os
import sys

DISABLED_SENTINEL = os.path.expanduser("~/.claude/hooks/DISABLED")

def main() -> None:
    # Kill switch — check first, before reading stdin
    try:
        if os.path.exists(DISABLED_SENTINEL):
            sys.exit(0)
    except Exception:
        sys.exit(0)  # stat error -> fail-open

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # bad payload -> fail-open

    # Only fire on user prompt turns
    try:
        if payload.get("hook_event_name") != "UserPromptSubmit":
            sys.exit(0)
    except Exception:
        sys.exit(0)

    # Inject context — never block
    try:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "Research protocol: ALWAYS check local context first — "
                    "(1) read relevant memory files, TRUTH.md, PLAYBOOK.md and workspace docs; "
                    "(2) grep/read workspace files for prior research; "
                    "THEN if still needed: (3) run web search for current/factual/market questions. "
                    "Never go online for something already saved locally. "
                    "Include at least one source URL when online search was used. "
                    "If search returns nothing useful, say so before any training-data fallback. "
                    "Training data only for syntax, math, stable definitions."
                )
            }
        }))
    except Exception:
        pass  # output error -> fail-open

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # top-level catch -> always fail-open
