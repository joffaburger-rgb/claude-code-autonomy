#!/usr/bin/env python3
"""PostToolUse hook: append tool call record to ~/.claude/logs/post-tool-use.jsonl"""
import json, os, sys
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.claude/logs/post-tool-use.jsonl")

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        record = {
            "ts": datetime.now().strftime("%Y%m%d-%H%M%S"),
            "tool": data.get("tool_name", "?"),
            "input": data.get("tool_input", {}),
        }
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
