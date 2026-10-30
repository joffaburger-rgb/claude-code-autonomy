#!/usr/bin/env python3
"""SubAgentStop hook: append sub-agent completion record to ~/.claude/logs/subagent-stop.jsonl."""
import json, os, sys
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.claude/logs/subagent-stop.jsonl")

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        record = {
            "ts": datetime.now().isoformat(),
            "session_id": data.get("session_id", ""),
            "agent_id": data.get("agent_id", ""),
            "stop_reason": data.get("stop_reason", ""),
            "tool_uses": data.get("num_tool_uses", 0),
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
