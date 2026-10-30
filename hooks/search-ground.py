#!/usr/bin/env python3
"""search-ground.py — search protocol grounding hook (UserPromptSubmit).

Injects a one-line search protocol reminder before every LLM turn.
Design principles (learned from Hermes rule-enforcer failures):
  - Context injection ONLY — never blocks, never gates tools
  - Fail-open: any error → exit 0 silently (broken hook must not disrupt work)
  - Kill switch: ~/.claude/hooks/DISABLED sentinel → skip immediately
  - No state tracking — nothing to get stuck
  - SIGTERM → exit 0 (fail-open; this is nudge-only, not a security boundary)
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
        sys.exit(0)  # stat error → fail-open

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # bad payload → fail-open

    # Inject context — never block
    # Correct CC format: hookSpecificOutput.additionalContext
    try:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "Research protocol: ALWAYS check local context first — "
                    "(1) read relevant memory files, TRUTH.md, PLAYBOOK.md and workspace docs; "
                    "(2) grep/read workspace files in ~/workspace/, ~/vault/, ~/.claude/ for prior research; "
                    "THEN if still needed: (3) run Brave search or WebFetch for current/factual/market questions. "
                    "Never go online for something already saved locally. "
                    "Include at least one source URL when online search was used. "
                    "If search returns nothing useful, say so before any training-data fallback. "
                    "Training data only for syntax, math, stable definitions. "
                    "Memory protocol active: all memory file writes (new or updated) use telegraph notation — "
                    "no prose sentences, drop articles/prepositions, key:value pairs, -> | & symbols. "
                    "Spec: memory/feedback-memory-notation.md. No exceptions. "
                    "Verification protocol: every task must be proven done — "
                    "show proof (command output, file read-back, test result) in the same response. "
                    "Never say done without evidence."
                )
            }
        }))
    except Exception:
        pass  # output error → fail-open (no output = hook skipped)

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)  # top-level catch → always fail-open

